# AI Coding Product Survey

本仓库用于沉淀 AI coding 头部产品调研、TRAE SOLO 产品策略分析、以及从产品经理视角评估 AI coding 产品的 LPME benchmark。

## 交付物

- 飞书在线文档：`https://my.feishu.cn/docx/GVk4d22dSo3jEXxst72cRjMfntg`
- 基础调研报告：[research/market_research_base.md](research/market_research_base.md)
- 技术 mapping 与论文路线：[research/technical_mapping.md](research/technical_mapping.md)
- 产品资料源清单：[research/sources.md](research/sources.md)
- LPME benchmark 说明：[benchmark/README.md](benchmark/README.md)
- LPME v0.1 固定测试集：[benchmark/lpme_v0.1/tasks.yml](benchmark/lpme_v0.1/tasks.yml)
- 评分 rubric：[benchmark/lpme_v0.1/scoring_rubric.md](benchmark/lpme_v0.1/scoring_rubric.md)
- 每日更新方案：[automation/daily_update_design.md](automation/daily_update_design.md)
- 每日抓取脚本：[scripts/daily_update.py](scripts/daily_update.py)

## 当前链路状态

- 飞书：已确认可以在 Chrome 登录态下打开并编辑目标文档。
- GitHub：当前本地仓库还没有 remote，且本机未安装 `gh`。需要提供 GitHub 仓库地址，或允许我在浏览器里创建仓库并推送。
- 产品实测：本机已发现 Codex CLI/App；Claude Code、Cursor、Windsurf/Devin Desktop、TRAE SOLO 尚未安装到 PATH。真正横评需要后续安装与账号/API key。
- 自动化：已先落本地脚本与 Codex 自动化方案。稳定写入飞书和群推送建议走飞书开放平台应用或群机器人 webhook。

## 调研范围

核心产品：

- OpenAI Codex
- Anthropic Claude Code
- Cursor
- TRAE SOLO
- GitHub Copilot
- Windsurf / Devin Desktop

观察型产品：

- Devin cloud agent
- Sourcegraph Amp / OpenCode / Gemini CLI 等开源或替代 agent runtime

本轮原则是只围绕头部路线做深，不做长尾工具大全。

