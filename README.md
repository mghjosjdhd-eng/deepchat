# deepchat —— DeepSeek 命令行聊天机器人

用 Python 写的终端 AI 聊天机器人：多轮对话、流式输出、能调用工具（calc），手写 Agent 循环。

## 快速开始

```bash
python -m venv venv && source venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env    # 填入你的 DEEPSEEK_API_KEY
python -m deepchat "用一句话解释机会成本"
```

## 功能

- 多轮对话（历史存 `.chat_history.json`，`--continue` 接着聊）
- 流式输出（逐字打印）
- calc 子命令：安全计算表达式（不用 eval）
- Agent 循环：模型自动决定调用 calc 工具（`deepchat/agent.py`）

## 技术栈

Python 3.13 / openai / python-dotenv / pytest

## 项目结构

```text
deepchat/
├── __main__.py   # CLI 入口（argparse）
├── config.py     # 环境变量与配置
├── llm.py        # DeepSeek 客户端封装（流式）
├── tools.py      # calc 工具定义
└── agent.py      # 手写 Agent 循环
tests/            # pytest 测试（全部 mock，不烧 token）
```

## 测试

```bash
pytest tests/ -v   # 全部用 mock，不烧 token
```
