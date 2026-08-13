# Review — run-baseline checkpoint

## Coverage

| reviewer | lens | targets and checks |
|---|---|---|
| independent terminal reviewer | mechanics / correctness | Full read of `Capture-RunBaseline.ps1` and `Test-Capture-RunBaseline.ps1`; reran the test suite; checked `$Host`, relative paths, Git revision/status/branch drift, file-change classes, pre-existing untracked trees, allowlists, root escape/reparse handling, multi-repository behavior, receipt integrity, and write sites. |
| independent terminal reviewer | evidence / governance | Checked the directory for README and implementation receipt, inspected repository status for source/Inventory/runtime changes, and compared the claimed safety surface with executable coverage. |

Files observed:

- `Capture-RunBaseline.ps1`, SHA-256 `212F89D4B4F4432DFBEA97814CE117B17D02919E2F5972EAC874CB1EABEB6E4C`.
- `Test-Capture-RunBaseline.ps1`, SHA-256 `240508DB9403E65081BB93DCBBF8B1BB245ED3829F8981FA66B06B005DB0FD6B`.
- No README exists in `execution-redesign/tools/`.
- No implementation receipt exists in `execution-redesign/tools/`.

Commands and literal results:

- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .../Test-Capture-RunBaseline.ps1` returned `RESULT: 5 passed, 0 failed` and exit `0`.
- `rg -n '\$Host|GetRelativePath|ReparsePoint|status_porcelain|\.branch|revision|renamed|rename|baseline-before|baseline-after|baseline-diff' .../tools` found no `$Host`, no native `GetRelativePath`, no `ReparsePoint`, and no rename handling.
- `git status --short -- '.arcanum/inventory' 'implementations/server/runtime' 'implementations/tests/runtime' '.../tools'` showed no Inventory change, showed the tools directory untracked, and showed multiple modified/untracked runtime and runtime-test files. With no trusted before receipt, those runtime changes cannot be attributed or cleared by this review.

## `Capture-RunBaseline.ps1`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---|---|---|---|---|
| 1 | `Capture-RunBaseline.ps1` | Containment is lexical: `return $candidatePath.StartsWith($prefix, ...)` (line 36), while existing paths are accepted through `(Resolve-Path ...).ProviderPath` (line 50). The entire corpus contains no `ReparsePoint` check or final-target resolution. A junction/reparse path lexically below an allowed root is therefore not proven to remain inside that root; the same unchecked mechanism governs the receipt directory at lines 200–205. | CRITICAL | A successor implementation must reject or securely resolve every reparse component before reads or receipt writes. |
| 2 | `Capture-RunBaseline.ps1` | The snapshot captures `branch` and `status_porcelain_v1_untracked_all` (lines 119–120), but `New-Diff` compares only `revision` (lines 177–191). Branch-only drift and status drift outside enumerated scopes can receive `verdict = 'PASS'`. | CRITICAL | A successor must bind and compare revision, branch, and full status for every repository. |
| 3 | `Capture-RunBaseline.ps1` | `baseline-before.json` is loaded directly with `Get-Content ... | ConvertFrom-Json` (lines 236 and 247); there is no digest, signature, immutable copy, schema validation, or binding to the invocation's roots/allowlists. `AllowedWritePath` is recomputed from the current invocation (lines 207–217), so authorization can change between Before and After. | CRITICAL | A successor must authenticate the before receipt and bind all inputs/authorizations across phases. |
| 4 | `Capture-RunBaseline.ps1` | After mode writes `baseline-after.json` before parsing the before receipt and computing the diff (lines 234–238). A corrupt or substituted before receipt leaves a partial, apparently authoritative after record. | MAJOR | A successor must validate all inputs before publication and publish the receipt set atomically or with explicit incomplete state. |
| 5 | `Capture-RunBaseline.ps1` | Change kinds are only `added`, `removed`, and `modified` (lines 163–165). There is no rename identity or pairing, so the required rename case is not represented; it is merely decomposed into removal/addition when both scopes happen to be covered. | MAJOR | A successor must define and test explicit rename semantics or formally state and verify the add/remove representation. |
| 6 | `Capture-RunBaseline.ps1` | Repository comparison iterates only `BeforeSnapshot.repositories` and finds an after match by `root` (lines 177–183). It does not reject additional after repositories, duplicate declarations, changed repository ordering/configuration, or a changed scope/allowlist contract. | MAJOR | A successor must compare a canonical, unique repository/configuration set in both directions. |
| 7 | `Capture-RunBaseline.ps1` | `Get-FileRecord` silently excludes any file under `$script:ReceiptPath` (line 75), while the receipt directory is only required to be inside an allowed root (lines 200–205), not disjoint from source/write scopes. A broad receipt path can therefore suppress monitored files. | CRITICAL | A successor must require a dedicated receipt root disjoint from monitored roots and record that invariant. |

**Verdict:** FIX

Verified survivals:

- The reserved automatic variable bug is absent: neither file uses `$Host`.
- Windows PowerShell compatibility does not rely on unavailable `[IO.Path]::GetRelativePath`; `Get-RelativePathCompat` uses `System.Uri` (lines 55–61).
- Revision drift is compared (lines 181–190).
- File hashes and sizes support added/removed/modified detection within enumerated scopes (lines 154–175).
- The script's explicit write statements target receipt files only (lines 203, 225, 235, 238, 250), but finding 1 means their physical destination is not safely bounded against junctions.

## `Test-Capture-RunBaseline.ps1`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---|---|---|---|---|
| 8 | `Test-Capture-RunBaseline.ps1` | The suite defines only five `Run-Test` cases (lines 41, 57, 71, 82, 93): allowed creation/pre-existing untracked capture, nested unauthorized creation, lexical outside path, overwrite refusal, and source modification. There are no tests for deletion, rename, revision drift, branch drift, status drift, multiple repositories/roots, tampered or mismatched receipts, junction/reparse escape, changed phase configuration, partial receipt failure, or write confinement. | CRITICAL | A successor test suite must execute every mandated adversarial case, including physical-path escape and cross-phase tampering. |
| 9 | `Test-Capture-RunBaseline.ps1` | The positive test asserts only `verdict`, changed-file count, and presence of one pre-existing untracked status line (lines 49–54). It does not compare complete before/after/diff content or prove that no filesystem write occurred outside temp plus the intended receipt path. | MAJOR | A successor must inventory the test sandbox before/after and assert the complete receipt schema and write set. |

**Verdict:** FIX

## Missing checkpoint artifacts

| # | file | evidence | severity | proposed fix |
|---|---|---|---|---|
| 10 | expected README and implementation receipt | `Get-ChildItem -Force execution-redesign/tools` listed only the two PowerShell scripts. There is no usage/contract README and no implementation receipt recording provenance, authorized writes, or verification. | MAJOR | Any successor checkpoint must include the declared documentation and a trustworthy implementation receipt. |

**Verdict:** FIX

## Write-scope audit

The test run itself uses a GUID-named directory under `[System.IO.Path]::GetTempPath()` and deletes it in `finally` (test lines 5 and 105–107). No Inventory path appears changed in the current targeted Git status. However, the repository currently contains modifications in `implementations/server/runtime/` and `implementations/tests/runtime/`, plus many unrelated dirty paths outside this tool checkpoint. Because no trusted pre-run baseline or implementation receipt exists, this review cannot prove that source/runtime remained untouched. That uncertainty is independently disqualifying under the terminal instruction.

## Change requests

1. CRITICAL — physical path containment is not established across junctions/reparse points, including for receipt writes.
2. CRITICAL — branch and Git status drift are captured but ignored by the verdict.
3. CRITICAL — before receipts and phase configuration are unauthenticated and mutable.
4. CRITICAL — monitored files can be silently excluded by overlapping the receipt root.
5. CRITICAL — the suite omits most mandatory adversarial scenarios.
6. MAJOR — after publication is non-atomic and can leave partial receipts.
7. MAJOR — rename semantics are absent.
8. MAJOR — repository/configuration set equality is not established.
9. MAJOR — before/after/diff integrity and global write confinement are not tested.
10. MAJOR — README and implementation receipt are absent.

KILL desta rota
