import akshare as ak

# 注意:东财源 stock_zh_a_hist 在这台机器上不通(RemoteDisconnected),
#      新浪源 stock_zh_a_daily 可用,symbol 必须带交易所前缀

def fetch(symbol, start_date, end_date):
    """拉 A 股日线数据,返回 DataFrame。"""
    df = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date,
                             end_date=end_date, adjust="qfq")
    return df

if __name__ == "__main__":
    df = fetch("sz000001", "20240101", "20241231")
    print(df.head())