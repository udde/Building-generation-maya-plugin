import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import random

kPluginCmdName = "build"

class buildingSection():
    idx = 0
    def __init__(self, dimension, roofSpec, position):
        self.pos = position
        self.dim = dimension
        self.roof = roofSpec
        self.idx = buildingSection.idx
        buildingSection.idx += 1

    def build(self):
        cmds.polyCube(sx=5, sy=5, sz=5, w=self.dim[0], h=self.dim[1], d=self.dim[2], n='box'+str(self.idx))
        cmds.move(self.pos[0],self.dim[1]*0.5,self.pos[2],r=1)
        self.buildRoof()
        cmds.select(clear = True)

    def buildRoof(self):
        cmds.polyCube(w=self.dim[0], h=self.roof[1], d=self.dim[2], n = 'roof' + str(self.idx))
        cmds.move(self.pos[0], self.dim[1] + 0.5*self.roof[1], self.pos[2], r=1)
        if(self.dim[2] < self.dim[0] ):
            cmds.select('roof' + str(self.idx) + '.vtx[2:3]')
            cmds.move(0, 0, -0.5 * self.dim[2], r=1)
            cmds.select('roof' + str(self.idx) + '.vtx[4:5]')
            cmds.move(0, 0, 0.5 * self.dim[2], r=1)
        else:
            cmds.select(['roof' + str(self.idx) + '.vtx[2]', 'roof' + str(self.idx) + '.vtx[4]'])
            cmds.move(0.5 * self.dim[0], 0, 0, r=1)
            cmds.select(['roof' + str(self.idx) + '.vtx[3]', 'roof' + str(self.idx) + '.vtx[5]'])
            cmds.move(-0.5 * self.dim[0], 0, 0, r=1)

class building():
    def __init__(self, lot, lot_pos):
        self.lot        = lot
        self.lot_pos    = lot_pos
        #store the different house sections here
        self.sections      = []
        self.sectionWidth  = random.randint(3,5)
        self.sectionHeight = random.randint(3,3)
        self.sectionDepth  = random.randint(3,5)
        self.roofHeight = random.randint(1,3)
        self.roofType   = random.randint(1,3)
        self.lawnX      = 15
        self.lawnZ      = 15

    def generateSection(self):
        #build the main section of the house

        #after some calculations

        self.sections.append( buildingSection([self.sectionWidth, self.sectionHeight, self.sectionDepth], [self.roofType, self.roofHeight], [0,0,0]) )

    def lotPlacement(self):
        cmds.select('box'+str(i))
        cmds.move( random.randint(-(self.lawnX)/2+self.width,self.lawnX/2-self.width), self.height/2 +0.2, random.randint(-(self.lawnZ)/2+self.depth,self.lawnZ/2-self.depth), 'box', absolute=True )
        cmds.select('roof'+str(i))
        cmds.move( random.randint(-(self.lawnX)/2+self.width,self.lawnX/2-self.width), self.height/2 +0.2, random.randint(-(self.lawnZ)/2+self.depth,self.lawnZ/2-self.depth), 'roof', absolute=True )

    def setSectionPosition(self):

        # set values of where previous section is, in each axis
        neighbourLowX = self.sections[0].pos[0] - self.sections[0].dim[0]*0.5
        neighbourCenterX = self.sections[0].pos[0]
        neighbourHighX = self.sections[0].pos[0] + self.sections[0].dim[0]*0.5

        neighbourLowY = self.sections[0].pos[1] - self.sections[0].dim[1]*0.5
        neighbourCenterY = self.sections[0].pos[1]
        neighbourHighY = self.sections[0].pos[1] + self.sections[0].dim[1]*0.5

        neighbourLowZ = self.sections[0].pos[2] - self.sections[0].dim[2]*0.5
        neighbourCenterZ = self.sections[0].pos[2]
        neighbourHighZ = self.sections[0].pos[2] + self.sections[0].dim[2]*0.5

        #if self.sectionWidth < self.sectionDepth:

        #elif self.sectionWidth > self.sectionDepth:
        
    def extend(self):
        #extend the house if its posible
        print "extend"
        self.generateSubSections()

    def generateSubSections(self):
        #Create smaller subparts
        print("hej")
        self.newSectionProb = 1
        self.maxSectionCount = 1

        for a in range(0,self.maxSectionCount):
            #print("johanss")
            self.randomInt = random.randint(0,100)
            self.createSection = self.newSectionProb * self.randomInt/40
            # if self.createSection >= 0.5:
            print("Created subpart")

            main = self.sections[0]
            mainX = main.dim[0]
            mainY = main.dim[1]
            mainZ = main.dim[2]
            mainRoof = main.roof[1]

            print "a"
            sectionFullHeight = random.randint(3, mainY + mainRoof )

            #height
            if(sectionFullHeight > mainY):
                sectionHeight = mainY
                roofHeight = sectionFullHeight - mainY
            else:
                sectionHeight = random.randint(2, sectionFullHeight - 1 )
                roofHeight = sectionFullHeight - sectionHeight

            sectionWidth  = random.randint(2,5)
            print "b"
            mainVolume = mainX*mainY*mainZ / (sectionWidth * sectionHeight)
            if(mainVolume < 2):
                mainVolume = 2
            sectionDepth  = random.randint(2, mainVolume)
            roofType   = random.randint(1,3)

            #decide direction
            mainAlign = 1
            if(mainX > mainZ):
                mainAlign = 2

            newAlign = 1
            if(sectionWidth > sectionDepth):
                newAlign = 2

            sectionPos = [2,0,0]
            translateX = 0
            directionX = 0
            if(mainAlign == 1):
                if(newAlign == 1):
                    #side to side
                    if(sectionHeight < mainY):
                        #if the section is low: move maximum the halv main width to avoid roof bug
                        translateX = random.randint(0, mainX/2)
                    else:
                        #if its full height
                        translateX = random.randint(mainX/2, (mainX+sectionWidth)/2)
                if(newAlign == 2):
                    if(sectionFullHeight < mainY):
                        print "1"
                        translateX = random.randint(0, mainX/2 + sectionWidth/2)
                    else:
                        print "2"
                        translateX = random.randint(0, sectionWidth/2)

            else:
                print "3"
            directionX = ((random.randint(0,1))-0.5)*2
            sectionPos = [directionX * translateX ,0,0]

            self.sections.append( buildingSection([sectionWidth, sectionHeight, sectionDepth], [roofType, roofHeight], sectionPos) )
            #self.sections.append( buildingSection([1, 1, 1], [2, 1], [0,0,0]) )
            self.newSectionProb = self.newSectionProb - 1/self.maxSectionCount


    def build(self):
        self.generateSection()
        self.extend()
        for section in self.sections:
            section.build()


# Command
class scriptedCommand(OpenMayaMPx.MPxCommand):

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    # Invoked when the command is run.
    def doIt(self,argList):
        hus = building(0,0)
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
