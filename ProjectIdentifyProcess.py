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
    
def identify_attribution(target_shp_path, identity_path,output_path):
    # 'E:/tmp/7451/casc7451/pasc7451.shp'
    # 'E:/tmp/7451/env7451.shp'
    # output_dir_path = os.path.dirname(target_shp_path)
    # basename = os.path.basename(target_shp_path)
    # filename = os.path.splitext(basename)[0]
    # id = int(filename[4:])
    # output_name = "ipasc%d.shp" % id
    # output_path = output_dir_path+'/'+output_name
    arcpy.Identity_analysis(target_shp_path,identity_path, output_path)

def CheckField4Delete(shp_path):
    # Check all fields
    # containing 'FID_' like 'FID_pasc7451' & 'FID_env7451'
    fields=arcpy.ListFields(shp_path)
    aliasName=map(lambda an:''+an.aliasName,fields)
    field4delete=filter(lambda n:'FID_' in n,aliasName)
    # print(field4delete)
    return field4delete

def DeleteField(shp_path):
    # 'E:/tmp/7451/casc7451/ipasc7451.shp'
    # ['FID_pasc7451', 'FID_env7451']
    # sts, length of field name is shortened
    fields=CheckField4Delete(shp_path)
    if len(fields)>0:
        arcpy.DeleteField_management(shp_path, fields)
    else:
        print('No fields to delete......')

def CalcShpField(shp_path,field,value):
    # calculate field
    if field=='Name':
        value="str(\'"+value+"\')"
    arcpy.CalculateField_management(shp_path, field, value, "PYTHON")
    # print(value)

def SetField(shp_path):
    # set the field value of fragments
    try:
        # get field names
        fields=arcpy.ListFields(shp_path)
        aliasName=map(lambda an:''+an.aliasName,fields)
        aliasName.remove('FID')
        aliasName.remove('Shape')
        aliasName.remove('ID')
        aliasName.remove('GRIDCODE')
        # print(len(aliasName))
        # one record -> return
        feature_count=int(arcpy.GetCount_management(shp_path).getOutput(0))
        # print(feature_count)
        if feature_count==1:
            return aliasName
        # get values
        records=arcpy.SearchCursor(shp_path,"","","","")
        for record in records:
            if float(record.Radius_deg)>0:
                field_value=[eval('record.'+fn) for fn in aliasName]
                break
        # print(field_value)
        # calculate field
        map(lambda f,v:CalcShpField(shp_path,f,v),\
                                aliasName,field_value)
        return aliasName# dissolveFields
    except:
        print(arcpy.GetMessages())
        return []

def DissolveShp(shp_path,out_path,dissolveFields):
    # projection difference causes fragments in ipasc
    # dissolve by field ID
    # dissolveFields=['ID']
    arcpy.Dissolve_management(shp_path,out_path,dissolveFields,\
        "","SINGLE_PART", "DISSOLVE_LINES")
    pass

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
    ipasc_path=folder_path+"casc"+id+"/ipasc"+id+".shp"
    if not os.path.exists(ipasc_path):
        # print(id+': identify is already done......')
        # return
        pasc_shp_path = ipasc_path
        dem_path = 'F:/Data/moon/Moon_LRO_LOLA_global_LDEM_118m_Feb2013.cub'#os.path.join(folder_path,"dem%d" % id)
        env_shp_path = folder_path+"env"+id+".shp"
    
        define_projection(pasc_shp_path, dem_path)
        identify_attribution(pasc_shp_path, env_shp_path,ipasc_path)
    DeleteField(ipasc_path)
    idpasc_path=folder_path+"casc"+id+"/idpasc"+id+".shp"
    if not os.path.exists(idpasc_path):
        # dissolve fragments
        dissolveFields=SetField(ipasc_path)
        # if no error from SetField
        if len(dissolveFields)>0:
            DissolveShp(ipasc_path,idpasc_path,dissolveFields)
    # get_minimun_bounding_circle(pasc_shp_path)

if __name__ == '__main__':
    folder_path = 'E:/tmp/7451/'#raw_input("enter the folder path:")
    ProjectIdentifyProcess(folder_path)
    # CalcShpField('F:/north-west/11/casc11/idpasc11.shp','ID',2)
    # SetField('F:/south-east/4/casc4/ipasc4.shp')
    

