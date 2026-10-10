import streamlit as st
from pathlib import Path

# 资源目录：基于脚本所在位置解析，避免从不同工作目录运行时找不到图片
RESOURCES_DIR = Path(__file__).resolve().parent / "resources"

# 设置页面配置项
st.set_page_config(
    page_title="原神牛逼",
    page_icon="🧊",
    layout="wide",
    #控制侧边栏状态
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://ys.mihoyo.com/',
        'Report a bug': "https://ys.mihoyo.com/",
        'About': "这是原神的streamlit测试"
    }
)

# 大标题
st.title("原神")
st.header("云原神")
st.subheader("原神.空月之歌")

# 段落文字
st.write("原神》是由中国游戏公司米哈游（miHoYo） 开发并发行的一款开放世界动作角色扮演游戏。它于2020年9月28日正式公测，自上线以来便在全球范围内取得了现象级的成功，成为中国文化产品出海的一个标杆。")
st.write("游戏的故事围绕着“旅行者”寻找失散血亲的主线展开。提瓦特大陆由七个国家组成，每个国家由一位神明统治，并对应一种元素")

# 图片
st.image(str(RESOURCES_DIR / "logo.png"), width=300)

# 音频
# st.audio()

# 视频
# st.video()

# logo
st.logo(str(RESOURCES_DIR / "img.png"))

st.divider()

# 表格
character_data = {
    "角色名称": ["温迪", "钟离", "雷电将军", "纳西妲", "芙宁娜", "玛维卡", "安娜斯塔夏"],
    "元素属性": ["风", "岩", "雷", "草", "水", "火", "冰"],
    "所属国家": ["蒙德", "璃月", "稻妻", "须弥", "枫丹", "纳塔", "至冬"],
    "武器类型": ["弓", "长柄武器", "长柄武器", "法器", "单手剑", "双手剑", "长柄武器"]
}

# 用 st.table 展示
st.table(character_data)

st.divider()

# 输入框
name = st.text_input("输入你喜欢的角色")
if name:
    st.write(f"你最喜欢的角色是{name}")

# 密码
password = st.text_input("输入你的密码", type="password")
if password:
    st.write("密码已输入（仅作演示，不会保存）")

# 单选按钮组件
gender = st.radio("请输入你的性别",["男","女","保密"])
st.write(f"你的性别为{gender}，推荐你玩原神：https://ys.mihoyo.com/")