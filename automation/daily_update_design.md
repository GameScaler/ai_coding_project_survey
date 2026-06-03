# Daily Update Design

目标：每天上午 11 点检查头部 AI coding 产品更新，只有重要变化才写深度 PM 短评；无重要变化时只记录“无重大更新”，避免硬推。

## Recommendation

当前直接采用正式 Feishu App Bot 路线。Codex 自动化负责每日/每周研究和 digest 生成；`AI Coding Survey Bot` 负责订阅推送；飞书文档继续承载提炼后的结论和长期基线。

1. 飞书 Docx API：把每日更新写入固定文档。
2. Feishu App Bot：按订阅表把摘要和文档链接推送到个人或群。
3. GitHub 仓库：保存 benchmark、原始抓取结果和历史更新。

原因：

- 浏览器登录态适合一次性写文档，但不适合无人值守定时任务。
- 飞书 Docx API 能稳定写 block，但需要 app_id、app_secret、文档权限。
- App Bot 支持真正的订阅管理：个人/群、多频率、退订、交互式卡片。
- 群自定义机器人只作为 fallback，不作为主路线。
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
5. 若配置了 Feishu App Bot 凭证和订阅表，向订阅对象推送短卡片。

周复盘只处理已经结束的完整自然周，不写进行中周，也不保留 `Wxx-in-progress` 文件。标题格式固定为 `2026-W23（2026-05-25～2026-05-31）`。例如 W24 对应 `2026-06-01～2026-06-07`，应在 2026-06-08 之后生成和推送。

2026 年历史周复盘已经回填到 `data/weekly_updates/2026-W01.md` 至 `2026-W23.md`，后续自动化只需要按周追加。

## Feishu Requirements

需要用户提供或协助创建：

- 飞书开放平台应用的 `APP_ID` 和 `APP_SECRET`
- 目标文档授权
- 文档 token：当前链接中的 `GVk4d22dSo3jEXxst72cRjMfntg`
- 可选 fallback：订阅群的自定义机器人 webhook

环境变量建议：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_DOC_TOKEN`
- `FEISHU_RECEIVE_ID`，正式 App Bot 推送目标，例如 `chat_id`
- `FEISHU_RECEIVE_ID_TYPE`，默认 `chat_id`
- `FEISHU_SUBSCRIBER_FILE`，可选，默认可用 `automation/feishu_subscribers.local.json`

不建议把 secret 写入仓库、飞书文档或 automation prompt。用本地 shell、Codex automation secret 或部署平台 secret 管理。

如果应用机器人已经加入目标订阅群，可以运行 `scripts/feishu_list_chats.py` 列出 bot 可见的群聊，拿到 `chat_id` 后填入 `FEISHU_RECEIVE_ID` 或订阅表。

## Subscription Reality Check

飞书文档内放一个按钮，让任意读者点击后自动订阅同一个自定义机器人，这条链路不可直接实现。飞书自定义机器人只能用于当前群聊，同一个 custom bot 不能添加到其他群。

因此当前推荐：

- 主路线：做飞书开放平台应用 bot，维护订阅表，支持个人或多群推送。
- 当前入口：分享文档时放固定订阅群链接/二维码或订阅表；读者加入群或填表后，由后台把 `chat_id/open_id/email` 写入订阅表。
- 新群订阅：群管理员需要主动把 `AI Coding Survey Bot` 添加到群里，自动化拿到该群 `chat_id` 后才能推送。
- fallback：如果 App Bot 权限审批卡住，再临时建立固定订阅群，用自定义机器人 webhook 推送。

详细方案见：[feishu_subscription_plan.md](feishu_subscription_plan.md)

## Codex Automation Prompt

每日自动化可以使用以下任务描述：

> 检查本仓库 `automation/product_sources.json` 中的 AI coding 产品官方更新源，结合网络资料判断今天是否有重大产品变化。运行 `python3 scripts/daily_update.py` 生成基础抓取草稿，然后补充产品经理视角短评：这次更新改变了什么用户工作流、对 TRAE SOLO 有什么启示、是否需要加入 LPME benchmark。把结果写入 `data/daily_updates/YYYY-MM-DD.md`，若无重大更新也保留简短记录。

每周自动化补充要求：

> 只复盘上一个已经结束的周一到周日周期，不生成进行中周，不创建 `Wxx-in-progress`。周标题使用 `2026-W23（2026-05-25～2026-05-31）` 格式。复盘必须横向扫描 OpenAI Codex、Claude Code、Cursor、TRAE SOLO、GitHub Copilot、Windsurf / Devin Desktop、OpenClaw，并覆盖产品 feature、模型版本/模型能力变化、产品能力如何补足模型短板、TRAE SOLO 路线启示和 LPME 是否需要调整。TRAE SOLO 是战略启示对象，不是唯一信号源。

## Update Cadence

建议每日检查、每周汇总：

- 每日：短评，只关注重大更新；无重大更新时只记录“无重大更新”。
- 每周：趋势复盘，把碎片变化归纳成产品路线判断。

这样可以兼顾“日新月异”和“不硬推”。
