import json, xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import OrderedDict
import arcpy

def _rgba(vals):
    if not vals:
        return 128,128,128,255
    r,g,b = vals[:3]
    a = vals[3] if len(vals)>3 else 100
    if a <= 1:
        alpha = int(round(a*255))
    elif a <= 100:
        alpha = int(round(a/100.0*255))
    else:
        alpha = int(round(min(max(a,0),255)))
    return r,g,b,alpha

def _hex(rgb):
    r,g,b = rgb
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def _field(name_list, target):
    tl = target.lower()
    for n in name_list:
        if n.lower() == tl:
            return n
    raise ValueError(f"Field {target} not found")

def lyrx_label_to_rgba(lyrx_path):
    with open(lyrx_path, "r", encoding="utf-8") as f:
        j = json.load(f)
    ld = j["layerDefinitions"][0]
    cz = ld["colorizer"]
    dc_vals = cz.get("defaultColor",{}).get("values",[128,128,128,100])
    dc = _rgba(dc_vals)
    out = {}
    for g in cz["groups"]:
        for c in g["classes"]:
            vals = c.get("color",{}).get("values", dc_vals)
            rgba = _rgba(vals)
            label = c["label"]
            for v in c.get("values", []):
                for token in [x.strip() for x in v.split(";") if x.strip()]:
                    out[token] = rgba
                    out[label] = rgba
    return out, dc

def rat_value_to_label(raster_path):
    fields = [f.name for f in arcpy.ListFields(raster_path)]
    vf = _field(fields, "Value")
    lf = _field(fields, "SECV8")
    rows = []
    with arcpy.da.SearchCursor(raster_path, [vf, lf]) as cur:
        for v,l in cur:
            rows.append((int(v), str(l)))
    return rows

def group_duplicates(entries):
    grouped = OrderedDict()
    for _, label, color, alpha in entries:
        if label not in grouped:
            grouped[label] = (color, alpha)
    return [(v, label, *grouped[label]) for v, label, color, alpha in entries]

def build_qml(entries, out_qml):
    root = ET.Element("qgis", {"version":"3.34.12-Prizren","hasScaleBasedVisibilityFlag":"0","autoRefreshTime":"0","styleCategories":"LayerConfiguration|Symbology|MapTips|AttributeTable|Rendering|CustomProperties|Temporal|Elevation|Notes","maxScale":"0","autoRefreshMode":"Disabled","minScale":"1e+08"})
    pipe = ET.SubElement(root,"pipe")
    rr = ET.SubElement(pipe,"rasterrenderer", {"type":"paletted","alphaBand":"-1","opacity":"1","band":"1","nodataColor":""})
    ET.SubElement(rr,"rasterTransparency")
    mmo = ET.SubElement(rr,"minMaxOrigin")
    ET.SubElement(mmo,"limits").text = "None"
    ET.SubElement(mmo,"extent").text = "WholeRaster"
    ET.SubElement(mmo,"statAccuracy").text = "Estimated"
    ET.SubElement(mmo,"cumulativeCutLower").text = "0.02"
    ET.SubElement(mmo,"cumulativeCutUpper").text = "0.98"
    ET.SubElement(mmo,"stdDevFactor").text = "2"
    cp = ET.SubElement(rr,"colorPalette")
    for v,label,hexcolor,alpha in entries:
        ET.SubElement(cp,"paletteEntry", {"value":str(v),"alpha":str(alpha),"label":label,"color":hexcolor})
    cr = ET.SubElement(rr,"colorramp", {"name":"[source]","type":"randomcolors"})
    ET.SubElement(cr,"Option")
    ET.SubElement(pipe,"brightnesscontrast", {"brightness":"0","gamma":"1","contrast":"0"})
    ET.SubElement(pipe,"huesaturation", {"colorizeBlue":"128","grayscaleMode":"0","colorizeRed":"255","colorizeGreen":"128","invertColors":"0","saturation":"0","colorizeStrength":"100","colorizeOn":"0"})
    ET.SubElement(pipe,"rasterresampler", {"maxOversampling":"2"})
    ET.SubElement(pipe,"resamplingStage").text = "resamplingFilter"
    ET.SubElement(root,"blendMode").text = "0"
    xml = ET.tostring(root, encoding="utf-8")
    pretty = minidom.parseString(xml).toprettyxml(indent="  ")
    with open(out_qml,"w",encoding="utf-8") as f:
        f.write(pretty)

def lyrx_to_qml(lyrx_path, raster_path, out_qml):
    label2rgba, dc = lyrx_label_to_rgba(lyrx_path)
    rat = rat_value_to_label(raster_path)
    entries = []
    for v,label in rat:
        rgba = label2rgba.get(label, dc)
        r,g,b,a = rgba
        entries.append((v,label,_hex((r,g,b)),a))
    entries.sort(key=lambda x: x[0])
    entries = group_duplicates(entries)
    build_qml(entries, out_qml)

lyrx_to_qml(
    r"lyrxs/Details.lyrx",
    r"C:\Users\m.rahman\qgis\land_use_report\data\details_tifs\WestWimmera\West Wimmera Details.tif",
    r"qmls\ww.qml"
)
