import arcpy
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

if __name__=='__main__':
    Fill("J:/6992/dem6992","J:/fill6992",True)