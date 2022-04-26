import arcpy, numpy
from arcpy.sa import * 

arcpy.CheckOutExtension("Spatial")
afolderpath = r"C:\Users\KHALID\Desktop\Geog408\Lab_02_406\Lab_02"
aGDB= "Orange_County.gdb"
nGDB= "Orange_County_PCS.gdb"


arcpy.CreateFileGDB_management(r"C:\Users\KHALID\Desktop\Geog408\Lab_02_406\Lab_02", "Orange_County_PCS.gdb")

arcpy.env.workspace = afolderpath + "\\" + aGDB
aFC=arcpy.ListFeatureClasses()
aRS=arcpy.ListRasters()

for x in aRS:
    print x
    outfile= afolderpath + "\\" + nGDB + "\\" + x
    arcpy.ProjectRaster_management(x, outfile, 26946, "", 30)


for x in aFC:
    outfile= afolderpath + "\\" + nGDB + "\\" + x
    arcpy.Project_management(x, outfile, 26946)


arcpy.env.workspace = afolderpath + "\\" + nGDB
outSlope =Slope("dem","PERCENT_RISE")
outSlope.save(r"C:\Users\KHALID\Desktop\Geog408\Lab_02_406\Lab_02\Orange_County_PCS.gdb\SLOPE")
outCostDist = CostDistance("Start_Pont", "SLOPE","", "backlink")
outCostDist.save(r"C:\Users\KHALID\Desktop\Geog408\Lab_02_406\Lab_02\Orange_County_PCS.gdb\CD")
outCostPath = CostPath("Destination_Pont","CD","backlink")
outCostPath.save(r"C:\Users\KHALID\Desktop\Geog408\Lab_02_406\Lab_02\Orange_County_PCS.gdb\CP")
arcpy.RasterToPolyline_conversion("CP", "PL")
arcpy.Dissolve_management("PL","LCP")
ZonalStatisticsAsTable("CP","Value", "SLOPE", "AVS", "", "MEAN")

aFile= open(r"C:\Users\KHALID\Desktop\Geog408\Lab_02_406\Lab_02\msg.txt", "w")
with arcpy.da.SearchCursor('LCP', "*") as cursor:
    for aRow in cursor:
        print "The length of the path is {} Meters".format(aRow[2])
        aFile.write("The length of the path is {} Meters \n".format(aRow[2]))

with arcpy.da.SearchCursor('AVS', "*",'Value =3') as cursor:
    for aRow in cursor:
        print "The average slop along this path is {}".format(aRow[4])
        aFile.write("The average slop along this path is {}".format(aRow[4]))

aFile.close()


print "done"
