# Wiki Schema v2.1（rev4）

> **本文件是页面层规范与校验表唯一来源。** 字段定义见 `ku-schema.md`；术语见 `glossary.md`；编号体系见 `glossary.md` §1。
> **rev1 修订**：解决评审报告 R-02 / R-03 / R-04 / R-05 / R-06 / R-08 / R-09 / M-03 / M-04 / M-08 / M-09 / M-12 / M-18、X1 / X3 / X6。逐条对账见 `00-修订对账表.md`。
> **rev2 修订（应第 2 轮复评 B-01~B-08 / MJ-01~MJ-15 / m-01~m-11）**：新增 §3.7 `DF-1~DF-6` 定义表（B-05）；`front-matter` 键集合闭合 + `CK-08` 扫描面限定为 `body_markdown`（B-02）；`K` 块强制 `id` 与 `rendered_blocks` 计数规则（B-06）；新增 §11.1 字段允许集表（MJ-01）；新增 §7.1 `refs.json` 结构（MJ-07）；`comparison` 的"选择建议"改名"适用场景"（MJ-06 / BL-2）；门禁不再允许子集口径（B-08）。
> **rev3 修订（应第 3 轮复评 B-01~B-03 / MJ-01~MJ-05 / m-01~m-12）**：EX-5 限定"无"式段、EX-6 限定 H1 必须等于 `title` 渲染值或 `slug`，并补反例列（B-03）；DF-4 增"分类词表"并明确豁免边界（MJ-03）；WS-09 判据改指 §7 `dimension` 值域（m-11）；`CK-08` 表述与 DF 定义对齐（m-12）；§10 补 `GAP_UNKNOWN_FIELD`（m-01）；§6.1 `检查人` 改"角色码 / 实名"两段式（MJ-02 / m-06）；EX-4 数据源改 `log.md`（B-02）。

---

## 0. 三条不可让渡底线（BL）

| 编号 | 底线 | 可机械检查的形式 |
|---|---|---|
| **BL-1** | 不造假：任何事实必须可回溯到 KU，缺失即登记 gap | CK-04（gap 或值必须有其一）+ CK-08（正文无事实形态） |
| **BL-2** | 不推论：来源没说结论的地方，不得出现结论性表述 | CK-02（动词集）+ 人工 Tier A 复核 |
| **BL-3** | 可判别：每条规则必须能回答"违反/未违反" | 本文件 §8 每行必须有"判据 + 错误码"；缺一即规则不成立 |

> 原"三条底线 B1–B3"与攻击项 B1–B4 同名，rev1 起底线统一前缀 `BL-`。

---

## 1. 真相源纪律（WS-01 ~ WS-09）

**每条 WS 必须归属一种校验方式**，不允许存在"写了但无人校验"的禁令（这是原否决项①的成因）。

| 编号 | 规则（可判定表述） | 校验归属 | 判据形态 |
|---|---|---|---|
| **WS-01** | 页面正文（`body_markdown`，即 front-matter 之外的全部内容）在派生块外不得出现任何**事实形态**内容。事实形态的**唯一定义**见 §3.7 的 DF-1~DF-6 与豁免白名单 | **CK-08** | 正则 + 词表，确定性 |
| **WS-02** | 17 个 fact-bearing 字段的值只能出现在派生块 / `kb:table` 块内；12 个 bookkeeping 字段名与值（含 `ku_id`）**一律不得**出现在 `body_markdown` 内，`ku_id` 仅可作块头属性 `ku=` / `ku_list=`（front-matter 的同名键另见 §5）。唯一例外：§2.5 的结构声明行（仅允许 3 个字段）；`## 更新记录` 段表格（数据源 `log.md`，非任何 KU 字段，见 EX-4） | **CK-08 + CK-09** | 字段名扫描 + 白名单值比对，确定性 |
| **WS-03** | `verbatim_excerpt` 必须能在 `snapshot_ref` 指向的快照中逐字命中；页面引用的原文片段必须是该字段的连续子串 | **CK-03** | 子串比对，确定性 |
| **WS-04** | 派生块内容必须等于渲染器对该 KU 的**重算输出**；不得人工增删改 | **CK-06** | 重渲染 + `render_hash` 比对，确定性 |
| **WS-05** | `confidence: low` 或 `gap` 非空的 KU，其派生块必须带 `⚠` 标记与来源等级注记 | **CK-04** | 标记存在性 + 字段值，确定性 |
| **WS-06** | `status ∉ {in_force}` 时，页面必须出现状态行，格式固定（§6.7） | **CK-10** | 行存在性 + 固定前缀，确定性 |
| **WS-07** | 范畴坍缩：`instrument_type` 的表述必须落在 §5 的"必须表述"列，且不得使用该类型的"禁止表述"列动词 | **CK-02** | 动词集 + 类型映射，确定性 |
| **WS-08** | `source_class ∈ {vendor, community}` 或 `instrument_type ∈ {advisory}` 的 KU：不得单独支撑任何义务性页面；`tier: C` 不得作为事实源 | **CK-05** | 授权矩阵，确定性 |
| **WS-09** | 两个 Tier A primary KU 对同一 `dimension` 给出不一致结论时，必须登记 `conflicts.yaml`，页面须显示未决标记 | **CK-13** | 结构校验 + 登记存在性；"是否冲突"由 **§7 `dimension` 闭合值域（7 值）**判定，不由人语感判定 |

> **残留风险披露**：WS-01 的 DF 词表无法覆盖"完全不含日期/编号/状态词的自然语言断言"（如"这是一项前置义务"）。此类残余由**编译期自查项 SC-01** + **Tier A 人审**承担，且**不入 CK 门禁**。此处 `SC-01` 是自查项编号，评审角色编号一律带 `R-` 前缀（见 `glossary.md` §1），两者不共用命名空间（第 2 轮复评 MJ-05）。该项已作为已知残余风险记入 G0 纪要（见 `00-MVP定义.md` §7）。

---

## 2. 派生块语法 v2（唯一版本）

### 2.1 语法

```markdown
<!-- kb:derived id="b1" ku="ku-eu-ai-act-art14" fields="obligation,evidence_requirement,applies_to" render_hash="sha256:9f2c…" ku_hash="sha256:41ab…" -->
（由 render.py 生成的块正文，人工不得编辑）
<!-- /kb:derived -->
```

**属性**（全部必填，缺一即 `SCHEMA_VIOLATION`）。`kb:derived` 与 `kb:table` 共用同一套 `id` 规则：

| 属性 | 说明 |
|---|---|
| `id` | 块在本页内的序号，格式 `b<正整数>`（`b1`、`b2`…）。同一页面内**从 `b1` 起按出现顺序连续递增、同页唯一**；语义化 id（如 `cmp-1`）作废。`rendered_blocks` 必须等于按出现顺序排列的 id 列表（§5、TC-09） |
| `ku` | KU 主键。**唯一属性名**（原 `ku_id=` 写法作废）。`kb:table` 用 `ku_list` |
| `fields` | 本块渲染的 fact-bearing 字段名，逗号分隔，**有序**（顺序参与 hash 计算） |
| `render_hash` | 块正文的封签，用于检出人工手改 |
| `ku_hash` | 渲染时所用 KU 内容的指纹，用于检出"KU 改了而页面没重编译" |

### 2.2 `render_hash` 计算规范（回应原 R-02）

- **覆盖范围**：**仅块正文**。不含起始标记行、不含结束标记行。
- **规范化**：正文按行切分 → 去行尾空白 → 空行压缩为一个 → 以 `\n` 连接 → UTF-8 编码。
- **输入串**：`normalized_body + "\n--meta--\n" + ku + "|" + fields + "|" + template_version`
- **算法**：`sha256`，输出小写十六进制，前缀 `sha256:`。
- **写者**：`render.py`（唯一写入方）。
- **校验者**：`validate.py` 的 **CK-06**；重算不一致 → `HASH_MISMATCH`（block）。
- **失败处置**：`block`，且页面不得进索引。

### 2.3 `ku_hash` 计算规范（回应原 X1：跨层过期检测）

- **覆盖范围**：该 KU 中所有 fact-bearing 字段（含 `fields` 未渲染的），取值规范化后按字段名字典序排列。
- **规范化**：`json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))`。
- **算法**：`sha256`，前缀 `sha256:`。
- **校验者**：**CK-07**；若 `ku_hash ≠ 当前 KU 内容哈希` → `STALE_DERIVED`（block）。
- **意义**：`render_hash` 只回答"块自编译后是否被手改"；`ku_hash` 回答"KU 变了页面是否跟上"。二者缺一即只解决 v1 失败点的一半。

### 2.4 `kb:table` 块（解决"结构性表格必须写在块外"的冲突）

对比表、约束力表等**需要多 KU 值并列**的结构，一律用表格块渲染，不得手写：

```markdown
<!-- kb:table id="b1" ku_list="ku-eu-ai-act-art14,ku-sg-magf-human-involvement" cols="short_name,jurisdiction,instrument_type,instrument_is_binding" render_hash="sha256:…" ku_hash="sha256:…" -->
| 简称 | 法域 | instrument_type | 约束力 |
|---|---|---|---|
| …  | … | … | … |
<!-- /kb:table -->
```

- `cols` 只允许 §2.1 的 fact-bearing 字段名 + `short_name`（由 `title` 派生的短名；`title` 自 rev2 起归 fact-bearing）。
- `id` 规则同 §2.1：格式 `b<正整数>`，按出现顺序连续递增（原 `cmp-1` 写法作废）。
- hash 规则同 §2.2 / §2.3，`input = normalized_body + cols + ku_list`。
- 校验：CK-06 / CK-07（同一套错误码）。

### 2.5 结构声明行（唯一白名单，解决原 R-05）

在 `entity` / `source` 两类页面的**指定段落**（§6 表"允许结构声明"列标注为"是"处），允许出现且仅允许出现如下固定格式的单行：

```markdown
> **结构声明**：instrument_type=nonbinding_guidance；instrument_is_binding=false；jurisdiction=US（依据 ku-us-nist-ai-rmf-govern）
```

- **白名单字段**：`instrument_type`、`instrument_is_binding`、`jurisdiction` —— 仅此 3 个。
- **格式**：必须完整四段（三字段 + `依据 ku_id`），顺序固定，分隔符固定。
- **值校验**：三个值必须与该 `ku_id` 的 KU **完全一致** → **CK-09**，不一致 `WHITELIST_VALUE_MISMATCH`（block）。
- **除结构声明行外，正文任何位置出现字段名或字段值 → `FIELD_BLOCKED`（CK-08/WS-02）**。
- 未在 §6 标注"允许结构声明"的段落，出现该行同样 `FIELD_BLOCKED`。

> 这样把"模板要求写在块外"从"违规"变为"受控例外"，并给出唯一格式，避免"标注法源即全豁免"的解释扩散。

---

## 3. 措辞强度：二维映射（解决原 R-04 / A1）

### 3.1 动词集定义

| 代号 | 动词集 | 语义 |
|---|---|---|
| **VB-OBL** | 必须、应当、须、不得、禁止、负有……义务、应确保、应保证 | 义务/禁止 |
| **VB-EXP** | 期待、期望、宜于、一般应、原则上应 | 期待（无法律约束力） |
| **VB-REC** | 建议、鼓励、倡导、可考虑、宜 | 建议 |
| **VB-CAP** | 具备、支持、能够、设有 | 能力描述 |
| **VB-DIS** | 披露、公布、告知、说明、标注 | 披露 |
| **VB-ATT** | 分析认为、评估认为、观察到、据……报道 | 分析归属 |
| **VB-VEN** | 自述、承诺、宣布、声称 | 厂商自述 |
| **VB-DEF** | 指、是指、定义为、构成为 | 定义 |

### 3.2 硬否决（先于矩阵生效）

**STR-01**：`instrument_is_binding=false` → 全文禁止 VB-OBL。此项单独可判定，不依赖 `source_class`。

### 3.3 二维矩阵 `(source_class × obligation_nature) → 允许动词集`

| source_class ＼ obligation_nature | obligation | prohibition | recommendation | expectation | capability | disclosure | definition |
|---|---|---|---|---|---|---|---|
| **primary** | VB-OBL | VB-OBL | VB-REC | VB-EXP | VB-CAP | VB-DIS | VB-DEF |
| **official_secondary** | VB-ATT† / VB-REC | VB-ATT† | VB-REC | VB-EXP | VB-CAP | VB-DIS | VB-DEF |
| **analyst** | VB-ATT | VB-ATT | VB-ATT | VB-ATT | VB-ATT | VB-ATT | VB-ATT |
| **vendor** | VB-VEN | VB-VEN | VB-VEN | VB-VEN | VB-VEN | VB-VEN | VB-VEN |
| **community** | VB-ATT | VB-ATT | VB-ATT | VB-ATT | VB-ATT | VB-ATT | VB-ATT |

**† 动词集的例外**：`official_secondary` 且 `obligation_nature=obligation` 且 `instrument_is_binding=true` 时，允许 VB-OBL，但**必须**写成归属句（"据某官方指南，X 须……"），归属前缀为固定词表 `据/依据/按照` 之一，且必须有 `ku_id`。此形态记为 **VB-ATT-OBL**，由 CK-02 用正则判定（`^(据|依据|按照).{0,20}(须|应当|必须)`）。

### 3.4 双向约束（回应 D1-b"只限制往强了写"）

- **STR-02**：`source_class=primary` 且 `obligation_nature ∈ {obligation, prohibition}` 时，**禁止**降级为 VB-REC/VB-EXP（不得把硬义务写成"建议"）。→ 防止把强制写成自愿。
- **STR-03**：`source_class=vendor` 的页面，禁止出现 VB-OBL/VB-EXP（不得把厂商承诺写得像监管期待）。

### 3.5 绕过词黑名单（解决原 X3：只黑不白）

**CK-02 除动词集外，另扫以下"规避词"**，命中即 `LANGUAGE_STRENGTH`：

```
监管期待 | 普遍认为 | 业界通行做法 | 事实上要求 | 实质上是强制 | 通常被理解为必须
视为强制 | 等同于强制 | 事实上必须 | 不成文要求 | 默示义务
```

同时给出**白名单集合**（允许出现的非义务表述）：`鼓励类表述`（VB-REC/VB-EXP 全集）、`能力类表述`（VB-CAP 全集）、`描述类表述`（VB-ATT/VB-VEN 全集）。**白名单 + 黑名单同时生效**，任一不满足即 FAIL。

### 3.6 「应当」的判定（回应 D1-d"应当（法律意义）不可判"）

`应当` 归入 **VB-OBL**，唯一例外：出现在 `instrument_type ∈ {management_system_standard, certification_scheme}` 的页面且 `obligation_nature=capability` 时，允许写作"应当建立……"（能力描述）。该例外由 CK-02 用 `(instrument_type, obligation_nature)` 判定，不做语感判断。

---

### 3.7 事实形态定义 `DF-1~DF-6`（`CK-08` 的唯一判据源）

此前 WS-01 / WS-02 / TC-02 / 模板填法要点共 9 处引用 `DF-1~DF-6`，但全包无一处给出定义，导致 `CK-08` 判据为空（第 2 轮复评 B-05）。本节补齐，**任何文件提到 DF 编号只引用本节**。

**扫描面**：`body_markdown` = 页面文件全文 **去掉 front-matter 块**后的部分。front-matter 不在扫描面内（B-02：否则 `status: in_force` 这类页面元数据会被自身规则判违规）。

| 编号 | 形态 | 正则 / 词表（对 `body_markdown` 逐行匹配） | 命中正例 | 不命中反例 |
|---|---|---|---|---|
| **DF-1** | ISO 日期 / 中文年月日 | `\b\d{4}-\d{2}-\d{2}\b`；`\d{4}\s*年\s*\d{1,2}\s*月` | `2023-01-26` | `每季度复核一次` |
| **DF-2** | 法条 / 条款定位 | `(Art\.|Article|Section|§)\s*[\dIVXivx]`；`第\s*[0-9一二三四五六七八九十]{1,4}\s*条` | `Art.14(1)`、`第 10 条` | `该条款要求…`（无编号定位） |
| **DF-3** | 状态词 | 英文：`\b(draft|in_force|transition|repealed|superseded)\b`；中文：`现行有效|已废止|被取代|过渡期` | `status: in_force`（写在正文时） | `当前口径` |
| **DF-4** | KB 字段名 | `ku-schema.md` §2.1 的 17 个 + §2.2 的 12 个字段名（合计 29；snake_case，前后为非字母数字或行边界） | `instrument_is_binding` | `文件性质`（中文段名不是字段名） |
| **DF-4b** | 分类用语（**限豁免**）：**仅** §4"必须表述"规定必须出现的固定短语 | 豁免面收窄为三个固定短语：`自愿采用` / `不产生法律义务` / `自愿框架`，且须**独立成句**（句中不含 DF-4 字段名、不含 `true`/`false`）。§4 之外的任何分类词用法一律落入 DF-4c 或不豁免 | `本来源为自愿框架，不产生法律义务` | ① `instrument_is_binding: 自愿`（分类词与字段名同句）→ 判 `FIELD_BLOCKED`；② `| 强制 | 自愿 |` 表格外正文里的裸分类词 → 落入 DF-4c |
| **DF-4c** | 约束力差异的叙事改述（**拦截**，防"用自然语言写出布尔/枚举值"） | 同一句内出现 **≥2 个分类词**且成对比结构，两个模式任一命中即拦：① `(强制\|自愿\|法定\|推荐)[^。；]{0,6}(、\|，\|/\|和\|与\|一个是\|另一是)[^。；]{0,12}(强制\|自愿\|法定\|推荐)`；② `(前者\|后一个\|另一个)?[^。；]{0,4}(强制\|自愿\|法定\|推荐)[^。；]{0,4}(后者\|后一个\|另一个\|另一)[^。；]{0,6}(强制\|自愿\|法定\|推荐)` | `A 是强制、B 是自愿`、`一个是强制，一个是自愿`、`前者强制后者自愿` | `约束力性质不同`（无值断言，不判）；`本来源为自愿框架，不产生法律义务`（DF-4b 单短语，不判） |
| **DF-5** | 义务动词 + 义务主体同句 | 同一句内同时命中 VB-OBL/VB-EXP 动词（§3.1）**且**命中主体词（`提供者|部署者|开发者|进口商|分销商|机构|企业|组织`） | `提供者应当标注…` | `本页解释如何判断…` |
| **DF-6** | 数字 + 期限 / 阈值 | `\d+\s*(天|日|个月|年|%|人日)`；`(超过|不少于|至少|不低于)\s*\d+` | `不少于 3 年` | `多个法域`、`11 页`（`页` 不在期限单位表内） |

**豁免白名单**（命中下列位置时不判 `NARRATIVE_FACT`，逐条可判定）：

| 豁免 | 范围 | 判定方式 | 反例（命中即**不**豁免） |
|---|---|---|---|
| EX-1 | front-matter 块 | 扫描前先去掉首个 `---` … `---` 区块 | 正文中第二个 `---` 起的水平分隔线区块被误当 front-matter 剔除 |
| EX-2 | 派生块 / `kb:table` 块（含标记行与正文） | 先剔除 `<!-- kb:` … `<!-- /kb:` 区间 | 未闭合的 `<!-- kb:`（缺 `-->`）→ 剔除失败，按正文扫描 |
| EX-3 | 结构声明行（§2.5） | 以 `> **结构声明**：` 开头的整行剔除，其值改由 CK-09 校验 | 以 `>` 引用块伪装事实断言、但不含 `**结构声明**：` 前缀的行 |
| EX-4 | `## 更新记录` 段内表格的 **`日期` 列单元格**（TC-02）。**数据源是 `log.md`（过程产物，结构见 §7.5）**，不是 KU 字段 `as_of`；列固定为 `日期 / 变更 / 操作角色` | **仅剔除 `日期` 列的 `\d{4}-\d{2}-\d{2}` 值**；`变更` / `操作角色` 两列**仍在 CK-08 扫描面内**（B-02 收回 rev3 的"整行剔除"粒度） | ① 同格式表格出现在其它段；② 表格内出现 `registry_id` / `snapshot_ref` 等簿记值（仍判 `FIELD_BLOCKED`）；③ `变更` 列写入事实句（如 `提供者须在 2026 年前完成登记`）→ 判 `NARRATIVE_FACT`（rev3 此处整表移出扫描面，可绕过 CK-08） |
| EX-5 | **仅限**"无"式段内（范围 = §6 通用规则 2 定义的**所有**"无"式段 + §6.1 单法域出口 + §6.3 不可比出口 + TC-06 topic `## 未决问题`）的 `检查日期 YYYY-MM-DD` 与 `依据 <ku_id>`。**§6.4 义务簇不在范围内**（§6.4 无"无"式，rev4 删误入项） | 先判定该段标题落在上述范围（六类页面的任一必备段写成 `无（… 已检查范围：…）` 即命中），再在该段内剔除 `检查日期 \d{4}-\d{2}-\d{2}`、`依据 ku-[a-z0-9-]+`（B-03：出口句必须能自证检查时点） | 同样的 `检查日期 2026-10-29` 出现在非"无"式段（如 `## 一句话定义`）→ 判 `NARRATIVE_FACT` |
| EX-6 | `# ` 一级标题行，**且**该 H1 渲染值等于 `title` 或 `slug` | 仅剔除首个 H1；剔除前用 CK-09 比对 H1 文本 = `title` 渲染值 或 `slug` | H1 写成任意其它事实性句子（如 `# 提供者须在 2026 年前完成评估`）→ 不豁免，判 `NARRATIVE_FACT` |
| EX-7 | `[[]]` 内链与 `ku-*` 标识符 | `\[\[[^\]]+\]\]`、`ku-[a-z0-9-]+` 先剔除 | `[[]]` 双括号外的裸 `reg-…` / `snapshots/…` 不算豁免 |

**口径澄清（避免过度拦截）**：

1. `CK-08` 不扫描"通用枚举词"——`jurisdiction` 的 `EU/CN/SG/US/INTL/VENDOR`、`source_class`、`tier`、布尔字面量 `true/false` 出现在正文不判违规；这些词是普通语言成分，无法与事实泄漏区分。
2. §4 的"必须表述"（如 `voluntary_framework` 必须出现"自愿采用、不产生法律义务"）是 `CK-02` 的要求；`CK-08` 仅对 DF-4b 列出的**三个固定短语**放行（须独立成句、不带布尔值或字段名）。**其余分类词的并列/对比用法由 DF-4c 拦截**（rev4：rev3 曾把全部分类词设为豁免，与 `templates/comparison.md` 填法要点 4 正面冲突）。
3. `CK-08` 对 bookkeeping 的拦截只针对**字段名**（DF-4）与**可识别值形态**（`snapshots/…`、`reg-…`、`sha256:`、`minhash96:`、ISO 时间戳），不针对等级枚举字面量。

---

## 4. 范畴坍缩禁止表（WS-07 / CK-02）

每种 `instrument_type` 给出"必须表述 / 禁止表述"，`description` 列即判据。

| instrument_type | 必须表述（至少出现一处） | 禁止表述（出现即 FAIL） |
|---|---|---|
| `statute` / `regulation` | 规定、要求、禁止 | 建议、自愿、可选择 |
| `executive_order` | 要求（对联邦机构） | 适用于所有企业、普遍强制 |
| `binding_guidance` | 对……具有约束力 | 自愿、仅供参考 |
| `nonbinding_guidance` | 指引、不产生法律义务 | 强制、必须遵守、法定要求 |
| `voluntary_framework` | 自愿采用、不产生法律义务 | 认证要求、合规义务、法定 |
| `management_system_standard` | 标准、可用于认证、本身不创设义务 | 法律要求、合规强制 |
| `certification_scheme` | 认证方案、证明符合标准、不创设法律义务 | 法规、法定要求、监管强制 |
| `vendor_standard` | 厂商标准、自我承诺 | 行业标准、监管要求、认证要求 |
| `industry_standard` | 行业共识、行业规范 | 法定、监管强制 |
| `advisory` | 咨询观点、不构成结论 | 规定、要求、依据 |

> 原表只有 8 类且无 `binding_guidance` 归类，rev1 按 `ku-schema.md` §3 的 11 值闭合重写。

---

## 5. 页面 front-matter 契约（解决原 M-04）

每份页面文件首部必须是如下 front-matter，**不得**使用平台水印字段（`AIGC.*` 一律禁止，见 M-05）：

```yaml
---
page_id: concept-human-oversight
page_class: concept            # overview | concept | entity | comparison | topic | source
template_version: "2.1"
status: draft                  # draft | published
as_of: 2026-10-29
ku_refs: [ku-eu-ai-act-art14, ku-sg-magf-human-involvement]
rendered_blocks: [b1, b2, b3]
narrative_author: ""           # 叙事段撰写者（人）；空表示未撰写
---
```

- `page_class` 取值域 = 六类，闭合；CK-09 校验派生块 `fields`（及 `kb:table` 的 `cols`）是否属于该类的允许字段集，允许集见 **§11.1**。
- `ku_refs` 必须等于文件中所有 `kb:derived` / `kb:table` 引用到的 `ku` 之并集，否则 `DANGLING_REF`。

**front-matter 键集合（闭合，8 键，缺一或多一即 `SCHEMA_VIOLATION`）**：
`page_id` `page_class` `template_version` `status` `as_of` `ku_refs` `rendered_blocks` `narrative_author`（共 8 键）。

**同名不同义声明（B-02 / MJ-02 的根因）**：`status` 与 `as_of` 在 front-matter 里是**页面元数据**（页面生命周期状态、页面核验基准日），在 KU 里是**字段**（KU 状态、KU 核验基准日）。两者语义不同、取值域不同（页面 `status` 只有 `draft|published`，KU `status` 有 5 值），因此：

1. front-matter 不属于 `body_markdown`，**不进 CK-08 扫描面**（§3.7 EX-1）；`status: in_force` 出现在正文才是 DF-3 命中。
2. front-matter 的键名允许与 KU 字段名重名，但**只允许上表 8 键**；出现 `title` / `instrument_type` / `jurisdiction` 等 KU 字段名作 front-matter 键 → `FIELD_BLOCKED`（CK-08/DF-4）。

**`rendered_blocks` 计数规则（B-06）**：

- 元素 = 文件中 `kb:derived` + `kb:table` 块的总数，**一个块一个 id**；
- 列表必须**按块出现顺序**排列，且与各块 `id` 属性逐一相等；
- 数量或顺序不符 → `SCHEMA_VIOLATION`（TC-09）；
- 块 `id` 必须从 `b1` 起连续无跳号，跳号 → `SCHEMA_VIOLATION`（TC-10）。

---

## 6. 六类页面的必备段与"无"出口

**通用规则**：
1. 段标题必须与本节**逐字一致**（CK-10 用标题集合比对，避免原 P-01 的优点被破坏）。
2. 每段必须非空；确无内容时写 `无`，并附 `已检查范围：……`（**"已检查范围"必须有内容，否则 `REQUIRED_SECTION_MISSING`**）。此即原 §6.5 与 topic 模板冲突的正解（回应 Phase B #1）。
3. 标注"允许结构声明"的段落，可含 §2.5 的结构声明行，且**全页最多 1 行**。

| 类 | 必备段（顺序固定） | 允许结构声明 | 触发条件 |
|---|---|---|---|
| `overview` | 适用范围 / 覆盖的法域与文件 / 强制与自愿边界 / 义务簇 / 常见误读 / 未决冲突 | 否（字段事实一律走 `kb:table`） | 单法域的主题总览，**文件数 ≥1**（`≥2` 时为多文件总览，`=1` 时为单文件总览；原"多文件"限定与本包 `overview-cn-genai` 自相矛盾，rev2 放开） |
| `concept` | 一句话定义 / 概念边界 / 各法域对应义务 / 与其它法域的差异 / 常见误读 / 使用边界 / 未决冲突 / 变更敏感度 | 否 | **被 ≥1 个法域的 KU 引用**（原 ≥2 改为 ≥1，见 §6.1） |
| `entity` | 文件性质 / 谁受约束 / 关键义务 / 证据要求 / 时间线 / 常见误读 / 未决冲突 | 是（第 1 段） | 单一文件/单一机构 |
| `comparison` | 对比对象 / 逐维对比 / 实质差异 / 不可比之处 / **适用场景** / 未决冲突 / 变更敏感度 | 否（字段事实一律走 `kb:table`） | ≥2 个 KU 跨法域 |
| `topic` | 问题定义 / 涉及文件 / 现状与分歧 / 实务影响 / 未决问题 / 常见误读 / 使用边界 / 变更敏感度 | 否 | 跨文件主题，无单一答案 |
| `source` | 文件概览 / 文件性质 / 时间信息 / 关键条款 / 局限与边界 / 更新记录 | 是（第 2 段，仅 1 行） | 单 KU 的来源卡 |

> `comparison` 的第 5 段原为"选择建议"，与 BL-2「不推论」直接冲突：给建议即须比较优劣，而优劣是评价而非来源陈述（MJ-06）。rev2 正式改名 **`适用场景`**，要求只陈述"各对象各自适用于什么场景，以及在什么条件下应由人决定"，不出现"更严格 / 更合适 / 建议选"等推介式表述。段标题改名后 **CK-10 的标题集合同步改为"适用场景"**，旧标题 `选择建议` 判 `REQUIRED_SECTION_MISSING`。

### 6.1 `concept` 触发条件与单法域出口（解决原 R-10 / B1）

- 触发：`≥1` 个法域（原 `≥2` 使 PH0 第 3 页 `concept-training-data-governance` 无法编译）。
- 模板槽位：`{{jurisdiction_1}} … {{jurisdiction_N}}`，N ≥ 1，由渲染器按 `ku_refs` 数量生成。
- **单法域出口**：`## 与其它法域的差异` 段写
  `无（单法域概念；已检查范围：EU/SG/US/INTL 无对应 KU，检查日期 2026-10-29，检查人：R-2 / 张三）`
- 该写法由 CK-10 判定：必须含"无"+ "单法域概念" + "已检查范围"三项；`检查日期` 与 `检查人` 由 CK-10 校验存在性。
- **`检查人` 格式（m-06 二选一的落地形态）**：固定两段式 `检查人：<角色码> / <实名>`。`<角色码>` 取 `glossary.md` §1 的 `R-*` 集合（`R-CHAIR` / `R-1` / `R-2` / `R-3` / `R-SEC`）；`<实名>` 为该页 front-matter `narrative_author` 的值，由 **CK-09 交叉比对**，二者不一致判 `WHITELIST_VALUE_MISMATCH`。`S1` 这类任务编号出现在此处即判 `REQUIRED_SECTION_MISSING`。
- PH0 内人员未定时允许写 `R-2 / 待指定`（否则 rev2 样例无法通过自身校验），但 **G0 门禁时 `待指定` 一律判 FAIL**（`01-整体规划.md` §G0-**⑥**；④ 是 RR 签字项）。
- 该"无"式中的 `检查日期 YYYY-MM-DD` 属 §3.7 EX-5 豁免，不判 `NARRATIVE_FACT`（B-03）。

### 6.2 无字段承载的段落（解决原 R-07）

`concept` 的 `一句话定义` / `概念边界` / `常见误读` 三段，字段承载为 `definition` / `scope_in`+`scope_out` / `common_misreadings`（见 `ku-schema.md` §4）。
若所引 KU 未填这 4 个字段 → 页面 `status: draft`，**不得进索引**，且 `gap` 必须有对应登记。**不得由编译器撰写**（BL-1）。

### 6.3 `comparison` 的不可比出口（解决原 B2 / M-09）

**前置规则（先判、后填）**：若不可比维度 **> 3**，本页不应存在，按 DC-6 降级为两页 `entity`——此情形下本段不填，属"页面结构错误"而非"段落空缺"。

在页面成立（不可比维度 ≤3）的前提下，`## 不可比之处` 允许且仅允许两种**段落写法**：

- `无（两对象在全部对比维度上均给出可比值；维度见「逐维对比」）`
- `第 N 维不可比：<理由>（依据 <ku_id> 或 来源未覆盖）`

"不得为空"改为"不得空缺且必须取上述两式之一"，由 CK-10 正则判定。原第三项"不可比维度超过 3 个 → 降级"是**结构前置规则**，不是段落文案，rev2 从"三选一"移出（m-10）。

### 6.4 `overview` 的义务簇定义（解决原 B4 / M-10）

`义务簇 = applies_to.subject × applies_to.stage`，按此笛卡尔积分组，**上限 6 组**；超过 6 组时按 `stage` 合并并在段首声明合并方式。该定义使两页结构可比、diff 稳定。

### 6.5 状态行格式（WS-06 / CK-10）

`> **状态**：status=<值>；effective_date=<值|未知>；依据 <ku_id>`

---

## 7. 冲突协议与 `conflicts.yaml` 最小结构（解决原 M-12）

```yaml
- id: CFL-001
  ku_ids: [ku-eu-ai-act-art14, ku-sg-magf-human-involvement]   # 恰 2 条，均为 Tier A
  dimension: human_oversight_intensity    # 取值域见下表
  status: open                            # open | resolved | accepted_divergence
  resolution: null                        # resolved 时必填，且须指向新的 KU 或裁定记录
  page_refs: [concept-human-oversight]
  opened_at: 2026-10-29
  owner: R-1 / 张三（KU 核验任务的执行评审人；格式同 §6.1 两段式）
```

`dimension` 闭合值域（用于把"是否冲突"从语感变为查表）：
`binding_nature` `obligation_subject` `obligation_stage` `evidence_form` `human_oversight_intensity` `timeline` `scope_threshold`

- `status: open` → 引用页必须显示 `> **未决冲突**：CFL-001`，否则 CK-13 FAIL。
- 同一 `(ku_ids, dimension)` 重复登记 → `CONFLICT_DUPLICATE`。
- `accepted_divergence` 必须附理由，且不得用于掩盖 `binding_nature` 维度的冲突。

### 7.1 `refs.json` 最小结构（解决 MJ-07：M6 交付物此前无契约）

`refs.json` 是**生成物**（由图级校验器输出），不是手写文件；它只承载"KU → 页面"的反向索引，不含事实内容。

```json
{
  "schema_version": "1.0",
  "generated_from": "wiki/pages/*.md + wiki/ku/*.yaml",
  "ku_to_pages": { "ku-eu-ai-act-art14": ["concept-human-oversight", "comparison-eu-vs-sg-human-oversight"] },
  "page_to_kus": { "concept-human-oversight": ["ku-eu-ai-act-art14", "ku-sg-magf-human-involvement"] }
}
```

- 4 个键**闭合**：`schema_version` / `generated_from` / `ku_to_pages` / `page_to_kus`；多一或少一即 `SCHEMA_VIOLATION`。
- `ku_to_pages` 与 `page_to_kus` 必须互为转置，边数相等；本包期望 **19 条边**（`seed-ku-list-v2.md` §5）。
- 数字型事实（边数、页数）**不得**写入 `refs.json`，一次写入即产生第二事实源；边数由校验器运行时统计并与 19 比对。
- 校验归属：CK-11（全部引用可解析）、D4（输出边数 = 19）。

### 7.5 `log.md` 最小结构（解决 MJ-07 同类"未定义依赖"；本轮由 N-04 指出，rev4 新增）

`source` 页 `## 更新记录` 表与 `{{log.date}}` / `{{log.actor}}` 两个占位符此前在包内**无任何结构定义**，与 rev2 的 `refs.json` 属同一类缺陷。本节为其唯一权威定义。

**形式**：单文件 `wiki/log.md`，按时间倒序的表格，**逐行追加、不修改历史行**。

| 列 | 字段 | 类型 / 值域 | 约束 |
|---|---|---|---|
| 1 | `date` | `YYYY-MM-DD` | ISO 日期；对应模板 `{{log.date}}` |
| 2 | `event` | 闭合枚举：`INGEST` / `RECOMPILE` / `RECHECK` / `SIGNOFF` / `SUPERSEDE` | 事件码，非自然语言 |
| 3 | `subject` | `<ku_id>` 或 `<page_slug>` 或 `<registry_id>` | 必须可被 CK-11 解析 |
| 4 | `actor` | `R-*` 角色码（`glossary.md` §1）或实名 | 对应模板 `{{log.actor}}`；不得写任务编号（`S1`…） |

- **渲染映射**：`日期 ← date`、`变更 ← event + subject 的固定模板串`（如 `RECOMPILE · concept-human-oversight`）、`操作角色 ← actor`。**渲染器不得把 `subject` 展开为自然语言描述**——否则等于让日志承载事实。
- **占位符闭合**：模板只允许 `{{log.date}}` / `{{log.event}}` / `{{log.subject}}` / `{{log.actor}}` 四个；其它 `{{log.*}}` 即 `SCHEMA_VIOLATION`（归 `CK-09` ② 的模板契约校验）。
- **`log.md` 不是事实源**：它记过程，不记法条内容；任何人试图从 `log.md` 取 `as_of` / 效力状态即违反 BL-1。
- 校验归属：`CK-11`（`subject` 可解析）、`CK-09`（占位符闭合）。追加性（历史行不被改写）由 `T6` 交付核对人工执行，不设自动门禁。

---

## 8. 校验表（CK-01 ~ CK-13）—— "13 条校验"的唯一权威定义

> 此前 `R4–R8 / P1–P5 / G1–G3` 三种构成互斥且零定义（原 R-03）。rev1 起**只有这张表**，编号统一 `CK-`，不再使用 `R/P/G` 前缀。
> `M4`、`S4`、`G0`、`记录表` 一律引用本表。

### 8.1 KU 层（CK-01 ~ CK-05）

| 编号 | 名称 | 判据（可机械执行） | 输出错误码 | 确定性 |
|---|---|---|---|---|
| **CK-01** | 字段完备与取值域 | 29 字段按 `ku-schema.md` 的必填/条件必填与枚举校验；`instrument_is_binding` 与 `instrument_type` 的 binding 列一致 | `INSUFFICIENT_INPUT` / `SCHEMA_VIOLATION` | 确定 |
| **CK-02** | 措辞强度 | §3.2 硬否决 + §3.3 矩阵 + §3.5 黑白名单（含规避词）+ §4 禁止表述 | `LANGUAGE_STRENGTH` / `CATEGORY_COLLAPSE` | 确定 |
| **CK-03** | 原文一致性 | ① `verbatim_excerpt` 在 `snapshot_ref` 中逐字命中；页面引用片段为其连续子串；② **命名章节式 locator**（§3.1 第 5 形态）必须在 `snapshot_ref` 指向的快照中检索到同名章节标题（标题比对去除编号与空白后逐字相等），检索不到即视为 locator 无效 | `EXCERPT_MISMATCH` | 确定 |
| **CK-04** | 缺失登记 | 条件必填字段为 `null` 时 `gap` 必须有对应项；`gap` 非空 → `status=draft`；`confidence=low` → 块内必须有 `⚠` | `INSUFFICIENT_INPUT` | 确定 |
| **CK-05** | 来源授权 | `tier/source_class/instrument_type` 组合授权矩阵：`vendor`/`community`/`advisory` 不得单独支撑义务性页面；`tier C` 不得作事实源；`definition` 类字段不得由 `tier C` 提供 | `FIELD_BLOCKED` | 确定 |

### 8.2 页面层（CK-06 ~ CK-10）

| 编号 | 名称 | 判据 | 输出错误码 | 确定性 |
|---|---|---|---|---|
| **CK-06** | 派生块封签 | 重渲染后按 §2.2 重算 `render_hash`，须与块头一致（`kb:derived` 与 `kb:table` 同规则） | `HASH_MISMATCH` | 确定 |
| **CK-07** | 派生块新鲜度 | 按 §2.3 重算 `ku_hash`，须等于当前 KU 内容哈希 | `STALE_DERIVED` | 确定 |
| **CK-08** | 正文禁止面 | 对 `body_markdown` 按 §3.7 依次应用 EX-1~EX-7 豁免后，扫描 §3.7 定义表内的 DF-1 / DF-2 / DF-3 / DF-4 / DF-4c / DF-5 / DF-6 七类形态（DF-4b 为限豁免项，仅豁免三固定短语）；DF 定义表本身即全部词表，不另立第二份清单 | `NARRATIVE_FACT` / `FIELD_BLOCKED` | 确定（词表 + 正则） |
| **CK-09** | 结构声明一致性 | ① 结构声明行最多 1 行、格式固定、三字段值须与 `依据 ku_id` 的 KU 完全一致，非白名单段出现即 FAIL；② `page_class` × 块字段集校验，允许集见 **§11.1**（`fields` 与 `cols` 一律按该表判定，表外字段即 FAIL）；③ **H1 校验**（EX-6 的前置条件）：首个 H1 渲染值须逐字等于 `title` 渲染值或 `slug`，否则不豁免、并由本项报 `REQUIRED_SECTION_MISSING`；④ **`检查人` 实名段校验**（§6.1）：`检查人：<角色码> / <实名>` 的 `<角色码>` ∈ `glossary.md` §1 的 `R-*` 集合、`<实名>` 逐字等于该页 front-matter `narrative_author`，二者任一不成立即 FAIL | `WHITELIST_VALUE_MISMATCH` / `FIELD_BLOCKED` / `REQUIRED_SECTION_MISSING` | 确定 |
| **CK-10** | 必备段与状态行 | 六类页面的段标题集合逐字比对；每段非空或为合法"无"式（§6.1/6.3/6.4）；`status ∉ in_force` 时状态行存在且格式合法 | `REQUIRED_SECTION_MISSING` | 确定 |

### 8.3 图级（CK-11 ~ CK-13）

| 编号 | 名称 | 判据 | 输出错误码 | 确定性 |
|---|---|---|---|---|
| **CK-11** | 断链 | `ku_refs`、`refs.json`（结构见 §7.1）反向引用、页面内 `[[...]]` 链接全部可解析；断链率必须为 0 | `DANGLING_REF` | 确定 |
| **CK-12** | 孤儿 KU | 未被任何页面引用的 KU 占比 ≤ 5%（10 条 KU 时 = 0 条） | `ORPHAN_KU` | 确定 |
| **CK-13** | 冲突显式化 | `conflicts.yaml` 结构校验（§7）+ `status: open` 的冲突必须在其 `page_refs` 页面显示标记；`dimension` 取值域校验 | `CONFLICT_UNLOGGED` | 确定（结构）/ 半确定（冲突存在性依赖 `dimension` 表） |

**门禁口径**：CK-01~CK-12 全部为**门禁项**（必须全绿）。**任何阶段门禁不得只声明子集**：G0 是"PH0 阶段增量验收"，其全量口径仍为 CK-01~CK-12；文件中出现"CK-06/07/10 即 G0 全部"这类写法即为口径错误（第 2 轮复评 B-08）。CK-13 的"冲突存在性"判定为**半确定**，仅"结构校验 + 标记存在性"入门禁；"是否真构成冲突"由 Tier A 人审签署，**不计入自动门禁**（回应原 M-07：门禁内不允许抽样项）。

**计数口径**：13 = 5（KU 层）+ 5（页面层）+ 3（图级）。任何文件提到"13 条校验"必须指本表，不得另立构成。

---

## 9. 编译期自查（SC-01 ~ SC-12，非门禁）

> 原问题：SC 被同时称作"来源等级规则"和"校验器规则"。rev1 明确定性：**SC 是 LLM 编译器在生成页面时的自查清单，不产生 error code，不进 CK 门禁**。其失效率为已知残余风险。

| 编号 | 自查项 |
|---|---|
| SC-01 | 是否有未指向 KU 的断言（WS-01 的语义兜底）。**注意：`SC-01` 仅指"本表第 1 项自查"，评审角色编号一律带 `R-` 前缀，禁止写成"主持人（SC-01）"（MJ-05）** |
| SC-02 | 派生块 `fields` 是否覆盖该段所需的全部事实 |
| SC-03 | 是否引用了本次未渲染的字段 |
| SC-04 | 原文引用是否为连续片段 |
| SC-05 | 是否使用了 §3.5 的规避词变体（未收录的近义词） |
| SC-06 | 段首是否与段标题语义一致 |
| SC-07 | 是否出现评价性表述（"完善""先进""严格"） |
| SC-08 | `page_class` 是否与该段结构匹配 |
| SC-09 | 段标题是否与 §6 逐字一致 |
| SC-10 | 是否所有段非空 |
| SC-11 | 是否出现"应当"以外的隐性义务表述 |
| SC-12 | 限定语（"仅""均""原则上"）是否与 KU 一致 |

---

## 10. 错误码表

| 错误码 | 级别 | 触发 | 处置 |
|---|---|---|---|
| `INSUFFICIENT_INPUT` | block | 必填缺失且无 gap | 补值或登记 gap |
| `GAP_UNKNOWN_FIELD` | block | `gap[].field` 不在 `ku-schema.md` §2.1/§2.2 的 29 个字段名内（回应第 3 轮复评 MJ-04：此前 `ku-schema.md` §2.3 引用该码但 §10 未定义） | 改 `field` 为合法字段名 |
| `NO_EVIDENCE` | block | `evidence_requirement` 为空数组且 `gap` 无 `field: evidence_requirement` 项；或 `evidence_requirement` 有值但 `status ∈ {in_force}` 而 `tier: C` | 登记 gap 并把 `status` 置 `draft`（回应原 M-13：原 §10 无本情形的码） |
| `SCHEMA_VIOLATION` | block | 语法/取值域/枚举不符 | 修文件 |
| `EXCERPT_MISMATCH` | block | 原文不逐字命中 | 改摘录 |
| `LANGUAGE_STRENGTH` | block | 动词越权 / 规避词 | 改措辞 |
| `CATEGORY_COLLAPSE` | block | 范畴坍缩 | 改表述 |
| `FIELD_BLOCKED` | block | 字段出现在禁止位置 / 来源未授权 | 移入派生块或换来源 |
| `NARRATIVE_FACT` | block | 正文出现事实形态 | 移入派生块 |
| `HASH_MISMATCH` | block | 派生块被手改 | 重新渲染 |
| `STALE_DERIVED` | block | KU 已变、页面未重编译 | 重编译 |
| `WHITELIST_VALUE_MISMATCH` | block | 结构声明值与 KU 不一致 | 改值 |
| `REQUIRED_SECTION_MISSING` | block | 必备段缺失 / "无"不合法 | 补段 |
| `DANGLING_REF` | block | 引用不可解析 | 修引用 |
| `ORPHAN_KU` | warn→block | 孤儿 KU 超 5% | 补页面或降级 KU |
| `CONFLICT_UNLOGGED` | block | 冲突未登记/未显示 | 登记 |
| `STALE_KU`（编译期） | warn | registry 指纹变更 | 排队重编译 |

---

## 11. 模板契约（解决原 M-03：强制项只写在模板注释里）

模板注释里的"【强制】/不得为空/至少 N 条"对人可见、对校验器不可见。rev1 起，这些要求全部升为下表编号，**模板注释只做解释，不创设规则**。

| 编号 | 规则 | 适用类 | 校验归属 |
|---|---|---|---|
| **TC-01** | `narrative_author` 非空（叙事段存在时），且必须是实名，不得为 `AI`/`auto`/空；`检查人`（§6.1）的实名段须与之逐字相等 | 全部（尤其 source） | CK-09 |
| **TC-02** | `## 更新记录` 是**唯一**允许出现 ISO 日期的段落，且日期只在表格单元格内；本表由渲染器从 `log.md` 生成，列固定 `日期 / 变更 / 操作角色` | source | CK-08（EX-4 显式豁免） |
| **TC-03** | 结构声明行只允许出现在 §6 表标注"允许结构声明"的段落，全页 ≤1 行 | entity / source | CK-09 |
| **TC-04** | `comparison` 的对比维度 ≤3；超 3 降级为两个 entity 页 | comparison | CK-10 |
| **TC-05** | `comparison` 的每个维度必须有 2 个 KU 的值，缺 1 个 → 该维度删除并在"不可比之处"登记 | comparison | CK-10 |
| **TC-06** | `topic` 的 `## 未决问题` 非空，或写合法"无"式（三类标签之一） | topic | CK-10 |
| **TC-07** | `concept` 的 `## 一句话定义` 必须来自 `definition` 字段渲染，不得手写 | concept | CK-08 |
| **TC-08** | 模板 front-matter 的 `page_id` 必须是槽位形式（含 `{{slug}}`），不得写具体值；**模板本身不参与页面级校验（CK-06~CK-10），但 `page_id` 槽位形态是硬要求** | 全部模板 | `grep -n "page_id" wiki/templates/` 每行须含 `{{slug}}` |
| **TC-09** | `rendered_blocks` 元素数 = `kb:derived` + `kb:table` **块数**，且顺序与块 `id` 逐一相等。**块数口径（rev2）**：只统计**开标记行** `<!-- kb:derived id="` 与 `<!-- kb:table id="`，**不计**闭标记与正文里反引号内的字样（模板注释、填法要点会引用工具名，用 `grep -c "kb:derived\|kb:table"` 会多数一倍，属仪器缺陷）。可复现命令：`grep -cE '<!-- kb:(derived\|table) id="' 模板文件` | 全部 | CK-10（结构项）/ `SCHEMA_VIOLATION` |
| **TC-10** | 块 `id` 从 `b1` 起连续无跳号，同页唯一，格式 `b<正整数>` | 全部 | `SCHEMA_VIOLATION` |

> 交付卫生检查项（非 CK）：无水印 front-matter（`AIGC.*`）、无页脚"由 AI 生成"、模板 `page_id` 全为槽位。

### 11.1 `page_class` × 允许 fact-bearing 字段集（`CK-09` 的判据表，解决 MJ-01）

`CK-09` 此前只写"允许集校验"而未给出允许集，因此无法判定任何 `fields`。本节逐类列出，**表中未出现的字段名出现在该类的 `fields` / `cols` 即 `FIELD_BLOCKED`**。表内取值与六套模板的实际 `fields` / `cols` 逐一对应。

| page_class | 允许的 fact-bearing 字段（`fields` / `cols` 用） | 允许的簿记提交项 |
|---|---|---|
| `overview` | `title`(→`short_name`) `jurisdiction` `instrument_type` `instrument_is_binding` `obligation_nature` `status` | 无 |
| `concept` | `title`(→`short_name`) `jurisdiction` `instrument_type` `obligation_nature` `definition` `scope_in` `scope_out` `obligation` `applies_to` `common_misreadings` | 无 |
| `entity` | `title` `instrument_type` `instrument_is_binding` `jurisdiction` `status` `effective_date` `transition_note` `applies_to` `obligation` `evidence_requirement` | 无 |
| `comparison` | `title`(→`short_name`) `jurisdiction` `instrument_type` `instrument_is_binding` `obligation_nature` `applies_to` `status` | 无 |
| `topic` | `title`(→`short_name`) `jurisdiction` `instrument_type` `instrument_is_binding` `status` `obligation` | 无 |
| `source` | `title` `instrument_type` `instrument_is_binding` `jurisdiction` `published_date` `status` `effective_date` `transition_note` `obligation` `evidence_requirement` `applies_to` | 无 |

- `short_name` 是 `title` 的派生呈现名，只在 `kb:table` 的 `cols` 中合法，**不得**出现在 `kb:derived` 的 `fields` 中。
- 结构声明行（§2.5）不受本表约束，其白名单恒为 3 字段。
- 扩展本表必须同时改模板与 `CK-09` 实现，属 RFC 范围（`01-整体规划.md` §9）。

---

## 12. 派生块渲染样例（解决原 m-03：原模板只有空占位）

以下为 `entity` 页一个真实渲染后的块（含标记行），用于对照写法，不参与任何页面校验。

```markdown
<!-- kb:derived id="b1" ku="ku-us-nist-ai-rmf-govern" fields="title,instrument_type" render_hash="sha256:3a7c1e5d0b8e4f21a6d3c9b7e5f8a2d4c6b0e9f1a3d5c7b2e4f6a8d0c2b4e6f8" ku_hash="sha256:41ab9f022c7d4e8b1a3f5c9d2b6e0a4f7c1d3b5e9a2c8f0d4b6e1a3c5f7d9b2e" -->
**Artificial Intelligence Risk Management Framework (AI RMF 1.0)** —— 类型：`voluntary_framework`
<!-- /kb:derived -->
```

要点：

1. 块内只出现 `fields` 声明的字段值，不出现字段名。
2. 标记行四要素（`id` / `ku` / `fields` / 两个 hash）齐全，顺序固定；hash 为 `sha256:` + **64 位**小写十六进制（原 8 位截断示例作废，m-07）。
3. 块内**没有**"该文件要求……"这类义务句——义务句只能在渲染 `obligation` 的块里。
4. 人改任何一个字 → CK-06 `HASH_MISMATCH`；KU 改了不重编译 → CK-07 `STALE_DERIVED`。
