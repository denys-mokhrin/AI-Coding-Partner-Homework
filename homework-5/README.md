# Homework 5: Configure MCP Servers

**Author**: Denys Mokhrin
**Course**: AI Coding Partner

---

## Overview

This project configures and demonstrates **four MCP (Model Context Protocol) servers** that connect Claude Code to external services and custom functionality.

---

## MCP Servers Configured

### 1. GitHub MCP (`@modelcontextprotocol/server-github`)

Connects Claude to the GitHub API via a Personal Access Token. Enables Claude to list repositories, pull requests, issues, and commits.

**Config**: `.mcp.json` → `"github"`
**Interaction demonstrated**: Listing recent pull requests on the AI-Coding-Partner-Homework repository.

### 2. Filesystem MCP (`@modelcontextprotocol/server-filesystem`)

Connects Claude to a local directory on the machine. Enables Claude to list files, read file contents, and explore directory structure without manual copy-paste.

**Config**: `.mcp.json` → `"filesystem"`
**Interaction demonstrated**: Listing files in the project directory.

### 3. Jira MCP (Atlassian plugin)

Connects Claude to Jira via the Atlassian MCP plugin configured in Claude Code. Enables querying issues, tickets, and project data.

**Config**: Claude Code Atlassian plugin (enabled globally)
**Interaction demonstrated**: Fetching the last 5 bug tickets from a Jira project.

### 4. Custom FastMCP Server (`lorem-ipsum-reader`)

A custom Python MCP server built with [FastMCP](https://github.com/jlowin/fastmcp). Exposes a **Resource** URI and a **Tool** that return word-limited excerpts from `lorem-ipsum.md`.

**Config**: `.mcp.json` → `"lorem-ipsum-reader"`
**Files**: `custom-mcp-server/server.py`

#### Resource vs Tool

| Concept | Description |
|---------|-------------|
| **Resource** (`lorem://ipsum/{word_count}`) | A URI Claude reads passively — like a file or API endpoint. Exposes data on demand. |
| **Tool** (`read(word_count)`) | An action Claude actively calls to perform an operation and receive a result. |

---

## Project Structure

```
homework-5/
├── README.md
├── HOWTORUN.md
├── STUDENT.md
├── TASKS.md
├── .mcp.json                          ← MCP server configuration
├── custom-mcp-server/
│   ├── server.py                      ← FastMCP server (resource + tool)
│   ├── lorem-ipsum.md                 ← Source text
│   └── requirements.txt               ← fastmcp dependency
└── docs/
    └── screenshots/
        ├── github-mcp-result.png
        ├── filesystem-mcp-result.png
        ├── jira-mcp-result.png
        └── custom-mcp-read-tool-result.png
```

---

## How to Run

See [HOWTORUN.md](HOWTORUN.md).
