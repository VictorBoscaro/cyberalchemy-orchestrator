"""Pure compiler and reducer for the RWO semantic-contract first slice.

This module deliberately owns only deterministic structural semantics:
composition compilation, command derivation, and cursor reduction.  It never
accepts an event into a real journal, schedules delivery, opens a transport, or
executes a command.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .canonical import (
    CanonicalizationError,
    DuplicateSemanticIdentity,
    canonical_payload_bytes,
    normalize_semantic_collection,
    semantic_digest,
    utf16_sort_key,
)
from .contract import Defect, VersionRegistry, VersionTuple, admit_json


CONTRACT_ID = "RWO-SEMANTIC-CONTRACT"
CONTRACT_VERSION = "1.0.0"
PROFILE_ID = "RWO-JCS-IJSON-SAFEINT"
PROFILE_VERSION = "1.0.0"
REDUCER_SEMANTICS_VERSION = "1.0.0"
_PHASE_RANK = {
    "decode": 0,
    "admission": 1,
    "schema": 2,
    "normalization": 3,
    "compilation": 4,
    "reduction": 5,
}


@dataclass(frozen=True)
class StructuralDefect:
    """A total-orderable kernel defect, independent of host exception text."""

    phase: str
    code: str
    path: tuple[str | int, ...] = ()
    detail_digest: str = ""

    def __post_init__(self) -> None:
        if self.phase not in _PHASE_RANK:
            raise ValueError(f"unknown RWO defect phase: {self.phase}")
        if not self.detail_digest:
            object.__setattr__(self, "detail_digest", _defect_detail_digest(self))


@dataclass(frozen=True)
class SourceBinding:
    """The registry's declared contract binding compared with local source bytes."""

    expected_sha256: str
    actual_sha256: str
    expected_size: int
    actual_size: int

    @property
    def valid(self) -> bool:
        return (
            self.expected_sha256 == self.actual_sha256
            and self.expected_size == self.actual_size
        )


@dataclass(frozen=True)
class SemanticRegistry:
    """Pinned schema registry loaded from the checked-in RWO contract surface."""

    document: Mapping[str, Any]
    version_registry: VersionRegistry
    schemas: Mapping[tuple[str, str], Mapping[str, Any]]
    payload_schemas: Mapping[tuple[str, str], Mapping[str, Any]]
    source_binding: SourceBinding

    def schema(self, schema_id: str, schema_version: str = "1.0.0") -> Mapping[str, Any]:
        try:
            return self.schemas[(schema_id, schema_version)]
        except KeyError as error:
            raise KeyError(f"unknown RWO schema {schema_id}/{schema_version}") from error

    def payload_schema(
        self, schema_ref: Mapping[str, Any]
    ) -> Mapping[str, Any] | None:
        schema_id = schema_ref.get("schema_id")
        schema_version = schema_ref.get("schema_version")
        if not isinstance(schema_id, str) or not isinstance(schema_version, str):
            return None
        return self.payload_schemas.get((schema_id, schema_version))


@dataclass(frozen=True)
class CompiledGraph:
    """A compiled WorkGraph bound to its immutable semantic identity."""

    graph: Mapping[str, Any]
    canonical_bytes: bytes
    graph_identity: str

    @classmethod
    def bind(
        cls, graph: Mapping[str, Any], *, graph_identity: str | None = None
    ) -> "CompiledGraph":
        """Bind a graph to bytes; tests may preserve an existing graph identity.

        Normal callers receive this object from :func:`compile_work_graph`.  The
        optional explicit identity exists for adversarial reducer tests that
        deliberately present malformed in-memory graph structure while holding
        the cursor's previously accepted identity fixed.
        """

        value = copy.deepcopy(dict(graph))
        payload = canonical_payload_bytes(value)
        identity = graph_identity or _typed_digest("WorkGraph", "WorkGraph", payload)
        return cls(value, payload, identity)


@dataclass(frozen=True)
class CompileOutcome:
    kind: str
    compiled: CompiledGraph | None = None
    defects: tuple[StructuralDefect, ...] = ()

    @property
    def graph(self) -> Mapping[str, Any] | None:
        return None if self.compiled is None else self.compiled.graph

    @property
    def canonical_bytes(self) -> bytes | None:
        return None if self.compiled is None else self.compiled.canonical_bytes

    @property
    def graph_identity(self) -> str | None:
        return None if self.compiled is None else self.compiled.graph_identity


@dataclass(frozen=True)
class CommandIntentResult:
    command: Mapping[str, Any] | None = None
    accepted_event_identity: str | None = None
    event_payload_digest: str | None = None
    command_intent_identity: str | None = None
    command_payload_digest: str | None = None
    defects: tuple[StructuralDefect, ...] = ()

    @property
    def admitted(self) -> bool:
        return not self.defects


@dataclass(frozen=True)
class ReduceOutcome:
    kind: str
    cursor: Mapping[str, Any]
    command: Mapping[str, Any] | None = None
    defects: tuple[StructuralDefect, ...] = ()
    accepted_event_identity: str | None = None
    event_payload_digest: str | None = None
    command_intent_identity: str | None = None
    command_payload_digest: str | None = None


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_default_registry() -> SemanticRegistry:
    """Load the local RWO schema registry and expose any source-binding drift."""

    contract_root = _repository_root() / (
        "docs/features/recursive-work-orchestrator/development/decision-gates/"
        "20260807T173437Z-rwo-language-contract-v2"
    )
    registry_path = contract_root / "schemas/registry.json"
    document = json.loads(registry_path.read_text(encoding="utf-8"))
    schemas: dict[tuple[str, str], Mapping[str, Any]] = {}
    for entry in document["schemas"]:
        path = registry_path.parent / entry["path"]
        schemas[(entry["schemaId"], entry["schemaVersion"])] = json.loads(
            path.read_text(encoding="utf-8")
        )
    payload_schemas = {
        (entry["schemaId"], entry["schemaVersion"]): entry["schema"]
        for entry in document.get("inlinePayloadSchemas", [])
    }
    contract_path = contract_root / "RWO-SEMANTIC-CONTRACT-1.0.0.md"
    contract_bytes = contract_path.read_bytes()
    declared = document["contract"]
    return SemanticRegistry(
        document=document,
        version_registry=VersionRegistry.from_document(document),
        schemas=schemas,
        payload_schemas=payload_schemas,
        source_binding=SourceBinding(
            expected_sha256=declared["sha256"],
            actual_sha256=hashlib.sha256(contract_bytes).hexdigest(),
            expected_size=declared["sizeBytes"],
            actual_size=len(contract_bytes),
        ),
    )


def _typed_digest(schema_id: str, value_type: str, payload: bytes) -> str:
    return semantic_digest(
        CONTRACT_ID,
        CONTRACT_VERSION,
        PROFILE_ID,
        PROFILE_VERSION,
        schema_id,
        "1.0.0",
        value_type,
        payload,
    )


def _path_sort_key(path: tuple[str | int, ...]) -> tuple[tuple[int, Any], ...]:
    return tuple(
        (0, utf16_sort_key(segment)) if isinstance(segment, str) else (1, segment)
        for segment in path
    )


def _defect_detail_digest(defect: StructuralDefect) -> str:
    wire_path = [
        {"kind": "field", "name": part}
        if isinstance(part, str)
        else {"kind": "index", "index": part}
        for part in defect.path
    ]
    payload = canonical_payload_bytes(
        {"phase": defect.phase, "path": wire_path, "code": defect.code}
    )
    return _typed_digest("StructuralDefect", "DefectDetail", payload)


def order_defects(
    defects: Iterable[StructuralDefect],
) -> tuple[StructuralDefect, ...]:
    """Apply the contract's total structural-defect comparator.

    A repeated fully equal defect is an implementation failure rather than a
    silently deduplicated outcome.
    """

    values = tuple(defects)
    if len(set(values)) != len(values):
        raise ValueError("duplicate fully-equal structural defect")
    return tuple(
        sorted(
            values,
            key=lambda defect: (
                _PHASE_RANK[defect.phase],
                _path_sort_key(defect.path),
                defect.code.encode("ascii"),
                defect.detail_digest.encode("ascii"),
            ),
        )
    )


def _defect(
    phase: str, code: str, path: Sequence[str | int] = ()
) -> StructuralDefect:
    return StructuralDefect(phase, code, tuple(path))


def _as_structural(defects: Iterable[Defect]) -> tuple[StructuralDefect, ...]:
    return order_defects(
        _defect(defect.phase, defect.code, defect.path) for defect in defects
    )


def _version_tuple(schema_id: str, value_type: str) -> VersionTuple:
    return VersionTuple(
        CONTRACT_ID,
        CONTRACT_VERSION,
        PROFILE_ID,
        PROFILE_VERSION,
        schema_id,
        "1.0.0",
        value_type,
    )


def _admit_document(
    value: Any,
    *,
    schema_id: str,
    value_type: str,
    schema: Mapping[str, Any],
    registry: SemanticRegistry,
) -> tuple[Any | None, tuple[StructuralDefect, ...]]:
    try:
        raw = canonical_payload_bytes(value)
    except CanonicalizationError:
        return None, (_defect("admission", "CANONICALIZATION_FAILED"),)
    result = admit_json(
        raw,
        version_tuple=_version_tuple(schema_id, value_type),
        registry=registry.version_registry,
        schema=dict(schema),
    )
    if not result.admitted:
        return None, _as_structural(result.defects)
    return result.value, ()


def _admit_payload(
    value: Any, schema: Mapping[str, Any]
) -> tuple[Any | None, tuple[StructuralDefect, ...]]:
    try:
        raw = canonical_payload_bytes(value)
    except CanonicalizationError:
        return None, (_defect("admission", "CANONICALIZATION_FAILED"),)
    result = admit_json(raw, schema=dict(schema))
    if not result.admitted:
        return None, _as_structural(result.defects)
    return result.value, ()


def _normalize_collection_fields(
    value: Mapping[str, Any], fields: Mapping[str, Sequence[str]]
) -> tuple[Mapping[str, Any] | None, tuple[StructuralDefect, ...]]:
    normalized = copy.deepcopy(dict(value))
    try:
        for field, primary_key_paths in fields.items():
            normalized[field] = normalize_semantic_collection(
                normalized[field], primary_key_paths
            )
    except DuplicateSemanticIdentity:
        return None, (_defect("normalization", "DUPLICATE_SEMANTIC_IDENTITY"),)
    except CanonicalizationError:
        return None, (_defect("normalization", "NORMALIZATION_FAILED"),)
    return normalized, ()


def normalize_for_schema(
    value: Mapping[str, Any], schema: Mapping[str, Any]
) -> tuple[Mapping[str, Any] | None, tuple[StructuralDefect, ...]]:
    """Apply the registered schema's declared order-insensitive collection rules."""

    declarations = schema.get("x-rwo-normalization", {})
    fields: dict[str, Sequence[str]] = {}
    if isinstance(declarations, Mapping):
        for field, declaration in declarations.items():
            if not isinstance(field, str) or not isinstance(declaration, Mapping):
                continue
            paths = declaration.get("primaryKeyPaths")
            if isinstance(paths, list) and all(isinstance(path, str) for path in paths):
                fields[field] = tuple(paths)
    return _normalize_collection_fields(value, fields)


def _schema_shape(schema: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return the first-slice compatibility shape, excluding descriptive keys."""

    ignored = {"$schema", "$id", "title", "description"}
    result: dict[str, Any] = {}
    for key, value in schema.items():
        if key in ignored:
            continue
        if isinstance(value, Mapping):
            result[key] = _schema_shape(value)
        elif isinstance(value, list):
            result[key] = [
                _schema_shape(item) if isinstance(item, Mapping) else item
                for item in value
            ]
        else:
            result[key] = value
    return result


def _validate_graph_declarations(
    composition: Mapping[str, Any], registry: SemanticRegistry
) -> tuple[StructuralDefect, ...]:
    defects: list[StructuralDefect] = []
    node_ids = {node["node_id"] for node in composition["nodes"]}
    for index, edge in enumerate(composition["edges"]):
        if edge["source_node_id"] not in node_ids:
            defects.append(
                _defect("compilation", "MISSING_ENDPOINT", ("edges", index, "source_node_id"))
            )
        if edge["target_node_id"] not in node_ids:
            defects.append(
                _defect("compilation", "MISSING_ENDPOINT", ("edges", index, "target_node_id"))
            )
        event_schema = registry.payload_schema(edge["event_payload_schema"])
        command_schema = registry.payload_schema(edge["command_payload_schema"])
        if event_schema is None:
            defects.append(
                _defect(
                    "compilation",
                    "PAYLOAD_SCHEMA_UNSUPPORTED",
                    ("edges", index, "event_payload_schema"),
                )
            )
        if command_schema is None:
            defects.append(
                _defect(
                    "compilation",
                    "PAYLOAD_SCHEMA_UNSUPPORTED",
                    ("edges", index, "command_payload_schema"),
                )
            )
        if (
            event_schema is not None
            and command_schema is not None
            and canonical_payload_bytes(_schema_shape(event_schema))
            != canonical_payload_bytes(_schema_shape(command_schema))
        ):
            defects.append(
                _defect("compilation", "INCOMPATIBLE_PAYLOAD_SCHEMA", ("edges", index))
            )
    return order_defects(defects)


def compile_work_graph(
    composition: Mapping[str, Any], *, registry: SemanticRegistry | None = None
) -> CompileOutcome:
    """Compile one explicit composition into a normalized, identity-bound graph."""

    registry = registry or load_default_registry()
    admitted, defects = _admit_document(
        composition,
        schema_id="ExplicitComposition",
        value_type="ExplicitComposition",
        schema=registry.schema("ExplicitComposition"),
        registry=registry,
    )
    if defects or not isinstance(admitted, Mapping):
        return CompileOutcome("Rejected", defects=defects)
    normalized, defects = normalize_for_schema(
        admitted, registry.schema("ExplicitComposition")
    )
    if defects or normalized is None:
        return CompileOutcome("Rejected", defects=defects)
    declaration_defects = _validate_graph_declarations(normalized, registry)
    if declaration_defects:
        return CompileOutcome("Rejected", defects=declaration_defects)

    graph = copy.deepcopy(dict(normalized))
    graph["schema_id"] = "WorkGraph"
    admitted_graph, defects = _admit_document(
        graph,
        schema_id="WorkGraph",
        value_type="WorkGraph",
        schema=registry.schema("WorkGraph"),
        registry=registry,
    )
    if defects or not isinstance(admitted_graph, Mapping):
        return CompileOutcome("Rejected", defects=defects)
    normalized_graph, defects = normalize_for_schema(
        admitted_graph, registry.schema("WorkGraph")
    )
    if defects or normalized_graph is None:
        return CompileOutcome("Rejected", defects=defects)
    compiled = CompiledGraph.bind(normalized_graph)
    return CompileOutcome("Compiled", compiled=compiled)


def _event_identity(event: Mapping[str, Any]) -> str:
    return _typed_digest(
        "AcceptedEventView",
        "AcceptedEventIdentity",
        canonical_payload_bytes(
            {"stream_id": event["stream_id"], "event_id": event["event_id"]}
        ),
    )


def _event_payload_digest(event: Mapping[str, Any]) -> str:
    return _typed_digest(
        "AcceptedEventView",
        "AcceptedEventPayload",
        canonical_payload_bytes(
            {
                "event_type": event["event_type"],
                "source_node_id": event["source_node_id"],
                "payload": event["payload"],
            }
        ),
    )


def _command_identity_payload(command: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "graph_identity": command["graph_identity"],
        "edge_id": command["edge_id"],
        "accepted_event_identity": command["accepted_event_identity"],
        "command_type": command["command_type"],
        "target_node_id": command["target_node_id"],
    }


def _command_payload(command: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "command_type": command["command_type"],
        "target_node_id": command["target_node_id"],
        "payload": command["payload"],
    }


def derive_command_intent(
    compiled: CompiledGraph,
    event: Mapping[str, Any],
    edge: Mapping[str, Any],
    *,
    registry: SemanticRegistry | None = None,
) -> CommandIntentResult:
    """Derive one immutable CommandIntent for a matching graph edge."""

    registry = registry or load_default_registry()
    admitted_event, defects = _admit_document(
        event,
        schema_id="AcceptedEventView",
        value_type="AcceptedEventView",
        schema=registry.schema("AcceptedEventView"),
        registry=registry,
    )
    if defects or not isinstance(admitted_event, Mapping):
        return CommandIntentResult(defects=defects)
    if (
        admitted_event["source_node_id"] != edge["source_node_id"]
        or admitted_event["event_type"] != edge["event_type"]
    ):
        return CommandIntentResult(
            defects=(_defect("reduction", "EDGE_EVENT_MISMATCH"),)
        )
    event_schema = registry.payload_schema(edge["event_payload_schema"])
    command_schema = registry.payload_schema(edge["command_payload_schema"])
    if event_schema is None or command_schema is None:
        return CommandIntentResult(
            defects=(_defect("compilation", "PAYLOAD_SCHEMA_UNSUPPORTED"),)
        )
    payload, defects = _admit_payload(admitted_event["payload"], event_schema)
    if defects or not isinstance(payload, Mapping):
        return CommandIntentResult(defects=defects)
    command_payload, defects = _admit_payload(copy.deepcopy(payload), command_schema)
    if defects or not isinstance(command_payload, Mapping):
        return CommandIntentResult(defects=defects)

    accepted_event_identity = _event_identity(admitted_event)
    event_payload_digest = _event_payload_digest(admitted_event)
    command = {
        "contract_id": CONTRACT_ID,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID,
        "profile_version": PROFILE_VERSION,
        "schema_id": "CommandIntent",
        "schema_version": "1.0.0",
        "graph_identity": compiled.graph_identity,
        "edge_id": edge["edge_id"],
        "accepted_event_identity": accepted_event_identity,
        "command_type": edge["command_type"],
        "target_node_id": edge["target_node_id"],
        "payload": command_payload,
    }
    admitted_command, defects = _admit_document(
        command,
        schema_id="CommandIntent",
        value_type="CommandIntent",
        schema=registry.schema("CommandIntent"),
        registry=registry,
    )
    if defects or not isinstance(admitted_command, Mapping):
        return CommandIntentResult(defects=defects)
    command_intent_identity = _typed_digest(
        "CommandIntent",
        "CommandIntentIdentity",
        canonical_payload_bytes(_command_identity_payload(admitted_command)),
    )
    command_payload_digest = _typed_digest(
        "CommandIntent",
        "CommandIntentPayload",
        canonical_payload_bytes(_command_payload(admitted_command)),
    )
    return CommandIntentResult(
        command=admitted_command,
        accepted_event_identity=accepted_event_identity,
        event_payload_digest=event_payload_digest,
        command_intent_identity=command_intent_identity,
        command_payload_digest=command_payload_digest,
    )


def _normalize_cursor(
    cursor: Mapping[str, Any], registry: SemanticRegistry
) -> Mapping[str, Any]:
    result, defects = normalize_for_schema(cursor, registry.schema("OrchestrationCursor"))
    if defects or result is None:
        raise ValueError("cursor normalization failed after successful reduction")
    return result


def _reduce_rejected(
    cursor: Mapping[str, Any], defects: Iterable[StructuralDefect]
) -> ReduceOutcome:
    return ReduceOutcome("Rejected", cursor=cursor, defects=order_defects(defects))


def _matching_edges(
    graph: Mapping[str, Any], event: Mapping[str, Any]
) -> list[Mapping[str, Any]]:
    return [
        edge
        for edge in graph["edges"]
        if edge["source_node_id"] == event["source_node_id"]
        and edge["event_type"] == event["event_type"]
    ]


def reduce_event(
    compiled: CompiledGraph,
    cursor: Mapping[str, Any],
    event: Mapping[str, Any],
    *,
    registry: SemanticRegistry | None = None,
) -> ReduceOutcome:
    """Reduce one accepted event without mutating the caller's cursor or event."""

    registry = registry or load_default_registry()
    # The reducer semantic version is a compatibility tuple member, not merely
    # an incidental cursor-schema constant.  Classify it before generic schema
    # validation so callers receive the contract's closed compatibility defect.
    if (
        isinstance(cursor, Mapping)
        and cursor.get("reducer_semantics_version") != REDUCER_SEMANTICS_VERSION
    ):
        return _reduce_rejected(
            cursor,
            (
                _defect(
                    "reduction",
                    "VERSION_TUPLE_UNSUPPORTED",
                    ("reducer_semantics_version",),
                ),
            ),
        )
    admitted_cursor, defects = _admit_document(
        cursor,
        schema_id="OrchestrationCursor",
        value_type="OrchestrationCursor",
        schema=registry.schema("OrchestrationCursor"),
        registry=registry,
    )
    if defects or not isinstance(admitted_cursor, Mapping):
        return _reduce_rejected(cursor, defects)
    admitted_event, defects = _admit_document(
        event,
        schema_id="AcceptedEventView",
        value_type="AcceptedEventView",
        schema=registry.schema("AcceptedEventView"),
        registry=registry,
    )
    if defects or not isinstance(admitted_event, Mapping):
        return _reduce_rejected(cursor, defects)
    compatibility_defects: list[StructuralDefect] = []
    if admitted_cursor["reducer_semantics_version"] != REDUCER_SEMANTICS_VERSION:
        compatibility_defects.append(
            _defect("reduction", "VERSION_TUPLE_UNSUPPORTED", ("reducer_semantics_version",))
        )
    if admitted_cursor["graph_identity"] != compiled.graph_identity:
        compatibility_defects.append(
            _defect("reduction", "GRAPH_IDENTITY_MISMATCH", ("graph_identity",))
        )
    if admitted_cursor["stream_id"] != admitted_event["stream_id"]:
        compatibility_defects.append(
            _defect("reduction", "STREAM_ID_MISMATCH", ("stream_id",))
        )
    if compatibility_defects:
        return _reduce_rejected(cursor, compatibility_defects)

    accepted_event_identity = _event_identity(admitted_event)
    event_payload_digest = _event_payload_digest(admitted_event)
    all_matches = _matching_edges(compiled.graph, admitted_event)
    existing_events = {
        entry["accepted_event_identity"]: entry["event_payload_digest"]
        for entry in admitted_cursor["accepted_events"]
    }
    if accepted_event_identity in existing_events:
        if existing_events[accepted_event_identity] != event_payload_digest:
            return ReduceOutcome(
                "DivergentDuplicate",
                cursor=cursor,
                defects=(_defect("reduction", "DIVERGENT_DUPLICATE", ("accepted_events",)),),
                accepted_event_identity=accepted_event_identity,
                event_payload_digest=event_payload_digest,
            )
        # A corrupt cursor with a stored command digest must never hide behind
        # duplicate convergence.  The CMD-002 vector exercises this preflight.
        if len(all_matches) == 1:
            derived = derive_command_intent(
                compiled, admitted_event, all_matches[0], registry=registry
            )
            if derived.admitted and derived.command_intent_identity is not None:
                emitted = {
                    entry["command_intent_identity"]: entry["command_payload_digest"]
                    for entry in admitted_cursor["emitted_commands"]
                }
                stored = emitted.get(derived.command_intent_identity)
                if stored is not None and stored != derived.command_payload_digest:
                    return _reduce_rejected(
                        cursor,
                        (_defect("reduction", "DIVERGENT_COMMAND_INTENT", ("emitted_commands",)),),
                    )
        return ReduceOutcome(
            "Duplicate",
            cursor=cursor,
            accepted_event_identity=accepted_event_identity,
            event_payload_digest=event_payload_digest,
        )

    satisfied = set(admitted_cursor["satisfied_edge_ids"])
    matches = [edge for edge in all_matches if edge["edge_id"] not in satisfied]
    if len(matches) > 1:
        return _reduce_rejected(
            cursor, (_defect("reduction", "MULTIPLE_EDGE_MATCH", ("edges",)),)
        )

    next_cursor = copy.deepcopy(dict(admitted_cursor))
    next_cursor["accepted_events"].append(
        {
            "accepted_event_identity": accepted_event_identity,
            "event_payload_digest": event_payload_digest,
        }
    )
    if not matches:
        return ReduceOutcome(
            "Applied",
            cursor=_normalize_cursor(next_cursor, registry),
            accepted_event_identity=accepted_event_identity,
            event_payload_digest=event_payload_digest,
        )

    derived = derive_command_intent(compiled, admitted_event, matches[0], registry=registry)
    if not derived.admitted or derived.command is None:
        return _reduce_rejected(cursor, derived.defects)
    emitted = {
        entry["command_intent_identity"]: entry["command_payload_digest"]
        for entry in admitted_cursor["emitted_commands"]
    }
    stored_payload_digest = emitted.get(derived.command_intent_identity)
    if stored_payload_digest is not None:
        if stored_payload_digest != derived.command_payload_digest:
            return _reduce_rejected(
                cursor,
                (_defect("reduction", "DIVERGENT_COMMAND_INTENT", ("emitted_commands",)),),
            )
        next_cursor["satisfied_edge_ids"].append(matches[0]["edge_id"])
        return ReduceOutcome(
            "Applied",
            cursor=_normalize_cursor(next_cursor, registry),
            accepted_event_identity=derived.accepted_event_identity,
            event_payload_digest=derived.event_payload_digest,
        )

    next_cursor["satisfied_edge_ids"].append(matches[0]["edge_id"])
    next_cursor["emitted_commands"].append(
        {
            "command_intent_identity": derived.command_intent_identity,
            "command_payload_digest": derived.command_payload_digest,
        }
    )
    return ReduceOutcome(
        "Applied",
        cursor=_normalize_cursor(next_cursor, registry),
        command=derived.command,
        accepted_event_identity=derived.accepted_event_identity,
        event_payload_digest=derived.event_payload_digest,
        command_intent_identity=derived.command_intent_identity,
        command_payload_digest=derived.command_payload_digest,
    )
