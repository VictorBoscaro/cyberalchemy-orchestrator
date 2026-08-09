# Ontology view: ResonantOS meetings

This view is the single home for the working vocabulary used by the meeting-model documents. It
does not approve policy or prescribe a schema. The public explanation lives in
[`system-view.md`](system-view.md); open verdicts and candidate fields live in
[`engineer-view.md`](engineer-view.md).

## ontology-view Result

- Status: **flag** — structurally complete, but the vocabulary has not been tested against the
  planned meeting inventory or community interviews.
- Target boundary: the proposed model for synchronous ResonantOS meetings and recurring meeting
  forums; asynchronous community spaces are external context, not classified here.
- Vault source: built-inline from [`research-plan.md`](research-plan.md) and current official
  ResonantOS, ResonantDAO, and Augmentatism sources.
- Lane handles:
  - terms: `terms.catalog`
  - relations: `relations.graph`
  - axes: `axes.model`
  - conflicts: `conflicts.register`
  - provenance: `provenance.boundary`
  - deferrals: `deferrals.handles`
- Single-owner check: **pass** — every load-bearing term is defined once, in the table below.
- Evidence boundary: official project claims are source-backed; meeting-model vocabulary is marked
  as a proposal or inference.
- Conflicts open: **6**.

## Terms

| Handle | Term | Working definition | Role | Confidence | Source |
| --- | --- | --- | --- | --- | --- |
| `term:meeting` | Meeting | A time-bounded synchronous gathering convened around a stated purpose. | Root object being organized. | Medium — inferred, not official terminology. | [`research-plan.md`](research-plan.md#purpose) |
| `term:forum` | Forum | A stable context in which related meetings recur with a known purpose, participation boundary, and authority posture. | Distinguishes an enduring venue from one event. | Medium — inferred. | [`research-plan.md`](research-plan.md#research-questions) |
| `term:meeting-family` | Meeting family | The proposed primary grouping based on the main value a meeting is intended to produce. | Coarse navigation axis. | Low — hypothesis awaiting real-case testing. | [`research-plan.md`](research-plan.md#proposals-to-test) |
| `term:work-family` | Work family | Candidate meeting family for gatherings whose primary intended value is an operational result such as orientation, coordination, construction, decision, or review. | Proposed first family. | Low — proposal. | [`research-plan.md`](research-plan.md#proposals-to-test) |
| `term:community-life-family` | Community-life family | Candidate meeting family for gatherings whose primary intended value is participation, learning, relationship, care, recognition, or belonging. | Proposed second family. | Low — proposal; boundary is contested. | [`research-plan.md`](research-plan.md#proposals-to-test); [ResonantDAO contribution sectors](https://resonantdao.com/whitepaper/#6-rct-and-contribution-reputation) |
| `term:meeting-format` | Meeting format | A repeatable way a meeting is conducted for a narrower function, such as coordination, workshop, town hall, peer review, or celebration. | Finer-grained classification beneath a family. | Medium — inferred from planned cases. | [`research-plan.md`](research-plan.md#evidence-sample) |
| `term:recurring-series` | Recurring series | The enduring identity and standing rules shared by multiple scheduled occurrences of the same forum. | Owns stable information such as purpose and cadence. | Medium — proposal. | [`research-plan.md`](research-plan.md#proposals-to-test) |
| `term:meeting-occurrence` | Meeting occurrence | One dated instance of a meeting or recurring series, with its own topic, intended result, and record. | Owns event-specific information. | Medium — proposal. | [`research-plan.md`](research-plan.md#proposals-to-test) |
| `term:purpose` | Purpose | The reason a meeting or forum exists and the need it is intended to serve. | Classification anchor. | High — required by the research objective. | [`research-plan.md`](research-plan.md#purpose) |
| `term:expected-outcome` | Expected outcome | The observable change the meeting is intended to leave, without claiming in advance that it will occur. | Operational test of purpose. | Medium — inferred. | [`research-plan.md`](research-plan.md#purpose) |
| `term:access` | Access | The boundary governing who may observe or enter a meeting. | Independent participation dimension. | Medium — proposed distinction. | [`research-plan.md`](research-plan.md#research-questions) |
| `term:participation` | Participation | The permissions and expectations governing who may speak, contribute, facilitate, or otherwise take part. | Separates presence from active involvement. | Medium — proposed distinction. | [`research-plan.md`](research-plan.md#research-questions) |
| `term:meeting-authority` | Meeting authority | The declared effect a forum may have: inform, advise, recommend, or decide. | Prevents attendance from implying decision power. | High as a needed distinction; values remain proposed. | [ResonantDAO governance](https://resonantdao.com/whitepaper/#10-governance); [`research-plan.md`](research-plan.md#research-questions) |
| `term:preparation` | Preparation | Material or activity requested before a meeting so participants can use synchronous time effectively. | Holds agenda and pre-read expectations. | Medium — inferred. | [`research-plan.md`](research-plan.md#research-questions) |
| `term:meeting-memory` | Meeting memory | The persistent record intentionally kept after a meeting, such as notes, decisions, actions, open questions, or a recording. | Connects meetings across time. | Medium — inference from ResonantOS memory principles. | [ResonantOS Living Archive](https://resonantos.com/#what-it-changes); [`research-plan.md`](research-plan.md#purpose) |
| `term:transparency` | Transparency | The degree to which a meeting's purpose, authority, process, and retained memory are inspectable by people affected by it. | Distinguishes inspectability from unrestricted attendance. | Medium — inference. | [ResonantOS trust boundaries and audit trails](https://resonantos.com/#what-makes-resonantos-different) |
| `term:privacy-exception` | Privacy exception | A stated reason to limit access, participation, recording, or retained memory in order to protect consent, safety, care, or sensitive work. | Boundary on openness-by-default proposals. | Medium — inference. | [Augmentatism anti-capture](https://augmentatism.com/#our-social-contract); [Community-Verified Integrity](https://augmentatism.com/#community-verified-integrity) |
| `term:community-rhythm` | Community rhythm | A recurring social infrastructure through which members align, learn, meet, and move toward active participation. | Official context for weekly calls. | High — source-backed wording. | [ResonantDAO weekly calls](https://resonantdao.com/whitepaper/#9-weekly-calls-and-community-rhythm) |

## Typed relations

- `relation:meeting--meeting-occurrence`: `term:meeting-occurrence` **is-a** `term:meeting`.
- `relation:series--occurrence`: `term:meeting-occurrence` **part-of** zero or one
  `term:recurring-series`.
- `relation:forum--series`: `term:recurring-series` **realizes** a `term:forum` through scheduled
  occurrences.
- `relation:family--work`: `term:work-family` **is-a** `term:meeting-family`.
- `relation:family--community-life`: `term:community-life-family` **is-a**
  `term:meeting-family`.
- `relation:meeting--purpose`: `term:meeting` **depends-on** an explicit `term:purpose` for useful
  classification.
- `relation:purpose--outcome`: `term:expected-outcome` **operationalizes** `term:purpose` without
  proving it was achieved.
- `relation:meeting--format`: `term:meeting` **uses** a `term:meeting-format`.
- `relation:meeting--family`: `term:meeting` **may-be-oriented-by** one primary
  `term:meeting-family`; this relation is provisional.
- `relation:meeting--dimensions`: `term:access`, `term:participation`, `term:meeting-authority`,
  `term:preparation`, and `term:meeting-memory` are **orthogonal-to** `term:meeting-family` as a
  design claim awaiting testing.
- `relation:transparency--access`: `term:transparency` **is-not-identical-to** `term:access`.
- `relation:privacy--transparency`: `term:privacy-exception` **constrains** particular transparency
  surfaces without automatically eliminating all `term:transparency`.
- `relation:rhythm--series`: `term:community-rhythm` **may-be-realized-by** one or more
  `term:recurring-series`.
- `relation:meeting--memory`: `term:meeting-memory` **follows** a `term:meeting-occurrence` when its
  documentation policy requires persistence.

## Axes

The proposed model contains several independent questions. Correlation in current practice does
not make these axes the same.

| Axis | Question answered | Relation to other axes |
| --- | --- | --- |
| Primary family | What main value is this meeting trying to produce? | Proposed navigation axis; independent of audience and authority. |
| Format | What narrower meeting function and interaction pattern are used? | May recur within either family. |
| Scope | Which project, circle, or community area does it concern? | Independent of family. |
| Access | Who may observe or enter? | Does not grant participation or authority. |
| Participation | Who may speak, contribute, or facilitate? | Does not itself grant decision authority. |
| Authority | What effect may this forum have? | Must be explicit even when access is open. |
| Preparation | What must happen before synchronous time? | Depends on the meeting's work, not its family alone. |
| Memory | What persists, for whom, and for how long? | Related to transparency and privacy, but not identical to either. |
| Cadence | Is this one-off or recurring? | Determines whether series-level information exists. |

## Conflicts register

| Conflict | Why it matters | Status / owner |
| --- | --- | --- |
| `work` versus `community life` | Community, care, onboarding, and education are also recognized contributions; the labels may create a false opposition. | OPEN → `engineer-view.md#D1` |
| `meeting` versus `forum` | Ordinary language often uses them interchangeably, while the model needs event versus enduring venue. | OPEN → test in participant interviews; `engineer-view.md#D1` |
| `open`, `public`, and `transparent` | These can refer separately to attendance, voice, authority, recording, or records. | OPEN → `engineer-view.md#D3` |
| `community leaders meeting` | The name does not reveal whether the forum coordinates, recommends, or decides. | OPEN → `engineer-view.md#D7` |
| `documentation` versus `recording` | A useful memory may be written and public even when recording would violate consent or care. | OPEN → `engineer-view.md#D4` |
| `attendance` versus `contribution` | Official sources allow useful call participation to matter but reject attendance as a lasting substitute for contribution. | Source boundary established; policy OPEN → `engineer-view.md#D8` |

## Provenance boundary

Source-backed facts:

- weekly calls have several social and participatory functions;
- contribution spans governance, community, creative, technical, financial, and educational work;
- current governance begins with custodian leadership and advisory community participation;
- ResonantOS emphasizes memory, visible action, explicit gates, and trust boundaries; and
- Augmentatism requires consent and does not equate integrity with mandatory openness.

Inferences and proposals:

- the two candidate families;
- every meeting-model term not used as official project language;
- the independence of classification axes;
- the recurring-series versus occurrence split; and
- all proposed policies and schema fields.

## Deferrals

- Narrative significance → [`system-view.md`](system-view.md).
- `term:meeting-family` naming verdict → [`engineer-view.md#D1`](engineer-view.md#d1).
- Family-plus-secondary-emphasis verdict → [`engineer-view.md#D2`](engineer-view.md#d2).
- Access/transparency policy → [`engineer-view.md#D3`](engineer-view.md#d3).
- Meeting-memory policy → [`engineer-view.md#D4`](engineer-view.md#d4).
- Preparation policy → [`engineer-view.md#D5`](engineer-view.md#d5).
- Series/occurrence contract → [`engineer-view.md#D6`](engineer-view.md#d6).
- Community-leaders authority → [`engineer-view.md#D7`](engineer-view.md#d7).
- Attendance/contribution treatment → [`engineer-view.md#D8`](engineer-view.md#d8).
- Ratification owner and pilot → [`engineer-view.md#D9`](engineer-view.md#d9).

Promotion into an `ontology-vault` is premature. Reconsider it only after real meeting cases and
participant language tests stabilize the vocabulary.
