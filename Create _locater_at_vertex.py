import maya.cmds as cmds

sel = cmds.ls(selection=True, flatten=True)
if sel and '.vtx' in sel[0]:
    pos = cmds.pointPosition(sel[0], world=True)
    loc = cmds.spaceLocator(name="muzzle_tracker_LOC")[0]
    cmds.xform(loc, ws=True, t=pos)
