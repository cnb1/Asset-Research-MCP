"""News-grounded answer logic.

Pure business logic — knows nothing about MCP. Calls OpenAI's Responses API
with the built-in web_search tool and returns a sourced answer. Imported by
server.py.
"""

from openai import OpenAI

# web_search is a built-in Responses API tool; gpt-4o supports it.
# Bump to a newer model (e.g. "gpt-5.1") if you want more search rounds.
MODEL = "gpt-4o"

ANALYST_PREAMBLE = (
    "You are a markets news analyst. Use web search to pull the most recent, "
    "relevant news for the given asset (prefer the last 24-72 hours), then "
    "answer the question using only what you find. Lead with the direct answer, "
    "then supporting context. Be specific about dates and figures, and flag "
    "rumor vs. confirmed. You are an analyst, NOT a financial advisor — "
    "describe, don't tell the user to buy, sell, or size a position. Attribute "
    "claims to their sources. If search is too thin to answer confidently, say "
    "so rather than guessing."
)

_client = None


def _get_client() -> OpenAI:
    """Lazily build the OpenAI client (reads OPENAI_API_KEY from env)."""
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


def grounded_answer(asset: str, question: str) -> str:
    """Search-grounded answer for `question` about `asset`, with sources."""
    response = _get_client().responses.create(
        model=MODEL,
        instructions=ANALYST_PREAMBLE,
        input=f"ASSET: {asset}\nQUESTION: {question}",
        tools=[{"type": "web_search"}],
    )
    text = response.output_text or "(no answer produced)"
    sources = _extract_sources(response)
    if sources:
        text += "\n\nSources:\n" + "\n".join(sources)
    return text


def _extract_sources(response) -> list[str]:
    """Pull url_citation annotations out of the response, de-duplicated."""
    out, seen = [], set()
    for item in getattr(response, "output", None) or []:
        for content in getattr(item, "content", None) or []:
            for ann in getattr(content, "annotations", None) or []:
                if getattr(ann, "type", None) == "url_citation":
                    url = getattr(ann, "url", None)
                    if url and url not in seen:
                        seen.add(url)
                        out.append(f"- {ann.title or url}: {url}")
    return out