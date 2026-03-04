Write-Host "Initialisation de la base de donnees..." -ForegroundColor Cyan

# Upgrade schema
Write-Host "Application des migrations..." -ForegroundColor Yellow
docker compose -f docker-compose.dev.yml exec backend flask db upgrade

if ($LASTEXITCODE -ne 0) {
    Write-Error "Erreur lors de l'application des migrations."
    exit $LASTEXITCODE
}

# Seed data
Write-Host "Peuplement de la base de donnees..." -ForegroundColor Yellow
powershell.exe -File .\seed.ps1 -Mode docker

if ($LASTEXITCODE -ne 0) {
    Write-Error "Erreur lors du peuplement de la base de donnees."
    exit $LASTEXITCODE
}

Write-Host "Base de donnees initialisee avec succes !" -ForegroundColor Green
