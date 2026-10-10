#电影榜单数据统计：读取 05 案例抓取的 csv 数据，输出四张汇总表（年份/语言/类型/评分）
#说明：本脚本只做本地数据统计，不发送任何网络请求，也不依赖 matplotlib、tabulate 等额外三方库
import pandas as pd
from pathlib import Path

#常量
BASE_DIR = Path(__file__).resolve().parent#当前脚本所在目录
CSV_DATA_DIR = BASE_DIR / "csv_data"#数据目录
MOVIE_LIST_FILE = CSV_DATA_DIR / "movie_list.csv"#原始电影数据（由 05 案例生成）

#四张汇总表的保存路径
YEAR_STAT_FILE = CSV_DATA_DIR / "movie_stat_by_year.csv"
LANGUAGE_STAT_FILE = CSV_DATA_DIR / "movie_stat_by_language.csv"
GENRE_STAT_FILE = CSV_DATA_DIR / "movie_stat_by_genre.csv"
SCORE_STAT_FILE = CSV_DATA_DIR / "movie_stat_by_score.csv"
MARKDOWN_FILE = CSV_DATA_DIR / "movie_statistics.md"#四张表的 Markdown 汇总文件

#原始数据需要包含的字段
MOVIE_FIELDS = ["电影名", "年份", "上映时间", "标签", "时长", "评分", "语言", "导演", "编剧", "slogan", "简介"]

#统计时用到的字段名与表头
FIELD_YEAR = "年份"
FIELD_LANGUAGE = "语言"
FIELD_TAG = "标签"
FIELD_SCORE = "评分"
GENRE_LABEL = "类型"#标签拆分后每一类的名称（对应原数据里的“标签”字段）
COUNT_COLUMN = "电影数量"
RATIO_COLUMN = "占比(%)"

#类型表的占比说明：一部电影可能有多个标签，占比分母用“标签出现总次数”而不是电影总数
GENRE_NOTE = "占比分母为标签出现总次数（一部电影可有多个标签，因此数量会大于电影总数，占比合计 100%）"


#读取电影数据，并校验字段是否齐全
def load_movie_data(file_path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"未找到原始数据文件：{file_path}\n请先运行 05.网络机器人-案例-电影榜单1.py 抓取数据")

    #05 案例用 utf-8 写入，这里同样用 utf-8 读取
    movie_df: pd.DataFrame = pd.read_csv(file_path, encoding="utf-8")

    missing_fields = [field for field in MOVIE_FIELDS if field not in movie_df.columns]
    if missing_fields:
        raise ValueError(f"原始数据缺少字段：{'、'.join(missing_fields)}")
    return movie_df


#把 value_counts 的结果转换成 [标签, 电影数量, 占比(%)] 三列的统计表
def build_count_table(count_series, label_name, total_count):
    stat_df = count_series.rename_axis(label_name).reset_index(name=COUNT_COLUMN)
    stat_df[RATIO_COLUMN] = (stat_df[COUNT_COLUMN] / total_count * 100).round(2)
    return stat_df


#按数量降序排序；数量相同时按名称升序，保证多次运行结果完全一致
def sort_by_count(stat_df, label_name):
    stat_df = stat_df.sort_values([COUNT_COLUMN, label_name], ascending=[False, True])
    return stat_df.reset_index(drop=True)


#不同年份电影数量：按年份升序，方便看时间趋势
def build_year_table(movie_df):
    year_counts = movie_df[FIELD_YEAR].dropna().value_counts().sort_index()
    return build_count_table(year_counts, FIELD_YEAR, len(movie_df))


#不同语言电影数量：按数量降序
def build_language_table(movie_df):
    language_counts = movie_df[FIELD_LANGUAGE].dropna().value_counts()
    stat_df = build_count_table(language_counts, FIELD_LANGUAGE, len(movie_df))
    return sort_by_count(stat_df, FIELD_LANGUAGE)


#不同标签电影数量：一个电影有多个标签，先按逗号拆分再统计
def build_genre_table(movie_df):
    tag_series = movie_df[FIELD_TAG].dropna().str.split(",").explode().str.strip()
    tag_series = tag_series[tag_series != ""]#去掉拆分后产生的空标签

    genre_total = len(tag_series)#标签出现总次数，作为占比分母
    genre_counts = tag_series.value_counts()
    stat_df = build_count_table(genre_counts, GENRE_LABEL, genre_total)
    return sort_by_count(stat_df, GENRE_LABEL), genre_total


#不同评分电影数量：按评分升序
def build_score_table(movie_df):
    score_counts = movie_df[FIELD_SCORE].dropna().value_counts().sort_index()
    return build_count_table(score_counts, FIELD_SCORE, len(movie_df))


#把统计表转换成 Markdown 文本（手写生成，避免依赖未安装的 tabulate 库）
def to_markdown_table(stat_df, title, note=""):
    lines = [f"## {title}", ""]
    if note:
        lines.append(f"> {note}")
        lines.append("")

    headers = list(stat_df.columns)
    lines.append("| " + " | ".join(headers) + " |")
    #第一列（名称）左对齐，数字列右对齐
    lines.append("| " + " | ".join([":---"] + ["---:"] * (len(headers) - 1)) + " |")
    for row in stat_df.itertuples(index=False):
        #占比统一显示两位小数，避免出现 38.0 与 22.44 这种混排
        cells = [f"{value:.2f}" if header == RATIO_COLUMN else str(value)
                 for header, value in zip(headers, row)]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


#打印并保存单张统计表：csv 用 utf-8-sig 编码，方便直接用 Excel 打开
def save_table(stat_df, title, file_path, note=""):
    stat_df.to_csv(file_path, index=False, encoding="utf-8-sig")
    markdown = to_markdown_table(stat_df, title, note)
    print(markdown)
    print(f"已保存：{file_path}\n")
    return markdown


#校验单张表的数量合计是否符合预期
def check_total(stat_df, expected, table_name):
    total = int(stat_df[COUNT_COLUMN].sum())
    if total == expected:
        print(f"[校验通过] {table_name}表数量合计 = {total}")
    else:
        print(f"[警告] {table_name}表数量合计 = {total}，与预期 {expected} 不一致，请检查原始数据")


#保存四张表的 Markdown 汇总文件
def save_markdown(sections, movie_count, genre_total, file_path):
    lines = [
        "# TMDB 高分电影榜单数据统计",
        "",
        f"- 数据来源：{MOVIE_LIST_FILE.name}",
        f"- 电影总数：{movie_count} 部",
        f"- 年份 / 语言 / 评分三张表的占比分母：{movie_count}（各表占比合计 100%）",
        f"- 类型表的占比分母：{genre_total}（标签出现总次数，占比合计 100%）",
        "",
    ]
    lines.extend(sections)
    file_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    #1. 读取原始数据
    movie_df = load_movie_data(MOVIE_LIST_FILE)
    print(f"读取电影数据成功，共 {len(movie_df)} 部电影\n")

    #2. 分别在四个维度上做统计
    year_table = build_year_table(movie_df)
    language_table = build_language_table(movie_df)
    genre_table, genre_total = build_genre_table(movie_df)
    score_table = build_score_table(movie_df)

    #3. 打印并保存四张统计表
    sections = [
        save_table(year_table, "不同年份电影数量", YEAR_STAT_FILE),
        save_table(language_table, "不同语言电影数量", LANGUAGE_STAT_FILE),
        save_table(genre_table, f"不同{GENRE_LABEL}电影数量", GENRE_STAT_FILE, GENRE_NOTE),
        save_table(score_table, "不同评分电影数量", SCORE_STAT_FILE),
    ]

    #4. 校验合计：三个单值维度的合计应等于电影总数，标签维度应等于标签出现总次数
    check_total(year_table, len(movie_df), FIELD_YEAR)
    check_total(language_table, len(movie_df), FIELD_LANGUAGE)
    check_total(genre_table, genre_total, GENRE_LABEL)
    check_total(score_table, len(movie_df), FIELD_SCORE)

    #5. 保存 Markdown 汇总文件
    save_markdown(sections, len(movie_df), genre_total, MARKDOWN_FILE)
    print(f"\n已保存 Markdown 汇总文件：{MARKDOWN_FILE}")


if __name__ == '__main__':
    main()
