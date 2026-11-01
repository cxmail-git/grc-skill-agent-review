# GRC Skill Agent · 设计 v0.5（送 CCC 评审）

> 状态：**v0.5，已吸收 v0.4 定向复核（3 Block / 28 Major）** ｜ 日期：2026-10-31 ｜ 项目：grc-skill-agent
> v0.5 修正：全文快照口径统一；`validate_answer` 增**句内容**校验（evidence_quote/数字/实体/否定）、`answer_id` 与宿主模拟器；determine 残留清零并列出 backlog；金标 #19 `groups` 恢复、`coverage_note` 可机检；Art.5 计数改 7；PyYAML 安装/离线路径明确。
> v0.4 重大变更：**determine 推迟**（G3/规则/判定用例移 backlog）；Tier A **全文快照**；ask 改**宿主成文 + `validate_answer` 校验**；允许 **PyYAML**；单人核验用 **UNVERIFIED** 降级；结论用词改"**评估**"。详见 `docs/review/v0.4-decisions.md`。
> v0.3 关键修正：CI 判据改为**双向**（required_updates ⊆ actual_changed）；prose/translations 纳入 sentence_map；absence 有 schema+CK-14；CK-03 发布门禁四字段校验；golden #1/#3/#7/#14 与库对齐。
> v0.2 变更：locator 7 形态、claim+prose 双轨、CK-03 状态机、影响面 CI 按 change_id、determine 增 applies_later、检索/核验指标补全；见 `docs/review/pre-review-resolution.md`。
> 自检：已完成 spec 自检（9 处内部不一致已修，记录见 `docs/review/spec-self-review.md`），此后版本为送审版。
> 上游依据：本项目继承 `ai-grc-kb-v2-p0-rev4` 的知识契约（下称 rev4），并吸收 `08-四轮缺陷聚类与流程改进建议.md` 的五条根因与 P-1~P-7。
> 与其它项目关系：**独立仓库、独立命名空间；与 GovernAI / AI-GRC-Consultant 零文件共享、零术语借用**。
> 本文是唯一设计基线；评审意见按 §13 流程处置后升 v0.2。

---

## 0. 一页摘要

**做什么**：一个可安装的 Agent 能力包——以可审计 GRC 知识库为核心，提供（1）来源消化与知识更新、（2）带逐句引用的问答、（3）范围问题的原文说明（**不输出适用性结论**；determine 推迟到 v0.2）；通过 **MCP + Skill** 跨平台输出。

**不做什么**：不输出"合规/不合规"结论、不评分、不构成法律意见；MVP 不做自动爬虫、Web UI、多租户、跨法域对比页、向量检索。

**MVP 规模**：3 周；**52 条 KU（EU 32 + CN 20）**；20 个金标问答 + 5 个独立负例；citation 覆盖 100%；无据必拒答；改 1 条 KU 后 5 分钟内给出过期页清单。

**三个关键设计取舍**：
1. **只做"评估"不做"判定"**：MVP 不输出适用/不适用结论；范围问题只引用 KU 原文 + `coverage_note` + 免责。determine 与规则引擎推迟到 v0.2。
2. **答案先抽取后措辞**：断言必须绑定 KU + locator + 原文；绑定失败即删句，删完不成立即拒答；LLM 只做意图解析与措辞。
3. **Tier A 全文快照**：官方公开法律文本存全文（不商业转售）；KU 存摘录索引；CK-03 可执行；答案显式标注核验模式、核验人与访问时间。

---

## 1. 背景与目标

### 1.1 为什么现在做

rev1→rev4 五轮把一个"法条 → KU → 派生页 → 校验"的可审计知识契约修到了只剩 1 个 Block。它证明了三件事：
- **契约可行**：29 字段 KU、六类派生页、CK-01~13、双哈希、log/refs 在被反复攻击后仍然站得住；
- **失败模式清楚**：五轮 100 条缺陷里没有一条需要重做架构，全部是"规则与载体脱节、判据缺失、仪器污染、元信息漂移、自评替代复核"（08 报告 G-1~G-5）；
- **缺的是运行体**：rev4 没有编译器、没有校验器、没有检索与问答——它是"设计包"，不是"能力"。

本项目的目标就是把这份契约变成**能更新、能回答、能跨平台安装**的 Agent 能力（适用性评估放到 v0.2）。

### 1.2 目标（可验收）

| # | 目标 | 验收 |
|---|---|---|
| G1 | 消化：新增/修订来源可进入知识库，且不破坏既有契约 | `grc ingest → validate → compile` 全绿；变更影响面清单可复现 |
| G2 | 回答：问题→带引用答案；无据必拒答 | 20 金标 citation 覆盖 100%；5 个负例全部拒答 |
| G3 | **推迟（v0.2 产品版本）**：determine 与规则引擎 | 不进入 3 周 MVP；范围类问题由 ask 按 KU 原文作答 |
| G4 | 跨平台：同一能力在两类 Agent 宿主可用 | DSH 与 Claude Code 各跑通 3 个问题；MCP `tools/list` 六工具可发现 |
| G5 | 更新可演示：改 1 条 KU 后 5 分钟内检出 | `grc impact` 输出受影响页 + 过期 KU；重编译后问答引用同步 |

### 1.3 非目标（MVP 明确不做）

合规结论/风险评分/法律意见；自动爬虫与定时 watcher；Web UI / HTTP 服务；多租户与鉴权；跨法域对比页；向量检索；自动撰写叙事段（永久排除）；对来源全文的再分发。

**来源级排除（明确不在 52 KU 内）**：EU AI Act 的 GPAI 章（Art.53–55）、罚则（Art.99）、附件 IV–XIII 细则、成员国转化立法；中国《算法推荐管理规定》《深度合成规定》（只收《标识办法》）；执法案例与处罚决定。

---

### 1.4 来源版本（2026-10-31 已核实）

- **EU**：`Regulation (EU) 2024/1689`，采用 **consolidated as at 2026-07-27**（含 Digital Omnibus on AI，OJ L 2026/01744）。高风险义务适用日按合并版为 **2027-12-02（Annex III）/ 2028-08-02（Annex I）**，不是原版的 2026-08-02。
- **CN**：《生成式人工智能服务管理暂行办法》（2023-08-15 施行，24 条）；《人工智能生成合成内容标识办法》（2025-09-01 施行，14 条）。
- **CN 定位**：CN 法规以"第 X 条"定位，rev4 的 5 形态无法表达 → 本设计扩为 **7 形态**：中国条款式（含款/项）与附件式（C4）。
- 条款地图、KU 拆分计划与抓取可行性见 `docs/research/source-map.md`、`eu-article-map.md`、`cn-article-map.md`、`ku-plan.md`（附录 D/E 摘要）。

## 2. 用户与场景

### 2.1 用户

| 角色 | 他们问什么 | MVP 支持 |
|---|---|---|
| 合规/法务 | "这条法规要求我做什么？依据哪句？" | ✅ 义务清单 + 原文（不输出适用性结论） |
| 产品/工程 | "我们要上线 X，哪些条款会管到？" | ✅ 按 KU 原文列相关条款 + coverage_note（不输出适用/不适用） |
| 知识维护者 | "来源更新了，哪些 KU/页面要改？" | ✅ ingest + impact + 重编译 |
| 外部评审/审计 | "这个结论凭什么？" | ✅ citation + as_of + 核验模式 |

### 2.2 场景类型（MVP 覆盖）

1. 事实查询（某条要求/定义/时间点）
2. 义务清单（按角色/阶段列义务）
3. 适用范围（某类系统/用途是否落入某条款）
4. 跨条关联（高风险分类 → 对应义务链）
5. 应拒答（库中无此规则 / 超出覆盖法域 / 要求法律意见）
6. 来源性质（厂商标准 vs 法规，不得混同）

### 2.3 五个演示问句（验收用，后续扩到 20）

- EU：高风险 AI 系统的提供者在投放市场前有哪些义务？
- EU：哪些做法属于 AI 实践禁止清单？
- CN：生成式 AI 服务提供者对生成内容承担什么标识义务？
- CN：我们做的是企业内部知识库问答，算不算"向境内公众提供生成式 AI 服务"？（应引 Art.2 原文 + coverage_note，不输出适用性结论）
- 陷阱题：某厂商白皮书说"必须通过 ISO 42001 认证"——这是法规要求吗？（应拒答/纠正范畴）

---

## 3. 范围与交付形态

### 3.1 In Scope（3 周）

| 类别 | 内容 |
|---|---|
| 知识 | **EU 32 KU**（Art.2、Art.5 选 7 项禁止、Art.6+Annex III、Art.8–15、Art.16、Art.26 选 3 款、Art.27、Art.50 选 3 款、Art.113）+ **CN 20 KU**（暂行办法 13 + 标识办法 7）；六类页面生产 concept/entity/overview/topic/source 五类（comparison 不用） |
| 能力 | MCP 六工具（只读）：`search_kus` `get_ku` `get_page` `ask` `validate_answer` `freshness`；CLI `grc` 另有 `ingest/validate/compile/impact/publish/verify-source`（写操作不对 Agent 暴露） |
| 更新 | registry + Tier A 全文快照 + verification.yaml + fingerprint + impact 矩阵 + log.md/refs.json + 人审签署 |
| 分发 | `skills/grc-agent/SKILL.md`（DSH 与 Claude Code 共用体）+ Codex `AGENTS.md` 适配说明 |
| 评估 | 20 金标 + **5 独立负例** + 检索召回 + 宿主合规（validate_answer）+ 变更传导；`grc eval` 一条命令跑完 |

### 3.2 Out of Scope

见 §1.3。另：不覆盖执法案例、不覆盖成员国转化立法、不覆盖中国算法推荐/深度合成之外的配套规章。

### 3.3 语言

- 作答语言：默认**跟随用户语言**；可显式指定（`--lang zh\|en` 或请求内声明）。
- 原文引用：始终保留**原文语言逐字**，不翻译；需要译文时单独标注 `translation` 字段。
- 免责声明与拒答理由：按作答语言本地化（zh/en 两套，MVP 不做第三语言）。

---

## 4. 架构

### 4.1 总览

```
来源登记 registry.yaml
   │  ingest（人工触发）
   ▼
Tier A 全文快照 snapshots/<source_id>.md（官方全文 + fulltext_sha256 + 核验头）
   │  extract（人工+可选 LLM 起草）
   ▼
KU YAML（29 字段，gsk-*）── validate（CK-01~13）── compile ──► 派生页 pages/*.md
   │                                                        │  render_hash / ku_hash
   └──────────────► 索引 index.json（BM25 + 元数据）◄────────┘
                          │
                    grc_core（Python，确定性）
                          │
              ┌───────────┴────────────┐
         grc_mcp（stdio，只读）      grc CLI（运维/写操作）
   search/get_ku/get_page/ask/       ingest/validate/compile/
   validate_answer/freshness          impact/publish/verify-source
              │
   DSH SKILL.md · Claude Code SKILL.md · Codex AGENTS.md
```

### 4.2 组件边界

| 组件 | 职责 | 依赖 | 可独立测试 |
|---|---|---|---|
| `grc_core.schema` | KU/页面/registry/catalog 的结构与取值域 | PyYAML | ✅ 单测 |
| `grc_core.validate` | CK-01~13（MVP 全实现；CK-13 冲突存在性人工） | schema | ✅ 夹具 |
| `grc_core.compile` | KU → 派生块/页面渲染、双哈希、refs.json | schema | ✅ 黄金文件 |
| `grc_core.index` | BM25 + 元数据过滤（jurisdiction/topic/type） | compile 产物 | ✅ |
| `grc_core.answer` | 答案组装、拒答、语言与免责 | index | ✅ 金标 |
| `grc_core.binder` | claim 三模式绑定（quote/translation/frame）+ 独立 unsupported 复核 | answer | ✅ 单测 |
| ~~`grc_core.determine`~~ | **推迟到 v0.2**；MVP 不实现 | — | — |
| `grc_core.ingest/impact/freshness` | 来源登记、fingerprint、影响面、过期检测 | 全部 | ✅ |
| `grc_mcp` | MCP stdio 协议、工具注册、入参校验 | core | ✅ 协议测试 |
| `skills/grc-agent` | 触发与流程编排（何时 ask / validate_answer / ingest） | MCP 或 CLI | ✅ 手工 |
| `grc_core.eval` | 金标/负例/宿主合规/传导 | 全部 | ✅ CI |

**硬边界**：MCP 与 CLI 不复制业务逻辑；skill 不复制规则，只编排；**唯一第三方运行时依赖是 `PyYAML==6.0.2`（pin；`pip install` 或 `vendor/wheels/` 离线安装）**，其余标准库（MCP 用手写 JSON-RPC stdio）。`grc doctor` 校验版本与离线可装。

**索引**：ASCII 按词、CJK 按**字符二元组（bigram）**，标题与 catalog 别名加权；不引入第三方分词。

### 4.2.1 MCP 工具契约（MVP）

| 工具 | 入参 | 出参 | 主要错误 |
|---|---|---|---|
| `search_kus` | `{query, jurisdiction?, doc_type?, top_k=5}` | `{hits:[{ku_id,title,jurisdiction,locator,snippet,score}]}` | `INVALID_INPUT` |
| `get_ku` | `{ku_id}` | `{ku: 完整 YAML}` | `NOT_FOUND` |
| `get_page` | `{slug}` | `{markdown, front_matter}` | `NOT_FOUND` |
| `ask` | `{query, language?, jurisdiction?, no_llm?}` | 见 §7.1（claims + skeleton） | `NO_KU` / `OUT_OF_SCOPE` / `INVALID_INPUT` |
| `validate_answer` | `{answer, claims, sentences, language}` | `{ok, errors[]}`（见 §7.4） | `UNSUPPORTED_CLAIM` / `SENTENCE_MAP_MISSING` / `CITATION_MISMATCH` |
| `freshness` | `{ku_ids?}` | `{oldest_verified_at, expired_ku_ids, verification}` | `NOT_FOUND` |


**MCP 协议面**：仅实现 `initialize` / `tools/list` / `tools/call` / 标准错误对象；不实现 resources、prompts、sampling（MVP 不需要，列入 v0.2）。

**边界**：`impact` 是运维动作，**只在 CLI**（`grc impact`），不通过 MCP 暴露给 Agent —— 最小权限，Agent 不能触发写操作。

**协议测试（6 条，预演 F-34）**：① 握手 `initialize` 版本协商（`protocolVersion: "2025-06-18"`，失败回退最近支持版本并记录）；② 未知工具 `NOT_FOUND`；③ 参数非法 `INVALID_INPUT`；④ 业务失败（`NO_KU`）走 `result.isError=true` + 业务 code，不占 JSON-RPC 错误码（-326xx）；⑤ 大响应 >64KB 时返回 `truncated:true` + `next_cursor`（不静默截断）；⑥ 并发按 request id 隔离，2 连接不共享状态。

### 4.3 跨平台策略

| 宿主 | 接入方式 | MVP 验证 |
|---|---|---|
| DSH | `~/.agents/skills/grc-agent/`（SKILL.md + MCP 配置） | 3 问 + validate_answer 1 例 |
| Claude Code | `.claude/skills/grc-agent/` 或用户级 skills | 3 问 + validate_answer 1 例 |
| 其它 MCP 宿主（Codex/Cursor 等） | 仅需 MCP server 配置 | **未验证（v0.2）**；G4 只承诺 DSH + Claude Code |

---

## 5. 数据契约（继承 rev4 + 五处变更）

### 5.1 原样继承（不重新发明）

- **KU 29 字段** = 17 fact-bearing（#2–#18）+ 12 bookkeeping（#1 + #19–#29）；`instrument_type` 11 值闭合；`locator` 5 形态；`gap` 为登记对象不入 29。
- **六类页面**必备段、`kb:derived` / `kb:table` 语法、`render_hash` / `ku_hash` 计算、`rendered_blocks` 与块 id 规则、结构声明行白名单（3 字段）。
- **13 条校验** CK-01~13；WS-01~09；DF-1~6 / DF-4b / DF-4c 与 EX-1~7；front-matter 8 键；`log.md` 4 列；`refs.json` 4 键。**v0.3 新增 CK-14（absence 依据）与 CK-15（核验来源）**，见 §7.4。
- **08 根因对策**：P-1 数字/命名生成化；P-2 变更影响面矩阵；P-3 规则四要素（判定主体/输入/闭合值域/错误码）；P-4 探针正反基线；P-5 证据 lint。
- **N-11 修法（W1-1b，用户无需再裁定）**：CK-11 增 `log.md` 每行校验——`event ∈ {INGEST,RECOMPILE,RECHECK,SIGNOFF,SUPERSEDE}`、`subject` 可解析为存在的 ku_id/page_slug/registry_id、`date` 为 ISO 且不早于上一行（`DANGLING_REF`）；CK-09 增 `## 更新记录` 表必须是 log.md 的投影（`WHITELIST_VALUE_MISMATCH`）；各配 1 反例。
- **页面侧引文**（预演 F-P1）：页面只渲染 `verbatim_excerpt` 的派生块；WS-03 增子项"块内引文必须是 excerpt 连续子串"；不得在正文另写引文。
- **语言**（F-23）：页面/派生块用中文叙述；KU 的 `verbatim_excerpt` 与 `obligation.text` 保留原文；DF/WS/EX 规则在 schema 里声明适用语言（英文 KU 走 DF 的英文等价词表）。
- **v0.3 闭合值域（导入时补 4 张表，F-13）**：

| 字段 | 闭合值 |
|---|---|
| `modality` | `obligation` / `prohibition` / `right` / `definition` |
| `subject` | `provider` / `deployer` / `importer` / `distributor` / `user` / `public_authority` |
| `frequency` | `once` / `per_placing_on_market` / `per_use` / `annual` / `on_request` / `continuous` |
| `scope_type` | `system` / `use_case` / `role` / `territory` / `organisation` |

`applies_to[]` 统一为 `{subject, stage, scope_type, scope_value, note?}`；`evidence_requirement[].frequency` 取上表。

### 5.2 六处变更（v0.4；需 CCC 重点挑战）

| # | 变更 | 理由 | 影响 |
|---|---|---|---|
| **C1** | **Tier A 存官方全文快照**（不商业转售）；**snapshot 是来源级全文的唯一真值**，每 KU 的核验元数据在 `kb/verification.yaml`；registry 只存来源级字段。元数据：`source_url` / `verification_url` / `version` / `fulltext_sha256` / `page_digest` / `excerpt_hash`（verification）/ `verification` / `verification_source` / `verified_at` / `verified_by` / `second_review` / `evidence_ref` | 让 CK-03②（章节定位）与"可审计"可执行；消除双真值 | §5.3；发布门禁按 §5.3 校验 |
| **C2** | 作答语言 = 用户语言或指定语言；原文引用恒为原文；译文单列并标 `machine` | 用户要求 | `language` / `translations[].claim_ids`；claim `binding_mode: translation` |
| **C3** | 新增**非 KU** 表：`catalog.yaml`、`kb/scope_exclusions.yaml`（absence 依据）；`rules/applicability-*` 与 `kb/profiles/` 随 determine 推迟 | 检索与否定句所需 | 新增 lint `NON_KU_FACT`；新增 **CK-14**（§7.2） |
| **C4** | `locator` 7 形态，**每条都给全文正则**（见下）；禁止区间与混写 | EU 字母项/附件、CN 款/项在原 5 形态下不可表达 | CK-01 的 locator 校验；ku-plan 52 条单 locator |
| **C5** | 答案改为「claim（证据单元）+ sentences（逐句映射）+ translations（带 claim_ids）」；`sentence_map` 由 binder 校验 | prose/译文可夹带无据事实（N-01） | §7 全文重写；binder 校验到句 |
| **C6** | `applies_from` 规则级设计**随 determine 推迟**；v0.4 只在 KU 的 `effective_date` 与 `transition_note` 保留双日期说明 | 多日期表达需求推迟到 v0.2 | backlog |

**locator 7 形态（全文正则；CK-01 逐字实现）**：

| # | 形态 | 正则 | 例 |
|---|---|---|---|
| ① | 条款式（含字母项） | `^Art\.\d+((\(\d+\))|(\([a-z]{1,3}\))){0,4}$` | `Art.5(1)(ba)` |
| ② | 章节式 | `^§\s?\d+(\.\d+)*$` | `§ 12.3` |
| ③ | 命名章节式 | `^[A-Z][A-Za-z0-9 .\-]{2,80}$` | `Chapter III` |
| ④ | 页码式 | `^p\.\d+$` | `p.42` |
| ⑤ | 条目式 | `^\([a-zA-Z0-9]{1,3}\)$` | `(a)` |
| ⑥ | 中国条款式（含款/项，全/半角括号） | `^第[一二三四五六七八九十百零〇\d]+条(第[（(]?[一二三四五六七八九十百零〇\d]+[）)]?款)?(第[（(]?[一二三四五六七八九十百零〇\d]+[）)]?项)?$` | `第四条第（二）项` |
| ⑦ | 附件式 | `^Annex [IVX]+( point \d+)?(\([a-z]\))?$` | `Annex III point 1` |

**禁止**：区间（`Art.26(1)-(2)`）、混写（`Art.5(1)(a)-(b)`）、把款/项塞进条款式；细分锚点用 `anchor`（`^[a-zA-Z0-9_-]+$`，如 `p1`、`art7`）。

### 5.3 快照与核验（v0.4：Tier A 全文快照）

**粒度**：**每来源一份全文快照**（Tier A primary）；KU 的 `verbatim_excerpt` 必须是全文的连续子串；每 KU 的核验状态记在 `kb/verification.yaml`。

```yaml
# kb/snapshots/reg-eu-ai-act.md 头部
source_id: reg-eu-ai-act
source_url: "https://eur-lex.europa.eu/..."          # 登记链接
verification_url: "https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14"
version: "02024R1689-20260727"                        # 合并版标识（作者核实）
amendment_ref: "OJ L 2026/01744 (Digital Omnibus)"   # 修订法令（作者核实）
accessed_at: 2026-10-31
fulltext_sha256: "sha256:…"                           # 对存下来的官方全文取哈希
license_note: "法律文本公开引用；不再分发用于商业转售"
```

```yaml
# kb/verification.yaml（每 KU）
gsk-eu-art14:
  snapshot_ref: "snapshots/reg-eu-ai-act.md#Art.14(1)"
  verification_mode: manual     # online | manual | offline
  freshness: fresh              # fresh | expired（由 verified_at + max_age 重算）
  verified_at: 2026-10-31
  verified_by: "R-2"            # 角色码，不写实名
  second_review: false          # 单人核验 → UNVERIFIED
  evidence_ref: "evidence/verify/eu-art14-2026-10-31.md"
  page_digest: "sha256:…"
```

**CK-03（v0.4）**：
1. `verbatim_excerpt` 是 `snapshots/<source>.md` 全文的连续子串（全文快照让这项可执行）；
2. `locator`/`anchor` 必须在全文里能定位到章节标题（rev4 CK-03② 可跑）；
3. `page_digest` 与 `verification_url` 最近抓取一致；
4. `offline` 只允许 `status: draft`，发布门禁拒绝；`freshness` 按运行日重算，不信任字段。

**核验与发布**：
- `manual` 必须有 `verified_by` + `verified_at` + `evidence_ref` + `page_digest`；
- `second_review: false` 的 KU 发布时标 **`UNVERIFIED`**，答案带警告（用户裁定 D5，单人模式）；
- 发布门禁按 `verified_at + max_age_days` 重算过期；EUR-Lex 走 manual（脚本抓取被拒，见 source-map §6）。

### 5.4 目录与命名

```
grc-skill-agent/
├── AGENTS.md / README.md
├── pyproject.toml
├── src/grc_core/{schema,validate,compile,index,answer,validate_answer,ingest,impact,freshness,eval}.py
├── src/grc_mcp/server.py
├── skills/grc-agent/{SKILL.md,references/{answer-contract,ingest}.md}
├── kb/
│   ├── ku/*.yaml                 # gsk-eu-* / gsk-cn-*
│   ├── pages/*.md
│   ├── snapshots/<source_id>.md  # Tier A 官方全文（唯一真值）+ 核验头
│   ├── catalog.yaml
│   ├── registry.yaml             # 来源级，不含 verification
│   ├── verification.yaml         # 每 KU 核验记录（verified_by/second_review/evidence_ref）
│   ├── scope_exclusions.yaml     # absence 依据（CK-14）
│   ├── profiles/*.yaml           # 推迟（v0.2）
│   ├── log.md
│   └── refs.json
├── changes/<change_id>.yaml      # 影响面申报（CI 读）
├── evidence/                     # 核验截图 / 变更实测输出
├── rules/                        # 推迟（v0.2）：applicability-*.yaml
├── eval/{golden.yaml,adversarial.yaml,run.py}
├── docs/{specs,adr,review}
└── tests/
```

**registry.yaml 条目（最小）**：

```yaml
- id: reg-eu-ai-act
  title: "Regulation (EU) 2024/1689"
  issuer: "European Parliament and Council"
  jurisdiction: EU
  source_class: primary
  tier: A
  source_url: "https://eur-lex.europa.eu/..."        # 登记链接
  verification_url: "https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14"
  accessed_at: 2026-10-31
  status: published
# 注意：verification / second_review / verified_by 只在 kb/verification.yaml，registry 不存
```

**catalog.yaml（检索索引，不承载事实）**：`topics: {high-risk: [gsk-…], prohibited: […]}`、`aliases: {…}`。只允许 `ku_id` 与标签；出现义务性句子即 lint 失败（`NON_KU_FACT`）。

---

## 6. 知识生产流水线

### 6.1 六步（每步有人审闸门）

| 步 | 命令 | 产物 | 闸门 |
|---|---|---|---|
| 1 登记 | `grc ingest register <id> --url <url>` | registry 条目（source_class/tier/jurisdiction） | 来源性质与等级人工定 |
| 2 摘录 | `grc ingest excerpt <id> --locator <loc>` | 全文快照 + 摘录索引 + excerpt_hash | 逐字人工核对（Tier A；单人时 UNVERIFIED） |
| 3 入库 | `grc ingest draft <id>`（可选 LLM 起草） | KU YAML 草稿 | 人工改毕、`gap` 登记 |
| 4 校验 | `grc validate [--ku <id>]` | 错误清单 | CK 全绿；CK-13 冲突人工签署 |
| 5 编译 | `grc compile --changed` | 派生页 + 双哈希 + refs.json | 渲染差异人工审 |
| 6 发布 | `grc publish` | log.md 追加 + registry.published | Tier A 签署记录 |

### 6.2 变更影响面（P-2 落地，v0.3 双向判据）

**核心修正（F-07）**：不再用"允许集"单向判断，而是**双向**：
- `required_updates(change)` = 由**变更文件本身**经依赖图推出的**必须同步更新**的实例集；
- 判据：`required_updates ⊆ actual_changed` **且** `actual_changed ⊆ changed_files ∪ all_consumers`。

```yaml
# changes/<change_id>.yaml（一个 PR 一个 change_id；不允许手写 ku_ids 为空）
change_id: CH-2026-11-001
summary: "Art.6 高风险分类 KU 修订"
changed_files: [kb/ku/gsk-eu-art6-2.yaml]
required_updates: [eval/golden.yaml, kb/pages/entity-eu-art6.md]   # PR 作者声明，CI 复核
evidence:
  - cmd: "grc eval --case ord-03 && grc validate"
    exit: 0
    output_file: evidence/CH-2026-11-001.txt
```

**CI 步骤**：
1. 从 PR 取 `Change-Id:`；缺失/重复 → `CHANGE_ID_MISSING` / `CHANGE_ID_UNKNOWN`；文件为空 → `DECLARED_EMPTY`；
2. `required_updates_actual = graph_required(changed_files)`：KU→`eval/golden.yaml` 与页面块、契约→模板、目录→alias lint；**不再从手写 `ku_ids` 推**；
3. `required_updates_actual ⊆ actual_changed`，否则 `IMPACT_UNREPORTED`；
4. `actual_changed ⊆ changed_files ∪ all_consumers`，否则 `IMPACT_OUT_OF_SCOPE`；
5. 重跑 `evidence[].cmd` 与 `output_file` 逐字比对 → `EVIDENCE_STALE`；
6. 读 `docs/impact-matrix.md`：`done` 行路径必须存在、`evidence` 必须存在，否则 `MATRIX_INVALID`；
7. **反向探针**：fixture"只改 `kb/ku/gsk-eu-art6-2.yaml`、不改 `eval/golden.yaml`"→ **必须 FAIL**，否则 `PROBE_BROKEN`。

### 6.3 演示脚本（验收用）

```
1. 改 `kb/ku/gsk-eu-art113.yaml` 的 `effective_date` / `transition_note`（该 KU 是"何时适用"的唯一来源）
2. `grc impact` → 输出受影响页（预计 2 页）+ 过期 KU + 需重编译对象；计时
3. grc compile --changed && grc validate && grc publish
4. `grc ask "高风险义务从什么时候开始适用？"` → 答案引用 `gsk-eu-art113`，日期与引用同步更新（通用适用日 2026-08-02；Annex III/Annex I 两日期写在 KU 的 `transition_note`）
   目标：第 1→4 步 < 5 分钟（不含人审思考）
```

---

## 7. 答案契约（v0.5：claim + sentence_map + 宿主成文 + 句内容校验）

> 用户可见措辞统一用"**评估**"（不用"判定"）；不输出适用/不适用结论。

### 7.1 输出对象（MCP `ask` 返回）

```json
{
  "mode": "answer|partial|refuse",
  "partial_reason": "conflict|cross_jurisdiction|coverage_gap|null",
  "answer_id": "ans_01J…",                 // validate_answer 必须回传
  "skeleton": ["c1", "c2"],                // 必须覆盖的 claim
  "groups": [{"label": "EU", "claim_ids": ["c1"]}],
  "language": "zh",
  "sentences": [
    {"text": "高风险系统的提供者须在投放市场前完成合格评定。", "claim_ids": ["c1"], "frame": false},
    {"text": "以下按法域分列。", "claim_ids": [], "frame": true}
  ],
  "translations": [
    {"lang": "en", "source": "machine",
     "sentences": [{"text": "Providers of high-risk AI systems …", "claim_ids": ["c1"]}]}
  ],
  "claims": [
    {"claim_id": "c1", "text": "…（与 sentence 语言一致）",
     "binding_mode": "quote|translation|frame",
     "support_type": "direct|composite|absence|frame",
     "ku_ids": ["gsk-eu-art16"], "scope_exclusion_id": null,
     "locator": "Art.16", "anchor": "p1",
     "verbatim": "…（原文逐字；translation 时为原文）",
     "extraction_span": {"field": "obligation[0].text", "start": 0, "end": 42},
     "confidence": "high"}
  ],
  "count_from_ku": {"c1": 12, "basis": "Art.16(a)-(l)"},
  "citations": [
    {"ku_id": "gsk-eu-art16", "title": "Article 16 — Obligations of providers",
     "source_class": "primary", "tier": "A", "locator": "Art.16", "anchor": "p1",
     "verbatim": "…", "source_url": "https://eur-lex.europa.eu/…",
     "verification_url": "https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-16",
     "accessed_at": "2026-10-31", "verification": "manual",
     "verified_at": "2026-10-31", "verified_by": "R-2 / 张三"}
  ],
  "coverage_note": "本库覆盖 Art.5 的 7 项禁止实践；其余 3 项（a/b/bb）未收录。",
  "freshness": {"oldest_verified_at": "2026-10-31", "expired_ku_ids": []},
  "refusal": {"reason": "no_ku|out_of_scope|conflict_unresolved|not_legal_advice|scope_correction",
               "missing": "…", "suggested_action": "…"},
  "disclaimer": "本回答仅基于所收录来源与所提供信息，不构成法律意见。"
}
```

### 7.2 硬规则（v0.3）

1. **事实句绑证据**：`support_type ∈ {direct, composite}` 的 claim 必须有 `ku_ids`；`absence` 必须有 `scope_exclusion_id` 且解析到 `kb/scope_exclusions.yaml`（**CK-14**）；`frame` 必须**不含 DF-1~DF-6 任一形态**，且只允许"定义/方法/回答结构"句。
2. **逐句映射**：`sentences[]` 每个 `frame=false` 的句子必须有非空 `claim_ids`；`frame=true` 的句子由 DF 扫描器复核。**不存在"不校验 prose"的例外**。
3. **译文受同一约束**：`translations[].sentences[].claim_ids` 必填且与原句一致；`citations[].verbatim` 永不翻译。
4. **prose 不引入新事实**：`sentences[].text` 只能复述所绑 claim 的内容；binder 逐句校验（§7.3）。
5. **无据必拒**：无命中 → `refuse(no_ku)`；要求法律结论/适用性结论 → `refuse(not_legal_advice)`；范畴混淆 → `refuse(scope_correction)`。
6. **partial 与 refuse 的分界**：整段答案无法成立 → `refuse`；仅部分断言可成立 → `partial` + `partial_reason`。`conflict`（部分冲突）与 `conflict_unresolved`（整体不可判）**二选一**，由"剩余 claim 是否足够回答"决定。
7. **元信息必带**：`as_of`（最旧核验日）、`verification`、`verified_by`（manual）、`disclaimer`；`coverage_note` 在 `coverage_gap`/`no_rule_matched` 时必填。
8. **宿主成文（D2）**：`ask` 返回 claims + citations + `skeleton`；宿主 LLM 负责最终措辞，但**必须**把 `sentences[]` 回传 `validate_answer`；校验失败不得展示答案。
9. **计数可复算**：`count_from_ku` 必须等于可复算的 claim/子项数，否则 `COUNT_MISMATCH`。

### 7.3 实现路线（防幻觉）

- **抽取优先**：core 从 KU 字段检索候选 claim；LLM 只做意图解析与 `sentences` 措辞。
- **binder 三模式**：`quote` 校验 span 是 KU 字段连续子串；`translation` 校验原文子串 + 译文标记；`frame` 走 DF-1~6 扫描。
- **句级校验**：`sentence_map` 校验每句 `claim_ids` 存在、claim 已绑定、句子不含未绑定的事实形态；`translations` 同规则。
- **独立复核**：`unsupported_claims` 由独立脚本重算（不调用 `answer.py`），按 `(ku_id,locator,verbatim)` 与句级映射双重比对。
- **frame 比例**：`frame` 句占比 >20% 时 WARN（防止用框架句逃避绑定）。
- **`--no-llm`**：纯抽取式；`--llm` 与 `--no-llm` 指标分表记录，不合并。

### 7.4 宿主成文与 `validate_answer`（v0.5 / D2）

**ask 返回**：`answer_id` + `skeleton` + `claims` + `citations` + `coverage_note` + `mode`（见 §7.1）。`answer_id` 由 core 签发并记录（`evidence/answers/<id>.json`，含 claims 快照），用于事后核对"用户看到的答案"。

**宿主契约**：宿主 LLM 负责措辞，但每个非 frame 句必须：

```json
{"text":"提供者须在投放市场前完成合格评定。",
 "claim_ids":["c1"],
 "evidence_quote":"…（必须能在这条 claim 的 verbatim/text 中找到的连续子串）",
 "frame":false}
```

**validate_answer（入参 = answer_id + sentences + claims + mode + coverage_note + as_of + disclaimer）** 校验：

1. **answer_id 有效**：能在记录的 ask 输出中找到，且 claims 未被替换；
2. **skeleton 覆盖**：skeleton 的每个 claim 至少被 1 句引用；
3. **句→证据**：非 frame 句的 `evidence_quote` 必须是 claim.verbatim 或 claim.text 的连续子串（不是只验编号）；
4. **数字/日期/实体**：从 `sentence.text` 抽取数字、日期、专名，必须 ⊆ `evidence_quote` 的对应 token 集合（防"c1 配 2027-12-02"）；
5. **否定/情态**：句中出现 shall/must/may/不得/无需 时，必须与 `evidence_quote` 的情态一致；
6. **mode 重算**：由 claims 覆盖与 coverage_note 推导 mode；与入参不符 → `MODE_MISMATCH`；
7. **元信息**：`coverage_note`（partial/coverage_gap 时必填）、`as_of`、`disclaimer`、`count_from_ku` 必须与 ask 输出一致；
8. **引用集合**：`citations` 的 ku_id 集合 = claims 的 ku_id 集合。

错误码：`ANSWER_ID_INVALID` / `SKELETON_UNCOVERED` / `EVIDENCE_QUOTE_MISSING` / `QUOTE_NOT_SUBSTRING` / `NUMBER_MISMATCH` / `MODALITY_MISMATCH` / `MODE_MISMATCH` / `META_MISSING` / `CITATION_MISMATCH`。

**宿主跳过校验**：skill 必须写"未拿到 `validate_answer.ok=true` 不得展示"；`grc eval --host-simulate skip` 模拟跳过，必须被 eval 判失败。`citation 100%` 指标只在 **validated answers** 上计算（§9.2）。

### 7.4.1 新增校验：CK-14 / CK-15

**CK-14（absence 依据）**：`support_type=absence` 的 claim 必须满足：
1. `scope_exclusion_id` 非空且能在 `kb/scope_exclusions.yaml` 解析；
2. 条目的 `as_of` 非空、`jurisdiction` 与 claim 一致；
3. 条目 `registry_id` 指向已登记来源；
否则 `ABSENCE_UNSUPPORTED`。

```yaml
# kb/scope_exclusions.yaml（示例）
- id: sx-eu-gpai
  jurisdiction: EU
  registry_id: reg-eu-ai-act
  as_of: 2026-10-31
  reason: "GPAI 章 Art.51–56 不在本库收录范围"
  evidence_url: "https://eur-lex.europa.eu/..."
- id: sx-eu-iso42001
  jurisdiction: EU
  registry_id: reg-eu-ai-act
  as_of: 2026-10-31
  reason: "ISO/IEC 42001 是管理体系标准，不是本条例义务"
  evidence_url: "https://www.iso.org/standard/81230.html"
```

**CK-15（核验来源）**：`verification` 只能由 `grc verify-source`（`verification_source: verify-source`）或 `grc signoff`（`manual-signoff`）写入；YAML 手填的 `verification` 与 `verification_source` 不匹配、或缺少 `verified_by`/`evidence_ref`/`page_digest` → `VERIFICATION_UNVERIFIED`。

## 8. 适用性评估（`determine`，v0.4 推迟到 v0.2）

> **v0.4 决定（D3）**：`determine` 不进入 3 周 MVP。以下 §8.1–8.4 保留为 **v0.2 产品版本 backlog**；MVP 中范围类问题（#8/#14/#16）由 `ask` 按 KU 原文回答，并带 `coverage_note`，**不输出适用/不适用结论**。
> 用词（用户要求）：对外结论统一用"**评估**"，不用"判定"。

### 8.1 输入画像（profile，v0.3 闭合值域）

```yaml
jurisdiction: EU | CN | OTHER          # OTHER → out_of_scope（可表达 SG/US）
role: provider | deployer | importer | distributor | user
entity: company | public_authority | research | individual
system:
  is_ai_system: true
  is_general_purpose: false
  domains: [biometrics, critical_infra, education, employment, essential_services, law_enforcement, migration, justice, other]
  use_cases: [social_scoring, real_time_rbi, emotion_recognition, biometric_categorisation, facial_scraping, predictive_policing, education_scoring, employment_scoring]
org: {size: sme | large}
timeline: {placing_on_market: 2026-12-01, in_service: 2026-12-01}
judgements:                              # 定性判断由用户自答（N-09/F-06）
  - {id: art6_3_no_material_influence, question: "系统是否未实质性影响决策结果？", answer: true|false|unknown}
```

**值域**：`domains` / `use_cases` 为闭合枚举；同义词映射由 `rules/synonyms.yaml` 负责（大小写/别名归一），映射缺失 → `INVALID_INPUT`。

### 8.2 输出（v0.3）

```json
{
  "verdict": "applies|applies_later|no_rule_matched|insufficient_info|out_of_scope",
  "applies_from": [
    {"scope":"Annex III","date":"2027-12-02","basis_ku":"gsk-eu-art113","basis_locator":"Art.113(c)(i)"},
    {"scope":"Annex I","date":"2028-08-02","basis_ku":"gsk-eu-art113","basis_locator":"Art.113(c)(ii)"}
  ],
  "currently_in_force": false,
  "evaluated_at": "2026-10-31",
  "findings": [
    {"rule_id":"eu-hr-annex3-01","ku_id":"gsk-eu-art6-2","locator":"Art.6(2)",
     "basis_verbatim":"…","reason_code":"USE_CASE_HIT",
     "obligations":[{"ku_id":"gsk-eu-art26-2","locator":"Art.26(2)","text":"…","basis":"obligation[0].text"}]}
  ],
  "listed_obligations_from_source": [{"ku_id":"…","locator":"…","text":"…","basis":"…"}],
  "coverage_note": "本库未收录 Art.43 合格评定细则。",
  "missing_fields": ["system.domains"],
  "citations": [{"ku_id":"…","locator":"…","verbatim":"…","verification":"manual","verified_by":"R-2 / 张三"}],
  "freshness": {"oldest_verified_at":"2026-10-31","expired_ku_ids":[]},
  "as_of": "2026-10-31",
  "verification": "manual",
  "verified_by": "R-2 / 张三",
  "disclaimer": "本评估仅基于所收录来源与所提供画像，不构成法律意见；最终适用性以监管解释/司法认定为准。"
}
```

**语义**：`applies` 命中且已生效；`applies_later` 命中但 `currently_in_force=false`；`no_rule_matched` **库内**未命中（不是法律上不适用，必须给 `coverage_note`）；`insufficient_info` 缺字段或 judgement=unknown；`out_of_scope` 法域/对象超范围。`findings[].basis_verbatim` 必须是 KU 字段连续子串（binder 同规则）。

### 8.3 规则引擎（v0.3）

```yaml
# rules/applicability-eu.yaml（单条）
- id: eu-hr-annex3-01
  ku_ids: [gsk-eu-art6-2, gsk-eu-annex3-1]
  jurisdiction: EU
  when:
    - {field: system.use_cases, op: intersects, value: [real_time_rbi, biometric_categorisation]}
  judgement_required:
    - {id: art6_3_no_material_influence, question: "是否未实质性影响决策结果？"}
  exceptions:
    - {id: ex-art6-3, when: [{field: judgements.art6_3_no_material_influence, op: eq, value: true}], basis_ku: gsk-eu-art6-3}
  obligations_from: [gsk-eu-art26-1, gsk-eu-art26-2]
  priority: 50            # 0–100，整数
  applies_from:
    - {scope: Annex III, date: 2027-12-02, basis_ku: gsk-eu-art113, basis_locator: Art.113(c)(i)}
```

**求值顺序**：`exceptions`（命中⇒规则不适用）→ `priority` 高者胜 → 同 priority 异结论 ⇒ `insufficient_info`（列规则 id）。**禁止**脚本表达式、禁止在规则里写死 judgement 答案。`--explain` 固定输出：规则 id / 命中项 / 例外 / 结论 / 依据 KU。

### 8.4 边界（写死）

- 不输出"合规/不合规/风险分值"；
- 画像缺字段 → `insufficient_info`，不得猜测；
- `out_of_scope`：法域未收录（如 SG/US）或对象非 AI 系统；
- 所有输出必带免责声明；MVP 不含 `determine`，`SKILL.md` 禁止输出适用/不适用结论（v0.2 再恢复）。

---

## 9. 评估与质量门禁

### 9.1 金标集（20 题 + 独立负例 5 题）

- **金标 20 题**（附录 A）：`id / question / language / expected_mode / expected_claim_ku_ids / expected_refusal_reason / expected_coverage_note / expected_facts / forbidden_terms / retrieval_expect / partial_reason?`。`expected_facts` 由非规则作者独立撰写（防自评）。
- **拒答题固定 5 题**：#4（no_ku）、#9（scope_correction）、#10（not_legal_advice）、#17（scope_correction）、#20（not_legal_advice）——脚本可复算 5/5。
- **独立负例 5 题**：`eval/adversarial.yaml`，不计入金标分母。
- **检索验收**：每题 `retrieval_expect`；top5 召回 ≥18/20；每题至少 1 个别名（lint 强制）；`no_ku` 判据 = 最低分阈值 + 必含词未命中；主题链由 `catalog.topics` 展开。
- **用例类（6 类）**：事实/义务、否定/纠正、跨域、时间敏感（`--now`）、提示注入、多轮/同题异措辞。
- **冻结**：W1 结束前打 tag；`expected_mode` 由脚本校验单值。

### 9.2 指标（CI 门禁，v0.3）

| 指标 | 判据 | 计算方式 |
|---|---|---|
| 检索召回 | top5 ≥18/20 | `eval/retrieval.py` 独立跑 |
| citation 覆盖 | claims 100% 有 `ku_ids` 或 `scope_exclusion_id`（**frame 不入分母**） | `eval/claims.py` |
| 句映射覆盖 | `frame=false` 的句子 100% 有 `claim_ids` | `eval/sentence_map.py` |
| 无据断言 | 0 | 独立脚本重算（不调用 `answer.py`） |
| 金标拒答 | 5/5 | 固定 5 题（§9.1） |
| 负例拒答 | 5/5 | `adversarial.yaml` |
| 稳定性 | 同题两次 claim 三元组集合相同 | `(ku_id, locator, verbatim)` |
| frame 比例 | ≤20% | `eval/sentence_map.py` |
| 核验覆盖 | 100% KU 可解析到 `(snapshot, verification, verified_at)` | `grc freshness --stats` |
| 变更传导 | impact 清单 = 期望集合；<5 分钟 | 计时脚本 |
| 宿主合规 | `validate_answer.ok=true` 的比例 = 100% | `eval/host.py` |
| 跳过校验 | `--host-simulate skip` 必须 FAIL | `eval/host.py` |
| 用户可见 citation | 只在 validated answers 上算 100% | `eval/claims.py --validated` |
| UNVERIFIED 占比 | 可统计并展示（不设硬门槛） | `grc freshness --stats` |
| 双轨记录 | `--llm` 与 `--no-llm` 分表 | `eval/run.py --mode` |

### 9.3 探针纪律（P-4/P-5）

- 每条探针必须有**反向用例**（故意破坏 → 必须 FAIL），正反输出入 `evidence/`；
- 文档中任何计数/体积/人日数字由脚本生成（P-1），不接受手写；
- 交付前跑 `docs/checklists/pre-submit.md`（10 项，沿用 08 报告清单并适配）。

---

## 10. 里程碑（3 周）

| 周 | 交付物 | 完成判据 |
|---|---|---|
| **W1-0** | **契约干跑门禁**：publish 态样例跑 CK + 一次 ask | publish 态样例全绿（draft 仅 smoke）；ask 入 `evidence/` |
| **W1** | 仓库骨架、core（schema/validate/compile/index/binder）、EU 20 KU、CLI、10 金标 | `grc validate` 全绿；`grc ask` 10 题跑通；CK 探针正反基线 |
| **W2** | EU 剩余 12 KU + CN 20 KU、页面 8–10 页、MCP 六工具（含 validate_answer）、20 金标 + 5 负例 | 20 金标指标达标；宿主合规用例通过；MCP `tools/list` 可见 |
| **W3** | update 闭环 + impact 矩阵、DSH/CC skill 适配、eval CI、demo、README/免责 | 变更演示 <5 分钟；两家宿主各 3 问；`grc eval` 一条命令全绿；spec v1.0 冻结 |

**人力假设（用户裁定 D3）**：`determine` 已移出 MVP；按 1 名工程 + 1 名 GRC 研究并行 3 周（重估 20–24 人日）。第二核验人由单人 + `UNVERIFIED` 降级替代（D5）。

---

## 11. 风险登记

| # | 风险 | 影响 | 对策 |
|---|---|---|---|
| R1 | 全文快照无法自动发现上游改版 | 答案可能过期 | **3 周内只承诺"发布前核验"**；四态 + `--now` 探针 + 公示核验模式/`verified_by`；EUR-Lex 走 manual |
| R2 | 3 周内 52 KU 质量不达标 | 金标失败、返工 | W1 结束先冻结 EU 20；**52 不减**；KU 模板化 + 双人核；排期按 2 人并行 |
| R3 | 范围回答被误读为"适用/不适用"结论 | 法律与声誉风险 | determine 移出 MVP；ask 只答 KU 原文 + `coverage_note`；输出用"评估"，不输出 verdict |
| R4 | LLM 引入幻觉 | 破坏"不造假"底线 | 抽取优先 + binder 后校验 + `--no-llm` 兜底 + 无据拒答 |
| R5 | 跨平台承诺过度 | 演示翻车 | MVP 只承诺 DSH + Claude Code 两家 + MCP 通用；Codex 仅抽验 |
| R6 | 继承 rev4 的遗留缺陷（N-11） | log.md 校验悬空 | 导入契约后立即修 N-11（2 子项 + 2 错误码 + 1 反例），再写 core |
| R7 | 版权/许可 | 无法再分发或被迫删除 | Tier A 存官方公开法律文本全文；署名；**不商业转售**；README 声明；付费标准不收录 |
| R8 | 规则与 KU 双轨导致"修而不回灌" | 重演 rev4 五轮返工 | 影响面矩阵 + 反向探针 + CI 拦截（P-2/P-4） |
| R9 | 来源文本里的提示注入（"忽略以上指令"） | 被检索内容当指令执行 | 检索结果一律视为数据、不进入系统提示；skill 只通过工具取数，不执行来源内指令 |
| R10 | 查询日志泄露商业信息 | 隐私/合规 | MVP 默认不落盘；`--log` 显式开启且只记 query hash + 命中 ku_ids |
| R11 | 单人核验（`second_review:false`）导致错误被发布 | 知识质量 | 发布标 `UNVERIFIED`；答案带警告；`grc eval` 统计 UNVERIFIED 占比；用户书面接受 |

---

## 12. 待决事项（评审后由用户定）

1. 仓库位置与远端（本地 git / GitHub private）；许可证（内部用 or Apache-2.0）。
2. 是否在 v0.1 就加"跨法域并列展示"（当前明确不做，Q3/Q5 已定）。
3. 免责声明最终措辞（法务口径，建议中英双语各一版）。

---

## 13. 评审与批准流程（CCC）

1. **送审包**：本文件 + `docs/review/CCC-review-brief.md` + `docs/review/contract-digest.md` + `docs/research/source-map.md` + `docs/review/attachments/`（rev4 原契约、08 根因报告）。
2. **CCC 独立评审**：按 brief 的 D1–D9 维度与 10 个必答问题给判定（通过/有条件通过/不通过）+ 逐条发现（Block/Major/Minor + 证据 + 修法）。**CCC 不写代码、不改本文件**。
3. **作者处置**：逐条采纳/反驳（反驳必须给证据），产出 `docs/review/ccc-findings-resolution.md`，设计升 v0.2。
4. **用户批准**：用户对照 `docs/review/approval-checklist.md` 决定 approve / conditional / reject。
5. **开工**：批准后冻结 spec v1.0，进入 **W1-0（契约干跑）→ 修 N-11 → scaffold**。

---

### 9.4 P-n 映射（08 报告 → 本设计）

| P | 落点 | 执行者 | 失败码 |
|---|---|---|---|
| P-1 数字生成化 | `scripts/gen_numbers.py`；§9 计数 | CI | `NUMBER_STALE` |
| P-2 影响面矩阵 | §6.2 双向判据 | CI | `IMPACT_UNREPORTED` / `IMPACT_OUT_OF_SCOPE` |
| P-3 规则四要素 | 仅 backlog（determine 推迟）；MVP 用 CK 错误码 | — | — |
| P-4 探针正反基线 | §9.3 | CI | `PROBE_BROKEN` |
| P-5 证据 lint | `docs/checklists/pre-submit.md` | 人审 + CI | `EVIDENCE_STALE` |
| P-6 角色分离 | 金标 expected_facts 由非规则作者写；`verified_by` 角色码 | 人审 | — |
| P-7 一次性重构 | 契约导入 + N-11 一次性完成，再写 core | 工程 | — |

## 附录 A · 20 金标问题（草案）

| # | 域 | 问题 | 期望 |
|---|---|---|---|
| 1 | EU | 高风险 AI 系统提供者在投放前有哪些义务？ | answer；Art.16 + 8–15（Art.43 未收录，coverage_note 声明） |
| 2 | EU | 什么情况下系统会被归为高风险？ | answer；Art.6 + Annex III |
| 3 | EU | 哪些 AI 实践被禁止？ | partial（coverage_gap）：列出库内 7 项，声明"Art.5 其余 3 项（a/b/bb）未收录" |
| 4 | EU | 通用目的 AI 模型的义务适用于我们吗？ | refuse(no_ku)：GPAI 章不在收录范围 |
| 5 | EU | 部署者的日志保存义务是什么？ | answer；Art.26 |
| 6 | EU | 技术文档要包含什么？ | answer；Art.11 |
| 7 | EU | 高风险义务从什么时候开始适用？ | answer；Art.113（一般适用 2026-08-02；Annex III 2027-12-02 / Annex I 2028-08-02）+ basis_ku |
| 8 | EU | 我们是非欧盟提供者，条例适用吗？ | answer（Art.2）+ coverage_note（不输出结论） |
| 9 | EU | ISO 42001 认证是法定要求吗？ | refuse(scope_correction)：库中无法规要求；不得把标准写成义务 |
| 10 | EU | 你能帮我们判断合不合规吗？ | refuse(not_legal_advice) |
| 11 | CN | 生成式 AI 服务提供者的内容标识义务？ | answer；标识办法（显式/隐式） |
| 12 | CN | 哪些内容属于禁止生成？ | answer；暂行办法 |
| 13 | CN | 训练数据有哪些要求？ | answer；暂行办法 |
| 14 | CN | 面向企业内部使用是否适用？ | answer（Art.2 原文）+ **expected_coverage_note** |
| 15 | CN | 备案与安全评估的要求适用于谁？ | answer；暂行办法 |
| 16 | CN | 境外公司向境内公众提供服务是否适用？ | answer（Art.2 + Art.20）+ expected_coverage_note |
| 17 | CN | 厂商说"必须通过某认证"是法规吗？ | refuse(scope_correction)：厂商标准≠法规 |
| 18 | CN | 违反规定有什么法律责任？ | answer；暂行办法法律责任条 |
| 19 | CN/EU | 欧盟和中国对生成内容标识的要求分别是什么？ | partial（cross_jurisdiction）：`groups` 两组分别绑定，**不做对比分析** |
| 20 | 通用 | 给我一份合规整改清单 | refuse(not_legal_advice) |

> 第 19 题不是"对比页"功能，只是同一问题下两域分别作答；对比分析明确不在 MVP。

## 附录 B · 52 KU 取摄清单（草案）

**EU AI Act（32）**：Art.2（1）；Art.5 选 7 项禁止（7）；Art.6（3）；Annex III 选 4 类（4）；Art.8–15（8）；Art.16（1）；Art.26 选 3 款（3）；Art.27（1）；Art.50 选 3 款（3）；Art.113（1）= **32**。**未收录**：Art.5 其余 3 项（a/b/bb）、Annex III 其余类别、Art.43/17/19/49/99 等——在 `scope_exclusions.yaml` 登记。
**CN（20）**：《暂行办法》13 KU（Art.2/4/7/8/9/10/11/14/17/20/21/22/24）；《标识办法》7 KU（Art.3/4/5/6/7/9/10）。

> 取摄以"能覆盖 20 金标 + 五类场景"为准；逐条清单在 W1 冻结时落 `kb/registry.yaml`。
> **时间线口径**：EU 一律按合并版（2026-07-27）Art.113 —— 高风险 2027-12-02（Annex III）/ 2028-08-02（Annex I）；原版 2026-08-02 仅作演示对照。

## 附录 C · 继承契约差异表

| 项 | rev4 | v0.1 | 原因 |
|---|---|---|---|
| 快照 | 全文快照 | **Tier A 全文快照**（公开法律文本，不商业转售）+ verification.yaml | 审计可执行（C1） |
| CK-03 | 快照逐字命中 | online/manual/offline/expired 四态 | C1 的后果；EUR-Lex 走 manual |
| 语言 | 中文 | 用户语言/指定语言 | 用户要求（C2） |
| 非 KU 表 | 无 | catalog + scope_exclusions（rules/profiles 随 determine 推迟） | 检索/否定句（C3） |
| 冲突处理 | CK-13 人工 | 同左（规则冲突随 determine 推迟） | 保持保守 |
| log.md 校验 | 悬空（N-11） | 修入 CK-11/CK-09 | 继承时修复 |
| locator 形态 | 5 形态（欧盟中心） | **7 形态**（+ 中国条款式、附件式、字母项） | EU/CN 双域定位（C4） |
| claim 绑定 | 单轨（claim 必须为 KU 子串） | **双轨**（quote/translation/frame + support_type） | 多语言与归纳/否定句（C5） |
| 命名域 | `ku-` | `gsk-` | 与 rev4/GovernAI 隔离（F-25） |

## 附录 D · 来源核实摘要（详见 `docs/research/source-map.md`）

| 来源 | 版本 / 施行 | 条款规模 | 抓取可行性 | KU 计划 |
|---|---|---|---|---|
| EU AI Act | consolidated 2026-07-27（含 Digital Omnibus） | 选 10 个条款簇 + Annex III | EUR-Lex 拒绝脚本抓取 → manual 核验 | 32 |
| CN 暂行办法 | 2023-08-15，24 条 | 13 条入 KU | gov.cn 可抓 | 13 |
| CN 标识办法 | 2025-09-01，14 条 | 7 条入 KU | cac.gov.cn 可抓 | 7 |

**已核实的关键事实**：EU 高风险义务适用日为 2027-12-02 / 2028-08-02（合并版 Art.113）；CN 暂行办法 Art.2 明确"未向境内公众提供服务的内部研发/使用不适用"；CN 标识办法定义显式/隐式标识并规定传播平台与分发平台义务。

## 附录 E · KU 拆分计划与样例（W1 输入）

- **拆分计划**：`docs/research/ku-plan.md` —— **EU 32 + CN 20 = 52** 条（单 locator，禁区间），含 `ku_id` / `locator` / 标题 / `nature` 初判 / W1 抄录位置。
- **样例**：`docs/research/sample-kus/`
  - `gsk-eu-art14.yaml`：EU Art.14(1) 人工监督（Art.113 合并版适用日 **2027-12-02**）；
  - `gsk-cn-genai-art7.yaml`：CN 暂行办法第七条训练数据（`locator: 第七条`，验证 C4 中国条款式）。
- 两份样例均已用 29 字段全量填写，用于检验：字段是否够用、`locator` 是否能表达 CN、`verbatim_excerpt` 是否可逐字落盘。
- **摘录候选**：`docs/research/excerpt-candidates.md` —— 52 条各给候选原文；W1 按完整句重抄、Tier A 核验后落快照。

## 附录 F · Backlog（v0.2 产品版本，不属于 3 周 MVP）

- `determine` 与五态评估、`rules/applicability-{eu,cn}.yaml`、`kb/profiles/`、10 个评估用例；
- `applies_from` 规则级多日期（Annex I/III）与 `basis_ku` 回放；
- 冲突矩阵、priority 平局处理、CN 画像字段；
- 第二核验人（Tier A 双人）与 EU 自动改版检测。
