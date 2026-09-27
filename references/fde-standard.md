# FDE 模式标准与分工工作流（三要素 / Echo-Delta / 10 步 / 插件化 / Harness 接入）

> 本文件由 `sayelf-base` 从源文档《FDE分工工作流 Skill 标准与 Agent 评测集完整文档》
> （FDE 分工工作流、Skill 标准与 Agent 评测集规范）整理，属于 **L3 按需引用**资源。
> 冲突时以 `SKILL.md` 为权威口径；源文档未被修改。

## 第三部分：FDE 模式标准

### 3.1 核心定义标准（三要素判别法）

判断一个岗位/模式是否为真正的 FDE，需同时满足以下三个要素，缺一不可：

| 要素 | 内涵 | 反例（非FDE） |
|------|------|---------------|
| **生产工程责任** | 承担生产级代码编写/评审，交付可运行系统 | 仅产出 PPT、Demo 或方案文档 |
| **客户现场问题发现** | 直接接触真实用户、真实数据与真实系统约束 | 远程开发、依赖客户口头描述需求 |
| **可复用产品反馈** | 将现场模式抽象为平台能力，回流产品团队 | 一次性项目交付，经验随人员流失 |

**本质定义**：FDE 是一种"规模化解决非规模化问题"的组织机制，核心是**交付业务结果（Outcome）而非交付软件**，通过"前线探索 + 后方沉淀"的飞轮实现从定制化到规模化的复利效应。

### 3.2 组织形态标准（Echo-Delta 双人单元）

原生 FDE 交付单元采用**双人制式、缺一不可**的协同架构：

| 角色 | 代号 | 核心职责 | 能力特质 |
|------|------|----------|----------|
| **部署策略师** | Echo | 挖掘模糊需求、定义核心问题、维护客户关系、推动组织变革 | 领域专家、业务理解、战略咨询 |
| **部署工程师** | Delta | 快速构建原型、系统对接、模型调优、迭代部署 | 全栈工程、快速实现、技术决策 |

**运作原则**：两人不是分阶段接力，而是在客户现场作为一个整体单元紧密协同作战——Echo 与业务沟通的同时，Delta 已开始搭建原型；Delta 遇技术阻碍，Echo 立即协调资源。

**团队规模**：通常以 **2-6 人的项目小队（Pod）** 形式运作，强调小编制、短周期（如 45-90 天交付周期）、高授权。

### 3.3 落地流程标准（四阶段闭环）

FDE 项目遵循"**进场 → 立项 → 交付 → 放大**"四阶段流程：

- **进场期**：需求考古、流程测绘、切口选择
- **立项期**：定义可量化验收标准、POC纪律
- **交付期**：知识结构化、人机分工设计、合规风险兜底
- **放大期**：渐进放量、信任运营、资产化复制

**关键纪律**：
- **Time-box 约束**：设定明确时间限制（如 90 天冲刺到 Production），避免无限期咨询化。
- **Demo 驱动开发**：以可运行结果验证可行性，而非依赖纸面需求文档。
- **价值量化先行**：立项时即定义可量化的验收标准（如节省人工时、提升处理速度、降低错误率）。

### 3.4 能力模型标准

#### 七项核心能力模型

1. **价值嗅觉**：判断场景频次、现有解决方式及 AI 改善幅度，评估投入产出比
2. **问题重构**：将表层需求翻译为真实业务问题（如"知识库问答"→"经验传承"）
3. **快速构建**：选对工具组合拼接，先做可验证原型，砍掉非核心功能
4. **评测和护栏**：建立评测集、设定边界与兜底策略，确保 Demo 达生产可用标准
5. **业务认知**：理解业务逻辑（流转环节与瓶颈）、组织逻辑（权力结构）、决策逻辑
6. **组织推动**：识别关键决策人，化解员工担忧，小步验证，量化价值
7. **资产复利**：沉淀场景模板、评测资产、工程连接器和 SOP

#### 四大技术能力底座

| 能力域 | 核心内容 |
|--------|----------|
| **企业数据基建** | 多源数据接入、清洗、向量化及多系统口径对齐 |
| **本体语义建模** | 定义业务对象、关系与规则，构建 AI 可理解的企业数据含义层 |
| **RAG 智能体开发** | RAG 知识库、Agent 推理、Skill 编排 |
| **RPA 业务自动化** | 调用系统接口、触发工作流，实现 AI 操作闭环 |

### 3.5 资产回流标准

#### 可回流的四类通用资产

1. **通用软件组件**：连接器、管道、重试脚本、安全中间层
2. **通用语义资产**：行业标准本体模型、通用流程模板
3. **脱敏元资产**：报错模式、推理失败案例、边界测试用例
4. **方法论资产**：行业架构、痛点体系、交付标准流程

#### 不可回流的红线

- 客户原始数据、单据
- 独有审批规则、内部保密规则
- 客户专属定制代码
- 隐性业务知识

### 3.6 适用边界标准

| 适用 FDE 的场景 | 不适用 FDE 的场景 |
|-----------------|-------------------|
| 产品形态尚未稳定成行业共识（如 AI Agent） | 产品形态已趋于稳定，可通过标准化配置覆盖 |
| 客户关键场景对本地流程高度敏感且差异大 | 客户工作流高度同质，通用 SaaS 即可满足 |
| 单个客户或单条场景价值足够高 | 客户分散、单客户价值低，适合 PLG 模式 |
| 数据高度敏感、合规要求高（金融/政务/医疗） | 数据可自由流通、无强合规约束 |
| 历史遗留系统陈旧、需求频繁变化 | 系统现代化程度高、需求稳定 |

### 3.7 成功评判标准

评判 FDE 模式是否成功，不看驻场人数、不看交付进度，只有**两个硬指标**：

1. **客户价值持续扩张**：客单价越来越高，老客户复购与转介绍占比在涨
2. **产品杠杆持续提升**：后续同类客户所需交付人力逐步变少

---

---

## 第四部分：分工工作流

### 4.1 分工工作流总览

| 阶段 | 角色/模块 | 核心任务 | 输出物 |
|------|-----------|----------|--------|
| 1. 场景选择 | Echo | 选择高价值、高频、可量化、数据就绪场景 | 场景优先级清单 |
| 2. 业务发现 | Echo | 梳理存量系统、流程瓶颈、失败成本 | AI机会地图 |
| 3. 技术定界 | Delta | 判断实现路径，定义MVP边界 | 技术方案+MVP范围 |
| 4. 系统设计 | Delta | 设计身份权限、数据层、Agent层、评估层 | 系统架构图 |
| 5. 快速原型 | Delta | 60-90天交付可见改进的Pilot | 可运行原型 |
| 6. 评测体系 | Delta | 建立黄金样本集、评分机制 | Eval Harness |
| 7. 生产化 | Delta | 鉴权、审计、压测、SLA对齐 | 生产部署包 |
| 8. 用户采用 | Echo | 灰度试点、培训、反馈收集 | 采用率报告 |
| 9. 资产沉淀 | Echo+Delta | 提炼Skill/模板/连接器 | 可复用资产包 |
| 10. 商业扩展 | Echo | 同客户扩展、同行业复制 | 行业Solution |

> Echo 负责"该做什么"（业务理解、需求定义、组织推动），Delta 负责"怎么做出来"（工程实现、系统集成、模型调优）。两者紧密协同，非分阶段接力。

### 4.2 插件化封装（Agent Plugins 1.0.0）

#### 标准插件目录结构

```
my-plugin/
├── plugin.json              # 插件清单（必填）
├── skills/                  # Skill 集合
│   ├── skill-a/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   └── skill-b/
│       ├── SKILL.md
│       └── assets/
├── mcp.json                 # MCP 服务器配置（可选）
└── com.example.client/      # 客户端扩展（可选）
    └── hooks/
```

#### plugin.json 最小配置

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-awesome-plugin",
  "version": "1.0.0",
  "description": "插件描述",
  "author": "Local team",
  "license": "MIT",
  "keywords": ["ai", "agent", "skill"]
}
```

#### mcp.json 配置示例

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

#### 跨平台兼容性

该规范由 OpenAI、AWS、Cursor、GitHub、微软、Vercel 六家共建，谷歌后续加入维护。兼容客户端包括：

- **全支持**：VS Code、Cursor、GitHub Copilot、Kiro
- **部分支持**：ChatGPT、Codex

---

---

## 第五部分：FDE Skill 标准规范（SKILL.md）

### 5.1 目录结构

```
fde-workflow-skill/
├── SKILL.md                    # Skill 主指令
├── plugin.json                 # Harness 插件清单
├── mcp.json                    # MCP 连接器配置（可选）
├── assets/
│   ├── templates/              # 输出模板（机会地图、架构图等）
│   └── eval-harness/           # 评测集模板
├── references/
│   ├── fde-10step.md           # 10步流程详细说明
│   ├── role-responsibilities.md # Echo/Delta 职责矩阵
│   └── asset-catalog.md        # 可复用资产目录
└── tests/
    ├── golden-cases.json       # 正例测试集
    └── edge-cases.json         # 边界/对抗测试集
```

### 5.2 SKILL.md 核心内容

```markdown
---
name: fde-workflow
description: "Use when planning or executing FDE (Forward Deployed Engineer) projects. Triggers: FDE项目规划、驻场交付流程设计、AI落地方案制定、Echo-Delta分工、资产沉淀路径。Not for: 纯远程SaaS交付、标准化产品配置。"
version: 1.0.0
allowed-tools: [Read, Write, Bash]
---

# FDE 分工工作流

## 触发条件
- 用户提及"FDE"、"驻场交付"、"AI落地"、"Echo-Delta"、"现场部署"
- 需要制定从业务发现到资产沉淀的完整交付流程
- 需要明确 Echo（部署策略师）与 Delta（部署工程师）的职责分工

## 执行步骤

### Step 1: 场景选择（Scene Selection）
**负责人：Echo**
- 评估场景价值：战略重要性、ROI、是否可形成行业模板
- 进门标准检查：低风险 × 高频 × 可量化 × 数据在客户手里 × 不碰终局决策
- 输出：场景优先级清单（红/黄/绿分级）

### Step 2: 业务发现（Discovery）
**负责人：Echo**
- 驻场深度调研，梳理存量系统清单与业务流程
- 识别最慢/最贵/最易错环节，量化失败成本
- 将模糊需求转化为可落地的技术目标
- 输出：AI机会地图、业务流程图、量化验收指标

### Step 3: 技术定界（Technical Scoping）
**负责人：Delta**
- 判断实现路径：LLM / 规则引擎 / 检索 / 传统软件
- 确定是否需要 RAG、Fine-tuning、Agent、Human-in-the-loop
- 定义 MVP 范围，拒绝或延后非核心需求
- 输出：技术方案文档、MVP 范围说明

### Step 4: 系统设计（Architecture）
**负责人：Delta**
- 设计分层架构：用户入口 → 身份权限（SSO/RBAC/审计）→ 数据层 → 检索层（Embedding/Chunking/Rerank/Vector DB）→ Agent层（Tool Calling/Planner/Memory）→ 模型层（选择/Fallback/Guardrail）→ 评估层 → 可观测性与部署层
- ERP场景优先插件嵌入模式，复杂跨系统任务采用工作流编排
- 输出：系统架构图、接口清单、权限矩阵

### Step 5: 快速原型（Prototype）
**负责人：Delta**
- 60-90天交付可用Pilot，头30-60天交付可见改进
- 原型需包含：前端、后端、模型调用、数据接入、权限、日志、反馈按钮
- 与客户工程师协同开发，验证用户需求、数据可用性、模型达标情况
- 输出：可运行原型、用户反馈记录

### Step 6: 评测体系（Eval）
**负责人：Delta**
- 建立黄金样本集（Golden Cases）：真实业务场景的标准输入输出
- 设计评分机制：规则校验 + LLM-as-Judge
- 定义验收标准：人工工时下降率、差错率、审批周期缩短等
- 输出：评测集JSON、自动评分器、验收报告模板

### Step 7: 生产化（Productionization）
**负责人：Delta**
- 处理鉴权与权限过滤、数据新鲜度、错误处理与Fallback
- 完成审计日志、安全合规、部署环境差异、成本控制
- 容器化打包、私有化环境部署、全链路压测
- 输出：生产部署包、SLA/SLO文档、运维手册

### Step 8: 用户采用（Adoption）
**负责人：Echo**
- 单部门灰度试点、周度版本迭代
- 推动培训、反馈收集、工作流调整、管理层汇报
- 以业务指标作为验收标准持续跟踪
- 输出：采用率报告、用户反馈汇总、迭代计划

### Step 9: 资产沉淀（Generalization）
**负责人：Echo + Delta**
- 将一次性项目转化为可复用模块：
  - Skill：原子化业务能力单元
  - 连接器：系统接口封装（ERP/CRM/知识库等）
  - 行业模板：标准化解决方案
  - Eval Harness：评测集与评分器
  - 部署Playbook：实施操作手册
- 输出：可复用资产包、产品需求文档

### Step 10: 商业扩展（Commercial Expansion）
**负责人：Echo**
- 向同客户更多部门扩展、同行业复制
- 打包成行业Solution，支持销售缩短周期
- 实现 Land and Expand
- 输出：行业Solution包、扩展路线图

## 输入输出规范

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| project_name | string | 是 | 项目名称 |
| industry | string | 是 | 所属行业（金融/制造/政务等） |
| current_phase | string | 否 | 当前所处阶段（1-10），默认从Step 1开始 |
| team_size | int | 否 | 团队人数，默认5人 |
| target_systems | array | 否 | 需对接的存量系统列表 |

**输出格式**：按阶段输出结构化报告，包含负责人、核心任务、输出物、检查点

## 边界与约束
- 严禁跳过 Step 1-3 直接进入开发
- MVP 范围必须在 Step 3 明确锁定，后续变更需走变更流程
- Step 9 资产沉淀为必选项，不可省略
- 所有生产部署必须经过 Step 6 评测体系验证
- 涉及敏感数据的操作必须在 Step 7 完成脱敏与权限对齐
```

---

---

## 第六部分：Harness 插件清单

### 6.1 plugin.json（FDE插件清单）

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "fde-workflow-skill",
  "version": "1.0.0",
  "description": "FDE（前线部署工程师）分工工作流 Skill 插件，覆盖从场景选择到商业扩展的10步闭环流程，支持 Echo-Delta 双人协同模式，内置资产沉淀与评测体系。",
  "author": "FDE Team",
  "license": "MIT",
  "keywords": ["fde", "workflow", "echo-delta", "ai-deployment", "enterprise-ai"],
  "capabilities": {
    "skills": [
      {
        "name": "fde-workflow",
        "path": "skills/fde-workflow/SKILL.md",
        "description": "FDE 10步分工工作流执行引擎"
      }
    ],
    "tools": [
      {
        "name": "scene-selector",
        "description": "场景价值评估与优先级排序工具"
      },
      {
        "name": "eval-harness-builder",
        "description": "评测集构建与自动评分器"
      },
      {
        "name": "asset-catalog",
        "description": "可复用资产目录管理"
      }
    ]
  },
  "dependencies": {
    "mcp-servers": ["filesystem", "database"],
    "min-harness-version": "1.0.0"
  }
}
```

### 6.2 MCP 连接器配置（mcp.json）

```json
{
  "mcpServers": {
    "erp-connector": {
      "command": "npx",
      "args": ["-y", "@mcp/erp-connector", "--endpoint", "${ERP_API_URL}"]
    },
    "crm-connector": {
      "command": "npx",
      "args": ["-y", "@mcp/crm-connector", "--endpoint", "${CRM_API_URL}"]
    },
    "knowledge-base": {
      "command": "npx",
      "args": ["-y", "@mcp/vector-store", "--collection", "${KB_COLLECTION}"]
    }
  }
}
```

---

---

## 第八部分：AI Harness 接入说明

### 8.1 接入步骤

1. **安装插件**：将 `fde-workflow-skill/` 目录放入 Harness 的 `plugins/` 目录
2. **注册 Skill**：在 Harness 配置中声明 `fde-workflow` Skill 路径
3. **配置 MCP**（可选）：如需连接 ERP/CRM 等系统，在 `mcp.json` 中配置连接器
4. **加载评测集**：将 `tests/golden-cases.json` 导入 Eval Harness
5. **验证接入**：运行 `batch_evaluate()` 确认评分器正常工作

### 8.2 跨 Harness 兼容性

| Harness 平台 | 兼容方式 |
|-------------|---------|
| **DeepSeek Harness** | 直接放入 `plugins/`，Cordis 自动加载 |
| **Coze/豆包** | 封装为自定义 Skill 插件，通过 API 网关接入 |
| **Claude Code** | 作为 MCP Server 注册，通过 `mcp.json` 对接 |
| **通用 Agent 框架** | 按 Agent Plugins 1.0.0 规范打包，`plugin.json` 声明能力 |

### 8.3 核心设计原则

- **原子复用**：每个 Skill 只对应单一业务能力，一处封装、多 Harness 共享
- **安全前置**：敏感数据脱敏、权限校验在 Harness 主循环内完成，Skill 内部只做基础校验
- **统一出入参**：所有 Skill 返回固定三层结构 `{code, msg, data}`，便于上层统一解析
- **资产可移植**：Skill、评测集、模板均为标准 JSON/Markdown 格式，不绑定特定 Harness 实现

### 8.4 交付物清单

| 文件 | 用途 | 状态 |
|------|------|------|
| `SKILL.md` | FDE 10步工作流主指令 | 已完成 |
| `plugin.json` | Harness 插件清单 | 已完成 |
| `mcp.json` | MCP 连接器配置（可选） | 未随本 Skill 发布 |
| `tests/golden-cases.json` | 评测集（5条正例+1条边界） | 已完成 |
| `eval_scorer.py` | 自动评分器 | 已完成 |
| `assets/templates/` | 输出模板 | 已完成 |
| `references/` | 详细参考文档 | 已完成 |

---
