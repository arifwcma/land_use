import arcpy
from get_class_maps import parse_lyrx_classes
import numpy as np


def report(map, layer_name, style_path):
    lyr = map.listLayers(layer_name)[0]
    raster = arcpy.Raster(lyr.dataSource)
    arr = arcpy.RasterToNumPyArray(raster)

    mapping = parse_lyrx_classes(style_path)

    nodata = raster.noDataValue
    vals, counts = np.unique(arr, return_counts=True)

    class_counts = {}
    total = 0
    for v, c in zip(vals, counts):
        if v == nodata:
            continue
        if v in mapping:
            label = mapping[v]
            class_counts[label] = class_counts.get(label, 0) + c
            total += c

    for label, c in sorted(class_counts.items(), key=lambda x: -x[1]):
        print(f"{label}: {(c / total) * 100:.2f}%")