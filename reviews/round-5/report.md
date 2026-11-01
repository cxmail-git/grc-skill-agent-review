# CCC 评审报告 · GRC Skill Agent 设计 v0.5（Round 5）

## 绑定

| 项 | 值 |
|---|---|
| 评审对象 | `02-design-v0.5.md`（分支 `design-v0.5`，commit `1231c57a36803a047b2ac2e5a24f4772c90dcc2d`） |
| design_sha256 | `c763b8eb2c50e43c27c9e26ddc5666c97e33e0c869ac3ec3d91af02dbc931ab7`（我对该 commit 的文件自算，**一致**） |
| package_sha256 | Issue #3 评论给出 `e0562258…ba6de`。**我无法复现**：包内未说明计算方法。我只核对了 `SHA256SUMS.txt`：22 个文件全部 OK，含设计文件 |
| 评审轮次 | 第 5 轮（Issue #3）。评审人：CCC（独立第三方） |
| 评审依据 | `01-review-brief.md` 协议；设计全文；`attachments/06-ku-plan.md`、`07-sample-kus.md`；`05-source-map.md` 定点；`10-ccc-findings-resolution.md` 全文、`12-pre-review-v04-report.md` 前 60 行 |
| 未核 | `08-defect-clustering.md`、rev4 两份 schema 未通读。依赖原文或上游事实的结论均标「需作者核实」，我无法独立验证 2026-07 之后的 EU 事实 |

**独立性说明**：评审包含作者侧的预演与处置文档（05–08、10、12），与 brief §7「本包不含作者自评」不符。我把它们当作作者声明而非证据：所有「已修」状态都按 v0.5 实际文本重新核对。

**过程提示（作者需处理）**：`reviews/round-5/REQUEST.md` 里的 hash（`a92939d2…` / `1c3210d1…`）对应旧 commit `c5d353d`，与 Issue 评论指定的 `c763b8eb…` 不一致。按同步协议硬规则 2 这会触发 `REVIEW_STALE`。本报告按作者指示绑定 `c763b8eb…`，请作者更新 REQUEST.md。

---

## 0. 总评估（总裁定）

**B 有条件通过**：命中一票否决 **无**（包内仍未定义否决条款）。

- 计数：**Block 2 / Major 15 / Minor 4**。
- 方向正确：砍 determine、全文快照、宿主成文、UNVERIFIED 降级这四个用户裁定都落进了设计，3 周范围比 v0.1 可信得多。
- 但 v0.4 复核的 3 个 Block 里，**只有 B-01（全文快照口径）基本关闭**；B-02（句内容校验）与 B-03（宿主跳过校验）**部分关闭**，仍有两个会造成「看起来被校验过、实则放行」的缺口，即本报告的两条 Block（V5-01、V5-02）。
- **降级触发器**：若作者只加文字声明而不增加可机检的校验项/错误码，则降为 **C 不通过**。

### 对 Issue #3 重点复核项的结论

| 复核项 | 结论 | 依据 |
|---|---|---|
| B-01 全文快照口径统一 | **基本关闭，有残留** | §0/§1.3/§4.1/R7 的旧口径已改。残留：样例 KU 仍写逐 KU 快照；锚点正则与 `verification.yaml` 的锚点冲突；C1 元数据清单与 §5.3 示例不一致（V5-07） |
| B-02 `validate_answer` 句内容校验 | **部分关闭（仍 Block）** | `evidence_quote` 子串、数字/日期/专名、情态词三项都是词面级，拦不住「范围扩大」「结论句」（V5-01/02） |
| B-03 宿主跳过校验可检测 | **部分关闭（Major）** | 有 `answer_id` 与 `--host-simulate skip`，但只在 CI 模拟里可检；生产无已签发/已校验对账，且校验的句子与最终展示文本无绑定（V5-03） |
| determine 是否清零 | **可接受，有残留** | MCP 工具、规则 YAML、判定用例已移出。§8 全节（约 80 行）仍留在基线正文，目录树仍列 `rules/` `profiles/`（V5-18） |
| 金标 #19 `groups` / `coverage_note` | **结构已有，机检不足** | `groups` 在 §7.1 与 #19 中恢复。但 `coverage_note` 是自由文本且硬编码数字，`mode` 重算无算法（V5-10/11） |
| 32 KU 分项和 | **一致** | 我自算 1+7+3+4+8+1+3+1+3+1 = 32，`06-ku-plan` 表 32 行，加 CN 13+7 = 20，合计 52。但 §1.3 与 CK-14 示例对 GPAI 的条款号不一致（V5-17） |
| PyYAML 安装/离线路径 | **有路径，缺加载策略** | `pip` / `vendor/wheels/` / `grc doctor` 已写。缺 `safe_load`、隐式日期/布尔、重复键策略（V5-14） |

---

## 1. 逐条发现

| # | 维度 | 位置 | 等级 | 问题 | 依据/反例 | 修法 |
|---|---|---|---|---|---|---|
| V5-01 | D4 | §7.4 | **Block** | `validate_answer` 通过（`ok:true`）不等于句子忠实于证据，且校验对象与最终展示文本无绑定。 | ① 第 3–5 项只管 `evidence_quote ⊂ claim`、数字/日期/专名、情态词。**反例**：claim 为「High-risk AI systems shall be designed … overseen」，宿主写「所有 AI 系统都必须能被有效监督」，`evidence_quote` 取「can be effectively overseen」。没有数字，情态词一致，`ok:true`，但主体范围由「高风险」扩大到「所有」。②「专名」在无 NLP 的纯标准库实现下无法可靠抽取中文实体。③ 宿主校验句子集 A，展示文本 B：§4.2.1 入参是 `{answer, claims, sentences, language}`，§7.4 入参是 `answer_id + sentences + …`，二者不一致，且都不要求 `final_text == join(sentences)`。④「校验失败不得展示答案」后用户看到什么，没有退路。 | ① `ask` 返回 **core 生成的候选句**（抽取式、带 claim_ids），宿主只能选用/重排/加 frame；自由改写句标 `paraphrase`，并校验范围词/主体词/条件词（所有、任何、仅、除非、provider/deployer、high-risk 等）与所绑 claim 的差集为空。② 入参增 `final_text`，校验其等于句子拼接；返回 `validation_token = H(answer_id, sha256(final_text))`，宿主展示须带 token。③ 失败回退 `render_extractive`：直接逐字展示 claim 原文。④ 统一 §4.2.1 与 §7.4 的入参。是否接受自由改写：**转用户裁定** |
| V5-02 | D4/D5 | §0 取舍1、§8.4、§7.2 | **Block** | determine 移出后，「不输出适用/不适用结论」只靠 `SKILL.md` 文字，没有机检执行点。 | `frame` 句只扫 DF-1~6，不含「适用/不适用/合规/违法/applies/compliant/exempt」。`forbidden_terms` 只在金标与 eval 用，不在运行时 `validate_answer`。**反例**（#14）：宿主输出 frame 句「因此贵司内部知识库不适用该办法。」，无日期/条款/状态词/数字，`ok:true`。这是 R3 的核心风险，现在也是唯一防线。 | `validate_answer` 对**所有**句子（含 frame 与 claim 绑定句）扫结论词表，命中则 `CONCLUSION_FORBIDDEN`，除非该句整句是 `evidence_quote` 的逐字引文；配反向探针与 `adversarial.yaml` 用例；范围问题的结尾句改为 core 固定模板（引原文 + `coverage_note`） |
| V5-03 | D4/D8 | §7.4、§9.2、R10 | Major | 宿主跳过校验只在模拟中可检，生产不可检。 | `--host-simulate skip` 只模拟坏宿主；真实宿主若跳过，core 只能看到「已签发 `answer_id`」，没有与「已校验」对账指标。`answer_id` 记录落盘到 `evidence/answers/`，与 R10「MVP 默认不落盘」冲突；stdio 进程重启或 2 连接并发时，answer 状态在何处共享也未定义。G4 的「各跑 3 问」没有要求留宿主转录。 | 增 `issued_vs_validated` 计数和 `grc audit-answers`；answer 状态存放位置与 R10 的例外写明；G4 验收要求宿主转录归档 |
| V5-04 | D4 | §7.1 `claim.text`、§7.4 第 4–5 项 | Major | 跨语言校验缺规范化与职责归属。 | 中文问 EU 英文 KU：`claim.text`「与 sentence 语言一致」，由谁生成？core 无 LLM、宿主自写则校验循环。第 4 项「数字/日期 ⊆ quote」没有 `2027-12-02` ↔ `2 December 2027` ↔ `2027年12月2日` ↔ `twelve` ↔ `12` 的规范化；第 5 项没有 shall/must/may ↔ 须/应当/可以 与 `shall not` ↔ 不得 的映射表。F-02 在处置表标「已修」，机制未闭合。 | 定义规范化函数与情态映射表，并为之配正反用例；明确 `claim.text` 的唯一生成方 |
| V5-05 | D3 | §5.3 | Major | 全文快照仍是人工自证，CK-03 第 3 项对不可抓取来源不可执行。 | EU 32/52 KU 的全文由人工下载（`05` §6：EUR-Lex 脚本抓取返回 0 字节），`fulltext_sha256` 是对自己保存副本的哈希；`KU ⊂ 快照` 现在可机检，但「快照 = 官方文本」仍是 `manual` 声明。第 3 项「`page_digest` 与 `verification_url` 最近抓取一致」要求可抓取，Service Desk 页是否可抓**包内无证据**。 | 明确每个来源的核验路径：可抓取 → `online`；不可抓取 → 写明 `manual` 的存证内容与复核频率，并从 CK-03 的机检项中剔除第 3 项。可抓取性需作者核实 |
| V5-06 | D4/D9 | §5.3、§7.1、R2、R11 | Major | UNVERIFIED 没有输出字段与行为定义；风险登记仍写「双人核」。 | 单人核验后 52 条 KU 全部 `second_review:false`，即**所有**答案都带 UNVERIFIED，但 §7.1 对象无该字段，`validate_answer` 第 7 项不检查，`UNVERIFIED 占比` 不设门槛。R2 仍写「KU 模板化 + 双人核」，与 D5/R11 矛盾。`expired` 对 `mode` 的影响也未定义（`partial_reason` 无 `expired`）。 | §7.1 增 `unverified:true` 与警告文案；`validate_answer` 校验其存在；R2 改写；定义 expired 时的 mode |
| V5-07 | D3 | §5.2 C1、§5.3、`07` | Major | B-01 文本残留（四处）。 | ① 样例 KU `snapshot_ref: "snapshots/gsk-eu-art14.md#p1"` 为逐 KU 文件，§5.3 为 `snapshots/<source_id>.md`。② `verification.yaml` 的锚点 `#Art.14(1)` 含点和括号，违反 §5.2 的 `anchor` 正则 `^[a-zA-Z0-9_-]+$`。③ C1 元数据列表有 `excerpt_hash`，§5.3 示例用 `fulltext_sha256` + `page_digest`，§6.1 第 2 步产物仍是 `excerpt_hash`。④ §7.1 citation 示例 `verified_by: "R-2 / 张三"`，§5.3 要求只写角色码。 | 逐条对齐；实名只在审计存证中出现 |
| V5-08 | D3 | `effective_date`、`transition_note` | Major | 产品里最关键的事实（适用日期）不受 CK-03 约束。 | CK-03 只比对 `verbatim_excerpt ⊂ 快照`。`effective_date` 与 `transition_note`（含 Art.113 的三个日期）是作者手写字段，答案 #7 的日期来自它们。 | 增校验：这两个字段里的日期 token 必须能在 `verbatim_excerpt` 解析出对应日期（含 `2 December 2027` 这类英文写法的规范化）；日期以外的内容标为作者注 |
| V5-09 | D3/D4 | §7.4.1 CK-14、`scope_exclusions.yaml` | Major | 「否定/缺席」断言混了两种东西，且未利用全文快照做机检。 | `sx-eu-gpai`（本库未收录）是覆盖范围声明；`sx-eu-iso42001`（条例不含该要求）是对来源的否定断言，`evidence_url` 指向 iso.org（标准机构页面，不是该法规）。全文快照现在使「源文不含 ISO/42001」可机检，CK-14 却只查三项存在性。#17（CN 厂商认证）没有 CN 条目，而 CK-14 第 2 项要求 `jurisdiction` 一致。 | `absence_kind: coverage \| source_silent`；`source_silent` 增 `absence_terms` 并对快照全文扫描 0 命中；补 CN 条目；措辞与 `kind` 绑定（「本库未收录」≠「法规未要求」） |
| V5-10 | D4/D7 | §7.2-6、`validate_answer` 第 6 项 | Major | `mode` 重算没有算法，金标期望前后不一。 | 「由 claims 覆盖与 coverage_note 推导 mode」未给函数。#3（Art.5 缺 3 项）期望 `partial(coverage_gap)`；#1（缺 Art.17/43）、#2（Annex III 只收 8 类里的 4 类）、#6（Annex IV 不在库，而 Art.11 的内容在 Annex IV）同样有范围缺口，却期望 `answer + coverage_note`。#19 两域各自完整，却标 `partial(cross_jurisdiction)`。#4 期望 `no_ku`，但库里登记了 `sx-eu-gpai`，更像 `out_of_scope`；`out_of_scope` 与 `conflict_unresolved` 无任何用例。 | 给出 `mode` 的确定性函数（输入 = skeleton 覆盖、scope_exclusion 命中、groups、冲突）；按函数重排 20 题的期望值；每个 `refuse.reason` 至少 1 条用例 |
| V5-11 | D7 | §9.1、附录 A | Major | `coverage_note` 无法机检，且含手写计数。 | 示例「覆盖 Art.5 的 7 项……其余 3 项」违反 P-1。`expected_coverage_note` 是自由文本，比对规则未给。 | 用 `coverage_codes: [sx-…]` 表达，文案由 core 从 `scope_exclusions` 与 KU 集合生成，计数脚本生成 |
| V5-12 | D4 | §7.2-5、F-10 | Major | `not_legal_advice` 的识别责任方未定义。 | 处置表自认「仍依赖意图解析」。宿主成文后，`ask` 的 `query` 谁来识别「我们这样做算不算违规」？`no_llm` 参数在 core 无 LLM 的前提下含义不明。#10/#20 在换措辞时可能被当作普通问答答出。 | 在 core 内规则化关键词/句式表，由 `ask` 返回 `refuse(not_legal_advice)`；定义 `no_llm` 的实际含义 |
| V5-13 | D6 | §6.2 | Major | 影响面 CI：粒度与安全两个缺口。 | ① `graph_required(KU → eval/golden.yaml)` 到文件级，改该文件任一无关行即满足，**拦不住**「改了 KU、没改对应金标条目」；**能拦**：只改 KU 不动 `golden.yaml`（反向探针）。② `evidence[].cmd` 由 PR 提供，CI 执行并逐字比对输出：既是命令注入面，也会因时间戳/路径抖动产生 `EVIDENCE_STALE` 误报。 | 粒度到 `golden` 条目（`expected_claim_ku_ids` 反查）；`cmd` 只允许白名单 `grc` 子命令；输出比对前做规范化 |
| V5-14 | D2 | §4.2、§5.4 | Major | PyYAML 的加载策略缺失。 | `safe_load` 对**重复键静默以后者覆盖**，在 29 字段闭合 schema 里是完整性风险；`effective_date: 2027-12-02` 被解析为 `date`，`no`/`on` 被解析为布尔。`vendor/wheels/` 需按平台/CPython 版本备齐；`==6.0.2` 对较新的 CPython 是否有 wheel：**需作者核实**。 | 写明：`safe_load` + 重复键检测 + 关闭隐式日期/布尔解析；wheels 矩阵；`pip --require-hashes` |
| V5-15 | D1 | §10、R2 | Major | 排期仍无法验证。 | 「重估 20–24 人日」没有分解，也没说是工程一人的量还是两人合计。以下是我的**估算，请作者复核**：CK-01~15 + 7 形态 locator + binder + `validate_answer`（含宿主模拟器）+ MCP 六工具 + 变更 CI 七步 + eval 约 18–22 工程人日，高于 1 名工程的 15 个工作日；研究侧 52 KU × 1.2–1.5 h ≈ 8–10 天。R2 同时写「52 不减」，而 §10 / 审批清单里仍有 CN 15 条的弹性方案。 | 给出分项人日并标明归属；固定弹性方案的触发点 |
| V5-16 | D7 | §9.1–9.2 | Major | 评测设计仍有自评空间。 | 检索召回 `top5 ≥18/20` 与「每题至少 1 个别名」用同一批题：别名按验收题调，召回等于训练集成绩。`frame ≤20%` 在 §7.3 是 WARN、在 §9.2 是门禁。「稳定性」在确定性 core 上必然通过，信息量低。6 类用例没有数量。「宿主合规」只覆盖模拟宿主。 | 增留出集（异措辞，别名不看）；统一 WARN/门禁；稳定性改测 `--llm` 轨；各类用例定数量 |
| V5-17 | D1/D3 | §1.3、§7.4.1、`06` | Minor | 范围声明不一致。 | §1.3 写 GPAI 为 Art.53–55，CK-14 示例与 `05` 为 Art.51–56（我在 round-3 的 F-18 中已指出，未改）。`gsk-eu-art26-5` 的 locator 是 `Art.26(6)`。Art.5 选 7 项与 (ba)(bb) 的存在及生效日：**需作者核实**。 | 统一条款号；ku_id 与 locator 对齐 |
| V5-18 | D5 | §8、§5.4 | Minor | determine 已移出，但 §8 整节仍在基线正文。 | §8.1–8.4 保留了完整输入/输出/规则 schema，目录树仍列 `rules/` `profiles/`，易被当作 MVP 规格实现。 | 移到独立 backlog 文件，正文只留一行指针 |
| V5-19 | D3 | §5.1 N-11 修法 | Minor | `date` 校验方向与 rev4 日志表冲突。 | rev4 §7.5 规定 `log.md` 为时间**倒序**，修法写「`date` 不早于上一行」，倒序下方向相反；追加性仍是人工项。 | 指明方向，或改为末尾追加；追加性用「git diff 仅新增行」自动校验 |
| V5-20 | D9 | §1.3、§5.3 `license_note`、R7 | Major | 「不再分发」与「存全文」口径冲突，且评审仓库是公开的。 | §1.3 非目标仍写「对来源全文的再分发」，`license_note` 写「不再分发用于商业转售」；若 `kb/snapshots/` 随可安装包或公开仓库发布，就是再分发。**法律结论需作者/法务核实**。 | 明确快照是否随包发布；若不随包，写入打包清单；`license_note` 与 §1.3 统一为同一表述（**转用户裁定**） |
| V5-21 | — | 全文 | Minor | 版本与自检残留；流程项。 | 头部 `升 v0.2`（§13）、「9 处内部不一致」「v0.1」表头（附录 C）、MANIFEST 写 v0.3；R5 写「Codex 仅抽验」而 §4.3 为「未验证」。`review/round-3` 分支含 `docs/review/ccc-report.md`，会触发 `review-guard` 的 `REVIEW_WRITE_OUT_OF_SCOPE`（我按用户指示提交，请作者留意）。 | 清理残留；round-3 分支处置请作者决定 |

---

## 2. 十个必答问题

**Q1 最大单点风险？**
A1：**`validate_answer` 的规格不足**（V5-01/02）。它是 determine 被砍之后唯一的运行时防线，同时是最难做的组件：在无 NLP 库的纯标准库下做「句子忠实于证据」的词面检查。次要风险是排期（V5-15）：我估算工程约 18–22 人日对 15 个工作日，超出约 20–45%；若「20–24 人日」是两人合计，则隐含工程仅 12–14 人日，低于我的估算。

**Q2 C1 是否使 CK-03 的「可审计」不成立？**
A2：**不再成立，但未完全闭合**。全文快照使 `KU ⊂ 快照` 与 locator 定位可机检，修了 v0.1 的核心问题。残留：「快照 = 官方文本」对 EU 仍是人工自证（V5-05），日期字段不受约束（V5-08）。UNVERIFIED 降级是诚实的，但要给输出字段（V5-06）。

**Q3 法务风险：哪类输出最容易被误读为法律意见？**
A3：determine 移出后，最易误读的是三类：① 范围问题（#8/#14/#16）里「引 Art.2 原文 + 宿主一句结论」，读成「适用/不适用」（V5-02）；② 带范围缺口却标 `answer` 的列表（#1/#2/#6），读成完整清单（V5-10）；③ 未标 UNVERIFIED 的答案读成已双人核验（V5-06）。免责措辞仍需法务，**转用户裁定**。

**Q4 「每条 claim 绑定 KU」在什么题型下必然失败？降级路径？**
A4：归纳/综述、计算类、多 KU 条件推理仍然失败；否定类已由 `support_type=absence` + CK-14 承接（需 V5-09 修补）；跨语言作答在规范化缺失时失败（V5-04）。降级路径缺最后一环：「校验失败不得展示」之后用户看到什么（V5-01 修法 ③：core 抽取式回退）。

**Q5 中文 BM25 分词？**
A5：**不是 Block**。§4.2 已有 bigram，纯标准库可行。缺口是评测设计（V5-16）：别名与召回验收同一批题。

**Q6 影响面 CI：能拦与不能拦各一例？**
A6：**能拦**：只改 `kb/ku/gsk-eu-art6-2.yaml`、不动 `eval/golden.yaml`（§6.2 第 7 步反向探针，必须 FAIL）。**拦不住**：改了 KU，同时改 `golden.yaml` 的无关行，文件级 `required_updates ⊆ actual_changed` 满足但对应条目未更新（V5-13）。

**Q7 20 金标里哪几题在当前设计下会失败？**
A7：
- #1、#2、#6：有范围缺口却期望 `answer`，与 #3 的 `partial` 口径冲突（V5-10）。
- #4：`sx-eu-gpai` 已登记，应为 `out_of_scope` 而非 `no_ku`（V5-10）。
- #17：没有 CN 的 `scope_exclusion` 条目，CK-14 第 2 项（法域一致）不满足（V5-09）。
- #19：两域各自完整，标 `partial` 语义偏差，且 `ask` 的 `jurisdiction?` 是单值，分组路由未定义（V5-10）。
- #10、#20：换措辞时依赖未定义的识别方（V5-12）。
- #1–#3、#5–#8：中文提问 + 英文 KU，在 V5-04 规范化缺失下，数字/情态词校验无法通过或会误拒。

**Q8 N-11 的修法？**
A8：§5.1 已有具体修法（五值事件、`subject` 解析、`date` 校验、CK-09 投影、各配 1 反例），**已足够开工**。仅需指明 `date` 的方向（V5-19）。

**Q9 只能砍一件事？只能加一件事？**
A9：**砍**：§6.2 第 5–6 步（重跑 `evidence.cmd` 逐字比对、`impact-matrix` 路径检查）改为人工清单，保留反向探针；这是 V5-13 的安全面，也省下 CI 工作量。**加**：V5-01 修法 ①②——core 候选句 + `final_text` 绑定 + `validation_token`。

**Q10 总评估与条件？**
A10：**B 有条件通过**，条件清单见 §3。

---

## 3. 条件清单

| # | 对应发现 | 修法 | 为什么必须在 W1 前完成 |
|---|---|---|---|
| 1 | V5-01 | core 候选句 + 自由改写校验 + `final_text`/`validation_token` + 抽取式回退 | 它决定 `ask`/`validate_answer` 的接口，改晚了 MCP 与 skill 都要返工 |
| 2 | V5-02 | 运行时结论词表扫描 + 反向探针 + 固定结尾模板 | 这是 R3 唯一防线，且是用户明确的「不输出结论」要求 |
| 3 | V5-03、V5-04 | 对账指标、答案状态存放、跨语言规范化与情态映射表 | 金标 7 题依赖它 |
| 4 | V5-05–V5-09、V5-20 | 快照核验路径、UNVERIFIED 字段、文本残留、日期校验、absence 分类、再分发口径 | 它们决定 KU 录入格式，录入开始后改会全部返工 |
| 5 | V5-10–V5-12 | `mode` 函数，按函数重排金标期望，`coverage_codes`，识别方 | 金标在 W1 末冻结 |
| 6 | V5-13、V5-14 | CI 粒度与白名单，YAML 加载策略 | W1 第一批代码 |
| 7 | V5-15、V5-16 | 排期分项与归属，留出集 | 容量与验收口径 |
| 8 | 所有「需作者核实」 | Digital Omnibus 相关事实（OJ L 2026/01744、各生效日、Art.5(1)(ba)(bb)）、合并版法律地位、Service Desk 页可抓取性、PyYAML 对目标 CPython 的 wheel、版权/再分发结论 | 影响 KU 内容、时间线与发布 |

## 4. 我认为设计做对的 3 件事

1. **砍 determine 并把「评估」限定为原文 + `coverage_note`**：直接降低 R3，同时让 3 周范围可信；用户裁定被完整落地。
2. **`answer_id` + `skeleton` + `--host-simulate skip` 的组合**：把「宿主可能跳过校验」当作一等风险来设计，方向正确（缺的是生产侧对账，见 V5-03）。
3. **全文快照 + 两轴核验 + UNVERIFIED 如实标注**：把「可审计」从声明变成可机检的子串与定位，并诚实暴露单人核验的局限；单 locator + 7 形态全文正则也让 CK-01 可执行。
