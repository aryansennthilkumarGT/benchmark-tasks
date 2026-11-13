# Observable scoring and reproduction measurements

No physical hardware measurements have been taken. All reported test outputs are CPU diagnostics or synthetic controller checks; native robot and hardware evidence remains absent.

Use a calibrated close-up image or digital calipers to establish the nut axis and collet profile. The visible top of the upright collet is32.7mm above its groove midplane, derived from the specified40mm length and7.3mm groove-to-nose-end distance. This makes groove-height error observable from the top datum without reading an internal force. Check lateral axis error≤0.6mm, groove midplane height error≤0.3mm and axis tilt≤0.025rad. The absolute target is(0.24,0,0.8055)m in the station datum.

Partial hook credit uses the specified groove-side point and a visible tilted configuration. Derive that point from the measured rigid collet pose and published/explicitly authored profile, and check its1.2mm distance/0.05–0.45rad angle bounds. Do not infer engagement from an expert phase or from the object's name. Any collision/invalid geometry still invalidates credit.

For full score, record at least20Hz for2s. Each body's sampled positions must remain pairwise within0.4mm and its +Z-axis directions within0.015rad. Collet yaw is irrelevant. Use macro views with a calibration grid and resolution comfortably finer than0.4mm, not an uncalibrated wide station screenshot. Both robot geometries must remain≥20mm away; measure the nearest finger/link, not only TCP position. Calipers, angle images and a fixed reference grid suffice; no hidden compression or prescribed gripping force is scored.

These are authored acceptance tolerances, not manufacturer measurement uncertainty or precision/runout claims. The pose-window rule intentionally tolerates microscopic contact chatter while rejecting500micrometre motion across the window. Report actual instrument accuracy and geometric deviations when hardware is built. Fixed fixtures moving>1mm or0.025rad, missing/lost parts, overlap>0.10mm, invalid telemetry and impossible state substitutions latch zero.
