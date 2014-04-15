
# -*- coding: cp936 -*-
import os
import sys
import datetime
from multiprocessing import Pool
from unitcomputation import *
#from splitdem import *

## Master Control Function
## Time: 11/4/14
## Author: Edison Qian
##
## execute all files in directories:
## north-east,north west,
## south east,south west

def parallel(paras):
	pool = Pool(len(paras))
	pool.map(ExtractRidge,paras)
	pool.close()
	pool.join()

def Execute(files,process_num):
##############################################################
	pool_costtime_start=datetime.datetime.now()

	if process_num==1:
		# serial
		map(ExtractRidge,files)
	elif process_num>1:
		# parallel
		#print("slice_paras:")
		slice_paras=map(lambda x:files[x:x+process_num],\
			range(0,len(files),process_num))
		#print(slice_paras[:3])
		map(parallel,slice_paras)
	else:
		print("Process number must be positive......")

	pool_costtime_end=datetime.datetime.now()
##############################################################
	#"F:/north-east/0/asc0.txt"
	base,filename=os.path.split(files[0])
	rec_time=base.split('/')[-3]+"/extract_time.txt"
	print ('[Pool Cost time: '+\
		str((pool_costtime_end - pool_costtime_start).seconds)+\
		' seconds]')
	'''
	f=open(rec_time,'a')
	f.writelines(unicode('Extract Cost time: '+\
		str((pool_costtime_end - pool_costtime_start).seconds)+' seconds\n'))
	f.close()
	'''

if __name__ == '__main__':
	'''
	# split dem
	Process("","")
	'''
	ids_ne=[]
	ids_se=[]
	ids_nw=[]
	ids_sw=[]
	data_dir="F:/"
	if os.path.exists(data_dir+"north-east/ids.txt"):
		f=open(data_dir+"north-east/ids.txt")
		ids_ne=map(lambda x:int(x),f.readlines()[0][1:-1].split(','))
		f.close()
	else:
		print(data_dir+"north-east/ids.txt is not found......")

	if os.path.exists(data_dir+"south-east/ids.txt"):
		f=open(data_dir+"south-east/ids.txt")
		ids_se=map(lambda x:int(x),f.readlines()[0][1:-1].split(','))
		f.close()
	else:
		print(data_dir+"south-east/ids.txt is not found......")

	if os.path.exists(data_dir+"north-west/ids.txt"):
		f=open(data_dir+"north-west/ids.txt")
		ids_nw=map(lambda x:int(x),f.readlines()[0][1:-1].split(','))
		f.close()
	else:
		print(data_dir+"north-west/ids.txt is not found......")

	if os.path.exists(data_dir+"south-west/ids.txt"):
		f=open(data_dir+"south-west/ids.txt")
		ids_sw=map(lambda x:int(x),f.readlines()[0][1:-1].split(','))
		f.close()
	else:
		print(data_dir+"south-west/ids.txt is not found......")

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
	Execute(files,1)
	#os.system('shutdown -s -f -t 10')