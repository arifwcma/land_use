import json

def _find_cim_rgbcolor(obj):
    if isinstance(obj, dict):
        if obj.get("type") == "CIMRGBColor" and isinstance(obj.get("values"), list):
            return obj["values"]
        for v in obj.values():
            out = _find_cim_rgbcolor(v)
            if out is not None:
                return out
    elif isinstance(obj, list):
        for it in obj:
            out = _find_cim_rgbcolor(it)
            if out is not None:
                return out
    return None

def _to_rgba(vals):
    if not vals:
        return (0.5, 0.5, 0.5, 1.0)
    r, g, b = vals[:3]
    if (r, g, b) == (255, 255, 255):
        r, g, b = (220, 220, 220)
    a = vals[3] if len(vals) > 3 else 100
    if a <= 1:
        alpha = a
    elif a <= 100:
        alpha = a / 100.0
    else:
        alpha = a / 255.0
    return (r / 255.0, g / 255.0, b / 255.0, min(max(alpha, 0.0), 1.0))

def parse_lyrx_classes(lyrx_path):
    with open(lyrx_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    class_map = {}
    color_map = {}
    unique_classes = []

    colorizer = data["layerDefinitions"][0]["colorizer"]
    for g in colorizer.get("groups", []):
        for c in g.get("classes", []):
            label = c.get("label")
            if label and label not in unique_classes:
                unique_classes.append(label)

            vals = c.get("defaultColor", {}).get("values")
            if vals is None:
                vals = (_find_cim_rgbcolor(c.get("symbol"))
                        or _find_cim_rgbcolor(c.get("patch"))
                        or _find_cim_rgbcolor(c))

            rgba = _to_rgba(vals)

            for v in c.get("values", []):
                try:
                    class_map[int(v)] = label
                except:
                    pass

            if label is not None:
                color_map[label] = rgba

    return class_map, color_map, unique_classes



if __name__ == "__main__":
    class_map, color_map, unique_classes = parse_lyrx_classes("lyrxs/Simplified.lyrx")

    for k, v in sorted(color_map.items()):
        print(k, v)
