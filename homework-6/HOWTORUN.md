# How to Run — Homework 6

---

## Prerequisites

- Python 3.12+
- pip

---

## 1. Install dependencies

```bash
cd homework-6
pip install -r requirements.txt
```

---

## 2. Run the pipeline

```bash
python integrator.py
```

Output: pipeline summary in terminal + result files in `shared/results/`.

---

## 3. Run tests with coverage

```bash
python -m pytest tests/ -v --cov=agents --cov=integrator --cov-report=term-missing
```

Expected: 37 tests pass, coverage ≥ 90%.

---

## 4. Run the coverage gate

```bash
python check_coverage.py
```

Exits 0 if coverage ≥ 80%, exits 1 (blocks push) if below.

---

## 5. Use slash commands

In Claude Code from the `homework-6/` directory:

- `/write-spec` — generate specification from template
- `/run-pipeline` — run the full pipeline end-to-end
- `/validate-transactions` — validate transactions without processing

---

## 6. Custom MCP server (pipeline-status)

Start manually for testing:

```bash
python mcp/server.py
```

Or use via Claude Code — it loads automatically from `mcp.json`.

**Available tools**:
- `get_transaction_status(transaction_id)` — status of a single transaction
- `list_pipeline_results()` — summary of all results

**Resource**: `pipeline://summary` — full text summary of latest run

---

## 7. context7 MCP

Configured in `mcp.json`. Used during code generation to look up Python `decimal` and `datetime` modules. See `research-notes.md` for documented queries.
