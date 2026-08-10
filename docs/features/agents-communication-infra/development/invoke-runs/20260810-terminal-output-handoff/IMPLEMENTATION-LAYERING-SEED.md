# Implementation layering seed
1. **L0 — durable producer evidence:** schema/migration plus exact response artifact commit and receipt verification; no downstream launch.
2. **L1 — one sequential handoff:** one producer, one required consumer slot, materialization and launch gate, restart-safe.
3. **L2 — bounded fan-in:** canonical slot order, total cardinality, typed missing/failed outcomes.
4. **L3 — governed rollout:** three-stage review topology, observability, compatibility retirement, and negative security suite.

The connected-topology compiler fence remains through L0 and is relaxed only for topologies proven by the active layer. `invoke plan` must turn these layers into executable units and assign owners.
