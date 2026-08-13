$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$verifier = Join-Path $root 'verify-post-audit-telemetry.ps1'
$positive1 = Join-Path $root 'cases/positive-attempt-1'
$positive2 = Join-Path $root 'cases/positive-attempt-2'
$passed = 0

function Invoke-Case([string]$Name, [string]$Barrier, [string]$Ledger, [bool]$ShouldPass, [string]$FailureCode = '') {
    $beforeBarrier = (Get-FileHash -LiteralPath $Barrier -Algorithm SHA256).Hash
    $beforeLedger = (Get-FileHash -LiteralPath $Ledger -Algorithm SHA256).Hash
    $raw = & powershell -NoProfile -ExecutionPolicy Bypass -File $verifier -AuditBarrier $Barrier -SignalJsonl $Ledger 2>&1
    $exitCode = $LASTEXITCODE
    $afterBarrier = (Get-FileHash -LiteralPath $Barrier -Algorithm SHA256).Hash
    $afterLedger = (Get-FileHash -LiteralPath $Ledger -Algorithm SHA256).Hash
    if ($beforeBarrier -cne $afterBarrier -or $beforeLedger -cne $afterLedger) { throw "$Name mutated an input" }
    $result = ($raw -join "`n") | ConvertFrom-Json
    if ($ShouldPass -and ($exitCode -ne 0 -or $result.result -cne 'TELEMETRY_VERIFIED')) { throw "$Name expected pass" }
    if (-not $ShouldPass -and ($exitCode -ne 2 -or $result.result -cne 'BLOCK/OBSERVABILITY_GAP')) { throw "$Name expected block" }
    if ($FailureCode -and @($result.failures) -cnotcontains $FailureCode) { throw "$Name missing $FailureCode" }
    $script:passed++
}

Invoke-Case 'positive-attempt-1' (Join-Path $positive1 'audit-barrier.json') (Join-Path $positive1 'sigil-invocations.jsonl') $true
Invoke-Case 'positive-attempt-2' (Join-Path $positive2 'audit-barrier.json') (Join-Path $positive2 'sigil-invocations.jsonl') $true

$barrier = Join-Path $positive1 'audit-barrier.json'
$sourceLines = @(Get-Content -LiteralPath (Join-Path $positive1 'sigil-invocations.jsonl'))
$temporaryRoot = Join-Path ([IO.Path]::GetTempPath()) ('d1-r2-fixture-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temporaryRoot | Out-Null
try {
    $cases = [ordered]@{
        'terminal-missing' = @{ lines = @($sourceLines[0]); code = 'TERMINAL_MATCH_COUNT:0' }
        'pre-audit-missing' = @{ lines = @($sourceLines[1]); code = 'PRE_AUDIT_MATCH_COUNT:0' }
        'terminal-duplicate' = @{ lines = @($sourceLines[0],$sourceLines[1],$sourceLines[1]); code = 'TERMINAL_MATCH_COUNT:2' }
        'pre-audit-duplicate' = @{ lines = @($sourceLines[0],$sourceLines[0],$sourceLines[1]); code = 'PRE_AUDIT_MATCH_COUNT:2' }
        'terminal-before-pre-audit' = @{ lines = @($sourceLines[1],$sourceLines[0]); code = 'EVENT_ORDER_INVALID' }
        'malformed-json' = @{ lines = @($sourceLines[0],'{bad-json',$sourceLines[1]); code = 'JSONL_INVALID_JSON:2' }
        'wrong-run' = @{ lines = @($sourceLines[0],($sourceLines[1] -replace '"run_id":"d1-fixture-run"','"run_id":"other-run"')); code = 'TERMINAL_MATCH_COUNT:0' }
        'wrong-sheet-attempt' = @{ lines = @($sourceLines[0],($sourceLines[1] -replace '"sheet_producer_attempt":3','"sheet_producer_attempt":4')); code = 'DIVERGENT_D1_ATTEMPT:2' }
        'wrong-audit-attempt' = @{ lines = @($sourceLines[0],($sourceLines[1] -replace '"audit_attempt":1','"audit_attempt":2')); code = 'DIVERGENT_D1_ATTEMPT:2' }
        'wrong-writer-attempt' = @{ lines = @($sourceLines[0],($sourceLines[1] -replace '"consumed_writer_attempt":1','"consumed_writer_attempt":2')); code = 'DIVERGENT_D1_ATTEMPT:2' }
        'verdict-mismatch' = @{ lines = @($sourceLines[0],($sourceLines[1] -replace '"auditor_verdict":"PASS"','"auditor_verdict":"BLOCK"')); code = 'VERDICT_MISMATCH' }
        'correction-mismatch' = @{ lines = @($sourceLines[0],($sourceLines[1] -replace '"correction_count":0','"correction_count":1')); code = 'CORRECTION_COUNT_MISMATCH' }
        'exit-reason-mismatch' = @{ lines = @($sourceLines[0],($sourceLines[1] -replace '"exit_reason":"audit_passed"','"exit_reason":"different"')); code = 'EXIT_REASON_MISMATCH' }
        'artifact-mismatch' = @{ lines = @($sourceLines[0],($sourceLines[1] -replace '"size":101','"size":102')); code = 'AUDIT_ARTIFACT_MISMATCH' }
    }
    foreach ($entry in $cases.GetEnumerator()) {
        $ledger = Join-Path $temporaryRoot ($entry.Key + '.jsonl')
        [IO.File]::WriteAllLines($ledger, [string[]]$entry.Value.lines, [Text.UTF8Encoding]::new($false))
        Invoke-Case $entry.Key $barrier $ledger $false $entry.Value.code
    }

    $badBarrier = Join-Path $temporaryRoot 'bad-barrier.json'
    ((Get-Content -LiteralPath $barrier -Raw) -replace '"audit_attempt":1','"audit_attempt":"1"') | Set-Content -LiteralPath $badBarrier -Encoding UTF8
    Invoke-Case 'typed-attempt-required' $badBarrier (Join-Path $positive1 'sigil-invocations.jsonl') $false 'AUDIT_BARRIER_SCHEMA_INVALID'

    $mixedLedger = Join-Path $temporaryRoot 'mixed-attempt.jsonl'
    [IO.File]::WriteAllLines($mixedLedger, [string[]]@($sourceLines[0], $sourceLines[1], ($sourceLines[1] -replace '"audit_attempt":1','"audit_attempt":2')), [Text.UTF8Encoding]::new($false))
    Invoke-Case 'mixed-correct-wrong-attempt' $barrier $mixedLedger $false 'DIVERGENT_D1_ATTEMPT:3'

    $badTime = Join-Path $temporaryRoot 'bad-time.jsonl'
    [IO.File]::WriteAllLines($badTime, [string[]]@(($sourceLines[0] -replace '2026-08-13T10:00:00Z','2026-08-13T10:00:00+01:00'), $sourceLines[1]), [Text.UTF8Encoding]::new($false))
    Invoke-Case 'emitted-at-must-be-utc-z' $barrier $badTime $false 'PRE_AUDIT_SCHEMA_INVALID:1'

    $snapshotLedger = Join-Path $temporaryRoot 'snapshot-change.jsonl'
    [IO.File]::WriteAllLines($snapshotLedger, [string[]]$sourceLines, [Text.UTF8Encoding]::new($false))
    $hook = Join-Path $temporaryRoot 'mutate.ps1'
    [IO.File]::WriteAllText($hook, 'param($p) [IO.File]::AppendAllText($p,"`n")', [Text.UTF8Encoding]::new($false))
    $env:D1_R2_FIXTURE_TEST_MODE='1'
    $raw = & powershell -NoProfile -ExecutionPolicy Bypass -File $verifier -AuditBarrier $barrier -SignalJsonl $snapshotLedger -BeforeSnapshotRecheckHook $hook 2>&1
    Remove-Item Env:D1_R2_FIXTURE_TEST_MODE
    $snapshotResult = ($raw -join "`n") | ConvertFrom-Json
    if ($LASTEXITCODE -ne 2 -or @($snapshotResult.failures) -cnotcontains 'SIGNAL_JSONL_CHANGED_DURING_READ') { throw 'snapshot mutation not detected' }
    $passed++

    $invalidUtf8 = Join-Path $temporaryRoot 'invalid-utf8.jsonl'
    [IO.File]::WriteAllBytes($invalidUtf8, [byte[]](0xFF,0x0A))
    Invoke-Case 'invalid-utf8-ledger' $barrier $invalidUtf8 $false 'SIGNAL_JSONL_INVALID_UTF8'

    $invalidBarrier = Join-Path $temporaryRoot 'invalid-utf8-barrier.json'
    [IO.File]::WriteAllBytes($invalidBarrier, [byte[]](0xFF,0x0A))
    Invoke-Case 'invalid-utf8-barrier' $invalidBarrier (Join-Path $positive1 'sigil-invocations.jsonl') $false 'AUDIT_BARRIER_INVALID_UTF8'

    $runRoot = Join-Path $temporaryRoot 'runs'
    $runDir = Join-Path $runRoot 'd1-fixture-run'
    New-Item -ItemType Directory -Path $runDir | Out-Null
    $exactOutput = Join-Path $runDir 'post-audit-telemetry-check-1.json'
    $raw = & powershell -NoProfile -ExecutionPolicy Bypass -File $verifier -AuditBarrier $barrier -SignalJsonl (Join-Path $positive1 'sigil-invocations.jsonl') -RunRoot $runRoot -OutputPath $exactOutput 2>&1
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $exactOutput)) { throw 'exact output write failed' }
    $written = Get-Content -LiteralPath $exactOutput -Raw | ConvertFrom-Json
    if ($written.result -cne 'TELEMETRY_VERIFIED') { throw 'written output content invalid' }
    $fileCount = @(Get-ChildItem -Recurse -File $runRoot).Count
    if ($fileCount -ne 1) { throw 'unexpected output writes' }
    $passed++
    $ErrorActionPreference='Continue'
    & powershell -NoProfile -ExecutionPolicy Bypass -File $verifier -AuditBarrier $barrier -SignalJsonl (Join-Path $positive1 'sigil-invocations.jsonl') -RunRoot $runRoot -OutputPath $exactOutput *> $null
    $ErrorActionPreference='Stop'
    if ($LASTEXITCODE -eq 0) { throw 'no-overwrite failed' }
    $passed++

    $raceRun = Join-Path $runRoot 'd1-fixture-run-race'
    New-Item -ItemType Directory -Path $raceRun | Out-Null
    $raceBarrier = Join-Path $temporaryRoot 'race-barrier.json'
    ((Get-Content -LiteralPath $barrier -Raw) -replace '"run_id":"d1-fixture-run"','"run_id":"d1-fixture-run-race"') | Set-Content -LiteralPath $raceBarrier -Encoding UTF8
    $raceLedger = Join-Path $temporaryRoot 'race-ledger.jsonl'
    (($sourceLines -join "`n") -replace '"run_id":"d1-fixture-run"','"run_id":"d1-fixture-run-race"') | Set-Content -LiteralPath $raceLedger -Encoding UTF8
    $raceOutput = Join-Path $raceRun 'post-audit-telemetry-check-1.json'
    $raceHook = Join-Path $temporaryRoot 'race-create.ps1'
    [IO.File]::WriteAllText($raceHook, 'param($p) [IO.File]::WriteAllText($p,"competitor",[Text.UTF8Encoding]::new($false))', [Text.UTF8Encoding]::new($false))
    $env:D1_R2_FIXTURE_TEST_MODE='1'
    $ErrorActionPreference='Continue'
    & powershell -NoProfile -ExecutionPolicy Bypass -File $verifier -AuditBarrier $raceBarrier -SignalJsonl $raceLedger -RunRoot $runRoot -OutputPath $raceOutput -BeforeOutputCreateHook $raceHook *> $null
    $raceExit=$LASTEXITCODE
    $ErrorActionPreference='Stop'
    Remove-Item Env:D1_R2_FIXTURE_TEST_MODE
    if ($raceExit -eq 0 -or (Get-Content -LiteralPath $raceOutput -Raw) -cne 'competitor') { throw 'atomic contention overwrote competitor' }
    $passed++

    $badOutput = Join-Path $temporaryRoot 'not-attempt-specific.json'
    $ErrorActionPreference = 'Continue'
    & powershell -NoProfile -ExecutionPolicy Bypass -File $verifier -AuditBarrier $barrier -SignalJsonl (Join-Path $positive1 'sigil-invocations.jsonl') -RunRoot $temporaryRoot -OutputPath $badOutput *> $null
    $ErrorActionPreference = 'Stop'
    if ($LASTEXITCODE -eq 0 -or (Test-Path -LiteralPath $badOutput)) { throw 'output allowlist case expected refusal without write' }
    $passed++
}
finally {
    Remove-Item -LiteralPath $temporaryRoot -Recurse -Force
}

python (Join-Path $root 'validate-schemas.py')
if ($LASTEXITCODE -ne 0) { throw 'schema validation failed' }
$passed++
"PASS: $passed telemetry post-audit fixture cases"
