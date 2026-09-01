# Decision Gate — Resumable Dispatch Feedback

## Result

`RESOLVED`: option A, durable runtime confirmation, was selected by the user on 2026-08-31.
This decision authorizes the local CONF-000 contract/oracle slice and, after its readiness gate,
the CONF-001 durable writer. It does not authorize TASK-CONT-001 before CONF-001 verification,
L2 real-provider admission, production cutover, commit, push or deploy.

The technical component sequence through BUS-001 is now complete and independently reviewed. The
current result for consequential continuation work is `BLOCK` at `PRODUCT-PASS`.

## Hard blocker — PRODUCT-PASS

The next authority package cannot be inferred from the component fixture. Product must supply:

- exact revision-instruction bytes, reference and digest;
- actual prompt bytes, references and digests;
- role and task references;
- `provider_ref` when it is distinct from the other selected references;
- concrete resource-budget, sandbox and execution/authority-fence policies; and
- a complete canonical audit-opening 0.6.4 row mapping, including dispatch type/route, goal,
  context, approver, agents and every remaining required field.

These are not presentation-only defaults: they change `confirmed_authority_digest`. Real opening
and execution therefore require a new dispatch identity, a CONF v2 authority package and a new
explicit user confirmation. CONF v1 remains a component fixture and cannot be silently upgraded.

Until that decision package exists, OPEN, positive Run transition, RESUME, WORKER and VERIFY remain
blocked. HEADS-001 and BUS-001 retain their component-level `PASS / KEEP`; CONT-002 remains
unpromoted.

## Historical resolved blocker — confirmation authority source

O-CONT-S5 requires suspension to consume a continuation identity and two mappings preallocated by
the confirmed turn graph. At the 2026-08-31 gate, the runtime had neither a `ConfirmedDispatch`
writer nor a persisted confirmed turn graph, and `dispatch_links` could not supply runtime-managed
authority. CONF-001 later implemented and independently verified the writer/graph; CONT-001 then
consumed that authority and is also `implemented-reviewed-pass`.

| Option | Benefit | Cost/risk | Downstream impact |
|---|---|---|---|
| A — durable runtime confirmation (recommended) | Proves the real JSON-to-authority path and lets suspension derive, rather than trust, its identity/mappings | Adds a reviewed prerequisite SWU and delays continuation code | Freeze canonical `DispatchSpec`, create `ConfirmedDispatch`/run authority and expand the bounded turn graph before TASK-CONT-001 |
| B — test-only seeded authority fixture | Reaches the suspension consumer seam faster | Does not prove confirmation, provenance or the writer-to-consumer path; cannot support a real deterministic launch claim | TASK-CONT-001 remains only a synthetic local consumer proof and durable confirmation is still required later |

Reject using the caller or legacy `dispatch_links` row as a third option: it contradicts the
accepted authority boundary rather than representing a viable implementation choice.

## Previous resolved decisions

| Decision | Selected option | Evidence/source | Consequence |
|---|---|---|---|
| Scope | Dispatch infrastructure only; no Schema Service | User direction in this session | Work Pack writes only ACI runtime/tests/evidence. |
| Wait model | Park a terminal turn; do not hold a running process or poll the bus | [ACI-CONT-001](../../../../../../decisions/aci-resumable-agent-continuation.md) | Journal state and reconstruction input are correctness boundaries. |
| Delivery | Runtime resolves official mapped bus outputs and creates the next attempt | ACI-CONT-001 + reviewed DomainSpec | Chat orchestrator is absent after confirmation. |
| Identity | Prefer same provider session; never rely on implicit memory | ACI-CONT-001 + host probe | Exact input is always materialized; replacement is explicit. |
| First implementation | Fake adapter L0/L1 before a real Codex adapter | [Layering](implementation-layering.md) | Core atomicity and degraded modes are proven before host assumptions. |
| Agent topology | Sequential single-writer SWUs, each with two auditors and an independent reviewer | User request + Work Pack | No overlapping code writers; every coder has a reviewer. |

## Deferred, non-blocking decisions

- Real Codex handle retention/restart/cancellation semantics belong to L2 empirical admission.
- The general skill-profile capability and whether `dispatch_type` survives belong to L3.
- Multi-host claiming, deployment and production cutover are out of L0/L1.

## Resolution

The user selected option A and clarified that confirmation authority originates in an explicit
user approval observed by the host. The approval may arrive through chat now or through a future
UI; the UI is transport, not authority. CONF-000 closed the canonical authority contract and
offline oracle before CONF-001 wrote that authority atomically. The seeded-authority option B was
rejected for the runtime-managed path.

TASK-CONT-001 is `implemented-reviewed-pass`. Migration 013 added isolated continuation tables with
direct CONF-001 parentage and no legacy schema/row mutation or backfill. The current dependency is
PRODUCT-PASS for a new CONF v2 authority package before OPEN onward; it does not reopen CONT-001.

## Assumptions

- The existing ordered SQLite migration pattern remains authoritative for this Python runtime; the
  PostgreSQL/Drizzle-specific DomainSpec persistence obligation is not applicable.
- Fake adapter observations exercise the provider-neutral interface but are not evidence that a real
  provider supports continuation.

## Validation

- ACI-CONT-001 and the continuation DomainSpec were independently reviewed.
- Work Pack link targets and `git diff --check` pass at this gate stage.
- CONF-000, CONF-001, CONT-001, HEADS-001 and BUS-001 have bounded reviewed evidence.
- BUS-001 closes 23/23 focused, 200/200 runtime and independent `PASS / KEEP` without opening,
  resume, effect or adapter reachability.
- Decision-gate result: `BLOCK`, with PRODUCT-PASS as the only next continuation gate.
