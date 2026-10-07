# 构建决策记录：Agent Ops × sayelf-base

**真实任务：** 修正规划、后续子任务、证据与交付状态的接口语义。
**最近能力：** sayelf-base Convergence / Skill 边界；Sayelf Agent Ops `WorkItem → Router → Planner → StateEngine`。
**Step 0：** `Improve`。**Execution Verdict：** `GO`，限定文档、数据模型透传与本地预览。
**度量：** cross-industry Router 返回的 1 个 follow-up 从 Plan/API/UI 的可见率由 `0/1` 提升到 `1/1`，状态明确 `NOT_CREATED`；依赖、激活岗位、WorkItem 状态数增量均为 `0`。
**最小核心：** 可选 `DeferredSubtask`、Planner 透传、局部 `READY` 与底座 `CONVERGED/PROMOTED` 语义说明。
**插件边界：** 路由、规划分层；follow-up 不创建、不执行。
**本地与数据：** 本地处理，源代码 `Internal`，测试数据合成；不外发。
**公开发布：** `Blocked`；只改本机安装目录及 Agent Ops 工作树，未提交/推送。
**状态：** 缺失配对 follow-up → Plan 拒绝；存在完整 follow-up → 计划中保留未创建条目；单岗位用户流程不变。
**Fact / Hypothesis：** follow-up 当前会在 Planner 中丢失为事实；预览提示是否消除误解是待验证假设。
**演进与回滚：** 变更前快照存于本地回滚快照；运行基线和修订评测；不部署。
**WebUI：** 已有预览足够；仅跨行业情况出现内联未创建提示。
**最简实现：** Python dataclass 与本地 Agent Skills validator/scorer。
**明确不建：** 执行器、状态引擎扩展、新角色、新技能、外部框架和公网发布。
