import maya.cmds as cmd
import random
import math

# Delete old window if it exist.
if cmd.window("grassMaker", ex=True):
    cmd.deleteUI("grassMaker", window=True)

cmd.window("grassMaker", title="Grass generation")
cmd.columnLayout(rowSpacing=10, adj=True);

cmd.intSliderGrp("iterations", label="Number of grasses", min=1, max=100, fieldMaxValue=300, field=True)
cmd.intSliderGrp("radius", label="Max radius", min=0, max=100, field=True)
cmd.text(label="Path to texture to use on grass: (ex: \"C:/Users/TheBestPerson/Desktop/grassTex.png\")")
cmd.textField("imageLink")
cmd.button(label="Create", height=100, command="import grassMaker as g\ng.createGrass()")
cmd.showWindow("grassMaker")

def makeRandomPoint(radius):
    randomAngle = random.uniform(0, 2 * math.pi)
    return (math.cos(randomAngle) * radius, 0, math.sin(randomAngle) * radius)

# Create material
def createMaterial():
    nodes = cmd.ls(materials=True)
    for node in nodes:
        if node == "grassMaterial":
            return False
    shader = cmd.shadingNode('lambert', asShader=True, name="grassMaterial")
    fileNode = cmd.shadingNode('file', asTexture=True, name="grassTexture")
    shadingGroup = cmd.sets(renderable=True, noSurfaceShader=True, empty=True, name="grassMaterialSG")

    cmd.connectAttr('%s.outColor' % shader, '%s.surfaceShader' % shadingGroup)
    cmd.connectAttr('%s.outColor' % fileNode, '%s.color' % shader)
    cmd.connectAttr('%s.outTransparency' % fileNode, '%s.transparency' % shader)

    link = cmd.textField("imageLink", query=True, text=True)
    print(link)
    if not link:
        link = "http://jallaboika.com/images/grassTex.png"
    cmd.setAttr('%s.fileTextureName' % fileNode, link, type="string")
    return shader

def createGrass():
    material = createMaterial()
    if material:
        print("Material created")
    else:
        print("Material was not created")

    plane = 0
    totalIterations = cmd.intSliderGrp("iterations", query=True, value=True)
    maxRadius = cmd.intSliderGrp("radius", query=True, value=True)

    for iteration in range(0, totalIterations):
        if not plane:
            plane = cmd.polyPlane(axis=(1, 0, 0), sx=1, sy=1)
            copyPlane = cmd.duplicate()
            cmd.polyNormal()
            plane = cmd.polyUnite(plane[0], copyPlane[0], name="grass#")
            cmd.polyMergeVertex(distance=0.001)
            cmd.delete(plane[0], ch=True)

            cmd.sets(edit=True, forceElement="grassMaterialSG")
            instancesGroup = cmd.group( empty=True, name=plane[0] + '_instance_grp#' )
        else:
            current = cmd.instance(plane[0], name="%s_instance#" % plane[0])
            cmd.select(current[0], r=True)
            cmd.scale(1, random.uniform(1, 2), random.uniform(1, 3))
            degrees = '%ddeg' % random.uniform(0, 360)
            cmd.rotate(0, degrees, 0, relative=False)
            x, y, z = makeRandomPoint(random.uniform(0, maxRadius))
            cmd.move(x, y, z, current[0])
            cmd.parent(current, instancesGroup)
    cmd.scale(1, random.uniform(1, 2), random.uniform(1, 3), plane[0])
