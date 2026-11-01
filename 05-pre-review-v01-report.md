预演评审（非 CCC 正式报告）｜对象：设计 v0.1｜轮次：0

# GRC Skill Agent 设计 v0.1 · CCC 预演评审报告

> 评审人：独立设计评审（非实现者）｜日期：2026-10-31｜性质：dry-run，不代表 CCC 正式结论
> 依据（按 brief 顺序）：`CCC-review-brief.md`、设计 v0.1、`contract-digest.md`、`source-map.md`、`ku-plan.md`、两份样例 KU、`rev4-ku-schema.md`/`rev4-wiki-schema.md`（按需）、`08` 报告（仅 D8 对照）、`docs/impact-matrix.md` 与 `docs/plans/w1-plan.md`（设计 §6.2 与 §10 引用，属被评范围）。
> 边界：不评法条内容、不写实现、不改任何被评文件。凡依赖法条原文的判断，一律标「需作者核实」。附录 A 为本次实核的可复跑证据；§0/§1/§2 先独立完成，未采用作者自评定级（`spec-self-review.md` 在包内，仅用于核对数字口径）。

---

## 0. 总裁定

**B 有条件通过**

命中一票否决：**无**。7 个 Block 全部是契约层缺口（字段域、绑定语义、判定语义、CI 判据），改法在 1–2 人日内可落到 v0.2，不需要动架构；但若作者反驳 F-01（locator 域）或 F-07（impact CI）而不给替代判据，本裁定应降为 **C 不通过**。

- Block 7｜Major 18｜Minor 9｜Pending 1（无判据项不计 PASS，见 §1 末）
- 判断依据一句话：方向对、机制骨架对，但**「契约可执行」目前是文档声明而非实测事实**——两份样例在继承契约下即有硬失败（CK-04 两份、逐字性 6/6、指纹占位），计划中的 33 条 EU KU 有 15 条 locator 非法，影响面 CI 的判据在逻辑上拦不住 G-1。
- 结论适用条件：§3 的 7 条条件须在 **W1 第 0 天（契约导入前）** 落进 v0.2；其中 C1–C3 是验收能否成立的前置，C4–C7 是"结论是否可信"的前置。
- 对"3 周"的独立判断：**排期重估 27–32 人日 vs 22.5 可用（120–142%），最可能爆在 W2**（详见 Q1），但可以通过"砍 determine"（Q9）在不动 G1/G2/G4/G5 的前提下救回来。

---

## 1. 逐条发现

| # | 维度 | 位置 | 判定 | 问题 | 依据/反例 | 修法 |
|---|---|---|---|---|---|---|
| F-01 | D3 | §5.2 C4 + `ku-plan.md` EU 表 | **Block** | C4 只补了"中国条款式"，但继承的 `locator` 5 形态对 **EU 字母项、附件、区间** 同样不闭合；C4 的前提"5 形态是欧盟中心"只对数字段成立 | 实测：33 条 EU 计划中 **15 条** locator 违反 rev4 §3.1 正则——`Art.5(1)(a)-(b)`、`Art.5(1)(ba)`、`Art.5(1)(f)`、`Art.26(1)-(2)`、`Art.26(3)-(6)`、`Art.50(3)-(4)`、`Annex III 1–4`、`Annex III 5–8` 等；CK-01 会在 W1 第一天全部判 `SCHEMA_VIOLATION`，而这些 KU 正是金标 #1/#2/#3/#5/#7 的唯一来源（附录 A-3） | 条款式扩为允许字母项与可选区间：`^Art\.\d+((\(\d+\))\|(\([a-z]{1,3}\)))*$`；新增**附件式** `^Annex [IVX]+( item \d+)?$`；区间式禁止，按段/项切 KU（与 1200 字符上限一致） |
| F-02 | D4 | §3.3 C2 × §7.2-1 × §7.3 | **Block** | C2 要求"用户语言作答"，binder 要求"每条 claim 的 span 是 KU 字段的**连续子串**"，两者对跨语言问答互斥 | 中文问"高风险系统提供者投放前有哪些义务"：答案句是中文，绝不可能出现在英文 `verbatim_excerpt`/`obligation.text` 中 → 要么全删句（答案不成立→拒答），要么放弃 C2；`--no-llm` 抽取式更不可能翻译。金标 #19 必挂 | 给 claim 增 `binding_mode: quote\|translation\|frame`：quote 校验子串；translation 校验 `verbatim` 是 KU 字段子串、译文单列并标注 `machine`；frame 走 DF 扫描（见 F-03）。同步改 §7.2-1 措辞为"每条**事实性** claim" |
| F-03 | D4 | §7.2-1、§7.3、§7.1 refusal | **Block** | "每条 claim 绑定 KU"对四类句子没有出路，而设计写的降级路径（删句→拒答）会**过保守**：该答的题变成"不知道" | ① 归纳/计数句"提供者共 12 项义务"无单一 span；② 否定/缺失句"ISO 42001 不是法定要求"（金标 #9、#17）在库内没有任何 KU 可绑；③ 跨域对比句（#19）；④ 时间推断句"你从 2027-12-02 起适用"（#7）。refusal 枚举也没有"范畴纠正"出口，`scope_correction` 缺失 | 引入三类句：事实句（必绑）、框架句（不含 DF-1/2/4/6 形态（日期/条款定位/义务动词/数字期限），免绑，用现有 DF 扫描器判定）、否定句（绑 registry 的 `scope_exclusion` 条目而非 KU）；refusal 增 `scope_correction` |
| F-04 | D3 | §5.3 CK-03 四态 | **Block** | 四态没有状态机，且 manual 要求的"截图或页面 hash"**没有字段可放**（§5.3 的元数据清单是闭合的 6 项）；offline 与 manual 在机器上只差一个自报标签 | 谁能设 offline？expired→manual 由谁触发？一次核验覆盖整部法（registry 示例 `snapshots/eu-ai-act.md`）还是每篇（样例 `#p1`）？两个问题都没答案 → "可审计"退化为"自说自话"（Q2） | 补状态机四元组（状态 × 触发 × 执行者 × 错误码）；snapshot 头增 `evidence_ref`（截图/页面 hash 路径）与 `page_digest`（对可抓的官方页面全文取 sha256，不存正文）；见 C4 |
| F-05 | D5 | §8.2 verdict 枚举 | **Block** | 判定枚举缺"**适用但尚未生效 / 部分适用**"，在 EU 的时间维度上必然给出错误结论 | 画像 `placing_on_market: 2026-12-01`、Annex III 系统：义务 2027-12-02 才适用。`applies` 错（现在还没义务）、`does_not_apply` 更错（将来有）、`insufficient_info` 是撒谎（信息齐全）。设计 §6.3 的演示正落在这个窗口（附录 A-9） | 输出增 `applies_from: <date>` 与 `verdict: applies_later`（或 `applies + currently_in_force: false`）；determine 用例必须含 1 个"跨生效日"正例 |
| F-06 | D5 | §8.3 运算符 | **Block** | 运算符集 `eq/neq/in/not_in/lt/gte/exists` 无法表达关键适用条件；且 `in/not_in` 对 **list 字段的语义未定义**（字段∈列表，还是列表⊂字段） | 例 1：EU Art.6(3) 例外要求"未实质性影响决策结果"的**定性判断**，画像无此字段，`exists` 只会把判断挪给用户却不留痕；例 2：CN 暂行办法 Art.17「具有舆论属性或社会动员能力」由**被 §1.3 排除**的《算法推荐规定》定义，值域不闭合；例 3：`domains ∩ Annex III ≠ ∅` 无法表达，`in` 的两种读法会给出相反结论（附录 A-9） | ① 增 `judgement_required` 槽（用户自答 true/false/unknown，unknown→insufficient，并在 findings 留痕）；② 明确 `in`=标量属于列表，新增 `intersects`/`contains_all`；③ Art.17 增 `opinion_attribute` 三值槽并由用户填；见 C6 |
| F-07 | D6 | §6.2 + `docs/impact-matrix.md` | **Block** | CI 判据是"本次变更集 ⊆ **全表所有 done 行的并集**"，不是"本变更自己声明的消费集"；申报集随每行单调增长，最终≈全仓库，鉴别力趋 0 | **拦得住**：改动一个从未在任何行出现过的文件（如新增 `kb/ku/gsk-cn-genai-art12.yaml`）→ 不在 declared → `IMPACT_UNREPORTED`。**拦不住**：只改 `rules/applicability-eu.yaml` 的 Art.6(3) 例外列表，不碰 `eval/determination.yaml` 与 `gsk-eu-art6-3.yaml`——规则文件早在某行 `changed_files` 里 → PASS。这正是 G-1 的复现（附录 A-7） | 每次变更绑定唯一 `change_id`（commit trailer 或 `changes/<id>.yaml`），`declared` 只取该行；消费集改为从 `ku_ids`/`depends_on` **图计算出**的受影响集，不靠申报；`evidence` 必须是可复跑产物（命令 + 退出码 + 输出文件），并给 CI 自己加一个"故意漏申报必须 FAIL"的反向探针；见 C7 |
| F-08 | D3 | §5.2 C4 + §7.1 citations | Major | 第 6 形态不能表达**款/项**，而设计把款/项推给 `snapshot_ref` 锚点；锚点又不进答案 | 实测 `第七条第二款`、`第四条第（二）项`、`第十七条第一款` 均不匹配；CN 样例 5 条义务同属第七条不同项，`citations[].locator` 只能全写"第七条"，用户与审计都无法定位到"（三）个人信息同意" | 第 6 形态扩为 `第X条(第X款)?(第X项)?`；`citations` 增 `anchor` 字段；已有 `snapshot_ref` 锚点保持兼容 |
| F-09 | D3 | §5.4 registry 示例 + §5.3 + §9.2 | Major | 核验元数据的**粒度矛盾**：registry 用整部法一个 snapshot + 一个 `excerpt_hash`，样例用每篇一 snapshot；§9.2 的"100% KU 有 verification"在字段层面不可计算 | 一个 `excerpt_hash` 覆盖不了 33 条摘录；`verification`/`verified_by` 存在 snapshot/registry，不在 KU 上，而指标按 KU 统计 → 指标与数据结构不对齐 | 规定 snapshot 粒度 = KU（或 snapshot 内每条摘录一个 hash 条目）；`freshness` 按 KU 聚合出 `verification`；§9.2 指标改写为"每 KU 可解析到 (snapshot, excerpt, verification)" |
| F-10 | D3/D9 | §5.3 online + `source-map.md` §6 | Major | EU 的 `source_url` 是 EUR-Lex（实测 curl 0 字节），人工实际在 EC Service Desk 核对；**登记的 URL 与被核验的 URL 不是同一个** | online 对 EU **0/33**（占 KU 62%）；CK-03 的"逐字命中"没有可抓的落点；人工核的是 Service Desk 页（`eu-article-map.md` 全部来自它），答案里给的却是 EUR-Lex 链接，且 Service Desk 文本带 "AMENDED" 编辑标记，逐字抄录会把编辑标记当法条文本 | registry 增 `verification_url`（Service Desk 条文页）与 `source_url` 分离；online/manual 一律针对 `verification_url`；`page_digest` 也取它——这一条同时是 R1 的可行缓解 |
| F-11 | D3 | 两份样例 + rev4 §5 | Major | 设计称"两份样例 29 字段全量填写"——**字段数成立，契约校验不成立** | 实测：EU 样例 `definition/scope_in/scope_out/common_misreadings` 全 null、CN 样例 3 个 null，且 `gap: []`；rev4 §5 明写"gap 为空但条件必填字段为 null → `CK-04 FAIL(INSUFFICIENT_INPUT)`"（附录 A-4）。设计未定义 CK-04 与"被 concept 页引用"条件的先后 | 二选一：CK-04 明确"概念四字段仅在被 concept 页引用时校验"，或两份样例补 4/3 条 gap；并把"两份样例必须过 validate"写成 W1 门禁 |
| F-12 | D3 | 样例 `obligation`/`evidence_requirement`/`fingerprint` | Major | 事实字段不是逐字：义务文本被改写；证据文本引自**未入库的另一条**；`fingerprint` 是占位符 | 实测 6/6 条 obligation 都不是 `verbatim_excerpt` 的子串（EU ob-1 把 "in such a way…that" 改成 "…so that"；CN ob-5 把《中华人民共和国网络安全法》简称化）；CN 样例 `evidence_requirement[0].text` 实际来自暂行办法**第十九条**（监督检查配合），而 19 条不在 53 条计划内、excerpt 也不含该句；两份样例 `fingerprint: minhash96:pending-w1`（附录 A-2） | CK-03 增子项：`obligation[].text`/`evidence_requirement[].text` 必须是 `verbatim_excerpt` 的连续子串，或有显式 `paraphrase: true` 且**禁止进 citation**；`fingerprint` 加格式校验（`minhash96:[0-9a-f]{96}`） |
| F-13 | D8 | §5.1 P-3 + 样例 | Major | P-3（规则四要素/闭合值域）只在文档层落地：四个事实子字段值域开放，样例已出现两种写法 | `obligation.modality`（obligation/prohibition）、`applies_to.subject`（provider/deployer…）、`evidence_requirement.frequency`（`per_placing_on_market` vs `on_request`）、`applies_to.scope`（英文短语 vs 中文句子）均无枚举表 → CK-01 无法判定（附录 A-2） | 在 schema 补 4 张闭合表（含 `SCHEMA_VIOLATION` 错误码）并给每个值一句判据；`scope` 拆成 `scope_type`（枚举）+ `scope_note`（自由文本） |
| F-14 | D5 | §8.2 determine 输出 | Major | determine 输出没有 `as_of`/`verification`/`verified_by`/freshness，`citations` 还是字符串数组 `["..."]`；§7.2-6 的元信息要求只约束 ask | 判定结果无法审计时效，也无法回放到原文；与 G2/G5 的"可审计"口径不一致 | 复用 §7.1 的 `citations[]` 结构与 `freshness`，determine 输出增 `as_of`、`verification`、`verified_by` |
| F-15 | D5 | §8.3 exceptions/priority | Major | `exceptions` 与 `priority` 只有字段名没有求值语义；"规则冲突 → `insufficient_info`"与"例外命中"是两件事，被混为一谈 | 两条同 priority 规则同时命中但结论相同 → 按设计要拒答（过保守）；不同 priority 谁赢未写；例外命中是"规则不适用"还是"结论相反"未写 | 固定求值顺序：exceptions 先行（命中即该规则不适用）→ priority 高者胜 → 同 priority 且结论不同才 `insufficient_info`；`--explain` 输出固定三列（规则 id / 命中项 / 结论） |
| F-16 | D1 | §0/§3.1 vs 附录 E/`ku-plan`/§10 | Major | 范围数字不自洽：文中"约 50"，附录 E 与 ku-plan 是 **53**；ku-plan 标题写"EU（32）"而表内 33 行；§10 弹性方案"金标 15 题"直接击穿 G2 的"20 金标 100%" | 若弹性触发，`G2` 验收条件不成立，却被写成"仍在范围声明内"；+6% 的 KU 增量没有对应的人日调整（附录 A-6） | 统一为 **53 KU / 20 金标**；弹性方案改成"减 KU 不减题"，或把 G2 改写成"金标 ≥15 且全绿"并同步 §1.2 |
| F-17 | D7 | §9.1 vs 附录 A | Major | 金标分类表与题目对不上：写"拒答 3、跨条 2"，附录里拒答/纠正型有 **5** 题（#4/#9/#10/#17/#20），跨条只有 #19 | CI 门禁的分母不确定，`grc eval` 无法给出确定的通过/失败；"20 题冻结"冻结的是一张与分类表不符的表 | 分类表由脚本从 `golden.yaml` 统计生成（P-1）；按实测重算 6/5/4/2/3 或补一题跨条；"5 个负例"与"金标内拒答"明确区分为两套集合 |
| F-18 | D7 | §9.2 指标 | Major | 三个指标存在自欺面：citation 稳定性未定义比较单位；`unsupported_claims` 由 binder 自报（binder 即被测物）；"无据断言 0"在 `--no-llm` 下恒为 0 | 同题两次"结果一致"到底比措辞还是比 `(ku_id, locator, verbatim)` 集合？若比措辞，与 LLM 天然冲突；若比集合，则与"无据断言"重复。binder 自己判自己 = G-3 仪器污染的翻版 | 稳定性只比 claims 的三元组集合；`unsupported` 由独立脚本重算（不在 `answer.py` 内）；CI 分 `--llm` / `--no-llm` 两套记录，指标不得合并 |
| F-19 | D9 | §11 R1 + §5.3 | Major | R1 的缓解不成立：CI 周检的成本未进排期；`expired` 在 3 周内**不可触发**（默认 90 天，且无时钟注入） | 周检 53 KU × 双人 × 15 分钟 ≈ 26.5 人时/周 ≈ 3.3 人日/周（约 1/3 FTE），§10 未计入；`max_age_days=90`，2026-10-31 核验的 KU 到 2027-01-29 才过期，MVP 窗口内永不走 expired 分支 → 第四态无探针 | MVP 只承诺"发布前核验"，把"周检"移出 3 周承诺并在 §11 明示"不承担改版监测"；`freshness` 增 `--now` 注入用于 expired 探针 |
| F-20 | D4 | §4.2.1 ask 入参 × §8.4 × 附录 A #14 | Major | 适用性问题在 `ask` 通道没有画像入口，而 §8.4 又禁止 skill 未调 `determine` 自行判定；同一演示问句在两处期望不同 | `ask` 入参只有 `{query, language?, jurisdiction?, no_llm?}`；§2.3 演示 Q4 期望"信息不足/需按画像细分"，附录 A #14 期望"insufficient **或按 Art.2 回答**"——同一题两个判据，金标无法判定 | `ask` 增可选 `profile`；或 SKILL.md 写死"适用性问题必须先 `determine`，`ask` 只取原文"；#14 的期望 mode 与 `ku_ids` 写唯一值 |
| F-21 | D2 | §4.2 索引 + W1-4 | Major | 中文检索的分词方案**已经给了**（CJK bigram，不算 Block），但检索质量没有判据：W1-4 只用 5 个已知 query 的 top-3，20 金标的措辞差异未纳入验收 | "备案" vs "算法备案"、"训练数据" vs "预训练、优化训练"：bigram 召回的稳定性无判据；`catalog.aliases` 由作者手写且无覆盖门槛 → 金标失败时无法区分"检索没召回"还是"答案绑不上" | 每题登记 `retrieval_expect: [ku_ids]`，`grc eval` 先判召回（top5 覆盖 ≥18/20）再判答案；aliases 由金标反推，加"每题至少 1 个别名"门槛；不足再加 50 条人工别名表（0.5 人日） |
| F-22 | D6 | `docs/impact-matrix.md` 现有两行 | Major | 现有两行示例都不满足矩阵自己的规则：N-11 行的 consumers 指向本仓库**不存在**的 `templates/source.md`、`00-MVP定义.md`，evidence 写"见 W1"（规则 4 明说不接受） | 实测两路径均不存在；C4 行的 evidence 是一句 `python3 -c "…" → 2/2 PASS`，没有可复跑产物 → 矩阵当前 **0 条有效证据**，P-2 仍是口号 | 删示例行或改成本仓库真实路径；`status=pending` 不计入 declared；evidence 必须指向 `evidence/` 下的文件 |
| F-23 | D3 | §7.1 citations 结构 | Major | 输出对象自相矛盾：`citations[]` 没有 `verbatim`，也没有 `verified_by`，但 §7.1 末句（"`citations[].verbatim` 永不翻译"）与 §7.2-6（"`verified_by` manual 时必填"）都要求它们 | 按给出的 JSON 实现，C2 的"原文逐字"和 §7.2-6 的元信息**无处落**；`refusal` 在 `mode=answer` 时也无 null 约定 | `citations[]` 增 `verbatim`、`verified_by`、`anchor`；`refusal` 声明为 `answer` 时省略 |
| F-24 | D2 | §4.1 图 / §4.2 边界表 / §5.4 目录 | Minor | `binder` 在 §7.3 是独立组件、在 `w1-plan` 是独立文件，但 §4.2 组件边界表里没有它（隐含在 answer 内） | 组件契约与目录/计划不一致，`binder` 的测试归属不明 | §4.2 增 `grc_core.binder` 行，或在答案契约里注明它是 answer 的内部模块 |
| F-25 | D3 | 两份样例 `ku_id` | Minor | 未申报的命名变更：rev4 规定 `ku-<jurisdiction>-<source>-<locator-slug>`（如 `ku-eu-ai-act-art14`），设计改用 `gsk-`，附录 C 差异表未列 | 与 §5.1"原样继承"冲突；将来与 rev4 合并会撞命名域 | 附录 C 增一行"ku_id 前缀 `gsk-`（本仓库命名域）"，或改回 `ku-` |
| F-26 | D3 | 样例 `title` 与 `source_id`/`registry_id` | Minor | EU 样例 `title` 是拼接串"Regulation (EU) 2024/1689 — Article 14(1) human oversight"，不是原文标题，违反 #18"原文标题，不改写"；`source_id` 与 `registry_id` 恒同值，契约未定义差异 | CK-09 要求 H1 = `title` → 编辑加工会被渲染进页面事实层 | `title` 取原文标题（"Article 14 — Human oversight"），文件级名称走 source 页；合并 `source_id`/`registry_id` 或写明差异 |
| F-27 | D3 | §1 小节顺序 + 文件头自述 | Minor | 小节顺序是 1.1 → **1.4** → 1.2 → 1.3；文件头写"9 处内部不一致已修"，而自检记录是 11 处 | 自检清单里"小节编号连续 0–13"的勾选不成立（P-1/G-4 的典型元信息漂移） | 调整 1.4 到 1.3 之后；"9"改为脚本生成的计数 |
| F-28 | D7 | §9.2 "refs 对账 19→50 边" | Minor | 硬编码的 19 是 rev4 seed 的遗留数字（rev4 wiki-schema §7.1"本包期望 19 条边"），与 8–10 页 × 53 KU 的规模无推导关系 | 违反设计自己承诺的 P-1"计数由脚本生成"，也给 W1-3 留了一个错判据 | 改为"refs 互转置 + 边数 = 运行时统计值"；如需基线，由 `gen_numbers.py` 生成 |
| F-29 | D8 | §11 R6 / §13.5 vs `w1-plan` W1-1a | Minor | N-11 的顺序三处不一致：设计"先修 N-11 再 scaffold"、w1-plan 先 W1-1 scaffold 再 W1-1a、approval-checklist"W1 第一件事 = 修 N-11"；修法只有"修入 CK-11/CK-09"，无错误码、无探针 | 0.1 人日的事，但"第一件事"会变成一句空话；N-11 是 rev4 唯一遗留 Block，判据必须可执行（见 Q8） | 明确 N-11 = 2 条可执行子项 + 2 个错误码 + 1 个反例夹具，落在 W1-1a，并把设计 §13.5 改成"先导入契约，再 W1-1a 修 N-11" |
| F-30 | D9 | §4.3 跨平台表 vs G4 | Minor | §4.3 列了三类宿主（含 Codex），G4 只验两家，Codex 只有"抽验"没有判据 | 承诺与验收不一致；演示翻车风险主要在未定义的那一列 | 承诺表删 Codex 列或标"未验证（v0.2）"；G4 明确只验 DSH + Claude Code |
| F-31 | — | 评审包本身（brief §1 / `README-评审包说明.md`） | Minor | 文件清单与实际不符：README 列的 `01/02/03` 与 brief 列的 `05/06/07` 文件名都不存在（实际是 `docs/specs`、`docs/research` 下的命名）；brief 声称"包内不含作者自评"，但 `spec-self-review.md` 在包内 | 外部 CCC 按清单找文件会缺附件，D1/D3/D8 结论会被动降级；自评在包内会削弱反锚定 | 统一一份 `MANIFEST.md`（真实路径 + 用途 + 必读/按需）；自评文件移出评审包 |
| F-32 | D4 | §7.2-3 + 附录 A #19 | **Major** | `partial` 被两处定义且相互冲突：§7.2-3 只表示"冲突未消解"，而 #19 期望 `partial`（本题无冲突，只是两域分列） | 按 §7.2-3 实现，`grc eval` 永远无法产出 #19 的期望 mode；若为 #19 放宽 partial，则"冲突"与"跨域分列"两种语义混在一个枚举值里，审计无法区分"没答案"与"答案分成两段" | 给 `partial` 加第二个触发条件并在 §7.1 增 `partial_reason: conflict\|cross_jurisdiction`；或把 #19 期望改为 `answer` + `groups: [EU, CN]` |
| F-33 | — | `approval-checklist.md` §3 vs §5.2 C1 | Minor | 同一变更三处表述不一致：设计是 CK-03 **四态**（含 manual），用户批准清单写"CK-03 **三态**（online/offline/expired）"，`source-map.md` §6 又写"由三态改为四态" | 用户按清单签字时，会以为 manual 不存在——恰是 EU 唯一可用的模式；P-5 的证据 lint 本应抓住这类复述 | 全包统一为四态；批准清单的勾选项改为"四态状态机 + manual 证据字段" |
| F-34 | D2 | §4.2.1 MCP 协议面 | Major | 手写 JSON-RPC 只列了 `initialize`/`tools/list`/`tools/call`/错误对象四项，未定义握手完成通知、`protocolVersion` 协商、`tools/call` 的业务失败与 JSON-RPC 协议错误的分界，以及 stdio 的 framing/并发 | DSH 与 Claude Code 首次对接最常见的失败点就是握手与错误语义；W1 明确不做 MCP，风险全部压到已超载的 W2（Q1） | §4.2.1 补 6 条协议用例（握手/未知工具/参数非法/工具内失败/大响应/并发），W2 第 1 天先跑 MCP 冒烟再写适配 |

> Pending 1 项：**F-P1（D3）** §5.1 声称"六类页面必备段/WS/DF/EX 原样继承"，但本包未提供 `spec/` 导入后的落地形态，无法判断 C1 变更（`verbatim_excerpt` 从全文快照改为摘录）是否需要同步改 WS-03/CK-03 的页面侧判据——缺"页面侧如何引用摘录"的定义才能判。**不计 PASS。**

### 1.1 判级分布与"最该先修的三条"

| 判定 | 条数 | 集中在 |
|---|---|---|
| Block | 7 | 字段域（F-01）、绑定语义（F-02/F-03）、核验语义（F-04）、判定语义（F-05/F-06）、CI 判据（F-07） |
| Major | 18 | 数据契约 5（F-08~F-12）、值域 1（F-13）、判定/输出 2（F-14/F-15）、评估与计数 3（F-16~F-18）、运维检索排期 4（F-19~F-22）、输出对象 1（F-23）、模式语义 1（F-32）、协议面 1（F-34） |
| Minor | 9 | 命名/编号/承诺/包一致性（F-24~F-31、F-33） |
| Pending | 1 | 页面侧如何引用摘录（缺定义） |

先修顺序建议：**F-01 → F-07 → F-02/F-03 → F-04 → F-05/F-06**。理由：前两条决定"数据能不能入库"和"改规则能不能被拦住"，是其余一切的地基；后三条决定"答案/判定能不能成立"。

---

## 2. 十个必答问题

### Q1. 3 周内 50 KU + 20 金标 + MCP + 两家 skill，最大单点风险是什么？给量化理由。
**最大单点是工程侧的单人带宽，不是 KU 数量。** 假设 8h/人日、1 名工程 + 1 名 GRC 研究 × 15 个工作日（§10 人力假设）：

| 侧 | 估算 | 可用 | 负荷 |
|---|---|---|---|
| 工程（schema / CK-01~13 / compile+6 页+双哈希 / index / answer+binder / determine / ingest+impact+freshness / 手写 MCP / CLI / eval / 两家 skill） | 18–20 人日 | 15 | **120–133%** |
| 研究（53 KU × ~1.25h ≈ 8.3 + 20 金标 + 10 判定 + 双人核验复本 ≈ 12） | ~12 人日 | 15 | 80% |

- W1 已被自己排到 **7.7 人日 / 7.5 可用 = 103%**，其中 W1-7（EU 20 KU + 快照 + registry）只有 **1.5 人日 = 36 分钟/KU**，而 Tier A **双人核验**本身就要 20–30 分钟/KU，加上 29 字段结构化，60–75 分钟/KU 才是地板价 → 20 KU 需 4–5 人日，是该行预算的 3 倍。
- 最可能爆的是 **W2**：同周要交付 33 条新 KU（EU 13 + CN 20）、8–10 页、`determine`、MCP 六工具、20 金标。按 W1 真实速率，33 KU ≈ 5–6 人日，determine 2–3，MCP 1.5–2，页面 1，金标 1 → 10.5–13 人日 vs 7.5 可用。
- 关键结构性缺陷：**"只有 1 人"的弹性方案（CN 砍到 15 KU、金标 15 题）只砍研究侧，工程侧的 18–20 人日一分不少**，所以它救不了最大风险，反而顺手击穿 G2（见 F-16）。+6% 的 KU 增量（53 vs 50）也没有对应人日调整。

分周负荷（人日；1.5 FTE → 每周 7.5 可用）：

| 周 | 计划内容（设计 §10 + `w1-plan`） | 自估 / 重估 | 可用 | 判断 |
|---|---|---|---|---|
| W1 | core 四模块 + CLI + EU 20 KU + 4 页 + 10 金标 + 探针 | 7.7 / **10–12** | 7.5 | 自估即 103%；按 60–75 分钟/KU 重估超 30–60% |
| W2 | EU 13 + CN 20、8–10 页、`determine`、MCP 六工具、20 金标 | 未估 / **10.5–13** | 7.5 | 超 40–70%，是全周期最危险的一周 |
| W3 | update 闭环 + impact CI + 两家 skill + eval CI + demo + 文档 | 未估 / **6–7** | 7.5 | 依赖前两周产物；前两周超支，这周会被压成"演示补丁" |

三条量化结论：① 全周期重估 **27–32 人日 vs 22.5 可用**（120–142%）；② 唯一写进设计的降级手段只作用于研究侧；③ 15 条 locator 非法（F-01）会在 W1 第一天追加 0.5–1 人日返工，正好吃掉设计仅有的 3% 余量。

### Q2. C1（只存摘录）是否使 CK-03 的"可审计"主张不成立？如果是，最小修法是什么？
**部分不成立，但不是"必须存全文"的问题。** 三点机制性缺口：

1. **核验动作没有可复核产物**：manual 要求"截图或页面 hash"，§5.3 的元数据清单（source_url/accessed_at/excerpt_hash/verification/verified_at/verified_by）里没有字段放它 → 审计人只能看到"某实名说核过了"。
2. **被核验的 URL ≠ 答案里给的 URL**：EU 的 `source_url` 是 EUR-Lex（脚本 0 字节），人工核的是 EC Service Desk；答案给用户的链接打不开同样的文本（F-10）。这不是"不能自动追踪"，是"审计人无法重放"。
3. **四态只差一个自报标签**：offline 与 manual 在机器上不可区分（F-04），而 `expired` 在 3 周内不会触发（F-19）。

最小修法（不重分发全文，3 个字段 + 1 条规则）：snapshot 头增 `verification_url`（可抓的官方镜像）、`page_digest`（对 `verification_url` 全文取 sha256，**只存 hash 不存正文**）、`evidence_ref`（截图/页面 hash 路径）；CK-03 改为"摘录 = 快照摘录（逐字）+ 快照 `page_digest` 与本次抓取一致"。这样改版可被**发现**（digest 变了即 stale），证据可被**重放**（同一 URL + digest），而全文仍不分发——同时把 R1 从"无法发现改版"降为"能发现、需人工复核"。

### Q3. `determine` 的三态在法务风险上是否足够安全？哪类输出最容易被误读为法律意见？
**不够安全。** 最容易被误读的不是 `applies`，而是：

1. **`does_not_apply`**——这是一个**否定性法律结论**，用户读到的是"我们没事"，比"适用"更容易被当成放行许可；且它由"画像命中哪些规则"的**未命中**推出，等于用"库内没有规则"证明"法律上不适用"。
2. **`obligations` 清单**——不管加多少免责，交付一份"你要做这 12 件事"的清单，事实上就是合规建议；而 `findings[].reason` 是自由文本（"use_cases 命中'实时远程生物识别'；角色为 deployer"），读起来就是法律分析。
3. **缺 `as_of`/核验模式**（F-14）→ 用户无法知道依据何时核过，反而更敢用。

被误读风险排序（高 → 低）与本设计现状：

| 输出 | 用户会读成 | 现有护栏 | 缺口 |
|---|---|---|---|
| `does_not_apply` | "我们不受监管，可以上线" | 免责声明一句 | 无"未命中≠不适用"的措辞、无规则命中清单、无 `as_of` |
| `obligations` 列表 | "合规整改清单"（金标 #20 明确拒绝的东西，换了个入口又给出来了） | 无 | 没有与"清单"区分的命名/结构，也没有"这是条文转写、不是整改建议"的固定句 |
| `findings[].reason` 自由文本 | "法律分析" | 无 | 无模板约束，可写任意推断 |
| `applies` | "确认违法" | 免责 | 无"命中即推定，需监管解释确认"的强度标注 |

最小加固：`does_not_apply` 改名为 `no_rule_matched`（语义从"法律上不适用"降为"库内规则未命中"）；每条 finding 必须带 `basis`（规则 id + KU locator + 原文逐字）；`obligations` 改名为 `listed_obligations_from_source`；`does_not_apply` 只在画像字段全填时才允许输出（缺一即 `insufficient_info`）。免责声明替代不了这些，"不构成法律意见"挡不住"根据我的情况我不适用"这种个性化结论。

### Q4. "每条 claim 绑定 KU"在什么题型下必然失败？失败时的降级路径是否可接受？
**必然失败的五类**：① 归纳/计数句（"提供者共 12 项义务"）；② 否定/缺失句（"ISO 42001 不是法定要求"、"GPAI 章未收录"）；③ 跨域对比句（#19）；④ 译文句（C2 下所有"中文问欧盟"的答案）；⑤ 时间/适用性推断句（"你从 2027-12-02 起适用"）。

**降级路径不可接受**：删句→拒答会把 #19 变成拒答、把 #9/#17 从"纠正"变成"不知道"，把"义务清单"打碎成一串引文；用户体验上等于"什么都不敢说"，与 G2/G3 的目标相反；而 §7.1 的 refusal 枚举里根本没有"范畴纠正"这一类，作者连"正确地拒绝并纠正"都表达不出来。

可接受的最小设计：设三类句——**事实句**（必须绑 KU）、**框架句**（免绑，判据复用 rev4 的 DF-1/2/4/6 扫描：不含数字/日期/义务动词/条款定位即视为框架）、**否定句**（绑 registry 的 `scope_exclusion` 元数据，而不是假装有 KU）；refusal 增 `scope_correction`；跨域题按域分组，每组内部独立绑定。

逐题型对照（现状 vs 可用降级）：

| 题型 | 现设计的必然行为 | 用户可见后果 | 可用降级（最小） |
|---|---|---|---|
| 归纳/计数（"共几项义务"） | 计数句删句 → 只剩逐条引文 | 问题没被回答，用户自己去数 | 计数句归"框架句"，数字必须可由 claims 条数复算并输出 `count_from_ku: n` |
| 否定/缺失（#4/#9/#17） | `refuse(no_ku)`，无法纠正 | "这不是法规要求"被答成"库里没有" | 否定句绑 `scope_exclusion`；refusal 增 `scope_correction` 与固定句式 |
| 跨域分列（#19） | 要么拒答，要么违反 partial 语义 | 两个域的问题被当成"有冲突" | 按域分组，`answer` + `groups: [EU, CN]`，组内逐条绑 |
| 译文（C2 全场景） | 删句→拒答，或放弃 `--no-llm` | 中文用户拿不到中文答案 | `binding_mode: translation`，`verbatim` 绑原文、译文单列标 `machine` |
| 时间/适用性（#7/#8） | 只能引原文，不能给"你何时起适用" | 读完条文仍不知道自己的日期 | 时间句只由 `determine` 的 `applies_from` 产出，`ask` 不得自行推断 |

### Q5. 中文 BM25 的分词方案设计里没有——这算 Block 吗？最小可行方案是什么？
**不算 Block，而且 brief 的这个前提不成立**：设计 §4.2 已经给了最小方案——"ASCII 按词、CJK 按字符二元组（bigram），标题与 catalog 别名加权；不引入第三方分词"。在 50 KU / ~10 页规模上，bigram + 元数据过滤是够用的。

残留问题（Major，F-21）：① 没有检索质量的**判据**——W1-4 只用 5 个已知 query 的 top-3，20 金标的措辞差异不进验收；② `catalog.aliases` 无覆盖门槛，全凭作者手感；③ 数字/法条号（"2027-12-02"、"Art.5"、"第七条"）在 bigram 下会被切碎，需要整词保留。最小可行方案：bigram + 标题×2 加权 + 数字/拉丁整词 + 每题至少 1 个人工别名，验收判据"20 题 top5 召回 ≥18"；不达标再加 50 条别名表（0.5 人日），仍不达标才考虑引第三方分词（与"零依赖"冲突，需用户裁定）。

建议写进 `eval` 的检索验收（替换 W1-4 的"5 个 query 冒烟"）：

| 用例类 | 数量 | 判据 | 失败时的动作 |
|---|---|---|---|
| 标题直译型（问题词≈KU 标题） | ≥8 | top3 命中 8/8 | 查分词是否把术语切碎（数字/法条号整词化） |
| 同义改写型（"备案"↔"算法备案"） | ≥6 | top5 召回 6/6 | 补 aliases；统计每 KU 至少 1 别名 |
| 跨域混合型（含 EU + CN 实体） | ≥4 | 两域各至少 1 个 KU 进 top5 | 查元数据过滤是否把另一域整段滤掉 |

不达标时的最小补救是"人工别名表"（50 条 ≈ 0.5 人日），不是引第三方分词——后者与"零第三方运行时依赖"承诺冲突。

### Q6. 影响面矩阵的 CI 检查能否真正拦住"改规则不改样例"？给一个能拦和一个拦不住的例子。
**按现判据拦不住目标故障模式**（F-07）。

- **能拦**：新增/修改一个从未在任何矩阵行出现过的文件，如 `kb/ku/gsk-cn-genai-art12.yaml` → 不在 declared 并集 → `IMPACT_UNREPORTED`。这拦的是"忘记登记新文件"，不是"改了规则没回灌"。
- **拦不住**：只改 `rules/applicability-eu.yaml` 里 Art.6(3) 例外的 `not_in` 值，不动 `gsk-eu-art6-3.yaml` 的原文、也不动 `eval/determination.yaml` 的用例 7 → `actual_changed = {规则文件}`，而该文件早在某 done 行的 `changed_files` 里 → **PASS**。这正是 G-1 的原始形态；而且并集随每行单调增长，三周后 declared ≈ 全仓库，鉴别力趋 0。
- 修复三条：① 每次变更绑定唯一 `change_id`，declared 只取该行；② 消费集由 `ku_ids`/`depends_on` **图计算**（金标声明它依赖哪些 KU，规则声明它消费哪些 KU 字段），不靠申报；③ evidence 必须是可复跑产物 + 给 CI 自己加"故意漏申报必须 FAIL"的反向探针（P-4 纪律目前只覆盖 CK，没覆盖 CI）。

### Q7. 20 金标里哪几题在当前设计下**必然无法通过**？
| 题 | 为什么必然挂 |
|---|---|
| **#19 跨域标识要求** | `partial` 在 §7.2-3 只表示"冲突未消解"，本题无冲突 → 期望与 mode 语义冲突（F-32、F-17）；且中文作答 + 英文 verbatim 在 binder 下不可能同时成立（F-02） |
| **#9 ISO 42001 / #17 厂商认证** | 期望"refuse/纠正"，但纠正句是否定陈述，无 KU 可绑（F-03）；refusal 无 `scope_correction` 出口 → 只能 `refuse(no_ku)`，与期望的"纠正范畴"不符 |
| **#14 企业内部使用** | 同一问句两处期望不同（§2.3"信息不足"vs 附录 A"insufficient 或按 Art.2 回答"），且 `ask` 无 profile 槽（F-20）→ 无唯一判据，无法判"通过" |
| **#5 部署者日志 / #2 高风险分类** | 依赖 `Art.26(3)-(6)` 与 `Annex III 1–4/5–8` 的 locator，二者在继承域下非法 → 对应 KU 无法入库（F-01） |

需作者核实（不计入"必然"）：**#7 时间线**依赖 Art.113 单 KU 同段承载 2025/2026/2027/2028 四个日期，而 `verbatim_excerpt` 上限 1200 字符且禁止省略号；`eu-article-map.md` 里 Art.16 与 Art.113 的"段落数：0"（正文未抓），#1/#7 的底稿尚不存在。

### Q8. N-11 的修法在设计中缺失——最小修法（一句话）。
**CK-11 增一项"`log.md` 每行 `subject` 必须能解析为已存在的 `ku_id` / `page_slug` / `registry_id`，否则 `DANGLING_REF`"；CK-09 增一项"source 页 `{{log.*}}` 只允许 4 个占位符，且渲染值必须逐字取自 `log.md` 对应行/列，否则 `WHITELIST_VALUE_MISMATCH`"，并各配 1 个反例夹具。**

判 **Major 而非 Block**：位置已定（附录 C）、成本 0.1 人日、不阻塞 core；但设计只写"修入 CK-11/CK-09"，没有错误码、没有探针，与 08 报告 P-3 的四要素要求不符。顺序问题见 F-29：§13.5 写"先修 N-11 再 scaffold"，而 `w1-plan` 是 scaffold 之后 W1-1a 再修——两者只能留一个。

### Q9. 只能砍一件事保 3 周，砍什么？只能加一件事保质量，加什么？
**砍 `determine`（G3 整体移到 v0.2）**。理由：它是三项能力里唯一同时需要"封闭值域 + 定性法律判断 + 时间维度"的功能，成本 3–4 人日（规则表 + profiles + 10 用例 + 例外/优先级语义 + `--explain`），也是 R3 法务风险的唯一来源；砍掉后 G1/G2/G4/G5 全部保留，20 金标只需把 #8/#14/#16 改成"引用 Art.2 原文 + 声明库内规则未命中"，10 个判定用例降级为 5 个"引用式适用性问答"。反过来，如果砍 KU 或砍金标，伤的是 G2 这条唯一能证明"不造假"的验收线。

**加"契约干跑门禁"**：W1 第 0 天用**现有的两份样例 KU** 跑一遍 CK-01~13 + 一次 `ask`，把结果作为第一份 `evidence/`。本次实核已证明这两份样例在 CK-04（F-11）与逐字项（F-12）下会红——先让契约在真实载体上跑红一次，比再加任何功能都更能防 G-1/G-5 复发。

砍与不砍的取舍代价（同一张表看两个方向）：

| 方案 | 保住的验收 | 失去的验收 | 人日变化 | 法务风险 |
|---|---|---|---|---|
| 砍 `determine`（建议） | G1/G2/G4/G5 全保 | G3 移到 v0.2；3 个适用性金标改"引用 Art.2 + 库内未命中声明" | −3~4 | 降（唯一的高风险输出消失） |
| 砍 CN 域 | G1/G2/G4/G5 形式保留 | "双域"承诺作废（用户明确要的）；CN 7 题全废 | −4~5 | 不变 |
| 砍 20 金标到 15 | 工期 | G2 的"20 题 100%"彻底不可验收（F-16） | −1 | 升（证明"不造假"的唯一仪器没了） |
| 砍 MCP 只留 CLI | 工期 1.5~2 | G4 跨平台承诺作废，三家宿主全落空 | −1.5~2 | 不变 |

判断依据：四项里只有 `determine` 是"高风险 + 高成本 + 可后置"三者同时成立；砍它不会让任何一条已承诺的验收指标变成"无法验收"，只会让 G3 后移。

### Q10. 总裁定与条件清单？
**B 有条件通过**（命中一票否决：无）。条件见 §3：7 条，全部是 **W1 第 0 天前** 的契约修改，不涉及实现。任一条被反驳且无替代判据 → 降为 C。

---

## 3. 条件清单（B 的前提）

| # | 对应发现 | 修法 | 为什么必须在 W1 前完成 |
|---|---|---|---|
| C1 | F-01 | 扩 `locator` 条款式（允许字母项）并新增附件式；按新域重扫 ku-plan 33 条 | W1-1 的"契约导入"会把旧域固化进 `spec/`，之后 15 条 KU 与金标 #1/#2/#3/#5 都要返工（G-1 模式） |
| C2 | F-02 | claim 分三类绑定（quote/translation/frame），改 §7.2-1 与 §7.3，`citations[]` 补 `verbatim`/`verified_by`/`anchor`（F-23） | 绑定语义是 answer 模块的输入契约；W1-5 一开工就要按它写 binder，改一次等于重写 |
| C3 | F-03 | 归纳/否定/对比句的绑定或免绑规则 + refusal 增 `scope_correction` | 20 金标 W1 冻结；不先定判据，冻结的就是一张判不了的卷子（F-17） |
| C4 | F-04/F-10 | CK-03 状态机 + `evidence_ref` + `page_digest` + `verification_url` | 核验元数据决定 sniff/snapshot 的文件格式；W1-7 写 53 个快照头时再改，成本×53 |
| C5 | F-05 | verdict 增 `applies_later` / `applies_from` | 判定枚举是 rules YAML 的值域，规则写完再改要重写全部规则 |
| C6 | F-06/F-15 | 明确 `in/not_in` 列表语义、增 `intersects`、`judgement_required`；写死 exceptions→priority 求值顺序 | 规则引擎的运算符集是"禁止脚本表达式"承诺的基础，改运算符集 = 改全部规则 |
| C7 | F-07/F-22 | impact CI 改 change_id 绑定 + 图计算消费集 + evidence 产物 + CI 反向探针；清理矩阵假路径行 | G-1 是 08 报告的第一根因，也是本设计唯一承诺"机器拦截"的机制；W3 再改等于没有拦截 |

> 附条件（不阻塞 W1，但须在 W1 结束前关闭）：F-08（款/项）、F-09（核验粒度）、F-11/F-12（样例过 validate）、F-13（值域闭合）、F-16/F-17（数字与分类）、F-19（R1 承诺降级）、F-21（召回判据）。这些若拖到 W2，会以"改一处、返工三处"的方式兑现 G-1。

---

## 4. 我认为设计做对的 3 件事

1. **把"不造假"从口号变成了机制**：判定与 LLM 解耦（规则引擎 + `--explain`）、答案先抽取后措辞、binder 后校验、`--no-llm` 兜底——这是 rev4 五轮里始终缺的"运行体"，方向完全正确。问题只在绑定语义的边界（F-02/F-03），不在思路上。
2. **C1 的方向对，而且比 rev4 更诚实**：只存摘录 + 四态核验 + **把核验模式提升为答案必带元信息**，这是 rev4 没有的进步；它把"我们核过"变成用户可见的字段。要补的是证据落点，不是推翻取舍。
3. **范围克制 + 工装化意识**：comparison 页明确移出 MVP、GPAI/罚则/算法推荐明确排除、20 金标 W1 冻结、影响面矩阵 + 探针正反基线 + 数字生成化——这四条都是 08 报告 P-1/P-2/P-4 的正确落点。即便判据要重写（F-07），"先造工装再写内容"的顺序是对的。

---

## 附录 A · 实核记录（可复跑，非实现代码）

> 方法：`python3` + `PyYAML` 单行脚本对样例与计划做机械核对；locator 用 rev4 §3.1 的 5 条正则 + 设计 C4 的第 6 条逐条匹配。命令不构成实现，仅为评审证据。

**A-1 字段完整性（①）**：两份样例均为 **30 个顶层键 = 29 字段 + `gap`**，17 个 fact-bearing、12 个 bookkeeping 无缺、无多余；`gap` 未混入 29。→ 作者的"字段齐"成立。
**A-2 逐字性与值域（①）**：
- `obligation[].text ⊂ verbatim_excerpt`：**6/6 全部失败**（EU ob-1 1/1；CN ob-1..ob-5 5/5）。
- CN `evidence_requirement[0].text` 来自暂行办法第十九条（不在 53 条计划内，excerpt 不含）。
- `fingerprint` 两份均为 `minhash96:pending-w1`（占位符）。
- 四个事实子字段（`modality`/`subject`/`frequency`/`scope`）无枚举表；两份样例已出现 `per_placing_on_market` 与 `on_request` 两种 frequency 写法。
**A-3 locator 域（②）**：`ku-plan` EU 33 条中 **15 条非法**：`Art.5(1)(a)-(b)`、`(ba)`、`(bb)`、`(c)`、`(d)`、`(e)`、`(f)`、`(g)`、`(h)+Art.5(2)`、`Annex III 1–4`、`Annex III 5–8`、`Art.26(1)-(2)`、`Art.26(3)-(6)`、`Art.26(7)-(9)`、`Art.50(3)-(4)`。CN 16 条"第X条"全部合法；但 `第七条第二款`、`第四条第（二）项`、`第十七条第一款` 等款/项形态 **4/4 不匹配**。
**A-4 CK-04（①）**：EU 样例 `definition`/`scope_in`/`scope_out`/`common_misreadings` 全 null，CN 样例 3 个 null，两份 `gap: []` → 按 rev4 §5 均 `CK-04 FAIL(INSUFFICIENT_INPUT)`。
**A-5 金标计数（⑧）**：附录 A 20 题中拒答/纠正期望 **5** 题（#4/#9/#10/#17/#20），跨条仅 **1** 题（#19）；§9.1 写"拒答 3、跨条 2"；§3.1/§9.2 另有一组"5 个负例"，与金标内 5 题易混。
**A-6 数字漂移（③）**：50（§0/§3.1）vs 53（附录 E/ku-plan）；ku-plan 标题"EU（32）"vs 表内 33 行；"9 处已修"（设计头）vs"11 处"（自检）；"refs 19→50 边"（§9.2，19 为 rev4 遗留）；§10 弹性"金标 15"vs G2"20 金标"。
**A-7 影响面矩阵（⑦）**：现有 2 行，`templates/source.md` 与 `00-MVP定义.md` 在本仓库不存在；N-11 行 evidence = "见 W1"；C4 行 evidence 无产物文件。判据为"全表并集"，推演见 Q6：改 `rules/applicability-eu.yaml` 而不改样例/金标 → PASS。
**A-8 输出对象（⑨）**：§7.1 的 `citations[]` 缺 `verbatim` 与 `verified_by`，与 §7.1 末句、§7.2-6 冲突；`refusal` 无 null 约定。
**A-9 判定语义（⑥）**：`verdict` 四值无法表达"未生效/部分适用"；`in/not_in` 对列表字段有两种读法；`exceptions`/`priority` 无求值顺序 → 三个不可判定场景（Art.6(3) 定性例外、CN Art.17 开放性限定、跨生效日画像）。
**A-10 核验可行性（④）**：`source-map.md` §6 实测 EUR-Lex 返回 0 字节、gov.cn/cac.gov.cn 200、Service Desk 可读；设计 `source_url` 全部指向 EUR-Lex → offline/manual 是 EU 的唯一路径，online 覆盖 0/33（CN 20/20 可 online）。

## 附录 B · D1–D9 逐维小结

| 维度 | 判定 | 一句话结论 | 关键发现 |
|---|---|---|---|
| D1 目标与范围 | 有条件 | 四数字不自洽（50/53/32/33），弹性方案会击穿 G2 | F-16、F-17 |
| D2 架构 | 基本成立 | 三层边界清楚；MCP 协议面未闭合；bigram 方案已给但无检索判据；组件表漏 binder | F-21、F-24、F-34 |
| D3 数据契约 | **不成立（须修）** | 29 字段继承无误，但 locator 域、CK-04、逐字性、核验粒度四处实测失败 | F-01、F-08~F-13、F-23 |
| D4 答案契约 | **不成立（须修）** | 绑定语义在译文/归纳/否定三类句上互斥或缺口；refusal 不穷尽 | F-02、F-03、F-20、F-32 |
| D5 判定 | **不成立（须修）** | 缺"尚未生效"态；运算符与例外语义不足；输出无元信息 | F-05、F-06、F-14、F-15 |
| D6 更新闭环 | 有条件 | 六步在 5 分钟内可跑（证据规模小）；但 CI 判据拦不住 G-1，矩阵现有行无效 | F-07、F-22 |
| D7 评估 | 有条件 | 用例类型缺"多轮追问/同一问题不同措辞/时间敏感"；三个指标可自欺 | F-17、F-18 |
| D8 历史病 | 部分治愈 | G-5（独立复核）由 CCC 流程承接；G-1/G-2/G-4 仍是口号，工装判据未落地 | F-07、F-13、F-27、F-29 |
| D9 风险与跨平台 | 有条件 | R1 缓解成本未入排期；语言策略补字段后可表达；跨平台承诺应收窄到两家 | F-10、F-19、F-23、F-30 |

补充三点 brief 未点名但影响验收的问题：① 用例类型缺"同一问题不同措辞"与"时间敏感题"，而金标 #7 正是时间敏感；② `--no-llm` 与 C2（用户语言）不可同时满足，见 F-02；③ 多轮追问完全未定义（MVP 无会话状态），若宿主自动带上下文，`ask` 的"同题两次一致"指标会失真（并入 F-18）。

---

**局限**：① 未核法条原文（brief §2 边界），凡涉及条文内容的判断标"需作者核实"；② 未运行任何实现（本轮无代码）；③ 08 报告只用于 G-1~G-5 与 P-1~P-7 的对照，未作为定级依据；④ 作者自评文件在包内（brief 声称不含），我在完成 A-1~A-10 后阅读，仅用于核对"9 vs 11"这一数字矛盾，未采用其定级。
