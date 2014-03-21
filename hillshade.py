# -*- coding: cp936 -*-
import arcpy
from arcpy import env
from arcpy.sa import *
from multiprocessing import Pool
from test_clearfile import *
import datetime

def Ascii2Raster(ascii,rasterType,raster,isprint):
    arcpy.ASCIIToRaster_conversion(ascii, raster, rasterType)
    if isprint:
        print ('Ascii2Raster is finished....')

def Raster2Ascii(raster,ascii,isprint):
    arcpy.RasterToASCII_conversion(raster, ascii)
    if isprint:
        print ('Raster2Ascii is finished....')

def HillShade(paras):
	raster=paras[0]
	result=paras[1]
	azimuth=paras[2]
	altitude=paras[3]
	model=paras[4]
	zfactor=paras[5]
	arcpy.CheckOutExtension("Spatial")
	arcpy.gp.HillShade_sa(raster,result, azimuth, altitude, model, zfactor)
	print('HillShade is finished....')
	#return result

def Process(raster,altitude,azimuth):
	import os;
	base,filename=os.path.split(raster)
	name = filename.split('.')[0]
    #fileformat=filename.split('.')[1]
	tmp_dir = base+"\\tmp\\"
	#print(tmp_dir)
	isprint = True
	if os.path.exists(tmp_dir):
		CleanDir(tmp_dir,isprint)
	os.mkdir(tmp_dir)

	# 1. Ascii2Raster - DEM
	rasterType = "INTEGER"
	dem = tmp_dir+"dem"
	Ascii2Raster(raster,rasterType,dem,isprint)

	size = len(azimuth)
	result = map(lambda x:tmp_dir+name+"_hs_"+str(x)+"x"+str(altitude),azimuth)
	result_txt = map(lambda x:tmp_dir+name+"_hs_"+str(x)+"x"+str(altitude)+".txt",azimuth)
	#print(result)
	model = "SHADOWS"
	zfactor = 1
	# (dem,result,azimuth,altitude,model,zfactor)
	paras=map(lambda x:[dem,\
						tmp_dir+name+"_hs_"+str(x)+"x"+str(altitude),\
						x,\
						altitude,\
						model,\
						zfactor],\
						azimuth)
	print(paras)
	# 2. Hillshade
	# pool = Pool(size)
	# pool.
	map(HillShade,paras)
	# pool.close()
	# pool.join()
	print("calculate HillShade is finished....")

	# 3. Raster2Ascii - Txt
	map(Raster2Ascii,result,result_txt,[isprint]*size)
	print("calculate Raster2Ascii is finished....")

	print("Process is finished....")

if __name__=='__main__':
	path = "E:\\R\\Moon\\code4crater\\matlab\\finish\\dem.txt"
	altitude = 0
	num_of_position = 8
	azimuth = map(lambda x,y:x*y/num_of_position,\
				range(num_of_position),\
				[360]*num_of_position)
	print(azimuth)
	start_time=datetime.datetime.now()

	Process(path,altitude,azimuth)

	print ('[Cost time: '+\
		str((datetime.datetime.now() - start_time).seconds)+\
		' seconds]')

