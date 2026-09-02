# Review — DraftGraph specification and compiler closeout

Date: 2026-09-01

- Pairing: independent reviewer for `/root/draftgraph_closeout_worker`
- Aggregate verdict: **KEEP**
- `recheck_required`: `false`
- Exit reason: `closeout_claims_match_current_bounded_evidence_no_finding_survived`
- Agents spawned by this reviewer: `0`

## Coverage

The user-required one-worker/one-reviewer topology replaces the multi-seat review topology for this
dispatch. This reviewer attacked the complete target corpus under each declared lens.

| reviewer | lens | targets attacked | findings raised | zero-findings defence |
|---|---|---|---:|---|
| `/root/draftgraph_closeout_reviewer` | fidelity / governance | `CLOSEOUT.md`; synchronized SPEC/IMPL records; final SPEC/IMPL reviews | 0 | Statuses remain bounded to a proposed DraftGraph and fixture-backed compiler. Canonical-v2 and runtime authority are explicitly excluded. |
| `/root/draftgraph_closeout_reviewer` | mechanics / correctness | compiler, tests, schemas, fixtures and four accepted checks | 0 | Fresh directed 22/22, adjacent 34/34, predecessor validation and `py_compile` all passed. The directed suite also proved embedded-schema digest correspondence. |
| `/root/draftgraph_closeout_reviewer` | ownership / reference integrity | review hashes, write scope, Git status/diff and synchronized records | 0 | Both declared review hashes are exact. The closeout distinguishes tracked requirements changes from untracked corpus location and does not use Git to claim historical authorship. |
| `/root/draftgraph_closeout_reviewer` | operability / residue | requirements, environment health and next-work boundary | 0 | Both direct dependencies are imported and exercised. `pip check` still fails and the records do not describe the environment as clean. Every requested residual boundary is named. |
| `/root/draftgraph_closeout_reviewer` | abuse / gaming | stale status/count scans and authority-expansion language | 0 | No stale 20/20, 21/21, 33/33, N01-N20, runtime-ready, production-ready or canonical-promotion claim survived the scans. |

Lens coverage is complete for every target named in the dispatch. The zero-findings result is not a
clean-worktree inference: it rests on exact review hashes, fresh checks, literal claim ceilings and
an explicit dirty-tree evidence boundary.

## Commands and results

| Check | Fresh result |
|---|---|
| `Get-FileHash -Algorithm SHA256` over both final reviews | SPEC `E70B8D68CC426BF9E5F64B6ADD37BE2867F9864AE76BCC4DED8B30D54B2F3D94`; IMPL `7083B3E20EC391826D36B3509D2E3F8F5958E6CD44AD18F8219EB8C428A13984`; both exactly match `CLOSEOUT.md`. |
| `python -m unittest implementations.tests.runtime.test_draft_graph_compiler -v` | exit `0`; 22/22 passed in 8.420s. |
| `python -m unittest implementations.tests.runtime.test_draft_graph_compiler implementations.tests.runtime.test_protocol_compilation -q` | exit `0`; 34/34 passed in 8.839s. |
| predecessor `validate_artifacts.py` | exit `0`; all declared checks passed, including F1-F6, R1-R2, S1 and 105/105 ownership leaves; it retained its no-compiler/no-live-allocator/no-RFC-8785 evidence limit. |
| `python -m py_compile ...draft_graph_compiler.py ...test_draft_graph_compiler.py` | exit `0`; no output. |
| `git diff --check` | exit `0`; only line-ending warnings, no whitespace error. |
| stale scans over the closeout and five synchronized records | no positive stale count/status/readiness match; the only historical-preexistence match is the explicit negation in IMPL `VALIDATION.md`. |
| `python -m pip check` | exit `1`; `python-bcb 0.2.0` conflicts with `httpx 0.27.0`; the invalid local Django distribution remains a warning. |
| dependency import/version check | `jsonschema 4.21.1`, `cryptography 49.0.0`; compiler directly uses `Draft202012Validator`, `Ed25519PublicKey` and `InvalidSignature`. |
| sensitive-path diff/status | `CRAFT.md` and `.craft/ledger.yml` are tracked-dirty; the original session and proposed v2 schema are untracked; canonical `specs/SPEC.md` and `TEST-SPEC.md` have no diff; the CRAFT/ledger diff contains no DraftGraph closeout/review/compiler markers. |

The current test durations differ from the recorded closeout durations, as expected. Counts and
outcomes agree; this review does not rewrite historical timing evidence.

## `CLOSEOUT.md`

No finding survived.

The artifact says:

> “This is an evidence synchronization closeout, not a new implementation or a canonical-v2
> promotion.” (`CLOSEOUT.md:5-6`)

> “All other SPEC+IMPL artifacts are currently untracked, so Git proves their present location but
> cannot prove historical authorship or distinguish individual edits within those directories.”
> (`CLOSEOUT.md:108-110`)

> “It does **not** support claims of” canonical promotion, general RFC 8785 compliance, projectors,
> confirmation `@2`, persistence, ingestion, scheduling, worker/provider/tool/credential execution,
> live allocator/key lifecycle, or production/runtime readiness. (`CLOSEOUT.md:140-149`)

Those quotations match the current repository evidence and prevent the bounded implementation from
being presented as runtime authority.

| # | file | evidence | severity | proposed fix |
|---|---|---|---|---|
| — | — | No surviving finding. | — | — |

**Verdict:** **KEEP**

## Synchronized SPEC records

No finding survived across `WORK-PACK.md`, `TASK-SESSION.md` and `VALIDATION.md`.

- `WORK-PACK.md:3-4` marks only the bounded implementation complete after dedicated `KEEP`.
- `WORK-PACK.md:76-80` keeps canonical promotion, projectors, confirmation `@2`, persistence,
  compatibility and runtime parser/scheduler/effects as non-goals.
- `TASK-SESSION.md:113-124` distinguishes the later fixture-backed compiler from general RFC 8785,
  live credentials and the still-open canonical graph/view/confirmation/ingestion contract.
- `VALIDATION.md:32-36` preserves the predecessor validator's no-compiler evidence ceiling, while
  `VALIDATION.md:96-99` refers to the separately reviewed implementation without retroactively
  expanding that predecessor evidence.

| # | file | evidence | severity | proposed fix |
|---|---|---|---|---|
| — | — | No surviving finding. | — | — |

**Verdict:** **KEEP**

## Synchronized IMPL records

No finding survived across `TASK-SESSION.md` and `VALIDATION.md`.

- `TASK-SESSION.md:6-18` reports bounded implementation completion and dedicated review without
  claiming runtime integration or canonical-spec mutation.
- `TASK-SESSION.md:81-90` explicitly retains live allocator, general satisfiability, credentials,
  feedback scheduling, canonical promotion, projectors, confirmation, persistence and runtime
  execution as residue.
- `VALIDATION.md:64-94` labels broad/exclusion, `pip check` and unavailable `ruff` evidence as
  retained rather than freshly rerun, rejects historical-preexistence inference and reports the
  environment failure.
- `VALIDATION.md:97-115` limits the result to fixture allocator evidence, the admitted schema
  subset, conditional initial-DAG readiness and use as input to a future canonical-v2 work unit.

The requirements additions are justified by direct production imports: JSON Schema validation uses
`jsonschema`, while allocator receipt verification uses `cryptography`. The fresh `pip check`
failure prevents any clean-environment inference, and no synchronized record makes one.

| # | file | evidence | severity | proposed fix |
|---|---|---|---|---|
| — | — | No surviving finding. | — | — |

**Verdict:** **KEEP**

## Review freeze, implementation and schema correspondence

No finding survived.

The two current complete-file hashes exactly equal the hashes declared in `CLOSEOUT.md:25-31`, and
both files end in Recheck 3 `KEEP` with `recheck_required: false`. The fresh directed test proves
the seven embedded schema byte strings still match their artifact SHA-256 values and exercises the
final reviewed implementation. This establishes current correspondence; it does not reconstruct
all prior edits to untracked files.

| # | file | evidence | severity | proposed fix |
|---|---|---|---|---|
| — | — | No surviving finding. | — | — |

**Verdict:** **KEEP**

## Write scope and sensitive files

No finding survived, subject to the evidence boundary below.

The tracked requirements diff adds only `jsonschema==4.21.1` and `cryptography==49.0.0`. The SPEC
and IMPL directories plus compiler/test files are untracked, exactly as the closeout reports.
Canonical `specs/SPEC.md` and `TEST-SPEC.md` are clean relative to `HEAD`. `CRAFT.md` and
`.craft/ledger.yml` are already dirty and the original session/proposed schema are untracked; their
current diff/status cannot prove when or by whom each change was made. No closeout marker appears in
the CRAFT/ledger diff, and the closeout correctly treats those changes as shared/out-of-scope rather
than deriving authorship from Git.

| # | file | evidence | severity | proposed fix |
|---|---|---|---|---|
| — | — | No surviving finding. | — | — |

**Verdict:** **KEEP**

## Change requests

None. No CRITICAL, MAJOR or MINOR finding survived verification.

## Evidence boundary

This review establishes current-tree consistency of the evidence-synchronization closeout. It
reexecuted only the directed 22-test suite, adjacent 34-test suite, predecessor validator,
`py_compile`, `git diff --check`, stale scans and `pip check`. It did not rerun the 284-test broad
runtime suite or the 267-test exclusion suite and does not upgrade their retained historical run
into fresh evidence.

Git can show that canonical tracked specs have no current diff and that CRAFT/ledger do, but it
cannot prove that an untracked file was never edited during closeout or establish historical
authorship inside an untracked directory. The KEEP therefore accepts the closeout's bounded action
record and exact review hashes while expressly refusing a stronger baseline-history claim.

No canonical ExecutionGraph v2 promotion, general RFC 8785 proof, topology/basic/full projector,
confirmation `@2`, CONF v1 cutover, persistence, runtime ingestion/scheduler, live allocator/key
lifecycle, provider/tool/credential execution or production readiness was exercised. These remain
required, separately reviewed future work.

