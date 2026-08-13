---
tags: [dispatch-governance, agent-lifecycle, writing-system]
artifact_kind: audit
layer: task
version: 0.1.0
created_at: 2026-08-13T03:50:57-03:00
updated_at: 2026-08-13T03:50:57-03:00
---

# Implementation dispatch review

## Verdict

**AMEND**

The dispatch has a sound authority model and passes deterministic Dispatch Spec validation, but it
is not yet safe to execute. Four operational defects can produce self-review, receipt collisions,
or an unprovable terminal state. One review-persistence instruction also contradicts the governing
`review` skill. Apply only the exact repairs below, re-run the validator, and obtain a new
independent review against the repaired dispatch hash before launching any seat.

Reviewed dispatch SHA-256:
`FD8CDAA967251C916B7B27593FF149680DBF90801DC96166FA7A9D436EB60657`.

## Required repairs

### 1. Give every final-review attacker exactly one lens

**Severity: MAJOR**

The role `review_attacker_operability` is assigned both `operability` and `abuse/gaming`
(`implementation-dispatch.json:133,420,435,453`). The governing review contract says, “Each
attacker takes ONE lens” (`.agents/skills/review/SKILL.md:66`). The current route therefore cannot
prove target-by-lens coverage using the required independent attack topology.

**Exact repair:** restrict `review_attacker_operability` to the operability lens and add a distinct
`review_attacker_abuse` role for abuse/gaming. Give the new role the same whole-corpus, read-only,
no-self-verification, no-persisted-transcript constraints. Add it to `r01`, `r02`, the repair-loop
topology, convergence and coverage requirements, identity-separation checks, lifecycle receipts,
and observability. Four attackers may fan out together under the declared concurrency limit of
four; writer, verifier, auditor, and dedicated approver remain downstream in that order.

### 2. Make every attempted seat and repair iteration own a unique receipt

**Severity: MAJOR**

The lifecycle contract requires one entry and a `receipt_artifact` for every attempted seat and
iteration (`implementation-dispatch.json:116,143-146`). Several multi-seat steps expose only one
shared receipt path: the two definition analysts share `r04-definition-analysis.json`; three
implementation owners share `r08-implementation.json`; the complete review topology shares
`r10-final-review.json`; repair owners and reviewers share `r11-review-repair-loop.json`; and the
closing agent and session reviewer share `r13-session-review.json`
(`implementation-dispatch.json:263,370,431,465,526,613-616`). No role is authorized to synthesize
those other agents' receipts, and root is expressly prohibited from doing so. Reusing one mutable
receipt across distinct identities also defeats file ownership and per-iteration terminal proof.

**Exact repair:** assign a unique immutable receipt path to every attempted `agent_id` / `role_id`
/ `iteration_id`, including conditional and repair seats. A stable pattern such as
`<run_root>/<step_id>/<iteration_id>/<role_id>.json` is sufficient. Group-level ledgers may contain
only references and hashes to those seat receipts and must have an explicitly named mechanical
owner; they may not substitute for seat receipts or contain synthesized model judgment. Update
every affected step output, `boundary_evidence.receipts`, lifecycle requirements, and terminal
checks. A not-needed role receives a non-spawn lifecycle entry; it must not receive a fabricated
completed-seat receipt.

### 3. Remove the final reconciler's impossible self-terminal claim

**Severity: MAJOR**

`x01` requires `terminal_reconciler` to verify that every spawned seat is already joined, closed,
and receipted, while that reconciler is itself a spawned seat whose receipt and close are still in
progress (`implementation-dispatch.json:140,533-553,571,590,641`). It cannot truthfully prove its
own later join and close from inside its running turn. A second verifying agent would only move the
same recursion to a new last seat.

**Exact repair:** make `x01` a pre-terminal reconciliation of every earlier seat and all substantive
gates. Its own receipt must not claim a future terminal state. After root joins and closes `x01`,
root may perform only its already-authorized mechanical lifecycle duty: verify the host runtime or
ACI journal records `x01` as terminal and that no dispatch seat remains live. Make `g08`'s final
lifecycle owner `root_orchestrator` for that mechanical check only, and define completion evidence
as the reconciler's frozen receipt plus the host-owned close/join record. Do not persist
orchestration-bridge stdout in the working folder, and do not let root author or alter any judgment
artifact or seat receipt.

### 4. Make the product-documentation namespace explicitly disjoint

**Severity: MAJOR**

`product_documentation_implementer` owns `README.md plus approved prose under
internal-tools/need-driven-system-writing/`, with only an undefined reference to “reserved
namespaces” (`implementation-dispatch.json:127`). Its explicit exclusions do not name
`definition/**`, even though the definition synthesizer, architecture reviewer, and deterministic
validator own prose there (`implementation-dispatch.json:123-130,261-346,395-399`). The later
artifact-plan disjointness gate can detect a collision, but role ownership should prevent one
before mutation.

**Exact repair:** define the role's fixed ownership as the existing `README.md` plus only exact
additional product-prose paths assigned to it by the PASS-reviewed artifact plan. Explicitly
exclude `definition/**`, `robot-talks/**`, `implementation-review/**`, `schemas/**`, `scripts/**`,
`tests/**`, the implementation dispatch and its review, all session paths, and both skill-runtime
trees. Preserve the existing rule that no path may be assigned to more than one owner.

### 5. Do not persist refuted review findings

**Severity: MAJOR**

The repair loop requires preservation of “dropped/refuted findings”
(`implementation-dispatch.json:473`). The review skill instead accepts the loss of rejected
candidate reconstruction, requires a refuted finding to be dropped, and makes `review.md` the only
review artifact (`.agents/skills/review/SKILL.md:25-41,145,156-170`). Calling this material receipt
data would still persist review working material outside the one-artifact contract.

**Exact repair:** remove preservation of the content of dropped or refuted findings. Runtime
working returns remain ephemeral. Receipts may record lifecycle, lens/target coverage, counts,
hashes, convergence state, and final approval, but not attacker/verifier transcripts or rejected
finding content. The current `review.md` must contain only verified surviving change requests,
Coverage, per-artifact verdicts, and the report fields required by the review skill.

## Contract checks that pass

- **Delegated authority — PASS.** The quoted 2026-08-13 statement is represented as delegated
  operational authority, not as fabricated direct selections. The delegated seat may choose only
  frozen reviewed A/B options; an independent reviewer checks the proposal; the recorder copies it
  mechanically. `D-03` and `D-05` remain reversible deferrals.
- **Root orchestration-only — PASS.** Root is limited to launch, ACI-bound handoff, join, close,
  exact reroute, and receipt reporting. Decision, definition, implementation, validation, review,
  repair, session authorship, and substantive terminal judgment remain agent-owned.
- **Evidence-gated components — PASS.** Essay, interviewer, profile, shared-core representation,
  schema, specialization, evaluation, research, automation, code, and tests are explicitly
  candidates rather than presumed deliverables. Every build-now component requires evidence, a
  distinct owner/consumer contract, validation, and independent architecture review; absence is a
  valid disposition.
- **Existing work preservation and no commit — PASS.** `s00` freezes the dirty worktree and in-scope
  hashes before mutation; implementers receive exact allowlists; validation compares against the
  baseline. Reset, checkout, staging, commit, push, cleanup, unrelated edits, and destructive
  overwrite are forbidden. The current repository has extensive user-owned modified and untracked
  work, so this gate is necessary and correctly blocking on ambiguity.
- **Repair authority — PASS, subject to Repairs 1, 2, and 5.** Only original file owners repair
  verified CRITICAL/MAJOR findings; deterministic validation and full-corpus review repeat; three
  passes are a ceiling; unresolved major findings block completion. MINOR residue does not silently
  expand product scope.
- **Close-session order — PASS.** `close-session` begins only after final review passes with no
  CRITICAL/MAJOR. The closing agent authors the node; one stable small reviewer comments; only the
  closing agent repairs; the loop stops on no comments or blocks after three passes. The following
  terminal reconciliation is observational, not a later product or session mutation.
- **ACI feasibility — PASS, subject to Repairs 2 and 3.** Every governed prompt requires the ACI
  binding as its first line, bridge-hook failure has a defined direct fallback and recorded gap,
  and bridge stdout is excluded from working folders.

## Validation evidence

- Repository validator:
  `python .agents/skills/dispatch-spec/scripts/validate-dispatch.py internal-tools/need-driven-system-writing/implementation-dispatch.json`
  returned `VALIDATION=pass`.
- All 27 frozen source paths exist and match their declared SHA-256 values.
- The current `.codex` and `.agents` copies of `write-need-driven-documents/SKILL.md` match their
  declared hashes and each other.
- Deterministic validation does not override the semantic amendments above.

## Dispatch Spec Result

- **Dispatch ID:** `need-driven-system-writing-implementation-v1`
- **Status:** amend
- **Mode:** mixed
- **Step count:** 15
- **Gates:** structurally valid; execution blocked pending the five repairs above
- **Subagent strategy:** required and user-authorized; role separation is conceptually sound but
  receipt ownership and final lifecycle proof require repair
- **Subagent lifecycle:** pre-run `none`; not yet terminally feasible
- **Observability:** amend — unique seat receipts and a non-recursive final close proof are required
- **Promotion guardrail:** pass
- **Next route:** dispatch author repairs only the cited defects, re-runs validation and all frozen
  hashes, then requests a new independent review; no implementation seat may launch before PASS

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [implementation-dispatch.json](implementation-dispatch.json) | `validates` | This audit checks whether the proposed implementation route is safe and executable before any seat launches. |

## Repair verification

**PASS**

The repaired dispatch at SHA-256
`A8F4D0546B4732EA0A299552873439FD9DADF4ED75177B7FAE72885F6B7A4A1E` resolves all five required
repairs. The historical `AMEND` above remains the correct verdict for the prior dispatch hash; this
addendum authorizes execution only against the repaired hash stated here and subject to its runtime
gates.

### Repair-by-repair evidence

1. **One lens per attacker — PASS.** The route now defines four distinct whole-corpus, read-only
   attackers: fidelity/governance, mechanics/correctness, operability, and abuse/gaming
   (`implementation-dispatch.json:133-136`). Both review steps include all four identities
   (`:428,461`); `r01` explicitly fans them out under one lens each before writer, verifier,
   coverage auditor, and dedicated approver proceed downstream (`:442-447`); and the repair-loop,
   boundary, coverage, and observability contracts preserve the same topology (`:568,615`). No
   attacker verifies its own work or owns a second lens.
2. **Unique immutable seat receipts — PASS.** Every single-seat and multi-seat step now names a
   distinct receipt path per `step_id`, `iteration_id`, and `role_id`; conditional implementation
   roles receive a receipt only when spawned, while not-needed roles receive non-spawn lifecycle
   entries. The general contract forbids shared receipts from substituting for seat receipts
   (`:620`). The deterministic validator alone may build the implementation manifest as a
   mechanical path/hash/status index from the unique receipts, plan, and baseline (`:408,621`), so
   root does not synthesize agent judgment. Review receipts retain only lifecycle, coverage,
   counts, hashes, convergence, and approval metadata.
3. **Non-recursive terminal proof — PASS.** `terminal_reconciler` now performs a pre-terminal check
   of `s00` through `c02`, excludes its running seat, and never claims its future join or close
   (`:143,548-562`). After root joins and closes `x01`, root performs only the authorized mechanical
   check of the host runtime or ACI journal and absence of live seats (`:580,599,617,622`). The
   completion contract requires both the frozen `x01` receipt and host-owned terminal evidence,
   without persisting bridge stdout (`:649-658`). This eliminates the infinite last-reviewer
   regress while preserving root's orchestration-only boundary.
4. **Disjoint product-documentation ownership — PASS.** The prose implementer owns only the
   existing README and exact additional prose paths assigned by the PASS-reviewed artifact plan.
   Its contract explicitly excludes `definition/**`, `robot-talks/**`,
   `implementation-review/**`, automation namespaces, both dispatch files, sessions, and both
   skill trees, and prohibits assigning one exact path to multiple owners
   (`implementation-dispatch.json:129`). Definition, review, validation, automation, and skill
   owners retain their separate namespaces.
5. **No persisted refuted findings — PASS.** The review convergence contract persists only
   `review.md` as the review artifact and prohibits attacker/verifier transcripts plus rejected or
   refuted finding content (`:442-447`). The repair loop keeps only artifact hashes, unique
   receipts, counts, convergence state, approval, and owner assignments; all dropped/refuted
   content and working returns remain ephemeral (`:481`). The boundary and receipt contracts repeat
   the same restriction (`:615,620`). The resulting `review.md` contract contains Coverage,
   verified surviving quoted findings, per-artifact verdicts, and the governing skill's required
   report fields.

### Revalidation

- Deterministic Dispatch Spec validator: `VALIDATION=pass`.
- Frozen source verification: **27 of 27 match; 0 mismatches**.
- User-delegated authority remains attributed to delegated operational judgment, never fabricated
  as direct option selection.
- Component creation remains conditional on reviewed evidence, an owner/consumer contract, exact
  ownership, and validation; no essay, interviewer, profile, schema, specialization, research,
  automation, code, or test is presumed necessary.
- Worktree preservation, ACI binding/fallback, no-commit policy, owner-only CRITICAL/MAJOR repair,
  final review topology, and the three-pass close-session reviewer loop remain intact.

### Final result

- **Dispatch status:** PASS
- **Execution authority:** repaired dispatch hash above only
- **Subagent lifecycle:** feasible; runtime remains pre-run `none`
- **Remaining dispatch-review repairs:** none
- **Next route:** root may execute the repaired dispatch exactly as gated; this review does not
  execute it
