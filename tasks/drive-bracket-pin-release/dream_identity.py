"""Validate recorded provider identity without inventing omitted SDK config fields."""
import math


def verify_identity(spec, policy, transcripts):
    expected = 'dreamlabs/dream-1-beta'
    if policy.get('name') != 'dream' or not isinstance(transcripts, list) or not transcripts:
        raise ValueError('Missing recorded Dream policy/provider transcript')
    models = [x for x in (spec.get('policy_config', {}).get('model'),
                          policy.get('checkpoint')) if x is not None]
    count = 0
    for transcript in transcripts:
        if transcript.get('dry_run') is not False:
            raise ValueError('Missing or non-genuine Dream dry-run status')
        models.append(transcript.get('model'))
        for request in transcript.get('requests', []):
            if (not isinstance(request.get('rows'), int) or request['rows'] <= 0
                    or not isinstance(request.get('session_id'), str) or not request['session_id']
                    or any(not isinstance(request.get(key), (int, float))
                           or not math.isfinite(request[key]) or request[key] < 0
                           for key in ('infer_ms', 'rtt_s'))):
                raise ValueError('Incomplete real Dream provider-request evidence')
            count += 1
    if not models or any(x != expected for x in models) or not count:
        raise ValueError('Wrong/inconsistent Dream identity or no genuine provider requests')
    return {'model': expected, 'dry_run': False, 'provider_requests': count}
