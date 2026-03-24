"""
Agent 2: Fraud Detector
Scores validated transactions for fraud risk using rule-based scoring.
"""

import logging
from datetime import datetime, timezone
from decimal import Decimal

logger = logging.getLogger(__name__)

THRESHOLD_HIGH = Decimal("10000")
THRESHOLD_VERY_HIGH = Decimal("50000")
UNUSUAL_HOUR_START = 2
UNUSUAL_HOUR_END = 5


def _compute_risk_score(data: dict) -> tuple[int, list[str]]:
    score = 0
    flags = []
    amount = Decimal(str(data["amount"]))

    if amount > THRESHOLD_VERY_HIGH:
        score += 7  # +3 for >10k and +4 for >50k
        flags.append("VERY_HIGH_VALUE")
    elif amount > THRESHOLD_HIGH:
        score += 3
        flags.append("HIGH_VALUE")

    try:
        ts = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        hour = ts.astimezone(timezone.utc).hour
        if UNUSUAL_HOUR_START <= hour < UNUSUAL_HOUR_END:
            score += 2
            flags.append("UNUSUAL_HOUR")
    except (ValueError, KeyError):
        pass

    country = data.get("metadata", {}).get("country", "US")
    if country != "US":
        score += 1
        flags.append("CROSS_BORDER")

    return min(score, 10), flags


def _risk_level(score: int) -> str:
    if score <= 2:
        return "LOW"
    if score <= 6:
        return "MEDIUM"
    return "HIGH"


def process_message(message: dict) -> dict:
    data = message.get("data", {})
    txn_id = data.get("transaction_id", "UNKNOWN")

    if data.get("status") == "rejected":
        return message

    score, flags = _compute_risk_score(data)
    level = _risk_level(score)

    logger.info(
        "agent=fraud_detector txn=%s score=%d level=%s flags=%s",
        txn_id, score, level, flags,
    )

    message["data"]["fraud_risk_score"] = score
    message["data"]["fraud_risk_level"] = level
    message["data"]["fraud_flags"] = flags
    return message
