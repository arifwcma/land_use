import arcpy
from get_class_maps import parse_lyrx_classes
import numpy as np


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
    import os
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np

    if not class_counts:
        print(f"No data to plot for {area} ({report_type})")
        return

    items = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
    labels = [label for label, _ in items]
    percents = [(c / total) * 100 for _, c in items]

    cmap = cm.get_cmap("viridis", len(labels))
    colors = cmap(np.linspace(0, 1, len(labels)))

    fig, ax = plt.subplots()
    bars = ax.barh(range(len(labels)), percents, color=colors)

    for i, (bar, pct) in enumerate(zip(bars, percents)):
        ax.text(pct + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{pct:,.2f}%", va="center", ha="left", fontsize=9)
        ax.text(-1, bar.get_y() + bar.get_height() / 2,
                labels[i], va="center", ha="right", fontsize=9)

    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, max(percents) + 5)
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.title(f"{area} ({report_type})", fontsize=11, weight="bold")
    plt.tight_layout()

    out_dir = fr"plots\{report_type}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{file_name}.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
