<#
.SYNOPSIS
    Builds the uploadable release assets from source.

.DESCRIPTION
    One asset per skill, in the form Copilot Studio stores best:

      single SKILL.md   -> <name>.md   stored inline, readable by the agent
      anything bundled  -> <name>.zip  SKILL.md at the archive root

    Zips are written with System.IO.Compression.ZipFile and explicit
    forward-slash entry names. Compress-Archive writes backslashes, which the
    ZIP format does not allow and Copilot Studio can refuse with no useful
    error - see docs/research/copilot-studio-skill-contract.md.

.EXAMPLE
    pwsh scripts/build-release.ps1
    pwsh scripts/build-release.ps1 -OutputDir dist -Verify
#>
[CmdletBinding()]
param(
    [string] $OutputDir = 'dist',
    [switch] $Verify
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

$repoRoot = Split-Path -Parent $PSScriptRoot
$outPath = if ([System.IO.Path]::IsPathRooted($OutputDir)) { $OutputDir } else { Join-Path $repoRoot $OutputDir }

if (Test-Path $outPath) { Remove-Item $outPath -Recurse -Force }
New-Item -ItemType Directory -Path $outPath | Out-Null

$sourceDirs = @(
    (Join-Path $repoRoot 'skills'),
    (Join-Path $repoRoot 'diagnostics')
) | Where-Object { Test-Path $_ }

$results = foreach ($sourceDir in $sourceDirs) {
    foreach ($skillDir in Get-ChildItem -Path $sourceDir -Directory) {
        $manifest = Join-Path $skillDir.FullName 'SKILL.md'
        if (-not (Test-Path $manifest)) {
            throw "$($skillDir.Name): no SKILL.md"
        }

        # The frontmatter name is what Copilot Studio installs the skill as.
        # It must match the folder, or two skills can collide in one agent.
        $head = Get-Content -LiteralPath $manifest -TotalCount 10 -Encoding utf8
        $match = @($head | Select-String -Pattern '^name:\s*(\S+)\s*$')
        if ($match.Count -ne 1) {
            throw "$($skillDir.Name): SKILL.md has no single 'name:' line in its frontmatter"
        }
        $declared = $match[0].Matches[0].Groups[1].Value
        if ($declared -ne $skillDir.Name) {
            throw "$($skillDir.Name): frontmatter name is '$declared', folder is '$($skillDir.Name)'"
        }

        $payload = @(Get-ChildItem -Path $skillDir.FullName -Recurse -File)
        $bundled = @($payload | Where-Object { $_.FullName -ne $manifest })

        if ($bundled.Count -eq 0) {
            $asset = Join-Path $outPath "$($skillDir.Name).md"
            Copy-Item -LiteralPath $manifest -Destination $asset
        }
        else {
            $asset = Join-Path $outPath "$($skillDir.Name).zip"
            $archive = [System.IO.Compression.ZipFile]::Open($asset, 'Create')
            try {
                foreach ($file in $payload) {
                    $entryName = $file.FullName.Substring($skillDir.FullName.Length + 1).Replace('\', '/')
                    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                        $archive, $file.FullName, $entryName) | Out-Null
                }
            }
            finally { $archive.Dispose() }
        }

        [pscustomobject]@{
            Skill = $skillDir.Name
            Asset = Split-Path $asset -Leaf
            Files = $payload.Count
            Bytes = (Get-Item $asset).Length
        }
    }
}

$results | Format-Table -AutoSize

if ($Verify) {
    foreach ($zip in Get-ChildItem -Path $outPath -Filter *.zip) {
        $archive = [System.IO.Compression.ZipFile]::OpenRead($zip.FullName)
        try {
            $names = @($archive.Entries | ForEach-Object { $_.FullName })
            if ($names -notcontains 'SKILL.md') { throw "$($zip.Name): SKILL.md is not at the archive root" }
            $bad = @($names | Where-Object { $_ -match '\\' })
            if ($bad.Count -gt 0) { throw "$($zip.Name): backslash entry names: $($bad -join ', ')" }
        }
        finally { $archive.Dispose() }
        Write-Host "ok  $($zip.Name)"
    }
    foreach ($md in Get-ChildItem -Path $outPath -Filter *.md) {
        $bytes = [System.IO.File]::ReadAllBytes($md.FullName)
        if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
            throw "$($md.Name): UTF-8 BOM - Copilot Studio cannot read the file"
        }
        Write-Host "ok  $($md.Name)"
    }
}
