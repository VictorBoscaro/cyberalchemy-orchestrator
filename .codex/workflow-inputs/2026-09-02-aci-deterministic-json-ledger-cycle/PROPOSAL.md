# Craft cycle proposal — deterministic JSON dispatch ledger

## Result proposed

Run two separately governed, single-seat dispatches after the applicable confirmation gate:

1. `2026-09-02-aci-deterministic-json-ledger-update` uses the officially resolved `craft` route to update, validate, and export the owning ledger.
2. `2026-09-02-aci-deterministic-json-ledger-validate` uses the same official `craft` route for an independent, read-only `validate` audit of the first dispatch's exact terminal outputs.

The second seat is the updater's required independent reviewer, but it produces a Craft `pass | flag | block`, not a canonical review `KEEP | FIX`. The officially resolved review route is recorded below and remains unusable for this cycle because its required multi-group topology would hit the same pre-launch sequential-handoff deadlock being recorded.

No dispatch in this proposal has been compiled, opened, registered, launched, or closed.

## Workspace resolution

Four Craft ledgers exist:

- `.craft/ledger.yml`
- `docs/features/agents-communication-infra/.craft/ledger.yml`
- `projects/schema-service/.craft/ledger.yml`
- `tools/test-derivation-engine/.craft/ledger.yml`

The unique owning ledger is `docs/features/agents-communication-infra/.craft/ledger.yml`, `ledger_id: craft.agents_communication_infra`. It owns `CTX-ACI-ROOT`, `DEF-ACI-DETERMINISTIC-DISPATCH-001`, `CTX-ACI-RUNTIME-BASELINE`, `CTX-ACI-RESUMABLE-FEEDBACK`, compiler/runtime artifacts, and the canonical graph gap. The other three ledgers do not own this work.

Authority remains:

- source: `docs/features/agents-communication-infra/.craft/ledger.yml`
- generated human view: `docs/features/agents-communication-infra/CRAFT.md`

## Evidence frozen for the update

| Evidence | Path | SHA-256 | Authorized claim |
|---|---|---|---|
| Local runtime final review | `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-EXECUTION-RUNTIME-001/review.md` | `8B5F152CD04AE9BBE44BC868802241432C779ACAE5FA3C01E0828937EB8F9DFF` | KEEP for the exact local scripted runtime ceiling |
| Research initial definitions | `docs/features/agents-communication-infra/research/deterministic-json-dispatch/research-initial-definitions.md` | `56039AD49883D94B5F4AC65D2D1DEDFCF527F95C90B598ADEA927267BA2D0B61` | Accepted research boundary |
| Initial-definitions review | `docs/features/agents-communication-infra/research/deterministic-json-dispatch/review-initial-definitions.md` | `20FC0888D1DE91AD5AA25176528C89696B2C6774C7CC67161175D188DBA6DECC` | KEEP for those definitions |
| Confirmed research opening | `.codex/workflow-inputs/2026-09-02-deterministic-json-dispatch-host-gap/opening.json` | `C4A4EE6409548DA652AA1182F1B6CFDACF16F4EDEB559EBBF867DE925306702C` | Exact sheet was confirmed; no successful compile or execution followed |
| Research lifecycle review | `docs/features/agents-communication-infra/research/deterministic-json-dispatch/review-research-lifecycle.md` | `9173AB80B3C7FE1F1B2FC6017B97021F9CBD440262A3E3A4DB05C97B5A785F9B` | BLOCK: pre-launch producer receipt cycle and unimplemented feedback; zero downstream lifecycle artifacts |

The accepted local capability is exactly:

`9 manifested JSON inputs -> compiler -> proposed ExecutionGraph -> exact local acceptance -> SQLite/state machine -> ScriptedLocalAdapter -> terminal state`.

It does **not** prove host-live execution, canonical `aci.execution-graph@2`, `ConfirmRuntimeDispatch@2`, production authentication, provider/tool/credential execution, or external effects.

## Row-by-row update contract

The updater must first re-check all IDs against the current ledger. If any proposed ID already exists with different content, it must stop `block`; it must not rename or overwrite the conflict silently.

### Existing rows to update

| Row | Exact change |
|---|---|
| `ART-ACI-LOCAL-EXECUTION-RUNTIME-IMPL` | Change `status: flag` to `status: pass`; replace the stale “awaiting same-reviewer recheck” notes with the final KEEP hash and exact local ceiling/exclusions. Preserve its existing path and owner. |
| `DESC-ACI-RUNTIME-003` | Mark `superseded`, preserving history. |
| `DESC-ACI-ROOT-006` | Mark `superseded`, preserving history. |
| `DESC-ACI-CONTINUATION-006` | Mark `superseded`, preserving history. |
| `GAP-ACI-CANONICAL-GRAPH-CONTRACT-001` | Remove only the stale “awaiting same-reviewer recheck” premise. Preserve `status: active`, `severity: block`, its canonical-v2/confirmation/production exclusions, and its existing links. Add a link to the final local-runtime review artifact. |
| `CTX-ACI-ROOT` | Preserve `gate: block`; add new evidence artifacts to `owned_artifacts`; set next move to the bounded task-session repair, independent validation/review, and JSON-to-host proof while preserving exclusions. |
| `CTX-ACI-RUNTIME-BASELINE` | Preserve its bounded scope; add final review and lifecycle evidence artifacts; set next move to repair the compile/handoff bootstrap without expanding into provider/external effects. |
| `CTX-ACI-RESUMABLE-FEEDBACK` | Preserve `gate: block`; add host-gap artifacts/decision/gap links; set next move to the bounded task-session repair followed by an independent reviewer and an end-to-end JSON-to-host witness. |
| `CTX-ACI-PROTOCOL-COMPILATION` | Replace the stale next move that says downstream runtime review is still proceeding. Preserve identity/role KEEP and point next to the bounded host compile/handoff repair without claiming runtime ingestion or canonical-v2 completion. |
| `DEC-ACI-AGENT-IDENTITY-ROLE-001` | Replace only the stale impact clause that says independent implementation recheck is pending. State that identity/role recheck is KEEP while runtime ingestion, canonical-v2, confirmation, and host-live execution remain blocked. |
| `REL-ACI-IDENTITY-ROLE-DECISION-INFORMS-GAP` | Replace only the stale reason clause that says identity implementation recheck is unproven. Preserve the relation as active and state that accepted identity narrows the compiler boundary while runtime ingestion and the other explicit execution gaps remain unproven. |

Within `GAP-ACI-CANONICAL-GRAPH-CONTRACT-001`, replace the existing link label `Local fake execution repair pending same-reviewer recheck` with `Final reviewed local fake execution runtime`; preserve its target `ART-ACI-LOCAL-EXECUTION-RUNTIME-IMPL` and update no authority semantics through this label change.

### New descriptions

| ID | Owner | Status | Required content/evidence |
|---|---|---|---|
| `DESC-ACI-RUNTIME-004` | `CTX-ACI-RUNTIME-BASELINE` | `active` | State the final local KEEP ceiling and exclusions; evidence `ART-ACI-LOCAL-EXECUTION-RUNTIME-REVIEW`. |
| `DESC-ACI-ROOT-007` | `CTX-ACI-ROOT` | `active` | State that local deterministic execution is proven but host-bound dispatch remains blocked at compile/handoff; evidence `ART-ACI-DETERMINISTIC-JSON-HOST-GAP-REVIEW`. |
| `DESC-ACI-CONTINUATION-007` | `CTX-ACI-RESUMABLE-FEEDBACK` | `active` | State the exact producer-receipt-before-plan cycle and unsupported feedback edge; evidence `ART-ACI-DETERMINISTIC-JSON-HOST-GAP-REVIEW`. |

### New artifacts

| ID | Owner | Path | Type | Status |
|---|---|---|---|---|
| `ART-ACI-LOCAL-EXECUTION-RUNTIME-REVIEW` | `CTX-ACI-RUNTIME-BASELINE` | `development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-EXECUTION-RUNTIME-001/review.md` | `implementation-review` | `pass` |
| `ART-ACI-DETERMINISTIC-JSON-RESEARCH-INITIAL` | `CTX-ACI-ROOT` | `research/deterministic-json-dispatch/research-initial-definitions.md` | `research-initial-definitions` | `pass` |
| `ART-ACI-DETERMINISTIC-JSON-RESEARCH-INITIAL-REVIEW` | `CTX-ACI-ROOT` | `research/deterministic-json-dispatch/review-initial-definitions.md` | `research-initial-definitions-review` | `pass` |
| `ART-ACI-DETERMINISTIC-JSON-HOST-GAP-OPENING` | `CTX-ACI-RESUMABLE-FEEDBACK` | `[repo-root] .codex/workflow-inputs/2026-09-02-deterministic-json-dispatch-host-gap/opening.json` | `confirmed-dispatch-opening` | `block` |
| `ART-ACI-DETERMINISTIC-JSON-HOST-GAP-REVIEW` | `CTX-ACI-RESUMABLE-FEEDBACK` | `research/deterministic-json-dispatch/review-research-lifecycle.md` | `dispatch-lifecycle-review` | `block` |

Each artifact note must contain its exact hash and only the claim authorized by the evidence table. The opening note must explicitly say that confirmation occurred but compilation failed and no open/register/session/seat/binding/output/close followed.

### New decision

`DEC-ACI-TASK-SESSION-FALLBACK-001`:

- scope: `CTX-ACI-RESUMABLE-FEEDBACK`
- type: `selection`
- question: which bounded implementation route may repair the host compile/handoff gap while formal `domainspec-implement` is hard-blocked by absent `implementation-axioms`?
- options: `task-session-with-independent-review`, `wait-for-implementation-axioms`, `unreviewed-direct-code`
- selected: `task-session-with-independent-review`
- rationale: the user explicitly said “então vamos usar”, authorizing the previously proposed task-session fallback; this does not waive subagent-only execution or the one-independent-reviewer requirement
- evidence: `ART-ACI-LEDGER` as the durable record of the current human decision, linked to the host-gap review
- status: `closed`, `blocking: false`, owner `repository-owner`
- impact: permits only the bounded code repair; it does not prove the repair or authorize broader canonical-v2/production work

### New gap

`GAP-ACI-HOST-SEQUENTIAL-HANDOFF-001`:

- scope: `CTX-ACI-RESUMABLE-FEEDBACK`
- severity: `block`
- treatment: `plan`
- owner: `runtime-architecture`
- status: `active`
- evidence: `ART-ACI-DETERMINISTIC-JSON-HOST-GAP-REVIEW`
- summary must separately preserve both witnessed blockers:
  1. `_sequential_handoffs` requires the producer-output receipt before emitting the plan that would launch the producer;
  2. `feedback` with `loop_cap` is not executable by the current compiler/runtime path.
- closure requires a bounded implementation plus independent review and a real parent-bound JSON-to-host witness; local scripted terminal evidence alone cannot close it

### New relations

| ID | Source | Target | Type | Status | Evidence |
|---|---|---|---|---|---|
| `REL-ACI-LOCAL-RUNTIME-INFORMS-HOST-GAP` | `ART-ACI-LOCAL-EXECUTION-RUNTIME-REVIEW` | `GAP-ACI-HOST-SEQUENTIAL-HANDOFF-001` | `informs` | `active` | `ART-ACI-LOCAL-EXECUTION-RUNTIME-REVIEW` |
| `REL-ACI-HOST-HANDOFF-GAP-BLOCKS-CONTINUATION` | `GAP-ACI-HOST-SEQUENTIAL-HANDOFF-001` | `CTX-ACI-RESUMABLE-FEEDBACK` | `blocks` | `active` | `ART-ACI-DETERMINISTIC-JSON-HOST-GAP-REVIEW` |
| `REL-ACI-TASK-SESSION-DECISION-GOVERNS-HOST-GAP` | `DEC-ACI-TASK-SESSION-FALLBACK-001` | `GAP-ACI-HOST-SEQUENTIAL-HANDOFF-001` | `informs` | `active` | `ART-ACI-LEDGER` |
| `REL-ACI-HOST-GAP-RESEARCH-INFORMS-GAP` | `ART-ACI-DETERMINISTIC-JSON-RESEARCH-INITIAL-REVIEW` | `GAP-ACI-HOST-SEQUENTIAL-HANDOFF-001` | `informs` | `active` | `ART-ACI-DETERMINISTIC-JSON-HOST-GAP-REVIEW` |

### Index and export updates

The updater must rebuild, not hand-wave, all required indexes:

- add every new ID to `indexes.by_id` with its actual final array position;
- add the new active gap to `indexes.active_gaps`;
- update `indexes.next_moves` for the four touched contexts, including `CTX-ACI-PROTOCOL-COMPILATION`;
- add all new artifact paths to `indexes.artifacts_by_path`;
- preserve empty `open_decisions`, `blocking_decisions`, and `active_blockers` unless the actual ledger disproves that state;
- verify every pointer and reference resolves;
- export `CRAFT.md` as a linked view with quick links, the local-runtime ceiling, the active host-handoff gap, the fallback decision, evidence hashes, residue, and next move.

## Dispatch A — Craft updater

- Opening: `opening-craft-update.json`
- Route: `craft`, `dispatch_type_ref/ledger_dispatch_type: other`, `legacy-managed`, `host/inherited@1`
- Agent: Lampson, Butler; role `writer`; model `gpt-5.6-terra`; budget 7,000
- Anti-bias: disabled
- Maximum loops: 1
- Working folder: `docs/features/agents-communication-infra/.craft/artifacts/2026-09-02-deterministic-json-dispatch-ledger-update`
- Effects after confirmation: mutate only the owning `ledger.yml`, its `CRAFT.md` view, and `update-report.md` in the working folder
- Frozen source preconditions checked by the seat before mutation: proposal bytes at the exact SHA-256 embedded in the opening, ledger SHA-256 `4CD03CC9376CE607710C5E1F52D04B7A72AA627BA4445E0B765C408E8C51A492`, and view SHA-256 `E15F4FD0357A8EB10B966C45270D3A27B6C18E91316584565411D5E9FF928B1C`; mismatch returns `block` with zero target edits
- Forbidden effects: runtime/source/spec edits, telemetry hand-edits, bridge stdout copies, commit, push, or any host-live/canonical-v2 claim
- Close contract: close `resolved` only after terminal bound-seat evidence, structurally valid ledger, rebuilt indexes, exported view, and `update-report.md` containing exact post-update hashes; otherwise `error` or the applicable lifecycle outcome

## Dispatch B — independent Craft validator

- Opening template: `opening-craft-validate.provisional.json`
- Route: `craft`, `dispatch_type_ref/ledger_dispatch_type: other`, `legacy-managed`, `host/inherited@1`
- Agent: Parnas, David; role `auditor`; model `gpt-5.6-sol`; budget 6,000
- Anti-bias: disabled
- Maximum loops: 1
- Working folder: `docs/features/agents-communication-infra/.craft/artifacts/2026-09-02-deterministic-json-dispatch-ledger-validation`
- Effects after its later confirmation: read target ledger/view/update report; write only `validation-report.md`
- Required precondition: after A closes, create an exact runtime-owned `aci-workflow-input-manifest/v1` pinning the exact proposal bytes/digest embedded in B plus A's terminal `update-report.md`, `ledger.yml`, and `CRAFT.md` bytes and digests; only then freeze and show B's exact sheet for confirmation
- Close contract: close `resolved` only if the validator is terminal and its report is accepted, even when the report is `flag` or `block`; a block result triggers a new bounded repair dispatch, never an in-place ungoverned fix

This is a separate single-seat validation dispatch, so the worker has one independent reviewer without requiring a sequential edge inside one graph.

## Why canonical review is not used here

The official review route was resolved successfully:

- registry digest: `sha256:4fc9fa8c0092fb2833ffa634b291453c09c525d586067c97eea8f5c9618477d3`
- capability digest: `sha256:60dbcb97707949aa7fe102479dbcd712e491bb833362f54b285a536365abd4be`
- route digest: `sha256:34013d06ac00aaf69c8b2553eb7456930e9dce730e62da8deb71186bdcb7ec66`

But `review/SKILL.md` requires a canonical topology with 2–4 independent attackers, a writer/synthesizer, and skeptic/verifier flow. Reducing it to one seat would falsely label a nonconforming audit as canonical review; using its full topology would reproduce the sequential/feedback lifecycle blocker. Therefore B is honestly routed as Craft validation. A canonical review remains pending until the handoff repair is implemented.

## Acceptance and rollback

Acceptance for A requires:

- exact evidence hashes reproduced;
- the frozen proposal, pre-update ledger, and pre-update view hashes match before the first mutation;
- only listed rows changed/added;
- no duplicate IDs or dangling links;
- indexes mechanically agree with source rows;
- `CRAFT.md` is a view, not authority;
- local KEEP and host BLOCK coexist without contradiction;
- task-session decision records authorization, not implementation success;
- post-update ledger/view hashes are emitted for B.

Acceptance for B requires:

- an exact post-A input manifest covering the frozen proposal, A report, ledger, and view, with byte match before launch;
- read-only target audit;
- complete coverage of rows, claims, indexes, paths, hashes, and unrelated-diff boundary;
- an explicit `pass | flag | block`, residue, and next move.

Rollback is forward repair from the pre-update hashes recorded by A. The worker must not use reset, checkout, or broad overwrite in the dirty worktree. A failed validation leaves the ledger's active gap open and routes a new bounded Craft repair; it does not erase evidence or claim success.

## Confirmation sequence

1. Ask the user to confirm **only Dispatch A's exact frozen opening** and effects.
2. Compile/open/register/launch/verify/close A through the governed lifecycle.
3. Materialize and verify the exact post-A input manifest.
4. Freeze B, show its exact effective inputs and effects, and obtain a separate explicit confirmation.
5. Compile/open/register/launch/verify/close B.

Confirming this proposal does not pre-confirm B's not-yet-existing post-A bytes.
