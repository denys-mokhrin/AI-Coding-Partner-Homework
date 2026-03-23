# Skill: Research Quality Measurement

## Purpose

This skill defines a standardized framework for measuring and reporting the quality of bug research output.
Use this skill when producing `verified-research.md` to assign a consistent quality level to the research being verified.

---

## Quality Levels

| Level | Label | Score Range | Description |
|-------|-------|-------------|-------------|
| 5 | **EXCELLENT** | 90–100 | All file:line references verified, all code snippets match source, root cause clearly explained, no discrepancies found. Research is immediately actionable. |
| 4 | **GOOD** | 75–89 | Most references verified, minor discrepancies (e.g. off-by-one line numbers), root cause identified, small gaps in explanation. Actionable with minor clarifications. |
| 3 | **ADEQUATE** | 55–74 | Core references correct, some snippets outdated or misquoted, root cause present but incomplete. Requires additional verification before implementation. |
| 2 | **POOR** | 30–54 | Multiple incorrect references or missing snippets, root cause vague or partially wrong. Significant rework needed before implementation. |
| 1 | **UNACCEPTABLE** | 0–29 | Majority of references wrong or absent, root cause missing or incorrect. Research must be redone entirely. |

---

## Scoring Criteria

Each criterion is scored 0–20 points (max 100 total):

| # | Criterion | Max Points |
|---|-----------|-----------|
| 1 | **File references** — every `file:line` citation exists and is accurate | 20 |
| 2 | **Code snippets** — quoted code matches actual source file content | 20 |
| 3 | **Root cause** — root cause is identified correctly and completely | 20 |
| 4 | **Completeness** — all affected files and call paths are covered | 20 |
| 5 | **Clarity** — findings are clearly written and unambiguous | 20 |

---

## Usage Instructions

1. Evaluate each criterion independently and assign a score (0–20).
2. Sum all scores to get a total (0–100).
3. Map the total to the corresponding Quality Level.
4. In `verified-research.md`, include:
   - The numeric score per criterion
   - The total score
   - The Quality Level label
   - A one-sentence reasoning statement

---

## Example Output Block

```
## Research Quality Assessment

| Criterion | Score |
|-----------|-------|
| File references | 18/20 |
| Code snippets | 20/20 |
| Root cause | 20/20 |
| Completeness | 17/20 |
| Clarity | 19/20 |
| **Total** | **94/100** |

**Quality Level**: EXCELLENT
**Reasoning**: All references verified and accurate; root cause correctly identified as type coercion mismatch; minor point deducted for not listing the `/health` route as out-of-scope note.
```
