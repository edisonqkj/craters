# -*- coding: cp936 -*-

# merge all the input shapefiles into a single shp file
# i.e. merge individual craters into a shp file

## Time: 21/4/14
## Author: Edison Qian

from __future__ import print_function
import os
import arcpy
from check import *
from test_clearfile import *

def GetAllIds(ids_txt):
    f=open(ids_txt)
    all_ids=map(lambda x:str(int(x)),\
                f.readlines()[0][1:-1].split(','))
    f.close()
    # print(len(all_ids))

def MergeShp(sources,target):
    # arcpy.env.workspace = 
    try:
        arcpy.Merge_management(sources, target)
        print(target+" is Merged......")
    except:
        print("MergeShp:\n"+arcpy.GetMessages()+"\n\n")
        return unicode("MergeShp:\n"+arcpy.GetMessages()+"\n\n")

if __name__=='__main__':
    save_dir='f:/'
    expect_dir=[save_dir+"north-east/",\
                save_dir+"south-east/",\
                save_dir+"north-west/",\
                save_dir+"south-west/"]
    work_dir=filter(lambda dir:os.path.exists(dir),expect_dir)
    if len(work_dir)==0:
        print("No directory is found......")
        sys.exit()

    print("Current Directories:")
    print(work_dir)

    ##############################################################
    # existing sub-directories of each work_dir
    # get "f:/north-east/0/"
    exist_paths=\
        map(lambda subdir:\
            map(lambda validfolder:subdir+validfolder+"/",\
                filter(lambda folder:\
                       (not "error" in folder) and \
                       (not ".txt" in folder),\
                        os.listdir(subdir))\
                ),\
            work_dir)
    # check successful extraction & covering
    valid_paths=\
        map(lambda subdir:\
            filter(lambda folder:\
                   not IsExtractionFailed(folder) and \
                   not IsCoverFailed(folder),\
                   subdir),\
            exist_paths)
    # "f:/north-east/0/"--- 0
    valid_ids=map(lambda subdir:Dir2Id(subdir),valid_paths)

    print("Checking is finished......")
    # Sum of craters in four regions
    num_of_all_craters=reduce(lambda x,y:x+y,map(len,valid_paths))
    print("Numbers: "+str(num_of_all_craters))

    if num_of_all_craters==0:
        print("No valid crater is found......")
        sys.exit()

    ##############################################################
    sources=\
        map(lambda subdir,ids:\
            map(lambda cdir,cid:\
                cdir+"casc"+str(cid)+"/pasc"+str(cid)+".shp",\
                subdir,ids),\
            valid_paths,valid_ids)

    save_merge=save_dir+"merge/"
    if os.path.exists(save_merge):
        CleanDir(save_merge,False)
    os.mkdir(save_merge)
    print("Directories are ready......")

    target=[save_merge+"merge_ne.shp",save_merge+"merge_se.shp",\
            save_merge+"merge_nw.shp",save_merge+"merge_sw.shp"]
    ##############################################################
    map(MergeShp,sources,target)
    print("Merge is finished......")