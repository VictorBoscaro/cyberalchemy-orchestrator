# System view: a meeting model for ResonantOS

This is the plain-language view of the proposal. Terms have one home in
[`ontology-view.md`](ontology-view.md). Decisions have one home in
[`engineer-view.md`](engineer-view.md). This document explains the context, shape, and stakes; it
does not settle the open choices.

## system-view Result

- Status: **flag** — the shape is explainable, but it has not yet been tested against the planned
  meeting inventory or participant interviews.
- Target boundary: a minimal model for synchronous ResonantOS meetings and recurring forums.
- Stakeholder altitude: community members, meeting organizers, stewards, and new contributors.
- Lane handles:
  - surface: `surface.summary`
  - shape: `shape.narrative`
  - layering: `layering.model`
  - stances: `stances.named`
  - alternative framings: `framings.tables`
  - shape diagrams: omitted — the axes table in `ontology-view.md` is clearer at this stage
  - deferrals: `deferrals.handles`
- Decided-nothing check: **pass**.
- Term-deferral check: **pass** — term meanings remain in `ontology-view.md`.
- Evidence boundary: official context is source-backed; the meeting model is a proposal under
  research.

## 1. Context: why meetings matter here

ResonantOS is the operating layer within a wider project. Augmentatism supplies the philosophical
floor. ResonantDAO supplies the stewardship, membership, contribution, and governance layer. The
current project is moving from founder custody toward growing community stewardship, while the DAO
remains in a custodian-led bootstrap. These are current project claims, not conclusions of this
meeting research. See [About ResonantOS](https://resonantos.com/about/) and the
[ResonantDAO whitepaper](https://resonantdao.com/whitepaper/).

Meetings already carry several jobs. Officially, weekly calls help people align, learn, discuss
ResonantOS, understand the roadmap, meet contributors, and move toward active participation. This
makes meetings part of the community's early infrastructure, not just calendar events.

The practical problem is that a growing community can no longer rely on everyone knowing, by
context, why a call exists or what power it has. A meeting can be open without being decisive. It
can be social while producing real contribution. It can leave public notes without being recorded.
The proposed model exists to make those differences visible.

| Alternative framing considered | Why it is held aside in this view |
| --- | --- |
| Treat meetings as an informal culture matter only. | It cannot explain authority, preparation, or persistent decisions; verdict deferred to `engineer-view.md#D9`. |
| Treat every meeting as a governance mechanism. | Official weekly calls have broader social and learning functions; authority still requires an explicit verdict. |

## 2. First layer: orient people before describing every format

The protagonist idea is small: give each meeting one primary orientation, then describe its other
important properties separately. The candidate orientation uses `term:meeting-family`, with
`term:work-family` and `term:community-life-family` as provisional labels.

This is navigation, not a claim that community life is outside work. ResonantDAO explicitly
recognizes onboarding, mentoring, moderation, care, education, governance, creative work, and
technical work as contribution. The label tension is therefore real and remains open.

The classification question is practical: after a good meeting, what main kind of change should be
visible? The answer may orient the meeting without exhausting everything that happened in it.

| Alternative framing considered | Why it is held aside in this view |
| --- | --- |
| One flat list of formats. | It gives detail but weak orientation; pending `engineer-view.md#D1`. |
| Three top-level families, adding governance. | Governance may be an authority posture or function rather than a peer family; pending real-case testing. |
| Allow every meeting to be simply “hybrid.” | It risks becoming a non-classification; the secondary-emphasis question is owned by `engineer-view.md#D2`. |

## 3. Second layer: a family does not determine who can enter or decide

Once a meeting is oriented, the model asks separate questions using `term:meeting-format`,
`term:access`, `term:participation`, `term:meeting-authority`, `term:preparation`, and
`term:meeting-memory`.

This separation matters because the same format can operate under different boundaries. A public
town hall may inform. A member forum may recommend. A small working circle may be authorized to
decide within a narrow scope. None of those effects follows automatically from attendance.

The same is true for transparency. ResonantOS emphasizes visible action, explicit gates, memory,
and auditability. Augmentatism also protects consent and allows open and closed worlds under its
ethical floor. Together, those sources support making boundaries explicit; they do not prove that
every meeting must be open or recorded.

| Alternative framing considered | Why it is held aside in this view |
| --- | --- |
| “All meetings are public” as a philosophical requirement. | Current sources do not establish it; the policy verdict belongs to `engineer-view.md#D3`. |
| Use one field called openness. | It hides distinct questions about observing, speaking, deciding, recording, and accessing records. |

## 4. Third layer: recurring identity and one meeting are different things

A stable forum needs continuity. One occurrence needs specificity. The proposed split between
`term:recurring-series` and `term:meeting-occurrence` keeps standing purpose, cadence, ownership,
and boundaries separate from a dated topic, intended result, decisions, actions, and open
questions.

This layer connects to a central ResonantOS theme: useful context should compound instead of
resetting. For meetings, continuity does not require recording everything. It requires a deliberate
choice about what becomes `term:meeting-memory`, who may see it, and what should remain ephemeral.

| Alternative framing considered | Why it is held aside in this view |
| --- | --- |
| One document per meeting series, continually overwritten. | It may erase event-specific history; contract verdict belongs to `engineer-view.md#D6`. |
| Record every meeting in full. | It may create cost and consent problems; proportional-memory verdict belongs to `engineer-view.md#D4`. |

## 5. Fourth layer: the model should make power legible

The highest-risk ambiguity is not taxonomy. It is authority. A “community leaders meeting” could
coordinate work, advise a custodian, recommend a proposal, or decide within delegated scope. The
name alone answers none of those questions.

The model therefore needs to expose the forum's effect without pretending current governance is
already settled. This is consistent with the whitepaper's explicit description of a custodian-led
bootstrap and contextual future governance.

Attendance and contribution must also remain distinct. The whitepaper says useful call
participation may eventually matter, while attendance alone should not become a lasting substitute
for contribution. The meeting model can preserve that distinction; it should not invent reward
rules.

| Alternative framing considered | Why it is held aside in this view |
| --- | --- |
| Infer authority from organizer role or attendee list. | It creates invisible power; authority verdict belongs to `engineer-view.md#D7`. |
| Reward every attendance event. | Official sources reject attendance as a permanent contribution substitute; policy remains outside this model. |

## 6. Fifth layer: learn before ratifying

The current structure is a hypothesis. The research plan calls for real meeting examples, short
participant conversations, classification tests, comprehension tests, and an adversarial search for
cases that do not fit.

The immediate goal is not a universal ontology. It is a model that can orient the next 10–15 real
meeting cases with low maintenance cost. A short pilot can reveal where names, fields, or policies
fail before they become governance.

| Alternative framing considered | Why it is held aside in this view |
| --- | --- |
| Ratify the model from document review alone. | No community validation or real-case saturation has occurred; ratification owner is CRITICAL in `engineer-view.md#D9`. |
| Expand the research into a broad study of DAOs. | The research plan limits precedents to concrete ambiguities so the model remains grounded in ResonantOS. |

## Layering model

| Layer | What is given or source-backed | What is being optimized or proposed | What accumulates later |
| --- | --- | --- | --- |
| Project context | Three project layers; weekly calls as social infrastructure; current governance bootstrap. | None in this view. | Updated official policy. |
| Orientation | Meetings carry different purposes and outcomes. | Two provisional primary families. | Real classifications and counterexamples. |
| Boundaries | Human governance, consent, trust boundaries, and memory matter. | Separate access, participation, authority, preparation, and memory. | Forum-specific policies. |
| Continuity | ResonantOS values context that compounds. | Series/occurrence split and proportional memory. | Agendas, records, decisions, and open questions. |
| Governance | Authority is currently contextual and not fully decentralized. | Make every forum's effect explicit. | Ratified delegations and policies. |
| Learning | The research plan defines evidence and stopping conditions. | Pilot before ratification. | Findings and revisions. |

## Named stances

- `stance:family-names` → [`engineer-view.md#D1`](engineer-view.md#d1)
- `stance:secondary-emphases` → [`engineer-view.md#D2`](engineer-view.md#d2)
- `stance:openness-boundaries` → [`engineer-view.md#D3`](engineer-view.md#d3)
- `stance:proportional-memory` → [`engineer-view.md#D4`](engineer-view.md#d4)
- `stance:conditional-pre-read` → [`engineer-view.md#D5`](engineer-view.md#d5)
- `stance:series-occurrence-split` → [`engineer-view.md#D6`](engineer-view.md#d6)
- `stance:leaders-forum-authority` → [`engineer-view.md#D7`](engineer-view.md#d7)
- `stance:attendance-contribution` → [`engineer-view.md#D8`](engineer-view.md#d8)
- `stance:ratification-owner` → [`engineer-view.md#D9`](engineer-view.md#d9)

## What this view does not cover

- Definitions: [`ontology-view.md`](ontology-view.md).
- Policy verdicts and candidate fields: [`engineer-view.md`](engineer-view.md).
- Full governance architecture, reward policy, tooling, and final meeting schedule: outside the
  research boundary.
- A diagram: omitted until prose or a table demonstrably fails to explain a relationship.
