# APT-P004 — Capture cadence, cost and ritual noise

## Claim under test

Topic capture can add reconstructible provenance without materially degrading task execution or
producing mostly duplicate/ceremonial records.

## Compared regimes

Each of the 12 shared fixtures is executed under all three regimes with order counterbalanced and at
least three independent repetitions per fixture/regime:

- `R0 — none`: no topic emission; task baseline.
- `R1 — close`: one mandatory close snapshot.
- `R2 — activation`: initial + close, plus a context-shift snapshot only when the agent declares a
  material shift.

Use the same model/provider/profile and frozen task bytes. Runs are independent; provider cache or
resumed conversation state must not cross regimes.

## Metrics

- input/output token delta against `R0`;
- wall-time delta;
- terminal task success under the fixture's existing objective checks;
- emitted record count and canonical duplicate rate;
- unique normalized tags per 1,000 added tokens;
- missing-emission rate;
- percentage of emitted tags that are neither present in task text nor retained by another snapshot
  from the same run, named `single_snapshot_novelty` and never treated as false by itself;
- blinded relevance judgment against the task artifact/trace for a stratified sample of novel terms;
- paired effect estimates and uncertainty intervals across repetitions.

## Preregistered decision

For continuous metrics, first take the median across repetitions within each fixture/regime, then the
median paired delta across the 12 fixtures. For failures and missing emissions, first compute each
fixture/regime repetition rate, then compare the mean paired rate across fixtures with a 95% bootstrap
interval. For canonical duplicates, compute the duplicate fraction within each fixture/regime across
repetitions, then use the median across fixtures with a 95% bootstrap interval.

- Prefer `R1` when it adds at most 3% median tokens, its task-failure rate exceeds `R0` by at most 8.33
  percentage points with the upper 95% bound below 16.67 points, and missing-emission rate is at most
  10% with the upper 95% bound below 20%.
- Promote `R2` over `R1` only if APT-P002 supports `initial + close`, its median additional token cost
  over `R1` is at most 5%, and median canonical duplicate rate is below 50% with its upper 95% bound
  also below 50%. If that interval crosses 50%, the cadence decision is `unresolved`.
- If `R1` exceeds 8% median token overhead or its task-failure rate exceeds `R0` by at least 16.67
  percentage points with the lower 95% bound above zero, mandatory self-emission is rejected; use
  tool-gateway observation or post-hoc experimental capture instead.
- Any threshold whose uncertainty interval crosses two decision bands is `unresolved`; a single run
  or fixture cannot decide the cadence.

## Falsifiers and invalid runs

- The task prompt, tools, model or context differ across regimes beyond the capture instruction.
- Task quality is judged only by the emitting agent.
- Missing emissions are retried with extra coaching in one regime but not the others.
- Token or timing measurements omit the capture tool call.

## Output

Per-run measurements, paired regime deltas, failures, missing emissions and a cadence disposition:
`close-default`, `activation-default`, `gateway-only` or `unresolved`.
