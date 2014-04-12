
# -*- coding: cp936 -*-
import os
import sys
import datetime
from multiprocessing import Pool
from unitcomputation import *
from splitdem import *

## Master Control Function
## Time: 11/4/14
## Author: Edison Qian
##
## execute all files in directories:
## north-east,north west,
## south east,south west

def Execute(files):
	'''
	workpath=os.path.abspath('.')
	dirs='/'.join(workpath.split('\\'))
	files=map(lambda x:dirs+'/'+x,files)
	'''
	pool_costtime_start=datetime.datetime.now()

	#pool = Pool(len(files))
	map(ExtractRidge, files)
	#pool.close()
	#pool.join()

	pool_costtime_end=datetime.datetime.now()
	print ('[Pool Cost time: '+\
		str((pool_costtime_end - pool_costtime_start).seconds)+\
		' seconds]')
	f=open("costtime.txt",'a')
	f.writelines('Extract Cost time: '+\
		str((pool_costtime_end - pool_costtime_start).seconds)+' seconds')
	f.close()

if __name__ == '__main__':
	'''
	Process("","")
'''
	data_dir="F:/"
	f=open(data_dir+"north-east/ids.txt")
	ids_ne=map(lambda x:int(x),f.readlines()[0][1:-1].split(','))
	f.close()
	f=open(data_dir+"south-east/ids.txt")
	ids_se=map(lambda x:int(x),f.readlines()[0][1:-1].split(','))
	f.close()
	f=open(data_dir+"north-west/ids.txt")
	ids_nw=map(lambda x:int(x),f.readlines()[0][1:-1].split(','))
	f.close()
	f=open(data_dir+"south-west/ids.txt")
	ids_sw=map(lambda x:int(x),f.readlines()[0][1:-1].split(','))
	f.close()

	print(ids_ne)
	print(ids_se)
	print(ids_nw)
	print(ids_sw)

	files=[]
	for i in range(len(ids_ne)):
		files.append(data_dir+"north-east/"+str(ids_ne[i])+"/asc"+str(ids_ne[i])+".txt")
	for i in range(len(ids_se)):
		files.append(data_dir+"south-east/"+str(ids_se[i])+"/asc"+str(ids_se[i])+".txt")
	for i in range(len(ids_nw)):
		files.append(data_dir+"north-west/"+str(ids_nw[i])+"/asc"+str(ids_nw[i])+".txt")
	for i in range(len(ids_sw)):
		files.append(data_dir+"south-west/"+str(ids_sw[i])+"/asc"+str(ids_sw[i])+".txt")
		
	#files=["f:/north-east/0/asc0.txt"]
	Execute(files)