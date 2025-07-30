import maya.cmds as cmds
import maya.mel as mel
import os

# Create Folder
output_dir = os.path.expanduser("~/Desktop/test/Playblast")  # RENAME YOUR SAVE PATH HERE #
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get all panel showing (viewport)
viewPanels = cmds.getPanel(type="modelPanel")
visiblePanels = cmds.getPanel(visiblePanels=True)
renderPanels = list(set(viewPanels) & set(visiblePanels)) 

# Playblast for each panel
for panel in renderPanels:
    cmds.setFocus(panel)
    panelName = cmds.panel(panel, q=True, label=True).split(" ")[0]
    print(panelName)

    renderPath = os.path.join(output_dir, f"{panelName}.mov").replace("\\", "/")

    # Delete old file if exist
    if os.path.exists(renderPath):
        os.remove(renderPath)

    mel.eval(f'''
        playblast 
        -format qt 
        -filename "{renderPath}" 
        -sequenceTime 0 
        -clearCache 1 
        -viewer 1 
        -showOrnaments 1 
        -offScreen 
        -fp 4 
        -percent 100 
        -compression "jpeg" 
        -quality 100;
    ''')
