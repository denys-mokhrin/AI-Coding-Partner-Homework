"""
Custom MCP Server — Lorem Ipsum Reader
Built with FastMCP

Concepts:
  Resources: URIs that Claude can read from (e.g. files, APIs, databases).
             They expose data passively — Claude reads them like web pages.
  Tools:     Actions Claude can call to perform operations (e.g. reading a file,
             running a command, calling an API). They execute logic and return results.
"""

from pathlib import Path
from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="lorem-ipsum-reader",
    instructions="Read word-limited excerpts from lorem-ipsum.md.",
)

LOREM_FILE = Path(__file__).parent / "lorem-ipsum.md"


def _read_words(word_count: int) -> str:
    """Read exactly `word_count` words from lorem-ipsum.md."""
    text = LOREM_FILE.read_text(encoding="utf-8")
    words = text.split()
    selected = words[:word_count]
    return " ".join(selected)


# ---------------------------------------------------------------------------
# Resource
# ---------------------------------------------------------------------------

@mcp.resource("lorem://ipsum/{word_count}")
def lorem_resource(word_count: int = 30) -> str:
    """
    Resource URI: lorem://ipsum/{word_count}

    Returns exactly `word_count` words from lorem-ipsum.md.
    Default word_count is 30.

    Example URIs:
      lorem://ipsum/30   → first 30 words
      lorem://ipsum/100  → first 100 words
    """
    return _read_words(word_count)


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------

@mcp.tool()
def read(word_count: int = 30) -> str:
    """
    Read words from lorem-ipsum.md.

    Args:
        word_count: Number of words to return (default: 30).

    Returns:
        A string containing exactly `word_count` words from the lorem ipsum text.
    """
    if word_count < 1:
        return "Error: word_count must be at least 1."

    words = _read_words(word_count)
    actual = len(words.split())
    if actual < word_count:
        return f"{words}\n\n(Note: only {actual} words available in source file.)"

    return words


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
