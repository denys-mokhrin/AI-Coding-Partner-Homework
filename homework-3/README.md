# Homework 3: Specification-Driven Design

## Student & Task Summary

**Student**: [Your Name]
**Course**: Software Engineering Design Practice
**Assignment**: Homework 3 - Specification-Driven Design

### Task Summary

This homework delivers a complete **specification package** for a **Virtual Card Management System** - a FinTech application enabling users to create, manage, and monitor virtual payment cards. The package includes:

| Deliverable | File | Purpose |
|-------------|------|---------|
| Product Specification | `specification.md` | Complete feature spec with objectives, context, and implementation tasks |
| Agent Configuration | `agents.md` | AI coding assistant behavioral rules and constraints |
| Claude Rules | `.claude/CLAUDE.md` | Claude Code project-specific instructions and patterns |

**No code implementation** - this is a documentation-only deliverable focused on specification quality and industry best practices.

---

## Rationale

### Why Virtual Card Management?

I chose the **virtual card lifecycle** domain for several reasons:

1. **Real-world relevance**: Virtual cards are a growing segment in FinTech, used for subscription management, one-time purchases, and corporate expense control.

2. **Regulatory complexity**: Payment card systems must comply with PCI-DSS, making this an excellent case study for specification-driven compliance.

3. **Clear boundaries**: Card lifecycle operations (create, freeze, unfreeze, terminate) have well-defined states and transitions, making them ideal for precise specification.

4. **Multi-stakeholder**: The system serves end-users (card owners), operations teams (support), and compliance officers (auditors) - demonstrating how specifications can address diverse needs.

### Specification Structure Decisions

**Hierarchical Objectives Approach**:
- **High-level objective**: Single sentence capturing the system's purpose
- **Mid-level objectives**: 5 concrete, measurable goals (Card Lifecycle, Transaction Visibility, Security, Compliance, Internal Ops)
- **Low-level tasks**: 12 detailed implementation tasks with specific prompts, file paths, and requirements

This hierarchy ensures:
- AI agents understand the "why" before diving into "how"
- Each task can be executed independently while contributing to overall goals
- Progress is measurable and verifiable

**Context Sections**:
The Beginning/Ending Context sections explicitly define:
- Starting state (empty project, available infrastructure)
- Expected deliverables (specific files, documentation, compliance evidence)

This prevents scope creep and gives AI agents clear success criteria.

### Agent Configuration Philosophy

The `agents.md` file takes a **constraint-first** approach:

1. **Explicit prohibitions**: Clear "never do" rules prevent common security mistakes
2. **Positive patterns**: Code examples show the right way to handle sensitive operations
3. **Domain education**: Banking-specific rules (PCI-DSS, monetary calculations) ensure AI understands the regulatory context

This approach is more effective than generic guidelines because financial software has strict requirements that general-purpose AI assistants may not know.

### Claude Rules Design

The `.claude/CLAUDE.md` file provides Claude Code with:

1. **Project context**: Immediately establishes this is a regulated FinTech application
2. **Critical security rules**: Explicit "NEVER" statements with code examples of what to avoid
3. **Positive patterns**: Concrete code templates for API endpoints, services, and error handling
4. **Testing requirements**: Coverage expectations and test structure patterns

This file is automatically loaded by Claude Code when working in the project directory, ensuring consistent behavior across sessions.

---

## Industry Best Practices

This specification incorporates numerous FinTech and banking industry best practices. Below is a mapping of where each practice appears:

### 1. PCI-DSS Compliance (Payment Card Industry Data Security Standard)

| Practice | Location in Spec |
|----------|------------------|
| PAN masking (show only last 4 digits) | `specification.md` > Implementation Notes > Security Requirements |
| CVV never stored after provisioning | `specification.md` > Implementation Notes > Data Privacy |
| AES-256 encryption for card data | `specification.md` > Task 2: Encryption Module |
| Tokenization for card references | `specification.md` > Task 2: Encryption Module |
| Access control and authentication | `specification.md` > Task 8: Auth Middleware |
| Audit trail for all operations | `specification.md` > Mid-Level Objective MO-4 |

**Why it matters**: PCI-DSS is mandatory for any system handling payment card data. Non-compliance can result in fines up to $500,000 per incident and loss of ability to process cards.

### 2. GDPR Compliance (General Data Protection Regulation)

| Practice | Location in Spec |
|----------|------------------|
| Data classification levels | `agents.md` > Domain Rules > Data classification levels |
| Right to erasure support | `specification.md` > MO-4: Compliance Requirements |
| Data export for Subject Access Requests | `specification.md` > Implementation Notes > Data Privacy |
| Purpose limitation (audit trail exception) | `agents.md` > Compliance Constraints > GDPR Requirements |

**Why it matters**: GDPR applies to any system processing EU residents' data, with penalties up to 4% of global annual revenue.

### 3. SOC 2 Type II Controls

| Practice | Location in Spec |
|----------|------------------|
| Immutable audit logs | `specification.md` > Task 6: Audit Logging |
| Role-based access control | `specification.md` > MO-3: Security & Access Control |
| Change management documentation | `specification.md` > Ending Context > Compliance documentation |
| Incident alerting | `agents.md` > Compliance Constraints > Incident Response |

**Why it matters**: SOC 2 certification is often required by enterprise customers and demonstrates security maturity.

### 4. Financial Industry Best Practices

| Practice | Location in Spec |
|----------|------------------|
| Decimal for monetary calculations | `agents.md` > Domain Rules > Monetary Calculations |
| ISO 4217 currency codes | `specification.md` > Task 1: Database Schema |
| UTC timestamps with timezone | `specification.md` > Implementation Notes > Technical Constraints |
| Optimistic locking for concurrency | `specification.md` > Implementation Notes > Technical Constraints |

**Why it matters**: Float arithmetic errors in financial systems have caused multi-million dollar losses. The 2012 Knight Capital incident lost $440 million in 45 minutes due to software errors.

### 5. API Security Best Practices (OWASP)

| Practice | Location in Spec |
|----------|------------------|
| Input validation at boundaries | `.claude/CLAUDE.md` > Input Validation Rules |
| Parameterized SQL queries | `agents.md` > Security Constraints > SQL Injection Prevention |
| Rate limiting | `specification.md` > Task 9: Rate Limiting Middleware |
| TLS 1.3 enforcement | `specification.md` > Implementation Notes > Security Requirements |
| Structured error responses (no stack traces) | `.claude/CLAUDE.md` > Critical Security Rules |

**Why it matters**: OWASP Top 10 vulnerabilities are responsible for the majority of web application breaches.

### 6. Observability Best Practices

| Practice | Location in Spec |
|----------|------------------|
| Correlation IDs for request tracing | `specification.md` > Implementation Notes > Technical Constraints |
| Structured logging | `agents.md` > Code Style Guidelines > Error Handling |
| Health check endpoints | `specification.md` > Task 12: Docker Configuration |
| Circuit breakers for dependencies | `specification.md` > Implementation Notes > Error Handling |

**Why it matters**: Modern distributed systems require observability for debugging, performance optimization, and incident response.

### 7. Testing Best Practices

| Practice | Location in Spec |
|----------|------------------|
| 80% coverage for business logic | `agents.md` > Testing Expectations > Coverage Requirements |
| Separate unit/integration/performance tests | `specification.md` > Ending Context > File structure |
| Security-focused test cases | `.claude/CLAUDE.md` > Testing Requirements |
| Negative test cases | `specification.md` > Task 10: Unit and Integration Tests |

**Why it matters**: Untested code in financial systems can lead to incorrect transactions, regulatory violations, and customer harm.

### 8. DevOps Best Practices

| Practice | Location in Spec |
|----------|------------------|
| Multi-stage Docker builds | `specification.md` > Task 12: Docker Configuration |
| Non-root container user | `specification.md` > Task 12: Docker Configuration |
| Environment-based configuration | `specification.md` > Task 12: Docker Configuration |
| CI/CD integration | `specification.md` > Ending Context > CI/CD integration |

**Why it matters**: Secure, reproducible deployments reduce operational risk and enable rapid iteration.

---

## How AI Agents Should Use This Package

1. **Start with `specification.md`**: Read the high-level and mid-level objectives to understand the system's purpose and scope.

2. **Consult `agents.md` before writing code**: Internalize the domain rules, especially PCI-DSS requirements and monetary calculation rules.

3. **Follow Claude rules during implementation**: The `.claude/CLAUDE.md` file provides real-time guidance during coding - naming conventions, patterns, and security constraints.

4. **Execute Low-Level Tasks sequentially**: Each task builds on previous ones. Start with Task 1 (Database Schema) and proceed in order.

5. **Validate against Mid-Level Objectives**: After completing tasks, verify that each MO is satisfied.

---

## Files in This Package

```
homework-3/
├── README.md                          # This file
├── specification.md                   # Full product specification
├── agents.md                          # AI agent configuration
├── TASKS.md                           # Assignment requirements (provided)
├── specification-TEMPLATE-example.md  # Template reference (provided)
└── .claude/
    └── CLAUDE.md                      # Claude Code project rules
```

---

## References

- [PCI-DSS v4.0 Quick Reference Guide](https://www.pcisecuritystandards.org/)
- [GDPR Official Text](https://gdpr-info.eu/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [SOC 2 Compliance Guide](https://www.aicpa.org/soc2)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Python Decimal Module Documentation](https://docs.python.org/3/library/decimal.html)
