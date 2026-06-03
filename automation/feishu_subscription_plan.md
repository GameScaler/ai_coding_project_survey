# Feishu Subscription Plan

更新时间：2026-06-03

## Conclusion

飞书文档里放一个按钮，让任意读者点击后“订阅同一个自定义机器人并推送到他的飞书”，这个路径不成立。

原因是飞书/Lark 官方文档明确说明：custom bot 只能用于当前群聊，同一个自定义机器人不能被添加到其他群。它适合群内通知 webhook，不适合作为跨用户、跨群的订阅系统。

可行方案分两档：

## MVP: Subscription Group + Custom Bot

适合现在快速落地。

### Workflow

1. 用户创建一个飞书群：`AI Coding Product Update`.
2. 在该群添加自定义机器人。
3. 复制 webhook URL，建议开启签名校验。
4. 在本地或 Codex automation 配置环境变量：
   - `FEISHU_BOT_WEBHOOK`
   - `FEISHU_BOT_SECRET`，如果开启签名
5. 每天 11 点生成更新后，通过 webhook 推送 message card 到该群。
6. 飞书文档里放一个“订阅入口”：
   - 群二维码；
   - 入群链接；
   - 或一个“申请订阅”表单链接。

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

### Workflow

1. 创建飞书开放平台应用，启用 bot 能力。
2. 配置 app_id/app_secret、事件订阅和消息权限。
3. 建立订阅表：
   - subscriber open_id
   - chat_id
   - subscription type: daily / weekly / major-only
   - status
4. 飞书文档里放按钮或链接，打开一个订阅页面 / 飞书多维表格 / 申请表。
5. 用户订阅后，应用机器人按 open_id 或 chat_id 发送消息。
6. 支持退订、频率选择、只看指定产品等功能。

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

- 文档内放“订阅更新”的入口，但本质是加入固定飞书群或填写订阅表。
- 每日自动化只往这个群推送。
- 等报告稳定、订阅人数增加后，再升级为 Feishu App Bot。

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
3. 命名：`AI Coding Product Update`.
4. 开启签名校验，并复制 webhook 和 secret。
5. 把 webhook 和 secret 提供给本地环境或 Codex automation。

拿到 webhook 后，本仓库的脚本可以直接推送。

