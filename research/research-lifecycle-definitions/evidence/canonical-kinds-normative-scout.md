---
tags: [research, evidence, canonical-kinds, lifecycle]
artifact_kind: research-evidence
status: draft
---

# Canonical Kinds — Normative Scout

## Sources inspected

- Frozen local context: `research/research-lifecycle-definitions/research-initial-definitions.md:36-63,65-99` and `vault/ontology-conventions.md:67-92,296-319,389-506`.
- Frozen sibling corpus: `../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md:11-39,58-170,172-255,296-395,411-486`; `../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml:1-52`; `../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/EDGES.yaml:1-183`; `../domainspec-core/sessions/2026-07-13-1624-canonical-kinds-instance-contract.md:20-48,50-79`; and `../domainspec-core/cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:88-105,121-165,182-205,219-240`.

## Direct contract evidence

- **What is registered/canonical there.** A canonical artifact is an instance of an enumerated fine `canonical_kind`; it is typed and process-born, but does not thereby gain authority. An unenumerated kind is non-canonical/free working material. `CANONICAL-KINDS.md:13-24`.
- **Important qualification.** The same candidate document says Tier-1 is *not closed yet* and extension is owner-gated, but its OQ-1 says whether Tier-1 is ultimately closed/default-deny or open/additive remains unresolved. `CANONICAL-KINDS.md:58-64,112-114,413-418`. Therefore “enumerated only” is the present candidate rule, not proof that a future portable registry must be immutable or permanently closed.
- **Authority boundary.** `process`, `authority_kind`, `durability`, contradiction handling, and authority reachability are type-level facts; instances are to look them up rather than declare them, specifically to prevent self-promotion. Canonical membership and authority are separate; promotion is owned elsewhere. `CANONICAL-KINDS.md:30-39,101-108,143-153,241-251`.
- **Scope boundary.** The actual instance-frontmatter contract is candidate and expressly limited to `discovery`, `research`, `findings`, and `session`; no contract may be inferred for other kinds. `CANONICAL-KINDS.md:120-124`. The review independently warns that no current validator enforces either kind enum and the canonical admission branch has zero instances. `findings.md:92-98,144-147`.

## Discovery and research generation processes

- The candidate enumeration associates `discovery` with `domainspec-discovery-writing`, and `research` plus `findings` with a research dispatch under `domainspec-subagents-strategy`; a `session` is associated with `close-session`. `CANONICAL-KINDS.md:66-71`.
- This is not a universal membership criterion even inside domainspec-core: six listed kinds lack a genuine producing owner route, and OQ-6 concludes that “produced by a declared process” was never the membership test for canonicity. `CANONICAL-KINDS.md:457-476`.
- A session can record only provenance acts: it may `creates` or `updates` an Evidence artifact, while claims such as refutation or opening a question belong in the artifact. `CANONICAL-KINDS.md:318-337`; `EDGES.yaml:4-20`.
- `creates` is intentionally partial because a session record exists only when `close-session` ran; absence of that edge proves nothing. `ALLOWED-EDGES.yaml:49-52`; `EDGES.yaml:48-57`.

## Fields and valid values

- For the four scoped Evidence kinds, the required core frontmatter is `canonical_kind`, `title`, `description`, `evidence_for`, `created`, `last_updated`, and `tags`; `last_updated` starts as `created` and is to be bumped on content edits, but the document says no bump is enforced. `CANONICAL-KINDS.md:172-182`.
- The kind carrier is external to frontmatter: `research.md`, `discovery.md`, and `findings.md` determine kind by filename, whereas `sessions/` determines the session kind by path; `canonical_kind` is a mirror, and filename wins on conflict. `CANONICAL-KINDS.md:128-153`. This is explicitly scoped and already known not to generalize across the repository. `sessions/2026-07-13-1624-canonical-kinds-instance-contract.md:35-39,81-84`.
- Per-kind additions: `research` requires `question`; `findings` requires `question` and `outcome`; `discovery` may carry both; sessions carry neither. Research and findings share the dispatch question, and research deliberately has no outcome because findings provides the synthesis/outcome. `CANONICAL-KINDS.md:207-222`.
- `evidence_for` is a required list-valued target field only for Evidence kinds. Its valid domain is closed/default-deny in the cited model—`Definition`, `Constitution`, `Discipline`, `Decision`, `Spec`, and `Runtime contract`—and it grants no authority. `CANONICAL-KINDS.md:224-255`.
- In contrast, no `authority_state` or `status` is carried by these Evidence instances; open/closed is derived from question/outcome and supersession is an edge. `CANONICAL-KINDS.md:154-170`.

## Edge and endpoint rules

- For the four scoped kinds, `ALLOWED-EDGES.yaml` is the authority for permission and is default-deny: anything absent is forbidden; `EDGES.yaml` owns verb meanings. `CANONICAL-KINDS.md:296-305`; `ALLOWED-EDGES.yaml:1-14`.
- Allowed typed endpoints/cardinality are: `research --derives-from--> discovery` (0..1); `discovery --derives-from--> research` (0..N); `findings --derives-from--> research` (0..1); `discovery --contradicts--> discovery` (0..N, symmetric); and `session --creates|updates-->` any of the four Evidence kinds (0..N). `ALLOWED-EDGES.yaml:16-50`.
- No edge is mandatory. A research may start cold from a bare question (a field, not a node); a single-agent research dispatch can emit findings without a research artifact. `CANONICAL-KINDS.md:309-316`; `EDGES.yaml:74-95`.
- Inverse names are read directions rather than separately declarable edges. A question is always a field, not a graph node. `EDGES.yaml:17-20,125-129`.
- The type graph can cycle, but grounding instances must not derive from themselves directly or transitively; that constraint is expressly marked unenforced. `EDGES.yaml:171-183`; `CANONICAL-KINDS.md:347-358`.
- The categorical reading is only proposed: grounding and succession are proposed morphisms, while provenance, conflict, and navigational edges are not; hom-sets are not settled. `CANONICAL-KINDS.md:371-395`.

## Reusable versus local-only

**Portable interpretation (not a declared local schema).** Cyberalchemy can reuse the separation between: (1) an artifact-kind registry, (2) instance fields, (3) type-level lookup facts, (4) a typed allowed-edge matrix, and (5) separately owned validation/promotion. It can also reuse the distinction between provenance acts and epistemic claims, and record unenforced constraints explicitly. This is an interpretation from the separation and admission rules above, not an instruction to import their names, filenames, Tier-2 authority model, or closed vocabulary. `CANONICAL-KINDS.md:26-39,143-153,296-305,318-337`; `EDGES.yaml:171-183`.

**Domainspec-core-specific.** The exact four-kind scope; filename/path as kind carrier; Evidence/authority-kind rollup; `evidence_for` enum; named skills/routes; session-only provenance; and the particular edge matrix are all source-specific candidate contracts. `CANONICAL-KINDS.md:66-89,120-124,128-153,224-255,296-316`.

## Contradictions and gaps

- **Local naming conflict is already resolved by the owner constraint, not by import.** Local initial definitions fixes `artifact_kind` as the single kind field and says `node_type` is not a separate dimension. `research/research-lifecycle-definitions/research-initial-definitions.md:43-53`. The sibling review records a decision that `node_type` is the old name of the same field, not another axis. `findings.md:188-190`. But sibling source names the field `canonical_kind`; it does not authorize declaring `artifact_kind` values or a local schema.
- **Direct contradiction with current local conventions.** `vault/ontology-conventions.md` requires seven frontmatter dimensions including a closed `node_type` list and a human-readable Connections catalog. `vault/ontology-conventions.md:67-92,296-319,389-506`. That conflicts with the local owner’s one-field naming decision and with the sibling Evidence contract’s different, kind-specific fields and default-deny YAML edges. `research/research-lifecycle-definitions/research-initial-definitions.md:50-53`; `CANONICAL-KINDS.md:172-182,296-305`.
- **Do not overstate “every registered artifact has frontmatter and edges.”** The local requirement is only an investigation constraint: registered nodes need an identifiable generator and meaningful edges when supported, not invented. `research/research-lifecycle-definitions/research-initial-definitions.md:43-63`. The sibling contract says no edge is mandatory, scopes frontmatter to four kinds, and admits kinds without processes. `CANONICAL-KINDS.md:120-124,316,457-476`.
- **Authority/validation blocker.** The sibling review finds missing definition cards for its load-bearing terms, unresolved ownership routing, no kind enum enforcement, and recommends owner/gate action; it also says the proposed one-enumeration shape is not itself decided. `findings.md:88-105,155-165,219-240`. Thus its normative fragments are useful evidence, not settled authority for cyberalchemy-orchestrator.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [canonical-kinds-usage-scout.md](canonical-kinds-usage-scout.md) | `other` | Paired evidence from the empirical/usage lens; the precise relation type remains intentionally unclassified. |
