# Bug Implementer Agent — Fix Applied

**Bug ID**: API-404
**File**: `demo-bug-fix/src/controllers/userController.js`
**Date**: 2026-03-23
**Overall Status**: COMPLETE

## Change Made

| Field | Value |
|-------|-------|
| File | `demo-bug-fix/src/controllers/userController.js` |
| Location | Line 23 — function `getUserById` |
| Test result | PASS |

**Before:**
```js
const user = users.find(u => u.id === userId);
```

**After:**
```js
const user = users.find(u => u.id === parseInt(userId, 10));
```

## Root Cause

`req.params.id` returns a string (e.g. `"123"`), but `u.id` is a number (`123`).
Strict equality `"123" === 123` is always `false` → always 404.
Fix: `parseInt(userId, 10)` converts the string to a number before comparison.

## Test Output

```
> demo-bug-fix@1.0.0 test
> jest --rootDir=.. --testMatch=**/tests/**/*.test.js

Test Suites: 1 passed, 1 total
Tests:       10 passed, 10 total
Snapshots:   0 total
Time:        0.134 s
Ran all test suites.
```
