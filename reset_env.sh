#!/usr/bin/env bash
set -euo pipefail

# Always run relative to repo root (where this script lives)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYVER="${PYVER:-3.12.8}"
KERNEL_NAME="${KERNEL_NAME:-4543-geo}"
KERNEL_DISPLAY="${KERNEL_DISPLAY:-4543 Geo (.venv)}"

echo "=== 4543 Reset Environment ==="
echo "Repo root: $ROOT_DIR"
echo "Python:    $PYVER"
echo "Kernel:    $KERNEL_NAME  ($KERNEL_DISPLAY)"
echo ""

# Prefer `python3` first on macOS; some shells expose a broken `python` shim.
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
else
  echo "ERROR: Neither python nor python3 was found in PATH."
  exit 1
fi

# Pin python for this repo folder (pyenv)
if command -v pyenv >/dev/null 2>&1; then
  pyenv local "$PYVER"
else
  echo "WARNING: pyenv not found. Skipping pyenv local $PYVER"
fi

# Rebuild venv
rm -rf .venv
"$PYTHON_CMD" -m venv .venv
source .venv/bin/activate

./.venv/bin/python -m pip install -U pip
./.venv/bin/python -m pip install -r requirements.txt

# Kernel registration (user scope is correct)
./.venv/bin/python -m pip install -U ipykernel
./.venv/bin/python -m ipykernel install --user \
  --name "$KERNEL_NAME" \
  --display-name "$KERNEL_DISPLAY"

echo ""
echo "✅ Environment rebuilt."
echo "Next:"
echo "  1) Open the notebook"
echo "  2) Select kernel: $KERNEL_DISPLAY"