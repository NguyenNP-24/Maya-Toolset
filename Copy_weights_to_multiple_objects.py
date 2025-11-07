# First select the source mesh with good skinning, then shift select the other meshes you want to copy the skin to
# The other meshes should have existing skincluster, if not, the joints from the source mesh will be binded to these meshes

import maya.cmds as cmds

def copy_skin_weights_to_multiple():
    # Get all selected objects
    selection = cmds.ls(selection=True)

    # Check if there are enough objects selected (at least 2: source and one target)
    if len(selection) < 2:
        cmds.warning("Please select the source object first, followed by one or more target objects.")
        return

    # The first selected object is the source
    source_mesh = selection[0]
    # The rest of the selected objects are the targets
    target_meshes = selection[1:]

    # 1. Find the skinCluster on the source mesh
    source_skin_cluster = None
    history = cmds.listHistory(source_mesh)
    if history:
        skin_clusters = cmds.ls(history, type='skinCluster')
        if skin_clusters:
            source_skin_cluster = skin_clusters[0]
            print(source_skin_cluster)

    if not source_skin_cluster:
        cmds.warning("Source object '{source_mesh}' does not have a skinCluster.")
        return

    # Get the influences (joints) from the source skin cluster
    influences = cmds.skinCluster(source_skin_cluster, query=True, influence=True)

    # 2. Iterate through each target mesh and copy the skin weights
    for target_mesh in target_meshes:
        cmds.select(clear=True) # Clear selection before new operations

        # Bind the target mesh to the same influences if it's not skinned already
        target_skin_cluster = None
        target_history = cmds.listHistory(target_mesh)
        if target_history:
            target_skin_clusters = cmds.ls(target_history, type='skinCluster')
            if target_skin_clusters:
                target_skin_cluster = target_skin_clusters[0]
        
        # If no skin cluster exists, create one using the source influences
        if not target_skin_cluster:
            try:
                # Bind the target mesh to the influences from the source
                # 'tsb=True' is 'toSkeleton' and 'bindMethod=0' is 'Closest Hierarchy' (default)
                cmds.skinCluster(influences, target_mesh, toSkeleton=True, bindMethod=0, name="{target_mesh}_skinCluster")
                target_skin_cluster = cmds.ls(cmds.listHistory(target_mesh), type='skinCluster')[0]
            except Exception as e:
                cmds.error(f"Failed to bind target mesh '{target_mesh}'. Error: {e}")
                continue


        # Now copy the skin weights
        try:
            # Select the source and the current target
            cmds.select(source_mesh, target_mesh, replace=True)

            cmds.copySkinWeights(
                noMirror=True,
                surfaceAssociation='closestPoint',
                influenceAssociation='oneToOne',
                normalize=True # Good practice to normalize after copying
            )

            
            cmds.select(target_mesh, replace=True)
            cmds.skinCluster(target_skin_cluster, e=True, forceNormalizeWeights=True) # Final normalization for good measure

            cmds.inViewMessage(message="Copied skin weights to: <hl>{target_mesh}</hl>", fade=True, pos='midCenter')

        except Exception as e:
            cmds.error("Failed to copy skin weights to '{target_mesh}'. Error: {e}")
            continue

    cmds.select(selection, replace=True) # Reselect the original selection
    cmds.inViewMessage(message="Skin weight copy process completed.", fade=True, pos='midCenter')


copy_skin_weights_to_multiple()