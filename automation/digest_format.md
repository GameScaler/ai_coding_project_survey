# Digest Format Contract

这是 daily / weekly digest 的唯一格式规范。GitHub 归档、飞书文档小节、Feishu App Bot 推送卡片、Codex 自动化 prompt 都必须以本文件为准。

不要把抓取源变化、网页变化、内部监控状态、原文摘录、自动化运行问题写进正式 digest。机器抓取草稿中的 `Source / Changed / Excerpt` 等字段只用于本地复核；公开内容只回答产品本身有没有重要变化。

## Core Product Order

所有 daily / weekly 产品列表都按以下固定顺序：

1. OpenAI Codex
2. Claude Code
3. Cursor
4. TRAE SOLO
5. GitHub Copilot
6. Windsurf / Devin Desktop
7. OpenClaw
8. Kimi Code
9. Zhipu GLM Coding Plan / CodeGeeX

## Daily Digest Format

```markdown
## Summary

无新增产品级重大公开更新。

## Product Updates

### OpenAI Codex
- 无

### Claude Code
- 无

### Cursor
- 无

### TRAE SOLO
- 无

### GitHub Copilot
- 无

### Windsurf / Devin Desktop
- 无

### OpenClaw
- 无

### Kimi Code
- 无

### Zhipu GLM Coding Plan / CodeGeeX
- 无

## PM Notes

- **产品官短评**：无新增产品级重大公开更新。
- **对 TRAE SOLO 的启示**：只记录真正改变用户 workflow 的新 feature、模型迭代、agent workflow、治理、定价和交付物边界变化。
- **LPME 是否更新**：不更新。
```

有重大变化时，只在对应产品项下写 1 到 2 句中文产品结论；其他产品仍写 `无`。每日更新要短、明确、读者视角，不硬凑新闻。

## Weekly Digest Format

周复盘只处理已经结束的完整周一到周日周期，不生成进行中周，不创建 `Wxx-in-progress`。

```markdown
## Weekly Summary

## Head Product Signals

- **OpenAI Codex**：无
- **Claude Code**：无
- **Cursor**：无
- **TRAE SOLO**：无
- **GitHub Copilot**：无
- **Windsurf / Devin Desktop**：无
- **OpenClaw**：无
- **Kimi Code**：无
- **Zhipu GLM Coding Plan / CodeGeeX**：无

## Competitive Reading

## TRAE SOLO Implication

## LPME Implication

## Source Notes
```

有重大变化时，只在对应产品项下写 1 到 2 句产品结论；其他产品仍写 `无`。周复盘需要归纳产品路线、模型版本 / 模型能力变化、产品能力如何补足模型短板、TRAE SOLO 启示和 LPME 是否调整。

## Publishing Rules

- GitHub daily / weekly markdown、飞书文档、机器人推送使用同一套结构。
- Feishu App Bot 卡片正文不额外增加旧四段式栏目。
- 链接入口可以放在卡片按钮中；正文保持 `Summary / Product Updates / PM Notes` 或 weekly 固定结构。
- TRAE SOLO 是战略解释对象，不是唯一信号源；每次都必须横向扫描完整核心产品池。
