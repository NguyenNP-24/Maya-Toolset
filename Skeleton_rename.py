import maya.cmds as cmds

# Each entry is a string in the format "old_name:new_name"
rename_rules = [
    "Root_M:root",
    "Twrist_L:hand_l",
    "Twrist_R:hand_r",
    "Spine1_M:spine_01",
    "Spine2_M:spine_02",
    "Spine3_M:spine_03",
    "Neck1_M:neck",
    "Head_M:head",
    "UpLeg_L:thigh_l",
    "UpLeg_R:thigh_r",
    "Leg_L:shin_l",
    "Leg_R:shin_r",
    "Foot_L:foot_l",
    "Foot_R:foot_r"
]

# Convert rules into dictionary for faster lookup
rename_dict = dict(rule.split(":") for rule in rename_rules)

# Get selected joints
selected_joints = cmds.ls(selection=True, type="joint")

# Rename logic
for joint in selected_joints:
    new_name = None
    for old, new in rename_dict.items():
        if old in joint:
            new_name = joint.replace(old, new)
            break

    if new_name and new_name != joint:
        print(f"Renaming: {joint} -> {new_name}")
        cmds.rename(joint, new_name)
