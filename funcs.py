# -*- coding: cp936 -*-
import os
import sys
import datetime
import arcpy

## Functions for Unit Computation
## Time: 14/4/14
## Author: Edison Qian

def IsFailed(info,err_txt):
    if not info==None:
        err_func=info.split(':')[0]
        err_info=info.split(':')[1]
        f=open(err_txt+"_"+err_func+".txt",'a')
        '''
        f.writelines(unicode(str(datetime.datetime.now())))
        #print(info)
        f.writelines(info)'''
        f.close()
        
        return True
    return False

def Ascii2Raster(ascii,rasterType,raster,isprint):
    try:
        arcpy.ASCIIToRaster_conversion(ascii, raster, rasterType)
        if isprint:
            print ('Ascii2Raster is finished....')
        return None
    except:
        #print(arcpy.GetMessages())
        return unicode("Ascii2Raster:\n"+arcpy.GetMessages()+"\n\n")

def Raster2Ascii(raster,ascii,isprint):
    try:
        arcpy.RasterToASCII_conversion(raster, ascii)
        if isprint:
            print ('Raster2Ascii is finished....')
        return None
    except:
        #print(arcpy.GetMessages())
        return unicode("Raster2Ascii:\n"+arcpy.GetMessages()+"\n\n")
    
def CalShpArea(inshp,outshp,isprint):
    #CalShpArea("E:/select/tr0_101x109/p1.shp","E:/select/tr0_101x109/p1a3.shp")
    try:
        arcpy.CalculateAreas_stats(inshp, outshp)
        if isprint:
            print ('CalShpArea is finished....')
        return None
    except:
        #print(arcpy.GetMessages())
        return unicode("CalShpArea:\n"+arcpy.GetMessages()+"\n\n")

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
        if len(feature_area)>0:
            index=feature_area.index(max(feature_area))
            where_clause = '"ID" = '+str(ID[index])
            arcpy.Select_analysis(inshp, outshp, where_clause)
            if isprint:
                print ('GetMaxAreaFeature is finished....')
            return None
        else:
            if isprint:
                print("GetNoArea:\nNo Filled Area is found......")
            return unicode("GetNoArea:\n"+"No Filled Area is found......\n\n")
    except:
        #print(arcpy.GetMessages())
        return unicode("GetMaxAreaFeature:\n"+arcpy.GetMessages()+"\n\n")

def Fill(dem,fill,isprint):
    #Fill('E:/select/tr0_101x109/raster','E:/select/tr0_101x109/fill1')
    try:
        arcpy.CheckOutExtension("spatial")
        arcpy.gp.Fill_sa(dem, fill, "")
        if isprint:
            print ('Fill is finished....')
        return None
    except:
        #print(arcpy.GetMessages())
        return unicode("Fill:\n"+arcpy.GetMessages()+"\n\n")

def FlowDirection(dem,flowdir,isprint):
    #FlowDirection('E:/select/tr0_101x109/raster','E:/select/tr0_101x109/d1')
    try:
        arcpy.CheckOutExtension("spatial")
        arcpy.gp.FlowDirection_sa(dem, flowdir, "NORMAL", '')
        if isprint:
            print ('FlowDirection is finished....')
        return None
    except:
        #print(arcpy.GetMessages())
        return unicode("FlowDirection:\n"+arcpy.GetMessages()+"\n\n")

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
        return None
    except:
        #print(arcpy.GetMessages())
        return unicode("GetFilledArea:\n"+arcpy.GetMessages()+"\n\n")

def Raster2Polygon(raster,plg,isprint):
    #Raster2Polygon('E:/select/tr0_101x109/area','E:/select/tr0_101x109/plg.shp')
    try:
        arcpy.RasterToPolygon_conversion(raster, plg, "NO_SIMPLIFY", "VALUE")
        if isprint:
            print ('Raster2Polygon is finished....')
        return None
    except:
        #print(arcpy.GetMessages())
        return unicode("Raster2Polygon:\n"+arcpy.GetMessages()+"\n\n")

def Polygon2Raster(plg,cellsize,extent,raster,isprint):
    #Polygon2Raster('E:/select/tr0_101x109/ps.shp',499.542418,'E:/select/tr0_101x109/raster','E:/select/tr0_101x109/ps')
    #GRIDCODE=1
    try:
        arcpy.env.extent=extent
        arcpy.env.snapRaster=extent
        arcpy.PolygonToRaster_conversion(plg, "GRIDCODE", raster, "CELL_CENTER", "NONE", cellsize)
        if isprint:
            print ('Polygon2Raster is finished....')
        return None
    except:
        #print(arcpy.GetMessages())
        return unicode("Polygon2Raster:\n"+arcpy.GetMessages()+"\n\n")

def Watershed(flowdir,outlet,extent,watershed,isprint):
    #Watershed('E:/select/tr0_101x109/dir','E:/select/tr0_101x109/ps','E:/select/tr0_101x109/raster','E:/select/tr0_101x109/w')
    #outlet: raster or point shp
    try:
        arcpy.CheckOutExtension("Spatial")
        field="VALUE"
        arcpy.gp.Watershed_sa(flowdir,outlet,watershed,field)
        if isprint:
            print ('Watershed is finished....')
        return None
    except:
        #print(arcpy.GetMessages())
        return unicode("Watershed:\n"+arcpy.GetMessages()+"\n\n")