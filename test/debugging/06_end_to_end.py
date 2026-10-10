import akshare as ak
from adapter import to_standard
from task import calc_indicators

df = ak.stock_zh_a_daily(symbol="sz000001", start_date="20240101",
                         end_date="20241231", adjust="qfq")
std = to_standard(df)
print(std.head())
print(calc_indicators(std))