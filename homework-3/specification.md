# Virtual Card Management System Specification

> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

Build a secure, compliant Virtual Card Management System that enables end-users to create, manage, and monitor virtual payment cards while providing internal operations and compliance teams with full audit capabilities and control mechanisms.

---

## Mid-Level Objectives

### MO-1: Card Lifecycle Management
- Users can create new virtual cards with customizable spending limits and validity periods
- Users can freeze/unfreeze cards instantly with immediate effect on transaction authorization
- Users can set and modify per-transaction, daily, and monthly spending limits
- Users can terminate cards permanently with proper closure audit trail

### MO-2: Transaction Visibility & Monitoring
- Users can view real-time transaction history with merchant details, amounts, and status
- System categorizes transactions automatically (e.g., travel, dining, subscriptions)
- Users receive configurable notifications for transactions exceeding thresholds
- Internal ops can view aggregated transaction patterns for fraud detection

### MO-3: Security & Access Control
- All card operations require multi-factor authentication
- Card numbers and CVVs are encrypted at rest and masked in UI/logs
- Role-based access control separates end-user, ops, and compliance permissions
- Session management with automatic timeout and re-authentication

### MO-4: Compliance & Audit Requirements
- All state changes generate immutable audit log entries with actor, timestamp, and before/after states
- PCI-DSS compliant data handling for cardholder data
- GDPR-compliant data retention and right-to-erasure support
- Regulatory reporting capabilities for suspicious activity (SAR-ready)

### MO-5: Internal Operations Dashboard
- Ops team can search and filter cards by status, user, limit, or creation date
- Ops can override card status in emergency situations with mandatory reason logging
- Compliance team can generate audit reports for specific time periods or users
- System health metrics and alerting for failed transactions or service degradation

---

## Implementation Notes

### Technical Constraints
- Use Decimal types (never float) for all monetary calculations to prevent precision errors
- All timestamps must be stored in UTC with timezone-aware datetime objects
- API responses must include request correlation IDs for traceability
- Database transactions must be ACID-compliant; use optimistic locking for concurrent updates

### Security Requirements
- Cardholder data (PAN, CVV, expiry) must be encrypted using AES-256-GCM at rest
- Use tokenization for card references in non-payment contexts
- Implement rate limiting: 10 requests/second per user, 1000 requests/second globally
- All API endpoints require TLS 1.3; reject older protocols
- Input validation on all fields; reject requests with unexpected parameters

### Data Privacy
- PAN must be masked in all logs and UI displays (show only last 4 digits)
- CVV must never be stored after initial card creation
- Implement data classification: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
- Support data export in machine-readable format for GDPR Subject Access Requests

### Error Handling
- Use structured error responses with error codes, messages, and correlation IDs
- Never expose internal system details or stack traces in error responses
- Log all errors with full context but sanitize sensitive data before logging
- Implement circuit breakers for external service dependencies (payment processor, fraud engine)

### Testing Requirements
- Unit test coverage minimum 80% for business logic
- Integration tests for all API endpoints with positive and negative cases
- Performance tests: system must handle 500 concurrent card operations
- Security tests: automated vulnerability scanning in CI/CD pipeline

---

## Context

### Beginning Context

**Existing Files/Systems:**
- Empty project directory with initialized git repository
- Python 3.11+ environment with pip/poetry available
- PostgreSQL 15+ database instance (empty schema)
- Redis instance for caching and rate limiting
- CI/CD pipeline skeleton (GitHub Actions)

**Available Resources:**
- Payment processor sandbox API credentials
- Fraud detection service API (mock available)
- Email/SMS notification service endpoints
- Internal identity provider (OAuth 2.0 / OIDC)

**Organizational Context:**
- Development team familiar with Python/FastAPI
- Existing authentication service can be integrated
- Compliance team requires weekly audit report capability

### Ending Context

**Files to be Created:**
```
src/
  api/
    __init__.py
    routes/
      cards.py           # Card CRUD and lifecycle endpoints
      transactions.py    # Transaction query endpoints
      admin.py           # Internal ops endpoints
    middleware/
      auth.py            # Authentication middleware
      audit.py           # Audit logging middleware
      rate_limit.py      # Rate limiting middleware
  domain/
    __init__.py
    models/
      card.py            # Card domain model
      transaction.py     # Transaction domain model
      audit_log.py       # Audit log model
    services/
      card_service.py    # Card business logic
      transaction_service.py
      notification_service.py
  infrastructure/
    __init__.py
    database/
      connection.py      # Database connection management
      repositories/
        card_repository.py
        transaction_repository.py
        audit_repository.py
    encryption/
      crypto.py          # Encryption utilities
      tokenization.py    # Card tokenization
    external/
      payment_processor.py
      fraud_service.py
tests/
  unit/
    test_card_service.py
    test_encryption.py
  integration/
    test_card_api.py
    test_transactions_api.py
  performance/
    test_load.py
docs/
  api/
    openapi.yaml         # OpenAPI 3.0 specification
  compliance/
    data_classification.md
    audit_procedures.md
```

**Expected System State:**
- Fully functional API serving card management endpoints
- Audit logs capturing all operations
- Integration tests passing in CI/CD
- OpenAPI documentation generated and accessible
- Compliance documentation complete

**Deliverables:**
- Deployable containerized application (Dockerfile + docker-compose)
- Database migration scripts
- API documentation
- Runbook for operations team
- Compliance evidence package

---

## Low-Level Tasks

### Task 1: Database Schema and Migrations

**What prompt would you run to complete this task?**
Create the database schema for the Virtual Card Management System. Define tables for cards, transactions, audit_logs, and card_limits with proper constraints, indexes, and foreign keys. Use Alembic for migrations.

**What file do you want to CREATE or UPDATE?**
- `src/infrastructure/database/migrations/001_initial_schema.py`
- `src/infrastructure/database/models.py`

**What function do you want to CREATE or UPDATE?**
- SQLAlchemy ORM models: `Card`, `Transaction`, `AuditLog`, `CardLimit`
- Alembic migration: `upgrade()`, `downgrade()`

**What are details you want to add to drive the code changes?**
- Card table: id (UUID), user_id, card_token, encrypted_pan, status (ACTIVE/FROZEN/TERMINATED), created_at, updated_at
- CardLimit table: id, card_id (FK), limit_type (PER_TXN/DAILY/MONTHLY), amount (Decimal), currency (ISO 4217)
- Transaction table: id, card_id (FK), amount, currency, merchant_name, merchant_category_code, status, created_at
- AuditLog table: id, entity_type, entity_id, action, actor_id, actor_type (USER/SYSTEM/ADMIN), before_state (JSONB), after_state (JSONB), correlation_id, created_at
- Add indexes on: card.user_id, card.status, transaction.card_id, transaction.created_at, audit_log.entity_id
- Use UUID for all primary keys; timestamps with timezone

---

### Task 2: Encryption and Tokenization Module

**What prompt would you run to complete this task?**
Implement AES-256-GCM encryption for cardholder data and a tokenization system that generates reversible tokens for card references. Include key rotation support.

**What file do you want to CREATE or UPDATE?**
- `src/infrastructure/encryption/crypto.py`
- `src/infrastructure/encryption/tokenization.py`

**What function do you want to CREATE or UPDATE?**
- `encrypt_pan(pan: str, key_version: int) -> EncryptedData`
- `decrypt_pan(encrypted: EncryptedData, key_version: int) -> str`
- `generate_card_token(card_id: UUID) -> str`
- `resolve_card_token(token: str) -> UUID`
- `rotate_encryption_key(old_version: int, new_version: int) -> None`

**What are details you want to add to drive the code changes?**
- Use `cryptography` library for AES-256-GCM
- EncryptedData dataclass: ciphertext, nonce, tag, key_version
- Store encryption keys in environment variables or secrets manager (not in code)
- Token format: `vcard_` prefix + base64url-encoded HMAC of card_id + random suffix
- Maintain token mapping in Redis with TTL of 24 hours
- Include comprehensive input validation (PAN format, length checks)
- Log encryption operations without exposing sensitive data

---

### Task 3: Card Service Business Logic

**What prompt would you run to complete this task?**
Implement the CardService class with all card lifecycle operations: create, freeze, unfreeze, update limits, and terminate. Include validation, audit logging, and notification triggers.

**What file do you want to CREATE or UPDATE?**
- `src/domain/services/card_service.py`

**What function do you want to CREATE or UPDATE?**
- `CardService.create_card(user_id, limits, validity_months) -> Card`
- `CardService.freeze_card(card_id, reason, actor) -> Card`
- `CardService.unfreeze_card(card_id, actor) -> Card`
- `CardService.update_limits(card_id, limits, actor) -> Card`
- `CardService.terminate_card(card_id, reason, actor) -> None`
- `CardService.get_card(card_id, actor) -> Card`

**What are details you want to add to drive the code changes?**
- All methods must create AuditLog entries before returning
- Validate actor has permission for the operation
- Freeze/unfreeze must be idempotent (freezing frozen card returns success)
- Terminate is irreversible; terminated cards cannot be reactivated
- Use dependency injection for repositories and external services
- Raise domain exceptions (CardNotFoundError, CardAlreadyTerminatedError, InsufficientPermissionError)
- Trigger notifications on status changes via NotificationService
- All monetary amounts must use Decimal with 2 decimal places

---

### Task 4: Card API Endpoints

**What prompt would you run to complete this task?**
Create FastAPI routes for card operations with proper request/response models, authentication, rate limiting, and OpenAPI documentation.

**What file do you want to CREATE or UPDATE?**
- `src/api/routes/cards.py`
- `src/api/schemas/card_schemas.py`

**What function do you want to CREATE or UPDATE?**
- `POST /api/v1/cards` - create_card endpoint
- `GET /api/v1/cards/{card_id}` - get_card endpoint
- `POST /api/v1/cards/{card_id}/freeze` - freeze_card endpoint
- `POST /api/v1/cards/{card_id}/unfreeze` - unfreeze_card endpoint
- `PATCH /api/v1/cards/{card_id}/limits` - update_limits endpoint
- `DELETE /api/v1/cards/{card_id}` - terminate_card endpoint
- `GET /api/v1/cards` - list_user_cards endpoint

**What are details you want to add to drive the code changes?**
- Use Pydantic v2 for request/response schemas with strict validation
- Include correlation_id in all responses (from X-Correlation-ID header or generate UUID)
- Mask PAN in responses (show only last 4 digits)
- Never return CVV in any response after card creation
- HTTP status codes: 201 (created), 200 (success), 400 (validation), 401 (auth), 403 (forbidden), 404 (not found), 429 (rate limit)
- Include OpenAPI tags and descriptions for all endpoints
- Apply rate limiting decorator from middleware
- Log all requests with sanitized payloads

---

### Task 5: Transaction Query Service and API

**What prompt would you run to complete this task?**
Implement transaction retrieval with filtering, pagination, and automatic categorization. Create corresponding API endpoints.

**What file do you want to CREATE or UPDATE?**
- `src/domain/services/transaction_service.py`
- `src/api/routes/transactions.py`
- `src/api/schemas/transaction_schemas.py`

**What function do you want to CREATE or UPDATE?**
- `TransactionService.get_transactions(card_id, filters, pagination) -> PaginatedResult[Transaction]`
- `TransactionService.get_transaction(transaction_id) -> Transaction`
- `TransactionService.categorize_transaction(merchant_category_code) -> Category`
- `GET /api/v1/cards/{card_id}/transactions` endpoint
- `GET /api/v1/transactions/{transaction_id}` endpoint

**What are details you want to add to drive the code changes?**
- Filters: date_from, date_to, min_amount, max_amount, status, category
- Pagination: cursor-based (not offset) for performance; default page_size=20, max=100
- Categorization based on MCC (Merchant Category Code) mapping
- Include running balance calculation (optional, expensive)
- Response includes total_count and next_cursor
- Cache transaction list for 30 seconds (invalidate on new transaction)
- Verify actor owns the card before returning transactions

---

### Task 6: Audit Logging Middleware

**What prompt would you run to complete this task?**
Create middleware that automatically captures audit logs for all state-changing operations with before/after state snapshots.

**What file do you want to CREATE or UPDATE?**
- `src/api/middleware/audit.py`
- `src/domain/services/audit_service.py`
- `src/infrastructure/database/repositories/audit_repository.py`

**What function do you want to CREATE or UPDATE?**
- `AuditMiddleware.__call__(request, call_next)` - FastAPI middleware
- `AuditService.log_action(entity_type, entity_id, action, actor, before, after, correlation_id)`
- `AuditService.get_audit_trail(entity_id, filters) -> List[AuditLog]`
- `AuditRepository.save(audit_log) -> AuditLog`
- `AuditRepository.find_by_entity(entity_id, limit, offset) -> List[AuditLog]`

**What are details you want to add to drive the code changes?**
- Audit logs are immutable; no update or delete operations allowed
- Capture: HTTP method, endpoint, request body (sanitized), response status, duration_ms
- Actor information from JWT token (user_id, roles, session_id)
- Before/after states as JSONB; sensitive fields must be masked
- Correlation ID propagated through entire request lifecycle
- Async write to avoid blocking request processing (use background task)
- Retention policy: 7 years for compliance (configurable)

---

### Task 7: Admin Operations API

**What prompt would you run to complete this task?**
Create internal admin API for operations and compliance teams with card search, emergency controls, and audit report generation.

**What file do you want to CREATE or UPDATE?**
- `src/api/routes/admin.py`
- `src/api/schemas/admin_schemas.py`
- `src/domain/services/admin_service.py`

**What function do you want to CREATE or UPDATE?**
- `GET /api/v1/admin/cards` - search_cards (with filters)
- `POST /api/v1/admin/cards/{card_id}/emergency-freeze` - emergency_freeze
- `GET /api/v1/admin/audit-report` - generate_audit_report
- `GET /api/v1/admin/cards/{card_id}/audit-trail` - get_card_audit_trail
- `AdminService.search_cards(filters) -> PaginatedResult[CardSummary]`
- `AdminService.emergency_freeze(card_id, reason, admin_actor) -> Card`
- `AdminService.generate_audit_report(date_from, date_to, format) -> ReportResult`

**What are details you want to add to drive the code changes?**
- Require ADMIN or COMPLIANCE role for all admin endpoints
- Emergency freeze bypasses normal freeze (even if already frozen) and triggers alert
- Mandatory reason field for all admin actions (min 10 characters)
- Search filters: user_id, status, created_date_range, limit_range
- Audit report formats: JSON, CSV, PDF
- Include aggregated statistics in reports (cards created, frozen, terminated)
- Rate limit admin endpoints separately (lower limits)

---

### Task 8: Authentication and Authorization Middleware

**What prompt would you run to complete this task?**
Implement JWT-based authentication middleware with role-based access control. Integrate with external identity provider.

**What file do you want to CREATE or UPDATE?**
- `src/api/middleware/auth.py`
- `src/domain/models/auth.py`

**What function do you want to CREATE or UPDATE?**
- `AuthMiddleware.__call__(request, call_next)` - verify JWT on protected routes
- `get_current_user(token: str) -> AuthenticatedUser` - dependency injection helper
- `require_roles(*roles)` - decorator for role-based access
- `AuthenticatedUser` dataclass with user_id, roles, session_id, permissions

**What are details you want to add to drive the code changes?**
- Validate JWT signature using RS256 with public key from JWKS endpoint
- Check token expiration and issuer claims
- Extract roles from `roles` or `groups` claim
- Roles hierarchy: USER < SUPPORT < ADMIN < COMPLIANCE
- Cache JWKS for 1 hour with background refresh
- Return 401 for missing/invalid token, 403 for insufficient permissions
- Log authentication failures with client IP (not token contents)
- Support API key authentication for service-to-service calls

---

### Task 9: Rate Limiting Middleware

**What prompt would you run to complete this task?**
Implement Redis-based rate limiting with per-user and global limits. Include graceful degradation if Redis is unavailable.

**What file do you want to CREATE or UPDATE?**
- `src/api/middleware/rate_limit.py`

**What function do you want to CREATE or UPDATE?**
- `RateLimitMiddleware.__call__(request, call_next)`
- `check_rate_limit(user_id, endpoint) -> RateLimitResult`
- `rate_limit(requests_per_second, burst)` - decorator for endpoint-specific limits

**What are details you want to add to drive the code changes?**
- Use sliding window algorithm for accurate limiting
- Default limits: 10 req/sec per user, 1000 req/sec global
- Return 429 with Retry-After header when exceeded
- Include X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset headers
- Different limits for read vs write operations
- Admin endpoints have separate, lower limits
- Graceful degradation: if Redis unavailable, allow requests with warning log
- Configurable via environment variables

---

### Task 10: Unit and Integration Tests

**What prompt would you run to complete this task?**
Create comprehensive test suite covering card service business logic, API endpoints, and security controls.

**What file do you want to CREATE or UPDATE?**
- `tests/unit/test_card_service.py`
- `tests/unit/test_encryption.py`
- `tests/integration/test_card_api.py`
- `tests/integration/test_transactions_api.py`
- `tests/conftest.py` (fixtures)

**What function do you want to CREATE or UPDATE?**
- Unit tests for all CardService methods (happy path + error cases)
- Unit tests for encryption/decryption with various inputs
- Integration tests for all API endpoints
- Fixtures: test_db, test_client, mock_user, mock_admin

**What are details you want to add to drive the code changes?**
- Use pytest with pytest-asyncio for async tests
- Test database: use PostgreSQL in Docker or SQLite for speed
- Mock external services (payment processor, fraud service)
- Test cases must cover:
  - Card creation with valid/invalid limits
  - Freeze/unfreeze idempotency
  - Authorization failures (wrong user, wrong role)
  - Rate limiting behavior
  - Audit log generation
- Use factories (factory_boy) for test data generation
- Aim for 80%+ coverage on business logic
- Include negative tests: invalid inputs, unauthorized access, edge cases

---

### Task 11: API Documentation and OpenAPI Spec

**What prompt would you run to complete this task?**
Generate comprehensive OpenAPI 3.0 specification with examples, error responses, and authentication documentation.

**What file do you want to CREATE or UPDATE?**
- `docs/api/openapi.yaml`
- `src/api/main.py` (FastAPI app configuration)

**What function do you want to CREATE or UPDATE?**
- FastAPI app metadata configuration
- Custom OpenAPI schema generation
- Example request/response payloads

**What are details you want to add to drive the code changes?**
- Include all endpoints with full request/response schemas
- Document all error codes and their meanings
- Add authentication section (Bearer token, API key)
- Include example values for all fields
- Document rate limiting headers
- Add webhook documentation for notifications (future)
- Generate Redoc and Swagger UI endpoints
- Version the API (v1) with deprecation policy documented

---

### Task 12: Docker and Deployment Configuration

**What prompt would you run to complete this task?**
Create containerized deployment with Docker, including database migrations, health checks, and environment configuration.

**What file do you want to CREATE or UPDATE?**
- `Dockerfile`
- `docker-compose.yml`
- `.env.example`
- `scripts/entrypoint.sh`

**What function do you want to CREATE or UPDATE?**
- Multi-stage Dockerfile for minimal production image
- docker-compose with app, postgres, redis services
- Entrypoint script for migrations and startup

**What are details you want to add to drive the code changes?**
- Use Python 3.11-slim base image
- Multi-stage build: builder stage for dependencies, runtime stage for app
- Run as non-root user in container
- Health check endpoint: GET /health (returns 200 if db + redis connected)
- Environment variables for all configuration (no hardcoded values)
- .env.example with all required variables documented
- docker-compose profiles: dev (with hot reload), prod (optimized)
- Volume for persistent database data
- Network isolation between services
