import arcpy
from get_class_maps import parse_lyrx_classes
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm


def report(map, area, report_type):
    layer_name = f"{area} ({report_type})"
    style_path = f"lyrxs/{report_type}.lyrx"
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
    file_name = area.replace(" ", "_")
    report_plots(area, file_name, report_type, class_counts, total)

def report_text(class_counts, total):
    for label, c in sorted(class_counts.items(), key=lambda x: -x[1]):
        print(f"{label}: {(c / total) * 100:.2f}%")

def report_plots(area, file_name, report_type, class_counts, total):
    items = sorted(
        class_counts.items(),
        key=lambda x: (x[0].strip().lower().startswith("other"), x[0].strip().lower())
    )
    labels = [label for label, _ in items]
    percents = [(c / total) * 100 for _, c in items]

    cmap = cm.get_cmap("viridis", len(labels))
    colors = cmap(np.linspace(0, 1, len(labels)))

    fig, ax = plt.subplots()
    bars = ax.barh(labels, percents, color=colors)

    for bar, pct in zip(bars, percents):
        ax.text(pct + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{pct:,.2f}%", va="center", ha="left", fontsize=9)

    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.title(f"{area} ({report_type})", fontsize=11, weight="bold")
    plt.tight_layout()

    out_dir = r"plots\ag"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{file_name}.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
