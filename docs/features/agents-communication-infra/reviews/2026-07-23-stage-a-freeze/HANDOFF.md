# Stage-A independent-review handoff

Cycle 2 incorporates every cycle-1 finding: exact APT-requested profile identities, transactional
semantic uniqueness rules, `dissent_irreconcilable`, exact opening/close bytes and digests, a
complete command/event/state trace, repaired SPEC links and regenerated manifests.

The authoring agent did not approve this corpus. The reviewer must:

1. recompute every raw file digest in `artifact-manifest.json`;
2. recompute each profile's `aci-cjson-1` canonical digest;
3. review ADR-002, compatibility/sole-writer fixtures, storage policy and exact descriptor;
4. confirm B-001/B-002 closure and only B-003's W0 contract freeze;
5. confirm mutation-test authorization remains distinct from local-pilot serving; and
6. replace the pending reviewer receipt only with an independently authored PASS or findings.

The root separately merges APT TASK-105 evidence and APT-owned Stage-A artifacts into the
cross-workpack authorization predicate. This ACI handoff alone cannot enable mutation.
