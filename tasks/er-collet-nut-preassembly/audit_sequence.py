"""Explicit ideal rigid-grasp controller trace; never actual task physics."""
from pathlib import Path
from audit_full_fk_path import audit
if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent,collision_checks=False))
