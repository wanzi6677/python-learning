import akshare as ak

# 注意:东财源 stock_zh_a_hist 在这台机器上不通(RemoteDisconnected),
#      新浪源 stock_zh_a_daily 可用,symbol 必须带交易所前缀

def fetch(symbol, start_date, end_date):
    """拉 A 股日线数据,返回 DataFrame。"""
    try:
        df = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date,
                             end_date=end_date, adjust="qfq")

    except Exception as e:
        raise ValueError(symbol + " 拉取失败: " + type(e).__name__ + " " + str(e))

    if len(df) == 0:
        raise ValueError(symbol + " 没有数据")
    if "date" not in df.columns:
        raise ValueError(symbol + "返回的数据缺 date 列")
    return df

if __name__ == "__main__":
    for sym in ["sz000001", "sz999999"]:
        try:
            df = fetch(sym, "20240101", "20241231")
            print(sym, "OK, 行数 =", len(df))
        except ValueError as e:
            print("❌", e)