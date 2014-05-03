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

def GetErrorTxtId(dir,err_func):
    # Format:
    # .../error+FID+"_"+err_func+".txt"
    # err_func = GetNoArea
    # .../north-east/error2_GetNoArea.txt
    if not os.path.exists(dir):
        print(dir+" is not found......")
        return None
    content=os.listdir(dir)
    # err_func="GetNoArea"
    # 'ids.txt'
    errortxtfiles=filter(lambda x:"error" in x and \
                                  ".txt" in x and \
                                  err_func in x,\
                                  content)
    return map(lambda x:int(x.split('_')[0][5:]),errortxtfiles)

def ReadEdgeShpId(txt):
    f=open(txt)
    content=f.readlines()
    f.close()
    records=content[1:]
    edge_ORIGFID=map(lambda record:\
                     int(record.split(',')[-1]),records)
    # print(len(edge_ORIGFID))
    return edge_ORIGFID

def Dir2Id(dirlist):
    # "f:/north-east/0/"--- 0
    id_int=map(lambda x:int(x.split('/')[-2]),dirlist)
    id_int.sort()
    return id_int

def Check(dir):
    # "f:/north-east/0/asc0.txt"
    # dir: "f:/north-east/"
    # return 3 lists--->split_ids,extract_ids,expand_ids
    print(dir+": Checking is started......")
    if not os.path.exists(dir):
        print(dir+' is not found......')
        return None#create dir
    ids_txt=dir+'ids.txt'
    if not os.path.exists(ids_txt):
        print(ids_txt+' is not found......')
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
    exist_ids=filter(lambda x:(not "error" in x) and (not ".txt" in x),content)
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
    # remove no filled area ids
    nofill_ids=GetErrorTxtId(dir,"GetNoArea")
    need_reextract_ids=Dir2Id(need_reextract)
    without_nofillids=list(set(need_reextract_ids).difference(set(nofill_ids)))
    if len(need_reextract)==len(left_exist_paths):
        return Dir2Id(absent_paths),without_nofillids,[]
    
    # check Cover failure dems
    '''
    left_extract_paths=list(set(left_exist_paths).difference(set(need_reextract)))
    need_expand=filter(lambda x:IsCoverFailed(x),left_extract_paths)
	'''
    print(dir+": Checking is finished......")
    return Dir2Id(absent_paths),without_nofillids,[]#Dir2Id(need_expand)

    #########################################################

if __name__=='__main__':
    center='e:/qkj/GoranSalamuniccar_MoonCraters/LU78287GT_GIS/LU78287GT_Moon2000.shp'
    # envelope='E:/qkj/env_p30.shp'
    dem="E:/qkj/Moon_LRO_LOLA_global_LDEM_118m_Feb2013.cub"
    edgeshp='E:/qkj/edge.txt'

    save_dir="d:/qkj/"
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

    # Here, we eliminate craters on the edge
    # Further, with re-projection of dem, they should be considered.
    edgeShpId=ReadEdgeShpId(edgeshp)

    ratio=1.3
    if ne is not None:
        # print(ne)
        ne=map(lambda x:list(set(x)-set(edgeShpId)),ne)
        print("North East:")
        # split
        if ne[0] is not None:
            print("split number: "+str(len(ne[0])))
            files_split=map(lambda x:[dem,center,north_east+str(x)+"/",ratio],\
                            ne[0])
            len(files_split)>0 and map(split,files_split)
        if ne[1] is not None:
            # extract
            ne[1].extend(ne[0])
            print("extract number: "+str(len(ne[1])))
            files_extract=map(lambda x:north_east+str(x)+"/asc"+str(x)+".txt",\
                              ne[1])
            len(files_extract)>0 and Execute(files_extract)
        print("OK......")
    else:
        print(north_east+" is empty......")
    # south east
    if se is not None:
        # print(se)
        se=map(lambda x:list(set(x)-set(edgeShpId)),se)
        print("South East:")
        if se[0] is not None:
            # split
            print("split number: "+str(len(se[0])))
            files_split=map(lambda x:[dem,center,south_east+str(x)+"/",ratio],\
                            se[0])
            len(files_split)>0 and map(split,files_split)
        if se[1] is not None:
            # extract
            se[1].extend(se[0])
            print("extract number: "+str(len(se[1])))
            files_extract=map(lambda x:south_east+str(x)+"/asc"+str(x)+".txt",\
                              se[1])
            len(files_extract)>0 and Execute(files_extract)
        print("OK......")
    else:
        print(south_east+" is empty......")
    # north west
    if nw is not None:
        # print(nw)
        nw=map(lambda x:list(set(x)-set(edgeShpId)),nw)
        print("North West:")
        if nw[0] is not None:
            # split
            print("split number: "+str(len(nw[0])))
            files_split=map(lambda x:[dem,center,north_west+str(x)+"/",ratio],\
                            nw[0])
            len(files_split)>0 and map(split,files_split)
        if nw[1] is not None:
            # extract
            nw[1].extend(nw[0])
            print("extract number: "+str(len(nw[1])))
            files_extract=map(lambda x:north_west+str(x)+"/asc"+str(x)+".txt",\
                              nw[1])
            len(files_extract)>0 and Execute(files_extract)
        print("OK......")
    else:
        print(north_west+" is empty......")
    # south west
    if sw is not None:
        # print(sw)
        sw=map(lambda x:list(set(x)-set(edgeShpId)),sw)
        print("South West:")
        if sw[0] is not None:
            # split
            print("split number: "+str(len(sw[0])))
            files_split=map(lambda x:[dem,center,south_west+str(x)+"/",ratio],\
                            sw[0])
            len(files_split)>0 and map(split,files_split)
        if sw[1] is not None:
            # extract
            sw[1].extend(sw[0])
            print("extract number: "+str(len(sw[1])))
            files_extract=map(lambda x:south_west+str(x)+"/asc"+str(x)+".txt",\
                              sw[1])
            len(files_extract)>0 and Execute(files_extract)
        print("OK......")
    else:
        print(south_west+" is empty......")