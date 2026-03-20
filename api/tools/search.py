"""
Tavily web search tool.

Searches the web for up-to-date information and returns results with references.
"""
from tavily import TavilyClient

from api.config import TAVILY_API_KEY

_client = TavilyClient(api_key=TAVILY_API_KEY)


def _run_web_search(query: str) -> str:
    """
    Execute a Tavily web search and return formatted results with references.

    Args:
        query: The search query.

    Returns:
        Formatted string with search results and source URLs.
    """
    response = _client.search(query)

    results = response.get("results", [])
    if not results:
        return "No web search results found."

    lines = []

    # Include AI-generated answer if present
    if response.get("answer"):
        lines.append(f"Summary: {response['answer']}\n")

    lines.append("Web search results:\n")
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r.get('title', 'No title')}")
        lines.append(f"    URL: {r.get('url', '')}")
        lines.append(f"    {r.get('content', '')}\n")

    output = "\n".join(lines)
    print("\n[WebSearch] Query:", query)
    print("[WebSearch] Result:\n", output)
    return output
