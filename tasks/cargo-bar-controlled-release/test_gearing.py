"""Actual second-engine gear contact tests; no robot or Isaac evidence."""
from probe_gearing_cpu import probe

def test_contact_drives_rack_with_numeric_lead_without_virtual_constraint():
 d=probe();assert d['passed'] and not d['virtual_gear_constraint']
 assert d['checks'][-1]['rack_m']>.01

def test_disabled_contacts_do_not_magic_the_rack_forward():
 d=probe(contact_enabled=False)
 assert abs(d['checks'][-1]['rack_m'])<1e-9
 assert d['checks'][-1]['pinion_rad']<-.5

def test_real_contact_drive_is_robust_to_declared_friction_range():
 for friction in (.08,.25):assert probe(friction=friction)['passed']
