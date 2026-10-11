"""
独立校验脚本 —— 不要修改这个文件，用来检查 task.py 写得对不对。

用法：
    python check_task.py

它不看你 task.py 的内部实现，只看输入输出是否符合要求。
"""
import sys
import traceback

# Windows 控制台默认 GBK，先切到 utf-8，否则中文/符号输出会乱码或直接报错
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd

import task

# 12 行原始数据：
#   - 1 行完全重复（2026-01-05）
#   - 1 行成交额为空（2026-01-09）
#   - 1 行收盘价是 "N/A"，转数值后变缺失，要删
#   - 1 行收盘价为负（-5.0），是脏数据，要删
#   → 剩 8 行
EXPECTED_ROWS = 8

results = []


def check(name, fn):
    try:
        fn()
        results.append((True, name, ""))
    except Exception as error:
        detail = f"{type(error).__name__}: {error}"
        results.append((False, name, detail))


def test_load():
    df = task.load_and_clean()
    assert isinstance(df, pd.DataFrame), "返回值不是 DataFrame"
    assert list(df.columns) == ["日期", "收盘价", "成交额"], f"列不对：{list(df.columns)}"
    assert pd.api.types.is_datetime64_any_dtype(df["日期"]), "日期列不是 datetime 类型"
    assert pd.api.types.is_numeric_dtype(df["收盘价"]), "收盘价列不是数值类型"
    assert not df["成交额"].isna().any(), "成交额还有空值没删掉"
    assert not (df["收盘价"] <= 0).any(), "还有收盘价 <= 0 的脏数据"
    assert df["日期"].is_monotonic_increasing, "没有按日期升序排序"
    assert not df.duplicated().any(), "还有完全重复的行"
    assert len(df) == EXPECTED_ROWS, f"行数应该是 {EXPECTED_ROWS}，实际是 {len(df)}"
    # 日期必须解析正确（检查三种格式都认出来了）
    first, last = df["日期"].iloc[0], df["日期"].iloc[-1]
    assert first == pd.Timestamp("2026-01-05"), f"第一天日期不对：{first}"
    assert last == pd.Timestamp("2026-01-19"), f"最后一天日期不对：{last}"
    globals()["_clean_df"] = df


def test_indicators():
    df = globals().get("_clean_df")
    if df is None:
        raise AssertionError("清洗没通过，无法校验指标")
    got = task.calc_indicators(df)
    assert isinstance(got, dict), "返回值不是 dict"
    for key in ["总收益率", "日收益率波动率", "最大回撤"]:
        assert key in got, f"缺少字段：{key}"

    # 用独立算法重算一遍作为标准答案
    close = df["收盘价"]
    exp_total = round((close.iloc[-1] / close.iloc[0] - 1) * 100, 2)
    exp_vol = round(close.pct_change().std() * 100, 2)
    exp_dd = round(abs((close / close.cummax() - 1).min() * 100), 2)

    for key, expected in [("总收益率", exp_total), ("日收益率波动率", exp_vol), ("最大回撤", exp_dd)]:
        actual = got[key]
        assert abs(float(actual) - expected) < 0.02, f"{key} 应该是 {expected}，实际是 {actual}"


def test_save():
    import os
    if os.path.exists(task.CLEAN_FILE):
        os.remove(task.CLEAN_FILE)
    df = globals().get("_clean_df")
    if df is None:
        raise AssertionError("清洗没通过，无法校验保存")
    task.save_clean(df)
    assert os.path.exists(task.CLEAN_FILE), "没有生成 clean_stock.csv"
    back = pd.read_csv(task.CLEAN_FILE)
    assert "Unnamed: 0" not in back.columns, "保存时带上了索引列"
    assert len(back) == EXPECTED_ROWS, f"存回去的行数不对：{len(back)}"


check("任务1 读取与清洗", test_load)
check("任务2 三个指标计算", test_indicators)
check("任务3 保存 CSV", test_save)

print("=" * 52)
for ok, name, detail in results:
    print(("  ✅ " if ok else "  ❌ ") + name + ("" if ok else f"  ->  {detail}"))
print("=" * 52)
passed = sum(1 for ok, _, _ in results if ok)
print(f"通过 {passed} / {len(results)}")

if passed == len(results):
    print("\n结论：数据清洗 + 指标计算这一层你已经能独立完成，不需要补基础语法。")
else:
    print("\n结论：把失败的那几项当作起点，不用重学整个 Python。")
