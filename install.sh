#!/usr/bin/env bash
set -euo pipefail

# Simple installer for the project dependencies.
# Usage:
#  ./install.sh        # create and use a local venv, install requirements
#  ./install.sh --conda   # create/activate a conda env and install pygame from conda-forge

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "Project installer — working in $SCRIPT_DIR"

if [ "${1:-}" = "--conda" ]; then
  if ! command -v conda >/dev/null 2>&1; then
    echo "Conda not found in PATH. Install Miniconda/Anaconda or use the default venv installer." >&2
    exit 1
  fi
  ENV_NAME="snakesnake"
  echo "Creating/activating conda env '$ENV_NAME' with python 3.11 (if not present) and installing pygame from conda-forge..."
  # create env if missing
  if ! conda info --envs | awk '{print $1}' | grep -qx "$ENV_NAME"; then
    conda create -n "$ENV_NAME" python=3.11 -y
  fi
  echo "Activating conda environment..."
  # shellcheck source=/dev/null
  source "$(conda info --base)/etc/profile.d/conda.sh"
  conda activate "$ENV_NAME"
  conda install -c conda-forge pygame -y
  echo "Conda environment ready. To use it: 'conda activate $ENV_NAME' and then 'python snake.py'"
  exit 0
fi

PYTHON_CMD="$(command -v python3 || command -v python)"
if [ -z "$PYTHON_CMD" ]; then
  echo "No python or python3 found in PATH." >&2
  exit 1
fi

echo "Using python: $PYTHON_CMD"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
  echo "requirements.txt not found at $REQUIREMENTS_FILE" >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating venv in $VENV_DIR..."
  "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

echo "Activating venv..."
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements from $REQUIREMENTS_FILE..."
pip install -r "$REQUIREMENTS_FILE"

echo "Install complete. To run the game:"
echo "  source $VENV_DIR/bin/activate"
echo "  python snake.py"

exit 0
