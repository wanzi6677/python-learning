import akshare as ak
from adapter import to_standard

df = ak.stock_zh_a_daily(symbol="sz000001", start_date="20240101",
                         end_date="20241231", adjust="qfq")
print(to_standard(df))