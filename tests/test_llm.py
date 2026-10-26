"""llm.py 的单元测试 —— 全部用假客户端，不发真实 API 请求（不烧 token）。

假客户端的原理（手册 04 章第 4 节）:
    依赖注入 —— stream_chat/chat 接受 client 参数，测试传假货进去。
"""

from deepchat.llm import chat, stream_chat


# ---------- 假客户端（mock） ----------

class FakeDelta:
    def __init__(self, content):
        self.content = content


class FakeChunk:
    def __init__(self, content=None):
        self.choices = [FakeChoice(FakeDelta(content))] if content is not None else []


class FakeChoice:
    def __init__(self, delta):
        self.delta = delta


class FakeMessage:
    def __init__(self, content):
        self.content = content


class FakeChoiceResp:
    def __init__(self, message):
        self.message = message


class FakeResponse:
    def __init__(self, content):
        self.choices = [FakeChoiceResp(FakeMessage(content))]


class FakeClient:
    """模仿 openai.OpenAI：client.chat.completions.create(**kwargs)。"""

    def __init__(self, stream_chunks=None, reply="你好！"):
        self.stream_chunks = stream_chunks
        self.reply = reply
        self.calls = []

    @property
    def chat(self):
        return self

    @property
    def completions(self):
        return self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if kwargs.get("stream"):
            return iter(FakeChunk(c) for c in (self.stream_chunks or ["你", "好", "！"]))
        return FakeResponse(self.reply)


# ---------- 测试 ----------

def test_stream_chat_yields_deltas():
    client = FakeClient(stream_chunks=["机", "会", "成本"])
    msgs = [{"role": "user", "content": "什么是机会成本"}]
    got = "".join(stream_chat(msgs, client=client))
    assert got == "机会成本"
    # 断言把完整 messages 和 stream=True 传给了模型
    assert client.calls[0]["messages"] == msgs
    assert client.calls[0]["stream"] is True
    assert client.calls[0]["model"] == "deepseek-chat"


def test_chat_returns_full_reply():
    client = FakeClient(reply="机会成本是放弃的最高价值选项。")
    got = chat([{"role": "user", "content": "hi"}], client=client)
    assert got == "机会成本是放弃的最高价值选项。"
    assert client.calls[0]["stream"] is False
