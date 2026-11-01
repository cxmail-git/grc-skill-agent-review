# KU Schema · 唯一字段定义（rev4）

> **本文件是全包唯一字段定义源。** 任何其它文件提到"字段"时，一律引用本文件，不得再列举。
> **生效**：REV-01 起替代此前四套清单（14 / 14 / 22 / 19）。旧四套作废，见 `00-修订对账表.md` REV-01。
> **rev2 修订（应第 2 轮复评 B-01 / MJ-02 / MJ-09 / m-06）**：`title` 由 bookkeeping 移入 fact-bearing，`ku_id` 由 fact-bearing 移入 bookkeeping（标识符不是事实内容），29 = **17 + 12**；`gap` 明示为登记对象而非字段；结构声明行位置更正为 `wiki-schema.md` §2.5；`locator` 补闭合值域（§3.1）。
> **rev3 修订（应第 3 轮复评 B-01 / MJ-02 / m-06 / MJ-04）**：§3.1 由 4 形态扩为 **5 形态**，新增"命名章节式"（来源本身无条号时唯一合法出口，如 `§Oversight`），并明确**禁止章节+页码混写**（`§3.2 p.14` 一类为 B-01 根因），页码/子款等细化信息改以锚点追加到 `snapshot_ref`；`gap.owner` 与 §7 `conflicts.owner` 统一为 `R-* / 实名` 两段式（m-06 / MJ-02）；`gap[].field` 的非法值对应错误码 `GAP_UNKNOWN_FIELD` 已在 `wiki-schema.md` §10 定义（MJ-04）。
> **复核命令**：`grep -rc "个字段" .` 只应命中本文件与引用句；`grep -rn "obligation_nature\|verbatim_excerpt" wiki/schema/wiki-schema.md` 应只命中引用。

---

## 1. 字段总数与两类划分

**29 个字段 = 17 个 fact-bearing + 12 个 bookkeeping。**（rev2 第 2 次更正：`ku_id` 是标识符、`title` 是事实内容，前者归簿记、后者归事实，故为 17/12，非 18/11。）

划分规则只有一条，且它是可机械判定的：

| 类别 | 定义 | 允许出现的位置 |
|---|---|---|
| **fact-bearing（17）** | 其**值是事实内容**（义务、证据要求、定义、日期、状态、适用对象、原文摘录、文件标题），可以且只能出现在派生块内 | 派生块 body、`kb:table` 块、`结构声明`行（仅限白名单 3 个，见 wiki-schema §2.5） |
| **bookkeeping（12）** | 其值是**簿记信息**（KU 主键、来源、等级、指纹、定位、时间戳），不进入读者可见正文 | 仅 KU 文件、块头属性（`ku=` / `ku_list=`）与 `refs.json`；**任何页面 `body_markdown` 内出现即 `FIELD_BLOCKED`**（front-matter 的同名键见 wiki-schema §5） |

> 旧 WS-02 的"14 个字段不出块"之所以不可执行，是因为它只枚举字段名、未定义"什么是事实"。本节改为按**类别**约束，而非按清单枚举；类别由本表逐字段标注，无歧义。

> **编号与分类是两个维度（B-01 的根因）**：全表编号 `#1`–`#29` **固定不变且连续无缺号**，正文中的"§2.1 #12"一类引用依赖它；类别归属见各行所在小节。因此 `fact-bearing` 的编号集合为 `#2–#18`，`bookkeeping` 为 `#1` + `#19–#29`。任何"编号 = 分类序号"的解读都是错的，这正是 rev1 数出 16/13 的原因。

---

## 2. 字段总表

### 2.1 fact-bearing（17 个：编号 #2–#18）

| # | 字段 | 类型 | 必填 | 取值域 / 说明 | 可渲染进派生块 |
|---|---|---|---|---|---|
| 2 | `jurisdiction` | enum | 必填 | `EU` `CN` `SG` `US` `INTL`（国际标准） `VENDOR`（厂商自述，须带 `source_class: vendor`） | 是 |
| 3 | `instrument_type` | enum | 必填 | 见 §3 值域闭合表（11 值） | 是 |
| 4 | `instrument_is_binding` | bool | 必填 | `true` = 对至少一类主体产生法律约束力；`false` = 不产生 | 是 |
| 5 | `obligation_nature` | enum | 必填 | `obligation` `prohibition` `recommendation` `expectation` `capability` `disclosure` `definition` | 是（决定动词集，见 wiki-schema §4） |
| 6 | `obligation` | list[object] | 条件必填 | 每项 `{id, text, subject, modality}`；`obligation_nature=definition` 时可为空 | 是 |
| 7 | `evidence_requirement` | list[object] | 条件必填 | 每项 `{id, text, artefact, frequency}`；无则写 `[]` 并在 `gap` 中登记 | 是 |
| 8 | `applies_to` | list[object] | 必填 | 每项 `{subject, stage, scope}`；`stage` ∈ `design` `develop` `deploy` `operate` `retire` | 是 |
| 9 | `status` | enum | 必填 | `draft` `in_force` `transition` `repealed` `superseded` | 是（状态行） |
| 10 | `effective_date` | date \| null | 必填 | ISO-8601；未知写 `null` 且 `status: draft` | 是 |
| 11 | `transition_note` | string \| null | 条件必填 | `status=transition` 时必填；否则 `null` | 是 |
| 12 | `verbatim_excerpt` | string | 必填 | 原文逐字摘录，**不得改写、不得节略加省略号**；长度上限 1200 字符，超出切 KU | 是 |
| 13 | `definition` | string \| null | 条件必填 | 概念页所依赖的 KU 必填（见 §4） | 是 |
| 14 | `scope_in` | list[string] \| null | 条件必填 | 同 13 | 是 |
| 15 | `scope_out` | list[string] \| null | 条件必填 | 同 13 | 是 |
| 16 | `common_misreadings` | list[object] \| null | 条件必填 | 每项 `{misreading, correction, basis_ku}`；同 13 | 是 |
| 17 | `published_date` | date \| null | 必填 | 来源发布日；`source` 类页面须渲染，故归 fact-bearing（rev1 从 bookkeeping 移入） | 是 |
| 18 | `title` | string | 必填 | 原文标题，不改写；`source` 页 `## 文件概览` 与 `kb:table` 的 `short_name` 列均由它派生，故归 fact-bearing（rev2 从 bookkeeping 移入） | 是（仅 `source` 的 `文件概览` 块与 `kb:table`） |

### 2.2 bookkeeping（12 个：编号 #1 + #19–#29）

| # | 字段 | 类型 | 必填 | 取值域 / 说明 |
|---|---|---|---|---|
| 1 | `ku_id` | string | 必填 | `ku-<jurisdiction>-<source>-<locator-slug>`，全库唯一，**不得改**（改则视为新 KU）。**归簿记**：只作块头属性 `ku=` / `ku_list=`，从不渲染进块正文 |
| 19 | `source_id` | string | 必填 | 对应 `registry` 条目 ID |
| 20 | `source_class` | enum | 必填 | `primary` `official_secondary` `analyst` `vendor` `community` |
| 21 | `tier` | enum | 必填 | `A` `B` `C`（A = 双人核 + 原文逐字；B = 单人核；C = 仅索引不作事实源） |
| 22 | `confidence` | enum | 必填 | `high` `medium` `low`；`low` 时 `status` 必须为 `draft` |
| 23 | `source_class_confidence` | enum | 必填 | `high` `medium` `low`（对来源归属本身的置信度） |
| 24 | `as_of` | date | 必填 | 本 KU 事实的核验基准日 |
| 25 | `locator` | string | 必填 | 条/节/页定位，**取值域见 §3.1（闭合，5 形态，禁混写）**，如 `Art.14(1)`、`§II.B`、`§Oversight`、`GV-1.1`；页码锚点写 `snapshot_ref` |
| 26 | `registry_id` | string | 必填 | 来源登记表主键 |
| 27 | `snapshot_ref` | string | 必填 | 快照相对路径，`verbatim_excerpt` 必须能在其中逐字命中 |
| 28 | `first_seen` | datetime | 必填 | 首次进入 registry 的时间 |
| 29 | `fingerprint` | string | 必填 | 来源内容指纹（bottom-k MinHash，k=96） |

> `title` 已移入 §2.1（#18）；`ku_id` 已移入本节（#1）。全表编号 1–29 连续无缺号，`fact-bearing` = #2–#18（17 个），`bookkeeping` = #1 + #19–#29（12 个）。正文引用"`ku-schema.md` §2.1 #12"一类编号不受影响。

### 2.3 非字段的登记结构（不计入 29，不受 CK-09 约束）

以下三项是**登记对象**，此前被误当作"未定义字段"（第 2 轮复评 MJ-02）。它们不计入 29，也不参与页面字段集校验：

| 结构 | 归属 | 结构定义位置 |
|---|---|---|
| `gap` | KU 文件内的数组 | 本节 + §5 |
| `conflicts.yaml` | 冲突登记文件 | `wiki-schema.md` §7 |
| `refs.json` | 反向索引产物 | `wiki-schema.md` §7.1 |

**`gap` 元素结构（4 键，闭合）**：`field` / `reason` / `owner` / `due`。

- `field` 必须是 §2.1 或 §2.2 的字段名之一，否则 `CK-04 FAIL(GAP_UNKNOWN_FIELD)`（该码已在 `wiki-schema.md` §10 定义）。
- `owner` 采用 **`<角色码> / <实名>` 两段式**（`R-CHAIR` / `R-1` / `R-2` / `R-3` / `R-SEC`），与 `wiki-schema.md` §6.1 `检查人`、§7 `conflicts.owner` 同一格式；`S1` 等任务编号不是责任人，判 `SCHEMA_VIOLATION`。PH0 内可写 `R-1 / 待指定`，G0 门禁时仍为 `待指定` 判 FAIL。
- 判据"`gap` 不是字段"的可执行形式：`grep -c "个字段"` 的计数不因 `gap` 出现而变化（29 恒定）。

---

## 3. `instrument_type` 值域闭合表（11 值，闭合）

此前的问题：只有黑名单、无完整枚举，`binding_guidance` 两义。本节一次性闭合。

| 值 | 定义 | 是否 binding | 典型样例 |
|---|---|---|---|
| `statute` | 立法机关制定的法律 | true | EU AI Act（条例，归 `regulation`）；中国《生成式人工智能服务管理暂行办法》归 `regulation` |
| `regulation` | 行政机关/授权立法 | true | EU AI Act、CN 暂行办法 |
| `executive_order` | 行政命令 | true | US EO |
| `binding_guidance` | **对特定主体有约束力的官方指引/备忘录**（如 OMB M-24-10 对联邦机构） | true | OMB M-24-10 |
| `nonbinding_guidance` | 官方发布但无约束力的指引/问答 | false | 监管问答、执法指引 |
| `voluntary_framework` | 自愿性框架/测试标准 | false | NIST AI RMF、SG AI Verify |
| `management_system_standard` | 管理体系标准（可认证，但标准本身不创设义务） | false | ISO/IEC 42001 |
| `certification_scheme` | 认证方案 | false | 第三方认证项目 |
| `vendor_standard` | 厂商自定标准/承诺 | false | MS RAI Standard |
| `industry_standard` | 行业组织标准 | false | 行业协会规范 |
| `advisory` | 咨询/研究/媒体材料 | false | 分析报告、渠道文章 |

**闭合性规则**：`instrument_type` 只能取上表 11 值；新增需 RFC 并同步本表。
**一致性规则（可判定）**：`instrument_is_binding` 必须与上表 `是否 binding` 列一致，否则 `SCHEMA_VIOLATION`。
### 3.1 `locator` 取值域（闭合，解决 MJ-14）

`locator` 此前只有"条/节/页定位"的描述而无值域，导致 CK-03 无法定位、也无法判定"定位是否合法"。rev2 闭合为 4 种形态；**rev3 增第 5 形态"命名章节式"**（B-01：MS RAI Standard、SG MGF 等来源以命名章节组织、无条号，4 形态下无合法出口，导致 seed 中出现 `§Oversight`、`§4 GenAI` 等越域值）。任一不匹配即 `SCHEMA_VIOLATION`：

| 形态 | 正则 | 适用 `instrument_type` |
|---|---|---|
| 条款式 | `^Art\.\d+(\(\d+\))*$`、`^§?\d+(\.\d+)*$` | `statute` `regulation` `executive_order` `binding_guidance` |
| 章节式（罗马/数字） | `^§[IVXivx]+(\.[A-Za-z0-9]+)*$`、`^(Section|§)\s*\d+(\.\d+)*$` | 全部 |
| **命名章节式** | `^§[A-Za-z][A-Za-z0-9 &/-]{1,40}$`（如 `§Oversight`、`§GenAI`、`§Risk Management`） | 全部；**仅当快照内该章节标题可逐字检索到**时可用，CK-03 校验标题存在性 |
| 页码式 | `^p\.\d+$`、`^pp\.\d+-\d+$` | 全部（须与 `snapshot_ref` 对应页一致） |
| 条目式 | `^[A-Z][A-Z0-9]{0,7}(-[A-Z0-9]{1,8})*-\d+(\.\d+)*$`（如 `GV-1.1`、`GOVERN-1.1`、`M-24-10`、`ISO-42001-6.1`） | `voluntary_framework` `management_system_standard` `certification_scheme` `vendor_standard` `industry_standard` `advisory` |

**两条硬约束（B-01 的判据，CK-03 可执行）**：

1. **禁止混写**：一个 `locator` 只能落一个形态。`§3.2 p.14`（章节+页码）、`§4 GenAI`（数字+命名）、`§III(b)`（含括号子款）均**不合法**，判 `SCHEMA_VIOLATION`。
2. **细化信息另存**：子款（如 `(b)`）、页码等更细定位**不得**混入 `locator`，一律以锚点形式追加到 `snapshot_ref`（如 `snapshots/ms-rai-standard.html#p14`、`…#sec-III-b`）；`verbatim_excerpt` 仍按锚点位置逐字取文。

- 一条 KU 只有一个 `locator`；需多个定位时切 KU（与 `verbatim_excerpt` 长度上限 1200 字符同一设计取向）。
- `locator` 必须是 `snapshot_ref` 内可检索的位置标识，且 `verbatim_excerpt` 必须取自该位置（CK-03）。

---

**`binding_guidance` 的定义裁定**（回应报告 P-03）：对**特定受监管主体集合**有法律约束力、但不普遍适用于所有主体者归此类。判据：该文件能否被援引为"未遵守即违法"——能则 `binding_guidance`，不能则 `nonbinding_guidance`。

---

## 4. 概念字段（`definition` / `scope_in` / `scope_out` / `common_misreadings`）的强制条件

这 4 个字段是为解决"concept 页必填段无字段承载"（原 R-07）而设。

- **强制条件**：某 KU 被任一 `concept` 页引用 → 该 KU 必须填全 4 个字段；否则该页 `status: draft`，不得进索引。
- **来源要求**：4 个字段均为 **fact-bearing**，必须能由 `verbatim_excerpt` 支撑或由 `source_class ∈ {primary, official_secondary}` 的来源直接给出；**Tier C 来源不得填这 4 个字段**。
- **不得推断**：`scope_in` / `scope_out` 只能写来源明示的内容；来源未明示时写 `null` 并在 `gap` 登记，**不得由编辑者推理补全**（GK-2 不造假）。
- **`common_misreadings.basis_ku`**：每条误读必须指向一个真实存在的 KU（可为自身），用于 CK-09 校验。

---

## 5. `gap` 登记（缺失即登记，不推测）

任一条件必填字段无法填写时，写入 KU 的 `gap` 数组：

```yaml
gap:
  - field: evidence_requirement
    reason: "原文仅要求'采取适当措施'，未列举证据形式"
    owner: "R-1 / 张三"
    due: "PH0-G0"
```

- `gap` 非空 → `status: draft`，页面不得进索引（回应原 A5 无出口）。
- `gap` 为空但条件必填字段为 `null` → `CK-04 FAIL(INSUFFICIENT_INPUT)`。
- `gap` 是**登记对象**而非 KU 字段（§2.3）：它不进 29、不参与 `page_class × 字段集` 校验，也不会让 `grep -c "个字段"` 的计数漂移。

---

## 6. 命名

- 字段名唯一形式：`ku_id`（此前 `id` 与 `ku_id` 并存，作废 `id`）。
- 引用统一：`fields` 属性中只写字段名，不写别名。
- 结构示例见 `wiki/seed/seed-ku-list-v2.md` §3 的完整 KU 样例。
