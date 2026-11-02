# GRC Skill Agent · 术语标准 v1.0

> 状态：**v1.0（2026-11-01）** ｜ 项目：GRC Skill Agent ｜ 适用：设计、KU、页面、答案、MCP、eval、评审文档
> **效力**：本文是 **GRC Skill Agent 的项目用词唯一规范**。设计/代码/页面/答案中的术语以本文为准；与来源文档冲突处，按本文「本项目取用」列。
> **来源整合**：
> - `AI-GRC-Consultant/00_glossary.md`（项目版本 1.0，文档修订 v3.1，2026-10-18）：各体系**原义与出处**。
> - `AI-GRC-Consultant/10_terminology_standard.md`（项目版本 1.0，r4，2026-10-18）：**项目用词规范**（key、裸词禁用、Probo/OSCAL/Nexus 分层）。
> - 本文不是上述两份文件的复制；只保留对 GRC Skill Agent 有约束力的定义、规则与映射，并新增本项目术语（KU/Scope/Claim 等）。
> **版权**：NIST/GAO/OCC/EU/中国法规为公共领域或官方文本，可引用；ISO 37301、ISO/IEC 42001、IIA 准则受版权保护，**只给条款号与准确释义，不复制原文**。

---

## 1. 范围与效力

### 1.1 本文覆盖

1. GRC 核心概念：Requirement、Compliance Obligation、Compliance、Risk、Control/Measure、Assessment、Finding、Evidence 等；
2. GRC Skill Agent 自有概念：KU、Scope Registry/Scope ID、Claim、候选句、Answer 契约、Verification、UNVERIFIED、Page、Coverage code、Clarify；
3. 同名异指与裸词禁用；
4. 与 NIST / OSCAL / Probo / Nexus / EU AI Act / 中国法规的映射；
5. 写作规则（中文、体系标注、证据等级、评估 vs 判定）。

### 1.2 本文不覆盖

- Probo 租户数据模型、OSCAL 导出模型、Nexus 知识图谱的**实现**；
- AI-GRC-Consultant 的 Advisor/判定一/二/三流水线；
- 具体法条文本（在 `docs/research/sources/` 与 `kb/ku/`）；
- 法律意见或适用性结论。

> **边界**：GRC Skill Agent 是**只读知识/问答/MCP 能力包**，不是租户 GRC 平台。本文借用 AI-GRC-Consultant 的**概念区分与用词纪律**，**不采用**其 Probo/OSCAL/Nexus 数据模型、Advisor 契约或判定流水线。

---

## 2. 五条原则

| # | 原则 | 含义 |
|---|---|---|
| P1 | **一个概念一个 key** | 每个概念有稳定 `T-…` key；key 永不改；中文名可修订。文档/代码/schema 引用 key。 |
| P2 | **裸词禁用** | `Control`/`Measure`/`Action`/`Rule`/`Obligation`/`Requirement`/`Finding`/`Risk`/`Evidence` 不得裸写；必须带体系标注或本项目限定（§6）。 |
| P3 | **体系标注** | 同名异指一律写 `Control (Probo)`、`control (OSCAL)`、`Risk (NIST AI 100-1)`、`高风险分类 (EU AI Act)` 等；不写脚注。 |
| P4 | **定义与出处绑定** | 每条术语给来源；无来源的入「本项目自定义」并标 `【本项目自定义】`；不把自造词说成外部标准。 |
| P5 | **不输出合规结论** | 本项目用「评估/参考」，不用「判定合规/违法/适用」；determine 在 backlog（D-003）。 |

**证据等级**：`【已验证】`（原始文件+条款/页码）、`【外部依据】`（二手/未取得原文）、`【推测】`、`【未找到】`、`【本项目自定义】`。

---

## 3. 概念分层（GRC Skill Agent 版）

AI-GRC-Consultant 的 L0–L4 是租户 GRC 平台分层。本项目只实现 **L0/L1 的知识侧**与 **LJ 的一部分（范围说明，不做判定）**；L2–L4 明确 out of MVP。

```
L0 法源层（本项目实现）
  Scope Registry（sc-…） + KU（30 字段） + verbatim_excerpt + locator + snapshot
        │  派生：人工核验（CK-03/14/15/16/17）
        ▼
L1 要求与义务层（本项目实现）
  KU 的 obligation / evidence_requirement / applies_to / obligation_nature
        │  只读输出：候选句 + citation
        ▼
LJ 范围说明层（本项目实现，非判定）
  Scope/时间/法域解释 + coverage_note + UNVERIFIED
        │  determine（判定）在 backlog（D-003）
        ▼
L2 实施层 / L3 评估层 / L4 风险与处置层（本项目 out of scope）
  租户 Measure/Evidence/Audit/Risk 等；仅保留术语映射，不建模
```

| 层 | 本项目 | 说明 |
|---|---|---|
| L0 法源层 | ✅ | Scope Registry + KU + 快照/核验；`T-SCOPE`、`T-KU` |
| L1 要求与义务层 | ✅ | KU 的 `obligation_nature`、`obligation[]`、`evidence_requirement[]`、`applies_to[]` |
| L2 实施层 | ❌ | 不存租户保障措施/证据；MCP 只读知识 |
| L3 评估层 | ❌ | 不做审计/满足性判定；eval 是**开发期质量评估**，不是租户审计 |
| L4 风险与处置层 | ❌ | 不做风险评分/处置 |
| LJ 判定层 | 部分 | 只做「适用范围说明」；不输出 APPLIES/NOT_APPLICABLE |

---

## 4. 核心 GRC 概念（原义 + 本项目取用）

### 4.1 规范侧

| key | 术语 | 定义（出处） | 本项目取用 |
|---|---|---|---|
| `T-REQ` | **Requirement**<br>要求 | 转述/表达需要及其约束的陈述（NIST SP 800-160v1r1，源自 ISO/IEC/IEEE 29148）；ISO 37301 3.14：已陈述/通常隐含/强制的需求或期望 | 用「要求」指**框架/标准的要求项**；不把法规本身叫 requirement |
| `T-OBL` | **Compliance Obligation**<br>合规义务 | 组织必须遵守的要求 + 自愿选择遵守的要求（ISO 37301:2021 3.25） | KU 的 `obligation` 是**法条义务内容**；不把租户登记记录叫 obligation |
| `T-COMP` | **Compliance**<br>合规 | 满足组织全部合规义务（ISO 37301 3.26） | **本项目不输出合规结论**；只引用原文/免责声明 |
| `T-NONCOMP` | **Noncompliance** | 未满足合规义务（ISO 37301 3.27） | 同上；不得由系统判定 |
| `T-CONF` | **Conformity / Nonconformity** | 满足/未满足某项要求（ISO 37301 3.15/3.16）；不符合不必然不合规 | 与「合规」区分；本项目不做 conformity assessment |
| `T-CRIT` | **Criteria**<br>判据 | 用于比较/评价绩效的法律、法规、标准、基准（GAO-21-368G） | 用于 eval 的 expected facts/criteria；不用于「判定」 |
| `T-REG` | **Regulation / Rule**<br>法规/规章 | 1 CFR §1.1：regulation 与 rule 同义；5 U.S.C. §551(4)：普遍/特定适用、未来生效的机关声明 | 本项目说「法规/法条」；不写裸 `Rule` |
| `T-APPL` | **Applicability Determination**<br>适用性判定 | EPA 程序性用法 + 三值 APPLIES/NOT_APPLICABLE/UNKNOWN（本项目扩展） | **不采用**：D-003 不做适用性判定；只做「适用范围说明」 |
| `T-GAP` | **Gap**<br>差距 | 现状与判据之间的差异（GAO-21-368G ¶8.126 概念） | 仅用于 eval/差距说明，不输出合规结论 |
| `T-GOV` | **Governance**<br>治理 | 组织风险管理战略、预期与政策的确立/传达/监控（NIST CSF 2.0 GOVERN） | 背景词；不建治理模型 |

### 4.2 风险侧

| key | 术语 | 定义 | 本项目取用 |
|---|---|---|---|
| `T-RISK` | **Risk**<br>风险 | NIST AI 100-1 §1.1：事件发生概率与后果量级的复合度量；影响可正可负（AI RMF 采用） | 用 NIST AI 100-1 定义；**不做风险评分/计算** |
| `T-CRISK` | **Compliance Risk**<br>合规风险 | 未满足合规义务的发生可能性与后果（ISO 37301 3.24） | 概念引用；不输出 |
| `T-IR` | **Inherent Risk** | 管理层未采取措施前的风险组合（IIA） | 不建模 |
| `T-RR` | **Residual Risk** | 措施后残留风险（CNSSI 4009/SP 800-30） | 不建模 |
| `T-THREAT` | **Threat** | 可能对组织产生不利影响的情形/事件（FIPS 200） | 概念引用 |
| `T-VULN` | **Vulnerability** | 可被威胁利用的弱点（FIPS 200） | 概念引用 |
| `T-IMPACT` | **Impact** | CIA 丧失对组织/个人的效应（CNSSI 4009） | 概念引用 |
| `T-LIKE` | **Likelihood** | 威胁利用脆弱性的概率（SP 800-30） | 概念引用 |
| `T-TOL` | **Risk Tolerance** | 组织可接受的风险水平（SP 800-53） | 不建模 |

### 4.3 控制侧（**本项目不建模 Control**）

| key | 术语 | 定义 | 本项目取用 |
|---|---|---|---|
| `T-CONTROL` | **Control** | 裸词禁用：NIST=保障措施；OSCAL/Probo=要求项；Nexus/ISO=风险措施；IIA=行动 | **本项目不使用裸 Control**；需要时写 `Measure (Probo)`/`control (OSCAL)`/`Control (Probo)` |
| `T-SECCTRL` | **Security Control** | 为保护 CIA 规定的保障措施/对抗措施（SP 800-53） | 不建模 |
| `T-MEASURE` | **Measure (Probo)**<br>保障措施 | Probo 的保障措施；NIST control 的落点 | 术语映射；不建模 |
| `T-COBJ` | **Control Objective** | 特定控制的目的，针对实现实体目标的风险（GAO-21-368G） | 不建模 |
| `T-CBASE` | **Control Baseline** | 为满足法律/法规/政策要求而适用的控制集合（SP 800-37） | 不建模 |
| `T-IC` | **Internal Control** | 监督机构/管理层/人员实施的过程，提供合理保证（GAO） | 不建模 |
| `T-DEF` | **Deficiency in Internal Control** | 控制设计/实施/运行不能达成控制目标（GAO ¶8.53） | 不建模 |

> **关键区分**：NIST `control` = 保障措施（L2）；Probo/OSCAL `control` = 要求项（L1）。**本项目 KU 的 `obligation` 不是 control。** 裸 `Control` 不得使用（P2）。

### 4.4 评估侧

| key | 术语 | 定义 | 本项目取用 |
|---|---|---|---|
| `T-ASSESS` | **Assessment** | 对控制的测试/评价，判断实施正确/按预期/产生预期结果（OMB A-130/SP 800-171Ar3） | 本项目 `eval` 是**开发期质量评估**，不是租户审计 |
| `T-FIND` | **Finding** | GAO：含 criteria/condition/cause/effect 的问题；OSCAL：二值；Probo：不符合项工单 | 本项目 eval 的「发现」用 GAO 四要素；不建 Probo Finding |
| `T-COND` | **Condition** | 实际存在的情形（GAO ¶8.125） | eval 用语 |
| `T-CAUSE` | **Cause** | 现状与判据差异的因素（GAO ¶8.126） | eval 用语 |
| `T-EFFECT` | **Effect** | 差异导致的结果（GAO ¶8.127） | eval 用语 |
| `T-EVID` | **Evidence** | 相信/不相信的依据；NIST 证据；Probo 收集状态 | 本项目 `evidence/` 是**验证/测试产物**，不是租户证据 |
| `T-SUFF` | **Sufficiency** | 证据数量（GAO） | 不建模 |
| `T-APPROP` | **Appropriateness** | 证据质量（GAO） | 不建模 |
| `T-ASSUR` | **Assurance** | 对 claim 已达成的合理信心依据（NIST SP 800-12r1） | 概念引用 |
| `T-AUDIT` | **Audit** | 获取证据并客观评价判据满足程度的系统独立过程（ISO 37301 3.18） | 不建模 |

### 4.5 处置侧

| key | 术语 | 定义 | 本项目取用 |
|---|---|---|---|
| `T-RESP` | **Risk Response** | 接受/规避/缓解/分担/转移（CNSSI 4009） | 不建模 |
| `T-MIT` | **Risk Mitigation** | 排序/评价/实施降险措施（SP 800-30）；Risk Response 子集 | 不建模 |
| `T-CORR` | **Corrective Action** | 消除不符合成因并防再发的行动（ISO 37301 3.17） | 不建模 |

### 4.6 AI / 法域词条

| key | 术语 | 定义 | 本项目取用 |
|---|---|---|---|
| `T-AISYS` | **AI System** | NIST AI 100-1 无定义句，采用 OECD 维度；本项目以 OECD 描述 + 法域定义 | 用「AI 系统」；不把 NIST 描述当法律定义 |
| `T-AIACTOR` | **AI Actor** | 在 AI 生命周期发挥积极作用者（NIST AI 100-1 引 OECD） | 概念引用 |
| `T-TRUST` | **Trustworthy AI 七特征** | valid/reliable、safe、secure/resilient、accountable/transparent、explainable、privacy-enhanced、fair | 概念引用 |
| `T-RMF` | **AI RMF 四功能** | GOVERN/MAP/MEASURE/MANAGE（NIST AI 100-1） | 映射 NIST AI RMF；本项目不实现 RMF |
| `T-HRAI` | **High-Risk AI System (EU AI Act)** | Art.6(1)-(3)：Annex I 安全组件/产品 + Annex III 法定分类 + 例外 | 标 `高风险分类 (EU AI Act)`；不计算 risk |
| `T-GPAI` | **General-Purpose AI Model (EU AI Act)** | Art.3(63)：显著通用性、能胜任广泛任务 | 标 `(EU AI Act)`；本库暂未收录 GPAI 章 |
| `T-CNGEN` | **生成式人工智能服务提供者** | 暂行办法第二十二条(二)：利用生成式 AI 技术提供服务（含 API）的组织/个人 | 标 `(CN 暂行办法)` |
| `T-CNSCOPE` | **生成式人工智能服务（范围）** | 向中国境内公众提供生成文本/图片/音频/视频等服务；未向境内公众提供不适用 | 标 `(CN 暂行办法)`；不输出适用性结论 |

---

## 5. 本项目自有术语（GRC Skill Agent）

> 这些词**不是** NIST/OSCAL/Probo 术语；不得声称来自外部标准。定义以本节为准。

| key | 术语 | 定义 | 落点 |
|---|---|---|---|
| `T-KU` | **KU（Knowledge Unit）** | 一条法条/条款的知识单元；30 字段 YAML；含 `ku_id`、`verbatim_excerpt`、`scope_id`、核验字段 | `kb/ku/*.yaml`、`schema.py` |
| `T-SCOPE` | **Scope** | 适用范围对象：法域/法系/地域/行业/主体/生效时间/效力状态 | `kb/scopes.yaml` |
| `T-SCOPE-ID` | **Scope ID** | 稳定标识 `sc-<jur>-<instrument>-<variant>`；每 KU 一个 | KU `scope_id`；CK-17 |
| `T-SNAPSHOT` | **Full-text snapshot** | Tier A 官方全文快照（本地；不随包）；KU excerpt 必须是其连续子串 | `kb/snapshots/` |
| `T-CLAIM` | **Claim** | KU 派生的证据单元；绑定 `ku_ids`/`locator`/`verbatim`；`binding_mode=quote\|frame` | `answer.py`/`validate_answer.py` |
| `T-SENT` | **候选句（Candidate sentence）** | core 生成的句子；带 `sid`/`claim_ids`/`required`/`order`/`verbatim` | `ask` 输出 |
| `T-ANSWER` | **Answer contract** | `answer_id + sentences + skeleton + citations + coverage_codes + scope_ids + mode` | §7.1 设计 |
| `T-FINAL` | **final_text** | 宿主所选候选句按 `\n` 逐字拼接；不得改写 | `validate_answer` |
| `T-TOKEN` | **validation_token** | 服务端 HMAC 签发；绑定 `answer_id + final_text`；用于展示对账 | `validate_answer`/`verify-answer` |
| `T-VERIFY` | **Verification** | KU 来源核验：online/manual/offline + freshness + verified_by + evidence_ref | `verification.yaml`；CK-15 |
| `T-UNVER` | **UNVERIFIED** | `second_review=false` 的核验状态；答案必须带警告 | `freshness`；D-005 |
| `T-PAGE` | **Page** | 派生 Markdown 页面（concept/entity/overview/source）；含 front-matter 8 键与 `kb:derived` 块 | `kb/pages/`；CK-06/07/09/10 |
| `T-RHASH` | **render_hash** | `ku_id|fields|template_version|body` 的 SHA256；防手改块 | `compile.py` |
| `T-KHASH` | **ku_hash** | 17+1 fact-bearing 字段 canonical JSON 的 SHA256；防 KU 改而页面不重编译 | `compile.py` |
| `T-COV` | **coverage_code / coverage_note** | 库内缺口码（如 `sx-eu-art43`）与 core 生成的说明；不改变 mode | `ask`；§7.4 |
| `T-CLARIFY` | **Clarify** | 法域/框架/Scope 不确定时的结构化询问；多选；带 `clarify_id`/options/scope_id | `clarify.py`；MCP |
| `T-MCP` | **MCP tool** | 只读工具：`search_kus/get_ku/get_page/ask/validate_answer/freshness` + `resolve_clarify` | `mcp.py`/`mcp_server.py` |
| `T-EVAL` | **Eval** | 开发期质量门禁（金标/负例/宿主合规/impact）；不是租户审计 | `eval/`、`grc eval` |

### 5.1 近义词/禁用写法

| 不写 | 写 | 原因 |
|---|---|---|
| 判定合规/不适用 | 评估/范围说明；`out_of_scope` | D-003/D-006；不输出法律结论 |
| 合规结论 | 原文引用 + 免责声明 + `coverage_note` | 同上 |
| Control / control（裸） | `Measure (Probo)` / `control (OSCAL)` / `Control (Probo)` / `Control (Nexus)` | 同名异指（§6） |
| Scope | `Scope (GRC Skill Agent)` 或 `Scope ID` | 与 `scope_in/out` 字段、法律 scope 区分 |
| 法条 = requirement | 法规/法条; `Requirement` 仅指要求项 | 法规≠要求（§4.1） |
| 风险分类 = risk 计算 | `高风险分类 (EU AI Act)` | 法定判据，不是概率×严重度 |
| 证据 = 证明成立 | `Evidence`（依据） vs `Evidence (Probo)`（收集状态） | 同名异指 |

---

## 6. 裸词禁用与同名异指

### 6.1 禁用表（沿用 10 §3，适配本项目）

| 裸词 | 禁用原因 | 本项目写法 |
|---|---|---|
| Control | NIST 保障措施 / OSCAL/Probo 要求项 / Nexus/ISO 风险措施 / IIA 行动 | `Measure (Probo)`（保障措施）、`control (OSCAL)`/`Control (Probo)`（要求项） |
| Measure | Probo 保障措施；Nexus 描述句 | `Measure (Probo)` |
| Action | Nexus 缓解条目 vs 租户工作项 | `Action (Nexus)` / `Task (Probo)` |
| Rule | 1 CFR 与 regulation 同义；NISTIR 7275 机器检查元素；Nexus 道义规则；Cedar 策略 | 法规→「法规」；`Rule (Nexus)`；`策略 (Cedar)` |
| Obligation | Nexus 道义模态 vs Probo 登记记录 | `Obligation (Nexus)` / `Obligation (Probo)` |
| Requirement | FIPS 200 派生要求 / Nexus 法条载体 / Probo 文本列 | `Requirement (Nexus)` / `Control (Probo)` / 「要求」 |
| Finding | OSCAL 结论 / Probo 不符合项 / GAO 四要素 | `finding (OSCAL)` / `Finding (Probo)` / 「发现」 |
| Risk | NIST 两版 / Probo / EU Art.3(2) / OSCAL | `Risk (NIST AI 100-1)` 等 |
| Evidence | Probo 收集状态 / NIST 依据 | `Evidence (Probo)` / `Evidence` |

### 6.2 本项目新增同名区分

| 词 | 区分 |
|---|---|
| Scope | `Scope (GRC Skill Agent)`（适用范围对象） vs KU 字段 `scope_in/scope_out`（法条内含/排除） |
| Verification | `Verification`（KU 来源核验） vs `validate_answer`（答案校验） vs `Eval`（开发期评估） |
| Assessment | `Assessment (NIST/OMB)`（控制评估） vs `Eval`（本项目质量评估） vs `评估`（日常用语） |
| Clause | 法条条款文本 vs `claim`（证据单元）；不混用 |

---

## 7. 外部体系映射（本项目的对照）

| 本项目 | NIST | OSCAL | Probo | Nexus | 备注 |
|---|---|---|---|---|---|
| KU（法条单元） | — | — | — | `Requirement (Nexus)`（借结构） | 不借语义 |
| Scope ID | — | — | — | — | 本项目自造（D-015） |
| 义务内容 | FIPS 200 requirement | `control`（要求项） | `Control (Probo)` | `ControlActivity* (Nexus)` | 裸词禁用 |
| 保障措施 | security control | `implemented-requirement` | `Measure (Probo)` | `RiskControl (Nexus)` | 本项目不建模 |
| 证据 | Evidence | `relevant-evidence` | `Evidence (Probo)`（收集状态） | — | 本项目 `evidence/` 是测试产物 |
| 发现 | GAO Finding | `finding (OSCAL)`（二值） | `Finding (Probo)`（工单） | — | 不互换 |
| 风险 | Risk (NIST AI 100-1) | `risk` | `Risk (Probo)` | `Risk (Nexus)` | 本项目不评分 |
| 要求项 | Requirement | `control`/`profile` | `Control (Probo)` | `Requirement (Nexus)` | 不裸写 |

> **Probo/OSCAL/Nexus 仅作概念映射**；GRC Skill Agent 不导入其数据模型，不承诺导出兼容。

---

## 8. 写作规则

1. **中文正文**用中文名；**schema/代码/跨体系对照/导出映射**用英文规范写法 + 体系标注。
2. **裸词禁用**：§6 词无标注不得使用；工具 `tools/lint_terms.py`（如后续引入）只做提示，人工评审负责。
3. **一个概念一个 key**：新增术语先给 `T-…` key；无外部出处则标 `【本项目自定义】`。
4. **引用**：每条术语给来源；NIST/GAO/EU/CN 可直接引，ISO/IIA 只给条款号+释义。
5. **不输出结论**：用「评估/参考/范围说明」；不写「合规/违法/适用/不适用」作为系统结论。
6. **双语体例**：有英文原文时先原文后中文；ISO 不复制原文。
7. **术语修订**：改本文 + 决策日志 D-xxx；设计/代码只引用 key，不复述定义（沿 10 §7 指针原则）。

---

## 9. 与其他文档的关系

| 文档 | 关系 |
|---|---|
| `docs/specs/...v0.9.md` | 设计基线；术语引用本文 key/写法 |
| `spec/glossary.md` | rev4 继承词表（外部原义）；与本文冲突以本文为准 |
| `docs/decisions/user-decisions.md` | 术语相关用户裁定（D-003/D-006/D-015/D-021） |
| `docs/plan/w2-*` | Scope/Clarify 实现设计；术语以本文为准 |
| `docs/research/sources/` | 法条原文；不作为术语定义来源（术语定义在本文/00） |

---

## 10. 未决与维护

| 项 | 状态 | 说明 |
|---|---|---|
| `Control` 在本项目是否需要一个中立替代词 | open | 本项目不建模 control；文档提到时用 `Measure (Probo)`/`control (OSCAL)`；若未来引入控制库再定 |
| `Agent` | 未定义 | 本文不定义 Agent；GRC Skill Agent 是产品名，不是 AI-GRC-Consultant 的 Advisor/运行时组件 |
| 三值适用性（APPLIES/NOT_APPLICABLE/UNKNOWN） | **不采用** | D-003：determine 在 backlog；只做范围说明 |
| Probo/OSCAL 导出兼容 | out of scope | 不承诺 |
| CN 法域更多术语 | 待补 | 标识办法/算法推荐等入库时补 |

**维护**：本文每次修订需更新版本、决策日志；新增 KU/Scope/MCP 术语时同步本文 key；评审时检查裸词与「判定/合规结论」。

---

## 附录 A · 概念关系（本项目）

```
Scope ID ──► KU（30 字段）──► Claim ──► 候选句 ──► Answer
                  │                         │
                  ├─ verbatim_excerpt       ├─ required/order
                  ├─ verification           └─ validation_token
                  └─ page（kb:derived）──► render_hash/ku_hash

法域/框架不确定 ──► Clarify（多选）──► resolve_clarify ──► Answer
```

## 附录 B · 来源与版权

| 来源 | 版本 | 用途 | 版权 |
|---|---|---|---|
| AI-GRC-Consultant `00_glossary.md` | 项目 1.0 / v3.1 / 2026-10-18 | 各体系原义 | 项目文档 |
| AI-GRC-Consultant `10_terminology_standard.md` | 项目 1.0 / r4 / 2026-10-18 | 用词规范/分层/裸词 | 项目文档 |
| NIST AI 100-1 / SP 800-* / CSF 2.0 | 引用版本见 00/10 | 定义 | 美国政府作品 |
| GAO-21-368G | 2021 | Finding/Criteria | 美国政府作品 |
| ISO 37301:2021 / ISO/IEC 42001:2023 | 条款号 | 释义 | ISO 版权；不复制原文 |
| IIA 准则 2024 | 条款 | 释义 | IIA 版权；不复制原文 |
| EU AI Act | 02024R1689-20260727 | 法条 | 欧盟法律文本 |
| 中国《生成式人工智能服务管理暂行办法》 | 2023-08-15 | 法条 | 中国政府规章 |
