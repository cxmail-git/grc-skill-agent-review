# v0.4 定向复核（非 CCC 正式报告）｜轮次：3

> 复核人：独立复核（非实现者）｜日期：2026-10-31｜性质：v0.4 大手术后的定向复核，**不代表 CCC 正式结论**
> 被评对象：`docs/specs/2026-10-31-grc-skill-agent-design-v0.4.md`（下称 v0.4，`L###` 为行号）
> 对照：`v0.4-decisions.md`、`ccc-findings-resolution.md`、`ccc-report.md`、`CCC-review-brief.md`、`contract-digest.md`、rev4 附件（CK-03②/DF-1~6/WS-03）、`w1-plan.md`、`w1-task-specs.md`、`ku-plan.md`、`excerpt-candidates.md`、`source-map.md`、`impact-matrix.md`、`approval-checklist.md`、`approval-packet.md`、两份样例 KU、`evidence/`
> 边界：不评法条实体内容、不写代码、不改任何被评文件；本报告为唯一新建文件。依赖原文的判断一律标「需作者核实」。

---

## 0. 总裁定

**B 有条件通过**。命中一票否决：**无**。

- 计数：**Block 3 / Major 28 / Minor 14**（逐条见 §2、§4、§5）。
- 一句话：v0.4 的四个方向（全文快照、宿主成文、砍 determine、单人 UNVERIFIED）都对，但**两个头部改动的"单一真值"没闭合**——全文快照在文档里仍有 6 处旧口径（B-01）；`validate_answer` 只验"句→claim 编号"，不验"句→claim 内容"，可被合法输入绕过（B-02），而"宿主跳过校验"既不可检测也没有指标（B-03）。
- 范围判断：D3 的删除**没有破坏 G1/G2/G4/G5**（G3 已显式推迟），52 KU / 20 金标 / 5 负例 / 只读 MCP 仍在；但 13 条"v0.4 可改"里**0 条完整关闭、8 条未修**（§3.6），且计数/版本/附件出现新的漂移（§4 M-08/M-11/M-17/M-18/M-28）。
- 降级触发器：若作者以"文字声明"替代 B-02 的机械判据（例如再加一句"宿主必须复述 claim"而不改校验项/错误码），本裁定应降为 **C 不通过**。

---

## 1. 复核方法（自跑，不复用作者证据）

1. 全文 grep + 逐节编号核对：`determine|determination|applies_from|rules/|profiles|verdict|五态|groups|coverage_note`。
2. 自算计数：§3.1 分项和、附录 B 分项和、金标行数（=20）、`Art.5` 库内项数（ku-plan 7）。
3. 逐条比对 rev4 定义：CK-03② 原文只约束"命名章节式 locator"，v0.4 扩到全部 locator（`L266`）但未改判据；DF-1~6 定义见附件 §3.7。
4. 读取 `evidence/v0.4-design-check.txt`（49 PASS）并**反查它为什么没发现残留**（→ M-27）。
5. 读 `excerpt-candidates.md` 前 10 行并与 ku-plan 的 locator/标题对齐（→ M-15）。
6. 边界内不做：不核 Art.113 日期、不核 EUR-Lex 抓取、不核 DSH skill 格式（均标需核实）。

**方法结论（先给）**：`evidence/` 的 49 PASS 是"子串存在性 + 正则"断言，不是一致性证明；本报告因此不复用它作为"v0.4 自洽"的证据。

---

## 2. Block（3 条）

### B-01 全文快照的"单一真值"在文档内不成立：6 处旧口径 vs 2 处新口径

| 位置 | 引文 | 与 D1 的关系 |
|---|---|---|
| §0 `L25` | 「**快照只存摘录 + 链接**：不重分发全文；CK-03 改为四态」 | 直接否定 D1 |
| §1.3 `L52` | 非目标含「对来源全文的再分发」 | 与"存全文"字面冲突 |
| §5.2 C1 `L216` | 「快照只存**摘录片段**；**snapshot 是该 KU 核验元数据的唯一真值**」 | C1 行本身未改 |
| §4.1 `L127` | 「摘录快照 `snapshots/<id>.md`（摘录 + 原文链接 + `accessed_at` + `excerpt_hash`）」 | 架构图仍是摘录 |
| §5.4 registry 注 `L316` | 「verification / page_digest / verified_by 只在 `snapshots/<ku_id>.md`」 | 逐 KU 文件，与"每来源一份"冲突 |
| §5.3 `L239` | 「**每来源一份全文快照**（Tier A primary）；KU 的 `verbatim_excerpt` 必须是全文的连续子串」 | 新口径 |
| §5.4 `L287` | `snapshots/<source_id>.md  # Tier A 官方全文（唯一真值）` | 新口径 |
| §11 R7 `L629` | 「只存摘录 + 链接；署名；不内置付费标准全文」 | 风险对策仍是旧口径 |

**判据**：W1 的 `ingest → validate → publish` 与 CK-03 只能实现一套。现在 C1（摘录）/§5.3（全文）/registry 注（逐 KU）/C1 的元数据清单（含 `excerpt_hash`，全文里却叫 `fulltext_sha256`）四套并存；`verify-source` 写哪个文件、`page_digest` 对哪个字节取哈希，均无定义（并入 M-07）。
**修法**：删/改上述 6 处旧口径；把"snapshot=每来源全文"写成唯一口径；`C1` 元数据清单拆成"来源级（snapshot 头）/ KU 级（verification.yaml）"两张表；registry 注改 `snapshots/<source_id>.md`。

### B-02 `validate_answer` 的校验项不足以守住 citation：主语是"claim 编号存在"，不是"句子内容有据"

**位置与引文**：§7.4 `L458` 五项为「① 每个非 frame 句有 `claim_ids` 且 claim 存在；② claim 绑定可复核；③ 句中出现 DF-1/2/4/6 形态但无绑定 → 失败；④ 译文句 `claim_ids` 与原句一致；⑤ `citations` 与 claims 的 ku_id 集合一致」；§7.2 `L424` 却写「不存在"不校验 prose"的例外」、`L426`「prose 不引入新事实：`sentences[].text` 只能复述所绑 claim 的内容」。
**绕过（最短路径）**：宿主对 `c1`（Art.16 义务）输出句子「高风险系统的提供者须在 2027-12-02 前完成第三方合格评定，并保存日志三年。」并给 `claim_ids:["c1"]`。① claim 存在 → 过；② claim 自身可复核 → 过；③ DF-1 日期"有绑定"→ 按字面不失败；④⑤ 无关 → 过。**结果 `ok:true`，但句中"2027-12-02""第三方""三年"均不在 claim 文本内**——这正是 C5/N-01 要治的"prose 夹带"。
**同类缺口**：`skeleton` 只是 `["c1","c2"]`（`L446`）加一句自由文本 `host_contract`，未定义"必须覆盖/顺序/可省略"；宿主可只答 `c1` 而把 `mode:"answer"` 原样展示，`validate_answer` 不重算 mode；`coverage_note`/`as_of`/`disclaimer`/`second_review`/`count_from_ku` 五项硬规则（§7.2-7/9）都不在校验项内，`COUNT_MISMATCH` 也不在错误码表（`L172`）。
**判据**：D2 的目标是"校验入口能守住 citation"。现状是"守住 claim 登记"，不是"守住答案句"；§7.3 `L437` 的 sentence_map 承诺（"句子不含未绑定的事实形态"）与 §7.4 的窄化实现（DF 子集）互相矛盾。
**修法**：至少补 6 项可执行判据——(a) 每句文本的"事实片段集合" ⊆ 所绑 claim 的 `text`/`verbatim` 片段（或要求句文本是 claim.text 的释义且 token 级差集为空）；(b) 全 6 类 DF + DF-4c 扫描（不止 1/2/4/6）；(c) `skeleton` 覆盖与 mode 重算（缺 claim → 自动降 partial/refuse）；(d) `coverage_note`/`as_of`/`disclaimer`/UNVERIFIED 存在性；(e) `count_from_ku` 复算（`COUNT_MISMATCH`）；(f) citation 的 `verbatim`/`locator`/`anchor` 对快照复核（引用 CK-03）。

### B-03 "宿主跳过校验"不可检测，eval 与指标均无落点

**位置与引文**：§7.4 `L460`「skill/AGENTS.md 必须把"调用 `validate_answer` 后才展示"写成硬步骤；eval 增"宿主合规"用例（模拟跳过校验 → 必须被 eval 判失败）」；§10 `L612` W2 判据「宿主合规用例通过」；但 §9.2 指标表（`L582-596`）无此指标，§5.4 的 `eval/`（`L298`）只有 golden/adversarial/determination/run.py，无宿主模拟器；§3.1 只把它列为"评估"内容（`L105`）。
**判据**：`grc eval` 跑的是 core 输出；"跳过校验"发生在仓库外（宿主会话里），没有 transcript/canary 定义就无法模拟，更无法判失败。反过来，§9.2 的「citation 覆盖 claims 100%」（`L587`）是在 `ask` 输出上算的——即使宿主展示时删掉全部 citation，门禁仍 100%。这与 G2 的"20 金标 citation 覆盖 100%"不是同一个对象。
**旁证**：`approval-packet.md` R12 自认「`validate_answer` 只能校验"句→claim"映射；宿主若跳过校验，citation 保证失效（eval 会模拟并判失败）」——即"保证失效"已承认，而"eval 会模拟"没有契约。
**修法**：定义可执行的宿主合规判据（三选一或组合）：MCP 侧对每次 `ask` 注入 `answer_token`，`validate_answer` 必须回传同一 token 才签发"可展示凭证"；或 skill 契约要求把 `ask`→`validate_answer`→展示的调用序列写 session log，eval 读 log 判定；或明确删除"citation 100% 由宿主保证"的承诺，改称"claim 覆盖 100%"，并把 citation 责任限定在 core 输出。

---

## 3. 重点核查（按任务 7 项）

### 3.1 determine 移除是否彻底 —— **不彻底（4 类残留）**

- **彻底的部分（确认）**：G3 `L46` 明确"不进入 3 周 MVP"；工具表 `L168-173` 六工具无 `determine`；组件表 `L154` 划删除线；W2 `L612` 无 determine；金标无判定用例；风险 R3 `L625` 已改写。
- **残留 A（用户可见承诺）**：§2.1 `L72` 「产品/工程 … ✅ 画像 → 适用性五态」、`L71` 「✅ 义务清单 + 原文 + 适用性」；§2.2 `L80` 场景 3「适用范围（某类系统/用途是否落入某条款）」列为 MVP 覆盖；§2.3 `L90` 演示问句 #4 期望「应给"信息不足/需按画像细分"」。而 `ask` 入参无 `profile`（§4.2.1 `L171`），§8.4 `L568` 又禁止输出适用/不适用结论 → 三处承诺无实现路径。→ **M-01**
- **残留 B（目录/技能）**：§5.4 `L283` `references/{answer-contract,determination,ingest}.md`、`L298` `eval/determination.yaml`；同时**缺** `references/validate-answer.md` 与 `binder.py`（§4.2 `L153` 有 binder 组件）。→ **M-02**
- **残留 C（CI/演示载体）**：§6.2 `L346` `changed_files: [rules/applicability-eu.yaml]`、`L361` 反向探针"只改 rules/…"；§6.3 `L369` 「见规则级 `applies_from`」；但 `rules/` 已推迟（`L297`）。→ **M-03**
- **残留 D（附录/风险/计数）**：附录 C `L697` 仍写"rules/profiles 随 determine 推迟"（这行本身对），但 `L698` 冲突处理、`L695` CK-03 四态均未跟；R8 `L630` "规则与 KU 双轨"在无 rules 的 MVP 悬空；`grc signoff`（CK-15）不在 CLI 列表。→ M-11/m-07/M-05。
- **backlog 表述**：**不清楚**。`L4/§8-490` 说"v0.2 产品版本 backlog"，但设计本身已到 v0.4，"v0.2"指设计版本还是产品版本无定义；C3/C6 只说"backlog"，无 backlog 清单文件、无条目 id、无验收（§8.1–8.4 哪些随 determine、哪些留 MVP 未逐条标注）。→ **M-25 的一部分**（并入 F-18 未修）。

### 3.2 全文快照：CK-03 可执行性 / 单一真值 / UNVERIFIED / 版权

- **CK-03①（excerpt ⊂ fulltext）**：**可执行，但只证明内部一致**。全文是作者手工落盘的 markdown（`L287`），`fulltext_sha256` 是"对存下来的官方全文取哈希"（`L248`）——不是对上游的锚定；没有官方 checksum/ELI 版本号强校验（`version: 02024R1689-20260727` 只是注释"作者核实"，`L246`）。F-01 的"自说自话"从"KU 镜像摘录"降级为"KU 镜像全文"，**未闭环**。
- **CK-03②（locator/anchor 可定位）**：**对款/项不可执行**。`L266` 要求"locator/anchor 必须在全文里能定位到章节标题"，但 ku-plan 24/32 条 EU 是 `Art.5(1)(ba)`、`Art.26(2)`、`Annex III point 1` 级，全文只有 Article/Annex 级标题；rev4 CK-03② 原本只约束"命名章节式 locator"（附件 §8.1），v0.4 扩大了适用范围却没给新判据。**且示例自身违规**：`L255` `snapshot_ref: "snapshots/reg-eu-ai-act.md#Art.14(1)"` 的锚点含 `.` `(` `)`，与 `L235` `anchor` 正则 `^[a-zA-Z0-9_-]+$` 冲突；锚点由谁写入全文也未定义（写入即改动"官方全文"）。→ **M-06**
- **CK-03③（page_digest）**：`page_digest` 对何字节取哈希（HTML/正文/快照文件）、manual 模式下如何获得（EUR-Lex 脚本抓取被拒，source-map §6）、"最近抓取"的时间基准均未写 → 无法复算。→ **M-07**
- **CK-03④（offline 仅 draft）**：可执行，但 `offline` 在 MVP 无来源使用（EUR-Lex 走 manual、CN 可 online），四态中两态是"未用但必须实现"，属设计噪声（Minor，不单列）。
- **单一真值闭合**：**否**。C1 `L216`（snapshot 是 KU 核验元数据唯一真值）与 §5.3 `L239`（每 KU 核验记在 `verification.yaml`）、`L316`（只在 `snapshots/<ku_id>.md`）三处互斥；`excerpt_hash` 是幽灵字段（C1/§4.1/§6.1 有，§5.3 无）；`fulltext_sha256` 无 CK 消费；`page_digest` 无定义。→ **B-01 + M-05 + M-07**
- **UNVERIFIED 发布/答案路径**：**不明确**。`L272` 说"发布时标 UNVERIFIED，答案带警告"，但 §7.1 输出对象无 `unverified`/`second_review` 字段，`disclaimer` 是固定文本；`freshness` 出参（`L173`）无未核验列表；页面侧 front-matter 8 键闭合，无状态行槽位；§9.2 无占比指标（R11 `L633` 却承诺"grc eval 统计 UNVERIFIED 占比"）。→ **M-04**
- **版权/许可**：**不够**。只有 `license_note` 一句（`L249`）+ R7 的旧口径（`L629`，与全文快照矛盾）；registry 条目（`L305-316`）无 license/permitted_use 字段；§1.3 仍把"对来源全文的再分发"列为非目标；未写"官方文本非官方整合版/不得视为法律意见/第三方主张的移除流程"。EU 法律文本的再利用条件（Decision 2011/833/EU 一类）与 CN 官方文件例外均**需作者/法务核实**，本报告不替作者下结论。→ B-01 + 条件 C1。

### 3.3 宿主成文 + `validate_answer`

- **ask 返回 skeleton**：**仅名义定义**。`L446` `{"skeleton":["c1","c2"], "host_contract":"compose sentences from claims; call validate_answer; do not add facts"}`——无字段语义（是否必须全覆盖、能否省略、顺序是否约束、与 `mode` 的关系）、无机器可读约束，`host_contract` 是自由文本。→ B-02。
- **校验项是否守住 citation**：**否**，见 B-02。特别是"句内容"完全不校验；`coverage_note`（D5 对 #8/#14/#16 的硬要求）不在校验项内。
- **宿主跳过校验的风险是否被 eval 覆盖**：**名义上覆盖，机制未定义**。→ B-03。
- **skill 契约是否写了"必须调用"**：**只写了一句要求，没有 skill 契约**。§7.4 `L460` 说"skill/AGENTS.md 必须…写成硬步骤"，但 §5.4 `L283` 的 skill 文件清单没有 `references/validate-answer.md`，`SKILL.md` 应包含哪些硬步骤、失败时如何拒绝展示、如何记录调用，均未写；§4.3 只说"3 问 + validate_answer 1 例"。→ M-02/B-03。

### 3.4 PyYAML

- **依赖声明与"离线可跑"**：v0.4 **删掉了"离线可跑"承诺**（v0.3 `L159` 有，v0.4 `L160` 无），改为"唯一第三方运行时依赖 `PyYAML==6.0.2`（pin）" → 字面上**一致**，且全文无"零依赖/零第三方"残留（已 grep 确认 v0.4 为 0；`CCC-review-brief.md` D2 `L51` 仍按"零第三方"提问，属协议文档 stale，见 M-28）。
- **但安装路径缺失**：`skills/grc-agent` 以复制 SKILL.md + MCP 配置安装（§4.3 `L186-187`），没有"Python 环境 + PyYAML 如何就位"的步骤；D4 写了"（或 vendored）"（`v0.4-decisions.md` D4），v0.4 正文只 pin、未选 vendored，离网/受限网络安装不可复现。→ **Minor m-12**（不 Block：MVP 内可预装）。
- **解析风险已解决**：pin 6.0.2 覆盖 YAML 1.1 的 `no/on`、日期类型化、全角冒号问题；`verbatim_excerpt` 用 YAML 块标量即可逐字保真（需在 schema 明确块标量，未写 → 并入 m-12）。

### 3.5 用词"评估"

- **已一致**：§0 `L23`「只做"评估"不做"判定"」、§7 `L377`、§8 `L491`、R3 `L625`；§8 标题改"适用性评估"、§8.2 免责"本评估"（`L536`）。
- **残留（用户可见）**：§2.1 `L71-72` 仍承诺"适用性/适用性五态"；§2.2 `L80` 仍列"适用范围"场景；§2.3 `L90` 仍要"信息不足/画像细分"；§9.1 `L576` 「五态」；skill 引用文件仍叫 `determination.md`（`L283`），eval 仍叫 `determination.yaml`（`L298`）。→ **M-01 + M-02 + M-10**。
- **可接受的内部用法**：`L4` "判定用例"、`L199` P-3"判定主体"、`L648` 评审"判定"——属内部/评审术语，不建议强制替换，但 backlog 条目名建议改"评估用例"以与用户口径一致（Minor m-13）。

### 3.6 CCC v0.1 报告"v0.4 可改"的 13 条逐条核对

> 计数先纠：处置表标题写"**12**"，实际列 **13** 个 F 编号 + "用户补充"（14 行）；本报告按任务给出的 13 条核对。这是 F-18 同类问题（P-1），记为 m-14。

| # | v0.4 落点 | 状态 | 残留（本报告编号） |
|---|---|---|---|
| F-03 ask 执行点 | §7.4 `L442-460` | **部分** | 有执行点与校验入口，缺"成立"判据、skeleton 覆盖、句内容校验（B-02） |
| F-09 跨语言检索/链式 KU/no_ku 阈值 | §4.2.1 `L168`、§9.1 `L579` | **未修** | `top_k=5` 未改；无 no_ku 阈值、无别名 lint、无主题链；#1 需 9 KU（M-24） |
| F-10 拒答分类重叠 | §7.1 `L384-385/415` | **部分** | `partial_reason` 子码已拆；但 #4 GPAI 有 `scope_exclusions` 条目却期望 `no_ku`（应为 absence/out_of_scope）；`not_legal_advice` 无关键词规则（并入 M-24/M-26） |
| F-11 算子不足 | §8.3 `L546-561` | **未修** | 仍 `intersects/eq/in`；无 any/all/not、无 `field_ref`、§8.1 无 CN 画像字段（随 backlog，但 backlog 未登记该缺口） |
| F-12 冲突定义/priority 平局 | §8.3 `L561`、§7.2 `L428` | **部分** | 平局→insufficient 已写；"冲突仅同 KU 反结论"未写死，`conflict` vs `conflict_unresolved` 无定义 |
| F-13 规则 YAML 承载法律事实/ku_hash | §8.3 `L544-559` | **未修** | 规则无 `{ku_id, field, ku_hash}`，无字面量 lint（仅 catalog 的 `NON_KU_FACT`） |
| F-16 expected_facts/6 类用例/--now | §9.1 `L576`、§9.2 | **未修** | 无 `expected_facts`、无提示注入/多轮/改写/expired/vendor 用例；`--now` 只在 R1 `L623` 出现且未定义（M-23） |
| F-18 P-1~P-7 映射/数字生成 | §5.1 `L199`、§10 `L615` | **未修** | 仍只 P-1~P-5；无 P-n→步骤/人/错误码表；数字手写；GPAI `Art.53–55`（L54）vs `Art.51–56`（L476）（M-25） |
| F-19 N-11 修法 | §11 R6 `L628`、w1-task-specs W1-1b | **部分** | 只写"2 子项 + 2 错误码 + 1 反例"，未给子项名/错误码名；落点有（CK-11/CK-09） |
| F-20 元数据落点/两轴 | §5.2 C1 `L216`、§5.3 | **未修** | 三处真值并存；`expired` 仍混在 `verification` 四态；`verified_by` 实名（M-21）；C1 元数据清单与示例不一致（M-05） |
| F-21 EU 上游检测/primary 依据 | registry `L305-316`、R1 | **部分** | source-map 有 OJ L 2026/01744，但 registry 条目无修订法令/OJ 字段、无 primary 依据说明；周检降级只写在 R1 |
| F-22 样例 status/双日期 | `sample-kus/*.yaml` | **未修** | 样例仍 `status: draft` / `effective_date: 2027-12-02` / `transition_note: null`；单值 `effective_date` 无法表达 Annex I/III 双日期（M-13） |
| F-23 页面语言/DF 规则语言 | §3.3 `L113-115` | **未修** | 只规定答案语言；页面/KU 叙述语言、DF-5/WS 按语言适用与否未写 |
| 用户补充"评估" | §7 `L377`、§8 `L491` | **部分** | 答案/§8 已改；§2.1/§2.2/§9.1/determination 命名残留（§3.5） |

**小计**：完整关闭 0；部分 6（F-03/F-10/F-12/F-19/F-21/用户补充）；未修 8（F-09/F-11/F-13/F-16/F-18/F-20/F-22/F-23）。**处置表的"v0.4 可改 12 条"没有一条被验证关闭**，与 `approval-packet.md` §4"12 条 v0.4 已改"的表述不符（m-14）。

### 3.7 新手术引入的新问题（金标 / coverage_note / W1）

**金标期望是否还成立**：

| # | v0.4 期望（附录 A） | 删 determine 后 | 判据缺陷 |
|---|---|---|---|
| 8 | `answer`；Art.2（`L666`） | **可成立**（Art.2 原文可回放） | 期望无 `coverage_note`；宿主可把它写成"适用/不适用"结论而 `validate_answer` 不拦（M-26） |
| 14 | `answer`（Art.2 原文：内部研发/使用不适用）+ `coverage_note`（`L672`） | **可成立**（v0.4 已按 N-03 改写，不再依赖 profile） | §2.3 `L90` 同一问句仍要"信息不足/画像细分"，两处冲突（M-01）；"引原文"与"下结论"无词表区分 |
| 16 | `answer`；Art.2 + Art.20（`L674`） | **可成立** | 同 #8，缺 `coverage_note` 断言与 forbidden_terms |
| 19 | `partial(cross_jurisdiction)`：`groups` 两组分别绑定（`L677`） | **不成立** | §7.1 输出对象无 `groups`（v0.2 `L353` 曾有，v0.3 起删除，v0.4 未恢复）→ 20 金标只能验收 19/20（M-09） |
| 7 | `answer`；Art.113 + `basis_ku`（`L665`） | 可成立 | `basis_ku` 是 determine 术语，答案契约无此字段（并入 m-03） |
| 3 | `partial(coverage_gap)`：7 项 + 其余 3 项（`L661`） | 可成立（`coverage_note` 字段在 `L413`） | §3.1 `L101` 仍写"Art.5 选 5 项"，与 #3、附录 B、§7.1 示例（"7 项"）三处冲突（M-08） |

**`coverage_note` 是否有字段**：**有，但只到"输出字段"，没到"验收字段"**。§7.1 `L413` 有示例值、§7.2-7 `L429` 规定 `coverage_gap`/`no_rule_matched` 必填；但 §9.1 金标 schema（`L576`）无 `expected_coverage_note`，§7.4 校验项（`L458`）不查，D5 对 #8/#14/#16 的要求因此不可机检 → **M-26**。

**W1 计划是否与 v0.4 一致**：**不一致（三份文档三方）**。`w1-plan.md` 仍是 v0.2 基线：前置"设计 v0.2"（L3）、"CK-03 四态"（§2-2）、文件清单缺 `verification.yaml`/`scope_exclusions.yaml`/`validate_answer.py`、W1-9 把 5 负例放 W1；`w1-task-specs.md` 已升级（含 validate_answer、`verification.yaml`、UNVERIFIED），但把 5 负例 + 宿主合规提前到 W1；§10 `L611-612` 的 W1 只 10 金标、负例与宿主合规在 W2。→ **M-17**。

---

## 4. Major（28 条）

| # | 位置 | 问题与判据 | 修法 |
|---|---|---|---|
| M-01 | §2.1 `L71-72`、§2.2 `L80`、§2.3 `L90` | 仍承诺"适用性/五态/画像细分"，但 `ask` 无 profile、§8.4 禁结论 → 用户可见承诺无实现路径，且与 D3 冲突 | 改为"按 KU 原文说明范围 + coverage_note"；#4 演示期望改 `answer(Art.2)` |
| M-02 | §5.4 `L283`、`L298`；§4.2 `L153` | 树里仍有 `determination.md`、`eval/determination.yaml`；缺 `references/validate-answer.md`、缺 `binder.py`；与 §4.2 组件表不一致 | 删 determination、补两文件；eval 目录与 §9.2 脚本一致 |
| M-03 | §6.2 `L346`、`L361`；§6.3 `L369`；§5.4 `L297` | CI 示例、反向探针、G5 演示第 4 步全依赖已推迟的 `rules/` → G1/G5/P-4 演示无载体 | 换成 MVP 真实依赖链（如 `kb/ku → pages → eval/golden`），探针改"改 KU 不改 golden 必须 FAIL" |
| M-04 | §5.3 `L272`、§7.1 `L382-418`、§9.2、R11 `L633` | UNVERIFIED 无答案字段、无页面状态行槽位（front-matter 8 键闭合）、无 eval 占比 → D5 降级不可见，等于静默发布 | answer 增 verification 块 + 警告；WS-06 状态行扩展；§9.2 增占比阈值 |
| M-05 | §5.3 `L252-262`、C1 `L216`、CK-15 `L486`、§3.1 `L102` | `verification.yaml` 无闭合 schema；C1 清单含 `verification_source`/`excerpt_hash`，示例两者皆无；CK-15 要求 `grc signoff`，CLI 无此命令；`manual` ↔ `manual-signoff` 映射未写 | 给字段表 + 状态映射 + CLI 命令；示例补齐 |
| M-06 | §5.3 `L266`、`L255`、§5.2 `L235` | CK-03② 对 24/32 款/项级 locator 无判据（全文只有 Article 级标题）；示例锚点 `#Art.14(1)` 违反自身 anchor 正则；锚点写入方式未定义 | 定义"父条款标题 + 子项偏移"锚点；示例改 `#art14-1`；写明锚点由 ingest 生成、不改动官方正文 |
| M-07 | `L248`、`L216`、`L261`、`L267`、`L273` | `fulltext_sha256` 无 CK 消费；`excerpt_hash` 幽灵字段；`page_digest` 未定义取哈希对象/manual 获取方式；`max_age_days` 无取值 | 单一哈希口径 + 字段来源 + 默认值 + CK 断言 |
| M-08 | §3.1 `L101` vs 附录 B `L684`、§7.1 `L413` | 分项和 = 30 却标 32；同页三处写"7 项"；N-07（v0.2 预演）已点名同一处 | §3.1 改 7；计数由 `gen_numbers.py` 生成 |
| M-09 | 附录 A `L677`、§7.1 `L382-418` | `groups` 无字段 → #19 无法表达，20 金标不可全验 | 恢复 `groups:[{label,claim_ids}]` 或改写 #19 期望 |
| M-10 | §9.1 `L576` vs §7.1 `L383` | `expected_mode` 五态 vs 答案 mode 三值；五态是 determine verdict，D3 已推迟 → 脚本无法校验单值 | 改三值 + `partial_reason`/`refusal.reason` 单值 |
| M-11 | 附录 C `L694-698` | 快照/CK-03/冲突三行仍是 v0.1–v0.3 口径（"摘录+链接""四态"），与 D1/CK-03 四项冲突 | 按 v0.4 重写差异表 |
| M-12 | §9.2 `L592`、§7.3 `L435` | "稳定性 = 同题两次 claim 三元组集合相同"，但 `--llm` 下意图解析由 LLM 做，claim 集合会随解析变化 → 该指标在 LLM 轨必然抖动；F-16 建议的"限定 ku_id 集合 + mode 一致"未采纳 | 分轨定义：`--no-llm` 用三元组，`--llm` 用 ku_id 集合 + mode；或删 `--llm` 稳定性门禁 |
| M-13 | `sample-kus/gsk-eu-art14.yaml`、`gsk-cn-genai-art7.yaml` | 未按 F-22 更新；`snapshot_ref` 是逐 KU 文件（`snapshots/gsk-eu-art14.md#p1`）与每来源全文冲突；art14 locator `Art.14(1)` 与 ku-plan `Art.14` 不一致 | 重填样例 + 统一 snapshot_ref/locator；样例是 W1 模板，错误会传导 52 条 |
| M-14 | `ku-plan.md` 第 27 行、门禁行、第 22 行 | `gsk-eu-art26-5` 配 `Art.26(6)`；"Tier A 双人核"与 D5 单人冲突；art14 id/locator 与样例冲突；evidence 只验正则不验 id↔locator | 脚本生成 id=locator 归一表；删"双人核" |
| M-15 | `excerpt-candidates.md` 第 7–13 行 | 7 条 Art.5 候选文本与 locator 系统性错位（art5-d 行是 "(c) social scoring"、art5-g 行是 "(d) criminal offence"、art5-ba 行是 "(b) vulnerabilities"）；CK-03 只验子串 → 静默错标 | 重生成 + 断言"候选首句含 locator 子项号"；W1 重抄前先过对齐检查 |
| M-16 | `source-map.md` §5、§4 | #3 期望 answer（设计 partial）、#9/#17 双值（设计单值）、标识办法 8 条 vs 附录 B 7 条；header 仍"为设计 v0.1/50 KU" | 同步或首行标"以设计为准" |
| M-17 | `w1-plan.md`、`w1-task-specs.md`、§10 `L611-612` | 前置"设计 v0.2"、CK-03 四态、文件清单缺三件；两份 W1 文档与 §10 的 5 负例/宿主合规归属不一致 | 以 w1-task-specs 为唯一基线，回写 §10 |
| M-18 | `approval-checklist.md` §3/§5/§6 | 仍测"CK-03 五态""摘录快照""只存摘录""applies_from 规则级""1 人则 determine 移 v0.4"；§13-4 要求用户按此批准 | 重写至 v0.4（全文快照/UNVERIFIED/validate_answer/backlog） |
| M-19 | §9.2 `L582-596`、§7.4 `L460`、§10 `L612` | "宿主合规"有承诺无指标；UNVERIFIED 占比有承诺无指标；`grc freshness --stats` 未在工具/CLI 契约 | 增两行指标；定义 `--stats` 或改指标计算方式 |
| M-20 | §7.2 `L429` vs §7.1 `L382-418`；§7.4 `L458` | 硬规则要求 `as_of`，答案对象无此字段；`coverage_note`/`disclaimer` 不在校验项 | 增 `as_of` 或改指 `freshness.oldest_verified_at`；validate_answer 增 meta 检查 |
| M-21 | §7.1 `L411`、§8.2 `L531/L535` vs §5.3 `L258` | `verified_by` 仍写"R-2 / 张三"实名，违反 F-20 与"角色码，不写实名" | 全部改 `R-*`；样例去实名 |
| M-22 | §7.4 `L458`③ vs §7.2 `L423`、§7.3 `L437` | 三处扫描面不同（DF-1/2/4/6 vs DF-1~6 vs 全部事实形态）；DF-3/DF-5 可绕过 | 统一 DF-1~6 + DF-4c；定义"有绑定"的判据 |
| M-23 | §9.1 `L576`、§9.2、R1 `L623` | F-16 未修：无 `expected_facts`、无 6 类用例、`--now` 未定义 | golden 增 `expected_facts`（非规则作者写）+ `eval --now` |
| M-24 | §4.2.1 `L168`、§9.1 `L579` | F-09 未修：`top_k=5` vs #1 需 9 KU；无 no_ku 阈值/别名 lint/主题链 → G2 在 #1/#3 不可达 | ask 允许链式展开；no_ku = 最低分 + 必含词；每 KU 中英别名 lint |
| M-25 | §5.1 `L199`、§10 `L615`、R2 `L624`、§1.3 `L54` vs `L476` | F-18 未修：P-6/P-7 缺；无 P-n 映射表；数字手写；GPAI 章号自相矛盾 | 补 P-6/P-7 + 映射表 + 脚本生成数字；统一 Art.51–56（需核实） |
| M-26 | D5 附带要求、§9.1 `L576`、§7.4 `L458`、§7.2 `L429` | #8/#14/#16 的 `coverage_note` 无金标字段、无校验项、非必填（三题 mode=answer）→ 用户裁定不可机检 | golden 增 `expected_coverage_note` + `forbidden_terms`（禁"适用/不适用"结论词）；validate_answer 检查 |
| M-27 | `evidence/v0.4-design-check.txt`（49 PASS）、`approval-packet.md` §1 | 自检只做子串断言："PASS design stale: 适用性五态判定"未覆盖 §2.1 `L72` 的"适用性五态"；"excerpt ids == plan ids"不验内容；"locator all match 7 forms"只验正则 → G-3 仪器污染 | 证据改为"负例必须 FAIL"的可复跑断言（残留词表、id↔locator、候选↔locator、计数分项和） |
| M-28 | `CCC-review-brief.md` L4/L13/L30/§3–§4；`reviews/round-3/REQUEST.md`；`reviews/README.md` 硬规则 2 | brief 仍"第 3 轮（v0.3）"、D1–D9/Q1–Q10 仍按 50 KU/三态/零依赖/determine 提问；无 round-4 REQUEST 绑定 v0.4 `design_sha256`/`package_sha256` → 按现协议 v0.4 的 CCC 报告会被判 `REVIEW_STALE` | 写 round-4 REQUEST（三 hash）+ 重写 brief 到 v0.4 |

---

## 5. Minor（14 条）

| # | 位置 | 问题 | 改法 |
|---|---|---|---|
| m-01 | §5.1 `L196` | 「`locator` 5 形态」与 C4 七形态（`L223-235`）冲突，继承段未更新 | 改"7 形态"并指向 C4 |
| m-02 | §5.2 C3 `L218` | 「新增 CK-14（§7.2）」实际在 §7.4.1 | 改 `§7.4.1` |
| m-03 | §7.1 `L404` | `count_from_ku.basis` 用「Art.16(a)-(l)」区间/混写，与 C4 禁区间口径冲突 | 用子项枚举或 `anchor` |
| m-04 | §7.1 `L387` | 示例句"完成合格评定"落在未收录的 Art.43（附录 B）→ 示例本身是不可绑 claim | 换成 Art.16 内的义务 |
| m-05 | §7.1 `L395/L400/L407/L411` | 示例大量"…"占位，违反 `pre-submit.md`"占位符残留 = 0" | 给真实短句或标注"示例占位" |
| m-06 | §12 `L640`、§13 `L649` | "v0.1 就加跨法域""设计升 v0.2"版本残留 | 改 v0.4/v1.0 |
| m-07 | R8 `L630` | "规则与 KU 双轨"在 MVP 无 rules，风险描述悬空 | 改"KU 与页面/金标双轨" |
| m-08 | §4.2.1 `L173` | `freshness` 出参 `verification` 单值语义不明（模式？状态？） | 改名 `verification_modes` 或给枚举 |
| m-09 | §5.4 `L281` | 树缺 `binder.py`（§4.2 `L153` 有、w1-plan 有） | 补入树 |
| m-10 | `sample-kus/*.yaml` 头注 | 仍写"v0.2 修正" | 改 v0.4 |
| m-11 | `impact-matrix.md` CI 判据 2、CH-C5 行 | 仍用 `graph_affected(ku_ids)`（§6.2 已废手写 `ku_ids`）；消费者列含"`eval/golden.yaml`（W1 建立）"违反"路径必须真实" | 同步 §6.2 判据；消费者标 pending |
| m-12 | §4.2 `L160`、§4.3 `L186-187` | PyYAML 安装路径未写（复制 skill 时 Python 环境如何就位）；`verbatim_excerpt` 未要求块标量 | 增安装前置 + schema 要求 `|` 块标量 |
| m-13 | §4 `L4`、§5.4 `L283/L298` | 内部命名"判定用例/determination"与用户口径"评估"不一致 | backlog 条目改"评估用例"，文件改名可选 |
| m-14 | `ccc-findings-resolution.md` 汇总、`approval-packet.md` §4 | 写"12 条"实列 13 个 F 编号（+用户补充 14 行） | 改为 13/14 或按脚本生成 |

---

## 6. 条件清单（B 的通过条件）

| # | 对应 | 条件 | 为什么必须在 W1-0 前 |
|---|---|---|---|
| C1 | B-01 | 统一快照口径：删 6 处"只存摘录"，C1 元数据拆两张表，registry 注改 `source_id`；补 license/permitted_use 字段与再分发声明 | 它决定 ingest/publish 的文件布局，动工后改全部返工 |
| C2 | B-02 | `validate_answer` 补 6 项（句内容、DF 全 6 类、skeleton 覆盖/mode 重算、meta 四项、count、citation 对快照），错误码同步 | 这是 D2 唯一的可信度保证 |
| C3 | B-03 | 定义"宿主合规"可执行判据（answer_token 或 session log）+ §9.2 指标；否则把"citation 100%"降级为"claim 覆盖 100%" | 否则 G2 的验收对象是 core 而非用户看到的答案 |
| C4 | M-04 | UNVERIFIED 三落点：答案字段 + 页面状态行 + eval 占比 | D5 是用户裁定，必须可见 |
| C5 | M-05/M-06/M-07 | 闭合 `verification.yaml` schema、CK-15 映射、CK-03②/anchor、三哈希与 `max_age_days` | 决定 CK-03/发布门禁能否跑 |
| C6 | M-08/M-09/M-10/M-11/m-01 | 修计数与枚举：32/7、`groups`、三值 mode、附录 C、locator 7 | 金标在 W1 末冻结 |
| C7 | M-13~M-18、M-28、m-10~m-12 | 同步下游：样例、ku-plan、excerpt-candidates、source-map、W1 计划、approval-checklist、round-4 REQUEST | 这些是 W1/批准的输入，不是"附件" |
| C8 | M-23/M-24/M-25 | F-09/F-16/F-18 要么真修，要么在 backlog 清单逐条登记（含判据与责任人） | 否则"未修"会伪装成"已推迟" |

---

## 7. 我确认做对的 3 件事

1. **D1 的方向对**：把 registry 降为来源级、把核验元数据挪出 registry，第一次让"谁是真值"成为可讨论的问题；`excerpt ⊂ fulltext` 也是 CK-03① 第一次真正可跑（虽然只到内部一致）。
2. **D2 的方向对**：把 F-03 的"执行点未定义"变成"有契约"——`ask` 返回 claims + skeleton、`validate_answer` 有独立入口、`mode` 三值 + `partial_reason`/`refusal.reason` 单值。问题在判据强度，不在架构。
3. **D3/D5 的取舍留痕**：determine 移出但保留 §8 为 backlog、G3 显式标推迟、R11 书面接受单人风险、`52 KU 不减`，没有偷偷缩小范围；这比"删掉不提"诚实。

---

## 8. 未核事项与复现清单

**需作者核实（本报告不判）**：Art.113 合并版三日期与 Digital Omnibus（OJ L 2026/01744）；GPAI 章号 Art.51–56 vs 53–55；EUR-Lex/EU 法律文本再利用许可与 CN 官方文件例外；DSH skill 加载格式；`grc verify-source` 对 CN 站点的抓取稳定性。

**复现（本次自跑）**：
1. `grep -n "判定\|摘录\|determine\|五态\|双人" docs/specs/…v0.4.md` → 得到 §2.1/§2.2/§5.1/C1/R2/R7 等残留位置。
2. 自算 §3.1：`1+5+3+4+8+1+3+1+3+1 = 30`；附录 B：`1+7+3+4+8+1+3+1+3+1 = 32`。
3. `grep -c "^| [0-9]"` → 附录 A 行数 20（金标数正确）。
4. `grep -c "^PASS" evidence/v0.4-design-check.txt` = 49，但其中无一条验"候选↔locator 对齐"或"id↔locator 归一"。
5. 对照 `excerpt-candidates.md` 第 7–13 行与 `ku-plan.md` 的 Art.5 行：7 条内容错位。
6. `grep -n "groups"`：v0.2 `L353` 有，v0.3/v0.4 仅附录 A #19 引用。

**结论**：v0.4 的骨架可以继续，但 B-01/B-02/B-03 必须在 W1-0 前关闭；C6/C7 的一致性修复可与 W1-0 并行，不修则金标冻结与用户批准都会落空。
