# Formal explorer return — participants, lenses, schemas, and instances

## Result

The intuition is productive if stated as **role-indexed typing**, not identity of entities:
Victor, Vlad, and an agent are participants who, at a given turn, may (a) apply or expose a
readout, (b) supply a schema, (c) populate a schema with an instance, or (d) define a translation
between schemas. They are not thereby themselves schemas, instances, or functors. The alternation
is between typed acts/interfaces of a participant.

This gives the lens program three useful separations: joint observation versus sequential
translation; artifact production versus instance population; and preservation by a supplied
translation versus selection or repair of that translation. It also gives an operational account
of mutual consumption. If `S_p` is participant `p`'s offered schema, an instance is literally
`I_p : S_p ⥤ Type`; if `F_pq : S_p ⥤ S_q` is a supplied schema translation, then `p` can consume a
`q`-instance `I_q` by pullback `I_q ⋙ F_pq : S_p ⥤ Type`. This is directly supported by the local
definitions and composition law
[`SchemaInstance.lean:57-101`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/SchemaInstance.lean#L57).

## Minimal typed candidate

Let `P` be participants and `K` interaction contexts/turns. Do **not** put a categorical structure
on `P` yet. For each `(p,k)` allow independently optional data:

```text
Target X_k
Readout O[p,k] : X_k -> Y[p,k]
Schema  S[p,k] : Schema
Instance I[p,k] : Instance S[p,k]       -- S[p,k] -> Type
Translation F[p,q,k] : SchemaMorphism S[p,k] S[q,k]
Consumption consume[p<-q,k](I_q) := pullback F[p,q,k] I_q
Artifact A[p,k] with a separately stated conformance/interpretation into I[p,k]
```

The roles then type as follows.

| informal statement | typed reading | present status |
|---|---|---|
| “Victor, Vlad, and agent are different lenses” | they supply distinct `O[p,k]`, or distinct lens descriptors/operators, over a named common target | operational hypothesis; distinct names/personas do not prove distinct readouts |
| “we compose lenses” | joint family `p ↦ O[p,k]` on one `X_k`, or a separately typed sequential composition of translations | joint readouts witnessed narrowly; general lens composition unbuilt |
| “p is a schema for q” | `p` supplies `S[p,k]`, which constrains what `q` may express/populate | sound rephrasing; entity-level identity is a type error/metaphor |
| “p is a functor between q and r” | `p` supplies/executes `F : S[q,k] ⥤ S[r,k]` and witnesses identity/composition preservation | open per concrete episode; object/generator correspondence is insufficient |
| “we consume each other's instances” | one participant's `I_q : S_q ⥤ Type` is reindexed along `F : S_p ⥤ S_q`, or is interpreted as an artifact under another schema | pullback case is formally owned; artifact-to-instance conformance remains to be typed |
| “one output becomes the other's schema” | a reification operation produces `S[p,k+1]` from a prior artifact/residue | research-local hypothesis; no current derivation or justified selection rule |

The Composition Lab itself already distinguishes lens-as-coverage, lens-as-agent method/position,
and lens-as-transformation, and explicitly treats their convergence as open
[`02-composition-strategy.md:13-17`](C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/milestone-1-strategy/02-composition-strategy.md#L13).
Its live hypotheses separate descriptor, operator, relational position, and retrospective label
[`02-composition-strategy.md:33-36`](C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/milestone-1-strategy/02-composition-strategy.md#L33).
The candidate above preserves those alternatives instead of deciding prematurely that a person is
one categorical object.

## What is supported

1. **An instance is a functor; a participant is not automatically one.** The repo defines a schema
   as a bundled small category, an instance as a functor into `Type`, a schema morphism as a
   functor, and consumption/reindexing as precomposition
   [`SchemaInstance.lean:57-84`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/SchemaInstance.lean#L57).
   Pullback respects identity and composition
   [`SchemaInstance.lean:88-101`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/SchemaInstance.lean#L88).

2. **Different lenses can add information in one narrow sense.** For readouts on a common carrier,
   the joint family is defined at `ObservationBudget.joinFamily`; joint injectivity makes every task
   factor through it, while non-injectivity yields a task it cannot read
   [`ObservationBudget.lean:92-127`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/ObservationBudget.lean#L92).
   The audit consequently permits the smaller claim that an extra coordinate can strictly refine
   observational equivalence for an independently fixed task, but demotes general “lens
   composition” [`findings.md:11`](C:/Users/victo/domainspec-lean-formalization/research/audits/lens-reflexivity-bidirectional-refutation-2026-08-11/research/findings.md#L11).

3. **A mapping must earn functor status.** `PrefunctorCompositionFailure` constructs a mapping with
   the same primitive object/generator data as the good semantics but a computed failure of
   composition; it concludes that primitive local data do not certify composition
   [`PrefunctorCompositionFailure.lean:99-110`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/PrefunctorCompositionFailure.lean#L99),
   [`PrefunctorCompositionFailure.lean:152-185`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/PrefunctorCompositionFailure.lean#L152).
   Thus “the agent transported Vlad's idea into Victor's schema” is only a prefunctor-shaped claim
   until identities, composites, and the relevant preserved structure are checked.

4. **Partial translations and incompatible continuations are real, but static.** The repo defines
   object-supported partial functors, extension, extension failure, boundary, and maximality while
   explicitly denying that extension failure is thereby residue or any epistemic phenomenon
   [`PartialFunctorExtension.lean:28-50`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/PartialFunctorExtension.lean#L28),
   [`PartialFunctorExtension.lean:99-158`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/PartialFunctorExtension.lean#L99).
   It also exhibits two non-isomorphic extensions that fail to coextend
   [`ObjectPartialFunctorBranching.lean:70-108`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/ObjectPartialFunctorBranching.lean#L70).
   This is a good model for “our interpretations agree here but diverge when extended,” not yet a
   model of learning, reconstruction, or warranted revision.

5. **Reflexive reuse is plausible as reification, not automatic self-reference.** The genealogy
   permits the bounded wording that reflection can reify some structure that produced a prior
   claim into a next-level object, with source/lens/time/scope annotations
   [`victors-intuition findings.md:67-71`](C:/Users/victo/domainspec-lean-formalization/research/victors-intuition-lens-genealogy-2026-08-11/research/findings.md#L67).
   But the formal audit says composition/extension/generativity do not supply quotation,
   evaluation, universality, or point-surjectivity and therefore do not establish semantic
   self-reference [`minimalism findings.md:143`](C:/Users/victo/domainspec-lean-formalization/research/audits/minimalism-composition-generativity-analogy-limits-2026-08-10/research/findings.md#L143).

6. **Residue diagnoses a gap but does not choose the next schema.** Current tower promotion uses an
   already supplied carrier and explicitly defines no function from residue to carrier content
   [`ReflectionTowerPromotion.lean:12-23`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/ReflectionTowerPromotion.lean#L12),
   [`ReflectionTowerPromotion.lean:77-87`](C:/Users/victo/domainspec-lean-formalization/lean-formalization/ReflectionTowerPromotion.lean#L77).
   The audit likewise kills the claim that observation/residue/score alone determines or justifies
   the next probe or schema while retaining execution under an externally justified policy
   [`lens/reflexivity findings.md:20`](C:/Users/victo/domainspec-lean-formalization/research/audits/lens-reflexivity-bidirectional-refutation-2026-08-11/research/findings.md#L20).

## Contradictions and collapse boundaries

- **Person = lens = schema = functor = instance cannot be one unqualified equation.** `Schema` is a
  category; `Instance S` and `SchemaMorphism S T` are different functor types. A participant is the
  bearer/producer of any of these. “Sometimes” must be indexed by turn, target, source, codomain,
  and role.
- **General lens composition is not yet formalized.** There is no exhibited category of project
  lenses; merely bundling a category into `Lens` is tautological
  [`lens/reflexivity findings.md:12`](C:/Users/victo/domainspec-lean-formalization/research/audits/lens-reflexivity-bidirectional-refutation-2026-08-11/research/findings.md#L12).
  Nor are horizontal joint readouts and vertical tower promotion one double structure: squares,
  two compositions, units, and interchange are absent
  [`lens/reflexivity findings.md:15`](C:/Users/victo/domainspec-lean-formalization/research/audits/lens-reflexivity-bidirectional-refutation-2026-08-11/research/findings.md#L15).
- **Preservation is not recipient adequacy.** A named invariant may survive transport while a
  recipient-wide task separates a collapsed fiber; adequacy requires an image restriction or an
  independent contract [`lens/reflexivity findings.md:13`](C:/Users/victo/domainspec-lean-formalization/research/audits/lens-reflexivity-bidirectional-refutation-2026-08-11/research/findings.md#L13).
- **Composition does not select repair.** Incompatible extensions do not produce a new schema; that
  implication is explicitly refuted in the prior synthesis
  [`minimalism findings.md:149`](C:/Users/victo/domainspec-lean-formalization/research/audits/minimalism-composition-generativity-analogy-limits-2026-08-10/research/findings.md#L149).
- **Different people do not certify different lenses.** The Composition Lab warns that nominally
  different personas/angles may realize the same judgment and that names are not mechanisms
  [`02-composition-strategy.md:228-236`](C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/milestone-1-strategy/02-composition-strategy.md#L228).

## Earliest point categorical language becomes metaphor

The language remains literal through these declarations:

1. an explicit category/schema `S`;
2. an explicit functorial instance `I : S ⥤ Type`;
3. an explicit schema translation `F : S ⥤ T` with laws;
4. reindexing `F* I := I ⋙ F`;
5. common-domain readouts `O_i : X -> Y_i` and their joint kernel.

It becomes metaphor at the **first substitution of a participant for one of those typed values**
without an interface extracting the value and its laws. “Vlad is a schema” is metaphor until a
specific `S_Vlad` is given. “The agent is a functor from Vlad to Victor” is metaphor until source
and target categories, object/morphism maps, and identity/composition proofs are given. “Victor
consumes the agent's instance” is metaphor until the output is a functorial instance or a typed
artifact-to-instance interpretation exists. “Their composition causes a better lens” is an
additional empirical claim requiring a frozen task/baseline and a trace of transformation; the
program itself distinguishes coverage, confrontation, synthesis, selection, and no attributable
effect [`02-composition-strategy.md:40-53`](C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/milestone-1-strategy/02-composition-strategy.md#L40).

## What this adds to the lens program

The strongest usable proposal is a **participant-mediated lens protocol**, not an ontology of
persons:

```text
participant --supplies--> readout/schema/translation/instance
output(q) --conforms-to or is interpreted-as--> instance on S_q
translation F_pq --reindexes--> q-instance into p's schema
joint readouts --may refine--> a predeclared task's observability
residue/extension failure --triggers review of--> an externally justified revision policy
```

This protocol makes three currently vague effects observable: (i) which participant supplied the
distinctions versus populated them; (ii) whether another participant merely read an artifact or
actually transported a typed instance; and (iii) whether the interaction was joint coverage,
sequential translation, confrontation between incompatible extensions, or synthesis under an
extra operator. It should be treated as a candidate instrumentation vocabulary. The Composition
Lab explicitly forbids turning an attractive category-theoretic vocabulary into the theory before
case fit is demonstrated
[`02-composition-strategy.md:227-237`](C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/milestone-1-strategy/02-composition-strategy.md#L227).

## Candidate verdicts

| candidate | witnessed? | sound? | verdict | use-mode |
|---|---:|---:|---|---|
| participant-indexed role alternation | partially | yes, if roles are kept distinct | **GO** | build-from-owned typing/instrumentation candidate |
| mutual instance consumption by pullback | yes as formal mechanism; no named Victor/Vlad/agent episode | yes | **GO/OPEN EPISODE** | already-deployed mechanism, concrete witness still needed |
| participants literally are schemas/functors | no | no without explicit extraction and laws | **KILL as literal claim** | typed negative; retain metaphor only |
| joint participant lenses improve a fixed task | narrowly | yes with common carrier and independent task | **GO narrow** | already-deployed readout theorem; empirical episode open |
| interaction/residue automatically yields next schema | no | no | **KILL/no-witness** | revision policy remains external |
| horizontal participant composition + vertical reflection form one structure | no | no under current types | **KILL/tautological** | future construction only |

One-line answer: the intuition helps most by revealing that a “lens” may be an alternating,
participant-mediated bundle of readout, schema, population, and transport acts; it stops helping
the moment those acts are collapsed into the persons themselves or functoriality is asserted
without typed source, target, maps, and laws.
