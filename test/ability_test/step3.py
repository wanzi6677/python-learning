import pandas as pd
df = pd.read_csv("resourse/raw_stock.csv")
df["日期"] = pd.to_datetime(df["日期"], format="mixed")

print("总行数:",len(df))
print("完全重复的行数:",df.duplicated().sum())
print("收盘价为空的行数:",df["收盘价"].isnull().sum())
print("成交额为空的行数:",df["成交额"].isnull().sum())
print("收盘价小于等于0的行数:",(df["收盘价"]<=0).sum())
print("成交额小于等于0的行数:",(df["成交额"]<=0).sum())
print("日期是否已排序:",df["日期"].is_monotonic_increasing)



