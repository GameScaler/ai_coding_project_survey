# AI Coding 产品实测报告：LPME v0.2 Core-3

更新时间：2026-06-04

## 结论先行

本轮只评价已经跑通 Core-3 的产品：**OpenAI Codex、Claude Code、Cursor、TRAE SOLO**。未跑通同一条 coding-agent 任务链路的产品不进入本轮评分，避免把 access/blocker 分混入真实产品能力分。

核心判断：**AI coding 产品能力 = 模型能力 × 产品能力**。模型决定能力上限；产品层决定模型能否稳定完成上下文收集、执行、验证、纠错、交付和协作。当前模型还没有强到可以裸奔，所以产品能力不是 UI 外壳，而是把模型能力转成 outcome 的乘数。

## 分数表

| 产品 | 实测状态 | Interaction | Model | Delivery | Scenario | Commercialization | 总分 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenAI Codex | Core-3 完成 | 17 | 17 | 30 | 14 | 10 | 88 |
| Cursor | Core-3 完成 | 18 | 16 | 29 | 14 | 8 | 85 |
| Claude Code | Core-3 完成，有权限/纠错摩擦 | 15 | 16 | 27 | 13 | 11 | 82 |
| TRAE SOLO | Core-3 完成，有产品重试摩擦 | 16 | 13 | 27 | 15 | 9 | 80 |

分差刻意没有拉得很大：四个产品都能完成核心任务。真正的差异不在“会不会写”，而在 **低摩擦地把任务跑完、把证据留下、把风险讲清楚**。

## 评分框架

| 维度 | 分数 | 看什么 |
| --- | ---: | --- |
| Interaction | 20 | 任务定义、工作区、状态、权限、反馈迭代是否可控 |
| Model | 20 | 能力上限、模型多样性、路由、成本/延迟、弱模型适配 |
| Delivery | 30 | 上下文、执行、准确度、验证、交付物质量 |
| Scenario | 15 | 角色适配、模板/插件、协作交接、非工程师可用性 |
| Commercialization | 15 | 价格/plan、额度、团队治理、组织分发 |

完整协议：https://github.com/GameScaler/ai_coding_project_survey/tree/main/benchmark/lpme_v0.2

## 任务完成度

| 产品 | SE bugfix | PM prototype | DS analysis | 主要摩擦 |
| --- | --- | --- | --- | --- |
| OpenAI Codex | 通过测试并生成 PR 描述 | 生成原型、PRD、验收文档 | 脚本可复跑，生成 CSV/图表/摘要 | 工程师 CLI 形态偏强，非工程师工作台不足 |
| Cursor | 通过测试并生成 PR 描述 | 原型和需求文档完整 | 数据清洗、图表、caveat 较完整 | 桌面端强，CLI/模型/成本透明度不足 |
| Claude Code | 通过测试并生成 PR 描述 | 原型、PRD、验收文档完整 | 修正一次日期解析后可复跑 | `acceptEdits` 权限摩擦、token/cost 高、数据任务有一次纠错 |
| TRAE SOLO | 通过测试并生成 PR 描述 | 重试后完成 | 重试后完成并可复跑 | PM/DS 均遇到 server error，模型路由不透明 |

## 产品读法

**OpenAI Codex：88/100。** 本轮最强的是 execution harness：本地上下文、文件编辑、命令执行、测试验证、报告交付这条链路最干净。它不是最适合非工程师的形态，但作为 agent 能力基线非常硬。

**Cursor：85/100。** Cursor 是最强 workbench 型竞品。它的优势是把 workspace、artifact、验证和审查组织成一个稳定循环；不足是桌面端可用性强于可复现自动化，模型和成本透明度仍不够。

**Claude Code：82/100。** Claude Code 的最终产物很强，适合专家型终端用户。但这次实测暴露了权限模式、预算消耗和纠错循环的摩擦：它有强工具感，却还不是低摩擦产品评测机器。

**TRAE SOLO：80/100。** TRAE SOLO 最接近多角色 workbench 方向，PM/DS 任务的产物证明 MTC 路线成立。它现在输在可靠性和透明度：server error、重试成本、UI 状态和模型路由如果不前置，会把模型能力折损掉。

## 横向判断

1. **Codex 当前最强。** 它赢在“把模型能力接到真实机器上”的完成度，模型强只是上限，真正加分的是 harness 稳。
2. **Cursor 是 TRAE SOLO 最重要的正面参照。** 它证明 AI IDE 正在变成 agent workbench，TRAE SOLO 需要在非工程师、多角色和业务产物上反超。
3. **Claude Code 是专家入口，不是大众工作台。** 透明度高，但需要把权限、预算、验证、纠错做成产品对象，才能降低 PM/运营/数据用户的使用门槛。
4. **TRAE SOLO 的方向没错，但可靠性必须先产品化。** 对非工程师来说，一次 server error 不是小 bug，而是信任断点。

## 对 TRAE SOLO 的启示

- **先补 execution depth，再放大场景。** Work 模式可以更像产品工作台，但底层必须有 Codex 级别的文件、命令、测试、证据链。
- **把模型状态变成产品状态。** 当前模型、备用模型、预计成本、额度、失败原因、是否适合长任务，都应该在任务开始前可见。
- **把验证证据产品化。** 测试结果、脚本复跑、图表生成、文件清单、caveat、回滚点应进入 UI，而不是藏在日志里。
- **把 approval 改成业务语义。** PM/数据/运营用户需要确认的是分析口径、资料权限、发布动作和交付物状态，不是 shell 命令本身。

## 过程文件

- Round 2 实测证据：https://github.com/GameScaler/ai_coding_project_survey/tree/main/data/product_tests/2026-06-04_round2
- Round 2 评分卡：https://github.com/GameScaler/ai_coding_project_survey/blob/main/data/product_tests/2026-06-04_round2/scorecards.yml
- Codex round1 evidence：https://github.com/GameScaler/ai_coding_project_survey/tree/main/data/product_tests/2026-06-04/codex
- LPME v0.2 协议：https://github.com/GameScaler/ai_coding_project_survey/tree/main/benchmark/lpme_v0.2
