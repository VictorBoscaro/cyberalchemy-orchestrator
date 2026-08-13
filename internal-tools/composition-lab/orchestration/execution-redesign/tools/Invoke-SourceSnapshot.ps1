[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Create', 'Verify', 'Cleanup')]
    [string]$Mode,

    [Parameter(Mandatory = $true)]
    [string]$SnapshotParent,

    [string]$SourceRepository,
    [string]$ManifestPath,
    [ValidateSet('D1', 'D3', 'D4')]
    [string]$Batch,
    [string]$SnapshotPath
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

function Get-FullPath([string]$Path) {
    return [IO.Path]::GetFullPath($Path).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
}

function Assert-SafeParent([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) { throw "Snapshot parent does not exist: $Path" }
    $resolved = Get-FullPath (Resolve-Path -LiteralPath $Path).ProviderPath
    $temporary = Get-FullPath ([IO.Path]::GetTempPath())
    if (-not ($resolved -eq $temporary -or $resolved.StartsWith($temporary + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase))) {
        throw "Snapshot parent must be inside the system temporary directory: $resolved"
    }
    $cursor = Get-Item -LiteralPath $resolved -Force
    while ($null -ne $cursor -and (Get-FullPath $cursor.FullName).StartsWith($temporary, [StringComparison]::OrdinalIgnoreCase)) {
        if (($cursor.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw "Reparse point forbidden in snapshot parent: $($cursor.FullName)" }
        if ((Get-FullPath $cursor.FullName) -eq $temporary) { break }
        $cursor = $cursor.Parent
    }
    return $resolved
}

function Assert-SafeSnapshot([string]$Parent, [string]$Path) {
    $full = Get-FullPath $Path
    if (-not $full.StartsWith($Parent + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw "Snapshot escapes parent: $full" }
    $relative = $full.Substring($Parent.Length + 1)
    if ($relative.Contains([IO.Path]::DirectorySeparatorChar) -or -not $relative.StartsWith('composition-lab-snapshot-', [StringComparison]::OrdinalIgnoreCase)) {
        throw "Snapshot must be a direct, prefixed child of its parent: $full"
    }
    return $full
}

function Invoke-Git([string]$Repository, [string[]]$Arguments) {
    $result = & git -C $Repository @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) { throw "git failed ($($Arguments -join ' ')): $($result -join [Environment]::NewLine)" }
    return @($result | ForEach-Object { $_.ToString() })
}

function Get-VerifiedManifest([string]$Path, [string]$BatchName, [string]$Repository) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Manifest not found: $Path" }
    $manifest = Get-Content -Raw -LiteralPath $Path | ConvertFrom-Json
    if ($manifest.schema_version -ne 1) { throw 'Unsupported source manifest schema' }
    $resolvedCommit = ((Invoke-Git $Repository @('rev-parse', "$($manifest.source_revision)^{commit}")) -join '').Trim()
    if ($resolvedCommit -ne $manifest.source_revision) { throw "Pinned revision mismatch: $resolvedCommit" }
    $tree = ((Invoke-Git $Repository @('rev-parse', "$($manifest.source_revision)^{tree}")) -join '').Trim()
    if ($tree -ne $manifest.source_tree) { throw "Pinned tree mismatch: $tree" }
    $files = @($manifest.batches.$BatchName)
    if ($files.Count -ne 3) { throw "$BatchName must contain exactly three files" }
    $paths = @($files | ForEach-Object { [string]$_.path })
    if (($paths | Sort-Object -Unique).Count -ne 3) { throw "Duplicate path in $BatchName" }
    return [ordered]@{ manifest = $manifest; files = $files; commit = $resolvedCommit; tree = $tree }
}

function Test-Snapshot([string]$Path, [switch]$ThrowOnFailure) {
    $receiptPath = Join-Path $Path 'snapshot-manifest.json'
    $digestPath = Join-Path $Path 'snapshot-manifest.sha256'
    if (-not (Test-Path -LiteralPath $receiptPath -PathType Leaf) -or -not (Test-Path -LiteralPath $digestPath -PathType Leaf)) { throw 'Snapshot receipt or digest missing' }
    $receiptHash = (Get-FileHash -LiteralPath $receiptPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $expectedReceiptHash = (Get-Content -Raw -LiteralPath $digestPath).Trim().ToLowerInvariant()
    if ($receiptHash -ne $expectedReceiptHash) { throw 'Snapshot receipt digest mismatch' }
    $receipt = Get-Content -Raw -LiteralPath $receiptPath | ConvertFrom-Json
    $archive = Join-Path $Path 'source.zip'
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $receipt.archive_sha256) { throw 'Archive digest mismatch' }
    foreach ($file in @($receipt.files)) {
        $materialized = Join-Path (Join-Path $Path 'tree') ($file.path.Replace('/', [IO.Path]::DirectorySeparatorChar))
        if (-not (Test-Path -LiteralPath $materialized -PathType Leaf)) { throw "Snapshot file missing: $($file.path)" }
        $item = Get-Item -LiteralPath $materialized
        $sha = (Get-FileHash -LiteralPath $materialized -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($item.Length -ne $file.bytes -or $sha -ne $file.sha256) { throw "Snapshot file drift: $($file.path)" }
        $blob = ((Invoke-Git $receipt.source_repository @('hash-object', '--no-filters', '--', $materialized)) -join '').Trim()
        if ($blob -ne $file.blob) { throw "Blob equivalence failed: $($file.path)" }
    }
    return [ordered]@{ verdict = 'PASS'; snapshot_path = $Path; batch = $receipt.batch; files = @($receipt.files).Count }
}

$parent = Assert-SafeParent $SnapshotParent

if ($Mode -eq 'Cleanup') {
    if ([string]::IsNullOrWhiteSpace($SnapshotPath)) { throw 'SnapshotPath is required for Cleanup' }
    $target = Assert-SafeSnapshot $parent $SnapshotPath
    if (-not (Test-Path -LiteralPath $target -PathType Container)) { throw "Snapshot does not exist: $target" }
    Get-ChildItem -LiteralPath $target -File -Recurse -Force | ForEach-Object { $_.IsReadOnly = $false }
    Remove-Item -LiteralPath $target -Recurse -Force
    [ordered]@{ verdict = 'CLEANED'; snapshot_path = $target } | ConvertTo-Json -Compress
    exit 0
}

if ($Mode -eq 'Verify') {
    if ([string]::IsNullOrWhiteSpace($SnapshotPath)) { throw 'SnapshotPath is required for Verify' }
    $target = Assert-SafeSnapshot $parent $SnapshotPath
    Test-Snapshot $target | ConvertTo-Json -Depth 6 -Compress
    exit 0
}

if ([string]::IsNullOrWhiteSpace($SourceRepository) -or [string]::IsNullOrWhiteSpace($ManifestPath) -or [string]::IsNullOrWhiteSpace($Batch)) {
    throw 'SourceRepository, ManifestPath and Batch are required for Create'
}
$repository = Get-FullPath (Resolve-Path -LiteralPath $SourceRepository).ProviderPath
$binding = Get-VerifiedManifest $ManifestPath $Batch $repository
$identity = "composition-lab-snapshot-$($Batch.ToLowerInvariant())-$($binding.commit.Substring(0,12))-$([Guid]::NewGuid().ToString('N'))"
$staging = Join-Path $parent (".staging-" + $identity)
$final = Join-Path $parent $identity
New-Item -ItemType Directory -Path $staging | Out-Null
try {
    $archive = Join-Path $staging 'source.zip'
    $paths = @($binding.files | ForEach-Object { [string]$_.path })
    Invoke-Git $repository (@('archive', '--format=zip', "--output=$archive", $binding.commit, '--') + $paths) | Out-Null
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip = [IO.Compression.ZipFile]::OpenRead($archive)
    try {
        $entries = @($zip.Entries | Where-Object { -not $_.FullName.EndsWith('/') })
        $entryNames = @($entries | ForEach-Object { $_.FullName })
        $sortedEntryNames = (@($entryNames | Sort-Object) -join "`n")
        $sortedPaths = (@($paths | Sort-Object) -join "`n")
        if ($sortedEntryNames -ne $sortedPaths) { throw 'Archive member set differs from manifest' }
        $treeRoot = Join-Path $staging 'tree'
        New-Item -ItemType Directory -Path $treeRoot | Out-Null
        foreach ($entry in $entries) {
            $segments = @($entry.FullName -split '/')
            if ([IO.Path]::IsPathRooted($entry.FullName) -or $segments -contains '..' -or $segments -contains '.' -or $entry.FullName.Contains('\')) { throw "Unsafe archive member: $($entry.FullName)" }
            $destination = Join-Path $treeRoot ($entry.FullName.Replace('/', [IO.Path]::DirectorySeparatorChar))
            $destinationParent = Split-Path -Parent $destination
            New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
            [IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $destination, $false)
        }
    } finally { $zip.Dispose() }

    $records = @()
    foreach ($expected in $binding.files) {
        $materialized = Join-Path (Join-Path $staging 'tree') ($expected.path.Replace('/', [IO.Path]::DirectorySeparatorChar))
        $item = Get-Item -LiteralPath $materialized
        $sha = (Get-FileHash -LiteralPath $materialized -Algorithm SHA256).Hash.ToLowerInvariant()
        $blob = ((Invoke-Git $repository @('rev-parse', "$($binding.commit):$($expected.path)")) -join '').Trim()
        $actualBlob = ((Invoke-Git $repository @('hash-object', '--no-filters', '--', $materialized)) -join '').Trim()
        if ($item.Length -ne [int64]$expected.bytes -or $sha -ne $expected.sha256 -or $actualBlob -ne $blob) { throw "Source binding failed: $($expected.path)" }
        $records += [ordered]@{ path = $expected.path; blob = $blob; bytes = [int64]$item.Length; sha256 = $sha }
        $item.IsReadOnly = $true
    }
    $receipt = [ordered]@{
        schema_version = 1; verdict = 'READY_FOR_READ'; batch = $Batch
        source_repository = $repository; source_revision = $binding.commit; source_tree = $binding.tree
        archive_sha256 = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant()
        files = @($records)
    }
    $receiptPath = Join-Path $staging 'snapshot-manifest.json'
    $receipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $receiptPath -Encoding UTF8
    (Get-FileHash -LiteralPath $receiptPath -Algorithm SHA256).Hash.ToLowerInvariant() | Set-Content -LiteralPath (Join-Path $staging 'snapshot-manifest.sha256') -Encoding ASCII
    Move-Item -LiteralPath $staging -Destination $final
    Test-Snapshot $final | ConvertTo-Json -Depth 6 -Compress
} catch {
    if (Test-Path -LiteralPath $staging) {
        Get-ChildItem -LiteralPath $staging -File -Recurse -Force | ForEach-Object { $_.IsReadOnly = $false }
        Remove-Item -LiteralPath $staging -Recurse -Force
    }
    throw
}
