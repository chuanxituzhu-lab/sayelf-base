# SAYELF Shared Foundation / SAYELF 共享总底座

**Version / 版本: 1.1.4** · **Codex Skill** · **Provider-neutral / 不绑定模型或运行时供应商**

一个面向 Codex 与工程型 AI 工作的共享底座：把立项判断、动态原则选择、工具调用安全、多 Skill 编排、实现验收与交接收敛成一套可复用、可验证的门禁。

A shared foundation for Codex and engineering-oriented AI work. It combines evidence-gated assessment, an adaptive principle registry, safe tool execution, multi-Skill orchestration, implementation validation, and converged handoff.

## 核心能力 / Core capabilities

### 1. Assessment：先判断是否值得做 / Decide before building

**中文：** Step 0 搜索和比较现有方案，并将结论归为 `Duplicate`、`Integrate`、`Improve`、`Differentiate` 或 `Innovate` 之一；随后给出 `GO`、`CLARIFY` 或 `STOP`。证据不足时不得 `GO`。

**English:** Step 0 searches for and compares existing solutions, classifies the decision as exactly one of `Duplicate`, `Integrate`, `Improve`, `Differentiate`, or `Innovate`, then returns `GO`, `CLARIFY`, or `STOP`. Insufficient evidence must never produce `GO`.

### 2. Dynamic principles：原则数量按任务调整 / Adapt principles to the task

**中文：** 底座原则数量不固定。`P01–P14` 只是当前基线注册项；系统根据任务、数据、权限、破坏性风险、交付阶段和证据需求生成最小 `Principle Profile`，用 `mandatory`、`conditional`、`not_applicable`、`blocked` 标记。新增或移除必须可解释，不能删除权限、数据主权、fail-closed、证据、收敛、版本和回滚等安全不变量。

**English:** The foundation does not have a fixed-size principle list. `P01–P14` are the current baseline registry entries only. Each task derives a minimal `Principle Profile` using `mandatory`, `conditional`, `not_applicable`, and `blocked`; additions and removals require evidence, and immutable authorization, data-sovereignty, fail-closed, evidence, convergence, versioning, and rollback invariants remain in force.

### 3. Build gates：最小、可追溯的工程决策 / Minimal, traceable engineering

**中文：** 通过构建决策记录、简单优先、模块化边界、本地优先、数据主权、证据约束与回滚要求，控制从需求到最小可验证切片的过程；动态原则注册表与 12 步开发序列共同构成 Gate 层。

**English:** Build Decision Records, simple-first design, modular boundaries, local-first execution, data sovereignty, evidence-bounded automation, and rollback requirements guide work from intent to the smallest verifiable slice. The Gate layer combines the dynamic principle registry with a 12-step development sequence.

### 4. Runtime Guardrail：供应商中立的工具调用契约 / Provider-neutral tool contract

**中文：** 每次工具调用遵循 `PRE CHECK → EXECUTE → POST CHECK`：执行前检查权限、作用域、敏感数据、破坏性影响与人工批准；执行后检查输出结构、数据泄露、证据和状态变更。未通过检查即阻断或安全降级。

**English:** Every tool call follows `PRE CHECK → EXECUTE → POST CHECK`. Before execution, check permissions, scope, sensitive data, destructive impact, and required human approval. Afterwards, verify output structure, data leakage, evidence, and state changes. Failed checks block execution or require a safe fallback.

### 5. Shared capabilities：可插拔、API-ready / Pluggable shared AI capabilities

**中文：** 共用 AI 平台、Agent、模型、会话、记忆、审批、评测、策略、缓存、调度和追踪统一视为 provider-neutral `Shared Capability`。底座只定义语义契约和接口预留，不实现宿主登记器、供应商客户端、密钥配置或模型调用；向上 Harness/MCP 接入路由到 `sayelf-mcp-bridge`，向下大模型调用路由到 `sayelf-llm-gateway`。Skill 要求契约可接入，但不强制网络化；能力可用不等于已授权。

**English:** Shared AI platforms, Agents, models, sessions, memory, approvals, evaluation, policy, caching, scheduling, and tracing are provider-neutral `Shared Capabilities`. The foundation reserves semantic contracts and access surfaces only; it does not implement host registration, provider clients, credential setup, or model calls. Upward Harness/MCP integration routes to `sayelf-mcp-bridge`; downward model calls route to `sayelf-llm-gateway`. Skills are contract-ready but are not forced onto the network; capability availability is not authorization.

### 6.1 Access surfaces and local rendering / 接入面与本地渲染优先

**中文：** Agent/Skill 需要大模型或共享能力时，底座只按证据预留 API、MCP、CLI 接口，并通过能力契约声明权限、数据边界、证据和回退；实际大模型调用交给 `sayelf-llm-gateway`。需要接入 AI Harness 时，底座只预留 MCP、CLI 或宿主插件入口；实际多宿主登记、计划、安装、撤销和回滚交给 `sayelf-mcp-bridge`。所有调用接受 `PRE CHECK → EXECUTE → POST CHECK`。图像、3D、视频等可确定性渲染优先本地代码或本地引擎。

**English:** When an Agent or Skill needs a model or shared capability, the foundation reserves API, MCP, and CLI surfaces according to evidence and records permissions, data boundaries, evidence, and fallback; actual model calls belong to `sayelf-llm-gateway`. When it must integrate with an AI Harness, the foundation reserves an MCP, CLI, or host-plugin entry point; multi-host registration, planning, installation, removal, and rollback belong to `sayelf-mcp-bridge`. All calls follow `PRE CHECK → EXECUTE → POST CHECK`. Use local code or a local engine first for deterministic image, 3D, and video rendering.

### 6.2 Multi-Harness and optional self-run / 多平台 Harness 与可选自运行

**中文：** 同一 Agent/Skill 接入多个 Harness 时，底座只登记 host adapter matrix 和 `adapter_owner`，不直接写入宿主配置；优先复用共享宿主能力，向上路由 `sayelf-mcp-bridge`。大模型调用和可选自运行向下路由 `sayelf-llm-gateway`；底座只声明 runtime、预算、工具权限、数据边界、人工批准、停止/取消/恢复、证据与回退。不满足时返回 `UNAVAILABLE` / `BLOCKED` / `CLARIFY`，不得在底座内复制实现或无限循环。

**English:** When the same Agent or Skill connects to multiple Harnesses, the foundation records a host adapter matrix and `adapter_owner` but does not write host configuration; reuse shared host capabilities first and route upward integration to `sayelf-mcp-bridge`. Model calls and optional self-run route downward to `sayelf-llm-gateway`; the foundation declares runtime, budgets, tool permissions, data boundaries, human approval, stop/cancel/pause/resume, evidence, and fallback only. Unknown or unmet conditions return `UNAVAILABLE` / `BLOCKED` / `CLARIFY`; the foundation never duplicates adapters or permits an unbounded loop.

### 7. Multi-Skill orchestration：最小编排与证据链 / Minimal orchestration with evidence

**中文：** 以 `Goal → Registry → Capability Match → Minimum Skill Set → Dependency Graph → Execution Contract → Acceptance → Evidence → Handoff → Convergence` 组装工作流；先选最小能力集合，再按依赖串行、条件或安全并行。分工层只使用 `Router / Sequential / Parallel / Loop / Agent-as-Tool` 五种模式；Session 与 Memory Bank 分离，已知单一接口用函数/API 或 CLI，多后端共用协议才用 MCP。编排不会增加 BMAD 多角色，也不实现供应商专属运行时。

**English:** Assemble workflows as `Goal → Registry → Capability Match → Minimum Skill Set → Dependency Graph → Execution Contract → Acceptance → Evidence → Handoff → Convergence`. The division layer uses only five patterns: `Router`, `Sequential`, `Parallel`, `Loop`, and `Agent-as-Tool`; Session and Memory Bank remain separate, a known single interface may use a function/API or CLI, and MCP is reserved for shared protocols across multiple backends. This adds no BMAD-style role system and no vendor-specific runtime.

### 8. Convergence：按意图收敛后再交接 / Converge before handoff

**中文：** 将当前实现与 `Intent / Spec / Plan / Task` 逐项做差距检查，至少识别 `missing`、`partial`、`contradicts`、`unrequested`。未处理的差距意味着 `NOT_CONVERGED`，不得报告完成或交接。

**English:** Compare the implementation against `Intent / Spec / Plan / Task` and classify gaps as at least `missing`, `partial`, `contradicts`, or `unrequested`. Any unresolved gap means `NOT_CONVERGED`; completion and handoff are not allowed.

### 9. Standards, FDE delivery, and evaluation / 标准、FDE 交付与评测

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

**v1.1.4** narrows P10/P11/P13/P14 to interface reservations and adapter ownership: upward Harness/MCP integration is delegated to `sayelf-mcp-bridge`, downward model integration is delegated to `sayelf-llm-gateway`; the foundation does not duplicate host registration or provider clients. It retains P12 local-render-first placement, the adaptive Principle Registry, bounded Agent division workflow, evidence-gated `Execution Verdict`, provider-neutral Tool Guardrail Contract, generic multi-Skill orchestration, and the Convergence Gate before handoff.

**v1.1.4** 将 P10/P11/P13/P14 收窄为接口预留与适配器归属：向上的 Harness/MCP 接入交给 `sayelf-mcp-bridge`，向下的大模型接入交给 `sayelf-llm-gateway`；底座不复制宿主登记或供应商客户端实现。同时保留 P12 本地渲染优先、动态原则注册表、按任务生成的原则 Profile、有界 Agent 分工工作流、基于证据的 `Execution Verdict`、供应商中立的 Tool Guardrail Contract、通用多 Skill 编排，以及交接前的 Convergence Gate。

## License

MIT. See [LICENSE](LICENSE).
