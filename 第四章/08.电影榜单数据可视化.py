#电影榜单数据可视化：读取 csv_data/movie_list.csv，用已有的 Streamlit + Altair 画 2x2 统计图
#运行方式：streamlit run 第四章/08.电影榜单数据可视化.py
import altair as alt
import pandas as pd
import streamlit as st
from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent#当前脚本所在目录
MOVIE_LIST_FILE = BASE_DIR / "csv_data" / "movie_list.csv"#原始电影数据（由 05 案例生成）
ORANGE = "#E8A33D"#参考图里的橙黄色
CHART_SIZE = 300#每个子图的高度（给饼图留出放标签的空间）
PIE_LABEL_MIN = 5#饼图只给占比 >= 5% 的扇形标百分比，更小的扇形标了会互相压住

#统计口径与 07.电影榜单数据统计.py 保持一致（这里内联，避免用 importlib 导入中文模块名）
movie_df = pd.read_csv(MOVIE_LIST_FILE, encoding="utf-8")
year_df = movie_df["年份"].value_counts().sort_index().rename_axis("年份").reset_index(name="数量")
language_df = movie_df["语言"].value_counts().rename_axis("语言").reset_index(name="数量")
genre_df = movie_df["标签"].str.split(",").explode().str.strip().value_counts().rename_axis("类型").reset_index(name="数量")
score_df = movie_df["评分"].value_counts().sort_index().rename_axis("评分").reset_index(name="数量")
score_df["占比"] = (score_df["数量"] / len(movie_df) * 100).round(1).astype(str) + "%"
#ponytail: 用空字符串占位保留行，行被删掉的话 theta 的 stack 会按子集重算，标签就和扇形错位了
score_df["占比标签"] = score_df["占比"].where(score_df["数量"] >= PIE_LABEL_MIN, "")


#统一的柱状图：x 轴按数据顺序（数量降序）排列
def bar_chart(data, field):
    return alt.Chart(data).mark_bar(color=ORANGE).encode(
        x=alt.X(f"{field}:N", sort=None, axis=alt.Axis(labelAngle=-90, title=field)),
        y=alt.Y("数量:Q", title="数量"),
        tooltip=[field, "数量"],
    ).properties(title=f"不同{field}电影数量", height=CHART_SIZE, width=380)


#不同年份电影数量：折线图（按年份升序）
year_chart = alt.Chart(year_df).mark_line(color=ORANGE).encode(
    x=alt.X("年份:N", axis=alt.Axis(labelAngle=-90, title="年份")),
    y=alt.Y("数量:Q", title="数量"),
    tooltip=["年份", "数量"],
).properties(title="不同年份电影数量", height=CHART_SIZE, width=380)

#不同评分电影数量：饼图（百分比标在扇形内部，避免放外面被裁掉、互相压住）
#ponytail: 标签半径 60 需要跟着 outerRadius 调，扇形加白色描边做分隔
pie_base = alt.Chart(score_df).encode(theta=alt.Theta("数量:Q", stack=True))
pie_chart = (pie_base.mark_arc(outerRadius=100, stroke="white", strokeWidth=1)
             .encode(color=alt.Color("评分:N", title="评分"), tooltip=["评分", "数量", "占比"])
             + pie_base.mark_text(radius=55, size=12).encode(text="占比标签:N")
             ).properties(title="不同评分电影数量", height=CHART_SIZE, width=380)

#2x2 拼成一张大屏图
dashboard = (
    (year_chart | bar_chart(language_df, "语言")) & (bar_chart(genre_df, "类型") | pie_chart)
).configure_axis(grid=True, gridColor="#DDDDDD")

st.set_page_config(page_title="TMDB电影数据统计", layout="wide")
st.title(f"TMDB-TOP{len(movie_df)}电影数据统计")
st.altair_chart(dashboard, width="stretch")


#自检：用 python 直接运行本文件时的分支（IDE 的 Run 按钮、或命令行 python 08.xxx.py 都是这条路径）
#streamlit run 启动时 st.runtime.exists() 为 True，会跳过这里
def demo():
    tag_count = movie_df["标签"].str.split(",").explode().str.strip().str.len().gt(0).sum()
    assert year_df["数量"].sum() == len(movie_df)
    assert language_df["数量"].sum() == len(movie_df)
    assert score_df["数量"].sum() == len(movie_df)
    assert genre_df["数量"].sum() == tag_count
    print(f"自检通过：电影 {len(movie_df)} 部，三个单值维度合计均为 {len(movie_df)}，类型标签共 {tag_count} 个")


if __name__ == "__main__" and not st.runtime.exists():
    #上面那些 warning 是 streamlit 在“裸跑模式”下的正常提示，不是报错
    demo()
    print("正在启动 Streamlit，稍等几秒浏览器会自动打开 http://localhost:8501 ...")
    sys.exit(subprocess.call([sys.executable, "-m", "streamlit", "run", str(Path(__file__).resolve())]))
