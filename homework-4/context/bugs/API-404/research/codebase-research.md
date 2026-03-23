# Codebase Research: Bug API-404

**Researcher**: Bug Researcher Agent
**Date**: 2026-03-10
**Bug**: GET /api/users/:id returns 404 for valid user IDs

---

## Summary

The root cause of bug API-404 is a **type coercion mismatch** in the `getUserById` function. `req.params.id` returns a string (e.g., `"123"`), while user objects in the in-memory array store IDs as numbers (e.g., `123`). The strict equality operator (`===`) is used in the `.find()` call, which means `"123" === 123` evaluates to `false`, causing the user to never be found.

---

## Affected Files

### 1. `demo-bug-fix/src/controllers/userController.js`

**Location of bug**: Line 23

```js
const user = users.find(u => u.id === userId);
```

**Problem**: `userId` is a string from `req.params.id` (line 19), but `u.id` is a number in the `users` array (lines 8–11).

**Users array** (lines 7–11):
```js
const users = [
  { id: 123, name: 'Alice Smith', email: 'alice@example.com' },
  { id: 456, name: 'Bob Johnson', email: 'bob@example.com' },
  { id: 789, name: 'Charlie Brown', email: 'charlie@example.com' }
];
```

**userId assignment** (line 19):
```js
const userId = req.params.id;
```

Express route parameters are always strings. Strict equality between string `"123"` and number `123` returns `false`.

---

### 2. `demo-bug-fix/src/routes/users.js`

Route definition (line 14):
```js
router.get('/api/users/:id', userController.getUserById);
```

This confirms that `:id` is an Express route parameter, which is always delivered as a string to the controller.

---

### 3. `demo-bug-fix/server.js`

Routes mounted (line 16):
```js
app.use(userRoutes);
```

No route prefix is applied here — routes use their own `/api/users` prefix defined in `users.js`.

---

## Root Cause

**File**: `demo-bug-fix/src/controllers/userController.js`
**Line**: 23
**Type**: Type mismatch (string vs. number)

```js
// BUG: userId is string "123", u.id is number 123
// "123" === 123  → false (always)
const user = users.find(u => u.id === userId);
```

**Fix**: Parse `userId` to integer before comparison:
```js
const user = users.find(u => u.id === parseInt(userId, 10));
```

---

## Why `GET /api/users` Works

The `getAllUsers` function (lines 37–39) does not perform any ID lookup — it simply returns the entire `users` array. That's why the list endpoint works while the single-user endpoint does not.

---

## Call Chain

```
HTTP GET /api/users/123
  → users.js:14  router.get('/api/users/:id', getUserById)
  → userController.js:18  getUserById(req, res)
  → userController.js:19  userId = req.params.id   // "123" (string)
  → userController.js:23  users.find(u => u.id === userId)  // "123" === 123 → false
  → userController.js:25  res.status(404).json(...)  // always triggered
```

---

## References

- `demo-bug-fix/src/controllers/userController.js` — lines 7–29
- `demo-bug-fix/src/routes/users.js` — lines 10–14
- `demo-bug-fix/server.js` — lines 1–31
