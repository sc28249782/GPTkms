$bundledNode = "C:\Users\sc282\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
$repoRoot = Split-Path -Parent $PSScriptRoot
$testName = if ($args.Length -gt 0) { $args[0] } else { "browser-smoke.mjs" }
$testFile = Join-Path $repoRoot ("tests\" + $testName)

if (Test-Path $bundledNode) {
    & $bundledNode $testFile
    exit $LASTEXITCODE
}

& node $testFile
exit $LASTEXITCODE
