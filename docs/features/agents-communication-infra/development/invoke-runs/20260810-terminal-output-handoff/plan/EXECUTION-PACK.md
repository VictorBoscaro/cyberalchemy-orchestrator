# Execution Pack: Bounded Terminal-Output Handoff

## Control

| Field | Value |
| --- | --- |
| planningGateStatus | block pending HTR-000 host-payload preflight |
| complexity | high |
| baselineWave | W0 |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| specRef | `../../../../specs/SPEC.md` |
| activeLayerWindow | L0 |
| readinessProfile | pilot |

## Choreography

| Wave | Layer | Units | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | `SWU-ACI-HTR-000`, `SWU-ACI-HTR-001`, `SWU-ACI-HTR-002` | Accepted exact-response design. | Canonical host payload is proven; service commit and Codex capture then pass independently and end to end. |
| [W1](work-pack/waves/W1.md) | L1 | `SWU-ACI-HTR-003` | W0 receipts pass. | One producer unlocks one consumer exactly once across replay. |
| [W2](work-pack/waves/W2.md) | L2 roadmap | `SWU-ACI-HTR-004A`, `SWU-ACI-HTR-004B` | New normative spec/design version plus W1 proof. | Ordered complete fan-in first; declared-seat complete-close gate second. |
| [W3](work-pack/waves/W3.md) | L3 roadmap | `SWU-ACI-HTR-005`, `SWU-ACI-HTR-006`, verification exemption | W2 passes and the research record still verifies. | Research closes with `research.md`/`findings.md`; review closes separately with `review.md`. |

The executable frontier stops at HTR-003 because the accepted design authorizes only L0/L1. W2/W3 are roadmap until normative revalidation. A failed HTR-000 stops before runtime mutation; no path-based fallback is admitted.
