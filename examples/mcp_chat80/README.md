# Vrel Chat-80 MCP server

A minimal [MCP](https://modelcontextprotocol.io) server that exposes the Vrel
Chat-80 geography model as a tool Claude can call.

The server registers one tool, `ask_geography(question: str) -> str`. Claude
forwards a natural-language geography question; the server parses and executes
it against Chat-80's knowledge base (continents, countries, oceans, seas,
rivers, cities, populations, areas, borders) and returns the surface-form
answer.

## Install

From the repo root:

```sh
python3 -m venv venv
. venv/bin/activate
pip install -e .
pip install 'mcp[cli]'
```

## Run / smoke-test

```sh
python examples/mcp_chat80/server.py     # speaks MCP over stdio
```

It will block waiting for an MCP client. To verify it works without a real
client, drive it in-process:

```sh
python - <<'PY'
import asyncio, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command=sys.executable,
                                   args=["examples/mcp_chat80/server.py"])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            out = await s.call_tool("ask_geography",
                {"question": "What is the capital of Upper_Volta?"})
            print(out.content[0].text)

asyncio.run(main())
PY
```

## Register with Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`
(macOS) or the equivalent on your platform:

```json
{
  "mcpServers": {
    "vrel-chat80": {
      "command": "/absolute/path/to/vrel/venv/bin/python",
      "args": ["/absolute/path/to/vrel/examples/mcp_chat80/server.py"]
    }
  }
}
```

Restart Claude Desktop. Ask something like *"Using the geography tool, what
percentage of countries border each ocean?"* and Claude will call
`ask_geography`.

## Register with Claude Code

```sh
claude mcp add vrel-chat80 \
  /absolute/path/to/vrel/venv/bin/python \
  /absolute/path/to/vrel/examples/mcp_chat80/server.py
```

## Files

- `chat80_system.py` — factory that builds the Chat-80 `BasicSystem`. Mirrors
  the wiring in `tests/integration/chat80/test.py`.
- `server.py` — `FastMCP` server registering the `ask_geography` tool.

## Notes / limits

- Chat-80's grammar is fixed; if a question fails to parse it returns
  `"Could not understand: ..."`. Rephrase rather than asking the tool to retry.
- Multi-word names use underscores: `Upper_Volta`, `United_Kingdom`,
  `Soviet_Union`.
- The dataset is frozen at ~1982 (e.g. `Czechoslovakia`, `East_Germany`).
- The system is built once at startup and reused across requests.
