#!/usr/bin/env bash
# One entry point. No sudo, driver changes, cloud provisioning, or PR creation.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUTF8=1
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
PYTHON=${ROBOCURVE_PYTHON:-python3}
command -v "$PYTHON" >/dev/null || { echo 'Python 3.10+ is required.' >&2; exit 3; }
exec "$PYTHON" "$HERE/pipeline.py" "$@"
