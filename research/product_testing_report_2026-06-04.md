# AI Coding 产品实测报告：LPME v0.2 Core-3

更新时间：2026-06-04

## 结论先行

本轮已经进入真正的产品实测，而不是只做资料调研。当前最重要的结论是：

- **Cursor：85/100，完成 Core-3，是本轮最强的完整实测产品。**
- **TRAE SOLO：79/100，完成 Core-3，但 PM/DS 都出现一次 server error 后重试成功。**
- **Kimi Code：20/100，仅为当前机器 access score，不是模型能力分；Kimi Code agent 未能暴露可用 provider/model。**
- **OpenAI Codex：上一轮已完成 Core-3，80/100；它仍是 CLI/headless agent 的强基线。**
- **Claude Code：已安装 `2.1.161`，但当前未登录；下一步登录后复跑同一套 Core-3。**

最核心的产品判断没有变：**AI coding 产品能力 = 模型能力 × 产品能力**。模型决定能力上限，但当前模型还不够稳定，所以产品必须补上 context、workflow、verification、权限、回滚、协作和成本透明度。用户最终购买的不是“会写代码的模型”，而是“能把意图变成可验收 outcome 的产品系统”。

## 评分框架

LPME v0.2 将产品评测拆成 5 个一级维度：

| 维度 | 分数 | 关键问题 |
| --- | ---: | --- |
| Interaction | 20 | 任务定义、工作区、状态、权限、反馈迭代是否可控 |
| Model | 20 | 能力上限、模型多样性、路由、成本/延迟、弱模型适配 |
| Delivery | 30 | 上下文、执行、准确度、验证、交付物质量 |
| Scenario | 15 | 角色适配、模板/插件、协作交接、非工程师可用性 |
| Commercialization | 15 | 价格/plan、额度、团队治理、组织分发 |

完整协议：https://github.com/GameScaler/ai_coding_project_survey/tree/main/benchmark/lpme_v0.2

## 分数表

| 产品 | 实测状态 | 是否可比 | Interaction | Model | Delivery | Scenario | Commercialization | 总分 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Cursor | Core-3 完成 | 是 | 18 | 16 | 29 | 14 | 8 | 85 |
| OpenAI Codex | Core-3 完成 | 是 | 16 | 15 | 29 | 12 | 8 | 80 |
| TRAE SOLO | Core-3 完成，PM/DS 各重试一次 | 是 | 16 | 13 | 27 | 15 | 8 | 79 |
| Kimi Code | provider/model entitlement 阻塞 | 否 | 10 | 2 | 0 | 5 | 3 | 20 |
| Claude Code | 已安装，未登录 | 否 | 8 | 0 | 0 | 4 | 3 | 15 |
| Zhipu GLM Coding Plan / CodeGeeX | 待登录/待跑 | 否 | 6 | 0 | 0 | 5 | 4 | 15 |

> 注：Kimi、Claude Code、CodeGeeX 当前不是最终产品能力排名。它们的分数是“当前机器可用性/access 分”，等账号、模型和插件链路打通后必须复跑。

## Cursor 实测

### LPME-SE-001：Unfamiliar repo bug fix

- 结果：修复 `pricing.py`，生成 `PR_DESCRIPTION.md`。
- 验证：`python3 -m unittest discover -s tests -v`，3 个测试全部通过。
- PM 读法：工程交付质量强，修复最小化，PR handoff 清楚。

### LPME-PM-001：PRD to clickable prototype

- 结果：生成 `prototype/index.html`、`PRD.md`、`ACCEPTANCE_TESTS.md`。
- 覆盖：draft / ready / blocked、risk checklist、customer-data/PII 信号、Mark ready、export、responsive CSS。
- PM 读法：Cursor 不只是写代码，而是能把需求、风险、验收和原型组织成可审查 artifact。

### LPME-DS-001：Messy acquisition cohort analysis

- 结果：生成可复跑分析脚本、cleaned CSV、daily/channel metrics、data-quality log、4 张图和 executive summary。
- 验证：`python3 analysis/acquisition_analysis.py` 可复跑。
- PM 读法：最强点是 caveat 处理：没有把 missing spend 当 0，也没有忽略 `social / paid_social` 的口径问题。

### 产品官短评

Cursor 的领先点是 workbench loop：读 workspace、改文件、生成多类型 artifact、做验证、留下可审查证据。它的不足也很清楚：桌面端可用，但 CLI agent 当前没有登录/模型状态；模型选择、成本和自动化复现不够透明。

## TRAE SOLO 实测

### LPME-SE-001：Unfamiliar repo bug fix

- 结果：修复 `pricing.py`，生成 `PR_DESCRIPTION.md`。
- 验证：`python3 -m unittest discover -s tests -v`，3 个测试全部通过。
- PM 读法：说明 TRAE SOLO 不只是“场景入口”，底层也能完成基础工程任务。

### LPME-PM-001：PRD to clickable prototype

- 结果：第一次 server error `(-1)`；重试后成功，UI 显示成功 run 用时 4m42s。
- 产物：`prototype/index.html`、`PRD.md`、`ACCEPTANCE_TESTS.md`。
- 覆盖：draft / ready / blocked、risk checklist、Ready for Review、导出评审摘要、响应式布局。
- PM 读法：产物方向很对，明显比纯 CLI 更贴近非工程师工作台；但一次失败已经足够影响信任。

### LPME-DS-001：Messy acquisition cohort analysis

- 结果：第一次 server error `(-1)`；重试后成功，UI 显示成功 run 用时 3m58s。
- 产物：可复跑分析脚本、cleaned CSV、channel summary、4 张图、executive summary。
- 验证：`python3 analysis/acquisition_analysis.py` 可复跑。
- PM 读法：最终交付可用，但 UI completion 状态与本地文件出现有滞后。对数据任务来说，用户需要更清楚地知道“现在到底跑完了吗、哪些文件可信、验证是否通过”。

### 产品官短评

TRAE SOLO 的机会不在“比 Cursor 更会写代码”，而在把 agent 能力产品化成多角色 workbench。它已经更接近这个方向：MTC、场景化入口、本地 workspace、PM/DS artifact 都是正确信号。但可靠性必须提升，否则模型能力会被产品层损耗掉。

## Kimi Code 实测

- Kimi desktop chat 已登录，并能看到 K2.6 Fast。
- Kimi Work 页面没有进入可运行 coding workspace。
- Kimi Code CLI 版本：`0.9.0`。
- `kimi provider list` 返回 `No providers configured`。
- 登录/权益校验没有解锁 coding-agent 执行。

### 产品官短评

这里不能说“Kimi 模型弱”，只能说“Kimi Code 的产品链路在当前账号不可用”。这正好说明 LPME 为什么要把 Model 和 Product 分开评分：模型能力再强，如果 provider、会员权益、workspace 或 CLI 配置不能把模型接到真实任务里，用户侧得到的产品能力就是 0。

## 横向判断

### 1. Cursor 暂时是完整 workbench 标杆

Cursor 的核心能力已经从 IDE 补全进化到“任务执行 + 文件产物 + 验证证据”。这对 TRAE SOLO 最关键的启发是：不要只做聊天，也不要只做编辑器；要把 agent 的过程和结果组织成工作台。

### 2. TRAE SOLO 的差异化在非工程师工作流

TRAE SOLO 这轮不是输在场景，而是输在稳定性和透明度。它的 PM/DS 产物证明方向成立，但 server error、重试、UI 状态滞后会让真实用户不敢把长任务交给它。

### 3. Kimi 暴露的是国内产品常见的 access/plan 问题

国内模型和产品可能有成本、合规、本地生态优势，但如果用户搞不清“我到底有没有 coding-agent 权益、当前用哪个模型、为什么不能跑”，产品能力就被商业化/账号系统吃掉。

### 4. Codex 仍是强执行基线

Codex 的强项是 headless execution：读文件、改代码、跑命令、写报告。它不够非工程师，但作为 agent harness 基线很重要。TRAE SOLO 需要学习它的执行深度，而不是复制它的 CLI 形态。

## 对 TRAE SOLO 的产品建议

1. **把可靠性当成产品功能。** 每次 server error 都要有失败阶段、可恢复动作、已修改文件、是否安全重试、是否消耗额度的说明。
2. **把模型状态前置。** 用户开始任务前应该知道当前模型、可选模型、额度、预计成本、是否适合长任务。
3. **把验证证据产品化。** 测试结果、脚本复跑、图表生成、文件清单、失败 caveat 都应该在 UI 里可见。
4. **把 approval 从命令确认改成业务确认。** PM/运营/数据用户关心的是是否允许访问资料、是否采用分析口径、是否发布 artifact，不是 shell 命令本身。
5. **把 LPME 变成回归测试。** 每次模型或产品版本更新后，用同一套 Core-3 看分数是否真的提升，而不是只看 demo。

## 过程文件

- Round 2 实测证据：https://github.com/GameScaler/ai_coding_project_survey/tree/main/data/product_tests/2026-06-04_round2
- Round 2 评分卡：https://github.com/GameScaler/ai_coding_project_survey/blob/main/data/product_tests/2026-06-04_round2/scorecards.yml
- LPME v0.2 协议：https://github.com/GameScaler/ai_coding_project_survey/tree/main/benchmark/lpme_v0.2
