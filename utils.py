import requests
import json


def get_chat_response(prompt, siliconflow_api_key):
    # 构造请求数据
    url = "https://api.siliconflow.cn/v1/chat/completions"

    # 硅基流动API的请求参数
    payload = {
        "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
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

