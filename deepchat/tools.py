"""工具函数：给聊天机器人/Agent 用的能力。

【练习 05-1】补全 calc 的三个分支（数字 / 二元运算 / 一元正负号）。
禁止用 eval() —— 用 ast 白名单语法树（见手册 05 章第 3 节）。
"""

import ast
import operator

# 白名单：只允许这些运算符
_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calc(expression: str) -> float:
    """安全地计算四则运算表达式。例: calc("1000*(1+0.123)**3") -> 1416.247867...

    原理: 把表达式解析成语法树(ast)，只允许数字和 + - * / ** 节点，其余一律报错。
    """
    tree = ast.parse(expression, mode="eval")

    def ev(node):
        # TODO(练习 05-1): 补全三个分支
        #   1. ast.Expression -> ev(node.body)
        #   2. ast.Constant 且是 int/float -> node.value
        #   3. ast.BinOp / ast.UnaryOp 且运算符在白名单 -> 用 _BINOPS 里的函数递归算
        #   4. 其他 -> raise ValueError(f"不支持的表达式: {ast.dump(node)}")
        raise NotImplementedError("练习 05-1：实现 calc 的语法树求值")

    return ev(tree)


# 工具注册表：Agent 循环（agent.py）用它生成「工具说明书」并执行工具。
# 每个工具 = {"function": 函数, "schema": 参数的 JSON Schema}
TOOLS = {
    "calc": {
        "function": calc,
        "schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "只含数字和 + - * / ** 括号的算术表达式，如 1000*(1+0.123)**3",
                },
            },
            "required": ["expression"],
        },
    },
}
