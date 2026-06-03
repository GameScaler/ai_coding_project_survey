# LPME: Last Product Manager Examination

LPME 是一个从产品经理视角评估 AI coding 产品的 benchmark。它不是替代 SWE-bench、HumanEval 或 LHE，而是补上“真实产品交付”的评估缺口。

## Why LPME

现有 coding benchmark 主要问：模型能否修好一个 issue，或者写出正确代码。产品经理更关心另一个问题：一个 AI coding 产品能否让目标用户在真实上下文中完成可验收的工作。

AI coding 产品的第一性原理：

1. 用户要的是 outcome，不是代码本身。
2. 代码只是把意图变成可执行系统的中间表达。
3. 产品价值来自端到端工作流：理解任务、收集上下文、规划、执行、验证、交付、协作。
4. 模型能力是必要条件，但产品外壳决定真实可用性。
5. 非工程师用户不应该被迫理解 repo、terminal、diff 才能获得价值。

因此 LPME 关注的是“从人类工作目标到可用交付”的全过程。

## Personas

LPME v0.1 覆盖 9 类角色：

- Data Scientist：数据探索、建模、可视化、实验复现。
- Product Manager：PRD、原型、需求拆解、验收标准、数据口径。
- Marketing Creative：落地页、活动页、素材变体、品牌一致性。
- Operations：流程自动化、内部工具、表格清洗、状态看板。
- Sales：CRM 轻工具、客户分层、邮件/话术、跟进提醒。
- Investment Banking Analyst：公司可比、财务模型、图表、PPT 页面。
- Investment Manager：行业研究、投资 thesis、风险清单、跟踪 dashboard。
- Founder：MVP、增长实验、支付/登录/部署、演示材料。
- Software Engineer：未知仓库修复、测试、重构、PR review。

## Scenario Families

每个 persona 设计 1-2 个长期稳定任务，尽量不依赖热点资料，保证季度级别可复测。

- Build：从需求生成可运行 app / dashboard / notebook / landing page。
- Analyze：从数据、文档、网页资料生成结论和可复核依据。
- Automate：把重复流程做成脚本、任务、机器人或内部工具。
- Review：审查代码、数据、文档、结论或 PR 的可靠性。
- Ship：生成部署、发布、交付说明和协作材料。

## Metric Dimensions

LPME 每个任务按 10 个维度评分，总分 100。

1. Outcome correctness：结果是否满足目标。
2. Context acquisition：是否主动发现、组织、追问上下文。
3. Execution depth：是否真的运行、测试、验证，而不是只写方案。
4. Artifact quality：产物是否可读、可用、专业。
5. Controllability：用户能否理解和干预过程。
6. Iteration efficiency：用户反馈后能否局部修正，不重做全部。
7. Verification：是否提供测试、校验、来源、验收标准。
8. Collaboration handoff：是否能交给同事 review、复用、继续维护。
9. Safety and governance：权限、隐私、密钥、破坏性操作是否受控。
10. Cost and latency：时间、token/credit、人工纠错成本是否合理。

## Test Design Principles

- Stable over time：任务不依赖当天新闻，数据集可固定。
- Outcome-oriented：每个任务必须定义可验收产物。
- Tool-realistic：允许使用文件、shell、浏览器、表格、PPT、Git。
- Role-specific：不同角色关注不同交付标准。
- Product-sensitive：评分不仅看模型答案，也看产品交互、状态可视化、权限、回滚、协作。
- Reproducible：输入文件、任务说明、验收清单固定在仓库。

## Evaluation Protocol

1. 准备同一份任务包和输入文件。
2. 在每个产品里从新会话开始执行。
3. 记录模型/产品版本、账号计划、运行环境、耗时、花费、失败点。
4. 不做提示工程作弊，只允许一次“正常用户补充反馈”。
5. 用 rubric 独立打分，并保留产物截图、日志、PR、导出文件。
6. 形成产品 PM note：这个产品为什么成功/失败，背后是模型、工具、交互还是工作流问题。

## Versioning

- v0.1：本仓库当前版本，覆盖 10 个固定任务。
- v0.2：补齐真实样例文件、标准答案、自动化评测脚本。
- v0.3：加入多人打分和 inter-rater agreement。
- v1.0：建立公开 leaderboard 或内部长期跟踪表。

