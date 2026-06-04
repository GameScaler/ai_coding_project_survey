# LPME v0.2 Product Evaluation Protocol

更新时间：2026-06-04

LPME v0.2 把 v0.1 的任务集升级为可执行的产品横评协议。核心认知不变：

**AI coding 产品能力 = 模型能力 × 产品能力**。

模型能力决定上限，但当前模型还不能稳定补齐真实世界上下文、验证、权限、回滚和协作边界；产品能力决定模型能力能否被普通用户转化为可交付 outcome。

## 本轮评分对象

本轮进入 LPME v0.2 Core-3 评分的产品：

- OpenAI Codex
- Claude Code
- Cursor
- TRAE SOLO

其他未跑通同一条 coding-agent Core-3 链路的产品保留在市场监控和日更/周更产品池里，但不进入本轮产品实测评分。

## Core-3 任务

完整 LPME v0.1 有 10 个任务。本轮真机评测先跑 Core-3，覆盖 engineering、product、data 三类最关键能力。

1. **LPME-SE-001：Unfamiliar repo bug fix**
   - 目标：修复小型 Python repo 的 failing tests，并给出验证证据。
   - 重点：repo 理解、最小修改、执行测试、风险说明。

2. **LPME-PM-001：PRD to clickable prototype**
   - 目标：把 feature brief、wireframe、用户反馈转成可点击原型、PRD 和验收测试。
   - 重点：需求理解、交互产物、非工程师可审查性、移动端体验。

3. **LPME-DS-001：Messy acquisition cohort analysis**
   - 目标：清洗混乱投放数据，生成可复现分析和业务摘要。
   - 重点：数据清洗、图表、指标歧义处理、验证与 caveat。

## 一级评分维度

总分 100，一级维度按产品 PM 视角组织。

| 一级维度 | 分数 | 评估重点 |
| --- | ---: | --- |
| Interaction | 20 | 任务定义、工作区、状态可见性、权限/确认、反馈迭代 |
| Model | 20 | 能力上限、模型多样性、模型路由、成本/延迟、弱模型适配 |
| Delivery | 30 | 上下文、执行深度、准确度、验证、交付物质量 |
| Scenario | 15 | 角色适配、模板/插件、协作交接、非工程师可用性 |
| Commercialization | 15 | 价格/plan 透明度、团队治理、额度管理、组织分发 |

## v0.1 到 v0.2 的映射

- Outcome Correctness、Execution Depth、Verification、Artifact Quality 主要归入 **Delivery**。
- Context Acquisition 同时影响 **Delivery** 与 **Interaction**。
- Controllability、Iteration Efficiency 主要归入 **Interaction**。
- Collaboration Handoff、Safety and Governance 归入 **Scenario** 与 **Commercialization**。
- Cost and Latency 扩展为 **Model** 与 **Commercialization**，因为成本既来自模型，也来自产品套餐、额度、路由和团队管理。

## 输出要求

每个产品每个任务必须保存：

- `run_notes.md`：产品版本、模型/账号状态、执行路径、阻塞点、主观体验。
- `raw_logs.txt`：可公开的运行日志，必须去除密钥、账号 token、私人信息。
- `output_artifacts/`：产品生成的代码、文档、图表或原型。
- `scorecard.yml`：按统一维度打分。

每个产品还需要一个 `product_summary.md`，说明：

- 真实可跑程度；
- 模型能力和产品能力分别贡献了什么；
- 哪些失败来自模型，哪些失败来自产品交互/权限/工作流；
- 对 TRAE SOLO 的启示。

## 评分口径

这不是模型 benchmark，因此不能只看最终答案。若产品因为登录、额度、插件入口或权限流程导致无法完成任务，也要记录为产品现实阻力；但模型不可用时，不直接假设模型能力弱，而是把分数拆到：

- **Model availability / diversity**：是否有可选模型，是否能解释模型差异；
- **Product harness**：是否能让用户把模型接入真实任务；
- **Commercial friction**：用户是否能理解 plan、额度、价格和失败原因。
