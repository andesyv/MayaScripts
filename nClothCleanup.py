# Python script
import maya.cmds as cmd

if cmd.window("clothCleanup", ex=True):
    cmd.deleteUI("clothCleanup", window=True)

cmd.window("clothCleanup", title="nCloth cleanup tool")
cmd.columnLayout(adj=True, rs=10)

cmd.text(label="This tool makes the nCloth into a normal mesh.", align="center")
cmd.checkBox("rigid", label="Remove rigidbody?", value=True)
cmd.checkBox("nucleus", label="Remove nucleus?", value=True)
cmd.button(label="Cleanup", command="import nClothCleanup as g\ng.cleanup()")
cmd.showWindow("clothCleanup")

def cleanup():
    selection = cmd.ls(sl=True)
    print(selection)
    # deletes history and clears
    cmd.delete(selection, ch=True)
    cmd.makeIdentity(selection, apply=True, jointOrient=True, rotate=True, translate=True, scale=True)
    cmd.delete("nCloth*")
    if cmd.checkBox("rigid", query=True, value=True):
        cmd.delete("nRigid*")
    shapes = cmd.listRelatives(shapes=True)
    for item in shapes:
        if "outputCloth" in item:
            pass
        else:
            cmd.delete(item)
    print(shapes)

    if cmd.checkBox("nucleus", query=True, value=True):
        cmd.delete("*nucleus*")

    if cmd.window("clothCleanup", ex=True):
        cmd.deleteUI("clothCleanup", window=True)
