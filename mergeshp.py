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
from checkfuncs import *
from ProjectIdentifyProcess import *

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

def SearchCondition(dir):
    # dir='f:/north-east/0/'
    base,name=os.path.split(dir)
    id_str=os.path.basename(base)# 0

    # ratio_x.txt
    ratio_file=filter(lambda file: \
                        ('ratio' in file), \
                    os.listdir(dir))
    if len(ratio_file)==0:
        # Condition I: ratio_x.txt doesnt exist
        return (not IsExtractionFailed(dir)) and (not IsCoverFailed(dir))
    else:
        ratio_less_than_4=filter(lambda r:not '4.0' in r,ratio_file)
        # Condition II: ratio_x.txt, x<4.0 && size< 100M
        return len(ratio_less_than_4)>1 and (not IsOutofExtent(dir+'asc'+id_str+'.txt'))

if __name__=='__main__':
    save_dir="f:/"
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
    # "f:/north-east/" --> 'ne'
    work_dir_short=map(lambda dir:\
                        dir.split('/')[-2].split('-')[0][0]+\
                        dir.split('/')[-2].split('-')[1][0],\
                        work_dir)
    # print(work_dir_short)
    ##############################################################
    # Check Process
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
    print("Checking is started......")
    valid_paths=\
        map(lambda subdir:\
            filter(lambda folder:\
                SearchCondition(folder),\
                   # not IsExtractionFailed(folder) and \
                   # not IsCoverFailed(folder),\
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
    # Project && Identify Process
    print("Process is started......")
    map(lambda subdir:\
            map(lambda folder:\
                ProjectIdentifyProcess(folder),\
                subdir),\
        valid_paths)
    print("Process is finished......")
    ##############################################################
    # Merge Process
    sources=\
        map(lambda subdir,ids:\
            map(lambda cdir,cid:\
                cdir+"casc"+str(cid)+"/ipasc"+str(cid)+".shp",\
                subdir,ids),\
            valid_paths,valid_ids)

    save_merge=save_dir+"merge/"
    if os.path.exists(save_merge):
        CleanDir(save_merge,False)
    os.mkdir(save_merge)
    print("Directories are ready......")

    # work_dir_short:['ne']
    target=map(lambda dir:\
                save_merge+'merge_'+dir+'.shp',\
                work_dir_short)
    # print(target)
    # target=[save_merge+"merge_ne.shp",save_merge+"merge_se.shp",\
    #         save_merge+"merge_nw.shp",save_merge+"merge_sw.shp"]
    map(MergeShp,sources,target)
    print("Merge is finished......")
    ##############################################################