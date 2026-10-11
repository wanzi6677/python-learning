import pandas as pd

def load_and_clean(path = "resourse/raw_stock.csv"):
    df = pd.read_csv(path)

    df["日期"] = pd.to_datetime(df["日期"],format = 'mixed')
    df["收盘价"] = pd.to_numeric(df["收盘价"], errors = 'coerce')
    df = df.drop_duplicates()#去重
    df = df.dropna(subset = ["收盘价", "成交额"])#删除空值
    df = df[(df["收盘价"]>0) & (df["成交额"]>0)]
    df = df.sort_values("日期").reset_index(drop = True)

    return df[["日期", "收盘价","成交额"]]

print(load_and_clean())

