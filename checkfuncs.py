# -*- coding: cp936 -*-
## Check functions

## Time: 5/16/2014
## Author: Edison Qian

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

    # eliminate NoData rows & columns
    # ffdir: "F:/north-east/0/tasc0/ffdir.txt"
    txt_std=dir+"tasc"+FID+"/ffdir.txt"
    head_std,data_std=ReadAscii(txt_std)
    nodata=0#head_std[5]
    head,data=ReadAscii(txt)

    return IsExpanded(ContractMatrix(data,data_std,nodata))

def ContractMatrix(ori_data,std_data,nodata):
    # contract matrix without nodata value
    # return contracted matrix with respect to std_data
    cols=len(std_data[0])
    rows=len(std_data)
    # in each row
    res_row=map(lambda r:\
                len(filter(lambda c:c==nodata,r)),\
                std_data)
    # in each col
    res_col=map(lambda i:\
                len(filter(lambda x:x==nodata,\
                           map(lambda r:r[i],std_data))),\
                range(cols))
    row_index=[i for i,j in enumerate(res_row) if j!=cols]
    col_index=[i for i,j in enumerate(res_col) if j!=rows]
    # example:
    # res_row=[5,5,5,0,0,0,0,5]
    # row_index=[3,4,5,6]
    # row_up=3
    # row_down=6
    row_up= min(row_index)
    row_down=max(row_index)
    col_left= min(col_index)
    col_right=max(col_index)

    res_data=map(lambda x:x[col_left:col_right+1],\
                 ori_data[row_up:row_down+1])
    return res_data

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

def Str2Int(data):
    return map(lambda x: int(x),data)

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

def ClearFakeErrorFiles(dir):
    print(dir+": Clearing is started......")
    if not os.path.exists(dir):
        print(dir+' is not found......')
        return None#create dir
    # find all error id in each directory
    all_error_ids=GetErrorTxtId(dir,'')
    fake_error_ids=\
    filter(lambda x: not IsExtractionFailed(dir+str(x)+'/'),\
                           all_error_ids)
    print('error nums:%d' %(len(all_error_ids)-len(fake_error_ids)))
    # remove errorfile if corresponding result is got
    # need dictionary structure {'id':file}
    map(lambda x:'error'+str(x)+'_',\
        fake_error_ids)
    print(dir+": Clearing is finished......")
    return list(set(all_error_ids).difference(set(fake_error_ids)))

def ExpandCheck(dir):
    # dir: "f:/north-east/"
    # return 1 list--->expand_ids (str)
    print(dir+": Checking is started......")
    if not os.path.exists(dir):
        print(dir+' is not found......')
        return None#create dir

    exp_path=dir+'exp_ids.txt'
    if not os.path.exists(exp_path):
        # first to expand process
        exact_error_ids=map(lambda x:str(x),ClearFakeErrorFiles(dir))
        
        # subdirectories
        content=os.listdir(dir)
        subdirs=filter(lambda x:(not "error" in x) and (not ".txt" in x),content)
        check_ids=list(set(subdirs).difference(set(exact_error_ids)))
        
        # filter out ids for reextraction
        print('Cover checking is stated......')
        reextraction_ids=filter(lambda x:IsCoverFailed(dir+x+'/'),check_ids)
        
        # write into txt
        f=open(exp_path,'w')
        f.writelines(str(Str2Int(reextraction_ids)))
        f.close()
    else:
        # continue last process
        f=open(exp_path)
        record_ids=map(lambda x:str(int(x)),\
                       f.readlines()[0][1:-1].split(','))
        f.close()
        # 'ratio_'+str(ratio)+'.txt'
        reextraction_ids=\
        filter(lambda x:\
               not os.path.exists(dir+x+'/ratio_4.0.txt'),\
               record_ids)
        # if last process is stopped by sudden power off,
        # exp_path should be updated.
        # write into txt
        f=open(exp_path,'w')
        f.writelines(str(Str2Int(reextraction_ids)))
        f.close()

    print(dir+": Checking is finished......")
    return reextraction_ids

def ReExtractionByRatio(paras):
    # dem,center,f:/north-east/0/
    dem=paras[0]
    center=paras[1]
    target=paras[2]
    ratio_max=paras[3]
    FID=target.split('/')[-2]

    ratios=map(lambda x:1.3+0.1*x,\
               range(1,(ratio_max-1.3)/0.1+1))
    
    for ratio in ratios:
        # resplit dem with new ratio
        split([dem,center,target,ratio])
        # reextract
        if not IsSplitFailed(target):
            ExtractRidge(target+'asc'+str(FID)+".txt")
            if not IsExtractionFailed(target):
                if not IsCoverFailed(target):
                    return ''
    return target#ratio=2