import streamlit as st
from utils import get_chat_response

st.title("💬 智能AI助手")

with st.sidebar:
    siliconflow_api_key = st.text_input("请输入硅基流动API Key：", type="password")
    st.markdown("[获取硅基流动API key](https://siliconflow.cn/console/api-keys)")

    # 添加重试次数设置（可选）
    max_retries = st.slider("最大重试次数", 1, 5, 3)

    # 添加“新对话”按钮
    if st.button("新对话"):
        st.session_state["messages"] = [
            {"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}
        ]
        st.rerun()

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}
    ]

# 显示对话历史
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 获取用户输入
prompt = st.chat_input()
if prompt:
    if not siliconflow_api_key:
        st.info("请输入你的硅基流动API Key")
        st.stop()

    # 添加用户消息到显示列表
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    # 获取AI响应
    # 提取历史对话用于传递给API
    history = [msg for msg in st.session_state["messages"] if msg["role"] != "ai"]  # 这样可以避免将AI的回复作为历史传递
    with st.spinner("AI正在思考中，请稍等..."):
        # 将历史对话传递给API
        response = get_chat_response(prompt, siliconflow_api_key, max_retries, history)

    # 添加AI响应到显示列表
    st.session_state["messages"].append({"role": "ai", "content": response})
    st.chat_message("ai").write(response)
