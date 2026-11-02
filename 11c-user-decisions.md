# 用户决策日志（running log）

> 规则：**只追加、不覆盖**。每条决策有稳定 ID；状态：`confirmed` / `superseded` / `open`。
> 维护人：DSH。每次用户做出新选择，追加一行并更新相关设计/计划文档。
> 最后更新：2026-11-01

## 索引

| 范围 | 决策 |
|---|---|
| 知识契约/快照 | D-001、D-004、D-005 |
| 答案契约 | D-002、D-008、D-013、D-017 |
| 范围/判定 | D-003、D-006、D-014、D-015、D-016、D-018 |
| 排期/流程 | D-009、D-010、D-011、D-019 |
| 评审 | D-012 |
| 本日志 | D-020 |

---

## 1. 知识契约与数据

| ID | 日期 | 问题 | 用户选择 | 影响/落点 |
|---|---|---|---|---|
| D-001 | 2026-10-31 | 快照策略：只存摘录 vs Tier A 全文 | **A. Tier A 全文快照**（仅本地，不随包/不公开；发布只带 `fulltext_sha256` 与核验记录） | 设计 C1；`kb/snapshots/`；`verification.yaml` |
| D-004 | 2026-10-31 | PyYAML 版本策略 | **A. 固定 PyYAML 6.0.2** | `pyproject.toml`/环境文档；W1 实现 |
| D-005 | 2026-10-31 | 第二核验人 | **B. 单人核验 + `UNVERIFIED`** | 设计 §5.3/§11；21 KU 当前均 UNVERIFIED |

## 2. 答案契约

| ID | 日期 | 问题 | 用户选择 | 影响/落点 |
|---|---|---|---|---|
| D-002 | 2026-10-31 | 宿主如何成文 | **A. 宿主只能从 core 候选句中选句/排序，不得改写**；`final_text` 逐字拼接 | 设计 §7；`answer.py`/`validate_answer.py`；服务端 token |
| D-008 | 2026-11-01 | 是否保留机器译文 | **删除**（MVP 无 `translations` / `binding_mode=translation`） | 设计 v0.8 §3.3/§7；W1-6.2 回归 |
| D-013 | 2026-11-01 | 多法域如何处理 | **先判法域；只含适用法域；不确定先问；多法域逐域分答并清晰标注** | `jurisdiction.py`、`answer.py`；W1-9.2 |
| D-017 | 2026-11-01 | clarify 是否多选；MCP 如何呈现 | **允许多选**；MCP 用结构化 `clarify` + `resolve_clarify`，宿主渲染 radio/checkbox、不得自动选择 | [W2 Clarify/MCP](../plans/w2-clarify-mcp.md) |

## 3. 范围与判定

| ID | 日期 | 问题 | 用户选择 | 影响/落点 |
|---|---|---|---|---|
| D-003 | 2026-10-31 | `determine` 是否进 MVP | **B. 移出 MVP，只答 KU 原文 + coverage_note；不做适用性结论** | §8 移 backlog；`docs/backlog/determine-v02.md` |
| D-006 | 2026-10-31 | 措辞与结论 | **用“评估”而非“判定”；任何回复不得输出合规/违法结论** | 设计全文；`CONCLUSION_FORBIDDEN`；intent refusal |
| D-014 | 2026-11-01 | 强 hint（算法备案/GDPR）如何定域 | **直接定域**，不再 clarify；“每个法条均可确定使用范围” | W2 法域配置 + Scope Registry |
| D-015 | 2026-11-01 | 如何维护法条适用范围 | **独立 Scope 表**：Scope/地域/管辖权/行业/生效时间；**Scope ID**；**每个 KU 一个 Scope ID** | [W2 Scope Registry](../plans/w2-scope-registry.md)；KU 29→30 字段；CK-17 |
| D-016 | 2026-11-01 | US/SG 等不支持法域 | **`supported:false`，但给出可替代建议**（NIST AI RMF、ISO 42001、EU AI Act、CN 规则等），用户选择；**不得静默替换** | W2 clarify `unsupported_jurisdiction`；Scope Registry `suggestion:true` |
| D-018 | 2026-11-01 | Annex III 子 Scope 生效日 | **2027-12-02**（与 Art.113 对齐，用户确认；仍需作者在 KU 核验时复核） | Scope Registry `effective_from` |

## 4. 排期与流程

| ID | 日期 | 问题 | 用户选择 | 影响/落点 |
|---|---|---|---|---|
| D-009 | 2026-11-01 | 工程 16–19 人日 vs 15 个工作日 | **C. 延到 4 周**（W1–W3 + W4 缓冲） | 设计 §10；W1 计划 |
| D-010 | 2026-11-01 | 是否等 CCC Round-8 | **批准 W1-0，跳过 Round-8 先开工** | W1 开工；v0.8 仍留档 |
| D-011 | 2026-11-01 | W1 实施节奏 | **按 W1-0→W1-10 逐项批准/继续**（每项完成后汇报） | W1 完成；W1 报告 |
| D-019 | 2026-11-01 | 何时升设计版本 | **W2 做完后统一升版（v0.9）**；W2 期间只改计划/KU/代码，不逐项改设计基线 | 设计 v0.9 待 W2 收尾；CCC/Gemini 复审 |

## 5. 评审

| ID | 日期 | 问题 | 用户选择 | 影响/落点 |
|---|---|---|---|---|
| D-012 | 2026-11-01 | Gemini 评审方式 | Reviewer 不能读目录，**只能通过粘贴/上传包**通讯；报告走 `Review-DSH-Gemini/` | `Review-DSH-Gemini/` 协议；Round-1~4 |

## 6. 本日志

| ID | 日期 | 问题 | 用户选择 | 影响/落点 |
|---|---|---|---|---|
| D-020 | 2026-11-01 | 如何记录问题与选择 | **维护单一决策日志，持续更新** | 本文件；后续每轮追加 |
| D-021 | 2026-11-01 | 法域/Scope 何时可自动判定 | **没有确定法域适用范围时必须先与用户确认**；不得从行业/主题（如“教育类高风险”）推断法域；clarify 按用户语言/画像给出**法域 + 支持的 framework（EU/CN/ISO 42001/SOC 2/NIST）**多选；用户选定后才回答。强 hint 仅限**显式法律标识**（GDPR/AI Act/算法备案等），不适用于主题词。 | `jurisdiction.py` clarify；`answer.py`；[W2 Clarify/MCP](../plans/w2-clarify-mcp.md)；`W2-clarify-cases.json` |

---

## 待办 / 未决

| 项 | 状态 | 说明 |
|---|---|---|
| Scope Registry 实现 | open | `kb/scopes.yaml`、21 KU 回填 `scope_id`、CK-17 |
| 强 hint 配置 | open | 算法备案→CN、GDPR→EU、AI Act→EU、生成式人工智能→CN |
| unsupported 建议 | open | NIST/ISO/EU/CN 选项；不静默替换 |
| MCP clarify/resolve_clarify | open | 结构化多选；错误码；DSH/CC skill |
| 设计 v0.9 | open | W2 完成后统一升版（30 字段 + Scope 契约） |

## 更新约定

1. 新决策追加到对应小节，ID 连续（D-021…），不修改历史行；
2. 若推翻旧决策，旧行标 `superseded`，新行写 `supersedes D-xxx`；
3. 每次追加后更新“最后更新”日期与索引；
4. 相关设计/计划文档必须在“影响/落点”列有链接。
