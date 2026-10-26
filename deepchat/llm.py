"""DeepSeek 调用封装：多轮对话 + 流式输出。

【练习 04-1】补全 stream_chat 的流式循环。
【练习 04-2】补全 chat 的非流式调用。
验收: pytest tests/test_llm.py -v 全绿。
"""

from .config import MODEL, get_client


def stream_chat(messages, model=MODEL, client=None):
    """流式对话：逐段 yield 文本增量。

    参数:
        messages: [{"role": "system"|"user"|"assistant", "content": str}, ...]
    用法:
        for piece in stream_chat(messages):
            print(piece, end="", flush=True)
    """
    client = client or get_client()
    # TODO(练习 04-1): 补全流式循环，3 行
    #   1. stream = client.chat.completions.create(model=model, messages=messages, stream=True)
    #   2. for chunk in stream: 遍历
    #   3. 取 delta = chunk.choices[0].delta.content，非 None 时 yield delta
    raise NotImplementedError("练习 04-1：实现流式循环，见上方注释")


def chat(messages, model=MODEL, client=None):
    """非流式对话：一次返回完整回复。"""
    client = client or get_client()
    # TODO(练习 04-2): 补全非流式调用，2 行
    #   1. resp = client.chat.completions.create(model=model, messages=messages, stream=False)
    #   2. return resp.choices[0].message.content
    raise NotImplementedError("练习 04-2：实现非流式调用，见上方注释")
