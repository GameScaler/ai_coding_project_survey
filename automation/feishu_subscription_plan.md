# Feishu Subscription Plan

更新时间：2026-06-03

## Conclusion

飞书文档里放一个按钮，让任意读者点击后“订阅同一个自定义机器人并推送到他的飞书”，这个路径不成立。

原因是飞书/Lark 官方文档明确说明：custom bot 只能用于当前群聊，同一个自定义机器人不能被添加到其他群。它适合群内通知 webhook，不适合作为跨用户、跨群的订阅系统。

可行方案分两档：

当前应用状态：

- 已创建开放平台应用：`AI Coding Survey Bot`
- App ID：`cli_aa955d3cef3a5be6`
- App Secret：已由用户提供，但不写入仓库或文档。
- 结论：这个 App ID/Secret 可以支撑正式 App Bot 路线，但不能替代 MVP 的群自定义机器人 webhook。MVP 仍需要在目标订阅群里创建 custom bot 并提供 webhook。

## MVP: Subscription Group + Custom Bot

适合现在快速落地。

### 用户操作步骤

1. 创建一个固定飞书群，例如：`AI Coding Product Update`.
2. 打开群设置。
3. 进入 `群机器人` / `添加机器人`。
4. 选择 `自定义机器人`。
5. 命名建议：`AI Coding Survey Bot - Group Push`。
6. 安全设置建议开启 `签名校验`，不要只靠关键词。
7. 保存后复制 webhook URL；如果开启签名，复制 secret。
8. 把群邀请链接或二维码放进飞书文档的“订阅入口”。
9. 把 webhook/secret 配置到本地 shell、Codex automation secret 或部署环境。

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

## Formal: Feishu App Bot + Subscription Service

适合稳定运营。

### 用户操作步骤

1. 打开应用后台：`AI Coding Survey Bot`。
2. 在 `应用能力` 中启用机器人。
3. 在 `权限管理` 中添加消息发送权限。最小权限建议：
   - 给用户或群发送消息；
   - 获取用户/群基本信息，如果要做订阅管理；
   - 读写文档权限，仅当要让机器人自动写飞书文档。
4. 发布/提交权限审批。企业租户下可能需要管理员审批。
5. 把应用机器人添加到固定订阅群。
6. 获取目标群的 `chat_id`，或通过事件订阅/群信息 API 获取。
7. 建立订阅表：
   - subscriber open_id
   - chat_id
   - subscription type: daily / weekly / major-only
   - status
8. 飞书文档里放订阅页面、飞书多维表格或申请表链接。
9. 用户订阅后，应用机器人按 open_id 或 chat_id 发送消息。
10. 支持退订、频率选择、只看指定产品等功能。

### 自动化配置

本仓库提供 `scripts/feishu_app_send.py`，读取环境变量发送 App Bot 消息卡片：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_RECEIVE_ID`
- `FEISHU_RECEIVE_ID_TYPE`，默认 `chat_id`

测试命令：

```bash
python scripts/feishu_app_send.py data/daily_updates/2026-06-03.md \
  --title "AI Coding Daily Update - 2026-06-03" \
  --github-url "https://github.com/GameScaler/ai_coding_project_survey/blob/main/data/daily_updates/2026-06-03.md" \
  --dry-run
```

注意：App Secret 只放本地环境变量或自动化 secret，不写入仓库、不写入飞书文档。

### Pros

- 可以做真正的订阅、退订和个性化推送。
- 可以支持个人私聊、多个群、多租户。
- 可以做交互式 message card。

### Cons

- 需要飞书开放平台配置。
- 可能需要租户权限审批。
- 需要维护一个小型后端或自动化服务。

## Recommendation

当前调研报告阶段，建议先用 MVP：

- 文档内放“订阅更新”的入口，本质是加入固定飞书群或填写订阅表。
- 每日自动化只往这个群推送。
- 等报告稳定、订阅人数增加后，再升级为 Feishu App Bot。

飞书文档中的文案建议：

> 订阅更新：加入固定飞书群，每天 11:00 接收重大更新；无重大更新时只记录“无重大更新”。每周复盘会归纳趋势和 TRAE SOLO 产品启示。当前为 MVP 订阅群方案，后续升级为 AI Coding Survey Bot 个性化订阅。

## Message Card Shape

每日卡片建议：

- 标题：`AI Coding Daily Update - YYYY-MM-DD`
- 状态色：
  - green：有重大更新
  - grey：无重大更新
  - orange：需要人工确认
- 内容：
  - 今日重大更新数量
  - 产品逐条摘要
  - 产品官短评
  - 对 TRAE SOLO 的启示
  - 文档链接
  - GitHub digest 链接

## Required User Action

MVP 需要用户在飞书里完成：

1. 创建或选择一个订阅群。
2. 群设置 -> 群机器人 -> 添加机器人 -> 自定义机器人。
3. 命名：`AI Coding Survey Bot - Group Push`.
4. 开启签名校验，并复制 webhook 和 secret。
5. 把 webhook 和 secret 提供给本地环境或 Codex automation。

拿到 webhook 后，本仓库的脚本可以直接推送。

正式 App Bot 需要用户在飞书开放平台继续完成：

1. 给 `AI Coding Survey Bot` 开启机器人能力。
2. 添加并审批消息发送权限。
3. 将应用机器人加入目标订阅群。
4. 提供目标群 `chat_id` 或让脚本通过事件回调/群 API 获取。
5. 如需自动写飞书文档，再补充文档 API 权限与目标文档 token。
