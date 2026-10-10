import requests
import csv
import time
import re
from lxml import html

#常量
MOVIE_LIST_FILE= "csv_data/movie_list.csv"
TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL_1 = "https://www.themoviedb.org/movie/top-rated"#高分电影榜单地址（默认第一页）
TMDB_TOP_URL_2 = "https://www.themoviedb.org/discover/movie/items"#第二页以及后面的地址



HEADERS = {
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

#保存电影数据为 csv文件
def save_to_csv(all_movies):
    with open(MOVIE_LIST_FILE,'w',encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["电影名", "年份", "上映时间", "标签", "时长", "评分", "语言", "导演", "编剧", "slogan", "简介"])
        writer.writeheader()
        writer.writerows(all_movies)



#清洗时长：统一换算为分钟，并带上单位 m（如 1h 19m -> 79m、32m -> 32m、2h -> 120m）
def clean_runtime(runtime):
    match = re.match(r"(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?$", runtime)
    if not runtime or not match:
        return runtime
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    return f"{hours * 60 + minutes}m"


#清洗电影数据：年份去掉括号、上映时间去括号及国家、时长统一为分钟
def clean_movie_info(movie_info):
    #年份：(2026) -> 2026
    movie_info["年份"] = re.sub(r"[()（）]", "", movie_info["年份"])
    #上映时间：2026-08-25 (US) -> 2026-08-25
    movie_info["上映时间"] = re.sub(r"\s*\(.*?\)", "", movie_info["上映时间"]).strip()
    #时长：1h 19m -> 79m
    movie_info["时长"] = clean_runtime(movie_info["时长"])
    return movie_info


# 获取电影详情
def get_movie_info(movie_info_url):
    #1. 发送请求，获取电影详情，失败时最多重试 3 次
    for attempt in range(1, 4):
        try:
            response = requests.get(movie_info_url, headers=HEADERS, timeout=60)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as error:
            print(f"第 {attempt} 次请求失败：{movie_info_url}\n错误信息：{error}")
            if attempt == 3:
                return {}
            time.sleep(2)

    #2. 解析数据，获取电影详情
    movie_doc = html.fromstring(response.text)
    #电影名称
    movie_name = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")
    movie_year = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")
    movie_datas = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='release']/text()")
    movie_tags = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='genres']/a/text()")
    movie_cost_times = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='runtime']/text()")
    movie_scores = movie_doc.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")
    movie_language = movie_doc.xpath("//*[@id='media_v4']//p[strong[contains(normalize-space(.), '默认语言')]]/text()")
    movie_directors = movie_doc.xpath("//*[@id='original_header']//ol/li["
    "p[contains(@class, 'character') and contains(., 'Director')]"
    "]/p[1]/a/text()")
    movie_writer = movie_doc.xpath("//*[@id='original_header']//ol/li["
    "p[contains(@class, 'character') and "
    "(contains(., 'Writer') or contains(., 'Screenplay'))]"
    "]/p[1]/a/text()")
    movie_slogan = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/h3[1]/text()")
    movie_description = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/div/p/text()")

    # 3. 清洗数据，返回电影详情
    movie_info = {
        "电影名": movie_name[0].strip() if movie_name else '',
        "年份": movie_year[0].strip() if movie_year else '',
        "上映时间": movie_datas[0].strip() if movie_datas else '',
        "标签": ",".join(movie_tags) if movie_tags else '',
        "时长": movie_cost_times[0].strip() if movie_cost_times else '',
        "评分": movie_scores[0].strip() if movie_scores else '',
        "语言": movie_language[0].strip() if movie_language else '',
        "导演": ",".join(movie_directors) if movie_directors else '',
        "编剧": ",".join(movie_writer) if movie_writer else '',
        "slogan": movie_slogan[0].strip() if movie_slogan else '',
        "简介": movie_description[0].strip() if movie_description else '',
    }
    #4. 清洗数据后返回电影详情
    return clean_movie_info(movie_info)


def main():
    # 1.发送请求，获取高分电影榜单数据
    all_movies = []
    print("发送请求获取电影详情中...")
    for page_num in range(1,6):
        if page_num == 1:
            response = requests.get(TMDB_TOP_URL_1, headers=HEADERS, timeout=60)
        else:
            response = requests.post(TMDB_TOP_URL_2,
                                     f"air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-03-19&show_me=undefined&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400",
                                     headers=HEADERS,
                                     timeout=60)

        print(f"正在访问第{page_num}页的数据")
        # 2.解析数据，获取电影列表
        document = html.fromstring(response.text)
        movie_list = document.xpath('//div[@data-object-id and .//span[contains(@class, "release_date")]]')
        # 3.遍历电影列表，获取电影评价
        for movie in movie_list:
            movie_urls = movie.xpath('.//a[.//h2]/@href')
            if movie_urls:
                # 电影详情的url
                movie_info_url = TMDB_BASE_URL + movie_urls[0]
                print(f"发送请求 {movie_info_url}，获取电影详情中...")
                # 发送请求,获取电影详情数据
                movie_info = get_movie_info(movie_info_url)
                if movie_info:
                    all_movies.append(movie_info)

                # 每部电影之间暂停 1 秒
                time.sleep(1)


    # 4.保存数据为csv文件
    save_to_csv(all_movies)
    print("成功保存数据为csv文件")



if __name__ == '__main__':
    main()