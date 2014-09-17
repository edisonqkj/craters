'''
Created on 2014-9-6

@author: Wang Ke
@description: 
    the folders named by number(#) contains datas of crater.
    first, define the pasc#.shp projection with the dem#'s.
    second, identify the pasc#.shp attribution with the env#.shp's.
    last, get the minimum bounding circle of the pasc#.shp.

@folder constuction:
    -#
    ....-casc#
    .   ....case#(raster)
    .   ....pasc#.shp
    .   ....pasc#.txt
    ....+tasc#
    ....dem#(raster)
    ....env#.shp

@function:
    
'''
import arcpy
import os
import re
from test_clearfile import *

def define_projection(target_shp_path, source_path):
    dem = arcpy.Raster(source_path)
    sr = arcpy.Describe(dem).spatialReference
    arcpy.DefineProjection_management(target_shp_path, sr)
    return 0
    
def identify_attribution(target_shp_path, identity_path):
    # 'E:/tmp/7451/casc7451/pasc7451.shp'
    # 'E:/tmp/7451/env7451.shp'
    output_dir_path = os.path.dirname(target_shp_path)
    basename = os.path.basename(target_shp_path)
    filename = os.path.splitext(basename)[0]
    id = int(filename[4:])
    output_name = "ipasc%d.shp" % id
    output_path = output_dir_path+'/'+output_name
    arcpy.Identity_analysis(target_shp_path,identity_path, output_path)

def get_minimun_bounding_circle(input_shp_path):
    output_dir_path = os.path.dirname(input_shp_path)
    basename = os.path.basename(input_shp_path)
    filename = os.path.splitext(basename)[0]
    id = int(filename[4:])
    output_name = "bcircle%d.shp" % id
    output_path = os.path.join(output_dir_path, output_name)
    arcpy.MinimumBoundingGeometry_management(input_shp_path, output_path, "CIRCLE")

def ProjectIdentifyProcess(folder_path):
    # 'E:/tmp/7451/'
    base,name=os.path.split(folder_path)# 'E:/tmp/7451'
    id = os.path.basename(base)# '7451'
    # PIP_dir=folder_path+'/PIP/'
    # if os.psth.exists(PIP_dir):
    #     CleanDir(PIP_dir,False)
    # os.mkdir(PIP_dir)
    if os.path.exists(folder_path+"casc"+id+"/ipasc"+id+".shp"):
        print(id+': identify is already done......')
        return
    pasc_shp_path = folder_path+"casc"+id+"/pasc"+id+".shp"
    dem_path = 'F:/Data/moon/Moon_LRO_LOLA_global_LDEM_118m_Feb2013.cub'#os.path.join(folder_path,"dem%d" % id)
    env_shp_path = folder_path+"env"+id+".shp"
    
    define_projection(pasc_shp_path, dem_path)
    identify_attribution(pasc_shp_path, env_shp_path)
    # get_minimun_bounding_circle(pasc_shp_path)
    
    print "END"
if __name__ == '__main__':
    folder_path = 'E:/tmp/7451/'#raw_input("enter the folder path:")
    ProjectIdentifyProcess(folder_path)
    

