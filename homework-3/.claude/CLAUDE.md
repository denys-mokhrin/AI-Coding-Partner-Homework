# Claude Code Instructions for Virtual Card Management System

## Project Context

This is a **regulated FinTech application** handling virtual payment cards. All code must be PCI-DSS compliant and follow banking industry security standards.

**Domain**: Virtual Card Management (create, freeze/unfreeze, set limits, view transactions)
**Regulatory Environment**: PCI-DSS, GDPR, SOC 2 Type II
**Risk Level**: High - handles payment card data and financial transactions

---

## Tech Stack

- **Python 3.11+** with strict type hints
- **FastAPI** for API development (async-first)
- **SQLAlchemy 2.0** async ORM with PostgreSQL
- **Pydantic v2** for validation (strict mode)
- **pytest** with pytest-asyncio for testing
- **Redis** for caching and rate limiting

---

## Critical Security Rules

### NEVER Generate Code That:

1. **Logs or exposes sensitive card data:**
   ```python
   # FORBIDDEN
   logger.info(f"Processing card: {card_number}")
   logger.debug(f"CVV: {cvv}")
   print(f"PAN: {pan}")
   ```

2. **Uses float for monetary amounts:**
   ```python
   # FORBIDDEN - causes precision errors
   amount = 100.50

   # REQUIRED
   from decimal import Decimal
   amount = Decimal("100.50")
   ```

3. **Concatenates user input into SQL:**
   ```python
   # FORBIDDEN - SQL injection vulnerability
   query = f"SELECT * FROM cards WHERE id = '{card_id}'"

   # REQUIRED - parameterized queries
   query = "SELECT * FROM cards WHERE id = $1"
   await conn.execute(query, card_id)
   ```

4. **Hardcodes secrets or credentials:**
   ```python
   # FORBIDDEN
   api_key = "sk_live_abc123..."
   db_password = "secret123"

   # REQUIRED
   import os
   api_key = os.environ["API_KEY"]
   ```

5. **Exposes stack traces in API responses:**
   ```python
   # FORBIDDEN
   return {"error": str(exception), "traceback": traceback.format_exc()}

   # REQUIRED
   return {"error_code": "INTERNAL_ERROR", "correlation_id": correlation_id}
   ```

---

## PCI-DSS Compliance Rules

### Card Data Handling

1. **PAN (Primary Account Number)**
   - Never log full PAN under any circumstances
   - Always encrypt at rest using AES-256-GCM
   - Display only last 4 digits: `**** **** **** {pan[-4:]}`
   - Use tokenization for internal references

2. **CVV/CVC**
   - Never store after initial card provisioning
   - Never log, even partially
   - Process in memory only, then immediately discard

3. **Encryption Keys**
   - Store in environment variables or secrets manager
   - Never commit to version control
   - Implement key rotation capability

### Masking Pattern

```python
def mask_pan(pan: str) -> str:
    """Mask PAN showing only last 4 digits."""
    if len(pan) < 4:
        return "****"
    return f"**** **** **** {pan[-4:]}"
```

---

## Code Patterns to Follow

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | snake_case | `card_service.py` |
| Classes | PascalCase | `CardService` |
| Functions | snake_case | `create_card` |
| Constants | UPPER_SNAKE | `MAX_DAILY_LIMIT` |
| Private | _prefix | `_validate_pan` |

### API Endpoint Pattern

```python
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

router = APIRouter(prefix="/api/v1/cards", tags=["cards"])

@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: UUID,
    current_user: AuthenticatedUser = Depends(get_current_user),
    card_service: CardService = Depends(get_card_service),
) -> CardResponse:
    """Retrieve card details by ID."""
    card = await card_service.get_card(card_id, current_user)
    return CardResponse.from_domain(card)  # Masks sensitive data
```

### Service Layer Pattern

```python
@dataclass
class CardService:
    card_repo: CardRepository
    audit_service: AuditService

    async def freeze_card(
        self,
        card_id: UUID,
        actor: AuthenticatedUser,
        reason: str,
    ) -> Card:
        card = await self.card_repo.get(card_id)
        if not card:
            raise CardNotFoundError(card_id)

        if not self._can_access(card, actor):
            raise InsufficientPermissionError()

        before_state = card.to_audit_dict()
        card.freeze()
        await self.card_repo.save(card)

        await self.audit_service.log(
            entity_type="card",
            entity_id=card_id,
            action="FREEZE",
            actor=actor,
            before_state=before_state,
            after_state=card.to_audit_dict(),
            reason=reason,
        )

        return card
```

### Domain Exception Pattern

```python
class CardError(Exception):
    """Base exception for card operations."""
    error_code: str = "CARD_ERROR"

class CardNotFoundError(CardError):
    error_code = "CARD_NOT_FOUND"

    def __init__(self, card_id: UUID):
        self.card_id = card_id
        super().__init__(f"Card not found: {card_id}")

class CardAlreadyFrozenError(CardError):
    error_code = "CARD_ALREADY_FROZEN"
```

---

## Audit Trail Requirements

Every state-changing operation MUST create an audit log entry:

```python
@dataclass
class AuditEntry:
    entity_type: str      # "card", "transaction", "user"
    entity_id: UUID       # ID of affected entity
    action: str           # "CREATE", "UPDATE", "FREEZE", "TERMINATE"
    actor_id: UUID        # Who performed action
    actor_type: str       # "USER", "ADMIN", "SYSTEM"
    before_state: dict    # Snapshot before (sensitive fields masked)
    after_state: dict     # Snapshot after (sensitive fields masked)
    correlation_id: str   # Request trace ID
    timestamp: datetime   # UTC timezone-aware
    reason: str | None    # Required for admin actions
```

---

## Input Validation Rules

Always validate at API boundaries using Pydantic strict mode:

```python
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class CreateCardRequest(BaseModel):
    user_id: UUID
    daily_limit: Decimal = Field(gt=0, le=Decimal("50000.00"))
    monthly_limit: Decimal = Field(gt=0, le=Decimal("200000.00"))
    currency: str = Field(pattern=r"^[A-Z]{3}$")

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        allowed = {"USD", "EUR", "GBP", "CAD"}
        if v not in allowed:
            raise ValueError(f"Currency must be one of: {allowed}")
        return v

    model_config = {
        "strict": True,
        "extra": "forbid",  # Reject unexpected fields
    }
```

---

## Authorization Pattern

Always verify permissions before operations:

```python
async def get_card(self, card_id: UUID, actor: AuthenticatedUser) -> Card:
    card = await self.card_repo.get(card_id)

    is_owner = card.user_id == actor.user_id
    is_admin = "ADMIN" in actor.roles

    if not (is_owner or is_admin):
        logger.warning(
            "Unauthorized card access attempt",
            extra={"card_id": str(card_id), "actor_id": str(actor.user_id)}
        )
        raise CardNotFoundError(card_id)  # Don't reveal existence

    return card
```

---

## Testing Requirements

### Test Structure

```python
class TestCardService:
    async def test_freeze_card_success(self, card_service, active_card, mock_user):
        result = await card_service.freeze_card(
            active_card.id, mock_user, reason="User requested"
        )
        assert result.status == CardStatus.FROZEN

    async def test_freeze_card_not_found(self, card_service, mock_user):
        with pytest.raises(CardNotFoundError):
            await card_service.freeze_card(uuid4(), mock_user, reason="Test")

    async def test_freeze_card_wrong_user_forbidden(self, card_service, card, other_user):
        with pytest.raises(CardNotFoundError):
            await card_service.freeze_card(card.id, other_user, reason="Test")
```

### Coverage Requirements

| Category | Minimum |
|----------|---------|
| Business logic | 80% |
| Security-critical code | 90% |
| API routes | 70% |

---

## What to Include in Every Change

1. **Type hints** on all parameters and return values
2. **Input validation** at API boundaries
3. **Audit logging** for state changes
4. **Error handling** with domain exceptions
5. **Tests** for new functionality

---

## What to Avoid

- Generic exception handlers that swallow errors
- Print statements (use structured logging)
- Synchronous database calls in async context
- Magic numbers (use named constants)
- Commented-out code
- TODO comments without issue references
- Using `Any` type when specific types are possible
- Mutable default arguments in function signatures
