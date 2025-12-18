#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"
REQ_FILE="requirements.txt"

echo "Using Python: $PYTHON_BIN"

# 1. Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment in $VENV_DIR"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
else
  echo "Virtual environment already exists"
fi

# 2. Activate venv
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "Python in venv: $(which python)"

# 3. Upgrade pip & install deps
python -m pip install --upgrade pip setuptools wheel
pip install -r "$REQ_FILE"

echo "Virtual environment ready"
echo "Run with: source $VENV_DIR/bin/activate"
