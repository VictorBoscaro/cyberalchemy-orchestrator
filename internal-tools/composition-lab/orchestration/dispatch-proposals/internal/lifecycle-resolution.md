---
artifact_kind: inventory-bounded-lifecycle-resolution
status: block-pending-transport-adjudication-host-mechanics-and-regenerated-exact-run
date: 2026-08-13
scope: internal-composition-study
registration: forbidden
---

# Lifecycle resolution — bounded internal composition inventory

## Verdict

An Inventory-owned, bounded, unregistered helper workflow is an honest semantic route. It is **not**
an Inventory dispatch and must not claim an Inventory ledger open, ACI dispatch close, registered
handoff, or accepted-output receipt.

Execution remains **BLOCKED**. The current host has no dedicated unregistered Inventory
open/bind/close primitive. Durable `ACI-WORKFLOW-BINDING-V1` binding is available only after a
registered parent has opened and issued bound workflow manifests; the bridge rejects opening a
non-LIVE type. An ordinary helper spawn is instead wrapped by the mandatory host hook in its generic
registered compatibility envelope. That per-call envelope may honestly record host supervision of
an arbitrary helper, but it must not be represented as the Inventory workflow's dispatch identity.

The compatibility envelope is **not yet an approved mechanism for this workflow**. It opens a real
LIVE dispatch row using the policy-selected compatibility type (currently described by the hook as
`review/inline`), whereas the controlling route decision says that no existing registered dispatch
type may be reused as a transport workaround. Calling the row "transport-level" does not remove
that contradiction. The human decision authority and the canonical Inventory owner must explicitly
adjudicate it; ordinary helper calls remain unavailable for execution until they do.

Even after that adjudication, the proposed sequence is not executable as written: no inspected host
primitive materializes the corpus manifest, artifact barriers, telemetry check, or
`completion.json`. The principal is forbidden to do that work. The exact-run package must therefore
either cite and fixture real host-owned primitives for those artifacts or predeclare separate
mechanical recorder/checker helper seats, write scopes, prompts, attempts, and wrapper semantics.
That topology change requires owner ratification, fresh review, and human confirmation.

## Evidence trail

- `AGENTS.md`, **Host wrapper binding**: a seat under a governed dispatch requires the binding marker
  as the first prompt line; bridge stdout belongs only in the journal; missed hooks must be recorded
  through close.
- `.agents/skills/inventory/SKILL.md`, **authority-rule**, **ingest-process**, and **quality-bar**:
  Inventory owns candidate evidence-cards, trace, residue, indexes, validation, and non-authority
  handoffs, but declares no delegated open/close lifecycle.
- `.agents/skills/domainspec-subagents-strategy/SKILL.md`, **Select the capability**: an owner-directed
  unregistered bootstrap terminates inside its capability and must not infer a registered type.
- `.agents/skills/discovery-writing/SKILL.md`, **Orchestration and Confirmation**: the local precedent
  treats proposals, manifests, acknowledgements, attempts, and completion as workflow evidence only;
  it explicitly denies durable dispatch/bus binding claims.
- `implementations/server/runtime/orchestration_bridge.py`, `_append`: opening is refused unless the
  record's type is LIVE in the canonical registry. `open_dispatch` and `close_dispatch` therefore
  cannot represent an unregistered Inventory parent.
- `implementations/server/runtime/host_dispatch_hook.py`, `_workflow_envelope` and `pre_tool_use`:
  an explicit ACI binding envelope is validated against an already bound workflow turn; an ordinary
  helper call is instead converted into a generic compatibility dispatch and opened through the
  bridge.
- `internal-tools/composition-lab/.../runtime-blocker/01-runtime-diagnosis.md`, **Existing lower-level
  runtime capabilities**: lower-level binding-output checks do not provide scheduling or accepted
  output publication.
- `.../runtime-blocker/10-final-route-decision.md`, **Compatibility obligations** and
  `11-inventory-governance.md`, **Ratification and authority**: bounded Inventory is preferred, LIVE
  registration is rejected, and owner/run/artifact approvals remain distinct.
- `.../inventory-bootstrap/02-bootstrap-design.md`, **Seats, connectionless topology, binding,
  handoff, and close**: the two-seat writer-then-auditor shape is connectionless and capability-local;
  its completion is workflow evidence, not ledger close.
- `.../inventory-bootstrap/04-execution-sheet.md`, **Seats and connectionless artifact barriers**:
  the principal only orchestrates; writer and auditor own semantic work; exact paths, attempts,
  prompts, barriers, mutations, and completion are predeclared.
- `.../inventory-bootstrap/10-human-confirmation-sheet.md` and `11-human-gate-check.md`: the required
  choices were not filled; the old sheet covers only the superseded 22-source denominator.
- `research/internal-composition-uses/dispatch-proposal.md`, **Proposed external-local annex**, and
  `orchestration/dispatch-proposals/internal/launch-readiness.md`: DomainSpec v2 adds 13 pinned
  sources, forcing regeneration and reaudit of the exact-run package.

## Candidate executable sequence (not yet executable)

This sequence becomes executable only after the prerequisites below pass and an exact package
replaces every unsupported "host-owned" act with a demonstrated primitive or a confirmed helper
seat.

1. A delegated preparer regenerates one 35-source corpus manifest, denominator, partitions, prompt
   bodies, path allowlists, hashes, budgets, attempts, and exact-run digest. It performs no corpus
   extraction.
2. Independent reviewers verify the regenerated package, including the DomainSpec v2 private-source
   boundary and the one-writer/one-auditor connectionless topology.
3. The human records: Inventory reuse; canonical owner/design ratification; exact-run confirmation;
   recovery and maintenance owners; acceptance of per-helper compatibility wrappers; and a separate
   launch authorization.
4. The principal launches only the predeclared `extractor-writer`. If the transport conflict has
   been explicitly adjudicated and it is launched as an ordinary
   helper, do not prepend a fabricated ACI workflow envelope. Let the mandatory host hook preserve
   its generic compatibility open/binding/close journal evidence. Record the returned host dispatch
   ID, agent ID, attempt identity, exact prompt digest, terminal state, and writer output hashes in
   the capability-local completion evidence; never relabel that wrapper as Inventory.
5. After writer termination, a demonstrated host primitive or a separately predeclared mechanical
   recorder seat records only predeclared artifact paths, hashes, sizes, and producer attempt. The
   principal does not create the barrier, summarize, or select semantic content.
6. The principal launches only the predeclared read-only `coverage-auditor`, under the same wrapper
   rule. The auditor opens the exact writer files and writes only its attempt-specific report.
7. `BOUNDED_CORRECTIONS` permits the frozen second writer/auditor attempts only. Each helper call has
   its own host wrapper evidence; attempts remain typed and are not collapsed.
8. A demonstrated host primitive or predeclared mechanical checker performs the telemetry check;
   a demonstrated host primitive or predeclared recorder materializes capability-local
   `completion.json`. It records proposal/run digests, human acknowledgements, helper-wrapper IDs,
   agent identities, full prompt digests and prompt source paths, attempt ordering, exact writes and
   hashes, auditor verdict, correction count, telemetry result, gaps, and exit reason.
9. Each mandatory hook closes its own compatibility wrapper. No additional Inventory bridge close
   is attempted. Bridge stdout is never copied into the run folder. A missed hook must follow the
   repository policy: call the bridge directly where a truthful open/close is still possible and
   record the missed-hook gap in the close record. A capability-local completion file is not a
   substitute for that close record.

## Preconditions that keep execution BLOCKED

1. The canonical Inventory owner must ratify this capability-local helper lifecycle and its
   description/adjudication boundary. No skill, registry, or runtime mutation is implied.
2. The human decision authority and canonical Inventory owner must explicitly resolve the conflict
   between generic LIVE compatibility rows and the route decision's prohibition on reusing an
   existing registered type as transport. Acceptance of a "dual record" alone is insufficient:
   the ratification must amend/supersede that compatibility obligation or reject this mechanism.
3. The 35-source DomainSpec-inclusive execution sheet and confirmation sheet must be regenerated,
   independently re-audited, and freshly confirmed. The old 22-source approvals and hashes carry no
   authority.
4. The exact run must freeze every helper identity, prompt byte/digest, model/tool/budget request,
   attempt, output/write allowlist, barrier, recovery owner, maintenance owner, and completion
   schema. Material drift requires reconfirmation.
5. The host-hook fixture must demonstrate ordinary helper open and terminal close, including what
   is actually preserved by the hook: wrapper dispatch ID, prompt bytes in `initial_prompt`, agent
   identity after completion, and terminal state. Attempt identity and prompt digests are not
   native generic-wrapper fields; the exact package must specify and test their separate factual
   derivation without calling it ACI binding.
6. Real producers for the manifest, barriers, telemetry check, and completion record must be
   identified and fixture-tested. If these are helper seats, the topology, identities, prompts,
   attempts, read/write allowlists, ordering, and wrapper rows must be frozen and ratified.
7. The final independent `/review` and separate human launch gate must pass.

Until all seven are satisfied, the terminal result is `BLOCK/HOST_WORKFLOW_AND_CONFIRMATION_PENDING`.

## Insecurities and limits

- The compatibility wrapper uses a LIVE generic type for host supervision. That is truthful only if
  its record remains explicitly transport-level and arbitrary-helper scoped; semantic consumers may
  still misread it. Human acceptance is therefore material, not ceremonial.
- Capability-local prompt digests and completion records preserve traceability but are not durable
  ACI approval or accepted-output receipts.
- The artifact barrier proves byte identity and ordering, not that the writer's semantics caused the
  auditor's judgment or that composition occurred.
- The principal-only-orchestrates rule is compatible with the sequence only if host-owned manifest,
  barrier, telemetry, and completion materialization is purely mechanical. Any semantic extraction,
  selection, repair, or synthesis by the principal violates the route and must stop.
- No atomic rollback exists; partial Inventory writes still require separately authorized recovery.

## Independent adversarial review

**Verdict: FIX / BLOCK.** Review date: 2026-08-13. The document may guide further preparation only;
it does not establish an executable lifecycle.

### Verified findings and disposition

1. **MAJOR — registered-type conflict was understated.** The prior text said a generic wrapper
   "may honestly" coexist with the unregistered workflow. The hook does create an explicit LIVE
   compatibility dispatch with an `initial_prompt`, but `10-final-route-decision.md` separately
   forbids borrowing an existing registered dispatch type as transport. **Disposition:** corrected
   to require explicit adjudication by the human decision authority and canonical Inventory owner.
2. **MAJOR — fictional host work violated principal-only orchestration.** The sequence assigned
   manifest, barrier, telemetry-check, and completion-file materialization to "the host", but no
   inspected runtime file supplies those primitives. If the principal performed them, it would
   violate `04-execution-sheet.md`'s prohibition on semantic or artifact work. **Disposition:**
   corrected to require demonstrated host primitives or separately confirmed mechanical seats.
3. **MAJOR — preservation claim exceeded runtime evidence.** Generic wrapper rows preserve the
   prompt as `initial_prompt`, and hook state preserves dispatch/terminal facts, but generic state
   has no workflow `attempt_id` or prompt-digest field. **Disposition:** corrected to require a
   separately specified and tested factual derivation, without claiming durable ACI binding.
4. **MINOR — missed-hook handling was ambiguous.** Capability completion cannot replace the
   policy-required bridge close record. **Disposition:** corrected to repeat the direct-bridge and
   close-record obligation.

### Question-specific conclusions

- Owner-directed ordinary helpers are semantically compatible with a principal that only launches,
  waits, and reports. They are not operationally authorized here until the registered-compatibility
  conflict is adjudicated and all mechanical work has a non-principal producer.
- Generic wrappers can supervise arbitrary helper calls, but their honest coexistence with this
  particular unregistered Inventory workflow is unresolved governance, not an implementation fact.
- Ratification must remain separated: reusable Inventory need; canonical Inventory owner/design;
  transport-conflict adjudication; exact run and effects; recovery and maintenance ownership; and a
  final launch authorization after fixtures and independent review.
- Agents, exact prompt bytes/digests, attempts, writes, terminal states, and close evidence are not
  yet covered by one native lifecycle. The regenerated package must state which evidence surface
  owns each fact and must not relabel compatibility rows or local completion as Inventory/ACI
  receipts.
