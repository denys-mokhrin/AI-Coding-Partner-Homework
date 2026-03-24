"""Unit tests for Settlement Processor agent."""

import json
import os
import pytest
from agents.settlement_processor import process_message


def _make_msg(status="validated", fraud_risk_level="LOW"):
    return {
        "data": {
            "transaction_id": "TXN001",
            "amount": "1500.00",
            "currency": "USD",
            "status": status,
            "fraud_risk_level": fraud_risk_level,
        }
    }


def test_low_risk_settled(tmp_path):
    result = process_message(_make_msg("validated", "LOW"), results_dir=str(tmp_path))
    assert result["data"]["settlement_status"] == "settled"
    assert (tmp_path / "TXN001.json").exists()


def test_medium_risk_settled(tmp_path):
    result = process_message(_make_msg("validated", "MEDIUM"), results_dir=str(tmp_path))
    assert result["data"]["settlement_status"] == "settled"


def test_high_risk_pending_review(tmp_path):
    result = process_message(_make_msg("validated", "HIGH"), results_dir=str(tmp_path))
    assert result["data"]["settlement_status"] == "pending_review"


def test_rejected_transaction(tmp_path):
    result = process_message(_make_msg("rejected", None), results_dir=str(tmp_path))
    assert result["data"]["settlement_status"] == "rejected"


def test_result_written_to_file(tmp_path):
    process_message(_make_msg("validated", "LOW"), results_dir=str(tmp_path))
    result_file = tmp_path / "TXN001.json"
    assert result_file.exists()
    data = json.loads(result_file.read_text())
    assert data["data"]["settlement_status"] == "settled"


def test_settlement_timestamp_present(tmp_path):
    result = process_message(_make_msg(), results_dir=str(tmp_path))
    assert "settlement_timestamp" in result["data"]
    ts = result["data"]["settlement_timestamp"]
    assert "T" in ts and "Z" in ts
