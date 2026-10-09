# 动态核心构建原则（Principle Registry）

> 本文件是 `sayelf-base` 的 **L3 动态原则注册表详版**，用于展开说明主 Skill §2–§3。
> 权威顺序：安装目录中的 `SKILL.md` 为唯一入口；Execution Verdict、Tool Guardrail Contract、Convergence 与任何冲突均以主 Skill 为准。
> 原独立构建原则 Skill 已并入 `sayelf-base`，不再作为单独触发入口。当前 P01–P12 只是基线种子，原则数量可随任务证据增减。

# Sayelf Dynamic Build Principles

Use this Skill in any compatible AI coding agent or agent platform before creating or materially changing an **Agent, Skill, Tool, System, or major feature**. It is a build-time decision and execution protocol, not a business framework or a prescribed technology stack.

## Trigger conditions

Activate when the request involves any of the following:

- a new Agent, Skill, Tool, System, product, or major capability;
- a new architecture, dependency, integration, plugin boundary, automation loop, or model/cloud service;
- a new data flow, external API/model, telemetry, synchronization, upload, or integration that could move local or sensitive data;
- a new or materially changed WebUI workflow;
- a proposal to replace, rebuild, or expand an existing solution.

For a small, local change with no new capability or design decision, apply the relevant principles proportionally and do not manufacture a large decision record.

Do not create a WebUI by default. First determine whether the real function needs a human-facing visual interface. If it does not, do not build one; use the host's native interaction, CLI, API, background workflow, or other simplest suitable interface.

## Portability contract

- Treat the installed `sayelf-base/SKILL.md` as the canonical source of truth. This reference expands the dynamic principle registry, current baseline entries, and development sequence.
- Depend only on the portable instruction surface: YAML frontmatter with `name` and `description`, plus Markdown instructions.
- Do not assume a particular model, tool name, shell, hook, path convention, environment variable, plugin API, or slash command. Use host-specific capabilities only when the host provides them, and keep them optional.
- If a host requires an adapter or manifest, translate only installation and invocation details; preserve the gates, decision classes, evidence boundaries, and user path unchanged.
- `AGENTS.md` in this repository is an optional concise project adapter. It is not required to load or apply this Skill.

## Hard stop before coding

Do not write implementation code until the Step 0 decision and the required pre-coding output are complete. If the request is a duplicate with no measurable improvement, stop and recommend reuse. If existing capabilities cover the need through composition, stop and recommend integration.

## Principle Registry and Task Principle Profile

The base does not have a fixed number of principles. It maintains a versioned registry of reusable principles, and derives the smallest applicable profile for each task.

Each registry entry records at least:

- `id` and stable title;
- purpose and scope;
- task, data, permission, and risk triggers;
- dependencies and conflicts;
- required evidence and completion check;
- status, version, replacement, and retirement note.

Each task profile records every relevant entry as one of:

- `mandatory`: applies and must be satisfied;
- `conditional`: applies only when its named trigger is present;
- `not_applicable`: excluded only with explicit evidence and reason;
- `blocked`: missing evidence, conflict, authorization, or safety condition prevents execution.

The registry is adjusted by this order:

1. detect task, data, permission, external-transfer, destructive-action, interface, and delivery-stage triggers;
2. match the triggers to registry entries and load their dependencies;
3. add conditional entries required by the matched profile;
4. preserve immutable safety invariants and resolve conflicts fail-closed;
5. record the resulting profile and its evidence in the Build Decision Record;
6. recompute the profile when scope, state, data boundary, or execution mode changes.

New principles may be added as new versioned entries. An entry may be removed from one task profile only when `not_applicable` is evidenced and no dependency or invariant is lost. Registry retirement requires a versioned replacement or an explicit reason. Silent deletion for brevity is prohibited.

The following invariants survive every profile-size adjustment: authorization, scope, sensitive-data and destructive-action checks; public-release and external-transfer classification; credential non-egress; evidence before promotion or handoff; convergence before completion; and version, traceability, and rollback readiness. Evidence insufficiency yields `CLARIFY` or `STOP`, never `GO`.

## Step 0 — Innovation Gate

Search GitHub, the open-source ecosystem, and the current workspace before proposing a new core implementation. Follow this sequence:

**Search → Compare → Distill → Gap Analysis → Differentiate → Decide**

Classify the proposal as exactly one of these:

| Decision | Test | Allowed action |
| --- | --- | --- |
| **Duplicate** | A mature solution already solves the real task without a meaningful gap. | Reuse; do not build a duplicate. |
| **Integrate** | Existing parts solve the need and only composition or an interface is missing. | Connect; do not rewrite the parts. |
| **Improve** | An existing solution has a specific, measurable weakness or opportunity. | Build the smallest verifiable optimization. |
| **Differentiate** | Similar solutions exist, but the proposed mechanism or workflow is materially different. | Build a focused MVP around the difference. |
| **Innovate** | No effective matching solution was found. | Validate the original hypothesis before expanding it. |

**Improve is the minimum self-development threshold.** “Better”, “more intelligent”, or “more complete” is not evidence. Name at least one measurable difference: local control, token use, latency, cost, dependency count, compatibility, reliability, evidence quality, automation boundary, or usability.

## Current baseline registry entries (active seed, not a fixed count)

### 01 — Negative Entropy

Keep only the **Object + Function + Interaction** required for the real task and its evidence loop.

- **Architecture Entropy:** remove unnecessary objects, state, modules, dependencies, and abstractions.
- **Functional Entropy:** remove features that do not move a real task toward a result.
- **Interaction Entropy:** remove user-facing complexity that does not help the user complete the task.

When a WebUI is present, the default user path is **Open → Input → Execute → Result**. Without a WebUI, use the simplest suitable interface. Complex internals may remain behind the interface; ordinary users should not need to understand them.

### 02 — Modular / Pluggable

Keep the Core platform-independent. Make platform, collector, analyzer, model, storage, publisher, and similar capabilities replaceable, independently enabled or disabled, upgradeable, and isolated where useful.

Treat an **AI harness**—the runner, agent loop, runtime, or orchestrator that drives model turns and tool execution—as a replaceable adapter outside the Core. Define a minimal bidirectional contract for task input and result output, capability discovery, tool calls, state and checkpoints, events, pause/resume/cancel, human approval, errors and retries, usage, and locally inspectable evidence. The Core must not depend on a provider-specific loop, event schema, or hosted control plane.

Reuse shared harness capabilities before implementing local duplicates. These may include registered tools, models, agents, sessions, sandboxes, caches, memory or state stores, approval services, policy and guardrail services, schedulers, usage accounting, and tracing. Discover and negotiate capabilities at runtime through stable names, versions, schemas, and declared limits; record which provider and version produced each result. Keep task state and credentials isolated, request only the minimum capability and scope needed, and provide an explicit unavailable/denied/degraded path so shared capability loss does not corrupt Core state. Capability availability is not authorization: every use remains subject to explicit permission, local-first placement, and data-sovereignty rules.

Treat shared AI platforms, agents, models, tools, memory, approval, evaluation, policy, cache, scheduling, and tracing as **Shared Capabilities** behind a provider-neutral contract. A capability may be supplied by a local implementation, API, plugin, MCP/connector, or Agent Endpoint. A Skill must be contract-ready—stable identity, version, input/output, permissions, data boundary, evidence, errors, health, and rollback—but does not have to become a network API when local execution is sufficient. API/plugin packaging is an adapter and deployment boundary, not a change to the Skill's semantic identity.

At minimum, the adapter contract must support **discover → match → authorize → invoke → verify → record → version/deprecate**. Version or schema incompatibility, unknown permission/data boundary, unavailable capability, incomplete evidence, or failed post-check must fail closed or use an already-validated local deterministic fallback. A discovered, installed, healthy, authenticated, or model-reported capability is not thereby authorized for the current task.

Harness integration must fail closed: it may coordinate or share only explicitly granted capabilities and must not silently widen permissions, tool access, telemetry, persistence, or data egress. Apply Principle 03 to execution placement, Principle 05 to automated decisions, Principle 06 to harness changes, and Principle 08 to prompts, traces, checkpoints, shared state, and tool inputs/outputs.

### 03 — Local-first

Prefer local execution for deterministic rules, parsing, transcription, frame extraction, metrics, caching, indexing, deduplication, and state management. Add cloud or model dependencies only when local capability is insufficient or evidence justifies them. This covers computation; Principle 08 independently governs data residency and egress.

### 04 — Dynamic by State

Do not default to fixed brute-force polling. Choose the next check from **State → Change Rate → Importance → Next Check**. Increase frequency for fast-changing important content, reduce it for stable content, sleep when unchanged, and wake on important change.

### 05 — Intelligent Automation

Automation may **Discover → Collect → Process → Compare → Detect → Hypothesize → Recommend**, but it must keep **Observation → Inference → Hypothesis → Fact** distinct. Never promote an unverified hypothesis to fact.

### 06 — Evidence-driven Evolution

Capability upgrades follow **Observe → Challenge → Validate → Canary → Promote**. Promotions are **versioned, traceable, and rollbackable**. No validation means no promotion.

### 07 — WebUI as Human Interface

First decide whether the real function needs a human-facing visual interface. Build a WebUI only when it materially improves task completion, visibility, control, or evidence for the target users. If it is not needed, do not build one.

When a WebUI is justified, treat it as the human execution interface, not decoration. Make the user-facing chain **Input → Processing → Evidence → State → Decision → Action → Outcome**, while preserving **Open → Input → Execute → Result** as the ordinary path. Progressively disclose evidence, plugins, models, parameters, logs, and developer controls.

### 08 — Local Data & Sensitive Data Sovereignty

Keep local data read from a device or workspace inside the local trust boundary by default. This includes local files, source code, documents, media, logs, databases, project context, and device-derived data. Do not upload or silently transmit it to cloud services, external models, web searches, third-party APIs, telemetry, remote logs, or automatic synchronization.

Treat credentials and secrets (passwords, API keys, tokens, private keys, cookies, and session credentials), personal data, customer data, proprietary material, financial, health, legal, biometric, location, unpublished, and security-sensitive information as sensitive or restricted. Sensitive data stays local; credentials and secrets must never be uploaded.

For GitHub and any public network, local, internal, sensitive, restricted, or unknown data must not leave the local trust boundary. This covers commits, pushes, public or private repositories, pull requests, issues, releases, packages, public websites, screenshots, logs, traces, metadata, archives, telemetry, and quoted or pasted content. A request to push or publish is not permission to expose non-public data. Encoding, compression, screenshots, transformation, or indirection must not bypass this rule.

Only content explicitly classified **Public** may leave the local trust boundary for GitHub or public publication. Before transfer, review the staged diff and every release artifact for local, internal, sensitive, restricted, or unknown data. If classification, authorization, destination, retention, or leak-check evidence is missing, block the transfer and keep the data local. Other external transfers are allowed only when necessary, specifically authorized, minimized, locally redacted or tokenized, sent through an approved secure route, and auditable for leakage.

Review prompts, outputs, errors, logs, traces, caches, and telemetry for accidental disclosure. Local-first therefore means both **local computation** and **local data control**.

### 09 — Local Deterministic Text Rendering

For text that must appear in a graphic (including cover headline/subhead), prefer deterministic local code rendering with existing SVG, Canvas, or raster-compositing capabilities. Do not send text, source images, or drafts to a third-party rendering service; do not add a dependency if an existing local renderer is sufficient. Reuse the same final rendered artifact across preview, export, and publishing; keep typography legible and within the target platform's safe area. Preserve the original media and make the rendered output a derived copy. Respect explicit human edits over generated suggestions. Verify rendered text and dimensions locally before handoff. Applies to image/cover and media-delivery tasks; excludes cases where the user explicitly requests a provider and separately authorizes the required data transfer, which must still pass Principle 08.

### 10 — Model / Capability Access Surface

When an Agent or Skill needs a large model, model capability, or a shared capability across processes, first define a stable provider-neutral semantic contract and reserve the applicable access surfaces: **API, MCP, and CLI**. These are replaceable adapters, not new capability identities, and a Skill does not need to expose all three.

At minimum, a CLI adapter declares a stable entry point, version, structured stdin/stdout (JSON preferred), stdout/stderr separation, exit codes, timeout/cancellation, idempotency or retry rules, minimum permissions and scope, data classification, call/evidence ID, and secure credential injection. Secrets must not be placed in command-line arguments. Unknown authorization, scope, data boundary, result structure, or evidence is `blocked` / `degraded`, never an implied success.

The API/MCP/CLI surface is selected by Step 0 based on reuse, isolation, deployment, interoperability, and data-boundary evidence. API-ready does not mean network-mandatory; local execution remains valid when it satisfies the real task.

### 11 — Harness Plugin Access Surface

When an Agent or Skill must connect to an AI Harness or run as a host plugin, define a provider-neutral plugin contract and reserve a host-compatible **MCP, CLI, or plugin entry point**. The manifest or adapter record must declare entry, version, host compatibility, capabilities, dependencies, permissions, data boundary, health check, evidence, degradation, uninstall, and rollback.

MCP is appropriate when multiple backends need a common tool/resource protocol; CLI is appropriate as a stable local or subprocess bridge; a host plugin entry is appropriate when the Harness owns lifecycle and discovery. None of these surfaces authorizes itself or may widen tools, persistence, telemetry, network egress, or data scope. Every call remains inside `PRE CHECK → EXECUTE → POST CHECK`, with fail-closed behavior when the host or adapter is unavailable.

### 12 — Local Render First

For image, 3D, video, and other rendering or processing that can be implemented deterministically, use local code or a local engine first when the device meets the required quality, performance, and capability thresholds. Connect a model or remote capability only when local execution is demonstrably insufficient or a measurable benefit justifies it.

The decision record must state the local insufficiency reason, quality/latency/cost evidence, selected provider and adapter version, data boundary, human-approval requirement, local fallback, and rollback path. Keep original assets locally, emit derived artifacts, and apply PRE/POST checks to any model or remote call. Do not hand deterministic layout, typography, conversion, or rendering to a model merely for convenience. Principle 09 remains the typography-specific control; Principle 12 is the broader image/3D/video placement rule.

## Simple-first constraint

Choose the least complex reliable option that satisfies the real task, in this order:

**Existing Capability → Native Solution → Lightweight Tool → Mature Dependency → Complex Framework → Custom Complex Technology**

Increase complexity only after simpler options are tested or ruled out with evidence. Do not add speculative features, dependencies, abstractions, or architecture.

## Mandatory Development Sequence

1. **Discover:** run Step 0 and record the comparison, gap, and decision.
2. **Specify:** define the real user task, success measure, and evidence needed to call it complete.
3. **Reduce:** remove unnecessary architecture, functions, and interactions.
4. **Select:** choose the simplest reliable implementation and state what is deliberately not being built.
5. **Bound:** define the minimum Core and isolate optional or platform-specific capabilities as plugins where needed.
6. **Localize:** decide what runs locally and justify every cloud or model boundary.
7. **Protect data:** classify data as `Public`, `Internal`, `Sensitive`, `Restricted`, or `Unknown`. Keep local, internal, sensitive, restricted, and unknown data local. For GitHub or public-network publication, allow only explicitly `Public` content after reviewing the staged diff and every release artifact; otherwise block. Record evidence for any other authorized external transfer.
8. **Model state:** define state, change signals, importance, and next-check behavior instead of fixed polling.
9. **Bound automation:** label observations, inferences, hypotheses, and facts; identify the validation evidence.
10. **Choose the interface:** decide whether the real function justifies a WebUI. If yes, make it follow Open → Input → Execute → Result and hide advanced controls behind progressive disclosure; if no, do not add a WebUI and keep the simplest suitable interface.
11. **Build the minimum slice:** implement only the smallest path that can produce the stated result.
12. **Verify and evolve:** run focused checks, record evidence, inspect outputs for data leakage, and promote changes only through validation, canary, versioning, and rollback readiness.

## Required Output Before Coding

Before implementation, provide a concise **Build Decision Record** in the task plan, issue, design note, or equivalent working record. It must contain:

```text
Idea / real task:
Closest existing projects or capabilities:
Step 0 decision: Duplicate | Integrate | Improve | Differentiate | Innovate
Measurable improvement or differentiator:
Success measure and required evidence:
Minimum Core:
Plugin boundaries (if any):
Local-first boundary:
Data classification and local trust boundary:
GitHub/public release decision: Allowed | Blocked — review evidence:
External transfer plan (if any; local and sensitive data excluded):
State, change signals, and next-check rule:
Observation / inference / hypothesis / fact boundary:
Evolution, validation, canary, version, and rollback plan:
WebUI decision: Required | Not required — reason:
Default WebUI path (if required): Open → Input → Execute → Result
Simplest reliable implementation:
Explicitly not building:
```

If a field is not applicable, write `N/A` with a reason. A missing measurable improvement or differentiator is a stop signal for new self-built functionality.

## Completion gate

Do not report completion until the implementation has a focused verification tied to the stated success measure. Report any untested behavior, unresolved evidence gap, or rollback limitation explicitly.
