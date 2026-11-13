"""Explicit one-session $15 policy. Legacy receipts retain legacy protections."""
from pathlib import Path

POLICY_ID='robocurve-brev-transfer-15usd-2026-11-13'
INSTANCE='yam-eval-launchable-0cb74b'
ROOT=Path('/data/robocurve-sprint')
AUTHORIZATION_REFERENCE='user-upload:sha256:0ffc4b46720794c4340cad0fe7f034062fc3fdb9e5d5698f2e6a1d6b76ecdf8a'
STOP_COMMAND='brev stop '+INSTANCE


def limits(receipt,path,read):
    policy=receipt.get('spending_policy_id')
    if policy is None:return {'cap':170.,'reserve':30.,'trigger':None,'new_session_only':False}
    if policy!=POLICY_ID:raise ValueError('Unknown spending policy; legacy guards cannot be bypassed')
    if (receipt.get('instance_name')!=INSTANCE or receipt.get('authorization_reference')!=AUTHORIZATION_REFERENCE
            or receipt.get('authorized_session_spend_usd')!=15. or receipt.get('estimated_shutdown_trigger_usd')!=13.5
            or receipt.get('provider_stop_command')!=STOP_COMMAND or receipt.get('shutdown_method_confirmed') is not True):
        raise ValueError('Scoped $15 policy identity/authorization/shutdown fields do not match')
    if Path(path).resolve().parent!=ROOT/'provider-observations':
        raise ValueError('Scoped $15 receipt must belong to the dedicated transfer session')
    state=read(ROOT/'handoff-state.json')
    if not receipt.get('authorization_session_id') or state.get('authorization_session_id')!=receipt['authorization_session_id']:
        raise ValueError('Scoped $15 receipt belongs to a different transfer session')
    return {'cap':15.,'reserve':0.,'trigger':13.5,'new_session_only':True}
