#!/usr/bin/env python3
"""Validate fixture schemas and positive/error outputs with Draft 2020-12."""
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
SCHEMAS = ROOT / "schemas"

def load(name):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))

def validate(schema, value):
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(value)

event_schema = load("telemetry-events.schema.json")
barrier_schema = load("audit-barrier.schema.json")
check_schema = load("post-audit-check.schema.json")
for case in ("positive-attempt-1", "positive-attempt-2"):
    directory = ROOT / "cases" / case
    barrier = json.loads((directory / "audit-barrier.json").read_text(encoding="utf-8"))
    validate(barrier_schema, barrier)
    for line in (directory / "sigil-invocations.jsonl").read_text(encoding="utf-8").splitlines():
        validate(event_schema, json.loads(line))
    proc = subprocess.run([
        "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
        str(ROOT / "verify-post-audit-telemetry.ps1"), "-AuditBarrier", str(directory / "audit-barrier.json"),
        "-SignalJsonl", str(directory / "sigil-invocations.jsonl")
    ], capture_output=True, text=True, check=True)
    validate(check_schema, json.loads(proc.stdout))

# Error output with unreadable inputs must remain schema-valid.
proc = subprocess.run([
    "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
    str(ROOT / "verify-post-audit-telemetry.ps1"), "-AuditBarrier", str(ROOT / "missing.json"),
    "-SignalJsonl", str(ROOT / "missing.jsonl")
], capture_output=True, text=True)
assert proc.returncode == 2
validate(check_schema, json.loads(proc.stdout))

bad_utf8 = ROOT / "invalid-utf8-schema-test.jsonl"
try:
    bad_utf8.write_bytes(b"\xff\n")
    proc = subprocess.run([
        "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
        str(ROOT / "verify-post-audit-telemetry.ps1"), "-AuditBarrier",
        str(ROOT / "cases" / "positive-attempt-1" / "audit-barrier.json"),
        "-SignalJsonl", str(bad_utf8)
    ], capture_output=True, text=True)
    assert proc.returncode == 2
    validate(check_schema, json.loads(proc.stdout))
finally:
    bad_utf8.unlink(missing_ok=True)
print("PASS: schemas and emitted positive/error results validate")
