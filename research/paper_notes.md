# Paper Notes: AI Coding 深入调研

更新时间：2026-06-03

## 总判断

AI coding 的产品能力不是单纯由模型能力决定，而是由 **模型能力 × 产品能力** 共同决定。这里用乘法而不是加法，是因为任一侧短板都会把真实交付拖垮：

- 模型强但产品弱：会表现为能写出聪明片段，但拿不到正确上下文、无法运行验证、协作不可控、非工程师无法使用。
- 产品强但模型弱：可以用模板、工具、检索、验证、权限、回滚补足一部分，但上限会被推理、代码理解、多模态和长任务能力限制。
- 模型和产品都强：才会从“写代码助手”升级为“工作交付系统”。

当前模型能力仍未强到能自动补齐真实世界中的上下文、验证、协作和责任边界，所以产品能力不是外壳，而是核心能力。产品要把模型的不稳定性变成可控工作流，把模型的强项放大，把模型的弱项用界面、工具和制度补齐。

## 论文到产品的主线

### 1. RepoBench：repo 级上下文是底座，不是增值功能

RepoBench 指出传统代码 benchmark 过多集中在单文件任务，无法评估真实多文件仓库里的检索、跨文件补全和 pipeline 能力。它把 repo 级任务拆为 retrieval、completion、pipeline 三段。

产品含义：

- AI coding 产品的第一层不是 chat，而是 repo context engine。
- “索引仓库”不是技术细节，而是影响用户信任的产品能力：用户会感知到 agent 是否懂项目。
- 对非工程师用户，repo context 还要扩展为业务 context：PRD、表格、飞书文档、设计稿、用户反馈、日志。

TRAE SOLO 启示：

- Context vault 应该成为核心模块，支持代码仓、文档、表格、PPT、截图、网页、历史任务的统一上下文管理。
- LPME 不能只测最终输出，要测产品是否主动发现和组织上下文。

### 2. SWE-bench：真实 issue 让评测走出算法题，但仍只覆盖工程交付的一部分

SWE-bench 用真实 GitHub issue 和 PR 构造任务，要求模型在给定 codebase 和 issue 描述后生成 patch。它的重要性在于把评测从“写一个函数”推进到“修一个真实仓库问题”。

产品含义：

- 真实软件工程难点不只是代码生成，而是定位问题、理解现有结构、做最小修改、运行验证。
- SWE-bench 适合衡量 coding agent 的工程底座，但不能代表 PM、数据、运营、投研等角色的工作交付。
- 因为任务来自公开历史仓库，模型迭代后需要警惕 benchmark contamination。

TRAE SOLO 启示：

- SWE-bench 类任务应该作为 Code 模式的底线测试。
- TRAE 还需要 LPME：评估多角色、多产物、多协作的产品交付能力。

### 3. SWE-bench Verified：评测也需要产品化的质量控制

SWE-bench Verified 将原始 SWE-bench 过滤为 500 个经过人工验证的任务，关注问题描述是否清楚、测试 patch 是否正确、任务是否可解。

产品含义：

- “可评测”本身需要人工和流程治理。
- benchmark 样本的质量会直接影响产品路线判断；如果测试本身不可靠，团队会优化错方向。
- AI coding 产品在真实使用中也要做类似工作：判断用户需求是否清楚、验收标准是否足够、数据/代码是否能支持结论。

TRAE SOLO 启示：

- LPME 每个任务都要有 acceptance criteria，不然会沦为主观体验评价。
- 产品里可以做“需求清晰度检查”和“验收标准生成”，把 Verified 的思想前置到用户任务创建阶段。

### 4. SWE-agent：agent-computer interface 是产品能力，不是工程实现

SWE-agent 的核心贡献是 agent-computer interface。它发现让模型直接使用人类 shell/IDE 并不总是最优，给模型设计更合适的导航、查看、编辑、反馈和错误恢复接口，可以显著提升任务完成能力。

产品含义：

- 产品界面不仅服务人，也服务模型。未来每个 AI coding 产品都有两套 UX：human UX 和 agent UX。
- 好的 agent action space 应该简单、紧凑、可恢复、有反馈。
- 编辑器、terminal、browser、file viewer、test runner 不是散装工具，而是 agent harness 的组件。

TRAE SOLO 启示：

- Work/Code 模式背后要有统一 agent harness，而不是多个独立聊天入口。
- 对模型不稳定的地方，产品应给结构化工具：查文件、看引用、改小块、跑测试、截图验证、回滚。
- 三栏工作区可以进一步演化为“模型可读、用户可控”的双向界面。

### 5. Agentless：不要迷信全自治，强产品可以把问题拆成稳定流程

Agentless 用 localization、repair、patch validation 三段式解决 SWE 任务，避免让模型自由决定复杂工具调用路径。

产品含义：

- 很多任务不需要“完全自治”，反而需要产品把流程限制在高成功率路径。
- 产品设计应区分高确定性流程和开放探索流程。
- 当前模型能力有限时，workflow scaffold 比“让 agent 自己想”更可靠。

TRAE SOLO 启示：

- 面向非工程师时，不要把自由度做得过高。应该提供角色任务模板和阶段性检查点。
- LPME 评分要区分“聪明但不可控”和“朴素但稳定可交付”。

### 6. CodeAct：动作空间可以统一，但必须可解释、可回放、可审查

CodeAct 将 agent 的动作统一为可执行代码，通过代码执行与观察反馈进行多轮修正。它说明 action representation 会影响 agent 的泛化和可控性。

产品含义：

- 工具调用不是越多越好，动作空间越统一，越容易记录、复现、审查和训练。
- 可执行代码是一种强 action space，但对非工程师来说必须包装为可理解结果。

TRAE SOLO 启示：

- Code 模式可以保留 code action 透明度；Work 模式要把 action 结果翻译成业务动作。
- 所有 agent action 都应该进入 action log，用于回放、调试、评分和安全审查。

### 7. VisualWebArena：从代码到网页，视觉和交互会成为刚需

VisualWebArena 强调许多真实网页任务需要视觉信息，text-only agent 难以完成面向人类界面的任务。

产品含义：

- AI coding 的验证不能只跑测试，还要看页面、点按钮、检查布局、识别视觉 bug。
- 前端/营销/运营/PM 场景天然需要 browser agent 和视觉理解。

TRAE SOLO 启示：

- SOLO 已经支持浏览器元素选中加入对话/评论，这是正确方向。
- LPME 应加入视觉验收指标：移动端是否溢出、图表是否可读、落地页是否符合品牌、交互是否完成。

### 8. SWE-bench Multimodal：软件工程任务正在从后端 patch 扩展到视觉前端

SWE-bench Multimodal 把 SWE-bench 扩展到视觉、用户界面、JavaScript 库等任务，问题描述或测试中包含图像。

产品含义：

- 真实软件产品越来越多 bug 是视觉和交互问题，纯文本 patch benchmark 不足。
- AI coding 产品要连接 screenshot、DOM、测试、视觉 diff 和用户评论。

TRAE SOLO 启示：

- 对 TRAE 来说，前端视觉任务是天然优势区，因为 SOLO 的定位不是纯 terminal agent。
- 应把“可视化评论 -> agent 修改 -> 浏览器验证 -> 用户确认”做成一条闭环。

### 9. SWE-Gym / R2E-Gym / SWE-smith：下一阶段模型能力来自可执行环境和 verifier

SWE-Gym、R2E-Gym、SWE-smith 都在解决同一个问题：真实 SWE agent 的训练数据和可执行环境太少、太贵、太难维护。它们通过真实/合成任务、执行环境、测试、verifier、inference-time scaling 来提高模型和 agent 表现。

产品含义：

- 模型能力的下一轮提升，不只来自更大模型，还来自更好的训练环境、轨迹数据、verifier 和测试时计算。
- 产品如果能收集高质量 agent trajectory、用户反馈、失败案例、验收结果，就能反哺模型和 agent harness。
- verifier 会从技术组件变成产品组件：用户需要知道“为什么系统认为这个结果是对的”。

TRAE SOLO 启示：

- TRAE 应沉淀真实用户任务轨迹，但要做好隐私、脱敏和权限治理。
- LPME 可以作为内部 verifier 训练的任务池，而不是一次性调研材料。

### 10. SWE-rebench：公开 benchmark 会被污染，产品需要动态评测

SWE-rebench 关注任务自动采集和 decontaminated evaluation，强调用持续新鲜任务减少 benchmark contamination。

产品含义：

- “某产品在某 benchmark 上得分高”不能直接推出真实用户体验好。
- 每日/每周模型更新需要关注 benchmark 是否更新、是否污染、是否只优化固定测试。
- 产品团队需要固定测试集 + 动态新鲜任务两套评估。

TRAE SOLO 启示：

- LPME v0.1 应作为固定回归集，保证产品改版不退化。
- 同时要建立 LPME Live：每周从真实需求和公开更新中抽取新任务，防止产品只对固定 benchmark 调优。

## 结论：模型版本迭代必须纳入产品路线

模型迭代会改变产品设计的最优解：

- 当模型能力弱：产品要强 scaffold，少自由探索，多模板、多检查点。
- 当模型能力中等：产品要强化 agent harness，给模型更好的 action space、上下文和 verifier。
- 当模型能力强：产品重点转向多任务编排、协作、治理、成本控制、跨角色交付。

所以每日/每周更新不能只看产品 feature，也要看模型版本：

- 新模型是否提升长上下文和 repo 理解？
- 是否提升工具调用可靠性？
- 是否提升前端视觉理解？
- 是否降低延迟和成本，从而允许更长 agent loop？
- 是否新增可控推理、computer use、代码执行或 verifier 能力？
- 是否改变产品的默认工作流，例如从人工 approval 转向 auto-review？

对 TRAE SOLO 来说，模型能力越强，越应该往 product workbench 走；模型能力越不稳定，越要通过产品能力把不稳定性关进流程里。

