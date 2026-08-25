# Review — Typed Interaction Relation Proposal

## Coverage

| attacker | lens | findings raised | zero-findings defence |
|---|---|---:|---|
| Coase, Ronald | fidelity / governance | 5 | Not applicable; the attacker raised findings. |
| Liskov, Barbara | mechanics / correctness | 8 | Not applicable; the attacker raised findings. |
| Capucci, Matteo | ownership / reference integrity | 6 | Not applicable; the attacker raised findings. |
| Jensen, Michael C. | abuse / gaming | 11 | Not applicable; the attacker raised findings. |

All four attackers were bound to the complete nine-target frozen corpus and reported completing that
scope. Target-by-lens coverage is therefore complete: all 36 required target/lens intersections were
attacked.

| frozen target | fidelity / governance | mechanics / correctness | ownership / reference integrity | abuse / gaming |
|---|:---:|:---:|:---:|:---:|
| `research-initial-definitions.md` | covered | covered | covered | covered |
| `dispatch-proposal.md` | covered | covered | covered | covered |
| `research.md` | covered | covered | covered | covered |
| `findings.md` | covered | covered | covered | covered |
| `stages/01-exploration/local-as-built.md` | covered | covered | covered | covered |
| `stages/01-exploration/generative-basis.md` | covered | covered | covered | covered |
| `stages/01-exploration/authority-evidence.md` | covered | covered | covered | covered |
| `stages/01-exploration/current-solutions.md` | covered | covered | covered | covered |
| `docs/decisions/typed-interaction-graph-research-execution.md` | covered | covered | covered | covered |

All nine current SHA-256 values match the frozen opening record. The 30 working findings were
deduplicated into 17 candidates. After the two verifier dispositions were applied, eight findings
survived and nine refuted findings were removed. Every surviving finding includes its file, exact
artifact quotation, proof, severity, and one-line proposed fix.

The verdict taxonomy is consistent: `findings.md` is **FIX** because eight MAJOR findings survive;
the other eight artifacts are **KEEP** because none has a surviving CRITICAL or MAJOR finding.

The all-attacker zero-findings red flag did not trigger because every attacker raised findings. Had
all four attackers returned zero findings, this auditor would have classified the result as a
failure to attack rather than evidence of cleanliness.

## `research-initial-definitions.md`

No candidate CRITICAL or MAJOR finding.

**Verdict:** KEEP

## `dispatch-proposal.md`

No standalone candidate finding. Its pending gates and acceptance contract are evidence for the
premature-verdict finding against `findings.md`, not a defect in this proposal.

**Verdict:** KEEP

## `research.md`

No standalone candidate finding. Its explicit candidate boundary is narrower than the formal
verdicts later emitted by `findings.md`.

**Verdict:** KEEP

## `findings.md`

| # | file | evidence (quoted from the artifact) | proof | severity | proposed fix |
|---:|---|---|---|---|---|
| F1 | `docs/features/agents-communication-infra/research/interaction-relations/findings.md` | “The smallest basis supported by the examined local and external traces has five directed relation types” and matrix verdicts such as “**GO — build from owned local precedent.**” | The same artifact leaves P1–P3, N1–N5, and D1–D5 to “the next gates”; `research.md` also says those gates remain next work. `dispatch-proposal.md` makes those skeptic gates and a final audit conditions of acceptance. `GO`, `KILL`, and “smallest” therefore state outcomes that the frozen execution has not produced. Candidate/draft caveats do not make a formal verdict matrix valid before its own decision gates. | MAJOR | Replace `GO`/`KILL` and “smallest” with explicit hypotheses, or execute and preserve the three gates and final audit before emitting formal verdicts. |
| F2 | `docs/features/agents-communication-infra/research/interaction-relations/findings.md` | “Subject identity is recoverable from the typed slot, the assessment obligation from the occurrence kind, criteria from its profile, authorship from its binding, and authority from a separate gate. Keeping the edge would duplicate those facts.” | The accepted reduction for `assessed_by` also eliminates `delegates`, `gates`, and `transfers_control` if one may introduce delegated-work, decision, and transfer occurrence kinds with bindings, policies, slots, and runtime effects. Conversely, forbidding that semantic relocation invalidates the stated demotion of `assessed_by`. The pairwise table proves behavioral distinctions, not irreducibility under a uniform representation budget. | MAJOR | Define observational equivalence and one allowed reduction vocabulary, forbid asymmetric semantic relocation, then rerun every removal and pairwise-collapse test. |
| F3 | `docs/features/agents-communication-infra/research/interaction-relations/findings.md` | “The implemented sequential path and the declared `depends_on` edge are local precedents” and “A pure prerequisite trace exists that does not disclose source evidence; otherwise `requires` should collapse into mandatory `supplies`.” | The implemented sequential path always couples readiness to an exact handoff receipt and materialized input. `ProtocolRecipe.depends_on` is non-executable candidate data and the frozen built-ins do not witness its asserted semantics. N1 explicitly leaves the required non-visibility witness unproved. An opaque mandatory completion slot remains an unrefuted collapse. | MAJOR | Remove `requires` from the admitted minimum until a pure prerequisite-without-delivery witness survives the non-vacuity gate, or prove why an opaque mandatory slot is observably inequivalent. |
| F4 | `docs/features/agents-communication-infra/research/interaction-relations/findings.md` | The endpoint model admits “Occurrence,” “Evidence,” “Slot or transition,” and “Control scope,” while `transfers_control` is “the current holder of a control scope -> the successor holder of that same scoped responsibility.” | Current and successor holders are not admitted endpoint kinds. Encoding both as the same control scope yields a self-edge; treating agents/seats as endpoints contradicts their classification as bindings; treating holdings as occurrences invents an unstated contract. The ambiguity prevents typing exclusive and shared holder transitions. | MAJOR | Introduce immutable `ControlHolding(scope, holder, epoch)` endpoints and define transfer between successive holdings, including exclusive/shared compatibility. |
| F5 | `docs/features/agents-communication-infra/research/interaction-relations/findings.md` | Delegation says “rejection, timeout, cancellation, or failure returns a typed outcome to the delegator”; transfer says “If delivery or acceptance fails, control remains with the source.” | The cited OpenAI and Microsoft sources witness retained-manager responsibility versus handoff ownership. They do not establish typed failure returns, atomic transfer receipts, exactly-one-holder guarantees, rollback on acceptance failure, cancellation behavior, or the proposed permission model. Those are candidate design requirements presented inside the admitted relation contract without independent evidence. | MAJOR | Separate externally witnessed semantic differences from additional design hypotheses and cite or test every failure, rollback, atomicity, and permission guarantee independently. |
| F6 | `docs/features/agents-communication-infra/research/interaction-relations/findings.md` | “the exact evidence becomes the materialized value of that slot” while the same view “may be full, filtered, or redacted by the slot contract.” | A permissive slot can accept `{redacted: true}`, produce a success receipt, and satisfy the input while preserving none of the evidence needed downstream. A filtered/redacted projection is not the “exact evidence”; it is new derived evidence with different fidelity. | MAJOR | Treat projections as distinct evidence with their own digest and transformation provenance, and require each slot to validate a minimum-disclosure/fidelity predicate. |
| F7 | `docs/features/agents-communication-infra/research/interaction-relations/findings.md` | “Relations connect logical, versioned endpoints”; “Reverse delivery in a feedback protocol targets a new round/version”; “New output is a new version and may be reassessed.” | Immutable W1 and W2 can both retain valid assessments and gates because the basis defines no lineage, supersession, currentness, or invalidation fact. A stale W1 approval can release after W2 exists, and round labels alone cannot identify the canonical zig-zag/feedback generation. | MAJOR | Add explicit lineage/currentness/invalidation semantics and demonstrate that stale gates and deliveries fail closed. |
| F8 | `docs/features/agents-communication-infra/research/interaction-relations/findings.md` | A new primitive is rejected when replacement by “the current relations plus combinators, roles, schemas, recipes, policies, and runtime effects” preserves the behavior; “Otherwise it belongs to one of those separated layers.” | The substitution language is unrestricted. Negotiation can be hidden in `NegotiationOccurrence` plus policy/runtime code and compensation in a recipe plus bespoke undo code, keeping five edges unchanged while every hard semantic case becomes special logic. This defeats the dispatch requirement for extension “sem fallback silencioso para lógica especial.” | MAJOR | Bound the substitution language, require an explicit semantic-remainder report, and admit a reusable primitive when validation/authority/failure obligations otherwise survive only in domain-specific policy or runtime code. |

**Verdict:** FIX

## `stages/01-exploration/local-as-built.md`

No candidate CRITICAL or MAJOR finding.

**Verdict:** KEEP

## `stages/01-exploration/generative-basis.md`

No standalone candidate finding. Its conditional treatment of `assessed_by` is evidence for F2;
the unconditional demotion occurs in `findings.md`.

**Verdict:** KEEP

## `stages/01-exploration/authority-evidence.md`

No candidate CRITICAL or MAJOR finding.

**Verdict:** KEEP

## `stages/01-exploration/current-solutions.md`

No candidate CRITICAL or MAJOR finding survived verification.

**Verdict:** KEEP

## `typed-interaction-graph-research-execution.md`

No candidate CRITICAL or MAJOR finding.

**Verdict:** KEEP

## Change requests

1. MAJOR — Withdraw formal `GO`/`KILL` and “smallest” verdicts until the declared gates and audit run.
2. MAJOR — Define a uniform minimality/reduction test and rerun every primitive and pair.
3. MAJOR — Resolve the missing non-vacuity witness for `requires`.
4. MAJOR — Repair control-holder endpoint typing.
5. MAJOR — Separate externally witnessed behavior from unsupported failure/atomicity guarantees.
6. MAJOR — Type filtered/redacted evidence as a distinct projection with fidelity requirements.
7. MAJOR — Add lineage/currentness/invalidation semantics for versioned endpoints.
8. MAJOR — Bound the extension substitution language so hard cases cannot disappear into bespoke policy/runtime code.
