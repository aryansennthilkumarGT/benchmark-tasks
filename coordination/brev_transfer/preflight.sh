#!/usr/bin/env bash
set -euo pipefail
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
for option in "$@"; do
  if [[ "$option" == '--gpu' ]]; then
    [[ -f /data/IsaacLab-Arena/yam.env ]] || { printf 'Missing existing yam.env; no reinstall attempted.\n' >&2; exit 2; }
    set +u
    source /data/IsaacLab-Arena/yam.env >/dev/null
    set -u
  fi
done
exec python3 "$here/transfer.py" preflight "$@"
