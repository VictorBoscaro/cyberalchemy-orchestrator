---
feature: agent-provenance-telemetry
artifact: independent-review-closure
reviewed_version: 0.2.0
date: 2026-07-22
final_verdict: PASS/PASS
---

# System-managed tags and emergent lens — independent review closure

Two read-only reviewers worked independently after the v0.2.0 amendment. Neither edited files,
spawned helpers or saw the other review while producing its initial verdict.

## Review axes

1. **Authority and architecture:** tag-registry ownership, isolation, raw testimony versus resolution,
   profile-field separation, ACI/KT/audit authority and cutover.
2. **Falsification and method:** equal-information lens baselines, gold labels, replay versus sample
   stability, leakage, verbosity, probe dependencies and the operational meaning of emergence.

Both initial verdicts rejected the first amended baseline. Their convergent high-severity findings
were:

- raw emission, system resolution and residue were represented too closely;
- tag-registry governance lacked an executable sole-writer/CAS contract;
- P007 gave the lens information its baselines did not receive;
- replay determinism was incorrectly standing in for sample stability;
- “material perspective” lacked a pre-projection gold-label procedure;
- P001/P003 could make the registry depend circularly on the fixtures used to test it.

## Remediation applied

- split `topic.emission_observed`, `tag.resolution_projected` and `lens.projected`;
- defined candidate `TagRegistryAuthority`, authenticated commands, CAS, idempotency, lifecycle events
  and a registry-specific sole-writer cutover;
- split free and assisted capture, with writer-stamped references and registry version;
- replaced unequal union/majority decision baselines with incidence/grouped projections that contain
  identical data and must round-trip to one canonical relation;
- added pre-projection labels, balanced evaluation, replay, enumeration, bootstrap and
  leave-one-seat-out checks;
- restricted the first lens to lexical/tag-presence organization and made semantic-position loss
  explicit;
- froze a fixture-independent seed registry, added held-out coverage and made the probe dependency DAG
  explicit;
- corrected empty-pair agreement, mutually exclusive P001 decisions, P002 content digests, randomized
  profile exposure and repeated-run aggregation for P004.

## Closure

The authority reviewer returned `PASS` after the second remediation round. The methodological reviewer
identified one final ambiguity in duplicate-rate aggregation; after per-fixture aggregation and a 95%
bootstrap boundary were added to P004, it returned `PASS`.

`PASS/PASS` means the discovery and preregistered methods are internally reviewable at this stage. It
does not mean the empirical claims passed: none of the seven probes has been executed.
