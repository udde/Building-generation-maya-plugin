#(import maya.cmds as c -> c.loadPlugin....)
#load plugin:
#maya.cmds.loadPlugin("/path/to/thisifle.py")
#run plugin:
#maya.cmds.build()

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
        self.roofType = roofSpec[0]
        self.roofHeight = roofSpec[1]
        self.idx = buildingSection.idx
        buildingSection.idx += 1

    def build(self):
        cmds.polyCube(sx=5, sy=5, sz=5, w=self.dim[0], h=self.dim[1], d=self.dim[2], n='box'+str(self.idx))
        cmds.move(self.pos[0],self.dim[1]*0.5,self.pos[2],r=1)
        self.buildRoof()
        cmds.select(clear = True)

    def buildRoof(self):
        cmds.select(clear = True)
        if(self.roofHeight < 2):
            cmds.polyPlane(w=self.dim[0],h=self.dim[2], sx=1, sy=1, n = 'roof' + str(self.idx))
            cmds.move(self.pos[0], self.dim[1] + 0.0*self.roofHeight, self.pos[2], r=1)
            cmds.select('roof'+str(self.idx)+'.f[1]')
            cmds.polyExtrudeFacet(s=[0.9,1.0,0.9], t=[0.0, self.roofHeight, 0.0])
        else:
            if(self.roofType == 1 or self.roofType == 2):
                cmds.polyCube(w=self.dim[0], h=self.roofHeight, d=self.dim[2], n = 'roof' + str(self.idx))
                cmds.move(self.pos[0], self.dim[1] + 0.5*self.roofHeight, self.pos[2], r=1)
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
    def __init__(self, lot, lotPos):
        self.lot        = lot
        self.lotPos    = lotPos
        #store the different house sections here
        self.lawnX      = lot[0]
        self.lawnZ      = lot[1]
        self.sections      = []
        self.sectionWidth  = random.randint(self.lawnX/2,self.lawnX)
        self.sectionHeight = random.randint(4,8)
        self.sectionDepth  = random.randint(self.lawnZ/2 ,self.lawnZ)
        self.roofHeight = random.randint(2,5)
        self.roofType   = random.randint(1,2)

    def generateSection(self):
        #build the main section of the house

        #after some calculations

        self.sections.append( buildingSection([self.sectionWidth, self.sectionHeight, self.sectionDepth], [self.roofType, self.roofHeight], [self.lotPos[0],self.lotPos[1],self.lotPos[2]]) )

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
        self.newSectionProb = 1
        self.maxSectionCount = 3

        for a in range(0,self.maxSectionCount):
            self.randomInt = random.randint(0,100)
            self.createSection = self.newSectionProb * self.randomInt/40
            if self.createSection >= 0.5:

                main = self.sections[0]
                mainX = main.dim[0]
                mainY = main.dim[1]
                mainZ = main.dim[2]
                mainRoof = main.roofHeight

                sectionFullHeight = random.randint(3, int(mainY + mainRoof))

                #height
                if(sectionFullHeight > mainY):
                    sectionHeight = mainY
                    roofHeight = sectionFullHeight - mainY
                else:
                    sectionHeight = random.randint(2, int(sectionFullHeight - 1 ))
                    roofHeight = sectionFullHeight - sectionHeight

                sectionWidth  = random.randint(8,int(self.lawnX-a*2))
                mainVolume = mainX*mainY*mainZ / (sectionWidth * sectionHeight)
                mainVolume *= 0.5
                if(mainVolume < 8):
                    mainVolume = 8
                sectionDepth = random.randint(8, int(mainVolume))
                sectionDepth = min(sectionDepth, int(self.lawnZ-a*2))
                roofType = random.randint(1,2)

                #decide direction
                mainAlign = 1
                if(mainX > mainZ):
                    mainAlign = 2

                newAlign = 1
                if(sectionWidth > sectionDepth):
                    newAlign = 2

                sectionPos = [0,0,0]
                translateX = 0
                directionX = 0
                translateZ = 0
                directionZ = 0
                if(mainAlign == 1):
                    # print "A"
                    #side to side
                        # print "a"
                    if(newAlign == 1):
                        if(sectionHeight < mainY):
                            #if the section is low: move maximum the halv main width to avoid roof bug
                            # print "1"
                            translateX = random.randint(0, int(mainX/2))
                        else:
                            # print "2"
                            #if its full height: move maximum half + half length, roof bug not in play
                            translateX = random.randint(int(mainX/2), int((mainX+sectionWidth)/2))
                        translateZ = random.randint(0, int(mainZ/2 + sectionDepth/4))

                    #counter side ways
                    if(newAlign == 2):
                        # print "b"
                        if(sectionFullHeight < mainY):
                            # print "1"
                            translateX = random.randint(0, int(mainX/2 + sectionWidth/2))
                            # print "2"
                        else:
                            translateX = random.randint(0, int(sectionWidth/2))
                        translateZ = random.randint(0, int(mainZ/2))
                #mainalign 2
                    # print "B"
                else:
                    #counter side ways
                    if(newAlign == 1):
                        # print "a"
                        if(sectionFullHeight < mainY):
                            # print "1"
                            #if the section is low: move maximum the halv main width to avoid roof bug
                            print mainZ/2
                            print sectionDepth/2
                            translateZ = random.randint(0, int(mainZ/2 + sectionDepth/2))
                        else:
                            # print "2"
                            #if its full height: move maximum half + half length, roof bug not in play
                            translateZ = random.randint(0, int(sectionDepth/2))
                        translateX = random.randint(0, int(mainX/2))

                    #side to side
                    if(newAlign == 2):
                        # print "b"
                        if(sectionHeight < mainY):
                            # print "1"
                            print mainZ/2
                            translateZ = random.randint(0, int(mainZ/2))
                        else:
                            # print "2"
                            translateZ = random.randint(int(mainZ/2), int((mainZ+sectionDepth)/2))
                        translateX = random.randint(0, int(mainX/2 + sectionWidth/4))
                        # translateZ = random.randint(0, mainZ/2 + sectionDepth/4)

                #Stay within the lot
                maxXtranslation = self.lawnX/2 - sectionWidth/2
                translateX = min(translateX, maxXtranslation)
                maxZtranslation = self.lawnZ/2 - sectionDepth/2
                translateZ = min(translateZ, maxZtranslation)

                directionX = ((random.randint(0,1))-0.5)*2
                directionZ = ((random.randint(0,1))-0.5)*2
                sectionPos = [self.lotPos[0] + directionX * translateX ,self.lotPos[1] , self.lotPos[2] + directionZ * translateZ]

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
        print "Trying to build a house in the selected allotment...."
        selected = cmds.ls(orderedSelection=True)
        if(len(selected) > 1):
            print "Illegal selection of allotment! Building aborted!"
        else:
            print "Selected %s" %(selected[0])
            tmp = selected[0]
            a = cmds.pointPosition(tmp+'.vtx[0]')
            b = cmds.pointPosition(tmp+'.vtx[1]')
            c = cmds.pointPosition(tmp+'.vtx[2]')
            d = cmds.pointPosition(tmp+'.vtx[3]')

            width = int(b[0] - a[0])
            print width
            depth = int(b[2] - c[2])
            print depth

            offsetX = b[0] - width/2
            offsetY = int(b[1])
            offsetZ = b[2] - depth/2
            # print "Calculated %d x %d lot at [ %d, %d ]." %(width, depth, offsetX, offsetY )

            house = building([width-2,depth-2],[offsetX,offsetY,offsetZ])
            house.build()

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
