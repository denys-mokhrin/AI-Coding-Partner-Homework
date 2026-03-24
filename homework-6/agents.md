# Agents — AI-Powered Multi-Agent Banking Pipeline

**Author**: Denys Mokhrin

---

## Pipeline Agents

### Agent 1: Transaction Validator (`agents/transaction_validator.py`)

**Role**: First stage. Validates every incoming transaction.
**Input**: Raw transaction dict wrapped in a message envelope
**Output**: Message with `data.status = "validated"` or `"rejected"` + `rejection_reason`

**Checks**:
- Required fields: `transaction_id`, `amount`, `currency`, `source_account`, `destination_account`, `timestamp`
- Amount is a positive `decimal.Decimal` (never float)
- Currency is a valid ISO 4217 code

---

### Agent 2: Fraud Detector (`agents/fraud_detector.py`)

**Role**: Second stage. Scores validated transactions for fraud risk.
**Input**: Validated message from Agent 1 (skips rejected ones)
**Output**: Message enriched with `fraud_risk_score` (0–10), `fraud_risk_level` (LOW/MEDIUM/HIGH), `fraud_flags`

**Scoring rules**:
| Rule | Points |
|------|--------|
| Amount > $10,000 | +3 |
| Amount > $50,000 | +4 (cumulative, total +7) |
| Unusual hour 02:00–05:00 UTC | +2 |
| Cross-border (country ≠ US) | +1 |

**Risk levels**: LOW (0–2), MEDIUM (3–6), HIGH (7–10)

---

### Agent 3: Settlement Processor (`agents/settlement_processor.py`)

**Role**: Third and final stage. Makes settlement decision and writes result to disk.
**Input**: Message from Agent 2 with risk scoring
**Output**: Message with `settlement_status` and `settlement_timestamp`; result file in `shared/results/`

**Decisions**:
| Condition | Settlement Status |
|-----------|------------------|
| Validated + LOW or MEDIUM risk | `settled` |
| Validated + HIGH risk | `pending_review` |
| Rejected by validator | `rejected` |

---

## Meta-Agents (Homework 6 Deliverables)

| Meta-Agent | Role | File |
|------------|------|------|
| **Agent 1 — Specification** | Produces `specification.md` via `write-spec` skill | `commands/write-spec.md` |
| **Agent 2 — Code Generation** | Builds pipeline using context7 MCP for framework lookup | `agents/` + `integrator.py` |
| **Agent 3 — Unit Tests** | Generates test suite with coverage gate hook | `tests/` + `.claude/settings.json` |
| **Agent 4 — Documentation** | Generates README, HOWTORUN with author name | `README.md`, `HOWTORUN.md` |

---

## Message Envelope Format

All inter-agent messages follow this structure:

```json
{
  "message_id": "uuid4-string",
  "timestamp": "2026-03-16T10:00:00Z",
  "source_agent": "transaction_validator",
  "target_agent": "fraud_detector",
  "message_type": "transaction",
  "data": {
    "transaction_id": "TXN001",
    "amount": "1500.00",
    "currency": "USD",
    "status": "validated",
    "fraud_risk_score": 0,
    "fraud_risk_level": "LOW",
    "settlement_status": "settled"
  }
}
```
