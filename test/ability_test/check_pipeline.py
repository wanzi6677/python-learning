"""
pipeline 回归测试 —— 只测纯计算函数,不联网、不读写文件

为什么不测 run / run_many:
    它们要联网 (fetch),今天能过、明天断网就红。
    回归测试必须快、稳定、可重复,否则没人会跑。

期望值来源:独立脚本重算(不是"跑一遍记下来")。
注意: pandas Series.std() 默认 ddof=1(样本标准差),小样本测试必须按 ddof=1 算。

用法:
    cd D:\\Python-Project\\py_project01\\test\\ability_test
    $env:PYTHONIOENCODING="utf-8"
    ..\\..\\.venv\\Scripts\\python.exe check_pipeline.py
"""
import sys

import pandas as pd

from task import calc_indicators
from adapter import to_standard


def check_indicators(closes, expect, note=""):
    """用已知答案的收盘价序列,断言三个指标"""
    df = pd.DataFrame({"收盘价": closes})
    got = calc_indicators(df)
    diffs = {k: abs(float(got[k]) - expect[k]) for k in expect}
    ok = all(d < 0.011 for d in diffs.values())
    flag = "✅" if ok else "❌"
    print(f"{flag} {closes} {note}")
    if not ok:
        print(f"     得到 { {k: float(v) for k, v in got.items()} }")
        print(f"     期望 {expect}")
    return ok


def check_adapter(columns, expect_ok=True, note=""):
    """给一个原始列名的 df,检查 to_standard 的输出"""
    data = {c: ([1, 2] if c != "date" else ["2024-01-02", "2024-01-03"]) for c in columns}
    if "amount" in data:
        data["amount"] = [1000, 2000]
    src = pd.DataFrame(data)
    try:
        out = to_standard(src)
    except Exception as e:
        ok = not expect_ok
        flag = "✅" if ok else "❌"
        print(f"{flag} to_standard({columns}) {note} -> 抛 {type(e).__name__}")
        return ok

    if not expect_ok:
        print(f"❌ to_standard({columns}) {note} -> 期待报错,却成功返回了")
        return False

    ok = (
        list(out.columns) == ["日期", "收盘价", "成交额"]
        and len(out) == len(src)
        and pd.api.types.is_datetime64_any_dtype(out["日期"])
    )
    flag = "✅" if ok else "❌"
    print(f"{flag} to_standard({columns}) {note} -> {list(out.columns)}")
    return ok


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    results = []

    # ===== calc_indicators =====
    # 单边上涨:121/100-1 = 21%;一路上涨没有回撤 = 0;日收益率都是 0.1,标准差 0
    results.append(check_indicators(
        [100, 110, 121],
        {"总收益率": 21.0, "日收益率波动率": 0.0, "最大回撤": 0.0},
        "# 单边上涨",
    ))

    # 单边下跌:-20%;从 100 跌到 80,回撤 20(取绝对值后是正数)
    # 日收益率 [-10%,-11.11%],std(ddof=1)=0.7857 -> 0.79
    results.append(check_indicators(
        [100, 90, 80],
        {"总收益率": -20.0, "日收益率波动率": 0.79, "最大回撤": 20.0},
        "# ← 照妖镜:最大回撤忘了 abs 会变 -20",
    ))

    # 先涨后跌:110/100-1 = 10%;历史最高 120 跌到 90 -> 90/120-1 = -25% -> 25
    results.append(check_indicators(
        [100, 120, 90, 110],
        {"总收益率": 10.0, "日收益率波动率": 26.65, "最大回撤": 25.0},
        "# 先涨后跌",
    ))

    # ← 最值钱的一条:50 是最低价,但历史最高是 200
    #   正确(cummax):先 100->50 跌 50%,再 200->150 跌 25% -> 最深 50
    #   若写成 close.min():150/50-1 = +200% -> abs 后 200  <- 只有这条会红
    results.append(check_indicators(
        [100, 50, 200, 150],
        {"总收益率": 50.0, "日收益率波动率": 195.26, "最大回撤": 50.0},
        "# ← 照妖镜:抓 cummax 写成 min",
    ))

    # 平盘:三个指标都必须是 0,不能是 NaN
    results.append(check_indicators(
        [100, 100, 100],
        {"总收益率": 0.0, "日收益率波动率": 0.0, "最大回撤": 0.0},
        "# ← 照妖镜:平盘不能出 NaN",
    ))

    # ===== to_standard =====
    results.append(check_adapter(["date", "close", "amount"], True, "# 标准三列"))
    results.append(check_adapter(["date", "close"], False, "# ← 照妖镜:缺 amount 列必须报错"))

    # ===== 汇总 =====
    print("=" * 52)
    passed = sum(results)
    print(f"通过 {passed} / {len(results)}")
    print("=" * 52)
    sys.exit(0 if passed == len(results) else 1)