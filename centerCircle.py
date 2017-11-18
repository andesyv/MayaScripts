import maya.cmds as cmd
import math

def findCenter(vertexList):
    x = 0
    y = 0
    z = 0
    for val in vertexList:
        coords = cmd.pointPosition(val, world=True)
        x += coords[0]
        y += coords[1]
        z += coords[2]
    x = x / len(vertexList)
    y = y / len(vertexList)
    z = z / len(vertexList)
    center = [x, y, z]
    return center

def crossProduct(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c

# makeCircle()

def circlify():
    # Find center
    vertices = cmd.ls(sl=True, fl=True)
    """
    for val in vertices:
        print(val)
    """
    if len(vertices) < 2:
        print("Please select 2 or more vertices.")
        return

    center = findCenter(vertices)
    midVectors = []
    for i in range(0, len(vertices)):
        vector = cmd.pointPosition(vertices[i], world=True)
        for index in range(0, 3):
            vector[index] -= center[index]
        midVectors.append(vector)
    # Find normal-vector
    normalVector = crossProduct(midVectors[0], midVectors[1])
    print(normalVector)
    averageDistance = 0
    for val in midVectors:
        averageDistance += math.sqrt((val[0] ** 2) + (val[1] ** 2) + (val[2] ** 2))
    averageDistance = averageDistance / len(midVectors)
    print(averageDistance)
    # Make 1st point correct distance from center.
    cmd.select(vertices[0], r=True)
    cmd.move(center[0] + )
