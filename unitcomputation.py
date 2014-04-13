# -*- coding: cp936 -*-
import os
import sys
import arcpy
from test_clearfile import *
from OutletAnalysis import *

## Unit Computation for each input data file
## Time: 3/3/14
## Author: Edison Qian

def ExtractRidge(ascii_path):
    #"F:/north-east/0/asc0.txt"
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
    dem=base+"/dem"+FID #tmp_dir+'dem'
    #rasterType = "INTEGER"
    #Ascii2Raster(ascii_path,rasterType,dem,isprint)
    #if isprint:
    #    print ('1 is finished......')

    # 2. Fill DEM
    fill=tmp_dir+'fill'
    Fill(dem,fill,isprint)
    if isprint:
        print ('2 is finished......')

    # 3. Flow Direction
    fdir=tmp_dir+'fdir'
    ffdir=tmp_dir+'ffdir'
    map(FlowDirection,[dem,fill],[fdir,ffdir],[isprint,isprint])
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
    
    GetFilledArea(dem,fill,filledarea,isprint)
    Raster2Polygon(filledarea,plg,isprint)
    CalShpArea(plg,plg_area,isprint)
    GetMaxAreaFeature(plg_area,plg_area_mshp,isprint)
    Polygon2Raster(plg_area_mshp,cellsize,dem,plg_area_mrst,isprint)
    if isprint:
        print ('4 is finished......')
    
    # 5. Initial Watershed
    iwatershed=tmp_dir+'iwatershed'
    Watershed(fdir,plg_area_mrst,dem,iwatershed,isprint)
    if isprint:
        print ('5 is finished......')

    # 6. Convert Filled Direction & Initial Watershed to Ascii
    ffdir_asc=tmp_dir+'ffdir.txt'
    iw_asc=tmp_dir+'iw.txt'
    Raster2Ascii(ffdir,ffdir_asc,isprint)
    Raster2Ascii(iwatershed,iw_asc,isprint)
    if isprint:
        print ('6 is finished......')

    # 7. Extract Outlets from Ascii
    outlet_asc=tmp_dir+'outlet.txt'
    OutletAnalysis(iw_asc,ffdir_asc,outlet_asc,isprint)
    if isprint:
        print ('7 is finished......')

    # 8. Create Outlet Raster
    outlet=tmp_dir+'outlet'
    rasterType = "INTEGER"
    Ascii2Raster(outlet_asc,rasterType,outlet,isprint)
    if isprint:
        print ('8 is finished......')

    # 9. Extract Crater Raster & Polygon
    crater=crater_dir+'c'+name
    crater_plg=crater_dir+'p'+name+'.shp'
    Watershed(ffdir,outlet,dem,crater,isprint)
    Raster2Polygon(crater,crater_plg,isprint)

    if isprint:
        print ('9 is finished......')

    #print (name+'\tExtractRidge is finished......')
    #return 'r '+crater,'r '+crater_plg
    print(ascii_path+" is finished......")

###########################################################

def Ascii2Raster(ascii,rasterType,raster,isprint):
    try:
        arcpy.ASCIIToRaster_conversion(ascii, raster, rasterType)
        if isprint:
            print ('Ascii2Raster is finished....')
    except:
        print(arcpy.GetMessages())

def Raster2Ascii(raster,ascii,isprint):
    try:
        arcpy.RasterToASCII_conversion(raster, ascii)
        if isprint:
            print ('Raster2Ascii is finished....')
    except:
        print(arcpy.GetMessages())
    
def CalShpArea(inshp,outshp,isprint):
    #CalShpArea("E:/select/tr0_101x109/p1.shp","E:/select/tr0_101x109/p1a3.shp")
    try:
        arcpy.CalculateAreas_stats(inshp, outshp)
        if isprint:
            print ('CalShpArea is finished....')
    except:
        print(arcpy.GetMessages())

def GetMaxAreaFeature(inshp,outshp,isprint):
    #GetMaxAreaFeature('E:/select/tr0_101x109/p1a.shp','E:/select/tr0_101x109/ps.shp')
    try:
        records=arcpy.SearchCursor(inshp,"","","","")
        feature_area=[]
        ID=[]
        for record in records:
            if int(record.GRIDCODE)==1:
                feature_area.append(float(record.F_AREA))
                ID.append(int(record.ID))
        index=feature_area.index(max(feature_area))
        where_clause = '"ID" = '+str(ID[index])
        arcpy.Select_analysis(inshp, outshp, where_clause)
        if isprint:
            print ('GetMaxAreaFeature is finished....')
    except:
        print(arcpy.GetMessages())

def Fill(dem,fill,isprint):
    #Fill('E:/select/tr0_101x109/raster','E:/select/tr0_101x109/fill1')
    try:
        arcpy.CheckOutExtension("spatial")
        arcpy.gp.Fill_sa(dem, fill, "")
        if isprint:
            print ('Fill is finished....')
    except:
        print(arcpy.GetMessages())

def FlowDirection(dem,flowdir,isprint):
    #FlowDirection('E:/select/tr0_101x109/raster','E:/select/tr0_101x109/d1')
    try:
        arcpy.CheckOutExtension("spatial")
        arcpy.gp.FlowDirection_sa(dem, flowdir, "NORMAL", '')
        if isprint:
            print ('FlowDirection is finished....')
    except:
        print(arcpy.GetMessages())

def GetFilledArea(dem,fill,filledarea,isprint):
    #GetFilledArea('E:/select/tr0_101x109/raster','E:/select/tr0_101x109/fill','E:/select/tr0_101x109/a1')
    try:
        arcpy.CheckOutExtension("spatial")
        base,filename=os.path.split(fill)
        minus=base+'/minus'
        arcpy.gp.Minus_sa(dem, fill,minus)
        arcpy.gp.LessThan_sa(minus, 0,filledarea)
        if isprint:
            print ('GetFilledArea is finished....')
    except:
        print(arcpy.GetMessages())

def Raster2Polygon(raster,plg,isprint):
    #Raster2Polygon('E:/select/tr0_101x109/area','E:/select/tr0_101x109/plg.shp')
    try:
        arcpy.RasterToPolygon_conversion(raster, plg, "NO_SIMPLIFY", "VALUE")
        if isprint:
            print ('Raster2Polygon is finished....')
    except:
        print(arcpy.GetMessages())

def Polygon2Raster(plg,cellsize,extent,raster,isprint):
    #Polygon2Raster('E:/select/tr0_101x109/ps.shp',499.542418,'E:/select/tr0_101x109/raster','E:/select/tr0_101x109/ps')
    #GRIDCODE=1
    try:
        arcpy.env.extent=extent
        arcpy.env.snapRaster=extent
        arcpy.PolygonToRaster_conversion(plg, "GRIDCODE", raster, "CELL_CENTER", "NONE", cellsize)
        if isprint:
            print ('Polygon2Raster is finished....')
    except:
        print(arcpy.GetMessages())

def Watershed(flowdir,outlet,extent,watershed,isprint):
    #Watershed('E:/select/tr0_101x109/dir','E:/select/tr0_101x109/ps','E:/select/tr0_101x109/raster','E:/select/tr0_101x109/w')
    #outlet: raster or point shp
    try:
        arcpy.CheckOutExtension("Spatial")
        field="VALUE"
        arcpy.gp.Watershed_sa(flowdir,outlet,watershed,field)
        if isprint:
            print ('Watershed is finished....')
    except:
        print(arcpy.GetMessages())
