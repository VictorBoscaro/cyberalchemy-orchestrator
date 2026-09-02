<#
.SYNOPSIS
Installs or verifies the canonical register-dispatch runtime package in a repository.

.DESCRIPTION
The closed package manifest pins every installed runtime file by SHA-256. Installation
rejects reparse points in existing source/destination path chains and never reads or
writes telemetry. Use -Check to detect missing files or drift without mutation.

.EXAMPLE
powershell -ExecutionPolicy Bypass -File tools/install-register-dispatch-runtime.ps1 -Target C:\path\to\repo

.EXAMPLE
powershell -ExecutionPolicy Bypass -File tools/install-register-dispatch-runtime.ps1 -Target C:\path\to\repo -Check
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Target,

    [switch]$Check,

    [switch]$LegacyVerification
)

$ErrorActionPreference = 'Stop'

function Assert-ExactProperties {
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string[]]$Expected,
        [Parameter(Mandatory = $true)][string]$Label
    )
    if ($null -eq $Object -or $Object -isnot [psobject]) {
        throw "$Label must be an object."
    }
    $actual = @($Object.PSObject.Properties.Name)
    $difference = @(Compare-Object -ReferenceObject $Expected -DifferenceObject $actual)
    if ($difference.Count -gt 0) {
        $rendered = ($actual | Sort-Object) -join ', '
        throw "$Label has an invalid property set: $rendered"
    }
}

function Assert-ContainedPath {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Label
    )
    $rootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd('\', '/')
    $pathFull = [System.IO.Path]::GetFullPath($Path)
    $prefix = $rootFull + [System.IO.Path]::DirectorySeparatorChar
    if (-not $pathFull.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "$Label escapes its declared root: $pathFull"
    }
    return $pathFull
}

function Assert-NoReparsePoints {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Label
    )
    $full = [System.IO.Path]::GetFullPath($Path)
    $qualifier = Split-Path -Qualifier $full
    if ([string]::IsNullOrWhiteSpace($qualifier)) {
        throw "$Label has no filesystem qualifier: $full"
    }
    $current = $qualifier
    $segments = $full.Substring($qualifier.Length).TrimStart('\', '/') -split '[\\/]'
    foreach ($segment in $segments) {
        if ([string]::IsNullOrWhiteSpace($segment)) { continue }
        $current = Join-Path $current $segment
        if (-not (Test-Path -LiteralPath $current)) { break }
        $item = Get-Item -LiteralPath $current -Force
        if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "$Label traverses a reparse point: $current"
        }
    }
}

$sourceRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..')).TrimEnd('\', '/')
$targetRoot = [System.IO.Path]::GetFullPath($Target).TrimEnd('\', '/')
$manifestRelative = if ($LegacyVerification) {
    if (-not $Check) {
        throw 'Legacy v1 is verification-only; use -LegacyVerification together with -Check.'
    }
    'implementations/contracts/register-dispatch-runtime-package.v1.json'
} else {
    'implementations/contracts/register-dispatch-runtime-package.v2.json'
}
$manifestPath = Assert-ContainedPath -Root $sourceRoot -Path (Join-Path $sourceRoot $manifestRelative) -Label 'manifest source'

Assert-NoReparsePoints -Path $sourceRoot -Label 'source root'
Assert-NoReparsePoints -Path $manifestPath -Label 'manifest source'
Assert-NoReparsePoints -Path $targetRoot -Label 'target root'
if (-not (Test-Path -LiteralPath $targetRoot -PathType Container)) {
    throw "Target repository does not exist: $targetRoot"
}
$gitMarker = Assert-ContainedPath -Root $targetRoot -Path (Join-Path $targetRoot '.git') -Label 'target git marker'
Assert-NoReparsePoints -Path $gitMarker -Label 'target git marker'
if (-not (Test-Path -LiteralPath $gitMarker)) {
    throw "Target is not a repository root: $targetRoot"
}

$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$manifestKeys = if ($LegacyVerification) {
    @('schema', 'canonical_source', 'package_version', 'registry_schema', 'ledger_schema_version', 'files')
} else {
    @('schema', 'canonical_source', 'package_version', 'registry_schema', 'ledger_schema_version', 'agent_role_registry_ref', 'files')
}
Assert-ExactProperties -Object $manifest -Expected $manifestKeys -Label 'package manifest'
$expectedPackageSchema = if ($LegacyVerification) { 'register-dispatch-runtime-package/v1' } else { 'register-dispatch-runtime-package/v2' }
if ($manifest.schema -ne $expectedPackageSchema) {
    throw "Unsupported package manifest schema: $($manifest.schema)"
}
if ($manifest.canonical_source -ne 'cyberalchemy-orchestrator') {
    throw "Unexpected canonical_source: $($manifest.canonical_source)"
}
if ($manifest.package_version -notmatch '^\d+\.\d+\.\d+$') {
    throw "package_version must be a semantic numeric version: $($manifest.package_version)"
}
# Policy: the runtime package and ledger schema advance in lockstep.
if ($manifest.package_version -ne $manifest.ledger_schema_version) {
    throw 'package_version must exactly equal ledger_schema_version.'
}
$expectedRegistrySchema = if ($LegacyVerification) { 'aci-dispatch-type-registry/v1' } else { 'aci-dispatch-type-registry/v2' }
if ($manifest.registry_schema -ne $expectedRegistrySchema) {
    throw "Unsupported registry_schema: $($manifest.registry_schema)"
}
if ($manifest.files -isnot [System.Array] -or $manifest.files.Count -eq 0) {
    throw 'Package manifest files must be a non-empty array.'
}

$requiredFiles = @(
    '.claude/skills/register-dispatch/SKILL.md',
    '.claude/skills/register-dispatch/append-dispatch.cjs',
    '.claude/skills/register-dispatch/agents/openai.yaml'
)
$requiredFiles += if ($LegacyVerification) {
    @('implementations/contracts/dispatch-type-registry.v1.json')
} else {
    @(
        'implementations/contracts/dispatch-type-registry.v2.json',
        'implementations/contracts/dispatch-ledger-row.v0.7.0.schema.json',
        'implementations/contracts/agent-role-registry.v1.json',
        'implementations/contracts/agent-role-registry-authority.v1.json',
        'implementations/contracts/agent-role-host-routing.v1.json'
    )
}
$seenPaths = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($entry in $manifest.files) {
    Assert-ExactProperties -Object $entry -Expected @('path', 'sha256') -Label 'package file entry'
    if ($entry.path -isnot [string] -or $entry.path -notmatch '^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*$' -or
        [System.IO.Path]::IsPathRooted($entry.path) -or $entry.path -match '(^|/)\.\.(/|$)') {
        throw "Unsafe package path: $($entry.path)"
    }
    if (-not $seenPaths.Add([string]$entry.path)) {
        throw "Duplicate package path: $($entry.path)"
    }
    if ($entry.sha256 -isnot [string] -or $entry.sha256 -notmatch '^[0-9A-Fa-f]{64}$') {
        throw "Invalid SHA-256 for package path $($entry.path)"
    }
}
$declaredFiles = @($manifest.files | ForEach-Object { [string]$_.path })
$fileSetDifference = @(Compare-Object -ReferenceObject ($requiredFiles | Sort-Object) -DifferenceObject ($declaredFiles | Sort-Object))
if ($fileSetDifference.Count -gt 0) {
    throw 'Package manifest must declare exactly the required register-dispatch runtime files.'
}

$registryPath = if ($LegacyVerification) {
    'implementations/contracts/dispatch-type-registry.v1.json'
} else {
    'implementations/contracts/dispatch-type-registry.v2.json'
}
$registryEntry = $manifest.files | Where-Object { $_.path -eq $registryPath }
$registrySource = Assert-ContainedPath -Root $sourceRoot -Path (Join-Path $sourceRoot $registryEntry.path) -Label 'registry source'
Assert-NoReparsePoints -Path $registrySource -Label 'registry source'
$registry = Get-Content -LiteralPath $registrySource -Raw | ConvertFrom-Json
if ($registry.schema -ne $manifest.registry_schema -or
    $registry.ledger_schema_version -ne $manifest.ledger_schema_version) {
    throw 'Package version does not match the canonical registry schema/version.'
}
if (-not $LegacyVerification) {
    Assert-ExactProperties -Object $manifest.agent_role_registry_ref -Expected @('name', 'version', 'digest') -Label 'package agent_role_registry_ref'
    Assert-ExactProperties -Object $registry.agent_role_registry_ref -Expected @('name', 'version', 'digest') -Label 'registry agent_role_registry_ref'
    if (($manifest.agent_role_registry_ref | ConvertTo-Json -Compress) -ne
        ($registry.agent_role_registry_ref | ConvertTo-Json -Compress)) {
        throw 'Package role registry ref does not match the dispatch registry.'
    }
}

$failures = [System.Collections.Generic.List[string]]::new()
foreach ($entry in $manifest.files) {
    $relative = [string]$entry.path
    $source = Assert-ContainedPath -Root $sourceRoot -Path (Join-Path $sourceRoot $relative) -Label "source $relative"
    $destination = Assert-ContainedPath -Root $targetRoot -Path (Join-Path $targetRoot $relative) -Label "destination $relative"
    Assert-NoReparsePoints -Path $source -Label "source $relative"
    Assert-NoReparsePoints -Path $destination -Label "destination $relative"
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
        throw "Canonical package file is missing: $source"
    }

    $sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
    if ($sourceHash -ne ([string]$entry.sha256).ToUpperInvariant()) {
        throw "Canonical source digest mismatch for ${relative}: expected $($entry.sha256), got $sourceHash"
    }

    if ($Check) {
        if (-not (Test-Path -LiteralPath $destination -PathType Leaf)) {
            $failures.Add("missing: $relative")
            continue
        }
        $destinationHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
        if ($destinationHash -ne $sourceHash) {
            $failures.Add("digest mismatch: $relative")
        }
        continue
    }

    $destinationDirectory = Split-Path -Parent $destination
    New-Item -ItemType Directory -Path $destinationDirectory -Force | Out-Null
    Assert-NoReparsePoints -Path $destination -Label "destination $relative after directory creation"
    Copy-Item -LiteralPath $source -Destination $destination -Force
    Assert-NoReparsePoints -Path $destination -Label "installed $relative"
    $installedHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
    if ($installedHash -ne $sourceHash) {
        throw "Installed digest mismatch for $relative"
    }
    Write-Output "installed $relative $installedHash"
}

$manifestDestination = Assert-ContainedPath -Root $targetRoot -Path (Join-Path $targetRoot $manifestRelative) -Label 'manifest destination'
Assert-NoReparsePoints -Path $manifestDestination -Label 'manifest destination'
if ($Check) {
    if (-not (Test-Path -LiteralPath $manifestDestination -PathType Leaf)) {
        $failures.Add("missing: $manifestRelative")
    } elseif ((Get-FileHash -LiteralPath $manifestDestination -Algorithm SHA256).Hash -ne
              (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash) {
        $failures.Add("digest mismatch: $manifestRelative")
    }
    if ($failures.Count -gt 0) {
        $failures | ForEach-Object { [Console]::Error.WriteLine($_) }
        exit 2
    }
    Write-Output "verified register-dispatch runtime $($manifest.package_version) at $targetRoot"
    exit 0
}

$manifestDirectory = Split-Path -Parent $manifestDestination
New-Item -ItemType Directory -Path $manifestDirectory -Force | Out-Null
Assert-NoReparsePoints -Path $manifestDestination -Label 'manifest destination after directory creation'
Copy-Item -LiteralPath $manifestPath -Destination $manifestDestination -Force
Assert-NoReparsePoints -Path $manifestDestination -Label 'installed manifest'
$manifestHash = (Get-FileHash -LiteralPath $manifestDestination -Algorithm SHA256).Hash
if ($manifestHash -ne (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash) {
    throw 'Installed package manifest digest mismatch.'
}
Write-Output "installed $manifestRelative $manifestHash"
Write-Output "installed register-dispatch runtime $($manifest.package_version) at $targetRoot"
