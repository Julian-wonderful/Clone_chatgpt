import streamlit as st
from utils import get_chat_response

st.title("💬 智能AI助手")

with st.sidebar:
    siliconflow_api_key = st.text_input("请输入硅基流动API Key：", type="password")
    st.markdown("[获取硅基流动API key](https://siliconflow.cn/console/api-keys)")
    
    # 添加新对话按钮
    if st.button("🆕 新对话"):
        st.session_state["messages"] = [
            {"role": "assistant", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}
        ]
        st.session_state["conversation_title"] = "新对话"
        st.rerun()
    
    # 添加中止对话按钮
    if st.button("⏹️ 中止对话"):
        if "generating" in st.session_state and st.session_state["generating"]:
            st.session_state["generating"] = False
            st.session_state["messages"].append({"role": "assistant", "content": "对话已被用户中止。"})
            st.rerun()

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}
    ]

# 初始化对话标题
if "conversation_title" not in st.session_state:
    st.session_state["conversation_title"] = "新对话"

# 初始化生成状态
if "generating" not in st.session_state:
    st.session_state["generating"] = False

# 显示对话历史
for message in st.session_state["messages"]:
    # 转换角色名称以匹配Streamlit的期望
    role = "assistant" if message["role"] == "ai" else message["role"]
    st.chat_message(role).write(message["content"])

# 获取用户输入
prompt = st.chat_input()

if prompt:
    if not siliconflow_api_key:
        st.info("请输入你的硅基流动API Key")
        st.stop()

    # 添加用户消息到显示列表
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 准备发送给API的消息历史
    api_messages = []
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            api_messages.append({"role": "user", "content": msg["content"]})
        elif msg["role"] == "assistant" or msg["role"] == "ai":
            api_messages.append({"role": "assistant", "content": msg["content"]})
    
    # 设置生成状态为True
    st.session_state["generating"] = True
    
    # 获取AI响应
    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(api_messages, siliconflow_api_key)
    
    # 只有在生成未被中止的情况下才添加响应
    if st.session_state["generating"]:
        # 添加AI响应到显示列表
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
    
    # 重置生成状态
    st.session_state["generating"] = False

# 显示历史对话标题（简化版）
with st.sidebar:
    st.subheader("历史对话")
    # 在实际应用中，你可能想要保存多个对话并在此列出
    st.write(f"当前对话: {st.session_state['conversation_title']}")

