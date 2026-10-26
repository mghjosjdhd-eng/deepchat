"""tools.py 的单元测试。"""

import pytest

from deepchat.agent import build_tool_specs
from deepchat.tools import TOOLS, calc


def test_calc_basic():
    assert calc("1+2") == 3
    assert calc("1000*(1+0.123)**3") == pytest.approx(1416.247867, rel=1e-9)


def test_calc_rejects_dangerous_input():
    # eval 会执行这些字符串，ast 白名单必须拒绝它们
    with pytest.raises(ValueError):
        calc("__import__('os').system('dir')")
    with pytest.raises(ValueError):
        calc("open('C:/windows/win.ini').read()")


def test_tool_specs_have_schema():
    specs = build_tool_specs(TOOLS)
    assert specs[0]["type"] == "function"
    assert specs[0]["function"]["name"] == "calc"
    assert "expression" in specs[0]["function"]["parameters"]["properties"]
    assert "expression" in specs[0]["function"]["parameters"]["required"]
