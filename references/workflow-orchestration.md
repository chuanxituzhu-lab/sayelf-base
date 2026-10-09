# 通用多 Skill 工作流编排

> `sayelf-base` v1.1.2 的 L3 参考。它把目标编译为最小、可验证、可恢复的多 Skill/Agent 工作流，并支持通过统一契约接入共享 AI 平台或 Agent 能力；不代替单个 Skill 的专业规则，不实现执行引擎。

## 1. 适用范围与边界

当一个真实目标需要多个 Skill、工具或人工节点协同时，按本标准组装和审查工作流。每个 Skill 仍只负责其声明的专业任务；编排层负责匹配能力、依赖顺序、输入/输出契约、验收、证据与恢复。

本标准与底座其它门禁的关系：

- `Execution Verdict`（`GO / CLARIFY / STOP`）决定任务是否允许进入执行；组装验证通过不能覆盖或推翻它。
- 每次编排先生成动态 `Principle Profile`（`mandatory / conditional / not_applicable / blocked`）；原则数量不固定，新增或移除必须由触发条件、依赖和证据解释，不能删除安全不变量来缩短工作流。
- FDE 的 Echo–Delta 角色和十步交付流程仍只用于 FDE 场景；多 Skill 编排决定如何组装能力，不增加新的 FDE 角色或阶段。
- Tool Guardrail 约束每次工具调用；Convergence Gate 检查整个目标最终是否按 `Intent / Spec / Plan / Task` 收敛。
- `READY`、评测通过、单个 Skill 完成或某一工作流分支完成，都不单独等于整个目标已完成。

本标准不代替专业 Skill 执行业务工作，不补造未定义的专业规则，不因能力可发现就推断其已授权，也不要求普通用户理解工作流图、Schema 或供应商内部细节。

## 2. 标准编排链

```text
Goal
→ Skill / Capability Registry
→ Capability Match
→ Minimum Skill Set
→ Dependency Graph
→ Serial / Conditional / Parallel Assembly
→ Adapter Selection (Local / API / MCP / CLI / Plugin / Agent Endpoint)
→ Validated Inputs
→ Execution Contracts
→ Acceptance / Human Gates
→ Checkpoint / Scoped Recovery
→ Versioned Work Results
→ Evidence / Run Ledger
→ Accepted Handoff
→ Run Closure / Convergence
```

一次运行只选择对当前 Goal 有实质贡献的 Skill 或共享能力。先根据真实交接依赖确定顺序，再决定串行、条件分支或并行；不得因 Skill/能力已安装、可调用或名称相似就自动纳入。API、MCP/连接器、CLI、插件和 Agent Endpoint 是适配器，不是新的业务能力身份。

## 3. 组装原则 P14–P18

- **P14 — Registry-driven Assembly**：从已登记且有能力画像的 Skill / Capability Registry 中选择；画像至少能说明能力、触发范围、输入、输出及边界。未知能力不得臆测为已具备。
- **P15 — Minimum Necessary Skill Set**：只有移除某个 Skill 会造成明确的能力、证据、验证或交付物缺口时，才将它纳入本次运行。
- **P16 — Dependency-first Ordering**：依据输入与交接依赖建立有向依赖图，确定串行或条件顺序；不使用任意固定编号代替依赖分析。
- **P17 — Safe Parallelism**：只有分支之间不存在未解决的数据或状态依赖，且每个分支输出能独立验证时才允许并行。否则串行执行或先补依赖。
- **P18 — Result-driven Assembly**：以当前 Goal 要求的 Work Results 是否全部产生并通过验收来判断工作流是否闭合；“所有 Skill 都跑过”不是完成标准。

## 3.1 共享能力原则 C1–C8

- **C1 — Capability as a Plug-in**：共用 AI 平台、Agent、模型、工具、记忆、审批、评测、策略、缓存、调度和追踪作为可插拔共享能力；核心只依赖语义契约。
- **C2 — Transport-neutral Contract**：本地实现、脚本、API、MCP/连接器、CLI、插件和 Agent Endpoint 都是可替换传输/部署层；更换适配器不改变能力语义、权限、数据边界或验收规则。
- **C3 — Contract-ready, not network-mandatory**：Skill 必须可声明稳定输入/输出、状态、错误、证据和权限契约；只有跨进程、跨项目、共享平台或部署场景有明确收益时才选择 API、MCP、CLI 或插件，不强迫本地 Skill 网络化。
- **C4 — Explicit Adapter Registry**：每个适配器声明名称、版本、提供方、入口、依赖、权限、健康检查、兼容范围、错误/降级和回滚；供应商专属字段不得渗入核心。
- **C5 — Capability Is Not Authorization**：已发现、已安装、健康、认证成功或模型声称可用，都不等于本次任务已授权；每次运行重新检查最小作用域和人工门禁。
- **C6 — Contract and Version Compatibility**：Schema、协议、权限、数据边界或行为发生变化时建立新版本，协商后灰度；破坏性变化不得复用旧身份覆盖旧契约。
- **C7 — Fail-closed and Local Fallback**：能力、适配器、版本、权限、数据分类或证据不明时阻断/降级；仅使用已验证的本地确定性回退，不伪造空成功。
- **C8 — Evidence and Sovereignty**：记录提供方、适配器、版本、调用 ID、结果版本、实际状态变化、数据边界、验收和下一检查；本地/内部/敏感/受限/未知数据不得因 API、MCP、CLI 或插件存在而自动外发。
- **C9 — Local Render First**：图像、3D、视频和其他可确定性渲染优先使用本地代码或本地引擎；只有本地质量、性能或能力不足且证据充分时，才选择模型/远程适配器，并记录不足原因、质量/延迟/成本、数据边界、版本和回退路径。

共享能力的最小调用链为：`DISCOVER → MATCH → AUTHORIZE → INVOKE → VERIFY → RECORD → VERSION / DEPRECATE`。字段和适配器最低契约见 `references/shared-capability-contract.md`；API、MCP、CLI 和插件调用均不得绕过 Tool Guardrail。

## 3.2 Agent 分工工作流：最小分工决策

本节吸收外部 `agent-division-workflow` 资料中的可复用模式，但不复制其独立 Skill、课程叙述或任何 ADK 运行时。它是本标准的一个条件分支：只有真实任务需要多个职责、依赖、并行收益或独立验收时才启用。

### 分工门控

1. 先绑定一个每天/每周可重复的真实任务，并写明触发、输入、Required Work Results、失败时谁停；缺少真实任务时 `CLARIFY`。
2. 一次工具调用能完成的任务，不建 Agent；一个 Agent 能安全串完的任务，不拆多 Agent。
3. 只有步骤类型不同、存在明确依赖/并行收益/独立验收或专职能力边界时才分工；“多角色看起来更专业”不是理由。
4. 分工仍须通过外层 `Execution Verdict`、动态 `Principle Profile`、Tool Guardrail 和 Convergence Gate；分工单通过不等于已授权、已执行或已完成。

### 五种且仅五种分工模式

| 模式 | 使用条件 | 不使用条件 | 约束 |
| --- | --- | --- | --- |
| `Router` | 入口意图不稳定，需要分到不同专职能力 | 路径只有一条 | Router 只负责路由和边界检查，不替专职能力执行 |
| `Sequential` | 后一步依赖前一步产物或验收 | 步骤可独立并行 | 每条依赖边写明输入版本、验收和下游消费者 |
| `Parallel` | 分支互不依赖，且结果可独立验收后汇总 | 有未解决的输入、状态或数据依赖 | 并行前检查冲突；不能用并行掩盖缺失依赖 |
| `Loop` | 生成结果后需按可判定标准反复修正 | 没有达标条件或无法验证改进 | 必须同时声明退出条件、最大次数、失败返回和最近检查点 |
| `Agent-as-Tool` | 编排者按需点名调用专职 Agent/Skill | 专职 Agent 还需自行开启未受控长循环 | 调用对象、输入/输出、权限、证据和 POST CHECK 必须明确 |

不得自造第六种模式。模式名称只描述编排结构，不绑定 ADK、SDK、供应商或部署平台；在本标准中分别映射为条件路由、串行依赖、安全并行、有界收敛循环和显式能力调用。

### 角色与通信契约

每个角色/Skill/Agent 一行声明：`输入`、`输出`、`工具`、`作用域`、`证据`、`禁止事项` 和 `失败返回`。编排者只路由、传递约定字段、执行验收和处理恢复，不隐式承担专职角色的业务工作。

跨角色通信只允许以下三类，按最小必要原则选择或组合：

- `shared session state`：同一 Run 的约定字段和状态交接；
- `LLM delegation`：父级把明确边界的子任务委派给子 Agent；
- `explicit invocation`：代码或编排契约点名调用某个 Skill/能力。

不得跨角色复制整段历史上下文；传递原始正文前必须重新检查数据分类、作用域和泄露风险。

### Session、Memory Bank 与工具边界

| 层/接口 | 可保存或使用 | 禁止事项 |
| --- | --- | --- |
| `Session` | 本次输入、当前状态、中间字段、检查点和本轮决定 | 不把它默认为跨会话长期事实；不存凭证或无必要敏感正文 |
| `Memory Bank` | 已确认、可追溯、跨会话仍有价值的偏好、稳定结论、契约和版本 | 不直接写入原始长对话、未核实推测、临时日志、凭证或客户原始数据 |
| 函数/API | 一个已知、调用方式固定的接口 | 不因每增加一个后端就复制适配器并称为新架构 |
| CLI | 本地进程、子进程或 Harness 插件桥接，stdin/stdout 可结构化 | 不把秘密放入 argv；必须声明版本、退出码、超时、权限、数据边界和证据 |
| MCP/连接器 | 多个后端需要共同工具协议的能力集合 | 不把单个 REST 接口包装成 MCP；必须声明服务器、工具、只读/可写和批准边界 |

写入 `Memory Bank` 前先从本轮证据中抽取事实，记录来源、版本、写入者、读取者、数据分类、保留期限和回滚方式。记忆层不改变底座的数据主权和 Tool Guardrail 约束。

### 三堵墙的最小对策

| 风险墙 | 现象 | 分工工作流必须采取的动作 |
| --- | --- | --- |
| 上下文退化 | 窗口变长后丢失目标、边界或验收 | 只传约定字段；定期摘要替换原文；稳定指令/Schema 放入共享前缀，动态内容放后缀 |
| 无持久状态 | 新会话从零开始或中途漂移 | 用 `Session` 保存当前 Run，用 `Memory Bank` 保存已验证跨会话事实，用检查点保存可恢复状态 |
| 无自检 | 不知道是否达标，循环空转 | `Loop` 必须有可判定退出条件、最大次数、POST CHECK 和失败返回；没有验收证据不得循环或报完成 |

未跑过的步骤、未验证的模式和未上线的能力必须明确标记 `未验证`；设计存在不等于执行存在，执行存在不等于验收通过。

## 4. 执行前组装验证 P19–P24

**P19 — Assembly Before Execution**：任何自动生成或人工拼装的工作流都必须先验证，不能因“结构看起来可运行”便开始执行。至少检查：

1. **P20 — Coverage Validation**：每项必需目标、能力和 Work Result 都有唯一负责 Skill，或有明确 Human Gate；未覆盖项必须阻断或澄清。
2. **P21 — No Redundant Skill**：每个已选 Skill 都能说明其关闭的具体缺口；冗余 Skill 应移除。
3. **P22 — Handoff Integrity**（与 P16 依赖排序配套）：每条依赖边说明上游输出/版本、交接状态、验收条件及下游消费者。
4. **P23 — Parallel Safety Validation**（落实 P17）：验证没有未满足的输入、数据或共享状态依赖，并且每个并行输出可独立验收。
5. **P24 — Deliverable Closure**（落实 P18）：每项 Required Work Result 都有生产者、可检验的验收规则和可追溯来源；缺一项不得判定工作流可执行。
6. **恢复范围**：标出有效检查点、失败影响范围与可局部重跑的依赖子图；无法安全恢复时先澄清，不做盲目重跑。

`Assembly Verdict`（组装验证结论）输出 `PASS`、`NEEDS_REVIEW` 或 `BLOCKED`：

- `PASS`：结构覆盖与依赖检查通过，工作流在结构上可执行；仍须满足外层 `Execution Verdict = GO`、输入验证、权限和人工门禁。
- `NEEDS_REVIEW`：需要人确认某个明确的范围、依赖、例外或验收判断；确认前不得把相关节点当作已授权。
- `BLOCKED`：关键能力、输入、依赖、权限或验收缺失；停止执行并给出可读阻断原因和下一步。

只有 `Assembly Verdict = PASS` 且必需输入、权限与执行前人工门禁均已闭合时，Assembly 状态才能为 `READY`；有待确认项时为 `NEEDS_REVIEW`，存在阻断项时为 `BLOCKED`。即便 Assembly 为 `READY`，仍须由外层 `Execution Verdict = GO` 授权进入执行。

## 5. 单个 Skill 的执行契约 P25–P32

开始一次 Skill Run 前，声明该次运行的契约；至少包括：

- Run Goal；
- Required Inputs 1..N 与 Optional Inputs 1..N；
- 输入可用性验证和 Work Scope；
- Expected Results 1..N、各自唯一生产者与 Acceptance Gates；
- Evidence Requirements 与 Human Gate Conditions；
- Failure Return；
- Checkpoint / Resume Point；
- Downstream Handoff；
- Final Run Status。

规则如下：

- **P25 — Contract Before Execution**：目标、必需输入或作用范围不充分时，不启动执行。
- **P26 — Input Validity**：文件/值存在不代表可用；按声明检查完整性、格式、来源、时效、权限与任务适用性。
- **P27 — Explicit Result Ownership**：每个预期结果有且仅有一个负责生产者及验收规则；允许协作，但不能责任悬空。
- **P28 — Safe Failure Return**：失败返回业务可读信息：失败点、仍有效的结果、受影响范围、所需下一步和可恢复位置；不得伪装成功。
- **P29 — Human Gate by Exception**：仅在契约声明的条件触发时请求人工确认；常规步骤不重复打断用户。人工批准只适用于明确的对象、范围、参数和状态。
- **P30 — Accepted Handoff Only**：下游默认只能消费通过上游必需验收的结果；例外必须事先声明为可审查的受限路径，并保留批准与证据。
- **P31 — Resume, Not Restart**：发生可恢复失败时，从最近有效检查点继续，只重跑受影响依赖范围；不得覆盖失败历史或重跑无关分支。
- **P32 — Run Closure**：Required Results、验收、证据和交接状态都闭合后，单次 Run 才能标记完成。

## 6. 运行状态与结论不可混用

| 状态类型 | 取值 | 表示什么 | 不表示什么 |
|---|---|---|---|
| 外层 Execution Verdict | `GO / CLARIFY / STOP` | 任务是否允许进入执行 | 工作流图已验证或结果已产生 |
| Assembly Verdict（组装验证结论） | `PASS / NEEDS_REVIEW / BLOCKED` | 工作流结构是否覆盖目标且可安全执行 | Skill 已运行或结果已验收 |
| Assembly 状态 | `READY / NEEDS_REVIEW / BLOCKED` | 当前组装是否达到对应准备状态 | `GO`、执行成功或目标完成 |
| Run 状态 | `READY / RUNNING / NEEDS_REVIEW / BLOCKED / FAILED / COMPLETED` | 单次 Run 的实际执行状态 | 其它 Run 或整个父目标的状态 |
| Work Result 验收 | `PASS / FAIL / NEEDS_REVIEW / BLOCKED` | 某个特定版本结果是否满足其规则 | 整个 Run 或父目标已收敛 |
| Convergence | `CONVERGED / NOT_CONVERGED` | 整个目标与当前实现的差距是否闭合 | 仅由局部测试通过自动推得 |

每个状态必须指明对象、范围和依据。Assembly `READY` 仅表示组装就绪；规划型 Runtime 的 `READY` 也只表示其明确定义的规划状态。两者都不等于执行、审批、生产推广或 Convergence。`COMPLETED` 只表示单次 Skill Run 按契约闭合；父目标仍需检查所有 Required Work Results、验收证据及底座 Convergence Gate。

## 7. Run State + Evidence Ledger P33–P40

重要运行事实以追加事件记录，不用新状态覆盖形成它的历史。每次状态或结果变化都指向证据，或明确说明证据不适用。

- **P33 — Event, Not Overwrite**：保留关键状态、验收、交接、失败与恢复事件的先后关系。
- **P34 — Evidence-linked State**：重要状态/结果转换附证据引用；无证据时标出原因和限制。
- **P35 — Versioned Results**：结果改变即生成新版本；之前已接受或拒绝的版本仍可追溯。
- **P36 — Acceptance is an Event**：记录 `PASS / FAIL / NEEDS_REVIEW / BLOCKED`，并包含目标版本、规则、证据、决策者与时间。
- **P37 — Handoff Lineage**：下游可追溯实际接收的上游结果版本、验收状态与证据。
- **P38 — Checkpoint from Valid State**：检查点仅能从已知有效状态创建，并标出可恢复范围。
- **P39 — Recovery Lineage**：保留 `failure → checkpoint → rerun → revalidation → new result/version` 链路，不能抹去失败。
- **P40 — Derived Current State**：当前状态可从账本事件重建；单个“当前状态”字段不能取代事件来源。

账本最小字段：Run ID、事件顺序/时间、事件类型、对象与前后状态、参与者/Skill、结果版本、验收状态、证据引用、检查点/恢复范围。宿主若没有事件存储，使用最小本地运行记录；只保留必要元数据，不复制敏感正文或凭证，按数据分级设置访问与留存。

## 8. 共享能力接入与非目标

多 Skill 工作流选择共享能力时，先在 Capability Registry 中匹配能力契约，再选择适配器；不要把 API、MCP/连接器、CLI、插件或 Agent Endpoint 直接当成新的 Skill。适配器必须携带能力身份、版本、Schema、权限/作用域、数据分类、健康、证据和回退声明，并按 `DISCOVER → MATCH → AUTHORIZE → INVOKE → VERIFY → RECORD` 执行。

一个本地 Skill 要不要 API 化、MCP 化、CLI 化或插件化，按真实复用、隔离、权限、部署和跨进程需求判定。只在有明确收益且通过 Step 0 时增加适配器；保持本地运行的 Skill 仍需契约可接入，但不被强制网络化。共享 AI 平台或 Agent 能力不可用、未授权、版本不兼容或 POST CHECK 失败时，工作流只能进入 `BLOCKED` / `DEGRADED` 或已验证的本地回退。

## 9. 普通用户结果视图与非目标

普通用户默认只需看到：要完成什么工作、还缺哪些必需材料、哪些事项需人工确认、已产出的 Work Results，以及失败影响与下一步。事件 ID、哈希、Provider 细节和原始 Schema 按需披露。

本标准定义的是可审查的工作流与共享能力契约，不是自动执行器、调度器、Skill/Capability Registry 产品或多 Agent 框架；不得为实现这些原则而增加新的运行时依赖。任一环节失败时，返回已验证结果、未闭合范围与安全恢复路径，并继续执行数据主权及 Convergence 门禁。
