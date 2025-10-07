import arcpy
from report_land_use import report

print("Start")

aprx = arcpy.mp.ArcGISProject(r"C:\Users\m.rahman\arcgis\local_land_use\local_land_use.aprx")
map = aprx.listMaps()[0]
report(map, "West Wimmera (Ag)", r"C:\Users\m.rahman\arcgis\local_land_use\data\original\clum_50m_2023_v2\Land use, agricultural industries.lyrx")

print("End")
