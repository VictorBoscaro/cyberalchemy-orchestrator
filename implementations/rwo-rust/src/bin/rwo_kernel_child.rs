//! Private local-process adapter for the RWO Rust semantic kernel.
//!
//! This binary is intentionally not a network service or a public wire
//! contract. It speaks one bounded, length-prefixed local protocol over stdin
//! and stdout so a Go host can call the existing Rust semantic implementation
//! without recreating admission, compilation, or reduction semantics.

use base64::{engine::general_purpose::STANDARD, Engine};
use rwo_rust::{
    admit_json, admit_version_tuple, canonical_payload_bytes, compile_work_graph, initial_cursor,
    reduce_event, CompiledGraph, PathSegment, StructuralDefect, VersionRegistry, VersionTuple,
};
use serde_json::{json, Map, Value};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::io::{self, Read, Write};
use std::path::PathBuf;

const PROTOCOL_VERSION: &str = "rwo-local-kernel/1";

struct Config {
    registry_path: PathBuf,
    max_frame_bytes: usize,
}

struct KernelChild {
    registry: VersionRegistry,
    graphs: HashMap<String, CompiledGraph>,
    next_handle: u64,
}

impl KernelChild {
    fn new(registry: VersionRegistry) -> Self {
        Self {
            registry,
            graphs: HashMap::new(),
            next_handle: 1,
        }
    }

    fn handle(&mut self, request: &Value) -> Value {
        let request_id = request
            .get("request_id")
            .and_then(Value::as_str)
            .map(str::to_owned);
        let operation = request
            .get("operation")
            .and_then(Value::as_str)
            .map(str::to_owned);
        let object = match request.as_object() {
            Some(object) => object,
            None => {
                return protocol_error(
                    request_id,
                    operation,
                    "MALFORMED_REQUEST",
                    "control envelope must be an object",
                )
            }
        };
        if object.get("protocol_version").and_then(Value::as_str) != Some(PROTOCOL_VERSION) {
            return protocol_error(
                request_id,
                operation,
                "UNSUPPORTED_PROTOCOL",
                "unsupported protocol_version",
            );
        }
        let Some(request_id) = request_id else {
            return protocol_error(
                None,
                operation,
                "MALFORMED_REQUEST",
                "request_id must be a non-empty string",
            );
        };
        if request_id.is_empty() {
            return protocol_error(
                Some(request_id),
                operation,
                "MALFORMED_REQUEST",
                "request_id must be a non-empty string",
            );
        }
        let Some(operation) = operation else {
            return protocol_error(
                Some(request_id),
                None,
                "MALFORMED_REQUEST",
                "operation must be a string",
            );
        };
        match operation.as_str() {
            "CompileV1" => self.compile(&request_id, &operation, object),
            "ReduceV1" => self.reduce(&request_id, &operation, object),
            _ => protocol_error(
                Some(request_id),
                Some(operation),
                "UNSUPPORTED_OPERATION",
                "unsupported operation",
            ),
        }
    }

    fn compile(
        &mut self,
        request_id: &str,
        operation: &str,
        request: &Map<String, Value>,
    ) -> Value {
        let tuple = match request_tuple(request) {
            Ok(tuple) => tuple,
            Err(error) => {
                return protocol_error(
                    Some(request_id.to_owned()),
                    Some(operation.to_owned()),
                    "MALFORMED_REQUEST",
                    &error,
                )
            }
        };
        let raw = match required_base64(request, "raw_composition_base64") {
            Ok(raw) => raw,
            Err(error) => {
                return protocol_error(
                    Some(request_id.to_owned()),
                    Some(operation.to_owned()),
                    "MALFORMED_REQUEST",
                    &error,
                )
            }
        };
        let mut defects = admit_version_tuple(&tuple, &self.registry);
        if tuple.schema_id != "ExplicitComposition" || tuple.value_type != "ExplicitComposition" {
            defects.push(tuple_defect());
        }
        let admitted = admit_json(&raw);
        if !admitted.admitted() {
            return semantic_response(
                request_id,
                operation,
                "Rejected",
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                &admitted.defects,
            );
        }
        let composition = admitted.value.expect("admitted JSON has a value");
        if !tuple_matches_value(&composition, &tuple) {
            defects.push(tuple_defect());
        }
        if !defects.is_empty() {
            return semantic_response(
                request_id, operation, "Rejected", None, None, None, None, None, None, None, None,
                None, &defects,
            );
        }
        let outcome = compile_work_graph(&composition);
        let Some(compiled) = outcome.compiled else {
            return semantic_response(
                request_id,
                operation,
                outcome.kind.as_str(),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                &outcome.defects,
            );
        };
        let handle = format!("graph-{}", self.next_handle);
        self.next_handle += 1;
        let identity = compiled.graph_identity.clone();
        self.graphs.insert(handle.clone(), compiled);
        semantic_response(
            request_id,
            operation,
            "Compiled",
            Some(handle),
            Some(identity),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            &[],
        )
    }

    fn reduce(&mut self, request_id: &str, operation: &str, request: &Map<String, Value>) -> Value {
        let graph_handle = match required_string(request, "graph_handle") {
            Ok(value) => value,
            Err(error) => {
                return protocol_error(
                    Some(request_id.to_owned()),
                    Some(operation.to_owned()),
                    "MALFORMED_REQUEST",
                    &error,
                )
            }
        };
        let Some(compiled) = self.graphs.get(&graph_handle).cloned() else {
            return protocol_error(
                Some(request_id.to_owned()),
                Some(operation.to_owned()),
                "UNKNOWN_GRAPH_HANDLE",
                "graph_handle is not known by this child process",
            );
        };
        let stream_id_hint = match required_string(request, "stream_id_hint") {
            Ok(value) if !value.is_empty() => value,
            Ok(_) => {
                return protocol_error(
                    Some(request_id.to_owned()),
                    Some(operation.to_owned()),
                    "MALFORMED_REQUEST",
                    "stream_id_hint must be a non-empty string",
                )
            }
            Err(error) => {
                return protocol_error(
                    Some(request_id.to_owned()),
                    Some(operation.to_owned()),
                    "MALFORMED_REQUEST",
                    &error,
                )
            }
        };
        let tuple = match request_tuple(request) {
            Ok(tuple) => tuple,
            Err(error) => {
                return protocol_error(
                    Some(request_id.to_owned()),
                    Some(operation.to_owned()),
                    "MALFORMED_REQUEST",
                    &error,
                )
            }
        };
        let raw_event = match required_base64(request, "raw_accepted_event_base64") {
            Ok(raw) => raw,
            Err(error) => {
                return protocol_error(
                    Some(request_id.to_owned()),
                    Some(operation.to_owned()),
                    "MALFORMED_REQUEST",
                    &error,
                )
            }
        };
        let original_cursor = match nullable_base64(request, "original_cursor_base64") {
            Ok(value) => value,
            Err(error) => {
                return protocol_error(
                    Some(request_id.to_owned()),
                    Some(operation.to_owned()),
                    "MALFORMED_REQUEST",
                    &error,
                )
            }
        };
        let admitted_event = admit_json(&raw_event);
        if !admitted_event.admitted() {
            return semantic_response(
                request_id,
                operation,
                "Rejected",
                Some(graph_handle.to_owned()),
                Some(compiled.graph_identity.clone()),
                None,
                original_cursor.as_deref(),
                None,
                None,
                None,
                None,
                None,
                &admitted_event.defects,
            );
        }
        let event = admitted_event.value.expect("admitted JSON has a value");
        let mut tuple_defects = admit_version_tuple(&tuple, &self.registry);
        if tuple.schema_id != "AcceptedEventView" || tuple.value_type != "AcceptedEventView" {
            tuple_defects.push(tuple_defect());
        }
        if !tuple_matches_value(&event, &tuple) {
            tuple_defects.push(tuple_defect());
        }
        if !tuple_defects.is_empty() {
            return semantic_response(
                request_id,
                operation,
                "Rejected",
                Some(graph_handle.to_owned()),
                Some(compiled.graph_identity.clone()),
                event_stream_id(&event),
                original_cursor.as_deref(),
                None,
                None,
                None,
                None,
                None,
                &tuple_defects,
            );
        }
        let Some(validated_stream_id) = event_stream_id(&event) else {
            let defect = StructuralDefect::new(
                "schema",
                "REQUIRED_FIELD_MISSING",
                vec![PathSegment::Field("stream_id".to_owned())],
            );
            return semantic_response(
                request_id,
                operation,
                "Rejected",
                Some(graph_handle.to_owned()),
                Some(compiled.graph_identity.clone()),
                None,
                original_cursor.as_deref(),
                None,
                None,
                None,
                None,
                None,
                &[defect],
            );
        };
        if validated_stream_id != stream_id_hint {
            let defect = StructuralDefect::new(
                "reduction",
                "STREAM_ID_MISMATCH",
                vec![PathSegment::Field("stream_id".to_owned())],
            );
            return semantic_response(
                request_id,
                operation,
                "Rejected",
                Some(graph_handle.to_owned()),
                Some(compiled.graph_identity.clone()),
                Some(validated_stream_id),
                original_cursor.as_deref(),
                None,
                None,
                None,
                None,
                None,
                &[defect],
            );
        }
        let (cursor, original_cursor_bytes) = match original_cursor {
            Some(bytes) => {
                let admitted_cursor = admit_json(&bytes);
                if !admitted_cursor.admitted() {
                    return semantic_response(
                        request_id,
                        operation,
                        "Rejected",
                        Some(graph_handle.to_owned()),
                        Some(compiled.graph_identity.clone()),
                        Some(validated_stream_id),
                        Some(&bytes),
                        None,
                        None,
                        None,
                        None,
                        None,
                        &admitted_cursor.defects,
                    );
                }
                let cursor = admitted_cursor.value.expect("admitted cursor has a value");
                if !cursor_tuple_matches(&cursor) {
                    let defect = tuple_defect();
                    return semantic_response(
                        request_id,
                        operation,
                        "Rejected",
                        Some(graph_handle.to_owned()),
                        Some(compiled.graph_identity.clone()),
                        Some(validated_stream_id),
                        Some(&bytes),
                        None,
                        None,
                        None,
                        None,
                        None,
                        &[defect],
                    );
                }
                (cursor, Some(bytes))
            }
            None => match initial_cursor(&compiled, validated_stream_id) {
                Ok(initial) => (initial.cursor, None),
                Err(error) => {
                    return protocol_error(
                        Some(request_id.to_owned()),
                        Some(operation.to_owned()),
                        "KERNEL_FAILURE",
                        &error,
                    )
                }
            },
        };
        let outcome = reduce_event(&compiled, &cursor, &event);
        let cursor_bytes = if outcome.kind == "Applied" {
            match canonical_payload_bytes(&outcome.cursor) {
                Ok(bytes) => Some(bytes),
                Err(error) => {
                    return protocol_error(
                        Some(request_id.to_owned()),
                        Some(operation.to_owned()),
                        "KERNEL_FAILURE",
                        &error,
                    )
                }
            }
        } else {
            original_cursor_bytes
        };
        let command_bytes = match outcome.command.as_ref() {
            Some(command) => match canonical_payload_bytes(command) {
                Ok(bytes) => Some(bytes),
                Err(error) => {
                    return protocol_error(
                        Some(request_id.to_owned()),
                        Some(operation.to_owned()),
                        "KERNEL_FAILURE",
                        &error,
                    )
                }
            },
            None => None,
        };
        semantic_response(
            request_id,
            operation,
            outcome.kind.as_str(),
            Some(graph_handle.to_owned()),
            Some(compiled.graph_identity.clone()),
            Some(validated_stream_id),
            cursor_bytes.as_deref(),
            command_bytes.as_deref(),
            outcome.accepted_event_identity,
            outcome.event_payload_digest,
            outcome.command_intent_identity,
            outcome.command_payload_digest,
            &outcome.defects,
        )
    }
}

fn parse_config() -> Result<Config, String> {
    let mut registry_path = None;
    let mut max_frame_bytes = None;
    let mut arguments = env::args().skip(1);
    while let Some(argument) = arguments.next() {
        match argument.as_str() {
            "--registry" => registry_path = arguments.next().map(PathBuf::from),
            "--max-frame-bytes" => {
                let value = arguments
                    .next()
                    .ok_or_else(|| "--max-frame-bytes requires a value".to_owned())?;
                let parsed = value
                    .parse::<usize>()
                    .map_err(|_| "--max-frame-bytes must be an integer".to_owned())?;
                if parsed == 0 || parsed > u32::MAX as usize {
                    return Err("--max-frame-bytes must be between 1 and u32::MAX".to_owned());
                }
                max_frame_bytes = Some(parsed);
            }
            "--help" | "-h" => {
                return Err(
                    "usage: rwo_kernel_child --registry <registry.json> --max-frame-bytes <positive-u32>"
                        .to_owned(),
                )
            }
            other => return Err(format!("unknown argument {other}")),
        }
    }
    Ok(Config {
        registry_path: registry_path.ok_or_else(|| "--registry is required".to_owned())?,
        max_frame_bytes: max_frame_bytes
            .ok_or_else(|| "--max-frame-bytes is required".to_owned())?,
    })
}

fn required_string(request: &Map<String, Value>, field: &str) -> Result<String, String> {
    request
        .get(field)
        .and_then(Value::as_str)
        .filter(|value| !value.is_empty())
        .map(str::to_owned)
        .ok_or_else(|| format!("{field} must be a non-empty string"))
}

fn request_tuple(request: &Map<String, Value>) -> Result<VersionTuple, String> {
    let tuple = request
        .get("tuple")
        .and_then(Value::as_object)
        .ok_or_else(|| "tuple must be an object".to_owned())?;
    let allowed = [
        "contract_id",
        "contract_version",
        "profile_id",
        "profile_version",
        "schema_id",
        "schema_version",
        "value_type",
    ];
    if tuple.len() != allowed.len() || tuple.keys().any(|field| !allowed.contains(&field.as_str()))
    {
        return Err("tuple must contain exactly the registered tuple fields".to_owned());
    }
    let string = |field| {
        tuple
            .get(field)
            .and_then(Value::as_str)
            .filter(|value| !value.is_empty())
            .map(str::to_owned)
            .ok_or_else(|| format!("tuple.{field} must be a non-empty string"))
    };
    Ok(VersionTuple {
        contract_id: string("contract_id")?,
        contract_version: string("contract_version")?,
        profile_id: string("profile_id")?,
        profile_version: string("profile_version")?,
        schema_id: string("schema_id")?,
        schema_version: string("schema_version")?,
        value_type: string("value_type")?,
    })
}

fn required_base64(request: &Map<String, Value>, field: &str) -> Result<Vec<u8>, String> {
    let value = required_string(request, field)?;
    STANDARD
        .decode(value)
        .map_err(|_| format!("{field} must be standard base64"))
}

fn nullable_base64(request: &Map<String, Value>, field: &str) -> Result<Option<Vec<u8>>, String> {
    match request.get(field) {
        Some(Value::Null) => Ok(None),
        Some(Value::String(value)) => STANDARD
            .decode(value)
            .map(Some)
            .map_err(|_| format!("{field} must be standard base64 or null")),
        _ => Err(format!("{field} must be standard base64 or null")),
    }
}

fn tuple_matches_value(value: &Value, tuple: &VersionTuple) -> bool {
    let Some(object) = value.as_object() else {
        return false;
    };
    [
        ("contract_id", tuple.contract_id.as_str()),
        ("contract_version", tuple.contract_version.as_str()),
        ("profile_id", tuple.profile_id.as_str()),
        ("profile_version", tuple.profile_version.as_str()),
        ("schema_id", tuple.schema_id.as_str()),
        ("schema_version", tuple.schema_version.as_str()),
    ]
    .into_iter()
    .all(|(field, expected)| object.get(field).and_then(Value::as_str) == Some(expected))
}

fn cursor_tuple_matches(cursor: &Value) -> bool {
    let Some(object) = cursor.as_object() else {
        return false;
    };
    [
        ("contract_id", rwo_rust::CONTRACT_ID),
        ("contract_version", rwo_rust::CONTRACT_VERSION),
        ("profile_id", rwo_rust::PROFILE_ID),
        ("profile_version", rwo_rust::PROFILE_VERSION),
        ("schema_id", "OrchestrationCursor"),
        ("schema_version", "1.0.0"),
        (
            "reducer_semantics_version",
            rwo_rust::REDUCER_SEMANTICS_VERSION,
        ),
    ]
    .into_iter()
    .all(|(field, expected)| object.get(field).and_then(Value::as_str) == Some(expected))
}

fn event_stream_id(event: &Value) -> Option<&str> {
    event
        .as_object()
        .and_then(|object| object.get("stream_id"))
        .and_then(Value::as_str)
        .filter(|value| !value.is_empty())
}

fn tuple_defect() -> StructuralDefect {
    StructuralDefect::new("admission", "VERSION_TUPLE_UNSUPPORTED", Vec::new())
}

fn defect_value(defect: &StructuralDefect) -> Value {
    let path = defect
        .path
        .iter()
        .map(|segment| match segment {
            PathSegment::Field(name) => json!({"kind": "field", "name": name}),
            PathSegment::Index(index) => json!({"kind": "index", "index": index}),
        })
        .collect::<Vec<_>>();
    json!({
        "phase": defect.phase,
        "code": defect.code,
        "path": path,
        "detail_digest": defect.detail_digest,
    })
}

#[allow(clippy::too_many_arguments)]
fn semantic_response(
    request_id: &str,
    operation: &str,
    outcome: &str,
    graph_handle: Option<String>,
    graph_identity: Option<String>,
    validated_stream_id: Option<&str>,
    cursor: Option<&[u8]>,
    command: Option<&[u8]>,
    accepted_event_identity: Option<String>,
    event_payload_digest: Option<String>,
    command_intent_identity: Option<String>,
    command_payload_digest: Option<String>,
    defects: &[StructuralDefect],
) -> Value {
    json!({
        "protocol_version": PROTOCOL_VERSION,
        "request_id": request_id,
        "operation": operation,
        "response_kind": "semantic",
        "outcome": outcome,
        "graph_handle": graph_handle,
        "graph_identity": graph_identity,
        "validated_stream_id": validated_stream_id,
        "cursor_base64": cursor.map(|bytes| STANDARD.encode(bytes)),
        "command_base64": command.map(|bytes| STANDARD.encode(bytes)),
        "accepted_event_identity": accepted_event_identity,
        "event_payload_digest": event_payload_digest,
        "command_intent_identity": command_intent_identity,
        "command_payload_digest": command_payload_digest,
        "defects": defects.iter().map(defect_value).collect::<Vec<_>>(),
    })
}

fn protocol_error(
    request_id: Option<String>,
    operation: Option<String>,
    code: &str,
    message: &str,
) -> Value {
    json!({
        "protocol_version": PROTOCOL_VERSION,
        "request_id": request_id,
        "operation": operation,
        "response_kind": "protocol_error",
        "error": {"code": code, "message": message},
    })
}

fn read_frame(reader: &mut impl Read, maximum: usize) -> Result<Option<Vec<u8>>, String> {
    let mut header = [0u8; 4];
    let first = reader
        .read(&mut header)
        .map_err(|error| format!("read frame header: {error}"))?;
    if first == 0 {
        return Ok(None);
    }
    reader
        .read_exact(&mut header[first..])
        .map_err(|error| format!("read incomplete frame header: {error}"))?;
    let length = u32::from_be_bytes(header) as usize;
    if length == 0 || length > maximum {
        return Err(format!("frame length {length} is outside 1..={maximum}"));
    }
    let mut frame = vec![0u8; length];
    reader
        .read_exact(&mut frame)
        .map_err(|error| format!("read frame body: {error}"))?;
    Ok(Some(frame))
}

fn write_frame(writer: &mut impl Write, value: &Value, maximum: usize) -> Result<(), String> {
    let payload =
        serde_json::to_vec(value).map_err(|error| format!("serialize response: {error}"))?;
    if payload.is_empty() || payload.len() > maximum {
        return Err(format!(
            "response length {} is outside 1..={maximum}",
            payload.len()
        ));
    }
    writer
        .write_all(&(payload.len() as u32).to_be_bytes())
        .and_then(|_| writer.write_all(&payload))
        .and_then(|_| writer.flush())
        .map_err(|error| format!("write response: {error}"))
}

fn serve(child: &mut KernelChild, maximum: usize) -> Result<(), String> {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut reader = stdin.lock();
    let mut writer = stdout.lock();
    loop {
        let frame = match read_frame(&mut reader, maximum) {
            Ok(None) => return Ok(()),
            Ok(Some(frame)) => frame,
            Err(error) => {
                write_frame(
                    &mut writer,
                    &protocol_error(None, None, "INVALID_FRAME", &error),
                    maximum,
                )?;
                return Err(error);
            }
        };
        let response = match serde_json::from_slice::<Value>(&frame) {
            Ok(request) => child.handle(&request),
            Err(_) => protocol_error(
                None,
                None,
                "MALFORMED_REQUEST",
                "control envelope is not valid JSON",
            ),
        };
        write_frame(&mut writer, &response, maximum)?;
    }
}

fn run() -> Result<(), String> {
    let config = parse_config()?;
    let registry_bytes = fs::read(&config.registry_path)
        .map_err(|error| format!("read registry {}: {error}", config.registry_path.display()))?;
    let registry_document: Value = serde_json::from_slice(&registry_bytes)
        .map_err(|error| format!("parse registry: {error}"))?;
    let registry = VersionRegistry::from_document(&registry_document)
        .map_err(|error| format!("build version registry: {error}"))?;
    serve(&mut KernelChild::new(registry), config.max_frame_bytes)
}

fn main() {
    if let Err(error) = run() {
        eprintln!("rwo_kernel_child: {error}");
        std::process::exit(1);
    }
}
