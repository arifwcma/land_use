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

