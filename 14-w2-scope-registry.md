# W2 Scope Registry：每个法条都有可判定的适用范围

> 用户裁定：每个法条均应能确定使用范围；用独立表维护 Scope/地域/管辖权/行业/生效时间；建立 Scope ID，每个法条配备 Scope ID。
> 关联：`kb/scopes.yaml`、KU 第 30 字段 `scope_id`、CK-17、`jurisdiction.py`。
> 状态：**W2-1/W2-3 已实现**（2026-11-01）：9 scopes / 21 KU scope_id / CK-17 / 生效时间过滤；设计 v0.9 待 W2 收尾统一升版。
> 证据：`evidence/W2-scope-cases.json`。
> 决策记录：`docs/decisions/user-decisions.md`

## 1. 为什么需要 Scope ID

当前 `jurisdiction` 只有 EU/CN 两值，无法回答：

- 同一部 EU AI Act 内，Art.5 禁止实践 vs Annex III 教育/就业高风险，**行业范围不同**；
- 某条 2026-08-02 生效、某条 2027-12-02 生效，**时间范围不同**；
- 美国 NIST RMF、ISO 42001 不是法规，但用户会问；需要登记为“可建议的参考框架”，**supported:false**；
- 跨境问题同时涉及 EU+CN，需要**多选**而不是二选一。

Scope ID 是把“法域”拆成可机检的**适用范围对象**。

## 2. Scope Registry 模型

文件：`kb/scopes.yaml`

```yaml
version: 1
scopes:
  - scope_id: sc-eu-ai-act-h
    label_zh: 欧盟 AI Act（横向）
    instrument: "Regulation (EU) 2024/1689"
    registry_id: reg-eu-ai-act
    jurisdiction: EU
    legal_system: EU law
    territory: [EU, EEA]
    industries: [horizontal]
    actors: [provider, deployer, importer, distributor]
    effective_from: 2026-08-02
    effective_to: null
    status: in_force            # in_force | transition | repealed | reference_only
    supported: true
    source_refs: [reg-eu-ai-act]

  - scope_id: sc-eu-ai-act-annex3-education
    parent: sc-eu-ai-act-h
    label_zh: 欧盟 AI Act · 教育类高风险
    industries: [education]
    effective_from: 2027-12-02
    status: transition
    supported: true
    source_refs: [reg-eu-ai-act]

  - scope_id: sc-cn-genai-measures
    label_zh: 中国生成式 AI 暂行办法
    instrument: "生成式人工智能服务管理暂行办法"
    registry_id: reg-cn-genai
    jurisdiction: CN
    legal_system: PRC law
    territory: [CN-mainland]
    industries: [horizontal]
    actors: [provider]
    effective_from: 2023-08-15
    effective_to: null
    status: in_force
    supported: true
    source_refs: [reg-cn-genai]

  - scope_id: sc-us-nist-ai-rmf
    label_zh: 美国 NIST AI RMF
    jurisdiction: US
    legal_system: US federal guidance
    territory: [US]
    industries: [horizontal]
    effective_from: 2023-01-26
    status: reference_only
    supported: false
    suggestion: true            # 可建议，但不作为法条答案
    source_refs: []

  - scope_id: sc-intl-iso-42001
    label_zh: ISO/IEC 42001
    jurisdiction: INTL
    legal_system: voluntary standard
    territory: [global]
    industries: [horizontal]
    status: reference_only
    supported: false
    suggestion: true
```

### 字段约束

| 字段 | 必填 | 说明 |
|---|---|---|
| `scope_id` | 是 | 稳定 ID，`sc-<jur>-<instrument>-<variant>`；不可复用/改义 |
| `jurisdiction` | 是 | EU/CN/US/SG/INTL |
| `legal_system` | 是 | EU law / PRC law / US federal guidance / voluntary standard |
| `territory` | 是 | 至少 1 项；跨境/EEA/global 显式列出 |
| `industries` | 是 | `[horizontal]` 或具体行业；空数组不允许 |
| `actors` | 建议 | provider/deployer/importer/distributor |
| `effective_from` | 是 | 不能为 null；`reference_only` 可为文档发布日 |
| `effective_to` | 否 | null = 仍有效 |
| `status` | 是 | in_force/transition/repealed/reference_only |
| `supported` | 是 | false = 可识别/可建议，但本库不答实体义务 |
| `parent` | 否 | 细分 scope 指向父 scope，避免重复 |

## 3. KU 契约变更：29 → 30 字段

每个 KU 增加：

```yaml
scope_id: sc-eu-ai-act-h
```

规则：
1. `scope_id` 必填，且能在 `scopes.yaml` 解析；
2. `scope.jurisdiction == ku.jurisdiction`；
3. `status: in_force` 的 KU 不得指向 `reference_only`/`repealed` scope；
4. 一个 KU 一个 scope ID；若一个条款同时覆盖多个行业/时间，优先归入**最具体**的 scope，父 scope 用 `parent` 表达；
5. 新增校验 **CK-17（SCOPE_UNRESOLVED）**：
   - KU 缺 scope_id → `SCOPE_UNRESOLVED`
   - scope_id 悬空 → `DANGLING_REF`
   - jurisdiction 不一致 → `SCOPE_UNRESOLVED`
   - scope 缺 territory/industries/effective_from → `SCOPE_UNRESOLVED`
   - orphan scope（无 KU 且 `supported:true`）→ `SCOPE_UNRESOLVED`

> 契约影响：29 字段 → 30 字段，需要设计 v0.9 + CCC/Gemini 评审；21 条 KU 需回填 scope_id。

## 4. 21 条 KU 的初始映射（建议）

| KU | scope_id | 理由 |
|---|---|---|
| art2 / art5-* / art6-1 / art6-2 / art8-11 / art14 | `sc-eu-ai-act-h` | 横向适用 |
| art6-3 | `sc-eu-ai-act-h` | 例外条款，横向 |
| annex3-1 | `sc-eu-ai-act-annex3-biometrics` | 生物识别行业 |
| annex3-3 | `sc-eu-ai-act-annex3-education` | 教育 |
| annex3-4 | `sc-eu-ai-act-annex3-employment` | 就业 |
| annex3-5 | `sc-eu-ai-act-annex3-essential-services` | 基本服务 |
| cn-genai-art7 | `sc-cn-genai-measures` | 中国生成式 AI |

Annex III 子 scope 的 `effective_from` 建议 `2027-12-02`，与 Art.113 对齐（需作者核实）。

## 5. Scope 解析算法

`ask` 在法域门禁后、检索前执行：

1. **显式 scope/jurisdiction 命中**：只有用户明确给出法域/框架/Scope，才进入候选；行业/主题词不得单独定域；
2. **强 hint 直接定域**：如“算法备案” → CN scope；“GDPR” → EU scope；“NIST” → US reference scope；
3. **时间过滤**：查询含日期/“现在/生效” → 按 `effective_from/to` 过滤；不匹配则 `partial(scope_time)` 并提示；
4. **行业过滤**：查询含教育/就业/医疗 → 匹配 industries；
5. **多 scope**：多选/显式多法域 → 逐 scope 分答，标注 scope_id；
6. **无法匹配** → clarify（见下）；
7. **unsupported** → 建议替代 scope（NIST/ISO/EU/CN），用户选择。

响应中的 citation 增加 `scope_id`，让宿主可审计“这条答案属于哪个适用范围”。

## 6. 不支持法域的建议

输入：`美国 NIST AI RMF 适用吗？`

返回 `clarify(unsupported_jurisdiction)`，选项：

| 选项 | scope_id | supported | 说明 |
|---|---|---|---|
| 美国 NIST AI RMF | `sc-us-nist-ai-rmf` | false | 参考框架，非本库法条 |
| ISO/IEC 42001 | `sc-intl-iso-42001` | false | 自愿标准 |
| 欧盟 AI Act | `sc-eu-ai-act-h` | true | 可答实体义务 |
| 中国生成式 AI 办法 | `sc-cn-genai-measures` | true | 可答实体义务 |

规则：
- **不静默替换**成 EU/CN；
- 选 reference-only → `out_of_scope` + 说明“可作为参考，但本库无该标准 KU”；
- 选 supported → 按该 scope 回答；
- 选“其他”自由文本 → `out_of_scope`。

## 7. 验收

- 21/21 KU 有可解析 scope_id；
- CK-17 负例：缺 scope/悬空/jurisdiction 不一致/scope 缺字段/orphan；
- Scope 解析：教育→annex3-3、就业→annex3-4、GDPR→EU、算法备案→CN、NIST→US reference；
- 不支持法域建议 4 选项；
- 多 scope 标注 scope_id；
- 设计 v0.9 更新 29→30 字段并评审。

## 8. 待确认

1. Scope 粒度：**1 KU = 1 scope_id**（本方案）是否接受？还是允许 `scope_ids: []`？
2. Annex III 子 scope 的 `effective_from` 用 2027-12-02 是否正确（需作者核实 Art.113）？
3. 新增第 30 字段需要设计 v0.9 送 CCC/Gemini；是否现在启动？
