Generate a technical specification for the banking pipeline project using the template in `specification-TEMPLATE-hint.md`.

Steps:
1. Read `specification-TEMPLATE-hint.md` to understand the required structure
2. Read `sample-transactions.json` to understand the input data
3. Write a complete `specification.md` with all 5 sections:
   - High-Level Objective (one sentence)
   - Mid-Level Objectives (4-5 testable requirements)
   - Implementation Notes (Decimal, ISO 4217, logging, PII)
   - Context (beginning and ending state)
   - Low-Level Tasks (one entry per agent with Prompt, File, Function, Details)
4. Ensure each Low-Level Task includes the exact prompt you will give Claude Code
