# PRD：PM Review Board（轻量评审看板）

## 1. 背景 / 问题
产品经理（PM）会收到大量由 AI 生成的项目产物：PRD、landing page、分析备忘录等。PM 需要一个地方快速判断：
- 哪些产物已准备好进入评审（Ready for Review）
- 哪些仍在草稿（Draft）
- 哪些因为风险未澄清而被阻塞（Blocked）

同时，PM 不希望“读代码”才能识别风险，也希望能把验收检查清单直接同步给工程团队。

## 2. 目标（Goals）
- 让 PM 在一个界面内完成：看状态 → 预览产物 → 检查风险 → 阅读评论 → 进行“Mark ready”决策。
- 让工程团队获得清晰、可复制的验收检查清单（用于 ticket）。

## 3. Scope（本期范围）
1) 任务列表按状态分组展示  
   - 至少包含：Draft、Ready for Review（可扩展示例：Blocked）

2) 产物预览区域（Artifact Preview）  
   - 预览区常驻在主页面（不使用 modal 隐藏预览）

3) 风险检查清单（Risk Checklist）  
   - 展示风险项、支持勾选/取消勾选
   - 支持“关键风险（critical）未解决 → 不允许标记 Ready”的逻辑提示
   - 至少包含一个与“customer data”相关的风险提示（来自反馈：Legal）

4) 评审评论（Reviewer Comments）  
   - 展示来自不同角色的评论（PM/Engineer/Designer/Legal）

5) “Mark ready”动作  
   - 当关键风险未清空时，提示用户先解决风险
   - 当任务处于 Blocked 时，不允许直接进入 Ready for Review

6) 导出摘要（Export Summary）  
   - 导出为纯文本文件（便于复制到 ticket/评审记录）

7) 响应式体验（Desktop + Mobile）
   - Desktop：左侧任务列表（按状态分组）+ 右侧预览/风险/评论
   - Mobile：使用状态 Tabs 切换当前状态下的任务，并纵向展示预览/风险/评论

> 交付形式：本地可打开的静态 HTML 原型（prototype/index.html），无需后端。

## 4. Non-goals（非目标）
- 真实登录/鉴权（No real authentication）
- 后端数据库 / 数据持久化（No backend database）
- 外部部署/上线（No external deployment）
- brief 之外的外部系统集成（例如：Jira/飞书/Slack/Google Drive 等）  
  > 允许“导出纯文本”作为手动复制到 ticket 的方式，但不对接任何外部 API。

## 5. 用户与使用场景
### 主要用户
产品经理（PM），需要快速做评审决策。

### 关键场景
1) PM 打开看板 → 默认看到 Draft → 选中一个任务  
2) PM 阅读预览与评论 → 检查风险清单  
3) 风险清空后 → 点击“Mark ready” → 任务进入 Ready for Review  
4) 点击“导出评审摘要” → 得到可复制到 ticket 的文本

## 6. User Stories
US-1（状态总览）：作为 PM，我想按状态看到任务列表，这样我能快速知道哪些可评审、哪些仍在草稿。  
US-2（常驻预览）：作为 PM/Designer，我想在主界面直接看到产物预览，这样不需要打开弹窗来回切换。  
US-3（风险优先）：作为 PM/Legal，我想在标记 ready 之前先看到未解决风险（尤其是 customer data），这样我不会漏掉合规风险。  
US-4（评论聚合）：作为 PM，我想看到不同角色的评论，这样我能快速收敛问题点。  
US-5（标记 ready）：作为 PM，我想在风险清空后把任务标记为 Ready for Review，这样评审流程能继续推进。  
US-6（验收可导出）：作为 Engineer，我希望验收检查能导出为 ticket 文本，这样我能直接复制使用。

## 7. Success Metrics（成功指标）
来自 brief 的指标（保持不扩展到外部埋点/系统）：
- Time to first review < 3 分钟（从打开到能做出“是否可评审”的初步判断）
- PM 不用读代码也能识别未解决风险（例如 customer data 提及）
- 工程团队拿到清晰的 acceptance checklist（通过导出摘要/验收文档）

## 8. Edge Cases（边界情况）
- 当前状态下没有任务  
  - 列表应显示“当前没有任务”
- 用户选择了任务后再切换状态 Tabs（移动端）  
  - 自动选中该状态下的第一条任务（或提示无任务）
- 关键风险未勾选时点击“Mark ready”  
  - 给出明确提示：请先完成关键风险检查
- 任务处于 Blocked 状态  
  - 不允许直接标记 Ready；提示需要先解除阻塞（在原型中仅提示，不实现解除逻辑）
- 风险勾选/取消勾选后，ready 判定需要即时刷新  
  - UI 应即时反映“当前结论”
- 导出摘要  
  - 若存在未解决风险，应在导出文本中明确列出（便于复制进 ticket）

## 9. Assumptions（假设）
- 数据为原型内置的静态示例（无后端、无持久化），演示交互逻辑即可。
- “customer data”相关风险来自合规反馈，作为关键风险项展示即可。
- “导出摘要”通过浏览器下载一个 .txt 文件实现，用户可手动复制到任何 ticket 系统。
- 目标读者是非工程 PM：文案与信息结构以“决策支持”为主，不讨论实现细节与技术栈。

