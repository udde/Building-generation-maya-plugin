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

#placing subparts...
mode = "random"
#mode = "calculated"

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
        if(self.roofType == 1):
            cmds.polyPlane(w=self.dim[0],h=self.dim[2], sx=1, sy=1, n = 'roof' + str(self.idx))
            cmds.move(self.pos[0], self.dim[1] + 0.0*self.roofHeight, self.pos[2], r=1)
            cmds.select('roof'+str(self.idx)+'.f[1]')
            cmds.polyExtrudeFacet(s=[0.9,1.0,0.9], t=[0.0, self.roofHeight, 0.0])
        else:
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
        self.roofType   = random.randint(2,2)

    def generateSection(self):
        #build the main section of the house
        #after some calculations
        self.sections.append( buildingSection([self.sectionWidth, self.sectionHeight, self.sectionDepth], [self.roofType, self.roofHeight], [self.lotPos[0],self.lotPos[1],self.lotPos[2]]) )

    def lotPlacement(self):
        cmds.select('box'+str(i))
        cmds.move( random.randint(-(self.lawnX)/2+self.width,self.lawnX/2-self.width), self.height/2 +0.2, random.randint(-(self.lawnZ)/2+self.depth,self.lawnZ/2-self.depth), 'box', absolute=True )
        cmds.select('roof'+str(i))
        cmds.move( random.randint(-(self.lawnX)/2+self.width,self.lawnX/2-self.width), self.height/2 +0.2, random.randint(-(self.lawnZ)/2+self.depth,self.lawnZ/2-self.depth), 'roof', absolute=True )

    def setPos(self, newSectionWidth, newSectionFullHeight, newSectionDepth):
        while True:
            #Section is randomly selected where new section will be placed from
            baseSection = random.randint(0,len(self.sections)-1)
            #get variables of base section
            sectionCenter = self.sections[baseSection].pos
            sectionDim = self.sections[baseSection].dim
            #save corners of the base section
            corner00 = [sectionCenter[0] - sectionDim[0]*0.5, sectionCenter[1], sectionCenter[2] - sectionDim[2]*0.5 ]
            corner10 = [sectionCenter[0] + sectionDim[0]*0.5, sectionCenter[1], sectionCenter[2] - sectionDim[2]*0.5 ]
            corner01 = [sectionCenter[0] - sectionDim[0]*0.5, sectionCenter[1], sectionCenter[2] + sectionDim[2]*0.5 ]
            corner11 = [sectionCenter[0] + sectionDim[0]*0.5, sectionCenter[1], sectionCenter[2] + sectionDim[2]*0.5 ]
            #save corners in a list 
            sectionCorners = [corner00, corner10, corner01, corner11]

            #give new section the position of one of the corners of the base section
            cornerIndex = random.randint(0,len(sectionCorners)-1)
            newSectionPos = sectionCorners[cornerIndex]
            #generate direction x or z in which new section will be placed along (width or depth). iDir = intervallDirection
            iDir = random.randint(0,1)*2

            neighbourCorner = sectionCorners[0]
            #Find neighbouring corner in the direction iDir
            for i in range(0, len(sectionCorners)-1):
                #if the new point has the coordinate in direction iDir in common with any corner in the list, we have found a neighbour 
                #We ensure that the neighbour of the new point isnt itself
                if i!=cornerIndex and sectionCorners[i][iDir] == newSectionPos[iDir]:
                    neighbourCorner = sectionCorners[i]

            #initiate limits
            lowerLimit = neighbourCorner[iDir]
            upperLimit = newSectionPos[iDir]
            breaky = False

            #Calculate lower and upper limit in which you will randomize new position for the new section
            for j in range(0,len(self.sections)-1):
                if ((self.sections[j].pos[0] - (self.sections[j].dim[0]*0.5)) < newSectionPos[0] < (self.sections[j].pos[0] + self.sections[j].dim[0]*0.5)) and ((self.sections[j].pos[2] - (self.sections[j].dim[2]*0.5)) < newSectionPos[2] < (self.sections[j].pos[2] + self.sections[j].dim[2]*0.5)):
                    breaky = True

                #Check direction in which new building will be placed
                if (iDir == 0):
                    #Check neigbourCorners position in relation
                    if (neighbourCorner[iDir] < newSectionPos[iDir]):
                        lowerLimit = neighbourCorner[iDir]
                        upperLimit = newSectionPos[iDir]
                        #Ajust limit if another section is in the way
                        if (self.sections[j].pos[2] - (self.sections[j].dim[2]*0.5) < newSectionPos[2] < self.sections[j].pos[2] + self.sections[j].dim[2]*0.5):
                            lowerLimit = self.sections[j].pos[iDir] + (newSectionWidth*0.5+1)

                    else:
                        lowerLimit = newSectionPos[iDir]
                        upperLimit = neighbourCorner[iDir]
                        if (self.sections[j].pos[2] - (self.sections[j].dim[2]*0.5) < newSectionPos[2] < self.sections[j].pos[2] + self.sections[j].dim[2]*0.5):
                            upperLimit = self.sections[j].pos[iDir] - (newSectionWidth*0.5-1)

                #Same theory as for iDir == 0
                if iDir == 2:
                    if neighbourCorner[iDir] < newSectionPos[iDir]:
                        lowerLimit = neighbourCorner[iDir]
                        upperLimit = newSectionPos[iDir]
                        if (self.sections[j].pos[0] - (self.sections[j].dim[0]*0.5) < newSectionPos[0] < self.sections[j].pos[0] + self.sections[j].dim[0]*0.5):
                            lowerLimit = self.sections[j].pos[iDir] + (newSectionDepth*0.5+1)

                    else:
                        lowerLimit = newSectionPos[iDir]
                        upperLimit = neighbourCorner[iDir]
                        if self.sections[j].pos[0] - (self.sections[j].dim[0]*0.5) < newSectionPos[0] < self.sections[j].pos[0] + self.sections[j].dim[0]*0.5:
                            upperLimit = self.sections[j].pos[iDir] - (newSectionDepth*0.5-1)

            if (((newSectionWidth*0.5) < (upperLimit - lowerLimit)) or breaky == True):
                break

        newSectionPos[iDir] = random.uniform(lowerLimit,upperLimit)
        return newSectionPos

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

                #height
                roofType = random.randint(1,2)

                sectionFullHeight = random.randint(4, int(mainY + mainRoof))
                if(roofType == 1):
                    roofHeight = 1
                    sectionHeight = random.randint(3, int(mainY) - roofHeight )

                else:
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

                #decide direction
                mainAlign = 1
                if(mainX > mainZ):
                    mainAlign = 2

                newAlign = 1
                if(sectionWidth > sectionDepth):
                    newAlign = 2

                sectionPos = self.setPos(sectionWidth, sectionFullHeight, sectionDepth)
                if(mode == "random"):
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
                            if(sectionWidth < mainX): translateX = int(sectionWidth/2)
                        translateZ = random.randint(0, int(mainZ/2) - int(sectionDepth/2))
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
                            if(sectionDepth < mainZ): translateZ = int(sectionDepth/2)
                        translateX = random.randint(0, int(mainX/2)-int(sectionWidth/2))

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
                #maxXtranslation = self.lawnX/2 - sectionWidth/2
                #translateX = min(translateX, maxXtranslation)
                #maxZtranslation = self.lawnZ/2 - sectionDepth/2
                #translateZ = min(translateZ, maxZtranslation)

                directionX = ((random.randint(0,1))-0.5)*2
                directionZ = ((random.randint(0,1))-0.5)*2
                if(mode == "random"):
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
        #print "Trying to build a house..."
        selected = cmds.ls(orderedSelection=True)
        if(len(selected) != 1):
            house = building([20,20],[0,0,0])
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
