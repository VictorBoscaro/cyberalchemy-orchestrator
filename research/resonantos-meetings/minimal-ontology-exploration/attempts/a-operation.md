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
