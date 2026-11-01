# 继承契约摘要（rev4 → grc-skill-agent v0.1）

> 用途：让评审人在不读 60 KB 附件的情况下，核对设计对上游契约的继承是否失真。
> 标注 `[照抄]` = 原样继承；`[改]` = 本设计变更；`[新增]` = 本设计新增。
> 权威全文见 `attachments/rev4-ku-schema.md` 与 `attachments/rev4-wiki-schema.md`。

---

## 1. KU 字段（29 = 17 fact-bearing + 12 bookkeeping）[照抄]

**fact-bearing（#2–#18，17 个）**：
`jurisdiction` `instrument_type` `instrument_is_binding` `obligation_nature` `obligation` `evidence_requirement` `applies_to` `status` `effective_date` `transition_note` `verbatim_excerpt` `definition` `scope_in` `scope_out` `common_misreadings` `published_date` `title`

**bookkeeping（#1 + #19–#29，12 个）**：
`ku_id` `source_id` `source_class` `tier` `confidence` `source_class_confidence` `as_of` `locator` `registry_id` `snapshot_ref` `first_seen` `fingerprint`

**关键约束**：
- `instrument_type` 11 值闭合：`statute` `regulation` `executive_order` `binding_guidance` `nonbinding_guidance` `voluntary_framework` `management_system_standard` `certification_scheme` `vendor_standard` `industry_standard` `advisory`；`instrument_is_binding` 必须与该表 binding 列一致。
- `locator` 5 形态（条款式 / 罗马或数字章节式 / 命名章节式 / 页码式 / 条目式），禁止混写；细化信息进 `snapshot_ref` 锚点。**本设计扩为 7 形态**：条款式（允字母项）、中国条款式（含款/项）、附件式 `[改]`。
- `gap` 是登记对象**不是第 30 个字段**（4 键：field/reason/owner/due）；`owner` 用 `R-* / 实名` 两段式。
- 概念字段（`definition`/`scope_in`/`scope_out`/`common_misreadings`）：被 concept 页引用时必填，缺失即 `status: draft`。
- `confidence: low` → `status: draft`。

---

## 2. 页面与派生块 [照抄]

- 六类页面：`overview` / `concept` / `entity` / `comparison` / `topic` / `source`；必备段逐字固定（见附件 §6）。
- 派生块：`<!-- kb:derived id="b1" ku="..." fields="..." render_hash="sha256:…" ku_hash="sha256:…" -->`；`kb:table` 同规则。
- `render_hash` 覆盖块正文，输入串含 `ku|fields|template_version`；`ku_hash` 覆盖该 KU 全部 fact-bearing 字段 → 检"KU 改了页面没跟上"。
- front-matter 8 键闭合：`page_id` `page_class` `template_version` `status` `as_of` `ku_refs` `rendered_blocks` `narrative_author`。
- `rendered_blocks` = 块开标记 id 序列；块 id 从 `b1` 连续。
- 结构声明行白名单仅 3 字段：`instrument_type` `instrument_is_binding` `jurisdiction`，仅 entity/source 指定段、全页 ≤1 行。

---

## 3. 13 条校验 [照抄，除 C1 变更]

| 编号 | 名称 | 判据要点 | 错误码 |
|---|---|---|---|
| CK-01 | 字段完备与取值域 | 29 字段必填/枚举；binding 一致性 | `INSUFFICIENT_INPUT` / `SCHEMA_VIOLATION` |
| CK-02 | 措辞强度 | STR-01/02/03 + (source_class × obligation_nature) 矩阵 + 规避词 | `LANGUAGE_STRENGTH` / `CATEGORY_COLLAPSE` |
| CK-03 | 原文一致性 | `verbatim_excerpt` 必须与来源逐字一致；**本设计改为 online/manual/offline/expired 四态** `[改]` | `EXCERPT_MISMATCH` |
| CK-04 | 缺失登记 | 条件必填 null ⇒ gap 有对应项；gap 非空 ⇒ draft | `INSUFFICIENT_INPUT` |
| CK-05 | 来源授权 | vendor/community/advisory 不得单独支撑义务页；tier C 不作事实源 | `FIELD_BLOCKED` |
| CK-06 | 派生块封签 | 重算 render_hash | `HASH_MISMATCH` |
| CK-07 | 派生块新鲜度 | 重算 ku_hash | `STALE_DERIVED` |
| CK-08 | 正文禁止面 | 对 body_markdown 应用 EX-1~EX-7 后扫 DF-1/2/3/4/4c/5/6 | `NARRATIVE_FACT` / `FIELD_BLOCKED` |
| CK-09 | 结构声明一致性 | 结构声明行 + page_class×字段允许集 + H1 + 检查人实名比对 | `WHITELIST_VALUE_MISMATCH` 等 |
| CK-10 | 必备段与状态行 | 六类段标题集合、合法"无"式、状态行 | `REQUIRED_SECTION_MISSING` |
| CK-11 | 断链 | ku_refs/refs.json/[[...]] 可解析；**本设计增 log.md subject 解析** `[改]` | `DANGLING_REF` |
| CK-12 | 孤儿 KU | 未引用 KU ≤5% | `ORPHAN_KU` |
| CK-13 | 冲突显式化 | conflicts.yaml 结构 + open 冲突页面标记；冲突存在性**人工** | `CONFLICT_UNLOGGED` |

**门禁**：CK-01~CK-12 全绿；CK-13 结构项入自动门禁，"是否真冲突"人工签署。
**已知遗留**：rev4 的 N-11 = CK-11/CK-09 未承接 `log.md` → 本设计 W1 第一件事修复 `[改]`。

---

## 4. 写作禁令与判据 [照抄]

- **WS-01** 正文不得出现事实形态（DF-1~6）；扫描面 = `body_markdown`（front-matter 除外）。
- **WS-02** 17 个 FB 字段值只能在派生块/`kb:table`；12 个 BK 字段名与值不得进正文；例外=结构声明行。
- **WS-03** 原文逐字；**WS-04** 块内容=渲染器输出；**WS-05** low/gap 须带 ⚠；**WS-06** 非 in_force 须有状态行；**WS-07** 范畴坍缩禁止表；**WS-08** vendor/community/advisory 授权；**WS-09** 冲突登记不消解。
- **DF-1~DF-6**：日期 / 条款定位 / 状态词 / 字段名 / 义务动词+主体 / 数字+期限；**DF-4b** 限豁免三固定短语；**DF-4c** 拦截"强制 vs 自愿"式对比改述。
- **EX-1~EX-7**：front-matter / 派生块 / 结构声明行 / 更新记录日期列 / 合法"无"式中的检查日期 / H1（须=title 或 slug）/ `[[]]` 与 `ku-*`。
- **STR-01** `instrument_is_binding=false` → 全文禁 VB-OBL；**STR-02/03** 双向强度约束。

---

## 5. 图与运维 [照抄 + 新增]

- `refs.json` 4 键闭合：`schema_version` / `generated_from` / `ku_to_pages` / `page_to_kus`；互转置、边数由运行时统计。
- `log.md` 4 列：`date` / `event`（INGEST|RECOMPILE|RECHECK|SIGNOFF|SUPERSEDE）/ `subject` / `actor`；只追加。
- `conflicts.yaml` 8 字段；`dimension` 7 值闭合；三态 status。
- `[新增]` `kb/catalog.yaml`（topic/alias → ku_id，检索用）
- `[新增]` `rules/applicability-{eu,cn}.yaml`（适用性规则：id/ku_ids/jurisdiction/applies_when/obligations_from/priority/exceptions）
- `[新增]` `kb/profiles/*.yaml`（判定画像样例）

---

## 6. 本设计的变更清单（评审重点）

| # | 变更 | 影响 | 需要评审回答 |
|---|---|---|---|
| C1 | 快照只存摘录+链接，不存全文 | CK-03 状态机（pending/online/manual/expired）；答案公示核验模式 | "可审计"是否被降级？最小修法？ |
| C2 | 作答语言 = 用户/指定语言；原文不译 | `language` + `translations` + claim `binding_mode` | 结构是否可表达？ |
| C3 | 四张非 KU 表（catalog/rules/profiles/scope_exclusions） | 检索/判定/否定句 | 是否污染契约？谁保证不承载事实？ |
| C4 | locator 7 形态 | CK-01 | 是否闭合？区间如何处理？ |
| C5 | claim+prose 双轨 | binder | 是否可执行？归纳/否定/译文如何绑定？ |
| C4 | N-11 修复 | CK-11/CK-09 | 修法是否足够？ |

---

## 7. 上游五轮评审的根因（来自 08 报告，用于 D8）

| 机制 | 含义 | 本设计的对策位置 |
|---|---|---|
| G-1 规则-载体脱节 | 改规则不改消费它的数据/模板 | §6.2 影响面矩阵 + CI 拦截 |
| G-2 判据缺四要素 | 判定主体/输入/值域/错误码不齐 | §5.1 P-3；CK 表延续四要素 |
| G-3 仪器污染 | 探针与被检文本同包 | §9.3 正反基线 + 排除探针载体 |
| G-4 元信息漂移 | rev/轮次/章节/计数无 lint | §9.3 P-1 生成化 + lint |
| G-5 自评替代复核 | 作者声明"已修"无实测 | §13 流程：CCC 独立评审 + 实测证据 |
