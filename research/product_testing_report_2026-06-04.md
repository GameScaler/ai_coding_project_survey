# AI Coding 产品实测报告：LPME v0.2 Core-3

更新时间：2026-06-04

## 结论先行

本轮完成了 LPME v0.2 的定义与首次真机跑分。结果非常明确：

- **OpenAI Codex 是当前机器上唯一完成 Core-3 的产品**，总分 80/100。
- **Claude Code、Cursor、TRAE SOLO、Kimi Code、CodeGeeX 都进入了实机检查**，但因为登录、模型可用性或产品形态限制，未能开始 Core-3 正式任务。
- 因此本轮不能把“未登录产品”与 Codex 做最终能力排名，只能记录“当前机器可用性分”。下一轮需要用户完成账号/模型配置后复跑。

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
| OpenAI Codex | Core-3 完成 | 是 | 16 | 15 | 29 | 12 | 8 | 80 |
| Claude Code | 未登录 | 否 | 8 | 0 | 0 | 4 | 3 | 15 |
| Cursor | 未登录 / 无可用模型 | 否 | 9 | 0 | 0 | 5 | 3 | 17 |
| TRAE SOLO | UI 可打开 / 未登录 | 否 | 12 | 0 | 0 | 8 | 4 | 24 |
| Kimi Code | 已安装 / 未配置模型 | 否 | 8 | 0 | 0 | 5 | 4 | 17 |
| Zhipu GLM Coding Plan / CodeGeeX | 插件已安装 / 未登录 | 否 | 6 | 0 | 0 | 5 | 4 | 15 |

> 注：未登录产品的分数是“当前机器实测可用性分”，不是最终产品能力分。

## Codex 任务结果

### LPME-SE-001：Unfamiliar repo bug fix

- 用时：61.8s
- 结果：修复 `pricing.py`，3 个 unittest 全部通过。
- 产物：`PR_DESCRIPTION.md` 解释 root cause、fix、verification、risk。
- 评价：工程任务完成质量很高，属于可直接进入 PR review 的结果。

### LPME-PM-001：PRD to clickable prototype

- 用时：263.9s
- 结果：生成本地可打开的 `prototype/index.html`、`PRD.md`、`ACCEPTANCE_TESTS.md`。
- 亮点：覆盖 draft / ready / blocked、risk checklist、customer-data flag、export summary、comments、mobile responsive。
- 缺口：原型视觉质量只能静态检查；本地浏览器因 file URL 策略未能完成截图级验证。

### LPME-DS-001：Messy acquisition cohort analysis

- 用时：294.0s
- 结果：生成清洗脚本、cleaned CSV、channel summary、data-quality report、4 张 SVG 图和 executive summary。
- 验证：`python3 analysis/acquisition_analysis.py` 可复跑。
- 亮点：对 `social / paid_social` 合并、missing spend、zero spend revenue 做了 caveat，没有直接编造结论。

## 产品官解读

**Codex 的高分不是单纯来自模型强，而是模型能力被产品 harness 放大了。** 它能在一个 CLI 会话里读任务、改文件、跑测试、生成报告、留下日志。模型能力决定它能理解任务，产品能力决定它能把理解转化为可验证交付。

但 Codex 也暴露出两个产品缺口：

- 对非工程师来说，CLI + raw logs 仍然太工程化，缺少任务看板、artifact preview、风险面板。
- 模型/成本透明度不足。本轮三个任务分别消耗约 43k、128k、96k tokens，但产品没有把“为什么用这个模型、是否可用低成本模型、成本是否值得”解释清楚。

**TRAE SOLO 的机会** 正在这里：不要只追“能不能写代码”，而要把模型能力包装成多角色的任务工作台。Work 模式要把目标、上下文、计划、风险、产物预览、验证证据放在一起；Code 模式负责可下钻执行。

## 下一轮必做

1. 完成 Claude Code 登录/API 配置后复跑 Core-3。
2. 完成 Cursor Agent 登录/模型配置后复跑 Core-3，并特别测试 Auto-review / worktree / cloud agent。
3. 完成 TRAE SOLO 登录后，优先跑 PM 与 DS 任务，因为这是 TRAE SOLO 最应该打出差异的场景。
4. 完成 Kimi Code 默认模型配置后，测试 K2.6 对 Core-3 的表现，并记录低成本/国内模型的 token 性价比。
5. 完成 CodeGeeX / GLM Coding Plan 登录后，测试 IDE 插件是否能从“补全助手”升级为完整 workflow。

完整过程文件：https://github.com/GameScaler/ai_coding_project_survey/tree/main/data/product_tests/2026-06-04

