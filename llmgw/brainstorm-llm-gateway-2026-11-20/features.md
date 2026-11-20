# LLM Gateway — Feature Catalog

**Purpose:** Comprehensive, actionable feature set for designing and building an LLM gateway.
**Source:** Derived solely from this session's `.memlog.md` brainstorming log. No other requirements were assumed.

## Scope & design anchors
Recorded decisions that constrain every pillar below:
- **Provider-agnostic internal contract** — applications never bind to a vendor's SDK or schema.
- **Config-as-code policies** — declarative, versioned, approval-gated routing/safety/compliance rules.
- **Gateway as trust boundary** — treat model inputs *and* outputs as untrusted; redact and validate at the edge.

## Status legend
| Tag | Meaning (from log) |
| --- | --- |
| **MVP** | First deliverable; log's explicit MVP insight and 1-year core. |
| **Later** | Near-term follow-on after MVP. |
| **Advanced** | ~3-year / differentiating capability. |
| **Vision** | ~10-year / speculative-future / post-scarcity direction. |

---

## 1. API & Routing

### 1.1 Unified API surface
- **OpenAI-compatible endpoint — MVP.** Single facade so apps swap providers with no code changes; ship adapters for Anthropic, Gemini, Azure, and local inference (vLLM).
- **Provider-agnostic internal contract — MVP.** Enforce one normalized internal request/response shape; eliminate vendor lock-in.
- **Hot-swappable model backends — Later.** Swap OpenAI/Anthropic/Gemini/local backends via config, not redeploys.
- **Request/response transformation layer — MVP.** Normalize schemas and map parameters across vendors.
- **Response shaping — MVP.** Enforce JSON schema / structured outputs; normalize function/tool calls across vendors.
- **Dynamic context-window management — Later.** Auto-truncate, summarize, or map-reduce history to fit model limits.
- **Streaming passthrough — MVP.** SSE streaming responses coupled with real-time token/cost metering.
- **Managed prompt templates / versioned prompt IDs — Later.** Replace raw inline prompts with addressable, versioned prompt resources.

### 1.2 Routing & selection policies
- **Unified route policy (route + fallback + load-balance) — MVP.** One policy expressing primary model, fallback chain, and weighted pools.
- **Policy-driven model selection (cost / latency / quality) — MVP.** Differentiator vs. a basic proxy.
- **QoS lanes — Later.** Latency-optimized, cost-optimized, and quality-optimized request classes.
- **SLA/criticality prioritization & degraded-mode routing — Later.** Prioritize by SLA/criticality; route to degraded mode under pressure.
- **Auto model selection by SLO — Advanced.** Gateway picks cheapest/fastest model that still meets the SLO; continuous eval feedback by task/cost/latency/quality.
- **Provider diversification — Advanced.** Multi-vendor sourcing strategy with automatic provider diversification.
- **Geo/edge routing — Later.** Regional PoPs with geo-routing to the nearest provider region.
- **Canary & declarative routes — Later.** API-gateway patterns: plugins, middleware, declarative routes, canaries.
- **Feature-flag rollouts & A/B experiments — Later.** Gradual model rollouts and prompt/model experiments via flags.

### 1.3 Gateway-composed capabilities
- **RAG retrieval hooks + tool-call mediation — Later.** Compose retrieval and tool calling inside the gateway layer.
- **Prompt optimization hints & result ranking — Advanced.** Query rewriting / prompt-optimization hints and ranking of RAG outputs.

---

## 2. Auth, Tenancy, Quotas & Budgets

- **Gateway-issued virtual keys — MVP.** Replace hardcoded provider keys in apps with scoped, rotatable gateway tokens.
- **Centralized secrets vault — MVP.** Hold provider credentials in a vault integration; eliminate secret sprawl; rotation; no-secret logging.
- **Authentication & authorization — MVP.** Adapt OAuth/OIDC + RBAC for tenant/team-level access control.
- **Unified request pipeline — MVP.** Bundle authn/authz, quotas, and audit logging into a single request pipeline.
- **Token-aware rate limiting — MVP.** TPM/RPM/concurrency limits per key, user, team, or tenant.
- **Quotas & budgets — MVP.** Per-tenant/per-team quotas and budget ceilings.
- **Tenant isolation & fair scheduling — MVP.** Isolation, fair scheduling, and per-tenant quotas/budgets to stop noisy neighbors.
- **Priority tiers & graceful shedding — Later.** Overbooking/concurrency queues with priority boarding, graceful 429 shedding.
- **Spend caps & kill switches — MVP.** Hard spend caps, budget thresholds, and kill switches to prevent surprise bills.
- **Cost attribution & chargeback — MVP.** Centralized attribution replacing per-app billing; auditable double-entry usage ledger.

---

## 3. Reliability & Performance

- **Configurable retries — MVP.** Exponential backoff, jitter, and idempotency keys.
- **Adaptive throttling handling — MVP.** Adaptive backoff, token-bucket smoothing, and request queuing on provider throttling.
- **Provider failover — MVP.** Automatic failover to secondary provider/model using policy-based equivalence mapping.
- **Health-based ejection — Later.** Circuit-breaker/bulkhead patterns; auto-failover with health-based provider ejection and self-healing.
- **Declarative reconciliation — Advanced.** Desired-state config, health probes, and self-healing reconciliation (Kubernetes-style).
- **Latency mitigation — MVP.** Streaming-first responses, timeouts, hedged requests, and fast-model fallback.
- **Request tracking IDs — MVP.** Tracking IDs spanning retries, fallbacks, and tool calls for end-to-end tracing.

---

## 4. Caching

- **Exact cache — MVP.** Deterministic prompt/response cache with TTL and cache keys by model + params + hash.
- **Prompt-prefix caching — MVP.** Reuse shared prefixes to cut latency/cost.
- **Semantic cache — Advanced.** Combine with exact and prefix caching; semantic similarity lookup.
- **Shared embeddings cache — Advanced.** Cross-team shared embeddings cache to cut spend materially.
- **Edge response caching — Later.** CDN-style regional caching of deterministic prompts/responses.

---

## 5. Observability, Evals & FinOps

- **Real-time token/cost metering — MVP.** Meter tokens and cost on every request, including streaming.
- **Gateway-native tracing & metrics — MVP.** Shift instrumentation from apps to the gateway; OpenTelemetry end-to-end tracing.
- **Audit logging — MVP.** Request/response audit trail in the single request pipeline.
- **Replay & diffing — Later.** Prompt/response replay and diffing for debuggability.
- **Basic cost dashboard — MVP.** Visibility into spend from day one.
- **Per-request cost estimation — MVP.** Estimate cost before/at request time with budget enforcement and anomaly kill switches.
- **FinOps integration — Later.** Export metrics for forecasting and budget alerts.
- **Anomaly detection — Advanced.** Detect spend spikes, prompt abuse, and exfiltration patterns.
- **Eval harness / prod-traffic replay — Advanced.** Replay production traffic against candidate models; built-in eval/replay loop from prod traffic (key differentiator).
- **Dataset pipeline — Advanced.** Turn gateway logs into fine-tuning/distillation datasets, with consent and PII controls.

---

## 6. Safety, Security & Compliance

- **Configurable redaction — MVP.** Strip PII/secrets from prompts and logs via policy; retention controls; no-secret logging.
- **Untrusted output handling — MVP.** Validate/guardrail model outputs before returning them (reverse trust boundary).
- **Input/output guardrails — MVP.** Guardrails plus tool sandboxing and allow/deny policies.
- **Schema validation & repair — Later.** Schema validation, self-check/repair retries, and verifier models for bad/non-deterministic outputs.
- **Compliance choke point — MVP.** Data-residency routing, PII redaction, retention controls, and audit trails at the gateway.
- **Deep auditability & provenance — Advanced.** Watermark/provenance checks and abuse-response playbooks for misuse risk cases.
- **Policy-as-code for safety/compliance — Advanced.** Versioned, approval-gated safety/compliance/routing policies.
- **Verifiable privacy — Vision.** Confidential computing / attestation and provable data handling.

---

## 7. Developer Experience & Governance

- **Declarative config-as-code — MVP.** All routing/safety policies declared as versioned code; hot-swap without deploys.
- **Plugin/middleware architecture — Later.** API-gateway-style extensibility for custom behavior.
- **Developer sandbox mode — Later.** Mock models and recorded fixtures for testing.
- **Versioned prompts & replay/diffing — Later.** Versioned prompt IDs plus replay/diff tooling for debugging.
- **Feature flags & canaries — Later.** Safe gradual rollout and experimentation workflow.
- **Policy versioning & approvals — Advanced.** Approval gates on policy/prompt changes.
- **Zero-config DX & self-optimizing SLOs — Vision.** Seamless global routing with near-zero configuration.

---

## 8. Future / out-of-MVP directions
Deferred by explicit decision (do not build in MVP):
- Autonomous optimization, full eval harness, advanced privacy attestation.
- Agent-to-agent gateway mediating tool use, permissions, and inter-agent contracts (**Vision**).
- Verifiable privacy / confidential-computing attestation (**Vision**).
- Post-scarcity cheap inference: shift emphasis from cost toward quality, safety, and provenance (**Vision**).

## 9. MVP acceptance set (log-derived)
Ship these first:
1. OpenAI-compatible proxy + provider adapters (Anthropic/Gemini/Azure/local).
2. Provider-agnostic internal contract + request/response transformation + structured outputs.
3. Virtual keys, vaulted secrets, OAuth/OIDC + RBAC, tenant isolation, token-aware rate limits/quotas.
4. Logging, OpenTelemetry tracing, real-time token/cost metering, basic cost dashboard, spend caps/kill switches.
5. Basic failover, retries/backoff, timeouts, streaming-first responses, tracking IDs.
6. Exact + prefix caching.
7. Core redaction, output validation, and compliance choke point (residency/retention/audit).
