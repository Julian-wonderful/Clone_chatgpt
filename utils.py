import requests
import json
import time
from typing import Optional


def get_chat_response(prompt: str, siliconflow_api_key: str, max_retries: int = 3) -> str:
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

        except requests.exceptions.RequestException as e:
            return f"网络请求错误: {str(e)}"

        except KeyError as e:
            return f"API响应格式错误: {str(e)}"

        except Exception as e:
            return f"未知错误: {str(e)}"

    return "请求失败，请稍后重试"
