"""Integration test — full pipeline run."""

import json
import os
import pytest
from pathlib import Path
from integrator import run_pipeline


SAMPLE_FILE = Path(__file__).parent.parent / "sample-transactions.json"


def test_full_pipeline_processes_all_transactions(tmp_path):
    results = run_pipeline(transactions_file=SAMPLE_FILE, results_dir=tmp_path)

    assert len(results) == 8

    result_files = list(tmp_path.glob("*.json"))
    assert len(result_files) == 8


def test_invalid_currency_rejected(tmp_path):
    results = run_pipeline(transactions_file=SAMPLE_FILE, results_dir=tmp_path)
    txn006 = next(r for r in results if r["data"]["transaction_id"] == "TXN006")
    assert txn006["data"]["settlement_status"] == "rejected"
    assert "INVALID_CURRENCY" in txn006["data"]["rejection_reason"]


def test_negative_amount_rejected(tmp_path):
    results = run_pipeline(transactions_file=SAMPLE_FILE, results_dir=tmp_path)
    txn007 = next(r for r in results if r["data"]["transaction_id"] == "TXN007")
    assert txn007["data"]["settlement_status"] == "rejected"
    assert txn007["data"]["rejection_reason"] == "NEGATIVE_AMOUNT"


def test_high_value_pending_review(tmp_path):
    results = run_pipeline(transactions_file=SAMPLE_FILE, results_dir=tmp_path)
    txn005 = next(r for r in results if r["data"]["transaction_id"] == "TXN005")
    assert txn005["data"]["settlement_status"] == "pending_review"
    assert txn005["data"]["fraud_risk_level"] == "HIGH"


def test_normal_transaction_settled(tmp_path):
    results = run_pipeline(transactions_file=SAMPLE_FILE, results_dir=tmp_path)
    txn001 = next(r for r in results if r["data"]["transaction_id"] == "TXN001")
    assert txn001["data"]["settlement_status"] == "settled"
    assert txn001["data"]["fraud_risk_level"] == "LOW"
