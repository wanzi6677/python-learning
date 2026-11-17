"""11 月数据层:SQLite 入库。

第一阶段只做 stocks 表 —— 把 stock_list.py 里 30 只股票的基本信息落库。

为什么要分三张表(考试第 2 章"码"的概念,也是面试题):
    三种数据的变化频率完全不同,混成一张表会重复存储。
        stocks  每只股票 1 条,几乎不变(名称会改,如国泰君安 -> 国泰海通)
        prices  每只股票 ~727 条(3 年交易日),每天 +1
        metrics 每只股票 1 条,算一次就固定
    挤成一张表:stocks 那一行信息要跟着 prices 复制 727 遍,
    名称一改要改 727 行,漏一行同一个代码就有两个名字。

主键选 symbol 而不是自增 id:
    prices 表用 (symbol, date) 就能指回是哪只股票,不用先查一次 id 转一手。
    代价:股票代码一旦变(合并/改名换代码)要手动维护 —— 记在待办里。

用法(在 ability_test 目录下):
    ..\\..\\.venv\\Scripts\\python.exe db.py
"""
import sqlite3
import sys
from pathlib import Path

from stock_list import STOCKS

# 库文件和 db.py 放同一个文件夹。
# 不能写相对路径 "stocks.db" —— 那是相对"运行时所在目录",
# 换个目录跑就会新建一个空库,查出来 0 行还以为数据丢了。
DB_PATH = Path(__file__).parent / "stocks.db"


# ── 建表 / 写数据 / 查数据 ────────────────────────────────────

def connect():
    """打开(不存在就创建)数据库连接。"""
    return sqlite3.connect(DB_PATH)


def create_tables(conn):
    """建 stocks 表。

    IF NOT EXISTS: 跑第二遍不报错也不重建 —— 重复执行是安全的。
    PRIMARY KEY:  symbol 唯一且不能为 NULL(实体完整性)。
    NOT NULL:     name / industry 不许空 —— 表是给未来数据定的规矩,
                  不是只给今天这 30 条。
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            symbol   TEXT PRIMARY KEY,
            name     TEXT NOT NULL,
            industry TEXT NOT NULL
        )
    """)
    conn.commit()


def insert_stocks(conn, stocks):
    """把 30 只股票写进 stocks 表。

    INSERT OR IGNORE: 主键已存在就跳过,不报错。
        第一次跑 30 条全部插入;第二次跑全部被忽略,COUNT 仍是 30 不是 60。
        这就是"幂等"—— 同一个脚本跑几遍结果都一样。
    返回: 本次真正插入的行数。
    """
    rows = [(s["symbol"], s["name"], s["industry"]) for s in stocks]
    cur = conn.executemany(
        "INSERT OR IGNORE INTO stocks (symbol, name, industry) VALUES (?, ?, ?)",
        rows,
    )
    conn.commit()
    return cur.rowcount


def count(conn, table):
    """查表行数。"""
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


# ── 验证 ─────────────────────────────────────────────────────

def verify(conn):
    """跑完必须看到的几个数字,返回 True/False。"""
    results = []
    n = count(conn, "stocks")
    results.append((n == 30, f"stocks 行数 = {n}(应为 30)"))

    # 行业分布:7 个行业,加起来必须还是 30
    dist = conn.execute(
        "SELECT industry, COUNT(*) FROM stocks GROUP BY industry ORDER BY COUNT(*) DESC"
    ).fetchall()
    total = sum(c for _, c in dist)
    results.append((total == 30 and len(dist) == 7,
                    f"行业 {len(dist)} 个,合计 {total}(应为 7 个 / 30 只)"))
    for industry, c in dist:
        print(f"     {industry:<6} {c}")

    # 主键不能有重复(符号上 PRIMARY KEY 已保证,这里再实证一次)
    dup = conn.execute(
        "SELECT COUNT(*) FROM (SELECT symbol FROM stocks GROUP BY symbol HAVING COUNT(*) > 1)"
    ).fetchone()[0]
    results.append((dup == 0, f"重复 symbol = {dup}(应为 0)"))

    # 对照源数据:库里每个 symbol 都能在 STOCKS 里找到
    in_db = {r[0] for r in conn.execute("SELECT symbol FROM stocks")}
    in_src = {s["symbol"] for s in STOCKS}
    results.append((in_db == in_src,
                    f"库 vs 名单差异 = {len(in_db ^ in_src)}(应为 0)"))

    return results


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    print(f"库文件: {DB_PATH}")
    conn = connect()

    create_tables(conn)
    inserted = insert_stocks(conn, STOCKS)
    print(f"本次插入 {inserted} 行")

    print("-" * 40)
    results = verify(conn)

    print("-" * 40)
    for ok, msg in results:
        print(("✅ " if ok else "❌ ") + msg)

    passed = sum(1 for ok, _ in results if ok)
    print(f"通过 {passed} / {len(results)}")

    conn.close()
    sys.exit(0 if passed == len(results) else 1)
