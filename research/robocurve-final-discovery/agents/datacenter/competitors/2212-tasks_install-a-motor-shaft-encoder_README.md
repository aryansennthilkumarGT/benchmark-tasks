# Install and field-check a magnetic motor encoder

Fit a keyed magnetic carrier to the motor shaft, position the encoder PCB bracket on both guide posts, and close the bracket catch. A local test button checks the installed magnetic geometry. The motor is unpowered throughout.

## Reproduce the scene

| Part | Material, dimensions and fixed reset |
| --- | --- |
| Motor and shaft | Unpowered Ø80 mm aluminium motor body and 8 mm steel D-shaft, upright on a 265 × 205 × 12 mm base. Axis at (306, 10) mm, motor face 77 mm and shaft end 92 mm above the table. D-flat faces +X. |
| Magnet carrier | 24 mm orange carrier with a keyed bore and a 6 × 2.5 mm diametric magnet, in its dark dock at (179, −148) mm. Leave the shaft bare. |
| Sensor bracket | 71 × 95 mm aluminium carrier with a 47 × 45 mm PCB and insulating grip. Start in the near-left dock at (269, 139) mm. Guide posts are spaced 76 mm along Y around the shaft. The fixture stops establish a 1.5 mm nominal magnet-to-sensor gap. |
| Catch and test box | Red 27 × 23 mm retention catch at (365, −54) mm, open with 12 mm closing travel. Blue 18 mm test button at (250, −124) mm. The diagnostic LED starts off. |

Coordinates are from the midpoint of the arm bases, +X away from the robot and +Y to its left. The assembly follows the usual on-axis diametric-magnet placement of a magnetic rotary encoder. The fixture-specific gap needs bench validation. [AS5047P sensor installation reference](https://jcsdoc.arbite.io/latest/devices/JCS0004_dev_encoder_absolute/on_axis_jcs_network/JCS00040001010000/hw_reference/oa_ae_hw_installation/)

## Run

From this directory, in the RoboCurve YAM Arena environment with Inspect Robots 1.0:

```bash
python run_task.py yam_scripted --log-dir runs/demo --setup setup.png
python run_task.py dream --log-dir runs/dream
python run_task.py yam_scripted --case skip-catch --log-dir runs/open-catch
python run_task.py yam_scripted --case missing-magnet --log-dir runs/no-magnet
python make_evidence.py runs/demo demo.mp4 --title 'Scripted YAM demo'
python make_evidence.py runs/dream model.mp4 --title 'Dream-1 baseline'
```

The runner uses seed 42, 20 Hz and a 1,400-step (70 s) limit, with zero object jitter.

## Scoring and fidelity

A seated keyed magnet carrier scores 0.25. A seated sensor bracket on both guides increases the score to 0.45. Closing the catch increases it to 0.65. Full credit requires a green field check after a test press, tools released and both hands clear. The simulated keyed guides require the correct approach, yaw tolerance of 0.13 rad and lateral seat tolerances of 4 mm for the carrier and 5 mm for the bracket. The test button must be pressed for at least 0.30 s. A real inspection checks the bracket position, retention and local diagnostic light.

The model uses keyed insertion and catch geometry driven by actual YAM hand poses. Magnetic flux, press-fit friction and electrical faults are simplified. The LED checks the modeled installation geometry and catch, with no claim about angular accuracy, calibration or encoder performance under power. The scripted policy uses fixed robot waypoints.

## Recorded results

| Trial | Score | Control steps | Runtime including startup |
| --- | ---: | ---: | ---: |
| Scripted YAM | 1.00 | 581 | 282 s |
| Dream-1 | 0.00 | 1,400 | 433 s |

The scripted run seated both parts, closed the catch and showed the green diagnostic LED after release. Dream-1 ended at the step limit without seating the carrier. The contact-model controls score 0.45 when the catch is left open and 0.0 with the magnet missing. Both controls fail the field check.

