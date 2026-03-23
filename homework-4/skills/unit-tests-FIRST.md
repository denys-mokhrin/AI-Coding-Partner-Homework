# Skill: FIRST Principles for Unit Tests

## Purpose

This skill defines the **FIRST** principles that every generated unit test must satisfy.
The Unit Test Generator agent must apply this skill when writing tests and verify each principle before finalizing the test suite.

---

## FIRST Principles

### F — Fast
- Tests must run in milliseconds (< 100 ms per test).
- No real network calls, file I/O, or database connections — use mocks/stubs.
- The full test suite should complete in under 5 seconds.

### I — Independent
- Each test must be self-contained and executable in any order.
- Tests must not share mutable state.
- Use `beforeEach`/`afterEach` to reset state between tests.
- No test should depend on another test having run first.

### R — Repeatable
- Tests must produce the same result every time, regardless of environment.
- No dependency on system time, random values, or environment variables (mock them if needed).
- Tests must pass on any developer machine, CI/CD, or OS.

### S — Self-validating
- Tests must produce a clear binary outcome: **pass** or **fail** — no manual inspection required.
- Use explicit assertions (`expect(...).toBe(...)`, `expect(...).toEqual(...)`, etc.).
- Avoid `console.log` as a substitute for assertions.

### T — Timely
- Tests must be written for the changed/added code only.
- Tests should be written as part of the fix, not as an afterthought.
- Focus on edge cases introduced by the fix (type boundaries, null inputs, invalid IDs).

---

## Checklist (use before submitting test-report.md)

- [ ] Each test runs in < 100 ms
- [ ] Tests can run in any order and still pass
- [ ] No mutable shared state between tests
- [ ] Tests produce identical results on every run
- [ ] Every test has at least one explicit `expect` assertion
- [ ] Tests cover only changed code (no unrelated legacy tests)
- [ ] Edge cases for the bug fix are covered

---

## Example FIRST-compliant test

```js
// F: fast — no I/O, pure function or mock
// I: independent — uses beforeEach to reset
// R: repeatable — no Date.now() or Math.random()
// S: self-validating — explicit expect
// T: timely — tests the exact fix (parseInt coercion)

describe('getUserById', () => {
  it('should find user when id is passed as string (type coercion fix)', async () => {
    const req = { params: { id: '123' } };
    const res = { json: jest.fn(), status: jest.fn().mockReturnThis() };

    await getUserById(req, res);

    expect(res.json).toHaveBeenCalledWith(
      expect.objectContaining({ id: 123, name: 'Alice Smith' })
    );
  });
});
```
