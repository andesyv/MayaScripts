import maya.cmds as cmd
import random as rand


def arts():
    print("pls")
    cube = cmd.polyCube()

    for i in range(0, 8):
        faceCount = cmd.polyEvaluate(cube[0], face=True)
        cmd.select("%s.f[%d]" % (cube[0], rand.randrange(0, faceCount)), r=True)
        print(cmd.ls(sl=True))
        for i in range(0, rand.randrange(0, faceCount)):
            cmd.select("%s.f[%d]" % (cube[0], rand.randrange(0, faceCount)), add=True)
        cmd.polyExtrudeFacet(keepFacesTogether=False, localTranslateZ=rand.uniform(0, 3))
        cmd.select(cube[0], r=True)
        cmd.polyMergeVertex(d=0.01)
