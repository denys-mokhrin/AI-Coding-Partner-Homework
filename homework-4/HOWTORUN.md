# How to Run

## Prerequisites

- Node.js 18+
- npm

---

## Run the Application

```bash
cd homework-4/demo-bug-fix
npm install
npm start
```

Server starts at `http://localhost:3000`.

### Available endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/health` | Health check |
| GET | `/api/users` | Get all users |
| GET | `/api/users/:id` | Get user by ID |

### Example requests

```bash
curl http://localhost:3000/api/users
curl http://localhost:3000/api/users/123
curl http://localhost:3000/api/users/456
curl http://localhost:3000/api/users/999   # → 404
```

---

## Run Tests

```bash
cd homework-4/demo-bug-fix
npm install
npm test
```

Expected output:
```
Tests: 10 passed, 10 total
```

---

## Run the Agent Pipeline (conceptual)

The 4-agent pipeline is defined as agent markdown files in `agents/`. Each agent reads from and writes to `context/bugs/API-404/`.

Pipeline order:
1. **Bug Research Verifier** (`agents/research-verifier.agent.md`)
   - Reads: `context/bugs/API-404/research/codebase-research.md`
   - Writes: `context/bugs/API-404/research/verified-research.md`

2. **Bug Implementer** (`agents/bug-implementer.agent.md`)
   - Reads: `context/bugs/API-404/implementation-plan.md`
   - Writes: `context/bugs/API-404/fix-summary.md`
   - Applies: code changes to `demo-bug-fix/src/controllers/userController.js`

3. **Security Verifier** (`agents/security-verifier.agent.md`)
   - Reads: `context/bugs/API-404/fix-summary.md` + changed files
   - Writes: `context/bugs/API-404/security-report.md`

4. **Unit Test Generator** (`agents/unit-test-generator.agent.md`)
   - Reads: `context/bugs/API-404/fix-summary.md` + changed files
   - Writes: `tests/userController.test.js` + `context/bugs/API-404/test-report.md`
