# 提高缓存命中率：Codex、代码代理与其它大模型

## 1. 定义与边界

缓存命中率不是“相似问题比例”，而是后续请求实际复用了多少输入前缀：

```text
weighted_cache_hit_rate = sum(cached_input_tokens) / sum(input_tokens)
```

缓存复用要求渲染后的前缀精确匹配，并且相关请求设置兼容。相同会话不保证命中；命中输入也仍计入速率限制。先记录 `cached_tokens`、总输入 token、P95 首 token 延迟、输入成本和 miss reason，再调整结构。

## 2. 跨模型通用原则

1. **稳定前缀在前**：系统/开发指令、Skill、稳定参考、工具定义和固定示例放在前面。
2. **动态内容在后**：当前问题、时间戳、请求 ID、随机数、分支状态、实时日志、工作区 diff 和用户专属数据放到后缀或后续消息。
3. **追加而不是重写**：多轮任务保留早期消息、工具调用和结果，追加新消息；不要为了格式整齐重排历史或反复生成整段共享提示。
4. **保持渲染一致**：稳定内容的字节、空白、顺序、序列化方式、工具名称/描述/Schema、结构化输出格式保持不变。
5. **保持请求设置一致**：模型、服务层、推理强度、verbosity、并行工具配置和输出 Schema 只在必要时变更；变更时接受该请求可能断开缓存前缀。
6. **显式断点按变化率放置**：缓存稳定的长前缀，在第一段高频变化内容前设置 breakpoint；不同变化率的稳定层可使用多个断点。不要把低复用动态尾部写入缓存。
7. **缓存键分域**：需要 cache key 时使用 `provider:model:tenant-or-project:prompt-version` 等稳定标识；同一分域复用同一 key，不把原始用户数据、密钥或完整 Prompt 放入 key。
8. **预热要有复用证据**：只有启动后很快会重复使用的稳定前缀才预热；预热会产生缓存写入成本，不是无条件优化。
9. **压缩要看总成本**：上下文压缩可能降低命中率，但减少总输入 token 仍可能更便宜；比较总 token、缓存 token、延迟和质量，不只看单一命中率。
10. **租户隔离优先**：禁止为提高命中率把不同客户的敏感上下文放进同一可复用前缀；缓存范围、留存和地区必须符合数据策略。

## 3. Codex 与代码代理布局

普通 Codex/IDE/CLI 用户通常不能直接设置宿主内部的缓存参数，优化重点是让宿主看到稳定、可追加的上下文：

| 放入共享前缀 | 放入动态后缀 |
|---|---|
| `AGENTS.md`、稳定 Skill 指令、固定项目规范 | 当前用户任务、当前日期、请求 ID |
| 稳定工具名称、描述、Schema 与调用约定 | 当前分支、`git diff`、变更文件内容 |
| 稳定 API/领域参考和少量固定示例 | 实时日志、测试输出、临时错误、工作区快照 |

代码代理的执行规则：

- 不要每轮把完整仓库、完整日志和完整 diff 重新塞进系统/开发指令；只把必要增量放在后续消息。
- 不要为每个任务动态修改共享 `AGENTS.md` 或 Skill 正文；项目事实用后缀证据表达，稳定规则通过版本化文件更新。
- 工具集合和 Schema 采用追加式演进；暂时不用的工具优先禁用调用，而不是从请求中删除，前提是宿主支持这种能力。
- 模型、reasoning、verbosity 和工具配置在同一迭代链保持一致；需要切换时记录为一次有意的缓存边界变化。
- 新建任务或触发上下文压缩会改变可复用前缀；这是状态变化，不要声称仍可完整命中。

## 4. OpenAI/Codex API 适配

OpenAI Responses API 与 Agents/Codex harness 使用同类提示缓存行为。按当前模型支持选择：

### GPT-5.6 及更新模型

- 可使用隐式缓存，或用 `prompt_cache_options.mode = "explicit"` 选择显式缓存。
- 在稳定内容块末尾放置 `prompt_cache_breakpoint: {"mode": "explicit"}`。
- 可用 `prompt_cache_options.prewarm = true` 预热已知的共享前缀。
- 可用 `prompt_cache_options.ttl = "30m"` 控制最低缓存寿命；按组织数据策略确认是否适用。
- 用 `usage.input_tokens_details.cached_tokens` 计算实际复用，用 `prompt_cache_diagnostics` 查找 miss reason。

### 更早的支持模型

- 按模型文档使用稳定 `prompt_cache_key` 帮助相关请求路由到同一缓存。
- 只有在复用频率、成本和数据留存要求都成立时才使用 extended retention，例如 `prompt_cache_retention` 的受支持值。
- 不把 GPT-5.6+ 的 breakpoint、TTL 或诊断字段假定为所有模型都支持。

示例（仅展示请求布局；不要把真实客户资料放入公共样例）：

```python
from openai import OpenAI

client = OpenAI()
STABLE_DEVELOPER_TEXT = "稳定的项目规则、Skill 摘要和工具约定……"
TOOLS = [
    {
        "type": "function",
        "name": "read_file",
        "description": "Read an allowed workspace file.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}},
    }
]

response = client.responses.create(
    model="gpt-5.6",
    input=[
        {
            "role": "developer",
            "content": [
                {
                    "type": "input_text",
                    "text": STABLE_DEVELOPER_TEXT,
                    "prompt_cache_breakpoint": {"mode": "explicit"},
                }
            ],
        },
        # 动态任务放在断点之后；不要把时间戳写回上面的稳定文本。
        {"role": "user", "content": "只提供当前任务的最小必要上下文。"},
    ],
    tools=TOOLS,  # 名称、顺序、描述和 Schema 在迭代请求中保持稳定。
    prompt_cache_options={"mode": "explicit", "ttl": "30m"},
)

cached = response.usage.input_tokens_details.cached_tokens
print({"cached_tokens": cached, "input_tokens": response.usage.input_tokens})
```

诊断 miss 时，保留基线 response ID，在下一次请求设置 `prompt_cache_options.comparison_response_id`，再读取 `prompt_cache_diagnostics`。诊断请求本身不替代命中度量；仍需统计实际 `cached_tokens` 与总成本。

## 5. 其它大模型与框架的适配契约

把供应商差异收敛到一个适配器，不把供应商字段写进核心工作流：

| 能力 | 有该能力时 | 没有该能力时 |
|---|---|---|
| Breakpoint | 在稳定前缀结尾设置 | 仍保持稳定前缀/动态后缀布局 |
| Cache key | 使用稳定、分域、无原文的 key | 依靠稳定前缀与宿主默认路由 |
| Retention/TTL | 按复用证据与数据策略选择 | 不假定缓存长期存在 |
| Usage | 读取 cached/input tokens、成本、延迟 | 记录请求结构与可观测替代指标 |
| Diagnostics | 读取 miss reason 并归因 | 用请求版本、设置 diff 和前缀哈希做本地比对 |

通用请求构造伪代码：

```python
stable_prefix = [system_rules, skill_rules, stable_tools, stable_references]
dynamic_suffix = [current_task, current_diff, current_logs]
request = adapter.build(
    stable_prefix=stable_prefix,
    dynamic_suffix=dynamic_suffix,
    cache_scope="project-or-tenant",
    prompt_version="base-v1",
)
```

`adapter.build` 必须返回结构化请求和本地可查证据：模型/版本、稳定前缀哈希、动态段计数、缓存键是否使用、断点位置、数据分级和下一次检查条件。它不得上传本地原文，也不得声称 provider 未报告的命中。

## 6. Miss 归因与验收

常见 miss 原因：`model_changed`、`tools_changed`、`text_format_changed`、`reasoning_effort_changed`、`verbosity_changed`、`service_tier_changed`、`context_compacted`、`input_changed` 和 `prompt_cache_key_changed`。先修复意外变化，保留有意变化的证据。

每次优化至少做一组基线/改进对照：

1. 用同一模型、设置和代表性任务发送基线请求。
2. 只改变一个缓存布局因素，保留 response ID 或 provider 等价诊断上下文。
3. 比较 `cached_tokens / input_tokens`、缓存写入/读取、P95 首 token 延迟、输入成本、输出质量和安全事件。
4. 连续多次请求确认不是一次性命中；不同租户、权限和数据分级分别验证。
5. 没有 provider 证据时标记为 `Hypothesis`，不能把结构相似写成 `Fact`。

## 7. 本地代码检查

使用 `scripts/cache_prefix.py` 对请求布局做无网络、无模型调用的预检：

```bash
python scripts/cache_prefix.py --self-test
python scripts/cache_prefix.py --request request.json
```

脚本只检查分段顺序、动态内容是否出现在稳定段前、缓存键字段和前缀哈希；它不模拟供应商缓存，也不替代线上 `cached_tokens` 或诊断数据。
