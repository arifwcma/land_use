import arcpy
from get_class_maps import parse_lyrx_classes
import numpy as np
import os
import matplotlib.pyplot as plt


def report(map, area, report_type):
    layer_name = f"{area} ({report_type})"
    style_path = f"lyrxs/{report_type}.lyrx"
    lyr = map.listLayers(layer_name)[0]
    raster = arcpy.Raster(lyr.dataSource)
    arr = arcpy.RasterToNumPyArray(raster)

    mapping, color_mapping, unique_classes = parse_lyrx_classes(style_path)

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
    file_name = area.replace(" ", "_")
    report_plots(area, file_name, report_type, class_counts, total, color_mapping, unique_classes)

def report_text(class_counts, total):
    for label, c in sorted(class_counts.items(), key=lambda x: -x[1]):
        print(f"{label}: {(c / total) * 100:.2f}%")

def report_plots(area, file_name, report_type, class_counts, total, color_mapping, unique_classes):
    if not class_counts:
        print(f"No data to plot for {area} ({report_type})")
        return

    merged = {cls: class_counts.get(cls, 0) for cls in unique_classes}
    items = sorted(merged.items(), key=lambda x: x[1], reverse=True)
    labels = [label for label, _ in items][::-1]
    percents = [((c / total) * 100)+10 if total > 0 else 0 for _, c in items][::-1]
    colors = [color_mapping.get(label, (0.5, 0.5, 0.5, 1.0)) for label in labels]

    fig, ax = plt.subplots()
    bars = ax.barh(range(len(labels)), percents, color=colors)

    for i, (bar, pct) in enumerate(zip(bars, percents)):
        ax.text(pct + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{pct:,.2f}%", va="center", ha="left", fontsize=9)
        ax.text(-1, bar.get_y() + bar.get_height() / 2,
                labels[i], va="center", ha="right", fontsize=9)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, max(percents) + 5 if percents else 1)
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.title(f"{area} ({report_type})", fontsize=11, weight="bold")
    plt.tight_layout()

    out_dir = fr"plots\{report_type}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{file_name}.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
