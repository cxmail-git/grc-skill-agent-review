# W2 Clarify：多选与 MCP 呈现细化

> 用户裁定：clarify 允许多选；MCP 端如何呈现需要细化。
> 关联：`ask` / `resolve_clarify` MCP 工具、Scope Registry、DSH/CC skill。
> 状态：**W2-2/W2-4 已实现**（2026-11-01）：clarify 状态/多选/resolve + MCP stdio server + DSH/CC skill。
> 证据：`evidence/W2-2-cases.json`。
> 决策记录：`docs/decisions/user-decisions.md`

## 1. 原则

1. **clarify 是一等对象**，不是普通自然语言回复；宿主必须能结构化渲染。
2. **不自动选择**：宿主/模型不得替用户选法域或 Scope。
3. **可多选**：跨境、多法域、多 Scope 时 `selection: "multi"`。
4. **选项带 scope_id**：用户选的是适用范围，不是模糊的“国家”。
5. **不支持项明确标注**：`supported:false` / `reference_only`，不得伪装成可答。
6. **安全拒答优先**：clarify 只在需要范围消歧时出现；不用于规避 not_legal_advice 等拒答。

## 2. MCP 工具面

新增两个工具（`tools/list` 可见）：

### 2.1 `ask`

```json
{
  "name": "ask",
  "inputSchema": {
    "type": "object",
    "required": ["query"],
    "properties": {
      "query": {"type": "string"},
      "language": {"enum": ["zh","en"], "default": "zh"},
      "clarify_id": {"type": "string", "description": "回填上一轮 clarify"},
      "selected_option_ids": {"type": "array", "items": {"type":"string"}},
      "other_text": {"type": "string"}
    }
  }
}
```

- 不带 `clarify_id`：正常问答；若需消歧返回 `clarify`。
- 带 `clarify_id` + `selected_option_ids`：等价于 resolve；保留单工具路径，便于只支持一个工具的宿主。

### 2.2 `resolve_clarify`（推荐）

```json
{
  "name": "resolve_clarify",
  "inputSchema": {
    "type": "object",
    "required": ["clarify_id","selected_option_ids"],
    "properties": {
      "clarify_id": {"type": "string"},
      "selected_option_ids": {"type": "array", "items": {"type":"string"}},
      "other_text": {"type": "string"}
    }
  }
}
```

- 幂等：同一 clarify_id + 同一选择返回同一结果；
- 过期/无效 → 结构化错误；
- 选 reference-only → `out_of_scope`；
- 选多个 supported → 逐 scope 分答。

## 3. Clarify 返回结构

```json
{
  "mode": "clarify",
  "clarify_id": "clr_01J...",
  "reason": "ambiguous_jurisdiction | unsupported_jurisdiction | multi_scope | scope_time",
  "question": "请确认适用的法域与范围（可多选）",
  "selection": "single | multi",
  "min_selections": 1,
  "max_selections": 3,
  "allow_other_text": true,
  "options": [
    {
      "id": "EU",
      "label": "欧盟 AI Act（横向）",
      "scope_id": "sc-eu-ai-act-h",
      "jurisdiction": "EU",
      "supported": true,
      "kind": "scope",
      "description": "Regulation (EU) 2024/1689；EU/EEA",
      "badges": ["supported"]
    },
    {
      "id": "US-NIST",
      "label": "美国 NIST AI RMF",
      "scope_id": "sc-us-nist-ai-rmf",
      "jurisdiction": "US",
      "supported": false,
      "kind": "reference",
      "description": "参考框架；本库暂无法条 KU",
      "badges": ["reference_only"]
    }
  ],
  "expires_at": "2026-11-01T21:50:00-04:00"
}
```

MCP `CallToolResult`：

```json
{
  "content": [{"type":"text","text":"请确认适用的法域与范围（可多选）"}],
  "structuredContent": { "mode":"clarify", "clarify_id":"clr_...", "options":[...] }
}
```

## 4. 多选语义

| 选择 | 行为 |
|---|---|
| 1 个 supported | 单 scope 回答 |
| ≥2 个 supported | `partial(cross_jurisdiction)`；`groups` 按 scope/jurisdiction；句子前缀 `【EU】/【CN】`；每域 top1 |
| 仅 reference-only（NIST/ISO） | `out_of_scope`，说明“参考框架，本库无实体 KU” |
| supported + reference-only | 答 supported，附 reference 说明；不把标准当义务 |
| 选“其他”且无配置 | `out_of_scope` |
| 超过 max_selections | `SELECTION_COUNT_INVALID` |

多选不合并为一个“综合答案”；必须逐 scope 分列，避免跨域混淆。

## 5. Host（DSH / CC）呈现规范

- `selection=single`：radio / 下拉；`multi`：checkbox；
- 选项显示 `label + scope_id + jurisdiction + badge`；
- `supported:false` 项**可点但标注“参考/不可答”**，不得隐藏；
- “其他/不确定”用自由文本输入；
- 宿主不得默认选中第一项或自动提交；
- 提交时回传 `selected_option_ids`（多选数组），不传自然语言；
- 若宿主不支持结构化渲染：必须把 `question + options` 原样展示，禁止猜。

DSH/CC skill 提示词增加硬规则：

> 当工具返回 `mode=clarify` 时，必须展示全部 options；多选时必须允许勾选多个；不得替用户选择；用户提交后调用 `resolve_clarify`。

## 6. 状态与安全

- `var/clarifies/<clarify_id>.json`：`{query_hash, options, selection, created_at, expires_at, state_mac}`；
- 不存查询原文；TTL 10 分钟；
- `clarify_id` 不可猜测；`state_mac` HMAC；
- clarify 阶段不产生 `answer_id`/`validation_token`；
- 过期 → `CLARIFY_EXPIRED`，重新 `ask`；
- 同一 clarify 幂等；不允许改 options。

## 7. 错误码

| code | 含义 |
|---|---|
| `CLARIFY_ID_INVALID` | 不存在/被篡改 |
| `CLARIFY_EXPIRED` | 超过 TTL |
| `OPTION_INVALID` | option id 不在本 clarify |
| `SELECTION_COUNT_INVALID` | 少于 min 或多于 max |
| `MULTI_SELECT_NOT_ALLOWED` | single 模式收到多个 |
| `OTHER_TEXT_REQUIRED` | 选“其他”但未给文本 |
| `SCOPE_UNRESOLVED` | 选择后仍无法解析 scope |

## 8. 示例

### 示例 A：法域不明

用户：“训练数据有哪些要求？”（无显式法域/框架，必须先问）  
→ `ask` 返回 `clarify(reason=ambiguous_jurisdiction, selection=multi, options=[EU,CN,US-NIST,ISO,OTHER])`  
用户勾选 EU+CN → `resolve_clarify` → `partial(cross_jurisdiction)`，`【EU】/【CN】` 两段。

### 示例 B：不支持法域

用户：“美国 NIST AI RMF 适用吗？”  
→ `clarify(reason=unsupported_jurisdiction, options=[US-NIST(reference), ISO(reference), EU(supported), CN(supported), OTHER])`  
用户选 US-NIST → `out_of_scope` + “本库无 NIST KU，可改选 EU/CN”。

### 示例 C：行业/时间

用户：“教育类高风险 AI 什么时候生效？”（主题词不足以定域）  
→ `clarify(reason=ambiguous_jurisdiction, options=[EU annex3-education (transition, 2027-12-02), EU horizontal])`  
选择 education → 答 Art.6/Annex III + 生效时间提示（不输出法律结论）。

## 9. 兼容与限制

- 旧宿主若只支持单轮 `ask`：可把 clarify 作为文本展示，用户回复后由宿主拼 `clarify_id` 再调 `ask`；
- 不做多轮对话状态机；clarify 只解决一次范围选择；
- options 上限 7（EU/CN/ISO 42001/SOC 2/NIST/其他），multi 上限 3；
- 不把 clarify 用于“追问事实细节”（那是对话，不是范围门禁）。

## 10. 验收

- `tools/list` 含 `ask`/`resolve_clarify`；
- clarify structuredContent 可被 JSON schema 校验；
- single/multi/unsupported/other 四类用例；
- 过期/非法 id/超选 错误码；
- DSH/CC skill 渲染测试：不自动选择、多选可提交；
- 与 Scope Registry 的 scope_id 对齐。
