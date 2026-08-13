---
artifact_kind: inventory-bootstrap-execution-gate-adversary
status: block
date: 2026-08-13
scope: design-02-pre-human-execution-gate
reviewed:
  - 01-source-location.md
  - 02-bootstrap-design.md
  - 03-bootstrap-adversary.md
  - .arcanum/inventory/
mutation: none-to-targets
---

# Gate adversary — bounded Inventory bootstrap

## Verdict

**BLOCK.** Design 02 is coherent enough to preserve and revise, but it is not ready for the exact-run
or launch gate. T3 passes as a static design property. T1, T2, and T4–T16 lack their required
pre-launch evidence or contain an unresolved contract defect. This review does not implement the
bootstrap and does not authorize Inventory, skill-surface, sibling-checkout, ledger, or D1 mutation.

The strongest improvement over 03 is real: 02 removes the unsupported connected
extractor → assembler → auditor graph. However, it still uses handoff language and an unowned
artifact/report path to describe a connectionless writer/auditor sequence. It also has no
demonstrated transactional rollback. Its only demonstrated reversal concept is a later, separately
human-approved `superseded`/tombstone operation.

## Evidence boundary

- `01` proves that canonical source location is **FOUND**, while owner ratification, generated
  surface conformance, and `.codex` ownership remain unresolved.
- `02` is a proposal with `status: proposed-blocked-for-execution`; no fixtures claimed by it were
  found under `.arcanum/inventory/`.
- `03` supplies T1–T16 as the attack obligations; 02 replaces the connected T5/T6 fixture with a
  connectionless artifact barrier rather than waiving those obligations.
- `.arcanum/inventory/index.json` parses, declares `inventory-read-model-only`, and is empty. The
  D1 manifest, card bundles, and validation report named by 02 do not yet exist.
- No second Inventory `index.json` or `schema.md` was found under
  `internal-tools/composition-lab/`; this supports T3 only.

Absence of a fixture is reported as missing readiness evidence, not as proof that a fixture cannot
be built.

## T1–T16 gate matrix

| Test | State | Adversarial finding / evidence required |
|---|---|---|
| T1 canonical owner | **BLOCK** | `01` closes location only. `02` itself says owner ratification, `.codex` ownership, stale metadata, and generated-surface conformance remain BLOCK. Obtain the separate owner/conformance decision; do not infer authority from source discovery. |
| T2 reuse falsifier | **BLOCK** | The reuse gate is specified at 02:313–315 but no human answer naming a concrete consumer/revalidation event is present. Record the answer as a separate gate result. |
| T3 single system | **PASS (design/static)** | 02:54–57 and 131–166 name `.arcanum/inventory/` as sole owner. Static inspection found no competing Inventory index/schema under Composition Lab. This does not validate later writes. |
| T4 artifact fit | **BLOCK** | 02:158–169 materially redefines `research.md` and `findings.md` and explicitly requires human approval. No such approval or projection fixture exists. |
| T5 lifecycle dry run | **BLOCK** | No first-line binding, attempt identity, terminal-order, completion, or parent-close fixture exists. The proposed two-seat run remains host-dependent by 02:294–295. |
| T6 connection integrity / artifact barrier | **BLOCK** | `connections: []` is plausible, but the contract is internally equivocal: 02:32 calls the artifact set “the only handoff”; 02:272 returns `WriterHandoff`; 02:288 calls parent-supplied rows “the auditor handoff.” Rename and fixture this as a host-owned artifact barrier, not an inter-seat return. Prove wrong path/hash/attempt, early launch, missing output, and parent-authored prose fail closed. |
| T7 confirmation | **BLOCK** | Four gates exist, but are not completed. The exact-run gate also omits explicit acceptance/rejection of non-transactional mutation risk and does not name the owner/path of every terminal report. |
| T8 immutability | **BLOCK** | The hash and allowlist design is sound, but no frozen manifest or drift/target-escape fixture exists. Detection of partial writes is not rollback. |
| T9 minimal schema | **BLOCK** | No D1 card fixture or canonical v0.2 schema validation is present in the installed package. The local package contains conventions, not the machine schema invoked by 02:186–189, while 01 records stale generated surfaces. Validate against the owner-ratified schema and show extension-field acceptance before gate. |
| T10 authority escape | **BLOCK** | Boundary language is strong, but the definition/causality/novelty/soundness/promotion/GO-KILL negative fixtures have not run. |
| T11 denominator | **BLOCK** | `.arcanum/inventory/raw/d1-lens-use-corpus.manifest.json` does not exist. No frozen source × control denominator or cell coverage can yet be audited. |
| T12 mechanical validation | **BLOCK** | The base `index.json` parses, but there are zero D1 rows and no cross-view fixture. More importantly, 02:263–264 says files update in one writer attempt and partial update is a validation failure; it supplies no multi-file atomic commit or rollback. Detection is not recovery. |
| T13 observability | **BLOCK** | Signals and D1 dimensions are proposed, not fixture-proven. The exact write owner, destination, and failure semantics for observability are not frozen. |
| T14 conflict preservation | **BLOCK** | Separate-card/residue rules are specified, but no disagreement fixture proves that overwrite, normalization, and majority choice fail. |
| T15 reversibility | **BLOCK** | 02:347–361 defines later retirement, not transactional rollback. No rollback is demonstrated. Reversal is a subsequent Inventory operation requiring separate human approval, marking records `superseded` and appending a tombstone; it cannot repair an interrupted writer attempt automatically. The retirement fixture is also absent. |
| T16 no-launch review | **BLOCK** | 02 requires R1–R4, final `/review`, and explicit human launch authorization. Those gates are not evidenced here; any surviving material finding must hold launch. |

## Load-bearing defects

### 1. Connectionless topology still uses false handoff semantics

02 correctly declares “There is no inter-seat return edge” and `connections` exactly `[]`, but then
declares a `WriterHandoff` and an “auditor handoff” supplied by the parent. A connectionless design
may sequence seats through independently readable, predeclared files; it must not describe a writer
return as if the runtime delivered it to the auditor.

**Required correction:** replace `WriterHandoff` with `WriterCompletionManifest`; define a
host-owned `ArtifactBarrierManifest` containing only predeclared path/hash/size/attempt/terminal
facts; make the auditor open those files directly. State that neither writer prose nor writer return
is an effective input. If the host cannot create and bind this barrier without parent interpretation,
remain BLOCK with `inventory-connected-topology-required`.

### 2. Terminal outputs do not have complete ownership

The layout reserves `.arcanum/inventory/lint/d1-lens-use-validation.md`, but the fixed-seat table says
the auditor writes “none.” The completion section requires “one capability-local completion report”
without naming its author, path, write boundary, or relation to the lint report. The writer cannot
pre-author an independent audit. The parent cannot synthesize it while claiming to only orchestrate.
The one-correction loop also implies auditor → writer → auditor artifact consumption that is not
declared.

**Required correction:** add an output-ownership table covering every file and every attempt. A
minimal honest split is:

- writer owns only candidate bundles, manifest-derived projections, and the Inventory index/tag/log
  changes frozen for its attempt;
- auditor owns one predeclared, immutable capability-local audit/completion report outside the
  Inventory read model, and writes no candidate/index/log content;
- the host owns barrier manifests and attempt/terminal metadata, never semantic prose;
- correction defects are frozen as an auditor artifact and rebound to the single allowed writer
  correction attempt; the second audit writes a new attempt-specific report rather than overwriting
  the first.

Either remove `lint/d1-lens-use-validation.md` from the writer-era layout or explicitly introduce a
post-audit indexing act with its own owner and revalidation. Do not leave a future audit file
pre-indexed before it exists.

### 3. Partial mutation has detection but no transactional rollback

The bootstrap mutates card bundles, two indexes, tags/log, and two Composition Lab projections.
02 makes partial update a validation failure, but no staging transaction, commit protocol, backup,
or restore fixture is specified. Therefore a failed attempt can leave a mechanically invalid
read model even when the run truthfully returns BLOCK.

**Required correction:** state explicitly in the exact-run gate:

> No transactional rollback has been demonstrated. Failure may leave partial generated state.
> Reversal, if later approved by a human, is a separate operation using `superseded` records and an
> append-only tombstone; it is not rollback of the failed attempt.

Before mutation, either demonstrate a bounded staging/commit-and-restore fixture for the entire
write set, or ask the human to accept the non-transactional risk together with an exact recovery
plan and recovery owner. T15 must remain named “retirement/reversal,” not “rollback.”

### 4. The human gate is not yet decision-complete

The four-gate structure is useful but does not yet present one closed decision surface. In addition
to the fields at 02:313–325, the human must receive:

1. the T1 owner/conformance result and T2 reuse answer;
2. the exact output-ownership and attempt-specific path table;
3. the artifact-barrier schema and evidence that it is host-owned, connectionless, and fail-closed;
4. the canonical schema validator/version actually used;
5. the full allowlist and an explicit statement that observability writes are inside or outside it;
6. the correction-cycle artifact flow and cap;
7. the absence of transactional rollback, the possible partial-state consequence, and the separate
   human-approved `superseded`/tombstone reversal path; and
8. fixture and independent-review results, including unresolved findings.

Any change to those fields invalidates confirmation. Milestone-wide permission to use agents is not
authorization for this mutation.

## Corrections required before re-review

1. Resolve T1 and record T2/T4 human decisions separately from launch authorization.
2. Replace handoff terminology with an explicit host-owned artifact-barrier contract and freeze its
   schema.
3. Assign every output, audit, completion, observability record, and correction artifact to exactly
   one owner and attempt-specific path.
4. State the no-rollback fact and choose, at the human gate, between demonstrated bounded recovery
   and explicit acceptance of partial-state risk. Keep later tombstone reversal separate.
5. Produce, without launching D1, the T5–T15 fixtures named by 02; preserve their hashes and verdicts.
6. Run the independent R1–R4 reviews and final `/review`; carry every surviving material finding
   into the launch gate.

## Gate disposition

| Decision | Result |
|---|---|
| Preserve/revise design 02 | **PASS** |
| Present current design as execution-ready | **BLOCK** |
| Run bootstrap fixtures | **BLOCK** until exact fixture proposal, output ownership, host binding/barrier path, and mutation-risk terms are confirmed |
| Launch D1 or mutate Inventory | **BLOCK** |
| Reverse later via `superseded` + tombstone | **BLOCK pending separate human approval** |

Re-review only after the corrections above are represented as artifacts and the required fixtures
exist. A cleaner description alone cannot turn a missing execution proof into PASS.
