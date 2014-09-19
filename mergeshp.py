# -*- coding: cp936 -*-

# merge all the input shapefiles into a single shp file
# i.e. merge individual craters into a shp file

## Time: 21/4/14
## Author: Edison Qian

from __future__ import print_function
import os
from ProjectIdentifyProcess import *
from sound import *

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
    # write valid ids into txt
    map(lambda subdir,ids:Write2Txt(subdir+'valid_ids.txt',str(ids)),\
                            work_dir,valid_ids)

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
                cdir+"casc"+str(cid)+"/idpasc"+str(cid)+".shp",\
                subdir,ids),\
            valid_paths,valid_ids)
    # check existing idpascx.shp after ProjectIdentifyProcess
    # missing shp not recorded in valid_paths
    sources=map(lambda subdir:\
                     filter(lambda path:\
                              os.path.exists(path),subdir),sources)

    save_merge=save_dir+"merge/"
    if os.path.exists(save_merge):
        CleanDir(save_merge,False)
    os.mkdir(save_merge)
    print("Directories are ready......")

    # work_dir_short:['ne']
    target=map(lambda dir:\
                save_merge+'merge_'+dir+'.shp',\
                work_dir_short)
    # print(sources)
    # target=[save_merge+"merge_ne.shp",save_merge+"merge_se.shp",\
    #         save_merge+"merge_nw.shp",save_merge+"merge_sw.shp"]
    # map(MergeShp,sources,target)
    print("Merge is finished......")
    print("Please inform ******** Qian Ke Jian ******** Thanks! :D")
    musci_file='c:/SleepAway.wav'
    play(musci_file)
    ##############################################################