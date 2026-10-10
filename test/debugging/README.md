# 数据源排查记录

2026-10-10，在用 akshare 获取 A 股数据时遇到的真实问题，以及完整的排查过程。

## 问题

调用 `ak.stock_zh_a_hist()` 报错：

```
ConnectionError: ('Connection aborted.', RemoteDisconnected(
    'Remote end closed connection without response'))
```

## 排查步骤

| 文件 | 做了什么 | 结论 |
|---|---|---|
| `01_test_domains.py` | 测三个网址：百度 / eastmoney / 新浪 | 百度 ✅、eastmoney 根路径 ✅(404)、新浪 ✅ |
| `02_reproduce_failure.py` | **精确复现**：测带参数的完整接口地址 | eastmoney 接口 ❌ 连接被重置 |
| `03_find_alternative.py` | 读 `inspect.getsource()` 源码 | 发现 `stock_zh_a_daily` 走**新浪**源 |
| `04_try_sina.py` | 换用新浪源接口 | ✅ 成功，242 行数据 |
| `05_test_adapter.py` | 测试自己写的适配层 | ✅ 列名统一成功 |
| `06_end_to_end.py` | 端到端：数据源 → 适配 → 指标 | ✅ 算出真实指标 |

## 关键发现

1. **报错类型决定问题层次**：`ConnectionError` 是网络层错误，不是代码错误 —— 改代码没用。
2. **域名通 ≠ 接口通**：`push2his.eastmoney.com` 根路径返回 404（说明能连上），
   但 `/api/qt/stock/kline/get` 这个接口地址连接被重置。
   **排查必须精确到失败的那次请求**，不能只测域名。
3. **解决方案**：切换到走新浪数据源的 `ak.stock_zh_a_daily`。

## 踩到的坑

新浪源的 `symbol` 参数需要**交易所前缀**：

```python
# ❌ 不行
ak.stock_zh_a_daily(symbol="000001")

# ✅ 正确（sz = 深市，sh = 沪市）
ak.stock_zh_a_daily(symbol="sz000001")
```

## 最终代码

```python
import akshare as ak

df = ak.stock_zh_a_daily(
    symbol="sz000001",      # 平安银行
    start_date="20240101",
    end_date="20241231",
    adjust="qfq",           # 前复权
)
```

返回列：`date, open, high, low, close, volume, amount, outstanding_share, turnover`

## 收获

- 学会区分「代码错误」和「环境错误」
- 学会用最小可复现的方式定位问题
- 用适配层（`adapter.py`）解决数据源格式差异，新增数据源不需要改动分析逻辑
