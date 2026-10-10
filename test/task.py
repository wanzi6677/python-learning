"""
动手能力检验任务（关掉 AI 完成）

题目：把一份「脏」的股票日线 CSV 清洗成干净数据，并算出 3 个指标。

规则：
  1. 全程不要问 AI，不要搜。可以查官方文档（docs.python.org / pandas 文档）。
  2. 卡住就跳过，写下你是怎么想的（注释或笔记），卡住的地方也是信息。
  3. 限时 60 分钟。时间到了就停，即使没写完 —— 没写完也是有效结果。
  4. 写不出来完全没关系，这个测试的目的是定位起点，不是考你。

运行自检（写完再跑，先别偷看 check_task.py 的实现）：
    python check_task.py
"""
import pandas as pd

# 输入文件（故意做脏了，包含下面这些问题）：
#   - 有完全重复的行
#   - 有 "成交额" 为空的行
#   - "收盘价" 里混进了字符串 "N/A"
#   - "日期" 列格式不统一（2026-01-05 / 2026/1/6 / 20260107 三种混着）
#   - 有一行的收盘价明显是错的（负数）
#   - 数据没有按日期排序
RAW_FILE = "raw_stock.csv"
CLEAN_FILE = "clean_stock.csv"


def load_and_clean(path=RAW_FILE):
    """
    任务 1：读入 CSV 并清洗，返回一个干净的 DataFrame，要求：
      - "日期" 解析成 pandas 的 datetime 类型（处理三种混用格式）
      - "收盘价" 转成数值类型，无法转换的（如 "N/A"）变成缺失值
      - 删掉完全重复的行
      - 删掉"成交额"为空的行
      - 删掉收盘价 <= 0 的行（脏数据）
      - 按日期升序排序，重置索引
      - 最终只保留列：日期、收盘价、成交额

    提示（只是 API 名字，不是答案）：pd.to_datetime / pd.to_numeric /
         drop_duplicates / dropna / sort_values / reset_index


    """
    df = pd.read_csv(path)
    df["日期"] = pd.to_datetime(df["日期"], format="mixed")
    df["收盘价"] = pd.to_numeric(df["收盘价"], errors="coerce")
    df = df.drop_duplicates()
    df = df.dropna(subset=["成交额", "收盘价"])
    df = df[df["收盘价"] > 0]
    df = df.sort_values("日期").reset_index(drop=True)
    return df[["日期", "收盘价", "成交额"]]
    raise NotImplementedError("任务 1 还没写")


def calc_indicators(df):
    """
    任务 2：基于清洗后的 df，算出并返回一个 dict：
      - "总收益率"：  (最后一天收盘价 / 第一天收盘价 - 1) * 100，保留 2 位小数
      - "日收益率波动率"：日收益率( pct_change() )的标准差 * 100，保留 2 位小数
      - "最大回撤"：  用 (收盘价 / 收盘价的累计最大值 - 1) 的最小值 * 100，
                      结果取绝对值保留 2 位小数

    返回示例：{"总收益率": 12.34, "日收益率波动率": 1.23, "最大回撤": 5.67}
    """
    close = df["收盘价"]
    total_return = round((close.iloc[-1] / close.iloc[0] - 1) * 100, 2)
    daily_return_std = round(close.pct_change().std() * 100, 2)

    # 最大回撤：cummax() 是历史最高价，比值-1 后 min() 是最深回撤（负数），再取绝对值
    max_drawdown = round(abs((close/close.cummax()-1).min()*100), 2)

    return {
        "总收益率": total_return,
        "日收益率波动率": daily_return_std,
        "最大回撤": max_drawdown,
    }


def save_clean(df, path=CLEAN_FILE):
    """任务 3：把清洗后的 df 存成 CSV（utf-8，不要索引）"""
    df.to_csv(path, index=False,encoding="utf-8")


if __name__ == "__main__":
    clean = load_and_clean()
    print(clean)
    print()
    print(calc_indicators(clean))
    save_clean(clean)
    print(f"\n已保存到 {CLEAN_FILE}")
