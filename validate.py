import pandas as pd

df = pd.read_csv("test.csv")
total = df["Count"].sum()
result = df.groupby("AGIND")["Count"].sum().reset_index()
result["Percent"] = (result["Count"] / total) * 100
print(result)
