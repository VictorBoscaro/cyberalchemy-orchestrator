# Research corpus: minimal meeting ontology exploration

This file preserves the six independent attempts verbatim. Each section heading records the source path; no synthesis or correction has been introduced into the preserved text.

## Source: `attempts/a-authority.md`

# Authority-boundary attempt: a minimal meeting ontology

## Boundary and conclusion

This is a tentative, pre-validation proposal for synchronous meeting occurrences.  Its narrow test
is whether a record can say separately: who was present, who actually took part, what advice was
offered, and what determination was made with authority.  Four concepts suffice for that test;
the authority grant itself is a qualified relation, not a fifth concept.

## Concepts

| Concept | Tentative definition | Why irreducible | Exact loss if removed |
| --- | --- | --- | --- |
| **Meeting occurrence** | One bounded synchronous gathering in which presence, participation, recommendations, and decisions can be situated. | The other distinctions need a common event boundary; neither a recurring forum nor a calendar label identifies this particular encounter. | A record cannot tell whether the same person, advice, or determination belongs to this meeting rather than another occurrence. |
| **Agent** | A person or named collective that can be present, participate, offer advice, or exercise delegated decision authority. | The model must attribute those different relations to a bearer without assuming that all activity is individual or that every attendee is authorized. | Presence, participation, recommendations, and decisions become unattributed, so an attendee list can be mistaken for a list of contributors or decision-makers. |
| **Recommendation** | A non-binding advisory proposition offered for another agent or authorized process to consider. | Its intended effect is influence rather than commitment, which cannot be represented by presence, participation, or a decision. | Advice is either discarded or recorded as a decision, making recommendation look like authority. |
| **Decision** | A determination that commits its authorized maker within an explicitly bounded scope. | Commitment under authority is materially different from advice, discussion, or a facilitation act. | A meeting can record that something was said but cannot distinguish a binding determination from a recommendation or informal consensus. |

## Necessary typed relations

Only the following relations are needed for this narrow boundary:

| Relation | Meaning and constraints |
| --- | --- |
| `Agent present-at Meeting occurrence` | Records attendance or observership only; it grants neither participatory nor decision rights. |
| `Agent participates-in Meeting occurrence` | Records a substantive meeting act, such as speaking, facilitating, or contributing; it does not by itself grant authority and, for this synchronous scope, entails presence at that occurrence. |
| `Agent offers Recommendation in Meeting occurrence` | Attributes advice to an agent and situates it; the recommendation remains non-binding until an authorized decision is made. |
| `Agent makes Decision in Meeting occurrence` | Attributes a determination to an agent and situates it. |
| `Agent authorized-to-decide in Meeting occurrence` | A qualified relation whose required attributes are *granting source* and *scope*; a `makes Decision` assertion counts as authoritative only when this relation applies within that scope. |

The last relation is intentionally not a generic `authority` concept: it expresses a contingent,
scoped grant between an agent and an occurrence.  Its source, scope, expiry, and delegation path
are attributes of that relation when the governing process requires them.

## What is not a concept here

- **Presence** and **participation** are relations, not kinds of people or meetings; their being
  separate prevents attendance from silently becoming contribution.
- **Authority** is the qualified `authorized-to-decide` relation, not a label attached to a forum,
  organizer, or attendee list.
- **Observer, participant, facilitator, recommender, and decider** are labels or relation-derived
  roles, not additional concepts.
- **Inform, advise, recommend, and decide** are values/effects.  Only recommendation and decision
  need objects here because the record must retain what was advised or determined; `inform` needs
  no durable object for this boundary.
- **Forum, recurring series, meeting family, format, access, preparation, memory, transparency,
  recording, and contribution** are attributes, relations, labels, mechanics, or external policy
  concerns unless later evidence shows they are required to resolve one of the four confusions.

## Small optional proposals

- Add an `access-permitted` relation only if the meeting inventory shows that eligibility to enter
  is repeatedly confused with actual presence.
- Add a recurring-series concept only if stable rules must be inherited across occurrences rather
  than recorded as occurrence attributes or external policy.
- Give recommendations and decisions stable record identifiers only when memory, review, or
  contestation requires cross-occurrence reference.

## Deliberate omissions

- No meeting-family taxonomy or format classification.
- No policy that meetings are open, recorded, transparent, or consensus-based.
- No inference from participation or attendance to contribution, reward, membership, or authority.
- No claim that these four concepts are final, ratified, or novel; the specified evidence remains
  candidate and has not yet been tested against real cases or participant language.

## Source: `attempts/a-operation.md`

# Minimal meeting ontology — organizer/operation attempt A

## Boundary and test

This is a tentative four-concept ontology for the organizer's job: convene a meeting, run one
occurrence, and preserve what it usefully changed.  It does not treat the current candidate
vocabulary as ratified, and it does not assert a policy for access, authority, privacy, or
retention.

## Concepts

| Concept | Tentative definition | Why irreducible | Exact loss if removed |
| --- | --- | --- | --- |
| **Meeting context** | An enduring organizer-facing identity that supplies the standing reason and repeatable arrangements for related meeting instances. | A repeating forum must retain continuity independently of any one date. | A recurring meeting becomes either many unrelated instances (losing standing purpose and stable arrangements) or one overwritten record (losing occurrence history). |
| **Meeting instance** | One bounded synchronous convening at which people are brought together to pursue a stated objective. | Convening and running happen at a particular time and require a distinct operational unit. | There is no object to schedule, invite people to, facilitate, or attach an actual result to; a context alone cannot say what happened on a date. |
| **Participant** | An external actor referenced in relation to a meeting instance because their presence or permitted contribution affects how it can run. | A meeting is not operationally convened without identifying who may be involved. | Invitations, facilitation, contribution boundaries, and accountability collapse into unaddressed prose, so the organizer cannot determine who is expected or permitted to do what. |
| **Result** | A durable, addressable post-meeting item that states a change, commitment, question, or other follow-on matter worth carrying forward. | Preserving useful meeting value requires an object more specific than an undifferentiated note or recording. | Notes may remain, but no part can be reliably found, assigned, revisited, or connected to later work; the meeting's useful residue is not operationally preserved. |

## Necessary typed relations

- `Meeting instance —realizes→ Meeting context` (zero or one context per instance): preserves a series when it exists without requiring every ad hoc meeting to belong to one.
- `Participant —participates in→ Meeting instance` (many-to-many): relation qualifiers carry capacity and boundary information, such as invited, observer, contributor, facilitator, or delegated decider.
- `Meeting instance —yields→ Result` (zero-to-many): makes the retained residue traceable to the occurrence that produced it.

## Not concepts in this attempt

- **Purpose/objective, topic, time, cadence, format, preparation, access, and memory policy** are attributes of a context or instance: they describe a thing or its handling, but do not require independent identity to operate this core.
- **Observer, speaker, facilitator, recommender, and decider** are values of the participation relation's capacity qualifier, not kinds of participant or meeting.
- **Inform, advise, recommend, and decide-within-delegated-scope** are values describing the effect permitted by a participation arrangement or result; they are not authority concepts in this minimal core.
- **Decision, action, open question, insight, and record** are result types or labels.  A note, agenda, transcript, or recording is evidence or storage mechanics for a result (and may be absent), not the preserved result itself.
- **Work/community-life families, forum, transparency, privacy exception, contribution, and reward** are labels, policies, external governance, or later classifications.  They may matter, but this organizer core can represent their chosen values without elevating them to concepts.

## Small optional proposals

- Give each `Result` a status and a responsible participant reference when follow-through is needed.
- Let a meeting context own default participation capacities and retention expectations, with an instance allowed to state exceptions.
- Test whether a separate `Decision` concept becomes necessary only if downstream governance must distinguish decisions from all other results by more than a type value.

## Deliberate omissions

- No meeting-family taxonomy or format hierarchy.
- No separate access, authority, preparation, memory, privacy, or documentation concept.
- No rule that a meeting is public, recorded, recurring, decisive, or contribution-bearing.
- No claim that these four concepts are sufficient beyond the bounded organizer/operation use case; real-case and participant validation remain necessary.

## Source: `attempts/a-participant.md`

# Participant attempt: the smallest meeting ontology

## Boundary and status

This is a tentative participant-facing core, derived from the supplied candidate views rather than
a policy or a claim about actual meeting practice.  It answers only: *what is this meeting, why
does it exist, and what is my relationship to it?*  It uses five concepts because the supplied
views make a specific distinction load-bearing: entry, active involvement, and decision effect do
not follow from one another.

## Concepts

| Concept | Tentative definition | Why irreducible | Exact loss if removed |
| --- | --- | --- | --- |
| **Meeting** | A bounded synchronous gathering to which people can stand in a stated relationship. | It is the common referent for purpose and all participant boundaries; neither a calendar label nor a recurring context can replace the particular gathering. | There is no identifiable thing that a person can attend, understand, enter, contribute to, or whose effect can be described. |
| **Purpose** | The need a meeting is intended to serve. | A participant needs a reason for the gathering in order to judge relevance; topic, format, and hoped-for result can vary without supplying that reason. | The model can say when and how to join but cannot say why the meeting exists or whether it is worth the participant's time. |
| **Access** | The boundary that determines whether a person may enter or observe a meeting. | Presence is distinct from speaking, contributing, or deciding, so no other core concept can state who may simply be there. | A model may describe contribution rights but cannot distinguish an excluded person from an admitted observer. |
| **Participation** | The boundary that determines how a person who has access may take part in a meeting. | Active involvement is distinct from mere presence and from a meeting's collective authority. | A participant cannot tell whether access means listen-only, discussion, facilitation, or another permitted form of contribution. |
| **Authority** | The declared effect that the meeting or its outputs may have on a shared decision or action. | Speaking or facilitating does not itself establish decision effect; this distinction protects participants from inferring power from attendance. | The model cannot distinguish a meeting that informs, advises, recommends, or acts within delegated scope, so participants may mistake involvement for decision power. |

## Necessary typed relations

- A **meeting** `serves` a **purpose**.
- A **person** `has access to` a **meeting**.
- A **person** `participates in` a **meeting** under its participation boundary.
- A **meeting** `has declared` **authority**.

`Person` is an external reference point, not an additional meeting-domain concept: the ontology is
being used by a participant, rather than attempting an ontology of people.

## What is not a sixth concept

| Item | Treatment | Reason |
| --- | --- | --- |
| Topic, time, location, convener, and cadence | Attributes of a meeting. | They identify or arrange an instance but do not answer what a meeting is or a person's standing toward it. |
| Outcome | An optional, testable expression of purpose. | It operationalizes purpose; it need not be present for a newcomer to understand why the meeting exists. |
| Format and meeting family | Labels or classifications. | They can help navigation but do not determine access, participation, authority, or purpose. |
| Forum, recurring series, and occurrence | Identity/continuity relations and record structure. | They matter to organizers and history, but a participant can relate to a meeting before knowing its persistence model. |
| Preparation and memory | Optional meeting attributes or policies. | They govern readiness and retention, not the minimum relationship to the gathering. |
| Open, member-only, observer, facilitator, inform, advise, recommend, and decide | Values or labels for the relevant boundaries. | Treating them as concepts would prematurely freeze an unvalidated value set. |
| Invitations, agendas, recordings, scheduling, and follow-up | Mechanics and artifacts. | They may implement or communicate the core facts but are not those facts themselves. |

## Small optional proposals

- Present the five facts as five plain-language questions: “What is this?”, “Why?”, “May I join?”,
  “How may I take part?”, and “What can this meeting affect?”
- Test whether participants naturally separate access, participation, and authority before adopting
  any labels or fields.
- Add an expected outcome only where it makes purpose clearer, rather than making it mandatory.

## Deliberate omissions

- No meeting-family taxonomy, because its names and usefulness remain open.
- No openness, recording, retention, privacy, or reward policy, because none is ratified here.
- No series/occurrence model, because it exceeds the newcomer-facing minimum and remains a
  candidate contract.
- No claim that all meetings need all five facts displayed in the same way; this is a comprehension
  core to test, not a schema or policy.

## Source: `attempts/b-authority.md`

# Authority-boundary attempt: two-concept meeting ontology

## Claim boundary

This is a tentative reduction for the stated confusion problem, not a proposed policy, schema, or
replacement for the candidate vocabulary.  It assumes only that a meeting can have people in
relation to it; it does not assume any particular access, governance, recording, reward, or
ratification rule.

## Concepts

| Concept | Tentative definition | Why irreducible | Exact loss if removed |
| --- | --- | --- | --- |
| **Meeting occurrence** | One bounded synchronous event to which people may bear presence, participation, or authority relations. | The relations need a common, occasion-specific object; a recurring forum, format, or purpose cannot substitute because none identifies the event at which the relation held. | The model could not say whether a person was present, participated, recommended, or decided *at a particular meeting*, so all such facts would float free of their occasion. |
| **Actor** | A person or explicitly recognized collective that can be present, participate, recommend, or decide in relation to a meeting occurrence. | Authority and participation belong to a bearer, including a collective where the meeting recognizes one; roles alone cannot bear or exercise a relation. | The model could state that a meeting had attendance or authority in the aggregate but could not distinguish whose presence, participation, recommendation, or decision it was. |

No third concept is required merely to distinguish the four states.  In particular, `recommend`
and `decide` below are governed effects, not entities.  A proposal, decision record, role,
delegation instrument, forum, or recurring series becomes a concept only if later work needs to
identify, compare, retain, or govern instances of it independently.

## Necessary typed relations

All relations are between `Actor` and `Meeting occurrence`; none entails another unless an
authorized policy later says so.

| Relation | Meaning | What it excludes |
| --- | --- | --- |
| `is-present-at(actor, occurrence)` | The actor entered or observed the occurrence. | Presence does not establish speech, contribution, recommendation, or decision power. |
| `participates-in(actor, occurrence)` | The actor took an allowed active part in the occurrence. | Participation does not establish a recommendation or a binding decision. |
| `may-recommend-at(actor, occurrence)` | The actor is authorized for the occurrence to advance a recommendation within its stated scope. | A recommendation is not a decision and does not itself bind anyone. |
| `may-decide-at(actor, occurrence)` | The actor is authorized for the occurrence to make a decision within its stated scope. | Decision authority is not inferred from presence, participation, title, or recommendation. |

`may-recommend-at` and `may-decide-at` concern authority, not evidence that the actor actually
recommended or decided.  If the model must preserve those acts or their results, add a separately
identified proposal/decision artifact only after a concrete retention or audit need is established.

## Classification of nearby material

| Item | Treatment in this reduction |
| --- | --- |
| Access or eligibility | A condition for being permitted to become present; an attribute, rule, or policy, not a concept. |
| Speaking, facilitating, voting, or contributing | Forms or attributes of participation, unless a future policy must govern each separately. |
| `recommend` / `decide` | Values of distinct authority relations, not labels for attendees and not concepts. |
| Scope, delegation source, quorum, consent, and ratification | Qualifiers or mechanics of an authority relation; their policies remain deliberately open. |
| Public, open, private, steward, member, town hall, and community leaders meeting | Labels or classifications; none proves a relation. |
| Forum, recurring series, purpose, format, preparation, memory, transparency, and privacy exception | Useful candidate concepts or attributes for other questions, but unnecessary to prevent this four-way confusion. |
| Attendance and contribution | Observed facts or evaluative mechanics outside the model; neither follows from presence or participation here. |

## Optional proposals

- Attach a declared `scope` qualifier to each authority relation before treating an exercised
  decision as binding.
- Record `access` separately from presence if the pilot needs to distinguish who could attend from
  who did attend.
- Add an `Authority grant` concept only if authority must persist across occurrences, be revoked,
  or be audited as its own object.

## Deliberate omissions

- No rule that any meeting is open, recorded, participatory, recommendatory, or decisive.
- No inference from participation to contribution, status, reward, or authority.
- No event/series split, decision-record model, proposal model, role taxonomy, or governance
  ratification route; each would solve a different, as-yet-unproven information need.

## Source: `attempts/b-operation.md`

# Organizer attempt: a minimal meeting ontology

## Boundary and status

This is an independent, tentative organizer-perspective reduction, not a policy, schema, or claim
that the existing candidate vocabulary is necessary.  It asks only what an organizer must be able
to convene, conduct, and leave with a usable trace of one synchronous meeting; recurring
arrangements are deliberately represented without treating them as an additional kind of thing.

## Proposed core: four concepts

| Concept | Tentative definition | Why irreducible | Exact loss if removed |
| --- | --- | --- | --- |
| **Meeting occurrence** | A bounded synchronous occasion that an organizer brings people together to conduct around an expressed intent. | It is the unit at which a time, attendees, conduct, and post-meeting trace coincide; no other proposed concept denotes that situated event. | There is no subject to schedule, run, or attach people and retained material to; a recurring context or document cannot tell which actual gathering occurred. |
| **Actor** | A person, group, or accountable role that can organize, attend, facilitate, receive an assignment, or be entitled to see a meeting trace. | The organizer needs a referent for responsibility and participation, while *organizer*, *facilitator*, and *attendee* are roles an actor has in a particular occurrence rather than separate entities. | Invitations, facilitation responsibility, assignments, and visibility boundaries can only be free text; the model cannot say who did or may do anything. |
| **Intent** | A stated reason and sought observable result that gives a meeting occurrence its point before it happens. | It distinguishes convening toward a result from merely booking synchronous time, and can remain stable across occurrences without making a series a new concept. | The organizer cannot assess whether a meeting is warranted or whether the retained trace answers why people gathered; date, format, and participant labels cannot supply that missing justification. |
| **Meeting record** | A deliberately retained, access-bounded account linking an occurrence to the decisions, commitments, questions, and other result material worth carrying forward. | The useful result must survive beyond those present, and the persistent account is distinct from both the live gathering and the result statements it contains. | Decisions, actions, unresolved questions, and any evidence of what happened become ephemeral or unlinked; later work cannot reliably retrieve or qualify the meeting's result. |

## Necessary typed relations

Only these relations are required by the stated organizer boundary:

| Relation | Meaning | Why necessary |
| --- | --- | --- |
| `Actor --organizes--> Meeting occurrence` | An actor is accountable for convening or maintaining the occurrence. | Makes ownership legible without reifying an organizer role. |
| `Actor --participates-in--> Meeting occurrence` | An actor has a stated occurrence-specific participation role. | Connects the people who may be invited, speak, facilitate, or receive follow-up to the event; the exact role is an attribute/value of this relation. |
| `Meeting occurrence --pursues--> Intent` | The occurrence is convened toward an intent. | Retains the reason for spending synchronous time and permits comparison with the retained result. |
| `Meeting record --records--> Meeting occurrence` | A record is the retained trace of one occurrence. | Prevents a document or recording from floating free of the event it is evidence about. |

`Meeting record` may cite or contain the material that realizes, fails to realize, or revises an
`Intent`; that containment/link is useful but need not be a new typed relation in the minimal core.

## Deliberate classification decisions

- **Attributes:** time, duration, location/channel, cadence, topic, access rule, retention rule,
  and a record's visibility are properties of an occurrence or record.  They constrain use but do
  not need independent identity for this boundary.
- **Values and labels:** work/community orientation, format, access level, participation role,
  authority posture, and record type are controlled or provisional values, not core concepts.
  In particular, `inform`, `advise`, `recommend`, and `decide-within-delegated-scope` describe
  the authorized effect of an occurrence; they do not create authority merely by being recorded.
- **Relations rather than concepts:** organizer, attendee, facilitator, assignee, and viewer are
  actor-to-occurrence or actor-to-record roles.  A recurring series is a grouping/link among
  occurrences with shared attributes, not necessary to convene one occurrence.
- **Mechanics:** invitations, agenda creation, pre-reads, turn-taking, consent checks, recording,
  publishing notes, and routing actions are procedures.  They can be selected from the intent,
  participant roles, and record boundary without enlarging the ontology.

## Small optional proposals

- Add **recurring context** only if stable identity and standing rules must be queried separately
  from individual occurrences; otherwise a recurrence key and shared attributes suffice.
- Add **commitment** only if decisions, assigned actions, and open questions must have independent
  lifecycle, ownership, and completion queries outside a meeting record.
- Split `Actor --participates-in--> Meeting occurrence` into distinct access, voice, and authority
  relations only if practice shows that one role field loses a consequential distinction.

## Deliberate omissions

- No meeting family, format, forum, transparency, privacy exception, preparation, community
  rhythm, contribution, governance body, tool, or reward concept is included: each is either a
  value, attribute, relation role, mechanic, or a broader policy boundary for this minimal task.
- No claim is made that all meetings should be open, recorded, recurring, decisive, or documented
  in the same way.
- No claim is made that this four-concept core is validated; the supplied material itself marks
  vocabulary, policies, and the series/occurrence split as candidate and awaiting real cases and
  participant evidence.

## Source: `attempts/b-participant.md`

# Participant attempt: the minimum needed to relate to a meeting

## Tentative result

This attempt proposes **two concepts**.  It is a comprehension hypothesis for a participant or
newcomer, not a policy, schema, or replacement for the candidate vocabulary.

| Concept | Tentative definition | Why irreducible | Exact loss if removed |
| --- | --- | --- | --- |
| **Meeting** | A bounded, synchronous occasion in which people are invited to gather around a stated purpose. | The participant needs an object to which an invitation, attendance, contribution, and follow-up can refer; neither a calendar time nor a group of people supplies that identity. | We cannot say what someone is joining, what a boundary applies to, or which occasion produced a later action or record. |
| **Purpose** | The need a meeting is convened to address, including the change it intends to make possible. | It distinguishes a meeting from mere simultaneous presence and lets a newcomer judge relevance before attending. | A participant can know when and where to appear but not why it exists, whether it concerns them, or what useful contribution would look like. |

## Necessary typed relations

- `Meeting --serves--> Purpose`: every intelligible meeting is related to the need it is convened
  to address.
- `Person --may-access--> Meeting`: an access relation says whether a person may enter or observe
  this occasion; it does not imply voice or power.
- `Person --may-participate-in--> Meeting`: a participation relation states the permitted mode of
  engagement, such as observe, speak, facilitate, or contribute; its mode is a value, not a new
  concept.

The first relation explains what the meeting is for; the latter two explain how a newcomer relates
to it.  Decision effect is a meeting attribute that must be stated when relevant, not a third
participant-facing core concept: its values may include inform, advise, recommend, or
decide-within-delegated-scope, and none follows from access or participation.

## Not concepts in this minimum

| Item | Treatment | Reason |
| --- | --- | --- |
| Date, duration, location, topic, cadence, facilitator, and invite label | Attributes or labels of a meeting. | They describe or identify an occasion; they do not explain what kind of thing it is. |
| Open/closed, observer/speaker/facilitator, and authority effect | Values on the two person-to-meeting relations or on a meeting attribute. | Treating the values as concepts falsely turns each permission or effect into a distinct object. |
| Series, forum, format, family, and community rhythm | Optional grouping or continuity structures. | A newcomer can understand and relate to a single meeting without classifying it or knowing its recurrence context. |
| Expected outcome | A more specific expression of purpose. | It can sharpen an invitation but does not add a different kind of thing. |
| Preparation, memory, transparency, privacy exception, agenda, notes, recording, decision, action, and contribution | Mechanics, artifacts, policies, or consequences. | They may matter greatly in particular meetings, but none is required for someone to recognize an occasion and relate to it. |
| Participant | A role played by a person in relation to a meeting. | Reifying the role hides the actual participation relation and excludes observers or invitees prematurely. |

## Small optional proposals

- Put a plain-language purpose and the applicable access, participation, and decision-effect
  values on each invitation.
- Add a series reference only when it helps a person understand standing expectations across
  occurrences.
- Add a retained-record link only when a record exists and the person may access it.

## Deliberate omissions

- No meeting families, formats, or universal classification scheme.
- No claim that every meeting is open, recorded, recurring, decisive, or contribution-bearing.
- No reward, governance, privacy, retention, or ratification policy.
- No claim that this two-concept core has been tested with real meeting cases or participant
  language.
