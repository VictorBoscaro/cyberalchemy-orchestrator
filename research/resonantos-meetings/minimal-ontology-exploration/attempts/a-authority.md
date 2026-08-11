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
