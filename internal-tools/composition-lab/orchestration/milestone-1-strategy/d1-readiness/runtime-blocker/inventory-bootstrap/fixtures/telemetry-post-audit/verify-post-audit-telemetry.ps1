param(
    [Parameter(Mandatory = $true)][string]$AuditBarrier,
    [Parameter(Mandatory = $true)][string]$SignalJsonl,
    [string]$RunRoot,
    [string]$OutputPath,
    [string]$BeforeSnapshotRecheckHook,
    [string]$BeforeOutputCreateHook
)

$ErrorActionPreference = 'Stop'

function Get-BytesSnapshot([string]$Path) {
    $resolved = [IO.Path]::GetFullPath($Path)
    $bytes = [IO.File]::ReadAllBytes($resolved)
    $sha = [Security.Cryptography.SHA256]::Create()
    try { $hash = -join ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString('x2') }) }
    finally { $sha.Dispose() }
    [ordered]@{ path = $resolved; sha256 = $hash; size = [int64]$bytes.Length; bytes = $bytes }
}

function Get-PublicIdentity($Snapshot) {
    if ($null -eq $Snapshot) { return $null }
    [ordered]@{ path = $Snapshot.path; sha256 = $Snapshot.sha256; size = $Snapshot.size }
}
function Decode-Utf8($Bytes) {
    $text = [Text.UTF8Encoding]::new($false, $true).GetString($Bytes)
    if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) { return $text.Substring(1) }
    return $text
}

function Snapshot-Unchanged($Snapshot) {
    try {
        $again = Get-BytesSnapshot $Snapshot.path
        return $again.sha256 -ceq $Snapshot.sha256 -and $again.size -eq $Snapshot.size
    } catch { return $false }
}

function Has-ExactProperties($Object, [string[]]$Required) {
    if ($null -eq $Object) { return $false }
    (@($Object.PSObject.Properties.Name | Sort-Object) -join "`n") -ceq (@($Required | Sort-Object) -join "`n")
}
function Is-PositiveInteger($Value, [int]$Maximum = [int]::MaxValue) { ($Value -is [int] -or $Value -is [long]) -and $Value -ge 1 -and $Value -le $Maximum }
function Is-NonNegativeInteger($Value) { ($Value -is [int] -or $Value -is [long]) -and $Value -ge 0 }
function Is-UtcTimestamp($Value) {
    if (-not ($Value -is [string]) -or $Value -cnotmatch '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$') { return $false }
    try {
        $parsed = [DateTimeOffset]::Parse($Value, [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::AssumeUniversal)
        return $parsed.Offset -eq [TimeSpan]::Zero
    } catch { return $false }
}
function Is-Artifact($Value) {
    (Has-ExactProperties $Value @('path','sha256','size')) -and ($Value.path -is [string]) -and
    $Value.path.Length -gt 0 -and ($Value.sha256 -is [string]) -and $Value.sha256 -cmatch '^[0-9a-f]{64}$' -and
    (Is-PositiveInteger $Value.size)
}
function Artifacts-Equal($Left, $Right) { $Left.path -ceq $Right.path -and $Left.sha256 -ceq $Right.sha256 -and [int64]$Left.size -eq [int64]$Right.size }
function Has-ReparseComponent([string]$Path, [string]$StopAt) {
    $current = [IO.Path]::GetFullPath($Path)
    $stop = [IO.Path]::GetFullPath($StopAt).TrimEnd([IO.Path]::DirectorySeparatorChar)
    while ($current.Length -ge $stop.Length) {
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { return $true }
        }
        if ($current -ceq $stop) { break }
        $current = [IO.Path]::GetDirectoryName($current)
        if (-not $current) { break }
    }
    return $false
}

$failures = [Collections.Generic.List[string]]::new()
$barrierSnapshot = $null; $ledgerSnapshot = $null; $barrier = $null; $events = @(); $preLine = $null; $terminalLine = $null
try { $barrierSnapshot = Get-BytesSnapshot $AuditBarrier } catch { $failures.Add('AUDIT_BARRIER_UNREADABLE') }
try { $ledgerSnapshot = Get-BytesSnapshot $SignalJsonl } catch { $failures.Add('SIGNAL_JSONL_UNREADABLE') }

if ($barrierSnapshot) {
    try { $barrierText = Decode-Utf8 $barrierSnapshot.bytes }
    catch [Text.DecoderFallbackException] { $failures.Add('AUDIT_BARRIER_INVALID_UTF8') }
    if ($null -ne $barrierText) {
        try { $barrier = $barrierText | ConvertFrom-Json }
        catch { $failures.Add('AUDIT_BARRIER_INVALID_JSON') }
    }
}
$barrierFields = @('schema_version','artifact_kind','run_id','sheet_producer_attempt','writer_attempt','audit_attempt','terminal_state','correction_count','exit_reason','audit_artifact')
if ($barrier) {
    if (-not (Has-ExactProperties $barrier $barrierFields) -or $barrier.schema_version -cne '1.0.0' -or
        $barrier.artifact_kind -cne 'inventory-bootstrap-audit-barrier' -or $barrier.run_id -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*$' -or
        -not (Is-PositiveInteger $barrier.sheet_producer_attempt) -or -not (Is-PositiveInteger $barrier.writer_attempt 2) -or
        -not (Is-PositiveInteger $barrier.audit_attempt 2) -or @('PASS','BOUNDED_CORRECTIONS','BLOCK') -cnotcontains $barrier.terminal_state -or
        -not (Is-NonNegativeInteger $barrier.correction_count) -or -not ($barrier.exit_reason -is [string]) -or
        $barrier.exit_reason.Length -eq 0 -or -not (Is-Artifact $barrier.audit_artifact)) { $failures.Add('AUDIT_BARRIER_SCHEMA_INVALID') }
}

if ($ledgerSnapshot) {
    $text = $null
    try { $text = Decode-Utf8 $ledgerSnapshot.bytes }
    catch [Text.DecoderFallbackException] { $failures.Add('SIGNAL_JSONL_INVALID_UTF8') }
    if ($null -ne $text) {
        $lines = $text -split "`r?`n"
        if ($lines.Count -gt 0 -and $lines[-1] -eq '') { $lines = $lines[0..($lines.Count - 2)] }
        for ($index = 0; $index -lt $lines.Count; $index++) {
            if ([string]::IsNullOrWhiteSpace($lines[$index])) { $failures.Add("JSONL_EMPTY_LINE:$($index+1)"); continue }
            try { $events += [pscustomobject]@{ line = $index + 1; event = $lines[$index] | ConvertFrom-Json } }
            catch { $failures.Add("JSONL_INVALID_JSON:$($index+1)") }
        }
    }
}

if ($barrier -and -not $failures.Contains('AUDIT_BARRIER_SCHEMA_INVALID')) {
    $preFields = @('schema_version','event_kind','emitted_at','run_id','sheet_producer_attempt','writer_attempt','mode','source_count','created_entries','updated_entries','contradictions','lint_gaps','validation','downstream_lookup_count','filed_synthesis_count','corpus_digest','profile_version')
    $terminalFields = @('schema_version','event_kind','emitted_at','run_id','sheet_producer_attempt','audit_attempt','consumed_writer_attempt','auditor_verdict','correction_count','exit_reason','audit_artifact')
    $preMatches = @(); $terminalMatches = @()
    foreach ($row in $events) {
        $event = $row.event
        if ($event.run_id -ceq $barrier.run_id -and @('inventory-bootstrap-pre-audit','inventory-bootstrap-terminal') -ccontains $event.event_kind) {
            $divergent = $event.sheet_producer_attempt -ne $barrier.sheet_producer_attempt
            if ($event.event_kind -ceq 'inventory-bootstrap-pre-audit') { $divergent = $divergent -or $event.writer_attempt -ne $barrier.writer_attempt }
            else { $divergent = $divergent -or $event.audit_attempt -ne $barrier.audit_attempt -or $event.consumed_writer_attempt -ne $barrier.writer_attempt }
            if ($divergent) { $failures.Add("DIVERGENT_D1_ATTEMPT:$($row.line)"); continue }
        }
        if ($event.event_kind -ceq 'inventory-bootstrap-pre-audit' -and $event.run_id -ceq $barrier.run_id) {
            $valid = (Has-ExactProperties $event $preFields) -and $event.schema_version -ceq '1.0.0' -and (Is-UtcTimestamp $event.emitted_at) -and
                (Is-PositiveInteger $event.sheet_producer_attempt) -and (Is-PositiveInteger $event.writer_attempt 2) -and $event.mode -ceq 'backfill-validate-lint' -and
                (Is-NonNegativeInteger $event.source_count) -and (Is-NonNegativeInteger $event.created_entries) -and (Is-NonNegativeInteger $event.updated_entries) -and
                (Is-NonNegativeInteger $event.contradictions) -and (Is-NonNegativeInteger $event.lint_gaps) -and @('pass','fail','blocked') -ccontains $event.validation -and
                (Is-NonNegativeInteger $event.downstream_lookup_count) -and (Is-NonNegativeInteger $event.filed_synthesis_count) -and
                $event.corpus_digest -cmatch '^[0-9a-f]{64}$' -and ($event.profile_version -is [string]) -and $event.profile_version.Length -gt 0
            if (-not $valid) { $failures.Add("PRE_AUDIT_SCHEMA_INVALID:$($row.line)") }; $preMatches += $row
        }
        if ($event.event_kind -ceq 'inventory-bootstrap-terminal' -and $event.run_id -ceq $barrier.run_id) {
            $valid = (Has-ExactProperties $event $terminalFields) -and $event.schema_version -ceq '1.0.0' -and (Is-UtcTimestamp $event.emitted_at) -and
                (Is-PositiveInteger $event.sheet_producer_attempt) -and (Is-PositiveInteger $event.audit_attempt 2) -and (Is-PositiveInteger $event.consumed_writer_attempt 2) -and
                @('PASS','BOUNDED_CORRECTIONS','BLOCK') -ccontains $event.auditor_verdict -and (Is-NonNegativeInteger $event.correction_count) -and
                ($event.exit_reason -is [string]) -and $event.exit_reason.Length -gt 0 -and (Is-Artifact $event.audit_artifact)
            if (-not $valid) { $failures.Add("TERMINAL_SCHEMA_INVALID:$($row.line)") }; $terminalMatches += $row
        }
    }
    if ($preMatches.Count -ne 1) { $failures.Add("PRE_AUDIT_MATCH_COUNT:$($preMatches.Count)") }
    if ($terminalMatches.Count -ne 1) { $failures.Add("TERMINAL_MATCH_COUNT:$($terminalMatches.Count)") }
    if ($preMatches.Count -eq 1) { $preLine = $preMatches[0].line }; if ($terminalMatches.Count -eq 1) { $terminalLine = $terminalMatches[0].line }
    if ($terminalMatches.Count -eq 1) {
        $terminal = $terminalMatches[0].event
        if ($terminal.auditor_verdict -cne $barrier.terminal_state) { $failures.Add('VERDICT_MISMATCH') }
        if ($terminal.correction_count -ne $barrier.correction_count) { $failures.Add('CORRECTION_COUNT_MISMATCH') }
        if ($terminal.exit_reason -cne $barrier.exit_reason) { $failures.Add('EXIT_REASON_MISMATCH') }
        if ((Is-Artifact $terminal.audit_artifact) -and -not (Artifacts-Equal $terminal.audit_artifact $barrier.audit_artifact)) { $failures.Add('AUDIT_ARTIFACT_MISMATCH') }
    }
    if ($preLine -and $terminalLine -and $terminalLine -le $preLine) { $failures.Add('EVENT_ORDER_INVALID') }
}

if ($BeforeSnapshotRecheckHook) {
    if ($env:D1_R2_FIXTURE_TEST_MODE -cne '1') { throw 'SNAPSHOT_HOOK_FORBIDDEN' }
    & ([IO.Path]::GetFullPath($BeforeSnapshotRecheckHook)) $SignalJsonl
}
if ($barrierSnapshot -and -not (Snapshot-Unchanged $barrierSnapshot)) { $failures.Add('AUDIT_BARRIER_CHANGED_DURING_READ') }
if ($ledgerSnapshot -and -not (Snapshot-Unchanged $ledgerSnapshot)) { $failures.Add('SIGNAL_JSONL_CHANGED_DURING_READ') }

$result = if ($failures.Count -eq 0) { 'TELEMETRY_VERIFIED' } else { 'BLOCK/OBSERVABILITY_GAP' }
$check = [ordered]@{
    schema_version='1.0.0'; artifact_kind='inventory-bootstrap-post-audit-telemetry-check'
    run_id=if ($barrier) {$barrier.run_id} else {$null}; sheet_producer_attempt=if ($barrier) {$barrier.sheet_producer_attempt} else {$null}
    audit_attempt=if ($barrier) {$barrier.audit_attempt} else {$null}
    inputs=[ordered]@{audit_barrier=(Get-PublicIdentity $barrierSnapshot);signal_jsonl=(Get-PublicIdentity $ledgerSnapshot)}
    matches=[ordered]@{pre_audit_line_number=$preLine;terminal_line_number=$terminalLine};result=$result;failures=@($failures|Sort-Object -Unique)
}
$json = $check | ConvertTo-Json -Depth 8

if ($OutputPath) {
    if (-not $RunRoot -or -not $barrier -or $failures.Contains('AUDIT_BARRIER_SCHEMA_INVALID')) { throw 'OUTPUT_CONTEXT_INVALID' }
    $resolvedRunRoot = [IO.Path]::GetFullPath($RunRoot).TrimEnd([IO.Path]::DirectorySeparatorChar)
    $expectedRunDir = [IO.Path]::GetFullPath((Join-Path $resolvedRunRoot $barrier.run_id))
    $expected = [IO.Path]::GetFullPath((Join-Path $expectedRunDir "post-audit-telemetry-check-$($barrier.audit_attempt).json"))
    $resolvedOutput = [IO.Path]::GetFullPath($OutputPath)
    if ($resolvedOutput -cne $expected) { throw 'OUTPUT_PATH_NOT_ALLOWLISTED' }
    if (Has-ReparseComponent $expectedRunDir $resolvedRunRoot) { throw 'OUTPUT_PATH_REPARSE_ESCAPE' }
    if (-not (Test-Path -LiteralPath $expectedRunDir -PathType Container)) { throw 'OUTPUT_RUN_DIRECTORY_MISSING' }
    if ($BeforeOutputCreateHook) {
        if ($env:D1_R2_FIXTURE_TEST_MODE -cne '1') { throw 'OUTPUT_HOOK_FORBIDDEN' }
        & ([IO.Path]::GetFullPath($BeforeOutputCreateHook)) $resolvedOutput
    }
    $payload = [Text.UTF8Encoding]::new($false).GetBytes($json + "`n")
    $stream = $null
    try {
        $stream = [IO.FileStream]::new($resolvedOutput, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
        $stream.Write($payload, 0, $payload.Length)
        $stream.Flush($true)
    } catch [IO.IOException] { throw 'OUTPUT_PATH_ALREADY_EXISTS_OR_CONTENDED' }
    finally { if ($null -ne $stream) { $stream.Dispose() } }
}
$json
if ($result -eq 'TELEMETRY_VERIFIED') { exit 0 } else { exit 2 }
