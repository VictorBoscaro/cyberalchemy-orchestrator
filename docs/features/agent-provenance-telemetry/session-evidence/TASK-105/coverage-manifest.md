# TASK-105 Bounded Coverage Manifest

This manifest maps executable smoke cases to the exact clause or variant they exercise. A row is
not a PASS for the complete parent TEST-SPEC family.

| Parent ID | Bounded clause/variant | Executable case | Status |
|---|---|---|---|
| APT-TEST-C05 | digest exact shape, fresh decode, candidate digest exclusion | `Digest is exact and fresh`; `Candidate canonicalizer...` | pass |
| APT-TEST-R3 | artifact receipt-shaped reference; no caller `finalized`; capture unknown/raw fields | `Artifact is structural...`; `Capture rejects...` | pass |
| APT-TEST-R8 | completion-log exact shape, scalar/length/enum and prohibited-content rejection | `Telemetry rejects extra, nested, raw content...` | pass |
| APT-TEST-C10 | closed discriminator and pure fresh construction; deeply frozen successful/rejected inputs remain unchanged | decoder and frozen-input cases | pass |
| APT-TEST-C09 | exact `QuestionDerivationRef` variants; exact superseded question fact identity; injected snapshot declared-field/pointer verification that fails closed when unavailable | `QuestionDerivationRef is an exact local union...` | pass |
| APT-TEST-C12 | typed nested/evidence refs; fact evidence and all problem block subjects resolve one current local Entity among eight fact-bearing kinds | nested/evidence/block-target cases | pass |
| APT-TEST-R7 | structural profile/registry equality only; no registry authority claim | `Profile matching is structural...` | pass |
| APT-TEST-C17 | duplicate source-observation rejection and nested registry unknown-field rejection | probe structural cases | pass |
| APT-TEST-C08/R7 | exact `probe`/`probe_bundle` OriginRef shapes, namespaces, profile/digest and acceptance evidence | `OriginRef probe and probe_bundle...` | pass |
| APT-TEST-R6 | fixture provenance label and deterministic candidate replay | fixture/replay candidate cases | pass |
| APT-TEST-C07 | UTF-8 byte bounds, full-artifact digest and selected-slice digest | `Selector checks byte bounds...` | pass |
| APT-TEST-C11/C12 | relation target existence/type/same-capture locality | `Relation targets must exist...` | pass |
| APT-TEST-C13/C14 | exact check enums, relation/use identity equality, and formalization/claim locality | `Check and formalization targets...` | pass |
| APT-TEST-R1 | exact link duplicate; conflicting Dispatch owner; same Session may link another Dispatch | `Join returns exact duplicate...` | pass |
| APT-TEST-C02 | explicit host/human rollover authorization | `Rollover needs explicit...` | pass |
| APT-TEST-R5/C06 | capture head CAS; current non-missing same-Dispatch/snapshot synthesis pin | `Capture correction and synthesis...` | pass |
| APT-TEST-C15 | fact subject-head predecessor CAS | `Entity fact CAS...` | pass |
| APT-TEST-C16 | aggregate CAS; target exact current Entity in same current non-missing capture; target-kind disposition/assessment enums | aggregate/current/cross-kind cases | pass |
| APT-TEST-C18 | injected candidate canonical bytes with bytewise ordering; Unicode/case vector; no ACI compatibility claim | candidate canonicalizer case | pass |
| APT-TEST-C01/C04/C07/R8 | one strict RFC3339 decoder for Session/link/capture/fact/extraction/telemetry plus completion outcome matrix | shared timestamp/completion cases | pass |

Planned/not-run: complete rule/clause variant matrices, property generators, every operation ID,
event-envelope conformance, interface/adapter cases, durable atomicity, crash/race, accepted-prefix,
checkpoint/replay parity, ACI profile conformance, observability exporter faults and all L3/L4
integration families.
