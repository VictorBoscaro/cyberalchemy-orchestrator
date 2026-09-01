//! Raw JSON admission for the pinned RWO Unicode and numeric profile.
//!
//! This module is intentionally the only `unsafe` boundary in the Rust
//! prototype. It binds the locally installed ICU 74 ABI, whose Unicode data is
//! checked at runtime to be exactly 15.1.0 before it is used. Every caller
//! otherwise receives ordinary `serde_json::Value` data or typed defects.

#![allow(unsafe_code)]

use crate::{canonical_payload_bytes, ordered, PathSegment, StructuralDefect};
use serde_json::{Map, Number, Value};
use std::collections::{HashMap, HashSet};

const SAFE_INTEGER_MINIMUM: i64 = -9_007_199_254_740_991;
const SAFE_INTEGER_MAXIMUM: i64 = 9_007_199_254_740_991;
const PINNED_UNICODE_VERSION: [u8; 4] = [15, 1, 0, 0];

/// The result of decoding and admitting raw JSON under the RWO profile.
#[derive(Debug, Clone, PartialEq)]
pub struct AdmissionResult {
    pub value: Option<Value>,
    pub payload_bytes: Option<Vec<u8>>,
    pub defects: Vec<StructuralDefect>,
}

/// Exact version tuple carried by every RWO semantic value.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VersionTuple {
    pub contract_id: String,
    pub contract_version: String,
    pub profile_id: String,
    pub profile_version: String,
    pub schema_id: String,
    pub schema_version: String,
    pub value_type: String,
}

/// Parsed closed registry used to admit exact version tuples.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VersionRegistry {
    pub contract_id: String,
    pub contract_version: String,
    pub profile_id: String,
    pub profile_version: String,
    schemas: HashMap<(String, String), HashSet<String>>,
}

impl VersionRegistry {
    /// Parse the checked-in registry shape without granting it any authority.
    pub fn from_document(document: &Value) -> Result<Self, String> {
        let contract = document["contract"]
            .as_object()
            .ok_or_else(|| "registry contract must be an object".to_owned())?;
        let profile = document["profile"]
            .as_object()
            .ok_or_else(|| "registry profile must be an object".to_owned())?;
        let text = |object: &Map<String, Value>, field: &str| {
            object
                .get(field)
                .and_then(Value::as_str)
                .map(str::to_owned)
                .ok_or_else(|| format!("registry field {field} must be a string"))
        };
        let mut schemas = HashMap::new();
        for schema in document["schemas"]
            .as_array()
            .ok_or_else(|| "registry schemas must be an array".to_owned())?
        {
            let schema = schema
                .as_object()
                .ok_or_else(|| "registry schema entry must be an object".to_owned())?;
            let schema_id = text(schema, "schemaId")?;
            let schema_version = text(schema, "schemaVersion")?;
            let value_types = schema["valueTypes"]
                .as_array()
                .ok_or_else(|| "registry valueTypes must be an array".to_owned())?
                .iter()
                .map(|value| {
                    value
                        .as_str()
                        .map(str::to_owned)
                        .ok_or_else(|| "registry value type must be a string".to_owned())
                })
                .collect::<Result<HashSet<_>, _>>()?;
            schemas.insert((schema_id, schema_version), value_types);
        }
        Ok(Self {
            contract_id: text(contract, "id")?,
            contract_version: text(contract, "version")?,
            profile_id: text(profile, "id")?,
            profile_version: text(profile, "version")?,
            schemas,
        })
    }

    fn admits(&self, value: &VersionTuple) -> bool {
        value.contract_id == self.contract_id
            && value.contract_version == self.contract_version
            && value.profile_id == self.profile_id
            && value.profile_version == self.profile_version
            && self
                .schemas
                .get(&(value.schema_id.clone(), value.schema_version.clone()))
                .is_some_and(|types| types.contains(&value.value_type))
    }
}

impl AdmissionResult {
    pub fn admitted(&self) -> bool {
        self.defects.is_empty()
    }

    fn rejected(defects: Vec<StructuralDefect>) -> Self {
        Self {
            value: None,
            payload_bytes: None,
            defects: ordered(defects),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
enum RawString {
    Text(String),
    InvalidScalar,
}

#[derive(Debug, Clone, PartialEq)]
enum RawValue {
    Null,
    Bool(bool),
    Number(String),
    String(RawString),
    Array(Vec<RawValue>),
    Object(Vec<(RawString, RawValue)>),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum ParseFailure {
    InvalidJson,
    TrailingToken,
    DuplicateObjectName,
}

struct Parser<'a> {
    bytes: &'a [u8],
    position: usize,
}

impl<'a> Parser<'a> {
    fn new(bytes: &'a [u8]) -> Self {
        Self { bytes, position: 0 }
    }

    fn parse(mut self) -> Result<RawValue, ParseFailure> {
        self.skip_whitespace();
        let value = self.parse_value()?;
        self.skip_whitespace();
        if self.position == self.bytes.len() {
            Ok(value)
        } else {
            Err(ParseFailure::TrailingToken)
        }
    }

    fn skip_whitespace(&mut self) {
        while matches!(self.peek(), Some(b' ' | b'\t' | b'\r' | b'\n')) {
            self.position += 1;
        }
    }

    fn peek(&self) -> Option<u8> {
        self.bytes.get(self.position).copied()
    }

    fn consume(&mut self, expected: u8) -> Result<(), ParseFailure> {
        if self.peek() == Some(expected) {
            self.position += 1;
            Ok(())
        } else {
            Err(ParseFailure::InvalidJson)
        }
    }

    fn consume_literal(&mut self, literal: &[u8]) -> Result<(), ParseFailure> {
        if self.bytes.get(self.position..self.position + literal.len()) == Some(literal) {
            self.position += literal.len();
            Ok(())
        } else {
            Err(ParseFailure::InvalidJson)
        }
    }

    fn parse_value(&mut self) -> Result<RawValue, ParseFailure> {
        match self.peek() {
            Some(b'n') => {
                self.consume_literal(b"null")?;
                Ok(RawValue::Null)
            }
            Some(b't') => {
                self.consume_literal(b"true")?;
                Ok(RawValue::Bool(true))
            }
            Some(b'f') => {
                self.consume_literal(b"false")?;
                Ok(RawValue::Bool(false))
            }
            Some(b'"') => self.parse_string().map(RawValue::String),
            Some(b'[') => self.parse_array(),
            Some(b'{') => self.parse_object(),
            Some(b'-') if self.starts_with(b"-Infinity") => {
                self.consume_literal(b"-Infinity")?;
                Ok(RawValue::Number("-Infinity".to_owned()))
            }
            Some(b'N') if self.starts_with(b"NaN") => {
                self.consume_literal(b"NaN")?;
                Ok(RawValue::Number("NaN".to_owned()))
            }
            Some(b'I') if self.starts_with(b"Infinity") => {
                self.consume_literal(b"Infinity")?;
                Ok(RawValue::Number("Infinity".to_owned()))
            }
            Some(b'-' | b'0'..=b'9') => self.parse_number(),
            _ => Err(ParseFailure::InvalidJson),
        }
    }

    fn starts_with(&self, bytes: &[u8]) -> bool {
        self.bytes.get(self.position..self.position + bytes.len()) == Some(bytes)
    }

    fn parse_array(&mut self) -> Result<RawValue, ParseFailure> {
        self.consume(b'[')?;
        self.skip_whitespace();
        let mut values = Vec::new();
        if self.peek() == Some(b']') {
            self.position += 1;
            return Ok(RawValue::Array(values));
        }
        loop {
            values.push(self.parse_value()?);
            self.skip_whitespace();
            match self.peek() {
                Some(b',') => {
                    self.position += 1;
                    self.skip_whitespace();
                }
                Some(b']') => {
                    self.position += 1;
                    return Ok(RawValue::Array(values));
                }
                _ => return Err(ParseFailure::InvalidJson),
            }
        }
    }

    fn parse_object(&mut self) -> Result<RawValue, ParseFailure> {
        self.consume(b'{')?;
        self.skip_whitespace();
        let mut fields = Vec::new();
        let mut names = HashSet::new();
        if self.peek() == Some(b'}') {
            self.position += 1;
            return Ok(RawValue::Object(fields));
        }
        loop {
            if self.peek() != Some(b'"') {
                return Err(ParseFailure::InvalidJson);
            }
            let key = self.parse_string()?;
            if let RawString::Text(name) = &key {
                if !names.insert(name.clone()) {
                    return Err(ParseFailure::DuplicateObjectName);
                }
            }
            self.skip_whitespace();
            self.consume(b':')?;
            self.skip_whitespace();
            let value = self.parse_value()?;
            fields.push((key, value));
            self.skip_whitespace();
            match self.peek() {
                Some(b',') => {
                    self.position += 1;
                    self.skip_whitespace();
                }
                Some(b'}') => {
                    self.position += 1;
                    return Ok(RawValue::Object(fields));
                }
                _ => return Err(ParseFailure::InvalidJson),
            }
        }
    }

    fn parse_number(&mut self) -> Result<RawValue, ParseFailure> {
        let start = self.position;
        if self.peek() == Some(b'-') {
            self.position += 1;
        }
        match self.peek() {
            Some(b'0') => self.position += 1,
            Some(b'1'..=b'9') => {
                self.position += 1;
                while matches!(self.peek(), Some(b'0'..=b'9')) {
                    self.position += 1;
                }
            }
            _ => return Err(ParseFailure::InvalidJson),
        }
        if self.peek() == Some(b'.') {
            self.position += 1;
            if !matches!(self.peek(), Some(b'0'..=b'9')) {
                return Err(ParseFailure::InvalidJson);
            }
            while matches!(self.peek(), Some(b'0'..=b'9')) {
                self.position += 1;
            }
        }
        if matches!(self.peek(), Some(b'e' | b'E')) {
            self.position += 1;
            if matches!(self.peek(), Some(b'+' | b'-')) {
                self.position += 1;
            }
            if !matches!(self.peek(), Some(b'0'..=b'9')) {
                return Err(ParseFailure::InvalidJson);
            }
            while matches!(self.peek(), Some(b'0'..=b'9')) {
                self.position += 1;
            }
        }
        let token = std::str::from_utf8(&self.bytes[start..self.position])
            .map_err(|_| ParseFailure::InvalidJson)?;
        Ok(RawValue::Number(token.to_owned()))
    }

    fn parse_string(&mut self) -> Result<RawString, ParseFailure> {
        self.consume(b'"')?;
        let mut output = Vec::new();
        let mut invalid_scalar = false;
        loop {
            let Some(byte) = self.peek() else {
                return Err(ParseFailure::InvalidJson);
            };
            match byte {
                b'"' => {
                    self.position += 1;
                    if invalid_scalar {
                        return Ok(RawString::InvalidScalar);
                    }
                    return String::from_utf8(output)
                        .map(RawString::Text)
                        .map_err(|_| ParseFailure::InvalidJson);
                }
                0x00..=0x1f => return Err(ParseFailure::InvalidJson),
                b'\\' => {
                    self.position += 1;
                    let Some(escape) = self.peek() else {
                        return Err(ParseFailure::InvalidJson);
                    };
                    self.position += 1;
                    match escape {
                        b'"' => output.push(b'"'),
                        b'\\' => output.push(b'\\'),
                        b'/' => output.push(b'/'),
                        b'b' => output.push(0x08),
                        b'f' => output.push(0x0c),
                        b'n' => output.push(b'\n'),
                        b'r' => output.push(b'\r'),
                        b't' => output.push(b'\t'),
                        b'u' => {
                            let first = self.parse_hex_quad()?;
                            if (0xd800..=0xdbff).contains(&first) {
                                if self.peek() == Some(b'\\')
                                    && self.bytes.get(self.position + 1) == Some(&b'u')
                                {
                                    self.position += 2;
                                    let second = self.parse_hex_quad()?;
                                    if (0xdc00..=0xdfff).contains(&second) {
                                        let scalar = 0x1_0000
                                            + (((first as u32 - 0xd800) << 10)
                                                | (second as u32 - 0xdc00));
                                        push_scalar(&mut output, scalar)?;
                                    } else {
                                        invalid_scalar = true;
                                    }
                                } else {
                                    invalid_scalar = true;
                                }
                            } else if (0xdc00..=0xdfff).contains(&first) {
                                invalid_scalar = true;
                            } else {
                                push_scalar(&mut output, first as u32)?;
                            }
                        }
                        _ => return Err(ParseFailure::InvalidJson),
                    }
                }
                _ => {
                    output.push(byte);
                    self.position += 1;
                }
            }
        }
    }

    fn parse_hex_quad(&mut self) -> Result<u16, ParseFailure> {
        let bytes = self
            .bytes
            .get(self.position..self.position + 4)
            .ok_or(ParseFailure::InvalidJson)?;
        let mut value = 0u16;
        for byte in bytes {
            value = (value << 4)
                | match byte {
                    b'0'..=b'9' => (byte - b'0') as u16,
                    b'a'..=b'f' => (byte - b'a' + 10) as u16,
                    b'A'..=b'F' => (byte - b'A' + 10) as u16,
                    _ => return Err(ParseFailure::InvalidJson),
                };
        }
        self.position += 4;
        Ok(value)
    }
}

fn push_scalar(output: &mut Vec<u8>, scalar: u32) -> Result<(), ParseFailure> {
    let character = char::from_u32(scalar).ok_or(ParseFailure::InvalidJson)?;
    let mut buffer = [0u8; 4];
    output.extend_from_slice(character.encode_utf8(&mut buffer).as_bytes());
    Ok(())
}

fn defect(phase: &str, code: &str, path: Vec<PathSegment>) -> StructuralDefect {
    StructuralDefect::new(phase, code, path)
}

fn parse_failure(failure: ParseFailure) -> AdmissionResult {
    let (phase, code) = match failure {
        ParseFailure::InvalidJson => ("decode", "INVALID_JSON"),
        ParseFailure::TrailingToken => ("decode", "TRAILING_TOKEN"),
        ParseFailure::DuplicateObjectName => ("admission", "DUPLICATE_OBJECT_NAME"),
    };
    AdmissionResult::rejected(vec![defect(phase, code, Vec::new())])
}

fn integer_token(token: &str) -> bool {
    let bytes = token.as_bytes();
    match bytes {
        [b'0'] => true,
        [b'-', b'1'..=b'9', rest @ ..] => rest.iter().all(u8::is_ascii_digit),
        [b'1'..=b'9', rest @ ..] => rest.iter().all(u8::is_ascii_digit),
        _ => false,
    }
}

fn safe_integer(token: &str) -> Option<i64> {
    if !integer_token(token) {
        return None;
    }
    let value = token.parse::<i64>().ok()?;
    (SAFE_INTEGER_MINIMUM..=SAFE_INTEGER_MAXIMUM)
        .contains(&value)
        .then_some(value)
}

fn is_noncharacter(scalar: u32) -> bool {
    (0xfdd0..=0xfdef).contains(&scalar) || matches!(scalar & 0xffff, 0xfffe | 0xffff)
}

fn scalar_defects(value: &str, path: &[PathSegment]) -> Vec<StructuralDefect> {
    let version = match unicode_runtime_version() {
        Ok(version) if version == PINNED_UNICODE_VERSION => version,
        Ok(_) | Err(_) => {
            return vec![defect(
                "admission",
                "UNICODE_RUNTIME_UNAVAILABLE",
                path.to_vec(),
            )]
        }
    };
    let _ = version;
    for character in value.chars() {
        let scalar = character as u32;
        if is_noncharacter(scalar) {
            return vec![defect("admission", "UNICODE_NONCHARACTER", path.to_vec())];
        }
        match host_icu::is_assigned(scalar) {
            Ok(false) => return vec![defect("admission", "UNICODE_UNASSIGNED", path.to_vec())],
            Err(_) => {
                return vec![defect(
                    "admission",
                    "UNICODE_RUNTIME_UNAVAILABLE",
                    path.to_vec(),
                )]
            }
            Ok(true) => {}
        }
    }
    match host_icu::is_nfc(value) {
        Ok(true) => Vec::new(),
        Ok(false) => vec![defect("admission", "NON_NFC_TEXT", path.to_vec())],
        Err(_) => vec![defect(
            "admission",
            "UNICODE_RUNTIME_UNAVAILABLE",
            path.to_vec(),
        )],
    }
}

fn admit_value(raw: RawValue, path: Vec<PathSegment>) -> (Value, Vec<StructuralDefect>) {
    match raw {
        RawValue::Null => (Value::Null, Vec::new()),
        RawValue::Bool(value) => (Value::Bool(value), Vec::new()),
        RawValue::Number(token) => match safe_integer(&token) {
            Some(value) => (Value::Number(Number::from(value)), Vec::new()),
            None if integer_token(&token) => (
                Value::Null,
                vec![defect("admission", "INTEGER_OUT_OF_RANGE", path)],
            ),
            None => (
                Value::Null,
                vec![defect("admission", "NON_CANONICAL_INTEGER", path)],
            ),
        },
        RawValue::String(RawString::Text(value)) => {
            let defects = scalar_defects(&value, &path);
            (Value::String(value), defects)
        }
        RawValue::String(RawString::InvalidScalar) => (
            Value::Null,
            vec![defect("admission", "INVALID_UNICODE_SCALAR", path)],
        ),
        RawValue::Array(values) => {
            let mut admitted = Vec::with_capacity(values.len());
            let mut defects = Vec::new();
            for (index, value) in values.into_iter().enumerate() {
                let mut child_path = path.clone();
                child_path.push(PathSegment::Index(index));
                let (value, child_defects) = admit_value(value, child_path);
                admitted.push(value);
                defects.extend(child_defects);
            }
            (Value::Array(admitted), defects)
        }
        RawValue::Object(fields) => {
            let mut admitted = Map::new();
            let mut defects = Vec::new();
            for (key, value) in fields {
                let RawString::Text(key) = key else {
                    defects.push(defect("admission", "INVALID_UNICODE_SCALAR", path.clone()));
                    continue;
                };
                let mut child_path = path.clone();
                child_path.push(PathSegment::Field(key.clone()));
                defects.extend(scalar_defects(&key, &child_path));
                let (value, child_defects) = admit_value(value, child_path);
                admitted.insert(key, value);
                defects.extend(child_defects);
            }
            (Value::Object(admitted), defects)
        }
    }
}

/// Admit raw UTF-8 JSON without losing duplicate names or numeric token shape.
pub fn admit_json(raw: &[u8]) -> AdmissionResult {
    if raw.starts_with(&[0xef, 0xbb, 0xbf]) {
        return AdmissionResult::rejected(vec![defect("decode", "UTF8_BOM_FORBIDDEN", Vec::new())]);
    }
    if std::str::from_utf8(raw).is_err() {
        return AdmissionResult::rejected(vec![defect("decode", "INVALID_UTF8", Vec::new())]);
    }
    let parsed = match Parser::new(raw).parse() {
        Ok(value) => value,
        Err(failure) => return parse_failure(failure),
    };
    let (value, defects) = admit_value(parsed, Vec::new());
    if !defects.is_empty() {
        return AdmissionResult::rejected(defects);
    }
    match canonical_payload_bytes(&value) {
        Ok(payload_bytes) => AdmissionResult {
            value: Some(value),
            payload_bytes: Some(payload_bytes),
            defects: Vec::new(),
        },
        Err(_) => AdmissionResult::rejected(vec![defect(
            "admission",
            "CANONICALIZATION_FAILED",
            Vec::new(),
        )]),
    }
}

/// Admit a JSON string under the schema-owned canonical-decimal rule.
pub fn admit_canonical_decimal(raw: &[u8]) -> AdmissionResult {
    let result = admit_json(raw);
    if !result.admitted() {
        return result;
    }
    let is_decimal = result
        .value
        .as_ref()
        .and_then(Value::as_str)
        .is_some_and(is_canonical_decimal);
    if is_decimal {
        result
    } else {
        AdmissionResult::rejected(vec![defect("schema", "NON_CANONICAL_DECIMAL", Vec::new())])
    }
}

fn is_canonical_decimal(value: &str) -> bool {
    if value == "0" {
        return true;
    }
    let unsigned = value.strip_prefix('-').unwrap_or(value);
    if unsigned.is_empty() || unsigned == "0" {
        return false;
    }
    let (integer, fractional) = match unsigned.split_once('.') {
        Some((integer, fractional)) => (integer, Some(fractional)),
        None => (unsigned, None),
    };
    let integer_valid = if integer == "0" {
        fractional.is_some()
    } else {
        integer
            .as_bytes()
            .first()
            .is_some_and(|first| (b'1'..=b'9').contains(first))
            && integer.as_bytes().iter().all(u8::is_ascii_digit)
    };
    let fraction_valid = fractional.is_none_or(|fractional| {
        !fractional.is_empty()
            && fractional.as_bytes().iter().all(u8::is_ascii_digit)
            && !fractional.ends_with('0')
    });
    integer_valid && fraction_valid
}

/// Admit a value's exact tuple against the supplied closed registry.
pub fn admit_version_tuple(
    value: &VersionTuple,
    registry: &VersionRegistry,
) -> Vec<StructuralDefect> {
    if registry.admits(value) {
        Vec::new()
    } else {
        vec![defect("admission", "VERSION_TUPLE_UNSUPPORTED", Vec::new())]
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
enum PrimaryComponent {
    Integer(i64),
    Text(Vec<u16>),
}

fn resolve_key_path<'a>(value: &'a Value, path: &str) -> Option<&'a Value> {
    if path == "$" {
        return Some(value);
    }
    path.split('.')
        .try_fold(value, |current, segment| current.as_object()?.get(segment))
}

fn primary_component(value: &Value) -> Option<PrimaryComponent> {
    match value {
        Value::Number(value) => value.as_i64().map(PrimaryComponent::Integer),
        Value::String(value) => Some(PrimaryComponent::Text(value.encode_utf16().collect())),
        _ => None,
    }
}

/// Normalize an order-insensitive semantic collection by declared primary keys.
///
/// Equal primary keys are deterministically resolved by canonical payload bytes;
/// a fully equal semantic identity is rejected rather than deduplicated.
pub fn normalize_semantic_elements(
    elements: Vec<Value>,
    primary_key_paths: &[String],
) -> Result<Vec<Value>, StructuralDefect> {
    if primary_key_paths.is_empty() {
        return Err(defect("normalization", "NORMALIZATION_FAILED", Vec::new()));
    }
    let mut decorated = Vec::with_capacity(elements.len());
    for element in elements {
        let primary = primary_key_paths
            .iter()
            .map(|path| resolve_key_path(&element, path).and_then(primary_component))
            .collect::<Option<Vec<_>>>()
            .ok_or_else(|| defect("normalization", "NORMALIZATION_FAILED", Vec::new()))?;
        let payload = canonical_payload_bytes(&element)
            .map_err(|_| defect("normalization", "NORMALIZATION_FAILED", Vec::new()))?;
        decorated.push((primary, payload, element));
    }
    decorated.sort_by(|left, right| left.0.cmp(&right.0).then_with(|| left.1.cmp(&right.1)));
    if decorated
        .windows(2)
        .any(|pair| pair[0].0 == pair[1].0 && pair[0].1 == pair[1].1)
    {
        return Err(defect(
            "normalization",
            "DUPLICATE_SEMANTIC_IDENTITY",
            Vec::new(),
        ));
    }
    Ok(decorated
        .into_iter()
        .map(|(_, _, element)| element)
        .collect())
}

/// Return the host ICU Unicode data version used for scalar admission.
pub fn unicode_runtime_version() -> Result<[u8; 4], String> {
    host_icu::version()
}

#[cfg(target_os = "linux")]
mod host_icu {
    use core::ffi::{c_int, c_void};

    #[link(name = "icuuc")]
    extern "C" {
        #[link_name = "u_getUnicodeVersion_74"]
        fn u_get_unicode_version(version_array: *mut u8);
        #[link_name = "u_charType_74"]
        fn u_char_type(scalar: c_int) -> c_int;
        #[link_name = "unorm2_getNFCInstance_74"]
        fn unorm2_get_nfc_instance(status: *mut c_int) -> *const c_void;
        #[link_name = "unorm2_isNormalized_74"]
        fn unorm2_is_normalized(
            normalizer: *const c_void,
            value: *const u16,
            length: c_int,
            status: *mut c_int,
        ) -> i8;
    }

    pub fn version() -> Result<[u8; 4], String> {
        let mut version = [0u8; 4];
        // SAFETY: ICU writes exactly four `UVersionInfo` bytes to the provided
        // initialized, writable buffer and retains no pointer to it.
        unsafe { u_get_unicode_version(version.as_mut_ptr()) };
        Ok(version)
    }

    pub fn is_assigned(scalar: u32) -> Result<bool, String> {
        let scalar = c_int::try_from(scalar).map_err(|_| "scalar out of range")?;
        // SAFETY: scalar values come from Rust `char`, so they are Unicode
        // scalar values accepted by ICU's `UChar32` parameter.
        Ok(unsafe { u_char_type(scalar) } != 0)
    }

    pub fn is_nfc(value: &str) -> Result<bool, String> {
        let units = value.encode_utf16().collect::<Vec<_>>();
        let length = c_int::try_from(units.len()).map_err(|_| "string too long")?;
        let mut status = 0;
        // SAFETY: ICU returns an immutable singleton normalizer, and `status`
        // points to writable `UErrorCode` storage for this call.
        let normalizer = unsafe { unorm2_get_nfc_instance(&mut status) };
        if status != 0 || normalizer.is_null() {
            return Err("could not acquire ICU NFC normalizer".to_owned());
        }
        // SAFETY: `units` remains live for the duration of the call, has the
        // supplied UTF-16 length, and the ICU normalizer is immutable.
        let normalized =
            unsafe { unorm2_is_normalized(normalizer, units.as_ptr(), length, &mut status) };
        if status != 0 {
            return Err("ICU NFC normalization failed".to_owned());
        }
        Ok(normalized != 0)
    }
}

#[cfg(not(target_os = "linux"))]
mod host_icu {
    pub fn version() -> Result<[u8; 4], String> {
        Err("pinned ICU 74 bridge is only installed for this Linux prototype".to_owned())
    }

    pub fn is_assigned(_scalar: u32) -> Result<bool, String> {
        Err("pinned ICU 74 bridge is unavailable".to_owned())
    }

    pub fn is_nfc(_value: &str) -> Result<bool, String> {
        Err("pinned ICU 74 bridge is unavailable".to_owned())
    }
}
