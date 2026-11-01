# 预演评审发现处置表（v0.1 → v0.2）

> 来源：`docs/review/pre-review-report.md`（独立预演，非 CCC 正式报告）
> 处置口径：`采纳`（改 v0.2）/ `部分采纳`（改一半，理由见行）/ `反驳`（附证据）/ `转用户裁定`。
> **总裁定 B（7 条件）全部采纳**；F-01/F-07/F-02/F-03 为 v0.2 必改。
> 评审人指出的"作者自评在包内"经核：`spec-self-review.md` **不在**评审包/公开仓库，仅在本地 docs；F-31 按"路径清单不一致"采纳，其余部分反驳。

| # | 级别 | 摘要 | 处置 | v0.2 落点 |
|---|---|---|---|---|
| F-01 | Block | locator 域对 EU 字母项/附件/区间不闭合，15/33 非法 | **采纳** | §5.2 C4 改为 **7 形态**（条款式允字母项、新增附件式、区间禁止）；ku-plan 重写为 52 条单 locator |
| F-02 | Block | C2 用户语言 vs binder 连续子串互斥 | **采纳** | §7.1/§7.2/§7.3 改为 `binding_mode: quote\|translation\|frame`；claim 与 prose 分离 |
| F-03 | Block | 归纳/否定/跨域/时间句无绑定路径；refusal 缺 scope_correction | **采纳** | §7.2 三类句（事实/框架/否定）+ `support_type` 五值；refusal 增 `scope_correction` |
| F-04 | Block | CK-03 四态无状态机；manual 证据无字段 | **采纳** | §5.3 状态机 + `verification_url/page_digest/evidence_ref`；offline 不得发布 |
| F-05 | Block | verdict 缺"未生效/部分适用" | **采纳** | §8.2 增 `applies_later` + `applies_from` + `currently_in_force` |
| F-06 | Block | 运算符表达力不足；in 对 list 语义未定义 | **采纳** | §8.3 明确 `in/intersects/contains_all`；增 `judgement_required` 三值槽；例外→优先级求值顺序 |
| F-07 | Block | impact CI 用全表并集，拦不住 G-1 | **采纳** | §6.2 改 `change_id` 单行 + 依赖图计算消费集 + evidence 产物 + CI 反向探针 |
| F-08 | Major | CN 款/项不可表达；citations 无 anchor | **采纳** | C4 第 6 形态扩 `第X条(第X款)?(第X项)?`；citations 增 `anchor` |
| F-09 | Major | 核验粒度矛盾（整部法 vs 每篇） | **采纳** | 快照粒度 = **每 KU**；freshness 按 KU 聚合 |
| F-10 | Major | 登记 URL（EUR-Lex）≠ 核验 URL（Service Desk） | **采纳** | registry 增 `verification_url`；online/manual 一律针对它；`page_digest` 取它 |
| F-11 | Major | 样例 CK-04 失败（概念字段 null + gap 空） | **采纳** | ku-schema 明确"概念四字段仅被 concept 页引用时校验"；样例补 gap + `status: draft` |
| F-12 | Major | obligation/evidence 非逐字；fingerprint 占位 | **采纳** | CK-03 增子项：obligation.text 必须为 excerpt 连续子串，否则 `paraphrase: true` 且禁入 citation；fingerprint 格式校验 |
| F-13 | Major | 四个事实子字段无闭合值域 | **采纳** | 导入时补 4 张闭合表（modality/subject/frequency/scope_type）+ `scope_note` |
| F-14 | Major | determine 输出无 as_of/verification | **采纳** | §8.2 复用 §7.1 citations + freshness + as_of |
| F-15 | Major | exceptions/priority 无求值语义 | **采纳** | 固定顺序：exceptions → priority → 同 priority 异结论才 insufficient |
| F-16 | Major | 50/53/32/33 数字漂移；弹性击穿 G2 | **采纳** | 统一 **52 KU（EU 32 + CN 20）/ 20 金标**；删除"金标 15"弹性 |
| F-17 | Major | 金标分类与题目不符；负例混用 | **采纳** | 分类由脚本统计；"金标内拒答 5 题"与"独立负例集 5 题"分离 |
| F-18 | Major | 三个指标可自欺 | **采纳** | 稳定性只比 claims 三元组集合；unsupported 由独立脚本算；llm/no-llm 分开记录 |
| F-19 | Major | R1 缓解未入排期；expired 3 周内不触发 | **采纳** | R1 收窄为"发布前核验"；3 周不承诺周检；freshness 增 `--now` 供探针 |
| F-20 | Major | ask 无画像入口；#14 两处期望不同 | **采纳** | ask 增可选 `profile`；适用性问题未给 profile → `insufficient_profile`；#14 唯一期望 |
| F-21 | Major | 检索无质量判据 | **采纳** | eval 增 `retrieval_expect`；top5 召回 ≥18/20；aliases 由金标反推 + 每题至少 1 别名 |
| F-22 | Major | 影响面矩阵示例行指向不存在文件/无证据 | **采纳** | 重写矩阵：真实路径、`changes/<id>.yaml`、evidence 产物 |
| F-23 | Major | citations 缺 verbatim/verified_by；refusal 无 null 约定 | **采纳** | 补字段；`refusal` 在 answer 时省略 |
| F-24 | Minor | 组件表漏 binder | **采纳** | §4.2 增 `grc_core.binder` |
| F-25 | Minor | `gsk-` 前缀未申报 | **采纳** | 附录 C 增命名域行；不兼容时由迁移脚本映射 |
| F-26 | Minor | 样例 title 为拼接串；source_id/registry_id 未区分 | **采纳** | title 取原文标题；source_id=来源登记、registry_id=条目主键，样例区分 |
| F-27 | Minor | 1.4 位置错；"9 处" vs "11 处" | **采纳** | §1.4 移到 §1.3 后；数字由 `gen_numbers.py` 生成 |
| F-28 | Minor | "refs 19→50 边" 硬编码遗留 | **采纳** | 删 19；改"互转置 + 运行时统计" |
| F-29 | Minor | N-11 顺序三处不一致 | **采纳** | 统一：导入契约 → W1-1a 修 N-11（2 子项 + 2 错误码 + 1 反例） |
| F-30 | Minor | 跨平台承诺含 Codex 但未验 | **采纳** | §4.3 标 Codex "未验证（v0.2）"；G4 只验 DSH+CC |
| F-31 | Minor | 包内清单路径不符；称"不含自评" | **部分采纳** | MANIFEST 改真实路径；自评确认不在包内（仅本地），brief 措辞改为"包内不含作者定级" |
| F-32 | Major | partial 两处语义冲突 | **采纳** | `partial_reason: conflict\|cross_jurisdiction\|coverage_gap`；#19 用 `groups` |
| F-33 | Minor | 三态/四态复述不一致 | **采纳** | 全包统一四态；批准清单同步 |
| F-34 | Major | MCP 协议面未闭合 | **采纳** | §4.2.1 增 6 条协议用例（握手/未知工具/参数非法/业务失败/大响应/并发） |
| F-P1 | Pending | 页面侧如何引用摘录未定义 | **采纳** | §5.1 增：页面只渲染 `verbatim_excerpt` 的派生块；WS-03 增加"块内引文=excerpt 子串" |

## 对评审人两条建议的取舍

1. **"砍 determine"**：不采纳（用户明确要"简单合规判定"）。改为：determine 只做适用性三态 + 义务清单，**不做法务定性**；8.2 增 `applies_later`；排期在 W2 增加 1 人日并砍 Art.50 余项（见 §10 修订）。
2. **"加契约干跑门禁"**：采纳，列为 W1-0（两份样例跑 CK + 一次 ask，结果入 evidence）。

## 复核声明

- F-01/F-07/F-02/F-03 已由我方独立复跑确认（locator 15/33、impact 并集逻辑、binder 冲突推演）。
- F-12/F-11 实测成立；样例已按修法更新。
- F-31 的"自评在包内"不成立：`spec-self-review.md` 未进评审包/公开仓库（可核 `MANIFEST.md`）。
