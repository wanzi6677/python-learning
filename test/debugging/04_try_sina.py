import akshare as ak

df = ak.stock_zh_a_daily(
    symbol="sz000001",        # ← 带 sz 前缀
    start_date="20240101",
    end_date="20241231",
    adjust="qfq",
)
print(df.shape)
print(df.columns.tolist())
print(df.head())