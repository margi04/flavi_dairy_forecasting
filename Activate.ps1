# This script activates the Python virtual environment for this project.
# Usage: Run this script in PowerShell to activate the venv.

$venvRoot = Join-Path $PSScriptRoot ".."
$venvScripts = Join-Path $venvRoot ".venv\Scripts"
$venvPath = Join-Path $venvScripts "Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
} else {
    Write-Host 'Virtual environment activation script not found. Please create the venv first.'
}
