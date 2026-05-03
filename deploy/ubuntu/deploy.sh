#!/usr/bin/env bash
set -euo pipefail

APP_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-$APP_ROOT/backend/.venv}"

echo "[1/5] Preparing backend virtual environment..."
"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$APP_ROOT/backend/requirements.txt"

echo "[2/5] Syncing frontend documents data..."
"$VENV_DIR/bin/python" "$APP_ROOT/backend/scripts/sync_frontend_data.py"

echo "[3/5] Installing frontend dependencies..."
cd "$APP_ROOT/frontend"
npm ci

echo "[4/5] Building frontend..."
npm run build

echo "[5/5] Deployment build completed."
echo "Frontend dist: $APP_ROOT/frontend/dist"
echo "Backend venv:   $VENV_DIR"
