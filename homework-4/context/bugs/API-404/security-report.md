# Security Report

**Bug ID**: API-404
**Reviewer**: Security Vulnerabilities Verifier Agent
**Date**: 2026-03-10
**Scope**: Files changed in `context/bugs/API-404/fix-summary.md`

---

## Executive Summary

The single-line fix (type coercion via `parseInt`) introduces no new vulnerabilities. The changed code correctly handles non-numeric input by producing `NaN`, which results in a safe 404 response. The existing codebase has minor informational findings related to missing input validation verbosity and lack of request logging, but no critical or high-severity issues.

---

## Findings

### Finding 1 — No input validation error message for non-numeric IDs

| Field | Value |
|-------|-------|
| Severity | INFO |
| File | `demo-bug-fix/src/controllers/userController.js` |
| Line | 19–23 |
| Class | Missing input validation (informational) |

**Description**: When a non-numeric string (e.g., `/api/users/abc`) is passed, `parseInt("abc", 10)` returns `NaN`. The `.find()` call returns `undefined`, which results in a generic `{ error: "User not found" }` 404 response. While this is safe and correct, a client cannot distinguish between "user with this ID does not exist" and "invalid ID format". This is not a security vulnerability but a UX/API design concern.

**Remediation**: Optionally add an explicit check before the find:
```js
const parsed = parseInt(userId, 10);
if (isNaN(parsed)) {
  return res.status(400).json({ error: 'Invalid user ID format' });
}
```

---

### Finding 2 — No rate limiting on the endpoint

| Field | Value |
|-------|-------|
| Severity | LOW |
| File | `demo-bug-fix/server.js` |
| Line | 16 |
| Class | Missing validation / DoS exposure |

**Description**: The Express app has no rate limiting middleware. The `/api/users/:id` endpoint can be called at unlimited rate, which in a production setting would be a DoS risk. This predates the fix and is not introduced by it.

**Remediation**: Add `express-rate-limit` middleware for production use.

---

## No Issues Found

The following vulnerability classes were checked and no issues were found in the changed code:

| Class | Result |
|-------|--------|
| Injection (eval, exec, dynamic query) | No issues — no dynamic code execution, no database |
| Hardcoded secrets | No issues — no credentials in source |
| Insecure comparison (auth/authz) | No issues — comparison is for data lookup, not auth |
| XSS | Not applicable — JSON API, no HTML output |
| CSRF | Not applicable — read-only GET endpoint |
| Information leakage | No issues — stack traces not exposed in error responses |
| Unsafe dependencies | No issues — express@4.18.x has no known CVEs in current version |

---

## Summary Table

| # | Title | Severity | File:Line |
|---|-------|----------|-----------|
| 1 | No input validation error message for non-numeric IDs | INFO | `userController.js:19–23` |
| 2 | No rate limiting on the endpoint | LOW | `server.js:16` |

---

## References

- Fix summary: `context/bugs/API-404/fix-summary.md`
- Files reviewed:
  - `demo-bug-fix/src/controllers/userController.js`
  - `demo-bug-fix/src/routes/users.js`
  - `demo-bug-fix/server.js`
