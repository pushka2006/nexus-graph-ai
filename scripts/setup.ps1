# NEXUS GRAPH AI - Automated Setup Script for Windows PowerShell
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   NEXUS GRAPH AI: Environment Initialization" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check Python
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python 3.11+ is required but not found in PATH."
    exit 1
}
Write-Host "[OK] Detected: $pythonVersion" -ForegroundColor Green

# 2. Check Node
$nodeVersion = node -v 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Node.js 18+ is required but not found in PATH."
    exit 1
}
Write-Host "[OK] Detected Node.js: $nodeVersion" -ForegroundColor Green

# 3. Setup Backend venv
Write-Host "`nSetting up Python virtual environment in backend\.venv..." -ForegroundColor Yellow
if (-not (Test-Path "backend\.venv")) {
    python -m venv backend\.venv
}
Write-Host "[OK] Virtual environment created." -ForegroundColor Green

Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
backend\.venv\Scripts\pip install -r backend\requirements.txt
Write-Host "[OK] Backend dependencies installed." -ForegroundColor Green

# 4. Copy Environment configuration
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] Generated .env file from .env.example." -ForegroundColor Green
}

# 5. Seed Knowledge Graph
Write-Host "`nSeeding FalkorDB Knowledge Graph with NexusWorks dataset..." -ForegroundColor Yellow
backend\.venv\Scripts\python scripts\seed_demo.py

# 6. Run Self-Check Benchmarks
Write-Host "`nRunning Acceptance & Benchmark Suite..." -ForegroundColor Yellow
backend\.venv\Scripts\python scripts\evaluate.py

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "   NEXUS GRAPH AI Setup Complete!" -ForegroundColor Green
Write-Host "   Start Backend:  backend\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000"
Write-Host "   Start Frontend: cd frontend; npm run dev"
Write-Host "==========================================================" -ForegroundColor Cyan
