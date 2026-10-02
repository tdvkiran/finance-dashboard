#!/bin/bash

# Navigate to backend directory
BACKEND_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$BACKEND_DIR")"

# Create virtual environment if it doesn't exist
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$BACKEND_DIR/venv"
fi

# Activate virtual environment
source "$BACKEND_DIR/venv/bin/activate"

# Install requirements
echo "Installing requirements..."
pip install -r "$BACKEND_DIR/requirements.txt" -q

# Start the server from the backend directory
# PYTHONPATH set so submodule relative imports (..database, ..models) resolve correctly
echo "Starting FastAPI server at http://localhost:8000 ..."
echo "API docs available at http://localhost:8000/docs"
cd "$BACKEND_DIR"
PYTHONPATH="$BACKEND_DIR" uvicorn main:app --host 127.0.0.1 --port 8000 --reload
