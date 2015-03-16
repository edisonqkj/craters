'''
# Convert crater raster to polygon with SIMPLIFY method & Merge
# Crater catalog:
# 	- raster: .../select/dem[d]-[d]/cr[d]_[W]x[H]/cr[d]_[W]x[H]
# 	- polygon: .../select/dem[d]-[d]/cr[d]_[W]x[H]/pr[d]_[W]x[H]
# Process:
# 	- get file paths of all crater rasters
# 	- convert raster to polygon
# 	- merge them into one shp
'''
import os
import sys

def CheckRaster(dir,regex):
	if not os.path.exists(dir):
		print(dir+" is not found......")
		return ''
	print('Start Checking: '+dir)
	content=os.listdir(dir)
	# directory is empty
	if len(content)==0:
		return ''

	# print(content)
	regions=FindIt(content,regex)
	print('Get: '+','.join(regions))

	# crater level
	shps=FindIt(content,r'(pr\d+_\d+x\d+[.]shp)')
	if len(shps)>0:
		return dir+regions[0]

	subregex=r'(cr\d+_\d+x\d+)'
	rasters=map(lambda subdir:\
					CheckRaster(dir+subdir+'/',subregex),\
					regions)
	return rasters

def FindIt(content,regex):
	list=','.join(content)
	# print(list)
	import re
	res=re.findall(regex,list)
	return res

def Raster2Polygon(raster,plg,isprint):
	import arcpy
	#Raster2Polygon('E:/select/tr0_101x109/area','E:/select/tr0_101x109/plg.shp')
	# method: SIMPLIFY
	try:
		arcpy.RasterToPolygon_conversion(raster, plg, "SIMPLIFY", "VALUE")
		if isprint:
			print (plg+' is converted....')
		return None
	except:
		#print(arcpy.GetMessages())
		return unicode("Raster2Polygon:\n"+arcpy.GetMessages()+"\n\n")

def MergeShp(sources,target):
	import arcpy
	try:
		arcpy.Merge_management(sources, target)
		print(target+" is Merged......")
	except:
		# print("MergeShp:\n"+arcpy.GetMessages()+"\n\n")
		return unicode("MergeShp:\n"+arcpy.GetMessages()+"\n\n")
##############################################################
if __name__=='__main__':
	dir='E:/R/Moon/code4crater/matlab/code/select/'

	# 1. get rasters' file path
	print('****** Start Checking ******')
	regex=r'(\w{3}\d+-\d+)'
	rasters=CheckRaster(dir,regex)
	print('Crater Number: '+str(sum(map(len,rasters))))
	print('****** Finish Converting ******')
##############################################################
	# 2. convert rasters to polygons
	# [['.../cr0_118x124', '.../cr0_203x168',],[dir2],...]
	# save path: 
	#    '.../cr0_118x124' --> '.../select/pcr0_118x124.shp'
	print('****** Start Converting ******')
	savedir=dir+'tmp/'
	if not os.path.exists(savedir):
		os.mkdir(savedir)
	else:
		print(savedir+' is existing.')
		exit(0)

	plgs=map(lambda subrst:\
			map(lambda r:\
				savedir+'p'+r.split('/')[-1]+'.shp',\
				subrst),\
			rasters)
	# print(plgs)
	# start converting
	polygons=map(lambda subrst,subplg:\
				map(lambda r,p:\
					Raster2Polygon(r,p,True),\
					subrst,subplg),\
				rasters,plgs)
	print('****** Finish Converting ******')
##############################################################
	# 3. merge
	print('****** Start Merging ******')
	shps=filter(lambda f:\
				f.split('.')[-1] == 'shp',\
				os.listdir(savedir))
	# print(shps)
	sources=map(lambda shp:savedir+shp,shps)
	# print(sources)
	OneShp=savedir+'craters.shp'
	MergeShp(sources,OneShp)
	print('****** Finish Merging ******')

