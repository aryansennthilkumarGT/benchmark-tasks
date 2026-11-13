# Supplemental contact diagnostics on CPU

The optional MuJoCo3.3.7 exporter uses the exact task scene's independent rigid bodies, original box/cylinder collision shapes, masses, COM/inertia, poses and timestep. It refuses articulated mechanisms and unsupported primitives rather than flattening them. Friction is read from the scene or actual authored USD material. MuJoCo uses a scalar dynamic-friction approximation and different compliant contacts from PhysX; rolling/torsional friction and solver settings are explicit diagnostic assumptions. No GPU, rendering, robot or paid service is involved.

Install into an isolated Python3.12 environment with the normal task CPU dependencies:

```bash
uv pip install --python /path/to/venv/bin/python -r coordination/requirements-cpu-contact.txt
python coordination/cpu_contact_probe.py --folder /path/to/task --output /tmp/new-contact-probe
```

Each declared native force probe is repeated after an independent reset. Forces are applied for the declared steps and removed during settling, matching the native test harness. Assertions examine final contact depth as the native assertion does. Peak transient penetration is separately recorded and must not be hidden. Root/body initialized diagnostic poses are never demonstrations, and scorer rejection of those initialized states is expected when the case says so. This validates the probe design and gives second-engine risk evidence; it cannot qualify Isaac contacts or certify robot manipulation.

The first ER run exposed a mismatch in the initial exporter protocol: it settled before applying force and enforced a peak-penetration assertion, whereas the native case applies force first and checks final penetration. That failed result is preserved. The corrected protocol passes all six final assertions, while still recording about1.26 mm transient overlap in the intentionally forced free-entry case. This remains a contact-impact/solver risk. Neither an initialized seated state nor this result proves a complete expert run.

The first shackle run found a substantive test-design defect: an unretained0.18 kg pin under8 N for0.75 s rises about9.74 m, outside the unchanged0.8 m upper bound. The diagnostic force was corrected to2 N (about0.366 m ideal rise). The physically separate seated-pin retention test remains12 N. Original source/evidence is preserved; fresh tests identify the changed input hashes.

Run coordination/test_cpu_contact_probe.py for actual CPU free-fall/contact support, transform/dimension conversion and strict unsupported-input checks. These tests are not simulated GPU receipts. An actual native Isaac run, real robot experts and genuine model/media checks remain mandatory.
