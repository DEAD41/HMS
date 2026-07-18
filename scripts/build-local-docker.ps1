$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "Building and testing Healthcare ERP..."
dotnet build "HealthcareERP.sln" --configuration Release --no-restore
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

dotnet test "HealthcareERP.sln" --configuration Release --no-build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Publishing API artifacts..."
dotnet publish "src/Host/HealthcareERP.Api/HealthcareERP.Api.csproj" `
    --configuration Release `
    --no-restore `
    --output "artifacts/api"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Building and starting local Docker services..."
docker compose up --build --detach
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
docker compose ps
