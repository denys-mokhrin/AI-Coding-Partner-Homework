# Research Notes — context7 Queries

**Author**: Denys Mokhrin
**Project**: AI-Powered Multi-Agent Banking Pipeline

---

## Query 1: Python `decimal` module for monetary arithmetic

- **Search**: "Python decimal module monetary arithmetic ROUND_HALF_UP"
- **context7 library ID**: `/python/decimal`
- **Applied**: Used `decimal.Decimal` throughout the pipeline instead of `float` for all monetary values. Configured `ROUND_HALF_UP` rounding mode in settlement calculations to ensure consistent rounding (e.g., $9999.995 rounds to $10000.00, not $9999.99).

**Key insight**: `float` cannot represent most decimal fractions exactly (e.g., `0.1 + 0.2 != 0.3`). Banking applications must use `Decimal` to avoid accumulated rounding errors that would cause balance discrepancies. The `Decimal` constructor must receive a string, not a float: `Decimal("1500.00")` not `Decimal(1500.00)`.

```python
from decimal import Decimal, ROUND_HALF_UP
amount = Decimal(str(raw_amount))
```

---

## Query 2: Python `datetime` module — ISO 8601 parsing and UTC timezone

- **Search**: "Python datetime fromisoformat UTC timezone ISO 8601 parsing"
- **context7 library ID**: `/python/datetime`
- **Applied**: Used `datetime.fromisoformat()` with `.replace("Z", "+00:00")` to parse ISO 8601 timestamps from transaction records. Used `datetime.now(timezone.utc)` for generating audit log timestamps.

**Key insight**: Python 3.11+ supports `datetime.fromisoformat("2026-03-16T10:00:00Z")` natively, but Python 3.10 and earlier require replacing the `Z` suffix with `+00:00` before parsing. Since the project targets Python 3.12, both approaches work — but using the explicit replace is more portable.

```python
from datetime import datetime, timezone
ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
hour = ts.astimezone(timezone.utc).hour
```
