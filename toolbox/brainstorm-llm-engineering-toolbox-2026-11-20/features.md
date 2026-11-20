# LLM Engineering Toolbox — Features

## Product thesis

The toolbox is an evidence machine: versioned artifacts, executable evals, and replayable traces are the core, and routing-style ideas are downstream consumers of that evidence rather than the product itself. It is a local-first, CLI-first evidence layer for LLM engineering — eval-driven, git-native, and model-agnostic. The crown jewels are deliberately cut: library and CLI before UI, deterministic checks plus human review instead of LLM-as-judge, and no hosted service — it runs locally against the user's own keys, built on git, pytest, and OpenTelemetry rather than new infrastructure.

## Feature groups

### Versioning and reproducibility

- **Immutable build bundle** — model + prompt + params + tools treated as one versioned artifact with a digest (prompts are source code, not notebook strings).
- **Prompt git** — diff, blame, branch, and revert for prompts, with semantic conflict detection.
- **One-click rollback tied to eval score** — the unlogged prompt change becomes a signed, reversible event.
- **Model-version pinning and deprecation alerts** — unpinned aliases are replaced with pinned versions; "model pension" auto-migrates off deprecated models with evidence of equivalence.
- **Digest-keyed cache invalidation** — cached results are invalidated by prompt digest so regressions cannot stay masked.
- **Dataset snapshots beside the repo** — golden data survives staff turnover as repo-adjacent, signed snapshots.
- **Experiment cards** — diffable JSON bundling prompt, dataset, eval, and result; merges the electronic-lab-notebook idea, the signed/timestamped "reagents" record, and the shareable experiment card into one file format.
- **Semantic diff** — "this prompt change shifted 7 cases to fail, and here is why."

### Evaluation and quality gates

- **Eval runner (better-or-worse)** — scores a CSV of cases and diffs against a baseline; merges the "pytest for prompts" surface (fixtures, parametrize, snapshot assertions) with the single eval runner that answers "did it actually get better?" with evidence.
- **Regression gate on every commit** — deploy gate is an eval score threshold, with a canary report auto-commented on the PR.
- **Distributional scoring** — treat nondeterminism as a test input: sample N times, judge a distribution, and use p95 pass-rate SLAs.
- **Incremental eval** — rerun only affected cases; 10,000 cases in under a minute via parallel sampling and caching.
- **Two-tier eval** — fast smoke gate plus deep nightly suite; nightly score backfill feeds a trend dashboard.
- **Deterministic checks + human review** — LLM-as-judge is deleted; the linter and evaluator are merged to flag ambiguous instructions before a run costs anything.
- **Executable specification** — the eval set is the spec of the product, and every improvement claim is a hypothesis with an experiment ID.
- **Hardened scoring** — holdout set with a secret salt rotated weekly, plus negative selection that generates cases the system must not do.
- **Eval-case commons / meta-eval** — shared library of anonymized eval cases (not prompts), and a meta-eval scoring which toolbox features actually improved outcomes.

### Observability and debugging

- **Replayability (one trace format)** — merges flight recorder (last-1000-calls, crash-surviving buffer), time-travel debugging (scrub the timeline, see exact context at each step), and one-click repro from a single trace ID; one format powers all three.
- **One-line call logging** — middleware logging prompt digest, model, tokens, and latency on one line.
- **Per-call token ledger with anomaly alerts** — every model call is a measurable transaction; tracing adds cost attribution down to feature, tenant, and user.
- **Structured step trace with reason receipts** — merges the structured trace with tool I/O, the streaming "why did it do that" debug tail, and a mandatory reason receipt per step to explain, e.g., why an agent looped 14 times.
- **Token-stream oscilloscope** — live TTFT, latency, and token cadence.
- **Failure minimization** — merges delta debugging (reverse a failing output into the minimal input that still breaks it) and backward eval (find the prompt token that caused a bad answer).
- **Incident bundles** — merges one-click issue bundles (complaint to exact trace and failing case), self-contained audit bundles, and auto-generated runbooks from the last incident's trace.
- **Anomaly-only digest** — a digest of notable events instead of a trace firehose.

### Data and grounding

- **Golden-set curation** — one command regenerates the golden set from approved traces built from real traffic, with a scanner for PII at ingest and at call time.
- **RAG soil test** — sample the corpus and report freshness, gaps, and duplication; a consistency checker catches drifting embedding and text stores.
- **Retrieval EXPLAIN + empty-result alarms** — database-style EXPLAIN shows why the wrong chunk was returned, with alarms and a fallback policy for silent empty retrieval.
- **Untrusted retrieved context** — retrieved context carries provenance tags, and a data-lineage report shows which prompts and data touched which output.
- **Context budget allocator** — context windows are an explicit budget with receipts, relevance scoring, and an eviction log.
- **Wind tunnel** — replay a fixed traffic corpus against builds under identical conditions, including side-by-side RAG chunking-strategy comparisons.
- **Mined few-shots and synthetic reuse** — replace handwritten few-shots with examples auto-mined from logs; reuse production traces as a synthetic set for a router or distilled model.
- **Eval harness as load-test generator** — reuse the eval harness for capacity planning.

### Cost and routing

- **Cost autopilot** — route each call to the cheapest model likely to clear the quality bar for that specific task.
- **Model CV and compatibility matrix** — auto-refreshed measured strengths per model on your tasks, plus a matrix of model versions against supported features.
- **Spend forecast** — projected cost per 1k tasks by candidate model; swap a paid model for a local one behind the same eval suite and see the delta.
- **Cost circuit breaker** — cost is a hard runtime constraint, not an after-the-fact report.
- **Scout/verifier routing** — merges cheap scout models exploring with a strong solver for the hard residue, and a fast weak model paired with a slow verifier that wakes only on doubt.

### Safety and control

- **Abstain channel and safe error taxonomy** — merges a confidence-plus-abstain channel ("I don't know") with a taxonomy mapping raw model errors to safe user-facing messages.
- **Typed tool contracts** — tool calls are typed signatures with contracts; merges in schema-validator middleware so free-text parsing is unnecessary.
- **Local redaction** — pre-flight redactor strips secrets and PII before prompts or traces leave the machine.
- **Step and concurrency budgets** — hard budgets with graceful degradation instead of infinite agent loops.
- **Scarce human review** — route only uncertain cases to humans; merges approval checkpoints before autonomous actions with suggest mode (tool proposes, human approves).
- **Replayable evidence packet** — self-contained per-release audit bundle of jailbreak and red-team results, provable to an auditor.
- **Adversarial red-team agent** — an agent whose only job is finding prompts that beat the evaluator.
- **Provenance watermark** — watermark outputs so provenance survives copy-paste.

### Authoring ergonomics

- **Prompt compiler** — type-check variables and catch missing placeholders before runtime; targets a model the way a C compiler targets a CPU.
- **Prompt lint as pre-commit gate** — lint runs before a run is spent.
- **Intent-to-scaffold** — merges turning a vague job-to-be-done into a testable prompt spec and sketch-to-CAD (rough natural-language intent into a structured prompt scaffold).
- **Variant scratchpad** — side-by-side outputs from three prompt variants.
- **Retrieval preview pane** — preview retrieved context while authoring.
- **Single-source parameterization** — prompts parameterized by locale and persona from one source of truth, via templates with a task-adapter plugin slot.
- **Synthetic test generator** — generate test cases from the prompt.
- **Prompt registry** — a registry with owners and reviews so the best prompt does not live in one head.

### Agents and orchestration

- **Conversation state machine** — explicit transitions and invariants rather than ad-hoc loops.
- **A/B prompt variants** — traffic splitting with guardrails for prompt variants.
- **Darwinian prompts** — spawn variants, score them, breed winners, retire losers.
- **Shared context breadcrumbs** — a context layer where agents leave breadcrumbs for the next agent.
- **Flocking workers** — local rules align agent workers with no central orchestrator.
- **Antifragile staging** — inject faults in staging so the pipeline learns to route around them.
- **Self-filing bug tickets** — an agent files its own ticket when it detects a novel failure pattern.

## Priority

| Bucket | Features |
|---|---|
| **Must** | Eval runner with regression gate; versioned prompt/model/data bundles with rollback; trace + token ledger with one-click repro; golden sets from approved traces with PII redaction; CLI-first library surface |
| **Should** | Cost autopilot and model CV; abstain plus safety checks plus step budgets; structured step traces and budgets |
| **Could** | Semantic diff; time-travel debugging; eval-case commons; self-healing prompts; meta-eval of the toolbox itself |
| **Won't this time** | Hosted service and marketplace; elaborate UI; autonomous agent fleet; LLM-written rubrics |

## MVP build sequence

1. **Call logging and trace format** — one line per call carries prompt digest, model, tokens, and latency, and one trace ID reproduces a call locally.
2. **Eval runner and regression gate** — a CSV of cases scores against a baseline and every commit gets a better-or-worse verdict.
3. **Versioned bundles and rollback** — any regression rolls back to a prior signed bundle with its eval score.
4. **Golden-set curation** — the golden set is regenerable from approved traces with PII redacted at ingest and at call time.

## Non-obvious bets

- **Red-team agent beats the evaluator** — a predator-prey loop where an agent's only job is finding prompts that beat the evaluator turns evals from a static score into an adversarial process that stays honest; reinforced by a weekly-rotating secret-salt holdout set.
- **60-minute CLI** — the buried winners are constraint-derived: a CLI that scores a CSV and diffs against a baseline, one-line call logging, and experiment cards as diffable files. The whole toolbox is testable before any UI exists, under a $0 mandate (git, pytest, OpenTelemetry), as a single binary with offline replay from recorded fixtures.
- **Two-tier eval rhythm** — the real tension is not quality vs cost but speed vs rigor; a fast smoke gate plus a deep nightly suite resolves it, with cached results under a staleness budget and incremental reruns.
