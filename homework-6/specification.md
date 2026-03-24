# Specification: AI-Powered Multi-Agent Banking Pipeline

**Author**: Denys Mokhrin

---

## 1. High-Level Objective

Build a 3-agent Python pipeline that validates, scores for fraud risk, and settles banking transactions using file-based JSON message passing through shared directories.

---

## 2. Mid-Level Objectives

- Transactions with invalid or missing fields are rejected with a descriptive reason (e.g. `INVALID_CURRENCY`, `NEGATIVE_AMOUNT`, `MISSING_FIELD`)
- Transactions above $10,000 are assigned `fraud_risk_level: "HIGH"` with a risk score ≥ 7; transactions above $50,000 receive an additional penalty
- Cross-border transactions (country != "US") and transactions at unusual hours (02:00–05:00 UTC) receive additional fraud risk points
- All agent operations are logged to `pipeline.log` with ISO 8601 timestamps, agent name, transaction ID, and outcome; account numbers are masked in all log output
- The pipeline processes all 8 sample transactions and writes 8 result files to `shared/results/`; rejected transactions include a `rejection_reason` field

---

## 3. Implementation Notes

- **Monetary calculations**: `decimal.Decimal` only — never `float`
- **Currency validation**: ISO 4217 whitelist (USD, EUR, GBP, JPY, CHF, CAD, AUD, CNY, HKD, SGD, NOK, SEK, DKK, NZD, MXN, BRL, INR, KRW, ZAR, RUB)
- **Logging**: audit trail with `timestamp`, `agent`, `transaction_id`, `outcome`; mask account numbers as `ACC-****`
- **PII**: account numbers must never appear in plaintext in log files
- **Message format**: all inter-agent messages are JSON files in `shared/` subdirectories following the standard envelope format

---

## 4. Context

- **Beginning state**: `sample-transactions.json` exists with 8 raw transaction records. No agents exist. No `shared/` directories exist.
- **Ending state**: All 8 transactions processed. Results in `shared/results/`. Test coverage ≥ 90%. `README.md` and `HOWTORUN.md` complete.

---

## 5. Low-Level Tasks

### Task: Transaction Validator

**Prompt**: "Build a Python module `agents/transaction_validator.py` with a `process_message(message: dict) -> dict` function. It must: (1) check required fields: transaction_id, amount, currency, source_account, destination_account, timestamp; (2) validate amount is a positive decimal.Decimal; (3) validate currency against the ISO 4217 whitelist; (4) return the message dict with `data.status` set to 'validated' or 'rejected' and a `data.rejection_reason` field when rejected. Log each outcome with masked account numbers."

**File to CREATE**: `agents/transaction_validator.py`
**Function to CREATE**: `process_message(message: dict) -> dict`
**Details**:
- Check required fields: `transaction_id`, `amount`, `currency`, `source_account`, `destination_account`, `timestamp`
- Validate amount is positive `decimal.Decimal` (reject negative and zero)
- Validate currency against ISO 4217 whitelist
- Return message with `status: "validated"` or `status: "rejected"` + `rejection_reason`

---

### Task: Fraud Detector

**Prompt**: "Build a Python module `agents/fraud_detector.py` with a `process_message(message: dict) -> dict` function. It must score each validated transaction for fraud risk on a 0–10 scale using these rules: amount > $10,000 → +3 pts; amount > $50,000 → +4 additional pts; unusual hour 02:00–05:00 UTC → +2 pts; cross-border (country != 'US') → +1 pt. Map score to level: LOW (0–2), MEDIUM (3–6), HIGH (7–10). Add `fraud_risk_score` and `fraud_risk_level` to message data. Log each result."

**File to CREATE**: `agents/fraud_detector.py`
**Function to CREATE**: `process_message(message: dict) -> dict`
**Details**:
- Score: amount > $10,000 → +3 pts; amount > $50,000 → +4 pts (cumulative); unusual hour (02–05 UTC) → +2 pts; cross-border → +1 pt
- Levels: LOW (0–2), MEDIUM (3–6), HIGH (7–10)
- Add `fraud_risk_score` and `fraud_risk_level` to `data`

---

### Task: Settlement Processor

**Prompt**: "Build a Python module `agents/settlement_processor.py` with a `process_message(message: dict) -> dict` function. It must: (1) approve LOW and MEDIUM risk transactions for settlement; (2) flag HIGH risk transactions as 'pending_review' rather than settling; (3) add `settlement_status` ('settled', 'pending_review', 'rejected') and `settlement_timestamp` (ISO 8601) to message data; (4) write the final result JSON to shared/results/. Log each decision."

**File to CREATE**: `agents/settlement_processor.py`
**Function to CREATE**: `process_message(message: dict) -> dict`
**Details**:
- LOW/MEDIUM risk + validated → `settlement_status: "settled"`
- HIGH risk → `settlement_status: "pending_review"`
- Rejected by validator → `settlement_status: "rejected"`
- Write result to `shared/results/{transaction_id}.json`
