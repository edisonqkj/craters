# -*- coding: cp936 -*-
## Check extent not enough
## Expand && Reextract

## Time: 5/16/2014
## Author: Edison Qian

from __future__ import print_function
from checkfuncs import *

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

    ne,se,nw,sw=map(ExpandCheck,[north_east,south_east,\
                                 north_west,south_west])
    print("Checking is finished......")

    # Here, we eliminate craters on the edge
    # Further, with re-projection of dem, they should be considered.
    # edgeShpId=ReadEdgeShpId(edgeshp)

    # expand ratio for reextraction
    if ne is not None:
        print("North East:")
        files_extract=map(lambda x:[dem,center,north_east+x+'/'],ne)
        if len(files_extract)>0:
            ne_res=filter(lambda x:len(x)>0,map(ReExtractionByRatio,files_extract))
            print('Expansion Failed: '+len(ne_res))
        print("OK......")
    else:
        print(north_east+" is empty......")

    if se is not None:
        print("South East:")
        files_extract=map(lambda x:[dem,center,south_east+x+'/'],se)
        if len(files_extract)>0:
            se_res=filter(lambda x:len(x)>0,map(ReExtractionByRatio,files_extract))
            print('Expansion Failed: '+len(se_res))
        print("OK......")
    else:
        print(south_east+" is empty......")

    if nw is not None:
        print("North West:")
        files_extract=map(lambda x:[dem,center,north_west+x+'/'],nw)
        if len(files_extract)>0:
            nw_res=filter(lambda x:len(x)>0,map(ReExtractionByRatio,files_extract))
            print('Expansion Failed: '+len(nw_res))
        print("OK......")
    else:
        print(north_west+" is empty......")
        
    if sw is not None:
        print("South West:")
        files_extract=map(lambda x:[dem,center,north_east+x+'/'],sw)
        if len(files_extract)>0:
            sw_res=filter(lambda x:len(x)>0,map(ReExtractionByRatio,files_extract))
            print('Expansion Failed: '+len(sw_res))
        print("OK......")
    else:
        print(south_west+" is empty......")