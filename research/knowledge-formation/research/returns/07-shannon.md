# Explorer return - Claude Shannon - repository operational map

## Boundary and evidence discipline

- **Snapshot inspected:** `master` at `48d5f7b830fc52773da8ce5191131ec2e05274f4`.
- **Worktree condition:** the repository was on that exact commit but dirty. All repository claims below were read from the committed snapshot with `git show`/`git grep`; dirty and untracked source artifacts were not used. The only worktree file read as a research boundary was `research/knowledge-formation/research-initial-definitions.md`.
- **Excluded:** other knowledge-formation dispatch artifacts and agent returns; external scholarship; the work essay as conceptual evidence; novelty claims.
- **Status vocabulary used here:**
  - `IMPLEMENTED` - executable code/schema with tests or an implementation receipt.
  - `IMPLEMENTED-PROTOCOL` - an invocable skill, validator, or repository convention exists, but it is not an integrated semantic runtime.
  - `PROPOSED` - a design/specification describes the object or transition but the operational path is absent or explicitly deferred.
  - `ASPIRATIONAL` - a desired product capability without an accepted operational contract.
  - `INTERPRETED` - this return's bounded reconstruction from cited native evidence.
  - `STALE/CONTESTED` or `RETRACTED` - the repository itself records reversal, retirement, or unresolved contradiction.

The repository has a strong implemented account of **admission, identity, immutable capture, scoped authority, lineage, replay, and currentness**. It does not have an implemented account of **accepting an understanding for governed reuse**. That boundary is the main result of this map.

## 1. Native map

| Requested notion | Native repository objects and operational use | Status | Owner / exact evidence / evidence type | Representational limit |
|---|---|---|---|---|
| **Information** | Raw or produced bytes become immutable artifacts with media type, schema, classification, content hash, retention/redaction/tombstone/authorization policies. Research submissions are encoded as a bounded artifact containing declared question, answer, references and problems; a claim exists only when supplied through a formalization and is marked `mode: inferred`. Supported host ingestion records exact repository reads, metadata-only searches/web acquisitions, and opaque shell evidence. | `IMPLEMENTED`, local pilot | `implementations/server/runtime/artifacts.py`, declarations `PreparedArtifact`, `ArtifactStore.prepare`, `finalize`, `get_authorized`; `implementations/server/runtime/provenance.py`, `ProvenanceService.append_research_submission`, especially record construction and artifact finalization; `docs/features/agent-provenance-telemetry/integration/stage-g/reference-scout-and-ingestion.md`, headings **Dispatch input ingestion** and **Boundary**. Code + implementation record. | The runtime stores attributable textual/byte records, not a general account of perception, learning, skill, memory, or understanding. Web/MCP capture is locator metadata only; shell is deliberately opaque. |
| **Assertion** | The implemented APT object is a `ResearchClaimExtraction`: a research-local proposition, explicitly not a global assertion or promoted-knowledge identity. In the convenience submission path, it is inferred only from a declared formalization's `claim`. A broader judgment-free `emit-assertion` layer (decision, premise, hypothesis, doubt, definition; always `proposed`, low veracity) is designed but explicitly unbuilt. | Narrow claim extraction `IMPLEMENTED`; general assertion capture `PROPOSED` | `docs/features/agent-provenance-telemetry/specs/domain.md`, heading **ResearchClaimExtraction**, especially identity/lifecycle text; `implementations/server/runtime/provenance.py`, `append_research_submission`, records at `mode: inferred`, `type: claim`, `derivation: formalization-declared-claim`; `docs/discovery/agent-assertion-capture/README.md`, opening status, headings **C1 - Emitter as stenographer**, **3.1 Emission record shape**, and **Review findings & open design gaps**. In-review spec + code + draft discovery. | No implemented general assertion identity spans decisions, premises, definitions, claims, and doubts. Assertions made outside the formalization path are not promoted into a common claim graph. |
| **Evidence** | Evidence is represented as immutable artifact references/digests, exact byte selectors, source refs, host observations, accepted event/receipt references, reference-use classifications, explicit problem evidence refs, and inventory evidence cards. Evidence-card `authority_level` identifies source standing; cards and EvidenceSets remain non-authoritative candidates. APT keeps `mentioned`, `cited`, and `claimed_consulted` distinct; claimed consultation is not host access evidence. | Runtime evidence spine `IMPLEMENTED`; card/set authoring and validation `IMPLEMENTED-PROTOCOL`; populated inventory `ABSENT` | `docs/features/agent-provenance-telemetry/specs/domain.md`, headings **ResearchReferenceUse**, **ReferenceCheck**, **ExtractionProvenance**, **ArtifactReference**, enums **ReferenceUseKind** and **ReferenceCheckResult**; `implementations/server/runtime/provenance.py`, `_validate_bound_batch` and `append_research_submission`; `.claude/skills/inventory/templates/evidence-card.schema.yml`, schema `inventory.evidence-card.v0.2`; `.claude/skills/inventory/templates/evidence-set.schema.yml`, schema `inventory.evidence-set.v0.1`; `.arcanum/inventory/index.json` (`entries: []`) and `.arcanum/inventory/index.md`, heading **Open Gaps**. Spec/code/schema/empty installed instance. | Evidence can support or contest a statement but does not itself establish acceptance. The implemented submission path does not implement the full specified `ReferenceCheck`, reference-to-claim relation, or multi-assessor disposition surface. |
| **Review** | The review skill defines review as verified change requests over existing artifacts. Findings must quote the target artifact, attackers cannot self-verify, refuted findings are dropped, and a final approver accepts the change-request list. Review intentionally persists no attacker/verifier transcript; the quotation is treated as the proof. APT separately specifies ReferenceChecks and policy/assessor-keyed disposition projections, preserving disagreement and forbidding a guessed singular disposition. | Review workflow `IMPLEMENTED-PROTOCOL`; APT dispositions/reference checks largely `PROPOSED` | `.claude/skills/review/SKILL.md`, headings **What you produce**, **Gate it**, **Write the report**, **Close**, and the explicit **No transcript** ruling; `docs/features/agent-provenance-telemetry/specs/states.md`, heading **Disposition Read Projections**; `docs/features/agent-provenance-telemetry/specs/domain.md`, headings **ReferenceCheck** and **Disposition and Assessment Payload Variants**. Invocable skill + in-review spec. | There is no implemented stable link `review -> reviewed claim/fact version -> criteria/policy -> acceptance decision`. Deliberative provenance is deliberately lost in review artifacts, so later consumers can inspect conclusions and quotations but cannot reconstruct rejected findings or independence from the persisted record. |
| **Acceptance** | The word has at least four non-equivalent native uses: (1) ACI accepts an event/command into the durable journal; (2) a human confirms/authorizes a dispatch; (3) a review final approver accepts a change-request list and resolves the review; (4) the proposed knowledge model accepts understanding for reuse. Inventory also has promotion states and external governed refs. | (1)-(3) `IMPLEMENTED` or `IMPLEMENTED-PROTOCOL`; (4) `PROPOSED/ASPIRATIONAL` | `implementations/tests/runtime/test_apt_projector.py`, test `test_authoritative_receipt_survives_projector_failure_and_catches_up` (`status == accepted` while projection is pending); `docs/features/agent-provenance-telemetry/specs/rules.md`, **APT-R2 - Idempotent Append** (`Durable ACI acceptance precedes acknowledgment`); `.claude/skills/review/SKILL.md`, **Close**; `plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md`, frontmatter `authority: proposal-only`, headings **Um segundo olhar**, **Continuidade do conhecimento**, **Escopo e estado atual**. Test/spec/skill/proposal. | There is no implemented `KnowledgeAcceptance` record carrying accepter, governing authority/policy, claim/understanding version, evidence set, review, scope, effective time, state, and revocation/supersession links. Journal acceptance must not be read as truth or reuse permission. |
| **Authority** | Runtime authority is capability-bound to principal, action, phase, exact context, expiry, and revocation. Inputs may not self-supply authority fields. Store ownership is split: ACI owns journal acceptance and Session-Dispatch links; APT owns captures/facts/projections; ArtifactStore owns bytes; the YAML appender owns the compatibility ledger; Inventory owns read models; Ontology Vault owns governed meaning/relations/confidence/promotion; Definitions Governance owns canonical definitions; humans/repository owners decide consequential promotion/confirmation. | Runtime capability boundary `IMPLEMENTED`; cross-owner governance `IMPLEMENTED-PROTOCOL`/manual | `implementations/server/runtime/capabilities.py`, `CapabilityManager.issue`, `resolve`, `reject_authority_fields`, `revoke`, `consume`; `implementations/server/runtime/migrations/003_profile_capability.sql`, table `capabilities`; `docs/features/agent-provenance-telemetry/specs/rules.md`, **APT-R1 - Single Join Authority** and **APT-R8 - Telemetry Non-Authority**; `.claude/skills/inventory/SKILL.md`, `<authority-rule>`; `.claude/skills/ontology-vault/SKILL.md`, steps 25, 36-38 and quality bar; `.claude/skills/definitions-governance/SKILL.md`, `<project-authority-boundary>` and `<authority-rule>`. Code/schema/spec/skills. | Authority for accepting reusable understanding is named as external but has no shared executable decision contract. Multiple policy owners can coexist in specified APT assessments, but no bridge turns one into knowledge authority. |
| **Provenance** | APT binds Session -> Dispatch -> ResearchCapture -> extracted facts -> exact artifact byte selectors. Producer, extractor, method, timestamp, source capture digest, dispatch snapshot, origin refs, event IDs, journal offsets, and artifact hashes are preserved. Stage G adds exact file-read ingestion and Reference Scout lineage. Projections are reconstructible and non-authoritative. | `IMPLEMENTED`, local pilot | `docs/features/agent-provenance-telemetry/specs/domain.md`, headings **ResearchCapture**, **FactEnvelope**, **ExtractionProvenance**, and cross-entity invariants APT-DOM-1/4/19-22; `implementations/server/runtime/provenance.py`, `_validate_bound_batch`, `get_research`, `get_answer`; migrations `004_apt_projection.sql`, `005_apt_granular_projection.sql`, `006_apt_projector_state.sql`; `implementations/tests/runtime/test_apt_stage_b.py`, test `test_capture_query_protected_answer_and_restart`; Stage G implementation record. Spec/code/schema/test/receipt. | Provenance records production, declaration, delivery, and some observed access. It cannot establish that a person or agent understood a source, that a citation supports a claim, or that an accepted understanding remains usable. Coverage is instrument-dependent and partial. |
| **Version** | Versions occur as schema refs, protocol profile ID/version/digest, document versions, immutable fact/capture versions, predecessor links, aggregate versions, and projection reducer versions. Corrections append rather than mutate. | `IMPLEMENTED` for runtime/schema versioning; document versioning `IMPLEMENTED-PROTOCOL` | `docs/features/agent-provenance-telemetry/specs/domain.md`, **ResearchCapture** lifecycle and **FactEnvelope**; `implementations/server/runtime/migrations/004_apt_projection.sql`, `supersedes_*` and current-head indexes; `implementations/server/runtime/migrations/006_apt_projector_state.sql`, `projector_version`; `implementations/server/runtime/migrations/003_profile_capability.sql`, `protocol_profiles(profile_id, profile_version, ...digest)`; `vault/ontology-conventions.md`, frontmatter catalog and heading **status - Maturity Level**. Schema/spec/convention. | There is no composite version of “accepted understanding under conditions.” A document version, capture version, schema version, and policy version are not joined into one reuse decision. |
| **Scope** | Scope is enforced in capabilities and query bindings through exact Session, Dispatch, contribution/capture, target, action, and phase. Formalization candidates have a free-text `scope`. Evidence cards have source selectors and authority levels; dispatch snapshots pin declared scope. | Runtime scope `IMPLEMENTED`; semantic/reuse scope `PROPOSED` or untyped text | `implementations/server/runtime/provenance.py`, capability scope checks in `append_research_submission`, `get_research`, `get_dispatch`, `get_answer`; `docs/features/agent-provenance-telemetry/specs/domain.md`, **FormalizationCandidate** field `scope`; `.claude/skills/inventory/templates/evidence-card.schema.yml`, `source_refs`, `authority_level`; `docs/features/agent-provenance-telemetry/specs/queries.md`, **DispatchScopeProjection** and AgentReferenceLineage query boundaries. Code/spec/schema. | Runtime authorization scope says who may perform an operation; it does not type the domain in which a conclusion may be relied on. `FormalizationCandidate.scope` is text, not a composable or enforceable reuse boundary. |
| **State** | State is plural and non-unified: capture status (`captured|partial|missing`) is immutable; current/superseded is a derived head projection; projection status is `current|pending`; capabilities become revoked; documents mature `draft -> ... -> evergreen`; evidence cards have promotion status; reviews resolve with KEEP/FIX outputs. | Each local state system ranges from `IMPLEMENTED` to `IMPLEMENTED-PROTOCOL`; no unified epistemic state | `docs/features/agent-provenance-telemetry/specs/states.md`, **Research Capture Currentness**; `implementations/server/runtime/projections.py`, capture/fact predecessor and current-head reducers; `implementations/server/runtime/capabilities.py`, `revoke`/`consume`; `vault/ontology-conventions.md`, **status - Maturity Level**; evidence-card/set schemas; review skill **Close**. Code/spec/schema/convention. | The labels cannot be safely ordered into one ladder. `current`, `active`, `supported`, `reviewed`, `promoted`, `accepted`, and `resolved` answer different questions. |
| **Supersession** | APT implements append-only capture and fact chains: a replacement names the current predecessor; prior bytes/status remain; currentness is derived; stale/cross-chain/self predecessors fail. Inventory cards/sets admit `superseded`; document conventions tell readers to supersede discoveries/plans, but the document `status` enum has no `superseded` value. | APT chain `IMPLEMENTED`; inventory status `IMPLEMENTED-PROTOCOL`; document supersession `INTERPRETED/manual` | `docs/features/agent-provenance-telemetry/specs/rules.md`, **APT-R5 - Capture Supersession**; `docs/features/agent-provenance-telemetry/specs/states.md`, **Research Capture Currentness**; migrations `004_apt_projection.sql` and `005_apt_granular_projection.sql`; inventory schemas; `vault/ontology-conventions.md`, **node_type - Epistemic Role** challenge responses and the closed `status` catalog. Spec/schema/convention. | There is no cross-surface supersession edge from a reviewed/accepted understanding to its replacement. A capture can be superseded while any downstream prose, review, or decision continues to cite the old version without machine-detectable invalidation. |
| **Revocation** | Capability revocation is implemented: a revoked/consumed token no longer resolves. The architectural proposal says accepted knowledge may later be revoked or restricted while preserving history. The knowledge/vault/document models do not provide an implemented revocation record/state. | Authorization revocation `IMPLEMENTED`; knowledge revocation `ASPIRATIONAL` | `implementations/server/runtime/capabilities.py`, `CapabilityManager.revoke` and `consume`; migration `003_profile_capability.sql`, `revoked_at`; Stage-D `ACCEPTANCE-MATRIX.md`, probes **T-LCB-REVOKE-01..03**; proposal-only `work-and-knowledge-system-overview.md`, **Continuidade do conhecimento** and **Escopo e estado atual**. Code/schema/acceptance tests/proposal. | The model cannot say “understanding U, accepted by O for scope S, is revoked from time T for reason R, except in sub-scope S1, and replaced by U2,” nor enumerate affected consumers. `refuted`, `rejected`, `superseded`, and capability `revoked` are not substitutes. |
| **Reusable understanding** | Inventory is designed as a compiled reusable knowledge layer with source-backed evidence cards, selector-level lookup, lint, EvidenceSets, and downstream handoffs. Ontology Vault can recommend promotion/demotion; Definitions Governance maintains canonical terms. The installed repository inventory has zero entries and explicitly says every lookup is a gap. The architectural definition of knowledge as understanding accepted under provenance/evidence/review/scope/version/state is proposal-only. | Infrastructure `IMPLEMENTED-PROTOCOL`; instance empty; end-to-end reusable understanding `ASPIRATIONAL` | `.claude/skills/inventory/README.md`, opening and headings on evidence cards/EvidenceSets; `.arcanum/inventory/README.md`; `.arcanum/inventory/index.json`; `.arcanum/inventory/index.md`, **Open Gaps**; `.claude/skills/ontology-vault/SKILL.md`, **Review Premises And Confidence**; `.claude/skills/definitions-governance/SKILL.md`, authority rule; proposal-only overview cited above. Skill/package/proposal. | The repository cannot yet answer a reusable-knowledge query from an operational source of truth. It can retrieve records and lineage, but not decide or prove reuse permission. |

## 2. Repository protocol as it actually exists

This is a protocol reconstruction, not a claim that one end-to-end workflow is implemented.

| Step | Native transition | Standing | Exact owner and evidence |
|---|---|---|---|
| 1. Capture bytes/records | Finalize immutable artifact; bind hash, classification, retention, redaction, tombstone and authorization policy. | `IMPLEMENTED` | ArtifactStore: `implementations/server/runtime/artifacts.py`; table `artifacts` from `migrations/002_artifact_store.sql`. |
| 2. Admit an operation | Resolve exact scoped capability; validate closed input; atomically append journal events and receipt before acknowledgment. | `IMPLEMENTED` | ACI runtime: `capabilities.py`; APT-R2; runtime tests including `test_apt_stage_b.py`. |
| 3. Attribute the capture | Link one Session to Dispatch, pin dispatch snapshot, producer, contribution, artifact and capture digest. | `IMPLEMENTED` | ACI owns Session/Dispatch link; APT owns capture: APT-R1 and `ProvenanceService.append_research_submission`. |
| 4. Extract local facts | Materialize question, answer, references, problems, optional claim/formalization with exact byte selectors and extraction provenance. | `IMPLEMENTED`, bounded variant set | APT: `_validate_bound_batch`; tables in `005_apt_granular_projection.sql`. |
| 5. Derive current views | Replay verified event groups; refuse reads when projection lags; derive capture/fact head without changing history. | `IMPLEMENTED` | Projection manager and `test_authoritative_receipt_survives_projector_failure_and_catches_up`. |
| 6. Assemble reusable evidence | Author evidence cards/EvidenceSets with selectors, authority level, promotion owner, residue, inclusions/exclusions. | `IMPLEMENTED-PROTOCOL`, unused instance | Inventory schemas/validators; `.arcanum/inventory/index.json` has no entries. |
| 7. Review | Attack an artifact, verify findings against quotations, synthesize `review.md`, final approver accepts change requests. | `IMPLEMENTED-PROTOCOL` | `review/SKILL.md`; no generic runtime entity binds this output to APT claims. |
| 8. Promote governed meaning | Downstream owner evaluates evidence/confidence and creates governed meaning or canonical definition. | `IMPLEMENTED-PROTOCOL`, manual/external | Ontology Vault and Definitions Governance skills. Inventory explicitly cannot promote. |
| 9. Accept for reusable understanding | Record acceptance together with provenance, evidence, review, scope, version and state. | `PROPOSED` | `work-and-knowledge-system-overview.md`, proposal-only. No source declaration, schema, migration, service method or populated store implements it. |
| 10. Supersede/restrict/revoke reusable understanding | Append a successor or revocation while preserving earlier history and narrowing future use. | Capture supersession `IMPLEMENTED`; reusable-understanding lifecycle `ASPIRATIONAL` | APT-R5 implements capture correction only. The overview proposes knowledge supersession/revocation; no governing runtime object exists. |

The implemented pipeline therefore ends at **attributable research-local records and projections**. Steps 6-8 are repository operating practices; steps 9-10 are not operational.

## 3. Owner and source-type matrix

| Owner surface | Owns | Explicitly does not own | Source type / authority standing |
|---|---|---|---|
| ACI runtime | Journal admission, receipts, Sessions, Session-Dispatch link, capabilities, scoped effects | Truth, knowledge, APT semantic meaning | Implemented code + SQLite contracts + tests. |
| ArtifactStore | Immutable bytes and policy-bound artifact references | Meaning of the bytes or permission to rely on a proposition | Implemented code/schema/tests. |
| APT | Research captures, research-local facts, lineage and replay projections | Dispatch authority, artifact bytes, global assertions, ontology/knowledge acceptance | In-review spec with a substantial implemented local-pilot subset. Domain **External References, Not APT Concepts** explicitly places knowledge/assertion/ontology acceptance outside APT. |
| YAML dispatch appender | Confirmed legacy opening/close rows | Research semantics or knowledge | Implemented compatibility authority, with known historic bypass evidence and cutover conflict. |
| Inventory | Candidate source-backed cards, sets, indexes, lint and handoff projections | Governed meaning, canonical definitions, terminal promotion | Invocable skill + schema validators; installed instance empty. |
| Ontology Vault | Governed meaning, relations, confidence review and promotion recommendations | Source mutation or promotion without owner approval | Invocable manual governance skill; outputs are evidence/recommendations unless owner acts. |
| Definitions Governance | Canonical definitions in configured `definitions/` authority | Runtime state and narrative definitions outside the canonical store | Invocable skill/convention. Current `definitions/DEFINITIONS.md` contains no entries for information, assertion, evidence, review, acceptance, knowledge, or understanding. |
| Review workflow | Verified change-request report and dispatch resolution | Applying fixes; global truth or knowledge promotion | Invocable skill; human/dedicated approver gate. |
| Repository owner/human gate | Confirmation, consequential choices, owner promotion | Not automatically the producer, verifier, or runtime writer | Decision/session/dispatch records; authority is contextual and often manual. |
| Vault frontmatter conventions | Document role, maturity, veracity and conviction | Executable acceptance/revocation of claims | Active convention document, but state is frontmatter/prose rather than an integrated runtime. |

## 4. Gaps and inconsistencies

### G1 - No reusable-understanding aggregate

There is no schema or service whose identity is an accepted understanding and whose required fields bind:

`content/fact version + provenance + evidence set + review result + accepting actor + authority/policy + scope + policy/version + effective state/time + supersession/revocation`.

Evidence: APT Domain **External References, Not APT Concepts** assigns knowledge/assertion/ontology acceptance to “Future external governance”; the installed Inventory is empty and non-authoritative; the overview that names the composite is `authority: proposal-only`. This is an absence claim bounded to the inspected snapshot and supported by the schema/code search, not a novelty claim.

### G2 - “Accepted” is overloaded across layers

`accepted_event_id` and command receipt `status: accepted` mean that a closed command was durably admitted. Review acceptance means a final approver accepted a change-request report. Dispatch confirmation means execution authorization. Proposed knowledge acceptance means permission for bounded reuse. No native type prevents a reader from conflating them.

Evidence: APT-R2; projector failure test where the authoritative receipt is accepted while the projection is absent; review skill **Close**; proposal-only overview **Continuidade do conhecimento**.

### G3 - Review provenance is intentionally incomplete

Review preserves the target quotation, conclusion, coverage summary, and accepted change requests, but explicitly discards attacker/verifier returns. This is an owner-accepted cost, not an accidental omission. It conflicts with any later requirement to reconstruct independence, rejected alternatives, or why a finding was refuted.

Evidence: `.claude/skills/review/SKILL.md`, warning **No transcript. At all** and the recorded owner ruling. The same skill states historical `attacks.md`/`findings.md` remain as history, proving the protocol changed.

### G4 - Document maturity cannot encode negative lifecycle outcomes

`vault/ontology-conventions.md` provides `draft|exploratory|active|consolidated|evergreen`; it says discoveries/plans may be superseded and evergreen leaves only by documented refutation plus formal review. Yet `superseded`, `refuted`, `retired`, `restricted`, and `revoked` are not document status values. Inventory has some of these statuses; APT has different research-local dispositions; none composes with document status.

### G5 - Supersession is local, not transitive

APT correctly preserves immutable predecessor chains for captures/facts, but citations, reviews, decisions, inventory cards, and narrative claims are not invalidated when their source capture becomes non-head. `input_now_superseded` is query-time display state for synthesis pins, not a dependency invalidation protocol.

Evidence: APT `ResearchCapture` lifecycle, APT-R5, and **Research Capture Currentness**.

### G6 - Scope is operationally exact but epistemically weak

Capabilities strongly constrain runtime operations. Formalization `scope` and proposed knowledge scope are semantic boundaries, but the former is free text and the latter has no schema. No operation checks whether a future application falls within the scope in which a claim was accepted.

### G7 - Source consultation is not understanding or support

The model correctly separates recommendation, delivery, access observation, declared use, claim relation and claim-support check. However, only part of that chain is implemented. Even a complete chain would show use/support evidence, not learning or understanding.

Evidence: APT-DOM-19..22; Stage G ingestion coverage table; `ReferenceUseKind.claimed_consulted` explicitly says it is not host access evidence.

### G8 - Canonical definition authority has no operational knowledge terms

Definitions Governance says only configured canonical definition sources may define normative semantics. `definitions/DEFINITIONS.md` currently maps system primitives and category-theory parallels but not the requested epistemic vocabulary. The proposal-only overview therefore cannot quietly become the canonical definition of knowledge.

### G9 - Spec/implementation boundary is easy to overread

APT specs define ReferenceChecks, reference-claim relations, policy-keyed dispositions, independent assessments, formalization governance refs, and other extensions. The convenience implementation accepts a smaller closed union: question, answer, reference use, problem, inferred claim, formalization. The detailed spec has `specAuthoringGate: in-review` and many rules say “planned.” Claims about implemented semantic review must use code/tests, not the complete spec.

### G10 - The repository records stale-state conflict but does not resolve it

`vault/audit/ledger-enum-drift-finding.md`, heading **Repair path (open)**, calls enum drift the keystone next step for Phase 2. `sessions/2026-07-22-1315-phase2-confirm-handoff.md`, **Contradictions**, says Phase 2 shipped after re-scoping the drift to a veracity label. Root `README.md`, **Open questions**, concludes either its own framing or the audit is stale. `.craft/ledger.yml`, decision `DEC-CUTOVER-GATE-001`, keeps the conflict active and production cutover blocked. The contradiction is visible but not superseded in place.

## 5. Tensions and translation failures

| Translation attempted | Why it fails | Native evidence |
|---|---|---|
| `journal accepted` -> `claim accepted` | Admission proves transactional validity, not semantic warrant. | APT-R2; projector-failure test. |
| `claim current` -> `claim true/currently usable` | Current means head of an immutable chain at an offset. | APT states **Research Capture Currentness**. |
| `reference delivered` -> `source consulted` | Delivery, access, declared use, relation and support check are independent axes. | APT-DOM-19..22; Stage G. |
| `review resolved` -> `artifact correct` | A FIX review may resolve when the change-request list is accepted; fixes remain future acts. | Review skill **Close**. |
| `formalization reviewed` -> `canonical` | The APT disposition is research-local; external governance must act. | Domain **FormalizationCandidate** and **FormalizationDisposition**. |
| `inventory promoted` -> `knowledge accepted` | Inventory is a non-authority read model; `promoted` requires a real external `governed_ref`. | Inventory authority rule and evidence-card schema. |
| `document active/evergreen` -> `accepted understanding` | Document maturity is not an acceptance record and has no scoped revocation mechanism. | Ontology conventions **status**. |
| `capability revoked` -> `knowledge revoked` | One retires action authority; the other would withdraw reuse permission for a proposition/understanding. | CapabilityManager vs proposal-only overview. |
| `provenance complete` -> `understanding preserved` | Exact lineage can preserve bytes, attribution and use evidence while losing interpretation, skill, memory and practice. | Implemented APT boundary plus `research/knowledge-formation/research-initial-definitions.md`, **Known Gaps**. |

## 6. Coherence test

### Test question

Given one proposition `C` captured in research, can the repository answer, from a single operationally authoritative path:

> “May consumer `P` rely on version `v(C)` now, for domain scope `S`, because owner `O` accepted it under policy/version `V` after review `R` using evidence set `E`; and has that acceptance been superseded, restricted, or revoked?”

### Result: FAIL at the reuse boundary

| Required fact | Can snapshot represent it? | Evidence |
|---|---|---|
| Exact captured bytes and proposition-local extraction | Yes, bounded to APT capture/formalization path | ProvenanceService, ArtifactStore, APT projection tables. |
| Session, Dispatch, producer/extractor and source lineage | Yes, within instrumented coverage | APT domain/rules; Stage G. |
| Evidence references and declared use | Yes, partially; support checks are not the same as uses | APT reference objects; implementation subset caveat. |
| Independent review result linked to exact claim version | No integrated record | Review produces artifact-level `review.md`; APT dispositions are specified but not the knowledge bridge. |
| Owner acceptance under a named knowledge policy/version | No | Future external governance only. |
| Enforceable semantic reuse scope | No | Runtime scope exists; formalization scope is text. |
| Current acceptance after supersession/restriction/revocation | No | Capture heads and capability revocation do not represent knowledge lifecycle. |

The strongest supported conclusion is therefore narrow: **the repository can establish where a bounded research record came from, what exact bytes and declared structures were admitted, and which version is current in that capture chain; it cannot establish that the record is reusable understanding.**

## 7. Strongest conflict

The strongest conflict is between the proposal's definition of reusable knowledge and the implemented runtime's meaning of acceptance.

- Proposal: `work-and-knowledge-system-overview.md`, **Um segundo olhar** and **Continuidade do conhecimento**, calls knowledge understanding accepted under provenance, evidence, review, scope, version and state, later supersedable/revocable/restrictable. Frontmatter says `authority: proposal-only`; **Escopo e estado atual** says the knowledge system remains proposed.
- Runtime: ACI/APT accepts closed events and commands, projects research-local facts, and explicitly refuses to infer knowledge/ontology acceptance. APT Domain **External References, Not APT Concepts** names that acceptance as future external governance.

Any synthesis that labels accepted ACI events “knowledge” violates both sources: it inflates transactional acceptance into epistemic acceptance and erases the proposal's missing conditions.

## 8. Reversal evidence

1. **Protocol rule retired:** `.claude/skills/review/SKILL.md`, warning block under the operating guide, records that review previously persisted `attacks.md` + `findings.md`; after the 2026-07-13 owner ruling it deliberately persists no transcript. Historical files remain rather than being reinterpreted. Status: `RETRACTED` old protocol, replacement active.
2. **Cutover blocker re-scoped but not resolved:** enum-drift audit says “keystone next step for Phase 2”; the 2026-07-22 session says it blocks a veracity label rather than operation; README and `DEC-CUTOVER-GATE-001` preserve the unresolved contradiction. Status: `STALE/CONTESTED`, not silently reversed.
3. **Machine supersession works locally:** APT-R5 and projection migrations make replacement append a successor and derive prior capture/fact as non-current without mutating history. Status: `IMPLEMENTED`, but only for APT chains.

Together these show that the repository knows three different ways to handle reversal - retire a protocol in prose, preserve an unresolved conflict in governance records, and append a machine successor - but has no shared reversal object across them.

## 9. Rejected synthesis move

**Rejected:** construct one epistemic ladder such as

`captured -> accepted -> current -> supported -> reviewed -> promoted -> active -> knowledge`.

This move is invalid because every term belongs to a different owner and answers a different predicate:

- `captured`: whether a raw witness exists;
- `accepted`: whether ACI durably admitted a command/event;
- `current`: which immutable chain member is the replay head;
- `supported/contested/refuted`: research-local assessment under a policy;
- `reviewed`: a formalization was examined without becoming canonical;
- `promoted`: an Inventory candidate points to a downstream governed artifact;
- `active/evergreen`: document maturity;
- `resolved`: a review dispatch delivered an accepted change-request list.

Collapsing these labels would manufacture an authority transition that no owner grants. The repository's native separation should be retained until a real acceptance aggregate and owner contract exist.

## 10. Return decision

**Decision: needs review, with a negative operational verdict on end-to-end reusable understanding.** The provenance and authority substrate is substantial and test-backed, but the operational model stops before governed acceptance, semantic reuse scope, and knowledge revocation. The appropriate next inspection target is not another vocabulary synthesis; it is the missing cross-owner acceptance contract, reviewed against the rejected-ladder failure above. This is a gap classification, not a claim of novelty.
