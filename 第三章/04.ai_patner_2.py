import streamlit as st
from openai import OpenAI
import os

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
st.logo("resources/logo.png")
#系统提示词
system_message = "你是一个 有用的AI助理"

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
#展示聊天信息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

#消息输入框
prompt = st.chat_input("请输入你要问的问题")
if prompt:#字符串自动转化为bool值，非空字符串为True
    st.chat_message("user").write(prompt)
    print("用户：", prompt)
    #保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    #调用大模型（必须先拿到response，后面才能使用它）
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    #保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    #输出结果
    print("<------------大模型返回的结果",response.choices[0].message.content)
    st.chat_message("assistant").write(response.choices[0].message.content)