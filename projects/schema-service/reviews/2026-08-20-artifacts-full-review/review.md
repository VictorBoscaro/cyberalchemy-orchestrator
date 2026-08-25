# Review — Schema Service artifact model and experimentation package

## Result

**FIX.** The frozen corpus is internally coherent enough to continue as design work, but it is not
ready for the `analysis` experiment's pre-registration. Four MAJOR change requests survived literal
verification. No target was modified by this review.

This review used the user-authorized degraded execution mode: the attackers, verifiers and writer
worked independently over the same frozen corpus, without inter-agent handoffs. The parent
reconciled their returns and eliminated findings that lacked independent or literal support. This
reduces confidence relative to the canonical sequential review graph and is not evidence that the
runtime's handoff limitation has been solved.

## Coverage

The frozen manifest contains 46 unique targets. Before launch and within every agent return, all
46 paths existed and all 46 SHA-256 values matched `targets.json`.

| Seat | Lens or gate | Result |
| --- | --- | --- |
| Booch | fidelity / governance | Two candidate findings; neither survived reconciliation as a separate change request. |
| Hamming | mechanics / reference-correctness | Parsers, catalog, dispatch bindings and local targets passed; the `#L…` link hypothesis was refuted as renderer-dependent. |
| Deming | operability / gaming-resistance | Five candidates; two survived directly and one was independently corroborated. |
| Parnas | boundary and authority | Three MAJOR findings, including independent confirmation of lifecycle and base-resolution failures. |
| Dijkstra | mechanical non-vacuity | Independently confirmed lifecycle non-representability; catalog and binding checks otherwise passed. |
| Weick | full independent synthesis | Independently confirmed lifecycle non-representability and supplied a 46-file inventory. |

Checks executed read-only:

- 46/46 target paths and hashes;
- JSON, YAML and Markdown frontmatter parsing with no reported parse failures;
- 96 local Markdown link targets with no missing files;
- 5/5 candidate-definition paths, digests and identities;
- inheritance references, candidate properties and experiment references;
- five prior launch bindings, manifests, route digests, seats and attempts;
- explicit boundary between experimental and normative schema resolution.

The zero-findings red flag was executed and did not fire: four MAJOR findings survived. Findings
about line-fragment rendering, historical `git diff --check`, absent runtime implementation and
open publication authority were not promoted merely because the review could not prove them; the
corpus either states those limitations or the attack lacked a stable failure criterion.

## Verified findings

### F1 — Candidate lifecycle is promised but cannot be represented per candidate

- **Severity:** MAJOR
- **Targets:**
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/catalog.yaml:5-33`
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/README.md:25-35,47-49`
- **Evidence:** the catalog has one top-level `"lifecycle_state: active"`; none of its five
  definition entries has a lifecycle state. The contract says: `"Only active candidates may serve
  new runs. superseded, abandoned and promoted candidates are retained for exact replay"`.
- **Failure:** one candidate cannot be superseded, abandoned or promoted while its siblings remain
  active. The resolver can satisfy its documented check by observing only the active catalog and
  continue serving a terminal candidate.
- **Minimum fix:** add authoritative lifecycle state per candidate revision (and successor or
  promotion reference where applicable), define allowed transitions, and require the experimental
  resolver to check both catalog availability and the exact candidate's state.

### F2 — The stated execution gate still leaves every candidate resolution fail-closed

- **Severity:** MAJOR
- **Targets:**
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis@0.yaml:9-11`
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/README.md:29-35`
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/README.md:30-33`
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/experiment-manifest.yaml:10-18`
- **Evidence:** the root declares `"base_schema_ref: null"` and
  `"base_status: unresolved_bootstrap_dependency"`; the resolver contract says an unavailable base
  `"must fail closed"`. Yet the package says concrete fixtures may execute after only the criterion
  is frozen, and the manifest records no independent base-resolution gate.
- **Failure:** all four refinements extend the root, so satisfying the documented criterion-freeze
  gate still cannot produce a valid experimental resolution. A maintainer must either invent an
  exemption or execute fixtures that are required to fail before exercising the intended subtype
  behavior.
- **Minimum fix:** keep fixtures blocked until the root's base is revision-exact and resolvable, or
  explicitly define and validate an experiment-local root-without-base semantic. Represent this as
  a distinct pre-run gate in the manifest and criterion contract.

### F3 — Candidate revision immutability begins too late

- **Severity:** MAJOR
- **Targets:**
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experimentation-plan.md:56,80-87`
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/README.md:41-49`
- **Evidence:** the plan calls the candidate definition files immutable and says changes create new
  revisions. The candidate contract weakens this to `"it is never edited in place after use by a
  frozen run"`.
- **Failure:** bytes may be rewritten after catalog admission or criterion freeze but before the
  first frozen run, while retaining the same `candidate_revision_id`. Updating the catalog digest
  would preserve snapshot integrity but destroy revision identity and invalidate the frozen
  criterion's meaning.
- **Minimum fix:** make a candidate revision immutable from catalog admission. Every byte change
  must create a new `candidate_revision_id`; criterion freeze must pin the catalog and exact
  candidate digests used by its fixtures.

### F4 — Local placeholders weaken the program's substantive successor gates

- **Severity:** MAJOR
- **Targets:**
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/02-skill/README.md:8-10`
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/03-folder/README.md:8-11`
  - `projects/schema-service/experimentation-plans/artifact-types-v0/experimentation-plan.md:31-36,126-127,146-147`
- **Evidence:** the plan permits Experiment 2 only if Experiment 1 finds a useful kernel without
  collapsing roles, and Experiment 3 only if Experiment 2 preserves containment separately from
  identity; both also require an explicit plan revision. The local placeholders say only
  `"Deferred until Experiment 01 findings are accepted"` and `"Deferred until Experiment 02
  findings are accepted"`.
- **Failure:** accepted negative findings can satisfy the local text without satisfying the
  substantive learning gate. A maintainer entering through a working-folder README can therefore
  treat acceptance alone as authorization to proceed.
- **Minimum fix:** restate the substantive gate and explicit-plan-revision requirement in both
  placeholders, or link to the exact normative section while stating that accepted findings are
  necessary but insufficient.

## Refuted and bounded hypotheses

Nine candidate hypotheses were eliminated or bounded during reconciliation:

- path, label, digest or `latest` silently granting normative authority;
- promotion rewriting earlier experimental references;
- reclassification mutating artifact identity or history;
- an A/B result analysis collapsing into the A/B experiment itself;
- a folder becoming an artifact solely by being present;
- malformed JSON, YAML or frontmatter;
- mismatched candidate IDs, digests, inheritance or launch bindings;
- local Markdown file targets being absent;
- `#L…` fragments being universally broken independent of renderer.

Open questions about durable ID serialization, concrete publication authority, a future resolver,
criterion contents, fixtures and validators remain limitations, not verified defects in a package
that explicitly declares itself `preparing`.

## Target inventory

| # | Target | Verdict |
| ---: | --- | --- |
| 1 | `.codex/workflow-inputs/2026-08-17-schema-concrete-artifact-precedents/close.json` | KEEP |
| 2 | `.codex/workflow-inputs/2026-08-17-schema-concrete-artifact-precedents/explorers-0-turn-0.json` | KEEP |
| 3 | `.codex/workflow-inputs/2026-08-17-schema-concrete-artifact-precedents/explorers-1-turn-0.json` | KEEP |
| 4 | `.codex/workflow-inputs/2026-08-17-schema-concrete-artifact-precedents/launch-plan.json` | KEEP |
| 5 | `.codex/workflow-inputs/2026-08-17-schema-concrete-artifact-precedents/non_vacuity_review-0-turn-0.json` | KEEP |
| 6 | `.codex/workflow-inputs/2026-08-17-schema-concrete-artifact-precedents/opening.json` | KEEP |
| 7 | `.codex/workflow-inputs/2026-08-17-schema-experimental-type-staging-rule/close.json` | KEEP |
| 8 | `.codex/workflow-inputs/2026-08-17-schema-experimental-type-staging-rule/launch-plan.json` | KEEP |
| 9 | `.codex/workflow-inputs/2026-08-17-schema-experimental-type-staging-rule/opening.json` | KEEP |
| 10 | `.codex/workflow-inputs/2026-08-17-schema-experimental-type-staging-rule/rule_reviewers-0-turn-0.json` | KEEP |
| 11 | `.codex/workflow-inputs/2026-08-17-schema-experimental-type-staging-rule/rule_reviewers-1-turn-0.json` | KEEP |
| 12 | `projects/schema-service/experimentation-plans/artifact-types-v0/experimentation-plan.md` | **FIX** |
| 13 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/catalog.yaml` | **FIX** |
| 14 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis@0.yaml` | **FIX** |
| 15 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis-ab-test-result@0.yaml` | KEEP |
| 16 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis-general@0.yaml` | KEEP |
| 17 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis-observational-study@0.yaml` | KEEP |
| 18 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/definitions/analysis-observed-phenomenon@0.yaml` | KEEP |
| 19 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/candidate-types/README.md` | **FIX** |
| 20 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/experiment-initial-definitions.md` | KEEP |
| 21 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/experiment-manifest.yaml` | **FIX** |
| 22 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/fixtures/README.md` | KEEP |
| 23 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/README.md` | **FIX** |
| 24 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/runs/README.md` | KEEP |
| 25 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/02-skill/README.md` | **FIX** |
| 26 | `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/03-folder/README.md` | **FIX** |
| 27 | `projects/schema-service/README.md` | KEEP |
| 28 | `projects/schema-service/research/artifact-schema-governance-landscape/findings.md` | KEEP |
| 29 | `projects/schema-service/research/artifact-schema-governance-landscape/research-initial-definitions.md` | KEEP |
| 30 | `projects/schema-service/research/concrete-artifact-family-precedents/findings.md` | KEEP |
| 31 | `projects/schema-service/research/concrete-artifact-family-precedents/reports/01-ontology-conventions.md` | KEEP |
| 32 | `projects/schema-service/research/concrete-artifact-family-precedents/reports/02-domainspec-core.md` | KEEP |
| 33 | `projects/schema-service/research/concrete-artifact-family-precedents/reports/03-non-vacuity-review.md` | KEEP |
| 34 | `projects/schema-service/research/concrete-artifact-family-precedents/research.md` | KEEP |
| 35 | `projects/schema-service/research/concrete-artifact-family-precedents/research-initial-definitions.md` | KEEP |
| 36 | `projects/schema-service/research/concrete-artifact-family-precedents/verification.md` | KEEP |
| 37 | `projects/schema-service/research/experimental-type-staging-rule/findings.md` | KEEP |
| 38 | `projects/schema-service/research/experimental-type-staging-rule/reports/01-staging-precedents.md` | KEEP |
| 39 | `projects/schema-service/research/experimental-type-staging-rule/reports/02-authority-leak-review.md` | KEEP |
| 40 | `projects/schema-service/research/experimental-type-staging-rule/research.md` | KEEP |
| 41 | `projects/schema-service/research/experimental-type-staging-rule/research-initial-definitions.md` | KEEP |
| 42 | `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/dialogue.md` | KEEP |
| 43 | `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/findings.md` | KEEP |
| 44 | `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/reports/01-conceptual-model.md` | KEEP |
| 45 | `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/reports/02-admission-governance.md` | KEEP |
| 46 | `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/reports/03-representation.md` | KEEP |

## Ordered change requests

1. Make lifecycle state representable and enforceable per candidate revision.
2. Add a distinct, machine-checkable base-resolution gate before any fixture execution.
3. Make candidate revisions immutable from catalog admission and pin their digests at criterion freeze.
4. Restore the substantive successor gates and explicit plan-revision requirement in the Experiment 2 and 3 placeholders.
