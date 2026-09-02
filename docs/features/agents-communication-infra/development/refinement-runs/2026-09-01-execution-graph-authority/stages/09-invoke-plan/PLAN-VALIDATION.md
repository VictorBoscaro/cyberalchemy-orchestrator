# Automatic Distill validation of the plan

- Smallest coherent unit: accepted v2 specification + conformance vectors.
- Smallest work unit: `SPEC-ACI-EXECUTION-GRAPH-V2-001` only.
- Recomposition: L0 contract feeds L1 vectors; their PASS gates L2 compiler/projector; L2 gates L3
  acceptance; L3 separately gates L4 execution.
- Scope test: first unit changes specifications/fixtures/ledger only after review; it cannot mutate
  runtime code.
- Evidence test: acceptance criteria are observable through schema, semantic, digest, projection
  and negative-vector checks.
- Authority test: no layer may invent product choices or promote itself.
- Verdict: `pass` for planning, `block` for code entry until L0/L1 review evidence exists.
