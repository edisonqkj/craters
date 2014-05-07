# -*- coding: cp936 -*-
from __future__ import print_function
import os
import sys
import arcpy
import datetime
import time
from test_clearfile import *
from OutletAnalysis import *
from funcs import *

## Unit Computation for each input data file
## Time: 3/3/14
## Author: Edison Qian

def ExtractRidge(ascii_path):
    #"F:/north-east/0/asc0.txt"
    if not os.path.exists(ascii_path):
        print(ascii_path+" is not found......")
        return
    print(ascii_path+" is executed......")
    isprint=False
    # full path of file
    if isprint:
        print("Dealing with %s" %ascii_path)
    base,filename=os.path.split(ascii_path)
    FID=base.split('/')[-1]
    #base+="/"
    name=filename.split('.')[0]
    fileformat=filename.split('.')[1]
    err_txt='/'.join(base.split('/')[:-1])+"/error"+FID#+".txt"
###########################################################
    # 0. Prepare Temporal & Crater Directory
    if isprint:
        print ('###################################')
    tmp_dir=base+'/t'+name+'/'
    crater_dir=base+'/c'+name+'/'
    # Temporal
    if os.path.exists(tmp_dir):
        if isprint:
            print ('Exist '+tmp_dir)
        CleanDir(tmp_dir,isprint)
        if isprint:
            print ('Clear '+tmp_dir)
    os.mkdir(tmp_dir)
    if isprint:
        print ('Create '+tmp_dir)
    # Crater
    if os.path.exists(crater_dir):
        if isprint:
            print ('Exist '+crater_dir)
        CleanDir(crater_dir,isprint)
        if isprint:
            print ('Clear '+crater_dir)
    os.mkdir(crater_dir)
    if isprint:
        print ('Create '+crater_dir)
    if isprint:
        print("Directories are ready......")

###########################################################

    arcpy.env.workspace = base #F:/north-east/0/

    # 1. Create DEM Raster
    dem=tmp_dir+'dem'
    rasterType = "INTEGER"
    Ascii2Raster(ascii_path,rasterType,dem,isprint)
    if isprint:
       print ('1 is finished......')

    arcpy.env.extent=dem

    # 2. Fill DEM
    fill=tmp_dir+'fill'
    if IsFailed(Fill(dem,fill,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt"+"_*.txt")
        return
    if isprint:
        print ('2 is finished......')

    # 3. Flow Direction
    fdir=tmp_dir+'fdir'
    ffdir=tmp_dir+'ffdir'
    # bug: overide err_txt
    map(lambda x:IsFailed(x,err_txt) and print("Error: check out in "+err_txt+"_*.txt"),\
        map(FlowDirection,[dem,fill],[fdir,ffdir],[isprint,isprint]))
    if isprint:
        print ('3 is finished......')

    # 4. Filled Area & Select Max Area
    filledarea=tmp_dir+'filledarea'
    plg=tmp_dir+'plg.shp'
    plg_area=tmp_dir+'plg_area.shp'
    plg_area_mshp=tmp_dir+'plg_area_max.shp'
    plg_area_mrst=tmp_dir+'plg_area_max'

    head_asc,asc=ReadAscii(ascii_path)
    cellsize=head_asc[4] #118.4505876499.542418
    
    if IsFailed(GetFilledArea(dem,fill,filledarea,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if IsFailed(Raster2Polygon(filledarea,plg,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if IsFailed(CalShpArea(plg,plg_area,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if IsFailed(GetMaxAreaFeature(plg_area,plg_area_mshp,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if IsFailed(Polygon2Raster(plg_area_mshp,cellsize,dem,plg_area_mrst,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if isprint:
        print ('4 is finished......')
    
    # 5. Initial Watershed
    iwatershed=tmp_dir+'iwatershed'
    if IsFailed(Watershed(fdir,plg_area_mrst,dem,iwatershed,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if isprint:
        print ('5 is finished......')

    # 6. Convert Filled Direction & Initial Watershed to Ascii
    ffdir_asc=tmp_dir+'ffdir.txt'
    iw_asc=tmp_dir+'iw.txt'
    if IsFailed(Raster2Ascii(ffdir,ffdir_asc,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if IsFailed(Raster2Ascii(iwatershed,iw_asc,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if isprint:
        print ('6 is finished......')

    # 7. Extract Outlets from Ascii
    outlet_asc=tmp_dir+'outlet.txt'
    if IsFailed(OutletAnalysis(iw_asc,ffdir_asc,outlet_asc,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if isprint:
        print ('7 is finished......')

    # 8. Create Outlet Raster
    outlet=tmp_dir+'outlet'
    rasterType = "INTEGER"
    if IsFailed(Ascii2Raster(outlet_asc,rasterType,outlet,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if isprint:
        print ('8 is finished......')

    # 9. Extract Crater Raster & Polygon
    crater=crater_dir+'c'+name
    crater_plg=crater_dir+'p'+name+'.shp'
    crater_txt=crater_dir+'p'+name+'.txt'
    if IsFailed(Watershed(ffdir,outlet,dem,crater,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if IsFailed(Raster2Polygon(crater,crater_plg,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return
    if IsFailed(Raster2Ascii(crater,crater_txt,isprint),err_txt):
        print("Error: check out in "+err_txt+"_*.txt")
        return

    if isprint:
        print ('9 is finished......')

    #print (name+'\tExtractRidge is finished......')
    #return 'r '+crater,'r '+crater_plg
    print(ascii_path+" is finished......")

###########################################################
