# ACCEPTANCE TESTS：PM Review Board

说明：以下验收测试按 User Stories 编号组织，便于工程/产品直接引用。

---

## US-1（状态总览）：任务列表按状态分组
**Given** 我打开 PM Review Board  
**When** 页面加载完成  
**Then** 我能在任务列表中看到按状态分组的任务（至少包含 Draft 与 Ready for Review 两种状态）  
**And** 每个任务条目显示：标题、状态标签、更新时间（或等价信息）  

**Given** 某个状态下没有任务  
**When** 我查看该状态分组  
**Then** 列表区域显示“当前没有任务”（或等价空态提示）  

---

## US-2（常驻预览）：预览区不隐藏在弹窗
**Given** 我在任务列表中选择任意任务  
**When** 任务被选中  
**Then** 右侧（或移动端主内容区）立即展示 Artifact Preview  
**And** 我无需打开 modal/弹窗即可看到预览内容  

---

## US-3（风险优先）：标记 Ready 前先看到未解决风险（含 customer data）
**Given** 我选择一个任务  
**When** 我查看 Risk Checklist  
**Then** 我能看到风险项列表，并能勾选/取消勾选每一项  

**Given** 风险清单中存在“customer data”相关风险项  
**When** 我查看该风险项  
**Then** 我能明确识别这是一个风险点（文案中包含 customer data 或等价提示）  

**Given** 任务存在未解决的关键风险（critical）  
**When** 我点击 “Mark ready / 标记为 Ready for Review”  
**Then** 系统提示“还有关键风险未解决”（或等价提示）  
**And** 任务状态不会变为 Ready for Review  

---

## US-4（评论聚合）：展示多角色评审评论
**Given** 我选择一个任务  
**When** 我查看 Reviewer Comments  
**Then** 我能看到来自不同角色（PM/Engineer/Designer/Legal）的评论（若有）  
**And** 每条评论至少展示：角色、优先级、评论内容  

---

## US-5（标记 ready）：风险清空后可进入 Ready for Review
**Given** 我选择一个 Draft 任务  
**And** 该任务所有关键风险（critical）都已勾选为已解决  
**When** 我点击 “Mark ready / 标记为 Ready for Review”  
**Then** 该任务状态更新为 Ready for Review  
**And** 状态标签与列表分组显示同步更新  

**Given** 我选择一个 Blocked 任务  
**When** 我点击 “Mark ready / 标记为 Ready for Review”  
**Then** 系统提示该任务被阻塞，需先解除阻塞  
**And** 状态不会变为 Ready for Review  

---

## US-6（验收可导出）：导出摘要用于 ticket
**Given** 我选择任意任务  
**When** 我点击 “Export Summary / 导出评审摘要”  
**Then** 浏览器下载一个 .txt 文本文件  
**And** 文件内容包含：任务标题、当前状态、摘要、未解决风险列表、评审评论列表  
**And** 文本可直接复制粘贴到 ticket 或评审记录中（无需系统集成）  

