"""
AI agent using OpenAI tool calling.

Flow per user message:
  1. Build messages (system + history + user)
  2. Call OpenAI with both tools defined
  3. If the model requests tool calls, execute each tool
  4. Feed tool results back and call the model again for a final answer
  5. Return the final text response

Tools:
  search_gender_reports — Pinecone RAG (Tool 1)
  query_lfs_data        — DuckDB on LFS parquet files (Tool 2)
  web_search            — Tavily web search for current info (Tool 3)
"""

import asyncio
import json
from functools import lru_cache
from typing import AsyncIterator

import pandas as pd
import pyarrow.parquet as pq
from openai import AsyncOpenAI, OpenAI

from api.config import CHAT_MODEL, OPENAI_API_KEY, PARQUET, VARIABLES_CSV
from api.tools.data import _run_query
from api.tools.rag import _run_search
from api.tools.search import _run_web_search

_client = OpenAI(api_key=OPENAI_API_KEY)
_async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

_SYSTEM_TEMPLATE = """\
You are a ParityMetrics AI analyst specializing in gender equality data for Rwanda.

You have access to three tools:
1. search_gender_reports — search official reports and policy documents
2. query_lfs_data — query Rwanda Labour Force Survey (LFS) microdata (2022–2024)
3. web_search — search the web for current news, recent events, or broader context

Strategy:
- For EVERY user question, call ALL THREE tools in parallel:
  1. query_lfs_data — write a SQL query relevant to the topic
  2. search_gender_reports — search for related policy or document context
  3. web_search — search the web with a precise, focused query on the topic
- Always state which data source (year, document, or URL) your figures come from.
- Use SUM(weight2) instead of COUNT(*) when computing population estimates from LFS data.
- Always include the source URLs from web_search as references at the end of your answer.

Rwanda Geographic Reference:
PROVINCES (province field):
  1 = Eastern Province
  2 = Kigali City
  3 = Northern Province
  4 = Southern Province
  5 = Western Province

DISTRICTS (code_dis field) - Complete mapping:
Eastern Province (11-13):
  11 = Bugesera
  12 = Gatsibo
  13 = Kayonza

Kigali City (21-28):
  21 = Gasabo
  22 = Kicukiro
  23 = Nyarugenge
  24 = Kirehe
  25 = Ngoma
  26 = Nyagatare
  27 = Rwamagana
  28 = Rwamagana (alternate)

Northern Province (31-37):
  31 = Burera
  32 = Gakenke
  33 = Gicumbi
  34 = Musanze
  35 = Rulindo
  36 = Rulindo (alternate)
  37 = Musanze (alternate)

Southern Province (41-45):
  41 = Gisagara
  42 = Huye
  43 = Kamonyi
  44 = Muhanga
  45 = Nyamagabe

Western Province (51-57):
  51 = Karongi
  52 = Ngororero
  53 = Nyabihu
  54 = Nyamasheke
  55 = Rubavu
  56 = Rusizi
  57 = Rutsiro

IMPORTANT: When displaying results with district codes (code_dis), ALWAYS translate them to district names using this mapping. Present results with district names, not codes, for better readability.

LFS variable reference (columns available in lfs2022 / lfs2023 / lfs2024):
{variable_context}
"""

_TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_gender_reports",
            "description": (
                "Search official Rwanda gender reports, policy documents, and research "
                "publications. Use for policy insights, qualitative context, or citations."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_lfs_data",
            "description": (
                "Execute a SQL SELECT query against Rwanda LFS parquet datasets. "
                "Tables: lfs2022 (70k rows), lfs2023 (72k rows), lfs2024 (103k rows). "
                "Key cols: A01=Sex(1=M,2=F), A04=Age, province(1-5), code_dis=district(11-57), "
                "Code_UR(1=Urban,2=Rural), weight2=survey weight, "
                "status1=labour force status(1=Employed,2=Unemployed,3=Outside), "
                "UR1=unemployment rate, LFPR=participation rate. "
                "Only SELECT allowed. Use SUM(weight2) for population estimates. "
                "District codes (code_dis): Eastern(11-17), Kigali(21-23), Northern(31-35), "
                "Southern(41-48), Western(51-57)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "A valid SQL SELECT statement.",
                    }
                },
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for current information, recent news, or broader context "
                "not available in internal documents or LFS data. Returns results with "
                "source URLs to include as references. Use a precise, focused search query."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A precise search query tailored to find relevant information.",
                    }
                },
                "required": ["query"],
            },
        },
    },
]


@lru_cache(maxsize=1)
def _system_prompt() -> str:
    desc = pd.read_csv(VARIABLES_CSV)
    parquet_cols = set(pq.read_schema(str(next(iter(PARQUET.values())))).names)
    desc = desc[desc["name"].isin(parquet_cols)]
    lines = [f"  {r['name']}: {r['varlab']}" for _, r in desc.iterrows()]
    # Use replace instead of format to avoid issues with braces in the template
    return _SYSTEM_TEMPLATE.replace("{variable_context}", "\n".join(lines))


def _dispatch_tool(name: str, args: dict) -> str:
    if name == "search_gender_reports":
        return _run_search(args["query"])
    if name == "query_lfs_data":
        return _run_query(args["sql"])
    if name == "web_search":
        return _run_web_search(args["query"])
    return f"Unknown tool: {name}"


def run_agent(user_message: str, history: list[dict]) -> str:
    """
    Run the agent for one turn.

    Args:
        user_message: The latest user input.
        history: List of {"role": ..., "content": ...} dicts from prior turns.

    Returns:
        The agent's final text answer.
    """
    messages = [
        {"role": "system", "content": _system_prompt()},
        *history,
        {"role": "user", "content": user_message},
    ]

    # Agentic loop — iterate until model stops calling tools (max 6 rounds)
    for _ in range(6):
        response = _client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            tools=_TOOL_DEFINITIONS,
            tool_choice="auto",
            temperature=0.2,
        )
        msg = response.choices[0].message

        # No tool calls — we have the final answer
        if not msg.tool_calls:
            return msg.content or ""

        # Append assistant message with tool_calls
        messages.append(msg)

        # Execute each tool call and append results
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = _dispatch_tool(tc.function.name, args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                }
            )

    # Fallback: ask for a plain answer after exhausting iterations
    messages.append(
        {"role": "user", "content": "Please summarise your findings in a final answer."}
    )
    final = _client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.2,
    )
    return final.choices[0].message.content or ""


_TOOL_STATUS: dict[str, str] = {
    "search_gender_reports": "Searching gender reports...",
    "query_lfs_data": "Querying LFS dataset...",
    "web_search": "Searching the web...",
}


async def stream_agent(user_message: str, history: list[dict]) -> AsyncIterator[str]:
    """
    Async generator that streams the agent response chunk by chunk.

    Yields two kinds of strings:
    - "STATUS:<message>"  — progress update during tool-calling phase
    - anything else       — a text chunk to append to the assistant bubble

    The bug in the previous version: when the model answered after tool calls
    (the normal 2-step flow), we yielded msg.content all at once and returned,
    never reaching the streaming code.  Fix: always stream the final answer.
    """
    messages = [
        {"role": "system", "content": _system_prompt()},
        *history,
        {"role": "user", "content": user_message},
    ]

    did_tool_calls = False

    # Tool-calling loop — run until the model stops requesting tools
    for _ in range(6):
        response = await _async_client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            tools=_TOOL_DEFINITIONS,
            tool_choice="auto",
            temperature=0.2,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            if not did_tool_calls:
                # Direct answer with no tools needed — yield at once
                yield msg.content or ""
                return
            # After tool calls the model returned an answer without streaming.
            # Discard it and fall through to the streaming block below so the
            # final answer is always streamed rather than sent as one big chunk.
            break

        did_tool_calls = True
        messages.append(msg)

        # Emit a status event for every tool being called
        for tc in msg.tool_calls:
            label = _TOOL_STATUS.get(tc.function.name, f"Using {tc.function.name}...")
            yield f"STATUS:{label}"

        # Execute all tools concurrently
        args_list = [json.loads(tc.function.arguments) for tc in msg.tool_calls]
        results = await asyncio.gather(
            *[
                asyncio.to_thread(_dispatch_tool, tc.function.name, a)
                for tc, a in zip(msg.tool_calls, args_list)
            ]
        )
        for tc, result in zip(msg.tool_calls, results):
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    else:
        # Exhausted all iterations without a clean answer
        messages.append(
            {
                "role": "user",
                "content": "Please summarise your findings in a final answer.",
            }
        )

    # Stream the final text answer
    yield "STATUS:Generating response..."
    stream = await _async_client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.2,
        stream=True,
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content
