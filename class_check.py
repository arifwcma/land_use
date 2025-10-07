import json

def parse_lyrx_classes(lyrx_path):
    with open(lyrx_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    mapping = {}
    colorizer = data["layerDefinitions"][0]["colorizer"]
    for g in colorizer["groups"]:
        for c in g["classes"]:
            label = c["label"]
            for v in c["values"]:
                try:
                    mapping[int(v)] = label
                except:
                    pass
    return mapping

lyrx_path = r"C:\Users\m.rahman\arcgis\local_land_use\data\original\clum_50m_2023_v2\Land use, agricultural industries.lyrx"
mapping = parse_lyrx_classes(lyrx_path)
for k, v in sorted(mapping.items()):
    print(f"{k:>5} → {v}")

