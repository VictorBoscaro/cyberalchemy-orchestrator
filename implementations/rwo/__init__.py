"""Local, deterministic prototype of the Recursive Work Orchestrator.

The package contains a pure semantic kernel and explicitly in-memory adapter
examples.  It intentionally does not open a network connection, persist a
journal, or perform work on behalf of a command intent.
"""

from .kernel import (
    CommandIntentResult,
    CompileOutcome,
    CompiledGraph,
    ReduceOutcome,
    compile_work_graph,
    derive_command_intent,
    reduce_event,
)

__all__ = [
    "CommandIntentResult",
    "CompileOutcome",
    "CompiledGraph",
    "ReduceOutcome",
    "compile_work_graph",
    "derive_command_intent",
    "reduce_event",
]
