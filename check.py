# -*- coding: cp936 -*-
## Check unsplitted dem & execute
## Check dem without extraction & execute
## Check extent not enough

## Time: 16/4/14
## Author: Edison Qian

from __future__ import print_function
from splitdem import *
from execute import *
from OutletAnalysis import *
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

    ne,se,nw,sw=map(Check,[north_east,south_east,north_west,south_west])
    print("Checking is finished......")
    # north east
    # print(type(ne[0]))
    # print(type(ne[1]))
    # print(ne[1].extend(ne[0]))
    # print(ne[2])

    # Here, we eliminate craters on the edge
    # Further, with re-projection of dem, they should be considered.
    edgeShpId=ReadEdgeShpId(edgeshp)

    ratio=1.3
    if ne is not None:
        # print(ne)
        ne=map(lambda x:list(set(x)-set(edgeShpId)),ne)
        print("North East:")
        # split
        if ne[0] is not None:
            print("split number: "+str(len(ne[0])))
            files_split=map(lambda x:[dem,center,north_east+str(x)+"/",ratio],\
                            ne[0])
            len(files_split)>0 and map(split,files_split)
        if ne[1] is not None:
            # extract
            ne[1].extend(ne[0])
            print("extract number: "+str(len(ne[1])))
            files_extract=map(lambda x:north_east+str(x)+"/asc"+str(x)+".txt",\
                              ne[1])
            files_extract=filter(lambda x:not IsOutofExtent(x),files_extract)
            len(files_extract)>0 and Execute(files_extract)
        print("OK......")
    else:
        print(north_east+" is empty......")
    # south east
    if se is not None:
        # print(se)
        se=map(lambda x:list(set(x)-set(edgeShpId)),se)
        print("South East:")
        if se[0] is not None:
            # split
            print("split number: "+str(len(se[0])))
            files_split=map(lambda x:[dem,center,south_east+str(x)+"/",ratio],\
                            se[0])
            len(files_split)>0 and map(split,files_split)
        if se[1] is not None:
            # extract
            se[1].extend(se[0])
            print("extract number: "+str(len(se[1])))
            files_extract=map(lambda x:south_east+str(x)+"/asc"+str(x)+".txt",\
                              se[1])
            files_extract=filter(lambda x:not IsOutofExtent(x),files_extract)
            len(files_extract)>0 and Execute(files_extract)
        print("OK......")
    else:
        print(south_east+" is empty......")
    # north west
    if nw is not None:
        # print(nw)
        nw=map(lambda x:list(set(x)-set(edgeShpId)),nw)
        print("North West:")
        if nw[0] is not None:
            # split
            print("split number: "+str(len(nw[0])))
            files_split=map(lambda x:[dem,center,north_west+str(x)+"/",ratio],\
                            nw[0])
            len(files_split)>0 and map(split,files_split)
        if nw[1] is not None:
            # extract
            nw[1].extend(nw[0])
            print("extract number: "+str(len(nw[1])))
            files_extract=map(lambda x:north_west+str(x)+"/asc"+str(x)+".txt",\
                              nw[1])
            files_extract=filter(lambda x:not IsOutofExtent(x),files_extract)
            len(files_extract)>0 and Execute(files_extract)
        print("OK......")
    else:
        print(north_west+" is empty......")
    # south west
    if sw is not None:
        # print(sw)
        sw=map(lambda x:list(set(x)-set(edgeShpId)),sw)
        print("South West:")
        if sw[0] is not None:
            # split
            print("split number: "+str(len(sw[0])))
            files_split=map(lambda x:[dem,center,south_west+str(x)+"/",ratio],\
                            sw[0])
            len(files_split)>0 and map(split,files_split)
        if sw[1] is not None:
            # extract
            sw[1].extend(sw[0])
            print("extract number: "+str(len(sw[1])))
            files_extract=map(lambda x:south_west+str(x)+"/asc"+str(x)+".txt",\
                              sw[1])
            files_extract=filter(lambda x:not IsOutofExtent(x),files_extract)
            len(files_extract)>0 and Execute(files_extract)
        print("OK......")
    else:
        print(south_west+" is empty......")