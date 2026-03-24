"""
Agent 3: Settlement Processor
Approves, flags, or rejects transactions based on validation and fraud risk.
Writes final result to shared/results/.
"""

import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "shared", "results")


def _settlement_status(data: dict) -> str:
    if data.get("status") == "rejected":
        return "rejected"
    if data.get("fraud_risk_level") == "HIGH":
        return "pending_review"
    return "settled"


def process_message(message: dict, results_dir: str = None) -> dict:
    data = message.get("data", {})
    txn_id = data.get("transaction_id", "UNKNOWN")

    status = _settlement_status(data)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    message["data"]["settlement_status"] = status
    message["data"]["settlement_timestamp"] = timestamp

    logger.info(
        "agent=settlement txn=%s settlement=%s risk=%s",
        txn_id, status, data.get("fraud_risk_level", "N/A"),
    )

    out_dir = results_dir or RESULTS_DIR
    os.makedirs(out_dir, exist_ok=True)
    result_path = os.path.join(out_dir, f"{txn_id}.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(message, f, indent=2)

    return message
