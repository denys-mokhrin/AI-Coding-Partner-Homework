# AI-Powered Multi-Agent Banking Pipeline

**Created by**: Denys Mokhrin
**Course**: AI Coding Partner — Homework 6 (Capstone)

---

## What This System Does

This project implements a multi-agent banking transaction processing pipeline built in Python. Four meta-agents (Specification, Code Generation, Unit Tests, Documentation) collaborate to produce a working system that validates, scores for fraud risk, and settles banking transactions.

Transactions flow through three cooperating pipeline agents that communicate via JSON files in shared directories. The system processes all transactions from `sample-transactions.json` and writes results to `shared/results/`, producing a full audit log and pipeline summary.

---

## Agent Responsibilities

- **Transaction Validator** — checks required fields, validates positive decimal amounts, enforces ISO 4217 currency codes; rejects invalid transactions with descriptive reason codes
- **Fraud Detector** — scores validated transactions 0–10 using rule-based risk assessment (amount thresholds, unusual hours, cross-border); assigns LOW/MEDIUM/HIGH risk level
- **Settlement Processor** — approves LOW/MEDIUM risk transactions, flags HIGH risk as pending review, writes final JSON result to `shared/results/`

---

## Architecture

```
sample-transactions.json
         │
         ▼
   [integrator.py]
         │
         ▼
┌─────────────────────┐
│ Transaction         │  validates fields, amount,
│ Validator           │  currency (ISO 4217)
└────────┬────────────┘
         │  status: validated / rejected
         ▼
┌─────────────────────┐
│ Fraud Detector      │  scores risk 0-10
│                     │  LOW / MEDIUM / HIGH
└────────┬────────────┘
         │  fraud_risk_score + fraud_risk_level
         ▼
┌─────────────────────┐
│ Settlement          │  settled / pending_review
│ Processor           │  / rejected
└────────┬────────────┘
         │
         ▼
  shared/results/{TXN_ID}.json
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.12 |
| Monetary arithmetic | `decimal.Decimal` |
| Testing | pytest + pytest-cov |
| MCP server | FastMCP |
| Framework lookup | context7 MCP |
| Coverage gate | PreToolUse hook |

---

## Sample Results (8 transactions)

| Transaction | Settlement | Risk | Notes |
|-------------|-----------|------|-------|
| TXN001 | settled | LOW | $1,500 domestic |
| TXN002 | settled | MEDIUM | $25,000 high value |
| TXN003 | settled | LOW | $9,999.99 near-threshold |
| TXN004 | settled | MEDIUM | €500 unusual hour + cross-border |
| TXN005 | pending_review | HIGH | $75,000 very high value |
| TXN006 | rejected | N/A | Invalid currency (XYZ) |
| TXN007 | rejected | N/A | Negative amount (-$100) |
| TXN008 | settled | LOW | $3,200 mobile transfer |

---

## Quick Start

See [HOWTORUN.md](HOWTORUN.md) for full instructions.

```bash
cd homework-6
pip install -r requirements.txt
python integrator.py
```
