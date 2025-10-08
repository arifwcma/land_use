import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("affected_wetlands.csv")
df["wetland_total"] = df["wetland_nodata"] + df["wetland_positive"]
wcma_row = pd.DataFrame(df.drop(columns=["area"]).sum()).T
wcma_row.insert(0, "area", "Whole WCMA")
df = pd.concat([df, wcma_row], ignore_index=True)


df["Affected Wetlands (%)"] = (df["overlapped"] / df["wetland_total"] * 100).round(2)
df["Affected Wetlands (%)"] = df["Affected Wetlands (%)"].apply(lambda x: f"{x:.2f}")

colors = plt.cm.tab10.colors
bars = plt.bar(df["area"], df["Affected Wetlands (%)"].astype(float), color=colors[:len(df)])

for bar, val in zip(bars, df["Affected Wetlands (%)"]):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), val, ha='center', va='bottom')

#plt.xlabel("Area")
plt.ylabel("Affected Wetlands (%)")
plt.title("Affected Wetlands by Local Area")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
