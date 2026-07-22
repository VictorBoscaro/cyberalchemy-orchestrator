---
feature: agents-communication-infra
review_date: 2026-07-21
scope: SWU-ACI-001
axis: canonical-contract-vectors
baseline_sha256: 35e54db2591fc2aa88f19345f91209e7ed99a379bf06dd3dc534daf78dfbf946
verdict: FIX
runtime_gate: block
---

# SWU-ACI-001 canonical-contract review

## Verdict: FIX

The baseline is intact and every supplied positive vector reproduces its declared UTF-8 byte
length and SHA-256. The contract is not yet acceptable because its normative digest rendering,
dependency pin and required golden coverage are internally incomplete.

## Material findings

1. **The fixture's normative digest representation contradicts the ADR.**
   [ADR-001 lines 273-274](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#6-pydantic-and-canonical-acceptance-bytes)
   requires `sha256:<lowercase 64-hex>`, while
   [`canonical-contract-vectors.json` line 21](../../adrs/fixtures/canonical-contract-vectors.json)
   specifies lowercase hexadecimal only and every `sha256` value (lines 46, 63, 84 and 99) omits
   the `sha256:` prefix. The future executable assertion in
   [`SWU-ACI-001-TEST-PLAN.md` line 25](../../adrs/fixtures/SWU-ACI-001-TEST-PLAN.md)
   therefore cannot prove the rendered digest contract. Make the fixture assert the exact rendered
   value, or explicitly separate a raw `sha256_hex` field from the normative prefixed digest and
   test both.

2. **The exact Pydantic pair is not frozen by the fixture/test contract.**
   ADR-001 lines 248-252 and 326 require exact `pydantic==2.13.4` and
   `pydantic-core==2.46.4` pins. The fixture lines 7-9 records only Pydantic's version and asks for a
   range plus a future lock, and the test plan lines 18-20 likewise says nothing about asserting the
   resolved `pydantic-core` version. The local host currently reports the intended pair, but that is
   not portable contract evidence. Record both exact expected versions and require an executable
   assertion for both before TASK-010.

3. **Required golden cases are missing from both the corpus and the named tests.**
   ADR-001 lines 276-278 explicitly requires schema-version change and integers including zero and
   negative values. Fixture lines 23-101 contain only `aci.contract@1`; no vector proves that a
   schema-version change changes the bytes/digest. The integer examples contain positive `7`, both
   signed extrema, but no JSON integer zero or `-0` normalization case; the only zero-normalization
   example is a decimal string. Test-plan lines 23-34 name no schema-version or integer-zero test.
   Add exact vectors and named assertions for those ADR-required cases.

4. **Five of six rejection vectors are fragments, not independently executable invalid inputs.**
   Fixture lines 102-108 provide `input_fragment` without a declared valid base input, schema/model,
   mutation operation or expected stable error code. A validator can therefore reject them first for
   missing required fields instead of the stated target invariant, so the future tests would not
   prove the claimed rejection cause. `R-ACI-CANON-005` is correctly preserved as raw JSON and does
   retain both pre-normalization keys. Give each other rejection a full input, or define a versioned
   valid base plus an unambiguous mutation and expected error identity.

## Independent verification receipt

| Check | Result |
|---|---|
| Four artifact hashes | Match BASELINE.md exactly |
| Review-set composition | Recomputed as `SHA256(UTF8(join(path=lowercase_sha256, LF)))` = `35e54db2591fc2aa88f19345f91209e7ed99a379bf06dd3dc534daf78dfbf946` |
| `V-ACI-CANON-001` | 135 bytes; `b95f58480e9f58c5d958023aa757c4f55dba7bdc1288fd05cd9a4f47d4ba3276` |
| `V-ACI-CANON-002` | 151 bytes; `8c41eaa6d528109a979fc175bdd33fb909ba071d85081b380b01f07115df9242` |
| `V-ACI-CANON-003` | 98 bytes; `3fae81e54e1c160267a63fadd01424eac2558c04764fdf00c323916582c3be95` |
| `V-ACI-CANON-004` | 150 bytes; `1f8856360b31e663eb65ed98a1cec145a6183a42a6b17395235554ebff37f63f` |
| Equivalent-input projection | Every supplied equivalent input independently canonicalized to its declared bytes |
| Omitted vs explicit null | Distinct bytes and digests, as required |
| NFC collision raw structure | Two raw key pairs retained; both normalize to one key |
| Test names | 26 names; 26 unique |
| Local Markdown file targets | 20 checked; none missing |

This review accepts no runtime claim and does not change `workPackGateStatus=block`.

## Closure review

### Verdict: PASS

Final baseline `d6093473703ce1cf21353dff785ad69f7aa38f253980adfbcc0e21ded1ec014f`
closes every material finding above with no residual finding:

- all four artifact hashes and the review-set composition match
  [`FINAL-BASELINE.md`](FINAL-BASELINE.md);
- all six canonical strings were independently projected from every supplied equivalent decoded or
  raw input, then re-encoded; their respective lengths are `135`, `151`, `98`, `150`, `135` and
  `44` bytes, and every recomputed SHA-256 matches its normative `sha256:<64 lowercase hex>` value;
- the fixture and test plan now freeze and assert both `pydantic==2.13.4` and
  `pydantic-core==2.46.4` rather than a compatible range or transitive resolution;
- `V-ACI-CANON-005` proves otherwise-equal `@1`/`@2` bodies have different canonical bytes and
  digests, while both raw inputs in `V-ACI-CANON-006` independently converge from integer `0` and
  `-0` to canonical integer `0`;
- all six rejection cases carry a complete duplicate-preserving `raw_json`, an existing versioned
  target-schema definition, and a stable expected stage/code; the NFC case retains both nested raw
  key pairs before normalization;
- the plan contains 28 unique executable test names. Its corpus-wide assertion and dedicated rows
  map all six positive vectors, all six rejection vectors, both exact dependency pins, schema
  identity and integer-zero behavior; all local Markdown file targets resolve.

This is acceptance of the W0 canonical contract artifacts only. It is not TASK-010 runtime evidence
and leaves `runtime_gate=block` unchanged.

## Final closure review

### Verdict: PASS

The later ADR, schema and test-plan changes introduce no vector regression. Final review-set digest
`70c2312b9ecd75bfa814ba9548fa11c3508b75a662fec42db3d29b71429b310b` and all four component
hashes exactly match [`FINAL-BASELINE.md`](FINAL-BASELINE.md).

- Independently projecting every supplied input still reproduces all six canonical byte strings.
  Their byte lengths remain `135`, `151`, `98`, `150`, `135` and `44`; all six recomputed digests
  match their literal `sha256:<64 lowercase hex>` assertions.
- The exact `pydantic==2.13.4` and `pydantic-core==2.46.4` target pins remain present in the fixture,
  test plan and ADR. Schema-version identity, omission/null, recursive ordering/NFC, int64 bounds,
  integer `0`/`-0`, decimals, timestamps and array-order coverage remain intact.
- The six rejection vectors remain complete raw inputs with an existing target schema and a stable
  expected stage/code. All six positive and all six rejection cases map to named plan assertions.
- The expanded plan has 45 test names and all 45 are unique. Twenty-three local Markdown targets
  were checked in the ADR and plan; none is missing.
- Claim calibration is explicit: W0 can accept the decision, SQL/canonical contract fixtures and
  downstream executable obligations, while dependency locking and every production/runtime result
  remain TASK-010 evidence. Accepting this review neither starts TASK-010 nor promotes the blocked
  work-pack/runtime gate.

No residual finding.
