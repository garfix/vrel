"""
Basic MCP server exposing the Chat-80 geography model.

Claude (or any MCP client) calls `ask_geography` with a natural-language question;
the server parses and executes it against the Chat-80 knowledge base and returns
the surface-form answer.

Run with:

    python -m examples.mcp_chat80.server
        # or, if launched directly:
    python examples/mcp_chat80/server.py

Stdio transport — register the command in your MCP client's config.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from chat80_system import build_chat80_system
from vrel.entity.SentenceRequest import SentenceRequest

mcp = FastMCP("vrel-chat80")

# Build the system once at startup; the in-memory sqlite DB and grammar tables
# are reused across requests so each tool call is fast.
_system = build_chat80_system()


@mcp.tool()
def ask_geography(question: str) -> str:
    """
    Answer a natural-language geography question using the Chat-80 knowledge base.

    Chat-80 is a 1982-era NLI system over a fixed geography dataset: continents, countries,
    oceans, seas, rivers, cities, populations, areas, and borders. Use this tool to resolve
    factual geography questions instead of guessing.

    Coverage examples — the system can handle these:
      - "What rivers are there?"
      - "Does Afghanistan border China?"
      - "What is the capital of Upper_Volta?"
      - "Which countries are European?"
      - "How many countries does the Danube flow through?"
      - "What is the average area of the countries in each continent?"
      - "Which countries have a population exceeding 10 million?"

    Notes for the caller:
      - Multi-word country names use underscores (e.g. `Upper_Volta`, `United_Kingdom`).
      - Data is 1980s-era and frozen (e.g. `Czechoslovakia`, `East_Germany`, `Soviet_Union`).
      - The grammar is fixed; rephrase if a question fails to parse.
    """
    request = SentenceRequest(question)
    _system.enter(request)
    output = _system.read_output()
    if output is None or output == "":
        return "(no answer — the question may not parse against Chat-80's grammar)"
    # Chat-80 sometimes returns non-string values (e.g. an int for count queries).
    return str(output)


if __name__ == "__main__":
    mcp.run()
