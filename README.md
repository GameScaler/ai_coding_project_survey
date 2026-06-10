# AI Coding Product Survey

本仓库用于沉淀 AI coding 头部产品调研、TRAE SOLO 产品策略分析、以及从产品经理视角评估 AI coding 产品的 LPME benchmark。

## AI 接手入口

如果把这个仓库交给另一个 Codex 或其他 AI，请先读：

- AI 代理规则：[AGENTS.md](AGENTS.md)
- 项目上下文与当前状态：[docs/AI_HANDOFF.md](docs/AI_HANDOFF.md)
- 自动化与飞书推送 runbook：[docs/OPERATIONS_RUNBOOK.md](docs/OPERATIONS_RUNBOOK.md)
- 交接模板：[docs/HANDOFF_TEMPLATE.md](docs/HANDOFF_TEMPLATE.md)
- Daily / weekly 唯一格式规范：[automation/digest_format.md](automation/digest_format.md)

最重要的基本认知：**AI coding 产品能力 = 模型能力 x 产品能力**。模型能力决定上限，但当前模型还不够稳定，产品层必须通过 context、workflow、verification、recovery、collaboration、governance 和 cost control 补足模型短板。

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
- 2026-06-04 产品实测报告：[research/product_testing_report_2026-06-04.md](research/product_testing_report_2026-06-04.md)
- 2026-06-04 实测过程文件：[data/product_tests/2026-06-04](data/product_tests/2026-06-04)、[data/product_tests/2026-06-04_round2](data/product_tests/2026-06-04_round2)
- 核心论文 PDF：[references/papers/README.md](references/papers/README.md)
- LPME benchmark 说明：[benchmark/README.md](benchmark/README.md)
- LPME v0.2 产品实测协议：[benchmark/lpme_v0.2/README.md](benchmark/lpme_v0.2/README.md)
- LPME v0.1 固定测试集：[benchmark/lpme_v0.1/tasks.yml](benchmark/lpme_v0.1/tasks.yml)
- 评分 rubric：[benchmark/lpme_v0.1/scoring_rubric.md](benchmark/lpme_v0.1/scoring_rubric.md)
- 每日更新归档：[data/daily_updates](data/daily_updates)
- 每周复盘归档：[data/weekly_updates](data/weekly_updates)
- Daily / weekly 唯一格式规范：[automation/digest_format.md](automation/digest_format.md)
- 每日更新方案：[automation/daily_update_design.md](automation/daily_update_design.md)
- 飞书订阅与机器人方案：[automation/feishu_subscription_plan.md](automation/feishu_subscription_plan.md)
- 自动化与飞书推送 runbook：[docs/OPERATIONS_RUNBOOK.md](docs/OPERATIONS_RUNBOOK.md)
- 每日抓取脚本：[scripts/daily_update.py](scripts/daily_update.py)
- 飞书机器人推送脚本：[scripts/feishu_push.py](scripts/feishu_push.py)
- 飞书开放平台 App Bot 推送脚本：[scripts/feishu_app_send.py](scripts/feishu_app_send.py)
- Feishu delivery guard：[scripts/feishu_delivery_guard.py](scripts/feishu_delivery_guard.py)
- Daily fallback generator：[scripts/generate_daily_fallback.py](scripts/generate_daily_fallback.py)
- 飞书 App Bot 群 ID 辅助脚本：[scripts/feishu_list_chats.py](scripts/feishu_list_chats.py)
- 飞书群分享链接辅助脚本：[scripts/feishu_chat_link.py](scripts/feishu_chat_link.py)
- Feishu App Bot 订阅表示例：[automation/feishu_subscribers.example.json](automation/feishu_subscribers.example.json)
- 本地环境变量示例：[.env.example](.env.example)

## 当前链路状态

- 飞书：已确认可以在 Chrome 登录态下打开并编辑目标文档。当前路线切换为正式 Feishu App Bot 优先，文档承载基线、GitHub 承载细节、`AI Coding Survey Bot` 负责订阅推送。
- GitHub：remote 已连接到 `git@github.com:GameScaler/ai_coding_project_survey.git`，调研材料可通过 GitHub 链接同步飞书。
- 产品实测：LPME v0.2 Core-3 已落地并完成 2026-06-04 两轮真机测试。当前只评价 OpenAI Codex、Claude Code、Cursor、TRAE SOLO 四个跑通产品。
- 自动化：已落本地脚本、Codex daily/weekly automation、Feishu delivery guard、macOS launchd daily fallback。Codex 深度日更优先；如果 Codex 未产出当天文件，fallback 会生成保守日更并交给 Feishu watchdog 推送。
- 每周复盘：已覆盖 2026-W01 到 2026-W23。只生成已结束完整周，不生成进行中周。

## 调研范围

核心产品：

- OpenAI Codex
- Anthropic Claude Code
- Cursor
- TRAE SOLO
- GitHub Copilot
- Windsurf / Devin Desktop
- OpenClaw
- Kimi Code
- Zhipu GLM Coding Plan / CodeGeeX

观察型产品：

- Sourcegraph Amp / OpenCode / Gemini CLI 等开源或替代 agent runtime

本轮原则是只围绕头部路线做深，不做长尾工具大全。
