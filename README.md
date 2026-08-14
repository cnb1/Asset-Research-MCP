# asset-news MCP server

Standalone MCP server for news-grounded asset analysis.

Fully self-contained — no dependency on any agent. Each tool calls the Gemini
API directly with Google Search grounding, so this server owns its logic. Any
MCP client (an ADK agent, Claude Desktop, your own client) connects to it and
consumes the tools via `tools/list` + `tools/call`.

## Tools

- `analyze_asset_news(asset, question)` — grounded Q&A about a stock or crypto asset
- `get_asset_headlines(asset, hours=48)` — "just the latest" convenience wrapper

## Requirements

- Dependencies: `mcp`, `google-genai`
- Env: `GOOGLE_API_KEY` (from Google AI Studio)

```bash
pip install -r requirements.txt
cp .env.example .env   # then paste your key
```

## Run

Stdio transport (the default):

```bash
python server.py
```

Example Claude Desktop config:

```json
{
  "mcpServers": {
    "asset-news": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

## Notes

- `google_search` grounding requires a **Gemini 2** model (`gemini-2.5-flash`).
- Source URLs are pulled from `grounding_metadata.grounding_chunks[].web`, whose
  shape has shifted across google-genai versions — if the Sources block comes
  back empty, check there first. Answers are unaffected.