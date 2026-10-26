"""__main__ 的冒烟测试：不真的调用 API，只验证命令行能正常启动。"""

import os
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent


def test_help_exits_zero():
    env = {**os.environ, "PYTHONUTF8": "1"}  # 让子进程输出 UTF-8（手册 14 章第 1 条）
    r = subprocess.run(
        [sys.executable, "-m", "deepchat", "--help"],
        cwd=PROJECT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    assert r.returncode == 0, r.stderr
    assert "deepchat" in r.stdout
