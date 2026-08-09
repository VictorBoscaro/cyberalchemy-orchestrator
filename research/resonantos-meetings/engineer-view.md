# Engineer view: ResonantOS meeting-model decisions and candidate contracts

This view owns verdict status and candidate mechanics. It does not redefine vocabulary from
[`ontology-view.md`](ontology-view.md) or retell the narrative in
[`system-view.md`](system-view.md).

## engineer-view Result

- Status: **flag** — every stance has one row, but no meeting-model policy has been ratified.
- Target boundary: candidate mechanics needed to test the ResonantOS meeting model.
- Lane handles:
  - decision inventory: `decisions.table`
  - contracts: `contracts.catalog`
  - mechanics: `mechanics.map`
  - cross-reference map: `xref.map`
  - deferrals: `deferrals.handles`
- Stance-coverage check: **pass** — 9 stances, 9 decision rows.
- Authority check: **pass** — every OPEN/CRITICAL row explicitly cites the absence of a running
  gate and the evidence that frames the choice.
- Nothing-decided-twice check: **pass**.
- Open / Critical rows: D1–D8 OPEN; D9 CRITICAL.

## Decision inventory

| ID | Owning stance | Candidate verdict | Status | Authority |
| --- | --- | --- | --- | --- |
| <a id="d1"></a>D1 | `stance:family-names` | No ratified verdict. Test `work / community life` against real cases and participant language before naming the families. | OPEN | No running gate; [`research-plan.md`](research-plan.md#proposals-to-test) treats them as hypotheses. |
| <a id="d2"></a>D2 | `stance:secondary-emphases` | No ratified verdict. Candidate mechanics use one primary family plus optional secondary emphases; reject or revise if ambiguity remains high. | OPEN | No running gate; [`research-plan.md`](research-plan.md#research-questions). |
| <a id="d3"></a>D3 | `stance:openness-boundaries` | No ratified verdict. Candidate policy is open and transparent by default with justified exceptions, while access, participation, authority, recording, and records remain separate. | OPEN | No running gate; [ResonantOS trust boundaries](https://resonantos.com/#what-makes-resonantos-different), [Augmentatism integrity boundary](https://augmentatism.com/#community-verified-integrity). |
| <a id="d4"></a>D4 | `stance:proportional-memory` | No ratified verdict. Candidate policy requires useful work memory but does not require recording; retention and visibility vary by forum. | OPEN | No running gate; [ResonantOS Living Archive](https://resonantos.com/#what-it-changes); [`research-plan.md`](research-plan.md#research-questions). |
| <a id="d5"></a>D5 | `stance:conditional-pre-read` | No ratified verdict. Candidate policy requires pre-read only when preparation is necessary for a decision or substantive discussion. | OPEN | No running gate; [`research-plan.md`](research-plan.md#research-questions). |
| <a id="d6"></a>D6 | `stance:series-occurrence-split` | No ratified verdict. Candidate contract separates stable series data from occurrence-specific data. | OPEN | No running gate; [`research-plan.md`](research-plan.md#proposals-to-test). |
| <a id="d7"></a>D7 | `stance:leaders-forum-authority` | No ratified verdict. Any leaders or stewardship forum must state whether it coordinates, advises, recommends, or decides within delegated scope. | OPEN | No running gate; [current bootstrap posture](https://resonantdao.com/whitepaper/#10-governance). |
| <a id="d8"></a>D8 | `stance:attendance-contribution` | The model must not equate attendance with contribution. It may record useful participation without defining rewards. | OPEN | Policy remains open; boundary is source-backed by [weekly-call guidance](https://resonantdao.com/whitepaper/#9-weekly-calls-and-community-rhythm) and [open contribution questions](https://resonantdao.com/whitepaper/#21-open-questions-before-public-finalization). |
| <a id="d9"></a>D9 | `stance:ratification-owner` | No ratified verdict and no named final owner. The model may be piloted, but cannot become community policy until an authorized ratification route is named. | CRITICAL | No running gate; current governance is described as custodian-led with advisory community participation in the [whitepaper](https://resonantdao.com/whitepaper/#10-governance). |

## Candidate contracts

These fields are test instruments, not approved schema. Term meanings remain in
[`ontology-view.md`](ontology-view.md).

### Recurring series record

```yaml
name:
purpose:
primary_family:
secondary_emphases: []
format:
scope:
cadence:
owner:
access:
participation:
authority:
preparation_policy:
memory_policy:
review_date:
```

### Meeting occurrence record

```yaml
series:
date:
specific_topic:
relevance:
expected_outcome:
pre_read:
facilitator:
decisions: []
action_items: []
open_questions: []
meeting_record:
```

### Candidate authority values

```text
inform
advise
recommend
decide-within-delegated-scope
```

These are proposed effects, not governance rights created by the schema.

## Candidate mechanics

1. A forum owner proposes a recurring-series record.
2. The forum's purpose, boundaries, and authority posture are visible before scheduling.
3. Each occurrence states its specific topic, relevance, and expected outcome.
4. Preparation is attached only when D5's eventual policy requires it.
5. The meeting happens within the declared access, participation, and authority boundaries.
6. The occurrence retains only the memory permitted by its policy and participant consent.
7. Open questions and actions flow into the next appropriate work surface; attendance alone creates
   no reward or authority.
8. The series is reviewed after the pilot period or when its purpose or authority changes.

No automation, on-chain recording, contribution credit, or tooling is implied.

## Cross-reference map

| System stance | Decision owner | Term owners used |
| --- | --- | --- |
| `stance:family-names` | D1 | `term:meeting-family`, `term:work-family`, `term:community-life-family` |
| `stance:secondary-emphases` | D2 | `term:meeting-family`, `term:meeting-format` |
| `stance:openness-boundaries` | D3 | `term:access`, `term:participation`, `term:meeting-authority`, `term:transparency`, `term:privacy-exception` |
| `stance:proportional-memory` | D4 | `term:meeting-memory`, `term:privacy-exception` |
| `stance:conditional-pre-read` | D5 | `term:preparation` |
| `stance:series-occurrence-split` | D6 | `term:recurring-series`, `term:meeting-occurrence` |
| `stance:leaders-forum-authority` | D7 | `term:forum`, `term:meeting-authority` |
| `stance:attendance-contribution` | D8 | `term:participation`, `term:community-rhythm` |
| `stance:ratification-owner` | D9 | `term:forum`, `term:meeting-authority` |

## Deferrals

- Vocabulary → [`ontology-view.md`](ontology-view.md).
- Context, shape, and stakes → [`system-view.md`](system-view.md).
- Final governance decisions → a future authorized ResonantDAO decision route, not this view.
- Validation evidence → the inventory, interviews, classification tests, and pilot specified in
  [`research-plan.md`](research-plan.md).
