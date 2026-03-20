"""
Tool 1 — Pinecone RAG search.

Exposes _run_search() as the raw callable (used by the agent dispatcher)
and search_gender_reports as the OpenAI tool definition wrapper (for future
LangChain / LangGraph integrations if needed).
"""
from openai import OpenAI
from pinecone import Pinecone

from api.config import (
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    OPENAI_API_KEY,
    PINECONE_INDEX,
    PINECONE_KEY,
    TOP_K,
)

_openai = OpenAI(api_key=OPENAI_API_KEY)
_index = Pinecone(api_key=PINECONE_KEY).Index(PINECONE_INDEX)


def _run_search(query: str) -> str:
    """Search Pinecone for relevant gender report chunks."""
    vector = _openai.embeddings.create(
        input=[query],
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIM,
    ).data[0].embedding

    matches = _index.query(vector=vector, top_k=TOP_K, include_metadata=True).matches

    if not matches:
        return "No relevant documents found."

    parts = []
    for m in matches:
        meta = m.metadata
        parts.append(
            f"[Source: {meta.get('source', 'unknown')}, "
            f"Page {meta.get('page', '?')}]\n"
            f"{meta.get('text', '').strip()}"
        )
    return "\n\n---\n\n".join(parts)
