"""Unit tests for Fraud Detector agent."""

import pytest
from agents.fraud_detector import process_message, _compute_risk_score, _risk_level


def _make_msg(amount="1500.00", currency="USD", timestamp="2026-03-16T09:00:00Z", country="US", status="validated"):
    return {
        "data": {
            "transaction_id": "TXN001",
            "amount": amount,
            "currency": currency,
            "timestamp": timestamp,
            "status": status,
            "metadata": {"country": country},
        }
    }


# Risk levels
def test_low_risk_small_domestic():
    result = process_message(_make_msg("1500.00"))
    assert result["data"]["fraud_risk_level"] == "LOW"
    assert result["data"]["fraud_risk_score"] == 0


def test_medium_risk_high_value():
    result = process_message(_make_msg("25000.00"))
    assert result["data"]["fraud_risk_level"] == "MEDIUM"
    assert result["data"]["fraud_risk_score"] == 3


def test_high_risk_very_high_value():
    result = process_message(_make_msg("75000.00"))
    assert result["data"]["fraud_risk_level"] == "HIGH"
    assert result["data"]["fraud_risk_score"] == 7


def test_unusual_hour_adds_score():
    result = process_message(_make_msg("500.00", timestamp="2026-03-16T02:47:00Z"))
    assert "UNUSUAL_HOUR" in result["data"]["fraud_flags"]
    assert result["data"]["fraud_risk_score"] >= 2


def test_cross_border_adds_score():
    result = process_message(_make_msg("500.00", country="DE"))
    assert "CROSS_BORDER" in result["data"]["fraud_flags"]
    assert result["data"]["fraud_risk_score"] >= 1


def test_combined_flags_unusual_and_cross_border():
    result = process_message(_make_msg("500.00", timestamp="2026-03-16T03:00:00Z", country="GB"))
    assert result["data"]["fraud_risk_score"] == 3
    assert result["data"]["fraud_risk_level"] == "MEDIUM"


# Skips rejected transactions
def test_skips_rejected_transaction():
    msg = _make_msg(status="rejected")
    result = process_message(msg)
    assert "fraud_risk_score" not in result["data"]


# Risk level mapping
@pytest.mark.parametrize("score,expected", [
    (0, "LOW"), (2, "LOW"), (3, "MEDIUM"), (6, "MEDIUM"), (7, "HIGH"), (10, "HIGH")
])
def test_risk_level_boundaries(score, expected):
    assert _risk_level(score) == expected
