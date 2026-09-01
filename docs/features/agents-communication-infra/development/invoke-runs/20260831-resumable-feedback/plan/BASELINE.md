# Pre-mutation Runtime Test Baseline

## Command

```text
python -m unittest discover -s implementations/tests/runtime -t .
```

## Initial result on 2026-08-31

- Ran: 152 tests
- Duration: 31.580 seconds
- Result: 1 failure, 26 errors
- Continuation implementation files: not yet created or changed

## Repaired baseline on 2026-08-31

- Ran: 152 tests
- Result: PASS (152/152)
- Command: `python -m unittest discover -s implementations/tests/runtime -t .`
- Repairs: aligned agent-reference delivery fixtures with dispatch schema `0.6.4` and its canonical
  capability route; refreshed the Stage-E source-manifest hashes and local-pilot manifest pin.
- Scope: pre-existing global baseline repair only; no continuation or CONF-001 writer code was
  implemented by this repair.

## Repaired failure classes

1. Stage-E integrity drift was repaired by refreshing its manifest hashes and runtime pin.
2. Agent-reference fixtures now submit schema `0.6.4` with the canonical immutable capability
   route and route digest.
3. The derivative orchestration assertion now reaches its intended token-error path.

## Use during continuation work

- Every new continuation-focused test must pass.
- Rerun the full command after each SWU and compare failure/error signatures; any new signature is a
  regression owned by that SWU.
- Do not modify `AGENTS.md`, Stage-E manifests or old reference fixtures under continuation SWUs
  except when an explicitly allocated Stage-E integrity update is required by a newly admitted
  source.
- Any failure against the repaired 152/152 baseline is a regression until proven otherwise.
