# Findings — participants as lenses, schemas, instances, and transformations

## Answer

The intuition is useful, but its strongest literal wording is wrong. Victor, Vlad, and the agent
are not themselves lenses, schemas, instances, or functors. They are participants who can enact
different typed roles at different steps: expose a readout, propose or adopt a schema, populate a
schema, consume an artifact under a schema, or perform a transformation between representations.
The role belongs to the relation and episode, not permanently to the person
([formal return](explorer-formal.md); [operational return](explorer-operational.md);
[review](reviewer.md)).

This helps the lens program by moving its unit of analysis from `Person = Lens` to an observable
event:

```text
actor × episode × task × input × distinction-policy × operation → output/readout
```

A recurrent pattern across events may justify saying that someone often enacts a particular lens.
The person's name alone does not establish one.

## What survives

### 1. Different participants can enact different lenses

The claim is meaningful when each participant produces a distinct, attributable readout or
distinction policy over a named target. Distinct people, personas, or prompts do not suffice: two
participants can realize the same judgment, while the same person can realize different lenses in
different episodes ([formal return, “Contradictions and collapse boundaries”](explorer-formal.md);
[review, §1](reviewer.md)).

A minimal notation is:

```text
P                       participant
L(P,e)                  lens/configuration enacted by P in episode e
S(P,e)                  schema declared or adopted in e
a(P,e) : Inst(S(P,e))   artifact emitted under that schema
T(P→Q,e)(a)             Q's typed transformation/interpretation of a
```

This is not yet a category of lenses. It is an instrumentation vocabulary that keeps the types
apart ([review, §3](reviewer.md)).

### 2. “Being a schema for another” has a sound weaker reading

One participant can supply constraints, distinctions, slots, or admissibility rules that another
participant then instantiates. The participant supplies or induces `S`; the participant is not
identical to `S`. This distinction matters because the schema must be independently inspectable
and must admit distinguishable satisfying or violating instances
([operational return, “Working distinctions”](explorer-operational.md);
[review, “Person as schema”](reviewer.md)).

The adaptive handoff episode witnesses this pattern bilaterally: Victor supplied a bounded set of
constraints; the agent interpreted them through existing research and dispatch contracts and
produced concrete packet/proposal instances. The strongest supported description is
**contract-governed transformation**, not categorical functor
([operational return, episodes 3 and “Smallest positive witness”](explorer-operational.md)).

### 3. Consuming another's instance can become technically precise

The formal repository already owns a literal mechanism. A schema is a small category, an instance
on it is a functor `I : S ⥤ Type`, and a schema morphism `F : S_p ⥤ S_q` lets participant `p`
consume/reindex a `q`-instance by precomposition:

```text
I_q : S_q ⥤ Type
F_pq : S_p ⥤ S_q
consume[p←q](I_q) := I_q ⋙ F_pq : S_p ⥤ Type
```

Identity and composition laws for this pullback are already formalized. What remains absent is a
demonstrated Victor/Vlad/agent episode whose artifacts actually have these types
([formal return, Result and supported claim 1](explorer-formal.md)).

Operationally, “consume” should presently mean: an artifact crosses a declared interface, is
interpreted under a named schema, and changes a fixed task or readout in a traceable way. Without
those conditions it means only reading or communicating
([review, “Instâncias consumidas e síntese”](reviewer.md)).

### 4. A participant may execute a functor, but is not the functor

Calling a transformation a functor requires declared domain and codomain categories, object and
morphism mappings, and preservation of identities and composition. The local prefunctor witness
shows why plausible mappings do not earn that name merely by mapping primitive objects and
generators ([formal return, supported claim 3](explorer-formal.md)).

Therefore:

```text
“the agent is a functor from Vlad to Victor”              — unsupported identity
“the agent executes T from Vlad's schema to Victor's”     — possible typed hypothesis
“T is functorial”                                         — separate proof obligation
```

This separation is useful rather than pedantic: it lets us record what a transformation preserves,
what it loses, and where composition fails.

## What the recent corpus actually witnesses

The corpus supports bilateral Victor–agent alternation. It contains episodes of schema proposal,
interpretation, schema instantiation, revision, synthesis, and formal transformation. Both the
operational explorer and the independent reviewer found concrete witnesses
([operational return, episodes 1–3](explorer-operational.md);
[review, §2](reviewer.md)).

It does **not** contain a bounded recent episode with an independently attributable Vlad input,
output, and subsequent consumption. Vlad appears as collaborator, coauthor, co-leader,
destination, anticipated evaluator, or consumer. Those relations do not prove an enacted lens or
transformation. The trilateral claim is therefore a plausible hypothesis grounded in the user's
testimony, not an observed finding of this corpus
([operational return, Evidence boundary and episode 4](explorer-operational.md);
[review, “Ausência do terceiro vértice”](reviewer.md)).

This is the main evidence gap, not a conclusion that Vlad contributes no distinct lens.

## What this adds to the theory of lens

The result suggests four separations that the lens program should preserve:

1. **Bearer versus enactment:** a participant bears capacities; `L(P,e)` is what was enacted.
2. **Readout versus schema:** a readout makes distinctions visible; a schema constrains admissible
   representations. One may inform the other without being identical.
3. **Instance versus artifact:** an artifact becomes an instance only relative to an explicit
   schema or interpretation contract.
4. **Transformation versus functoriality:** a transformation can be observed before its
   preservation and composition laws are established.

This also sharpens lens composition. At least four neighboring events must not be collapsed:

- parallel readouts over a common target;
- sequential transport between schemas;
- confrontation between incompatible interpretations;
- synthesis by an additional operator.

The formal corpus supports narrow information gain for joint readouts and formal reindexing of
schema instances, but does not yet unify horizontal readout composition with vertical reflection,
nor does residue choose the next schema
([formal return, supported claims 2 and 6](explorer-formal.md)).

## Operational proposal

Instrument one future three-person episode with this minimal record:

```yaml
episode:
  task: fixed before interaction
  participant: Victor | Vlad | agent
  input: attributable artifact/reference
  enacted_lens:
    distinction_policy: what this step can separate or notice
    readout: produced observation or judgment
  schema_role: proposed | adopted | none
  artifact:
    schema_ref: independently inspectable schema
    instance_ref: concrete output under it
  transformation:
    source_schema: optional
    target_schema: optional
    preserved: declared property
    lost_or_residual: observed difference
  downstream_effect: change in the fixed task/readout
```

Do not call `transformation` a functor initially. Promote it only if mappings and laws are supplied.
This one record would distinguish whether the three participants contribute independent lenses,
whether they instantiate or revise one another's schemas, and whether “consumption” changes the
joint capability rather than merely aggregating text.

## Collapse test

The proposal collapses to ordinary collaboration terminology if all of the following hold:

1. replacing lens with frame/prompt/perspective changes no prediction or admissible evidence;
2. no schema exists independently of the participant;
3. no typed transformation has a testable preservation or loss claim;
4. no independently fixed task changes after consuming another output; and
5. roles can only be assigned retrospectively from the final result.

Under those conditions, observer + role + interface + interpretation already owns the phenomenon;
the categorical vocabulary adds no consequence
([review, §5](reviewer.md)).

## Verdict matrix

| candidate | owner | witnessed? | sound? | verdict | use-mode |
|---|---|---:|---:|---|---|
| participant-indexed role alternation | local conversation episodes and `DialogueStep`/lens research | bilateral | yes when episode-indexed | **GO** | build-from-owned instrumentation |
| participants literally are lenses/schemas/functors | local type owners | no | no; type collapse | **KILL** | typed negative; retain only qualified metaphor |
| mutual instance consumption by reindexing | `SchemaInstance.lean` | formal mechanism yes; human episode no | yes | **GO / OPEN EPISODE** | already-deployed mechanism awaiting case fit |
| Victor–agent schema/instance/transformation chain | recent conversations and artifacts | yes | yes | **GO** | contract-governed transformation |
| trilateral Victor–Vlad–agent chain | user testimony only in bounded corpus | no attributable Vlad vertex | open | **NO FINDING YET** | preregister one episode |
| interaction or residue automatically selects the next schema | reflection/lens audits | no | no | **KILL** | revision policy remains external |
| joint lenses improve an independently fixed task | observation-budget result | narrowly | yes under common carrier/task | **GO NARROW** | owned theorem; empirical validation open |

## Current position

The best formulation is: **Victor, Vlad, and the agent are situated participants who may enact
different lenses and alternate among schema-proposal, instantiation, interpretation, and
transformation roles. Their outputs—not their persons—can be instances, and transformations they
execute may later be proven functorial.** This turns the intuition into an observable protocol
without pretending that the current corpus already contains a category of people or a witnessed
three-person functorial system.

