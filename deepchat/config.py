"""配置：读取 .env 中的 DeepSeek API Key，创建客户端。

本文件已完成——读一遍，理解「配置」和「逻辑」为什么要分开。
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# 项目根目录的 .env（config.py 在 deepchat/ 包里，向上两级才是项目根）
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

BASE_URL = "https://api.deepseek.com"
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")


def get_api_key() -> str | None:
    return os.environ.get("DEEPSEEK_API_KEY")


def get_client() -> OpenAI:
    """创建 DeepSeek 客户端（OpenAI 兼容接口，只改 base_url）。"""
    key = get_api_key()
    if not key:
        raise RuntimeError(
            "未找到 DEEPSEEK_API_KEY。请把 .env.example 复制为 .env 并填入你的 key（见手册第 01 章）"
        )
    return OpenAI(api_key=key, base_url=BASE_URL, max_retries=3)
