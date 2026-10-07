# 共享能力与 API / 插件化契约

> `sayelf-base` v1.1.1 的 L3 参考。用于把共用 AI 平台、Agent、模型、工具、记忆、审批、评测或其它可复用能力接入 Skill / Harness。本文定义语义与安全契约，不绑定具体供应商、SDK、协议或托管平台。

## 1. 目标与非目标

共享能力是可被多个任务、Skill 或 Agent 复用的能力单元。它可以运行在本地，也可以由 API、插件、MCP/连接器或 Agent Endpoint 提供。核心只依赖能力契约；接入协议由适配器负责。

本标准不要求每个 Skill 都变成网络服务，也不把“API 化”误解为把所有业务逻辑搬到云端。单机、本地、低风险、无需跨进程复用的 Skill 可以保持本地实现；只有在复用、隔离、权限、部署或接入场景有明确收益时，才增加 API/插件适配层。

不建共享平台、注册中心、调度器或 Agent 框架本身；这些是可选宿主能力。底座只规定它们接入时必须满足的边界、证据和回退规则。

## 2. 核心模型

```text
Skill / Agent / Tool intent
        ↓
Capability Registry
        ↓ discover + match + compatibility
Provider-neutral Capability Contract
        ↓ authorize + data boundary + human gate
Local Adapter | API Adapter | Plugin Adapter | MCP/Connector | Agent Endpoint
        ↓ invoke
PRE CHECK → EXECUTE → POST CHECK
        ↓
Versioned Result + Evidence + State Change + Next Check
```

“能力”是语义对象，“API/插件/MCP/连接器/Agent Endpoint”是接入方式。更换接入方式不应改变目标、输入输出含义、权限边界、验收规则或证据结构。

## 3. Shared Capability Contract

每个注册能力至少提供以下字段；字段可在宿主中映射为 JSON、YAML、代码对象或其它结构，但语义不得丢失：

```yaml
capability:
  name: example.capability
  version: 1.0.0
  kind: skill | agent | model | tool | service | policy | evaluator
  provider: local | named-provider-or-team
  adapter: local | api | plugin | mcp | connector | agent-endpoint
  purpose: "一行说明可验证的能力"
  in_scope: []
  out_of_scope: []
interface:
  input_schema: "stable reference or inline schema"
  output_schema: "stable reference or inline schema"
  mode: sync | async | stream
  timeout: "declared limit"
  cancellation: supported | unsupported
  idempotency: required | supported | not-applicable
  retry: "bounded policy and retryable errors"
access:
  permission: "minimum named permission"
  scope: "resource / tenant / action / time boundary"
  human_approval: never | conditional | always
  rate_limit: "declared limit"
data:
  input_classification: Public | Internal | Sensitive | Restricted | Unknown
  output_classification: Public | Internal | Sensitive | Restricted | Unknown
  allowed_trust_boundary: local | approved-external | none
  retention: "minimum necessary retention"
evidence:
  call_id: required
  result_version: required
  provider_and_adapter_version: required
  state_change: required
  next_check: required
compatibility:
  protocol: "provider-neutral protocol identifier"
  schema_range: "accepted range"
  dependencies: []
  health: required
  rollback: "version or adapter rollback path"
```

`Unknown` 不是可默认放行的等级。未知的权限、作用域、输入/输出分类、留存、兼容性或结果证据，按 fail-closed 处理。

## 4. 能力生命周期

### 4.1 DISCOVER

从受信任的本地注册表、宿主能力目录或明确授权的远端目录发现能力。记录名称、版本、提供方、适配器、健康状态与声明边界。不得因自然语言相似、网络上存在或某个模型声称可用，就推断能力已注册。

### 4.2 MATCH

将当前 Goal 所需能力与注册能力的 `purpose`、输入、输出、约束、数据边界和验收规则对齐。选最小必要能力集合；删除只提供重复路径或无法关闭具体缺口的能力。

### 4.3 AUTHORIZE

在调用前独立检查权限、最小作用域、数据出境、人工批准、用量、时间有效性和当前状态。能力“可发现”“健康”“已安装”“已通过认证”都不能替代本次任务授权。

### 4.4 INVOKE

适配器将统一的能力调用翻译为本地函数、API 请求、插件入口、MCP 工具/资源、连接器或 Agent Endpoint 调用。只传输最小必要字段，保留调用 ID、契约版本、实际适配器和批准范围。不得静默增加工具、权限、遥测、持久化或出网。

### 4.5 VERIFY

执行 POST CHECK：验证输出 Schema、数据泄露、证据完整性、结果版本、状态变化、幂等结果、部分成功、错误/重试和回滚条件。验证不通过时隔离或脱敏输出，返回 `blocked` / `degraded`，不得将结果写入后续上下文、持久化状态或 handoff。

### 4.6 RECORD / VERSION / DEPRECATE

记录提供方、适配器和版本；能力、Schema、权限或行为改变时建立新版本并重跑相关评测。旧版本的接受/拒绝、迁移、撤销和回滚仍可追溯。停止服务、撤销授权、健康检查失败或契约不兼容时，进入 `DEPRECATED` / `UNAVAILABLE`，不得静默切换到未审查实现。

## 5. API 适配器最低契约

API 化是跨进程/跨服务接入层。API 适配器至少说明：

- 身份认证、凭证存储位置、凭证轮换与撤销；凭证不进入 Prompt、普通日志、结果或仓库；
- 请求/响应 Schema、协议版本、错误结构、调用 ID、超时、取消、重试与幂等键；
- 资源、动作、租户、地域和时间作用域；批量、分页、流式和部分成功语义；
- 数据分类、允许的出境路径、留存与删除；是否允许服务端日志、训练、遥测或缓存；
- 健康/能力检查与具体降级路径；API 不可用时不得伪造空成功；
- 结果版本、证据引用、实际状态变化和回滚/补偿路径。

API 只暴露经过契约批准的能力，不把任意供应商 API 直接透传为高权限“万能代理”。动态 URL、Header、工具名、租户或权限的扩大属于契约变化，必须重新走 Step 0、PRE CHECK 和版本/审批门禁。

## 6. 插件适配器最低契约

插件化是将能力与适配器、资源、配置和验证一起封装，以便在宿主中发现、安装、启用、升级、停用和回滚。插件至少声明：

- 唯一名称、版本、兼容宿主范围、入口与生命周期；
- 所需 Skill/工具/API/运行时依赖及其版本范围；
- 读取/写入路径、网络、进程、凭证、遥测和持久化权限；
- 能力 Schema、健康检查、错误/降级、卸载与回滚；
- 安装前后的数据分类、校验和证据；
- 正例、反例、边界和权限拒绝测试。

`plugin.json`、`mcp.json` 或其它清单只是宿主适配格式，不是本底座的唯一标准。若宿主需要清单，按宿主格式翻译本契约；核心语义、权限边界、fail-closed 和证据要求保持不变。

## 7. Agent 作为共享能力

Agent 可以作为一个共享能力节点，但不能仅以“Agent 名称”作为接口。必须声明：

- 输入任务类型、上下文来源、可调用工具、输出结构与终止条件；
- 使用的模型/策略版本、会话/记忆范围、最大轮次/用量和并发限制；
- 人工批准、敏感数据处理、外部动作和终局决策边界；
- 中间结果、最终结果、证据、状态变化、暂停/恢复/取消和失败返回；
- 可否作为下游 Skill 的输入，以及对应验收规则。

Agent 的“规划完成”“返回文本”或“声称调用成功”不等于业务结果已产生。没有执行证据、验收通过或 Convergence，不得 handoff 或报完成。

## 8. 兼容、升级与回退矩阵

| 场景 | 允许动作 | 禁止动作 |
|---|---|---|
| 同 Schema、同权限、同验收的补丁版本 | 按声明升级，保留结果版本与回滚点 | 静默替换提供方或扩大作用域 |
| 向后兼容的 Schema 变化 | 新版本协商后灰度，旧版本可回退 | 让旧消费者接收未声明的新字段语义 |
| 破坏性 Schema/权限/数据边界变化 | 新能力版本、重新评测、人工/发布门禁 | 复用旧名称覆盖旧契约 |
| API/插件健康失败 | `UNAVAILABLE` / `DEGRADED`，走已验证回退 | 空结果伪装成功、自动切未审查能力 |
| 能力授权过期或状态改变 | 重新 PRE CHECK；必要时暂停 | 使用过期批准继续执行 |
| 结果部分成功或状态不明 | 隔离、标记、查证或补偿 | 当作完整成功写入下游 |

## 9. 与底座其它门禁的关系

- Step 0 决定复用、接入、改进或停止；将现有 API/插件直接接入时仍须判断 `Integrate`，不因“已有接口”跳过证据。
- Tool Guardrail 负责单次工具动作；Shared Capability Contract 负责能力身份、接口、适配器和生命周期；二者同时适用。
- 多 Skill 编排负责能力匹配、最小集合、依赖、并行、执行契约、验收、交接与运行账本。
- Convergence Gate 负责整个目标是否与 `Intent / Spec / Plan / Task` 收敛；共享能力本身通过不代表父目标收敛。
- 数据主权优先于 API 便利性；本地、内部、敏感、受限或未知数据不可因插件/API/Agent 的存在自动外发。
