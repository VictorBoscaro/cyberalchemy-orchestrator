---
artifact_kind: external-local-corpus-manifest
status: adopted-for-redesign
launch_readiness: not-launch-ready
captured: 2026-08-13
source_repository: C:/Users/victo/domainspec-core
source_revision: 9bfec22712e4675d39c4cf1c21b36dc66614136c
source_branch: master
---

# Proposed corpus annex — DomainSpec v2

## Boundary and authority

`domainspec-core` is outside the `cyberalchemy-orchestrator` checkout but inside the same private
project ecosystem. For this study it is an **internal ecosystem source**, not external literature.
Its local `AGENTS.md` identifies DomainSpec and its authority spine as private. The corpus may be
read in place and cited by repository identity, relative path, revision and SHA-256; its prose must
not be copied into public Arcanum surfaces.

The source repository was on branch `master` at revision
`9bfec22712e4675d39c4cf1c21b36dc66614136c`. The repository had extensive unrelated worktree
changes, but `git status --short -- <the 13 paths below>` returned no entries. Revision identifies
the repository baseline; each SHA-256 below is the binding authority for the bytes actually
inspected. Any path, byte, revision, authority-boundary or availability drift requires a new
manifest and human confirmation.

This annex locates candidate evidence. It does not claim that any listed artifact realizes
composition, that the list is a taxonomy, or that DomainSpec v2 supplies a general theory.

## Exact inclusions

| # | repository-relative path | source role / reason for inclusion | authority state | SHA-256 | bytes |
|---:|---|---|---|---|---:|
| 1 | `projects/domainspec-v2/README.md` | Project boundary, implementation/research split, tower and artifact conventions. | project overview; not proof of execution | `ca5cfbc0a467e3f14e459236d373db4c046f428930c0fae7571246bfe0aeefff` | 6246 |
| 2 | `projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md` | Declared composition of opposed research lanes and their synthesis/decision boundary. | project discipline | `cb09d2412e53288ae891ad6d1f03ff5d56c10808824bf0d7e025fc233cd93557` | 2575 |
| 3 | `projects/domainspec-v2/research/domainspec-v2-research-towers.dispatch.json` | Concrete workflow graph connecting towers, dialectic lanes, synthesis, decision and handoff. | designed/validated route; README says not executed | `83206a57f4ed8d05a1c623ede6db17ae058e74fcfdc184150d20f2f7096147fd` | 15381 |
| 4 | `projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/lens-narrative.md` | One explicitly named independent research lens in a preserved three-lens case. | local research only | `8b58ef34e0ce95ee5dc76757a963bc3512f53fc97fadc6e460608d00bb23f11c` | 18694 |
| 5 | `projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/lens-example.md` | Second explicitly named independent research lens in the same case. | local research only | `d0885fe8899d245dcee081974d4551e9797f332b33afcfb399b031e3852ac20b` | 14843 |
| 6 | `projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/lens-distillation.md` | Third explicitly named independent research lens in the same case. | local research only | `c96a7366c8bf67d263def4ec1358feb08b55aa6acb5ded10535557f8a109eec5` | 20274 |
| 7 | `projects/domainspec-v2/research/target-state/2026-07-02-comprehension-narrative-model/findings.md` | Preserved synthesis that declares its three lens inputs and skeptic review. | candidate/local research; no promotion | `774c37b64ae35c9536ebb0fdc2442b052a578187f663f2ff39bece335639e3f4` | 7778 |
| 8 | `projects/domainspec-v2/research/2026-07-01-composability-edges-taxonomy-synthesis.md` | Explicit local attempt to relate composability, edges and taxonomy; useful as a claimed model, not accepted truth. | candidate Inventory synthesis | `bf2a5a45f7214e36eda2048251315571a6d8d27be7a1e59c1c8f0ce23963fc0d` | 10798 |
| 9 | `projects/domainspec-v2/research/typed-artifacts-precedent/findings.md` | Explicit claims and limits concerning composition of typed artifacts and an unwired integrated loop. | draft research findings | `597bdf17b876b2d4ab68b91e6c748cdb849214cd36cec011d3e83b75dc59606f` | 9923 |
| 10 | `projects/domainspec-v2/research/spec-ontology-unification/DESIGN.md` | Concrete toy pipeline mapping typed nodes and edges into patterns and composition rules. | candidate design; local research only | `e5410e893314d0c000d291e02a527b4535e5f689f9862ab0b1259e1d78138432` | 6410 |
| 11 | `projects/domainspec-v2/development/ds-d1-improvement-plan/WORK-PACK.md` | Work decomposition, dependency, artifact-contract and recomposition practice across definitions, schemas, validators and read models. | draft planning package; execution receipts remain separate | `c70bca7310ac0e3e06046f88a978e85edb82b6ba8fbe4d40f29f3f8526029d81` | 18242 |
| 12 | `projects/domainspec-v2/impl/spec/meta-types/ui/component.schema.yml` | Concrete interface/component formation candidate with typed I/O, edge participation and explicit non-authority flags. | implementation-owned development profile; not canonical DS-D1 authority | `46540796103bac845fc78aee3deceb8fe905a85968b76f7edb7d987efc8deca0` | 1286 |
| 13 | `projects/domainspec-v2/definitions/relationships/relationships.yml` | Active relationship-signature authority containing typed graph fragments and per-edge composition obligations. | active local relationship authority; not a general composition ontology | `7757884f599bb18707f105add8b9de92fb2ea58d78e216d3aa228b0ad25ea013` | 27039 |

## Deliberate exclusions

- The rest of `projects/domainspec-v2/**`: excluded to keep a bounded denominator and avoid turning
  corpus location into substantive research.
- `cyberAlchemy-v2/**`: private authority-spine and duplicated staging/refresh materials are not
  needed to establish these candidate cases.
- `implementation/domainspec/**` and `validation/**`: v1/frozen or validation mirrors are excluded
  from this v2 annex.
- `research/**/research.md`, broad session evidence, receipts, fixtures, generated outputs and
  refresh/baseline/staging copies: excluded unless a later selector-level need is separately
  justified; their inclusion now would duplicate occurrences and blur prescribed versus executed.
- External citations referenced inside the selected research files: not acquired here and do not
  become part of the internal corpus by transclusion.
- Untracked or modified source-repository files: excluded. This annex does not legitimize the
  surrounding dirty worktree.

## Contamination, privacy and interpretation risks

- DomainSpec v2 already uses words such as `composition`, `composable`, `lens` and `recomposition`.
  Extractors must record literal local use and authority state without importing those terms as the
  Composition Lab's definition.
- Several selected artifacts are proposals, candidate research or development profiles. They must
  not be collapsed into execution or canonical authority.
- The explicit three-lens case can anchor comparison but must not make lens composition the model
  for composition in general.
- Private project paths and prose may be cited inside the private ecosystem only. No source copy,
  public export, external upload or publication is authorized.
- A sibling checkout can move independently. Revalidation must check repository identity, revision,
  per-file status, exact path, size and SHA-256 before use.

## Effect on the existing internal proposal

This corpus annex is **adopted for redesign** and is **not launch-ready**. Adding it changes the
future corpus denominator. The prior freeze of 22 sources, 41 hashes and 176 obligations, together
with every derived partition, prompt, corpus digest and human confirmation sheet, must be
regenerated and independently re-audited before any new confirmation or launch decision. It does
not resolve or alter the Inventory-owned bounded-bootstrap blocker, registration prohibition, host
binding/close gap, or description/adjudication boundary.
