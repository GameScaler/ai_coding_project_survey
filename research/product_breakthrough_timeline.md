# AI Coding 重大产品功能突破时间线

更新时间：2026-06-04

## 入选标准

这条时间线只收录真正改变产品范式的节点，不收录普通 changelog。一个节点至少满足以下标准之一：

1. **主入口变化**：从补全 / 聊天，升级为任务、工作台、移动调度或多 agent 指挥台。
2. **自治边界变化**：agent 开始能读 repo、改多文件、执行命令、跑测试、长时间工作、云端并行或跨设备执行。
3. **交付物边界变化**：输出从代码片段升级为 PR、网站、内部工具、dashboard、文档或可托管业务产物。
4. **市场心智变化**：形成强市场反馈，迫使竞品跟进同一方向。
5. **模型-产品联动**：模型节点只有在直接改变 coding 产品默认工作流时才进入。

## 单线时间轴

- **2021-06-29｜GitHub Copilot technical preview**：AI coding 的主心智从“问答式写代码”变成编辑器内实时共写，autocomplete 成为第一代大众入口。
- **2024-03｜Devin 发布**：用“自主软件工程师 + SWE-bench”重新定义市场叙事，把竞争问题从 completion 推到 end-to-end task。
- **2024-04｜GitHub Copilot Workspace preview**：从 issue / natural language 进入 spec、plan、build、test、run，开始把 Copilot 从助手升级为任务环境。
- **2024-06-20｜Claude 3.5 Sonnet 上线**：模型在 coding、速度和成本上的跃迁，让 Claude 系产品成为 agentic coding 的能力上限参照。
- **2025-02-24｜Claude Code research preview**：Claude Code 把强模型放进 terminal-native 工作流，建立“透明执行、shell / Git / test 可控”的专业开发者心智。
- **2025-04/05｜OpenAI Codex CLI + Codex Cloud**：Codex 从本地终端进入 ChatGPT 云端并行任务，形成 local execution 与 cloud delegation 的双入口。
- **2025-05-19｜GitHub Copilot coding agent public preview**：把 agent 放进 GitHub issue / PR / Actions 闭环，异步开发者开始进入企业工程流。
- **2025-06-04｜Cursor 1.0**：Background Agent、BugBot、Memories、MCP 一起出现，说明 Cursor 不再只是 AI editor，而是在做 agent runtime + review loop。
- **2026-03-31｜TRAE SOLO 0.1.0**：TRAE 把 SOLO 独立为 Web / Desktop 双端、Work / Code 双模式和三栏工作区，明确冲向“More Than Coding”的多角色工作台。
- **2026-04-02｜Cursor 3.0 Agents Window**：主界面从 editor / chat 升级为多 agent 并行窗口，支持 local、worktree、cloud、remote SSH，agent command center 成为正面范式。
- **2026-H1｜Kimi K2.6 + Kimi Code**：国内模型厂商开始把长任务 coding、agent swarm、CLI / IDE / ACP 打成一体，说明模型升级会直接改变产品默认 workflow。
- **2026-H1｜智谱 GLM Coding Plan / CodeGeeX 进入 coding plan 化**：不是单点 IDE 插件创新，而是用模型套餐、支持工具、MCP、团队额度和 CodeGeeX 入口抢占国内开发者工作流。
- **2026-05｜OpenAI Codex /goal**：目标模式把一次 prompt 变成可暂停、恢复、追踪的多小时任务，核心突破是让 agent 有“长期任务对象”而不是只响应回合。
- **2026-05-05/06｜TRAE SOLO Mobile**：手机变成 dispatch console，可以远程触发桌面 / Web 任务、查看进度和语音输入，AI coding 进入跨设备控制阶段。
- **2026-05-29～06-02｜长任务控制台集中爆发**：Cursor 3.6 Auto-review 降低 approval friction；Codex Sites 把代码产物变成托管网站 / 内部工具；GitHub Copilot App 做 agent-native desktop；Devin Desktop 把 local / cloud agent 放进 Kanban；OpenClaw 2026.6 beta 强化 multi-channel gateway、Workboard、Skill Workshop。这一周的共同信号是：AI coding 主战场从“写代码”升级为“管理 agent、验证风险、交付可用产物”。

## 压缩判断

如果只保留一条主线，AI coding 的演化不是“模型越来越会写代码”，而是：

**completion → repo-aware agent → async cloud engineer → multi-agent command center → product workbench**。

这也解释了为什么 TRAE SOLO 不能只追 Cursor 的 IDE 能力。模型能力决定上限，但当前模型仍需要产品能力补足上下文、验证、权限、回滚、协作和交付边界；真正的机会在于把 coding agent 变成多角色都能使用的工作交付平台。

## 主要资料源

- GitHub Copilot technical preview: https://github.blog/news-insights/product-news/introducing-github-copilot-ai-pair-programmer/
- Devin launch: https://cognition.ai/blog/introducing-devin
- GitHub Copilot Workspace: https://github.blog/news-insights/product-news/github-copilot-workspace/
- Claude 3.5 Sonnet: https://www.anthropic.com/news/claude-3-5-sonnet
- Claude 3.7 Sonnet and Claude Code: https://www.anthropic.com/news/claude-3-7-sonnet
- OpenAI Codex: https://openai.com/index/introducing-codex/
- Codex /goal: https://developers.openai.com/codex/use-cases/follow-goals
- GitHub Copilot coding agent: https://github.blog/changelog/2025-05-19-github-copilot-coding-agent-in-public-preview/
- Cursor 1.0: https://cursor.com/changelog/1-0
- Cursor 3.0: https://cursor.com/changelog/3-0
- Cursor 3.6: https://cursor.com/changelog
- TRAE SOLO changelog: https://docs.trae.ai/solo/changelog
- TRAE SOLO Mobile: https://www.trae.ai/blog/trae_solo_mobile_0506?v=1
- Kimi K2.6: https://www.kimi.com/ai-models/kimi-k2-6
- Kimi Code: https://www.kimi.com/code/en
- Zhipu GLM Coding Plan: https://docs.bigmodel.cn/cn/coding-plan/overview
- CodeGeeX: https://marketplace.visualstudio.com/items?itemName=aminer.codegeex
- Codex Sites: https://developers.openai.com/codex/changelog
- GitHub Copilot App: https://github.blog/news-insights/product-news/github-copilot-app-the-agent-native-desktop-experience/
- Devin Desktop: https://devin.ai/blog/windsurf-is-now-devin-desktop
- OpenClaw docs: https://docs.openclaw.ai/
- OpenClaw releases: https://github.com/openclaw/openclaw/releases
