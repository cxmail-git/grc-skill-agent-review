# 预演复审（非 CCC 正式报告）｜对象：v0.2｜轮次：2

> 评审人：独立复审（非实现者）｜日期：2026-10-31｜性质：dry-run 第 2 轮，不代表 CCC 正式结论
> 被评对象：`docs/specs/2026-10-31-grc-skill-agent-design-v0.2.md`（下称 v0.2）
> 对照：`pre-review-report.md`（v0.1 34 条）、`pre-review-resolution.md`（处置表）、`CCC-review-brief.md`、`ku-plan.md`、两份样例 KU、`impact-matrix.md`、`evidence/`；`contract-digest.md` 与 rev4 附件按需核对
> 边界：不评法条实体内容、不写代码、不改任何被评文件。凡依赖法条原文的判断标「需作者核实」。本轮**不复用作者证据**，locator/样例/数字/CI 判据均自跑自算（见 §8）。

---

## 0. 总裁定

**B 有条件通过**。命中一票否决：**无**。

- 计数：原 7 Block → **1 真修、5 部分、1 未修**；新增 Block **3 条**（N-01/N-02/N-03）；当前仍有 **5 个 Block 级开口**（F-04、F-07、N-01、N-02、N-03）。Major 18 条中本轮实核 11 条（7 条仅部分落地，F-20 完全未落地），Minor 10 条。
- 一句话：v0.2 把**字段与枚举**补得很齐，但没有把**判据方向**和**输出闭合**补上——CI 仍拿"申报集"当允许集（F-07 未修），claim 只验 claim、prose/`translations` 仍是自由文本（N-01），`absence` 的依据仍是一句口号（N-02），三条金标与库/接口互斥（N-03）。
- 与 v0.1 的差别：v0.1 的问题是"契约没写"；v0.2 的问题是"契约写了，但判据反向或字段未闭合"，后者更危险，因为它看起来已经可执行。
- 降级触发器：若作者反驳 **C1（CI 判据反向）** 或 **C2（CK-03 证据门禁）** 且不给替代判据 → 本裁定应降为 **C 不通过**。
- 对"34 条已吸收"的独立判断：**字段层吸收率约 2/3，验收层吸收率不足 1/2**。处置表里"采纳"的 7 个 Block，真正落到可执行判据的只有 F-02；F-07 的处置文本与 v0.1 的错误判据**方向相同**。

---

## 1. 七个 Block 逐条核对

> 读法：v0.1 问题 → v0.2 实际文本（§号+引文）→ 判定 → 残留缺口。

| # | v0.1 问题 | v0.2 实际文本（§号+引文） | 判定 | 残留缺口 |
|---|---|---|---|---|
| **F-01** | locator 5 形态对 EU 字母项/附件/区间不闭合；33 条 EU 中 15 条非法 | §5.2 C4：「`locator` 扩为**7 形态**：① 条款式 `^Art\.\d+((\(\d+\))\|(\([a-z]{1,3}\))){0,4}$`；…⑥ 中国条款式 `^第[…]条(第[…]款)?(第[…]项)?$`；⑦ 附件式 `^Annex [IVX]+( point \d+)?(\([a-z]\))?$`。**禁止区间**」；ku-plan 52 条单 locator | **部分** | 52/52 只对 ①⑥⑦ 三条正则成立（自跑，见 §4-①）；②–⑤ 四形态仍只有名字、无正则，CK-01 无法判；⑥ 不匹配 `第四条第（二）项`（v0.1 F-08 点名的形态）；rev4 §3.1「子款不得混入 locator」硬约束未被明文废止；`excerpt-candidates.md` 仍有 3 条禁用区间 locator、7 个旧 ku_id（N-05） |
| **F-02** | C2 用户语言 vs binder「连续子串」互斥 | §5.2 C5：「claim（证据单元）+ prose（措辞）双轨；claim 有 `binding_mode: quote\|translation\|frame` 与 `support_type: direct\|composite\|absence\|frame`」；§7.2-3：「`translation` 的 `verbatim` 绑原文、`text` 为译文并标 `machine`」 | **是**（原互斥解除） | 互斥本身已解；但替代路径不可执行：§5.2 C5 写「binder 只校验 claim，不校验 prose」，§7.2-4 却写「prose 每个句子必须映射到 ≥1 claim，否则 binder 失败」，而 §7.1 没有 `sentence_map` 字段 → 新 Block N-01 |
| **F-03** | 归纳/否定/跨域/时间句无绑定路径；refusal 缺 `scope_correction` | §7.2-2：「否定/缺失句…`absence`，依据 `kb/scope_exclusions.yaml` 条目（含 `registry_id` + `as_of` + 理由），**不假装有 KU**」；§7.1 refusal 增 `scope_correction`；§7.2-6 `partial` 三义 | **部分** | `absence` 只有"应绑"的声明：`scope_exclusions.yaml` 不在 §5.4 目录树、无字段 schema、无 CK/lint、无样例；claim JSON 也没有 `scope_exclusion` 键（只有 `ku_ids`）；§9.2 的 citation 覆盖只要求"有 `ku_ids` 或 `scope_exclusion`"，不校验条目存在 → 任意否定句都能"有依据"（N-02） |
| **F-04** | CK-03 四态无状态机；manual 证据无字段 | §5.3 增 4 条转移（pending→online/manual、online/manual→expired、expired→manual/online）+ `verification_url`/`page_digest`/`evidence_ref`；「**offline…只允许用于 `status: draft`，不得发布**」 | **部分** | snapshot 头枚举写「`# pending \| online \| manual \| expired`」——**没有 offline**；状态机也没有任何→offline 的转移，offline 只在布尔规则里出现一次；发布门禁只查 `verification ∈ {online, manual}`，**不查 `evidence_ref`/`verified_by`**，手填 `manual` 即可发布；`verification` 是自由 YAML 字段，手填 `online` 也无需抓取产物；`expired` 只能靠人跑 `freshness` 触发，发布门禁不按 `verified_at+max_age` 重算（§4-⑦） |
| **F-05** | verdict 缺"未生效/部分适用"，EU 时间窗必给错 | §8.2：「`verdict: applies\|applies_later\|no_rule_matched\|insufficient_info\|out_of_scope`」「`applies_later`：命中规则但 `currently_in_force=false`（`applies_from` 必填）」；§8.2 示例 `applies_from: 2027-12-02` | **部分** | 枚举补了，但 §0/§1.2/G3/§8.4/R3 仍写「三态」；G3 验收仍是「适用/不适用/信息不足/超范围」四类，**没有 applies_later**，而 W2 又要求「含 1 个 applies_later」；每 KU 只有一个 `effective_date`，无法同时表达 Annex III 2027-12-02 与 Annex I 2028-08-02；`applies_from` 无 `basis_ku`/`basis_verbatim`，不可回放（N-04） |
| **F-06** | 运算符表达力不足；`in` 对 list 语义未定义 | §8.3：「`in`/`not_in`：**标量 ∈ 列表**（不是列表 ⊂ 字段）」「`intersects`：字段列表 ∩ 值列表 ≠ ∅」「`contains_all`：值列表 ⊆ 字段列表」「`judgement_required`：`{field, question, answer: true\|false\|unknown}`；`unknown` → `insufficient_info`」；求值顺序 exceptions→priority | **部分** | `in/not_in/intersects/contains_all` 语义已闭合；但 `judgement_required` 没有输入通道——§8.1 profile 无 `judgements` 字段，CLI/MCP 也无"向用户提问并回填"的步骤；Art.6(3)「未实质性影响决策」仍无法表达（把 answer 写死在规则 YAML 里没有意义）；`exceptions` 仍只有字段名，无表达式 schema |
| **F-07** | CI 判据是"变更集 ⊆ 全表并集"，拦不住"改规则不改样例" | §6.2：「`consumers = graph_affected(ku_ids)`…**不靠手写申报**」「`actual_changed ⊆ changed_files ∪ consumers`，否则 `IMPACT_UNREPORTED`」「CI 反向探针：固定一个'故意漏申报'的 fixture，必须 FAIL」 | **否** | 判据方向没变：仍是被动允许集，不是"必须更新集"。改 `rules/applicability-eu.yaml` 且 `changes/<id>.yaml` 声明 `ku_ids:[gsk-eu-art6-3]`，图计算会带出页面/金标，但 `actual_changed={规则文件} ⊆ declared ∪ consumers` → **PASS**，页面与金标原样未改；`ku_ids` 仍是申报字段，声明 `ku_ids: []` 就让 consumers 为空；`depends_on` 定义了却从未被 CI 消费；矩阵文件 `docs/impact-matrix.md` 也不被任何 CI 步骤读取；其第 25 行「未改即 FAIL」与 §6.2 步骤 3 直接矛盾（§4-⑤） |

### 1.1 F-07 的复现（最短路径）

1. `changes/CH-x.yaml`：`changed_files: [rules/applicability-eu.yaml]`、`ku_ids: [gsk-eu-art6-3]`、`depends_on: [eval/golden.yaml, kb/pages/entity-eu-art6.md]`。
2. 实际只改规则文件；`eval/golden.yaml` 与页面不动。
3. `actual_changed={rules/applicability-eu.yaml}`；`consumers` 含页面/金标/规则→KU 字段，是**允许改**的集合；子集判断为真 → PASS。
4. 反向探针用的是"漏申报一个**新文件**"，它测的是 `actual_changed ⊄ declared`，测不到"声明了消费者但没更新"。→ 这正是 G-1 的原始形态，v0.2 只是把"全表并集"换成了"单 change 并集"。

**结论**：F-07 应判 **未修**，不是"部分"。修法见 C1。

**判级说明**：F-01/F-03/F-05/F-06 的残余分别由 N-05/N-02/N-04/N-09 承接并降为 Major，不再单独计 Block；F-04、F-07 仍是 Block；新增 N-01/N-02/N-03 为 Block。故"当前 Block 级开口 5 条"= F-04、F-07、N-01、N-02、N-03，与 §0 的计数一致。

---

## 2. Major 落地核对

### 2.1 brief 点名 / 任务指定的 11 条

| # | v0.2 位置与文本 | 落地 | 残留与判据 |
|---|---|---|---|
| F-08 | §5.2 C4 ⑥ 增款/项；§7.1 `citations[].anchor` | **部分** | ⑥ 不匹配 `第四条第（二）项`；CN 样例 5 条义务同属 `第七条`，`anchor` 仅 `#art7`，无项级锚点；`citations[].locator` 仍只能写"第七条" |
| F-09 | §5.3「**每条 KU 一份 snapshot**」；§9.2「100% KU 可解析到 `(snapshot, verification, verified_at)`」 | **部分** | §5.4 registry 示例是**每来源**一条（`reg-eu-ai-act`），却只带一个 `snapshot_ref`/`excerpt_hash`/`verification`；32 条 EU KU 共用一条 registry 无法逐 KU 核验；样例 `registry_id: gsk-eu-art14` 又指向 KU 而不是 `reg-*` 条目 → 两份真值源（N-06） |
| F-10 | §5.3/§5.4/§7.1 增 `verification_url`，与 `source_url` 分离；EUR-Lex 走 manual | **是**（设计层） | 样例没有 snapshot 文件，`page_digest`/`evidence_ref` 无实测；`source_url` 仍是 EUR-Lex，用户点开的仍不是被核验页 |
| F-12 | §5.1/§7.2 增「`obligation[].text` 必须为 excerpt 连续子串」；`fingerprint` 格式校验 | **部分** | 自跑：两份样例 6/6 条 obligation 均为子串（真修）；但两份 `fingerprint` 完全相同（`minhash96:000…001`），格式正则通过，却证明它仍是占位——两个不同 excerpt 不可能有同一 MinHash，且无"fingerprint 必须由 excerpt 计算"的校验；`evidence_requirement` 两份均为 `[]`，字段形状仍未受检 |
| F-16 | §0/§3.1/附录 B/E 统一「52 KU（EU 32 + CN 20）」 | **部分** | §1.3 仍写「不在 50 KU 内」，R2 仍写「50 KU」且「CN 允许 15–20 弹性」；附录 B 的分项 `1+5+3+4+8+1+3+1+3+1=30` 却标 32；§3.1/附录 B 写「Art.5 选 5 项」，ku-plan 实为 7 项；附录 D 仍「30±3 / 14–16 / 6–8」；approval-checklist 仍「50 KU / 15 题」（N-07） |
| F-17 | §9.1「分类由脚本统计」；§9.2 金标拒答 5/5、负例 5/5 分列 | **部分** | 附录 A 仍有 `refuse/纠正`（#9/#17）、`answer/insufficient`（#16）、`insufficient_profile`（#14，非 mode 枚举值）；严格 `refuse` 只有 #4/#10/#20 三题，"金标拒答 5/5"无法由脚本算出；"独立负例 5 题"全文一致，**不存在"20 独立负例"** |
| F-19 | §11 R1「3 周内只承诺发布前核验」；§5.3 `freshness --now` 制造 expired 探针 | **是**（设计层） | approval-checklist §5 仍要求「接受 expired 降级与人工周检」，与 R1 的"不承诺周检"相反；W1/W2 排期无周检成本（若按旧承诺会再吃 3.3 人日/周） |
| F-20 | §4.2.1 `ask`：「`{query, language?, jurisdiction?, no_llm?}`」 | **否** | 处置表写"ask 增可选 `profile`"，实际**没加**；§7.2-8 又禁止 ask 推断适用性 → 附录 A #14「给'内部研发自用'画像时 answer」没有任何入口；`insufficient_profile` 只能是拒绝理由，不能是成功路径（N-03） |
| F-21 | §9.1 每题 `retrieval_expect`；§9.2 top5 ≥18/20；§4.2 bigram + alias | **部分** | 没有"每题至少 1 个别名"的覆盖门槛（处置表声称有）；W1-4 仍是「5 个已知 query 的 top-3」，与 20 题 top5 验收不一致；`catalog.aliases` 仍由作者手写，无覆盖统计 |
| F-23 | §7.1 `citations[]` 增 `verbatim`/`verified_by`/`anchor`；`refusal` 仅 `mode=refuse` 出现 | **是** | 无实质残留；仅 `anchor` 的取值域（`p1`/`#p1`/`art7` 三种写法）未统一 |
| F-32 | §7.1 `partial_reason: conflict\|cross_jurisdiction\|coverage_gap`；§7.2-6 三义；#19 用 `groups` | **部分** | `partial_reason=conflict` 与 `refusal.reason=conflict_unresolved` 是同一条件的两套值，何时用哪个未写；`groups` 只有 `claim_ids`，没有"组必须覆盖全部 claims"的规则；#3 的 `coverage_gap` 与"5 项"文本又冲突（N-03） |

### 2.2 其余 Major 抽查

| # | 落地 | 残留 |
|---|---|---|
| F-13 | **否** | 处置表说"导入时补 4 张闭合表（modality/subject/frequency/scope_type）"，v0.2 正文没有这 4 张表；样例 `applies_to[].scope` 仍是自由文本（`high-risk AI systems` / 中文长句），没有 `scope_type`/`scope_note`；`frequency` 因 `evidence_requirement: []` 从未被检验 |
| F-14 | **部分** | §8.2 增 `as_of`/`verification`/`verified_by`，但没有复用 §7.1 的 `citations[]`/`freshness`；`findings[].basis_verbatim` 无"必须是 KU 字段子串"的校验；`findings[].obligations` 是自由文本数组（`"Art.26(2) 指派人工监督"`），可幻觉 |
| F-15 | **部分** | 求值顺序写死（exceptions→priority→同 priority 异结论才 `insufficient_info`）是进步；但 `exceptions` 的表达式 schema、`priority` 的取值域、`--explain` 输出字段均未定义 |
| F-18 | **部分** | 稳定性只比 `(ku_id, locator, verbatim)` 集合、独立脚本重算、`--llm/--no-llm` 分列，均落地；但 frame claim 无 `ku_ids`，§9.2「claims 100% 有 `ku_ids` 或 `scope_exclusion`」会把 frame 判失败（分母未排除） |
| F-22 | **部分** | 矩阵重写为 change_id 行，CH-C4 有 `evidence/CH-C4-locator-check.txt`；但 CH-C5/CH-CK3 的 `changed_files` 用 `docs/specs/…v0.2.md`（省略号，不是真实路径），evidence 写「见 W1 契约干跑」（不是产物文件）；CI 不读矩阵，规则无法执行 |
| F-26 | **部分** | EU title 改为「Article 14 — Human oversight」；CN 仍是「第七条 — 训练数据处理」（编辑加工标题），`source_id`/`registry_id` 仍把 `registry_id` 填成 `ku_id`（应为 `reg-*` 主键） |
| F-34 | **部分** | §4.2.1 增 6 条协议用例（握手/未知工具/参数非法/业务失败/大响应/并发）；但 `protocolVersion` 协商值、JSON-RPC 协议错误与业务错误的边界、`>64KB` 是分块还是截断、并发"不串话"的判据均未写 |

**Minor 抽查（不展开）**：F-27 §1 顺序已修，但头部仍手写「9 处」（v0.1 自检为 11 处）；F-28 设计删了 19，`w1-plan.md` W1-3 仍写「边数=19→本项目数」；F-29 三处顺序仍不一致（设计 §13 第 5 条「修 N-11 → scaffold」；w1-plan「scaffold → W1-1a N-11」；approval「W1 第一件事 = 修 N-11」）；F-30 已收窄到 DSH + Claude Code；F-31 仍无 `MANIFEST.md`，brief 仍列 `02-design-v0.2.md`/`05-pre-review-report.md` 等不存在路径；F-33 approval-checklist 第 22 行仍写「CK-03 **三态**（online/offline/expired）」。

---

## 3. v0.2 新问题（回归 / 新不一致 / 新不可执行点）

| # | 级别 | 位置 | 判据 / 反例 | 修法 |
|---|---|---|---|---|
| **N-01** | **Block** | §5.2 C5 vs §7.2-4/§7.3；§7.1 `answer`/`translations` | C5 写「binder 只校验 claim，不校验 prose」，§7.2-4 写「prose 每个句子必须映射到 ≥1 claim，否则 binder 失败」；输出没有"句→claim"映射字段，`answer` 是一整串自由文本。构造：claim c1 只支持"提供者应做风险管理"，answer 追加一句"不做的后果是罚款"——binder 只验 c1 → 通过；独立脚本重算 claims 也通过 →「无据断言 0」为真，用户却读到无据句。`translations[]` 只有 `{lang,text,source}`，无 `claim_ids`，同样不受 binder 约束 | ① `answer` 改为 `[{sentence, claim_ids[]\|frame}]` 或增 `sentence_map`；② `translations[].claim_ids` 必填并纳入 binder/独立脚本；③ 删除 C5 的"不校验 prose"或改为"prose 只允许 claim 文本的复述"；④ 给 §7.2-4 配 1 个反例夹具 |
| **N-02** | **Block** | §5.2 C3、§7.2-2、§9.2 | `kb/scope_exclusions.yaml` 只在 C3/§7.2 出现，§5.4 目录树没有它，无字段 schema、无 CK、无 lint、无样例；claim JSON 没有 `scope_exclusion` 字段（只有 `ku_ids`）；§9.2 只要求"有 `ku_ids` 或 `scope_exclusion`"，不校验条目存在。构造：claim `{support_type:"absence", ku_ids:[], scope_exclusion:"no-such-id"}` → 指标判"有依据"，CK 无码可报 | ① 定义 `scope_exclusions.yaml` 条目 schema（`id/jurisdiction/registry_id/as_of/reason/evidence_url`）；② claim 增 `scope_exclusion_id`；③ 新增 `CK-14`：absence claim 必须解析到条目且 `as_of` 不为空；④ 把该文件加入 §5.4 树；⑤ #9/#17 用真实条目做正例、伪造 id 做反例 |
| **N-03** | **Block** | 附录 A #1/#3/#14 vs 附录 B/ku-plan/§4.2.1 | #1 期望「Art.16 + 8–15 + **43**」，附录 B 明写「Art.43/17/19/49 等——未收录」；#3 期望「列出库内 **5** 项」，ku-plan 有 **7** 条 Art.5（c/d/e/f/g/h/ba），若答 5 则漏 2 条在库项并谎称"其余未收录"，若答 7 则金标文本错；#14 期望"给画像时 answer"，但 `ask` 入参没有 `profile`、§7.2-8 禁止 ask 判适用性，唯一入口 `determine` 的 verdict 又不是 `insufficient_profile` | 三题重写后再冻结：① #1 删除 Art.43 或把 Art.43 纳入 52 条并同步附录 B；② #3 改 7 条并让 `coverage_gap` 只声明"Art.5 其余项未收录"；③ #14 二选一——`ask` 增 `profile?`，或把期望改为 `refuse(insufficient_profile)` 并把"给画像"用例移到 `determine` 的 10 个判定用例；④ 三题 `expected_mode` 必须单值，由脚本统计 |
| **N-04** | Major | §1.4、§5.1 #10、§8.2、`eu-article-map.md` Art.113、`excerpt-candidates.md` | 每 KU 只有一个 `effective_date`；§1.4 说高风险义务有两个适用日（Annex III 2027-12-02 / Annex I 2028-08-02），但 `gsk-eu-art14` 只能写一个 2027-12-02 → Annex I 系统会得到错误 `applies_from`；`applies_from` 无 `basis_ku`/`basis_verbatim`，不可回放；`eu-article-map.md` Art.113「段落数：0」，唯一候选摘录却写「It shall apply from 2 August 2026」，与 2027-12-02/2028-08-02 不一致 | ① 适用日改为规则级 `applies_from` + `basis_ku`/`basis_locator`，按 Annex I/III 分列；② 重抓合并版 Art.113 正文并逐字入库，或删除 2027/2028 断言只答"见 Art.113"；③ `currently_in_force` 用 `evaluated_at`（运行日）而非 `as_of`（核验日）；④ #7 金标加"两个日期各 1 个 KU/规则"的期望 |
| **N-05** | Major | `excerpt-candidates.md` 全表 vs `ku-plan.md` | 自跑：候选表 **53 行（EU 33 + CN 20）**，其中 **3 条 locator 非法**（`Annex III 1–4`、`Annex III 5–8`、`Art.50(3)-(4)`）；**7 个旧 id 不在 52 计划**（`art5-ab/bb`、`annex3-a/b`、`art26-3`、`art43`、`art50-34`）；**6 个计划 id 无候选**（`annex3-1/3/4/5`、`art26-5`、`art50-3`）；`art26-5`（金标 #5 的日志义务）无摘录；`art43` 仍在候选表而附录 B 说未收录 | ① 以 ku-plan 为准重生成候选表（id 集合、locator 集合必须相等）；② 删 `art43` 或改附录 B；③ 补 `Art.26(5)` 与 `Art.50(3)` 摘录；④ CI 加一条 `set(ku-plan.ids)==set(excerpt.ids)` 与 locator 校验 |
| **N-06** | Major | §5.2 C1、§5.3、§5.4 registry 示例、样例 `registry_id` | C1 说核验元数据落在「每 KU 一份的 snapshot 头**与 registry 条目**」，§5.4 的 registry 条目却是每来源一条（`reg-eu-ai-act`）且只有一个 `snapshot_ref`/`verification`；样例 `registry_id: gsk-eu-art14` 指向 KU，而条目主键是 `reg-*` → 同一事实两处存储、可漂移，且 CK-11 会判悬空 | ① 明确"snapshot 为唯一真值，registry 只存来源级字段"；或 registry 改每 KU 一条；② 禁止两处同时存 `verification`；③ 样例 `registry_id` 改为 `reg-eu-ai-act`，并加 CK-11 反例 |
| **N-07** | Major | §1.3、§3.1、R2、附录 B/D、approval-checklist | 自跑：附录 B 分项和 = **30**，却标 32；§3.1/附录 B 写「Art.5 选 5 项」，ku-plan 7 项；附录 D「30±3 / 14–16 / 6–8」；R2「50 KU / CN 15–20」；approval「50 KU / 15 题」；候选表 EU 33。52 只在标题层自洽，分项层不自洽 | ① 由 `gen_numbers.py` 生成所有计数（含附录 B 分项）；② 删除 R2 的 KU 弹性或改为"52 不减"；③ approval-checklist 同步 52/20；④ 附录 D 的 30±3/14–16/6–8 改为 32/13/7 |
| **N-08** | Major | §0、§1.2 G3、§8.4、R3 vs §8.2 | §8.2 枚举 5 值，§0/§1.2/§8.4/R3 仍写"三态"；G3 验收 4 类，W2 却要求 1 个 applies_later；`no_rule_matched` 取代"不适用"但 G3 仍写"不适用" | ① 统一改"五态（applies/applies_later/no_rule_matched/insufficient_info/out_of_scope）"；② G3 验收加入 applies_later 与 no_rule_matched；③ W2 的 10 用例与 G3 的分类表同源生成 |
| **N-09** | Major | §7.2-1、§7.3 | frame 只排除 **DF-1/2/4/6**（日期/条款定位/字段名/数字期限），**不排除 DF-3（状态词）与 DF-5（义务动词+主体）**；任何不含数字/日期/条号的义务句都可标 `frame`，从而免绑 KU。构造："提供者必须建立风险管理体系"（DF-5，无 DF-1/2/4/6）→ `binding_mode=frame` 通过 | ① frame 必须排除 DF-1~DF-6 全部形态；② 明确 frame 只允许"定义/方法论/回答结构"句，并给 1 个反例（含 DF-5 的句子必须绑）；③ 统计 frame 占比，超过阈值报警 |
| **N-10** | Major | §7.2-2、§8.3 vs §7.1/§8.2 | §7.2-2 要求"输出 `count_from_ku`"、§8.3 要求"输出 `coverage_note`"，但 §7.1/§8.2 的 JSON 都没有这两个字段；`findings[].obligations` 是 `["Art.26(2) 指派人工监督"]` 自由文本，无法回放到 KU/locator；`no_rule_matched` 只要求 `missing_fields` 或覆盖声明，与"必须 coverage_note"不一致 | ① 在 §7.1/§8.2 增 `count_from_ku`、`coverage_note`；② `findings[].obligations` 改为 `[{ku_id, locator, text, basis}]`；③ `count_from_ku` 必须等于可复算的 claims 条数，否则 CK/CI 失败 |
| **N-11** | Major | §8.1 vs §8.4/§1.2 G3 | §8.1 `jurisdiction: EU \| CN`，§8.4 却要求 `out_of_scope` 覆盖"SG/US"——profile 无法表达 SG/US，MCP 会先报 `INVALID_INPUT`，G3 的"超范围"用例不可达；`domains`/`use_cases` 是开放列表（`[biometrics, education, employment, ...]`），规则用 `intersects` 比对时无闭合值域，大小写/同义词会漏判 | ① `jurisdiction` 增 `OTHER`（或允许任意字符串，值域外→`out_of_scope`）；② 按域给 `domains`/`use_cases` 闭合枚举与同义词映射；③ 给"SG/US"和 `domains` 拼写差异各 1 个反例 |
| **N-12** | Major | §6.3、§10、`ku-plan.md` | G5 演示改 `kb/ku/gsk-eu-art6-high-risk.yaml`——ku-plan 没有这个 id（只有 `art6-1/2/3`）；演示改 art6 的 `effective_date`，第 4 步却问"高风险系统什么时候开始适用"（日期在 Art.113），改 art6 不会让答案日期变；§7.2-8 又禁止 `ask` 推断适用性；§10 W1 已写 EU 20 KU，W2 又写 EU 32 KU（重复计 20）；W1-0 行多出第 4 个单元格「0.5」，表头只有 3 列；W3 写「v0.1 冻结」（应为 spec v1.0） | ① 演示改 `gsk-eu-art113` 或 `gsk-eu-art6-2` 的 `effective_date`，并让 `ask` 只答"Art.113 原文日期"；② W2 改为"EU 剩余 12 + CN 20"；③ 修 §10 表格列数；④ v0.1→v1.0；⑤ 给 G5 一个可复跑脚本清单（改哪个文件、期望哪 2 页） |
| **N-13** | Major | §6.2、`impact-matrix.md` | `change_id` 只写"commit trailer 或 PR 标签"，未定义二者都有/都没有、一个 PR 多 commit、change 文件不存在时怎么办；错误码只有 `IMPACT_UNREPORTED`/`EVIDENCE_STALE`/`PROBE_BROKEN`，缺 `CHANGE_ID_MISSING`/`CHANGE_ID_UNKNOWN`/`DECLARED_EMPTY`；`depends_on` 未被消费；矩阵不被 CI 读取；矩阵 CH-C5/CH-CK3 用 `…v0.2.md` 与「见 W1」违反自己的"真实路径/产物"规则 | ① 定义"一个 PR 一个 change_id"与缺失/重复错误码；② 删除 `depends_on` 或让 CI 消费它；③ CI 增加"矩阵行必须可解析 + evidence 文件存在"；④ CH-C5/CH-CK3 补真实路径与 evidence 产物，否则改 `pending` |
| **N-14** | Minor | §5.4 树、§4.2.1 `freshness`、两份样例、gap | §5.4 树缺 `kb/profiles/`、`kb/scope_exclusions.yaml`、`changes/`、`evidence/`（C3/§6.2 都引用）；MCP `freshness` 出参 `oldest_as_of` 与 §7.1 `oldest_verified_at` 不同名；样例 `fingerprint` 相同占位；CN gap 写"待从第十九条补"，第十九条不在 52 条；EU gap 写"待从 Annex IV 补"，Annex IV 被 §1.3 排除；W1-0 允许"已知 gap 登记"即可全绿，等于把契约干跑降为自报 | ① 补树；② 统一 `freshness` 字段；③ 样例 fingerprint 由 excerpt 实算，或明确"draft 才允许占位"并由 CK 拒绝占位进 publish；④ gap 的 close 路径必须在收录范围；⑤ W1-0 的通过条件改为"publish 态样例过 CK"，draft 仅作 smoke |

---

## 4. 七项重点实核

### ① locator 7 形态与 52 条是否真闭合（自跑，不引用作者证据）

- 按 §5.2 C4 的 3 条显式正则跑 ku-plan：**52/52 通过**，`ku_id` 唯一，EU 32 / CN 20。这一层比 v0.1 的 15/33 非法是实质进步。
- 但 7 形态里 **②–⑤ 只有名字、没有正则**（"章节式/命名章节式/页码式/条目式"），CK-01 只能实现 ①⑥⑦；说"7 形态闭合"证据不足。
- ⑥ 对 `第四条第（二）项` / `第七条第（二）项` **不匹配**（`第[…]项` 不接受全角括号）；v0.1 F-08 点名的正是这个形态。
- 下游 `excerpt-candidates.md` 仍有 **3 条禁用区间**、**7 个旧 id**（见 N-05）。结论：**计划层闭合，链路层未闭合**；F-01 判"部分"。

### ② 两份样例：29 字段 / 子串 / gap 与 status

- 自跑 PyYAML：两份均为 **29 个顶层字段 + `gap`**（EU gap 5 项、CN gap 4 项），字段数成立。
- `obligation[].text ⊂ verbatim_excerpt`：**6/6 通过**（EU 1/1、CN 5/5），v0.1 的 6/6 失败已真修。
- `gap` 非空且 `status: draft`，CK-04 的"gap 非空→draft"自洽；概念字段 null 均有对应 gap；`evidence_requirement: []` 也登记了 gap。
- 但两份都停在 **draft**，从未在 publish 态跑过；`evidence_requirement`、`frequency`、`scope_type` 三个字段在两份样例里都是空/自由文本，**"29 字段全量填写"验证不到它们**。
- `fingerprint` 两份完全相同（`minhash96:000…001`），格式正则通过但内容未绑定 excerpt；`scope` 仍是自由文本（`high-risk AI systems` / 中文长句），F-13 的闭合表没有落地。

### ③ `claims.support_type=absence` 是否真有依据

- 设计层只有三处提及：§5.2 C3（新增 `kb/scope_exclusions.yaml`）、§7.2-2（条目含 `registry_id`+`as_of`+理由）、§9.2（指标接受 `scope_exclusion`）。
- **没有**：文件路径入 §5.4 树、条目 schema、CK 编号/错误码、样例、claim 字段（§7.1 的 claim 只有 `ku_ids`）。结论：**没有可执行依据**；`absence` 目前是"任意否定句的免绑后门"，不是证据类型。这也是 #9/#17 必然无法被判"通过"的原因之一。

### ④ `applies_later` 与 Art.113 日期

- §1.4 与附录 B/E 说 2027-12-02（Annex III）/ 2028-08-02（Annex I），`source-map.md` 的时间表也支持这对日期；§8.2 示例用 2027-12-02，逻辑上自洽（as_of 2026-10-31 < 2027-12-02 → `currently_in_force=false`）。
- 但**数据模型不自洽**：每 KU 只有一个 `effective_date`，而 Art.8–15 同时适用于 Annex I 与 Annex III，两个适用日无法落在同一 KU；`applies_from` 没有 `basis_ku`，无法说明"这个日期来自哪条 KU"。
- **摘录不自洽**：`eu-article-map.md` Art.113「段落数：0」（正文未抓），`excerpt-candidates.md` 的 Art.113 摘录是「It shall apply from 2 August 2026」，没有 2027-12-02/2028-08-02。按现候选摘录入库，金标 #7 的日期无法由 `verbatim_excerpt` 支撑；若按合并版重抄，必须替换候选并标注版本差异。**需作者核实合并版 Art.113 原文**。

### ⑤ impact CI 的 change_id→图计算消费集是否闭合、能否被绕过

- **能被绕过**，且是最短路径：`actual_changed ⊆ changed_files ∪ consumers` 只检查"改的东西在允许集内"，不检查"consumers 是否都改了"。改规则文件、`ku_ids` 正常声明 → consumers 算出一堆页面/金标，但它们**没改**也 PASS。
- `ku_ids` 仍是 `changes/<id>.yaml` 里的手写字段；声明 `ku_ids: []` → consumers 为空，仍然 PASS（规则文件在 `changed_files` 中）。
- 反向探针只测"漏申报一个新文件"，不测"声明了消费者但没更新"；`depends_on` 未被消费；矩阵文件不被 CI 读取，且矩阵自己第 25 行写「未改即 FAIL」，与 §6.2 的谓词矛盾。
- 结论：**F-07 未修**；这不是"实现没做"，是"判据写反"。

### ⑥ 52 KU / 20 金标 / 负例 / 双域全文一致性（grep + 自算）

| 数字 | 出现位置 | 结果 |
|---|---|---|
| 52 / EU 32 + CN 20 | §0、§3.1、附录 B/E、ku-plan | 标题层一致 |
| 50 | §1.3「不在 50 KU 内」、R2「50 KU」、approval | **不一致** |
| 附录 B 分项和 | `1+5+3+4+8+1+3+1+3+1` | **30**，却标 32 |
| Art.5 项数 | §3.1/附录 B「5 项」；ku-plan 7 项 | **不一致** |
| 附录 D | 「30±3 / 14–16 / 6–8」 | **不一致** |
| 候选表 | EU 33 + CN 20 = 53 | **不一致** |
| 独立负例 | 全文 5；未出现 20 | **若口径要求 20，则缺 15 题且无落点** |
| 金标拒答 | 严格 `refuse` 3 题；"refuse/纠正"2 题 | 「5/5」不可由脚本复算 |

结论：**52/20 只在摘要层一致，分项层与旧文档仍漂移**；F-16 判"部分"。

### ⑦ CK-03 状态机是否允许"manual 无证据"或"offline 发布"绕过

- **manual 无证据**：状态机写 pending→manual 需提交 `verified_by` + `evidence_ref`，错误码 `EVIDENCE_MISSING`；但发布门禁只要求 `verification ∈ {online, manual}` 且未过期，**没有** `evidence_ref`/`verified_by` 非空校验。直接手写 `verification: manual`、`verified_by: "R-2 / 张三"`、不填 `evidence_ref` → 发布门禁通过。
- **offline 发布**：offline 不在 snapshot 头的枚举注释里（`# pending | online | manual | expired`），也没有任何→offline 转移；它只在"只允许 draft"这一句里出现。若实现按枚举拒绝 offline，则 draft 无法标 offline；若实现接受 offline，则"不得发布"只靠发布门禁的 `{online,manual}` 排除——而手填 `manual` 即可绕过（上一条）。
- **online 伪装**：`verification` 是自由 YAML 字段，手填 `online` 不需要 `verify-source` 产物；没有 `evidence_ref` 与 `page_digest` 的绑定校验，脚本核验与人工自报在机器上仍不可区分。
- **过期不自动**：`expired` 只由 `grc freshness` 或 CI 触发；发布门禁写"未过期"但未规定按 `verified_at + max_age` 与运行日重算。结论：**CK-03 仍可自说自话**，F-04 判"部分"，且是 Block 级开口。

---

## 5. 十个必答问题（只答 v0.2 变化相关部分）

| Q | v0.2 增量回答 |
|---|---|
| **Q1 最大单点风险** | 仍是**工程侧单人带宽**，v0.2 又加了 W1-0（0.5 人日）、7 形态与 claim/prose 实现，重估从 27–32 人日升至 **28–33**；W1 仍 7.7+0.5 vs 7.5 可用，W2 仍 10.5–13 vs 7.5。最可能爆点仍是 W2；§10 W2 还重复计了 EU 32（应为剩余 12），说明排期表本身没对账 |
| **Q2 C1 可审计** | 状态机 + `verification_url`/`page_digest`/`evidence_ref` 方向正确，但"manual 无证据可发布、offline 可伪装 manual"使可审计仍不成立；最小修法见 C2。上轮 Q2 的结论"可发现、可重放"只有 `page_digest` 一半落地 |
| **Q3 determine 法务风险** | `no_rule_matched` 改名、`listed_obligations_from_source`、`basis_verbatim` 是进步；但 `findings[].obligations` 仍是自由文本"义务清单"，等于把上轮 Q3 批评的"整改清单"换个字段又给出来；`applies_from` 不可回放，风险未降 |
| **Q4 绑定在哪些题型失败** | 译文/归纳/否定/跨域四类有了名义出口；但 frame 只排 DF-1/2/4/6，**义务动词句可免绑**（N-09）；prose 与 translations 不受 binder 约束（N-01）。降级路径仍不可接受 |
| **Q5 中文 BM25** | 上轮结论不变（bigram 方案已给，不算 Block）；v0.2 增 `retrieval_expect` + top5≥18 是进步，但 alias 覆盖门槛缺失、W1-4 仍是 5 query top-3；不达标时仍无"加 50 条别名表"的预算 |
| **Q6 影响面 CI** | 上轮"能拦新增文件、拦不住改规则不改样例"的结论**仍然成立**；v0.2 只把"全表并集"换成"单 change 并集"，谓词方向未变。新例子：改 `rules/applicability-eu.yaml`、`ku_ids` 声明 art6-3，页面/金标不改 → PASS（§1.1） |
| **Q7 哪些金标必然挂** | v0.2 下仍必然挂：#1（Art.43 被排除）、#3（5 vs 7）、#14（ask 无 profile）；#7 取决于合并版 Art.113 原文能否逐字入库（需核实）；#9/#17 因 `absence` 无证据、`expected_mode` 写成 `refuse/纠正`，仍不可判 |
| **Q8 N-11 最小修法** | v0.2 正文仍没有 N-11 的修法（只有附录 C 一行"修入 CK-11/CK-09"、R6 一句"2 子项 + 2 错误码 + 1 反例"）；最小修法不变：CK-11 增 `log.md subject` 可解析（`DANGLING_REF`），CK-09 增 `{{log.*}}` 占位符白名单与逐字比对（`WHITELIST_VALUE_MISMATCH`），各配 1 反例 |
| **Q9 砍/加** | v0.2 不采纳"砍 determine"，改为确定三态+清单，方向可接受；但新增的 `applies_from` 日期模型是新的高风险点。若必须再加一件：**加"publish 态契约干跑 + CI 反向探针（规则改了/金标没改必须 FAIL）"**，而不是再加字段 |
| **Q10 总裁定** | **B 有条件通过**；条件见 §6。若 C1/C2 被反驳且无替代判据 → **C** |

---

## 6. 条件清单（B 的前提）

| # | 对应发现 | 修法（必须可执行） | 为什么必须在 W1 前 |
|---|---|---|---|
| **C1** | F-07 | 把 CI 判据改为**双向**：`actual_changed ⊆ declared ∪ consumers` **且** `required_updates(change) ⊆ actual_changed`（`required_updates` 由 `ku_ids` 经图计算得到）；`ku_ids` 从变更的规则文件/`changed_files` 解析，不接受手写空值；反向探针改为"只改规则、不改金标"必须 FAIL；补 `CHANGE_ID_MISSING/UNKNOWN` 错误码 | 这是 G-1 唯一承诺的机器拦截；W1-10 才写脚本，方向错了 W3 再改等于没有拦截 |
| **C2** | F-04 | CK-03 增校验：`manual` 必须同时有 `verified_by`+`verified_at`+`evidence_ref`+`page_digest`；发布门禁按 `verified_at + max_age_days` 与运行日重算过期，不依赖是否跑过 `freshness`；`offline` 要么删掉、要么补"→offline"转移并禁止 publish；`verification` 只允许脚本/人审命令写，禁止手填 | 快照文件格式 W1-7 一次写 32–52 份，之后改要 ×N |
| **C3** | N-03/F-20/N-04 | 冻结金标前三题重写：#1 与 Art.43 二选一；#3 改 7 项；#14 增 `ask.profile` 或移入 determine 用例；#7 先核实合并版 Art.113 原文，给 Annex I/III 两个日期各自的 KU/规则；`expected_mode` 全部单值 | 20 金标 W1 冻结；带着三条不可过的题冻结，G2 "100%" 永远不成立 |
| **C4** | N-01/N-02/N-09 | ① `answer` 增句→claim 映射（或 `sentence_map`）；② `translations[].claim_ids` 必填并纳入 binder；③ `scope_exclusions.yaml` 定义 schema、入树、加 CK-14、claim 增 `scope_exclusion_id`；④ frame 排除 DF-1~6 全部形态并配反例 | 这是"无据必拒"的最后一道门；W1-5 写 binder 时就要按它实现 |
| **C5** | N-05/N-06/N-07/N-08 | 以 ku-plan 为唯一源重生成 `excerpt-candidates.md`；registry 与 snapshot 定单一真值；所有计数由 `gen_numbers.py` 生成（52/32/20/7/5/13）；"三态"全部改"五态"；G3 验收加入 applies_later/no_rule_matched | 这些是 W1 抄录、W1-0 干跑与 eval 的输入；拖到 W2 会"改一处返工三处" |
| **C6** | N-12/N-13/N-14 | 修 §6.3 演示（改 `gsk-eu-art113`/`art6-2`，不存在的 KU 名删除）；§10 W2 改"EU 剩余 12"、修表列、v1.0；补 §5.4 树（`profiles/`、`scope_exclusions.yaml`、`changes/`、`evidence/`）；矩阵 CH-C5/CH-CK3 补真实路径与 evidence 或改 `pending` | G5 演示是 W3 的验收动作；演示脚本引用不存在的文件，验收当天必翻车 |

**裁定**：**B（有条件通过）**。C1–C3 是硬条件（不满足则 G1/G2/G3 不能验收）；C4–C6 是"结论可信"的前提。**一票否决：无**。若作者反驳 C1 或 C2 且不提供替代判据 → **C 不通过**。

---

## 7. 我认为 v0.2 做对的 3 件事

1. **locator 计划是真重写，不是文字游戏**：52/52 单 locator、`ku_id` 唯一、EU 32 + CN 20 对得上，v0.1 的 15/33 非法被实际消除；`Art.5(1)(ba)`、`Annex III point 1` 都能进域。问题只在"7 形态只实现了 3 条"和下游候选表没跟上。
2. **claim + prose 双轨与 `support_type` 五值是正确的分解**：把"事实/归纳/否定/跨域/译文"分开，比 v0.1 的单轨现实得多；#19 的 `groups` + `cross_jurisdiction` 也终于能表达。问题在执行层（prose/translations/absence 未闭合），不在方向。
3. **CK-03 的证据字段与影响面 CI 的工装意识是对的**：`verification_url`/`page_digest`/`evidence_ref`、`--now` 探针、`change_id` + 反向探针，都是 rev4 五轮里缺的"运行体"思维。即便 F-07 判据写反、F-04 门禁不严，这套骨架只要把方向修正，是能承接 G1/G5 的。

---

## 8. 复跑证据、局限与声明

**复跑（本轮实际执行，非引用作者证据）**：

```
python3 - <<'PY'
# 1) ku-plan 52 行，按 C4 的 ①⑥⑦ 三条正则：52/52 PASS，ku_id 唯一，EU 32/CN 20
# 2) CN 形态：第七条 PASS；第七条第二款 PASS；第四条第（二）项 FAIL；第十七条第一款 PASS
# 3) EU 旧非法值：Art.26(1)-(2)/Art.50(3)-(4)/Annex III 1–4 均 FAIL（说明禁止区间有效）
# 4) 样例：两份 29 字段 + gap(5/4)；obligation 6/6 是 verbatim_excerpt 子串；
#    fingerprint 均为 minhash96:000...001，[0-9a-f]{96} 通过；evidence_requirement 均为 []
# 5) excerpt-candidates：53 行（EU 33/CN 20）；3 条 locator 非法；7 个旧 id 不在 ku-plan；
#    6 个 ku-plan id 无候选
# 6) 附录 B 分项和 = 30，却标 32；ku-plan Art.5 = 7 项；§3.1/附录 B 写 5 项
PY
```

- **证据门槛**：每条 Block/N 级发现都有位置 + 判据/反例 + 修法；未写"应该可行"的 PASS。F-10/F-19/F-23/F-30 等设计层已修项，残留只记 Minor。
- **局限**：① 未核法条实体内容；Art.113 合并版日期、Annex I/III 的适用关系标「需作者核实」；② 未运行任何实现（本轮无代码）；③ 未采用 `spec-self-review.md` 的定级，仅用 v0.2 头部"9 处"与 v0.1 自检"11 处"做数字对账；④ 08 报告仅用于 G-1~G-5/P-1~P-5 的对照，未作为定级依据。
- **只改一个文件**：本报告为唯一新增文件，未修改设计、处置表、样例、矩阵或证据文件。
