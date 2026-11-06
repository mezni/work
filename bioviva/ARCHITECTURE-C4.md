# BioViva — C4 Component Diagram

## Software System Level

**BioViva**: Ecommerce platform for bio-products (olive oil, honey, herbal essences).
- Hosted in a single Docker container
- Axum HTTP server on port 3000
- Single PostgreSQL database (shared across all bounded contexts)
- React SPA served as fallback

## Container Level

```
┌─────────────────────────────────────────────────────────────────┐
│                        /app/bio-app                           │
│                                                                 │
│  +------------------+  +---------------------+  +------------+│
│  |  Axum HTTP Server|  |  sqlx::Pool<Postgres>|  |  .env      │
│  |  (port 3000)     |  |   (single connection)│  |  vars     │
│  +--------+----------+  +---------+-----------+  +------------+│
│           │                   │                     │            │
│           │                   │                     │            │
│    +------+----+         +-----+-----+         +------+------+│
│    |  Routing   |         |   Auth    |         |  Products   │
│    |  Layer     |         |   Crate   |         |   Crate     │
│    +------+----+         +-----+-----+         +------+------+│
│           │                   │                     │            │
│    +------+----+         +-----+-----+         +------+------+│
│    |  /api/v1   |         | /api/v1   |         | /api/v1     │
│    |  routes    |         |   auth    |         |   products  │
│    +------+----+         +-----+-----+         +------+------+│
│           │                   │                     │            │
│    ──────────────────────────────────────────────────────────── │
│                                                                  │
│  Static file serving (React SPA dist)                          │
│  Served at / when no API route matches                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Crate-Level Decomposition (7 Bounded Contexts)

```
┌─────────────────────────────────────────────────────────────────┐
│                        bio-api (entry point)                    │
│  │ Routes: /api/v1/* + fallback SPA                             │
│  │   • Composes all 7 context routers                             │
│  │   • CORS, tracing, error handling middleware                   │
│  │   • Extension(AuthClaims) injection                          │
│  └───────────────┬─────────────────────┬───────────────────────┘
│                  │                       │                       │
│          +-------+-----------------------+-------+           │
│          |                       |                       |           │
│      bio-auth                        bio-products        │
│  │ JWT/ RBAC                          │ Product CRUD          │
│  │ • Claims extraction                │ • Trust score         │
│  │ • Permission checks                │ • Freshness state     │
│  │ • Token revocation                 │ • Taste profiles      │
│          |                       |                       │
│          +-------+-----------------------+-------+           │
│                  │                       │                       │
│          bio-producers                      bio-orders       │
│  │ Certification & harvest              │ Order & subscription  │
│  │ • CertValidator                      │ • OrderValidator      │
│  │ • TrustScoreCalculator               │ • FreshnessEligibility│
│          |                       │                       │
│          +-------+-----------------------+-------+           │
│                  │                       │                       │
│          bio-users                         bio-search        │
│  │ User profiles & preferences           │ Discovery &           │
│  │ • TasteQuizEngine                    │   recommendations   │
│  │ • PreferenceEngine                   │ • TrustFilter       │
│          |                       │                       │
│          +─────────────────────────────────────────────────┤
│                          │                                │
│             Shared: sqlx::Pool<Postgres> from bio-core       │
│              (single connection pool, DI to all crates)    │
└─────────────────────────────────────────────────────────────────┘
```

## Key Relationships

| From → To | Governing AD | Data Flow |
| --- | --- | --- |
| bio-api → bio-auth | AD-4 | `Extension(AuthClaims)` injected into all route handlers |
| bio-api → bio-core (pool) | AD-2 | Single `sqlx::Pool<Postgres>` passed via DI |
| bio-products → bio-core (pool) | AD-2 | Reads/writes to `products`, `product_taste_profiles`, `product_aroma_notes` tables |
| bio-producers → bio-core (pool) | AD-2 | Reads/writes to `producers`, `certifications`, `harvest_batches` tables |
| bio-orders → bio-core (pool) | AD-2 | Reads/writes to `orders`, `order_lines`, `subscriptions` tables |
| bio-users → bio-core (pool) | AD-2 | Reads/writes to `users`, `user_preferences`, `taste_quiz_results` tables |
| bio-search → bio-core (pool) | AD-2 | Reads/writes to `search_index`, queries products/producers |
| bio-search → bio-products | AD-5 | Trust score filtering on search results |
| bio-search → bio-users | AD-7 | Preference-based filtering |
| All contexts → auth middleware | AD-4 | JWT validated before handler execution |

## Data Flow — Request Life Cycle

```
Client HTTP Request
    │
    ▼
Axum Router (bio-api)
    │
    ├─[/api/v1/auth/*] → bio-auth middleware → JWT validation → Claims in extensions
    │     └─→ Handler (login/register/refresh/logout)
    │
    ├─[/api/v1/products] → bio-products router → ProductRepository → SQL → PostgreSQL
    │     └─→ Handler (list, get, search) — Trust score + freshness filtering (AD-5, AD-6)
    │
    ├─[/api/v1/producers] → bio-producers router → CertificationValidator → SQL → PostgreSQL
    │     └─→ Handler (list, get, create)
    │
    ├─[/api/v1/orders] → bio-orders router → OrderValidator (freshness check AD-6) → SQL → PostgreSQL
    │     └─→ Handler (create, get, subscribe, reorders) — Only Fresh/Ripe products
    │
    ├─[/api/v1/users] → bio-users router → UserRepository → SQL → PostgreSQL
    │     └─→ Handler (profile, quiz, recommendations) — RBAC (AD-7)
    │
    └─[/*] → fallback handler → serves React SPA index.html
                     │
                     ▼
              Client-side TanStack Query → /api/v1 API calls
```

## Deployment Topology

```
┌───────────────────┐     ┌─────────────────────┐
|   Client Browser  |     |   Docker Container  │
|  (React SPA + API)│     |   bio-app (Axum)    │
└───────┬───────────┘     └───────┬───────────────┘
        │                     │
        │   HTTPS/WSS         │   localhost:3000
        ▼                     ▼
┌─────────────────────────────────────────────────┐
|  Single PostgreSQL Database                      │
|  - Shared across all 7 bounded contexts         │
|  - Connection pool: sqlx::Pool<Postgres>         │
|  - URL: DATABASE_URL env var                    │
└─────────────────────────────────────────────────┘
```

## Consistency Conventions (from ARCHITECTURE-SPINE.md)

| Concern | Convention |
| --- | --- |
| Entity/Type naming | StudlyCase (Rust); camelCase (TS API); snake_case (DB columns) |
| ID format | UUIDs (cosmic); ISO 8601 dates |
| Error handling | `Result<T, BioError>`; serde_json error envelopes |
| Auth | JWT via Axum extensions; `auth_middleware` → `Claims` in extensions |
| Trust score | 40% certification + 30% lab + 20% producer + 10% review (AD-5) |
| Freshness | Fresh(0-30)/Ripe(31-60)/Aging(61-90)/Archived(>90) — AD-6 |
| API versioning | All routes under `/api/v1/` — AD-9 |

---
*Generated from ARCHITECTURE-SPINE.md + .bmad/.memlog.md. This C4 diagram illustrates the component structure governed by the architecture spine invariants.*