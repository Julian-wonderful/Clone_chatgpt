import requests
import json
import time
from typing import Optional, List, Dict


def get_chat_response(prompt: str, siliconflow_api_key: str, max_retries: int = 3, history: List[Dict] = None) -> str:
    """
    向硅基流动API发送请求并获取响应。
    
    Args:
        prompt: 用户输入的提示词
        siliconflow_api_key: 硅基流动API密钥
        max_retries: 最大重试次数
        history: 包含对话历史的列表，每个元素为包含role和content的字典
    
    Returns:
        AI的回复内容
    """
    # 构造请求数据
    url = "https://api.siliconflow.cn/v1/chat/completions"

    # 构建消息列表，包含历史对话
    messages = []
    
    # 确保历史对话不为空
    if history:
        # 过滤掉无效的历史记录
        valid_history = [msg for msg in history if isinstance(msg, dict) and 'role' in msg and 'content' in msg]
        messages.extend(valid_history)
    
    # 添加当前用户消息
    messages.append({"role": "user", "content": prompt})

    # 硅基流动API的请求参数
    payload = {
        "model": "Qwen/Qwen3-Next-80B-A3B-Instruct",
        "messages": messages,
        "temperature": 0.7,
        "stream": False  # 禁用流式输出，避免可能的问题
    }

    headers = {
        "Authorization": f"Bearer {siliconflow_api_key}",
        "Content-Type": "application/json"
    }

    # 重试机制
    for attempt in range(max_retries):
        try:
            # 增加超时时间到60秒
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=60  # 增加超时时间
            )

            # 检查HTTP错误
            response.raise_for_status()

            # 解析响应
            result = response.json()

            # 检查API响应格式
            if 'choices' not in result or len(result['choices']) == 0:
                return "API响应格式错误: 没有返回有效的响应内容"

            answer = result['choices'][0]['message']['content'].strip()
            return answer

        except requests.exceptions.Timeout:
            error_msg = f"请求超时 (尝试 {attempt + 1}/{max_retries})"
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
                continue
            return error_msg

        except requests.exceptions.ConnectionError:
            error_msg = f"网络连接错误 (尝试 {attempt + 1}/{max_retries})"
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return error_msg

        except requests.exceptions.HTTPError as e:
            # 更详细的HTTP错误处理
            if response.status_code == 400:
                return f"请求参数错误 (400): 请检查API密钥和请求格式"
            elif response.status_code == 401:
                return f"未授权访问 (401): 请检查API密钥是否正确"
            elif response.status_code == 403:
                return f"访问被拒绝 (403): 请检查API密钥权限"
            elif response.status_code == 429:
                return f"请求过于频繁 (429): 请稍后重试"
            else:
                return f"HTTP错误 {response.status_code}: {str(e)}"
        except requests.exceptions.RequestException as e:
            return f"网络请求错误: {str(e)}"

        except KeyError as e:
            return f"API响应格式错误: {str(e)}"

        except Exception as e:
            return f"未知错误: {str(e)}"

    return "请求失败，请稍后重试"
