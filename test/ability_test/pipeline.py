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

def run_many(symbols, start_date="20240101", end_date="20241231"):
    rows = []
    for symbol in symbols:              # ← 循环拿每一只
        try:
            result = run(symbol, start_date, end_date)           # ← 复用 run!想想传哪三个参数
            result["symbol"] = symbol             # ← 补上股票代码这一列
            rows.append(result)             # ← 一行一个 dict,攒起来
        except Exception as e:
            rows.append({
                "symbol": symbol,
                "错误": f"{type(e).__name__}: {e}",  # ← 带类型名
            })
            continue

    # 打印表格
    print(f"{'股票':<10}{'总收益率':<10}{'日波动率':<10}{'最大回撤':<10}")
    for row in rows:
        if "错误" in row:
            print(f"⚠️ {row['错误']}")
        else:
            print(f"{row['symbol']:<10}{row['总收益率']:>8.2f} %{row['日收益率波动率']:>8.2f} %{row['最大回撤']:>8.2f} %")    # ← 自己填
    return rows


if __name__ == "__main__":
    run_many(["sz000001", "sz999999", "sh601318"])