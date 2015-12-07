import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import random

kPluginCmdName = "build"

class buildingPart():
    def __init__(self, dimension, roofSpec, position):
        self.pos = [0, 0, 0]
        self.dim = dimension
        self.roof = roofSpec

    def build(self):
        i = 0
        cmds.polyCube(sx=5, sy=5, sz=5, w=self.dim[0], h=self.dim[1], d=self.dim[2], n='box'+str(i))
        cmds.move(0,self.dim[1]*0.5,0,r=1)
        self.buildRoof(i)

    def buildRoof(self, i):
        cmds.polyCube(w=self.dim[0], h=self.roof[1], d=self.dim[2], n = 'roof' + str(i))
        cmds.move(0, self.dim[1] + 0.5*self.roof[1], 0, r=1)
        if(self.dim[2] < self.dim[0] ):
            cmds.select('roof' + str(i) + '.vtx[2:3]')
            cmds.move(0, 0, -0.5 * self.dim[2], r=1)
            cmds.select('roof' + str(i) + '.vtx[4:5]')
            cmds.move(0, 0, 0.5 * self.dim[2], r=1)
        else:
            cmds.select(['roof' + str(i) + '.vtx[2]', 'roof' + str(i) + '.vtx[4]'])
            cmds.move(0.5 * self.dim[0], 0, 0, r=1)
            cmds.select(['roof' + str(i) + '.vtx[3]', 'roof' + str(i) + '.vtx[5]'])
            cmds.move(-0.5 * self.dim[0], 0, 0, r=1)

class building():
    def __init__(self, lot, lot_pos):
        self.lot = lot
        self.lot_pos = lot_pos
        #store the different house parts here
        self.parts = []
        self.houseHeight = random.randint(3,8)
        self.houseWidth = random.randint(3,8)
        self.houseDepth = random.randint(3,8)
        self.roofHeight = random.randint(3,4)
        self.roofType = random.randint(1,3)
        self.lawnX = 15
        self.lawnZ = 15

    def generateMainPart(self):
        #build the main part of the house

        #after some calculations

        self.parts.append( buildingPart([self.houseWidth, self.houseHeight, self.houseDepth], [self.roofType, self.roofHeight], [0,0,0]) )

    def lotPlacement(self):
        cmds.select('box'+str(i))
        cmds.move( random.randint(-(self.lawnX)/2+self.width,self.lawnX/2-self.width), self.height/2 +0.2, random.randint(-(self.lawnZ)/2+self.depth,self.lawnZ/2-self.depth), 'box', absolute=True )
        cmds.select('roof'+str(i))
        cmds.move( random.randint(-(self.lawnX)/2+self.width,self.lawnX/2-self.width), self.height/2 +0.2, random.randint(-(self.lawnZ)/2+self.depth,self.lawnZ/2-self.depth), 'roof', absolute=True )


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
        hus = building(0,0)
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
