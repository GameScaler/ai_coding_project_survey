# LPME v0.2 Scoring Rubric

每个产品总分 100。Core-3 任务分数按任务平均，产品级体验分按实测过程修正。

## 1. Interaction, 20 pts

- **Task definition, 5**：能否帮助用户澄清目标、约束、非目标和验收标准。
- **Workspace and state, 5**：是否清楚展示计划、文件、diff、任务状态、阻塞点和下一步。
- **Controllability, 5**：权限、命令执行、危险操作、回滚、人工确认是否可理解。
- **Iteration loop, 5**：用户补充反馈后是否能局部修改，不重做、不引入回归。

## 2. Model, 20 pts

- **Capability ceiling, 7**：默认/最强模型是否能处理 repo、数据、产品需求和复杂推理。
- **Model diversity and routing, 5**：是否支持多模型、多 provider、BYOK、弱模型/低成本模型，并能解释适用场景。
- **Cost and latency, 5**：响应速度、长任务成本、token/credit 可见性和性价比。
- **Model-product coupling, 3**：模型升级是否真的改变 workflow，例如更长自治、更少确认、更强 verifier，而不是只多一个 model picker。

## 3. Delivery, 30 pts

- **Outcome correctness, 8**：是否完成任务目标和关键边界条件。
- **Context acquisition, 6**：是否主动读取文件、发现缺口、记录假设。
- **Execution depth, 6**：是否真实运行、修改、测试、生成文件，而不是只写方案。
- **Verification, 6**：是否提供测试、数据校验、截图、来源或验收证据。
- **Artifact quality, 4**：交付物是否专业、清晰、可复用。

## 4. Scenario, 15 pts

- **Role fit, 5**：是否适合 PM、数据、运营、投研、工程师等目标角色，而不是只适合开发者。
- **Templates and plugins, 4**：是否提供场景模板、插件、工具集成、MCP/ACP/IDE 扩展。
- **Collaboration handoff, 4**：是否能生成 PRD、PR 描述、决策日志、同事 review 摘要。
- **Non-engineer usability, 2**：非工程师是否能理解结果、风险和下一步。

## 5. Commercialization, 15 pts

- **Plan transparency, 5**：价格、额度、模型可用性、失败原因是否清楚。
- **Team governance, 4**：团队配置、权限、审计、安全策略是否可管理。
- **Distribution, 3**：是否容易进入组织工作流，例如 IDE、GitHub、飞书、企业账号。
- **Scalability, 3**：多任务、多 agent、长任务、云端/本地协同是否可扩展。

## Score Bands

- **90-100**：可用于真实业务，产品和模型共同形成强闭环。
- **75-89**：主线可用，有少量产品摩擦或模型补救成本。
- **60-74**：部分任务可用，但需要明显人工兜底。
- **40-59**：只能作为草稿工具或单点助手。
- **0-39**：无法完成核心任务，或登录/额度/权限/安全问题严重阻断。

