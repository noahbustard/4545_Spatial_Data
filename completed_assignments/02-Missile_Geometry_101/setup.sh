#!/usr/bin/env bash
set -euo pipefail

# This script lives in:
#   Assignments/02-Missile_Geometry_101/
# Repo root is two levels up:
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Optional: project-specific kernel naming (keeps kernels distinct if you want)
export KERNEL_NAME="4543-02"
export KERNEL_DISPLAY="4543 02 Missile Geo (.venv)"

bash "$ROOT_DIR/reset_env.sh"