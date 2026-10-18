#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "   NEXUS GRAPH AI: Environment Initialization (Linux)"
echo "=========================================================="

# 1. Verify Python & Node
python3 --version
node -v

# 2. Virtual Environment
if [ ! -d "backend/.venv" ]; then
    python3 -m venv backend/.venv
fi
source backend/.venv/bin/activate
pip install -r backend/requirements.txt

# 3. Environment Config
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

# 4. Seed Data
python3 scripts/seed_demo.py

# 5. Run Benchmarks
python3 scripts/evaluate.py

echo "=========================================================="
echo "   NEXUS GRAPH AI Setup Complete!"
echo "   Start Backend:  source backend/.venv/bin/activate && cd backend && uvicorn app.main:app --reload --port 8000"
echo "   Start Frontend: cd frontend && npm run dev"
echo "=========================================================="
