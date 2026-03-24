"""
Custom FastMCP Server — Pipeline Status
Exposes pipeline results as tools and a resource.
"""

import json
import os
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP(
    name="pipeline-status",
    instructions="Query the banking pipeline results.",
)

RESULTS_DIR = Path(__file__).parent.parent / "shared" / "results"


def _load_results() -> list[dict]:
    results = []
    if not RESULTS_DIR.exists():
        return results
    for f in sorted(RESULTS_DIR.glob("*.json")):
        with open(f, encoding="utf-8") as fh:
            results.append(json.load(fh))
    return results


@mcp.tool()
def get_transaction_status(transaction_id: str) -> dict:
    """
    Get the current status of a transaction by ID.

    Args:
        transaction_id: The transaction ID (e.g. 'TXN001')

    Returns:
        Transaction result dict or error message.
    """
    result_file = RESULTS_DIR / f"{transaction_id}.json"
    if not result_file.exists():
        return {"error": f"Transaction {transaction_id} not found in results."}
    with open(result_file, encoding="utf-8") as f:
        return json.load(f)


@mcp.tool()
def list_pipeline_results() -> list[dict]:
    """
    Return a summary of all processed transactions.

    Returns:
        List of dicts with transaction_id, settlement_status, fraud_risk_level.
    """
    results = _load_results()
    return [
        {
            "transaction_id": r["data"].get("transaction_id"),
            "settlement_status": r["data"].get("settlement_status"),
            "fraud_risk_level": r["data"].get("fraud_risk_level", "N/A"),
            "rejection_reason": r["data"].get("rejection_reason"),
        }
        for r in results
    ]


@mcp.resource("pipeline://summary")
def pipeline_summary() -> str:
    """
    Returns the latest pipeline run summary as text.
    """
    results = _load_results()
    if not results:
        return "No pipeline results found. Run the pipeline first."

    settled = sum(1 for r in results if r["data"].get("settlement_status") == "settled")
    pending = sum(1 for r in results if r["data"].get("settlement_status") == "pending_review")
    rejected = sum(1 for r in results if r["data"].get("settlement_status") == "rejected")

    lines = [
        "=== Pipeline Summary ===",
        f"Total processed : {len(results)}",
        f"Settled         : {settled}",
        f"Pending review  : {pending}",
        f"Rejected        : {rejected}",
        "",
    ]
    for r in results:
        d = r["data"]
        txn_id = d.get("transaction_id")
        status = d.get("settlement_status")
        risk = d.get("fraud_risk_level", "N/A")
        reason = d.get("rejection_reason", "")
        line = f"  {txn_id}: {status} | risk={risk}"
        if reason:
            line += f" | reason={reason}"
        lines.append(line)

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
