# -*- coding: cp936 -*-
import os
import sys
import datetime
from multiprocessing import Pool
#from multiprocessing.dummy import Pool as ThreadPool
from unit4map import *

## Master Control Function
## Time: 3/3/14
## Author: Edison Qian

#python E:/研究/Moon/code4crater/matlab/map.py

def Execute(files):
    workpath=os.path.abspath('.')
    dirs='/'.join(workpath.split('\\'))
    files=map(lambda x:dirs+'/'+x,files)
    
    #print files
    #print (workpath)
    '''   
    files=['E:/select/r0_51x47.txt',
           'E:/select/r0_79x77.txt',
           'E:/select/r0_89x65.txt',
           'e:/select/r0_101x109.txt',
           'e:/select/r0_104x88.txt',
           'e:/select/r0_127x80.txt',
           'e:/select/r0_139x136.txt',
           'e:/select/r0_204x209.txt']
    
    files=['e:/select/r0_101x109.txt',
           'e:/select/r0_104x88.txt',
           'e:/select/r0_127x80.txt',
           'e:/select/r0_139x136.txt',
           'e:/select/r0_204x209.txt']
    '''
    #isprint=[False]*len(files)
    #print (isprint)
    
    #if len(files)>1:
    #print ('')
    #print ('###################################')
    pool_costtime_start= datetime.datetime.now()

    # pool = Pool(len(files))
    # pool.map(ExtractRidge, files)
    # pool.close()
    # pool.join()

    map(ExtractRidge, files)
    
    print ('[Pool Cost time: '+\
           str((datetime.datetime.now() - pool_costtime_start).seconds)+\
          ' seconds]')
    # crater & plg path
    # format: [data crater_path crater_plg_path]
    data=map(lambda x: 'data '+\
                os.path.split(x)[0]+'/c'+\
                os.path.split(x)[1].split('.')[0]+'/c'+\
                os.path.split(x)[1].split('.')[0]+' '+\
                os.path.split(x)[0]+'/c'+\
                os.path.split(x)[1].split('.')[0]+'/p'+\
                os.path.split(x)[1].split('.')[0]+'.shp',
                files)
    print (data)
    '''
    print ('')
    print ('###################################')
    single_costtime_start= datetime.datetime.now()
    map(ExtractRidge, files)
    print 'Single Cost time: '+\
          str((datetime.datetime.now() - single_costtime_start).seconds)+\
          ' seconds'
    '''
if __name__ == '__main__':
    #files='select/r0_218x221.txt select/r0_183x194.txt select/r0_109x101.txt'.split(' ')
    files=sys.argv[1:][0].split(' ')
    # print(files)
    # files='E:/R/Moon/code4crater/matlab/finish/select/r0_101x101.txt'
    Execute(files)
