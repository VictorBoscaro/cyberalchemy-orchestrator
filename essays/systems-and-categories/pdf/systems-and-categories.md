# Systems and Categories

## Toward Domain Languages

*An essay on representation, composition, and the construction of domain languages.*


<!-- FIGURE PLACEHOLDER: cover mark (embedded image 1 in the source DOCX) -->

Victor Boscaro
ResonantOS
<!-- READER ORIENTATION -->

## 0. When a Domain Needs a Language

The objective of this document is to introduce a way of representing domains in natural language so that language-model agents can perform complex work within them. Complex work begins with an intention. The situation then reveals what must be understood before that intention can become action.

A company sees its revenue fall and asks an agent to investigate the cause. Revenue is an abstraction: it compresses many events into one measure. The investigation becomes concrete as it traces the decline back to what happened in the business. The cause determines which action becomes relevant.

Practitioners move between these levels of abstraction through experience. They connect a high-level result to the situations that produced it. They also know which distinction changes the next question. An agent encounters this structure through language.

Natural language carries the initial expression of the domain. People use it to describe events, explain causes and correct previous interpretations. An agent can use those expressions to move from an objective toward the concrete conditions that determine what should happen next.

Systems thinking helps us understand a whole by examining how its parts relate to one another. Category theory helps us examine what must be preserved when the same situation is represented in different contexts. Together, they help develop languages through which humans and agents can move between an intention, the context it inhabits, and the work required to act on it.

## 1. How Representations Shape Action

A company can represent the same problem from different perspectives. A decline in sales may first be represented as an acquisition problem. Analysis shows, however, that acquisition remains stable and that customers simply are not returning. A further investigation may reveal that customers are not returning because orders repeatedly arrive later than promised.

What began as a problem of advertising is now better described as a relation between the promise made to customers and the operation expected to fulfill it. Each representation did more than change how the problem was described. It changed what became visible, which questions mattered, and which courses of action appeared possible.

This is not a special feature of business problems. A representation becomes useful by keeping some differences visible while leaving others aside. Separating new from returning customers changes the investigation because it rules out one explanation. The selection changes what can be distinguished and therefore changes what can be asked or done. How a problem is represented helps determine which distinctions are relevant and which courses of action appear reasonable.

> **CENTRAL QUESTION**  
> *Which representation, or combination of representations, is adequate to the situation and the task at hand?*

The same situation can support several coherent representations, each making different relations visible and opening a different path of investigation. A representation that was adequate at one stage may cease to be so as the problem changes. What matters, then, is not whether a local representation is coherent in isolation, but whether its explanation still holds when the relations outside its boundary are brought back into view.

<!-- SYSTEMS AND CATEGORIES -->

## 2. Two Views About Structure

Systems thinking begins where a locally coherent explanation stops being enough. When an event keeps returning despite apparently reasonable interventions, its recurrence may be produced by relations that lie outside the boundary of the original explanation. The event is then less informative than the structure that keeps producing it.

When a problem persists in this way, attention shifts from isolated events to the pattern they form over time. Understanding that pattern requires tracing what accumulates, what changes those accumulations, and how those changes reshape what happens next. Feedback and delay matter because consequences may return through the system long after the decisions that produced them have disappeared from view (Forrester, 1961; Sterman, 2000).

The boundary of a model matters because it determines which consequences remain visible. A department can improve its own metric while making the larger organization perform worse. The kind of intervention matters as well: changing a parameter does not alter a system in the same way as changing a rule or the objective that organizes it. Systems thinking therefore asks both how local decisions participate in the behavior of a larger structure and which part of that structure an intervention actually impacts (Meadows, 1999; 2008).

Understanding the larger system reveals why the sales and fulfillment problems belong to the same explanation. But drawing a wider boundary around the problem, connecting sales and fulfullment, does not yet produce a model of how its parts work together. Building a common account requires an explicit interface between them and a rule for composing their structures. Systems thinking makes this connection necessary, but it does not, by itself, provide a general formal account of how models compose through their interfaces.

Category theory becomes useful for this second problem because it provides a language for relations, transformations, and composition. Once each representation has been given an explicit structure, we can ask which mappings between them are admissible and what those mappings must preserve. Systems thinking helps us investigate how relations within a system produce behavior; category theory helps us make precise what is claimed when one structured description is translated into, connected with, or composed with another. (Spivak, 2014; Fong & Spivak, 2019).

A categorical description does not tell us which boundary of a real system was appropriate or whether a causal interpretation is empirically justified. A systems model does not automatically provide a rigorous notion of equivalence between its different representations. The bridge is useful because each tradition exposes an obligation that the other can leave implicit.

<!-- ANALOGY AND FORMAL TRANSLATION -->

## 3. Translation Is a Claim About Preservation

Analogy often arrives before formal translation. A structure in one domain resembles something already understood elsewhere, and the resemblance suggests that certain relations may correspond. This is one reason analogies are cognitively productive: they allow a familiar organization to direct attention before we know whether the proposed correspondence is exact. But an analogy earns more trust by surviving pressure, not by accumulating similarities after the fact (Gentner, 1983; Hesse, 1966).

The pressure begins when we ask what the analogy must preserve. If two elements appear to correspond, do the relations between them correspond as well? If two transformations can be performed in sequence on one side, what happens to that sequence on the other? At this point resemblance begins to acquire obligations, and the transition from analogy to candidate translation becomes something we can inspect rather than merely admire.


<!-- FIGURE PLACEHOLDER: Figure 1 (embedded image 2 in the source DOCX) -->

*Figure 1. Analogy can suggest a correspondence; a formal translation adds preservation obligations.*

A category provides a minimal language for these obligations. Its objects are connected by morphisms, and those morphisms come with identities and a rule of composition. A functor translates from one category to another while preserving that compositional structure. The important point is not the terminology itself; it is that a translation can now fail for a reason that the formalism can name.

This also gives technical force to the word equivalence. Two categories do not need literally identical objects to express the same categorical structure, but an equivalence requires that the relevant relationships be preserved and recoverable and that the target be covered up to isomorphism. Even this strong result remains relative to the structure that was represented. If authority, timing, or another distinction is added later, a translation that was previously adequate may cease to be equivalent at the enriched level.

The consequence is methodological. We should resist the question "are these representations equivalent?" until we can say which structure is being compared and why that structure is enough for the task. Formal equivalence can then become a precise result rather than a vague declaration of sameness, while a failed equivalence becomes information about what the thinner representation was unable to carry.

<!-- PROGRESSIVE FORMALIZATION -->

## 4. The Language Belongs to the Domain

The previous section assumed that we already knew which objects and transformations deserved to be represented. Real domains rarely begin with that clarity. They begin with distinctions embedded in practice, and the need for formal language usually appears because leaving one of those distinctions implicit has started to produce ambiguity that matters. Formalization should therefore respond to pressure from the domain rather than treating the domain as raw material for a preselected ontology.

Consider a domain in which two actions look operationally similar but differ because only one was authorized. If that difference affects what can legitimately happen next, the language needs a way to preserve it. A typed relation may be enough at first. Only when relations themselves must be chained, compared, or constrained does the domain acquire a reason to introduce stronger compositional laws.

This suggests a gradual progression rather than a categorical starting point. Ordinary vocabulary can become a typed graph when the endpoints of relations need to be explicit. Some families of relations may later acquire signatures that restrict which compositions are meaningful. If identities and associative composition genuinely belong to the domain, then asking whether part of the language forms a category becomes a mathematical question rather than a stylistic choice.

The word "genuinely" carries most of the burden. Drawing arrows does not create composition, and naming a workflow step a morphism does not make categorical laws true. The formal language should grow only when a new law constrains something that the domain actually cares about. Otherwise formalism becomes decorative and begins to conceal assumptions behind notation.

A common infrastructure should respect the same boundary. It may need a small language for relations that are truly transversal, such as the ability to reconstruct how one piece of work depends on another. It should not absorb every local primitive simply because those primitives can be represented. Domain languages remain useful precisely because they preserve distinctions whose meaning is local, and the shared layer should make interaction possible without pretending that local semantics have become universal.

<!-- COMPOSITIONAL SYSTEMS MODELING -->

## 5. Where the Bridge Is Already Mathematical

The relation between systems thinking and category theory becomes more than analogy in specific modeling languages. A line of work on compositional System Dynamics has formalized stock-and-flow diagrams so that their syntax can be manipulated mathematically rather than treated only as a drawing convention. In this setting, composition and stratification are operations with explicit structure, and a model can be assembled from parts without rebuilding the whole language informally each time (Baez et al., 2022a; Baez et al., 2022b/2024).

This matters because it separates the diagram from any single interpretation placed on it. The same structural language can support different semantics, while the rule used to interconnect parts remains explicit. Li and collaborators extend this direction into a broader compositional account of System Dynamics diagrams and practice, while related work by Libkind and collaborators represents dynamical systems through algebras of wiring diagrams (Li et al., 2025; Libkind et al., 2021).

The strongest lesson is not that all systems thinking has secretly become category theory. It is that a sufficiently specified systems language can acquire a categorical semantics in which composition does real mathematical work. Once that happens, the semantics of a composite can be constrained by the semantics of its parts and by the rule through which they were connected, which makes modularity more than an informal engineering preference.


<!-- FIGURE PLACEHOLDER: Figure 2 (embedded image 3 in the source DOCX) -->

*Figure 2. Syntactic validity, compositional semantics, and empirical adequacy are related questions, not interchangeable claims.*

The result also clarifies where mathematics stops. A diagram may be syntactically well formed, and its chosen semantics may preserve composition, while the model still fails to describe the empirical phenomenon adequately. These are different questions because the first concerns the representation, the second concerns a mathematical interpretation of that representation, and the third concerns the relation between the interpretation and the world. A proof of the second cannot be silently promoted into evidence for the third.

This separation gives the bridge its proper strength. We have concrete cases in which domain structure has become categorical, so the proposal is not merely philosophical. At the same time, those cases show why the stronger claim must remain local: the formalism becomes powerful after the modeling language has specified what counts as structure, not before.

<!-- RUPTURE AND RESIDUE -->

## 6. When a Representation Stops Being Enough

A representation often reaches its limit without becoming useless. Imagine a model that has supported a recurring decision well because every distinction needed by that decision is preserved. A new task then appears, and two situations that the model treats as identical now require different actions. The problem is not necessarily that the old model was wrong; a distinction that was previously safe to compress has become relevant.

This failure is different from an incorrect instance. If a number was entered badly, correcting the number may restore the model without changing its language. If the language itself cannot express the distinction on which the decision now depends, no correction to an instance can solve the problem. The representation has reached a boundary that only became visible from the new task.

We can call the newly exposed difference a residue of the representation or translation. The term is useful only if it remains modest. A residue says that something relevant was not preserved; it does not tell us which richer schema should replace the current one. Several revisions may explain the same failure, and the observation that triggered the rupture may itself be noisy or incomplete.

This is where the discipline of analogy becomes useful again. A promising analogy should be pushed until we can say where the transported structure stops working, because the break often reveals a distinction that the resemblance had hidden. The same principle applies to formal models. A framework that grows after every surprise can become increasingly difficult to refute while explaining everything retrospectively, so preserving the failure is often more informative than immediately patching it.

The next move is therefore investigative rather than automatic. We need to understand what became distinguishable, why that difference now matters, and what further observation could separate competing revisions. Only then does enrichment become a justified change in the language. Sometimes learning adds structure; sometimes it consists in discovering exactly where the existing structure should stop.

<!-- MAKING THE REGIME OF INVESTIGATION EXPLICIT -->

## 7. Lenses

The essay has already changed how it looks at the same object several times. Systems thinking reorganized attention around behavior that emerges through relations over time, while category theory reorganized the problem around translation and preservation. The discussion of domains changed the focus again by asking which distinctions a language has earned the right to represent. There is a common role being played by these changes, and only now do we need a name for it.

A lens is used here as a working concept for a structured way of making some distinctions and relations salient enough to guide investigation. The term does not compress an entire discipline into a single object. A discipline contains far more than any one investigation can mobilize, so the systemic lens used in this essay is only a particular selection from systems thinking, just as the categorical lens is a selection from category theory.

This distinction helps explain reframing. When the sales problem moved from acquisition to retention and later to operational capacity, the change was not simply verbal. Different relations became relevant enough to govern the next question, which changed the space of plausible action. A frame can therefore be understood as the situated application of one or more lenses to a particular task rather than as a universal description of the object.

<!-- FIGURE SPECIFICATION: SAME SITUATION, DIFFERENT LENSES
Two panels use the same underlying sales/fulfillment network. The systemic lens highlights promise, capacity, delay, retention, and behavior over time. The categorical lens highlights representations, translations, composition, and preservation. Unselected relations remain visible in gray. Do not add a "domain lens."
-->

*Figure 3. The same situation under different lenses: the object remains, while different relations become salient enough to govern the next question.*

The lens also leaves a trace in the knowledge it helps produce. If a mode of investigation consistently separates some cases while collapsing others, observations made through it can contain information about the lens as well as about the object. A recurring blind spot may therefore indicate a limitation in the representation that was chosen to observe the phenomenon, not merely a missing fact inside the phenomenon itself.

This reflexive possibility is important, but the formal claim should not outrun the concept. We have not established that lenses themselves form a category, nor even that there is one correct formal carrier for every kind of lens. What has been earned here is smaller: lenses can be treated as objects of investigation once their effects on distinctions and questions become explicit enough to compare.

<!-- FROM REPRESENTATION TO ACTION -->

## 8. Work and Knowledge

Representations are rarely built only to be contemplated. They become part of work, and this introduces a different reason to care about what remains preserved. An intention can exist before the work needed to realize it is fully understood; as effort proceeds, the objective acquires internal structure because some uncertainties become questions and some questions become bounded pieces of work. The process is not merely execution of a fixed plan, since the work itself can change what the objective means.

Locality makes this possible. A person or system needs a bounded problem on which action can occur without reconstructing the entire history of the larger effort before every move. But the same local autonomy that makes focused work possible creates a risk: a task can remain internally coherent even while its connection to the broader objective weakens. Nothing inside the local boundary necessarily reveals that divergence.

This is where knowledge becomes more than stored information. In the sense needed here, knowledge preserves enough of the relations around the work for a result to remain interpretable beyond the moment that produced it. When understanding changes, the earlier state should not disappear as though the current account had always been obvious; the path matters because it tells us what the result depended on and when it is safe to reuse.

Work and knowledge therefore move differently but cannot be separated cleanly. Work changes something in the world or in an artifact, while knowledge preserves the structure through which that change can still be understood. As execution becomes more distributed, the amount of context that exists around the work increases even though no local execution should need all of it at once.

The requirement is not to materialize the whole context everywhere. That would destroy the locality that made work possible. What is not locally present should instead remain recoverable, so that a person can move from an objective toward the work through which it is being pursued and later return from a result toward the conditions that gave the result its meaning. Some connections will remain uncertain or missing, and a useful system should preserve those gaps rather than filling them with an invented coherence.

<!-- A DESIGN DIRECTION -->

## 9. An Infrastructure for Work and Knowledge

Increasing the capacity to perform work creates a coordination problem of its own. More can happen, but the surrounding context also becomes larger, and a person can easily end up spending the gain in execution capacity on the effort required to keep the work coherent. A useful infrastructure should change that relation by allowing the scope of work to grow without requiring the user's cognitive burden to grow at the same rate.

The human-facing boundary of such a system can be understood as an orchestrator. A person begins from an intention that may still be incomplete, and the orchestrator helps turn that intention into a sufficiently bounded next movement without requiring the person to manage every internal operation. Its value is not that it performs all work itself, but that it preserves continuity between what the user is trying to accomplish and the work that becomes possible as the situation develops.

That continuity depends on selective context. A local execution should receive enough of the larger history to remain faithful to its purpose, while the rest stays recoverable rather than being forced into every local window. This distinction is more than an efficiency trick. If the omitted context contained a constraint that should have governed the action, the execution can be locally correct and globally wrong, which means that choosing what to materialize is part of how the work is governed.

The same separation is necessary between knowledge and authority. A system may be able to recover why a decision was made without being entitled to remake it, just as access to a description of a capability does not itself grant permission to exercise that capability. Delegation becomes safer when the infrastructure can preserve these relationships explicitly instead of inferring authorization from proximity or convenience.


<!-- FIGURE PLACEHOLDER: Figure 3 (embedded image 4 in the source DOCX) -->

<!-- FIGURE SPECIFICATION: TRANSVERSAL LANGUAGES -->

*Figure 4. Domain languages can participate across intention, orchestration, bounded work, and effect, while context preserves the translations and limits that keep them interpretable.*

<!-- TODO: Revise Figure 3 and the surrounding Section 9 language so domain languages are shown across intention, orchestration, bounded work, effect, and recoverable context/knowledge—not as belonging only to Local Work. -->

Domain languages do not sit only inside local work. They can shape how an intention is expressed, how orchestration translates and bounds it, how work proceeds, and how effects return in interpretable form. Their participation need not be uniform: different languages may appear at different stages, with different authority and precision.

A domain language is therefore not a container around local work. It is one of the structures through which intention, work, and effect remain mutually interpretable. Recoverable context should preserve which languages and translations were in force—including their scope, version, and unresolved mismatches—without promoting local semantics into a universal ontology.

Lenses can be treated similarly as available capacities rather than compulsory frames. The system may help make a particular way of investigating a problem available when it becomes relevant, but availability should not silently become obligation. If the infrastructure chooses the questions and standards through which every problem will be interpreted, reducing cognitive load has turned into determining the user's frame rather than supporting it.

The design direction is therefore not simply "more automation." It is an infrastructure in which local work can remain genuinely local while the larger structure that gives it meaning stays recoverable. That makes it possible to increase capacity without abandoning the distinctions that allow a person to understand what happened, contest a path when necessary, and continue the work from a changed understanding rather than from an invented clean slate.

<!-- REFLEXIVE TURN -->

## 10. Coda: The Lens Turns Back

The essay began with a company whose falling sales could become different problems depending on how the situation was described. We can now see that the example was doing more than illustrating representation. The object had not simply changed; different relations had become capable of governing the investigation. The essay itself has been changing what could be seen. Systems thinking made behavior over time harder to ignore; category theory made it harder to take for granted what survives when one representation becomes another.

There was also a quieter constraint on the argument. Whenever an analogy seemed capable of carrying more than it had earned, or a formal result invited a stronger conclusion, the investigation had to ask what was actually warranted. That restraint was epistemological: it governed what could responsibly be concluded from the representations already available.

Seen retrospectively, systems thinking and category theory were doing more than supplying concepts. Each organized attention differently, bringing some distinctions forward while leaving others less visible. This is the limited sense in which the essay can now speak of lenses. Once that role becomes explicit, the direction of inquiry can reverse: the structures through which we investigate can themselves become objects of investigation.

<!-- APPENDIX -->

## Appendix A. Claim Ledger

The ledger below records the standing of the claims that carry the short essay. It is intentionally smaller than the ledger of the longer investigation: the purpose here is to make visible where the argument relies on established literature, where it offers an interpretive synthesis, and where it remains a design or research proposal.

| Claim | Standing | Boundary |
| --- | --- | --- |
| Representations become usable through selection, so their adequacy is task-relative. | Working epistemic premise | Does not imply that every omitted distinction matters for every task. |
| Systems thinking and category theory share a concern with relational structure. | Interpretive synthesis | The overlap is productive but does not establish a global equivalence. |
| Specific System Dynamics languages admit categorical formalization and compositional operations. | Established literature | Applies to specified modeling languages; it is not a theorem about systems thinking as a whole. |
| A categorical equivalence is relative to the structure represented in the categories. | Standard mathematical point | Adding new structure can invalidate an equivalence that was correct at a thinner level. |
| Formal coherence does not imply empirical adequacy. | Structural distinction | The relation between a model and the world requires its own evidence. |
| A domain need not begin as a category. | Methodological position | Categorical structure should be asserted only when objects, admissible transformations, identities, and composition laws are justified. |
| A residue marks a relevant distinction that the current representation fails to preserve. | Working definition | A residue constrains investigation but does not determine its own repair. |
| A lens makes selected distinctions and relations salient for an investigation. | Working definition | Salience does not by itself warrant a conclusion, and no category of lenses is established here. |
| Lenses form a category. | Open question | No general LensSpec with objects, transformations, identities, and composition laws is established here. |
| Domain languages may participate across intention, orchestration, work, and effect. | Architectural thesis | This does not imply that every language is present, globally available, or equally authoritative at every stage. |
| Intention, work, effect, and knowledge should remain mutually interpretable as execution becomes distributed. | Architectural thesis | The minimal structure required to preserve those relations remains a design question. |
| An infrastructure can reduce coordination burden while preserving recoverability and human control. | Design hypothesis | Requires empirical evaluation against quality, autonomy, and cognitive load. |

<!-- APPENDIX -->

## Appendix B. Open Questions

### Formation and Revision

#### When is a domain distinction strong enough to enter the language?
Sections 4 and 6 make formalization answer to consequences rather than completeness. Both premature structure and prolonged ambiguity carry costs. An adequate criterion would distinguish recurring inconvenience from failures of reasoning, coordination, or composition that justify a durable distinction.

#### When should a distinction remain informal?
A language that grows with work need not absorb every recurring difference. Some distinctions may be tacit, contested, unstable, or too costly to maintain. A useful account would explain when explicitness improves action and when it falsely stabilizes what should remain revisable.

#### How should a failed representation be revised?
Section 6 distinguishes rupture from an incorrect instance, but a residue may also reflect environmental change or weak measurement. Revision therefore needs competing explanations and observations capable of separating them; enrichment should not be automatic.

### Lenses and Translations

#### What must a translation between domain languages preserve?
Sections 3 and 9 make translation central without assuming a universal schema. Work can cross domains fluently while losing authority, temporal order, provenance, or uncertainty. An adequate account would state which obligations are task-relative and how losses remain visible.

#### How do multiple lenses coexist or conflict in one investigation?
Section 7 allows more than one lens to make relations salient, but their questions may pull inquiry in incompatible directions. A useful account would distinguish complementarity from conflict and explain how choices are governed without treating one lens as total.

#### What must remain stable for two applications to count as the same lens?
The working concept joins selected distinctions with a mode of inquiry. Clarifying identity matters before comparison or composition can become rigorous. An answer should separate contextual variation from a change of lens.

### Infrastructure and Governance

#### How do multiple domain languages participate in the same work?
Section 9 allows languages to participate across intention, orchestration, work, and effect. Their distinctions may overlap or conflict. An adequate account must locate translation, preserve disagreement, and state who may accept a translation.

#### What does recoverable context mean operationally?
Sections 8 and 9 rely on context that need not be locally present. The claim becomes testable only if recovery is specified by actor, permission, version, latency, and fidelity, including how missing or uncertain links remain visible.

#### How can the infrastructure hypothesis be evaluated empirically?
Section 9 proposes reducing coordination burden while preserving recoverability and human control. Evidence should compare alternatives using context loss, correction cost, cognitive burden, autonomy, and the ability to reconstruct or contest a path.

<!-- APPENDIX -->

## Appendix C. Minimal Glossary

**Representation.** A selective structure through which some distinctions and relations in an object become available for reasoning or action.

**Category.** A mathematical structure with objects and morphisms together with identities and associative composition.

**Functor.** A translation between categories that preserves identities and composition.

**Equivalence.** A categorical relation expressing recoverability of categorical structure without requiring literal identity of objects.

**Domain language.** A vocabulary and structural grammar developed around distinctions that matter within a particular domain. It may participate across several stages of work and in translations with other languages without becoming globally authoritative.

**Translation.** A movement between structured representations that makes explicit what is intended to be preserved. It is not necessarily a functor unless the relevant categorical structure has been established.

**Schema.** An explicit description of the distinctions and relations admitted by a representation.

**Residue.** A difference that has become relevant but is not preserved by the current representation or translation.

**Lens.** A working term for a structured way of making selected distinctions and relations salient during investigation; it does not determine everything that can be expressed.

**Frame.** A situated, temporary, and revisable application of one or more lenses to a particular problem, task, and context.

**Work.** The movement through which an intention is pursued toward an effect.

**Knowledge.** The recoverable structure that allows work and results to remain interpretable beyond their immediate execution.

**Orchestrator.** The human-facing coordinating boundary of the proposed infrastructure, responsible for relating an intention to the work that becomes necessary without requiring the user to manage every internal operation.

## References

- Baez, J. C., Li, X., Libkind, S., Osgood, N. D., & Patterson, E. (2022a). Compositional Modeling with Stock and Flow Diagrams. arXiv:2205.08373.

- Baez, J. C., Li, X., Libkind, S., Osgood, N. D., & Redekopp, E. (2022b/2024). A Categorical Framework for Modeling with Stock and Flow Diagrams. arXiv:2211.01290.

- Fong, B., & Spivak, D. I. (2019). An Invitation to Applied Category Theory: Seven Sketches in Compositionality. Cambridge University Press.

- Forrester, J. W. (1961). Industrial Dynamics. MIT Press.

- Gentner, D. (1983). Structure-Mapping: A Theoretical Framework for Analogy. Cognitive Science, 7(2), 155-170.

- Hesse, M. B. (1966). Models and Analogies in Science. University of Notre Dame Press.

- Li, X. (2025). Enabling Compositional System Dynamics Modeling via Category Theory. Doctoral dissertation.

- Li, X., Patterson, E., Mabry, P. L., & Osgood, N. D. (2025). Compositional System Dynamics: The Higher Mathematics Underlying System Dynamics Diagrams & Practice. arXiv:2509.18475.

- Libkind, S., Baas, A., Patterson, E., & Fairbanks, J. (2021). Operadic Modeling of Dynamical Systems: Mathematics and Computation. arXiv:2105.12282.

- Meadows, D. H. (1999). Leverage Points: Places to Intervene in a System. Sustainability Institute.

- Meadows, D. H. (2008). Thinking in Systems: A Primer. Chelsea Green.

- Spivak, D. I. (2014). Category Theory for the Sciences. MIT Press.

- Sterman, J. D. (2000). Business Dynamics: Systems Thinking and Modeling for a Complex World. McGraw-Hill.

- Sterman, J. D. (2002). All Models Are Wrong: Reflections on Becoming a Systems Scientist. System Dynamics Review, 18(4), 501-531.

---

Victor Boscaro
ResonantOS
