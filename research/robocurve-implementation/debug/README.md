# Invalid/debug runs, not final evidence

The canonical outputs are the current per-candidate results used by verify_results.py. These scratch captures preserve early failures only:

- Initial contact test commanded only 9 s and did not complete an output revolution; it also hit NumPy-boolean JSON serialization. The final test stops on measured input stroke, not commanded output pose.
- An initial inward door sign was wrong for a left-hinged outward-opening door; final access results use the corrected outward geometry.
- A high joint-friction value did not actually seize MuJoCo wheel motion. The valid seized-wheel control fixes the wheel to its carrier, and independent wheel-marker motion is required.
- Initial duplicated YUBI captures precede canonical direct/raised-transit output names. They must not be interpreted as additional independent routes.

No original manufacturer geometry or previous research artifact was changed by these fixes.
