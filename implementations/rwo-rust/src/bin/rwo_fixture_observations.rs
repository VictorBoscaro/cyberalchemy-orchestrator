//! Offline structural observations over the frozen RWO fixture corpus.
//!
//! This binary is a thin witness around the pure Rust kernel. It opens no
//! transport; it loads the checked-in fixture corpus and serializes raw-admission,
//! compiler, reducer, digest, defect-ordering, and retry facts.

use rwo_rust::{
    admit_canonical_decimal, admit_json, canonical_payload_bytes, classify_retry,
    compile_work_graph, derive_command_intent, order_defects, reduce_event, semantic_digest,
    unicode_runtime_version, AdmissionResult, PathSegment, RetrySituation, StructuralDefect,
};
use serde_json::{json, Map, Value};
use sha2::{Digest, Sha256};
use std::fs;
use std::io::{self, Write};
use std::path::PathBuf;

type AppResult<T> = Result<T, String>;

fn manifest_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(
        "../../docs/features/recursive-work-orchestrator/development/decision-gates/20260807T173437Z-rwo-language-contract-v2/vectors/CONFORMANCE-MANIFEST.json",
    )
}

fn fixture(manifest: &Value, name: &str) -> AppResult<Value> {
    manifest["fixtures"]
        .get(name)
        .cloned()
        .ok_or_else(|| format!("missing fixture {name}"))
}

fn vector<'a>(manifest: &'a Value, id: &str) -> AppResult<&'a Value> {
    manifest["vectors"]
        .as_array()
        .ok_or_else(|| "manifest vectors must be an array".to_owned())?
        .iter()
        .find(|item| item["vectorId"] == id)
        .ok_or_else(|| format!("missing vector {id}"))
}

fn required_str<'a>(value: &'a Value, label: &str) -> AppResult<&'a str> {
    value
        .as_str()
        .ok_or_else(|| format!("{label} must be a string"))
}

fn defect_codes(defects: &[StructuralDefect]) -> Value {
    Value::Array(
        defects
            .iter()
            .map(|defect| Value::String(defect.code.clone()))
            .collect(),
    )
}

fn optional_string(value: Option<String>) -> Value {
    value.map(Value::String).unwrap_or(Value::Null)
}

fn base64_encode(input: &[u8]) -> String {
    const ALPHABET: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut output = String::with_capacity(input.len().div_ceil(3) * 4);
    for chunk in input.chunks(3) {
        let first = chunk[0];
        let second = *chunk.get(1).unwrap_or(&0);
        let third = *chunk.get(2).unwrap_or(&0);
        output.push(ALPHABET[(first >> 2) as usize] as char);
        output.push(ALPHABET[(((first & 0x03) << 4) | (second >> 4)) as usize] as char);
        output.push(if chunk.len() > 1 {
            ALPHABET[(((second & 0x0f) << 2) | (third >> 6)) as usize] as char
        } else {
            '='
        });
        output.push(if chunk.len() > 2 {
            ALPHABET[(third & 0x3f) as usize] as char
        } else {
            '='
        });
    }
    output
}

fn base64_decode(input: &str) -> AppResult<Vec<u8>> {
    fn value(byte: u8) -> Option<u8> {
        match byte {
            b'A'..=b'Z' => Some(byte - b'A'),
            b'a'..=b'z' => Some(byte - b'a' + 26),
            b'0'..=b'9' => Some(byte - b'0' + 52),
            b'+' => Some(62),
            b'/' => Some(63),
            _ => None,
        }
    }

    let bytes = input.as_bytes();
    if bytes.len() % 4 != 0 {
        return Err("base64 input length is not a multiple of four".to_owned());
    }
    let mut output = Vec::with_capacity(bytes.len() / 4 * 3);
    for (index, chunk) in bytes.chunks_exact(4).enumerate() {
        let first = value(chunk[0]).ok_or_else(|| "invalid base64 first sextet".to_owned())?;
        let second = value(chunk[1]).ok_or_else(|| "invalid base64 second sextet".to_owned())?;
        let third = if chunk[2] == b'=' {
            None
        } else {
            Some(value(chunk[2]).ok_or_else(|| "invalid base64 third sextet".to_owned())?)
        };
        let fourth = if chunk[3] == b'=' {
            None
        } else {
            Some(value(chunk[3]).ok_or_else(|| "invalid base64 fourth sextet".to_owned())?)
        };
        if third.is_none() && fourth.is_some()
            || (third.is_none() || fourth.is_none()) && index + 1 != bytes.len() / 4
        {
            return Err("base64 padding is invalid".to_owned());
        }
        output.push((first << 2) | (second >> 4));
        if let Some(third) = third {
            output.push(((second & 0x0f) << 4) | (third >> 2));
            if let Some(fourth) = fourth {
                output.push(((third & 0x03) << 6) | fourth);
            }
        }
    }
    Ok(output)
}

fn admission_observation(result: AdmissionResult) -> Value {
    json!({
        "admitted": result.admitted(),
        "payload_base64": result.payload_bytes.as_deref().map(base64_encode),
        "defect_codes": defect_codes(&result.defects),
    })
}

fn raw_admission_observations(manifest: &Value) -> AppResult<Value> {
    let mut raw_json = Map::new();
    for index in 1..=13 {
        let id = format!("ADM-{index:03}");
        let cases = vector(manifest, &id)?["cases"]
            .as_array()
            .ok_or_else(|| format!("{id} cases must be an array"))?;
        let observations = cases
            .iter()
            .map(|case| {
                let raw =
                    base64_decode(required_str(&case["rawUtf8JsonBase64"], "raw JSON base64")?)?;
                Ok(admission_observation(admit_json(&raw)))
            })
            .collect::<AppResult<Vec<_>>>()?;
        raw_json.insert(id, Value::Array(observations));
    }

    let mut decimal = Map::new();
    for index in 1..=2 {
        let id = format!("DEC-{index:03}");
        let cases = vector(manifest, &id)?["cases"]
            .as_array()
            .ok_or_else(|| format!("{id} cases must be an array"))?;
        let observations = cases
            .iter()
            .map(|case| {
                let raw = base64_decode(required_str(
                    &case["rawUtf8JsonBase64"],
                    "decimal JSON base64",
                )?)?;
                Ok(admission_observation(admit_canonical_decimal(&raw)))
            })
            .collect::<AppResult<Vec<_>>>()?;
        decimal.insert(id, Value::Array(observations));
    }

    let ordinary_cases = vector(manifest, "DEC-003")?["cases"]
        .as_array()
        .ok_or_else(|| "DEC-003 cases must be an array")?;
    let ordinary_strings = ordinary_cases
        .iter()
        .map(|case| {
            let raw = base64_decode(required_str(
                &case["rawUtf8JsonBase64"],
                "ordinary JSON base64",
            )?)?;
            Ok(admission_observation(admit_json(&raw)))
        })
        .collect::<AppResult<Vec<_>>>()?;

    Ok(json!({
        "unicode_runtime_version": unicode_runtime_version()?,
        "raw_json": raw_json,
        "canonical_decimal": decimal,
        "ordinary_strings": ordinary_strings,
    }))
}

fn digest_observations(manifest: &Value) -> AppResult<Value> {
    let tuple = &manifest["digestTupleFixture"];
    let contract_id = required_str(&tuple["contract_id"], "digest contract id")?;
    let contract_version = required_str(&tuple["contract_version"], "digest contract version")?;
    let profile_id = required_str(&tuple["profile_id"], "digest profile id")?;
    let profile_version = required_str(&tuple["profile_version"], "digest profile version")?;
    let schema_id = required_str(&tuple["schema_id"], "digest schema id")?;
    let schema_version = required_str(&tuple["schema_version"], "digest schema version")?;
    let mut observations = Map::new();
    for id in ["DIG-001", "DIG-002"] {
        let input = &vector(manifest, id)?["typedInput"];
        let payload = base64_decode(required_str(
            &input["payloadBase64"],
            "digest payload base64",
        )?)?;
        observations.insert(
            id.to_owned(),
            Value::String(semantic_digest(
                contract_id,
                contract_version,
                profile_id,
                profile_version,
                schema_id,
                schema_version,
                required_str(&input["valueType"], "digest value type")?,
                &payload,
            )),
        );
    }
    observations.insert(
        "DIG-003".to_owned(),
        observations
            .get("DIG-001")
            .cloned()
            .ok_or_else(|| "DIG-001 observation missing".to_owned())?,
    );
    Ok(Value::Object(observations))
}

fn replace_at(value: &mut Value, path: &[Value], replacement: Value) -> AppResult<()> {
    let (segment, remaining) = path
        .split_first()
        .ok_or_else(|| "mutation path must be nonempty".to_owned())?;
    if let Some(name) = segment.as_str() {
        let object = value
            .as_object_mut()
            .ok_or_else(|| "object mutation target is not an object".to_owned())?;
        if remaining.is_empty() {
            object.insert(name.to_owned(), replacement);
            return Ok(());
        }
        let child = object
            .get_mut(name)
            .ok_or_else(|| format!("missing object mutation segment {name}"))?;
        return replace_at(child, remaining, replacement);
    }
    let index = segment
        .as_u64()
        .ok_or_else(|| "array mutation segment must be an index".to_owned())?
        as usize;
    let array = value
        .as_array_mut()
        .ok_or_else(|| "array mutation target is not an array".to_owned())?;
    if remaining.is_empty() {
        let target = array
            .get_mut(index)
            .ok_or_else(|| format!("array mutation index {index} is absent"))?;
        *target = replacement;
        return Ok(());
    }
    let child = array
        .get_mut(index)
        .ok_or_else(|| format!("array mutation index {index} is absent"))?;
    replace_at(child, remaining, replacement)
}

fn ordered_defect_codes(manifest: &Value) -> AppResult<Value> {
    let definition = vector(manifest, "DEF-001")?;
    let discoveries = definition["typedInput"]["discoveryOrder"]
        .as_array()
        .ok_or_else(|| "DEF-001 discoveryOrder must be an array".to_owned())?;
    let mut defects = Vec::with_capacity(discoveries.len());
    for item in discoveries {
        let path = item["path"]
            .as_array()
            .ok_or_else(|| "DEF-001 path must be an array".to_owned())?
            .iter()
            .map(
                |segment| match required_str(&segment["kind"], "path kind")? {
                    "field" => Ok(PathSegment::Field(
                        required_str(&segment["name"], "field path name")?.to_owned(),
                    )),
                    "index" => Ok(PathSegment::Index(
                        segment["index"]
                            .as_u64()
                            .ok_or_else(|| "index path value must be an integer".to_owned())?
                            as usize,
                    )),
                    kind => Err(format!("unsupported path kind {kind}")),
                },
            )
            .collect::<AppResult<Vec<_>>>()?;
        defects.push(StructuralDefect::with_detail(
            required_str(&item["phase"], "defect phase")?,
            required_str(&item["code"], "defect code")?,
            path,
            required_str(&item["detail_digest"], "defect detail digest")?,
        ));
    }
    let ordered = order_defects(defects).map_err(|error| format!("order defects: {error}"))?;
    Ok(defect_codes(&ordered))
}

fn retry_observations(manifest: &Value) -> AppResult<Value> {
    let mut observations = Map::new();
    for index in 1..=11 {
        let id = format!("RTY-{index:03}");
        let retry_vector = vector(manifest, &id)?;
        let decision = classify_retry(&RetrySituation::from_vector_input(
            &retry_vector["typedInput"],
        ));
        observations.insert(id, Value::String(decision.treatment));
    }

    let mut semantic_outcomes = Map::new();
    for case in vector(manifest, "RTY-012")?["cases"]
        .as_array()
        .ok_or_else(|| "RTY-012 cases must be an array".to_owned())?
    {
        let outcome = match required_str(
            &case["typedInput"]["semanticVectorRef"],
            "RTY-012 semantic vector reference",
        )? {
            "RED-002" => "Duplicate",
            "RED-003" => "DivergentDuplicate",
            reference => return Err(format!("unsupported RTY-012 reference {reference}")),
        };
        let decision = classify_retry(&RetrySituation {
            kernel_outcome: Some(outcome.to_owned()),
            ..RetrySituation::default()
        });
        semantic_outcomes.insert(outcome.to_owned(), Value::String(decision.treatment));
    }
    observations.insert("RTY-012".to_owned(), Value::Object(semantic_outcomes));
    Ok(Value::Object(observations))
}

fn run() -> AppResult<()> {
    let manifest_bytes =
        fs::read(manifest_path()).map_err(|error| format!("read manifest: {error}"))?;
    let manifest: Value = serde_json::from_slice(&manifest_bytes)
        .map_err(|error| format!("parse manifest: {error}"))?;
    let manifest_sha256 = format!("{:x}", Sha256::digest(&manifest_bytes));

    let compile = compile_work_graph(&fixture(&manifest, "explicitComposition")?);
    let compile_kind = compile.kind.clone();
    let graph = compile
        .compiled
        .as_ref()
        .ok_or_else(|| "fixture composition did not compile".to_owned())?;

    let initial_cursor = fixture(&manifest, "initialCursor")?;
    let matching_event = fixture(&manifest, "matchingEvent")?;
    let applied = reduce_event(graph, &initial_cursor, &matching_event);
    let derived = derive_command_intent(graph, &matching_event, &graph.graph["edges"][0]);
    if !derived.admitted()
        || derived.command != applied.command
        || derived.command_intent_identity != applied.command_intent_identity
        || derived.command_payload_digest != applied.command_payload_digest
    {
        return Err("derived command observation does not agree with RED-001 reduction".to_owned());
    }

    let duplicate = reduce_event(graph, &fixture(&manifest, "nextCursor")?, &matching_event);
    let red_three = vector(&manifest, "RED-003")?;
    let mutation = &red_three["typedInput"]["mutation"]["replace"];
    let mut divergent_event = matching_event.clone();
    replace_at(
        &mut divergent_event,
        mutation["path"]
            .as_array()
            .ok_or_else(|| "RED-003 mutation path must be an array".to_owned())?,
        mutation["value"].clone(),
    )?;
    let divergent = reduce_event(graph, &fixture(&manifest, "nextCursor")?, &divergent_event);

    let output = json!({
        "schema_version": "rwo.fixture-observations/v1",
        "manifest_sha256": manifest_sha256,
        "compile": {
            "kind": compile_kind,
            "graph_identity": graph.graph_identity,
            "canonical_payload_base64": base64_encode(&graph.canonical_bytes),
        },
        "reduce": {
            "applied": {
                "kind": applied.kind,
                "cursor": applied.cursor,
                "command": applied.command,
                "accepted_event_identity": optional_string(applied.accepted_event_identity),
                "event_payload_digest": optional_string(applied.event_payload_digest),
                "command_intent_identity": optional_string(applied.command_intent_identity),
                "command_payload_digest": optional_string(applied.command_payload_digest),
            },
            "duplicate": {
                "kind": duplicate.kind,
                "cursor": duplicate.cursor,
            },
            "divergent": {
                "kind": divergent.kind,
                "defect_codes": defect_codes(&divergent.defects),
                "cursor": divergent.cursor,
            },
        },
        "admission": raw_admission_observations(&manifest)?,
        "digests": digest_observations(&manifest)?,
        "defects": {"ordered_codes": ordered_defect_codes(&manifest)?},
        "retry": retry_observations(&manifest)?,
    });
    let bytes = canonical_payload_bytes(&output)
        .map_err(|error| format!("canonicalize observation output: {error}"))?;
    io::stdout()
        .write_all(&bytes)
        .map_err(|error| format!("write observation output: {error}"))?;
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("rwo_fixture_observations: {error}");
        std::process::exit(1);
    }
}
