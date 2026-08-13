$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$toolPath = Join-Path $PSScriptRoot 'Capture-RunBaseline.ps1'
$testArea = Join-Path ([System.IO.Path]::GetTempPath()) ('composition-baseline-' + [Guid]::NewGuid().ToString('N'))
$passed = 0
$failed = 0

function Assert-True {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw $Message }
}

function Invoke-Tool {
    param([hashtable]$Parameters, [int]$ExpectedExit = 0)
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $toolPath @Parameters | Out-Null
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne $ExpectedExit) { throw "Expected exit $ExpectedExit, got $exitCode" }
}

function Run-Test {
    param([string]$Name, [scriptblock]$Body)
    try { & $Body; $script:passed++; Write-Output "PASS $Name" }
    catch { $script:failed++; Write-Output "FAIL $Name -- $($_.Exception.Message)" }
}

New-Item -ItemType Directory -Path $testArea | Out-Null
try {
    $repository = Join-Path $testArea 'repo'
    New-Item -ItemType Directory -Path $repository | Out-Null
    & git -C $repository init --quiet
    & git -C $repository config user.email 'baseline@example.invalid'
    & git -C $repository config user.name 'Baseline Fixture'
    Set-Content -LiteralPath (Join-Path $repository 'tracked.txt') -Value 'tracked'
    & git -C $repository add tracked.txt
    & git -C $repository commit --quiet -m fixture
    $preexistingTree = Join-Path $repository 'preexisting-untracked'
    New-Item -ItemType Directory -Path $preexistingTree | Out-Null
    Set-Content -LiteralPath (Join-Path $preexistingTree 'old.txt') -Value 'old'

    Run-Test 'positive allowed write and preexisting untracked tree' {
        $runRoot = Join-Path $repository 'run-positive'
        $receipts = Join-Path $runRoot 'receipts'
        $output = Join-Path $runRoot 'scout-return.md'
        $common = @{ AllowedRoot = @($repository); RepositoryRoot = @($repository); SourcePath = @((Join-Path $repository 'tracked.txt')); WriteRoot = @($runRoot); AllowedWritePath = @($output); ReceiptDirectory = $receipts }
        Invoke-Tool -Parameters ($common + @{ Mode = 'Before' })
        Set-Content -LiteralPath $output -Value 'allowed'
        Invoke-Tool -Parameters ($common + @{ Mode = 'After' })
        $diff = Get-Content -Raw -LiteralPath (Join-Path $receipts 'baseline-diff.json') | ConvertFrom-Json
        Assert-True ($diff.verdict -eq 'PASS') 'Allowed output should pass'
        Assert-True (@($diff.changed_files).Count -eq 1) 'Only allowed output should be reported'
        $before = Get-Content -Raw -LiteralPath (Join-Path $receipts 'baseline-before.json') | ConvertFrom-Json
        $status = @($before.repositories[0].status_porcelain_v1_untracked_all) -join "`n"
        Assert-True ($status -match 'preexisting-untracked/old.txt') 'Preexisting untracked file must be captured by Git status'
    }

    Run-Test 'negative write detection inside preexisting untracked tree' {
        $runRoot = Join-Path $repository 'run-negative-write'
        $receipts = Join-Path $runRoot 'receipts'
        $output = Join-Path $runRoot 'scout-return.md'
        $common = @{ AllowedRoot = @($repository); RepositoryRoot = @($repository); SourcePath = @($repository); WriteRoot = @($runRoot); AllowedWritePath = @($output); ReceiptDirectory = $receipts }
        Invoke-Tool -Parameters ($common + @{ Mode = 'Before' })
        Set-Content -LiteralPath (Join-Path $preexistingTree 'new.txt') -Value 'unauthorized'
        Invoke-Tool -Parameters ($common + @{ Mode = 'After' }) -ExpectedExit 2
        $diff = Get-Content -Raw -LiteralPath (Join-Path $receipts 'baseline-diff.json') | ConvertFrom-Json
        Assert-True ($diff.verdict -eq 'BLOCK') 'Unauthorized write must block'
        $nestedViolations = @(@($diff.unauthorized_changes) | Where-Object { $_.absolute_path -like '*new.txt' })
        Assert-True ($nestedViolations.Count -eq 1) 'New nested file must be identified'
    }

    Run-Test 'negative path escape' {
        $outside = Join-Path $testArea 'outside'
        New-Item -ItemType Directory -Path $outside | Out-Null
        $parameters = @{ Mode = 'Before'; AllowedRoot = @($repository); SourcePath = @($outside); WriteRoot = @((Join-Path $repository 'escape-run')); ReceiptDirectory = (Join-Path $repository 'escape-run/receipts') }
        $priorPreference = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $toolPath @parameters 2>$null | Out-Null
        $ErrorActionPreference = $priorPreference
        Assert-True ($LASTEXITCODE -ne 0) 'Path outside allowed roots must fail'
    }

    Run-Test 'negative receipt overwrite' {
        $runRoot = Join-Path $repository 'run-overwrite'
        $parameters = @{ Mode = 'Before'; AllowedRoot = @($repository); SourcePath = @((Join-Path $repository 'tracked.txt')); WriteRoot = @($runRoot); ReceiptDirectory = (Join-Path $runRoot 'receipts') }
        Invoke-Tool -Parameters $parameters
        $priorPreference = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $toolPath @parameters 2>$null | Out-Null
        $ErrorActionPreference = $priorPreference
        Assert-True ($LASTEXITCODE -ne 0) 'Existing receipt must not be overwritten'
    }

    Run-Test 'negative source modification' {
        $source = Join-Path $repository 'source-negative.txt'
        Set-Content -LiteralPath $source -Value 'before'
        $runRoot = Join-Path $repository 'run-source-negative'
        $parameters = @{ AllowedRoot = @($repository); RepositoryRoot = @($repository); SourcePath = @($source); WriteRoot = @($runRoot); ReceiptDirectory = (Join-Path $runRoot 'receipts') }
        Invoke-Tool -Parameters ($parameters + @{ Mode = 'Before' })
        Set-Content -LiteralPath $source -Value 'after'
        Invoke-Tool -Parameters ($parameters + @{ Mode = 'After' }) -ExpectedExit 2
        $diff = Get-Content -Raw -LiteralPath (Join-Path $runRoot 'receipts/baseline-diff.json') | ConvertFrom-Json
        Assert-True ($diff.verdict -eq 'BLOCK') 'Source modification must block'
    }
}
finally {
    Remove-Item -LiteralPath $testArea -Recurse -Force
}

Write-Output "RESULT: $passed passed, $failed failed"
if ($failed -ne 0) { exit 1 }
