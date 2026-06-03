# AI Coding Product Survey

本仓库用于沉淀 AI coding 头部产品调研、TRAE SOLO 产品策略分析、以及从产品经理视角评估 AI coding 产品的 LPME benchmark。

## 交付物

- 飞书在线文档：`https://my.feishu.cn/docx/GVk4d22dSo3jEXxst72cRjMfntg`
- 基础调研报告：[research/market_research_base.md](research/market_research_base.md)
- 技术 mapping 与论文路线：[research/technical_mapping.md](research/technical_mapping.md)
- 技术深度分析：[research/technical_deep_dive.md](research/technical_deep_dive.md)
- 论文综述与产品启示：[research/paper_notes.md](research/paper_notes.md)
- 技术思维导图：[research/diagrams/ai_coding_capability_map.mmd](research/diagrams/ai_coding_capability_map.mmd)
- 技术思维导图图片：[research/diagrams/ai_coding_capability_map.png](research/diagrams/ai_coding_capability_map.png)
- 产品资料源清单：[research/sources.md](research/sources.md)
- 产品实测安装与准备状态：[research/product_testing_setup.md](research/product_testing_setup.md)
- 核心论文 PDF：[references/papers/README.md](references/papers/README.md)
- LPME benchmark 说明：[benchmark/README.md](benchmark/README.md)
- LPME v0.1 固定测试集：[benchmark/lpme_v0.1/tasks.yml](benchmark/lpme_v0.1/tasks.yml)
- 评分 rubric：[benchmark/lpme_v0.1/scoring_rubric.md](benchmark/lpme_v0.1/scoring_rubric.md)
- 每日更新归档：[data/daily_updates](data/daily_updates)
- 每周复盘归档：[data/weekly_updates](data/weekly_updates)
- 每日更新方案：[automation/daily_update_design.md](automation/daily_update_design.md)
- 飞书订阅与机器人方案：[automation/feishu_subscription_plan.md](automation/feishu_subscription_plan.md)
- 每日抓取脚本：[scripts/daily_update.py](scripts/daily_update.py)
- 飞书机器人推送脚本：[scripts/feishu_push.py](scripts/feishu_push.py)
- 飞书开放平台 App Bot 推送脚本：[scripts/feishu_app_send.py](scripts/feishu_app_send.py)
- 飞书 App Bot 群 ID 辅助脚本：[scripts/feishu_list_chats.py](scripts/feishu_list_chats.py)
- Feishu App Bot 订阅表示例：[automation/feishu_subscribers.example.json](automation/feishu_subscribers.example.json)
- 本地环境变量示例：[.env.example](.env.example)

## 当前链路状态

- 飞书：已确认可以在 Chrome 登录态下打开并编辑目标文档。当前路线切换为正式 Feishu App Bot 优先，文档承载基线、GitHub 承载细节、`AI Coding Survey Bot` 负责订阅推送。
- GitHub：remote 已连接到 `git@github.com:GameScaler/ai_coding_project_survey.git`，调研材料可通过 GitHub 链接回填飞书。
- 产品实测：Codex、Claude Code、Cursor、TRAE SOLO、Windsurf、GitHub Copilot App、Devin CLI 已安装或确认存在。真正横评需要后续账号登录/API key。OpenClaw 本机不可用，暂不纳入本轮实测，但进入主要产品池和公开信号监控。
- 自动化：已落本地脚本与 Codex daily/weekly automation。Feishu App Bot 已打通固定会话测试推送，脚本支持单目标推送和订阅表群发；分享文档后的订阅入口采用固定群/表单，个人订阅需要下一阶段事件回调拿到 `open_id`。
- 每周复盘：已回填 2026-W01 到 2026-W23。只生成已结束完整周，W24（2026-06-01～2026-06-07）应在 2026-06-08 后生成。

## 调研范围

核心产品：

- OpenAI Codex
- Anthropic Claude Code
- Cursor
- TRAE SOLO
- GitHub Copilot
- Windsurf / Devin Desktop
- OpenClaw

观察型产品：

- Sourcegraph Amp / OpenCode / Gemini CLI 等开源或替代 agent runtime

本轮原则是只围绕头部路线做深，不做长尾工具大全。
