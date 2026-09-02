use base64::{engine::general_purpose::STANDARD, Engine};
use rwo_rust::{canonical_payload_bytes, compile_work_graph, initial_cursor, VersionTuple};
use serde_json::{json, Value};
use std::fs;
use std::io::{Read, Write};
use std::path::PathBuf;
use std::process::{Child, ChildStdin, ChildStdout, Command, Stdio};

const PROTOCOL_VERSION: &str = "rwo-local-kernel/1";

fn contract_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(
        "../../docs/features/recursive-work-orchestrator/development/decision-gates/20260807T173437Z-rwo-language-contract-v2",
    )
}

fn manifest() -> Value {
    serde_json::from_slice(
        &fs::read(contract_root().join("vectors/CONFORMANCE-MANIFEST.json"))
            .expect("frozen manifest is readable"),
    )
    .expect("frozen manifest is JSON")
}

fn fixture(manifest: &Value, name: &str) -> Value {
    manifest["fixtures"][name].clone()
}

fn tuple(value: &Value, value_type: &str) -> Value {
    json!({
        "contract_id": value["contract_id"],
        "contract_version": value["contract_version"],
        "profile_id": value["profile_id"],
        "profile_version": value["profile_version"],
        "schema_id": value["schema_id"],
        "schema_version": value["schema_version"],
        "value_type": value_type,
    })
}

fn encoded(value: &Value) -> String {
    STANDARD.encode(canonical_payload_bytes(value).expect("fixture canonicalizes"))
}

struct ChildClient {
    child: Child,
    stdin: ChildStdin,
    stdout: ChildStdout,
}

impl ChildClient {
    fn start() -> Self {
        let mut child = Command::new(env!("CARGO_BIN_EXE_rwo_kernel_child"))
            .args([
                "--registry",
                contract_root()
                    .join("schemas/registry.json")
                    .to_str()
                    .unwrap(),
                "--max-frame-bytes",
                "1048576",
            ])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .expect("kernel child starts");
        Self {
            stdin: child.stdin.take().expect("child stdin"),
            stdout: child.stdout.take().expect("child stdout"),
            child,
        }
    }

    fn send(&mut self, request: Value) -> Value {
        let bytes = serde_json::to_vec(&request).expect("request serializes");
        self.send_bytes(&bytes)
    }

    fn send_bytes(&mut self, bytes: &[u8]) -> Value {
        self.stdin
            .write_all(&(bytes.len() as u32).to_be_bytes())
            .and_then(|_| self.stdin.write_all(bytes))
            .and_then(|_| self.stdin.flush())
            .expect("request frame writes");
        let mut header = [0u8; 4];
        self.stdout
            .read_exact(&mut header)
            .expect("response header");
        let length = u32::from_be_bytes(header) as usize;
        assert!(length > 0 && length <= 1_048_576);
        let mut payload = vec![0u8; length];
        self.stdout
            .read_exact(&mut payload)
            .expect("response payload");
        serde_json::from_slice(&payload).expect("response JSON")
    }

    fn finish(mut self) {
        drop(self.stdin);
        let status = self.child.wait().expect("child exits");
        assert!(
            status.success(),
            "child stderr is intentionally diagnostic only"
        );
    }
}

fn compile(client: &mut ChildClient, manifest: &Value) -> Value {
    let composition = fixture(manifest, "explicitComposition");
    let response = client.send(json!({
        "protocol_version": PROTOCOL_VERSION,
        "request_id": "compile-1",
        "operation": "CompileV1",
        "tuple": tuple(&composition, "ExplicitComposition"),
        "raw_composition_base64": encoded(&composition),
    }));
    assert_eq!(response["response_kind"], "semantic");
    assert_eq!(response["outcome"], "Compiled");
    assert!(response["graph_handle"].as_str().is_some());
    response
}

#[test]
fn child_compiles_and_reduces_frozen_bytes_without_host_semantics() {
    let manifest = manifest();
    let composition = fixture(&manifest, "explicitComposition");
    let compiled = compile_work_graph(&composition)
        .compiled
        .expect("fixture graph compiles in the semantic kernel");
    let initial = initial_cursor(&compiled, "stream-1").expect("initial cursor builds");
    assert_eq!(
        initial.canonical_bytes,
        canonical_payload_bytes(&fixture(&manifest, "initialCursor")).unwrap()
    );

    let mut client = ChildClient::start();
    let compilation = compile(&mut client, &manifest);
    let graph_handle = compilation["graph_handle"].as_str().unwrap();
    let event = fixture(&manifest, "matchingEvent");
    let first = client.send(json!({
        "protocol_version": PROTOCOL_VERSION,
        "request_id": "reduce-1",
        "operation": "ReduceV1",
        "tuple": tuple(&event, "AcceptedEventView"),
        "graph_handle": graph_handle,
        "stream_id_hint": "stream-1",
        "raw_accepted_event_base64": encoded(&event),
        "original_cursor_base64": Value::Null,
    }));
    assert_eq!(first["response_kind"], "semantic");
    assert_eq!(first["outcome"], "Applied");
    assert_eq!(first["validated_stream_id"], "stream-1");
    assert_eq!(
        STANDARD
            .decode(first["cursor_base64"].as_str().unwrap())
            .unwrap(),
        canonical_payload_bytes(&fixture(&manifest, "nextCursor")).unwrap()
    );
    assert_eq!(
        STANDARD
            .decode(first["command_base64"].as_str().unwrap())
            .unwrap(),
        canonical_payload_bytes(&fixture(&manifest, "expectedCommand")).unwrap()
    );

    let duplicate = client.send(json!({
        "protocol_version": PROTOCOL_VERSION,
        "request_id": "reduce-duplicate",
        "operation": "ReduceV1",
        "tuple": tuple(&event, "AcceptedEventView"),
        "graph_handle": graph_handle,
        "stream_id_hint": "stream-1",
        "raw_accepted_event_base64": encoded(&event),
        "original_cursor_base64": first["cursor_base64"],
    }));
    assert_eq!(duplicate["outcome"], "Duplicate");
    assert_eq!(duplicate["cursor_base64"], first["cursor_base64"]);
    assert_eq!(duplicate["command_base64"], Value::Null);
    client.finish();
}

#[test]
fn child_rejects_stream_mismatch_and_fails_closed_on_control_errors() {
    let manifest = manifest();
    let mut client = ChildClient::start();
    let compilation = compile(&mut client, &manifest);
    let graph_handle = compilation["graph_handle"].as_str().unwrap();
    let event = fixture(&manifest, "matchingEvent");

    let mismatch = client.send(json!({
        "protocol_version": PROTOCOL_VERSION,
        "request_id": "stream-mismatch",
        "operation": "ReduceV1",
        "tuple": tuple(&event, "AcceptedEventView"),
        "graph_handle": graph_handle,
        "stream_id_hint": "other-stream",
        "raw_accepted_event_base64": encoded(&event),
        "original_cursor_base64": Value::Null,
    }));
    assert_eq!(mismatch["response_kind"], "semantic");
    assert_eq!(mismatch["outcome"], "Rejected");
    assert_eq!(mismatch["defects"][0]["code"], "STREAM_ID_MISMATCH");
    assert_eq!(mismatch["command_base64"], Value::Null);

    let unknown = client.send(json!({
        "protocol_version": PROTOCOL_VERSION,
        "request_id": "unknown-handle",
        "operation": "ReduceV1",
        "tuple": tuple(&event, "AcceptedEventView"),
        "graph_handle": "graph-never-compiled",
        "stream_id_hint": "stream-1",
        "raw_accepted_event_base64": encoded(&event),
        "original_cursor_base64": Value::Null,
    }));
    assert_eq!(unknown["response_kind"], "protocol_error");
    assert_eq!(unknown["error"]["code"], "UNKNOWN_GRAPH_HANDLE");

    let malformed = client.send_bytes(b"not JSON");
    assert_eq!(malformed["response_kind"], "protocol_error");
    assert_eq!(malformed["error"]["code"], "MALFORMED_REQUEST");
    client.finish();

    let mut zero_frame = ChildClient::start();
    zero_frame
        .stdin
        .write_all(&0u32.to_be_bytes())
        .and_then(|_| zero_frame.stdin.flush())
        .expect("zero frame writes");
    let mut header = [0u8; 4];
    zero_frame
        .stdout
        .read_exact(&mut header)
        .expect("invalid-frame response header");
    let mut payload = vec![0u8; u32::from_be_bytes(header) as usize];
    zero_frame
        .stdout
        .read_exact(&mut payload)
        .expect("invalid-frame response payload");
    let response: Value = serde_json::from_slice(&payload).expect("invalid-frame JSON");
    assert_eq!(response["response_kind"], "protocol_error");
    assert_eq!(response["error"]["code"], "INVALID_FRAME");
    drop(zero_frame.stdin);
    assert!(!zero_frame.child.wait().expect("child exits").success());
}

#[test]
fn protocol_tuple_is_explicit_and_registered() {
    let value = fixture(&manifest(), "matchingEvent");
    let tuple = VersionTuple {
        contract_id: value["contract_id"].as_str().unwrap().to_owned(),
        contract_version: value["contract_version"].as_str().unwrap().to_owned(),
        profile_id: value["profile_id"].as_str().unwrap().to_owned(),
        profile_version: value["profile_version"].as_str().unwrap().to_owned(),
        schema_id: value["schema_id"].as_str().unwrap().to_owned(),
        schema_version: value["schema_version"].as_str().unwrap().to_owned(),
        value_type: "AcceptedEventView".to_owned(),
    };
    assert_eq!(tuple.value_type, "AcceptedEventView");
}
