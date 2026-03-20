"""
Terminal RAG chatbot.

Flow per user message:
  1. Embed query  →  text-embedding-3-small (dim=512)
  2. Vector search →  Pinecone "giz" index (top-k chunks)
  3. Build prompt  →  system context + conversation history
  4. LLM response  →  OpenAI gpt-4o-mini

Usage:
    python starter-app/db/chat.py
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv(Path(__file__).parents[1] / ".env")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
INDEX_NAME = "giz"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 512
CHAT_MODEL = "gpt-4o-mini"
TOP_K = 5   # number of Pinecone chunks to retrieve per query

SYSTEM_PROMPT = """\
You are a helpful assistant specialising in gender data and statistics for Rwanda.
You answer questions using the provided context retrieved from official reports.
If the context does not contain enough information to answer, say so clearly.
Always cite the source document and page number when you use information from the context.
"""

# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_KEY"))
index = pc.Index(INDEX_NAME)


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------
def embed_query(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIM,
    )
    return response.data[0].embedding


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """Return top-k chunks from Pinecone with their metadata."""
    vector = embed_query(query)
    result = index.query(vector=vector, top_k=top_k, include_metadata=True)
    return result.matches


def build_context(matches: list[dict]) -> str:
    parts = []
    for m in matches:
        meta = m.metadata
        parts.append(
            f"[Source: {meta.get('source', 'unknown')}, Page {meta.get('page', '?')}]\n"
            f"{meta.get('text', '')}"
        )
    return "\n\n---\n\n".join(parts)


# ---------------------------------------------------------------------------
# Chat loop
# ---------------------------------------------------------------------------
def chat() -> None:
    print("Gender Data Chatbot  (type 'quit' or 'exit' to stop)\n")
    history: list[dict] = []  # running conversation for multi-turn context

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        # 1. Retrieve relevant context
        matches = retrieve(user_input)
        context = build_context(matches)

        # 2. Build messages
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "system",
                "content": f"Relevant context from the knowledge base:\n\n{context}",
            },
            *history,
            {"role": "user", "content": user_input},
        ]

        # 3. Call LLM
        response = openai_client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0.2,
        )
        answer = response.choices[0].message.content

        print(f"\nAssistant: {answer}\n")

        # 4. Update history (keep last 10 turns to avoid token bloat)
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": answer})
        if len(history) > 20:
            history = history[-20:]


if __name__ == "__main__":
    chat()
