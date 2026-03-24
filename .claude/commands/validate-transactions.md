Validate all transactions in sample-transactions.json without running the full pipeline.

Steps:
1. Read `sample-transactions.json`
2. Run only the validator agent on each transaction (dry-run — no files written to shared/)
3. Report: total count, valid count, invalid count, reasons for rejection
4. Show a table of results with columns: transaction_id, status, rejection_reason
