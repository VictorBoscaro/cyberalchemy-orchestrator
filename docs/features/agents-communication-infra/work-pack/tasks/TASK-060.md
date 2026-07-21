# TASK-060 — Preregistered product-value gate

## Objective

Decide whether the structured protocol justifies its cost before funding provider portability and
generic composition.

- **Layer boundary:** L2 -> L3 / S-004 / W4.
- **Dependencies:** one real adapter passes L2; OQ-PRODUCT-EVAL accepted before collecting results.
- **Write scope:** experiment protocol, immutable task corpus references, evaluation data and report.

## Smallest Working Units

- **SWU-ACI-021 — Preregistration:** freeze corpus/ground truth, blind rubric, evaluators, sample
  size, minimum effect, cost/latency ceilings and continue/simplify/stop rule.
- **SWU-ACI-022 — Baseline and protocol runs:** execute fixed single-agent and structured conditions;
  preserve randomized/blinded labels and operational receipts.
- **SWU-ACI-023 — Analysis and decision:** compare quality, relevant dissent, false consensus,
  latency, tokens/tools, recovery and operator load; apply the frozen rule without moving thresholds.

| SWU | Dependencies | Write scope | Acceptance evidence | Validation | Owner |
|---|---|---|---|---|---|
| 021 | L2 pass + product ADR | experiment protocol | timestamped immutable preregistration | independent human review | manual |
| 022 | 021 | evaluation runs/data | run receipts and blinded dataset | completeness/reproducibility check | local-fallback |
| 023 | 022 | analysis/report | applied threshold and signed decision | blinded analysis review | manual |

## Done when

The report records one decision: `continue`, `simplify`, or `stop`. Only `continue` opens W5;
`simplify` creates a replacement work-pack and `stop` closes W5/W6 as intentionally not pursued.
