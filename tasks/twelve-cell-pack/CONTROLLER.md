# Measured-state pressure-plate closure expert

The eighteen phases clear the right arm, grasp and lift the plate, align its twelve contact pads, compress the contacts, acquire the key with the other arm, insert it into the retaining channels, release the key, release the plate and withdraw both arms. The cells are already loaded in the declared starting layout.

The controller uses measured native body poses, joint positions and robot proprioception. Loaded carries use body-position gain 3 with a 20 mm lead cap and measured-pose reference gain 2 per second. Plate compression uses a 5 mm lead cap at a 10 mm/s motion limit. The loaded left tracking window is 0.20 radians and the right window is 0.08 radians. URDF position, velocity and effort limits apply through native actuation.

The pressure hold captures the current robot reference pose after compression. This preserves the loaded command while the right hand handles the key. Key insertion checks transverse alignment before advancing, tracks transverse and axial progress independently, and aborts a stall after two seconds. Neither body poses nor score states are written by the expert.

Five completed cell-placement sequences from the earlier loading prototype remain preserved in branch history and their original evidence. This focused closure revision requires fresh native mechanism tests, control tests, two recorded full-score experts and its own genuine model evaluation.


Compression completion requires all twelve measured terminal joints between-1.75mm and-0.40mm, together with the plate pose conditions. Position, angle and compression-range progress are tracked independently with a5second bounded stall timeout. The previous pose-only completion advanced while one measured spring had only0.039mm compression. Native scoring still independently checks cell poses, polarity, spring compression and final load capture.
