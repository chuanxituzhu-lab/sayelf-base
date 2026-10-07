# Agent runtime 对齐：规划、证据与完成状态

本参考把共享底座的状态/证据门禁映射到规划型 Agent Runtime。它不要求引入另一套 Agent、技能或执行引擎。

## 构建决策记录

1. 真实任务：让共享底座与 Sayelf Agent Ops Sprint 01 的输出语义一致，避免丢弃跨岗位后续工作、把局部规划误报成端到端完成。
2. 最近能力：sayelf-base 的 Evidence、Convergence、状态与回滚规则；Sayelf Agent Ops 的 WorkItem、Router、MinimumPlanner、StateEngine。生态比较：Agent Skills 官方格式已提供模块指令与渐进披露；LangGraph 提供持久 checkpoint 和人工中断，但 Sprint 01 没有执行器/审批工作流，直接接入会增加不必要的运行时依赖。
3. Step 0：Improve。Execution Verdict：GO，仅限本地语义修正和可核验字段透传。
4. 度量差距：已判定的跨行业 follow-up 从 Router 到 Plan 当前为 0/1 可见；修复后应为 1/1，并明确 `NOT_CREATED`。附加依赖、激活岗位和状态数仍为 0。
5. 成功证据：黄金路由回归通过；跨行业决策在 Plan/API/本机预览中带出原岗位、后续岗位和未创建状态；没有运行 follow-up；共享底座 Skill validator 与本地 scorer 通过。
6. 最小内核：可选的 DeferredSubtask 数据对象、Planner 透传、本机预览清晰标记、共享底座状态语义规则。
7. 插件边界：Router 继续负责确定性选择；Planner 只表达计划；后续 Role/Skill 不自动加载或执行。
8. 本地边界：代码、任务示例、评测与评分均本地运行。
9. 数据分类：源代码 Internal；测试任务合成；原始请求 Unknown，留在当前本机 UI 进程，不新增持久化或传输。
10. 公开发布：Blocked；这轮只改本地工作树，无公开发布。
11. 外发：N/A；官方 Agent Skills 与 LangGraph 文档只读查询，不上传仓库内容。
12. 状态规则：普通单岗位计划保持 Sprint 01 原 4 个状态；后续任务状态记录为 `NOT_CREATED`，不得视为子工作项状态，也不得将父任务宣称交付完成。
13. 认识边界：观察：Router 已生成 follow-up 字段，Planner 未透传；推断：用户预览中可能误认为结果完整；假设：字段透传能消除该差距；事实：测试将验证 Plan 和响应字段一致。15 个路由样本不代表总体置信度。
14. 演进与回滚：改动前完整保留 sayelf-base 和被触及的 Agent Ops 源文件于本地回滚快照。验证失败可原样恢复；不改角色注册、技能、执行或审批。
15. WebUI：保留现有路由预览；跨行业时渐进显示一条“未建立的后续工作”提示，无 follow-up 时不增加界面噪声。
16. 实现：stdlib dataclass 扩展、JSON 字段、现有单元评测、本机 Agent Skills validator 与 scorer；不加依赖。
17. 明确不做：执行 follow-up、自动创建子工作流、增加 BLOCKED/REVIEW/EXECUTING 状态、Agent Ops executor/evidence service、人类审批、LangGraph 集成、公开发布。

## 互操作语义

| Sayelf Agent Ops 表示 | 含义 | 共享底座处理 |
|---|---|---|
| `INBOX / SCOPED / WORKING` | Sprint 01 的路由样例生命周期 | Agent Ops 局部状态，不替代底座交付状态 |
| `READY` | 当前 WorkItem 有输出记录；demo 当前是占位输出 | 只表示局部样例/计划就绪，不等于产物已验证、Convergence、生产批准或用户验收 |
| `registered / selected` | Role 或 Skill 已登记/被规划引用 | 不表示已激活、加载、授权或执行 |
| `followup.status=NOT_CREATED` | Router 指出了后续责任人但尚未建立下游 WorkItem | 父请求存在未完成的后续范围；不允许报端到端完成 |
| `CONVERGED` | 已由意图与实现逐项核对，必需差异闭合 | 仅在实际完成对照后使用；不得由 Agent Ops `READY` 推导 |
| `PROMOTED / PRODUCTION` | 已过相应验证、灰度、授权与运行门禁 | Sprint 01 当前不产生这些状态 |

若不同 Runtime 使用同名状态，适配层必须记录该状态验证的对象与证据，不按字符串名称推断等价。

## 搜索与取舍

- 本机 Agent Ops：Router 保留 cross-industry `followup_role`，但旧 Plan 与 UI 预览没有可操作的交接记录。
- 本机共享底座：Convergence 明确 Intent/Spec/Plan/Task 对照；8 原则明确注册不等于授权/执行。
- 官方 Agent Skills 规范：[agentskills/agentskills](https://github.com/agentskills/agentskills) 支持可渐进加载的 Skill 目录格式；它不提供 WorkItem 执行状态引擎。
- 官方 LangGraph Human-in-the-loop 文档：[持久化中断与恢复](https://docs.langchain.com/oss/python/langgraph/human-in-the-loop) 覆盖 checkpoint、人工暂停和恢复。Sprint 01 明确未实现 Executor/Human Gate，因此不接入。

判断：保留现有专用小型 Planner；增加明确的 deferred metadata，与其引入通用图执行框架更贴近真实缺口。
