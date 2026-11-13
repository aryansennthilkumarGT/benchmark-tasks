"""Measured-input contract for LuK carrier mounting; no inferred hardware defaults.

Published kit data establishes thread families and the three-stud arrangement,
not carrier size, component mass or the installed vehicle's bolt circle.
"""
import math

THREAD_FAMILIES={'M6':(.006,.001),'M7':(.007,.001),'M8':(.008,.00125)}
REQUIRED=(
    'stud_circle_radius','stud_tip_height','stud_thread_length',
    'carrier_thickness','carrier_slot_inner_radius','carrier_slot_outer_radius',
    'carrier_slot_width','carrier_centre_bore','retracted_spindle_inner_bore',
    'centring_tool_outer_diameter','carrier_mass','retainer_diameter',
    'retainer_height','retainer_thread_length','retainer_mass',
    'retainer_thread_major','retainer_thread_pitch',
)


class MissingMeasurements(ValueError):
    pass


def validated(data, *, synthetic_test=False):
    missing=[name for name in REQUIRED if name not in data.get('measurements',{})]
    if missing:raise MissingMeasurements('Missing measured inputs: '+', '.join(missing))
    family=data.get('thread_family')
    if family not in THREAD_FAMILIES:raise ValueError('Unknown documented thread family')
    if not data.get('application_thread_verified'):
        raise ValueError('Kit thread availability does not establish the actual flywheel thread')
    result={}
    for name in REQUIRED:
        row=data['measurements'][name]
        if not isinstance(row,dict):raise ValueError('Measurement requires value and provenance: '+name)
        value=row.get('value');uncertainty=row.get('uncertainty')
        if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value) or value<=0:
            raise ValueError('Invalid measured value: '+name)
        if (isinstance(uncertainty,bool) or not isinstance(uncertainty,(float,int))
                or not math.isfinite(uncertainty) or uncertainty<0 or uncertainty>=value):
            raise ValueError('Invalid uncertainty: '+name)
        allowed={'manufacturer_dimensioned_document','physical_measurement'}
        if synthetic_test:allowed.add('synthetic_unit_fixture')
        if row.get('kind') not in allowed or not row.get('reference'):
            raise ValueError('Unsupported dimensional provenance: '+name)
        units={'kg':1.,'g':.001} if name.endswith('_mass') else {'m':1.,'mm':.001}
        if row.get('unit') not in units:raise ValueError('Invalid measurement unit: '+name)
        result[name]=float(value)*units[row['unit']]
    major,pitch=THREAD_FAMILIES[family]
    if result['carrier_slot_width']<=result['retainer_thread_major']:raise ValueError('Stud cannot pass through carrier slot')
    if not result['carrier_slot_inner_radius']<result['stud_circle_radius']<result['carrier_slot_outer_radius']:
        raise ValueError('Stud circle lies outside the carrier slots')
    if result['carrier_centre_bore']<=result['centring_tool_outer_diameter']:
        raise ValueError('Carrier interferes with centring tool')
    if result['retracted_spindle_inner_bore']<=result['centring_tool_outer_diameter']:
        raise ValueError('Spindle cannot pass over centring tool')
    if result['retainer_thread_length']>result['retainer_height']:
        raise ValueError('Retainer threaded length exceeds overall height')
    if result['stud_thread_length']<result['retainer_thread_length']:
        raise ValueError('Insufficient available stud thread')
    # The catalogue M6/M7/M8 values describe the FLYWHEEL end. They do not
    # establish the separate upper stud/retainer thread, even within one kit.
    result.update(flywheel_thread_major=major,flywheel_thread_pitch=pitch)
    return result
