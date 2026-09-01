//! Pure RWO semantics with a host-pinned raw JSON admission boundary.
//!
//! The compiler/reducer core remains fixture-bound. Raw JSON admission is
//! isolated in `admission` and checks that its local ICU runtime exposes the
//! contract's exact Unicode 15.1 data before accepting strings.

use serde_json::{json, Map, Value};
use sha2::{Digest, Sha256};
use std::cmp::Ordering;

mod admission;

pub use admission::{
    admit_canonical_decimal, admit_json, admit_version_tuple, normalize_semantic_elements,
    unicode_runtime_version, AdmissionResult, VersionRegistry, VersionTuple,
};

pub const CONTRACT_ID: &str = "RWO-SEMANTIC-CONTRACT";
pub const CONTRACT_VERSION: &str = "1.0.0";
pub const PROFILE_ID: &str = "RWO-JCS-IJSON-SAFEINT";
pub const PROFILE_VERSION: &str = "1.0.0";
pub const REDUCER_SEMANTICS_VERSION: &str = "1.0.0";
const SAFE_INTEGER_MINIMUM: i64 = -9_007_199_254_740_991;
const SAFE_INTEGER_MAXIMUM: i64 = 9_007_199_254_740_991;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PathSegment {
    Field(String),
    Index(usize),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StructuralDefect {
    pub phase: String,
    pub code: String,
    pub path: Vec<PathSegment>,
    pub detail_digest: String,
}

impl StructuralDefect {
    pub fn new(phase: impl Into<String>, code: impl Into<String>, path: Vec<PathSegment>) -> Self {
        let phase = phase.into();
        let code = code.into();
        let detail_digest = defect_detail_digest(&phase, &code, &path);
        Self {
            phase,
            code,
            path,
            detail_digest,
        }
    }

    pub fn with_detail(
        phase: impl Into<String>,
        code: impl Into<String>,
        path: Vec<PathSegment>,
        detail_digest: impl Into<String>,
    ) -> Self {
        Self {
            phase: phase.into(),
            code: code.into(),
            path,
            detail_digest: detail_digest.into(),
        }
    }
}

fn phase_rank(phase: &str) -> usize {
    match phase {
        "decode" => 0,
        "admission" => 1,
        "schema" => 2,
        "normalization" => 3,
        "compilation" => 4,
        "reduction" => 5,
        _ => usize::MAX,
    }
}

fn utf16_cmp(left: &str, right: &str) -> Ordering {
    left.encode_utf16()
        .collect::<Vec<_>>()
        .cmp(&right.encode_utf16().collect::<Vec<_>>())
}

fn path_cmp(left: &[PathSegment], right: &[PathSegment]) -> Ordering {
    for (left_part, right_part) in left.iter().zip(right.iter()) {
        let order = match (left_part, right_part) {
            (PathSegment::Field(left_name), PathSegment::Field(right_name)) => {
                utf16_cmp(left_name, right_name)
            }
            (PathSegment::Index(left_index), PathSegment::Index(right_index)) => {
                left_index.cmp(right_index)
            }
            (PathSegment::Field(_), PathSegment::Index(_)) => Ordering::Less,
            (PathSegment::Index(_), PathSegment::Field(_)) => Ordering::Greater,
        };
        if order != Ordering::Equal {
            return order;
        }
    }
    left.len().cmp(&right.len())
}

/// Order defects with the contract comparator and reject a fully duplicate one.
pub fn order_defects(mut defects: Vec<StructuralDefect>) -> Result<Vec<StructuralDefect>, String> {
    defects.sort_by(|left, right| {
        phase_rank(&left.phase)
            .cmp(&phase_rank(&right.phase))
            .then_with(|| path_cmp(&left.path, &right.path))
            .then_with(|| left.code.as_bytes().cmp(right.code.as_bytes()))
            .then_with(|| {
                left.detail_digest
                    .as_bytes()
                    .cmp(right.detail_digest.as_bytes())
            })
    });
    if defects.windows(2).any(|pair| pair[0] == pair[1]) {
        return Err("duplicate fully-equal structural defect".to_owned());
    }
    Ok(defects)
}

pub(crate) fn ordered(defects: Vec<StructuralDefect>) -> Vec<StructuralDefect> {
    order_defects(defects).expect("internally generated defects must be distinct")
}

/// Serialize an already-admitted safe-integer value in the fixture's
/// RFC 8785-compatible shape.
pub fn canonical_payload_bytes(value: &Value) -> Result<Vec<u8>, String> {
    fn encode(value: &Value, output: &mut String) -> Result<(), String> {
        match value {
            Value::Null => output.push_str("null"),
            Value::Bool(value) => output.push_str(if *value { "true" } else { "false" }),
            Value::Number(value) => {
                let Some(value) = value.as_i64() else {
                    return Err("numbers must be safe integers".to_owned());
                };
                if !(SAFE_INTEGER_MINIMUM..=SAFE_INTEGER_MAXIMUM).contains(&value) {
                    return Err("integer is outside the safe profile".to_owned());
                }
                output.push_str(&value.to_string());
            }
            Value::String(value) => {
                output.push_str(&serde_json::to_string(value).map_err(|error| error.to_string())?)
            }
            Value::Array(values) => {
                output.push('[');
                for (index, item) in values.iter().enumerate() {
                    if index > 0 {
                        output.push(',');
                    }
                    encode(item, output)?;
                }
                output.push(']');
            }
            Value::Object(values) => {
                let mut keys = values.keys().collect::<Vec<_>>();
                keys.sort_by(|left, right| utf16_cmp(left, right));
                output.push('{');
                for (index, key) in keys.into_iter().enumerate() {
                    if index > 0 {
                        output.push(',');
                    }
                    output
                        .push_str(&serde_json::to_string(key).map_err(|error| error.to_string())?);
                    output.push(':');
                    encode(&values[key], output)?;
                }
                output.push('}');
            }
        }
        Ok(())
    }

    let mut output = String::new();
    encode(value, &mut output)?;
    Ok(output.into_bytes())
}

pub fn semantic_digest(
    contract_id: &str,
    contract_version: &str,
    profile_id: &str,
    profile_version: &str,
    schema_id: &str,
    schema_version: &str,
    value_type: &str,
    payload_bytes: &[u8],
) -> String {
    let mut hasher = Sha256::new();
    hasher.update(b"RWO-SEMANTIC-DIGEST\0");
    for item in [
        contract_id,
        contract_version,
        profile_id,
        profile_version,
        schema_id,
        schema_version,
        value_type,
    ] {
        let bytes = item.as_bytes();
        hasher.update((bytes.len() as u32).to_be_bytes());
        hasher.update(bytes);
    }
    hasher.update((payload_bytes.len() as u64).to_be_bytes());
    hasher.update(payload_bytes);
    format!("sha256:{:x}", hasher.finalize())
}

fn typed_digest(schema_id: &str, value_type: &str, value: &Value) -> Result<String, String> {
    let payload = canonical_payload_bytes(value)?;
    Ok(semantic_digest(
        CONTRACT_ID,
        CONTRACT_VERSION,
        PROFILE_ID,
        PROFILE_VERSION,
        schema_id,
        "1.0.0",
        value_type,
        &payload,
    ))
}

fn defect_detail_digest(phase: &str, code: &str, path: &[PathSegment]) -> String {
    let path = path
        .iter()
        .map(|segment| match segment {
            PathSegment::Field(name) => json!({"kind": "field", "name": name}),
            PathSegment::Index(index) => json!({"kind": "index", "index": index}),
        })
        .collect::<Vec<_>>();
    typed_digest(
        "StructuralDefect",
        "DefectDetail",
        &json!({"phase": phase, "path": path, "code": code}),
    )
    .expect("closed defect detail always has canonical fixture representation")
}

#[derive(Debug, Clone, PartialEq)]
pub struct CompiledGraph {
    pub graph: Value,
    pub canonical_bytes: Vec<u8>,
    pub graph_identity: String,
}

impl CompiledGraph {
    pub fn bind(graph: Value, graph_identity: Option<String>) -> Result<Self, String> {
        let canonical_bytes = canonical_payload_bytes(&graph)?;
        let graph_identity = match graph_identity {
            Some(identity) => identity,
            None => semantic_digest(
                CONTRACT_ID,
                CONTRACT_VERSION,
                PROFILE_ID,
                PROFILE_VERSION,
                "WorkGraph",
                "1.0.0",
                "WorkGraph",
                &canonical_bytes,
            ),
        };
        Ok(Self {
            graph,
            canonical_bytes,
            graph_identity,
        })
    }
}

/// A pure initial cursor together with its canonical semantic representation.
///
/// The local runtime deliberately asks the Rust semantic kernel to construct
/// this value. A host therefore never has to duplicate the cursor tuple,
/// graph identity, or normalization policy.
#[derive(Debug, Clone, PartialEq)]
pub struct InitialCursor {
    pub cursor: Value,
    pub canonical_bytes: Vec<u8>,
}

/// Construct the empty cursor for one admitted event stream and compiled graph.
///
/// This is deliberately pure: it neither records history nor retains state.
/// Callers that need a durable cursor must provide that separately; the local
/// child process only returns the canonical bytes for its host to hold.
pub fn initial_cursor(
    compiled: &CompiledGraph,
    admitted_stream_id: &str,
) -> Result<InitialCursor, String> {
    let cursor = json!({
        "contract_id": CONTRACT_ID,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID,
        "profile_version": PROFILE_VERSION,
        "schema_id": "OrchestrationCursor",
        "schema_version": "1.0.0",
        "reducer_semantics_version": REDUCER_SEMANTICS_VERSION,
        "graph_identity": compiled.graph_identity,
        "stream_id": admitted_stream_id,
        "accepted_events": [],
        "satisfied_edge_ids": [],
        "emitted_commands": [],
    });
    let canonical_bytes = canonical_payload_bytes(&cursor)?;
    Ok(InitialCursor {
        cursor,
        canonical_bytes,
    })
}

#[derive(Debug, Clone, PartialEq)]
pub struct CompileOutcome {
    pub kind: String,
    pub compiled: Option<CompiledGraph>,
    pub defects: Vec<StructuralDefect>,
}

impl CompileOutcome {
    fn rejected(defects: Vec<StructuralDefect>) -> Self {
        Self {
            kind: "Rejected".to_owned(),
            compiled: None,
            defects: ordered(defects),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct CommandIntentResult {
    pub command: Option<Value>,
    pub accepted_event_identity: Option<String>,
    pub event_payload_digest: Option<String>,
    pub command_intent_identity: Option<String>,
    pub command_payload_digest: Option<String>,
    pub defects: Vec<StructuralDefect>,
}

impl CommandIntentResult {
    pub fn admitted(&self) -> bool {
        self.defects.is_empty()
    }

    fn rejected(defects: Vec<StructuralDefect>) -> Self {
        Self {
            command: None,
            accepted_event_identity: None,
            event_payload_digest: None,
            command_intent_identity: None,
            command_payload_digest: None,
            defects: ordered(defects),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ReduceOutcome {
    pub kind: String,
    pub cursor: Value,
    pub command: Option<Value>,
    pub defects: Vec<StructuralDefect>,
    pub accepted_event_identity: Option<String>,
    pub event_payload_digest: Option<String>,
    pub command_intent_identity: Option<String>,
    pub command_payload_digest: Option<String>,
}

fn reject_reduce(cursor: &Value, defects: Vec<StructuralDefect>) -> ReduceOutcome {
    ReduceOutcome {
        kind: "Rejected".to_owned(),
        cursor: cursor.clone(),
        command: None,
        defects: ordered(defects),
        accepted_event_identity: None,
        event_payload_digest: None,
        command_intent_identity: None,
        command_payload_digest: None,
    }
}

fn object(value: &Value) -> Option<&Map<String, Value>> {
    value.as_object()
}

fn string_at<'a>(object: &'a Map<String, Value>, field: &str) -> Option<&'a str> {
    object.get(field)?.as_str()
}

fn closed_object_defects(
    object: &Map<String, Value>,
    required: &[&str],
    allowed: &[&str],
    path: &[PathSegment],
) -> Vec<StructuralDefect> {
    let mut defects = Vec::new();
    for field in required {
        if !object.contains_key(*field) {
            let mut field_path = path.to_vec();
            field_path.push(PathSegment::Field((*field).to_owned()));
            defects.push(StructuralDefect::new(
                "schema",
                "REQUIRED_FIELD_MISSING",
                field_path,
            ));
        }
    }
    for field in object.keys() {
        if !allowed.contains(&field.as_str()) {
            let mut field_path = path.to_vec();
            field_path.push(PathSegment::Field(field.clone()));
            defects.push(StructuralDefect::new("schema", "UNKNOWN_FIELD", field_path));
        }
    }
    defects
}

fn exact_tuple_defects(
    object: &Map<String, Value>,
    schema_id: &str,
    path: &[PathSegment],
) -> Vec<StructuralDefect> {
    let expected = [
        ("contract_id", CONTRACT_ID),
        ("contract_version", CONTRACT_VERSION),
        ("profile_id", PROFILE_ID),
        ("profile_version", PROFILE_VERSION),
        ("schema_id", schema_id),
        ("schema_version", "1.0.0"),
    ];
    expected
        .into_iter()
        .filter_map(|(field, value)| {
            (string_at(object, field) != Some(value)).then(|| {
                let mut field_path = path.to_vec();
                field_path.push(PathSegment::Field(field.to_owned()));
                StructuralDefect::new("admission", "VERSION_TUPLE_UNSUPPORTED", field_path)
            })
        })
        .collect()
}

fn normalize_semantic_collection(
    value: &mut Value,
    field: &str,
    primary_key: &str,
) -> Result<(), StructuralDefect> {
    let values = value
        .as_object_mut()
        .and_then(|object| object.get_mut(field))
        .and_then(Value::as_array_mut)
        .ok_or_else(|| {
            StructuralDefect::new(
                "schema",
                "SCHEMA_TYPE_MISMATCH",
                vec![PathSegment::Field(field.to_owned())],
            )
        })?;
    let mut decorated = values
        .drain(..)
        .map(|item| {
            let key = item
                .as_object()
                .and_then(|object| object.get(primary_key))
                .and_then(Value::as_str)
                .ok_or_else(|| {
                    StructuralDefect::new(
                        "normalization",
                        "NORMALIZATION_FAILED",
                        vec![PathSegment::Field(field.to_owned())],
                    )
                })?
                .to_owned();
            let payload = canonical_payload_bytes(&item).map_err(|_| {
                StructuralDefect::new(
                    "normalization",
                    "NORMALIZATION_FAILED",
                    vec![PathSegment::Field(field.to_owned())],
                )
            })?;
            Ok::<_, StructuralDefect>((key, payload, item))
        })
        .collect::<Result<Vec<_>, _>>()?;
    decorated
        .sort_by(|left, right| utf16_cmp(&left.0, &right.0).then_with(|| left.1.cmp(&right.1)));
    for pair in decorated.windows(2) {
        if pair[0].0 == pair[1].0 && pair[0].1 == pair[1].1 {
            return Err(StructuralDefect::new(
                "normalization",
                "DUPLICATE_SEMANTIC_IDENTITY",
                vec![PathSegment::Field(field.to_owned())],
            ));
        }
    }
    values.extend(decorated.into_iter().map(|(_, _, item)| item));
    Ok(())
}

fn validate_fixture_schema_ref(value: Option<&Value>) -> bool {
    let Some(object) = value.and_then(Value::as_object) else {
        return false;
    };
    matches!(
        (
            string_at(object, "schema_id"),
            string_at(object, "schema_version")
        ),
        (Some("FixtureEventPayload"), Some("1.0.0"))
            | (Some("FixtureCommandPayload"), Some("1.0.0"))
    )
}

/// Compile the frozen first-slice ExplicitComposition shape to WorkGraph.
pub fn compile_work_graph(composition: &Value) -> CompileOutcome {
    let Some(composition_object) = object(composition) else {
        return CompileOutcome::rejected(vec![StructuralDefect::new(
            "schema",
            "SCHEMA_TYPE_MISMATCH",
            vec![],
        )]);
    };
    let required = [
        "contract_id",
        "contract_version",
        "profile_id",
        "profile_version",
        "schema_id",
        "schema_version",
        "composition_id",
        "nodes",
        "edges",
    ];
    let mut defects = closed_object_defects(composition_object, &required, &required, &[]);
    defects.extend(exact_tuple_defects(
        composition_object,
        "ExplicitComposition",
        &[],
    ));
    if composition_object
        .get("nodes")
        .and_then(Value::as_array)
        .is_none()
    {
        defects.push(StructuralDefect::new(
            "schema",
            "SCHEMA_TYPE_MISMATCH",
            vec![PathSegment::Field("nodes".to_owned())],
        ));
    }
    if composition_object
        .get("edges")
        .and_then(Value::as_array)
        .is_none()
    {
        defects.push(StructuralDefect::new(
            "schema",
            "SCHEMA_TYPE_MISMATCH",
            vec![PathSegment::Field("edges".to_owned())],
        ));
    }
    if !defects.is_empty() {
        return CompileOutcome::rejected(defects);
    }

    let nodes = composition_object["nodes"]
        .as_array()
        .expect("checked array");
    let node_ids = nodes
        .iter()
        .filter_map(Value::as_object)
        .filter_map(|node| string_at(node, "node_id"))
        .collect::<Vec<_>>();
    let edges = composition_object["edges"]
        .as_array()
        .expect("checked array");
    for (index, edge) in edges.iter().enumerate() {
        let path = vec![
            PathSegment::Field("edges".to_owned()),
            PathSegment::Index(index),
        ];
        let Some(edge_object) = object(edge) else {
            defects.push(StructuralDefect::new(
                "schema",
                "SCHEMA_TYPE_MISMATCH",
                path,
            ));
            continue;
        };
        let edge_required = [
            "edge_id",
            "source_node_id",
            "target_node_id",
            "event_type",
            "event_payload_schema",
            "command_type",
            "command_payload_schema",
            "payload_derivation",
        ];
        defects.extend(closed_object_defects(
            edge_object,
            &edge_required,
            &edge_required,
            &path,
        ));
        for endpoint in ["source_node_id", "target_node_id"] {
            if let Some(node_id) = string_at(edge_object, endpoint) {
                if !node_ids.contains(&node_id) {
                    let mut endpoint_path = path.clone();
                    endpoint_path.push(PathSegment::Field(endpoint.to_owned()));
                    defects.push(StructuralDefect::new(
                        "compilation",
                        "MISSING_ENDPOINT",
                        endpoint_path,
                    ));
                }
            }
        }
        if !validate_fixture_schema_ref(edge_object.get("event_payload_schema"))
            || !validate_fixture_schema_ref(edge_object.get("command_payload_schema"))
        {
            defects.push(StructuralDefect::new(
                "compilation",
                "PAYLOAD_SCHEMA_UNSUPPORTED",
                path.clone(),
            ));
        }
        if string_at(edge_object, "payload_derivation") != Some("copy-event-payload") {
            let mut derivation_path = path.clone();
            derivation_path.push(PathSegment::Field("payload_derivation".to_owned()));
            defects.push(StructuralDefect::new(
                "schema",
                "INVALID_ENUM_VALUE",
                derivation_path,
            ));
        }
    }
    if !defects.is_empty() {
        return CompileOutcome::rejected(defects);
    }

    let mut graph = composition.clone();
    graph
        .as_object_mut()
        .expect("composition was object")
        .insert(
            "schema_id".to_owned(),
            Value::String("WorkGraph".to_owned()),
        );
    if let Err(defect) = normalize_semantic_collection(&mut graph, "nodes", "node_id") {
        return CompileOutcome::rejected(vec![defect]);
    }
    if let Err(defect) = normalize_semantic_collection(&mut graph, "edges", "edge_id") {
        return CompileOutcome::rejected(vec![defect]);
    }
    match CompiledGraph::bind(graph, None) {
        Ok(compiled) => CompileOutcome {
            kind: "Compiled".to_owned(),
            compiled: Some(compiled),
            defects: Vec::new(),
        },
        Err(_) => CompileOutcome::rejected(vec![StructuralDefect::new(
            "admission",
            "CANONICALIZATION_FAILED",
            vec![],
        )]),
    }
}

fn event_identity(event: &Map<String, Value>) -> Result<String, String> {
    typed_digest(
        "AcceptedEventView",
        "AcceptedEventIdentity",
        &json!({
            "stream_id": string_at(event, "stream_id").ok_or("missing stream_id")?,
            "event_id": string_at(event, "event_id").ok_or("missing event_id")?,
        }),
    )
}

fn event_payload_digest(event: &Map<String, Value>) -> Result<String, String> {
    typed_digest(
        "AcceptedEventView",
        "AcceptedEventPayload",
        &json!({
            "event_type": string_at(event, "event_type").ok_or("missing event_type")?,
            "source_node_id": string_at(event, "source_node_id").ok_or("missing source_node_id")?,
            "payload": event.get("payload").ok_or("missing payload")?,
        }),
    )
}

fn fixture_payload_valid(payload: Option<&Value>) -> bool {
    let Some(object) = payload.and_then(Value::as_object) else {
        return false;
    };
    object.len() == 1 && string_at(object, "job_id").is_some_and(|job_id| !job_id.is_empty())
}

fn command_identity_payload(command: &Map<String, Value>) -> Value {
    json!({
        "graph_identity": command["graph_identity"],
        "edge_id": command["edge_id"],
        "accepted_event_identity": command["accepted_event_identity"],
        "command_type": command["command_type"],
        "target_node_id": command["target_node_id"],
    })
}

fn command_payload(command: &Map<String, Value>) -> Value {
    json!({
        "command_type": command["command_type"],
        "target_node_id": command["target_node_id"],
        "payload": command["payload"],
    })
}

/// Derive the first-slice immutable command request. It never delivers it.
pub fn derive_command_intent(
    compiled: &CompiledGraph,
    event: &Value,
    edge: &Value,
) -> CommandIntentResult {
    let Some(event_object) = object(event) else {
        return CommandIntentResult::rejected(vec![StructuralDefect::new(
            "schema",
            "SCHEMA_TYPE_MISMATCH",
            vec![],
        )]);
    };
    let Some(edge_object) = object(edge) else {
        return CommandIntentResult::rejected(vec![StructuralDefect::new(
            "compilation",
            "PAYLOAD_SCHEMA_UNSUPPORTED",
            vec![],
        )]);
    };
    if string_at(event_object, "source_node_id") != string_at(edge_object, "source_node_id")
        || string_at(event_object, "event_type") != string_at(edge_object, "event_type")
    {
        return CommandIntentResult::rejected(vec![StructuralDefect::new(
            "reduction",
            "EDGE_EVENT_MISMATCH",
            vec![],
        )]);
    }
    if !validate_fixture_schema_ref(edge_object.get("event_payload_schema"))
        || !validate_fixture_schema_ref(edge_object.get("command_payload_schema"))
    {
        return CommandIntentResult::rejected(vec![StructuralDefect::new(
            "compilation",
            "PAYLOAD_SCHEMA_UNSUPPORTED",
            vec![],
        )]);
    }
    if !fixture_payload_valid(event_object.get("payload")) {
        return CommandIntentResult::rejected(vec![StructuralDefect::new(
            "schema",
            "SCHEMA_TYPE_MISMATCH",
            vec![PathSegment::Field("payload".to_owned())],
        )]);
    }
    let accepted_event_identity = match event_identity(event_object) {
        Ok(identity) => identity,
        Err(_) => {
            return CommandIntentResult::rejected(vec![StructuralDefect::new(
                "schema",
                "REQUIRED_FIELD_MISSING",
                vec![],
            )])
        }
    };
    let event_payload_digest = match event_payload_digest(event_object) {
        Ok(digest) => digest,
        Err(_) => {
            return CommandIntentResult::rejected(vec![StructuralDefect::new(
                "schema",
                "REQUIRED_FIELD_MISSING",
                vec![],
            )])
        }
    };
    let command = json!({
        "contract_id": CONTRACT_ID,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID,
        "profile_version": PROFILE_VERSION,
        "schema_id": "CommandIntent",
        "schema_version": "1.0.0",
        "graph_identity": compiled.graph_identity,
        "edge_id": string_at(edge_object, "edge_id").unwrap_or_default(),
        "accepted_event_identity": accepted_event_identity,
        "command_type": string_at(edge_object, "command_type").unwrap_or_default(),
        "target_node_id": string_at(edge_object, "target_node_id").unwrap_or_default(),
        "payload": event_object.get("payload").expect("validated payload"),
    });
    let command_object = command.as_object().expect("constructed command object");
    let command_intent_identity = typed_digest(
        "CommandIntent",
        "CommandIntentIdentity",
        &command_identity_payload(command_object),
    )
    .expect("constructed command is canonical");
    let command_payload_digest = typed_digest(
        "CommandIntent",
        "CommandIntentPayload",
        &command_payload(command_object),
    )
    .expect("constructed command is canonical");
    CommandIntentResult {
        command: Some(command),
        accepted_event_identity: Some(accepted_event_identity),
        event_payload_digest: Some(event_payload_digest),
        command_intent_identity: Some(command_intent_identity),
        command_payload_digest: Some(command_payload_digest),
        defects: Vec::new(),
    }
}

fn matching_edges(graph: &Value, event: &Map<String, Value>) -> Vec<Value> {
    graph
        .get("edges")
        .and_then(Value::as_array)
        .into_iter()
        .flatten()
        .filter(|edge| {
            let edge_object = edge.as_object();
            edge_object.and_then(|object| string_at(object, "source_node_id"))
                == string_at(event, "source_node_id")
                && edge_object.and_then(|object| string_at(object, "event_type"))
                    == string_at(event, "event_type")
        })
        .cloned()
        .collect()
}

fn normalize_cursor(cursor: &mut Value) -> Result<(), StructuralDefect> {
    let cursor_object = cursor
        .as_object_mut()
        .ok_or_else(|| StructuralDefect::new("schema", "SCHEMA_TYPE_MISMATCH", vec![]))?;
    for (field, key) in [
        ("accepted_events", "accepted_event_identity"),
        ("emitted_commands", "command_intent_identity"),
    ] {
        let values = cursor_object
            .get_mut(field)
            .and_then(Value::as_array_mut)
            .ok_or_else(|| {
                StructuralDefect::new(
                    "schema",
                    "SCHEMA_TYPE_MISMATCH",
                    vec![PathSegment::Field(field.to_owned())],
                )
            })?;
        values.sort_by(|left, right| {
            let left = left
                .as_object()
                .and_then(|item| string_at(item, key))
                .unwrap_or_default();
            let right = right
                .as_object()
                .and_then(|item| string_at(item, key))
                .unwrap_or_default();
            utf16_cmp(left, right)
        });
    }
    let satisfied = cursor_object
        .get_mut("satisfied_edge_ids")
        .and_then(Value::as_array_mut)
        .ok_or_else(|| {
            StructuralDefect::new(
                "schema",
                "SCHEMA_TYPE_MISMATCH",
                vec![PathSegment::Field("satisfied_edge_ids".to_owned())],
            )
        })?;
    satisfied.sort_by(|left, right| {
        utf16_cmp(
            left.as_str().unwrap_or_default(),
            right.as_str().unwrap_or_default(),
        )
    });
    Ok(())
}

/// Reduce one externally accepted event without journal, delivery, or mutation.
pub fn reduce_event(compiled: &CompiledGraph, cursor: &Value, event: &Value) -> ReduceOutcome {
    let Some(cursor_object) = object(cursor) else {
        return reject_reduce(
            cursor,
            vec![StructuralDefect::new(
                "schema",
                "SCHEMA_TYPE_MISMATCH",
                vec![],
            )],
        );
    };
    if string_at(cursor_object, "reducer_semantics_version") != Some(REDUCER_SEMANTICS_VERSION) {
        return reject_reduce(
            cursor,
            vec![StructuralDefect::new(
                "reduction",
                "VERSION_TUPLE_UNSUPPORTED",
                vec![PathSegment::Field("reducer_semantics_version".to_owned())],
            )],
        );
    }
    let Some(event_object) = object(event) else {
        return reject_reduce(
            cursor,
            vec![StructuralDefect::new(
                "schema",
                "SCHEMA_TYPE_MISMATCH",
                vec![],
            )],
        );
    };
    let mut compatibility_defects = Vec::new();
    if string_at(cursor_object, "graph_identity") != Some(compiled.graph_identity.as_str()) {
        compatibility_defects.push(StructuralDefect::new(
            "reduction",
            "GRAPH_IDENTITY_MISMATCH",
            vec![PathSegment::Field("graph_identity".to_owned())],
        ));
    }
    if string_at(cursor_object, "stream_id") != string_at(event_object, "stream_id") {
        compatibility_defects.push(StructuralDefect::new(
            "reduction",
            "STREAM_ID_MISMATCH",
            vec![PathSegment::Field("stream_id".to_owned())],
        ));
    }
    if !compatibility_defects.is_empty() {
        return reject_reduce(cursor, compatibility_defects);
    }
    let accepted_event_identity = match event_identity(event_object) {
        Ok(identity) => identity,
        Err(_) => {
            return reject_reduce(
                cursor,
                vec![StructuralDefect::new(
                    "schema",
                    "REQUIRED_FIELD_MISSING",
                    vec![],
                )],
            )
        }
    };
    let event_payload_digest = match event_payload_digest(event_object) {
        Ok(digest) => digest,
        Err(_) => {
            return reject_reduce(
                cursor,
                vec![StructuralDefect::new(
                    "schema",
                    "REQUIRED_FIELD_MISSING",
                    vec![],
                )],
            )
        }
    };
    let all_matches = matching_edges(&compiled.graph, event_object);
    let accepted_events = cursor_object
        .get("accepted_events")
        .and_then(Value::as_array)
        .cloned()
        .unwrap_or_default();
    if let Some(existing) = accepted_events.iter().find(|entry| {
        entry
            .as_object()
            .and_then(|entry| string_at(entry, "accepted_event_identity"))
            == Some(accepted_event_identity.as_str())
    }) {
        let existing_digest = existing
            .as_object()
            .and_then(|entry| string_at(entry, "event_payload_digest"));
        if existing_digest != Some(event_payload_digest.as_str()) {
            return ReduceOutcome {
                kind: "DivergentDuplicate".to_owned(),
                cursor: cursor.clone(),
                command: None,
                defects: vec![StructuralDefect::new(
                    "reduction",
                    "DIVERGENT_DUPLICATE",
                    vec![PathSegment::Field("accepted_events".to_owned())],
                )],
                accepted_event_identity: Some(accepted_event_identity),
                event_payload_digest: Some(event_payload_digest),
                command_intent_identity: None,
                command_payload_digest: None,
            };
        }
        if all_matches.len() == 1 {
            let derived = derive_command_intent(compiled, event, &all_matches[0]);
            if derived.admitted() {
                let emitted = cursor_object
                    .get("emitted_commands")
                    .and_then(Value::as_array)
                    .cloned()
                    .unwrap_or_default();
                if let (Some(identity), Some(digest)) = (
                    derived.command_intent_identity.as_deref(),
                    derived.command_payload_digest.as_deref(),
                ) {
                    if let Some(stored) = emitted.iter().find_map(|entry| {
                        let entry = entry.as_object()?;
                        (string_at(entry, "command_intent_identity") == Some(identity))
                            .then(|| string_at(entry, "command_payload_digest"))
                            .flatten()
                    }) {
                        if stored != digest {
                            return reject_reduce(
                                cursor,
                                vec![StructuralDefect::new(
                                    "reduction",
                                    "DIVERGENT_COMMAND_INTENT",
                                    vec![PathSegment::Field("emitted_commands".to_owned())],
                                )],
                            );
                        }
                    }
                }
            }
        }
        return ReduceOutcome {
            kind: "Duplicate".to_owned(),
            cursor: cursor.clone(),
            command: None,
            defects: Vec::new(),
            accepted_event_identity: Some(accepted_event_identity),
            event_payload_digest: Some(event_payload_digest),
            command_intent_identity: None,
            command_payload_digest: None,
        };
    }

    let satisfied = cursor_object
        .get("satisfied_edge_ids")
        .and_then(Value::as_array)
        .cloned()
        .unwrap_or_default();
    let matches = all_matches
        .iter()
        .filter(|edge| {
            let edge_id = edge.as_object().and_then(|edge| string_at(edge, "edge_id"));
            !satisfied.iter().any(|item| item.as_str() == edge_id)
        })
        .cloned()
        .collect::<Vec<_>>();
    if matches.len() > 1 {
        return reject_reduce(
            cursor,
            vec![StructuralDefect::new(
                "reduction",
                "MULTIPLE_EDGE_MATCH",
                vec![PathSegment::Field("edges".to_owned())],
            )],
        );
    }

    let mut next_cursor = cursor.clone();
    next_cursor
        .as_object_mut()
        .and_then(|object| object.get_mut("accepted_events"))
        .and_then(Value::as_array_mut)
        .expect("admitted cursor fixture has accepted_events")
        .push(json!({
            "accepted_event_identity": accepted_event_identity,
            "event_payload_digest": event_payload_digest,
        }));
    if matches.is_empty() {
        if let Err(defect) = normalize_cursor(&mut next_cursor) {
            return reject_reduce(cursor, vec![defect]);
        }
        return ReduceOutcome {
            kind: "Applied".to_owned(),
            cursor: next_cursor,
            command: None,
            defects: Vec::new(),
            accepted_event_identity: Some(accepted_event_identity),
            event_payload_digest: Some(event_payload_digest),
            command_intent_identity: None,
            command_payload_digest: None,
        };
    }
    let derived = derive_command_intent(compiled, event, &matches[0]);
    if !derived.admitted() || derived.command.is_none() {
        return reject_reduce(cursor, derived.defects);
    }
    let command_identity = derived
        .command_intent_identity
        .clone()
        .expect("admitted command has identity");
    let command_digest = derived
        .command_payload_digest
        .clone()
        .expect("admitted command has payload digest");
    let emitted = cursor_object
        .get("emitted_commands")
        .and_then(Value::as_array)
        .cloned()
        .unwrap_or_default();
    let stored = emitted.iter().find_map(|entry| {
        let entry = entry.as_object()?;
        (string_at(entry, "command_intent_identity") == Some(command_identity.as_str()))
            .then(|| string_at(entry, "command_payload_digest"))
            .flatten()
    });
    if let Some(stored) = stored {
        if stored != command_digest {
            return reject_reduce(
                cursor,
                vec![StructuralDefect::new(
                    "reduction",
                    "DIVERGENT_COMMAND_INTENT",
                    vec![PathSegment::Field("emitted_commands".to_owned())],
                )],
            );
        }
        let edge_id = matches[0]
            .as_object()
            .and_then(|edge| string_at(edge, "edge_id"))
            .unwrap_or_default()
            .to_owned();
        next_cursor
            .as_object_mut()
            .and_then(|object| object.get_mut("satisfied_edge_ids"))
            .and_then(Value::as_array_mut)
            .expect("admitted cursor fixture has satisfied edges")
            .push(Value::String(edge_id));
        if let Err(defect) = normalize_cursor(&mut next_cursor) {
            return reject_reduce(cursor, vec![defect]);
        }
        return ReduceOutcome {
            kind: "Applied".to_owned(),
            cursor: next_cursor,
            command: None,
            defects: Vec::new(),
            accepted_event_identity: derived.accepted_event_identity,
            event_payload_digest: derived.event_payload_digest,
            command_intent_identity: None,
            command_payload_digest: None,
        };
    }
    let edge_id = matches[0]
        .as_object()
        .and_then(|edge| string_at(edge, "edge_id"))
        .unwrap_or_default()
        .to_owned();
    let next_object = next_cursor.as_object_mut().expect("cursor object");
    next_object
        .get_mut("satisfied_edge_ids")
        .and_then(Value::as_array_mut)
        .expect("admitted cursor fixture has satisfied edges")
        .push(Value::String(edge_id));
    next_object
        .get_mut("emitted_commands")
        .and_then(Value::as_array_mut)
        .expect("admitted cursor fixture has emitted commands")
        .push(json!({
            "command_intent_identity": command_identity,
            "command_payload_digest": command_digest,
        }));
    if let Err(defect) = normalize_cursor(&mut next_cursor) {
        return reject_reduce(cursor, vec![defect]);
    }
    ReduceOutcome {
        kind: "Applied".to_owned(),
        cursor: next_cursor,
        command: derived.command,
        defects: Vec::new(),
        accepted_event_identity: derived.accepted_event_identity,
        event_payload_digest: derived.event_payload_digest,
        command_intent_identity: derived.command_intent_identity,
        command_payload_digest: derived.command_payload_digest,
    }
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct RetrySituation {
    pub kernel_outcome: Option<String>,
    pub adapter_outcome: Option<String>,
    pub submission_state: Option<String>,
    pub command_validity: Option<String>,
    pub attempt_budget: Option<String>,
    pub budget_open: Option<bool>,
    pub frozen_policy: Option<String>,
    pub lease_state: Option<String>,
    pub policy_allows: bool,
    pub adapter_capabilities: Vec<String>,
}

impl RetrySituation {
    pub fn from_vector_input(value: &Value) -> Self {
        let object = value.as_object();
        let string = |field: &str| {
            object
                .and_then(|object| object.get(field))
                .and_then(Value::as_str)
                .map(str::to_owned)
        };
        let boolean = |field: &str| {
            object
                .and_then(|object| object.get(field))
                .and_then(Value::as_bool)
        };
        Self {
            kernel_outcome: string("kernelOutcome"),
            adapter_outcome: string("adapterOutcome"),
            submission_state: string("submissionState"),
            command_validity: string("commandValidity"),
            attempt_budget: string("attemptBudget"),
            budget_open: boolean("budgetOpen"),
            frozen_policy: string("frozenPolicy"),
            lease_state: string("leaseState"),
            policy_allows: boolean("policyAllows").unwrap_or(false),
            adapter_capabilities: object
                .and_then(|object| object.get("adapterCapabilities"))
                .and_then(Value::as_array)
                .into_iter()
                .flatten()
                .filter_map(Value::as_str)
                .map(str::to_owned)
                .collect(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RetryDecision {
    pub treatment: String,
    pub reason: Option<String>,
    pub preserve_identity_and_payload: bool,
    pub semantic_disposition: Option<String>,
    pub next_policy_routes: Vec<String>,
}

fn retry(treatment: &str) -> RetryDecision {
    RetryDecision {
        treatment: treatment.to_owned(),
        reason: None,
        preserve_identity_and_payload: false,
        semantic_disposition: None,
        next_policy_routes: Vec::new(),
    }
}

/// Classify a known delivery situation. This function never retries, waits, or
/// delivers anything.
pub fn classify_retry(situation: &RetrySituation) -> RetryDecision {
    let has_capability = |capability: &str| {
        situation
            .adapter_capabilities
            .iter()
            .any(|item| item == capability)
    };
    if situation.attempt_budget.as_deref() == Some("exhausted") {
        let mut decision = retry(
            if situation.frozen_policy.as_deref() == Some("dead-letter") {
                "DeadLetter"
            } else {
                "Escalate"
            },
        );
        decision.reason = Some("ATTEMPT_BUDGET_EXHAUSTED".to_owned());
        return decision;
    }
    if situation.lease_state.as_deref() == Some("ownership-lost") {
        let mut decision = retry(if has_capability("owner-recovery") {
            "ReconcileThenDecide"
        } else {
            "Escalate"
        });
        decision.reason = Some("OWNERSHIP_LOST".to_owned());
        return decision;
    }
    if matches!(
        situation.kernel_outcome.as_deref(),
        Some("Rejected") | Some("DivergentDuplicate")
    ) {
        let mut decision = retry("DoNotRetry");
        decision.reason = situation.kernel_outcome.clone();
        return decision;
    }
    if situation.kernel_outcome.as_deref() == Some("Duplicate") {
        let mut decision = retry("DoNotRetry");
        decision.semantic_disposition = Some("acknowledge-convergence".to_owned());
        return decision;
    }
    if situation.adapter_outcome.as_deref() == Some("terminal-rejection")
        || situation.command_validity.as_deref() == Some("invalid")
    {
        let mut decision = retry("DoNotRetry");
        decision.reason = Some("TERMINAL_REJECTION_OR_INVALID_COMMAND".to_owned());
        decision.next_policy_routes = vec!["DeadLetter".to_owned(), "Escalate".to_owned()];
        return decision;
    }
    if situation.submission_state.as_deref() == Some("unknown") {
        if has_capability("status-query") || has_capability("journal-lookup") {
            let mut decision = retry("ReconcileThenDecide");
            decision.reason = Some("DELIVERY_UNKNOWN".to_owned());
            return decision;
        }
        if has_capability("end-to-end-idempotency-key")
            && situation.policy_allows
            && situation.budget_open == Some(true)
        {
            let mut decision = retry("RetrySame");
            decision.preserve_identity_and_payload = true;
            return decision;
        }
        let mut decision = retry("Escalate");
        decision.reason = Some("AMBIGUOUS_DELIVERY".to_owned());
        return decision;
    }
    if situation.submission_state.as_deref() == Some("definitely-not-submitted")
        && situation.budget_open == Some(true)
    {
        if situation.adapter_outcome.as_deref() == Some("rate-limited")
            && !has_capability("policy-backoff")
        {
            let mut decision = retry("Escalate");
            decision.reason = Some("BACKOFF_CAPABILITY_REQUIRED".to_owned());
            return decision;
        }
        let mut decision = retry("RetrySame");
        decision.preserve_identity_and_payload = true;
        return decision;
    }
    let mut decision = retry("DoNotRetry");
    decision.reason = Some("INSUFFICIENT_RETRY_EVIDENCE".to_owned());
    decision
}
