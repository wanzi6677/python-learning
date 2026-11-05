"""A 股 30 只样本名单(11 月数据层用)。

symbol 必须带交易所前缀:sh = 上交所,sz = 深交所。
新浪源(akshare stock_zh_a_daily)要求这个格式,不带前缀会拉不到。

选股规则:
    1. 只用沪深主板/创业板的大市值蓝筹,保证 3 年以上连续上市历史
    2. 7 个行业,共 30 只 —— 12 月要做行业分组统计和风险对比
    3. 不含 ST、不含新上市、不含北交所

名称已用 akshare 的 stock_info_a_code_name() 逐条核对(2026-11-05)。
注意:数据源给的名称带空格(如 "五 粮 液"),这里统一用规范名("五粮液")。
"""
STOCKS = [
    # ── 银行 5 只 ──
    {"symbol": "sz000001", "name": "平安银行", "industry": "银行"},
    {"symbol": "sh600036", "name": "招商银行", "industry": "银行"},
    {"symbol": "sh601398", "name": "工商银行", "industry": "银行"},
    {"symbol": "sh601166", "name": "兴业银行", "industry": "银行"},
    {"symbol": "sz002142", "name": "宁波银行", "industry": "银行"},

    # ── 白酒 4 只 ──
    {"symbol": "sh600519", "name": "贵州茅台", "industry": "白酒"},
    {"symbol": "sz000858", "name": "五粮液", "industry": "白酒"},
    {"symbol": "sz000568", "name": "泸州老窖", "industry": "白酒"},
    {"symbol": "sh600809", "name": "山西汾酒", "industry": "白酒"},

    # ── 新能源 4 只 ──
    {"symbol": "sz300750", "name": "宁德时代", "industry": "新能源"},
    {"symbol": "sh601012", "name": "隆基绿能", "industry": "新能源"},
    {"symbol": "sz002594", "name": "比亚迪", "industry": "新能源"},
    {"symbol": "sz300274", "name": "阳光电源", "industry": "新能源"},

    # ── 医药 4 只 ──
    {"symbol": "sh600276", "name": "恒瑞医药", "industry": "医药"},
    {"symbol": "sh600436", "name": "片仔癀", "industry": "医药"},
    {"symbol": "sz000538", "name": "云南白药", "industry": "医药"},
    {"symbol": "sz300760", "name": "迈瑞医疗", "industry": "医药"},

    # ── 能源 4 只 ──
    {"symbol": "sh601857", "name": "中国石油", "industry": "能源"},
    {"symbol": "sh601088", "name": "中国神华", "industry": "能源"},
    {"symbol": "sh600900", "name": "长江电力", "industry": "能源"},
    {"symbol": "sh601985", "name": "中国核电", "industry": "能源"},

    # ── 券商 4 只 ──
    {"symbol": "sh600030", "name": "中信证券", "industry": "券商"},
    {"symbol": "sz300059", "name": "东方财富", "industry": "券商"},
    {"symbol": "sh601211", "name": "国泰海通", "industry": "券商"},
    {"symbol": "sh600999", "name": "招商证券", "industry": "券商"},

    # ── 地产基建 5 只 ──
    {"symbol": "sz000002", "name": "万科A", "industry": "地产基建"},
    {"symbol": "sh600048", "name": "保利发展", "industry": "地产基建"},
    {"symbol": "sh601668", "name": "中国建筑", "industry": "地产基建"},
    {"symbol": "sh601390", "name": "中国中铁", "industry": "地产基建"},
    {"symbol": "sh600606", "name": "绿地控股", "industry": "地产基建"},
]


def check_stocks(stocks):
    """返回格式不对的条目列表;空列表 = 全部合法。"""
    bad = []
    for s in stocks:
        if len(s["symbol"]) != 8 or s["symbol"][:2] not in ("sh", "sz"):
            bad.append(s)
        elif not s["name"] or not s["industry"]:
            bad.append(s)
    return bad

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    print(f"共 {len(STOCKS)} 只")
    bad = check_stocks(STOCKS)
    if bad:
        print(f"❌ 格式有问题 {len(bad)} 条:")
        for s in bad:
            print("   ", s)
    else:
        print("✅ 格式全部合法")

    from pipeline import fetch
    for s in STOCKS:
        try:
            df = fetch(s["symbol"], "20230101", "20251231")
            print(s["symbol"], s["name"], len(df), "✅")
        except Exception as e:
            print(s["symbol"], s["name"], "❌", e)