# Homework 4: 4-Agent Pipeline

**Author**: Denys Mokhrin
**Course**: AI Coding Partner

---

## Overview

This project implements a **4-agent pipeline** for automated bug fixing. The pipeline takes a reported bug, verifies research about it, applies a code fix, reviews security, and generates unit tests — each step performed by a dedicated AI agent.

### Bug Fixed: API-404

**Problem**: `GET /api/users/:id` returned 404 for all valid user IDs.

**Root cause**: `req.params.id` is a string (e.g., `"123"`), but user IDs in the array are numbers (`123`). Strict equality `===` always failed.

**Fix**: `parseInt(userId, 10)` converts the string parameter to a number before comparison.

---

## Agent Pipeline

```
Bug Research Verifier → Bug Implementer → Security Verifier
                                       → Unit Test Generator
```

| Agent | File | Input | Output |
|-------|------|-------|--------|
| Bug Research Verifier | `agents/research-verifier.agent.md` | `codebase-research.md` | `verified-research.md` |
| Bug Implementer | `agents/bug-implementer.agent.md` | `implementation-plan.md` | `fix-summary.md` + code fix |
| Security Verifier | `agents/security-verifier.agent.md` | `fix-summary.md` | `security-report.md` |
| Unit Test Generator | `agents/unit-test-generator.agent.md` | `fix-summary.md` | `test-report.md` + test files |

---

## Skills

| Skill | File | Used by |
|-------|------|---------|
| Research Quality Measurement | `skills/research-quality-measurement.md` | Bug Research Verifier |
| FIRST Principles | `skills/unit-tests-FIRST.md` | Unit Test Generator |

---

## Project Structure

```
homework-4/
├── README.md
├── HOWTORUN.md
├── STUDENT.md
├── agents/
│   ├── research-verifier.agent.md
│   ├── bug-implementer.agent.md
│   ├── security-verifier.agent.md
│   └── unit-test-generator.agent.md
├── skills/
│   ├── research-quality-measurement.md
│   └── unit-tests-FIRST.md
├── context/bugs/API-404/
│   ├── bug-context.md
│   ├── implementation-plan.md
│   ├── fix-summary.md
│   ├── security-report.md
│   ├── test-report.md
│   └── research/
│       ├── codebase-research.md
│       └── verified-research.md
├── demo-bug-fix/          ← Express app (bug fixed)
│   ├── server.js
│   ├── package.json
│   └── src/
│       ├── controllers/userController.js
│       └── routes/users.js
├── tests/
│   └── userController.test.js   ← 10 tests, all pass
└── docs/screenshots/
```

---

## Results

| Agent Output | Status |
|-------------|--------|
| verified-research.md | Research Quality: EXCELLENT (96/100) |
| fix-summary.md | COMPLETE — 1 change applied |
| security-report.md | No CRITICAL/HIGH findings |
| test-report.md | 10/10 tests passed |

---

## How to Run

See [HOWTORUN.md](HOWTORUN.md).
