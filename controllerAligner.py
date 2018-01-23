import maya.cmds as cmd
import math

# Options window
def alignOptions():
    # Delete old window if it exists.
    if cmd.window("controllerAlignerWindow", ex=True):
        cmd.deleteUI("controllerAlignerWindow", window=True)

    cmd.window("controllerAlignerWindow", title="Rigging-controller aligner tool")
    cmd.columnLayout(adj=True, rs=0)

    cmd.text(label="This tool aligns your rigging-controls onto the joins of the rig,", align="center")
    cmd.text(label="and parent constraints them for you.", align="center")
    cmd.columnLayout(adj=True, rs=20)
    cmd.checkBox("parentChecker", label="Add parentconstraint?", value=False)
    cmd.button(label="Apply", command="import controllerAligner as g\ng.align()")
    cmd.showWindow("controllerAlignerWindow")


def align():
    # Make an array for all joints and controllers, respectively.
    joints = cmd.listRelatives(cmd.ls(sl=True), type="joint", allDescendents=True)
    controllers = cmd.listRelatives(cmd.listRelatives(cmd.ls(sl=True), type="nurbsCurve", shapes=True), parent=True)

    if not joints:
        return
    if not controllers:
        return

    # Loop for each item in the controller-array.
    for controller in controllers:
        controllerCoords = cmd.xform(controller, query=True, translation=True, worldSpace=True)
        shortestIndex = 0;

        # Finds closest joint to controller
        for i in range(0, len(joints)):
            # The current iterations length to controller
            currentJoint = cmd.xform(joints[i], query=True, translation=True, worldSpace=True)
            currentLength = math.sqrt((currentJoint[0] - controllerCoords[0]) ** 2 + (currentJoint[1] - controllerCoords[1]) ** 2 + (currentJoint[2] - controllerCoords[2]) ** 2)

            # The current shortest length to controller
            oldJoint = cmd.xform(joints[shortestIndex], query=True, translation=True, worldSpace=True)
            oldLength = math.sqrt((oldJoint[0] - controllerCoords[0]) ** 2 + (oldJoint[1] - controllerCoords[1]) ** 2 + (oldJoint[2] - controllerCoords[2]) ** 2)

            # If a shorter length is found, make "shortestIndex" point to the new length
            if currentLength < oldLength:
                shortestIndex = i

        # Move controller to the closest joint found.
        newTransforms = cmd.xform(joints[shortestIndex], query=True, translation=True, worldSpace=True)
        cmd.move(newTransforms[0], newTransforms[1], newTransforms[2], controller, absolute=True, worldSpace=True)

        # Parentconstraints them
        if cmd.window("controllerAlignerWindow", ex=True):
            if cmd.checkBox("parentChecker", query=True, value=True):
                cmd.parentConstraint(controller, joints[shortestIndex], maintainOffset=True)

    # Delete old window if it exists.
    if cmd.window("controllerAlignerWindow", ex=True):
        cmd.deleteUI("controllerAlignerWindow", window=True)
