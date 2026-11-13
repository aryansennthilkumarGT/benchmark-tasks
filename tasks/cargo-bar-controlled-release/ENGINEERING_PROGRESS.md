# Active housing and physical-interface repair

This head is an engineering checkpoint, not offline-ready or qualified. Historical clean source3bda168/evidencebc6ad88 is preserved; its reports do not validate these changed mechanics.

Implemented work: original enclosure with close tube/hub ports; exposed operating bars above the guard; a real slotted trigger guide instead of intersecting solid members; pad rods and annular guides; bearing bridges outside the shaft journal and inner tube. These are benchmark-authored dimensions, never OEM measurements.

The current native-style cam diagnostic passes because normal joint adjacency filters parent/child contacts. The new unfiltered audit exposes a remaining real CAD interference: the moving handle-cam spoke passes through the fixed annular spacer. The telescope/inner-tube interference was repaired by moving bearing ties outside the tube.

Next: move the fixed spacer to axialX0.026–0.032m, clear of the handle spoke atX0.037–0.043m. Connect the fixed release cam to the guard at a radial location outside moving cam sweep. Regenerate scene and physical cam reference; rerun audit_interfaces.py and audit_housing.py. Then run the affected contact, actual FK, controller, grasp and source-provenance checks. Update the full parameter/reproduction/fidelity tables and source manifest deliberately, then independently clean-HTTPS verify and publish current-source evidence.

Current parameter-provenance hash predates the housing edits and must fail validation. It is not bypassed; regenerate it only after intentional geometry review. Old dimensions/docs/test counts remain historical until that update. No Isaac/YAM expert/model/hardware success is claimed.
