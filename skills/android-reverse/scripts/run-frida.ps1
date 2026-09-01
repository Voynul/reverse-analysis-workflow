param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Tool,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ToolArguments
)

$ErrorActionPreference = "Stop"
$environmentName = "android"

$defaultCondaExe = Join-Path $env:USERPROFILE "miniconda3\Scripts\conda.exe"
$pathCondaCommand = Get-Command conda.exe -CommandType Application -ErrorAction SilentlyContinue |
    Select-Object -First 1
$condaExe = @($defaultCondaExe, $pathCondaCommand.Source) |
    Where-Object { $_ -and (Test-Path -LiteralPath $_) } |
    Select-Object -First 1

if (-not $condaExe) {
    throw "Conda executable was not found on PATH or at: $defaultCondaExe"
}

$environmentList = (& $condaExe env list --json | ConvertFrom-Json).envs
$environmentPath = $environmentList |
    Where-Object { (Split-Path $_ -Leaf) -eq $environmentName } |
    Select-Object -First 1

if (-not $environmentPath) {
    throw "Conda environment '$environmentName' was not found."
}

$toolName = if ($Tool.EndsWith(".exe", [System.StringComparison]::OrdinalIgnoreCase)) {
    $Tool
} else {
    "$Tool.exe"
}

$toolPath = Join-Path $environmentPath "Scripts\$toolName"
if (-not (Test-Path -LiteralPath $toolPath)) {
    throw "Tool '$Tool' was not found in Conda environment '$environmentName': $toolPath"
}

& $toolPath @ToolArguments
exit $LASTEXITCODE
