# FractalTerrain 2.0!
import maya.cmds as cmd
import random as rand

def fractalize():
    # I can only dream...
    """
    objectSelected = cmd.ls(sl=True)
    verteces = cmd.polyListComponentConversion(objectSelected, toVertex=True)
    """
    maxHeight = 10
    # cmd.move(0, rand.uniform(0, maxHeight), 0, r=True)
    cmd.move(0, (maxHeight), 0, r=True)
    alreadyModifiedVertices = 0
    print("Hello?")
    for i in range(1, 10):
        currentSelection = cmd.ls(sl=True, fl=True)
        for item in currentSelection:
            if alreadyModifiedVertices is 0:
                alreadyModifiedVertices = [item]
            else:
                alreadyModifiedVertices.append(item)
        print("Already modified vertices: %s" % alreadyModifiedVertices)
        cmd.select(cmd.polyListComponentConversion(cmd.polyListComponentConversion(cmd.ls(sl=True, fl=True), fromVertex=True, toEdge=True), fromEdge=True, toVertex=True), r=True)
        cmd.select(alreadyModifiedVertices, deselect=True)
        currentSelection = cmd.ls(sl=True, fl=True)
        if len(cmd.ls(sl=True, fl=True)) is not i*4:
            print("Stopped on iteration %d, because length of selection is %d" % (i, len(cmd.ls(sl=True, fl=True))))
            print(cmd.ls(sl=True, fl=True))
            return
        for item in currentSelection:
            cmd.select(item, r=True)
            # cmd.move(0, rand.uniform(0, (maxHeight/2)/i), 0, r=True)
            cmd.move(0, (maxHeight/2)/i, 0, r=True)
        cmd.select(currentSelection, r=True)
