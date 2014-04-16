# -*- coding: cp936 -*-
## Check unsplitted dem & execute
## Check dem without extraction & execute
## Check extent not enough

## Time: 16/4/14
## Author: Edison Qian

from __future__ import print_function
import os
import re
from splitdem import *
from execute import *
from OutletAnalysis import *

def IsSplitFailed(dir):
    # "f:/north-east/0/"
    if not os.path.exists(dir):
        print(dir+" is not found......")
        return True
    content=os.listdir(dir)
    if len(content)==0:
        print(dir+" is empty......")
        return True
    FID=dir.split('/')[-2]
    dem="dem"+FID
    env="env"+FID+".shp"

    return dem not in content \
        or env not in content

def IsExtractionFailed(dir):
    # "f:/north-east/0/"
    if not os.path.exists(dir):
        print(dir+" is not found......")
        return True
    content=os.listdir(dir)
    FID=dir.split('/')[-2]
    casc="casc"+FID
    tasc="tasc"+FID
    if casc not in content or tasc not in content:
        return True
    # "f:/north-east/0/casc0/"
    content=os.listdir(dir+casc)
    pasc="pasc"+FID+".shp"
    pasc_txt="pasc"+FID+".txt"

    return casc not in content \
        or pasc not in content \
        or pasc_txt not in content

def IsCoverFailed(dir):
    # "f:/north-east/0/"
    if not os.path.exists(dir):
        print(dir+" is not found......")
        return True
    # "f:/north-east/0/casc0/pasc0.txt"
    FID=dir.split('/')[-2]
    txt=dir+"casc"+FID+"/pasc"+FID+".txt"
    if not os.path.exists(txt):
        return True

    head,data=ReadAscii(txt)
    return IsExpanded(data)

def IsExpanded(data):
    # data is binary: 0, 1
    if len(data)<3 or len(data[0])<3:
        return True
    # check 4 edges
    Up=''.join(map(lambda x:str(x),data[0]))
    Down=''.join(map(lambda x:str(x),data[-1]))
    Left=''.join(map(lambda x:str(x[0]),data))
    Right=''.join(map(lambda x:str(x[-1]),data))
    
    # clockwise check 4 corners
    # Up_Left_Corner
    # 1 1 1
    # 0 1 1
    # 0 0 1
    # Up_Left_Corner: 00111
    Up_Left_Corner=''.join(map(lambda x:str(x[0]),data[1:3])[::-1])+\
                   ''.join(map(lambda x:str(x),data[0][:3]))
    # Up_Right_Corner
    # 0 0 1
    # 0 1 1
    # 1 1 1
    # Up_Right_Corner: 00111
    Up_Right_Corner=''.join(map(lambda x:str(x),data[0][-3:]))+\
                    ''.join(map(lambda x:str(x[-1]),data[1:3]))
    # Down_Left_Corner
    # 1 1 1
    # 1 1 0
    # 1 0 0
    # Down_Left_Corner: 00111
    Down_Left_Corner=''.join(map(lambda x:str(x),data[-1][1:3])[::-1])+\
                     ''.join(map(lambda x:str(x[0]),data[-3:])[::-1])
    # Down_Right_Corner
    # 1 0 0
    # 1 1 0
    # 1 1 1
    # Down_Right_Corner: 00111
    Down_Right_Corner=''.join(map(lambda x:str(x[-1]),data[-3:]))+\
                    ''.join(map(lambda x:str(x),data[-1][-3:-1])[::-1])
    # pattern recognize
    pattern=re.compile('1{3}')# 000111000
    res=pattern.findall(Up+' '+Down+' '+Left+' '+Right+' '+\
                        Up_Left_Corner+' '+\
                        Up_Right_Corner+' '+\
                        Down_Left_Corner+' '+\
                        Down_Right_Corner)
    return len(res)>0

def Dir2Id(dirlist):
    # "f:/north-east/0/"--- 0
    return map(lambda x:int(x.split('/')[-2]),dirlist)

def Check(dir):
    # "f:/north-east/0/asc0.txt"
    # dir: "f:/north-east/"
    # return 3 lists--->split_ids,extract_ids,expand_ids
    print(dir+": Checking is started......")
    if not os.path.exists(dir):
        # print(dir+' is not found......')
        return None#create dir
    ids_txt=dir+'ids.txt'
    if not os.path.exists(ids_txt):
        # print(ids_txt+' is not found......')
        return None
    #########################################################
    # all ids
    f=open(ids_txt)
    all_ids=map(lambda x:str(int(x)),\
                f.readlines()[0][1:-1].split(','))
    f.close()
    # print(len(all_ids))
    # already existing ids
    content=os.listdir(dir)
    #exist_ids.remove('ids.txt')
    exist_ids=filter(lambda x:not ".txt" in x,content)
    # print(type(exist_ids))

    # absent ids
    absent_ids=list(set(all_ids).difference(set(exist_ids)))

    #########################################################
    # convert ids to paths
    exist_paths=map(lambda x:dir+x+"/",exist_ids)#
    absent_paths=map(lambda x:dir+x+"/",absent_ids)#

    # "f:/north-east/0/"
    # check Split failure dems
    need_resplit=filter(lambda x:IsSplitFailed(x),exist_paths)
    absent_paths.extend(need_resplit)
    if len(need_resplit)==len(exist_paths):
        return Dir2Id(absent_paths),[],[]

    # check Extraction failure dems
    left_exist_paths=list(set(exist_paths).difference(set(need_resplit)))
    need_reextract=filter(lambda x:IsExtractionFailed(x),left_exist_paths)
    if len(need_reextract)==len(left_exist_paths):
        return Dir2Id(absent_paths),Dir2Id(need_reextract),[]
    
    # check Cover failure dems
    left_extract_paths=list(set(left_exist_paths).difference(set(need_reextract)))
    need_expand=filter(lambda x:IsCoverFailed(x),left_extract_paths)
	
    print(dir+": Checking is finished......")
    return Dir2Id(absent_paths),Dir2Id(need_reextract),Dir2Id(need_expand)

    #########################################################

if __name__=='__main__':
    envelope='E:/qkj/env_p30.shp'
    dem="E:/qkj/Moon_LRO_LOLA_global_LDEM_118m_Feb2013.cub"

    save_dir="e:/qkj/split/"
    north_east=save_dir+"north-east/"
    south_east=save_dir+"south-east/"
    north_west=save_dir+"north-west/"
    south_west=save_dir+"south-west/"

    ne,se,nw,sw=map(Check,[north_east,south_east,north_west,south_west])
    print("Checking is finished......")
    # north east
    # print(type(ne[0]))
    # print(type(ne[1]))
    # print(ne[1].extend(ne[0]))
    # print(ne[2])
    if ne is not None:
        # print(ne)
        # split
        files_split=map(lambda x:[dem,envelope,north_east+str(x)+"/"],\
                        ne[0])
        map(split,files_split)
        # extract
        ne[1].extend(ne[0])
        files_extract=map(lambda x:north_east+str(x)+"/asc"+str(x)+".txt",\
                          ne[1])
        Execute(files_extract)
    else:
        print(north_east+" is empty......")
    # south east
    if se is not None:
        # print(se)
        # split
        files_split=map(lambda x:[dem,envelope,south_east+str(x)+"/"],\
                        se[0])
        map(split,files_split)
        # extract
        se[1].extend(se[0])
        files_extract=map(lambda x:south_east+str(x)+"/asc"+str(x)+".txt",\
                          se[1])
        Execute(files_extract)
    else:
        print(south_east+" is empty......")
    # north west
    if nw is not None:
        # print(nw)
        # split
        files_split=map(lambda x:[dem,envelope,north_west+str(x)+"/"],\
                        nw[0])
        map(split,files_split)
        # extract
        nw[1].extend(nw[0])
        files_extract=map(lambda x:north_west+str(x)+"/asc"+str(x)+".txt",\
                          nw[1])
        Execute(files_extract)
    else:
        print(north_west+" is empty......")
    # south west
    if sw is not None:
        # print(sw)
        # split
        files_split=map(lambda x:[dem,envelope,south_west+str(x)+"/"],\
                        sw[0])
        map(split,files_split)
        # extract
        sw[1].extend(sw[0])
        files_extract=map(lambda x:south_west+str(x)+"/asc"+str(x)+".txt",\
                          sw[1])
        Execute(files_extract)
    else:
        print(south_west+" is empty......")