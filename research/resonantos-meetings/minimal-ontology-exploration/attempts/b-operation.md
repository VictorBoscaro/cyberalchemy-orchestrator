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
