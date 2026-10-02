#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  💰 Finance Dashboard"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Backend ──────────────────────────────────
echo ""
echo "▶ Starting Backend (FastAPI)..."

if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo "  Creating Python virtual environment..."
    python3 -m venv "$BACKEND_DIR/venv"
fi

source "$BACKEND_DIR/venv/bin/activate"
pip install -r "$BACKEND_DIR/requirements.txt" -q
echo "  ✅ Backend dependencies ready"

cd "$BACKEND_DIR"
PYTHONPATH="$BACKEND_DIR" uvicorn main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
echo "  ✅ Backend running → http://localhost:8000"
echo "  📖 API docs       → http://localhost:8000/docs"

# Wait for backend to be ready
sleep 3

# ── Frontend ─────────────────────────────────
echo ""
echo "▶ Starting Frontend (React + Vite)..."

cd "$FRONTEND_DIR"

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "  Installing npm packages (first run, takes ~1 min)..."
    npm install --silent
fi

echo "  ✅ Frontend dependencies ready"
npm run dev &
FRONTEND_PID=$!
echo "  ✅ Frontend running → http://localhost:5173"

# ── Summary ───────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 App is running!"
echo ""
echo "  Open in browser → http://localhost:5173"
echo ""
echo "  Press Ctrl+C to stop both servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Keep running — kill both on Ctrl+C
trap "echo ''; echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT
wait
