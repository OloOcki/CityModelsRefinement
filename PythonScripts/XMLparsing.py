import xml.etree.ElementTree as ET #xml parser
from fmeobjects import (FMELogFile,
                        FME_WARN)#FME native logs


FMELogFile().logMessageString("#--- The MXL parser has started: ---#", FME_WARN)
tree = ET.parse(FME_MacroValues['XMLinput']) 
root = tree.getroot()
 

def xmlChanger(feature):
   
    #Use dictionary index to accesss specific values

    #---------------------------------------------------------------#
    #---Access 'Screened Poisson'---#
    #---------------------------------------------------------------#

    #Set up value for the octree depth
    #default == 12
    octreeDepth = float(root[1][2].get('value')) #take deafult value
    userOctreeDepth = float(FME_MacroValues['userOctreeDepth']) #use input value from user
    strUOD = str(userOctreeDepth)
    
    #if a value from user is different from the default value then use the user value
    if userOctreeDepth == octreeDepth:
        FMELogFile().logMessageString(' -> Surface Reconstruction: Screened Poisson Octree Depth applied with default value 12')
    else:
        root[1][2].set('value', strUOD)
        FMELogFile().logMessageString(' -> Surface Reconstruction: Screened Poisson Octree Depth applied with value ' + strUOD)

        
    #---------------------------------------------------------------#
    #---Access 'Simplification: Quadric Edge Collapse Decimation'---#
    #---------------------------------------------------------------#

    #Set up desired number of faces in the end of the simplification process
    #Use it on your own risk! :) -> if this is not known go to the next step
    #default = 1160554
    targetFaceNr = float(root[2][0].get('value'))
    userTargetFaceNr = float(FME_MacroValues['userTargetFace'])
    uTFN = str(userTargetFaceNr)

    if targetFaceNr == userTargetFaceNr:
        FMELogFile().logMessageString(' -> Target number of faces same as default 1160554')
    elif 0 == userTargetFaceNr:
        FMELogFile().logMessageString(' -> Target number of faces NOT applied')
    else:
        root[2][0].set('value', uTFN)
        FMELogFile().logMessageString(' -> Target number of faces applied with value' + uTFN + 'only true if Percentage reduction set to 0')
    

    #Set up desired percentage of faces in the end of the simplification process
    #Easier for user to estimate only range (0..1)
    targetPerc = float(root[2][1].get('value'))
    userTargetPerc = float(FME_MacroValues['userTargetPerc'])
    uTP = str(userTargetPerc)
    
    if userTargetPerc == targetPerc:
        FMELogFile().logMessageString(' -> Percentage reduction (0..1) applied with default value')
    elif 0 == userTargetPerc:
        root[2][1].set('value', uTP)
        FMELogFile().logMessageString(' -> Percentage reduction (0..1) NOT applied')
    else:
        root[2][1].set('value', uTP)
        FMELogFile().logMessageString(' -> Percentage reduction (0..1) applied with value ' + uTP)


    #Set up some cleaning to the process, like erasing unreferenced vertices, bad faces, etc.
    #default = true
    #autoClean = bool(root[2][11].get('value'))
    userAutoClean = str(FME_MacroValues['autoClean'])
    
    if userAutoClean == 'true':
        FMELogFile().logMessageString(' -> Post-simplification cleaning applied')
    else:
        root[2][11].set('value', userAutoClean)
        FMELogFile().logMessageString(' -> Post-simplification cleaning NOT applied')
    
    #write new mlx    
    tree.write(FME_MacroValues['XMLOutput'])
    
    FMELogFile().logMessageString("#--- The MXL was parsed successfully ---#", FME_WARN)
            
