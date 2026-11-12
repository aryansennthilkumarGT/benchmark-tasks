"""Explicit supported native CPU PhysX profile; RTX RGB cameras remain on the L40S.
Task geometry, integration cadence, solver settings, actions and scorer are unchanged.
"""
import run

original_command = run.command

def command_with_native_cpu(*values, **keywords):
    return [*original_command(*values, **keywords), '-E', 'device=cpu']

run.command = command_with_native_cpu
if __name__ == '__main__':
    raise SystemExit(run.main())
