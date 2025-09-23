import streamlit as st
from utils import get_chat_response

st.title("💬 智能AI助手")

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}
    ]

if "conversations" not in st.session_state:
    st.session_state["conversations"] = [{"id": "1", "title": "新对话", "messages": st.session_state["messages"]}]
    st.session_state["current_conversation_id"] = "1"

# 侧边栏
with st.sidebar:
    siliconflow_api_key = st.text_input("请输入硅基流动API Key：", type="password")
    st.markdown("[获取硅基流动API key](https://siliconflow.cn/console/api-keys)")
    
    # 新对话按钮
    if st.button("➕ 新对话"):
        # 创建新对话
        new_id = str(len(st.session_state["conversations"]) + 1)
        new_conversation = {
            "id": new_id,
            "title": f"对话 {len(st.session_state['conversations']) + 1}",
            "messages": [
                {"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}
            ]
        }
        st.session_state["conversations"].append(new_conversation)
        st.session_state["current_conversation_id"] = new_id
        st.session_state["messages"] = new_conversation["messages"]
        st.rerun()
    
    # 历史对话列表
    st.markdown("### 历史对话")
    for i, conv in enumerate(st.session_state["conversations"]):
        if st.button(conv["title"], key=f"conv_{conv['id']}"):
            st.session_state["current_conversation_id"] = conv["id"]
            st.session_state["messages"] = conv["messages"]
            st.rerun()

# 显示当前对话历史
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 获取用户输入
prompt = st.chat_input()
if prompt:
    if not siliconflow_api_key:
        st.info("请输入你的硅基流动API Key")
        st.stop()

    # 添加用户消息到当前对话
    current_conv = next(conv for conv in st.session_state["conversations"] if conv["id"] == st.session_state["current_conversation_id"])
    current_conv["messages"].append({"role": "human", "content": prompt})
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    # 获取AI响应
    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(prompt, siliconflow_api_key)
    
    # 添加AI响应到当前对话
    current_conv["messages"].append({"role": "ai", "content": response})
    st.session_state["messages"].append({"role": "ai", "content": response})
    st.chat_message("ai").write(response)
    
    # 更新对话标题（如果需要）
    if len(current_conv["messages"]) == 2:  # 只有初始AI消息和用户消息
        current_conv["title"] = prompt[:20] + "..." if len(prompt) > 20 else prompt
</FILE_CONTENT>

## utils.py
```python
import requests
import json


def get_chat_response(prompt, siliconflow_api_key):
    # 构造请求数据
    url = "https://api.siliconflow.cn/v1/chat/completions"

    # 硅基流动API的请求参数
    payload = {
        "model": "Qwen/Qwen3-Next-80B-A3B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {siliconflow_api_key}",
        "Content-Type": "application/json"
    }

    try:
        # 发送POST请求到硅基流动API
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()  # 检查HTTP错误

        # 解析响应
        result = response.json()
        answer = result['choices'][0]['message']['content'].strip()

        return answer

    except requests.exceptions.RequestException as e:
        return f"网络请求错误: {str(e)}"
    except KeyError as e:
        return f"API响应格式错误: {str(e)}"
    except Exception as e:
        return f"未知错误: {str(e)}"
