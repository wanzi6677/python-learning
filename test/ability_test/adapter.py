import pandas as pd

# 全字段:入库用。顺序和 db.py 里 prices 表的列顺序一一对应,不许改顺序。
# volume=成交量(股),  amount=成交额(元),  turnover=换手率
FULL_COLUMNS = ["日期", "开盘价", "最高价", "最低价", "收盘价", "成交量", "成交额", "换手率"]


def to_full(df):
    """把 akshare(新浪源) 的原始 DataFrame 转成全字段标准格式。

    跟 to_standard 的区别:
        to_standard  只留 三列(日期/收盘价/成交额),算指标用,已稳定,不动它
        to_full      留 八列,prices 表入库用 —— 12 月算 MACD/RSI 需要高低价和成交量

    date 列的元素是 datetime.date,不是字符串,也不是 Timestamp,
    所以按天比较时要把查询区间也转成 date,不能转成 Timestamp。

    时间顺序是故意的:先 to_full 再 to_standard。
    如果先 to_standard,df 只剩三列,to_full 就找不到 open/high 了。
    """
    if set(FULL_COLUMNS).issubset(df.columns):
        return df[FULL_COLUMNS].reset_index(drop=True)

    missing = [c for c in ["date", "open", "high", "low", "close", "volume", "amount", "turnover"]
               if c not in df.columns]
    if missing:
        raise ValueError(f"to_full 输入缺列: {missing}")

    dates = pd.to_datetime(df["date"])
    out = pd.DataFrame({
        "日期": _parse_mixed(dates),
        "开盘价": pd.to_numeric(df["open"], errors="coerce"),
        "最高价": pd.to_numeric(df["high"], errors="coerce"),
        "最低价": pd.to_numeric(df["low"], errors="coerce"),
        "收盘价": pd.to_numeric(df["close"], errors="coerce"),
        "成交量": pd.to_numeric(df["volume"], errors="coerce"),
        "成交额": pd.to_numeric(df["amount"], errors="coerce"),
        "换手率": pd.to_numeric(df["turnover"], errors="coerce"),
    })
    return out.sort_values("日期").reset_index(drop=True)


def _parse_mixed(series, **kwargs):
    """兼容新旧 pandas 的日期解析写法。

    老写法 format="mixed"(pandas 2.0+,本项目 2.3.3):能处理一条一个格式
    新写法 format="ISO8601"(pandas 3.0 起,mixed 被移除)
    直接写 format="mixed" 将来升级 pandas 会 SyntaxError,所以在这里兜一层。
    """
    try:
        return pd.to_datetime(series, format="mixed", **kwargs)
    except (TypeError, ValueError):
        return pd.to_datetime(series, format="ISO8601", **kwargs)


def to_standard(df):
    """
        把 akshare(新浪源) 的 DataFrame 转成标准格式。

        输入列: date, open, high, low, close, volume, amount, ...
        输出列: 日期, 收盘价, 成交额

        要求:
          - date  → 日期（转成 datetime 类型）
          - close → 收盘价
          - amount → 成交额
          - 只保留这三列
        """
    if set(["日期", "收盘价", "成交额"]).issubset(df.columns):
        return df[["日期", "收盘价", "成交额"]].reset_index(drop=True)

    df["日期"] = df["date"].rename("日期")
    df["收盘价"] = df["close"].rename("收盘价")
    df["成交额"] = df["amount"].rename("成交额")
    df["日期"] = pd.to_datetime(df["日期"])
    df = df[["日期", "收盘价", "成交额"]]
    return df.reset_index(drop=True)
