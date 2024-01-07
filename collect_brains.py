import os
import shutil

brainDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "brains")
gameDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "game")

collectionPath = os.path.join(gameDir, "brains.py")
baseBrainPath = os.path.join(brainDir, "base_brain.py")

shutil.copyfile(baseBrainPath, collectionPath)

for fileName in os.listdir(brainDir):
    if fileName.endswith(".py"):
        if fileName != "base_brain.py":
            with open(collectionPath, "a") as collectionFile:
                customBrainPath = os.path.join(brainDir, fileName)
                with open(customBrainPath, "r") as customBrainFile:
                    collectionFile.write("\n\n")
                    collectionFile.write(customBrainFile.read())

