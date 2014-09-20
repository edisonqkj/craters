# -*- coding: cp936 -*-
# 
# merge shps according to valid_ids.txt if it exists
# instead of the check process in mergeshp.py
# 
## Time: 9/19/14
## Author: Edison Qian

import os
from ProjectIdentifyProcess import *
from sound import *

def MergeByTxt(dir,out_path):
    # valid_ids.txt exists
    # f:/north-west/
    ids=GetAllIdsByEval(dir+'valid_ids.txt')
    # no idpascx.shps --> create
    valid_paths=map(lambda id:\
                      ProjectIdentifyProcess(dir+str(id)+'/'),ids)
    sources=map(lambda id:\
                    dir+str(id)+'/casc'+str(id)+'/idpasc'+str(id)+'.shp',\
                    ids)
    sources=filter(lambda file:os.path.exists(file),sources)
    # print(sources)
    MergeShp(sources,out_path)
    print('')

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

    # res=map(lambda subdir:\
    #             filter(lambda id:\
    #                     os.path.exists(subdir+str(id)+'/casc'+str(id)+'/idpasc'+str(id)+'.shp'),\
    #                     GetAllIdsByEval(subdir+'valid_ids.txt')),\
    #         work_dir)
    # # print(res)
    # res_len=map(len,res)
    # print(res_len)
    have_ids_txt=filter(lambda d:os.path.exists(d+'valid_ids.txt'),work_dir)
    # "f:/north-east/" --> 'ne'
    work_dir_short=map(lambda dir:\
                        dir.split('/')[-2].split('-')[0][0]+\
                        dir.split('/')[-2].split('-')[1][0],\
                        have_ids_txt)
    if len(have_ids_txt)>0:
        print('have valid_ids.txt:')
        print(have_ids_txt)
        save_merge=save_dir+"merge/"
        if os.path.exists(save_merge):
            CleanDir(save_merge,False)
        os.mkdir(save_merge)
        targets=map(lambda dir:\
                save_merge+'merge_'+dir+'.shp',\
                work_dir_short)
        print(have_ids_txt)
        print(targets)
        map(MergeByTxt,have_ids_txt,targets)

        print("Merge is finished......")
        print("Please inform ******** Qian Ke Jian ******** Thanks! :D")
        musci_file='c:/SleepAway.wav'
        play(musci_file)
    else:
        print('No directory has valid_ids.txt......')
