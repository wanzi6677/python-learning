import pandas as pd
df = pd.read_csv("resourse/raw_stock.csv")

df["日期"] = pd.to_datetime(df["日期"],format="mixed")
print(df["日期"])
print(df["日期"].dtypes)
