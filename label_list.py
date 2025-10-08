import json

with open("Details.json", "r", encoding="utf-8") as f:
    data = json.load(f)

colorizer = data["layerDefinitions"][0]["colorizer"]
labels = []

for group in colorizer.get("groups", []):
    for cls in group.get("classes", []):
        labels.append(cls.get("label"))

for label in labels:
    print(label)
