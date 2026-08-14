from mcp.server import MCPServer

from grounding import grounded_answer

mcp = MCPServer("asset-news")   # <- this is what's missing

@mcp.tool()
def analyze_asset_news(asset: str, question: str) -> str:
    """Answer a question about a stock or crypto asset using live web news.

    Searches recent news for the asset via Google Search grounding, reasons
    over the results, and returns a sourced answer. Ephemeral — each call
    re-retrieves; nothing is stored.

    Args:
        asset: Ticker or token symbol, e.g. "NVDA" or "HYPE".
        question: What you want to know, e.g. "what's driving the move today?"
    """
    return grounded_answer(asset, question)


@mcp.tool()
def get_asset_headlines(asset: str, hours: int = 48) -> str:
    """Summarize the most notable recent news for an asset.

    Convenience wrapper for the "just tell me the latest" case.

    Args:
        asset: Ticker or token symbol, e.g. "BTC".
        hours: How far back to prioritize, in hours (default 48).
    """
    question = (
        f"Summarize the most notable news from roughly the last {hours} hours. "
        "Give 3-5 bullet headlines, each with a date and source, and note "
        "whether each is confirmed or rumor."
    )
    return grounded_answer(asset, question)

if __name__ == "__main__":
    mcp.run()