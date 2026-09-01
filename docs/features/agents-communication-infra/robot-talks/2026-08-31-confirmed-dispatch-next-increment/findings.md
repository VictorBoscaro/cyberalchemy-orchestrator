---
node_type: agent-findings
status: human-gate-approved
date: 2026-08-31
topic: confirmed-dispatch-next-increment
---

# Findings: ConfirmedDispatch next increment

## Executive synthesis

The next safe action is not continuation code and not yet the writer itself. First close one small,
reviewed confirmation-authority contract with a canonical fixture and golden vector. That contract
must make the approval observation, three distinct digests, deterministic identity derivation,
confirmed graph expansion and opening-intent boundary executable. Then implement one bounded writer
SWU that ends at durable `opening_pending`. Only after that evidence passes should TASK-CONT-001
readiness be reissued.

## Cross-layer tensions

### RT-T01 — Simple consent versus exact runtime authority

- Product layer: the user may approve with a simple conversational action such as "pode seguir";
  chat now and a future UI are interchangeable ingress surfaces.
- Contract/runtime layer: authority requires an authenticated principal, the exact dispatch and
  revision, approved bytes/digests, `runtime-managed` mode and a durable observation binding.
- Tension: the current contract names `confirmed_by` and `confirmed_at`, but not an immutable
  confirmation-observation reference and digest. The sentence alone is not replayable evidence.
- Severity: **block** for a real chat-to-authority claim.
- Evidence: [Authority report, findings 1–4 and gap 1](reports/01-authority-product.md).
- Proposed disposition: **real + actionable** — add a versioned confirmation-observation record
  bound to principal, channel, host observation identity, dispatch revision, presented spec digest
  and timestamp; transports may differ but must yield the same canonical semantics.
- Human disposition: **real + actionable; approved**. CONF-000 will define the immutable
  confirmation-observation record before writer implementation.

### RT-T02 — Server-side DispatchSpec resolution versus missing executable projection

- Interface layer: the command service is required to read and hash pending bytes, compile/finalize
  the exact `DispatchSpec`, freeze versions and capability resolution, then accept confirmation.
- Architecture/implementation layer: candidate-to-`DispatchSpec` confirmation mapping is still
  excluded, `DispatchSpec.group_graph` lacks a concrete bounded expansion schema, and no runtime
  compiler implements this path.
- Tension: a writer cannot prove JSON-to-authority by accepting caller-supplied expanded authority,
  but it also has no canonical server-side projection to run.
- Severity: **block** before writer code.
- Evidence: [Persistence report, finding 4](reports/02-persistence-transaction.md) and
  [slicing report, findings 1–2](reports/03-slicing-verification.md).
- Proposed disposition: **real + actionable** — freeze one bounded admitted input and golden vector
  for the exact `author:0 -> reviewer:0 -> author:1` graph before implementation.
- Human disposition: **real + actionable; approved**. A reviewed bounded projection and golden
  vector must precede writer code.

### RT-T03 — Confirmation atomic unit versus implicit continuation preallocation

- Confirmation layer: O-CONF explicitly creates `ConfirmedDispatch`, `Run`, `run.created`,
  `audit_opening.requested` and the opening intent.
- Continuation layer: O-CONT-S5 requires the same confirmation to have preallocated the
  `continuation_id`, two ordered mappings and source-message identities.
- Tension: graph and mapping creation are not explicit O-CONF postconditions or covered by
  T-ACI-AUTH1; the atomic unit is inferred across documents.
- Severity: **block** because TASK-CONT-001 cannot verify its authority otherwise.
- Evidence: [Persistence report, finding 2](reports/02-persistence-transaction.md) and
  [slicing report, local tension 2](reports/03-slicing-verification.md).
- Proposed disposition: **real + actionable** — promote graph artifact/row, continuation identity
  and exactly two normalized mapping rows into the confirmation operation and test contract.
- Human disposition: **real + actionable; approved**. Graph, continuation and both mappings become
  explicit atomic confirmation outputs.

### RT-T04 — Ratified effect-intent contract versus missing outbox primitive

- Specification layer: confirmation must atomically persist a durable audit-opening effect intent
  with the run facts and receipt.
- Implementation layer: the journal supports transactional mutation and failpoints, but there is no
  general `effect_intents` table; only an operation-specific sandbox launch table exists.
- Tension: reusing the journal is coherent, but the new writer cannot represent the required
  opening effect without adding a new outbox surface.
- Severity: **high** implementation decision.
- Evidence: [Persistence report, finding 3 and local tension 2](reports/02-persistence-transaction.md).
- Proposed disposition: **real + actionable** — add the ratified generic `effect_intents` schema in
  the prerequisite migration, but implement only creation of one unclaimed audit-opening intent;
  claiming/materialization remains outside the SWU.
- Human disposition: **real + actionable; approved**. Use a generic `effect_intents` outbox; this
  slice creates only the unclaimed audit-opening intent.

### RT-T05 — Identity-level replay versus key-level journal idempotency

- Operation layer: the same dispatch/authority digest must return the original receipt even when
  observed again; the same identity with a different authority must conflict permanently.
- Journal layer: current replay is keyed by `(scope_key, idempotency_key)`, and the command digest
  includes that key.
- Tension: a new client idempotency key for the same confirmed identity does not automatically
  return the original receipt; an unlocked pre-read would race.
- Severity: **high** for convergence and crash recovery.
- Evidence: [Persistence report, finding 5 and local tension 4](reports/02-persistence-transaction.md).
- Proposed disposition: **real + actionable** — specify an in-transaction
  `dispatch_id + confirmed_authority_digest` identity lookup that returns the first accepted
  receipt; a digest mismatch conflicts.
- Human disposition: **real + actionable; approved**. CONF-000 must specify identity-level replay
  and permanent authority-digest conflict semantics.

### RT-T06 — Current work pack versus the prerequisite now selected

- Ledger/readiness layer: durable confirmation is selected and continuation correctly remains
  blocked until its prerequisite is accepted.
- Work-pack layer: the old decision gate still asks A/B, the dry-run says zero blockers,
  TASK-CONT-001 assumes seeded confirmed data and already reserves migration 012.
- Tension: beginning either task now creates contradictory authority and a migration collision.
- Severity: **block** for code entry.
- Evidence: [Slicing report, finding 3 and gaps 4–5](reports/03-slicing-verification.md).
- Proposed disposition: **real + actionable** — create CONF-000/CONF-001 before W1, allocate
  migration 012 to confirmation, move TASK-CONT-001 to 013, remove the seeded-authority shortcut
  and refresh gate/dry-run/readiness records.
- Human disposition: **real + actionable; approved**. CONF-001 takes migration 012;
  TASK-CONT-001 moves to 013 and loses the seeded-authority shortcut.

### RT-T07 — New authority source versus legacy dispatch foreign keys

- Governance layer: `dispatch_links` may not act as runtime-managed confirmation authority.
- Persistence layer: current host workflow bindings and agent attempts still reference
  `dispatch_links` through foreign keys.
- Tension: the writer can establish independent authority, but later runtime attempts still depend
  structurally on a legacy row. Inserting that row is acceptable only as an explicitly
  non-authoritative compatibility projection; using it to satisfy O-CONT-S5 is forbidden.
- Severity: **high**, potentially blocking end-to-end execution but not writer acceptance.
- Evidence: [Persistence report, local tension 1](reports/02-persistence-transaction.md).
- Proposed disposition: **real + staged** — keep decoupling outside CONF-001, record the legacy row
  as a non-authoritative compatibility dependency, and require an explicit follow-up decision
  before claiming a fully runtime-managed attempt path.
- Human disposition: **real + staged; approved**. Legacy-FK decoupling remains outside CONF-001 but
  must occur before a complete runtime-managed execution claim.

## Recommended sequence

### CONF-000 — Contract and golden-vector closure (no runtime code)

Freeze and independently review:

1. the versioned confirmation-observation shape and trusted issuer boundary;
2. distinct `pending_sheet_digest`, `dispatch_spec_digest` and
   `confirmed_authority_digest` meanings;
3. one admitted bounded pending-sheet/`DispatchSpec` fixture;
4. deterministic, versioned derivation for run, graph, continuation, mapping, source-message and
   opening-effect identities;
5. the exact graph artifact/row and two normalized mapping rows;
6. O-CONF postconditions and expanded T-ACI-AUTH1 golden/negative vectors;
7. the success boundary: durable `opening_pending` with one unclaimed effect intent.

### CONF-001 — Durable confirmation writer

Use migration 012 and the existing single SQLite/journal writer to atomically finalize authority
artifacts, create `ConfirmedDispatch`/`Run`/graph/mappings, append both confirmation events, create
one generic opening intent, advance the run head and return a stable receipt. Include full
failpoint, reopen, lost-response, identity replay and conflict evidence. Do not call a provider,
materialize the external audit row, suspend an agent or execute continuation.

### Reissue continuation readiness

After CONF-001 passes focused tests and independent review, update the work pack, shift
TASK-CONT-001's migration to 013, remove seeded authority, and rerun readiness. The unrelated global
test drift remains FLAG/BLOCK and cannot be converted into a feature-wide PASS.

## Human gate

The repository owner approved the recommended dispositions in chat on 2026-08-31. The accepted
decisions are:

1. CONF-000 precedes CONF-001 and closes the immutable confirmation observation, digest taxonomy,
   deterministic identity derivation, bounded graph projection and golden vectors.
2. CONF-001 uses a generic `effect_intents` outbox and ends at durable `opening_pending`; external
   audit materialization is deferred.
3. Legacy-FK decoupling is staged after CONF-001 and remains required before a complete
   runtime-managed execution claim.
4. CONF-001 owns migration 012; TASK-CONT-001 moves to migration 013 and cannot use seeded
   confirmation authority.

This gate authorizes preparation of the separate CONF-000 planning/contract route. It does not by
itself authorize runtime code mutation or claim that any prerequisite is implemented.
