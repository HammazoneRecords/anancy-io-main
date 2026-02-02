#!/usr/bin/env bash
# Run AnancyIO (no Docker) using Conda
# Usage: ./run-web.sh

set -e
cd "$(dirname "$0")"
ENV_NAME="anancyio"

echo "=== AnancyIO (Conda) ==="

if ! command -v conda &>/dev/null; then
  echo "Conda not found. Install Miniconda or Anaconda, then run this script again."
  exit 1
fi
echo "Using Conda"

# Initialize conda for this shell if needed
eval "$(conda shell.bash hook 2>/dev/null)" || true

if ! conda env list | grep -q "^\s*${ENV_NAME}\s"; then
  echo "Creating Conda env '$ENV_NAME' with Python 3.12..."
  conda create -n "$ENV_NAME" python=3.12 -y
fi

conda activate "$ENV_NAME"

if ! python -c "import flask" 2>/dev/null; then
  echo "Installing dependencies (first time may take several minutes)..."
  pip install -r requirements.txt
fi

PORT=5000
[ -f .env ] && val=$(grep -E '^\s*WEB_UI_PORT\s*=' .env 2>/dev/null | head -1 | sed -E 's/.*=\s*([0-9]+).*/\1/') && [ -n "$val" ] && PORT=$val

echo "Starting at http://localhost:$PORT ..."
echo "Press Ctrl+C to stop."
exec python run_ui.py
