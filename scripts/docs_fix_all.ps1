param(
    [string]$DocsDir = "docs"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$fixScript = Join-Path $repoRoot ".agent/skills/mintlify-markdown-kb/scripts/auto_fix_frontmatter.py"
$checkScript = Join-Path $repoRoot ".agent/skills/mintlify-markdown-kb/scripts/check_frontmatter_titles.py"

Write-Host "[1/2] Auto-fixing frontmatter issues..." -ForegroundColor Cyan
python $fixScript --docs-dir $DocsDir
if ($LASTEXITCODE -ne 0) {
    Write-Error "Auto-fix failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "[2/2] Running consistency checks..." -ForegroundColor Cyan
python $checkScript --docs-dir $DocsDir
$checkExit = $LASTEXITCODE

if ($checkExit -eq 0) {
    Write-Host "Done: all checks passed." -ForegroundColor Green
} else {
    Write-Host "Done: checks found remaining issues (see output above)." -ForegroundColor Yellow
}

exit $checkExit
