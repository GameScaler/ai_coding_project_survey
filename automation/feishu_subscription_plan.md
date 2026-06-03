# Feishu Subscription Plan

更新时间：2026-06-03

## Conclusion

飞书文档里放一个按钮，让任意读者点击后“订阅同一个自定义机器人并推送到他的飞书”，这个路径不成立。

原因是飞书/Lark 官方文档明确说明：custom bot 只能用于当前群聊，同一个自定义机器人不能被添加到其他群。它适合群内通知 webhook，不适合作为跨用户、跨群的订阅系统。

当前直接采用正式 App Bot 路线。自定义群机器人只保留为 fallback。

当前应用状态：

- 已创建开放平台应用：`AI Coding Survey Bot`
- App ID：`cli_aa955d3cef3a5be6`
- App Secret：已由用户提供，但不写入仓库或文档。
- 结论：这个 App ID/Secret 已足够支撑 App Bot 鉴权。接下来要补的是飞书侧的机器人能力、消息权限、目标 `chat_id/open_id`、订阅表。

## Formal: Feishu App Bot + Subscription Service

这是当前主路线。

### 分享文档后的订阅方式

把飞书文档分享给别人后，读者不会因为点击文档里的按钮就自动把机器人安装到自己的群或个人会话里。飞书的权限模型要求用户或群管理员主动建立和应用机器人的关系。

当前可落地入口：

1. 固定订阅群：文档中放群邀请链接或二维码。读者加入群后，`AI Coding Survey Bot` 已在群内，所有 daily/weekly digest 都推到这个群。
2. 订阅表：文档中放飞书表单/多维表格链接。读者填写姓名、飞书邮箱、订阅频率；后台把对应 `open_id`、`email` 或 `chat_id` 加入订阅表。
3. 新群订阅：如果某个团队想让自己的群接收推送，群管理员需要把 `AI Coding Survey Bot` 添加到群里；之后用 `scripts/feishu_list_chats.py` 或事件回调拿到该群 `chat_id`，再加入订阅表。

正式个人订阅需要下一阶段补一个小型订阅服务：用户打开订阅页或点击交互式卡片按钮后，App Bot 通过事件回调拿到用户 `open_id`，再写入订阅表，并支持退订、改频率和只订阅某些产品。

### 用户操作步骤

1. 打开应用后台：`AI Coding Survey Bot`。
2. 在 `应用能力` 中启用机器人。
3. 在 `权限管理` 中添加消息发送权限。最小权限建议：
   - 给用户或群发送消息；
   - 获取用户/群基本信息，如果要做订阅管理；
   - 读写文档权限，仅当要让机器人自动写飞书文档。
4. 发布/提交权限审批。企业租户下可能需要管理员审批。
5. 把应用机器人添加到固定订阅群，或让用户主动和机器人私聊。
6. 获取目标群的 `chat_id`，或获取个人 `open_id`。
   - 如果是固定订阅群，先把机器人加进群，再运行 `scripts/feishu_list_chats.py` 查看 bot 可见群聊。
   - 如果是个人订阅，可以先用 `email` / `open_id` 作为 `receive_id_type`，但前提是用户在同一飞书租户且权限可用。
7. 建立订阅表：
   - `receive_id`
   - `receive_id_type`: `chat_id` / `open_id` / `user_id` / `email` / `union_id`
   - `name`
   - `subscription`: `daily` / `weekly` / `major-only`
   - `status`: `active` / `paused`
8. 飞书文档里放订阅入口：
   - 当前阶段：固定订阅群链接/二维码，或者飞书表单/多维表格；
   - 后续阶段：独立订阅页或交互式卡片按钮。
9. 用户订阅后，应用机器人按订阅表发送 daily/weekly 消息。
10. 支持退订、频率选择、只看指定产品等功能。

### 自动化配置

本仓库提供 `scripts/feishu_app_send.py`，读取环境变量发送 App Bot 消息卡片。
本仓库还提供 `scripts/feishu_list_chats.py`，用于列出机器人可见群聊并拿到 `chat_id`。

必需环境变量：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`

本地运行时可以使用 `.env.local` 放置这些变量，脚本会自动读取 `.env.local`；`.env.local` 已加入 `.gitignore`。

单目标推送：

- `FEISHU_RECEIVE_ID`
- `FEISHU_RECEIVE_ID_TYPE`，默认 `chat_id`

订阅表群发：

- `FEISHU_SUBSCRIBER_FILE`，例如 `automation/feishu_subscribers.local.json`

测试命令：

```bash
python scripts/feishu_app_send.py data/daily_updates/2026-06-03.md \
  --title "AI Coding 产品更新｜2026-06-03" \
  --github-url "https://github.com/GameScaler/ai_coding_project_survey/blob/main/data/daily_updates/2026-06-03.md" \
  --dry-run
```

推送卡片规范：

- 标题用中文，例如 `AI Coding 产品更新｜2026-06-03`。
- 正文只保留四块：今日结论、重点信号、产品官短评、来源链接。
- 不直接推送网页英文原文、`Source / Changed / Excerpt` 等机器抓取字段。
- 如果只有机器初筛、尚未人工复核，卡片只说明“哪些产品的官方源发生变化、需要复核哪些方向”，不把内部判断字段原样发给订阅者。
- 来源链接只放官方 changelog、GitHub digest、飞书文档入口，避免把长网页摘录贴进群。

订阅表 dry-run：

```bash
python scripts/feishu_app_send.py data/daily_updates/2026-06-03.md \
  --title "AI Coding Daily Update - 2026-06-03" \
  --subscriber-file automation/feishu_subscribers.local.json \
  --subscription daily \
  --dry-run
```

注意：App Secret 只放本地环境变量或自动化 secret，不写入仓库、不写入飞书文档。

获取群聊 `chat_id`：

```bash
python scripts/feishu_list_chats.py
```

输出的第一列就是可作为 `FEISHU_RECEIVE_ID` 的 `chat_id`。如果列表为空，通常说明机器人还没有被添加到目标群，或应用权限/发布状态未生效。

### Pros

- 可以做真正的订阅、退订和个性化推送。
- 可以支持个人私聊、多个群、多租户。
- 可以做交互式 message card。
- 可以和飞书文档、飞书表格、多维表格形成闭环。

### Cons

- 需要飞书开放平台配置。
- 可能需要租户权限审批。
- 需要维护一个订阅表；当前用本地 JSON 即可，后续可升级为多维表格/数据库。

## Fallback: Subscription Group + Custom Bot

仅当 App Bot 权限或 `chat_id/open_id` 获取被卡住时使用。

### 用户操作步骤

1. 创建一个固定飞书群，例如：`AI Coding Survey 订阅群`。
2. 群设置里开启“群链接/二维码邀请”，复制群链接或保存二维码。
3. 在群设置里添加 `AI Coding Survey Bot` 应用机器人。
4. 运行 `scripts/feishu_list_chats.py` 获取该群 `chat_id`，填入订阅表或 `FEISHU_RECEIVE_ID`。
5. 把群链接/二维码放进飞书文档“自动化更新与订阅”部分。
6. 分享文档给别人时，对方加入这个群即视为订阅。
7. 若暂时用自定义机器人 fallback，再进入 `群机器人` / `添加机器人`，创建 custom bot webhook。
8. 自定义机器人安全设置建议开启 `签名校验`，不要只靠关键词。
9. webhook/secret 只配置在本地 shell、Codex automation secret 或部署环境，不写入仓库/文档。

### 自动化配置

需要配置环境变量：

   - `FEISHU_BOT_WEBHOOK`
   - `FEISHU_BOT_SECRET`，如果开启签名

测试命令：

```bash
python scripts/feishu_push.py data/daily_updates/2026-06-03.md \
  --title "AI Coding Daily Update - 2026-06-03" \
  --github-url "https://github.com/GameScaler/ai_coding_project_survey/blob/main/data/daily_updates/2026-06-03.md" \
  --dry-run
```

确认卡片内容没问题后去掉 `--dry-run`。

### Pros

- 配置快。
- 不需要租户管理员审核。
- 非技术订阅者只需要进群。

### Cons

- 订阅不是“文档按钮自动订阅”，而是加入固定群。
- 自定义机器人只能发到当前群。
- 不能天然管理个人订阅、退订、分组推送。

## Recommendation

当前调研报告阶段，直接使用 Feishu App Bot：

- 文档内放“订阅更新”的入口，本质是进入订阅群、填写订阅表，或后续打开订阅页。
- 每日/每周自动化通过 `AI Coding Survey Bot` 推送消息卡片。
- 订阅表先用本地 JSON，后续升级为飞书多维表格或数据库。
- 周复盘只推送已结束完整周；进行中周不推送、不入归档。

飞书文档中的文案建议：

> 订阅更新：通过 AI Coding Survey Bot 订阅，每天 11:00 接收重大更新；无重大更新时只记录“无重大更新”。每周一 11:20 接收周复盘。当前订阅入口为固定群/表单，后续升级为交互式订阅卡片。

## Message Card Shape

每日卡片建议：

- 标题：`AI Coding 产品更新｜YYYY-MM-DD`
- 状态色：
  - green：有重大更新
  - grey：无重大更新
  - orange：需要人工确认
- 内容：
  - 今日结论
  - 重点信号
  - 产品官短评
  - 来源链接

示例：

```text
AI Coding 产品更新｜2026-06-03

今日结论
OpenClaw 纳入主要产品池。今天的核心不是又多一个 IDE，而是 agent gateway / runtime 路线进入观察范围。

重点信号
- OpenClaw：Workboard、Skill Workshop、channels/mobile、runtime recovery。
- Codex：Sites preview 继续把代码产物变成可部署业务 artifact。
- GitHub Copilot：App、SDK、sandboxes、agent apps 共同强化 GitHub-native agent platform。

产品官短评
AI coding 产品能力 = 模型能力 + 产品能力。模型决定上限，产品层决定真实可用性。

来源链接
- 飞书文档
- GitHub digest
- 官方 changelog
```

## Required User Action

当前还需要用户在飞书里完成：

1. 在飞书客户端创建一个普通群，建议命名为 `AI Coding Survey 订阅群`。
2. 至少选择一位真人成员后再创建群；web 端创建 0 成员群会失败，应用机器人也不能在建群成员搜索里直接作为普通成员选中。
3. 群创建后，进入群设置，添加 `AI Coding Survey Bot` 应用机器人；只有机器人在群内，App Bot 才能向该群推送。
4. 在群设置里开启群邀请链接或群二维码；把这个入口放到飞书文档“自动化更新与订阅”部分。
5. 运行 `scripts/feishu_list_chats.py` 拿到该群 `chat_id`，写入 `automation/feishu_subscribers.local.json` 或本地环境变量。
6. 后续读者通过文档里的群链接/二维码进群，即完成 MVP 订阅；正式个人订阅再升级为交互式卡片/订阅页。

拿到 `chat_id/open_id` 后，本仓库的 App Bot 脚本可以直接推送。
