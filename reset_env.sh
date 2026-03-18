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

# Pin python for this repo folder (pyenv)
if command -v pyenv >/dev/null 2>&1; then
  pyenv local "$PYVER"
else
  echo "WARNING: pyenv not found. Skipping pyenv local $PYVER"
fi

# Rebuild venv
rm -rf .venv
python -m venv .venv
source .venv/bin/activate

python -m pip install -U pip
python -m pip install -r requirements.txt

# Kernel registration (user scope is correct)
python -m pip install -U ipykernel
python -m ipykernel install --user \
  --name "$KERNEL_NAME" \
  --display-name "$KERNEL_DISPLAY"

echo ""
echo "✅ Environment rebuilt."
echo "Next:"
echo "  1) Open the notebook"
echo "  2) Select kernel: $KERNEL_DISPLAY"