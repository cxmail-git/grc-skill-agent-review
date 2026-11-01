# 预演复审处置表（v0.2 → v0.3）

> 来源：`docs/review/pre-review-v02-report.md`（独立复审，非 CCC 正式报告）
> 结论：B 有条件通过；当前 Block 开口 5 条（F-04、F-07、N-01、N-02、N-03）；条件 C1–C6 全部采纳。
> 关键自纠：**F-07 上一轮改反了**——`actual_changed ⊆ declared ∪ consumers` 是"允许集"，不是"必须更新集"；v0.3 改为**双向判据**。

| # | 级别 | 摘要 | 处置 | v0.3 落点 |
|---|---|---|---|---|
| F-01 | Block 残留 | 7 形态只实现 3 条正则；CN 第（二）项不匹配；下游候选表未跟 | 采纳 | §5.2 C4 给出 **7 条正则全文**（含全角项号）；`scripts/regen_excerpts.py` 从 ku-plan 生成候选表并校验 id 集合相等 |
| F-02 | Block 残留 | prose/translations 不受 binder 约束 | 采纳 | §7.1 增 `sentence_map`、`translations[].claim_ids`；§7.3 prose 逐句校验 |
| F-03 | Block 残留 | absence 无 schema/CK/样例 | 采纳 | §5.4 增 `scope_exclusions.yaml`；§7.1 claim 增 `scope_exclusion_id`；新增 **CK-14** + 反例 |
| F-04 | **Block** | manual 无证据可发布；offline 不在枚举；过期不重算 | 采纳 | §5.3 状态机补 offline、发布门禁四字段校验、按 `verified_at+max_age` 重算、`verification_source` 只允许命令写入 |
| F-05 | Block 残留 | 每 KU 单 effective_date 无法表达 Annex I/III 两日期 | 采纳 | `applies_from` 上移到**规则级**，带 `basis_ku/basis_locator`；KU 只存 `effective_date` 的条文主日期 |
| F-06 | Block 残留 | judgement_required 无输入通道；exceptions 无 schema | 采纳 | §8.1 profile 增 `judgements`；§8.3 定义 `exceptions[]` 表达式与 `--explain` 字段 |
| F-07 | **Block（未修）** | CI 判据方向反了 | 采纳 | §6.2 改**双向**：`required_updates(change) ⊆ actual_changed` 且 `actual_changed ⊆ changed_files ∪ consumers`；`ku_ids` 由变更文件解析；错误码补 3 个；反向探针改为"只改规则不改金标必须 FAIL" |
| N-01 | **Block（新）** | prose/translations 可夹带无据事实 | 采纳 | `answer` 改 `sentences[]`（每句 `claim_ids[]` 或 `frame`）；`translations[].claim_ids` 纳入 binder |
| N-02 | **Block（新）** | absence 是免绑后门 | 采纳 | `scope_exclusions.yaml` schema（id/jurisdiction/registry_id/as_of/reason/evidence_url）+ CK-14（absence 必须解析到条目） |
| N-03 | **Block（新）** | 金标 #1/#3/#14 与库/接口互斥 | 采纳 | #1 删 Art.43；#3 改 7 项且 `coverage_gap` 只声明"其余 3 项"；#14 增 `ask.profile`；#7 补 Art.113 两日期与 `basis_ku` |
| N-04 | Major | Art.113 摘录仍是 2026-08-02；applies_from 不可回放 | 采纳 | 重抓 Art.113 合并版；候选表更新；`applies_from` 带依据 |
| N-05 | Major | 候选表与 ku-plan 不一致 | 采纳 | 脚本重生成；CI 校验 `set(ids)==set(plan.ids)` 且 locator 合法 |
| N-06 | Major | registry 与 snapshot 双真值 | 采纳 | **snapshot 唯一真值**；registry 只存来源级（不含 verification）；样例 `registry_id: reg-eu-ai-act` |
| N-07 | Major | 计数漂移（附录 B 和=30 标 32 等） | 采纳 | `scripts/gen_numbers.py` 生成计数；附录 B/D、R2、approval 全部改为 32/20/7/5/13 |
| N-08 | Major | "三态"与五态并存 | 采纳 | 全文统一**五态**：applies/applies_later/no_rule_matched/insufficient_info/out_of_scope |
| N-09 | Major | frame 可免绑 DF-3/DF-5 | 采纳 | frame 必须排除 DF-1~6 全部；frame 占比报警 |
| N-10 | Major | count_from_ku/coverage_note 无字段；obligations 自由文本 | 采纳 | §7.1/§8.2 增字段；`findings[].obligations` 改结构化 `{ku_id, locator, text, basis}` |
| N-11 | Major | jurisdiction 无法表达 SG/US；domains 开放 | 采纳 | `jurisdiction` 增 `OTHER`；domains/use_cases 闭合枚举 + 同义词 |
| N-12 | Major | 演示改不存在的 KU；W1/W2 重复计 20 | 采纳 | 演示改 `gsk-eu-art113`；W2 改"EU 剩余 12 + CN 20"；表列修正；v1.0 |
| N-13 | Major | change_id 边界未定义；矩阵不被 CI 读 | 采纳 | 一 PR 一 change_id；错误码 `CHANGE_ID_MISSING/UNKNOWN/DECLARED_EMPTY`；CI 读矩阵并校验 evidence 存在 |
| N-14 | Minor | 目录树缺 4 项；freshness 字段名不一；fingerprint 占位 | 采纳 | 补树；统一 `oldest_verified_at`；fingerprint 由 excerpt 实算（样例用 sha384 前 96 hex，注明近似） |
| 其余 Minor | Minor | F-13/F-14/F-15/F-18/F-22/F-26/F-27/F-29/F-31/F-33/F-34 | 采纳 | 见 v0.3 对应节；不再逐条列 |

## 对"为什么上一轮 F-07 会改反"的说明（自纠，不反驳）

我把"declared ∪ consumers"误当成"必须集合"。正确形式是：
- `required_updates(change)` = 由**变更文件本身**（规则/模板/契约）经依赖图推出的**必须同步更新**的实例集；
- `required_updates ⊆ actual_changed`（必须改了）**且** `actual_changed ⊆ changed_files ∪ all_consumers`（不能乱改）。
反向探针固定 fixture：只改 `rules/applicability-eu.yaml`、不更新金标/页面 → 必须 FAIL。

## 复核声明

- 本轮不反驳任何 Block；C1–C6 全部进 v0.3。
- 金标三题（#1/#3/#14）在 v0.3 重写；#7 补齐 Art.113 原文后再冻结。
- 仍待用户：排期 A（2 人）/ B（determine 移后）；CCC 对 v0.3 的正式复审。
