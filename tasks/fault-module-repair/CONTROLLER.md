# Fixed robot action demonstration

The demonstration expert executes `expert_joint_trajectory.json`, an authored program of robot joint and jaw commands. It has no runtime hidden object, mechanism or scorer feedback. The fixed terminal action count is not a success signal; actual observations must independently score 1.0. `controller.json` and feedback utilities are retained as disclosed offline development and native-mechanism test tools, not the expert runtime.
