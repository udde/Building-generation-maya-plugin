import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginCmdName = "build"
class housePart():
    def __init__(self, dimension, rof_spec, position):
        self.pos    = [0, 0, 0]
        self.dim    = [1, 1, 1]
    def build(self):
        i = 0
        cmds.polyCube(n='box'+str(i))
        cmds.move(0,0,0,r=1)
        cmds.polyCube(n='roof'+str(i))
        cmds.move(0,1,0,r=1)
        cmds.select('roof'+str(i)+'.vtx[2:3]')
        cmds.move(0,-0.5,-0.5,r=1)
        cmds.select('roof'+str(i)+'.vtx[4:5]')
        cmds.move(0,-0.5,0.5,r=1)

class house():
    def __init__(self, lot, lot_pos):
        self.lot = lot
        self.lot_pos = lot_pos
        #store the different house parts here
        self.parts = []

    def generateMainPart(self):
        #build the main part of the house

        #after some calculations
        self.parts.append( housePart([1,1,1], 0.5, [0,0,0]) )

    def extend(self):
        #extend the house if its posible
        return False

    def build(self):
        for part in self.parts:
            part.build()



# Command
class scriptedCommand(OpenMayaMPx.MPxCommand):

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    # Invoked when the command is run.
    def doIt(self,argList):
        print "johan sylvan"
        hus = house(0,0)
        hus.generateMainPart()
        # while(extend):
        hus.build()





# Creator
def cmdCreator():
    return OpenMayaMPx.asMPxPtr( scriptedCommand() )

# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )
