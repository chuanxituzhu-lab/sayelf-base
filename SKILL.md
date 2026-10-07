---
name: sayelf-base
description: "Use when deciding or delivering changes to Agents, Skills, tools, systems, features, data flows, evaluations, prompts, shared AI capabilities, API/plugin adapters, agent-division workflows, or FDE deployments. Provides build gates, local-data protection, provider-neutral runtime guardrails, capability contracts, workflow evidence, convergence, and delivery standards. Chinese triggers: 总底座 / 底座 / 共享底座 / 走底座 / 构建门禁 / 共享能力 / 分工工作流 / 多Agent分工 / MCP和API / 记忆和Loop / AI平台接入 / Agent接入 / API化 / 插件化 / FDE标准. Not for ordinary consultation, non-engineering writing, or routine SaaS configuration."
metadata:
  short-description: 共享总底座（构建门禁 + 共享能力契约 + 分工编排 + FDE 内容标准）
  aliases: [总底座, 底座, 共享底座, 走底座, 按底座来, 构建门禁, 共享能力, 分工工作流, 多Agent分工, MCP和API, 记忆和Loop, AI平台接入, Agent接入, API化, 插件化, FDE标准]
---

# SAYELF 共享总底座

> 当前内容版本：1.1.1。版本信息保留在正文，避免进入 Agent Skills 校验器不允许的 frontmatter 字段。

> **调用名：`sayelf-base`**（斜杠调用 `/sayelf-base`）。口头说「总底座」「走底座」「按底座来」「构建门禁」「共享能力」「AI 平台接入」「Agent 接入」「API 化」「插件化」「FDE 标准」也应触发。

## Purpose

单一权威底座，两层合一，解决两类不同问题：

| 层 | 回答什么 | 来源 |
|---|---|---|
| **Gate 构建门禁层** | 该不该建、怎么建、边界在哪、能否安全执行与交接 | 动态核心原则注册表（Step 0 + Execution Verdict + 12 步序列 + 17 项决策记录） |
| **Standard 内容标准层** | 如何组装共享能力与多 Skill/Agent、按什么流程交付、交付成什么样、怎么验收与沉淀 | 共享能力契约 + 通用多 Skill/Agent 分工编排 + FDE 分工工作流 + Skill 标准 + Agent 评测集 |

**层级关系**：Gate 层凌驾 Standard 层。Standard 层的每一步（场景选择、原型、生产化、资产沉淀）都受 Gate 层约束——本地优先、数据主权、证据驱动、WebUI 非默认。

**约束强度：硬门禁**。本文件所有"严禁 / 必须 / fail-closed"条款是不可协商的停止条件，不是建议。裁剪只允许发生在 `references/`、`assets/`、`scripts/`、`tests/` 四个可插拔目录，不允许发生在门禁条款本身。

渐进式披露：本文件为 L2 主指令（`references/` 是 L3 按需加载，`assets/templates/` 是填写模板，`tests/` 是可执行评测）。

## Use this skill when

- 新建或重大修改 Agent、Skill、Tool、System、产品能力、人机 WebUI；
- 新增架构、依赖、集成、插件边界、自动化回路、模型或云服务；
- 新增或改变数据流、外部 API、遥测、上传、同步——任何可能移动本地或敏感数据的动作；
- 需要立项门禁：场景选择、进门标准、MVP 边界锁定、价值量化；
- 需要设计评测集、评分器、验收标准或出口门；
- 需要判断一项交付是否属于 FDE 场景、Echo 与 Delta 如何分工；
- 需要把重复任务拆成最小 Agent 分工，选择 Router / Sequential / Parallel / Loop / Agent-as-Tool，并定义 Session、Memory Bank、API/MCP 和退出条件；
- 需要设计、迁移、调试或迭代生产提示词，并建立可复现的评测基线；
- 项目结项前的资产沉淀、知识转移与退出标准检查；
- 需要提高 Codex、代码代理或其它大模型的提示/上下文缓存命中率；
- 审查既有 Skill / Agent 是否符合标准（用本文件当 checklist）。

不适用：纯业务咨询与调研、无工程产出的文档写作、纯远程标准化 SaaS 配置（见 §5 适用边界）。

**默认不建 WebUI**。先判断真实功能是否需要人机可视化界面；不需要就不建，用宿主原生交互、CLI、API 或后台工作流。

## Operating contract

### §0 硬门禁：编码前必须输出「构建决策记录」

写代码前，在任务计划 / issue / 设计说明中给出以下 17 项及 `Execution Verdict`。**缺失"可度量改进或差异点"= 停止信号，不得开工。**

```text
1  真实任务（用户到底要什么结果）:
2  最接近的既有能力（工作区内 / 开源 / 已装 Skill）:
3  Step 0 判定: Duplicate | Integrate | Improve | Differentiate | Innovate
3a Execution Verdict: GO | CLARIFY | STOP（证据不足不得 GO）:
4  可度量改进或差异点（本地控制/token/延迟/成本/依赖数/兼容性/可靠性/证据质量/自动化边界/可用性，至少一项）:
5  成功度量与判定证据:
6  最小内核（缺了就不成立的部分）:
7  插件边界（可裁剪、可替换的部分）:
8  本地优先边界（什么必须本地跑，什么允许上云，理由）:
9  数据分级与信任边界（Public/Internal/Sensitive/Restricted/Unknown）:
10 是否公开发布: 是 | 否
11 外发计划（目标、字段、脱敏、授权、留痕）:
12 状态与下一次检查的触发条件:
13 观测 / 推断 / 假设 / 事实 的边界:
14 演进 · 验证 · 灰度 · 版本 · 回滚计划:
15 WebUI 决策: Required | Not required —— 理由:
16 最简可靠实现（技术选型与依赖）:
17 明确不做（显式排除）:
```

不适用项写 `N/A` 并给理由。小型本地改动按比例裁剪，不要为了凑格式编造大型决策记录。

### §1 Step 0 创新门禁

先搜 GitHub、开源生态与当前工作区，按 **搜索 → 比对 → 提炼 → 差距分析 → 差异化 → 判定** 执行，然后归入且仅归入一类；完成分类后再给出 **Execution Verdict**：`GO | CLARIFY | STOP`。这两个判断不可混同：Build Decision 说明“属于哪类变化”，Execution Verdict 说明“现在是否允许进入执行”。

| 判定 | 判据 | 允许动作 |
|---|---|---|
| **Duplicate** | 成熟方案已解决真实任务，无实质差距 | 复用，不得重建 |
| **Integrate** | 现有部件可满足，只缺组合或接口 | 连接，不得重写部件 |
| **Improve** | 既有方案存在具体、可度量的弱点 | 只做最小可验证优化 |
| **Differentiate** | 有近似方案，但机制或流程实质不同 | 围绕差异点做聚焦 MVP |
| **Innovate** | 未找到有效匹配方案 | 先验证原始假设，再扩展 |

**Improve 是自研的最低门槛。**“更好、更智能、更完整”不是证据。

### Step 0 Execution Verdict

- **GO**：仅当真实任务、成功度量、最小边界、数据/权限边界与所需证据均已明确，且现有证据足以支持该 Build Decision；允许进入限定范围的执行。
- **CLARIFY**：存在已命名但未解决的关键未知、冲突或证据缺口；不得开始实现，必须先补证据、澄清约束或重算判定。
- **STOP**：判定为 `Duplicate` 且已有能力可直接复用，或存在安全、权限、数据主权、不可逆风险或证据已否定可行性的阻断；不得进入构建，并记录复用、降级或终止路径。

**证据不足一律 `CLARIFY`，不得 `GO`。** `Duplicate` 不得借 `GO` 进入重复构建；`Integrate`、`Improve`、`Differentiate`、`Innovate` 也必须分别具备可追溯的组合证据、度量基线、差异证据或假设验证证据。Verdict 必须写入决策记录，并成为后续状态的进入条件。

### §2 核心构建原则（动态原则集摘要，完整版见 `references/build-principles.md`）

原则数量不固定。`P01–P08` 是当前默认基线注册项，不是永久的八项清单；任务会依据触发条件、数据/权限风险、交付阶段和所需证据，自动生成最小适用原则集（Principle Profile）。每个注册项至少记录 `id`、名称、适用范围、触发条件、依赖、不变量、所需证据、状态和版本。

原则状态只能明确记录为 `mandatory`（强制）、`conditional`（条件触发）、`not_applicable`（有证据证明不适用）或 `blocked`（缺证据/冲突/风险阻断）。先识别任务触发器，再匹配注册表、补齐依赖、锁定安全不变量，最后把本次原则 Profile 写入构建决策记录；任务变化时重新计算。新增原则以新注册项加入，移除原则必须有不适用证据且不得破坏不变量，不能为缩短文档而静默删除。

以下不变量不受原则数量调整影响：权限、作用域、敏感数据、破坏性动作和外发检查必须 fail-closed；凭证不得外发；提升/交接前必须有证据；未收敛不得报完成；变更必须可版本化、可追溯、可回滚。证据不足时 `Execution Verdict` 只能为 `CLARIFY` 或 `STOP`，不得 `GO`。

1. **负熵**：只保留真实任务与证据链所需的 对象 + 功能 + 交互；删架构熵、功能熵、交互熵。默认用户路径 `打开 → 输入 → 执行 → 结果`。
2. **模块化可插拔**：核心与平台无关；AI Harness 与共用 AI 平台/Agent 能力视为**可替换适配器**，最小双向契约见 §2.1 与 §2.3；共享能力先复用再自研；能力可用 ≠ 已授权。
3. **本地优先**：确定性规则、解析、指标、缓存、索引、去重、状态管理默认本地；云与模型依赖需证据。
4. **状态驱动**：禁止默认固定轮询；按 `状态 → 变化率 → 重要性 → 下次检查` 决定节奏。
5. **智能自动化**：可 `发现→采集→处理→比对→检出→假设→建议`，但 **观测 / 推断 / 假设 / 事实** 必须分层，未验证假设不得升格为事实。
   状态名只对其明确的对象与门槛有效：`selected / planned / executed / reviewed`、`READY`、`CONVERGED` 与 `PROMOTED` 不可互相替代。登记/选择不等于加载/执行；未建立的 follow-up 必须显式保留，父级任务不据此宣称完成。规划型 Agent Runtime 的映射见 `references/agentops-alignment.md`。
6. **证据驱动演进**：`观察 → 挑战 → 验证 → 灰度 → 提升`；可版本、可追溯、可回滚；无验证不提升。
7. **WebUI 仅作人机界面**：先论证是否需要；需要时按 `输入 → 处理 → 证据 → 状态 → 决策 → 动作 → 结果` 设计，高级控制渐进披露。
8. **本地与敏感数据主权**：本地读取的数据默认留在本地信任边界内；凭证永不上传；GitHub 与公共网络只放行显式 `Public` 内容，发布前复查 staged diff 与每个发布物；缺失分类/授权/留存/查泄证据即阻断。

**§2.1 Harness 最小契约**：任务输入与结果输出、能力发现、工具调用、状态与检查点、事件、暂停/恢复/取消、人工批准、错误与重试、用量、本地可查证据。核心不得依赖特定供应商的循环、事件结构或托管控制面。

### §2.3 共享能力与 API / 插件化契约（provider-neutral）

共用 AI 平台、Agent、模型、会话、记忆、评测、审批、策略、缓存、调度和追踪等，统一视为**共享能力（Shared Capability）**。核心只依赖稳定的能力契约，不直接依赖某个平台的 SDK、Agent 循环或托管控制面。共享能力可由本地实现、脚本/MCP/连接器、HTTP/API 服务、插件包或 Agent Endpoint 提供。

**Skill 的结论**：Skill 必须“契约可接入、适配器可替换”，但不要求每个 Skill 都变成网络 API。单机、本地、低风险 Skill 可以继续以本地目录/脚本运行；当 Skill 需要跨项目复用、跨进程调用、接入共享 AI 平台或作为 Agent 能力暴露时，再通过 API 或插件适配器发布。API 化/插件化是传输与部署层，不改变 Skill 的语义身份、数据边界和验收规则。

**统一能力生命周期**：

```text
DISCOVER → MATCH → AUTHORIZE → INVOKE → VERIFY → RECORD → VERSION / DEPRECATE
```

每个共享能力至少声明以下契约：

- `capability`：稳定名称、能力类型、版本、提供方/实现、适用范围与不适用范围；
- `interface`：输入/输出 Schema、同步/异步/流式模式、超时、取消、幂等、重试、分页或批处理规则；
- `access`：所需权限、最小作用域、租户/资源边界、人工批准条件、速率/用量限制；
- `data`：输入/输出数据分类、允许的信任边界、是否允许外发、保留/删除要求；
- `evidence`：调用 ID、结果版本、来源、检查结果、状态变化、错误/降级原因与下一检查；
- `compatibility`：协议/Schema 兼容范围、依赖、健康状态、版本替换和回滚路径。

**适配器边界**：API、插件、MCP/连接器和 Agent Endpoint 都是适配器；适配器负责协议翻译、认证、连接、健康检查、限流和生命周期，不得把供应商专属字段渗入核心。适配器不可用、能力未注册、版本不兼容、权限/数据边界未知或返回结构不完整时，必须 `blocked` / `degraded` 或回退本地确定性路径，不得伪装为成功。

**API / 插件化最低要求**：

1. 能力有稳定身份与版本；同一能力不同适配器仍能映射到同一语义契约；
2. 调用前完成能力发现、版本/Schema 协商、权限、作用域、数据分类与人工批准检查；
3. 调用后验证结构、泄露、证据、实际状态变更和结果版本；
4. 插件声明入口、配置、依赖、权限、资源、健康检查、错误/降级和卸载/回滚；API 声明认证、超时、幂等、错误、限流、版本和撤销；
5. 共享能力只能获得本次任务的最小权限，不得借由 API、插件、Agent 或连接器扩大数据出境、持久化、遥测或工具访问；
6. 能力注册、启用、批准、版本升级和替换均留有本地可查证据；“发现/登记/可调用”不等于“已授权/已执行/已验收”。

详细字段、适配器矩阵与示例见 `references/shared-capability-contract.md`。

### §2.2 Tool Guardrail Contract（provider-neutral）

Harness / Runtime 对每一次工具调用都必须执行同一份三段式契约；工具可由任何供应商或本地实现提供，但不得绕过契约：

```text
PRE CHECK → EXECUTE → POST CHECK
```

| 阶段 | 必查内容 | fail-closed 结果 |
|---|---|---|
| **PRE CHECK** | 工具身份/版本；调用者权限与最小作用域（资源、动作、租户、时间）；输入结构；敏感数据分类与出境边界；破坏性/不可逆动作；人工批准要求；当前状态、幂等性与回滚条件 | 权限、作用域、数据分类、批准或证据任一未知/被拒/过期时，不执行；批准后的状态或参数发生变化时，必须在执行前重新检查。 |
| **EXECUTE** | 只执行已批准的精确调用；禁止静默扩大工具、权限、持久化、遥测或数据出网；记录调用 ID、输入摘要、批准、实际副作用与错误/重试状态 | Harness 不可用、能力未授权、调用不匹配或执行状态不明时，返回 `blocked` / `degraded`，不得伪装成功，不得污染核心状态。 |
| **POST CHECK** | 输出结构；敏感信息/凭证/本地数据泄露；结果与证据是否一致；实际状态变更、未变更或部分变更；回滚与下一检查条件 | 输出不合结构、疑似泄露、证据不足或状态不一致时，隔离/脱敏输出并返回非零 `code`；不得把结果接受为后续模型输入、持久化状态或 handoff 完成证据。 |

工具门禁沿用统一返回结构 `{code, msg, data}`。`data` 至少保留 `tool`、`call_id`、`permission`、`scope`、`approval`、`evidence`、`data_classification`、`state_change` 与 `next_check`；缺失字段视为不完整结果。能力可用不等于已授权，人工批准也不替代执行前的最终复核。

**简单优先序列**：既有能力 → 原生方案 → 轻量工具 → 成熟依赖 → 复杂框架 → 自研复杂技术。

### §3 12 步强制开发序列

发现（Step 0 搜索、分类与 Execution Verdict 留痕；证据不足不得 GO）→ 定义真实任务与成功度量 → 做减法 → 选最简实现并声明不做什么 → 界定最小内核与插件边界 → 决定本地/云边界 → 数据分级与外发管控 → 状态与变化建模 → 界定自动化与证据层级 → 决定是否需要 WebUI → 只实现最小可出结果的切片；每次工具调用执行 `PRE CHECK → EXECUTE → POST CHECK` → 聚焦验证并复查数据泄露，经 Convergence Gate 收敛，再通过验证/灰度/版本/回滚才提升或交接。

规划型运行时可以报告 `READY`，但必须指出它代表的对象和已验证条件；没有执行器或证据时，不得把计划就绪解释为产物已交付、Convergence、批准或生产推广。跨岗位 follow-up 尚未创建时，显式呈现 `NOT_CREATED` 并保留父级未完成范围；不得暗示已经调度或执行。

### §4 Skill 内容标准（详见 `references/skill-standard.md`）

**目录结构（§1.5 标准）**：`SKILL.md`（必需）+ `scripts/` + `references/` + `assets/` + `tests/`（后四项可选、可裁剪）。

**YAML 契约**：`name`（kebab-case、≤64、与目录名一致）+ `description`（`Use when...` + 触发场景 + 核心功能 + 不适用场景，≤1024）；可选 `version` / `license` / `compatibility` / `allowed-tools`。

**7 项设计原则**：① 只处理模糊逻辑，确定性操作下沉脚本/MCP；② 渐进式披露（L1 元数据 <100 tokens，L2 正文 <5k tokens，L3 按需）；③ description 显式含高频触发词；④ 指令绝对化，命令式动词，消灭"你应该/我建议"；⑤ 明确边界——否定约束、失败路径、安全阈值；⑥ 工程化闭环，`tests/` 含正例/反例/边缘；⑦ 最小够用，只写模型不知道的。

**5 种设计模式**：Tool Wrapper / Generator / Reviewer / Inversion（先提问后执行）/ Pipeline（硬检查点）。

### §5 FDE 分工工作流（详见 `references/fde-standard.md`）

**三要素判别（缺一即非 FDE）**：① 承担生产级代码与可运行系统；② 直接接触真实用户、真实数据与真实系统约束；③ 现场模式抽象为平台能力回流。本质是 **交付业务结果而非交付软件**。

**Echo（部署策略师）** 管"该做什么"，**Delta（部署工程师）** 管"怎么做出来"；两人现场作为整体单元协同，不是分阶段接力。

**10 步闭环**：

| 步 | 阶段 | 负责 | 输出物 |
|---|---|---|---|
| 1 | 场景选择 | Echo | 场景优先级清单 |
| 2 | 业务发现 | Echo | AI 机会地图、量化验收指标 |
| 3 | 技术定界 | Delta | 技术方案 + MVP 范围 |
| 4 | 系统设计 | Delta | 系统架构图、接口清单、权限矩阵 |
| 5 | 快速原型 | Delta | 可运行原型（60-90 天，30-60 天见改进） |
| 6 | 评测体系 | Delta | 评测集 JSON、评分器、验收报告模板 |
| 7 | 生产化 | Delta | 生产部署包、SLA/SLO、运维手册 |
| 8 | 用户采用 | Echo | 采用率报告、反馈汇总、迭代计划 |
| 9 | 资产沉淀 | Echo + Delta | 可复用资产包 |
| 10 | 商业扩展 | Echo | 行业 Solution |

**硬门禁（fail-closed，不可协商）**：

- 严禁跳过 Step 1-3 直接进入开发；
- MVP 范围必须在 Step 3 锁定，后续变更走变更流程；
- 所有生产部署必须先过 Step 6 评测体系验证（离线评测集通过率 ≥80%）；
- Step 9 资产沉淀为必选项，不可省略；
- 敏感数据操作必须在 Step 7 完成脱敏与权限对齐；
- **不碰终局决策**——客户要求 AI 直接做最终审批/战略决策，应拒绝并改为 Human-in-the-loop 辅助；
- 进门标准五项全过才可立项：低风险 × 高频 × 可量化 × 数据在客户手里 × 不碰终局决策（+ 明确业务 Owner）；
- 出口门：系统在无 FDE 工程师触碰下**稳态运行一整周**且业务指标持续达标，方可结项。

**适用边界**：产品形态未成行业共识、客户流程高度敏感差异大、单客户价值高、强合规（金融/政务/医疗）、遗留系统陈旧需求多变 → 适用；标准化配置可覆盖、工作流同质、客户分散低价值、无强合规、系统现代化需求稳 → 不适用。

**资产回流**：可回流 通用软件组件 / 通用语义资产 / 脱敏元资产 / 方法论资产；**红线（禁回流）** 客户原始数据与单据、独有审批与保密规则、客户专属定制代码、隐性业务知识。

### §5.1 通用 Agent 分工工作流（详见 `references/workflow-orchestration.md`）

这不是新的运行时或角色框架，而是多 Skill/Agent 编排时的最小决策契约：先绑定一个重复任务；一次工具调用能完成就不建 Agent，一个 Agent 能完成就不拆多 Agent；只有存在明确的不同职责、依赖、并行收益或独立验收时才分工。

只使用五种模式：`Router`（入口不稳定）、`Sequential`（后一步依赖前一步）、`Parallel`（互不依赖后汇总）、`Loop`（对照标准迭代且有条件与次数上限）、`Agent-as-Tool`（编排者点名调用专职能力）。每个角色必须声明输入、输出、工具和禁止事项；编排者只路由与验收，不替专职角色隐式做活。

通信只允许 `shared session state`、`LLM delegation`、`explicit invocation`；跨角色只传约定字段，不复制整段上下文。记忆分为本轮 `Session` 与跨会话、已验证事实的 `Memory Bank`；原始长对话、未核实推测、凭证和敏感正文不得直接进入长期记忆。已知单一接口优先函数/API；仅当多个后端需要共同工具协议时才选择 MCP，并声明服务器、工具、读写权限和批准边界。

每个分工工作流必须处理三堵墙：上下文退化（字段化交接与摘要）、无持久状态（Session + Memory Bank + 检查点）、无自检（Loop 必须有退出条件；无可判定验收不得循环）。未验证步骤必须标记 `未验证`，不能把课程模式或设计草图写成已上线能力。

### §6 评测与验收（详见 `references/eval-harness.md`）

- **四类覆盖**：黄金集（核心高频，要求 100% 通过）、边界集（异常/对抗）、回归集（历史 bug 固化防退化）、扩展集（`references/extended-cases-25.md`，五阶段 25 条，人工或 LLM 裁判）。
- **双轨评分**：规则校验（硬门槛、零成本）+ LLM-as-Judge（语义质量）。本底座只落地规则轨，Judge 轨留接口位不实现。
- **稳定性**：每条用例采样 N 次（建议 5 次），看通过率与分数方差，识别"时灵时不灵"。
- **数据来源优先级**：真实业务数据 70-80% > 人工专家设计 10-20% > 合成数据 5-10%。
- **分层指标**：L1 任务执行（完成率、操作准确率、端到端成功率）｜L2 会话交互（轮次、无效澄清率、转人工率）｜L3 工具使用（选择/参数/工具链准确率）｜L4 系统资源（P90/P99 延迟、Token、单位成本）｜**安全红线**（死循环率=0%、幻觉率、危险操作率）。
- **可执行评分器**：

```bash
python tests/eval_scorer.py --self-test
python tests/eval_scorer.py --cases tests/golden-cases.json --outputs <outputs.json>
```

### §7 提高缓存命中率（详见 `references/cache-hit-principles.md`）

- **稳定前缀优先**：把稳定的底座指令、Skill、项目规范、工具定义和可复用参考放在前面；把任务描述、时间戳、请求 ID、当前 diff、日志和用户专属数据放到后缀。
- **前缀必须可重复渲染**：保持字节、消息顺序、工具名称/描述/Schema、模型、服务层、结构化输出、推理强度和 verbosity 稳定；不要为每轮请求重写共享指令。
- **Codex/代码代理**：把 `AGENTS.md`、Skill 和稳定编码约定视为共享前缀；追加对话和工具结果，不反复重排历史；当前分支、工作区 diff、时间和临时日志只进入动态后缀。普通 Codex 客户端不能强制缓存命中，只能通过稳定上下文提高命中概率。
- **OpenAI API**：按模型能力选择隐式或显式 breakpoint；GPT-5.6+ 可使用 `prompt_cache_options`、显式 `prompt_cache_breakpoint` 和 `prewarm`，旧模型按官方支持使用稳定 `prompt_cache_key`/retention；用 `usage.input_tokens_details.cached_tokens` 和诊断结果验证，不能把同一会话等同于命中。
- **其它模型/代码框架**：先适配能力矩阵（breakpoint、cache key、retention、usage、diagnostics）；没有显式缓存 API 时仍执行稳定前缀、动态后缀、追加历史、稳定工具 Schema 和租户分域这五项通用规则。
- **安全与度量**：缓存键只含供应商、模型、租户/项目作用域和 Prompt 版本，不放原始用户数据；按 `cached_tokens / input_tokens`、P95 首 token 延迟、输入成本和 miss reason 评估，不用平均请求数掩盖低命中长前缀。
- **执行检查**：先运行 `python scripts/cache_prefix.py --self-test`；需要检查请求布局时运行 `python scripts/cache_prefix.py --request <request.json>`。脚本只输出结构、告警和哈希，不回显敏感正文。

### §8 提示词设计与评测先行迭代（详见 `references/prompt-engineering.md`）

- 修改生产提示词前先定义完成标准、代表性评测用例和当前基线；新稿或缺少基线时明确标为未验证，不声称可生产使用。
- 先判断失败来自指令歧义、数据缺失、模型能力、工具/代码或 Harness；每轮聚焦一个主要失败原因，再重跑完整相关评测并记录质量、安全、延迟与成本变化。
- 将角色、任务、可信数据、嵌入文档等不可信输入、策略、工具和输出契约清楚分区；XML、Markdown 标题或 JSON 结构按模型与调用方需要选用，不强制单一格式。
- 可确定性执行的硬约束、计算和查证放入代码或工具；提示词负责表达任务与工具使用条件，软偏好用明确评测标准衡量。
- 模型、提示词与 Harness 一起评估；只有当中间产物需要审查或硬检查点时，才拆成生成、评估、修复阶段。

## AI Harness boundary

- Harness（运行器 / Agent 循环 / 编排器）是**可替换适配器**，位于核心之外，fail-closed：不得静默扩大权限、工具访问、遥测、持久化或数据出网。
- 每一次工具调用必须通过 §2.2 的 **Tool Guardrail Contract**；PRE CHECK 未通过不得执行，POST CHECK 未通过不得接受输出、写入状态或交接。
- 每一次共享能力调用必须通过 §2.3 的 **Shared Capability Contract** 和 §2.2 的工具门禁；能力发现、API/插件适配和 Agent 交接不得绕过 PRE CHECK / POST CHECK。
- 共享能力（已注册工具、模型、Agent、会话、沙箱、缓存、状态、审批、策略护栏、调度、计量、追踪）先复用再自研；按稳定名称/版本/结构在运行时发现与协商，记录"哪个提供方、适配器和版本产出了哪个结果"。
- API、插件、MCP/连接器或 Agent Endpoint 只是可替换接入面；核心不得直接导入供应商循环/SDK，不得把某一适配器的可用性当成共享能力的存在性。
- 任务状态与凭证隔离；只申请最小能力与最小作用域；共享能力不可用时必须走显式 不可用/被拒/降级 路径，不得污染核心状态。
- 敏感数据脱敏与权限校验在 Harness 主循环完成，Skill 内部只做基础校验。
- 人工批准只授权同一工具、调用 ID、作用域与参数集合；批准等待期间若状态或参数改变，必须重新 PRE CHECK。
- 统一出入参：所有 Skill 返回固定三层结构 `{code, msg, data}`。
- Harness 不可用、被拒或返回不完整结构时：**回退本地确定性结果**，不得把失败当成"未发现问题"，不得损坏已有产物；工具 POST CHECK 失败时不得将结果写入后续上下文或 handoff 状态。
- 对 Harness 相关改动适用原则 06（观察→挑战→验证→灰度→提升）；对 prompts、traces、检查点、共享状态、工具输入输出适用原则 08（数据主权）。

## Validation before handoff

未完成以下检查不得报完成：

1. 存在与 §0 成功度量绑定的**聚焦验证**（不是"跑了一遍没报错"）；
2. `tests/` 用例可被评分器解析并执行；规则轨未通过的用例已逐条说明原因；
3. 显式列出**未验证的行为**、未闭合的证据缺口、回滚限制；
4. 复查 prompts、输出、错误、日志、追踪、缓存、遥测是否泄露本地或敏感数据；
5. 度量未达成时走 `观察 → 挑战 → 调整` 并留痕，**不得静默修改口径**；
6. **Convergence Gate**：以 `Intent / Spec / Plan / Task` 为意图源，与当前实现逐项 gap check；每项至少归类为 `missing`、`partial`、`contradicts` 或 `unrequested`。`missing`、`partial`、`contradicts` 必须修复并复查；`unrequested` 必须删除，或有明确授权并回写到相应意图/计划/任务。存在未处理 gap 时状态为 `NOT_CONVERGED`，不得 handoff、不得报完成。
7. 只有当必需项无未处理 `missing` / `partial` / `contradicts`，且所有 `unrequested` 已删除或有明确处置证据时，才能标记 `CONVERGED`。
8. 若为交付项目：资产沉淀已完成（Step 9）、知识转移清单已签、出口门（无触碰稳态一周）已满足。

## Handoff shape

统一返回三层结构：

```json
{"code": 0, "msg": "ok|blocked|degraded", "data": {}}
```

`data` 固定包含：

| 字段 | 内容 |
|---|---|
| `decision_record` | §0 的 17 项决策记录与 `Execution Verdict` |
| `stage_artifacts` | 当前阶段的负责人、核心任务、输出物、检查点 |
| `evidence` | 验证命令、执行结果、评测通过率与失败原因 |
| `convergence` | `CONVERGED` / `NOT_CONVERGED`、Intent/Spec/Plan/Task 对照、gap 分类、修复或处置证据 |
| `unverified` | 未测试行为、证据缺口、回滚限制 |
| `next_check` | 下一次检查的触发条件（状态驱动，非固定轮询） |
| `capability_contract` | 共享能力身份/版本、适配器、接口、权限/作用域、数据分类、兼容性、证据与回退路径；未接入时标 `N/A` |
| `adapter_evidence` | API/插件/MCP/连接器/Agent Endpoint 的发现、授权、调用、健康、结果版本、错误与回滚证据；未接入时标 `N/A` |

`code != 0` 时必须给出可读的阻断原因与降级路径，不得产出"看似正常"的空结论；`convergence != CONVERGED` 时即使局部测试通过，也不得以完成、交接或已满足意图的名义返回成功。

## 资源索引（L3 按需加载）

| 文件 | 何时读 |
|---|---|
| `references/build-principles.md` | 需要动态原则注册表、当前基线与 12 步序列的完整权威文本 |
| `references/skill-standard.md` | 写或审 `SKILL.md`、`plugin.json`、目录结构时 |
| `references/fde-standard.md` | 走 FDE 10 步、做 Echo-Delta 分工、插件化封装、Harness 接入时 |
| `references/shared-capability-contract.md` | 设计或审查共享 AI 平台、Agent、Skill API、插件、MCP/连接器和能力注册/版本/回退时 |
| `references/eval-harness.md` | 设计评测集、评分器、分层指标时 |
| `references/extended-cases-25.md` | 需要五阶段 25 条人工/裁判用例时 |
| `references/cache-hit-principles.md` | 需要优化 Codex、代码代理或其它模型的上下文缓存命中时 |
| `references/prompt-engineering.md` | 需要编写、迁移、调试提示词或设计提示词评测迭代时 |
| `assets/templates/*.md` | 需要填写调研、勘查、方案、计划、验收、ROI、知识转移、资产清单模板时（01-08） |
| `scripts/cache_prefix.py` | 需要对请求前缀、动态后缀、缓存键和命中率布局做本地确定性检查时 |
| `tests/` | 需要跑规则轨评分或扩充用例时 |
| `references/agentops-alignment.md` | 使用 WorkItem → Router → Planner → READY 的规划型 Agent Runtime、或在不同 Runtime 之间映射 READY / evidence / convergence 时 |

## 溯源

溯源：本 Skill 合并了动态核心构建原则注册表（当前基线为 P01–P08）、共享能力与 API/插件化契约、通用多 Skill 工作流编排、FDE 分工工作流、Skill 标准和 Agent 评测集（Standard）。本目录中的 `references/`、`assets/templates/`、`scripts/` 与 `tests/` 是配套的 L3 资源；本 Skill 是当前唯一权威入口。
