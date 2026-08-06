# Stage 06 Companion — Implementation Layering Seed

This is a Design seed, not the Plan-owned layering artifact.

| Layer | Question | Candidate evidence |
| --- | --- | --- |
| L0 | Can pure schemas and a deterministic classifier distinguish all treatments safely? | closed case/decision schemas, ordered table, RWF-001–016 fixtures |
| L1 | Can accepted decisions be persisted once and allocate identities/budgets/fences safely? | compare-and-append integration, replay, concurrency fixtures |
| L2 | Can domain mappings, ARE references, ACI acceptance, reconciliation, compensation, and degraded owner paths conform? | cross-owner schemas, negative zero-call fixtures, conformance receipts |
| L3 | Can the model be packaged/adopted without rewriting history or silently changing policy? | migrations, compatibility, observability, rollout and promotion owner evidence |

Promotion between layers requires passing evidence from the preceding layer.

