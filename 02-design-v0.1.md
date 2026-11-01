# GRC Skill Agent · 设计 v0.1（送 CCC 评审）

> 状态：**草案，待独立评审（CCC）→ 用户批准** ｜ 日期：2026-10-31 ｜ 项目：grc-skill-agent
> 自检：已完成 spec 自检（9 处内部不一致已修，记录见 `docs/review/spec-self-review.md`），此后版本为送审版。
> 上游依据：本项目继承 `ai-grc-kb-v2-p0-rev4` 的知识契约（下称 rev4），并吸收 `08-四轮缺陷聚类与流程改进建议.md` 的五条根因与 P-1~P-7。
> 与其它项目关系：**独立仓库、独立命名空间；与 GovernAI / AI-GRC-Consultant 零文件共享、零术语借用**。
> 本文是唯一设计基线；评审意见按 §13 流程处置后升 v0.2。

---

## 0. 一页摘要

**做什么**：一个可安装的 Agent 能力包——以可审计 GRC 知识库为核心，提供（1）来源消化与知识更新、（2）带逐句引用的问答、（3）适用性三态判定与义务清单；通过 **MCP + Skill** 跨平台输出。

**不做什么**：不输出"合规/不合规"结论、不评分、不构成法律意见；MVP 不做自动爬虫、Web UI、多租户、跨法域对比页、向量检索。

**MVP 规模**：3 周；EU AI Act（Art.5 / 6+Annex III / 8–15 / 26–27 / 50）约 30 KU + 中国《生成式人工智能服务管理暂行办法》与《人工智能生成合成内容标识办法》约 20 KU；20 个金标问答；citation 覆盖 100%；无据必拒答；改 1 条 KU 后 5 分钟内给出过期页清单。

**三个关键设计取舍**：
1. **判定是"适用性"不是"合规性"**：三态（适用/不适用/信息不足）+ 义务清单 + 免责，判定由确定性规则引擎执行，LLM 不参与判定。
2. **答案先抽取后措辞**：断言必须绑定 KU + locator + 原文；绑定失败即删句，删完不成立即拒答；LLM 只做意图解析与措辞。
3. **快照只存摘录 + 链接**：不重分发全文；CK-03 改为四态（online / manual / offline / expired），答案显式标注核验模式、核验人与访问时间。

---

## 1. 背景与目标

### 1.1 为什么现在做

rev1→rev4 五轮把一个"法条 → KU → 派生页 → 校验"的可审计知识契约修到了只剩 1 个 Block。它证明了三件事：
- **契约可行**：29 字段 KU、六类派生页、CK-01~13、双哈希、log/refs 在被反复攻击后仍然站得住；
- **失败模式清楚**：五轮 100 条缺陷里没有一条需要重做架构，全部是"规则与载体脱节、判据缺失、仪器污染、元信息漂移、自评替代复核"（08 报告 G-1~G-5）；
- **缺的是运行体**：rev4 没有编译器、没有校验器、没有检索与问答——它是"设计包"，不是"能力"。

本项目的目标就是把这份契约变成**能更新、能回答、能判定、能跨平台安装**的 Agent 能力。

### 1.4 来源版本（2026-10-31 已核实）

- **EU**：`Regulation (EU) 2024/1689`，采用 **consolidated as at 2026-07-27**（含 Digital Omnibus on AI，OJ L 2026/01744）。高风险义务适用日按合并版为 **2027-12-02（Annex III）/ 2028-08-02（Annex I）**，不是原版的 2026-08-02。
- **CN**：《生成式人工智能服务管理暂行办法》（2023-08-15 施行，24 条）；《人工智能生成合成内容标识办法》（2025-09-01 施行，14 条）。
- **CN 定位**：CN 法规以"第 X 条"定位，rev4 的 5 形态无法表达 → 本设计新增第 6 形态（C4）。
- 条款地图、KU 拆分计划与抓取可行性见 `docs/research/source-map.md`、`eu-article-map.md`、`cn-article-map.md`、`ku-plan.md`（附录 D/E 摘要）。

### 1.2 目标（可验收）

| # | 目标 | 验收 |
|---|---|---|
| G1 | 消化：新增/修订来源可进入知识库，且不破坏既有契约 | `grc ingest → validate → compile` 全绿；变更影响面清单可复现 |
| G2 | 回答：问题→带引用答案；无据必拒答 | 20 金标 citation 覆盖 100%；5 个负例全部拒答 |
| G3 | 判定：画像→适用性三态 + 义务清单 + 免责 | 10 个判定用例（适用/不适用/信息不足/超范围）全对 |
| G4 | 跨平台：同一能力在两类 Agent 宿主可用 | DSH 与 Claude Code 各跑通 3 个问题；MCP `tools/list` 六工具可发现 |
| G5 | 更新可演示：改 1 条 KU 后 5 分钟内检出 | `grc impact` 输出受影响页 + 过期 KU；重编译后问答引用同步 |

### 1.3 非目标（MVP 明确不做）

合规结论/风险评分/法律意见；自动爬虫与定时 watcher；Web UI / HTTP 服务；多租户与鉴权；跨法域对比页；向量检索；自动撰写叙事段（永久排除）；对来源全文的再分发。

**来源级排除（明确不在 50 KU 内）**：EU AI Act 的 GPAI 章（Art.53–55）、罚则（Art.99）、附件 IV–XIII 细则、成员国转化立法；中国《算法推荐管理规定》《深度合成规定》（只收《标识办法》）；执法案例与处罚决定。

---

## 2. 用户与场景

### 2.1 用户

| 角色 | 他们问什么 | MVP 支持 |
|---|---|---|
| 合规/法务 | "这条法规要求我做什么？依据哪句？" | ✅ 义务清单 + 原文 + 适用性 |
| 产品/工程 | "我们要上线 X，哪些条款会管到？" | ✅ 画像 → 适用性三态 |
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
- CN：我们做的是企业内部知识库问答，算不算"向境内公众提供生成式 AI 服务"？（应给"信息不足/需按画像细分"）
- 陷阱题：某厂商白皮书说"必须通过 ISO 42001 认证"——这是法规要求吗？（应拒答/纠正范畴）

---

## 3. 范围与交付形态

### 3.1 In Scope（3 周）

| 类别 | 内容 |
|---|---|
| 知识 | EU ~30 KU（Art.2 适用范围、Art.5 禁止、Art.6+Annex III 分类、Art.8–15 义务链、Art.16/43 合格评定、Art.26/27 部署者、Art.50 透明度、Art.113 时间线）+ CN ~20 KU（暂行办法按条 + 标识办法）；六类页面实际生产 concept/entity/overview/topic/source 五类（comparison 保留不用） |
| 能力 | MCP 六工具（只读）：`search_kus` `get_ku` `get_page` `ask` `determine` `freshness`；CLI `grc` 另有 `ingest/validate/compile/impact/publish/verify-source`（写操作不对 Agent 暴露） |
| 更新 | registry + 摘录快照 + fingerprint + impact 矩阵 + log.md/refs.json + 人审签署 |
| 分发 | `skills/grc-agent/SKILL.md`（DSH 与 Claude Code 共用体）+ Codex `AGENTS.md` 适配说明 |
| 评估 | 20 金标 + 5 拒答负例 + 10 判定用例 + 变更传导脚本；`grc eval` 一条命令跑完 |

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
摘录快照 snapshots/<id>.md（摘录 + 原文链接 + accessed_at + excerpt_hash）
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
   determine/freshness               impact/publish/verify-source
              │
   DSH SKILL.md · Claude Code SKILL.md · Codex AGENTS.md
```

### 4.2 组件边界

| 组件 | 职责 | 依赖 | 可独立测试 |
|---|---|---|---|
| `grc_core.schema` | KU/页面/registry/profile 的结构与取值域 | 无 | ✅ 单测 |
| `grc_core.validate` | CK-01~13（MVP 全实现；CK-13 冲突存在性人工） | schema | ✅ 夹具 |
| `grc_core.compile` | KU → 派生块/页面渲染、双哈希、refs.json | schema | ✅ 黄金文件 |
| `grc_core.index` | BM25 + 元数据过滤（jurisdiction/topic/type） | compile 产物 | ✅ |
| `grc_core.answer` | 断言-引用绑定、答案组装、拒答、语言与免责 | index | ✅ 金标 |
| `grc_core.determine` | 画像 → 适用性三态 + 义务清单（规则引擎） | schema+rules | ✅ 判定用例 |
| `grc_core.ingest/impact/freshness` | 来源登记、fingerprint、影响面、过期检测 | 全部 | ✅ |
| `grc_mcp` | MCP stdio 协议、工具注册、入参校验 | core | ✅ 协议测试 |
| `skills/grc-agent` | 触发与流程编排（何时 ask / determine / ingest） | MCP 或 CLI | ✅ 手工 |
| `grc_core.eval` | 金标/负例/判定/传导 | 全部 | ✅ CI |

**硬边界**：MCP 与 CLI 不复制业务逻辑；skill 不复制规则，只编排；核心包零第三方运行时依赖（MCP 用标准库手写 JSON-RPC stdio），保证离线可跑、跨宿主可装。

**索引**：ASCII 按词、CJK 按**字符二元组（bigram）**，标题与 catalog 别名加权；不引入第三方分词。

### 4.2.1 MCP 工具契约（MVP）

| 工具 | 入参 | 出参 | 主要错误 |
|---|---|---|---|
| `search_kus` | `{query, jurisdiction?, doc_type?, top_k=5}` | `{hits:[{ku_id,title,jurisdiction,locator,snippet,score}]}` | `INVALID_INPUT` |
| `get_ku` | `{ku_id}` | `{ku: 完整 YAML}` | `NOT_FOUND` |
| `get_page` | `{slug}` | `{markdown, front_matter}` | `NOT_FOUND` |
| `ask` | `{query, language?, jurisdiction?, no_llm?}` | 见 §7.1 | `NO_KU` / `OUT_OF_SCOPE` / `INVALID_INPUT` |
| `determine` | `{profile}` | 见 §8.2 | `INVALID_INPUT` / `INSUFFICIENT_PROFILE` |
| `freshness` | `{ku_ids?}` | `{oldest_as_of, expired_ku_ids, verification}` | `NOT_FOUND` |


**MCP 协议面**：仅实现 `initialize` / `tools/list` / `tools/call` / 标准错误对象；不实现 resources、prompts、sampling（MVP 不需要，列入 v0.2）。

**边界**：`impact` 是运维动作，**只在 CLI**（`grc impact`），不通过 MCP 暴露给 Agent —— 最小权限，Agent 不能触发写操作。

### 4.3 跨平台策略

| 宿主 | 接入方式 | MVP 验证 |
|---|---|---|
| DSH | `~/.agents/skills/grc-agent/`（SKILL.md + MCP 配置） | 3 问 + determine 1 例 |
| Claude Code | `.claude/skills/grc-agent/` 或用户级 skills | 3 问 + determine 1 例 |
| 其它 MCP 宿主（Codex/Cursor 等） | 仅需 MCP server 配置 | `tools/list` + 1 问（抽验） |

---

## 5. 数据契约（继承 rev4 + 三处变更）

### 5.1 原样继承（不重新发明）

- **KU 29 字段** = 17 fact-bearing（#2–#18）+ 12 bookkeeping（#1 + #19–#29）；`instrument_type` 11 值闭合；`locator` 5 形态；`gap` 为登记对象不入 29。
- **六类页面**必备段、`kb:derived` / `kb:table` 语法、`render_hash` / `ku_hash` 计算、`rendered_blocks` 与块 id 规则、结构声明行白名单（3 字段）。
- **13 条校验** CK-01~13；WS-01~09；DF-1~6 / DF-4b / DF-4c 与 EX-1~7；front-matter 8 键；`log.md` 4 列；`refs.json` 4 键。
- **08 根因对策**：P-1 数字/命名生成化；P-2 变更影响面矩阵；P-3 规则四要素（判定主体/输入/闭合值域/错误码）；P-4 探针正反基线；P-5 证据 lint。

### 5.2 三处变更（本次新增，需 CCC 重点挑战）

| # | 变更 | 理由 | 影响 |
|---|---|---|---|
| **C1** | 快照只存**摘录片段 + 原文链接 + accessed_at + excerpt_hash**，不存全文 | 不重分发全文；满足"可追溯"而非"可再分发" | CK-03 从"摘录必须在快照中逐字命中"改为**四态**（online / manual / offline / expired，见 §5.3）；答案必须公示核验模式。**这 4 项元数据不新增 KU 字段**，落在 registry 条目与快照文件头 |
| **C2** | 答案语言 = 用户语言或指定语言；原文引用恒为原文 | 用户要求 | 答案对象增 `language`；译文单列并标注 |
| **C3** | 新增三张**非 KU** 表：`catalog.yaml`（主题/别名→ku_id）、`rules/applicability-{eu,cn}.yaml`（适用性规则）、`kb/profiles/`（判定画像样例） | 检索与判定所需，不污染 29 字段契约 | CK-09 字段集校验不涉及它们；新增 lint 保证"非 KU 表不承载事实" |
| **C4** | `locator` 增第 6 形态「中国条款式」：`^第[一二三四五六七八九十百零〇\d]+条(之[一二三四五六七八九十])?$`（款/项以 `snapshot_ref` 锚点表达） | rev4 的 5 形态是欧盟中心；CN 法规的"第七条"无法表达 | CK-01 对 CN KU 的 locator 校验；CK-03 沿用锚点；样例见附录 E |

### 5.3 CK-03 的四态（C1 的直接后果）

**元数据放在哪（避免第 30 个字段）**：

| 位置 | 存放 | 说明 |
|---|---|---|
| KU 文件 | 仅 29 字段；`verbatim_excerpt` 必须与快照摘录逐字相等 | KU 侧是镜像，不是第二事实源 |
| `snapshots/<id>.md` 文件头 | `source_url` / `accessed_at` / `excerpt_hash` / `verification` / `verified_at` / `verified_by` | 摘录原文的唯一存放处 |
| `registry.yaml` 条目 | 同名字段 + `source_class` / `tier` / `status` | 来源级状态 |

- `excerpt_hash = sha256(normalize(摘录原文))`；`normalize` = 去行尾空白 → 空白折叠 → UTF-8。
- **单一事实源**：摘录原文只存快照文件；KU 的 `verbatim_excerpt` 是它的镜像。CK-03 第一项校验二者逐字相等（防 v1 的"同一事实两处"），第二项校验 `excerpt_hash` 自洽。
- **online**：脚本抓取 `source_url` 成功，且摘录为原文连续子串 → `verification: online` + `verified_at`。**仅对可稳定抓取的来源启用**（EUR-Lex 实测拒绝脚本抓取，见 source-map §6）。
- **manual**：人工打开官方页面核对摘录，记录 `verified_by`（实名）+ `verified_at` + 截图或页面 hash → `verification: manual`。**MVP 默认模式**。
- **offline**：只做"KU↔快照相等 + excerpt_hash 自洽" → `PASS(offline)`；答案显示"未核验（as_of=…）"。
- **expired**：超过 `freshness.max_age_days`（默认 90）未核验 → 答案降级为 `partial` 并提示可能过期。
- **已知限制**：离线模式无法发现上游改版；MVP 用 `grc verify-source --all`（手动触发 / CI 周检）缓解，不声称自动追踪。

### 5.4 目录与命名

```
grc-skill-agent/
├── AGENTS.md / README.md
├── pyproject.toml
├── src/grc_core/{schema,validate,compile,index,answer,determine,ingest,impact,freshness,eval}.py
├── src/grc_mcp/server.py
├── skills/grc-agent/{SKILL.md,references/{answer-contract,determination,ingest}.md}
├── kb/
│   ├── ku/*.yaml                 # gsk-eu-* / gsk-cn-*
│   ├── pages/*.md
│   ├── snapshots/*.md            # 摘录 + 链接，非全文
│   ├── catalog.yaml
│   ├── registry.yaml
│   ├── log.md
│   └── refs.json
├── rules/applicability-{eu,cn}.yaml
├── eval/{golden.yaml,adversarial.yaml,determination.yaml,run.py}
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
  source_url: "https://eur-lex.europa.eu/..."
  snapshot_ref: "snapshots/eu-ai-act.md"
  accessed_at: 2026-10-31
  excerpt_hash: "sha256:…"
  verification: manual
  verified_by: "R-2 / 张三"
  status: published
```

**catalog.yaml（检索索引，不承载事实）**：`topics: {high-risk: [gsk-…], prohibited: […]}`、`aliases: {…}`。只允许 `ku_id` 与标签；出现义务性句子即 lint 失败（`NON_KU_FACT`）。

---

## 6. 知识生产流水线

### 6.1 六步（每步有人审闸门）

| 步 | 命令 | 产物 | 闸门 |
|---|---|---|---|
| 1 登记 | `grc ingest register <id> --url <url>` | registry 条目（source_class/tier/jurisdiction） | 来源性质与等级人工定 |
| 2 摘录 | `grc ingest excerpt <id> --locator <loc>` | 摘录快照 + excerpt_hash | 逐字人工核对（Tier A 双人） |
| 3 入库 | `grc ingest draft <id>`（可选 LLM 起草） | KU YAML 草稿 | 人工改毕、`gap` 登记 |
| 4 校验 | `grc validate [--ku <id>]` | 错误清单 | CK 全绿；CK-13 冲突人工签署 |
| 5 编译 | `grc compile --changed` | 派生页 + 双哈希 + refs.json | 渲染差异人工审 |
| 6 发布 | `grc publish` | log.md 追加 + registry.published | Tier A 签署记录 |

### 6.2 影响面矩阵（P-2 落地）

每次规则/契约/样例变更，必须先在 `docs/impact-matrix.md` 登记：
`变更 id → 影响文件（KU/页/模板/规则/金标）→ 处理动作 → 实测输出（命令+结果）`。
CI 检查：变更文件集 ⊆ 矩阵中申报的文件集，否则 `IMPACT_UNREPORTED` 失败。目标是把 rev4 的"修而不回灌"变成机器拦截。

### 6.3 演示脚本（验收用）

```
1. 改 `kb/ku/gsk-eu-art6-high-risk.yaml` 的 `effective_date` / `transition_note`
   （演示素材：合并版 Art.113 → 2027-12-02；若误用原版 2026-08-02，改回即触发传导）
2. grc impact → 输出受影响页（预计 2 页）+ 过期 KU + 需重编译对象；计时
3. grc compile --changed && grc validate && grc publish
4. grc ask "高风险系统什么时候开始适用？" → 答案日期与引用同步更新
   目标：第 1→4 步 < 5 分钟（不含人审思考）
```

---

## 7. 答案契约

### 7.1 输出对象（MCP `ask` 返回）

```json
{
  "mode": "answer|partial|refuse",
  "language": "zh",
  "translations": [],
  "answer": "……",
  "claims": [
    {"span": "……", "ku_ids": ["gsk-eu-art14-oversight"], "locator": "Art.14(1)",
     "verbatim": "……", "as_of": "2026-10-31", "verification": "manual"}
  ],
  "citations": [
    {"ku_id": "...", "title": "...", "source_class": "primary", "tier": "A",
     "jurisdiction": "EU", "locator": "Art.14(1)", "source_url": "https://...",
     "accessed_at": "2026-10-31", "verification": "manual"}
  ],
  "freshness": {"oldest_as_of": "2026-10-31", "expired_ku_ids": []},
  "refusal": {"reason": "no_ku|out_of_scope|insufficient_profile|conflict_unresolved|not_legal_advice",
               "missing": "……"},
  "disclaimer": "本回答仅基于所收录来源与所提供信息，不构成法律意见。"
}
```

`translations` 仅在用户要求译文时出现：`[{"lang":"en","text":"…","source":"machine"}]`；`citations[].verbatim` 永不翻译。

### 7.2 六条硬规则

1. **无据不成句**：每个 claim 必须绑定 ≥1 KU；绑定失败 → 删句；删后答案不成立 → `refuse`。
2. **无 KU 即拒答**：检索无命中 → `refuse(no_ku)`，并说明"库中未收录/需要哪类来源"。
3. **冲突不消解**：未登记冲突 → 列双方，`mode=partial`；已登记 open 冲突 → 提示 `CFL-*`。
4. **来源分层**：`vendor`/`analyst` 不得支撑义务性断言；`tier C` 不得作事实源。
5. **不做法律意见**：合规结论、执法预测、责任判断一律拒绝并说明边界。
6. **必带元信息**：`as_of`（最旧）、`verification`（online/manual/offline/expired）、`verified_by`（manual 时必填）、免责声明。

### 7.3 实现路线（防幻觉）

- **抽取优先**：先由 core 从 KU/页面检索出候选 claim 片段（原文/义务条目/定义），答案骨架由模板生成；
- **LLM 仅做两件事**：意图解析（问题→检索参数/画像槽位）与措辞（在已绑定 claim 上改写，不得引入新事实）；
- **后校验**：`answer_binder` 校验每条 claim 的 span 是否为对应 KU 字段的**连续子串**，且实体/数字/日期逐字一致；不一致即删句，删后不成立则回退抽取式答案；binder 失败计入 `eval` 的 `unsupported_claims`；
- **可关**：`--no-llm` 模式完全抽取式（CI 与离线演示用）。

---

## 8. 适用性判定（`determine`）

### 8.1 输入画像（profile）

```yaml
jurisdiction: EU | CN
role: provider | deployer | importer | distributor | user
entity: company | public_authority | research | individual
system:
  is_ai_system: true
  is_general_purpose: false
  domains: [biometrics, education, employment, ...]
  use_cases: [social_scoring, real_time_remote_biometric_id, ...]
timeline:
  placing_on_market: 2026-08-02
  in_service: 2026-08-02
org:
  size: sme | large
```

### 8.2 输出

```json
{"verdict": "applies|does_not_apply|insufficient_info|out_of_scope",
 "findings": [
   {"ku_id": "gsk-eu-art5-prohibited", "locator": "Art.5(1)(f)",
    "reason": "use_cases 命中'实时远程生物识别'；角色为 deployer",
    "obligations": ["……"], "citations": ["..."]}
 ],
 "missing_fields": ["system.domains"],
 "disclaimer": "本判定仅基于所收录来源与所提供画像，不构成法律意见；最终适用性以监管解释/司法认定为准。"}
```

**义务清单的来源**：`obligations` 只能取自该 KU 的 `obligation` 字段（按 `applies_to.subject` 过滤），不得由 LLM 归纳；一条归纳句必须拆成多条 claim，各自绑定。

### 8.3 规则引擎

- 每条适用性规则是 YAML：`id / ku_ids / jurisdiction / applies_when（字段-运算符-值）/ obligations_from（KU 字段路径）/ priority / exceptions`；
- 运算符仅 `eq/neq/in/not_in/lt/gte/exists`；禁止脚本表达式（可审计、可回放）；
- 规则冲突 → `insufficient_info` + 冲突 id 列表，**不自动择一**；
- 判定结果必须能逐步回放到 KU 与规则行（`--explain` 输出推导链）。

### 8.4 边界（写死）

- 不输出"合规/不合规/风险分值"；
- 画像缺字段 → `insufficient_info`，不得猜测；
- `out_of_scope`：法域未收录（如 SG/US）或对象非 AI 系统；
- 所有输出必带免责声明；`SKILL.md` 禁止在未调用 `determine` 时凭 LLM 自行判定。

---

## 9. 评估与质量门禁

### 9.1 金标集（20 题）

结构：`id / 问题 / 期望 mode / 期望 citation ku_ids / 期望拒答理由 / 禁出现内容（如"合规""必须"误用）`。
覆盖：EU 10 / CN 10；事实 6、义务 5、范围 4、跨条 2、拒答 3（含厂商宣称、超范围、法律意见）。**金标在 W1 结束前冻结**（打 tag），W2 只增不改。

### 9.2 指标（CI 门禁）

| 指标 | 目标 | 判定 |
|---|---|---|
| citation 覆盖率 | 100% claims 有 KU | `grc eval` |
| 无据断言 | 0 | 同上 |
| 拒答正确率 | 5/5 负例全拒 | 同上 |
| citation 稳定性 | 同题两次结果一致 | 同题重跑 diff |
| 判定正确率 | 10/10 判定用例 | `eval/determination.yaml` |
| 变更传导 | impact 清单 = 期望集合；<5 分钟 | 计时脚本 |
| 核验覆盖 | 100% KU 有 `verification` + `verified_at`/`verified_by` | `grc freshness` |
| 契约校验 | CK 全绿、refs 对账 19→50 边 | validate |

### 9.3 探针纪律（P-4/P-5）

- 每条探针必须有**反向用例**（故意破坏 → 必须 FAIL），正反输出入 `evidence/`；
- 文档中任何计数/体积/人日数字由脚本生成（P-1），不接受手写；
- 交付前跑 `docs/checklists/pre-submit.md`（10 项，沿用 08 报告清单并适配）。

---

## 10. 里程碑（3 周）

| 周 | 交付物 | 完成判据 |
|---|---|---|
| **W1** | 仓库骨架、core（schema/validate/compile/index）、EU 20 KU、CLI、10 金标 | `grc validate` 全绿；`grc ask` 10 题跑通；CK 探针正反基线 |
| **W2** | EU 30 KU + CN 20 KU、页面 8–10 页、`determine`、MCP 六工具、20 金标 + 负例 | 20 金标指标达标；determine 10 用例通过；MCP `tools/list` 可见 |
| **W3** | update 闭环 + impact 矩阵、DSH/CC skill 适配、eval CI、demo、README/免责 | 变更演示 <5 分钟；两家宿主各 3 问；`grc eval` 一条命令全绿；v0.1 冻结 |

**人力假设**：1 名工程（兼 core/MCP）+ 1 名 GRC 研究（KU 录入与 Tier A 核验）+ 用户本人做判定规则签署；若只有 1 人，CN 侧砍到 15 KU、金标 15 题（仍在范围声明内）。

---

## 11. 风险登记

| # | 风险 | 影响 | 对策 |
|---|---|---|---|
| R1 | 摘录快照无法发现上游改版（C1 的代价） | 答案可能过期 | 四态核验（online/manual/offline/expired）+ CI 周检 + 答案公示核验模式与 `verified_by`；EUR-Lex 走 manual |
| R2 | 3 周内 50 KU 质量不达标 | 金标失败、返工 | W1 结束先冻结 EU 20；CN 允许 15–20 弹性；KU 模板化 + 双人核 |
| R3 | 适用性判定被误读为法律意见 | 法律与声誉风险 | 三态 + 免责 + 不评分 + 只回放规则 + 输出统一加"非法律意见" |
| R4 | LLM 引入幻觉 | 破坏"不造假"底线 | 抽取优先 + binder 后校验 + `--no-llm` 兜底 + 无据拒答 |
| R5 | 跨平台承诺过度 | 演示翻车 | MVP 只承诺 DSH + Claude Code 两家 + MCP 通用；Codex 仅抽验 |
| R6 | 继承 rev4 的遗留缺陷（N-11） | log.md 校验悬空 | W1 第一件事：修 N-11（CK-11/CK-09 承接 log.md）再开工 |
| R7 | 版权/许可 | 无法再分发或被迫删除 | 只存摘录 + 链接；署名；不内置付费标准全文；README 声明 |
| R8 | 规则与 KU 双轨导致"修而不回灌" | 重演 rev4 五轮返工 | 影响面矩阵 + 反向探针 + CI 拦截（P-2/P-4） |
| R9 | 来源文本里的提示注入（"忽略以上指令"） | 被检索内容当指令执行 | 检索结果一律视为数据、不进入系统提示；skill 只通过工具取数，不执行来源内指令 |
| R10 | 查询日志泄露商业信息 | 隐私/合规 | MVP 默认不落盘；`--log` 显式开启且只记 query hash + 命中 ku_ids |

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
5. **开工**：批准后冻结 spec v1.0，进入 W1（先修 N-11，再 scaffold）。

---

## 附录 A · 20 金标问题（草案）

| # | 域 | 问题 | 期望 |
|---|---|---|---|
| 1 | EU | 高风险 AI 系统提供者在投放前有哪些义务？ | answer；Art.16 + 8–15 + 43 |
| 2 | EU | 什么情况下系统会被归为高风险？ | answer；Art.6 + Annex III |
| 3 | EU | 哪些 AI 实践被禁止？ | answer；Art.5 |
| 4 | EU | 通用目的 AI 模型的义务适用于我们吗？ | refuse(no_ku)：GPAI 章不在收录范围 |
| 5 | EU | 部署者的日志保存义务是什么？ | answer；Art.26 |
| 6 | EU | 技术文档要包含什么？ | answer；Art.11 |
| 7 | EU | 高风险义务从什么时候开始适用？ | answer；Art.113（合并版：2027-12-02 / 2028-08-02）+ effective_date |
| 8 | EU | 我们是非欧盟提供者，条例适用吗？ | answer；Art.2 |
| 9 | EU | ISO 42001 认证是法定要求吗？ | refuse/纠正：库中无法规要求；不得把标准写成义务 |
| 10 | EU | 你能帮我们判断合不合规吗？ | refuse(not_legal_advice) |
| 11 | CN | 生成式 AI 服务提供者的内容标识义务？ | answer；标识办法（显式/隐式） |
| 12 | CN | 哪些内容属于禁止生成？ | answer；暂行办法 |
| 13 | CN | 训练数据有哪些要求？ | answer；暂行办法 |
| 14 | CN | 面向企业内部使用是否适用？ | insufficient（缺画像）或按 Art.2 回答 |
| 15 | CN | 备案与安全评估的要求适用于谁？ | answer；暂行办法 |
| 16 | CN | 境外公司向境内公众提供服务是否适用？ | answer/insufficient；Art.2 |
| 17 | CN | 厂商说"必须通过某认证"是法规吗？ | refuse/纠正：厂商标准≠法规 |
| 18 | CN | 违反规定有什么法律责任？ | answer；暂行办法法律责任条 |
| 19 | CN/EU | 欧盟和中国对生成内容标识的要求分别是什么？ | partial：两组分别列，**不做对比分析** |
| 20 | 通用 | 给我一份合规整改清单 | refuse(not_legal_advice) |

> 第 19 题不是"对比页"功能，只是同一问题下两域分别作答；对比分析明确不在 MVP。

## 附录 B · 50 KU 取摄清单（草案）

**EU AI Act（30±3）**：Art.5(1) 禁止实践（6–8 KU）；Art.6 + Annex III 高风险分类（5–6）；Art.8–15 提供者义务链（8–10）；Art.16/43 合格评定与 CE（2–3）；Art.26 部署者义务（3–4）；Art.27 FRIA（1–2）；Art.50 透明度（2–3）；Art.113 时间线（1）；Art.2 适用范围（1）。
**CN（~20）**：《生成式人工智能服务管理暂行办法》按条拆 14–16 KU（含备案/安全评估、法律责任各 1 条）；《人工智能生成合成内容标识办法》6–8 KU（显式/隐式标识、平台责任、用户提示）。

> 取摄以"能覆盖 20 金标 + 五类场景"为准；逐条清单在 W1 冻结时落 `kb/registry.yaml`。
> **时间线口径**：EU 一律按合并版（2026-07-27）Art.113 —— 高风险 2027-12-02（Annex III）/ 2028-08-02（Annex I）；原版 2026-08-02 仅作演示对照。

## 附录 C · 继承契约差异表

| 项 | rev4 | v0.1 | 原因 |
|---|---|---|---|
| 快照 | 全文快照 | 摘录 + 链接 + hash | 版权与体积（C1） |
| CK-03 | 快照逐字命中 | online/manual/offline/expired 四态 | C1 的后果；EUR-Lex 走 manual |
| 语言 | 中文 | 用户语言/指定语言 | 用户要求（C2） |
| 非 KU 表 | 无 | catalog/rules/profiles | 检索与判定（C3） |
| 冲突判定 | CK-13 人工 | 同左 + 规则冲突不择一 | 保持保守 |
| log.md 校验 | 悬空（N-11） | 修入 CK-11/CK-09 | 继承时修复 |
| locator 形态 | 5 形态（欧盟中心） | **6 形态**（+ 中国条款式） | CN 法规定位（C4） |

## 附录 D · 来源核实摘要（详见 `docs/research/source-map.md`）

| 来源 | 版本 / 施行 | 条款规模 | 抓取可行性 | KU 计划 |
|---|---|---|---|---|
| EU AI Act | consolidated 2026-07-27（含 Digital Omnibus） | 选 10 个条款簇 + Annex III | EUR-Lex 拒绝脚本抓取 → manual 核验 | 30±3 |
| CN 暂行办法 | 2023-08-15，24 条 | 14 条入 KU | gov.cn 可抓 | 14–16 |
| CN 标识办法 | 2025-09-01，14 条 | 8 条入 KU | cac.gov.cn 可抓 | 6–8 |

**已核实的关键事实**：EU 高风险义务适用日为 2027-12-02 / 2028-08-02（合并版 Art.113）；CN 暂行办法 Art.2 明确"未向境内公众提供服务的内部研发/使用不适用"；CN 标识办法定义显式/隐式标识并规定传播平台与分发平台义务。

## 附录 E · KU 拆分计划与样例（W1 输入）

- **拆分计划**：`docs/research/ku-plan.md` —— EU 33 + CN 20 = **53** 条，含 `ku_id` / `locator` / 标题 / `obligation_nature` 初判 / W1 抄录位置；每条在 W1 按 29 字段填充并做 Tier A 核验。
- **样例**：`docs/research/sample-kus/`
  - `gsk-eu-art14.yaml`：EU Art.14(1) 人工监督（Art.113 合并版适用日 **2027-12-02**）；
  - `gsk-cn-genai-art7.yaml`：CN 暂行办法第七条训练数据（`locator: 第七条`，验证 C4 第 6 形态）。
- 两份样例均已用 29 字段全量填写，用于检验：字段是否够用、`locator` 是否能表达 CN、`verbatim_excerpt` 是否可逐字落盘。
- **摘录候选**：`docs/research/excerpt-candidates.md` —— 53 条各给候选原文（截断 420 字）；W1 按完整句重抄、Tier A 核验后落快照。
