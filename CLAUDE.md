# deepchat 项目说明（Claude Code 专用）

## 这是什么
DeepSeek 命令行聊天机器人 + 手写 Agent 循环（学习项目，配套手册第 04/05 章）。

## 常用命令
- 运行: python -m deepchat "问题"
- 测试: python -m pytest tests/ -q
- 环境: 复制 .env.example 为 .env 并填 DEEPSEEK_API_KEY

## 约定
- 代码注释用中文；模型交互输出用中文
- 改动任何函数后必须跑对应测试
- 不要修改 tests/ 目录（测试是练习的验收标准）
- .env 永不提交；新依赖写进 requirements.txt
- 参考答案在 AI编程学习手册/examples/deepchat/（写练习时别看）
