# Stage 04 — Bounded Research Decision

Capability owner: `refine`  
Mode: `bounded-research`  
Decision: use the already-confirmed frozen primary-source set; do not expand  
Verdict: PASS

## Transport Evidence

| Source family | Supported observation | Design consequence |
| --- | --- | --- |
| gRPC retry/status/flow-control guidance | retry has a commitment boundary; a status such as deadline exceeded can coexist with completed state change; stream writes may be buffered/flow-controlled | model committed, failed-known, and outcome-unknown observations; never equate write return/status with business acceptance |
| Redis Streams | consumer groups have pending entries, explicit acknowledgement, redelivery/claim, and stream identities | expose entry/consumer/ack metadata; do not treat pending, ack, or claim as Work or effect truth |
| CloudEvents | event envelope and protocol bindings are separate; source plus id supports duplicate identification | keep canonical event identity independent from transport binding; CloudEvents does not supply RWO delivery policy |
| EventBridge | target delivery uses bounded retry/backoff and optional dead-letter handling; delivery ordering is not universal | declare retry/DLQ/ordering scope and treat exhaustion as observation, not terminal Work meaning |
| AWS messaging comparison | managed services differ in communication model and ordering support | transport family names cannot substitute for an exact implementation/configuration capability manifest |

## Research Decision

External evidence closes the heterogeneity question but cannot select RWO
ownership. The design must model capabilities as explicit atoms and require
proof per implementation/configuration. No new source is needed for the
candidate design.

## Claim Boundary

The comparison is documentation evidence. It is not a transport test,
benchmark, adapter selection, implementation proof, or production guarantee.

