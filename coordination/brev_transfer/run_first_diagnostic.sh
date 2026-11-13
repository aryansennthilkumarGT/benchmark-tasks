#!/usr/bin/env bash
set -euo pipefail
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
execute=0
dry_run=0
for option in "$@"; do
  [[ "$option" != '--execute' ]] || execute=1
  [[ "$option" != '--dry-run' ]] || dry_run=1
done
if ((execute && !dry_run)); then
  [[ -f /data/IsaacLab-Arena/yam.env ]] || { printf 'Missing existing yam.env; no reinstall attempted.\n' >&2; exit 2; }
  set +u
  source /data/IsaacLab-Arena/yam.env >/dev/null
  set -u
fi
exec python3 "$here/transfer.py" diagnostic "$@"
