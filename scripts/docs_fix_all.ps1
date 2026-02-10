param(
    [string]$DocsDir = "docs",
    [switch]$ApplyFix
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$fixScript = Join-Path $repoRoot ".agent/skills/mintlify-markdown-kb/scripts/auto_fix_frontmatter.py"
$checkScript = Join-Path $repoRoot ".agent/skills/mintlify-markdown-kb/scripts/check_frontmatter_titles.py"
$introStyleCheckScript = Join-Path $repoRoot "scripts/check_doc_intro_style.py"

if ($ApplyFix) {
    Write-Host "[1/3] Auto-fixing frontmatter issues..." -ForegroundColor Cyan
    python $fixScript --docs-dir $DocsDir
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Auto-fix failed with exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }
} else {
    Write-Host "[skip] Auto-fix disabled. Use -ApplyFix to enable frontmatter auto-fix." -ForegroundColor DarkYellow
}

Write-Host "[check] Running consistency checks..." -ForegroundColor Cyan
python $checkScript --docs-dir $DocsDir
$checkExit = $LASTEXITCODE

Write-Host "[check] Running intro style checks..." -ForegroundColor Cyan
python $introStyleCheckScript --root $DocsDir
$introCheckExit = $LASTEXITCODE

$finalExit = 0
if ($checkExit -ne 0 -or $introCheckExit -ne 0) {
    $finalExit = 1
}

if ($finalExit -eq 0) {
    Write-Host "Done: all checks passed." -ForegroundColor Green
} else {
    Write-Host "Done: checks found remaining issues (see output above)." -ForegroundColor Yellow
}

exit $finalExit
