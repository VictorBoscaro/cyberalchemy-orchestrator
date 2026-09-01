# RWO local Python prototype

This directory contains a deterministic, no-network prototype of the RWO
semantic core.

```text
ExplicitComposition
  -> compile_work_graph
  -> CompiledGraph
  -> reduce_event(graph, cursor, AcceptedEventView)
  -> zero or one immutable CommandIntent
  -> optional in-memory delivery observation
```

The pure kernel is in `kernel.py`. `retry.py` classifies one already-known
delivery situation but does not schedule it. `adapters.py` and `runtime.py` are
process-local test doubles; they are not a journal, queue, gRPC service, Redis
adapter, cloud-bus adapter, persistence layer, or effect executor.

Run the conformance and prototype tests from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  implementations.tests.rwo.test_contract_vectors \
  implementations.tests.rwo.test_kernel_vectors \
  implementations.tests.rwo.test_cross_language_witness \
  implementations.tests.rwo.test_prototype -v

PYTHONDONTWRITEBYTECODE=1 python3 -m implementations.rwo
```

The test suite verifies the accepted `snapshot-bridge` source-binding mode:
the repaired live registry binds the live semantic contract, while the frozen
manifest and detached review remain pinned to their immutable baseline bytes.
This is local conformance evidence only. It does not claim that the immutable
manifest directly binds the repaired registry, nor does it grant release,
promotion, runtime, or journal authority.

`test_cross_language_witness` invokes the offline Rust observation binary and
compares its compiler/reducer/defect/retry facts with independently calculated
Python results. It is structural parity evidence, not raw JSON-admission or
transport parity evidence.
