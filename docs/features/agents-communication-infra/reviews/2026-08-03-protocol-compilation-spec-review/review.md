# Protocol Compilation Candidate v1 — normative review

- Date: 2026-08-03
- Scope: ACI-PG-001, promoted discoveries, `SPEC.md`, `protocol-compilation.md`, architecture,
  glossary, feature/aspect TEST-SPECs, frozen fixtures and LF checkout rule.
- Dispatch registration: none; the owner authorized direct independent subagent review.

## Verdict

PASS after correction cycles.

## Independent lenses

1. Authority and ownership: PASS. Protocol Governance terminates at canonical non-authoritative
   candidate/result; capability resolution, `DispatchSpec`, confirmation and runtime remain
   separate. Canonicalization ownership is scoped by responsible boundary.
2. Executable mechanics: PASS. Outer/document canonicality, schema and digest precedence are total;
   fixed compiler identity is testable; the package admits one compiled and one
   required-unsupported tuple before result construction; no third tuple or unreachable failure remains.
3. DomainSpec conformance: PASS after removing the invalid Mapping-to-Value-Object graph edge,
   removing the unreachable `inference_required` failure and making the exact `superseded`
   obligation mutation terminate at `fixture_not_admitted`.
4. Template closure: PASS. V1 rejects invocation string values containing `{{` or `}}` as
   `invalid_parameter_value` before admission, so recursive or second-pass substitution is
   impossible while the compiled fixture remains the plain `protocol ownership` case.

## Evidence checked

- All fourteen fixture raw and canonical SHA-256 values match the normative table and manifest.
- `.gitattributes` pins the fixture corpus to LF.
- Feature-wide and aspect-level T-ACI-PC1 through T-ACI-PC12 obligations agree.
- The package contains no candidate-to-confirmation/runtime wiring authorization.

This receipt accepts the normative package for bounded work-pack preparation. It is not an
implementation or conformance receipt.
