import arcpy
from lu_type import report_by_type


print("Start")

aprx = arcpy.mp.ArcGISProject(r"C:\Users\m.rahman\arcgis\local_land_use\local_land_use.aprx")
map = aprx.listMaps()[0]

report_by_type(map,"Ag")
report_by_type(map,"Simplified")

print("End")
