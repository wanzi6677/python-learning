import csv
import os
import re
import time
from datetime import date

import requests
from lxml import html

#常量
BASE_DIR = os.path.dirname(os.path.abspath(__file__))#当前脚本所在目录
CSV_FILE = os.path.join(BASE_DIR, "csv_data", "chengdu_weather.csv")#成都历史天气数据保存的文件
MONTH_URL = "https://www.tianqihoubao.com/lishi/chengdu/month/{year}{month:02d}.html"#成都每月历史天气页面地址
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
FIELDNAMES = ["日期", "天气状况", "气温", "风力"]#csv文件的列
MONTHS_BACK = 24#从当前月份开始往前倒推抓取的月份数
MAX_RETRY = 3#单个页面最多请求次数
DATE_PATTERN = re.compile(r"(\d{4})年(\d{2})月(\d{2})日")#页面日期形如 2024年01月01日


#生成最近 months_back 个月的(年, 月)列表，从当前月份开始往前倒推
def build_months(months_back=MONTHS_BACK, today=None):
    today = today or date.today()
    year, month = today.year, today.month
    months = []
    for _ in range(months_back):
        months.append((year, month))
        month -= 1
        if month == 0:
            year, month = year - 1, 12
    return months


#发送请求获取页面html文本，失败时最多重试 MAX_RETRY 次
def get_html(url):
    for attempt in range(1, MAX_RETRY + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            response.encoding = "utf-8"#站点页面为 utf-8 编码
            return response.text
        except requests.exceptions.RequestException as error:
            print(f"第 {attempt} 次请求失败：{url}，错误信息：{error}", flush=True)
            if attempt == MAX_RETRY:
                break
            time.sleep(2)
    return None


#清洗日期：2024年01月01日 -> 2024-01-01
def clean_date(date_text):
    match = DATE_PATTERN.search(date_text)
    if not match:
        return ""
    return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"


#解析单个月份页面的天气数据，返回[{日期, 天气状况, 气温, 风力}, ...]
def parse_month_weather(html_text):
    document = html.fromstring(html_text)
    weather_list = []
    #天气数据都在 class 为 weather-table 的表格中，每行4列：日期、天气状况(白天/夜间)、最高/最低气温、风力风向(白天/夜间)
    tr_list = document.xpath("//table[@class='weather-table']//tr[td]")
    for tr in tr_list:
        td_list = [td.xpath("normalize-space()") for td in tr.xpath("./td")]
        if len(td_list) < 4:
            continue
        #表格最后一行是"前一月/后一月"的翻页行，没有日期，需要过滤掉
        day = clean_date(td_list[0])
        if not day:
            continue
        weather_list.append({
            "日期": day,
            "天气状况": td_list[1],
            "气温": td_list[2],
            "风力": td_list[3],
        })
    return weather_list


#保存天气数据为 csv 文件
def save_to_csv(all_weather):
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()#写入表头
        writer.writerows(all_weather)


def main():
    all_weather = []
    months = build_months()
    print(f"开始抓取成都 {months[-1][0]}年{months[-1][1]:02d}月 ~ {months[0][0]}年{months[0][1]:02d}月"
          f" 共 {len(months)} 个月的历史天气...", flush=True)

    #1.遍历每个月，发送请求并解析当月天气数据
    for year, month in months:
        url = MONTH_URL.format(year=year, month=month)
        print(f"正在抓取 {year}年{month:02d}月：{url}", flush=True)
        html_text = get_html(url)
        if html_text is None:
            print(f"  {year}年{month:02d}月抓取失败，跳过该月", flush=True)
            continue
        month_weather = parse_month_weather(html_text)
        print(f"  解析到 {len(month_weather)} 条数据", flush=True)
        all_weather.extend(month_weather)
        time.sleep(1)#每个月份页面之间暂停1秒，避免请求过于频繁

    #2.按日期去重并升序排序
    weather_by_date = {item["日期"]: item for item in all_weather}
    all_weather = [weather_by_date[day] for day in sorted(weather_by_date)]
    if not all_weather:
        print("没有抓取到任何数据，请检查网络或页面结构是否变化", flush=True)
        return

    #3.保存数据为csv文件
    save_to_csv(all_weather)
    print(f"抓取完成，共 {len(all_weather)} 条数据（{all_weather[0]['日期']} ~ {all_weather[-1]['日期']}），"
          f"已保存到：{CSV_FILE}", flush=True)


if __name__ == '__main__':
    main()

