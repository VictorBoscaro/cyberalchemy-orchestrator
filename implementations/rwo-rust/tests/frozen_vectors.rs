use base64::{engine::general_purpose::STANDARD, Engine};
use rwo_rust::{
    classify_retry, compile_work_graph, derive_command_intent, order_defects, reduce_event,
    CompiledGraph, PathSegment, RetrySituation, StructuralDefect,
};
use serde_json::Value;
use std::fs;
use std::path::PathBuf;

fn manifest() -> Value {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(
        "../../docs/features/recursive-work-orchestrator/development/decision-gates/20260807T173437Z-rwo-language-contract-v2/vectors/CONFORMANCE-MANIFEST.json",
    );
    serde_json::from_slice(&fs::read(path).expect("frozen manifest is readable"))
        .expect("frozen manifest is JSON")
}

fn vector(manifest: &Value, id: &str) -> Value {
    manifest["vectors"]
        .as_array()
        .expect("vectors array")
        .iter()
        .find(|item| item["vectorId"] == id)
        .cloned()
        .unwrap_or_else(|| panic!("missing vector {id}"))
}

fn fixture(manifest: &Value, name: &str) -> Value {
    manifest["fixtures"][name].clone()
}

fn codes(defects: &[StructuralDefect]) -> Vec<String> {
    defects.iter().map(|defect| defect.code.clone()).collect()
}

fn replace_at(value: &mut Value, path: &[Value], replacement: Value) {
    let segment = path.first().expect("nonempty mutation path");
    if path.len() == 1 {
        if let Some(name) = segment.as_str() {
            value
                .as_object_mut()
                .expect("object mutation target")
                .insert(name.to_owned(), replacement);
        } else {
            let index = segment.as_u64().expect("array index") as usize;
            value.as_array_mut().expect("array mutation target")[index] = replacement;
        }
        return;
    }
    let child = if let Some(name) = segment.as_str() {
        value
            .as_object_mut()
            .expect("object mutation target")
            .get_mut(name)
            .expect("object path exists")
    } else {
        let index = segment.as_u64().expect("array index") as usize;
        &mut value.as_array_mut().expect("array mutation target")[index]
    };
    replace_at(child, &path[1..], replacement);
}

fn compiled(manifest: &Value) -> CompiledGraph {
    let outcome = compile_work_graph(&fixture(manifest, "explicitComposition"));
    assert_eq!(outcome.kind, "Compiled", "{:?}", outcome.defects);
    outcome.compiled.expect("compiled fixture graph")
}

#[test]
fn frozen_corpus_has_the_declared_semantic_denominator() {
    let manifest = manifest();
    let prefixes = [
        "ADM", "DEC", "NRM", "DIG", "VER", "CMP", "RED", "CMD", "DEF", "RTY", "FIX",
    ];
    let applicable = manifest["vectors"]
        .as_array()
        .expect("vectors")
        .iter()
        .filter(|item| {
            item["vectorId"]
                .as_str()
                .and_then(|id| id.split_once('-').map(|pair| pair.0))
                .is_some_and(|prefix| prefixes.contains(&prefix))
        })
        .count();
    assert_eq!(applicable, 54);
}

#[test]
fn compile_vectors_prove_frozen_structural_graph_behavior() {
    let manifest = manifest();
    let first = compile_work_graph(&fixture(&manifest, "explicitComposition"));
    let second = compile_work_graph(&fixture(&manifest, "explicitComposition"));
    let expected = vector(&manifest, "CMP-001")["expected"].clone();
    let graph = first.compiled.as_ref().expect("compiled graph");
    assert_eq!(first.kind, expected["outcome"].as_str().unwrap());
    assert_eq!(graph.graph, fixture(&manifest, "compiledWorkGraph"));
    assert_eq!(
        graph.canonical_bytes,
        second.compiled.unwrap().canonical_bytes
    );
    assert_eq!(
        graph.graph_identity,
        expected["graphIdentity"].as_str().unwrap()
    );
    let expected_bytes = STANDARD
        .decode(
            fixture(&manifest, "compiledGraphPayload")["base64"]
                .as_str()
                .unwrap(),
        )
        .expect("base64 graph payload");
    assert_eq!(graph.canonical_bytes, expected_bytes);

    let mut unknown = fixture(&manifest, "explicitComposition");
    unknown["unknown"] = Value::Bool(true);
    let unknown = compile_work_graph(&unknown);
    assert_eq!(unknown.kind, "Rejected");
    assert_eq!(
        codes(&unknown.defects),
        vector(&manifest, "CMP-002")["expected"]["defectCodes"]
            .as_array()
            .unwrap()
            .iter()
            .map(|item| item.as_str().unwrap().to_owned())
            .collect::<Vec<_>>()
    );

    let mut missing = fixture(&manifest, "explicitComposition");
    missing["edges"][0]["target_node_id"] = Value::String("missing".to_owned());
    let missing = compile_work_graph(&missing);
    assert_eq!(missing.kind, "Rejected");
    assert_eq!(codes(&missing.defects), vec!["MISSING_ENDPOINT"]);
}

#[test]
fn reduce_and_command_vectors_preserve_identity_and_cursor_behavior() {
    let manifest = manifest();
    let compiled = compiled(&manifest);
    let initial = fixture(&manifest, "initialCursor");
    let event = fixture(&manifest, "matchingEvent");
    let applied = reduce_event(&compiled, &initial, &event);
    let expected = vector(&manifest, "RED-001")["expected"].clone();
    assert_eq!(applied.kind, "Applied");
    assert_eq!(applied.cursor, fixture(&manifest, "nextCursor"));
    assert_eq!(applied.command, Some(fixture(&manifest, "expectedCommand")));
    assert_eq!(
        applied.accepted_event_identity.as_deref(),
        expected["acceptedEventIdentity"].as_str()
    );
    assert_eq!(
        applied.event_payload_digest.as_deref(),
        expected["eventPayloadDigest"].as_str()
    );
    assert_eq!(
        applied.command_intent_identity.as_deref(),
        expected["commandIntentIdentity"].as_str()
    );
    assert_eq!(
        applied.command_payload_digest.as_deref(),
        expected["commandPayloadDigest"].as_str()
    );
    assert_eq!(initial, fixture(&manifest, "initialCursor"));

    let next = fixture(&manifest, "nextCursor");
    let duplicate = reduce_event(&compiled, &next, &event);
    assert_eq!(duplicate.kind, "Duplicate");
    assert_eq!(duplicate.cursor, next);
    assert!(duplicate.command.is_none());

    let mut divergent_event = event.clone();
    divergent_event["payload"]["job_id"] = Value::String("job-2".to_owned());
    let divergent = reduce_event(
        &compiled,
        &fixture(&manifest, "nextCursor"),
        &divergent_event,
    );
    assert_eq!(divergent.kind, "DivergentDuplicate");
    assert_eq!(codes(&divergent.defects), vec!["DIVERGENT_DUPLICATE"]);
    assert_eq!(divergent.cursor, fixture(&manifest, "nextCursor"));

    let no_match = vector(&manifest, "RED-004")["typedInput"]["event"].clone();
    let no_match = reduce_event(&compiled, &fixture(&manifest, "initialCursor"), &no_match);
    assert_eq!(no_match.kind, "Applied");
    assert_eq!(
        no_match.cursor["accepted_events"].as_array().unwrap().len(),
        1
    );
    assert_eq!(
        no_match.cursor["satisfied_edge_ids"],
        Value::Array(Vec::new())
    );
    assert!(no_match.command.is_none());

    for case in vector(&manifest, "RED-005")["cases"].as_array().unwrap() {
        let mut cursor = fixture(&manifest, "initialCursor");
        let replacement = &case["typedInput"]["mutation"]["replace"];
        replace_at(
            &mut cursor,
            replacement["path"].as_array().unwrap(),
            replacement["value"].clone(),
        );
        let result = reduce_event(&compiled, &cursor, &event);
        assert_eq!(result.kind, "Rejected");
        assert_eq!(
            codes(&result.defects),
            case["expected"]["defectCodes"]
                .as_array()
                .unwrap()
                .iter()
                .map(|item| item.as_str().unwrap().to_owned())
                .collect::<Vec<_>>()
        );
        assert_eq!(result.cursor, cursor);
    }

    let mut malformed_graph = fixture(&manifest, "compiledWorkGraph");
    malformed_graph["edges"]
        .as_array_mut()
        .unwrap()
        .push(vector(&manifest, "RED-006")["typedInput"]["graphMutation"]["appendEdge"].clone());
    let adversarial = CompiledGraph::bind(
        malformed_graph,
        Some(
            fixture(&manifest, "graphIdentity")
                .as_str()
                .unwrap()
                .to_owned(),
        ),
    )
    .expect("adversarial graph binding");
    let ambiguous = reduce_event(&adversarial, &fixture(&manifest, "initialCursor"), &event);
    assert_eq!(ambiguous.kind, "Rejected");
    assert_eq!(codes(&ambiguous.defects), vec!["MULTIPLE_EDGE_MATCH"]);

    let derived = derive_command_intent(&compiled, &event, &compiled.graph["edges"][0]);
    let command_expected = vector(&manifest, "CMD-001")["expected"].clone();
    assert!(derived.admitted(), "{:?}", derived.defects);
    assert_eq!(derived.command, Some(fixture(&manifest, "expectedCommand")));
    assert_eq!(
        derived.command_intent_identity.as_deref(),
        command_expected["commandIntentIdentity"].as_str()
    );
    assert_eq!(
        derived.command_payload_digest.as_deref(),
        command_expected["commandPayloadDigest"].as_str()
    );

    let mut corrupt_cursor = fixture(&manifest, "nextCursor");
    corrupt_cursor["emitted_commands"][0]["command_payload_digest"] =
        Value::String(format!("sha256:{}", "0".repeat(64)));
    let conflict = reduce_event(&compiled, &corrupt_cursor, &event);
    assert_eq!(conflict.kind, "Rejected");
    assert_eq!(codes(&conflict.defects), vec!["DIVERGENT_COMMAND_INTENT"]);
    assert_eq!(conflict.cursor, corrupt_cursor);
}

#[test]
fn defect_and_retry_vectors_remain_pure_and_ordered() {
    let manifest = manifest();
    let definition = vector(&manifest, "DEF-001");
    let defects = definition["typedInput"]["discoveryOrder"]
        .as_array()
        .unwrap()
        .iter()
        .map(|item| {
            let path = item["path"]
                .as_array()
                .unwrap()
                .iter()
                .map(|segment| match segment["kind"].as_str().unwrap() {
                    "field" => PathSegment::Field(segment["name"].as_str().unwrap().to_owned()),
                    "index" => PathSegment::Index(segment["index"].as_u64().unwrap() as usize),
                    kind => panic!("unknown path segment {kind}"),
                })
                .collect();
            StructuralDefect::with_detail(
                item["phase"].as_str().unwrap(),
                item["code"].as_str().unwrap(),
                path,
                item["detail_digest"].as_str().unwrap(),
            )
        })
        .collect::<Vec<_>>();
    let ordered = order_defects(defects.clone()).expect("unique defects order");
    assert_eq!(
        codes(&ordered),
        definition["expected"]["orderedCodes"]
            .as_array()
            .unwrap()
            .iter()
            .map(|item| item.as_str().unwrap().to_owned())
            .collect::<Vec<_>>()
    );
    assert!(order_defects(vec![defects[0].clone(), defects[0].clone()]).is_err());

    for index in 1..=11 {
        let retry_vector = vector(&manifest, &format!("RTY-{index:03}"));
        let decision = classify_retry(&RetrySituation::from_vector_input(
            &retry_vector["typedInput"],
        ));
        let expected = &retry_vector["expected"];
        assert_eq!(decision.treatment, expected["treatment"].as_str().unwrap());
        if let Some(identity) = expected["identityAndPayloadUnchanged"].as_bool() {
            assert_eq!(decision.preserve_identity_and_payload, identity);
        }
        if let Some(disposition) = expected["semanticDisposition"].as_str() {
            assert_eq!(decision.semantic_disposition.as_deref(), Some(disposition));
        }
        if let Some(routes) = expected["nextPolicyRoute"].as_array() {
            assert_eq!(
                decision.next_policy_routes,
                routes
                    .iter()
                    .map(|item| item.as_str().unwrap().to_owned())
                    .collect::<Vec<_>>()
            );
        }
    }
    for case in vector(&manifest, "RTY-012")["cases"].as_array().unwrap() {
        let outcome = match case["typedInput"]["semanticVectorRef"].as_str().unwrap() {
            "RED-002" => "Duplicate",
            "RED-003" => "DivergentDuplicate",
            other => panic!("unexpected semantic vector {other}"),
        };
        let decision = classify_retry(&RetrySituation {
            kernel_outcome: Some(outcome.to_owned()),
            ..RetrySituation::default()
        });
        assert_eq!(
            decision.treatment,
            case["expected"]["treatment"].as_str().unwrap()
        );
    }
}
