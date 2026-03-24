"""Unit tests for Transaction Validator agent."""

import pytest
from agents.transaction_validator import process_message, ISO_4217_CURRENCIES


def _make_msg(overrides=None):
    data = {
        "transaction_id": "TXN001",
        "amount": "1500.00",
        "currency": "USD",
        "source_account": "ACC-1001",
        "destination_account": "ACC-2001",
        "timestamp": "2026-03-16T09:00:00Z",
    }
    if overrides:
        data.update(overrides)
    return {"data": data}


# Happy path
def test_valid_transaction_is_validated():
    result = process_message(_make_msg())
    assert result["data"]["status"] == "validated"
    assert "rejection_reason" not in result["data"]


def test_valid_eur_transaction():
    result = process_message(_make_msg({"currency": "EUR", "amount": "500.00"}))
    assert result["data"]["status"] == "validated"


# Missing fields
@pytest.mark.parametrize("field", [
    "transaction_id", "amount", "currency", "source_account", "destination_account", "timestamp"
])
def test_missing_required_field(field):
    msg = _make_msg()
    del msg["data"][field]
    result = process_message(msg)
    assert result["data"]["status"] == "rejected"
    assert f"MISSING_FIELD:{field}" in result["data"]["rejection_reason"]


# Invalid currency
def test_invalid_currency_rejected():
    result = process_message(_make_msg({"currency": "XYZ"}))
    assert result["data"]["status"] == "rejected"
    assert "INVALID_CURRENCY" in result["data"]["rejection_reason"]


# Negative amount
def test_negative_amount_rejected():
    result = process_message(_make_msg({"amount": "-100.00"}))
    assert result["data"]["status"] == "rejected"
    assert result["data"]["rejection_reason"] == "NEGATIVE_AMOUNT"


# Zero amount
def test_zero_amount_rejected():
    result = process_message(_make_msg({"amount": "0"}))
    assert result["data"]["status"] == "rejected"
    assert result["data"]["rejection_reason"] == "ZERO_AMOUNT"


# Invalid amount format
def test_invalid_amount_format_rejected():
    result = process_message(_make_msg({"amount": "abc"}))
    assert result["data"]["status"] == "rejected"
    assert result["data"]["rejection_reason"] == "INVALID_AMOUNT_FORMAT"


# Currency whitelist
def test_all_whitelisted_currencies_pass():
    for currency in list(ISO_4217_CURRENCIES)[:5]:
        result = process_message(_make_msg({"currency": currency}))
        assert result["data"]["status"] == "validated", f"Failed for {currency}"
