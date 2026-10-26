"""命令行聊天入口。

用法:
    python -m deepchat "用一句话解释机会成本"   # 单轮提问
    python -m deepchat --continue              # 进入交互模式并显示历史条数
    python -m deepchat --clear                 # 清空对话历史

【练习 04-3】补全 ask_once（拼消息 → 流式输出 → 追加历史）。
"""

import argparse
import json
from pathlib import Path

from .llm import stream_chat

HISTORY_FILE = Path(__file__).resolve().parent.parent / ".chat_history.json"
SYSTEM_PROMPT = "你是一个友好的编程学习助手，回答简洁、准确，用中文。"


def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []


def save_history(messages):
    HISTORY_FILE.write_text(
        json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def ask_once(prompt, history):
    """问一轮：拼 messages → 流式打印并累积 → 返回追加后的历史。

    messages 结构: [system] + history + [user 新问题]
    """
    # TODO(练习 04-3): 补全，约 12 行
    #   1. messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    #   2. messages.append({"role": "user", "content": prompt})
    #   3. reply = ""; 遍历 stream_chat(messages): print(piece, end="", flush=True); reply += piece
    #   4. 最后 print() 换行，返回 history + [user 消息, assistant 消息]
    raise NotImplementedError("练习 04-3：实现 ask_once，见上方注释")


def main():
    parser = argparse.ArgumentParser(prog="deepchat", description="DeepSeek 命令行聊天机器人")
    parser.add_argument("prompt", nargs="?", help="直接提问（省略则进入交互模式）")
    parser.add_argument("--continue", dest="cont", action="store_true", help="接着上次对话追问")
    parser.add_argument("--clear", action="store_true", help="清空对话历史")
    args = parser.parse_args()

    if args.clear:
        HISTORY_FILE.unlink(missing_ok=True)
        print("对话历史已清空")
        return

    history = load_history()
    if args.cont:
        print(f"已载入 {len(history)} 条历史消息")

    if args.prompt:
        save_history(ask_once(args.prompt, history))
    else:
        print("交互模式（输入 exit 或空行退出；--clear 清空历史）")
        while True:
            try:
                line = input("你 > ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not line or line.lower() == "exit":
                break
            history = ask_once(line, history)
        save_history(history)


if __name__ == "__main__":
    main()
