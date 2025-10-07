import arcpy

aprx = arcpy.mp.ArcGISProject(r"C:\Users\m.rahman\arcgis\local_land_use\local_land_use.aprx")
for m in aprx.listMaps():
    print(f"Map: {m.name}")
    for lyr in m.listLayers():
        print(f"  Layer: {lyr.name}")
