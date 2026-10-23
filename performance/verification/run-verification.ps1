param(
    [ValidateSet('original','tuned')][string]$Variant = 'original',
    [ValidateSet('smoke','baseline','spike')][string]$Test = 'smoke'
)
$ErrorActionPreference = 'Stop'
node "$PSScriptRoot/run-verification.cjs" $Variant $Test
exit $LASTEXITCODE
