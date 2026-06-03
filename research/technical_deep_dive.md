# Technical Deep Dive: AI Coding Product Capability

更新时间：2026-06-03

## 1. 基本公式：模型能力 × 产品能力

AI coding 产品能力可以用一个简单但很有解释力的公式来理解：

> **AI Coding Product Capability = Model Capability × Product Leverage**

这里不是相加，而是相乘。原因是：

- 模型能力决定上限：推理、代码理解、长上下文、工具调用、多模态、可靠性、成本和速度。
- 产品能力决定转化率：上下文能否拿对、动作能否执行、失败能否恢复、结果能否验证、用户能否信任和协作。
- 任一侧接近 0，整体体验都会接近 0。

当前模型能力还没有强到“只靠一个输入框就能稳定交付真实工作”。所以产品能力不是外壳，而是把模型能力转化为真实交付的放大器。

## 2. 模型能力：决定产品能走多远

模型迭代需要持续追踪，不只是因为 leaderboard，而是因为它会改变产品设计空间。

### 2.1 Code reasoning

模型需要理解局部代码、跨文件依赖、调用链、框架惯例和隐藏约束。RepoBench 和 SWE-bench 说明，真实工程任务不再是单函数生成，而是 repo-level reasoning。

产品判断：

- 如果模型 repo 理解弱，产品要提供更强索引、检索、符号图和文件推荐。
- 如果模型 repo 理解强，产品可以让用户用更自然的任务表达，减少手动指定文件。

### 2.2 Tool use reliability

AI coding 产品不是只生成文本，而是要读写文件、执行命令、浏览网页、改表格、生成 PPT、调用 API、部署服务。SWE-agent 和 CodeAct 都说明 action space 的设计会显著影响 agent 表现。

产品判断：

- 工具调用不稳定时，产品要限制动作空间，提供结构化操作和回滚。
- 工具调用稳定后，产品可以从单步工具变成多步 workflow 和自动化。

### 2.3 Long-context and memory

长上下文不是简单把文件塞进去，而是要管理上下文优先级、来源、压缩和长期记忆。

产品判断：

- 长上下文弱时，产品要做 context selection 和 context compression。
- 长上下文强时，产品仍要做 provenance，否则用户无法知道结论来自哪里。

### 2.4 Multimodal understanding

VisualWebArena 和 SWE-bench Multimodal 说明，真实工作大量发生在视觉界面里：网页、图表、设计稿、截图、PPT、仪表盘。

产品判断：

- 多模态弱时，产品需要 DOM、OCR、视觉 diff、结构化截图辅助。
- 多模态强时，产品可以把“圈选/评论/截图”变成主要交互入口。

### 2.5 Cost and latency

长任务 agent 的体验受成本和延迟强约束。模型越便宜、越快、越能稳定长链路，产品越能默认开启更深验证和更多并行 agent。

产品判断：

- 高成本模型适合高价值任务和人工确认。
- 低成本模型适合背景索引、初筛、lint、轻量 reviewer、每日更新监控。

## 3. 产品能力：补足当前模型的缺口

产品能力可以分成 7 个 leverage layer。

### 3.1 Context leverage

目标：让模型拿到正确、足够、不过载的上下文。

关键能力：

- repo index、符号图、依赖图、调用链；
- 文档、表格、PPT、截图、网页、issue、聊天记录导入；
- 自动发现缺失上下文并追问；
- context provenance，标明每个结论来源；
- context compression，长任务中保留关键决策。

TRAE SOLO 产品化：

- 建立 Context Vault：项目资料、代码仓、飞书文档、数据源、历史任务、品牌规范统一管理。
- 每个任务开始前生成 Context Checklist：已有上下文、缺失上下文、假设、风险。

### 3.2 Harness leverage

目标：给模型一套适合模型使用的计算机接口。

关键能力：

- instructions / rules / memory；
- 文件查看器、结构化编辑器、命令执行器、测试执行器；
- action log、diff、checkpoint、rollback；
- tool permission policy；
- worktree / sandbox 隔离；
- agent-to-agent 分工。

TRAE SOLO 产品化：

- Work/Code 背后共享同一 agent harness。
- 非工程师看到计划、预览、风险和结果；工程师可下钻到 diff、shell、日志、测试。

### 3.3 Workflow leverage

目标：把开放任务拆成高成功率流程。

Agentless 的启示是，强 baseline 往往不是自由探索，而是稳定流程：定位、修复、验证。

TRAE SOLO 产品化：

- 角色化 workflow：PM 原型、数据分析、投研 memo、运营工具、创业 MVP。
- 每个 workflow 都有阶段门：理解任务、确认上下文、生成计划、执行、验证、交付。

### 3.4 Verification leverage

目标：让结果有证据。

关键能力：

- test、lint、typecheck、E2E、browser screenshot；
- 数据校验、公式审计、来源引用；
- visual diff、mobile layout check；
- verifier model / rule-based verifier / human review；
- 失败报告和置信度。

TRAE SOLO 产品化：

- 每个产物必须带 Validation Panel。
- 非工程师看到业务验收；工程师看到测试和日志。

### 3.5 Collaboration leverage

目标：让 agent 产物能进入组织流程。

关键能力：

- PR/issue/Jira/飞书任务；
- 评论、决策日志、变更摘要；
- 群推送和订阅；
- reviewer-specific summary；
- 多 agent command center。

TRAE SOLO 产品化：

- 飞书文档、飞书群、评论、审批和任务跟踪是国内市场的天然入口。
- “订阅每日/每周 AI coding 观察”可以作为产品工作流样板。

### 3.6 Safety leverage

目标：把模型的不确定性关进边界里。

关键能力：

- 权限分级；
- destructive action confirmation；
- secret detection；
- sandbox；
- rollback；
- audit log；
- data governance。

TRAE SOLO 产品化：

- Work 模式默认低权限，只生成方案、预览和草稿。
- Code 模式对文件写入、命令执行、部署、外发消息设置明确权限。

### 3.7 Evaluation leverage

目标：持续知道产品是否真的变强。

关键能力：

- 固定回归集：LPME v0.1；
- 动态新鲜集：LPME Live；
- 产品 telemetry：首个可用产物时间、纠错轮次、验证通过率；
- 模型版本追踪；
- 人工评分一致性。

TRAE SOLO 产品化：

- 每个版本发布前跑 LPME smoke test。
- 每周根据模型/产品更新刷新产品假设。

## 4. 技术路线的收敛方向

### 4.1 From autocomplete to issue resolution

早期产品解决的是单点效率：补全一行、解释一段、生成一个函数。

RepoBench 和 SWE-bench 代表从单文件到 repo issue 的跃迁。产品要从编辑器补全升级为能理解项目结构、定位问题、执行测试的 agent。

### 4.2 From agent to agent interface

SWE-agent 的核心不是“多调用几次模型”，而是为模型设计更合适的接口。产品上的对应物是 agent harness：模型用什么动作、收到什么反馈、如何编辑、如何恢复失败。

### 4.3 From free-form autonomy to structured workflows

Agentless 提醒我们：当前模型并不总适合无限自由行动。产品要在“自由探索”和“结构化流程”之间动态切换。

### 4.4 From text to multimodal software work

VisualWebArena 和 SWE-bench Multimodal 说明，软件工作越来越多和视觉界面绑定。对 TRAE SOLO 来说，这意味着浏览器、截图、设计稿、PPT、图表都是一等上下文。

### 4.5 From evaluation to training flywheel

SWE-Gym、R2E-Gym、SWE-smith 把评测环境变成训练环境。产品如果能沉淀真实任务轨迹和验收结果，就能形成数据飞轮：产品使用 -> 轨迹和失败案例 -> verifier/模型/工具改进 -> 更强产品。

### 4.6 From static benchmark to living benchmark

SWE-rebench 强调污染和新鲜任务。AI coding 产品的评测必须两条腿走路：固定任务保证回归可比，动态任务保证不被 leaderboard 绑架。

## 5. 对 TRAE SOLO 的架构建议

### 5.1 把 SOLO 定义为 Product Workbench

不要把 SOLO 定义为 IDE 的 agent 模式，而是定义为产品工作台：

- 用户输入的是目标和资料；
- 系统生成的是任务计划、上下文清单、可运行产物、验证证据和协作材料；
- 代码只是中间手段。

### 5.2 建立双视图

- Work View：任务目标、资料、计划、预览、评论、风险、交付。
- Code View：repo、diff、terminal、tests、logs、deployment。

双视图共享同一个 agent state，不是两个产品。

### 5.3 建立任务生命周期

每个任务都经过：

1. Intent capture：用户目标和角色。
2. Context audit：已有上下文、缺失上下文、假设。
3. Plan contract：任务计划和验收标准。
4. Execution loop：agent 执行、状态、阻塞点。
5. Verification panel：证据、测试、来源、风险。
6. Handoff package：文档、PR、导出文件、群摘要。

### 5.4 把模型迭代纳入产品发布机制

每次模型更新都要回答：

- 哪些任务可以减少产品 scaffold？
- 哪些任务可以增加自治程度？
- 哪些 verifier 可以更便宜地常开？
- 是否能扩大到新 persona 或新 artifact？
- 是否影响 LPME 分数和用户纠错轮次？

## 6. 对 LPME 的补强建议

LPME v0.2 应新增 4 类测试：

1. Model upgrade sensitivity：同一产品换模型后，任务成功率、纠错轮次、成本如何变化。
2. Context failure recovery：故意缺少关键上下文，测试产品是否追问或记录假设。
3. Long-running autonomy control：测试 auto-review、approval、rollback、checkpoint。
4. Multimodal artifact validation：测试 screenshot、UI、PPT、图表、网页视觉质量。

LPME 的核心不是给模型排名，而是给产品路线提供证据：到底应该投模型、投上下文、投工具、投验证，还是投协作工作流。

