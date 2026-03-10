# Implementation Plan: Bug API-404

**Planner**: Bug Planner Agent
**Date**: 2026-03-10
**Based on**: `research/verified-research.md` (Quality: EXCELLENT, 96/100)

---

## Summary

Fix the type coercion mismatch in `getUserById` by converting the route parameter string to an integer before comparison.

---

## Changes

### Change 1 — Fix type coercion in `getUserById`

**File**: `demo-bug-fix/src/controllers/userController.js`
**Location**: Line 23, inside function `getUserById`

**Before**:
```js
const user = users.find(u => u.id === userId);
```

**After**:
```js
const user = users.find(u => u.id === parseInt(userId, 10));
```

**Reason**: `req.params.id` is always a string. The users array stores IDs as numbers. `parseInt(userId, 10)` converts the string to a base-10 integer. If `userId` is non-numeric (e.g., `"abc"`), `parseInt` returns `NaN`, and `u.id === NaN` is always `false`, which correctly results in a 404 — no additional guard needed.

---

## Test Command

After applying Change 1, run:

```bash
npm test
```

Expected: all tests pass.

For manual smoke test:
```bash
# Start server in one terminal
npm start

# In another terminal
curl http://localhost:3000/api/users/123
# Expected: {"id":123,"name":"Alice Smith","email":"alice@example.com"}

curl http://localhost:3000/api/users/999
# Expected: {"error":"User not found"} with 404

curl http://localhost:3000/api/users/abc
# Expected: {"error":"User not found"} with 404
```

---

## Rollback

If the fix causes regressions, revert line 23 to:
```js
const user = users.find(u => u.id === userId);
```

---

## References

- Verified research: `context/bugs/API-404/research/verified-research.md`
- Target file: `demo-bug-fix/src/controllers/userController.js`
