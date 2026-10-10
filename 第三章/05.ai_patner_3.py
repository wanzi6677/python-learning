import streamlit as st
from openai import OpenAI
import os
from pathlib import Path


def _fix_no_proxy() -> None:
    """规整本机 no_proxy 环境变量（与 03.ai_patner_1.py 保持一致）。

    本机 no_proxy 形如 "localhost|127.*|[::1]"，既用了 "|" 分隔又带 IPv6 方括号，
    httpx 会把它整体当作一个 URL 模式解析并抛出 InvalidURL，导致 OpenAI() 构造失败。
    这里统一换成逗号分隔并忽略 IPv6 项（只影响当前进程）。
    """
    raw = os.environ.get("no_proxy", "")
    if "|" not in raw and "[" not in raw:
        return
    hosts = [item.strip() for item in raw.replace("|", ",").split(",")]
    hosts = [item for item in hosts if item and "[" not in item and "]" not in item]
    os.environ["no_proxy"] = ",".join(hosts)


_fix_no_proxy()

# 资源目录：基于脚本所在位置解析，避免从不同工作目录运行时找不到图片（与 03.ai_patner_1.py 一致）
RESOURCES_DIR = Path(__file__).resolve().parent / "resources"

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)
#大标题
st.title("AI智能伴侣")
#logo
st.logo(str(RESOURCES_DIR / "logo.png"))
#系统提示词
system_message = "你是一个 有用的AI助理"

#初始化聊天信息
if "messages" not in st.session_state:
     st.session_state.messages = []
#展示聊天信息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

#消息输入框st.session_state.messages
prompt = st.chat_input("请输入你要问的问题")
if prompt:#字符串自动转化为bool值，非空字符串为True
    st.chat_message("user").write(prompt)
    print("用户：", prompt)
    #保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    #调用大模型（stream=True 返回的是流对象 Stream，不是带 choices 的完整响应）
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_message},
            *st.session_state.messages
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )


    #输出结果(非流式)
    # print("<------------大模型返回的结果",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    #输出结果(流式)
    full_response = ""
    with st.chat_message("assistant"):          # 气泡只创建一次
        placeholder = st.empty()                # 空占位符：内容边生成边覆盖
        for chunk in response:
            if not chunk.choices:               # 收尾的用量包 choices 为空，跳过避免越界
                continue
            content = chunk.choices[0].delta.content
            if content:                         # 首个包可能只带 role，content 为 None
                full_response += content
                placeholder.markdown(full_response)

    # 保存大模型返回的结果：流式下没有 response.choices，要用累加出来的 full_response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
