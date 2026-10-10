import requests

url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
params = {
    "secid": "0.000001",
    "fields1": "f1,f2,f3,f4,f5",
    "fields2": "f51,f52,f53,f54,f55",
    "klt": "101",
    "fqt": "1",
    "beg": "20240101",
    "end": "20241231",
}
try:
    r = requests.get(url, params=params, timeout=15,
                     headers={"User-Agent": "Mozilla/5.0"})
    print("OK", r.status_code, len(r.text))
    print(r.text[:200])
except Exception as e:
    print("FAIL", type(e).__name__, str(e)[:120])