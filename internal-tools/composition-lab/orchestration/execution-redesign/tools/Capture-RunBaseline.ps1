[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Before', 'After', 'Diff')]
    [string]$Mode,

    [Parameter(Mandatory = $true)]
    [string]$ReceiptDirectory,

    [Parameter(Mandatory = $true)]
    [string[]]$AllowedRoot,

    [string[]]$RepositoryRoot = @(),
    [string[]]$SourcePath = @(),
    [string[]]$WriteRoot = @(),
    [string[]]$AllowedWritePath = @()
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

function Get-NormalizedFullPath {
    param([Parameter(Mandatory = $true)][string]$LiteralPath)
    return [System.IO.Path]::GetFullPath($LiteralPath).TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
}

function Test-PathInsideRoot {
    param(
        [Parameter(Mandatory = $true)][string]$Candidate,
        [Parameter(Mandatory = $true)][string]$Root
    )
    $candidatePath = Get-NormalizedFullPath $Candidate
    $rootPath = Get-NormalizedFullPath $Root
    if ([string]::Equals($candidatePath, $rootPath, [System.StringComparison]::OrdinalIgnoreCase)) { return $true }
    $prefix = $rootPath + [System.IO.Path]::DirectorySeparatorChar
    return $candidatePath.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)
}

function Assert-InAllowedRoots {
    param([Parameter(Mandatory = $true)][string]$Candidate, [string]$Description = 'path')
    foreach ($rootPath in $script:NormalizedAllowedRoots) {
        if (Test-PathInsideRoot -Candidate $Candidate -Root $rootPath) { return }
    }
    throw "$Description escapes all allowed roots: $Candidate"
}

function Get-ExistingResolvedPath {
    param([Parameter(Mandatory = $true)][string]$LiteralPath, [string]$Description = 'path')
    if (-not (Test-Path -LiteralPath $LiteralPath)) { throw "$Description does not exist: $LiteralPath" }
    $resolvedPath = (Resolve-Path -LiteralPath $LiteralPath).ProviderPath
    Assert-InAllowedRoots -Candidate $resolvedPath -Description $Description
    return Get-NormalizedFullPath $resolvedPath
}

function Get-RelativePathCompat {
    param([Parameter(Mandatory = $true)][string]$BasePath, [Parameter(Mandatory = $true)][string]$TargetPath)
    $baseFull = Get-NormalizedFullPath $BasePath
    $targetFull = Get-NormalizedFullPath $TargetPath
    $baseUri = New-Object System.Uri(($baseFull + [System.IO.Path]::DirectorySeparatorChar))
    $targetUri = New-Object System.Uri($targetFull)
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
}

function Invoke-GitText {
    param([Parameter(Mandatory = $true)][string]$Repository, [Parameter(Mandatory = $true)][string[]]$Arguments)
    $lines = & git -C $Repository @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) { throw "git failed in $Repository ($($Arguments -join ' ')): $($lines -join [Environment]::NewLine)" }
    return @($lines | ForEach-Object { $_.ToString() })
}

function Get-FileRecord {
    param([Parameter(Mandatory = $true)][string]$FilePath, [Parameter(Mandatory = $true)][string]$ScopeRoot)
    $resolvedFile = (Resolve-Path -LiteralPath $FilePath).ProviderPath
    Assert-InAllowedRoots -Candidate $resolvedFile -Description 'inventory file'
    if (Test-PathInsideRoot -Candidate $resolvedFile -Root $script:ReceiptPath) { return $null }
    $item = Get-Item -LiteralPath $resolvedFile -Force
    if ($item.PSIsContainer) { throw "Expected file but found directory: $resolvedFile" }
    return [ordered]@{
        scope_root = $ScopeRoot
        path = Get-RelativePathCompat -BasePath $ScopeRoot -TargetPath $resolvedFile
        absolute_path = Get-NormalizedFullPath $resolvedFile
        sha256 = (Get-FileHash -LiteralPath $resolvedFile -Algorithm SHA256).Hash.ToLowerInvariant()
        size = [int64]$item.Length
    }
}

function Get-ScopeRecord {
    param([Parameter(Mandatory = $true)][string]$RequestedPath, [Parameter(Mandatory = $true)][string]$Kind)
    $normalizedRequest = Get-NormalizedFullPath $RequestedPath
    Assert-InAllowedRoots -Candidate $normalizedRequest -Description $Kind
    if (-not (Test-Path -LiteralPath $normalizedRequest)) {
        if ($Kind -ne 'write_root') { throw "$Kind does not exist: $normalizedRequest" }
        return [ordered]@{ kind = $Kind; root = $normalizedRequest; exists = $false; files = @() }
    }
    $resolvedScope = Get-ExistingResolvedPath -LiteralPath $normalizedRequest -Description $Kind
    $scopeItem = Get-Item -LiteralPath $resolvedScope -Force
    $records = @()
    if ($scopeItem.PSIsContainer) {
        foreach ($fileItem in @(Get-ChildItem -LiteralPath $resolvedScope -File -Force -Recurse | Sort-Object FullName)) {
            $record = Get-FileRecord -FilePath $fileItem.FullName -ScopeRoot $resolvedScope
            if ($null -ne $record) { $records += $record }
        }
    } else {
        $record = Get-FileRecord -FilePath $resolvedScope -ScopeRoot (Split-Path -Parent $resolvedScope)
        if ($null -ne $record) { $records += $record }
    }
    return [ordered]@{ kind = $Kind; root = $resolvedScope; exists = $true; files = @($records) }
}

function New-Snapshot {
    $repositories = @()
    foreach ($repositoryCandidate in $RepositoryRoot) {
        $repositoryPath = Get-ExistingResolvedPath -LiteralPath $repositoryCandidate -Description 'repository root'
        $insideWorkTree = (Invoke-GitText -Repository $repositoryPath -Arguments @('rev-parse', '--is-inside-work-tree')) -join ''
        if ($insideWorkTree -ne 'true') { throw "Not a Git worktree: $repositoryPath" }
        $repositories += [ordered]@{
            root = $repositoryPath
            revision = ((Invoke-GitText -Repository $repositoryPath -Arguments @('rev-parse', 'HEAD')) -join '').Trim()
            branch = ((Invoke-GitText -Repository $repositoryPath -Arguments @('rev-parse', '--abbrev-ref', 'HEAD')) -join '').Trim()
            status_porcelain_v1_untracked_all = @(Invoke-GitText -Repository $repositoryPath -Arguments @('status', '--porcelain=v1', '--untracked-files=all'))
        }
    }
    $scopes = @()
    foreach ($sourceCandidate in $SourcePath) { $scopes += Get-ScopeRecord -RequestedPath $sourceCandidate -Kind 'source_allowlist' }
    foreach ($writeCandidate in $WriteRoot) { $scopes += Get-ScopeRecord -RequestedPath $writeCandidate -Kind 'write_root' }
    return [ordered]@{
        schema_version = 1
        captured_utc = [DateTime]::UtcNow.ToString('o')
        repositories = @($repositories)
        scopes = @($scopes)
    }
}

function Get-FlattenedFiles {
    param([Parameter(Mandatory = $true)]$Snapshot)
    $map = @{}
    foreach ($scope in @($Snapshot.scopes)) {
        foreach ($fileRecord in @($scope.files)) {
            $key = [string]$fileRecord.absolute_path
            $map[$key.ToLowerInvariant()] = $fileRecord
        }
    }
    return $map
}

function Test-AllowedWrite {
    param([Parameter(Mandatory = $true)][string]$AbsolutePath)
    foreach ($allowedPath in $script:NormalizedAllowedWrites) {
        if ([string]::Equals((Get-NormalizedFullPath $AbsolutePath), $allowedPath, [System.StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    return $false
}

function New-Diff {
    param([Parameter(Mandatory = $true)]$BeforeSnapshot, [Parameter(Mandatory = $true)]$AfterSnapshot)
    $beforeFiles = Get-FlattenedFiles $BeforeSnapshot
    $afterFiles = Get-FlattenedFiles $AfterSnapshot
    $changes = @()
    foreach ($key in @($beforeFiles.Keys + $afterFiles.Keys | Sort-Object -Unique)) {
        $beforeRecord = $beforeFiles[$key]
        $afterRecord = $afterFiles[$key]
        $changeKind = $null
        if ($null -eq $beforeRecord) { $changeKind = 'added' }
        elseif ($null -eq $afterRecord) { $changeKind = 'removed' }
        elseif (($beforeRecord.sha256 -ne $afterRecord.sha256) -or ($beforeRecord.size -ne $afterRecord.size)) { $changeKind = 'modified' }
        if ($null -ne $changeKind) {
            $displayRecord = if ($null -ne $afterRecord) { $afterRecord } else { $beforeRecord }
            $changes += [ordered]@{
                change = $changeKind
                absolute_path = $displayRecord.absolute_path
                before_sha256 = if ($null -ne $beforeRecord) { $beforeRecord.sha256 } else { $null }
                after_sha256 = if ($null -ne $afterRecord) { $afterRecord.sha256 } else { $null }
                allowed_write = Test-AllowedWrite -AbsolutePath $displayRecord.absolute_path
            }
        }
    }
    $repositoryDrift = @()
    foreach ($beforeRepository in @($BeforeSnapshot.repositories)) {
        $afterRepository = @($AfterSnapshot.repositories | Where-Object { $_.root -eq $beforeRepository.root })
        if ($afterRepository.Count -ne 1) { throw "Repository set changed for $($beforeRepository.root)" }
        if ($beforeRepository.revision -ne $afterRepository[0].revision) {
            $repositoryDrift += [ordered]@{ root = $beforeRepository.root; before_revision = $beforeRepository.revision; after_revision = $afterRepository[0].revision }
        }
    }
    $unauthorized = @($changes | Where-Object { -not $_.allowed_write })
    return [ordered]@{
        schema_version = 1
        changed_files = @($changes)
        unauthorized_changes = @($unauthorized)
        repository_revision_drift = @($repositoryDrift)
        verdict = if (($unauthorized.Count -eq 0) -and ($repositoryDrift.Count -eq 0)) { 'PASS' } else { 'BLOCK' }
    }
}

$script:NormalizedAllowedRoots = @()
foreach ($rootCandidate in $AllowedRoot) {
    if (-not (Test-Path -LiteralPath $rootCandidate -PathType Container)) { throw "Allowed root does not exist or is not a directory: $rootCandidate" }
    $script:NormalizedAllowedRoots += Get-NormalizedFullPath (Resolve-Path -LiteralPath $rootCandidate).ProviderPath
}
$script:ReceiptPath = Get-NormalizedFullPath $ReceiptDirectory
Assert-InAllowedRoots -Candidate $script:ReceiptPath -Description 'receipt directory'
if (-not (Test-Path -LiteralPath $script:ReceiptPath)) {
    New-Item -ItemType Directory -Path $script:ReceiptPath | Out-Null
}
$script:ReceiptPath = Get-ExistingResolvedPath -LiteralPath $script:ReceiptPath -Description 'receipt directory'

$script:NormalizedAllowedWrites = @()
foreach ($writePathCandidate in $AllowedWritePath) {
    $normalizedWrite = Get-NormalizedFullPath $writePathCandidate
    Assert-InAllowedRoots -Candidate $normalizedWrite -Description 'allowed write path'
    $insideWriteRoot = $false
    foreach ($writeRootCandidate in $WriteRoot) {
        if (Test-PathInsideRoot -Candidate $normalizedWrite -Root (Get-NormalizedFullPath $writeRootCandidate)) { $insideWriteRoot = $true; break }
    }
    if (-not $insideWriteRoot) { throw "Allowed write path is outside declared write roots: $normalizedWrite" }
    $script:NormalizedAllowedWrites += $normalizedWrite
}

$beforeFile = Join-Path $script:ReceiptPath 'baseline-before.json'
$afterFile = Join-Path $script:ReceiptPath 'baseline-after.json'
$diffFile = Join-Path $script:ReceiptPath 'baseline-diff.json'

if ($Mode -eq 'Before') {
    if (Test-Path -LiteralPath $beforeFile) { throw "Refusing to overwrite existing receipt: $beforeFile" }
    New-Snapshot | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $beforeFile -Encoding UTF8
    Write-Output $beforeFile
    exit 0
}

if ($Mode -eq 'After') {
    if (-not (Test-Path -LiteralPath $beforeFile)) { throw "Missing before receipt: $beforeFile" }
    if (Test-Path -LiteralPath $afterFile) { throw "Refusing to overwrite existing receipt: $afterFile" }
    if (Test-Path -LiteralPath $diffFile) { throw "Refusing to overwrite existing receipt: $diffFile" }
    $afterSnapshot = New-Snapshot
    $afterSnapshot | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $afterFile -Encoding UTF8
    $beforeSnapshot = Get-Content -Raw -LiteralPath $beforeFile | ConvertFrom-Json
    $diff = New-Diff -BeforeSnapshot $beforeSnapshot -AfterSnapshot $afterSnapshot
    $diff | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $diffFile -Encoding UTF8
    Write-Output $diffFile
    if ($diff.verdict -ne 'PASS') { exit 2 }
    exit 0
}

if (-not (Test-Path -LiteralPath $beforeFile)) { throw "Missing before receipt: $beforeFile" }
if (-not (Test-Path -LiteralPath $afterFile)) { throw "Missing after receipt: $afterFile" }
if (Test-Path -LiteralPath $diffFile) { throw "Refusing to overwrite existing receipt: $diffFile" }
$beforeSnapshot = Get-Content -Raw -LiteralPath $beforeFile | ConvertFrom-Json
$afterSnapshot = Get-Content -Raw -LiteralPath $afterFile | ConvertFrom-Json
$diff = New-Diff -BeforeSnapshot $beforeSnapshot -AfterSnapshot $afterSnapshot
$diff | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $diffFile -Encoding UTF8
Write-Output $diffFile
if ($diff.verdict -ne 'PASS') { exit 2 }
