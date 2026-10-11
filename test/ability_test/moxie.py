"""
默写测试 —— 凭记忆重写三个函数
规则：
  1. 不要打开 task.py，不要问 AI，不要搜现成的答案
  2. 可以查官方文档（pandas.pydata.org）—— 只查 API 名字，不查完整写法
  3. 想不起来某个 API 名字就写注释占位，比如：# 这里应该是去重的方法
  4. 全部写完后，再和 task.py 对照
期望结果（写完后跑一下验证）：
  - load_and_clean() 返回 8 行数据
  - calc_indicators() 返回 {'总收益率': 7.2, '日收益率波动率': 1.95, '最大回撤': 1.67}
自查方法：写完直接运行这个文件：
    ..\.venv\Scripts\python.exe moxie.py
"""
import pandas as pd
from pandas import read_csv, to_datetime

RAW_FILE = "raw_stock.csv"
CLEAN_FILE = "clean_stock_moxie.csv"  # 用新文件名，避免占用问题
def load_and_clean(path=RAW_FILE):
    """
    读入 CSV 并清洗，返回干净的 DataFrame。要求：
      - "日期" 解析成 datetime 类型（三种混用格式：2026-01-05 / 2026/1/6 / 20260107）
      - "收盘价" 转成数值，无法转换的（如 "N/A"）变成缺失值
      - 删掉完全重复的行
      - 删掉"成交额"为空的行
      - 删掉"收盘价"为空的行
      - 删掉收盘价 <= 0 的行
      - 按日期升序排序，重置索引
      - 最终只保留列：日期、收盘价、成交额
    顺序提示（想不起来就先照这个顺序写）：
        读 → 转日期 → 转数值 → 去重 → 删空 → 删脏 → 排序 → 选列
    """
    # >>> 在这里写你的代码 <<<
    #我要默写所以接下来不要提示代码
    df = read_csv(path)
    df["日期"] = pd.to_datetime(df["日期"],format = "mixed")
    df["收盘价"] = pd.to_numeric(df["收盘价"], errors="coerce")
    df = df.drop_duplicates()
    df = df.dropna(subset=["成交额", "收盘价"])
    df = df[df["收盘价"]>0]
    df = df.sort_values(by="日期").reset_index(drop=True)
    df = df[["日期", "收盘价", "成交额"]]
    return df

def calc_indicators(df):
    """
    基于清洗后的 df，返回一个 dict，包含三个指标：
      - "总收益率"       (最后一天收盘价 / 第一天收盘价 - 1) * 100，保留 2 位小数
      - "日收益率波动率"  日收益率的标准差 * 100，保留 2 位小数
                         （日收益率 = 收盘价的 pct_change()）
      - "最大回撤"       (收盘价 / 收盘价的累计最大值 - 1) 的最小值 * 100，
                         取绝对值，保留 2 位小数
    返回示例：{"总收益率": 12.34, "日收益率波动率": 1.23, "最大回撤": 5.67}
    """
    # >>> 在这里写你的代码 <<<
    close = df["收盘价"]
    total_return = round((close.iloc[-1]/close.iloc[0]-1)*100,2)
    daily_return_std = round(close.pct_change().std()*100,2)
    max_drawdown = round(abs((close/close.cummax()-1).min()*100),2)
    return{"总收益率": total_return, "日收益率波动率": daily_return_std, "最大回撤": max_drawdown}

def save_clean(df, path=CLEAN_FILE):
    """
    把清洗后的 df 存成 CSV，要求：
      - utf-8 编码
      - 不要写入索引列
    """
    # >>> 在这里写你的代码 <<<
    df.to_csv(path, index=False, encoding="utf-8")

if __name__ == "__main__":
    clean = load_and_clean()
    print("=== 清洗结果 ===")
    print(clean)
    print(f"\n行数：{len(clean)}   （期望 8）")
    print(f"索引：{list(clean.index)}   （期望 0~7）")
    print("\n=== 指标 ===")
    print(calc_indicators(clean))
    save_clean(clean)
    print(f"\n已保存到 {CLEAN_FILE}")
    # 完成后对照一下（可选，别提前看）
    # import task
    # print("\n=== 与 task.py 对照 ===")
    # print(task.load_and_clean().equals(clean))