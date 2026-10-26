"""agent.py 的工具循环测试 —— 假模型第一次回复工具调用，第二次回复最终答案。"""

import json

from deepchat.agent import run_agent
from deepchat.tools import TOOLS


class FakeFunc:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class FakeTC:
    def __init__(self, id_, name, arguments):
        self.id = id_
        self.function = FakeFunc(name, arguments)

    def model_dump(self):
        return {
            "id": self.id,
            "function": {"name": self.function.name, "arguments": self.function.arguments},
        }


class FakeToolMessage:
    def __init__(self, content=None, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls


class FakeAgentResponse:
    def __init__(self, msg):
        self.choices = [FakeAgentChoice(msg)]


class FakeAgentChoice:
    def __init__(self, msg):
        self.message = msg


class FakeAgentClient:
    """每次 create 弹出一个预先准备好的回复。"""

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    @property
    def chat(self):
        return self

    @property
    def completions(self):
        return self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return FakeAgentResponse(self.replies.pop(0))


def test_run_agent_uses_tool_then_answers():
    call = FakeTC("call_1", "calc", json.dumps({"expression": "1+2"}))
    client = FakeAgentClient(
        [
            FakeToolMessage(tool_calls=[call]),          # 第一轮：模型要调工具
            FakeToolMessage(content="结果是 3。"),         # 第二轮：最终回答
        ]
    )
    answer, history = run_agent(
        [{"role": "user", "content": "帮我算 1+2"}],
        TOOLS,
        client=client,
    )
    assert answer == "结果是 3。"
    roles = [h["role"] for h in history]
    assert roles == ["user", "assistant", "tool", "assistant"]
    # tool 消息里应包含工具执行结果 3
    assert json.loads(history[2]["content"]) == 3
    # 工具说明书随请求一起发出
    assert client.calls[0]["tools"][0]["function"]["name"] == "calc"


def test_run_agent_passes_tool_error_back_to_model():
    # 模型调用不存在的工具 → 回填错误文本而不是崩溃 → 模型给出最终回答
    call = FakeTC("call_1", "no_such_tool", json.dumps({}))
    client = FakeAgentClient(
        [
            FakeToolMessage(tool_calls=[call]),
            FakeToolMessage(content="抱歉，那个工具用不了。"),
        ]
    )
    answer, history = run_agent([{"role": "user", "content": "调用不存在的工具"}], TOOLS, client=client)
    assert answer == "抱歉，那个工具用不了。"
    assert "工具执行出错" in history[2]["content"]
