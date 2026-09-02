"""Pure DraftGraph v1 to proposed ExecutionGraph v2 compiler.

This module is deliberately outside confirmation and execution.  A successful
result is a deterministic candidate authority value; it does not accept,
persist, schedule, or execute that value.
"""

from __future__ import annotations

import hashlib
import base64
import json
import re
import weakref
import zlib
from dataclasses import dataclass
from typing import Any, NoReturn

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError as JsonSchemaValidationError


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_KEY = re.compile(r"[a-z][a-z0-9_]{0,63}\Z")
_REVISION = re.compile(r"r([1-9][0-9]*)\Z")
_LIMIT_FIELDS = ("max_attempts", "max_tokens", "wall_clock_seconds")
_TOPOLOGY_STATE_LIMIT = 4096
_UNPROVABLE_SCHEMA_KEYS = {
    "$ref", "$dynamicRef", "allOf", "anyOf", "oneOf", "not", "if", "then", "else"
}
_ALLOCATOR_KEY_ID = "aci-fixture-allocator-ed25519-1"
_ALLOCATOR_PUBLIC_KEY = bytes.fromhex("03a107bff3ce10be1d70dd18e74bc09967e4d6309ba50d5f1ddc8664125531b8")
_ISSUED_CONTEXTS: weakref.WeakSet[VerifiedCompilationContext] = weakref.WeakSet()

_EMBEDDED_CONTRACTS = {
    "compilation_context": ("aa83518b76c8eaec48be50161e9e0c5c024f64368fadecaf505095caef58c813",
        "eNqVUtFOgzAUfd9XkMqTGWMQNXFPfoCJvi9IanuBLozW9rLMEP7dWxiTRbPoC2nOPefc01O6RRCw0IkK9pxtAlYhGreJ453TTTTC"
        "K23LWFpeYJyu03WUpPGJvxzESnohF2ol9N6omqMirdANwhGjQh2xtfCUrOYi/DTgVfp9BwJHjEupvJTXr1YbsKjAEafgtYOBYOGj"
        "VRb8ui2b3AImlTMcRZVTkKVnHZQjG3/mda3FkOc0nAEOObbOg8YqbXMuBBgEmZeWmyqXqgSHLBs2m3mgjhDCzp11jO5K1L+UwPrl"
        "qJ6H9hZTIQ6takqfaq+aZ2hKrAhOJtn5cr9ryBLB+il7s9skesy2a/rchue9l438Y/PP5i5ubsGBPdDbTPxrpXqlbuCl8C/5naBp"
        "65r0NAwt+Bm7iUMJhYtPuj7rybwffzs/GJxmptcbcRVP7x82vhIeFVn3cNdTMf2iX3wBQHb2pg=="),
    "allocator_evidence": ("f595bd8d60335469f008c2c1e5d5ce7baf42e745a5a1d1e8cbf151edfff599c6",
        "eNqNkM1ugzAQhO95CmTlGIeAmkjh1AfoofcoRRtYYFNiU3upEiHevTbkB0VV1Zs9mm92d7pZEIi5zSo8gUgCUTE3NgnDo9VKjvJS"
        "mzLMDRQcxqt4JaM4vPoXA0y5ByGjJdS1zoC1kfhNOaoMZUFnbg2+Rsspw5cGPaQPR8x41CDPiUkrqN+NbtAwoXWeAmqLg8HgV0sG"
        "/bSduKUF4hMvqVvBvTKtGM+c5lSiZa+QTWvg66cBMqlTWnXQrRoIS6UCv5/YDyOa6eTOKU67d9P5AS7qH8eKfjHC1+We4ZtTTkLy"
        "eL2OtvLBPp3jM269WTakyvEoZjTKix+2gni9SXYruQVZ7LvNSz+/pz2qmAYdtK4R1N313NFf3kd5v692IvWGquTKyVHvmH7Wz34A"
        "Si3FMw=="),
    "draft": ("6d70aca724c5bf3c661b6ae95eff1f24de299094a5a8a59fb9ac12101fd7a395",
        "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"),
    "policy": ("328fb5ee1f9f32cf948c5ad6408357ed063b5aa59de533554c13389055ada15a",
        "eNq9V8tu2zAQvOcrDNWnIo6dFCjQnIpeigIF2nviCDS1thlTpEJSeTTQv3eXlCzJphUXMXpJIHJmd7mPIf16NholY8vXkLPkepSs"
        "nSvs9XR6b7WahOULbVbTzLClm17NrmaTy6tpjT/3ZJERkXFxwXVeCMmcQG6hpeAvk6V4dqWBr5cXXY57KYBIenEP3IU1lmWCmEz+"
        "NroA4wRYxCyZtOABBh5KYYC83SSNtVFi8b9ygtt0Ay+0UKqN0k+KPlPGySStqjIHI3gqRS5cCs8crO1so8NcWItf+3srqRdM1kwO"
        "Qgq18iZ1BvurTEr9BFnKVqBcuhAqww1LO5wVbIE495KuDMZsu/BHJkXGnDYUd9jhPo6u6RJTlNZ5yIEszH1qim7GXnEF17Y1fU24"
        "VtYdU6SkOq/JvaSSjbGBJZn4MB1nsLRTWm/QkYz33BrwZW7gQ6UgHiDAF9mAdQh0dPbaxrwxcrBgQ56jlYydziNsG/F+pY9gHegE"
        "YjYDwIxhvmmFg9xGjXr2t0BOqsb2fi/9o9nWwHfit5YPNGTUfKnEQwk/aifOlDDo0/fM1k+/vaNH95A2n/vtH2URLKmQUwWBotV2"
        "LpqGbg5DLRbGq2DOgaEOSu5u2OTPnP7MJl/S+evs/POnaryNpC5010wjZW8I2Y6M5ew5Ja95EdSAvp3egPJfT1iLlEvNN6kF7OmM"
        "5n132vs2uiEJ5WAFxtsVSuR+qi6rvpvjCJFIjiC2te728PuzZrSEJCTiUWRgGuXPcUxl84GbSyGh+eRIxiAEC4BIHr3Vw1K3424I"
        "2MbxhrltgEO4ncgJqhX8IuxNm0lVSknwA3bmVUQ6wuS/vx4dMaqz3YgIMf1VE+3cHd5QEiIGT6dIfe07xVhjA2zTEJ1ZAvTuOixx"
        "mzkprL/qYhEde9R9fcPR/Alq5db1cPaV+BRzCSxLUUXXQb0MBtN+KnBP2mz8LOocnxeZX4Zn0lzsbVgu0aVfewTjL3YUGodTGR3W"
        "1tVpktMVf4rTFozD9fTm7vbW3N6q+ccxXV39U/1fz00Co3eeb5Oqm9vTdXFtMrwDhpp5++zyzVztUqPpwquoydWs8ufc64jhA+82"
        "ywnkDIMWnlWUdh0VroDoulpovD6YCspOtOhmd+r8M+UUQ8e1QWH0ZPEI4bHs1/y1azsLRpeuC8AHdim3CBCFS8PPBtrRpeFw8LLc"
        "9dqtPzV9tRfGACLENQSoAz0AORj5gObT+/CsOvsLudfyQQ=="),
    "catalog": ("ba8f0b71aa0023f3b4cab9b6a71aa4a762e309bdf7d2f91cb58d0b7ecac216ed",
        "eNrFVkuP2jAQvvMrUJZjQoC2SOW010o9VHtFNPI6E/DWibO2syqN8t9rOy8nsGwQWXGBeOz5ZvzNy/lkOnVmAh8gRs5m6hykTMXG"
        "918ES7xSPGd874ccRdJfLVYLb7nyq/OuUSahVkSYzDGLU0KRJEoXI4ko23sR+SszDo/Lua0kjyloLfb8AliWMhSGRKsi+ouzFLgk"
        "INSZCFEB5gCH14xw0Oa2To02dYT6TyTBQi9Szt5ICNwsYhYCrcURoWC+MUrRM6HE4Kv1G6IkRJKVOlgZAAWnrDo7Yza1vcmVRMka"
        "wnIHs0TIQQw4hVtpNx5rgJoLxDk6aheIhLjcmnGI9NaDPwshEr4gcUrBKWqg9rY3AlVMXYlitDrelCRfCVPptUCdCF0J1ugeWzwr"
        "wjfyZGfHtY41qgpOoRVl9ei9Nq/+wLGDKyQnyd5kMJISeKKFv7fI+7fTPwvve7DLF+76SzFrsiskezAZ+RGMOKDVt/Vmq1CQF+3y"
        "9VcLpfQ+P6nUD+q0V6UJisHUmMpRpaI/K/d2br+yysPn3Y5J8hOSvTwo8bKwAAcetzjpx6XaKpoYVzG//fI6mG7JZONCIFjGMZy7"
        "fh37voNaXrhtRPr7elmcGBhCTLf8x7tx3ZaCkRno4N6JqrpZfRpZJhZ3Y661fid+rf49GsX6mJnJZsJLxmgwFrEW9Nl5oG75oxoJ"
        "S7XMEvKaQS2RPIOLM8NYKWyfP4v1Zjg9jdL3DygJKZQZLBhV3bpmXD2XJEdYBtZIEFjhBe8PhgptYK/vWLzE14krAw103B00UqzZ"
        "P1pSt5ijJXMP8vIr5umGrNPPn0kx+Q/gNPGN"),
    "resources": ("a3e7e111ca43ba2a0ee259198618dfb8b848814dd38ed97d671321751c9c19bd",
        "eNqNUstOwzAQvPcrqtBj07QFKuiJD+CAuFahMvGmXUjsYG8kSpR/x+skrVtVgkse453Z2R03o/E4mthsD6WI1uNoT1TZdZJ8WK3i"
        "Dp5ps0ukETkly/lyHi+WSV8/9WSUTBQZzjJdVlgIQsc1YHVtMohz/KbawNNiFrLoUAHT9PsHZNRhQkpkrihejK7AEIJ1NbkoLPgC"
        "A181GuB+m2hQY7hrZaPUl1Uhu3GIw44TNlGmlaX/WY7aaUc/tWCFwbwwRhzYARKU3dHEQM5HN8lEQm4TVAUqeO3pUds6vbbbG5+f"
        "DH7C4UzbkkG1Y/FKEIFRDL5tRPyT8mMeP27TZj5d3baTo0uJO/Cj/SVj92J5v1pvnIqI87RZ3QUqF5YHh9dD8/hfwfUrDMIb9rnl"
        "sZ25T1SS3yVIFFvfx/2ByrTs7bvUCBTxZz9mepS+EvhZatthuZfpMN5OTwRvgwtB1aU36tt++7anC1fpArMueFXVzkmoEYxwPYgS"
        "1TOoHe0dvAiZx3HPHNSUxw/MexcWVnfnzYatXOkUlgUX43IF/VHbF3dvf0tH7egX0345bg=="),
    "execution_graph": ("af54864f68e56b83d9107d82797bb1094e45e790a94d42ab57d16c95f11fa706",
        "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"),
}

# Identity/role successor schemas supersede only these three embedded contracts.  Keeping the
# remaining blobs unchanged preserves the reviewed catalog/resource/ExecutionGraph boundary.
_EMBEDDED_CONTRACTS.update({
    "compilation_context": (
        "74ca184928a8a4f425b4565baae3ca342fa592cd1924607f561299e94e9487ec",
        "eNqtVE1v2zAMvfdXBFpOQxzH2RZgOfU6YMB2DzxDtWlbnS1plBLUC/zfR/k7TZqkwC62RPE9kY+kjg+zGZubOIeSs+2M5dZqs/X9Z6Ok15qXCjM/QZ5af71ar7xg7Xf+iwYsEgfksVjGqtSi4FYQNlbSwot9DJYalVYGkqVIQFphKw9VAR4GLd5WGhyBenqG2LY2niTCsfDiJ4EBrQBDPikvDDQOCH/2AsHdvGN9NDOWCKO5jfOIYlo4r4MwROPWvChU3ITWHU4MxnK7N86oUSiMeByDtpBEGXKdR4nIwNiGkAKPEDJhLFa0SBuijNKKtFLFqYUbIzJZ0tKwsIlaT5M5koVsg/RHRpLRNW9r6aXixe4RHgNWL1r0NGFH0YtJ8QmZuVhKIb+DzGxO5qCHDcJcxhClBXSn7BfuAu9ruFvR5+N8uPdUzXfcfK76SeYIBvBAde39rxXEIZWEH6nrgjECuS8KwtPh3NWDLB/8eQKp8TtcHQ46nNVzewHmtkP8p8W+z33aCVOtOCKvOqm+WSjdaUBb0a3PuUcmVtd0Rd2OoDsbW2oiz/Xampyvv2y2rrjcS8Pj5nM9lrhLr9lcGNPbQ9qxTAZV8hIc8gDYj2UXazgALsxIY2+wdzXayH9/X77W7a3O6Zzb/1DksSj/WzCVQPQbqv5tK3gV9SI2vZsKGylKF+ltvWikLuX0lN8jcH/X7b7Zce9v6D7UOFF4XC02n8bGGd6lIdh3luE8sSnBE40ecMmuIvqsb74Qt8IKX1XcjdxD/fAPbUM62A==",
    ),
    "allocator_evidence": (
        "78aeadc4f619c8d9b2c8f5e224ce99131f0ad649b033a9c873b65a7f0ea30cb1",
        "eNqVUU1PwkAQvfMrmoabbguNEiUh0bsHzxJshnbaDpbdujs1YNP/7i600BDjx23n5b03b942I8/zxyYpcAv+3PML5srMw3BjlBRHOFA6D1MNGYfRJJqIaRR2/OuDmFInhIQCKEuVACst8INSlAmKjHZca3yIAgcw8V5oVaLQUTA04X2FzkWtN5jwEYM0JSYloXzWqkLNhMZyMigNHgga32vS6NYv/d7N8/vdsQ1mxzfcd69EScYdxynlaNghZOISuBsqIB1bpJZrVcuDwlAuweX3V4eN1TBIYxGLnbpr3AJr9Ycy/Pb6KB5mdQ59D4Y1ydxF2JJ8QplzYeFpL+tu+ofi4vbvlRUwo5YOfDUFRLez+XIi7kFkq2Z2045Psc+9DY3Wyv4syBPrstCfuOemf4+2fBQvID5tsqtw1dzN2sXCRrM+7agdfQGv2OLC",
    ),
    "draft": (
        "2659b5ddd24720a41e9a8333673847bb2bee302db75a1f57a014064a3cb7f691",
        "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",
    ),
})


def _load_contract_validators() -> dict[str, Draft202012Validator]:
    validators: dict[str, Draft202012Validator] = {}
    for name, (expected_digest, compressed) in _EMBEDDED_CONTRACTS.items():
        try:
            raw = zlib.decompress(base64.b64decode(compressed, validate=True))
            if hashlib.sha256(raw).hexdigest() != expected_digest:
                raise ValueError("contract digest mismatch")
            schema = json.loads(raw.decode("utf-8"), parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
            Draft202012Validator.check_schema(schema)
        except (ValueError, UnicodeError, zlib.error, json.JSONDecodeError, SchemaError) as error:
            raise RuntimeError(f"invalid bundled compiler schema {name}: {error}") from error
        validators[name] = Draft202012Validator(schema)
    return validators


def bundled_contract_schema_digests() -> dict[str, str]:
    """Exact SHA-256 values for the conformance schema bytes embedded in this module."""
    return {name: "sha256:" + value[0] for name, value in _EMBEDDED_CONTRACTS.items()}


_CONTRACT_VALIDATORS = _load_contract_validators()


class DraftGraphCompileError(Exception):
    """Stable fail-closed compiler error with a source-linked JSON path."""

    def __init__(self, code: str, path: str, detail: str = "") -> None:
        self.code = code
        self.path = path
        self.detail = detail
        super().__init__(f"{code} at {path}" + (f": {detail}" if detail else ""))


def _fail(code: str, path: str, detail: str = "") -> NoReturn:
    raise DraftGraphCompileError(code, path, detail)


def _reject_non_scalar_unicode(value: Any, path: str, code: str) -> None:
    """Reject lone surrogates before validators, hashing or canonical serialization."""
    if isinstance(value, str):
        try:
            value.encode("utf-8", errors="strict")
        except UnicodeEncodeError:
            _fail(code, path, "string contains a lone surrogate")
        return
    if isinstance(value, list):
        for position, member in enumerate(value):
            _reject_non_scalar_unicode(member, f"{path}[{position}]", code)
        return
    if isinstance(value, dict):
        for key, member in value.items():
            if isinstance(key, str):
                try:
                    key.encode("utf-8", errors="strict")
                except UnicodeEncodeError:
                    _fail(code, f"{path}.<member-name>", "member name contains a lone surrogate")
                member_path = f"{path}.{key}"
            else:
                member_path = f"{path}.<member-name>"
            _reject_non_scalar_unicode(member, member_path, code)


class VerifiedCompilationContext:
    """Opaque gate-issued allocator authority; direct/copy/pickle construction fails."""

    __slots__ = ("_context_bytes", "_evidence_bytes", "__weakref__")

    def __new__(cls, *_: Any, **__: Any) -> "VerifiedCompilationContext":
        raise TypeError("VerifiedCompilationContext is issued only by TrustedAllocatorContextGate")

    def __setattr__(self, _: str, __: Any) -> None:
        raise TypeError("VerifiedCompilationContext is immutable")

    def __copy__(self) -> "VerifiedCompilationContext":
        raise TypeError("VerifiedCompilationContext cannot be copied")

    def __deepcopy__(self, _: Any) -> "VerifiedCompilationContext":
        raise TypeError("VerifiedCompilationContext cannot be copied")

    def __reduce__(self) -> Any:
        raise TypeError("VerifiedCompilationContext cannot be pickled")

    @property
    def dispatch_id(self) -> str:
        return _context_from_issued(self)["dispatch_id"]

    @property
    def revision(self) -> str:
        return _context_from_issued(self)["revision"]

    @property
    def allocation_id(self) -> str:
        return _context_from_issued(self)["allocation_id"]

    @property
    def prior_accepted_graph_digest(self) -> str | None:
        return _context_from_issued(self)["prior_accepted_graph_digest"]


@dataclass(frozen=True, slots=True)
class CompilationResult:
    _canonical_bytes: bytes
    _report: tuple[bytes, ...]

    @property
    def canonical_bytes(self) -> bytes:
        return self._canonical_bytes

    @property
    def graph(self) -> dict[str, Any]:
        return json.loads(self._canonical_bytes.decode("utf-8"))

    @property
    def digest(self) -> str:
        return "sha256:" + hashlib.sha256(self._canonical_bytes).hexdigest()

    @property
    def report(self) -> tuple[dict[str, Any], ...]:
        return tuple(json.loads(item.decode("utf-8")) for item in self._report)


def _duplicate_rejector(path: str, structural_code: str):
    def reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, member in pairs:
            _reject_non_scalar_unicode(key, f"{path}.<member-name>", structural_code)
            if key in value:
                _fail("DG_DUPLICATE_JSON_KEY", path, key)
            value[key] = member
        return value
    return reject


def _parse(raw: bytes | str, path: str, structural_code: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    except UnicodeDecodeError as error:
        _fail(structural_code, path, "input is not UTF-8")
    if not isinstance(text, str):
        _fail(structural_code, path, "input must be JSON bytes or text")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_duplicate_rejector(path, structural_code),
            parse_constant=lambda token: _fail(structural_code, path, f"invalid number {token}"),
        )
    except DraftGraphCompileError:
        raise
    except (json.JSONDecodeError, UnicodeError) as error:
        _fail(structural_code, path, str(error))
    if not isinstance(value, dict):
        _fail(structural_code, path, "root must be an object")
    _reject_non_scalar_unicode(value, path, structural_code)
    return value


def _stable_error_path(root: str, parts: Any) -> str:
    path = root
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def _validate_structure(name: str, value: dict[str, Any], code: str, root: str) -> None:
    try:
        errors = list(_CONTRACT_VALIDATORS[name].iter_errors(value))
    except Exception as error:
        _fail(code, root, f"structural validation failed: {type(error).__name__}")
    if not errors:
        return
    error = min(
        errors,
        key=lambda item: (
            tuple((0, part) if isinstance(part, int) else (1, str(part)) for part in item.absolute_path),
            tuple(str(part) for part in item.absolute_schema_path),
            item.validator or "",
        ),
    )
    _fail(code, _stable_error_path(root, error.absolute_path), error.message)


def _allocator_message(value: dict[str, Any]) -> bytes:
    payload = {key: value[key] for key in ("schema", "evidence_id", "key_id", "context_digest", "is_latest", "pair_is_unbound")}
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _issue_context(context_bytes: bytes, evidence_bytes: bytes) -> VerifiedCompilationContext:
    context = object.__new__(VerifiedCompilationContext)
    object.__setattr__(context, "_context_bytes", context_bytes)
    object.__setattr__(context, "_evidence_bytes", evidence_bytes)
    _ISSUED_CONTEXTS.add(context)
    return context


def _verify_allocator_evidence(
    context_value: dict[str, Any],
    evidence_value: dict[str, Any],
    trust_value: dict[str, Any] | None = None,
    consumed_evidence_ids: set[str] | None = None,
) -> None:
    code = "DG_ALLOCATOR_EVIDENCE_INVALID"
    _validate_structure("allocator_evidence", evidence_value, code, "allocator_evidence")
    _exact(evidence_value, {"schema", "evidence_id", "key_id", "context_digest", "is_latest", "pair_is_unbound", "signature"}, "allocator_evidence", code)
    if evidence_value["schema"] != "aci.allocator-evidence-fixture@2":
        _fail(code, "allocator_evidence")
    _text(evidence_value["evidence_id"], "allocator_evidence.evidence_id", code)
    _validate_digest(evidence_value["context_digest"], "allocator_evidence.context_digest", code)
    _boolean(evidence_value["is_latest"], "allocator_evidence.is_latest", code)
    _boolean(evidence_value["pair_is_unbound"], "allocator_evidence.pair_is_unbound", code)
    if not isinstance(evidence_value["signature"], str): _fail(code, "allocator_evidence.signature")
    context_bytes = json.dumps(context_value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    actual_digest = "sha256:" + hashlib.sha256(context_bytes).hexdigest()
    if actual_digest != evidence_value["context_digest"]: _fail("DG_IDENTITY_CONTEXT_STALE", "compilation_context")
    public_key = _ALLOCATOR_PUBLIC_KEY
    if trust_value is not None:
        if not isinstance(trust_value, dict) or set(trust_value) != {"schema", "keys"} or trust_value.get("schema") != "aci.allocator-trust@1" or not isinstance(trust_value.get("keys"), list):
            _fail("DG_ALLOCATOR_TRUST_INVALID", "allocator_trust")
        matches = [row for row in trust_value["keys"] if isinstance(row, dict) and row.get("key_id") == evidence_value["key_id"] and row.get("enabled") is True]
        if len(matches) != 1 or matches[0].get("algorithm") != "Ed25519":
            _fail("DG_ALLOCATOR_KEY_UNTRUSTED", "allocator_evidence.key_id")
        try:
            public_key = base64.b64decode(matches[0]["public_key_base64"], validate=True)
        except (KeyError, TypeError, ValueError):
            _fail("DG_ALLOCATOR_TRUST_INVALID", "allocator_trust.keys")
    elif evidence_value["key_id"] != _ALLOCATOR_KEY_ID:
        _fail("DG_ALLOCATOR_KEY_UNTRUSTED", "allocator_evidence.key_id")
    try:
        signature = base64.b64decode(evidence_value["signature"], validate=True)
        Ed25519PublicKey.from_public_bytes(public_key).verify(signature, _allocator_message(evidence_value))
    except (ValueError, InvalidSignature):
        _fail(code, "allocator_evidence.signature")
    if consumed_evidence_ids is not None and evidence_value["evidence_id"] in consumed_evidence_ids:
        _fail("DG_ALLOCATOR_EVIDENCE_REPLAY", "allocator_evidence.evidence_id")
    if not evidence_value["is_latest"]: _fail("DG_IDENTITY_CONTEXT_STALE", "allocator_evidence.is_latest")
    if not evidence_value["pair_is_unbound"]: _fail("DG_AUTHORITY_CONFLICT", "allocator_evidence.pair_is_unbound")


def _context_from_issued(context: VerifiedCompilationContext) -> dict[str, Any]:
    if not isinstance(context, VerifiedCompilationContext) or context not in _ISSUED_CONTEXTS:
        _fail("DG_IDENTITY_CONTEXT_STALE", "compilation_context")
    value = _parse(context._context_bytes, "compilation_context", "DG_COMPILATION_CONTEXT_INVALID")
    evidence = _parse(context._evidence_bytes, "allocator_evidence", "DG_ALLOCATOR_EVIDENCE_INVALID")
    _verify_allocator_evidence(value, evidence)
    return value


def _exact(value: Any, fields: set[str], path: str, code: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        _fail(code, path, f"expected exactly {sorted(fields)}")
    return value


def _array(value: Any, path: str, code: str, *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list) or (nonempty and not value):
        _fail(code, path, "expected array" + (" with at least one member" if nonempty else ""))
    return value


def _text(value: Any, path: str, code: str, *, key: bool = False) -> str:
    if not isinstance(value, str) or not value or (key and not _KEY.fullmatch(value)):
        _fail(code, path, "invalid key" if key else "expected non-empty string")
    return value


def _boolean(value: Any, path: str, code: str) -> bool:
    if not isinstance(value, bool):
        _fail(code, path, "expected boolean")
    return value


def _positive_int(value: Any, path: str, code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        _fail(code, path, "expected positive integer")
    return value


def _validate_digest(value: Any, path: str, code: str) -> str:
    if not isinstance(value, str) or not _DIGEST.fullmatch(value):
        _fail(code, path, "expected lowercase qualified SHA-256 digest")
    return value


def _unique(values: list[Any], key, path: str, code: str = "DG_ID_COLLISION") -> None:
    seen: set[Any] = set()
    for position, value in enumerate(values):
        try:
            identity = key(value)
            duplicate = identity in seen
        except (KeyError, TypeError, AttributeError) as error:
            _fail(code, f"{path}[{position}]", f"invalid uniqueness key: {type(error).__name__}")
        if duplicate:
            _fail(code, f"{path}[{position}]", str(identity))
        try: seen.add(identity)
        except TypeError: _fail(code, f"{path}[{position}]", "unhashable uniqueness key")


def _limits(value: Any, path: str, code: str) -> dict[str, int]:
    result = _exact(value, set(_LIMIT_FIELDS), path, code)
    for field in _LIMIT_FIELDS:
        _positive_int(result[field], f"{path}.{field}", code)
    return result  # type: ignore[return-value]


def _versioned_ref(value: Any, path: str, code: str) -> dict[str, str]:
    result = _exact(value, {"name", "version", "digest"}, path, code)
    _text(result["name"], f"{path}.name", code)
    _text(result["version"], f"{path}.version", code)
    _validate_digest(result["digest"], f"{path}.digest", code)
    return result  # type: ignore[return-value]


class TrustedAllocatorContextGate:
    """The only constructor for the pure compiler's identity context."""

    @staticmethod
    def verify(
        raw: bytes | str,
        allocator_evidence: bytes | str,
        allocator_trust: bytes | str | None = None,
        consumed_evidence_ids: set[str] | None = None,
    ) -> VerifiedCompilationContext:
        value = _parse(raw, "compilation_context", "DG_COMPILATION_CONTEXT_INVALID")
        if value.get("allocation_status") != "reserved": _fail("DG_IDENTITY_CONTEXT_STALE", "compilation_context")
        _validate_structure("compilation_context", value, "DG_COMPILATION_CONTEXT_INVALID", "compilation_context")
        match = _REVISION.fullmatch(value["revision"]) if isinstance(value["revision"], str) else None
        prior = value["prior_accepted_graph_digest"]
        if match is None or ((int(match.group(1)) == 1) != (prior is None)):
            _fail("DG_COMPILATION_CONTEXT_INVALID", "compilation_context.revision")
        evidence = _parse(allocator_evidence, "allocator_evidence", "DG_ALLOCATOR_EVIDENCE_INVALID")
        trust = None if allocator_trust is None else _parse(allocator_trust, "allocator_trust", "DG_ALLOCATOR_TRUST_INVALID")
        _verify_allocator_evidence(value, evidence, trust, consumed_evidence_ids)
        context_bytes = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        evidence_bytes = json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return _issue_context(context_bytes, evidence_bytes)


def _validate_draft(value: dict[str, Any]) -> None:
    code = "DG_DRAFT_SCHEMA_INVALID"
    _exact(value, {"schema", "objective", "resources", "requested_global_limits", "nodes", "edges", "lifecycle"}, "draft", code)
    if value["schema"] != "aci.draft-graph@1": _fail(code, "draft.schema")
    objective = _exact(value["objective"], {"statement", "done_when"}, "objective", code)
    _text(objective["statement"], "objective.statement", code)
    for i, member in enumerate(_array(objective["done_when"], "objective.done_when", code, nonempty=True)):
        _text(member, f"objective.done_when[{i}]", code)
    bindings = _array(value["resources"], "resources", code)
    for i, binding in enumerate(bindings):
        binding = _exact(binding, {"alias", "resource_key"}, f"resources[{i}]", code)
        _text(binding["alias"], f"resources[{i}].alias", code, key=True)
        _text(binding["resource_key"], f"resources[{i}].resource_key", code, key=True)
    _limits(value["requested_global_limits"], "requested_global_limits", code)
    nodes = _array(value["nodes"], "nodes", code, nonempty=True)
    node_fields = {"key", "objective", "instructions", "agent_request", "capability_requests", "inputs", "outputs", "requested_limits", "access_request", "start_when", "validation", "success_condition", "stop_conditions"}
    for n, node_value in enumerate(nodes):
        base = f"nodes[{n}]"; node = _exact(node_value, node_fields, base, code)
        _text(node["key"], f"{base}.key", code, key=True); _text(node["objective"], f"{base}.objective", code); _text(node["instructions"], f"{base}.instructions", code)
        agent = _exact(node["agent_request"], {"role", "provider_key", "model_key", "profile_key", "credential_key"}, f"{base}.agent_request", code)
        for field in ("role", "provider_key", "model_key", "profile_key"):
            _text(agent[field], f"{base}.agent_request.{field}", code, key=True)
        if agent["credential_key"] is not None: _text(agent["credential_key"], f"{base}.agent_request.credential_key", code, key=True)
        capabilities = _array(node["capability_requests"], f"{base}.capability_requests", code)
        for i, request in enumerate(capabilities):
            request = _exact(request, {"capability_key", "operations"}, f"{base}.capability_requests[{i}]", code)
            _text(request["capability_key"], f"{base}.capability_requests[{i}].capability_key", code, key=True)
            operations = _array(request["operations"], f"{base}.capability_requests[{i}].operations", code, nonempty=True)
            for j, operation in enumerate(operations): _text(operation, f"{base}.capability_requests[{i}].operations[{j}]", code, key=True)
            _unique(operations, lambda item: item, f"{base}.capability_requests[{i}].operations", code)
        inputs = _array(node["inputs"], f"{base}.inputs", code)
        for i, item_value in enumerate(inputs):
            path = f"{base}.inputs[{i}]"; item = _exact(item_value, {"key", "required", "source"}, path, code)
            _text(item["key"], f"{path}.key", code, key=True); _boolean(item["required"], f"{path}.required", code)
            source = item["source"]
            if isinstance(source, dict) and source.get("kind") == "resource":
                source = _exact(source, {"kind", "resource_alias", "selector"}, f"{path}.source", code)
                _text(source["resource_alias"], f"{path}.source.resource_alias", code, key=True); _text(source["selector"], f"{path}.source.selector", code)
            elif isinstance(source, dict) and source.get("kind") == "node_output":
                source = _exact(source, {"kind", "node_key", "output_key"}, f"{path}.source", code)
                _text(source["node_key"], f"{path}.source.node_key", code, key=True); _text(source["output_key"], f"{path}.source.output_key", code, key=True)
            else: _fail(code, f"{path}.source")
        outputs = _array(node["outputs"], f"{base}.outputs", code, nonempty=True)
        for i, output_value in enumerate(outputs):
            path = f"{base}.outputs[{i}]"; output = _exact(output_value, {"key", "contract_resource_alias", "required"}, path, code)
            _text(output["key"], f"{path}.key", code, key=True); _text(output["contract_resource_alias"], f"{path}.contract_resource_alias", code, key=True); _boolean(output["required"], f"{path}.required", code)
        _limits(node["requested_limits"], f"{base}.requested_limits", code)
        access = _exact(node["access_request"], {"read_paths", "write_paths", "network", "commands", "external_effects", "version_control"}, f"{base}.access_request", code)
        for field in ("read_paths", "write_paths"):
            members = _array(access[field], f"{base}.access_request.{field}", code)
            for i, member in enumerate(members):
                if not isinstance(member, str) or not member.startswith("workspace:/") or "\n" in member or "\r" in member: _fail(code, f"{base}.access_request.{field}[{i}]")
            _unique(members, lambda item: item, f"{base}.access_request.{field}", code)
        for field in ("network", "external_effects"):
            allow = _exact(access[field], {"mode", "allow"}, f"{base}.access_request.{field}", code)
            if allow["mode"] not in {"deny", "allowlist"}: _fail(code, f"{base}.access_request.{field}.mode")
            members = _array(allow["allow"], f"{base}.access_request.{field}.allow", code)
            for i, member in enumerate(members): _text(member, f"{base}.access_request.{field}.allow[{i}]", code)
            _unique(members, lambda item: item, f"{base}.access_request.{field}.allow", code)
            if allow["mode"] == "deny" and members: _fail(code, f"{base}.access_request.{field}.allow")
        commands = _exact(access["commands"], {"mode", "grants"}, f"{base}.access_request.commands", code)
        if commands != {"mode": "deny", "grants": []}: _fail(code, f"{base}.access_request.commands")
        vcs = _exact(access["version_control"], {"commit", "push"}, f"{base}.access_request.version_control", code)
        _boolean(vcs["commit"], f"{base}.access_request.version_control.commit", code); _boolean(vcs["push"], f"{base}.access_request.version_control.push", code)
        if node["start_when"] not in {"roots_ready", "all_predecessors_succeeded", "any_predecessor_succeeded"}: _fail(code, f"{base}.start_when")
        rules = _array(node["validation"], f"{base}.validation", code, nonempty=True)
        for i, rule_value in enumerate(rules):
            path = f"{base}.validation[{i}]"; rule = _exact(rule_value, {"key", "validator_key", "configuration_resource_alias", "on_fail"}, path, code)
            _text(rule["key"], f"{path}.key", code, key=True); _text(rule["validator_key"], f"{path}.validator_key", code, key=True)
            if rule["configuration_resource_alias"] is not None: _text(rule["configuration_resource_alias"], f"{path}.configuration_resource_alias", code, key=True)
            if rule["on_fail"] not in {"retry", "stop_node", "stop_graph"}: _fail(code, f"{path}.on_fail")
        _validate_predicate(node["success_condition"], f"{base}.success_condition", code, success=True)
        stops = _array(node["stop_conditions"], f"{base}.stop_conditions", code, nonempty=True)
        for i, stop_value in enumerate(stops):
            path = f"{base}.stop_conditions[{i}]"; stop = _exact(stop_value, {"when", "action", "reason_code"}, path, code)
            _validate_predicate(stop["when"], f"{path}.when", code, success=False)
            if stop["action"] not in {"stop_node", "stop_graph", "fail_graph"}: _fail(code, f"{path}.action")
            _text(stop["reason_code"], f"{path}.reason_code", code, key=True)
        for field, members in (("inputs", inputs), ("outputs", outputs), ("validation", rules)):
            _unique(members, lambda item: item["key"], f"{base}.{field}")
        _unique(capabilities, lambda item: item["capability_key"], f"{base}.capability_requests")
    edges = _array(value["edges"], "edges", code)
    for i, edge_value in enumerate(edges):
        path = f"edges[{i}]"; edge = _exact(edge_value, {"key", "from_node_key", "to_node_key", "kind", "condition"}, path, code)
        for field in ("key", "from_node_key", "to_node_key"): _text(edge[field], f"{path}.{field}", code, key=True)
        if edge["kind"] not in {"control", "feedback"}: _fail(code, f"{path}.kind")
        if edge["condition"] not in {"always", "on_success", "on_failure"}: _fail(code, f"{path}.condition")
    lifecycle = _exact(value["lifecycle"], {"entry_node_keys", "terminal_node_keys", "completion", "failure", "cancellation", "max_parallel_nodes"}, "lifecycle", code)
    for field in ("entry_node_keys", "terminal_node_keys"):
        members = _array(lifecycle[field], f"lifecycle.{field}", code, nonempty=True)
        for i, member in enumerate(members): _text(member, f"lifecycle.{field}[{i}]", code, key=True)
        _unique(members, lambda item: item, f"lifecycle.{field}", code)
    if lifecycle["completion"] not in {"all_terminal_succeeded", "any_terminal_succeeded"}: _fail(code, "lifecycle.completion")
    if lifecycle["failure"] not in {"fail_fast", "complete_independent_branches"}: _fail(code, "lifecycle.failure")
    if lifecycle["cancellation"] not in {"cancel_running_nodes", "allow_running_nodes_to_stop"}: _fail(code, "lifecycle.cancellation")
    _positive_int(lifecycle["max_parallel_nodes"], "lifecycle.max_parallel_nodes", code)
    _unique(bindings, lambda item: item["alias"], "resources"); _unique(bindings, lambda item: item["resource_key"], "resources", "DG_RESOURCE_BINDING_CONFLICT")
    _unique(nodes, lambda item: item["key"], "nodes"); _unique(edges, lambda item: item["key"], "edges")


def _validate_predicate(value: Any, path: str, code: str, *, success: bool) -> None:
    if not isinstance(value, dict): _fail(code, path)
    kind = value.get("kind")
    if kind == "output_present":
        _exact(value, {"kind", "output_key"}, path, code); _text(value["output_key"], f"{path}.output_key", code, key=True)
    elif kind == "output_field_equals":
        _exact(value, {"kind", "output_key", "json_pointer", "value"}, path, code); _text(value["output_key"], f"{path}.output_key", code, key=True)
        if not isinstance(value["json_pointer"], str) or not value["json_pointer"].startswith("/"): _fail(code, f"{path}.json_pointer")
        scalar = value["value"]
        if isinstance(scalar, float) or not (scalar is None or isinstance(scalar, (str, int, bool))): _fail(code, f"{path}.value")
    elif not success and kind == "input_unavailable":
        _exact(value, {"kind", "input_key"}, path, code); _text(value["input_key"], f"{path}.input_key", code, key=True)
    elif not success and kind == "attempts_exhausted":
        _exact(value, {"kind"}, path, code)
    else: _fail(code, path)


def _validate_policy(value: dict[str, Any]) -> None:
    code = "DG_POLICY_SCHEMA_INVALID"
    fields = {"schema", "semantics_key", "unknown_key_action", "numeric_limit_excess_action", "permission_excess_action", "global_limit_ceiling", "node_limit_ceiling", "allowed_agent_bindings", "capability_grants", "allowed_validator_keys", "access_ceiling", "audit_requirements"}
    _exact(value, fields, "policy", code)
    if value["schema"] != "aci.compilation-policy-fixture@1" or value["unknown_key_action"] != "reject" or value["permission_excess_action"] != "reject" or value["numeric_limit_excess_action"] not in {"restrict", "reject"}: _fail(code, "policy")
    _text(value["semantics_key"], "policy.semantics_key", code, key=True); _limits(value["global_limit_ceiling"], "policy.global_limit_ceiling", code); _limits(value["node_limit_ceiling"], "policy.node_limit_ceiling", code)
    bindings = _array(value["allowed_agent_bindings"], "policy.allowed_agent_bindings", code)
    for i, row in enumerate(bindings):
        row = _exact(row, {"role", "provider_key", "model_key", "profile_key", "credential_key"}, f"policy.allowed_agent_bindings[{i}]", code)
        for field in ("role", "provider_key", "model_key", "profile_key"): _text(row[field], f"policy.allowed_agent_bindings[{i}].{field}", code, key=True)
        if row["credential_key"] is not None: _text(row["credential_key"], f"policy.allowed_agent_bindings[{i}].credential_key", code, key=True)
    grants = _array(value["capability_grants"], "policy.capability_grants", code)
    for i, row in enumerate(grants):
        row = _exact(row, {"capability_key", "allowed_operations"}, f"policy.capability_grants[{i}]", code); _text(row["capability_key"], f"policy.capability_grants[{i}].capability_key", code, key=True)
        operations = _array(row["allowed_operations"], f"policy.capability_grants[{i}].allowed_operations", code)
        for j, operation in enumerate(operations): _text(operation, f"policy.capability_grants[{i}].allowed_operations[{j}]", code, key=True)
        _unique(operations, lambda item: item, f"policy.capability_grants[{i}].allowed_operations", code)
    validators = _array(value["allowed_validator_keys"], "policy.allowed_validator_keys", code)
    for i, key in enumerate(validators): _text(key, f"policy.allowed_validator_keys[{i}]", code, key=True)
    _unique(validators, lambda item: item, "policy.allowed_validator_keys", code)
    access = _exact(value["access_ceiling"], {"read_paths", "write_paths", "network", "commands", "external_effects", "version_control"}, "policy.access_ceiling", code)
    for field in ("read_paths", "write_paths"):
        members = _array(access[field], f"policy.access_ceiling.{field}", code); _unique(members, lambda item: item, f"policy.access_ceiling.{field}", code)
        for i, member in enumerate(members): _text(member, f"policy.access_ceiling.{field}[{i}]", code)
    for field in ("network", "external_effects"):
        row = _exact(access[field], {"mode", "allow"}, f"policy.access_ceiling.{field}", code)
        if row["mode"] not in {"deny", "allowlist"}: _fail(code, f"policy.access_ceiling.{field}.mode")
        members = _array(row["allow"], f"policy.access_ceiling.{field}.allow", code); _unique(members, lambda item: item, f"policy.access_ceiling.{field}.allow", code)
        if row["mode"] == "deny" and members: _fail(code, f"policy.access_ceiling.{field}.allow")
    commands = _exact(access["commands"], {"mode", "command_keys"}, "policy.access_ceiling.commands", code)
    if commands != {"mode": "deny", "command_keys": []}: _fail(code, "policy.access_ceiling.commands")
    vcs = _exact(access["version_control"], {"commit", "push"}, "policy.access_ceiling.version_control", code); _boolean(vcs["commit"], "policy.access_ceiling.version_control.commit", code); _boolean(vcs["push"], "policy.access_ceiling.version_control.push", code)
    audit = _exact(value["audit_requirements"], {"record_objective", "record_agents", "record_route", "record_results", "receipt_schema_resource_key"}, "policy.audit_requirements", code)
    for field in ("record_objective", "record_agents", "record_route", "record_results"):
        _boolean(audit[field], f"policy.audit_requirements.{field}", code)
        if audit[field] is not True: _fail(code, f"policy.audit_requirements.{field}")
    _text(audit["receipt_schema_resource_key"], "policy.audit_requirements.receipt_schema_resource_key", code, key=True)
    _unique(bindings, lambda row: tuple(row[field] for field in ("role", "provider_key", "model_key", "profile_key", "credential_key")), "policy.allowed_agent_bindings", code)
    _unique(grants, lambda row: row["capability_key"], "policy.capability_grants", code)


def _validate_catalog(value: dict[str, Any]) -> None:
    code = "DG_CATALOG_SCHEMA_INVALID"
    tables = ("semantics", "providers", "models", "profiles", "capabilities", "validators", "credentials")
    _exact(value, {"schema", *tables}, "catalog", code)
    if value["schema"] != "aci.compilation-catalog-fixture@1": _fail(code, "catalog.schema")
    for table in tables:
        rows = _array(value[table], f"catalog.{table}", code)
        for i, row_value in enumerate(rows):
            path = f"catalog.{table}[{i}]"; row = row_value
            if table in {"semantics", "providers", "validators"}:
                row = _exact(row, {"key", "ref", "digest_source"}, path, code); _versioned_ref(row["ref"], f"{path}.ref", code)
            elif table == "models":
                row = _exact(row, {"key", "provider_key", "ref", "digest_source"}, path, code); _text(row["provider_key"], f"{path}.provider_key", code, key=True); _versioned_ref(row["ref"], f"{path}.ref", code)
            elif table == "profiles":
                row = _exact(row, {"key", "provider_key", "model_key", "ref", "digest_source"}, path, code); _text(row["provider_key"], f"{path}.provider_key", code, key=True); _text(row["model_key"], f"{path}.model_key", code, key=True); _versioned_ref(row["ref"], f"{path}.ref", code)
            elif table == "capabilities":
                row = _exact(row, {"key", "operations", "tool_ref", "digest_source"}, path, code); operations = _array(row["operations"], f"{path}.operations", code, nonempty=True)
                for j, operation in enumerate(operations): _text(operation, f"{path}.operations[{j}]", code, key=True)
                _unique(operations, lambda item: item, f"{path}.operations", code); _versioned_ref(row["tool_ref"], f"{path}.tool_ref", code)
            else:
                row = _exact(row, {"key", "credential_ref", "digest_source"}, path, code)
                credential = _exact(row["credential_ref"], {"handle", "resolver_ref", "contract_version", "scope_digest"}, f"{path}.credential_ref", code); _text(credential["handle"], f"{path}.credential_ref.handle", code); _versioned_ref(credential["resolver_ref"], f"{path}.credential_ref.resolver_ref", code); _text(credential["contract_version"], f"{path}.credential_ref.contract_version", code); _validate_digest(credential["scope_digest"], f"{path}.credential_ref.scope_digest", code)
            _text(row["key"], f"{path}.key", code, key=True); _text(row["digest_source"], f"{path}.digest_source", code)
        _unique(rows, lambda item: item["key"], f"catalog.{table}", "DG_AMBIGUOUS_REFERENCE")


def _validate_resources(value: dict[str, Any]) -> None:
    code = "DG_RESOURCE_SCHEMA_INVALID"
    _exact(value, {"schema", "resources"}, "resources", code)
    if value["schema"] != "aci.compilation-resource-fixture@1": _fail(code, "resources.schema")
    rows = _array(value["resources"], "resources.resources", code)
    for i, row_value in enumerate(rows):
        path = f"resources.resources[{i}]"
        row = _exact(row_value, {"resource_key", "kind", "media_type", "encoding", "content", "digest"}, path, code)
        if row["encoding"] not in {"utf-8", "base64"}: _fail(code, f"{path}.encoding")
        if not isinstance(row["content"], str): _fail(code, f"{path}.content")
        _text(row["resource_key"], f"{path}.resource_key", code, key=True); _text(row["kind"], f"{path}.kind", code); _text(row["media_type"], f"{path}.media_type", code)
        if row["kind"] not in {"context", "schema", "policy", "input"}: _fail(code, f"{path}.kind")
        _validate_digest(row["digest"], f"{path}.digest", code)
    _unique(rows, lambda item: item["resource_key"], "resources.resources", "DG_AMBIGUOUS_REFERENCE")


def _accepted_roles(raw: bytes | str, expected_ref: dict[str, Any]) -> set[str]:
    value = _parse(raw, "role_registry", "DG_ROLE_REGISTRY_SCHEMA_INVALID")
    if set(value) != {"schema", "name", "version", "roles"} or value.get("schema") != "aci.role-registry@1":
        _fail("DG_ROLE_REGISTRY_SCHEMA_INVALID", "role_registry")
    try:
        raw_bytes = raw if isinstance(raw, bytes) else raw.encode("utf-8")
    except UnicodeEncodeError:
        _fail("DG_ROLE_REGISTRY_SCHEMA_INVALID", "role_registry")
    actual_ref = {"name": value.get("name"), "version": value.get("version"), "digest": "sha256:" + hashlib.sha256(raw_bytes).hexdigest()}
    if actual_ref != expected_ref:
        _fail("DG_ROLE_REGISTRY_REF_DRIFT", "compilation_context.role_registry_ref")
    rows = value.get("roles")
    if not isinstance(rows, list) or not rows:
        _fail("DG_ROLE_REGISTRY_SCHEMA_INVALID", "role_registry.roles")
    result: set[str] = set()
    for index, row in enumerate(rows):
        path = f"role_registry.roles[{index}]"
        if not isinstance(row, dict) or set(row) != {"role_id", "enabled", "purpose"}:
            _fail("DG_ROLE_REGISTRY_SCHEMA_INVALID", path)
        role = row.get("role_id")
        if not isinstance(role, str) or not _KEY.fullmatch(role):
            _fail("DG_ROLE_REGISTRY_SCHEMA_INVALID", path + ".role_id")
        if role in result:
            _fail("DG_ROLE_REGISTRY_DUPLICATE", path + ".role_id")
        if row.get("enabled") is not True:
            _fail("DG_ROLE_REGISTRY_DISABLED", path + ".enabled")
        _text(row.get("purpose"), path + ".purpose", "DG_ROLE_REGISTRY_SCHEMA_INVALID")
        result.add(role)
    return result


def _normalized_pool(raw: bytes | str, expected_ref: dict[str, Any], accepted_roles: set[str]) -> dict[str, dict[str, Any]]:
    value = _parse(raw, "agent_pool", "DG_POOL_SCHEMA_INVALID")
    if set(value) != {"schema", "name", "version", "agents"} or value.get("schema") != "aci.normalized-agent-pool@1":
        _fail("DG_POOL_SCHEMA_INVALID", "agent_pool")
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    actual_ref = {"name": value.get("name"), "version": value.get("version"), "digest": "sha256:" + hashlib.sha256(canonical).hexdigest()}
    if actual_ref != expected_ref:
        _fail("DG_AGENT_POOL_REF_DRIFT", "compilation_context.agent_pool_ref")
    rows = value.get("agents")
    if not isinstance(rows, list) or not rows:
        _fail("DG_POOL_SCHEMA_INVALID", "agent_pool.agents")
    result: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        path = f"agent_pool.agents[{index}]"
        if not isinstance(row, dict) or set(row) != {"display_name", "role_fit"}:
            _fail("DG_POOL_SCHEMA_INVALID", path)
        name = row.get("display_name")
        if not isinstance(name, str) or not name:
            _fail("DG_POOL_NAME_EMPTY", path + ".display_name")
        if name in result:
            _fail("DG_POOL_DUPLICATE_NAME", path + ".display_name")
        fits = row.get("role_fit")
        if not isinstance(fits, list) or not fits or len(fits) != len(set(fits)) or any(role not in accepted_roles for role in fits):
            _fail("DG_ROLE_UNKNOWN", path + ".role_fit")
        result[name] = row
    return result


def _index(rows: list[dict[str, Any]], key: str = "key") -> dict[str, dict[str, Any]]:
    return {row[key]: row for row in rows}


def _lookup(table: dict[str, Any], key: str, path: str) -> Any:
    if key not in table: _fail("DG_UNKNOWN_REFERENCE", path)
    return table[key]


def _check_resource_digest(resource: dict[str, Any], path: str) -> None:
    if "content" not in resource:
        return
    try:
        raw = resource["content"].encode("utf-8") if resource["encoding"] == "utf-8" else base64.b64decode(resource["content"], validate=True)
    except (UnicodeError, ValueError) as error:
        _fail("DG_RESOURCE_SCHEMA_INVALID", path, str(error))
    actual = "sha256:" + hashlib.sha256(raw).hexdigest()
    if actual != resource["digest"]: _fail("DG_RESOURCE_DIGEST_MISMATCH", path)


def _decode_pointer_token(token: str, path: str) -> str:
    result = ""; position = 0
    while position < len(token):
        if token[position] != "~": result += token[position]; position += 1; continue
        if position + 1 >= len(token) or token[position + 1] not in {"0", "1"}: _fail("DG_PREDICATE_POINTER_INVALID", path)
        result += "~" if token[position + 1] == "0" else "/"; position += 2
    return result


def _resolve_pointer(schema: dict[str, Any], pointer: str, path: str) -> dict[str, Any]:
    current: Any = schema
    for raw in pointer[1:].split("/"):
        token = _decode_pointer_token(raw, path)
        if not isinstance(current, dict) or set(current) & _UNPROVABLE_SCHEMA_KEYS: _fail("DG_PREDICATE_POINTER_UNPROVABLE", path)
        if current.get("type") == "object":
            properties = current.get("properties")
            if not isinstance(properties, dict) or token not in properties: _fail("DG_PREDICATE_POINTER_INVALID", path)
            if token not in current.get("required", []): _fail("DG_PREDICATE_POINTER_UNPROVABLE", path)
            current = properties[token]
        elif current.get("type") == "array":
            if not token.isdigit() or (token != "0" and token.startswith("0")): _fail("DG_PREDICATE_POINTER_INVALID", path)
            if not isinstance(current.get("items"), dict) or int(token) >= current.get("minItems", 0): _fail("DG_PREDICATE_POINTER_UNPROVABLE", path)
            current = current["items"]
        else: _fail("DG_PREDICATE_POINTER_UNPROVABLE", path)
    if not isinstance(current, dict) or set(current) & _UNPROVABLE_SCHEMA_KEYS or not set(current) & {"type", "const", "enum"}: _fail("DG_PREDICATE_POINTER_UNPROVABLE", path)
    return current


def _validate_predicate_semantics(predicate: dict[str, Any], output_schema: dict[str, Any], path: str) -> None:
    if predicate["kind"] != "output_field_equals": return
    subschema = _resolve_pointer(output_schema, predicate["json_pointer"], f"{path}.json_pointer")
    try: Draft202012Validator(subschema).validate(predicate["value"])
    except JsonSchemaValidationError: _fail("DG_PREDICATE_VALUE_INVALID", f"{path}.value")


def _closed_json_schema(resource: dict[str, Any], path: str) -> dict[str, Any]:
    if resource["kind"] != "schema" or "content" not in resource or resource.get("encoding") != "utf-8": _fail("DG_OUTPUT_CONTRACT_INVALID", path)
    def reject_schema_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            _reject_non_scalar_unicode(key, f"{path}.<member-name>", "DG_OUTPUT_CONTRACT_INVALID")
            if key in result: _fail("DG_OUTPUT_CONTRACT_INVALID", path, f"duplicate JSON key: {key}")
            result[key] = value
        return result
    try:
        schema = json.loads(
            resource["content"],
            object_pairs_hook=reject_schema_duplicates,
            parse_constant=lambda token: _fail("DG_OUTPUT_CONTRACT_INVALID", path, f"invalid JSON number: {token}"),
        )
        _reject_non_scalar_unicode(schema, path, "DG_OUTPUT_CONTRACT_INVALID")
        Draft202012Validator.check_schema(schema)
    except DraftGraphCompileError:
        raise
    except (json.JSONDecodeError, SchemaError, TypeError, ValueError) as error:
        _fail("DG_OUTPUT_CONTRACT_INVALID", path, str(error))
    if not isinstance(schema, dict) or schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        _fail("DG_OUTPUT_CONTRACT_INVALID", path)
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    if not isinstance(required, list) or not isinstance(properties, dict) or not set(required) <= set(properties):
        _fail("DG_OUTPUT_CONTRACT_INVALID", path)
    try:
        witness = _schema_witness(schema, path)
        Draft202012Validator(schema).validate(witness)
    except DraftGraphCompileError:
        raise
    except JsonSchemaValidationError as error:
        _fail("DG_OUTPUT_CONTRACT_INVALID", path, f"no mechanically proven witness: {error.message}")
    return schema


def _schema_witness(schema: Any, path: str) -> Any:
    """Build one witness for the deliberately small admitted contract subset."""
    if schema is False: _fail("DG_OUTPUT_CONTRACT_INVALID", path, "false schema is unsatisfiable")
    if schema is True: return None
    if not isinstance(schema, dict): _fail("DG_OUTPUT_CONTRACT_INVALID", path, "schema must be object or boolean")
    if set(schema) & _UNPROVABLE_SCHEMA_KEYS:
        _fail("DG_OUTPUT_CONTRACT_INVALID", path, "composite/ref schema is outside the satisfiable subset")
    if "const" in schema:
        candidate = schema["const"]
    elif "enum" in schema:
        if not schema["enum"]: _fail("DG_OUTPUT_CONTRACT_INVALID", path, "empty enum")
        candidate = schema["enum"][0]
    else:
        kind = schema.get("type")
        if kind == "object":
            if schema.get("additionalProperties") is not False: _fail("DG_OUTPUT_CONTRACT_INVALID", path, "object contracts must be closed")
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            if not isinstance(properties, dict) or not isinstance(required, list) or not set(required) <= set(properties): _fail("DG_OUTPUT_CONTRACT_INVALID", path)
            candidate = {key: _schema_witness(properties[key], f"{path}.properties.{key}") for key in required}
        elif kind == "array":
            items = schema.get("items", True)
            minimum = schema.get("minItems", 0)
            if isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 0: _fail("DG_OUTPUT_CONTRACT_INVALID", path)
            candidate = [_schema_witness(items, f"{path}.items") for _ in range(minimum)]
        elif kind == "string":
            minimum = schema.get("minLength", 0); candidate = "x" * minimum
        elif kind == "integer":
            candidate = int(schema.get("minimum", 0))
        elif kind == "boolean": candidate = False
        elif kind == "null": candidate = None
        elif kind is None:
            candidate = None
        elif isinstance(kind, list):
            if "null" in kind:
                candidate = None
            elif kind:
                candidate = _schema_witness({**schema, "type": kind[0]}, path)
            else:
                _fail("DG_OUTPUT_CONTRACT_INVALID", path, "empty type union")
        else:
            _fail("DG_OUTPUT_CONTRACT_INVALID", path, f"unsupported type {kind}")
    try: Draft202012Validator(schema).validate(candidate)
    except JsonSchemaValidationError as error: _fail("DG_OUTPUT_CONTRACT_INVALID", path, error.message)
    return candidate


def _effective_limits(draft: dict[str, Any], policy: dict[str, Any]) -> tuple[dict[str, int], list[dict[str, int]], list[dict[str, Any]]]:
    report: list[dict[str, Any]] = []
    def restrict(requested: dict[str, int], ceiling: dict[str, int], path: str) -> dict[str, int]:
        effective: dict[str, int] = {}
        for field in _LIMIT_FIELDS:
            if requested[field] > ceiling[field] and policy["numeric_limit_excess_action"] != "restrict": _fail("DG_LIMIT_DENIED", f"{path}.{field}")
            effective[field] = min(requested[field], ceiling[field])
            if effective[field] != requested[field]: report.append({"kind": "numeric_limit_restriction", "path": f"{path}.{field}", "requested": requested[field], "effective": effective[field], "policy_ceiling": ceiling[field]})
        return effective
    global_limits = restrict(draft["requested_global_limits"], policy["global_limit_ceiling"], "global_limits")
    node_limits = [restrict(node["requested_limits"], policy["node_limit_ceiling"], f"nodes[{node['key']}].limits") for node in draft["nodes"]]
    for field in _LIMIT_FIELDS:
        if sum(limits[field] for limits in node_limits) > global_limits[field]: _fail("DG_GLOBAL_BUDGET_EXCEEDED", f"global_limits.{field}")
    return global_limits, node_limits, report


def _map_predicate(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    if "output_key" in result: result["output_id"] = "output:" + result.pop("output_key")
    if "input_key" in result: result["input_id"] = "input:" + result.pop("input_key")
    return result


def _jcs_string(value: str) -> str:
    if any(0xD800 <= ord(member) <= 0xDFFF for member in value): _fail("DG_CANONICALIZATION_ERROR", "execution_graph", "lone surrogate")
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def canonicalize_execution_graph(value: Any) -> bytes:
    """RFC 8785 serialization for the closed EG domain (no binary numbers)."""
    _reject_non_scalar_unicode(value, "execution_graph", "DG_CANONICALIZATION_ERROR")
    def render(member: Any) -> str:
        if member is None: return "null"
        if member is True: return "true"
        if member is False: return "false"
        if isinstance(member, int) and not isinstance(member, bool):
            if abs(member) > 2**53 - 1: _fail("DG_CANONICALIZATION_ERROR", "execution_graph", "integer outside I-JSON exact range")
            return str(member)
        if isinstance(member, float): _fail("DG_CANONICALIZATION_ERROR", "execution_graph", "binary numbers are outside the admitted EG schema")
        if isinstance(member, str): return _jcs_string(member)
        if isinstance(member, list): return "[" + ",".join(render(item) for item in member) + "]"
        if isinstance(member, dict):
            if not all(isinstance(key, str) for key in member): _fail("DG_CANONICALIZATION_ERROR", "execution_graph", "non-string key")
            keys = sorted(member, key=lambda key: key.encode("utf-16-be"))
            return "{" + ",".join(_jcs_string(key) + ":" + render(member[key]) for key in keys) + "}"
        _fail("DG_CANONICALIZATION_ERROR", "execution_graph", type(member).__name__)
    return render(value).encode("utf-8")


def validate_execution_graph(graph: dict[str, Any]) -> None:
    """Semantic fail-closed validation run before graph bytes are emitted."""
    members = _index(graph.get("content_members", []), "member_id")
    if len(members) != len(graph.get("content_members", [])): _fail("DG_ID_COLLISION", "execution_graph.content_members")
    nodes = _index(graph.get("nodes", []), "node_id")
    if len(nodes) != len(graph.get("nodes", [])): _fail("DG_ID_COLLISION", "execution_graph.nodes")
    edge_ids = [edge.get("edge_id") for edge in graph.get("edges", [])]
    if len(edge_ids) != len(set(edge_ids)): _fail("DG_ID_COLLISION", "execution_graph.edges")
    for node in graph["nodes"]:
        inputs = _index(node["inputs"], "input_id"); outputs = _index(node["outputs"], "output_id")
        if len(inputs) != len(node["inputs"]) or len(outputs) != len(node["outputs"]): _fail("DG_ID_COLLISION", node["node_id"])
        output_schemas: dict[str, dict[str, Any]] = {}
        for output in node["outputs"]:
            member = members.get(output["schema_member_id"])
            if member is None: _fail("DG_UNKNOWN_REFERENCE", f"{node['node_id']}.outputs")
            output_schemas[output["output_id"]] = _closed_json_schema(member, output["schema_member_id"])
        success = node["success_condition"]
        if success.get("output_id") not in outputs or not outputs[success["output_id"]]["required"]: _fail("DG_TOPOLOGY_INVALID", f"{node['node_id']}.success_condition")
        _validate_predicate_semantics(success, output_schemas[success["output_id"]], f"{node['node_id']}.success_condition")
        for stop in node["stop_conditions"]:
            predicate = stop["when"]
            if "output_id" in predicate:
                if predicate["output_id"] not in outputs: _fail("DG_UNKNOWN_REFERENCE", f"{node['node_id']}.stop_conditions")
                _validate_predicate_semantics(predicate, output_schemas[predicate["output_id"]], f"{node['node_id']}.stop_conditions")
            if "input_id" in predicate and (predicate["input_id"] not in inputs or not inputs[predicate["input_id"]]["required"]): _fail("DG_TOPOLOGY_INVALID", f"{node['node_id']}.stop_conditions")
        for input_value in node["inputs"]:
            source = input_value["source"]
            if source["kind"] == "content_member" and source["member_id"] not in members: _fail("DG_UNKNOWN_REFERENCE", f"{node['node_id']}.inputs")
            if source["kind"] == "node_output" and (source["node_id"] not in nodes or source["output_id"] not in _index(nodes[source["node_id"]]["outputs"], "output_id")): _fail("DG_INPUT_WITHOUT_PRODUCER", f"{node['node_id']}.inputs")
    for edge in graph["edges"]:
        if edge["from_node_id"] not in nodes or edge["to_node_id"] not in nodes: _fail("DG_TOPOLOGY_INVALID", "execution_graph.edges")
    if not set(graph["lifecycle"]["entry_nodes"] + graph["lifecycle"]["terminal_nodes"]) <= set(nodes): _fail("DG_TOPOLOGY_INVALID", "execution_graph.lifecycle")
    receipt = graph["audit_requirements"]["receipt_schema_member_id"]
    for field in ("record_objective", "record_agents", "record_route", "record_results"):
        if graph["audit_requirements"].get(field) is not True: _fail("DG_COMPILATION_MISMATCH", f"execution_graph.audit_requirements.{field}")
    if receipt not in members: _fail("DG_UNKNOWN_REFERENCE", "execution_graph.audit_requirements.receipt_schema_member_id")
    _closed_json_schema(members[receipt], receipt)


def validate_compilation_match(expected: dict[str, Any], candidate: dict[str, Any]) -> None:
    """Reject candidate authority drift before canonicalization."""
    _reject_non_scalar_unicode(expected, "execution_graph", "DG_COMPILATION_MISMATCH")
    _reject_non_scalar_unicode(candidate, "execution_graph", "DG_COMPILATION_MISMATCH")
    if expected == candidate: return
    def counts(value: dict[str, Any]) -> tuple[int, ...]:
        nodes = value.get("nodes", [])
        return (len(nodes), len(value.get("edges", [])), *(sum(len(node.get(field, [])) for node in nodes) for field in ("tools", "inputs", "outputs", "validation", "stop_conditions")))
    expected_counts, candidate_counts = counts(expected), counts(candidate)
    if any(candidate > baseline for candidate, baseline in zip(candidate_counts, expected_counts)):
        _fail("DG_AUTHORITY_EXPANSION", "execution_graph")
    def authority_tokens(value: dict[str, Any]) -> set[tuple[Any, ...]]:
        tokens: set[tuple[Any, ...]] = set()
        for node in value.get("nodes", []):
            node_id = node.get("node_id")
            tokens.add(("node", node_id))
            for tool in node.get("tools", []):
                ref = tool.get("tool_ref", {})
                tokens.add(("tool", node_id, ref.get("digest"), tuple(tool.get("allowed_operations", []))))
            isolation = node.get("isolation", {})
            for field in ("read_paths", "write_paths"):
                tokens.update((field, node_id, member) for member in isolation.get(field, []))
            for field in ("network", "external_effects"):
                request = isolation.get(field, {})
                tokens.update((field, node_id, member) for member in request.get("allow", []))
            vcs = isolation.get("version_control", {})
            if vcs.get("commit"): tokens.add(("commit", node_id))
            if vcs.get("push"): tokens.add(("push", node_id))
            for grant in isolation.get("commands", {}).get("grants", []):
                tokens.add(("command", node_id, json.dumps(grant, sort_keys=True, separators=(",", ":"))))
        return tokens
    if authority_tokens(candidate) - authority_tokens(expected):
        _fail("DG_AUTHORITY_EXPANSION", "execution_graph")
    _fail("DG_COMPILATION_MISMATCH", "execution_graph")


class DraftGraphCompiler:
    """Compile seven frozen logical inputs; perform no I/O or state mutation."""

    def compile(
        self,
        context: VerifiedCompilationContext,
        draft_raw: bytes | str,
        policy_raw: bytes | str,
        catalog_raw: bytes | str,
        resources_raw: bytes | str,
        accepted_role_registry_raw: bytes | str,
        normalized_agent_pool_raw: bytes | str,
    ) -> CompilationResult:
        context_value = _context_from_issued(context)
        accepted_roles = _accepted_roles(accepted_role_registry_raw, context_value["role_registry_ref"])
        pool_by_name = _normalized_pool(normalized_agent_pool_raw, context_value["agent_pool_ref"], accepted_roles)
        draft = _parse(draft_raw, "draft", "DG_DRAFT_SCHEMA_INVALID"); policy = _parse(policy_raw, "policy", "DG_POLICY_SCHEMA_INVALID"); catalog = _parse(catalog_raw, "catalog", "DG_CATALOG_SCHEMA_INVALID"); resource_set = _parse(resources_raw, "resources", "DG_RESOURCE_SCHEMA_INVALID")
        for name, value, code, root in (
            ("draft", draft, "DG_DRAFT_SCHEMA_INVALID", "draft"),
            ("policy", policy, "DG_POLICY_SCHEMA_INVALID", "policy"),
            ("catalog", catalog, "DG_CATALOG_SCHEMA_INVALID", "catalog"),
            ("resources", resource_set, "DG_RESOURCE_SCHEMA_INVALID", "resources"),
        ):
            _validate_structure(name, value, code, root)
        _validate_draft(draft); _validate_policy(policy); _validate_catalog(catalog); _validate_resources(resource_set)
        resources = _index(resource_set["resources"], "resource_key")
        tables = {name: _index(catalog[name]) for name in ("semantics", "providers", "models", "profiles", "capabilities", "validators", "credentials")}
        for key, model in tables["models"].items(): _lookup(tables["providers"], model["provider_key"], f"catalog.models[{key}].provider_key")
        for key, profile in tables["profiles"].items():
            _lookup(tables["providers"], profile["provider_key"], f"catalog.profiles[{key}].provider_key")
            _lookup(tables["models"], profile["model_key"], f"catalog.profiles[{key}].model_key")
        for table_name, table in tables.items():
            for key, record in table.items():
                ref = record.get("ref") or record.get("tool_ref") or record.get("credential_ref", {}).get("resolver_ref")
                if ref is not None:
                    actual = "sha256:" + hashlib.sha256(record["digest_source"].encode("utf-8")).hexdigest()
                    if actual != ref["digest"]: _fail("DG_CATALOG_DIGEST_MISMATCH", f"catalog.{table_name}[{key}]")
        for key, resource in resources.items(): _check_resource_digest(resource, f"resources[{key}]")
        bindings = _index(draft["resources"], "alias")
        for alias, binding in bindings.items(): _lookup(resources, binding["resource_key"], f"resources[{alias}]")
        receipt_key = policy["audit_requirements"]["receipt_schema_resource_key"]
        receipt_resource = _lookup(resources, receipt_key, "policy.audit_requirements.receipt_schema_resource_key")
        _closed_json_schema(receipt_resource, f"resources[{receipt_key}]")
        receipt_alias = next((alias for alias, binding in bindings.items() if binding["resource_key"] == receipt_key), receipt_key)
        semantics = _lookup(tables["semantics"], policy["semantics_key"], "policy.semantics_key")
        global_limits, node_limits, report = _effective_limits(draft, policy)
        node_by_key = _index(draft["nodes"])
        assignments = context_value["agent_assignments"]
        assignment_by_node: dict[str, dict[str, Any]] = {}
        assigned_names: set[str] = set()
        for assignment in assignments:
            node_key = assignment["node_key"]
            path = f"compilation_context.agent_assignments.{node_key}"
            if node_key in assignment_by_node:
                _fail("DG_AGENT_ASSIGNMENT_DUPLICATE", path)
            if node_key not in node_by_key:
                _fail("DG_AGENT_ASSIGNMENT_EXTRA", path)
            display_name = assignment["display_name"]
            if display_name in assigned_names:
                _fail("DG_AGENT_REUSED", path + ".display_name")
            if display_name not in pool_by_name:
                _fail("DG_AGENT_ASSIGNMENT_UNKNOWN", path + ".display_name")
            assigned_names.add(display_name)
            assignment_by_node[node_key] = assignment
        if set(assignment_by_node) != set(node_by_key):
            _fail("DG_AGENT_ASSIGNMENT_MISSING", "compilation_context.agent_assignments")
        node_positions = {node["key"]: position for position, node in enumerate(draft["nodes"])}
        required_input_producers: dict[str, set[str]] = {key: set() for key in node_by_key}
        policy_capabilities = _index(policy["capability_grants"], "capability_key")
        allowed_agent_tuples = {tuple(row[field] for field in ("role", "provider_key", "model_key", "profile_key", "credential_key")) for row in policy["allowed_agent_bindings"]}
        output_schemas: dict[tuple[str, str], dict[str, Any]] = {}
        for node in draft["nodes"]:
            for output in node["outputs"]:
                alias = output["contract_resource_alias"]
                binding = _lookup(bindings, alias, f"nodes[{node['key']}].outputs[{output['key']}].contract_resource_alias")
                output_schemas[(node["key"], output["key"])] = _closed_json_schema(_lookup(resources, binding["resource_key"], f"resources[{alias}]"), f"resources[{alias}]")
        emitted_nodes: list[dict[str, Any]] = []
        dependency_pairs: list[tuple[str, str]] = []
        feedback_data_pairs: set[tuple[str, str]] = set()
        feedback_pairs = {(edge["from_node_key"], edge["to_node_key"]) for edge in draft["edges"] if edge["kind"] == "feedback"}
        feedback_targets = {target for _, target in feedback_pairs}
        for node, limits in zip(draft["nodes"], node_limits, strict=True):
            key = node["key"]; request = node["agent_request"]
            if request["role"] not in accepted_roles:
                _fail("DG_ROLE_UNKNOWN", f"nodes[{key}].agent_request.role")
            assignment = assignment_by_node[key]
            fits = request["role"] in pool_by_name[assignment["display_name"]]["role_fit"]
            override = assignment["role_fit_override"]
            reason = assignment["role_fit_override_reason"]
            if not fits and (override is not True or not isinstance(reason, str) or not reason):
                _fail("DG_ROLE_FIT_MISMATCH", f"compilation_context.agent_assignments.{key}")
            if fits and (override is not False or reason is not None):
                _fail("DG_ROLE_FIT_OVERRIDE_INVALID", f"compilation_context.agent_assignments.{key}")
            provider = _lookup(tables["providers"], request["provider_key"], f"nodes[{key}].agent_request.provider_key")
            model = _lookup(tables["models"], request["model_key"], f"nodes[{key}].agent_request.model_key")
            profile = _lookup(tables["profiles"], request["profile_key"], f"nodes[{key}].agent_request.profile_key")
            agent_tuple = tuple(request[field] for field in ("role", "provider_key", "model_key", "profile_key", "credential_key"))
            if agent_tuple not in allowed_agent_tuples: _fail("DG_AGENT_BINDING_DENIED", f"nodes[{key}].agent_request")
            if model["provider_key"] != request["provider_key"] or profile["provider_key"] != request["provider_key"] or profile["model_key"] != request["model_key"]: _fail("DG_AGENT_BINDING_DENIED", f"nodes[{key}].agent_request")
            credential = None if request["credential_key"] is None else _lookup(tables["credentials"], request["credential_key"], f"nodes[{key}].agent_request.credential_key")["credential_ref"]
            tools = []
            for capability in node["capability_requests"]:
                capability_key = capability["capability_key"]; path = f"nodes[{key}].capability_requests[{capability_key}]"
                record = _lookup(tables["capabilities"], capability_key, path); grant = _lookup(policy_capabilities, capability_key, path)
                if not set(capability["operations"]) <= set(record["operations"]) & set(grant["allowed_operations"]): _fail("DG_PERMISSION_DENIED", path)
                tools.append({"tool_ref": record["tool_ref"], "allowed_operations": capability["operations"]})
            access = node["access_request"]; ceiling = policy["access_ceiling"]
            for field in ("read_paths", "write_paths"):
                for position, member in enumerate(access[field]):
                    if member not in ceiling[field]: _fail("DG_PERMISSION_DENIED", f"nodes[{key}].access_request.{field}[{position}]")
            for field in ("network", "external_effects"):
                if access[field]["mode"] == "allowlist" and ceiling[field]["mode"] != "allowlist": _fail("DG_PERMISSION_DENIED", f"nodes[{key}].access_request.{field}")
                if not set(access[field]["allow"]) <= set(ceiling[field]["allow"]): _fail("DG_PERMISSION_DENIED", f"nodes[{key}].access_request.{field}.allow")
            if (access["version_control"]["commit"] and not ceiling["version_control"]["commit"]) or (access["version_control"]["push"] and not ceiling["version_control"]["push"]): _fail("DG_PERMISSION_DENIED", f"nodes[{key}].access_request.version_control")
            inputs = []
            for item in node["inputs"]:
                source = item["source"]
                if source["kind"] == "resource":
                    _lookup(bindings, source["resource_alias"], f"nodes[{key}].inputs[{item['key']}].source.resource_alias")
                    if source["selector"] != "$": _fail("DG_SELECTOR_UNSUPPORTED", f"nodes[{key}].inputs[{item['key']}].source.selector")
                    mapped = {"kind": "content_member", "member_id": "member:" + source["resource_alias"], "selector": source["selector"]}
                else:
                    producer_key = source["node_key"]
                    producer_outputs = _index(node_by_key[producer_key]["outputs"]) if producer_key in node_by_key else {}
                    if source["output_key"] not in producer_outputs: _fail("DG_INPUT_WITHOUT_PRODUCER", f"nodes[{key}].inputs[{item['key']}]")
                    if item["required"] and not producer_outputs[source["output_key"]]["required"]:
                        _fail("DG_TOPOLOGY_INVALID", f"nodes[{key}].inputs[{item['key']}].required", "required input needs a required producer output")
                    if node_positions[producer_key] >= node_positions[key]:
                        if (producer_key, key) not in feedback_pairs: _fail("DG_TOPOLOGY_INVALID", f"nodes[{key}].inputs[{item['key']}]")
                        if item["required"]: _fail("DG_TOPOLOGY_INVALID", f"nodes[{key}].inputs[{item['key']}].required", "feedback inputs must be optional for initial entry")
                        feedback_data_pairs.add((producer_key, key))
                    elif item["required"]:
                        required_input_producers[key].add(producer_key)
                    dependency_pairs.append((producer_key, key)); mapped = {"kind": "node_output", "node_id": "node:" + producer_key, "output_id": "output:" + source["output_key"]}
                inputs.append({"input_id": "input:" + item["key"], "required": item["required"], "source": mapped})
            outputs_by_key = _index(node["outputs"])
            success = node["success_condition"]
            if success["output_key"] not in outputs_by_key or not outputs_by_key[success["output_key"]]["required"]: _fail("DG_TOPOLOGY_INVALID", f"nodes[{key}].success_condition")
            _validate_predicate_semantics(success, output_schemas[(key, success["output_key"])], f"nodes[{key}].success_condition")
            inputs_by_key = _index(node["inputs"])
            for position, stop in enumerate(node["stop_conditions"]):
                predicate = stop["when"]
                if "output_key" in predicate:
                    if predicate["output_key"] not in outputs_by_key: _fail("DG_UNKNOWN_REFERENCE", f"nodes[{key}].stop_conditions[{position}]")
                    _validate_predicate_semantics(predicate, output_schemas[(key, predicate["output_key"])], f"nodes[{key}].stop_conditions[{position}].when")
                if "input_key" in predicate and (predicate["input_key"] not in inputs_by_key or not inputs_by_key[predicate["input_key"]]["required"]): _fail("DG_TOPOLOGY_INVALID", f"nodes[{key}].stop_conditions[{position}]")
                if predicate["kind"] == "attempts_exhausted" and stop["action"] not in {"stop_node", "fail_graph"}: _fail("DG_TOPOLOGY_INVALID", f"nodes[{key}].stop_conditions[{position}]")
            emitted_validation = []
            for rule in node["validation"]:
                validator = _lookup(tables["validators"], rule["validator_key"], f"nodes[{key}].validation[{rule['key']}].validator_key")
                if rule["validator_key"] not in policy["allowed_validator_keys"]: _fail("DG_PERMISSION_DENIED", f"nodes[{key}].validation[{rule['key']}]")
                alias = rule["configuration_resource_alias"]
                if alias is not None:
                    binding = _lookup(bindings, alias, f"nodes[{key}].validation[{rule['key']}].configuration_resource_alias")
                    _closed_json_schema(_lookup(resources, binding["resource_key"], f"resources[{alias}]"), f"resources[{alias}]")
                emitted_validation.append({"rule_id": "rule:" + rule["key"], "validator_ref": validator["ref"], "configuration_member_id": None if alias is None else "member:" + alias, "on_fail": rule["on_fail"]})
            emitted_nodes.append({"node_id": "node:" + key, "objective": node["objective"], "instructions": node["instructions"], "agent": {"display_name": assignment["display_name"], "role": request["role"], "provider_ref": provider["ref"], "model_ref": model["ref"], "profile_ref": profile["ref"], "credential_ref": credential}, "tools": tools, "inputs": inputs, "outputs": [{"output_id": "output:" + output["key"], "schema_member_id": "member:" + output["contract_resource_alias"], "required": output["required"]} for output in node["outputs"]], "limits": limits, "isolation": access, "start_when": node["start_when"], "validation": emitted_validation, "success_condition": _map_predicate(success), "stop_conditions": [{"when": _map_predicate(stop["when"]), "action": stop["action"], "reason_code": stop["reason_code"]} for stop in node["stop_conditions"]]})
        authored_edges = []
        for edge in draft["edges"]:
            if edge["from_node_key"] not in node_by_key or edge["to_node_key"] not in node_by_key: _fail("DG_TOPOLOGY_INVALID", f"edges[{edge['key']}]")
            authored_edges.append({"edge_id": "edge:" + edge["key"], "from_node_id": "node:" + edge["from_node_key"], "to_node_id": "node:" + edge["to_node_key"], "kind": edge["kind"], "condition": edge["condition"]})
        seen_pairs: set[tuple[str, str]] = set(); data_edges = []
        for pair in dependency_pairs:
            if pair not in seen_pairs:
                seen_pairs.add(pair); data_edges.append({"edge_id": f"edge:{pair[0]}:{pair[1]}:data", "from_node_id": "node:" + pair[0], "to_node_id": "node:" + pair[1], "kind": "data", "condition": "on_success"})
        all_edges = data_edges + authored_edges
        if len({edge["edge_id"] for edge in all_edges}) != len(all_edges): _fail("DG_ID_COLLISION", "edges")
        incoming = {key: set() for key in node_by_key}; outgoing = {key: set() for key in node_by_key}
        incoming_routes: dict[str, list[tuple[str, str]]] = {key: [] for key in node_by_key}
        for edge in all_edges:
            source = edge["from_node_id"][5:]; target = edge["to_node_id"][5:]
            if edge["kind"] != "feedback" and not (edge["kind"] == "data" and (source, target) in feedback_data_pairs):
                incoming[target].add(source); outgoing[source].add(target)
                incoming_routes[target].append((source, edge["condition"]))
        roots = [key for key in node_by_key if not incoming[key]]
        lifecycle = draft["lifecycle"]
        if lifecycle["entry_node_keys"] != roots: _fail("DG_TOPOLOGY_INVALID", "lifecycle.entry_node_keys")
        for key, node in node_by_key.items():
            if (key in roots) != (node["start_when"] == "roots_ready"): _fail("DG_TOPOLOGY_INVALID", f"nodes[{key}].start_when")
        reachable = set(roots); frontier = list(roots)
        while frontier:
            source = frontier.pop(0)
            for target in sorted(outgoing[source], key=node_positions.get):
                if target not in reachable: reachable.add(target); frontier.append(target)
        if reachable != set(node_by_key) or not set(lifecycle["terminal_node_keys"]) <= reachable: _fail("DG_TOPOLOGY_INVALID", "lifecycle")
        indegree = {key: len(incoming[key]) for key in node_by_key}; ready = [key for key in node_by_key if indegree[key] == 0]; ordered = []
        while ready:
            source = ready.pop(0); ordered.append(source)
            for target in sorted(outgoing[source], key=node_positions.get):
                indegree[target] -= 1
                if indegree[target] == 0: ready.append(target)
        if len(ordered) != len(node_by_key): _fail("DG_TOPOLOGY_INVALID", "edges")
        OutcomeState = tuple[frozenset[str], frozenset[str]]
        succeeded_states: dict[str, set[OutcomeState]] = {}
        failed_states: dict[str, set[OutcomeState]] = {}

        def bounded(states: set[OutcomeState], path: str) -> set[OutcomeState]:
            if len(states) > _TOPOLOGY_STATE_LIMIT:
                _fail("DG_TOPOLOGY_INVALID", path, "conditional readiness proof exceeds the closed state limit")
            return states

        def merge(left: OutcomeState, right: OutcomeState) -> OutcomeState | None:
            succeeded = left[0] | right[0]
            failed = left[1] | right[1]
            return None if succeeded & failed else (succeeded, failed)

        for key in ordered:
            if key in feedback_targets and required_input_producers[key]:
                _fail(
                    "DG_TOPOLOGY_INVALID",
                    f"nodes[{key}].start_when",
                    "feedback activation cannot prove required producer inputs in the initial state model",
                )
            routes = incoming_routes[key]
            if not routes:
                start_states: set[OutcomeState] = {(frozenset(), frozenset())}
            else:
                route_states: list[set[OutcomeState]] = []
                for source, condition in routes:
                    if condition == "on_success":
                        states = succeeded_states[source]
                    elif condition == "on_failure":
                        states = failed_states[source]
                    else:
                        states = succeeded_states[source] | failed_states[source]
                    route_states.append(states)
                if node_by_key[key]["start_when"] == "any_predecessor_succeeded":
                    start_states = bounded(set().union(*route_states), f"nodes[{key}].start_when")
                else:
                    start_states = {(frozenset(), frozenset())}
                    for states in route_states:
                        combined: set[OutcomeState] = set()
                        for left in start_states:
                            for right in states:
                                state = merge(left, right)
                                if state is not None:
                                    combined.add(state)
                                    if len(combined) > _TOPOLOGY_STATE_LIMIT:
                                        bounded(combined, f"nodes[{key}].start_when")
                        start_states = combined
                        if not start_states:
                            break
            if not start_states:
                _fail("DG_TOPOLOGY_INVALID", f"nodes[{key}].start_when", "join conditions are mutually unsatisfiable")
            must_available = set.intersection(*(set(state[0]) for state in start_states))
            missing = required_input_producers[key] - must_available
            if missing:
                _fail(
                    "DG_TOPOLOGY_INVALID",
                    f"nodes[{key}].start_when",
                    "some activating outcome lacks required producer inputs: "
                    + ",".join(sorted(missing, key=node_positions.get)),
                )
            succeeded_states[key] = bounded(
                {(state[0] | {key}, state[1]) for state in start_states},
                f"nodes[{key}].start_when",
            )
            failed_states[key] = bounded(
                {(state[0], state[1] | {key}) for state in start_states},
                f"nodes[{key}].start_when",
            )
        can_finish = set(lifecycle["terminal_node_keys"])
        can_finish.update(node["key"] for node in draft["nodes"] if any(stop["action"] in {"stop_graph", "fail_graph"} for stop in node["stop_conditions"]))
        changed = True
        while changed:
            changed = False
            for source, targets in outgoing.items():
                if source not in can_finish and targets & can_finish:
                    can_finish.add(source); changed = True
        if not reachable <= can_finish: _fail("DG_TOPOLOGY_INVALID", "lifecycle.terminal_node_keys")
        members = []
        for binding in draft["resources"]:
            resource = resources[binding["resource_key"]]
            members.append({"member_id": "member:" + binding["alias"], **{field: resource[field] for field in ("kind", "media_type", "encoding", "content", "digest")}})
        if receipt_alias == receipt_key and receipt_key not in {binding["resource_key"] for binding in draft["resources"]}:
            members.append({"member_id": "member:" + receipt_key, **{field: receipt_resource[field] for field in ("kind", "media_type", "encoding", "content", "digest")}})
        audit = policy["audit_requirements"]
        graph = {"schema": "aci.execution-graph@2", "dispatch_id": context_value["dispatch_id"], "revision": context_value["revision"], "objective": draft["objective"], "semantics_ref": semantics["ref"], "content_members": members, "global_limits": global_limits, "nodes": emitted_nodes, "edges": all_edges, "lifecycle": {"entry_nodes": ["node:" + key for key in lifecycle["entry_node_keys"]], "terminal_nodes": ["node:" + key for key in lifecycle["terminal_node_keys"]], "completion": lifecycle["completion"], "failure": lifecycle["failure"], "cancellation": lifecycle["cancellation"], "max_parallel_nodes": lifecycle["max_parallel_nodes"]}, "audit_requirements": {"record_objective": audit["record_objective"], "record_agents": audit["record_agents"], "record_route": audit["record_route"], "record_results": audit["record_results"], "receipt_schema_member_id": "member:" + receipt_alias}}
        _validate_structure("execution_graph", graph, "DG_COMPILATION_MISMATCH", "execution_graph")
        validate_execution_graph(graph)
        canonical = canonicalize_execution_graph(graph)
        report_bytes = tuple(canonicalize_execution_graph(item) for item in report)
        return CompilationResult(canonical, report_bytes)
