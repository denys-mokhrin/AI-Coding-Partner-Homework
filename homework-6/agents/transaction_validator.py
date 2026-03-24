"""
Agent 1: Transaction Validator
Validates required fields, amount, and ISO 4217 currency code.
"""

import logging
from decimal import Decimal, InvalidOperation

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ["transaction_id", "amount", "currency", "source_account", "destination_account", "timestamp"]

ISO_4217_CURRENCIES = {
    "USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY", "HKD", "SGD",
    "NOK", "SEK", "DKK", "NZD", "MXN", "BRL", "INR", "KRW", "ZAR", "RUB",
}


def _mask_account(account: str) -> str:
    return "ACC-****"


def process_message(message: dict) -> dict:
    data = message.get("data", {})
    txn_id = data.get("transaction_id", "UNKNOWN")

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] is None:
            reason = f"MISSING_FIELD:{field}"
            logger.info("agent=validator txn=%s outcome=rejected reason=%s", txn_id, reason)
            message["data"]["status"] = "rejected"
            message["data"]["rejection_reason"] = reason
            return message

    # Validate amount
    try:
        amount = Decimal(str(data["amount"]))
    except InvalidOperation:
        reason = "INVALID_AMOUNT_FORMAT"
        logger.info("agent=validator txn=%s outcome=rejected reason=%s", txn_id, reason)
        message["data"]["status"] = "rejected"
        message["data"]["rejection_reason"] = reason
        return message

    if amount <= Decimal("0"):
        reason = "NEGATIVE_AMOUNT" if amount < Decimal("0") else "ZERO_AMOUNT"
        logger.info("agent=validator txn=%s outcome=rejected reason=%s", txn_id, reason)
        message["data"]["status"] = "rejected"
        message["data"]["rejection_reason"] = reason
        return message

    # Validate currency
    currency = data["currency"].upper()
    if currency not in ISO_4217_CURRENCIES:
        reason = f"INVALID_CURRENCY:{currency}"
        logger.info("agent=validator txn=%s outcome=rejected reason=%s", txn_id, reason)
        message["data"]["status"] = "rejected"
        message["data"]["rejection_reason"] = reason
        return message

    logger.info(
        "agent=validator txn=%s src=%s outcome=validated amount=%s %s",
        txn_id, _mask_account(data["source_account"]), amount, currency,
    )
    message["data"]["status"] = "validated"
    message["data"]["amount"] = str(amount)
    return message
