$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$tool = Join-Path $PSScriptRoot 'Invoke-SourceSnapshot.ps1'
$testRoot = Join-Path ([IO.Path]::GetTempPath()) ('composition-snapshot-test-' + [Guid]::NewGuid().ToString('N'))
$repo = Join-Path $testRoot 'source-repo'
$snapshotParent = Join-Path $testRoot 'snapshots'
$outputRoot = Join-Path $testRoot 'outputs'
$manifest = Join-Path $testRoot 'manifest.json'
$passed = 0
$failed = 0

function Assert-True([bool]$Condition, [string]$Message) { if (-not $Condition) { throw $Message } }
function Run-Test([string]$Name, [scriptblock]$Body) {
    try { & $Body; $script:passed++; Write-Output "PASS $Name" }
    catch { $script:failed++; Write-Output "FAIL $Name -- $($_.Exception.Message)" }
}

New-Item -ItemType Directory -Path $repo,$snapshotParent,$outputRoot | Out-Null
try {
    & git -C $repo init --quiet
    & git -C $repo config user.email 'snapshot@example.invalid'
    & git -C $repo config user.name 'Snapshot Fixture'
    & git -C $repo config core.autocrlf false
    foreach ($name in @('one.txt','two.txt','three.txt')) { [IO.File]::WriteAllText((Join-Path $repo $name), "committed-$name`n", [Text.UTF8Encoding]::new($false)) }
    & git -C $repo add one.txt two.txt three.txt
    & git -C $repo commit --quiet -m fixture
    $revision = (& git -C $repo rev-parse HEAD).Trim()
    $tree = (& git -C $repo rev-parse "$revision^{tree}").Trim()
    $files = @()
    foreach ($name in @('one.txt','two.txt','three.txt')) {
        $item = Get-Item -LiteralPath (Join-Path $repo $name)
        $files += [ordered]@{ path=$name; sha256=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant(); bytes=[int64]$item.Length }
    }
    [ordered]@{ schema_version=1; source_repository=$repo; source_revision=$revision; source_tree=$tree; batches=[ordered]@{ D1=$files; D3=$files; D4=$files } } | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifest -Encoding UTF8

    [IO.File]::WriteAllText((Join-Path $repo 'one.txt'), "dirty-working-tree`n", [Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText((Join-Path $repo 'untracked.txt'), "untracked`n", [Text.UTF8Encoding]::new($false))

    $script:snapshot = $null
    Run-Test 'create from pinned commit despite dirty checkout' {
        $json = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $tool -Mode Create -SnapshotParent $snapshotParent -SourceRepository $repo -ManifestPath $manifest -Batch D1
        Assert-True ($LASTEXITCODE -eq 0) 'Create failed'
        $result = $json | ConvertFrom-Json
        Assert-True ($result.verdict -eq 'PASS' -and $result.files -eq 3) 'Create did not verify 3/3'
        $script:snapshot = $result.snapshot_path
        $materialized = [IO.File]::ReadAllText((Join-Path $script:snapshot 'tree/one.txt'))
        Assert-True ($materialized -eq "committed-one.txt`n") 'Snapshot used dirty checkout bytes'
        Assert-True (@(Get-ChildItem -LiteralPath $outputRoot -Force).Count -eq 0) 'Snapshot wrote into output root'
    }

    Run-Test 'independent verification passes' {
        $json = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $tool -Mode Verify -SnapshotParent $snapshotParent -SnapshotPath $script:snapshot
        Assert-True ($LASTEXITCODE -eq 0) 'Verify failed'
        Assert-True (($json | ConvertFrom-Json).verdict -eq 'PASS') 'Verify verdict was not PASS'
    }

    Run-Test 'tampering is detected' {
        $target = Join-Path $script:snapshot 'tree/two.txt'
        (Get-Item -LiteralPath $target).IsReadOnly = $false
        [IO.File]::WriteAllText($target, "tampered`n", [Text.UTF8Encoding]::new($false))
        $process = Start-Process -FilePath 'powershell.exe' -ArgumentList @(
            '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', "`"$tool`"",
            '-Mode', 'Verify', '-SnapshotParent', "`"$snapshotParent`"",
            '-SnapshotPath', "`"$script:snapshot`""
        ) -Wait -PassThru -WindowStyle Hidden
        Assert-True ($process.ExitCode -ne 0) 'Tampered snapshot was accepted'
    }

    Run-Test 'cleanup is bounded and recoverable' {
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $tool -Mode Cleanup -SnapshotParent $snapshotParent -SnapshotPath $script:snapshot | Out-Null
        Assert-True ($LASTEXITCODE -eq 0 -and -not (Test-Path -LiteralPath $script:snapshot)) 'Cleanup did not remove exact snapshot'
        Assert-True (Test-Path -LiteralPath $repo -PathType Container) 'Cleanup touched source repository'
        Assert-True (Test-Path -LiteralPath $outputRoot -PathType Container) 'Cleanup touched output root'
    }
} finally {
    if (Test-Path -LiteralPath $testRoot) {
        Get-ChildItem -LiteralPath $testRoot -File -Recurse -Force | ForEach-Object { $_.IsReadOnly = $false }
        Remove-Item -LiteralPath $testRoot -Recurse -Force
    }
}

Write-Output "RESULT: $passed passed, $failed failed"
if ($failed -ne 0) { exit 1 }
