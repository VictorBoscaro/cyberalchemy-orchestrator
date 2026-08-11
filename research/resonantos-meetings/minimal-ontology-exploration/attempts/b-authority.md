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
