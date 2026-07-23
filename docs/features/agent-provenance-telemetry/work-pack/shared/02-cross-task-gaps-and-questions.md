# Cross-Task Gaps and Questions

- APT-B3: reference-probe APT-side contract frozen at an exact digest; ACI registration receipt
  absent.
- APT-B7: semantic-uniqueness/result-mapping APT-side contract frozen at an exact digest; ACI
  registration receipt absent.
- APT-B8: atomic receipt/accepted-prefix grouping APT-side contract frozen at an exact digest; ACI
  registration receipt absent.
- APT-B9: event-schema/canonicalizer registry APT-side contract frozen at an exact digest; ACI
  registration receipt absent.
- APT-B10: storage/artifact policy packet is ready but its independent PASS receipt is absent.
- Owner-recorded mutation gate remains BLOCK.

Frozen requests and their digests are in `../../integration/stage-a/`. They are not registrations.
These gaps no longer block TASK-105, which passed pure L0 construction. They block TASK-110 and all
later authority-bearing integration or enablement.
