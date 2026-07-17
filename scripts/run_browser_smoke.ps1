$bundledNode = "C:\Users\sc282\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
$repoRoot = Split-Path -Parent $PSScriptRoot
$testFile = Join-Path $repoRoot "tests\browser-smoke.mjs"

if (Test-Path $bundledNode) {
    & $bundledNode $testFile
    exit $LASTEXITCODE
}

& node $testFile
exit $LASTEXITCODE

