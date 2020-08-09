import os
import glob
from pyntcloud import PyntCloud
from fmeobjects import (FMELogFile,
                        FME_WARN)#FME native logs


####READ####

#read path as string
bldXYZ = str(FME_MacroValues['tmpXYZbld'])

#read, get all xyz files in a directory
list_walls = [PyntCloud.from_file(files,
                           sep=";",
                           header=1,
                           names=["x","y","z"]) 
                           for files in glob.glob (bldXYZ + '\*.xyz')]
                           
                           
#list of xyz file names
names_walls = [os.path.basename(x) for x in glob.glob(bldXYZ + '\*.xyz')]

#get range of elements to iterate on
index = len(list_walls)

#fire the RANSAC algorithm
FMELogFile().logMessageString("#--- The RANSAC algorithm has been triggered... ---#", FME_WARN)

def ransac(feature):
        
    for i in range (index):  
    
        ###RANSAC###
        # parameter t in RANSAC
        kwargs = {"max_dist": 0.1}
        
        is_plane = list_walls[i].add_scalar_field("plane_fit", **kwargs)
            
        ##select point cloud having only inliers (value==1), so-> not equal 0
        selectInliers = list_walls[i].points.loc[list_walls[i].points["is_plane"] == 1]
                
        ####WRITE####
        #create directory for output files and check if it exists already
        directoryInliers= str(FME_MacroValues['tmpXYZbldInliers'])
        
        #create one path
        writing_pathInliers = directoryInliers + '/' + names_walls[i]
        
        
        #write selected inliers as csv point cloud
        selectInliers.to_csv(writing_pathInliers, index = False, header=True)
        


        
