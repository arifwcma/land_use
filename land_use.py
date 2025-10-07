import arcpy

print("Start")

aprx = arcpy.mp.ArcGISProject(r"C:\Users\m.rahman\arcgis\local_land_use\local_land_use.aprx")
m = aprx.listMaps()[0]
lyr = m.listLayers("West Wimmera (Ag)")[0]
raster_path = lyr.dataSource

arcpy.BuildRasterAttributeTable_management(raster_path, "Overwrite")

total = 0
with arcpy.da.SearchCursor(raster_path, ["COUNT"]) as cur:
    for row in cur:
        total += row[0]

with arcpy.da.SearchCursor(raster_path, ["VALUE", "COUNT", "LABEL"]) as cur:
    for value, count, label in cur:
        percent = (count / total) * 100 if total > 0 else 0
        print(f"{label}: {percent:.2f}%")

print("End")
