# D1 — DomainSpec research structure (native rerun)

## Status and task declaration

**Proposed state: KEEP.** This is a bounded, native internal research task. It is **not** a governed dispatch, has no ACI binding, and provides no evidence that the dispatch infrastructure works.

KEEP here means only that every material claim below is traceable to the immutable D1 bytes and that the findings expose inspectable units, directed handoffs, preservation points, authority boundaries, and declared-versus-observed evidence states relevant to the Composition Lab investigation. It does not claim to satisfy the whole program gate, validate the configured route, or establish causal effects.

## Scope and source notation

Only these three immutable sources at repository revision `9bfec22712e4675d39c4cf1c21b36dc66614136c` were read:

- **S1** — `projects/domainspec-v2/README.md`, 6,246 bytes, SHA-256 `ca5cfbc0a467e3f14e459236d373db4c046f428930c0fae7571246bfe0aeefff`.
- **S2** — `projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md`, 2,575 bytes, SHA-256 `cb09d2412e53288ae891ad6d1f03ff5d56c10808824bf0d7e025fc233cd93557`.
- **S3** — `projects/domainspec-v2/research/domainspec-v2-research-towers.dispatch.json`, 15,381 bytes, SHA-256 `83206a57f4ed8d05a1c623ede6db17ae058e74fcfdc184150d20f2f7096147fd`.

Line selectors refer to those exact bytes. JSON-pointer-like selectors supplement S3 line selectors. No linked artifact was followed.

The Composition Lab program question was supplied separately by the parent only as evaluation context, not as a D1 source: how the phenomenon happens, differs from neighboring phenomena, what it produces/preserves/loses, and how it can be represented and evaluated without exceeding evidence. The D1 claims below remain derived exclusively from S1–S3.

### Contribution to the internal gate (bounded)

| Gate dimension supplied as evaluation context | D1 coverage | Boundary |
|---|---|---|
| DomainSpec v2 | Direct: all three sources identify DomainSpec v2 project structure, discipline, or configured route. | This does not represent the rest of the repository. (S1:L1-L12; S2:L1-L8; S3:L2-L19) |
| Workflows | Direct for declared/configured flow: tower builds, lanes, synthesis, decisions, and handoff. | No execution effect is covered. (S1:L53-L59; S2:L32-L50; S3:L35-L263; S3:L347-L350) |
| Artifacts / knowledge | Direct for named artifact inputs, outputs, storage conventions, local decisions, and promotion boundary. | Contents of the referenced route outputs and actual knowledge preservation are not covered. (S1:L64-L74; S2:L40-L50; S3:L128-L259; S3:L378-L416) |
| Interfaces | Partial: artifact handoffs, receipt fields, authority transfer, and write boundary are represented as declarations. | Runtime/API behavior and enforcement are not covered. (S3:L328-L416) |
| Skills | Reference-only: capability names and skill paths occur in configuration. | Skill contents or behavior were not read and cannot be assessed. (S3:L37-L44; S3:L72-L79; S3:L107-L114; S3:L198-L205) |
| Lenses | Not covered as an explicit unit in these bytes. | Requires a later lot; no classification is inferred from absence. |
| Positives, negatives, uncertainties | Covered as declared preservation/failure mechanisms, negative execution status, and explicit ambiguities below. | These are D1-local and do not satisfy corpus-wide completeness. (S1:L53-L59; S2:L18-L30; S3:L149-L157; S3:L347-L350) |

This lot therefore contributes one comparable internal finding set without predetermining any classification from external vocabulary. Independent review KEEP and the remaining corpus dimensions stay outside D1.

## Observations sustained by the bytes

### S1 — project README

| Required aspect | Observation and evidence state | Selector |
|---|---|---|
| Identity / authority | The document identifies DomainSpec v2 as both an implementation home and a research-tower program, names `DomainSpec v2` as owner, and dates the start. This is project self-description, not independent validation. | S1:L1-L12 |
| Parts / units | It names an `impl/` area, a `research/` area, individual research towers, two lanes per tower, tower-local artifacts, and program-level artifacts. | S1:L14-L20; S1:L22-L45; S1:L64-L74 |
| Relations, direction, order | A tower is described as taking one hypothesis or corpus toward source-backed understanding and bridge decisions. Each tower runs Lane Z and Lane A; later synthesis/adjudication precedes any governed promotion. Tower artifacts remain local while cross-tower artifacts live at the research root. | S1:L24-L36; S1:L64-L71 |
| Transformations / alleged results | The README claims necessary v1 capabilities are imported and reformulated into v2, and states separately that four DROP-verdict capabilities are never imported; it also describes a tower as turning an input hypothesis/corpus into auditable understanding and explicit decisions. These are declared project transformations, not effects observed in this lot. | S1:L7-L20; S1:L24-L29; S1:L78-L80 |
| Preservation | v1 is declared frozen as a read-only evidence source; tower-local seeds, receipts, learning packs, and notes are assigned stable locations; program artifacts receive a separate naming/location convention. | S1:L7-L12; S1:L64-L71; S1:L76-L80 |
| Loss / failure | The README states that four DROP-verdict capabilities are never imported and says a tower idea may either hold or break. It does not enumerate what information import+reformulate may lose. | S1:L20; S1:L24-L29; S1:L78-L80 |
| Absence / ambiguity / contradiction | The route is explicitly “designed and validated, not yet executed”; therefore this source contains no recorded run result for it. “Validated” is not operationally defined in these bytes. The simultaneous labels “implementation home” and “research-tower program” describe two roles but do not specify their interaction beyond folder boundaries. No direct contradiction is established by S1 alone. | S1:L3-L12; S1:L53-L62; S1:L76-L82 |
| Evidence state | Mixed textual status declaration and prescription. The strongest execution-status statement is negative: not yet executed. No observed effect is supplied. | S1:L3-L12; S1:L53-L62 |
| Byte limits / coverage | Coverage is the full file, S1:L1-L82. Linked manifests, seeds, learning packs, prior research, implementation, and skills are outside the authorized bytes and were not inspected. | S1:L10-L11; S1:L25; S1:L42-L45; S1:L57-L62; S1:L81-L82 |

### S2 — Two-Lane Discipline

| Required aspect | Observation and evidence state | Selector |
|---|---|---|
| Identity / authority | The document labels itself a project convention (“discipline”) for DomainSpec v2. Its authority in this lot is normative project text, not a run record. | S2:L1-L8 |
| Parts / units | It defines a tower SEED problem statement, Lane Z, Lane A, synthesis, claim-level bridge decisions, residue with an owner, and a later task-session for promotion. | S2:L10-L27; S2:L32-L50 |
| Relations, direction, order | The underlying problem is stated before evaluating the lanes; both lanes are measured against it; closure occurs only after synthesis adjudicates them; promotion is a separate later step. The text requires tension and joinability but does not state whether the two lanes execute sequentially or concurrently. | S2:L6-L8; S2:L32-L50; S2:L52-L57 |
| Transformations / alleged results | Lane Z iterates generation → counterexample → adjustment → repeat to locate where an idea holds or breaks. Lane A keeps the problem fixed while changing the proposed solution. Synthesis maps lane claims to solved/reframed judgments, bridge decisions, and owned residue. These are prescribed transformations. | S2:L10-L19; S2:L21-L30; S2:L40-L50 |
| Preservation | The same one-sentence underlying problem is intended to survive across both lane evaluations; synthesis must retain claim-level decisions and residue ownership; canonical promotion is kept separate from local decisions. | S2:L32-L50 |
| Loss / failure | Named failure conditions include a friendly demo without a real counterexample, Lane A becoming a variant of Lane Z, anchoring on the first framing, and confusing a reframed problem with a solved one. | S2:L18-L19; S2:L23-L30; S2:L42-L47 |
| Absence / ambiguity / contradiction | “Strongest counterexample,” “genuinely different,” and “distinct second alternative” have no operational test in these bytes. No artifact schema, execution receipt, or completed synthesis appears. The document permits a third lane conditionally but gives no join rule beyond folding it into Lane A or assigning an owner; this is underspecified, not a demonstrated contradiction. | S2:L12-L19; S2:L23-L27; S2:L42-L57 |
| Evidence state | Normative project convention with illustrative examples and an asserted rationale; no execution is recorded and no effect is observed. | S2:L3-L8; S2:L25-L30; S2:L40-L50 |
| Byte limits / coverage | Coverage is the full file, S2:L1-L57. Examples in Lane A illustrate alternatives but do not report that either example ran or succeeded. | S2:L21-L27 |

### S3 — dispatch configuration

| Required aspect | Observation and evidence state | Selector |
|---|---|---|
| Identity / authority | The JSON identifies dispatch `domainspec-v2-research-towers-20260611`, mode `research`, an objective and target artifact. Its authority map assigns lifecycle to `dispatch-spec`, future execution to a task-session with delegated subagents, validation to a validator plus human review, evidence to research artifacts, and later promotion to the DomainSpec v2 owner. | S3:L2-L19 (`/dispatch_id`, `/intent`, `/mode`); S3:L370-L376 (`/boundary_evidence/authority`) |
| Parts / units | The configured top-level units are intent, techniques, six steps, three gates, subagent strategy, lifecycle, boundary evidence, observability, and promotion guardrails. The six steps are two tower builds, a two-lane dialectic, program synthesis, bridge decisions, and handoff. | S3:L3-L34; S3:L35-L263 (`/steps`); S3:L265-L286; S3:L288-L435 |
| Relations, direction, order | Declared artifact flow is: tower seeds → two final learning packs → two lane-receipt ledgers → program synthesis → bridge decisions → program handoff. The dialectic joins by `parent_synthesis`; later steps consume prior outputs. | S3:L52-L65; S3:L87-L100; S3:L128-L154; S3:L171-L191; S3:L213-L225; S3:L242-L259 |
| Transformations / alleged results | The configuration intends to produce source-backed bridge decisions, to build each tower, challenge tower outputs through paired roles, synthesize them, adjudicate local decisions, and create a handoff without canonical promotion. These are intended/configured results only. | S3:L3-L18; S3:L35-L263 |
| Preservation | Artifact refs carry outputs into later inputs; convergence criteria retain problem/solution distinctions; stop conditions require path-cited evidence; receipt requirements preserve identifiers, status, artifacts, validation, blockers, residue, handoff data, and lifecycle-related fields; promotion guardrails preserve the local/canonical boundary. | S3:L58-L68; S3:L93-L103; S3:L128-L157; S3:L188-L195; S3:L226-L229; S3:L328-L345; S3:L432-L435 |
| Loss / failure | Configured block/flag cases include undated sources, conflated readings, unsupported 1:1 mapping, missing path evidence, Lane A collapse, direct promotion, boundary violation, and missing receipt fields. These are anticipated failure states, not observed failures. | S3:L66-L69; S3:L101-L104; S3:L149-L157; S3:L193-L195; S3:L226-L229; S3:L265-L286; S3:L351-L400 |
| Absence / ambiguity / contradiction | Execution is explicitly future; delegated execution requires permission; lifecycle is `none` with no agents. Thus no configured trace event is shown as emitted. The two tower steps each say `parallel: false`, while strategy text says towers can run in parallel; the bytes do not specify which statement controls inter-step scheduling. The strategy receipt list has 16 fields, while the boundary receipt has 10; their compatibility is unspecified. The receipt `stores` list omits `BRIDGE-DECISIONS.md` although that artifact is a configured output and later handoff input. The dialectic names two ledger outputs but designates only the target-state ledger as its `evidence_artifact`. | S3:L45-L47; S3:L80-L82; S3:L288-L327; S3:L328-L350; S3:L378-L400; S3:L138-L155; S3:L219-L255; S3:L419-L430 |
| Evidence state | This is configuration. Strings asserting installed capabilities or validation are configuration-carried claims, not independent proof. The only explicit lifecycle record is `status: none`, `agents: []`; no execution or effect is observed in these bytes. | S3:L40-L44; S3:L75-L79; S3:L109-L114; S3:L198-L205; S3:L326-L350 |
| Byte limits / coverage | Coverage is the full JSON, S3:L1-L437. Referenced seeds, skills, outputs, validators, task sessions, human reviews, receipts, traces, and runtime behavior are outside the authorized bytes and were not inspected. | S3:L42-L43; S3:L52-L65; S3:L203-L204; S3:L328-L350; S3:L419-L430 |

## Cross-source observations

1. **The sources align on a declared progression, not a demonstrated run.** S1 says towers produce non-canonical understanding and later decisions, S2 prescribes problem → lanes → synthesis → later promotion, and S3 encodes artifact dependencies through tower, lane, synthesis, decision, and handoff stages. S1 simultaneously says the route has not executed, and S3 records no agents. (S1:L24-L36; S1:L53-L59; S2:L32-L50; S3:L35-L263; S3:L347-L350)

2. **The underlying problem is the declared invariant across divergent work.** S2 explicitly requires both lanes to be evaluated against the same solution-independent problem; S3 repeats that condition as a gate and gives distinct advocate/challenger roles. (S2:L21-L38; S3:L274-L278; S3:L297-L321)

3. **The declared join retains adjudication rather than simple aggregation.** S2 requires synthesis to distinguish solved from reframed problems, issue a decision per claim, and retain owned residue; S3 configures `parent_synthesis`, repeats the solved/reframed criterion, and later separates synthesis from decision-gate output. (S2:L40-L50; S3:L148-L153; S3:L160-L229)

4. **Authority is intentionally split in the declarations.** Local research decisions cannot themselves promote canonical changes; S1, S2, and S3 all reserve promotion for a later governed action/owner. This is a consistent prescription, not evidence that the boundary was enforced in execution. (S1:L24-L29; S2:L45-L50; S3:L265-L286; S3:L370-L376; S3:L410-L416; S3:L432-L435)

5. **Expected observability is enumerated but uninstantiated.** S3 lists seven trace-event names and receipt fields, yet the same file records no agent lifecycle and supplies no emitted event or completed receipt. (S3:L328-L350; S3:L378-L430)

## Inferences (explicitly separated)

- **I1 — inspectable preservation chain.** The repeated use of artifact outputs as later inputs supports investigating whether a problem statement, alternatives, evidence, decisions, residue, and ownership remain traceable through a multi-unit workflow. This is an inference from configured references, not proof that preservation occurred. (S2:L32-L50; S3:L128-L259; S3:L378-L400)
- **I2 — declarations can be audited separately from effects.** Because normative discipline, executable-looking configuration, lifecycle status, and observed effects are distinguishable in the lot, these bytes help investigate the Composition Lab concern of not mistaking designed structure for functioning execution. This is a provisional relation to the larger problem, not a gate result. (S1:L53-L59; S2:L3-L8; S3:L347-L350; S3:L419-L430)
- **I3 — join quality depends on retained disagreement.** The explicit solved-versus-reframed judgment, per-claim decision, and residue owner suggest that the intended join is evaluative and may lose value if Lane A collapses into Lane Z. The dependency is textually motivated but has no observed outcome here. (S2:L21-L30; S2:L40-L47; S3:L149-L157)
- **I4 — operational semantics remain underdetermined.** The parallelism wording, asymmetric evidence-artifact reference, and two receipt-field lists leave multiple plausible runtime interpretations. No choice among them is supported by this lot. (S3:L107-L158; S3:L288-L345; S3:L378-L400)

## Open hypotheses

- **H1:** A completed run may preserve the declared problem invariant across both lanes in its receipts. No completed receipt is present to test this. (S2:L32-L38; S3:L138-L157; S3:L347-L350)
- **H2:** Parent synthesis may make disagreements more auditable than a merged undifferentiated output by recording solved/reframed judgments, claim decisions, and residue owners. No synthesis output is present to test this. (S2:L40-L47; S3:L148-L191)
- **H3:** The two receipt requirement lists may represent a base contract plus lifecycle extensions rather than conflicting contracts. The bytes do not state that relationship. (S3:L328-L345; S3:L378-L400)
- **H4:** The tower scheduling statements may distinguish intra-step parallelism from inter-tower parallelism. The bytes do not define that scheduling model. (S3:L45-L47; S3:L80-L82; S3:L288-L327)

## Negatives and ambiguities

- No executed run of the configured route, spawned agent for that route, emitted trace, completed receipt, or produced route output, observed preservation, observed loss, or causal effect is evidenced in the three sources. (S1:L53-L59; S3:L347-L350; S3:L419-L430)
- No operational metric defines “strongest counterexample,” “genuinely different solution,” “holds,” “breaks,” or “distinct second alternative.” (S2:L10-L30; S2:L52-L57)
- No runtime rule resolves tower concurrency, join scheduling, or the authority of `parallel` fields versus the prose strategy. (S3:L35-L47; S3:L71-L82; S3:L107-L158; S3:L288-L327)
- No rule in these bytes reconciles the two receipt field sets, the omitted bridge-decision store, or the single evidence-artifact reference for a two-ledger dialectic. (S3:L138-L155; S3:L219-L255; S3:L328-L345; S3:L378-L400)
- The configuration's “installed” and “validation” notes are assertions embedded in the configuration; no validator output or installation evidence is included. (S3:L40-L44; S3:L75-L79; S3:L109-L114; S3:L198-L205)

## Limits

- Findings are bounded to S1–S3 at the verified revision and hashes. They do not incorporate any linked seed, skill, implementation, manifest, receipt, output, trace, validator, prior findings, or external research.
- The lot supports descriptions of declared structure and negative execution status. It does not support classifying or defining composition, proving effectiveness, inferring causality, generalizing beyond D1, or recommending product, architecture, or governance changes.
- The provisional Composition Lab relation is limited to questions these bytes make inspectable: unit boundaries, directed artifact handoffs, preservation claims, join/adjudication claims, authority separation, and the gap between configuration and observed execution. It does not attempt to satisfy the full research gate.

## Questions for the next lot

1. Do completed receipts retain the same underlying problem, lane-specific evidence, claim decisions, and residue owner across every handoff? (Motivated by S2:L32-L50; S3:L128-L191; S3:L378-L400.)
2. What runtime evidence resolves the inter-tower and intra-lane ordering/parallelism ambiguity? (Motivated by S3:L45-L47; S3:L80-L82; S3:L107-L158; S3:L288-L327.)
3. Are the 16-field strategy receipt and 10-field boundary receipt distinct layers, alternatives, or an inconsistency? (Motivated by S3:L328-L345; S3:L378-L400.)
4. Where is the bridge-decision artifact retained as evidence, given that handoff consumes it but the receipt store list omits it? (Motivated by S3:L219-L255; S3:L394-L400.)
5. Which observed traces or artifacts, if any, demonstrate the expected events and boundary enforcement rather than merely declaring them? (Motivated by S3:L351-L377; S3:L419-L435.)

## Proposed disposition

**KEEP**, narrowly: the material findings are selector-backed and contribute a bounded inventory of units, relations, order, preservation/failure claims, authority splits, and evidence-state gaps for the Composition Lab investigation. They must remain tagged as observations, prescriptions, configuration, inferences, and hypotheses exactly as above. There is no execution evidence and no claim that the larger gate is met.

## Prior-attempt isolation record

After this findings file was first saved, a filename-only filesystem check confirmed that the prior artifact exists at `C:\Users\victo\cyberalchemy-orchestrator\internal-tools\composition-lab\orchestration\execution-redesign\runs\d1-domainspec-research-structure\scout-return.md`. Its contents were not opened, read, cited, corrected, summarized, compared, or used in this rerun. No prior `audit.md` or findings artifact was opened or used.
