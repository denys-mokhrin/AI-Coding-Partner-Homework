# Test Report

**Bug ID**: API-404
**Generator**: Unit Test Generator Agent
**Date**: 2026-03-10
**Test framework**: Jest 30.3.0
**Test file(s)**: `tests/userController.test.js`

---

## FIRST Compliance

| Principle | Status | Notes |
|-----------|--------|-------|
| Fast | PASS | Total suite: 0.255 s; avg < 1 ms per test; no I/O, no HTTP |
| Independent | PASS | Each test creates fresh `req`/`res` mocks; no shared mutable state |
| Repeatable | PASS | No `Date.now()`, `Math.random()`, or env dependencies |
| Self-validating | PASS | Every test has at least one explicit `expect` assertion |
| Timely | PASS | Tests written only for changed function (`getUserById`) + smoke test for `getAllUsers` |

---

## Test Results

| Test name | Status | Duration |
|-----------|--------|----------|
| returns user when id is passed as numeric string "123" | PASS | < 1 ms |
| returns user when id is "456" | PASS | < 1 ms |
| returns user when id is "789" | PASS | < 1 ms |
| REGRESSION: strict equality would have failed — parseInt fixes it | PASS | < 1 ms |
| returns 404 when user id does not exist | PASS | < 1 ms |
| returns 404 for non-numeric id "abc" (parseInt returns NaN) | PASS | < 1 ms |
| returns 404 for id "0" (no user with id 0) | PASS | < 1 ms |
| returns 404 for negative id "-1" | PASS | < 1 ms |
| returns 404 for empty string id "" | PASS | < 1 ms |
| getAllUsers returns all 3 users | PASS | < 1 ms |

**Total**: 10 passed, 0 failed

---

## Test Output

```
> demo-bug-fix@1.0.0 test
> jest

Test Suites: 1 passed, 1 total
Tests:       10 passed, 10 total
Snapshots:   0 total
Time:        0.255 s
Ran all test suites.
```

---

## Coverage of Changed Code

| Changed function | Tests written | Scenarios covered |
|-----------------|---------------|-------------------|
| `getUserById` | 9 | happy path (×3 users), bug regression, 404 for missing ID, non-numeric ID (NaN), boundary values (0, -1, empty string) |
| `getAllUsers` | 1 | smoke test — returns all users (function not changed, included for regression safety) |

---

## References

- Fix summary: `context/bugs/API-404/fix-summary.md`
- Test file: `tests/userController.test.js`
- FIRST skill: `skills/unit-tests-FIRST.md`
