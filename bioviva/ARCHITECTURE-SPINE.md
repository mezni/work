---
name: 'BioViva'
type: architecture-spine
purpose: build-substrate
altitude: epic
paradigm: hexagonal (DDD-style with ports/adapters, Axum framework)
scope: BioViva ecommerce system - 7 bounded contexts sharing 1 PostgreSQL DB
status: draft
created: '2026-11-05'
updated: '2026-11-05'
binds: [bio-auth, bio-core, bio-products, bio-producers, bio-orders, bio-users, bio-search]
sources: [ARCHITECTURE_SUMMARY.md, architecture.md, BUILD_PLAN.md, core-features.md, PROJECT_BRIEF.md, ux-design.md]
companions: []
---

# Architecture Spine — BioViva

## Design Paradigm

Hexagonal architecture (DDD-style) with Axum as the web framework. Seven bounded contexts (`bio-auth`, `bio-core`, `bio-products`, `bio-producers`, `bio-orders`, `bio-users`, `bio-search`) each as a separate crate/module with clear domain boundaries. All contexts share one PostgreSQL connection pool from `bio-core`. Route-level adaptation layers (Axum handlers + middleware) connect domains to the framework.

**Key mapping**: Bounded contexts = hexagonal ports. Repository traits = port interfaces. Axum router + middleware = adapter layer. DB connection pool = shared infrastructure injected via dependency inversion.

## Inherited Invariants

| Inherited | From parent | Binds here |
| --- | --- | --- |
| AD-1: Hexagonal paradigm | Initial spine | Module boundary enforcement; DI of DB pool |
| C-1: Rust 1.70 toolchain | BUILD_PLAN.md | Compiler compatibility; Cargo feature gating |
| C-2: PostgreSQL database | ARCHITECTURE_SUMMARY.md | Shared DB connection pool; schema evolution |
| C-3: Argon2 password hashing | ARCHITECTURE_SUMMARY.md | Password hash format; Argon2 params from env |

## Invariants & Rules

### AD-1 — Hexagonal Design Paradigm
- **Binds**: All 7 bounded contexts (bio-auth, bio-core, bio-products, bio-producers, bio-orders, bio-users, bio-search)
- **Prevents**: Monolithic code mixing across contexts; arbitrary DB access from handlers; circular dependencies between crates
- **Rule**: Each feature must live in its bounded context crate. DB access only via Repository traits. Web-facing handlers in Axum adapter layer. No crate may import business logic from another context crate.

### AD-2 — Single DB Connection Pool
- **Binds**: All crates (bio-auth through bio-search)
- **Prevents**: N+1 connection issues; inconsistent pool sizes; per-crate migration drift
- **Rule**: Single `sqlx::Pool<Postgres>` created in `bio-core` and passed via DI to all crates. Pool config (max connections, timeout) set once in `bio-api` router initialization. No per-crate pool creation.

### AD-3 — Repository Pattern per Bounded Context
- **Binds**: ProductRepository (bio-products), ProducerRepository (bio-producers), OrderRepository (bio-orders), UserRepository (bio-users), CertificationRepository (bio-producers)
- **Prevents**: Direct SQL in handlers; repository logic duplication across contexts; table access across context boundaries
- **Rule**: Each crate implements its own `Repository` trait (`Send + Sync + 'static`). Trait methods abstract all DB operations. Handlers call repository methods only. Crates may not query tables owned by other contexts.

### AD-4 — JWT Auth via Axum Extensions
- **Binds**: bio-auth crate; all context routers via `Extension(AuthClaims)` injection
- **Prevents**: Duplicate auth checks in every handler; plaintext password handling; bypassed authorization
- **Rule**: `auth_middleware` extracts/validates JWT, inserts `Claims` into Axum extensions. `permission_middleware` / `role_middleware` check before handler execution. Handlers receive `Claims` as extension, never re-validate JWT.

### AD-5 — Trust Score Calculation Invariants
- **Binds**: bio-products (Product trust score), bio-producers (Producer reputation), bio-search (Recommendation filtering)
- **Prevents**: Arbitrary trust score manipulation; inconsistent calculation across contexts; missing invariant in recommendations
- **Rule**: Trust Score (0-100) = 40% certification validity + 30% lab test results + 20% producer reputation + 10% review recency. Recalculated on: certification update, new lab results, producer rating change, new review. Visible on all product cards.

### AD-6 — Freshness Lifecycle States
- **Binds**: bio-products (FreshnessCalculator), bio-orders (FreshnessEligibilityChecker), bio-search (TrustFilter)
- **Prevents**: Selling expired products; subscription past certification window; search showing stale products
- **Rule**: FreshnessState enum: Fresh (0-30 days since harvest), Ripe (31-60 days), Aging (61-90 days), Archived (>90 days). Products beyond 90 days removed from catalog. Handlers enforce: Order valid only for Fresh/Ripe; Subscription manages certification renewal; Search filters by min trust score + seasonal availability.

### AD-7 — Role-Based Access Control
- **Binds**: bio-auth (role assignment), all contexts (role-based handler access)
- **Prevents**: Unauthorized role escalation; context-cross permission leaks; guest access to protected routes
- **Rule**: Roles: guest | buyer | producer | admin. Permissions scoped per role. Middleware: `role_required("admin")`, `permission_required("orders:create")`. Checks from `Claims` in extensions before handler execution.

### AD-8 — Docker Single-Container Deployment
- **Binds**: Deployment infrastructure; CI/CD pipeline; production environment
- **Prevents**: Multi-container orchestration drift; dev/prod parity issues; manual env config gaps
- **Rule**: Multi-stage Docker: builder (rust:1.70) → runtime (ubuntu:22.04). Single container serves Axum app (API + static frontend). Env vars: DATABASE_URL, JWT_SECRET, JWT_EXPIRES_MIN, REFRESH_TOKEN_EXPIRES_DAYS, ARGON2_*, ACCOUNT_LOCKOUT_*, CORS_ORIGINS.

### AD-9 — API Versioning at v1
- **Binds**: All API route definitions in bio-api router composition
- **Prevents**: Unversioned API breaks; route prefix inconsistency; SPA served at wrong path
- **Rule**: All API routes under `/api/v1/*` prefix. Auth at `/api/v1/auth/*`. Bounded contexts at `/api/v1/products`, `/api/v1/producers`, `/api/v1/orders`, `/api/v1/users`, `/api/v1/search`. Fallback handler serves React SPA at `/`.

## Consistency Conventions

| Concern | Convention |
| --- | --- |
| Naming (entities, files, interfaces) | StudlyCase for Rust types; snake_case for DB columns and env vars; camelCase for TypeScript/API; PascalCase for public structs |
| Data & formats (ids, dates, error shapes) | UUIDs for entity IDs (cosmic); ISO 8601 dates; BioError with context objects; serde_json error envelopes |
| State & cross-cutting (mutation, errors, logging, config, auth) | DB pool immutable after init; errors returned as Result<T, BioError>; tracing subscriber with structured fields; config from ENV vars with .env.example defaults |

## Stack

| Name | Version |
| --- | --- |
| Rust | 1.70 |
| Axum | 0.7 |
| SQLX | 0.7 |
| ArgON2 | 0.3 |
| Deadpool-postgres | 0.16 |
| TanStack Query | 5.0 |
| React | 18.3 |
| TypeScript | 5.5 |

## Structural Seed

```
/bio-viva/
  Cargo.toml (workspace)
  services/
    bio-core/         # Shared kernel: primitives, errors, DB types
    bio-auth/         # Auth & RBAC context
    bio-products/     # Product bounded context
    bio-producers/    # Producer bounded context
    bio-orders/       # Order/commerce context
    bio-users/        # User/account context
    bio-search/       # Discovery context
    bio-api/          # Axum entry point + router composition
  frontend/           # React + Vite build
  Dockerfile          # Multi-stage: builder → runtime
  .env.example        # Environment configuration
```

## Capability → Architecture Map

| Capability / Area | Lives in | Governed by |
| --- | --- | --- |
| Product CRUD | bio-products | AD-3 (Repository), AD-5 (Trust Score), AD-6 (Freshness) |
| Producer onboarding | bio-producers | AD-3 (Repository), AD-7 (RBAC: producer role) |
| Order placement | bio-orders | AD-3 (Repository), AD-6 (Freshness eligibility), AD-7 (RBAC: buyer role) |
| User profile & quiz | bio-users | AD-3 (Repository), AD-7 (RBAC: buyer/guest roles), AD-4 (Auth claims) |
| Product search & recommendation | bio-search | AD-5 (Trust score filtering), AD-6 (Seasonal availability) |
| Authentication & login | bio-auth | AD-4 (JWT), AD-7 (Roles), C-3 (Argon2) |
| Static file serving / SPA | bio-api | AD-8 (Docker), AD-9 (API versioning) |

## Deferred

### Q-1: Search Integration (ElasticSearch vs Typesense)
- **Type**: question
- **Text**: Should search use ElasticSearch or Typesense? This affects bio-search crate dependency structure and mapping to infrastructure.
- **Revisit condition**: When search infrastructure is provisioned; currently deferred until Phase 5 DB migrations
- **Related AD**: None yet (to be decided)

### Q-2: PostGIS for Origin Mapping
- **Type**: question
- **Text**: Should origin mapping use PostGIS or plain coordinates? Affects bio-core enum types and product origin handling.
- **Revisit condition**: When geo-search requirements are finalized with product team
- **Related AD**: AD-1 (paradigm choice may influence this)

### Q-3: Frontend Framework Evaluation
- **Type**: question
- **Text**: Should React + TypeScript + TanStack Query be maintained or evaluated against alternatives?
- **Revisit condition**: When frontend team decides or new requirements emerge
- **Related AD**: AD-8 (Docker config assumes React dist build)

### Q-4: Lab Report Ingestion API Design
- **Type**: question
- **Text**: How should third-party lab report ingestion be structured? Separate integration crate or part of bio-producers?
- **Revisit condition**: When third-party lab vendor contracts are finalized
- **Related AD**: AD-3 (repository pattern scope)

### Q-5: Subscription Certification Renewal Logic
- **Type**: question
- **Text**: Exact algorithm for certification renewal in SubscriptionManager — should it be 30 days before expiry, on expiry, or grace period?
- **Revisit condition**: When subscription flow is implemented in bio-orders
- **Related AD**: AD-6 (freshness lifecycle interacts with certification)

---