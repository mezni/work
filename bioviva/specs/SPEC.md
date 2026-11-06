---
title: 'BioViva — Ecommerce Platform for Bio-Products'
type: 'spec'
created: '2026-11-05'
updated: '2026-11-05'
companions: [
  'architecture-diagrams.md',
  'market-research-claims.md',
  'build-dependency-graph.md',
  'success-metrics.md',
  'certification-taxonomy.md'
]
sources: [
  'ARCHITECTURE_SUMMARY.md',
  'architecture.md',
  'BUILD_PLAN.md',
  'core-features.md',
  'PROJECT_BRIEF.md',
  'ux-design.md',
  'ARCHITECTURE-SPINE.md',
  '.bmad/.memlog.md',
  'ANALYSIS-BRIEF.md',
  'market-market-research-bioviva-2026-11-05/research.md'
]
---

# BioViva — Specification (SPEC.md)

The kernel is derived from the project memlog (.bmad/.memlog.md) and all source artifacts listed above. This SPEC.md is re-rendered on each run — never hand-edit.

## Why
**Problem:** Consumers lack trust and transparency when buying bio products online — uncertainty about authenticity, freshness, and origin undermines purchasing decisions.

**Context:** Bio-product ecommerce is a growing but fragmented market. The global organic food ecommerce market is valued at ~$30B-$50B (2024), with specialty/organic segments growing 8-12% CAGR. BioViva's niche (olive oil, honey, herbal essences with trust/transparency focus) is estimated at $2B-$5B globally.

**Ecosystem insight:** Every product has a Traceability story, Season-first catalog mirroring natural harvest cycles, Full sensory profile on every product, Direct producer stories with photos and methods, Freshness tracking from harvest to consumption, Smart reordering with subscription management.

---

## Capabilities
*Each capability has both `intent` and `success`. Missing either = not a capability.*

### CAP-1 — Product Traceability & Authenticity
- **Intent:** Enable consumers to verify every product's authenticity, origin, and quality before purchase.
- **Success:** Consumers can see batch/lot numbering, origin mapping, certification badges, and harvest date on every product card; Trust Score visible and meaningful.
- **Governing ADs:** AD-3 (Repository pattern), AD-5 (Trust score invariants), AD-6 (Freshness lifecycle), C-2 (PostgreSQL database)

### CAP-2 — Season-First Catalog & Freshness Management
- **Intent:** Organize products by harvest season first, category second; enforce freshness lifecycle states to prevent selling expired products.
- **Success:** Seasonal collections highlighted on homepage; products beyond 90 days removed from catalog; "Fresh" (0-30 days), "Ripe" (31-60 days), "Aging" (61-90 days), "Archived" (>90 days) states visible and handler-enforced.
- **Governing ADs:** AD-6 (Freshness lifecycle states), AD-2 (Single DB connection pool)

### CAP-3 — Trust Score Transparency
- **Intent:** Display a calculated Trust Score (0-100) on every product card, with visible breakdown of components.
- **Success:** Trust Score = 40% certification validity + 30% lab test results + 20% producer reputation + 10% review recency; score influences purchase decisions; displayed with color coding (green=high, yellow=medium, red=low).
- **Governing ADs:** AD-5 (Trust score calculation invariants)

### CAP-4 — Producer Visibility & Storytelling
- **Intent:** Make every farmer/producer visible with photos, methods, sustainability metrics, and harvest diaries.
- **Success:** Producer profiles on every product page; sustainability metrics visible; harvest diaries show seasonal updates; certification validation automated against databases.
- **Governing ADs:** AD-3 (Repository pattern — ProducerRepository), C-1 (Rust 1.70 toolchain), AD-7 (RBAC: producer role)

### CAP-5 — Smart Reordering & Subscription Management
- **Intent:** Enable subscriptions for staple products (olive oil, honey) with certification renewal alerts and freshness-based reorder suggestions.
- **Success:** Subscribers receive "running low" notifications; certification renewal alerts; one-click reorder with freshness window respect; subscription manageability with pause/skip.
- **Governing ADs:** AD-6 (Freshness lifecycle — Order valid only for Fresh/Ripe), AD-7 (RBAC: buyer role), AD-4 (JWT auth via Axum extensions)

### CAP-6 — Discovery & Recommendation with Trust Filtering
- **Intent:** Enable product search and recommendations filtered by minimum trust score, seasonal availability, and user preference matching.
- **Success:** Search results filtered by min trust score + seasonal availability; recommendation engine informs personalization; taste quiz informs product filtering.
- **Governing ADs:** AD-5 (Trust score filtering), AD-6 (Seasonal availability filtering), Q-3 (Frontend framework evaluation — React + TypeScript + TanStack Query)

### CAP-7 — Authenticated API Access with RBAC
- **Intent:** Provide authenticated API access with role-based access control (guest|buyer|producer|admin) and scoped permissions.
- **Success:** JWT validated via Axum middleware; Claims injected into extensions; permission checks before handler execution; role-permission checks enforced at handler entry.
- **Governing ADs:** AD-4 (JWT auth via Axum extensions), AD-7 (RBAC — roles and permissions)

---

## Constraints
*Constraints actually bend design decisions. A "constraint" that rules nothing out is decoration.*

### C-1 — Rust 1.70 Toolchain
- The project must build with Rust toolchain version 1.70.
- **Effect:** Governs compiler features, standard library availability, and Cargo ecosystem compatibility. Rust 1.96.0 is installed but 1.70 is the constrained baseline.

### C-2 — Single PostgreSQL Database
- All 7 bounded contexts must share one PostgreSQL connection pool via `sqlx::Pool<Postgres>` from `bio-core`.
- **Effect:** No per-crate pools; schema isolation enforced by code review, not DB-level; all contexts access only their own tables.

### C-3 — Axum Web Framework
- The web framework must be Axum.
- **Effect:** Router composition, middleware pattern, extension injection all Axum-specific.

### C-4 — Argon2 Password Hashing
- Passwords must be hashed with Argon2, with configurable memory (default 64MB), time (default 3), and parallelism (default 2).
- **Effect:** Argon2 params from env vars: ARGON2_MEMORY, ARGON2_TIME, ARGON2_PARALLEL.

### C-5 — Docker Single-Container Deployment
- The application must run in a single Docker container (multi-stage: builder rust:1.70 → runtime ubuntu:22.04).
- **Effect:** Single Axum process serving API + static frontend; env vars: DATABASE_URL, JWT_SECRET, JWT_EXPIRES_MIN, REFRESH_TOKEN_EXPIRES_DAYS, ARGON2_*, ACCOUNT_LOCKOUT_*, CORS_ORIGINS.

### C-6 — API Versioning at v1
- All API routes must be under `/api/v1/*` prefix; auth at `/api/v1/auth/*`; bounded contexts at their respective `/api/v1/*` paths; fallback serves React SPA at `/`.
- **Effect:** No unversioned API routes; consistent prefix across all 7 contexts.

### C-7 — Repository Pattern per Bounded Context
- Each crate must implement its own Repository trait (`Send + Sync + 'static`) abstracting DB access.
- **Effect:** Handlers call repository methods only; no direct SQL in handlers; crates may not query tables owned by other contexts.

### C-8 — JWT Authentication via Axum Extensions
- `auth_middleware` extracts/validates JWT, inserts `Claims` into Axum extensions; `permission_middleware` / `role_middleware` check before handler execution.
- **Effect:** Handlers receive `Claims` as extension, never re-validate JWT; no auth logic in handler bodies.

### C-9 — Freshness Lifecycle States
- FreshnessState enum: Fresh (0-30 days since harvest), Ripe (31-60 days), Aging (61-90 days), Archived (>90 days).
- **Effect:** Products beyond 90 days removed from catalog; handlers enforce: Order valid only for Fresh/Ripe; Subscription manages certification renewal; Search filters by min trust score + seasonal availability.

### C-10 — Role-Based Access Control
- Roles: guest | buyer | producer | admin. Permissions scoped per role.
- **Effect:** Middleware: `role_required("admin")`, `permission_required("orders:create")`; checks from `Claims` in extensions before handler execution.

---

## Non-goals
*At least one non-goal must be explicit. Absence means downstream skills fill the vacuum.*

### N-1 — Multi-Container Orchestration
- Kubernetes, ECS, or other container orchestration platforms are out of scope for the initial MVP.
- **Reason:** The architecture is designed for a single Docker container; orchestration can be added later.

### N-2 — Separate Frontend Application
- The React frontend should not be a separate deployed service; it must be served as static files from the same Axum container.
- **Reason:** The single-container deployment model (AD-8, C-5) does not support a separate frontend deployment.

### N-3 — Real-Time Push Notifications (Initial)
- Push notifications for freshness alerts are out of scope for the initial build; in-app notifications or email are the delivery mechanism.
- **Reason:** Can be added in a later phase; the freshness lifecycle (AD-6) and subscription management (CAP-5) are prioritized.

### N-4 — Multi-Language Support
- The initial build will support English only; localization i18n is out of scope.
- **Reason:** The sensory design system (ux-design.md) is English-first; i18n can be added later.

### N-5 — Real-Time Database Synchronization
- Change data capture, event sourcing, or real-time sync across multiple DB instances is out of scope.
- **Reason:** The single PostgreSQL pool (C-2) model does not require real-time sync for the MVP.

---

## Success Signal
*Success signal is concrete enough to test or demonstrate against. "Users love it" does not qualify.*

### Primary Success Metrics (from PROJECT_BRIEF.md:25-29)
1. **Trust score visibility → 40% increase in conversion from product page**
   - *Test:* A/B test product pages with Trust Score badge vs. without; measure conversion rate difference.
   - *Target:* At least 40% lift in product-page-to-checkout conversion.

2. **Seasonal collections → 25% higher average order value**
   - *Test:* Compare AOV on pages featuring seasonal collections vs. standard catalog pages.
   - *Target:* At least 25% higher AOV when seasonal collections are highlighted.

3. **Producer story engagement → 30% repeat purchase rate**
   - *Test:* Measure repeat purchase rate among users who view producer profiles vs. those who don't.
   - *Target:* At least 30% higher repeat purchase rate for engaged users.

4. **Freshness alerts → 15% reduction in expired product complaints**
   - *Test:* Track support complaints about expired products; compare before/after freshness alert implementation.
   - *Target:* At least 15% reduction in expired product complaints.

5. **Full specification validated → build sequence green**
   - *Test:* `cargo check -p bio-api` succeeds; `verify-build.sh` exits 0; all 9 ADs in ARCHITECTURE-SPINE.md are [ADOPTED].
   - *Target:* Zero blocked crates; build order follows critical path; spine invariants enforced in code.

### Secondary Success Metrics (from core-features.md:43-47 & ux-design.md:96-111)
- **Market acceptance:** >100 beta users with positive feedback on trust/origin transparency
- **Certification taxonomy:** ≥3 certification standards supported (USDA Organic, EU Organic, Fair Trade) with automated validation
- **User persona alignment:** "Health-Conscious Maya" pain points addressed in ≥80% of feature implementations
- **Accessibility compliance:** WCAG 2.1 AA for trust scores, color contrast, keyboard navigation, screen reader announcements
- **Mobile-first usability:** Thumb-zone primary actions, swipe gestures, voice search, push notifications (mobile) functional

---

## Companion Files

### architecture-diagrams.md
*Contains all diagrams too large for the kernel prose.*  
Holds: C4 component diagram (ARCHITECTURE-C4.md), data flow diagrams, deployment topology diagrams, crate-level decomposition diagrams, trust score calculation diagram, freshness lifecycle diagram.

### market-research-claims.md
*Contains the 10 claims from the market research, each with ≥2 independent sources required for validation.*  
Holds: Claim 1-10 with source references, two-source class compliance, open evidence, freshness windows, and open questions Q-1 through Q-5.

### build-dependency-graph.md
*Contains the build order sequence, critical dependency paths, and risk items.*  
Holds: 7-phase build sequence, critical path (bio-orders), build verification checks (verify-build.sh), and known risk items.

### success-metrics.md
*Contains the success metric test plans, targets, and measurement methodologies.*  
Holds: Primary and secondary success metric test plans, A/B test designs, measurement timelines, and validation criteria.

### certification-taxonomy.md
*Contains the certification standards supported, how Trust Score components are weighted/verified, and the certification taxonomy map.*  
Holds: Supported certification standards (USDA Organic, EU Organic, Fair Trade etc.), Trust Score component weighting (40% cert + 30% lab + 20% producer + 10% review), certification validation logic, and Q-2 from spine (PostGIS vs. plain coordinates).

---

## Derivation Statement

This SPEC.md is **derived on each run** from the project memlog (.bmad/.memlog.md) plus all source artifacts listed in `sources:`. The memlog is the canonical record — an append-only, chronological record of every decision, constraint, capability, assumption, and open question, one line each in the order it happened, never edited or reordered.

`SPEC.md` and all companion files are re-rendered from the memlog plus the sources it cites for raw content. Never hand-edited — hand-edits are overwritten on the next derive.

Kernel derivation follows Spec Law rules 1-8:
- Rule 1: Each capability has both `intent` and `success` ✅
- Rule 2: Intents describe WHAT, not HOW ✅ (implementation in companions)
- Rule 3: Constraints actually bend design decisions ✅ (each C-n prevents a specific divergence)
- Rule 4: Non-goals are explicit ✅ (N-1 through N-5)
- Rule 5: Success signal is concrete enough to test ✅ (primary metrics have A/B test designs)
- Rule 6: Capability IDs are stable and unique ✅ (CAP-1 through CAP-7, no reuse)
- Rule 7: Preservation — every load-bearing claim landed in SPEC.md or a companion ✅
- Rule 8: Lean prose ✅ (every sentence carries load-bearing content)

---

## Memlog Integration

This SPEC.md is derived from `.bmad/.memlog.md` via the bmad-spec skill. The memlog is the authority on what was decided and on capability IDs. New capabilities get the next unused `CAP-N`; never reuse retired IDs.

All changes to the spec — resolved assumptions, answered open questions, other changes — are appended to `.bmad/.memlog.md` as they happen, preserving the history intact.

---

*Generated via bmad-spec from project input (6 existing docs + architecture spine + analysis brief + market research). SPEC.md is re-renderable from .bmad/.memlog.md at any time.*