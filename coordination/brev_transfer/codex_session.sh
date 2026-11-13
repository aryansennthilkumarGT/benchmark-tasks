#!/usr/bin/env bash
set -euo pipefail
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f /data/IsaacLab-Arena/yam.env ]]; then
  set +u
  source /data/IsaacLab-Arena/yam.env >/dev/null
  set -u
fi
exec python3 "$here/transfer.py" launch-codex
