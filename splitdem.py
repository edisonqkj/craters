# -*- coding: cp936 -*-
# current script directory:
# E:/R/Moon/code4crater/python
import os
import datetime
import string
import sys
from test_clearfile import *

import arcpy
from arcpy import env
from arcpy.sa import *

#print 'level: '+sys.args[1]

#level=sys.args[1]
def Process(in_dem,in_envelope):
    workspace='F:/'

    folder_ne=workspace+"north-east/"
    folder_se=workspace+"south-east/"
    folder_nw=workspace+"north-west/"
    folder_sw=workspace+"south-west/"

    in_dem="E:/R/Moon/LOLA/Moon_LRO_LOLA_global_LDEM_118m_Feb2013.cub"
    in_envelope='E:/tmp/env1.shp'

    starttime_all = datetime.datetime.now()

    env.workspace = workspace

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
    print("Directories is ready......")
############################ Body ###########################
    print 'Splitting DEM starts......'
    starttime0 = datetime.datetime.now()
    records=arcpy.SearchCursor(in_envelope,"","","","")

    id_ne=[]
    id_nw=[]
    id_se=[]
    id_sw=[]

    for record in records:
        #if len(id_nw)>5:
        #    break
        '''
        1. iterate to select an envelope from envelopes layer
        '''
        lon=float(record.Lon_E)
        lat=float(record.Lat)
        if lon>0:
            if lat>0:
                target_dir=folder_ne+str(record.ORIG_FID)+"/"
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
                outshp=target_dir+"env"+str(record.ORIG_FID)+".shp"
                id_ne.append(record.ORIG_FID)
            elif lat<0:
                target_dir=folder_se+str(record.ORIG_FID)+"/"
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
                outshp=target_dir+"env"+str(record.ORIG_FID)+".shp"
                id_se.append(record.ORIG_FID)
        elif lon<0:
            if lat>0:
                target_dir=folder_nw+str(record.ORIG_FID)+"/"
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
                outshp=target_dir+"env"+str(record.ORIG_FID)+".shp"
                id_nw.append(record.ORIG_FID)
            elif lat<0:
                target_dir=folder_sw+str(record.ORIG_FID)+"/"
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
                outshp=target_dir+"env"+str(record.ORIG_FID)+".shp"
                id_sw.append(record.ORIG_FID)

        arcpy.env.extent=in_envelope
        where_clause = '"ORIG_FID" = '+str(record.ORIG_FID)
        arcpy.Select_analysis(in_envelope, outshp, where_clause)

        '''
        2. extract DEM in the envelope
        '''
        out_dem=target_dir+"dem"+str(record.ORIG_FID)

        arcpy.env.extent=outshp
        arcpy.env.snapRaster=in_dem
        # Check out the ArcGIS Spatial Analyst extension license
        arcpy.CheckOutExtension("Spatial")

        # Execute ExtractByMask
        outExtractByMask = ExtractByMask(in_dem, outshp)
        # Save the output 
        outExtractByMask.save(out_dem)

        '''
        3. convert DEM to Ascii
        '''
        out_asc=target_dir+"asc"+str(record.ORIG_FID)+".txt"
        Raster2Ascii(out_dem,out_asc,False)

        print("Finished Area: "+str(record.ORIG_FID)+"......")


    ids_path=[folder_ne+'ids.txt',\
              folder_se+'ids.txt',\
              folder_nw+'ids.txt',\
              folder_sw+'ids.txt']
    ids=[id_ne,id_se,id_nw,id_sw]
    #print(ids)

    map(writeids,ids_path,ids)
    print("write is finished......")

    ################################ end ##################################

    endtime_all = datetime.datetime.now()
    print 'All processes are finished......'
    print 'Cost time: '+str((endtime_all - starttime_all).seconds)+' seconds'
    
    f=open("costtime.txt",'a')
    f.writelines('Split Cost time: '+str((endtime_all - starttime_all).seconds)+' seconds')
    f.close()

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
    Process("","")
    os.system('shutdown -s -f -t 10')