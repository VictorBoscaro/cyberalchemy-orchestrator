# Bootstrap validation — `research-plan.md`

## Verdict

**PASS.**

The draft preserves the six accepted Robot-Talks dispositions and the bootstrap boundary from
`planning/inputs/02-repository-bootstrap.md`. It is safe to use as a proposed plan: accepting it authorizes only
founding-package preparation. No critical or high-severity finding was found. M1, M2, L1 and L2 from the initial
validation are resolved in the corrected draft.

## Revalidation

Scope: only M1, M2, L1 and L2 from this validation. No other part of the plan was reopened.

| finding | result | corrected evidence | assessment |
|---|---|---|---|
| M1 — receipt/commit ordering | **PASS — RESOLVED** | A4 lines 223–228 | The plan now commits the accepted package as a foundation commit, validates that commit from a clean clone, then adds the receipt in a closure commit. The receipt identifies the foundation commit and A5 uses the closure commit, eliminating self-reference. |
| M2 — validation evidence and pass conditions | **PASS — RESOLVED** | A4 lines 221–247 | V1–V8 are explicit. Each check records `PASS|FAIL|N/A`, evidence and reasons for `N/A`; V1–V7 must pass and V8 is conditional on authorized remote provisioning. |
| L1 — canonical manifest fields | **PASS — RESOLVED** | section 11, lines 440–452 | Source entries now name `id`, `role`, locator, revision, worktree state, path, selector, digest, capture/access and conditional snapshot path. Dependency entries now name `id`, `concern`, consumer, provider, interface, version, digest, compatibility, optionality, allowed surface, status and removal test. |
| L2 — A2 closure and owner acceptance | **PASS — RESOLVED** | A2 lines 204–206; immediate work lines 536–540 | A2 closes only after explicit owner acceptance of charter, authority model, decision `0001`, research plan and frozen manifest, recorded with version/digest. The text explicitly says review acceptance and ratification do not authorize repository creation. |

**Revalidation result: PASS.** No correction from the scoped set remains open.

## Gate validation

| gate | result | evidence in draft | assessment |
|---|---|---|---|
| A0 — plan acceptance | **PASS** | lines 21–23, 131–141 | Acceptance authorizes only package preparation; repo, remote, runtime and implementation remain unauthorized. Creation parameters are deferred explicitly. |
| A1 — founding package | **PASS** | lines 143–177 | The package matches the minimum input exactly and excludes full `mint`, vault, broad imports, runtime machinery, CI and implementation. |
| A2 — independent review | **PASS** | lines 179–193 | Review covers identity, authority, provenance, immediate consumers, provider boundary, execution link and clean-clone portability; it explicitly does not authorize creation. |
| A3 — creation authorization | **PASS** | lines 195–199 | Exact target parameters and accepted manifest digest are required; local creation and remote provisioning are separate permissions. |
| A4 — create and validate | **PASS** | lines 214–247 | Target safety, manifest-only installation, foundation/closure commit ordering, V1–V8 evidence, remote separation and clean-clone checks are explicit. |
| A5 — canonical handoff | **PASS** | lines 215–229 | Human acceptance precedes transfer; one canonical editable authority remains; antecedent, closure pointer and first scoped branch are explicit. |

## Accepted-findings coverage

| accepted finding | result | draft coverage |
|---|---|---|
| T1 — product authority vs research authority | **PASS** | Authority table separates charter, master context, plan, branches, findings, decisions and receipts; only a decision changes charter or authorizes implementation (lines 25–38). |
| T2 — clean repo as owner decision | **PASS** | The clean repo is named an owner decision with revisit condition rather than an empirical result (lines 48–49); `0001` is mandatory in A1. |
| T3 — research-first vs empirical prototype | **PASS** | No implementation is authorized by plan acceptance; experiments and one bounded prototype require discriminating evidence and B4 (lines 343–350, 462–474). |
| T4 — proportional bootstrap, not complete `mint` | **PASS** | Full `mint` is rejected; A1 excludes Universal Governance Baseline, constitutions, vault and empty taxonomies (lines 51–52, 171–173). |
| T5 — SWI as peer/provider candidate | **PASS** | SWI is not product authority and remains an external replaceable reference/provider candidate (lines 53–54, 275–279, 396–399). |
| T6 — lineage without architectural inheritance | **PASS** | Narrow source pins, dependency-by-consumer, execution link, portability and bans on broad/copy imports are explicit (lines 171–177, 181–190, 381–403). |

## Findings by severity

### Critical

None.

### High

None.

### Medium — resolved on revalidation

#### M1 — The creation receipt cannot reliably contain the commit that contains the receipt

**Evidence:** A4 requires `decisions/0002-bootstrap-receipt.md` to record the “initial commit” (lines 210–211),
but it does not define when the initial commit is created. If the receipt is part of that same commit, its content
cannot contain that commit's final identity without a self-reference cycle. The plan also never explicitly says
to create the commit between installation and clean-clone validation.

**Impact:** Creation can be performed in different, non-equivalent orders; the receipt may carry a placeholder,
the wrong commit, or an unverifiable claim. This weakens provenance and the A4/A5 handoff but does not broaden
authorization.

**Minimum correction:** In A4, define a two-commit sequence: (1) validate and commit the accepted package as the
foundation commit; (2) clean-clone that commit, then add `0002-bootstrap-receipt.md` in a closure commit that
records the foundation commit, validation results and any deviations. A5 should point to the closure commit while
the receipt identifies the foundation commit. Alternatively, record the Git tree digest rather than a same-commit
hash, but the two-commit sequence is clearer.

#### M2 — A4 names validation categories but not the required evidence or pass conditions

**Evidence:** A4 item 4 compresses manifest integrity, provenance, portability, authority, boundary, hygiene and
scratch reproducibility into one sentence (lines 208–209); item 7 adds clean-clone checks. The bootstrap input
requires distinct V1–V8 checks, including no-clobber, secrets/line-ending review, untracked-source truthfulness,
absence of junctions/hooks/copied frameworks, README authority resolution and conditional remote verification.

**Impact:** The correct concerns are present, but an executor could claim A4 complete without showing which
checks ran, what passed, or what was inapplicable. The plan's completion condition therefore lacks a reproducible
validation witness.

**Minimum correction:** Add to A4 or its receipt contract a checklist keyed to V1–V8 from the bootstrap input,
with `PASS|FAIL|N/A`, command or inspection evidence, and reason for every `N/A`. Require V1–V7 to pass and V8 only
when a remote is authorized before A5.

### Low — resolved on revalidation

#### L1 — Source and dependency manifests omit a few canonical field names

**Evidence:** Source policy (lines 383–394) includes locator, revision, worktree state, path/selector, digest,
capture date, access/license and snapshot rule, but does not explicitly require source `id`, `role`, or
`snapshot_path`. Dependency policy (lines 396–399) covers consumer, allowed surface, version, compatibility,
digest, optionality and removal, but does not explicitly require `id`, `concern`, `status`, or a separately named
`provider` field.

**Impact:** Semantics are substantially covered, but independently authored YAML may drift in shape and become
harder to validate.

**Minimum correction:** Refer from section 11 to the exact field sets in the accepted
`DEPENDENCIES-AND-PROVENANCE.md`, or list the missing names. Keep the policy semantic; do not add a schema or
tooling dependency at bootstrap.

#### L2 — A2 review closure and owner acceptance are separated across sections

**Evidence:** A2 says blocking findings are corrected and the package reviewed again (lines 192–193), while the
explicit acceptance of charter, authority model, decision `0001`, and plan appears only in “Immediate next work”
(lines 467–470).

**Impact:** A sequential reader of Horizon A could treat a clean review as sufficient input to A3 without
noticing the artifact acceptance requirement later. A3 still requires an “accepted transfer manifest,” so the
authorization boundary is not lost.

**Minimum correction:** Add one sentence to A2: it closes only when the owner explicitly accepts the charter,
authority model, decision `0001`, research plan and frozen transfer manifest. Preserve that this acceptance does
not authorize A3 actions.

## Cross-cutting checks

- **Authorization separation — PASS.** Planning/package preparation, local repo creation, remote provisioning,
  human foundation acceptance and product implementation are distinct decisions.
- **Minimum package — PASS.** All bootstrap-input artifacts are present; no extra object-level authority is
  smuggled in.
- **Provenance — PASS.** Dirty/untracked truthfulness, digest, selector, durable locator, snapshot rules and
  canonical manifest fields are present.
- **Portability — PASS.** Local paths are observational only; scratch and clean-clone checks are required; sibling
  paths, copied frameworks and broad submodules are excluded.
- **Creation and handoff — PASS.** Exact target, separate remote permission, two-commit provenance and explicit
  validation evidence are sound.
- **No premature implementation — PASS.** Horizon B may conduct low-commitment experiments, but B4 is a separate
  discriminating prototype gate and plan acceptance grants no implementation authority.
- **No complete `mint` — PASS.** Only proportional mold lessons, provenance and default-deny survive; there is no
  full casting, inherited vault, universal taxonomy or claim that `mint` is an executable repo creator.

## Required disposition

M1, M2, L1 and L2 are resolved. The draft may proceed to plan acceptance and A1 preparation. Repository creation
still requires A3, remote mutation remains separately authorized, and product implementation remains outside this
validation.
