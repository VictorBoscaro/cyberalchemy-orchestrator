---
feature: skill-control-center
version: 0.1.0
status: draft
updatedAt: 2026-07-25
docType: glossary
owners:
  - "@VictorBoscaro"
---

# Glossary: Skill & Dispatch Control Center

This glossary explains Phase 1 language. Formal behavior remains in [SPEC.md](SPEC.md), the
[discovery](discovery/control-center.md), and linked aspect documents.

## Feature Language

| Term | Meaning in this feature | Related Concepts |
|---|---|---|
| Authoritative | Able to change the owned source of truth; Phase 1 has no such configuration route. | [`ChangeProposal`](discovery/control-center.md#changeproposal), [`DraftPort`](SPEC.md#safe-preparation) |
| Draft-only | A proposal can be saved, diffed and checked, but cannot be applied or called applied. | [`ChangeProposal`](discovery/control-center.md#changeproposal), [`DraftLifecycle`](SPEC.md#safe-preparation) |
| Evidence | Proof supporting one claim in one scope/window, not a visual confidence guess. | [`EvidenceClassSet`](discovery/control-center.md#evidenceclassset), [`EvidenceAnswer`](SPEC.md#evidence-inspection) |
| Freshness | Whether each expected source was ingested within its named SLA; independent of proof strength. | [`FreshnessState`](discovery/control-center.md#freshnessstate) |
| Coverage | Which expected sources and time intervals are actually represented in an answer. | [`EvidenceCompleteness`](discovery/control-center.md#evidencecompleteness), [`EvidenceAnswer`](SPEC.md#evidence-inspection) |
| Strong relation | An `explicit_path` source reference with exact evidence location and snapshot. | [`SkillRelation`](discovery/control-center.md#skillrelation) |
| Weak mention | A `named_reference` textual mention; never a call or dependency claim. | [`SkillRelation`](discovery/control-center.md#skillrelation) |
| Focal topology | A bounded neighborhood opened only by an explicit action for one topology model. | [`TopologyModel`](discovery/control-center.md#topologymodel), [`GetTopology`](SPEC.md#catalog-and-topology-inspection) |
| Semantic mirror | A list/table alternative that exposes the same topology identity, selection and answer as the visual graph. | [`TopologyWorkspace`](SPEC.md#catalog-and-topology-inspection) |
| Route unavailable | Honest Phase 1 state for an absent authoritative configuration command. | [`DraftInspector`](SPEC.md#safe-preparation) |
| Variant equivalence | A, B and C differ structurally but keep the same semantics, fixtures, actions, states and test IDs. | [`VariantContract`](discovery/control-center.md#variantcontract) |

## Terms

| Term | Concept ID | Type | Definition | Source |
|---|---|---|---|---|
| ControlCenterWorkspace | `ui.skill-control-center.ControlCenterWorkspace` | Page | The task-led operator page that presents attention and scope before relational tools. | [Task-led landing](discovery/control-center.md#task-led-landing) |
| AttentionProjection | `skill-control-center.AttentionProjection` | Value Object | A presentation-neutral query output of prioritized attention facts and safe next actions. | [Operational orientation](SPEC.md#operational-orientation) |
| AttentionQueue | `ui.skill-control-center.AttentionQueue` | View Model | The UI-shaped attention list with scope, proof, freshness and next-action labels. | [Operational orientation](SPEC.md#operational-orientation) |
| StableSelection | `skill-control-center.StableSelection` | Value Object | The URL-restorable selection tuple whose update does not itself navigate. | [Discovery](discovery/control-center.md#stableselection) |
| TopologyModel | `skill-control-center.TopologyModel` | Enum / Type | The closed selector for skill relations, Dispatch lineage or intra-Dispatch topology. | [Discovery](discovery/control-center.md#topologymodel) |
| SkillRelation | `skill-control-center.SkillRelation` | Value Object | A directed, source-derived skill relation with typed evidence and snapshot identity. | [Discovery](discovery/control-center.md#skillrelation) |
| DispatchLineageProjection | `skill-control-center.DispatchLineageProjection` | Value Object | Presentation-neutral ancestry derived only from `parent_dispatch_id`. | [SPEC](SPEC.md#domain-concepts) |
| DispatchLineage | `ui.skill-control-center.DispatchLineage` | View Model | The UI-shaped ancestor/descendant view that retains unresolved-parent and source facts. | [Discovery](discovery/control-center.md#dispatchlineage) |
| IntraDispatchProjection | `skill-control-center.IntraDispatchProjection` | Value Object | Presentation-neutral groups and typed connections for one Dispatch. | [SPEC](SPEC.md#domain-concepts) |
| IntraDispatchTopology | `ui.skill-control-center.IntraDispatchTopology` | View Model | The UI-shaped group topology scoped by one Dispatch ID. | [Discovery](discovery/control-center.md#intradispatchtopology) |
| EvidenceClassSet | `skill-control-center.EvidenceClassSet` | Value Object | A positive proof-class subset or the singleton unknown/unavailable class at one claim grain. | [Discovery](discovery/control-center.md#evidenceclassset) |
| EvidenceCompleteness | `skill-control-center.EvidenceCompleteness` | Enum / Type | The independent complete, partial or unavailable coverage qualifier. | [Discovery](discovery/control-center.md#evidencecompleteness) |
| FreshnessState | `skill-control-center.FreshnessState` | Enum / Type | The fresh, stale or unknown reduction across expected source freshness records. | [Discovery](discovery/control-center.md#freshnessstate) |
| ObservationEnvelope | `skill-control-center.ObservationEnvelope` | Event | The accepted usage observation carrying distinct delivery, invocation and attempt identities. | [Discovery](discovery/control-center.md#observationenvelope) |
| EvidenceAnswer | `skill-control-center.EvidenceAnswer` | Value Object | The claim/scope/window result containing proof, completeness, freshness and source facts. | [Evidence inspection](SPEC.md#evidence-inspection) |
| EvidenceResponse | `skill-control-center.EvidenceResponse` | Value Object | The transport-safe evidence answer containing counts, diagnostics, qualifiers and source facts. | [Evidence inspection](SPEC.md#evidence-inspection) |
| EvidenceRules | `skill-control-center.EvidenceRules` | Rule | The executable constraints that prevent partial or unknown proof from becoming exhaustive fact. | [SPEC](SPEC.md#formal-rules-and-invariants) |
| PathResult | `skill-control-center.PathResult` | Value Object | A deterministic set of bounded paths or one typed non-success state. | [Discovery](discovery/control-center.md#6-deterministic-path-query-contract) |
| ChangeProposal | `skill-control-center.ChangeProposal` | Entity | A versioned local proposal with stable target, base, diff, origins and validation preview. | [Discovery](discovery/control-center.md#changeproposal) |
| WorkspaceNavigation | `skill-control-center.WorkspaceNavigation` | State Machine | The explicit selection, detail, topology, back and deep-link lifecycle. | [Explicit transitions](discovery/control-center.md#explicit-transitions) |
| DraftLifecycle | `skill-control-center.DraftLifecycle` | State Machine | The local clean, dirty, saved, validating, valid, invalid and save-failed lifecycle. | [Safe preparation](SPEC.md#safe-preparation) |
| ControlCenterReadAPI | `skill-control-center.ControlCenterReadAPI` | Interface | The versioned read-only transport for Phase 1 queries and typed failures. | [SPEC](SPEC.md#feature-concept-graph) |
| LocalPreferencePort | `skill-control-center.LocalPreferencePort` | Interface | The user-local persistence boundary for filters, layout, pins and saved views. | [SPEC](SPEC.md#feature-concept-graph) |
| DraftPort | `skill-control-center.DraftPort` | Interface | The local boundary that saves and validates proposals without authority effects. | [SPEC](SPEC.md#feature-concept-graph) |
| VariantContract | `skill-control-center.VariantContract` | Interface | The shared semantic, fixture, state, action and test-ID contract for A, B and C. | [Discovery](discovery/control-center.md#variantcontract) |
| ValidationEvidenceBundle | `skill-control-center.ValidationEvidenceBundle` | Value Object | The revision-bound package of test, accessibility, performance and screenshot evidence. | [Discovery](discovery/control-center.md#validationevidencebundle) |
| GetAttentionQueue | `skill-control-center.GetAttentionQueue` | Query | Reads prioritized attention items for one visible scope. | [SPEC](SPEC.md#operational-orientation) |
| SearchCatalog | `skill-control-center.SearchCatalog` | Query | Searches scoped skills and Dispatches while disclosing matched fields. | [SPEC](SPEC.md#catalog-and-topology-inspection) |
| GetObjectDetail | `skill-control-center.GetObjectDetail` | Query | Reads one selected object with provenance, qualifiers and safe actions. | [SPEC](SPEC.md#catalog-and-topology-inspection) |
| GetTopology | `skill-control-center.GetTopology` | Query | Reads one focal topology model and its semantic mirror. | [SPEC](SPEC.md#catalog-and-topology-inspection) |
| FindPath | `skill-control-center.FindPath` | Query | Executes deterministic bounded traversal over exactly one topology model. | [Discovery](discovery/control-center.md#pathquery) |
| GetUsageEvidence | `skill-control-center.GetUsageEvidence` | Query | Reads accepted usage counts, diagnostics, coverage and freshness separately. | [SPEC](SPEC.md#evidence-inspection) |
| SaveLocalPreference | `skill-control-center.SaveLocalPreference` | Operation | Changes only the current user's local workspace preference revision. | [SPEC](SPEC.md#safe-preparation) |
| SaveChangeProposal | `skill-control-center.SaveChangeProposal` | Operation | Persists a local proposal revision and explicit diff without applying it. | [SPEC](SPEC.md#safe-preparation) |
| ValidateChangeProposal | `skill-control-center.ValidateChangeProposal` | Operation | Computes a versioned non-authoritative validation preview for a saved proposal. | [SPEC](SPEC.md#safe-preparation) |
| AttentionQueuePanel | `ui.skill-control-center.AttentionQueuePanel` | Component | Renders priority, scope, evidence and safe-next-action information. | [Operational orientation](SPEC.md#operational-orientation) |
| CatalogWorkspace | `ui.skill-control-center.CatalogWorkspace` | Component | Renders searchable skill and Dispatch catalogs with stable selection. | [Catalog inspection](SPEC.md#catalog-and-topology-inspection) |
| TopologyWorkspace | `ui.skill-control-center.TopologyWorkspace` | Component | Renders a focal topology plus an equivalent semantic list/table. | [Catalog inspection](SPEC.md#catalog-and-topology-inspection) |
| DraftInspector | `ui.skill-control-center.DraftInspector` | Component | Renders proposal target, base, diff, origins, validation and unavailable authority route. | [SPEC](SPEC.md#safe-preparation) |
| DraftStatusIndicator | `ui.skill-control-center.DraftStatusIndicator` | State Indicator | Encodes the local draft lifecycle with text/icon as well as color. | [SPEC](SPEC.md#feature-concept-graph) |
| useCatalog | `ui.skill-control-center.useCatalog` | Hook | Provides reactive catalog query and selection state to components. | [Catalog inspection](SPEC.md#catalog-and-topology-inspection) |
| CatalogReadBinding | `ui.skill-control-center.CatalogReadBinding` | Binding | Connects the catalog data layer to `SearchCatalog`. | [SPEC](SPEC.md#feature-concept-graph) |
| useTopology | `ui.skill-control-center.useTopology` | Hook | Provides reactive focal topology and path-query state. | [Catalog inspection](SPEC.md#catalog-and-topology-inspection) |
| TopologyReadBinding | `ui.skill-control-center.TopologyReadBinding` | Binding | Connects the topology data layer to `GetTopology`. | [SPEC](SPEC.md#feature-concept-graph) |

## Cross-Feature Terms

No external canonical concept IDs are asserted by the current source corpus. Dispatch and skill
ownership boundaries are described in the discovery, but remain local source references rather
than glossary registry entries until their owning specifications declare canonical IDs.

## Maintenance Rules

- Formal rows derive from the [SPEC registry](SPEC.md#concept-registry).
- Backend query outputs remain Value Objects; render-shaped concepts use `ui.*` View Model IDs.
- Definitions explain but never add behavior.
- Update source concept first, then this glossary.
- Never introduce authoritative apply or benchmark promotion vocabulary as Phase 1 capability.
