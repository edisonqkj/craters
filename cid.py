import os
from ProjectIdentifyProcess import *

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

    res=map(lambda subdir:\
                filter(lambda id:\
                        os.path.exists(subdir+str(id)+'/casc'+str(id)+'/idpasc'+str(id)+'.shp'),\
                        GetAllIdsByEval(subdir+'valid_ids.txt')),\
            work_dir)
    print(res)
    res_len=map(len,res)
    print(res_len)
