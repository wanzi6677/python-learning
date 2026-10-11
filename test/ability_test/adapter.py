import pandas as pd

def to_standard(df):
    # 如果已经是标准格式，直接返回
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
        return df

    # >>> 你来写 <<<
    df["日期"] = df["date"].rename("日期")
    df["收盘价"] = df["close"].rename("收盘价")
    df["成交额"] = df["amount"].rename("成交额")
    df["日期"] = pd.to_datetime(df["日期"])
    df = df[["日期", "收盘价", "成交额"]]
    return df
