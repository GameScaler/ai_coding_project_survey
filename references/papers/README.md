# Paper References

本目录存放 AI coding / software engineering agent / web agent / benchmark 相关核心论文 PDF。文件名以 arXiv id 或论文编号开头，便于长期追踪。

## Downloaded Papers

| File | Paper | Why It Matters |
| --- | --- | --- |
| `2306.03091_repobench.pdf` | RepoBench | 证明 repo 级上下文检索、跨文件补全和 pipeline 评估是代码产品的基础层。 |
| `2310.06770_swe_bench.pdf` | SWE-bench | 把评估从算法题推进到真实 GitHub issue 和 PR。 |
| `2401.13649_visualwebarena.pdf` | VisualWebArena | 说明真实网页任务依赖视觉理解和 UI 操作，不只是文本规划。 |
| `2402.01030_codeact.pdf` | CodeAct | 把 agent action space 统一到可执行代码，强调动作空间设计的重要性。 |
| `2405.15793_swe_agent.pdf` | SWE-agent | 提出 agent-computer interface，说明产品接口本身能显著改变 agent 能力。 |
| `2407.01489_agentless.pdf` | Agentless | 证明复杂自治 agent 不是总是必要，定位、修复、验证三段式是强 baseline。 |
| `2410.03859_swe_bench_multimodal.pdf` | SWE-bench Multimodal | 将 SWE-bench 延展到视觉、UI、前端 JavaScript 任务。 |
| `2412.21139_swe_gym.pdf` | SWE-Gym | 把真实 SWE 任务做成可训练环境，并引入 verifier / inference-time scaling。 |
| `2504.07164_r2e_gym.pdf` | R2E-Gym | 用程序化生成环境和混合 verifier 扩大 SWE agent 训练数据。 |
| `2504.21798_swe_smith.pdf` | SWE-smith | 用自动合成任务把 SWE agent 训练数据扩到 50k 级别。 |
| `2505.20411_swe_rebench.pdf` | SWE-rebench | 强调 benchmark 污染和新鲜任务供给，适合长期评测体系设计。 |

## Reading Lens

这些论文不要按“谁分数更高”来读，而要按产品问题来读：

- 模型为什么失败？
- 产品界面如何降低失败概率？
- 哪些能力应该做成稳定工具，而不是交给模型即兴发挥？
- 评测如何避免只测模型，不测产品？
- 训练数据和 benchmark 污染会如何影响产品宣传？

