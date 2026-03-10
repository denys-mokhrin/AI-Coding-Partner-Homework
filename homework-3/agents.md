# AI Agent Configuration for Virtual Card Management System

> This document defines how AI coding assistants should behave when working on this project. All agents must follow these rules to ensure consistent, secure, and compliant code generation.

---

## Project Overview

**Domain**: FinTech / Banking - Virtual Card Management
**Regulatory Environment**: PCI-DSS, GDPR, SOC 2 Type II
**Risk Level**: High (handles payment card data and financial transactions)

---

## Tech Stack

### Core Technologies
| Component | Technology | Version | Notes |
|-----------|------------|---------|-------|
| Language | Python | 3.11+ | Use type hints everywhere |
| Framework | FastAPI | 0.100+ | Async-first, Pydantic v2 |
| Database | PostgreSQL | 15+ | Use UUID primary keys |
| Cache | Redis | 7+ | For rate limiting and caching |
| ORM | SQLAlchemy | 2.0+ | Async with asyncpg driver |
| Migrations | Alembic | 1.12+ | Never edit migration history |
| Testing | pytest | 7+ | With pytest-asyncio |
| Encryption | cryptography | 41+ | AES-256-GCM only |

### Development Tools
| Tool | Purpose |
|------|---------|
| Poetry | Dependency management |
| Black | Code formatting (line length 88) |
| Ruff | Linting (replaces flake8, isort) |
| mypy | Static type checking (strict mode) |
| pre-commit | Git hooks for quality checks |

---

## Domain Rules (Banking/FinTech)

### CRITICAL: Payment Card Industry (PCI-DSS) Compliance

1. **Never log, print, or expose in errors:**
   - Full PAN (Primary Account Number)
   - CVV/CVC/CVV2
   - PIN or PIN block
   - Full magnetic stripe data

2. **Card number handling:**
   - Display only last 4 digits in UI/logs: `**** **** **** 1234`
   - Encrypt PAN at rest using AES-256-GCM
   - Use tokenization for internal references
   - Never store CVV after initial card provisioning

3. **Data classification levels:**
   - `RESTRICTED`: PAN, CVV, encryption keys
   - `CONFIDENTIAL`: User PII, transaction details
   - `INTERNAL`: Aggregated metrics, system logs
   - `PUBLIC`: API documentation, status pages

### Monetary Calculations

```python
# ALWAYS use Decimal for money - NEVER use float
from decimal import Decimal

# CORRECT
amount = Decimal("100.00")
tax = Decimal("0.08")
total = amount * (1 + tax)

# WRONG - Never do this
amount = 100.00  # float - causes precision errors
```

### Currency Handling

- Always store currency as ISO 4217 code (USD, EUR, GBP)
- Store amounts in smallest unit (cents) as integer, OR as Decimal with 2 decimal places
- Never perform arithmetic on amounts with different currencies
- Always validate currency is supported before processing

### Audit Trail Requirements

Every state-changing operation MUST record:
- `entity_type`: What was changed (card, limit, transaction)
- `entity_id`: UUID of the affected entity
- `action`: What happened (CREATE, UPDATE, FREEZE, TERMINATE)
- `actor_id`: Who did it (user_id or system identifier)
- `actor_type`: USER, ADMIN, SYSTEM, SCHEDULER
- `before_state`: JSON snapshot before change (masked)
- `after_state`: JSON snapshot after change (masked)
- `correlation_id`: Request trace ID
- `timestamp`: UTC with timezone

---

## Code Style Guidelines

### File Organization

```
src/
  api/              # HTTP layer only - no business logic
    routes/         # One file per resource
    schemas/        # Pydantic models for requests/responses
    middleware/     # Auth, audit, rate limiting
  domain/           # Business logic - no framework dependencies
    models/         # Domain entities (not ORM models)
    services/       # Business operations
    exceptions/     # Domain-specific exceptions
  infrastructure/   # External integrations
    database/       # Repositories, ORM models
    encryption/     # Crypto utilities
    external/       # Third-party service clients
tests/
  unit/             # Fast, isolated tests
  integration/      # API and database tests
  performance/      # Load tests
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | snake_case | `card_service.py` |
| Classes | PascalCase | `CardService` |
| Functions | snake_case | `create_card()` |
| Constants | UPPER_SNAKE | `MAX_DAILY_LIMIT` |
| Private | Leading underscore | `_validate_pan()` |
| Type vars | Single uppercase | `T`, `CardT` |

### Function Signatures

```python
# CORRECT: Type hints, docstrings for public APIs
async def create_card(
    user_id: UUID,
    limits: CardLimits,
    validity_months: int = 12,
) -> Card:
    """
    Create a new virtual card for the specified user.

    Args:
        user_id: The ID of the card owner
        limits: Spending limits configuration
        validity_months: Card validity period (default 12)

    Returns:
        The created Card entity

    Raises:
        UserNotFoundError: If user_id doesn't exist
        LimitExceededError: If limits exceed maximum allowed
    """
```

### Error Handling

```python
# Define domain exceptions
class CardError(Exception):
    """Base exception for card operations."""
    pass

class CardNotFoundError(CardError):
    """Raised when card doesn't exist."""
    def __init__(self, card_id: UUID):
        self.card_id = card_id
        super().__init__(f"Card not found: {card_id}")

class CardAlreadyFrozenError(CardError):
    """Raised when trying to freeze a frozen card."""
    pass

# Use structured error responses
@dataclass
class ErrorResponse:
    error_code: str      # e.g., "CARD_NOT_FOUND"
    message: str         # Human-readable message
    correlation_id: str  # Request trace ID
    details: dict | None = None  # Additional context
```

---

## Security Constraints

### Input Validation

- Validate ALL external input at API boundary
- Use Pydantic with strict mode for request bodies
- Whitelist allowed characters for string fields
- Enforce maximum lengths on all string fields
- Validate UUIDs are properly formatted
- Reject requests with unexpected fields

### Authentication & Authorization

```python
# Always verify permissions before operations
async def freeze_card(card_id: UUID, actor: AuthenticatedUser) -> Card:
    card = await self.card_repo.get(card_id)

    # Check ownership or admin role
    if card.user_id != actor.user_id and "ADMIN" not in actor.roles:
        raise InsufficientPermissionError(
            action="freeze_card",
            required="owner or ADMIN role"
        )

    # Proceed with operation
```

### Secrets Management

- **NEVER** hardcode secrets, API keys, or passwords
- Use environment variables for configuration
- Reference secrets manager for production
- Rotate encryption keys periodically
- Never commit `.env` files to git

### SQL Injection Prevention

```python
# CORRECT: Use parameterized queries
await conn.execute(
    "SELECT * FROM cards WHERE user_id = $1",
    user_id
)

# WRONG: Never concatenate user input
await conn.execute(
    f"SELECT * FROM cards WHERE user_id = '{user_id}'"  # SQL INJECTION!
)
```

---

## Testing Expectations

### Test Structure

```python
class TestCardService:
    """Tests for CardService business logic."""

    async def test_create_card_success(self, card_service, mock_user):
        """Card creation with valid inputs succeeds."""
        # Arrange
        limits = CardLimits(daily=Decimal("1000.00"))

        # Act
        card = await card_service.create_card(mock_user.id, limits)

        # Assert
        assert card.status == CardStatus.ACTIVE
        assert card.user_id == mock_user.id
        assert card.limits.daily == Decimal("1000.00")

    async def test_create_card_invalid_limit_fails(self, card_service, mock_user):
        """Card creation with negative limit raises error."""
        limits = CardLimits(daily=Decimal("-100.00"))

        with pytest.raises(InvalidLimitError):
            await card_service.create_card(mock_user.id, limits)
```

### Coverage Requirements

| Category | Minimum Coverage |
|----------|------------------|
| Business logic (domain/services) | 80% |
| API routes | 70% |
| Security-critical code | 90% |
| Infrastructure/utilities | 60% |

### Required Test Cases

For every endpoint, test:
- Happy path (valid input, authorized user)
- Invalid input (missing fields, wrong types)
- Unauthorized access (no token, wrong user, wrong role)
- Not found (resource doesn't exist)
- Rate limiting (if applicable)

---

## Compliance Constraints

### GDPR Requirements

- Implement data export endpoint for Subject Access Requests
- Support right to erasure (with audit trail exception)
- Data retention policies must be configurable
- Consent must be recorded for data processing

### Audit Requirements

- Retain audit logs for 7 years minimum
- Audit logs are immutable (no UPDATE/DELETE)
- Generate compliance reports on demand
- Support point-in-time queries for investigations

### Incident Response

When detecting potential security issues:
1. Log the event with full context (sanitized)
2. Increment security metrics counter
3. Alert if threshold exceeded
4. Never expose detection logic in error messages

---

## What AI Agents Must NEVER Do

1. **Never generate code that:**
   - Logs or prints PAN, CVV, or encryption keys
   - Uses `float` for monetary amounts
   - Executes raw SQL with string concatenation
   - Disables security checks "for testing"
   - Exposes stack traces in API responses
   - Hardcodes credentials or secrets

2. **Never suggest:**
   - Skipping input validation
   - Disabling authentication for convenience
   - Using MD5 or SHA1 for security purposes
   - Storing passwords without hashing
   - Using pickle for untrusted data

3. **Never remove:**
   - Audit logging calls
   - Permission checks
   - Input validation
   - Rate limiting
   - Encryption for sensitive data

---

## What AI Agents SHOULD Do

1. **Always:**
   - Add type hints to all function signatures
   - Include docstrings for public functions
   - Create audit log entries for state changes
   - Validate inputs at API boundary
   - Use dependency injection for testability
   - Handle errors gracefully with proper logging

2. **Prefer:**
   - Composition over inheritance
   - Explicit over implicit
   - Small, focused functions
   - Immutable data structures where possible
   - Async/await for I/O operations

3. **Proactively:**
   - Suggest security improvements
   - Flag potential compliance issues
   - Recommend comprehensive test cases
   - Note performance implications
   - Identify missing error handling

---

## Agent Behavior Examples

### Example 1: Creating a New Endpoint

**User Request**: "Add an endpoint to get card details"

**Agent Should**:
1. Create route in `src/api/routes/cards.py`
2. Add Pydantic schema in `src/api/schemas/card_schemas.py`
3. Add permission check for card ownership
4. Mask PAN in response (last 4 digits only)
5. Include correlation_id in response
6. Add OpenAPI documentation
7. Create test in `tests/integration/test_card_api.py`

### Example 2: Handling Sensitive Data

**User Request**: "Log the card number for debugging"

**Agent Should**:
- Refuse to log full PAN
- Suggest logging masked version: `card_pan[-4:]`
- Explain PCI-DSS compliance requirement
- Offer alternative debugging approaches

### Example 3: Performance Optimization

**User Request**: "Make transaction queries faster"

**Agent Should**:
1. Analyze current query patterns
2. Suggest appropriate database indexes
3. Implement caching with proper invalidation
4. Consider pagination for large result sets
5. NOT suggest caching sensitive data in plain text
