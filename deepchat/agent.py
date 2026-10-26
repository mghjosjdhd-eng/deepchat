"""手写 Agent 循环：让模型自己决定调用工具，直到给出最终回答。

【练习 05-2】补全 run_agent 的循环体。
原理（手册 05 章第 2 节的流程图）:
    1. 把「工具说明书」(JSON Schema) 一起发给模型
    2. 模型回复两种可能:
       a) 普通文字            → 结束，返回答案
       b) tool_calls 工具调用  → 执行工具，结果作为 tool 消息喂回去，回到 1
    3. 重复直到普通文字回答，或超过 max_rounds（刹车）
"""

import json

from .config import MODEL, get_client
from .tools import TOOLS


def build_tool_specs(tool_registry):
    """把工具注册表转成 OpenAI 的 tools 参数格式。已完成，读一遍。"""
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": entry.get("description", ""),
                "parameters": entry["schema"],
            },
        }
        for name, entry in tool_registry.items()
    ]


def run_agent(messages, tool_registry=TOOLS, max_rounds=5, client=None, verbose=False):
    """工具调用循环。返回 (最终回答, 完整历史)。"""
    client = client or get_client()
    history = list(messages)

    # TODO(练习 05-2): 补全循环体，约 25 行
    #   for _ in range(max_rounds):
    #     1. resp = client.chat.completions.create(model=MODEL, messages=history,
    #                                              tools=build_tool_specs(tool_registry))
    #     2. msg = resp.choices[0].message
    #     3. 若没有 msg.tool_calls: 把最终回答追加进 history 再 return msg.content, history
    #     4. 否则把 assistant 消息回填（保留 tool_calls 原样: [tc.model_dump() for tc in ...]）
    #     5. 逐个执行工具: args = json.loads(tc.function.arguments or "{}")
    #        result = tool_registry[name]["function"](**args)
    #        出错也回填: result = f"工具执行出错: {e}"
    #     6. history.append({"role": "tool", "tool_call_id": tc.id,
    #                        "content": json.dumps(result, ensure_ascii=False, default=str)})
    #     7. verbose 时打印 [tool] 名称(参数)
    #   循环结束仍未答复: return None, history
    raise NotImplementedError("练习 05-2：实现 Agent 循环，见上方注释")
