# BioViva — Business Analysis Brief

**Analyst**: Mary, Business Analyst
**Date**: 2026-11-05
**Project**: BioViva — Ecommerce platform for bio-products
**Altitude**: Epic (system-wide)
**Purpose**: Build-substrate (consistency contract for independently-built crates)

---

## 1. Problem Statement — Verified ✅

**Existing articulation** (PROJECT_BRIEF.md:6-7):
> "Consumers lack trust and transparency when buying bio products online - uncertainty about authenticity, freshness, and origin undermines purchasing decisions."

**Corroborating evidence** across all 6 docs:

| Doc | Supporting Evidence |
| --- | --- |
| `core-features.md:3-8` | JTBD: "Users hire BioViva to discover authentic bio products they can trust for quality and origin", "Access the health benefits promised by genuine olive oil, honey, and herbal essences", "Connect with the story behind each product" |
| `ux-design.md:5-10` | Empathy map: Maya "wants to make sure this is real olive oil from the region it claims", "concerned about being misled", "proud when she finds authentic product" |
| `architecture.md:39-45` | Trust-as-Code: "Each product has a Trust Score (0-100) calculated from: Certification validity (40%), Lab test results (30%), Producer reputation (20%), Review recency (10%)" |
| `ARCHITECTURE_SUMMARY.md:15-16` | Key invariants: "Trust score calculation, freshness lifecycle (Fresh/Ripe/Aging/Archived), harvest date validation" |

**Verdict**: Problem statement is well-defined, validated across all stakeholder artifacts (business, UX, technical). **No revision needed**.

---

## 2. Solution — Partially Articulated ⚠️

**Existing articulation** (PROJECT_BRIEF.md:9-10):
> "BioViva - a platform that makes every product traceable, every farmer visible, and every purchase confidence-inspiring through sensory-rich design and ecosystem-based architecture."

**What's clear**:
- ✅ Traceability (batch/lot numbering, origin mapping, certification badges — `core-features.md:13-16`)
- ✅ Farmer visibility (profiles with photos, harvest diaries, sustainability metrics — `core-features.md:23-26`)
- ✅ Confidence-inspiring (Trust Score visible on all product cards — `architecture.md:39-45`, `ARCHITECTURE_SUMMARY.md:31`)
- ✅ Sensory-rich design (aroma notes, flavor profiles, texture descriptors — `ux-design.md:33-49`)

**What's missing or ambiguous**:

| Gap | Evidence | Risk |
| --- | --- | --- |
| **Market sizing / TAM** | Not quantified in any doc | Can't prioritize features without knowing addressable market |
| **Pricing model** | No mention of price points, subscription tiers, or certification cost-pass-through | Consumers need to know: "Why pay more for bio?" |
| **Regulatory / certification landscape** | `architecture.md:48-51` mentions "automated validation against certification databases" but no specifics on which certifications (USDA Organic, EU Organic, Fair Trade, etc.) | If the certification list is too narrow, the Trust Score feels fake |
| **Consumer decision journey** | UX flow maps "taste quiz → recommendations → farmer profile → purchase" but no post-purchase flow beyond "freshness alerts" | Missing: repeat purchase, gift, community engagement loops |
| **Competitive differentiation beyond "trust"** | Core thesis is "trust + transparency" but 5 other ecommerce platforms also offer "authenticity" claims | Need a defensible wedge beyond "we have trust scores" |

**Verdict**: Solution is compelling and internally consistent, but **lacks market-context validation**. The architecture supports the stated solution, but we don't know if the market will choose BioViva over alternatives without more research.

---

## 3. Target Audience — Well-Defined ✅

**Existing articulation** (PROJECT_BRIEF.md:19-23):
- Health-conscious consumers aged 25-55
- Culinary enthusiasts seeking quality ingredients
- People with dietary restrictions requiring authentic products
- Gift-givers wanting meaningful, story-rich presents

**Corroborating evidence**:

| Segment | Evidence from docs |
| --- | --- |
| "Health-Conscious Maya" (ux-design.md:5) | 35, values authenticity, buys olive oil/honey regularly, concerned about quality/origin |
| Pain points | "Uncertainty about product authenticity", "Difficulty finding detailed origin info", "Confusing certification jargon", "Worry about freshness/quality degradation" |
| Desires | "Clear, trustworthy sourcing info", "Simple freshness indicators", "Educational content that builds confidence", "Connection to the producer/farmer" |
| Success metrics | "Trust score visibility → 40% increase in conversion", "Seasonal collections → 25% higher AOV", "Producer story engagement → 30% repeat purchase", "Freshness alerts → 15% reduction in expired complaints" |

**Verdict**: Target audience is well-defined with persona, pain points, desires, and quantified success metrics. **No revision needed**.

---

## 4. Architecture Alignment — Strong ✅

**How the architecture enables the business goals**:

| Business Goal | Architectural Enabler | AD in Spine |
| --- | --- | --- |
| **Trust visibility** → 40% conversion lift | Trust Score (AD-5): 40% cert + 30% lab + 20% producer + 10% review, visible on all product cards | AD-5 |
| **Seasonal relevance** → 25% higher AOV | Season-first catalog (AD-6 freshness lifecycle + implicit season mapping) | AD-6 |
| **Producer engagement** → 30% repeat | Producer stories in bio-producers crate; CertificationValidator (AD-3 repo pattern) | AD-3, AD-7 |
| **Freshness reduction** → 15% fewer expired complaints | FreshnessState enum + handler enforcement (AD-6): Order valid only for Fresh/Ripe; Search filters by min trust + seasonal availability | AD-6 |
| **Data transparency** → no platform lock-in | Single PostgreSQL pool (AD-2), Repository pattern (AD-3), DI of AuthClaims (AD-4) | AD-2, AD-3, AD-4 |

**Architecture quality assessment**:

| Quality attribute | Status | Evidence |
| --- | --- | --- |
| **Modularity** (7 crates, clear boundaries) | ✅ Strong | ARCHITECTURE_SUMMARY.md:4-5; spine AD-1, AD-3 |
| **Testability** (each crate can be built/tested independently) | ✅ Strong | BUILD_PLAN.md:361-378 build order; verify-build.sh |
| **Deployability** (single Docker container) | ✅ Strong | ARCHITECTURE_SUMMARY.md:163-198; BUILD_PLAN.md:233-254; spine AD-8 |
| **Extensibility** (add new context without modifying existing) | ✅ Strong | Open/Closed principle (ARCHITECTURE_SUMMARY.md:202-203); spine AD-1 |
| **Observability** (tracing, errors, metrics) | ⚠️ Partial | Tracing subscriber mentioned (BUILD_PLAN.md:159); BioError with context (ARCHITECTURE_SUMMARY.md:207); no explicit metrics or logging conventions in conventions table |
| **Security** (auth, data protection) | ✅ Strong | AD-4: JWT middleware; Argon2 params (C-3); role-permission checks before handler execution |
| **Performance** (single DB pool, connection limits) | ⚠️ Partial | AD-2: single pool; no connection pooling strategy documented (pool size, max connections) |

**Verdict**: Architecture strongly aligns with business goals. The 7 bounded contexts map cleanly to the 4 primary value propositions (trust, seasonality, producer engagement, freshness). Two improvements would strengthen the alignment:

1. **Add metrics/conventions for observability** — the conventions table in the spine (naming, data formats, state/cross-cutting) could include tracing fields, error envelope shape, and DB pool config
2. **Document the certification taxonomy** — which certifications are supported, how they map to the 40% Trust Score component

---

## 5. Research Opportunities — Where to Focus Next

Per the bmad-agent-analyst menu, these `bmad-deep-recon` research types would add the most business value:

| Research Type | What It Answers | Why It Matters for Bioviva |
| --- | --- | --- |
| **Market** | TAM, growth rate, key players in "authentic food ecommerce" | Prioritize features; validate the 40% conversion claim; set revenue targets |
| **Domain** | Certification bodies, harvest cycles, geo-origin mapping standards (PostGIS vs. plain coords) | Fill Q-2 in the spine (PostGIS question); ensure Trust Score components are verifiable |
| **Competitive** | Direct competitors (e.g., Olive Oil Club, local honey subscriptions), indirect (Amazon Fresh, specialty food stores) | Define the defensible wedge beyond "trust scores" |
| **User-voice** | Reviews, forum discussions, Reddit threads about buying bio products online | Validate Maya's pain points; uncover unmet needs (e.g., "I wish I knew the harvest year, not just trust score") |
| **Technical** (already done by architect) | Rust/Axum/PostgreSQL viability, scaling limits, migration strategy | Confirmed viable; now need business-level technical requirements |

**Recommended next step**: Run `bmad-deep-recon` with **market** and **user-voice** research types to validate the problem-solution fit before committing to the full build sequence.

---

## 6. Action Recommendations

| Priority | Action | Owner | Evidence |
| --- | --- | --- | --- |
| **P0** | Validate market demand — TAM, competitor feature matrix, price sensitivity | Analyst + PM | Without this, risk building a well-architected product nobody will pay for |
| **P1** | Document certification taxonomy — which standards, how Trust Score components are weighted/verified | Architect + PM | Q-2 in spine (PostGIS/origin mapping); missing from any doc; affects AD-5 credibility |
| **P2** | Add observability conventions to spine — tracing fields, error envelope, DB pool config | Architect | Conventions table missing this; makes it harder to diagnose issues in 7 independently-built crates |
| **P3** | Postpone bio-search + bio-users preference integration — defer to Q-5 in spine | Architect + Dev lead | Q-5 deferred reason: "When subscription flow is implemented in bio-orders"; avoid premature coupling |
| **P4** | Produce PRFAQ or product brief using working-backwards method | PM + Analyst | PROJECT_BRIEF.md has the seed; bmad-prfaq or bmad-product-brief would formalize it |

---

## 7. Summary Verdict

| Dimension | Rating | Notes |
| --- | --- | --- |
| **Problem articulation** | ⭐⭐⭐⭐✅ | Well-defined, validated across all 6 docs |
| **Solution fit** | ⭐⭐⭐✅ | Compelling, internally consistent, but needs market validation |
| **Target audience** | ⭐⭐⭐⭐✅ | Persona "Maya" defined; pain points/desires quantified; success metrics stated |
| **Architecture alignment** | ⭐⭐⭐⭐✅ | 7 contexts map to 4 value propositions; strong modularity, deployability, extensibility |
| **Research gaps** | ⭐⭐⭐✅ | Market sizing, certification taxonomy, user-voice validation, observability conventions |
| **Build risk** | ⭐⭐⭐✅ | Dependency graph correct; bio-orders is the hardest path; all greenfield artifacts (Cargo.toml, main.rs, Dockerfile, .env.example) still need Phase 0 creation |

**Overall**: **Build viable, but validate market first**. The architecture is solid (spine + memlog + C4 + build order all produced), the business problem is well-defined, and the target audience is understood. The missing pieces are market-context evidence and a few documentation conventions. Without market validation, there's a risk of building a beautifully architected product that doesn't find product-market fit.

**Next immediate step**: Run bmad-deep-recon with market research type to estimate TAM and validate the 40% Trust Score → conversion claim with potential users.