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
from datetime import date
from pathlib import Path

import pandas as pd

from adapter import to_full
from stock_list import STOCKS

# 库文件和 db.py 放同一个文件夹。
# 不能写相对路径 "stocks.db" —— 那是相对"运行时所在目录",
# 换个目录跑就会新建一个空库,查出来 0 行还以为数据丢了。
DB_PATH = Path(__file__).parent / "stocks.db"

START_DATE = "20230101"
END_DATE = "20251231"


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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            symbol   TEXT NOT NULL,
            date     TEXT NOT NULL,          -- 存 'YYYY-MM-DD' 字符串,不用 SQLite 的 DATE 类型
            open     REAL,
            high     REAL,
            low      REAL,
            close    REAL,
            volume   REAL,                   -- 成交量(股)
            amount   REAL,                   -- 成交额(元)
            turnover REAL,                   -- 换手率
            PRIMARY KEY (symbol, date),
            FOREIGN KEY (symbol) REFERENCES stocks(symbol) ON DELETE CASCADE
        )
    """)
    # 外键检查 SQLite 默认是关的,必须每个连接单独打开(不是库文件属性)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.commit()


def _today():
    return date.today().isoformat()


def prices_span(conn):
    """prices 里已有多少行、覆盖哪段时间、多少只股票。"""
    n = conn.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
    row = conn.execute("SELECT MIN(date), MAX(date), COUNT(DISTINCT symbol) FROM prices").fetchone()
    return n, row[0], row[1], row[2]


def _last_date(conn, symbol):
    """某只股票在库里的最后一天。没记录就返回 None。"""
    r = conn.execute("SELECT MAX(date) FROM prices WHERE symbol = ?", (symbol,)).fetchone()
    return r[0]


def missing_trading_days(conn):
    """找出"比全市场最多那天少掉的行"。

    关键前提:中国神华 717 行、国泰海通 708 行,其余 727 行 —— 少掉的是停牌/零成交,
    新浪源当天不给那一行。所以这里**只登记事实,不补行、不补 0**。
    补 0 会让当日收益率变成 -100%,波动率全错(11-05 已实测记录)。

    "全市场交易日集合" 用 30 只股票里出现过日期的并集来定义:
        一只股票当天没出现,但它不是这个行业的个例 → 大概率是停牌,登记下来。
    """
    all_days = {r[0] for r in conn.execute("SELECT DISTINCT date FROM prices")}
    rows = []
    for sym, in conn.execute("SELECT symbol FROM stocks ORDER BY symbol"):
        have = {r[0] for r in conn.execute("SELECT date FROM prices WHERE symbol = ?", (sym,))}
        miss = sorted(all_days - have)
        rows.append((sym, len(have), len(miss), miss))
    return rows


# ── 写数据 ───────────────────────────────────────────────────

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


def insert_prices(conn, symbol, df):
    """把一只股票的全字段日线写进 prices 表。

    增量 + 幂等:
        先看库里这只股票最后一天是哪天,只插比它更新的行。
        重复跑不会插重,也不会因为 INSERT OR REPLACE 把已有行悄悄改写。
    df 必须已经过 adapter.to_full(八列,日期升序)。

    返回: 本次插入的行数;没有新数据返回 0。
    """
    last = _last_date(conn, symbol)
    if last is not None:
        # df["日期"] 是 datetime.date,用字符串比较会错(日期转字符串在 pandas 里可能变成 Timestamp),
        # 所以两边都统一成 date 再比。
        cut = date.fromisoformat(last)
        df = df[df["日期"].apply(lambda x: x.date() if hasattr(x, "date") else x) > cut]
    if len(df) == 0:
        return 0

    # 用位置下标取值,不用 r.open / r.high ——
    # 列名是中文(日期/开盘价/…),没有 open 这个属性,写 r.open 直接 AttributeError。
    # 位置顺序 = adapter.FULL_COLUMNS =(日期, 开盘价, 最高价, 最低价, 收盘价, 成交量, 成交额, 换手率)
    rows = []
    for r in df.itertuples(index=False):
        d = r[0]
        d = (d.date() if hasattr(d, "date") else d).isoformat()
        rows.append((symbol, d, _num(r[1]), _num(r[2]), _num(r[3]), _num(r[4]),
                     _num(r[5]), _num(r[6]), _num(r[7])))
    conn.executemany(
        "INSERT OR IGNORE INTO prices "
        "(symbol, date, open, high, low, close, volume, amount, turnover) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    return len(rows)


def _num(v):
    try:
        return None if pd.isna(v) else float(v)
    except (TypeError, ValueError):
        return None


def fetch_and_store(conn, symbols, start=START_DATE, end=END_DATE, log=print):
    """批量拉数据入库。单只失败不影响其他(和 pipeline.run_many 同一个思路)。

    返回: [(symbol, 状态, 说明), ...]
    """
    from fetch_stock import fetch       # 放函数里 import:让 db.py 被 import 时不去加载 akshare

    report = []
    for i, symbol in enumerate(symbols, 1):
        try:
            df = fetch(symbol, start, end)          # 原始 9 列
            full = to_full(df)                      # → 8 列标准全字段
            n = insert_prices(conn, symbol, full)
            tag = f"新增 {n} 行" if n else "无新数据"
            report.append((symbol, "OK", f"{len(full)} 行 / {tag}"))
            log(f"[{i:>2}/{len(symbols)}] {symbol} 源 {len(full)} 行,{tag}")
        except Exception as e:
            report.append((symbol, "失败", f"{type(e).__name__}: {e}"))
            log(f"[{i:>2}/{len(symbols)}] {symbol} ❌ {type(e).__name__}: {e}")
    return report


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


def verify_prices(conn, report=None):
    """prices 表的对账。返回 (results, 缺行清单)。

    注意这里**没有**"每只都应该是 727 行"这一条 —— 那会是一条错误的判据。
    停牌日就该缺行(11-05 实测:神华 717 / 国泰海通 708 / 其余 727)。
    """
    results = []
    n, dmin, dmax, nsym = prices_span(conn)
    results.append((nsym == 30, f"prices 覆盖 {nsym} 只股票(应为 30)"))
    results.append((n > 0, f"prices 总行数 = {n}(应 > 0),{dmin} ~ {dmax}"))

    if report is not None:
        ok_cnt = sum(1 for _, st, _ in report if st == "OK")
        results.append((ok_cnt == len(report), f"拉取成功 {ok_cnt} / {len(report)} 只"))

    # 复合主键:同一只股票同一天不能出现两行
    dup = conn.execute(
        "SELECT COUNT(*) FROM (SELECT symbol, date FROM prices "
        "GROUP BY symbol, date HAVING COUNT(*) > 1)"
    ).fetchone()[0]
    results.append((dup == 0, f"重复 (symbol,date) = {dup}(应为 0)"))

    # 参照完整性:每行的 symbol 都能在 stocks 表里找到
    orphan = conn.execute(
        "SELECT COUNT(*) FROM prices p "
        "LEFT JOIN stocks s ON s.symbol = p.symbol WHERE s.symbol IS NULL"
    ).fetchone()[0]
    results.append((orphan == 0, f"孤儿行(找不到对应 stock)= {orphan}(应为 0)"))

    # 价格不能 <= 0;缺行的行**本来就不存在**,所以不会误伤
    bad = conn.execute(
        "SELECT COUNT(*) FROM prices WHERE close IS NULL OR close <= 0"
    ).fetchone()[0]
    results.append((bad == 0, f"收盘价缺失或 <= 0 的行 = {bad}(应为 0)"))

    # 单只股票覆盖天数(排除停牌日,所以只要求"有数据的股票都在合理区间")
    short = conn.execute(
        "SELECT symbol, COUNT(*) c FROM prices GROUP BY symbol "
        "HAVING c < 200 ORDER BY c"
    ).fetchall()
    results.append((not short, f"覆盖少于 200 天的股票 = {len(short)} 只(应为 0)"
                    + (f",如 {short[:3]}" if short else "")))

    missing = missing_trading_days(conn)
    return results, missing


def print_missing(missing):
    """打印缺行登记表(事实,不是错误)。"""
    total = sum(m[2] for m in missing)
    affected = [m for m in missing if m[2]]
    print(f"缺行登记:共 {len(affected)} 只股票有缺行,合计 {total} 个交易日")
    for sym, have, miss, days in affected:
        head = ", ".join(days[:6]) + (" ..." if len(days) > 6 else "")
        print(f"     {sym}  {have} 行,缺 {miss} 天: {head}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    print(f"库文件: {DB_PATH}")
    conn = connect()

    create_tables(conn)
    inserted = insert_stocks(conn, STOCKS)
    print(f"stocks:本次插入 {inserted} 行")

    print("-" * 52)
    print(f"开始拉数据入库 {START_DATE} ~ {END_DATE}(30 只,约 3~5 分钟)")
    print("-" * 52)
    report = fetch_and_store(conn, [s["symbol"] for s in STOCKS])

    print("-" * 52)
    results = verify(conn) + verify_prices(conn, report)[0]
    for ok, msg in results:
        print(("✅ " if ok else "❌ ") + msg)

    print("-" * 52)
    print_missing(verify_prices(conn)[1])
    print("-" * 52)

    passed = sum(1 for ok, _ in results if ok)
    print(f"通过 {passed} / {len(results)}")

    conn.close()
    sys.exit(0 if passed == len(results) else 1)
