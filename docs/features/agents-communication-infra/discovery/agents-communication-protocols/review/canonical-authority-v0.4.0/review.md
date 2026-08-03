# Review — agents-communication-protocols v0.4.0

Target: `docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md`

Frozen target SHA-256: `B071046DD8B31A77E33C53A9AF020331EC55E8D73C7E351A98DFF45113B0BDC5`

Remediated target version: `0.4.1`

Remediated target SHA-256: `D7230A422CA08665A05D674430F806FA476D9AA9770B82681BB6B59EA3EED9E7`

Dispatch: `2026-08-03-agents-communication-protocols-v040-review`

Status: round 1 completed with objections; remediation applied; terminal re-review blocked because the current governed compiler cannot emit bound follow-up turns.

## Coverage

| attacker | lens | findings raised | zero-findings defence (if any) |
|---|---|---:|---|
| Liskov, Barbara | fidelity/governance through textual authority trace | 2 | — |
| Booch, Grady | ownership/reference integrity through architectural boundary graph audit | 4 | — |
| Lamport, Leslie | operability/state consistency through state-transition counterexamples | 4 | — |

All three reviewers independently read the complete frozen target and tested it against the same
companion corpus. They did not receive one another's returns. The parent collected the complete
barrier batch, verified each candidate finding against literal artifact and companion evidence,
deduplicated overlaps, and applied only supported changes to the target discovery.

The initial dispatch briefing named two companion paths one directory too deep. Reviewers resolved
the intended files through the target's own links. This was a briefing-path defect, not an artifact
finding; future prompts must use `discovery/bus-contracts/README.md` and
`discovery/dispatch-audit-ledger-cutover-contract.md`.

## agents-communication-protocols v0.4.0

| # | file | evidence (quoted from the artifact) | severity | proposed fix | resolution in v0.4.1 |
|---|---|---|---|---|---|
| ACP-R1-01 | `agents-communication-protocols/README.md:232,423` | “Essa matriz é normativa para ownership nesta discovery” / “the first ratified discovery decisions” | MAJOR | Mark ownership and ACPD entries as candidate proposals; keep ACPD-4 unsettled pending OQ-ATD3 synchronization and SPEC promotion. | Applied: ownership is explicitly proposed rather than normative; the ratification claim was removed; the mandatory empty `Decisions Baked In` register now states that no decisions are ratified. |
| ACP-R1-02 | `agents-communication-protocols/README.md:125-189,375` | “One persisted canonical authority governs a run; every view, ledger row, configuration and runtime action is a verifiable derivation.” | MAJOR | Scope the invariant and execution flow to `runtime-managed`; preserve the separate live/historical authority of `legacy-managed`. | Applied in the objective, invariant, required rules, skill-to-dispatch flow, ownership table, ACPD-1 and flow diagram. |
| ACP-R1-03 | `agents-communication-protocols/README.md:187,321-329` | “A confirmação congela os bytes canônicos” while the candidate-to-`DispatchSpec` representation remained an open question. | MAJOR | Make the user confirm an already server-resolved canonical `DispatchSpec` digest and define the candidate as non-authoritative input. | Applied through `ConfirmationProjection`, a digest-bound confirmation flow and a narrowed OQ-ACP3 for the versioned mapping/schema. |
| ACP-R1-04 | `agents-communication-protocols/README.md:228` | “`subagents-dispatch.yaml` opening/close | AuditLedgerMaterializer and validated appender” | MAJOR | Split journal/effect-intent authority, canonical row derivation/reconciliation and physical YAML mutation into separately owned seams. | Applied as distinct ownership rows, with a separate row preserving live/historical ledger authority. |
| ACP-R1-05 | `agents-communication-protocols/README.md:189` | “Persistir um `ConfirmedDispatch` e criar exatamente uma `Run`” | MAJOR | Define a transactional and idempotent confirmation transition with a stable key and recovery behavior. | Applied: one transaction keyed by `(dispatch_id, dispatch_spec_digest)` creates-or-returns the same `ConfirmedDispatch`, unique `Run`, opening facts/effect intent and stable receipt. |
| ACP-R1-06 | `agents-communication-protocols/README.md:179,249,351-359` | Active binding resolution and append-only revocation were specified while lifecycle effects remained open. | MAJOR | Bind confirmation to profile/binding revisions and a CAS token; close behavior for proposed, concurrent, confirmed, in-flight, retry, new execution and replay states. | Applied as confirmation-time CAS plus an explicit lifecycle matrix; OQ-ACP6 now concerns explicit cancellation/safety controls after confirmation. |
| ACP-R1-07 | `agents-communication-protocols/README.md:152,273-275` | “Run -> ... -> terminal result” without the mandatory opening-release and close-verification barriers. | MAJOR | Require `audit_opening.verified` before execution and distinguish the unique terminal fact from `audit_close.verified`/`closed`, including unresolved effect states. | Applied in the invariant diagram, runtime flow, convergence section and Mermaid flow. |
| ACP-R1-08 | `agents-communication-protocols/README.md:112-115` | Generic “receipts” were presented as one derived family. | MINOR | Name receipt/fact families and preserve their distinct owners and acceptance effects. | Applied to `DispatchDerivation`: confirmation/publication receipts, delivery facts, materializer acknowledgements and appender outcomes remain separately owned. |

**Verdict:** FIX

The verdict applies to frozen v0.4.0. Version 0.4.1 contains the requested remediations but has not
earned `KEEP`: all three reviewers must return `NO_OBJECTION` over the same remediated digest in one
governed round.

## Change requests

1. MAJOR — Preserve the v0.4.1 `runtime-managed` scope and never reinterpret current
   `legacy-managed` or historical YAML rows as ACI `ConfirmedDispatch`/`Run` authority.
2. MAJOR — Preserve digest-bound confirmation over server-resolved `DispatchSpec` bytes and reject
   any profile, binding, mode or digest drift before the confirmation transaction.
3. MAJOR — Preserve the transactional/idempotent creation rule and the audit opening/close barriers
   when promoting the discovery into SPEC and implementation.
4. MAJOR — Settle OQ-ATD3 in its owning companion before promoting protocol-governance ownership.
5. MAJOR — Run a second governed barrier round over SHA-256
   `D7230A422CA08665A05D674430F806FA476D9AA9770B82681BB6B59EA3EED9E7` after the infrastructure can
   compile a frozen `turn_ordinal > 0` workflow manifest and binding for each existing reviewer seat.

## Execution residue

- Rounds used: 1 of 5.
- Agents spawned: 3 independent explorers; no helper or peer-to-peer communication.
- Exit condition: infrastructure error, not convergence and not loop-ceiling exhaustion.
- Missing capability: the governed compiler emits only initial `turn_ordinal: 0` launch plans, while
  the mandatory host hook rejects unbound `followup_task` calls. Manual envelope synthesis is
  prohibited by the confirmed lifecycle.
- Discovery validation: every content/structure/link check passed; the sole validator failure is the
  pre-existing legacy nested path `discovery/agents-communication-protocols/README.md`, which is
  outside the current accepted `discovery/<slug>.md` shape. Moving it requires a separate coordinated
  link migration.
- Final approver: `victorboscaro@outlook.com`; acceptance remains pending because no terminal
  all-reviewer `NO_OBJECTION` round occurred.
