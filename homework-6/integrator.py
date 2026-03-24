"""
Integrator / Orchestrator
Loads sample-transactions.json and runs each transaction through the pipeline:
  Transaction Validator → Fraud Detector → Settlement Processor
"""

import json
import logging
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from agents.transaction_validator import process_message as validate
from agents.fraud_detector import process_message as detect_fraud
from agents.settlement_processor import process_message as settle

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
SHARED_DIR = BASE_DIR / "shared"
RESULTS_DIR = SHARED_DIR / "results"
TRANSACTIONS_FILE = BASE_DIR / "sample-transactions.json"


def setup_directories():
    for sub in ("input", "processing", "output", "results"):
        (SHARED_DIR / sub).mkdir(parents=True, exist_ok=True)


def clear_directories():
    for sub in ("input", "processing", "output", "results"):
        d = SHARED_DIR / sub
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)


def wrap_transaction(txn: dict) -> dict:
    return {
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_agent": "integrator",
        "target_agent": "transaction_validator",
        "message_type": "transaction",
        "data": txn,
    }


def run_pipeline(transactions_file: Path = None, results_dir: Path = None) -> list[dict]:
    txn_file = transactions_file or TRANSACTIONS_FILE
    res_dir = str(results_dir or RESULTS_DIR)

    logger.info("=== Pipeline started ===")
    setup_directories()

    with open(txn_file, encoding="utf-8") as f:
        transactions = json.load(f)

    results = []
    for txn in transactions:
        txn_id = txn.get("transaction_id", "UNKNOWN")
        logger.info("--- Processing %s ---", txn_id)

        message = wrap_transaction(dict(txn))

        # Stage 1: Validate
        message = validate(message)

        # Stage 2: Fraud detection (always runs, skips if already rejected)
        message = detect_fraud(message)

        # Stage 3: Settlement
        message = settle(message, results_dir=res_dir)

        results.append(message)

    logger.info("=== Pipeline complete: %d transactions processed ===", len(results))
    _print_summary(results)
    return results


def _print_summary(results: list[dict]):
    settled = sum(1 for r in results if r["data"].get("settlement_status") == "settled")
    pending = sum(1 for r in results if r["data"].get("settlement_status") == "pending_review")
    rejected = sum(1 for r in results if r["data"].get("settlement_status") == "rejected")

    print("\n" + "=" * 50)
    print("PIPELINE SUMMARY")
    print("=" * 50)
    print(f"  Total processed : {len(results)}")
    print(f"  Settled         : {settled}")
    print(f"  Pending review  : {pending}")
    print(f"  Rejected        : {rejected}")
    print("=" * 50)

    for r in results:
        d = r["data"]
        txn_id = d.get("transaction_id")
        status = d.get("settlement_status")
        risk = d.get("fraud_risk_level", "N/A")
        reason = d.get("rejection_reason", "")
        line = f"  {txn_id}: {status} | risk={risk}"
        if reason:
            line += f" | reason={reason}"
        print(line)
    print()


if __name__ == "__main__":
    clear_directories()
    run_pipeline()
