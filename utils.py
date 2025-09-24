import requests
import json


def get_chat_response(messages, siliconflow_api_key):
    # 构造请求数据
    url = "https://api.siliconflow.cn/v1/chat/completions"

    # 硅基流动API的请求参数
    payload = {
        "model": "Qwen/Qwen3-Next-80B-A3B-Instruct",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048
    }

    headers = {
        "Authorization": f"Bearer {siliconflow_api_key}",
        "Content-Type": "application/json"
    }

    try:
        # 发送POST请求到硅基流动API
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        # 检查HTTP状态码
        if response.status_code == 400:
            return f"请求参数错误 (400): {response.json().get('error', '未知错误')}"
        elif response.status_code == 401:
            return "认证失败，请检查API密钥是否正确"
        elif response.status_code == 403:
            return "权限不足，请检查API密钥权限"
        elif response.status_code == 429:
            return "请求过于频繁，请稍后重试"
        elif response.status_code != 200:
            return f"HTTP错误 {response.status_code}: {response.text}"
        
        response.raise_for_status()  # 检查HTTP错误

        # 解析响应
        result = response.json()
        
        # 检查API响应中是否有错误
        if 'error' in result:
            return f"API错误: {result['error'].get('message', '未知错误')}"
            
        answer = result['choices'][0]['message']['content'].strip()
        return answer

    except requests.exceptions.RequestException as e:
        return f"网络请求错误: {str(e)}"
    except KeyError as e:
        return f"API响应格式错误: {str(e)}"
    except Exception as e:
        return f"未知错误: {str(e)}"

