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
