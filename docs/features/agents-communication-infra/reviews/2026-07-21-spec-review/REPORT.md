---
feature: agents-communication-infra
review_date: 2026-07-21
final_review_set_sha256: ece990403fdadd40afd24e166eb67c38bb0bf086383590491cf0cb19c4346165
final_verdict: PASS
runtime_gate: block
---

# Independent SPEC Review Report

## Review protocol

Three reviewers worked independently across authority/architecture, formal traceability and
operability/failure recovery. Each pass used an ordered SHA-256 manifest, was read-only, prohibited
cross-reviewer consultation and required precise evidence for `FIX` or `BLOCK`.

| Stage | Authority / architecture | Formal / traceability | Operability / failures | Manifest |
|---|---|---|---|---|
| Initial review | FIX | FIX | BLOCK | [BASELINE](BASELINE.md) |
| Post-remediation closure | FIX | FIX | BLOCK | [POST-REMEDIATION](POST-REMEDIATION.md) |
| Final closure after accepted fixes | PASS | PASS | PASS | [FINAL-BASELINE](FINAL-BASELINE.md) |

## Accepted findings and disposition

All substantiated findings were accepted and resolved in the specification:

- cross-aggregate start races now use transactional `prerequisite_heads[]` checks;
- invocation ordering is `AgentInvocationPlan -> MaterializedAgentInvocation +
  EffectiveInputArtifact -> sealed AgentExecutionRequest -> sandboxed start`;
- effect outcomes check terminal idempotency before `claimed + claim_epoch` fencing and commit the
  outcome, receipt, event and head atomically;
- `publication.persisted` means durable candidate only; official acceptance occurs only after
  parent-side receipt verification;
- authoritative `publication_candidates` are separate from official `messages`, with a partial
  active-key constraint and CAS-governed unknown-attempt abandonment;
- persisted `PublicationReceipt` bytes are stable; optional `transport_replayed` metadata remains
  outside the receipt;
- reveal provenance, terminal results, budgets, sandbox policy, model heterogeneity and usage/cost
  persistence have explicit contracts and tests;
- the HTTP confirmation boundary maps every `ConfirmRuntimeDispatch` input;
- registry, glossary, task ownership and reverse concept-to-test evidence are exact 79/79 sets;
- discovery v0.2.1 and every normative `derived-from` reference are version-aligned.

No finding was rejected. A separate first-class registry concept for receipt recovery was not added:
recovery is deliberately specified as behavior of receipt verification/reconciliation rather than a
second public write authority.

## Remaining blockers

These are implementation evidence gates, not defects in the approved SPEC:

- W0 ADR acceptance and production SQLite/WAL transaction, crash and sole-writer proofs;
- EG-1 product-value evidence;
- target-host sandbox, credential and retention enforcement (`OQ-SANDBOX` included);
- real Codex adapter conformance and usage completeness in L2;
- a second provider and mixed-provider proof in L3;
- host-loss, multi-host and multi-tenant behavior, which remain outside the initial boundary.

Therefore `specAuthoringGate=pass` and `runtimeGate=block` are both intentional and consistent.
