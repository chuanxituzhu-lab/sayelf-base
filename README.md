# SAYELF Shared Foundation / SAYELF 共享总底座

**Version / 版本: 1.1.1** · **Codex Skill** · **Provider-neutral / 不绑定模型或运行时供应商**

一个面向 Codex 与工程型 AI 工作的共享底座：把立项判断、动态原则选择、工具调用安全、多 Skill 编排、实现验收与交接收敛成一套可复用、可验证的门禁。

A shared foundation for Codex and engineering-oriented AI work. It combines evidence-gated assessment, an adaptive principle registry, safe tool execution, multi-Skill orchestration, implementation validation, and converged handoff.

## 核心能力 / Core capabilities

### 1. Assessment：先判断是否值得做 / Decide before building

**中文：** Step 0 搜索和比较现有方案，并将结论归为 `Duplicate`、`Integrate`、`Improve`、`Differentiate` 或 `Innovate` 之一；随后给出 `GO`、`CLARIFY` 或 `STOP`。证据不足时不得 `GO`。

**English:** Step 0 searches for and compares existing solutions, classifies the decision as exactly one of `Duplicate`, `Integrate`, `Improve`, `Differentiate`, or `Innovate`, then returns `GO`, `CLARIFY`, or `STOP`. Insufficient evidence must never produce `GO`.

### 2. Dynamic principles：原则数量按任务调整 / Adapt principles to the task

**中文：** 底座不固定为八项原则。`P01–P08` 只是当前基线注册项；系统根据任务、数据、权限、破坏性风险、交付阶段和证据需求生成最小 `Principle Profile`，用 `mandatory`、`conditional`、`not_applicable`、`blocked` 标记。新增或移除必须可解释，不能删除权限、数据主权、fail-closed、证据、收敛、版本和回滚等安全不变量。

**English:** The foundation does not have a fixed eight-principle list. `P01–P08` are the current baseline registry entries only. Each task derives a minimal `Principle Profile` using `mandatory`, `conditional`, `not_applicable`, and `blocked`; additions and removals require evidence, and immutable authorization, data-sovereignty, fail-closed, evidence, convergence, versioning, and rollback invariants remain in force.

### 3. Build gates：最小、可追溯的工程决策 / Minimal, traceable engineering

**中文：** 通过构建决策记录、简单优先、模块化边界、本地优先、数据主权、证据约束与回滚要求，控制从需求到最小可验证切片的过程；动态原则注册表与 12 步开发序列共同构成 Gate 层。

**English:** Build Decision Records, simple-first design, modular boundaries, local-first execution, data sovereignty, evidence-bounded automation, and rollback requirements guide work from intent to the smallest verifiable slice. The Gate layer combines the dynamic principle registry with a 12-step development sequence.

### 4. Runtime Guardrail：供应商中立的工具调用契约 / Provider-neutral tool contract

**中文：** 每次工具调用遵循 `PRE CHECK → EXECUTE → POST CHECK`：执行前检查权限、作用域、敏感数据、破坏性影响与人工批准；执行后检查输出结构、数据泄露、证据和状态变更。未通过检查即阻断或安全降级。

**English:** Every tool call follows `PRE CHECK → EXECUTE → POST CHECK`. Before execution, check permissions, scope, sensitive data, destructive impact, and required human approval. Afterwards, verify output structure, data leakage, evidence, and state changes. Failed checks block execution or require a safe fallback.

### 5. Shared capabilities：可插拔、API-ready / Pluggable shared AI capabilities

**中文：** 共用 AI 平台、Agent、模型、会话、记忆、审批、评测、策略、缓存、调度和追踪统一视为 provider-neutral `Shared Capability`。核心只依赖语义契约；本地实现、API、插件、MCP/连接器和 Agent Endpoint 都是可替换适配器。Skill 要求契约可接入，但不强制每个 Skill 网络化；能力可用不等于已授权。

**English:** Shared AI platforms, Agents, models, sessions, memory, approvals, evaluation, policy, caching, scheduling, and tracing are provider-neutral `Shared Capabilities`. The Core depends only on semantic contracts; local implementations, APIs, plugins, MCP/connectors, and Agent Endpoints are replaceable adapters. Skills are API-ready but are not forced onto the network; capability availability is not authorization.

### 6. Multi-Skill orchestration：最小编排与证据链 / Minimal orchestration with evidence

**中文：** 以 `Goal → Registry → Capability Match → Minimum Skill Set → Dependency Graph → Execution Contract → Acceptance → Evidence → Handoff → Convergence` 组装工作流；先选最小能力集合，再按依赖串行、条件或安全并行。分工层只使用 `Router / Sequential / Parallel / Loop / Agent-as-Tool` 五种模式；Session 与 Memory Bank 分离，已知单一接口用函数/API，多后端共用协议才用 MCP。编排不会增加 BMAD 多角色，也不实现供应商专属运行时。

**English:** Assemble workflows as `Goal → Registry → Capability Match → Minimum Skill Set → Dependency Graph → Execution Contract → Acceptance → Evidence → Handoff → Convergence`. The division layer uses only five patterns: `Router`, `Sequential`, `Parallel`, `Loop`, and `Agent-as-Tool`; Session and Memory Bank remain separate, and a known single interface uses a function/API while MCP is reserved for shared protocols across multiple backends. This adds no BMAD-style role system and no vendor-specific runtime.

### 7. Convergence：按意图收敛后再交接 / Converge before handoff

**中文：** 将当前实现与 `Intent / Spec / Plan / Task` 逐项做差距检查，至少识别 `missing`、`partial`、`contradicts`、`unrequested`。未处理的差距意味着 `NOT_CONVERGED`，不得报告完成或交接。

**English:** Compare the implementation against `Intent / Spec / Plan / Task` and classify gaps as at least `missing`, `partial`, `contradicts`, or `unrequested`. Any unresolved gap means `NOT_CONVERGED`; completion and handoff are not allowed.

### 8. Standards, FDE delivery, and evaluation / 标准、FDE 交付与评测

**中文：** 提供 Skill 设计标准、FDE 交付方法、评测框架与评分器，以及客户发现、数据就绪、方案设计、项目门禁、验收、ROI、知识移交和资产目录等模板。仅在相关交付任务中使用 FDE 方法。

**English:** Includes Skill design standards, FDE delivery guidance, evaluation methods and a scorer, plus templates for discovery, data readiness, solution design, project gates, acceptance, ROI, knowledge transfer, and asset catalogs. Apply FDE practices only when relevant to the delivery task.

## 仓库结构 / Repository layout

```text
SKILL.md                         # Skill entry point and operating contract
references/build-principles.md   # Dynamic principle registry and baseline entries
references/                      # Guardrails, orchestration, FDE, Skill, and eval references
assets/templates/                # Reusable delivery templates
scripts/                         # Optional local helper scripts
tests/                           # Golden/edge cases, sample outputs, and local scorer
```

## 在 Codex 中使用 / Use with Codex

**中文：** 将本仓库作为 `sayelf-base` Skill 放入 Codex 的 `skills` 目录，使 `SKILL.md` 位于 `skills/sayelf-base/SKILL.md`。在工程型任务中按需调用；完整评测与交付参考资料位于 `references/`，模板位于 `assets/templates/`。

**English:** Install this repository as the `sayelf-base` Skill in Codex's `skills` directory so that `SKILL.md` is at `skills/sayelf-base/SKILL.md`. Invoke it as needed for engineering work. Detailed evaluation and delivery guidance lives in `references/`; reusable templates are in `assets/templates/`.

## 版本 / Version

**v1.1.1** adds the adaptive Principle Registry and task-level Principle Profile, plus the bounded Agent division workflow, while retaining the evidence-gated `Execution Verdict`, provider-neutral Tool Guardrail Contract, shared-capability API/plugin adapters, generic multi-Skill orchestration, and the Convergence Gate before handoff.

**v1.1.1** 新增动态原则注册表、按任务生成的原则 Profile 和有界 Agent 分工工作流，同时保留基于证据的 `Execution Verdict`、供应商中立的 Tool Guardrail Contract、共享能力 API/插件适配器、通用多 Skill 编排，以及交接前的 Convergence Gate。

## License

MIT. See [LICENSE](LICENSE).
