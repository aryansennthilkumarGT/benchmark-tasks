#!/usr/bin/env python3
"""CPU preflight for N044; missing data exits2, never passes by assumption."""
from access_core import main

if __name__ == "__main__":
    raise SystemExit(main("N044"))
