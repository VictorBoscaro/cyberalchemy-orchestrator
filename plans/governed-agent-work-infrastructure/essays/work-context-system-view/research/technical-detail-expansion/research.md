# Technical-detail expansion: verbatim researcher returns

## Abramsky — formal/compositional angle

All six candidates are `build-from-owned`: the repository already contains the underlying ideas, but the target essay either introduces them too late or does not connect them into one inspectable shape.

### 1. State the five independent paths immediately after §3

- **Insertion location:** End of §3, before §4.
- **Proposed explanatory payload:**  
  “The system must preserve five independently inspectable paths: purpose, authority, assignment, causation, and realization. These paths may converge on the same outcome, but convergence does not make them interchangeable. The remainder of this essay explains the properties, responsibilities, and validation strategy required to preserve them.”
- **Repository evidence:** The five paths already appear explicitly in §35, especially lines 784–810. Sections 4–5 already motivate upward purpose/authority and downward realization traversal, while §20 distinguishes logical work, attempts, effects, and artifacts.
- **Concrete consequence:** A reader can evaluate every later section against a compact contract. A reviewer can ask whether each path has independent evidence and whether any conclusion was imported from another path.
- **Ownership boundary:** This names path purposes and their required separability. It does not define relation vocabularies, sufficient-path rules, record shapes, or enforcement behavior.
- **Collapse condition:** Remove the addition if the five paths cannot be traced to distinct failure cases in the first-slice fixture. The existing fixture already supplies such cases: purpose/authority confusion, adjacency mistaken for causation, and authorized-but-unassigned execution (§36).

### 2. Replace the single “Context Graph” with a graph-family shape

- **Insertion location:** Replace the diagram and first explanatory paragraph in §29.
- **Proposed explanatory payload:**

  ```text
  accepted assertions, decisions, and events
                      |
                durable history
                      |
          +-----------+-----------+
          |           |           |
      purpose      authority    evidence
       graph         graph        graph
          |           |           |
          +-----------+-----------+
                      |
           task-specific projections
  ```

  Follow with: these labels indicate a possible family of overlapping graph views over attributable historical material, not one canonical graph or a decided persistence topology. Execution, assignment, causation, and realization may require additional views or intersections; which families are first-class remains open.
- **Repository evidence:** The current §29 diagram places `Context Graph` before accepted facts and `Event History` (lines 632–653), creating ambiguous derivation direction. §6 requires simultaneous organizations; §26 says projections derive views and must not acquire authority. The primitives essay says graphs may be descriptive, authoritative, provenance-bearing, or projections, and explicitly leaves first-class graph families open (`from-context-to-governed-primitives.md`, §§Graph, Runtime graph, Open questions).
- **Concrete consequence:** It prevents two false architecture assumptions: that one graph is canonical and that durable history is produced by a current graph. It gives later architecture work an explicit decision: whether graph views are persisted, derived, or hybrid.
- **Ownership boundary:** The system view names graph-family plurality and information flow only. Exact graph membership, edge kinds, persistence owners, schemas, and conformance mappings remain ontology/engineer/specification work.
- **Collapse condition:** Collapse back to one contextual structure only if a later owner proves that every required traversal, authority boundary, provenance distinction, and projection can share one semantic graph without manufactured inference or ownership ambiguity.

### 3. Give direct relations and derived conclusions visibly different epistemic roles

- **Insertion location:** §30, immediately after the two path examples.
- **Proposed explanatory payload:**  
  “A direct relation is attributable source material. A derived conclusion is a claim produced from direct relations under an accepted, version-applicable composition policy. The derived claim must remain defeasible without rewriting its direct sources: a changed rule, revoked acceptance, superseded edge, or failed assumption can invalidate the conclusion while leaving the historical witness intact.”
- **Repository evidence:** §11 distinguishes assertion, support, acceptance, and operational authority; §12 preserves accepted change; §30 already requires direct witnesses and applicable rule versions. The primitives essay’s “Path and witness” section says derived macro-to-micro connections must remain reconstructable from direct relations, rule versions, and assumptions.
- **Concrete consequence:** A reader can distinguish “this edge existed” from “this path licensed this conclusion.” A test can change a composition policy and expect derived results to change while historical direct relations remain reconstructable.
- **Ownership boundary:** This states the shape of epistemic separation, not what counts as direct, which relations compose, the inference language, invalidation algorithm, or storage layout.
- **Collapse condition:** Remove this distinction only if the system never materializes or relies on derived claims. If any derived path can influence inspection, context selection, or authority judgment, collapsing it into direct fact would erase its justification.

### 4. Explain a path witness as a replayable justification, not a stored path

- **Insertion location:** End of §30, before its alternative-framings table.
- **Proposed explanatory payload:**  
  “At this altitude, a witness is the inspectable justification for a path: the attributable direct links, the applicable composition stance, and the historical conditions under which the conclusion was accepted. It is sufficient only if another inspection can reconstruct why the conclusion held then and determine whether it still holds now. Whether a witness is stored, recomputed, or hybrid remains an implementation decision.”
- **Repository evidence:** §30 lines 669–683 and candidate invariant §31 require direct witnesses and composition rules. The primitives essay’s §Path and witness and §Invariants connect primitives require derivation and kernel-composition witnesses. §35 requires reconstructable purpose, authority, assignment, and causal execution paths.
- **Concrete consequence:** This turns “retain witnesses” into a falsifiable reader-level obligation: historical replay must explain both past validity and current status. It also prevents premature commitment to witness records or graph paths as the only representation.
- **Ownership boundary:** No witness schema, mandatory fields, cryptographic representation, recomputation strategy, or acceptance protocol is selected.
- **Collapse condition:** Drop the candidate if “witness” adds no capability beyond retaining source references. It survives only if rule applicability, assumptions, or historical acceptance can change the conclusion without changing those sources.

### 5. State projection preservation through observable negative obligations

- **Insertion location:** End of §26, with a short forward reference from §33’s “projection preservation.”
- **Proposed explanatory payload:**  
  “A projection is trustworthy only relative to what it claims to preserve. At minimum, a task-specific view must not create identity, fact, authority, causal binding, or currentness that its accepted sources do not support. Omission may be legitimate when declared by the projection’s purpose; invention is not. Which positive structures each projection must preserve remains an open stance.”
- **Repository evidence:** §26 says projections may be task-specific and cannot acquire authority; §31 says projections cannot manufacture facts or authority; §33 names projection preservation without explaining its stake. The primitives essay’s §Projection and view allows partial or stale projections but forbids convenience from becoming authority.
- **Concrete consequence:** Reviewers gain concrete negative tests: a projected folder tree cannot authorize an action; a task context package cannot turn adjacency into causation; an omitted supersession cannot be reported as current. This separates legitimate selection from semantic manufacture.
- **Ownership boundary:** The essay does not define a projection function, preservation laws, completeness classes, cache coherence, or per-projection contracts.
- **Collapse condition:** Remove “projection preservation” if projections are purely decorative and never used to answer governed questions. If a projection influences human or agent decisions, at least the non-manufacture obligation remains necessary.

### 6. Turn composition into a named obligation at both path and domain boundaries

- **Insertion location:** Add a short bridge between §30 and §32, then extend the §36 fixture inventory by one case.
- **Proposed explanatory payload:**  
  “Composition creates a new inspection obligation at two scales. Within a relation family, a multi-edge conclusion needs a path witness. Across independently governed contexts, locally valid judgments need a compatibility witness showing which properties survive their combination. Neither witness is evidence merely because its components passed separately.”
  
  Add to §36: one fixture where two locally accepted relations or domain judgments compose into a forbidden or unsupported global conclusion.
- **Repository evidence:** §30 covers relation-path composition; §31 says local validity does not imply global compatibility; §32 asks what must be witnessed when governed domains compose. The primitives essay states, “The composition needs its own witness” after demonstrating that valid authority, assignment, and effect relations do not automatically yield valid total execution.
- **Concrete consequence:** The first slice tests not only missing edges but false closure: individually valid inputs must not cause an unsupported global conclusion. This gives `OD-04` and `OD-05` distinct yet connected stakes.
- **Ownership boundary:** It does not choose a compatibility calculus, global invariants, trusted-boundary topology, kernel arrangement, or formal tool.
- **Collapse condition:** Collapse the two scales only if later analysis proves that cross-domain compatibility is identical to ordinary path composition. The repository currently presents different failure modes, so that equivalence is not established.

### Defended exclusions

- **No canonical graph taxonomy.** Naming purpose, authority, evidence, assignment, causation, realization, provenance, or execution as mandatory persisted graph types would decide the “which graph families need first-class support?” question owned downstream.
- **No event-sourcing verdict.** “Durable history” should describe reconstructability and attribution, not mandate an append-only event store. The essay explicitly distinguishes logical responsibility from deployment topology.
- **No witness record schema.** Fields such as edge IDs, rule IDs, validity intervals, hashes, or acceptance receipts belong in ontology, engineer, or domain-specification work.
- **No categorical formalization beyond the existing gate.** §34 already correctly requires carriers, identities, closure, associativity, preservation, and a falsifier before categorical vocabulary is admitted. Adding functors or natural transformations now would raise vocabulary density without a new decision or test.
- **No universal composition policy.** “Deny by default,” transitive closure, authority intersection, or one central inference service would each decide `OD-04` or `OD-05`.
- **No exact experiment thresholds.** The essay should add observable cases and failure conditions, but accuracy, time, and maintenance-cost thresholds must remain frozen by the later experiment owner.
- **No exhaustive positive preservation law for projections.** Negative non-manufacture obligations are justified now; the exact structure a given projection must preserve depends on its declared purpose and later formal ownership.

**One-line finding:** The strongest additions do not add new machinery; they expose the existing proposal as a graph-family system whose derived conclusions, projections, and cross-context compositions remain justified by replayable witnesses and falsifiable non-manufacture obligations.

## Hamming — operational/measurement angle

I found six additions that would make the essay materially more operational without importing ACI/APT schemas.

### 1. Define a path result contract, not only path shapes

- **Insertion:** Immediately after the five paths are introduced near §3, with a concrete example revisited in §35.
- **Payload:** Explain that a path query should return one of four broad outcomes: `witnessed`, `missing`, `conflicted`, or `superseded`. A witnessed result identifies the direct links, their currentness, and the evidence or accepted rule supporting each transition. Missingness identifies the first absent binding rather than returning “not found.” Conflict means two accepted but incompatible candidates remain unresolved. Superseded means a historically valid path is no longer current.
- **Repository evidence:** The essay already requires missing and superseded links to remain visible (§23–26, §31, §35–36). APT distinguishes immutable captured/partial/missing outcomes and treats supersession as derived currentness rather than rewriting history ([APT domain lines 65–151](../../../../../../docs/features/agent-provenance-telemetry/specs/domain.md)); ACI preserves immutable confirmed authority and terminal facts ([ACI domain lines 20–52](../../../../../../docs/features/agents-communication-infra/specs/domain.md)).
- **Observable consequence:** A reader can state what an inspection returns when no complete path exists. A test can freeze both a classification and the exact first broken edge.
- **Generality boundary:** Use semantic result classes, not APT status enums, record layouts, or field names. Domains may refine or rename the classes.
- **Collapse condition:** Remove this addition if the first slice cannot produce materially different actions for missing, conflicted, and superseded paths.

### 2. Add a minimal witness anatomy shared by all five paths

- **Insertion:** §30, before the discussion of composition rules.
- **Payload:** A defensible direct step minimally answers: **what relation is claimed, between which stable identities, under which applicable version or scope, who or what accepted it, and where its supporting evidence can be resolved**. A derived step additionally names the direct steps and the accepted composition rule. Each path may require different evidence, but none may rely on labels, filenames, timestamps, or proximity alone.
- **Repository evidence:** The essay’s candidate invariants already require relation type, direction, provenance, scope, version, direct witnesses, and composition rules (§31). APT rejects producer inference from persona, path, locator, prose similarity, or temporal proximity (APT lines 350–403); ACI binds confirmed intent and attempts through stable identities and frozen digests (ACI lines 20–30, 89ff).
- **Observable consequence:** Reviewers gain a stable checklist for deciding whether a displayed edge is inspectable or decorative. Fixtures can mutate each witness dimension independently.
- **Generality boundary:** This states questions every witness must answer, not a universal envelope, database row, or ownership protocol.
- **Collapse condition:** Collapse it into §31 if these five questions do not improve fixture design or review consistency beyond the existing invariant list.

### 3. Make terminal evidence a two-part claim

- **Insertion:** §35, replacing or expanding the paragraph beginning “The slice must classify terminal evidence.”
- **Payload:** State that terminal evidence has two separable obligations:

  1. **terminal-state witness** — evidence that an attempt, artifact publication, or effect observation reached a recognized terminal condition;
  2. **outcome-binding witness** — evidence that this terminal occurrence produced, effected, or otherwise supports the candidate outcome.

  A terminal attempt without the second witness is activity evidence, not causal evidence. A finalized artifact without a producer binding is durable content, not realization evidence. An intended effect without an accepted outcome observation is a request, not an effect.
- **Repository evidence:** The essay already distinguishes EffectIntent, committed observation, finalized artifact, and accepted causation (§20–23, §35). ACI separates unique terminal facts, effect intent, finalized artifacts, and publication results (ACI lines 50–52, 173–190, 579–587). APT requires committed evidence for missing outcomes and exact accepted origin bindings (APT lines 143–152, 405–465).
- **Observable consequence:** The fixture matrix gains three explicit negatives: terminal-without-outcome-binding, artifact-without-producer-binding, and intent-without-observed-outcome.
- **Generality boundary:** Do not prescribe which runtime event, receipt, artifact type, or observation satisfies either obligation.
- **Collapse condition:** Remove the split if every supported terminal kind necessarily and atomically includes the outcome binding; current repository evidence shows that this is not presently true.

### 4. Describe drift as invalidated dependency, not generic staleness

- **Insertion:** End of §24 or beginning of §25.
- **Payload:** Explain a minimal drift-detection cycle:

  ```text
  accepted source changes
        ↓
  dependent path steps are located
        ↓
  their applicability is re-evaluated
        ↓
  affected paths become current, superseded, conflicted, or missing
        ↓
  an attributable diagnostic is emitted
  ```

  The detector must name the changed source, dependent claim, invalidated assumption, and affected path. It may report a discrepancy; it may not silently repair semantic lineage.
- **Repository evidence:** §24 lists drift cases but does not specify what a useful diagnostic contains. §25 already prohibits hooks and observers from manufacturing relationships. APT pins exact snapshots/digests and rejects equivalent-looking, newer, cross-dispatch, or stale sources (APT lines 394–403, 614–632); immutable revisions preserve predecessor/currentness rather than overwriting (APT lines 85–107).
- **Observable consequence:** A drift test can mutate one dependency and assert both the affected paths and the reason, instead of merely asserting that “drift was detected.”
- **Generality boundary:** No commitment to event sourcing, dependency indexes, hook topology, hash algorithms, or automatic invalidation policy.
- **Collapse condition:** Remove the cycle if the system will only offer periodic human review and cannot identify dependency-specific consequences.

### 5. Turn the frozen corpus into a mutation-based fixture family

- **Insertion:** §36, after the current fixture list.
- **Payload:** Start from one completely witnessed golden case, then derive negatives by changing exactly one binding at a time:

  - remove purpose;
  - substitute stale authority;
  - change assignment to a different task;
  - replace causal evidence with adjacency;
  - retain intent but remove outcome observation;
  - retain an artifact but remove producer binding;
  - supersede one source while preserving history.

  Freeze expected results in both directions: outcome-to-purpose and purpose-to-outcome. Also freeze the first broken binding and ensure unrelated paths remain unchanged.
- **Repository evidence:** The current list mixes independent scenarios and does not guarantee single-cause discrimination. APT explicitly uses field-by-field golden/tamper vectors, closed status-matrix negatives, stale-snapshot negatives, and canonicalization tests (APT lines 134–152, 394–403). ACI treats same-identity divergent canonical content as conflict and identical retries as stable (ACI lines 239–241, 742–743).
- **Observable consequence:** Each false inference has a minimal counterexample; regressions can be attributed to one semantic obligation rather than an opaque scenario.
- **Generality boundary:** Borrow the testing principle—one controlled semantic mutation—not ACI/APT fixtures, schemas, or canonical encodings.
- **Collapse condition:** Drop a mutation when changing that binding cannot alter an expected answer independently of the others.

### 6. Operationalize “acceptable maintenance cost” as decision metrics

- **Insertion:** §36, replacing the final sentence about thresholds with a compact measurement frame.
- **Payload:** Freeze a baseline and measure at least:

  - **answer quality:** correct classification and correct first-broken-binding localization;
  - **investigation effort:** elapsed time and evidence sources inspected per question;
  - **capture burden:** additional declarations or review actions required per unit of work;
  - **repair burden:** effort to restore valid paths after a source changes;
  - **false confidence:** complete-looking answers later shown to depend on missing or stale bindings.

  Compare the structured system against reconstruction from ordinary repository artifacts. Report distributions or case counts, not only averages. The experiment should state a stopping rule: if quality or investigation-time gains do not compensate for capture and repair burden, the slice does not justify expansion.
- **Repository evidence:** §36 already names accuracy, time, capture, maintenance cost, and measurable benefit but leaves their observables unspecified. The ACI/APT models illustrate why write burden exists: exact identities, immutable records, evidence resolution, canonicalization, and supersession all impose work (ACI lines 20–52; APT lines 65–151, 792–808).
- **Observable consequence:** A future experiment can preregister denominators and make a go/no-go decision, instead of concluding qualitatively that inspectability “feels better.”
- **Generality boundary:** The essay should name measurement dimensions, leaving thresholds, instrumentation, sampling, and workload accounting to the experiment.
- **Collapse condition:** Remove any metric that cannot change the adoption decision or distinguish the proposal from baseline reconstruction.

### Defended exclusions

- **Do not copy `ConfirmedDispatch`, `DispatchAuthoritySnapshotRef`, `ResearchCapture`, `ProducerRef`, or their fields into the general narrative.** They are repository correspondence and would make the system view look like a runtime schema.
- **Do not prescribe canonical JSON, digest algorithms, CAS journals, idempotency tuples, discriminated unions, or fail-closed parsing.** They are strong implementation evidence for exactness, but belong in domain specifications or an engineer view.
- **Do not declare one universal evidence hierarchy.** Test, review, observation, proof, and accountable judgment establish different claims; §22 correctly leaves realization sufficiency open.
- **Do not define numerical thresholds in the essay.** Measurement dimensions belong here; thresholds require a frozen workload and preregistered experiment.
- **Do not make drift detection automatic semantic repair.** Repository evidence supports exact discrepancy detection, not autonomous authority or lineage invention.
- **Do not expand all five paths into separate runtime graph schemas.** The useful addition is a shared witness contract plus path-specific questions; ownership and storage remain open.

The strongest additions are the two-part terminal-evidence contract, minimal witness anatomy, and mutation-based fixture family. Together they convert the current thesis into falsifiable inspection behavior while remaining independent of ACI/APT implementation forms.
