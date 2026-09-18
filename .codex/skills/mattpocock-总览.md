# Matt Pocock Skills

本目录收纳从 `mattpocock/skills` 整理来的项目级 skill。目录名即 SKILL.md frontmatter 中的 canonical 英文名；中文展示名见各技能 `agents/openai.yaml` 的 `display_name`。

| Skill | 作用 | 适用场景 / 触发条件 |
|---|---|---|
| [测试驱动](tdd/SKILL.md) | 以测试驱动实现和修复 | 新功能、修 bug、需要先写测试、提到 TDD 或 red-green-refactor |
| [代码审查](code-review/SKILL.md) | 分别检查规范符合度和需求符合度 | review 分支、PR 或指定提交以来的改动 |
| [故障诊断](diagnosing-bugs/SKILL.md) | 建立复现回路，定位并验证根因 | 报告报错、失败、错误结果、性能变慢，或明确要求 debug/diagnose |
| [领域建模](domain-modeling/SKILL.md) | 统一术语，维护领域模型和决策记录 | 讨论项目概念、编辑 `CONTEXT.md`、新增或修改 ADR |
| [资料调研](research/SKILL.md) | 从高可信来源调查并沉淀 Markdown | 要求查资料、核实文档/API、整理研究结果 |
| [冲突解决](resolving-merge-conflicts/SKILL.md) | 处理 Git 合并或变基冲突 | 当前处于 merge/rebase 冲突状态 |
| [Agent 文档](writing-for-agents/SKILL.md) | 编写清晰、可触发的 Agent 文档 | 创建或修改 skill、`AGENTS.md`、`CLAUDE.md` |
| [极简编码](minimal-coding/SKILL.md) | 先澄清方案，保持最小改动和目标验证 | 所有写代码、重构、修 bug、review 或实现任务 |
| [深模块设计](codebase-design/SKILL.md) | 用小接口承载深实现，改善测试性和维护局部性 | 设计模块接口、划分 seam、提升可测试性或 AI 可读性 |
| [架构调优](improve-codebase-architecture/SKILL.md) | 扫描架构摩擦并提出深模块化候选 | 要求检查架构、寻找重构机会或改善代码库结构 |

## 使用原则

- 先按触发条件选择 skill；不满足条件时不要强行使用。
- `极简编码`负责通用编码约束，`测试驱动`负责测试先行流程，二者可以同时适用。
- `深模块设计`提供设计词汇，`架构调优`负责发现架构候选；后者需要时调用前者的概念。
