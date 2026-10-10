import requests

urls = [
    "https://www.baidu.com",
    "https://push2his.eastmoney.com",
    "https://hq.sinajs.cn/list=sz000001",
]

for url in urls:
    try:
        r = requests.get(url, timeout=10,
                         headers={"User-Agent": "Mozilla/5.0",
                                  "Referer": "https://finance.sina.com.cn"})
        print(f"OK   {r.status_code}  {url}")
    except Exception as e:
        print(f"FAIL {type(e).__name__:20s} {url}")