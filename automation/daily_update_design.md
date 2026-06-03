# Daily Update Design

目标：每天上午 11 点检查头部 AI coding 产品更新，只有重要变化才写深度 PM 短评；无重要变化时只记录“无重大更新”，避免硬推。

## Recommendation

MVP 阶段建议用 Codex 自动化生成每日草稿，飞书写入先通过当前登录态手动/半自动粘贴。稳定阶段建议接入飞书开放平台：

1. 飞书 Docx API：把每日更新写入固定文档。
2. 飞书群机器人 webhook：把摘要和文档链接推送给订阅群。
3. GitHub 仓库：保存 benchmark、原始抓取结果和历史更新。

原因：

- 浏览器登录态适合一次性写文档，但不适合无人值守定时任务。
- 飞书 Docx API 能稳定写 block，但需要 app_id、app_secret、文档权限。
- 群机器人 webhook 推送简单，不一定需要租户管理员审批，但只能推到当前群。
- Codex 自动化适合做每日“研究员 + PM note”，比纯 Python 爬虫更能给出产品判断。

## Daily Workflow

1. 拉取 `automation/product_sources.json` 中的官方 changelog。
2. 对比 `data/daily_updates/cache.json`，只保留新增或显著变化。
3. 对每条变化打标签：
   - new_feature
   - model_update
   - workflow_update
   - enterprise_governance
   - pricing_or_plan
   - bugfix_only
4. 过滤规则：
   - 只修 bug 且无产品含义：记录但不推送。
   - 涉及新 feature、模型、agent workflow、企业治理、定价：写 PM note。
5. 生成每日 markdown：
   - 今日是否有重大更新
   - 产品逐条摘要
   - PM 短评
   - 对 TRAE SOLO 的启示
   - source links
6. 写入飞书每日更新区，并把摘要推送给订阅群。

## Weekly Workflow

每周一 11:20 生成上周复盘，和每日 11:00 更新错开：

1. 读取上一周 `data/daily_updates/*.md`。
2. 重新检查官方源，避免漏掉周末或跨时区更新。
3. 合并成一个 weekly digest：
   - 本周主要产品变化；
   - 模型版本/模型能力变化；
   - 产品能力如何补足当前模型短板；
   - 对 TRAE SOLO 的路线启示；
   - 是否调整 LPME。
4. 写入 `data/weekly_updates/`。
5. 若配置了飞书 webhook 或 App Bot 凭证，向订阅群推送短卡片。

## Feishu Requirements

需要用户提供或协助创建：

- 飞书开放平台应用的 `APP_ID` 和 `APP_SECRET`
- 目标文档授权
- 文档 token：当前链接中的 `GVk4d22dSo3jEXxst72cRjMfntg`
- 可选：订阅群的自定义机器人 webhook

环境变量建议：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_DOC_TOKEN`
- `FEISHU_BOT_WEBHOOK`
- `FEISHU_BOT_SECRET`
- `FEISHU_RECEIVE_ID`，正式 App Bot 推送目标，例如 `chat_id`
- `FEISHU_RECEIVE_ID_TYPE`，默认 `chat_id`

## Subscription Reality Check

飞书文档内放一个按钮，让任意读者点击后自动订阅同一个自定义机器人，这条链路不可直接实现。飞书自定义机器人只能用于当前群聊，同一个 custom bot 不能添加到其他群。

因此推荐：

- MVP：建立固定订阅群，在文档里放群二维码/入群链接/申请订阅表；自定义机器人只推这个群。
- 正式版：做飞书开放平台应用 bot，维护订阅表，支持个人或多群推送。

详细方案见：[feishu_subscription_plan.md](feishu_subscription_plan.md)

## Codex Automation Prompt

每日自动化可以使用以下任务描述：

> 检查本仓库 `automation/product_sources.json` 中的 AI coding 产品官方更新源，结合网络资料判断今天是否有重大产品变化。运行 `python3 scripts/daily_update.py` 生成基础抓取草稿，然后补充产品经理视角短评：这次更新改变了什么用户工作流、对 TRAE SOLO 有什么启示、是否需要加入 LPME benchmark。把结果写入 `data/daily_updates/YYYY-MM-DD.md`，若无重大更新也保留简短记录。

## Update Cadence

建议每日检查、每周汇总：

- 每日：短评，只关注重大更新；无重大更新时只记录“无重大更新”。
- 每周：趋势复盘，把碎片变化归纳成产品路线判断。

这样可以兼顾“日新月异”和“不硬推”。
