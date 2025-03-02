
$projectPath = "C:\Projects\BB_BE"
$venvPath = "$projectPath\.venv\Scripts\activate.ps1"


if (-Not (Test-Path $projectPath)) {
    Write-Host "There is no folder ($projectPath)."
    exit 1
}

Set-Location $projectPath


if (Test-Path $venvPath) {
    & $venvPath
} else {
    Write-Host "Error with virtual env"
    exit 1
}

# Run Flask
flask run
