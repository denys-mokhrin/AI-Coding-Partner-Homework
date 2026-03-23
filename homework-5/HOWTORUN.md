# How to Run — Homework 5: MCP Servers

---

## Prerequisites

- Node.js 18+ and npm
- Python 3.12+ with `fastmcp` installed
- Claude Code CLI

---

## Task 1 & 2: GitHub + Filesystem MCP

These servers are configured in `.mcp.json` and use `npx` — no manual installation needed.

### Configure GitHub MCP

1. Create a GitHub Personal Access Token (PAT):
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate token with scopes: `repo`, `read:org`, `read:user`

2. Open `.mcp.json` and replace `<YOUR_GITHUB_PAT_HERE>` with your token.

3. Start Claude Code in this directory — MCP servers will launch automatically.

### Test GitHub MCP

Ask Claude:
> "List my recent pull requests on the AI-Coding-Partner-Homework repository"

### Test Filesystem MCP

Ask Claude:
> "List all files in the homework-5 directory"

---

## Task 3: Jira MCP

Jira is connected via the **Atlassian MCP plugin** configured in Claude Code settings.

Ask Claude:
> "Give me the Jira tickets of the last 5 bugs on a project"

---

## Task 4: Custom MCP Server (FastMCP)

### Install dependencies

```bash
cd homework-5/custom-mcp-server
pip install -r requirements.txt
```

### Run the server manually (for testing)

```bash
python C:\Users\denys\AppData\Local\Programs\Python\Python312\python.exe server.py
```

Or using fastmcp dev mode:
```bash
fastmcp dev server.py
```

### Connect to Claude Code

The server is already configured in `.mcp.json` as `lorem-ipsum-reader`.

Start Claude Code in the `homework-5/` directory — it will read `.mcp.json` and launch the server automatically.

### Use the `read` tool

Ask Claude:
> "Use the read tool to get 50 words from the lorem ipsum file"

Or:
> "Call the read tool with word_count=100"

### MCP Configuration (`.mcp.json`)

```json
{
  "mcpServers": {
    "lorem-ipsum-reader": {
      "command": "C:\\Users\\denys\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
      "args": ["C:\\...\\homework-5\\custom-mcp-server\\server.py"]
    }
  }
}
```

---

## Concepts: Resources vs Tools

| Concept | Description | Example in this project |
|---------|-------------|-------------------------|
| **Resource** | A URI Claude can read from — exposes data passively, like a file or API endpoint. Claude reads it on demand. | `lorem://ipsum/30` — returns 30 words from the file |
| **Tool** | An action Claude can call to perform an operation. Executes logic and returns a result. | `read(word_count=30)` — Claude actively calls this to get content |

Resources are like web pages Claude can browse; tools are like functions Claude can invoke.
