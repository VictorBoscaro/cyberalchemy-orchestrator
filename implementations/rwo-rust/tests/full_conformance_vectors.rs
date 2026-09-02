use base64::{engine::general_purpose::STANDARD, Engine};
use rwo_rust::{
    admit_json, admit_version_tuple, canonical_payload_bytes, normalize_semantic_elements,
    semantic_digest, VersionRegistry, VersionTuple,
};
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::fs;
use std::path::{Path, PathBuf};

fn contract_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(
        "../../docs/features/recursive-work-orchestrator/development/decision-gates/20260807T173437Z-rwo-language-contract-v2",
    )
}

fn manifest_path() -> PathBuf {
    contract_root().join("vectors/CONFORMANCE-MANIFEST.json")
}

fn review_path() -> PathBuf {
    contract_root().join("vectors/CONFORMANCE-MANIFEST-REVIEW.json")
}

fn manifest() -> Value {
    serde_json::from_slice(&fs::read(manifest_path()).expect("frozen manifest is readable"))
        .expect("frozen manifest is JSON")
}

fn vector<'a>(manifest: &'a Value, id: &str) -> &'a Value {
    manifest["vectors"]
        .as_array()
        .expect("vectors array")
        .iter()
        .find(|item| item["vectorId"] == id)
        .unwrap_or_else(|| panic!("missing vector {id}"))
}

fn hash(path: &Path) -> String {
    format!("{:x}", Sha256::digest(fs::read(path).expect("read source")))
}

fn version_tuple(input: &Value) -> VersionTuple {
    VersionTuple {
        contract_id: input["contract_id"].as_str().unwrap().to_owned(),
        contract_version: input["contract_version"].as_str().unwrap().to_owned(),
        profile_id: input["profile_id"].as_str().unwrap().to_owned(),
        profile_version: input["profile_version"].as_str().unwrap().to_owned(),
        schema_id: input["schema_id"].as_str().unwrap().to_owned(),
        schema_version: input["schema_version"].as_str().unwrap().to_owned(),
        value_type: input["value_type"].as_str().unwrap().to_owned(),
    }
}

fn registry() -> VersionRegistry {
    let document: Value = serde_json::from_slice(
        &fs::read(contract_root().join("schemas/registry.json")).expect("registry is readable"),
    )
    .expect("registry is JSON");
    VersionRegistry::from_document(&document).expect("registry shape is valid")
}

#[test]
fn normalization_vectors_match_the_frozen_contract() {
    let manifest = manifest();
    let tie_break = vector(&manifest, "NRM-001");
    let paths = tie_break["typedInput"]["declaration"]["primaryKeyPaths"]
        .as_array()
        .unwrap()
        .iter()
        .map(|value| value.as_str().unwrap().to_owned())
        .collect::<Vec<_>>();
    let normalized = normalize_semantic_elements(
        tie_break["typedInput"]["elements"]
            .as_array()
            .unwrap()
            .to_vec(),
        &paths,
    )
    .expect("tie-break collection is normalizable");
    assert_eq!(
        normalized,
        tie_break["expected"]["elements"]
            .as_array()
            .unwrap()
            .to_vec()
    );

    let duplicate = vector(&manifest, "NRM-002");
    let duplicate_paths = duplicate["typedInput"]["declaration"]["primaryKeyPaths"]
        .as_array()
        .unwrap()
        .iter()
        .map(|value| value.as_str().unwrap().to_owned())
        .collect::<Vec<_>>();
    let error = normalize_semantic_elements(
        duplicate["typedInput"]["elements"]
            .as_array()
            .unwrap()
            .to_vec(),
        &duplicate_paths,
    )
    .expect_err("duplicate semantic identity must be rejected");
    assert_eq!(error.code, "DUPLICATE_SEMANTIC_IDENTITY");

    let ordered = vector(&manifest, "NRM-003");
    let payloads = ordered["typedInput"]["orderedCases"]
        .as_array()
        .unwrap()
        .iter()
        .map(|value| STANDARD.encode(canonical_payload_bytes(value).unwrap()))
        .collect::<Vec<_>>();
    assert_eq!(
        payloads,
        ordered["expected"]["payloadBase64Cases"]
            .as_array()
            .unwrap()
            .iter()
            .map(|value| value.as_str().unwrap().to_owned())
            .collect::<Vec<_>>()
    );
    assert_ne!(payloads[0], payloads[1]);
}

#[test]
fn typed_digest_vectors_match_the_frozen_contract() {
    let manifest = manifest();
    let tuple = &manifest["digestTupleFixture"];
    let mut observed = Vec::new();
    for id in ["DIG-001", "DIG-002"] {
        let vector = vector(&manifest, id);
        let input = &vector["typedInput"];
        let digest = semantic_digest(
            tuple["contract_id"].as_str().unwrap(),
            tuple["contract_version"].as_str().unwrap(),
            tuple["profile_id"].as_str().unwrap(),
            tuple["profile_version"].as_str().unwrap(),
            tuple["schema_id"].as_str().unwrap(),
            tuple["schema_version"].as_str().unwrap(),
            input["valueType"].as_str().unwrap(),
            &STANDARD
                .decode(input["payloadBase64"].as_str().unwrap())
                .unwrap(),
        );
        assert_eq!(digest, vector["expected"]["semanticDigest"]);
        observed.push(digest);
    }
    assert_ne!(observed[0], observed[1]);
    assert_eq!(
        observed[0],
        vector(&manifest, "DIG-003")["expected"]["semanticDigest"]
    );
}

#[test]
fn version_tuple_vectors_match_the_frozen_registry_surface() {
    let manifest = manifest();
    let registry = registry();
    let accepted = version_tuple(&vector(&manifest, "VER-002")["typedInput"]);
    assert!(admit_version_tuple(&accepted, &registry).is_empty());
    for case in vector(&manifest, "VER-001")["cases"].as_array().unwrap() {
        let mut changed = accepted.clone();
        let input = &case["typedInput"];
        if let Some(value) = input["contract_version"].as_str() {
            changed.contract_version = value.to_owned();
        }
        if let Some(value) = input["schema_id"].as_str() {
            changed.schema_id = value.to_owned();
        }
        if let Some(value) = input["profile_version"].as_str() {
            changed.profile_version = value.to_owned();
        }
        if let Some(value) = input["value_type"].as_str() {
            changed.value_type = value.to_owned();
        }
        let defects = admit_version_tuple(&changed, &registry);
        assert_eq!(
            defects
                .iter()
                .map(|defect| defect.code.as_str())
                .collect::<Vec<_>>(),
            vec!["VERSION_TUPLE_UNSUPPORTED"]
        );
    }
}

#[test]
fn unicode_delta_repeatability_and_fixture_governance_remain_pinned() {
    for scalar in [0x2ffc, 0x31ef, 0x2ebf0, 0x2ee5d] {
        let raw = serde_json::to_vec(&Value::String(char::from_u32(scalar).unwrap().to_string()))
            .unwrap();
        assert!(admit_json(&raw).admitted(), "scalar U+{scalar:04X}");
    }
    let unassigned =
        serde_json::to_vec(&Value::String(char::from_u32(0x2ee5e).unwrap().to_string())).unwrap();
    assert_eq!(
        admit_json(&unassigned)
            .defects
            .iter()
            .map(|defect| defect.code.as_str())
            .collect::<Vec<_>>(),
        vec!["UNICODE_UNASSIGNED"]
    );
    let raw = b" \n {\"z\":[2,1],\"a\":\"value\"}\t ";
    let first = admit_json(raw);
    let second = admit_json(raw);
    assert_eq!(first, second);
    assert_eq!(
        first.payload_bytes.as_deref(),
        Some(b"{\"a\":\"value\",\"z\":[2,1]}".as_slice())
    );
    assert_eq!(raw, b" \n {\"z\":[2,1],\"a\":\"value\"}\t ");
    assert_eq!(
        admit_json(b"0\xc2\xa0")
            .defects
            .iter()
            .map(|defect| defect.code.as_str())
            .collect::<Vec<_>>(),
        vec!["TRAILING_TOKEN"]
    );

    let manifest_path = manifest_path();
    let review_path = review_path();
    let manifest_bytes = fs::read(&manifest_path).unwrap();
    let review_bytes = fs::read(&review_path).unwrap();
    let review: Value = serde_json::from_slice(&review_bytes).unwrap();
    let fixture_manifest: Value = serde_json::from_slice(&manifest_bytes).unwrap();
    let before_manifest_hash = hash(&manifest_path);
    let before_review_hash = hash(&review_path);
    assert_eq!(hash(&manifest_path), review["manifest"]["sha256"]);
    assert_eq!(
        manifest_bytes.len(),
        review["manifest"]["sizeBytes"].as_u64().unwrap() as usize
    );
    assert_ne!(
        Sha256::digest([manifest_bytes.as_slice(), b" "].concat()),
        Sha256::digest(&manifest_bytes)
    );
    assert_ne!(
        Sha256::digest([review_bytes.as_slice(), b" "].concat()),
        Sha256::digest(&review_bytes)
    );
    let mut changed: Value = serde_json::from_slice(&manifest_bytes).unwrap();
    changed["vectors"]
        .as_array_mut()
        .unwrap()
        .iter_mut()
        .find(|item| item["vectorId"] == "DIG-001")
        .unwrap()["expected"]["semanticDigest"] =
        Value::String(format!("sha256:{}", "0".repeat(64)));
    assert_ne!(
        format!(
            "{:x}",
            Sha256::digest(serde_json::to_vec(&changed).unwrap())
        ),
        review["manifest"]["sha256"]
    );
    let fixture_one = vector(&fixture_manifest, "FIX-001");
    let fixture_two = vector(&fixture_manifest, "FIX-002");
    let fixture_three = vector(&fixture_manifest, "FIX-003");
    let fixture_four = vector(&fixture_manifest, "FIX-004");
    let fixture_five = vector(&fixture_manifest, "FIX-005");
    let fixture_six = vector(&fixture_manifest, "FIX-006");
    assert_eq!(fixture_one["expected"]["writes"], Value::Array(Vec::new()));
    assert!(fixture_two["expected"]["manifestDigestChanges"]
        .as_bool()
        .unwrap());
    assert!(fixture_three["expected"]["reviewDigestChanges"]
        .as_bool()
        .unwrap());
    assert_eq!(fixture_four["expected"]["independentReview"], "fail");
    let producer = fixture_manifest["producer"]["identity"].as_str().unwrap();
    let reviewer = review["reviewer"]["identity"].as_str().unwrap();
    assert_ne!(producer, reviewer);
    let admits_reviewer = |producer: &str, reviewer: &str| producer != reviewer;
    assert!(!admits_reviewer(producer, producer));
    assert_eq!(fixture_five["expected"]["admission"], "block");
    assert_eq!(
        fixture_manifest["status"],
        fixture_six["expected"]["status"]
    );
    assert!(review["ownerDecision"]["reference"].is_null());
    assert!(!fixture_six["expected"]["canonicalApplyAllowed"]
        .as_bool()
        .unwrap());
    assert_eq!(hash(&manifest_path), before_manifest_hash);
    assert_eq!(hash(&review_path), before_review_hash);
}
