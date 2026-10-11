"""
股票数据管道(第一版)

输入: 股票代码(如 sz000001)
输出: 总收益率 / 日波动率 / 最大回撤

流程: fetch → to_standard → calc_indicators
"""

from fetch_stock import fetch
from adapter import to_standard
from task import calc_indicators


def run(symbol, start_date="20240101", end_date="20241231"):
    # ① 拉数据
    df = fetch(symbol, start_date, end_date)

    # ② 适配(统一列名)
    df = to_standard(df)

    # ③ 算指标
    result = calc_indicators(df)

    # ④ 打印
    print(f"{symbol}  {start_date[:4]}-{start_date[4:6]}-{start_date[6:]} ~ {end_date[:4]}-{end_date[4:6]}-{end_date[6:]}")
    for k,v in result.items():
        print(f"  {k:<14}{v:.2f} %")
    return result


if __name__ == "__main__":
    run("sz000001")