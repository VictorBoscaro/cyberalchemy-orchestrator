use base64::{engine::general_purpose::STANDARD, Engine};
use rwo_rust::{admit_canonical_decimal, admit_json, unicode_runtime_version, StructuralDefect};
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::fs;
use std::path::PathBuf;

fn manifest() -> Value {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(
        "../../docs/features/recursive-work-orchestrator/development/decision-gates/20260807T173437Z-rwo-language-contract-v2/vectors/CONFORMANCE-MANIFEST.json",
    );
    serde_json::from_slice(&fs::read(path).expect("frozen manifest is readable"))
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

fn codes(defects: &[StructuralDefect]) -> Vec<String> {
    defects.iter().map(|defect| defect.code.clone()).collect()
}

fn assert_case(raw: &[u8], expected: &Value, decimal: bool) {
    let result = if decimal {
        admit_canonical_decimal(raw)
    } else {
        admit_json(raw)
    };
    match expected["outcome"].as_str().expect("expected outcome") {
        "Admitted" => {
            assert!(
                result.admitted(),
                "unexpected defects: {:?}",
                result.defects
            );
            let payload = result.payload_bytes.expect("admitted payload");
            if let Some(encoded) = expected["payloadBase64"].as_str() {
                assert_eq!(payload, STANDARD.decode(encoded).expect("base64 payload"));
            }
            if let Some(size) = expected["payloadSizeBytes"].as_u64() {
                assert_eq!(payload.len() as u64, size);
            }
            if let Some(digest) = expected["payloadSha256"].as_str() {
                assert_eq!(format!("{:x}", Sha256::digest(&payload)), digest);
            }
        }
        "Rejected" => {
            assert!(
                !result.admitted(),
                "unexpected admitted value: {:?}",
                result.value
            );
            let expected_codes = expected["defectCodes"]
                .as_array()
                .expect("rejection codes")
                .iter()
                .map(|value| value.as_str().expect("defect code").to_owned())
                .collect::<Vec<_>>();
            assert_eq!(codes(&result.defects), expected_codes);
            assert!(result.value.is_none());
            assert!(result.payload_bytes.is_none());
        }
        outcome => panic!("unsupported expected outcome {outcome}"),
    }
}

#[test]
fn host_icu_is_the_pinned_unicode_15_1_runtime() {
    assert_eq!(
        unicode_runtime_version().expect("ICU runtime must be available"),
        [15, 1, 0, 0]
    );
}

#[test]
fn raw_admission_matches_all_frozen_adm_vectors() {
    let manifest = manifest();
    for index in 1..=13 {
        let id = format!("ADM-{index:03}");
        let input = vector(&manifest, &id);
        for case in input["cases"].as_array().expect("cases") {
            let raw = STANDARD
                .decode(case["rawUtf8JsonBase64"].as_str().expect("raw JSON base64"))
                .expect("raw JSON base64 decodes");
            assert_case(&raw, &case["expected"], false);
        }
    }
}

#[test]
fn canonical_decimal_matches_all_frozen_decimal_vectors() {
    let manifest = manifest();
    for index in 1..=2 {
        let id = format!("DEC-{index:03}");
        let input = vector(&manifest, &id);
        for case in input["cases"].as_array().expect("cases") {
            let raw = STANDARD
                .decode(case["rawUtf8JsonBase64"].as_str().expect("raw JSON base64"))
                .expect("raw JSON base64 decodes");
            assert_case(&raw, &case["expected"], true);
        }
    }
}

#[test]
fn ordinary_strings_are_not_treated_as_decimal_fields() {
    let manifest = manifest();
    for case in vector(&manifest, "DEC-003")["cases"]
        .as_array()
        .expect("cases")
    {
        let raw = STANDARD
            .decode(case["rawUtf8JsonBase64"].as_str().expect("raw JSON base64"))
            .expect("raw JSON base64 decodes");
        let result = admit_json(&raw);
        assert!(
            result.admitted(),
            "unexpected defects: {:?}",
            result.defects
        );
        assert_eq!(
            result.value,
            Some(Value::String(
                case["expected"]["value"].as_str().unwrap().to_owned()
            ))
        );
    }
}

#[test]
fn malformed_utf8_is_a_decode_failure() {
    let result = admit_json(b"\"\xff\"");
    assert_eq!(codes(&result.defects), vec!["INVALID_UTF8"]);
}
