# -*- coding: cp936 -*-
# current script directory:
# E:/R/Moon/code4crater/python
import os
import datetime
import string
import sys
from multiprocessing import Pool
from test_clearfile import *
from funcs import *

import arcpy
from arcpy import env
from arcpy.sa import *

#print 'level: '+sys.args[1]

#level=sys.args[1]
def region(workspace,center):
    ## index envelops into four regions
    ## based on the craters' (x,y)
    folder_ne=workspace+"north-east/"
    folder_se=workspace+"south-east/"
    folder_nw=workspace+"north-west/"
    folder_sw=workspace+"south-west/"
    
    if os.path.exists(folder_ne):
        CleanDir(folder_ne,False)
    os.mkdir(folder_ne)
    if os.path.exists(folder_se):
        CleanDir(folder_se,False)
    os.mkdir(folder_se)
    if os.path.exists(folder_nw):
        CleanDir(folder_nw,False)
    os.mkdir(folder_nw)
    if os.path.exists(folder_sw):
        CleanDir(folder_sw,False)
    os.mkdir(folder_sw)
    print("Directories are ready......")

    env.workspace = workspace
    records=arcpy.SearchCursor(center,"","","","")

    id_ne=[]
    id_nw=[]
    id_se=[]
    id_sw=[]

    for record in records:
        #if len(id_nw)>5:
        #    break
        lon=float(record.Lon_E)
        lat=float(record.Lat)
        if lon>0:
            if lat>0:
                id_ne.append(record.FID)
            elif lat<0:
                id_se.append(record.FID)
        elif lon<0:
            if lat>0:
                id_nw.append(record.FID)
            elif lat<0:
                id_sw.append(record.FID)
    ids_path=[folder_ne+'ids.txt',\
              folder_se+'ids.txt',\
              folder_nw+'ids.txt',\
              folder_sw+'ids.txt']
    ids=[id_ne,id_se,id_nw,id_sw]
    #print(ids)

    map(writeids,ids_path,ids)
    print("Indexing is finished......")

    return ids_path

def start(paras_father):
    print("paras_father")
    print(paras_father)
    in_dem=paras_father[0]
    in_center=paras_father[1]
    ids_txt=paras_father[2]
    ratio=paras_father[3]

    filedir,filename=os.path.split(ids_txt)# .../north-east
    name=filename.split('.')[0]# ids
    format=filename.split('.')[1]# txt

    #print("Current: "+filedir)

    f=open(ids_txt)
    paras_son=map(lambda x:\
                  [in_dem,in_center,filedir+"/"+str(int(x))+"/",ratio],\
                  f.readlines()[0][1:-1].split(','))
    f.close()
    print("Area Numbers: "+str(len(paras_son)))

    #process_num=16
    #print("Process Numbers: "+str(process_num))
    #print("slice_paras:")
    #slice_paras=map(lambda x:paras_son[x:x+process_num],\
    #               range(0,len(paras_son),process_num))
    #print(slice_paras)
    # parallel
    # parallel execution is failed by unstable processes
    #map(parallel,slice_paras)
    # serial
    map(split,paras_son)
    print(ids_txt+" is finished......")

def parallel(paras):
    pool = Pool(len(paras))
    pool.map(split,paras)
    pool.close()
    pool.join()

def split(paras):
    in_dem=paras[0]
    in_center=paras[1]
    target_dir=paras[2]
    ratio=paras[3]
    FID=target_dir.split('/')[-2]
    #print("target_dir: "+target_dir)

    if os.path.exists(target_dir):
        CleanDir(target_dir,False)
    os.mkdir(target_dir)
    # keep current ratio
    f=open(target_dir+'ratio_'+str(ratio)+'.txt','w')
    f.close()
    # print("Directory is ready......")

    arcpy.env.workspace = target_dir
    # 1. split center
    out_center=target_dir+"center"+FID+".shp"
    where_clause = '"FID" = '+FID
    Select(in_center,out_center,where_clause,False)
    
    # 2. create buffer with ratio
    # ./buf0_p30.shp
    out_buf=target_dir+"buf"+FID+".shp"
    Buffer(out_center,out_buf,ratio,False)

    # 3. create envelope
    # ./env0_p30.shp
    out_env=target_dir+"env"+FID+".shp"
    geotype='ENVELOPE'
    Envelope(out_buf,out_env,geotype,False)

    # 4. extract DEM in the envelope
    out_dem=target_dir+"dem"+FID
    # ExtractDemByMask(out_env,in_dem,out_dem,False)
    try:
        arcpy.env.extent=out_env
        arcpy.env.snapRaster=in_dem
        # Check out the ArcGIS Spatial Analyst extension license
        arcpy.CheckOutExtension("Spatial")

        # Execute ExtractByMask
        outExtractByMask = ExtractByMask(in_dem, out_env)
        # Save the output 
        outExtractByMask.save(out_dem)

        # 5. convert DEM to Ascii
        out_asc=target_dir+"asc"+FID+".txt"
        Raster2Ascii(out_dem,out_asc,False)

        print("Finished Area: "+FID+"......")
    except:
        print(arcpy.GetMessages())

def writeids(path,data):
    if len(data)>0:
        fwrite=open(path,'w')
        fwrite.writelines(str(data));
        fwrite.close();

def Raster2Ascii(raster,ascii,isprint):
    arcpy.RasterToASCII_conversion(raster, ascii)
    if isprint:
        print ('Raster2Ascii is finished....')

if __name__=='__main__':

    starttime_all = datetime.datetime.now()
    ############################### body ##################################
    ## 1. index envelops into four regions
    save_dir="F:/"
    # envelope='E:/tmp/env1.shp'
    center='E:/R/Moon/LOLA/GoranSalamuniccar_MoonCraters/LU78287GT_GIS/LU78287GT_Moon2000.shp'
    ratio=1.3
    ids_path=region(save_dir,center)

    ## 2. split dem with envelope
    dem="E:/R/Moon/LOLA/Moon_LRO_LOLA_global_LDEM_118m_Feb2013.cub"
    paras=map(lambda x:[dem,center,x,ratio],ids_path)
    #print(paras)
    map(start,paras)
    ################################ end ##################################

    endtime_all = datetime.datetime.now()
    print 'All processes are finished......'
    print 'Cost time: '+str((endtime_all - starttime_all).seconds)+' seconds'
    
    f=open(save_dir+"split_time.txt",'a')
    f.writelines('Split Cost time: '+str((endtime_all - starttime_all).seconds)+' seconds')
    f.close()

    #os.system('shutdown -s -f -t 10')