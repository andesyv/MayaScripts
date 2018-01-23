# FractalTerrain 2.0!
import maya.cmds as cmd
import random as rand

def removeWindow():
    if cmd.window("fractalTerrain", ex=True):
        cmd.deleteUI("fractalTerrain", window=True)

def fractalizeOptions():
    removeWindow()

    cmd.window("fractalTerrain", title="Fractal Terrain Generation")
    cmd.columnLayout(rowSpacing=10)

    cmd.intSliderGrp("height", label="Maximum height", min=1, max=100, fieldMaxValue=1000, field=True)
    cmd.checkBox("stopIfEdge", label="Stop making fractal terrain if it reaches the edge?", value=True)
    cmd.text(label="Maximum outgoing range. (Normally leave this to 10)")
    cmd.intField("range", min=1, max=100, value=10, width=30)

    cmd.rowLayout(nc=3)
    cmd.button(label="Apply and close", command="import betterFractalTerrain as g\ng.fractalize()\ng.removeWindow()")
    cmd.button(label="Apply", command="import betterFractalTerrain as g\ng.fractalize()")
    cmd.button(label="Close", command="import betterFractalTerrain as g\ng.removeWindow()")
    cmd.showWindow("fractalTerrain")

def fractalize():
    maxHeight = 10
    if cmd.window("fractalTerrain", ex=True):
        maxHeight = cmd.intSliderGrp("height", query=True, value=True)
    # Move the first vertex.
    cmd.move(0, (maxHeight), 0, r=True)
    alreadyModifiedVertices = 0
    iterations = 10
    if cmd.window("fractalTerrain", ex=True):
        iterations = cmd.intField("range", query=True, value=True)

    # For each loop, it goes outwards to the next vertices.
    for i in range(1, iterations):
        currentSelection = cmd.ls(sl=True, fl=True)
        for item in currentSelection:
            if alreadyModifiedVertices is 0:
                alreadyModifiedVertices = [item]
            else:
                alreadyModifiedVertices.append(item)
        # This finds the next vertices.
        cmd.select(cmd.polyListComponentConversion(cmd.polyListComponentConversion(cmd.ls(sl=True, fl=True), fromVertex=True, toEdge=True), fromEdge=True, toVertex=True), r=True)
        # This makes sure we don't select any vertices that has already been selected.
        cmd.select(alreadyModifiedVertices, deselect=True)
        currentSelection = cmd.ls(sl=True, fl=True)

        # If it reaches the edge it will stop
        if cmd.window("fractalTerrain", ex=True):
            if cmd.checkBox("stopIfEdge", query=True, value=True):
                if len(cmd.ls(sl=True, fl=True)) is not i*4:
                    print("Stopped on iteration %d." % i)
                    return
        # This finds out how high it will move the vertex.
        for item in currentSelection:
            cmd.select(item, r=True)
            surroundingVertices = cmd.filterExpand(cmd.polyListComponentConversion(cmd.polyListComponentConversion(cmd.ls(sl=True, fl=True), fromVertex=True, toEdge=True), fromEdge=True, toVertex=True), expand=True, selectionMask=31)
            y = 0
            for vertex in surroundingVertices:
                if vertex in alreadyModifiedVertices:
                    if y is 0:
                        y = cmd.pointPosition(vertex)[1]
                    else:
                        y += cmd.pointPosition(vertex)[1]
                        y /= 2

            # This is just a failsafe incase something goes wrong with the code.
            if y is 0:
                print("Error. This should'nt happen.")
                return
            # Finally this moves each vertex.
            cmd.move(0, rand.uniform(y/2, y), 0, r=True)
        cmd.select(currentSelection, r=True)
