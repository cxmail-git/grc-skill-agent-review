# CCC Round-5 发现处置表（v0.5 → v0.6）

> 报告：`docs/review/ccc-report.md`（绑定 v0.5 `c763b8eb…`，已验证）
> 结论：**B 有条件通过**；Block 2（V5-01/V5-02）、Major 15、Minor 4；条件 8 条。
> 处置口径：`采纳` / `采纳并加严` / `用户裁定` / `记录不修`。

| # | 级别 | 摘要 | 处置 | v0.6 落点 |
|---|---|---|---|---|
| V5-01 | Block | `validate_answer` 只做词面检查，范围扩大句可通过；校验句与展示文本无绑定 | **用户裁定** | 方案 A：core 候选句 + 宿主只选/排/加 frame；方案 B：允许改写但强制范围词/主体词/条件词差集为空 + `final_text` + `validation_token` |
| V5-02 | Block | "不输出适用/不适用结论"只靠 SKILL 文字 | **采纳并加严** | `validate_answer` 对所有句子扫结论词表 → `CONCLUSION_FORBIDDEN`（逐字引文例外）；反向探针 + adversarial 用例；范围问题结尾固定模板 |
| V5-03 | Major | 宿主跳过校验生产不可检 | 采纳 | `issued_vs_validated` 计数、`grc audit-answers`、answer 状态存放位置、G4 要求宿主转录归档 |
| V5-04 | Major | 跨语言校验缺规范化/职责 | 采纳 | `claim.text` 由 core 生成；日期/数字/情态映射表（2027-12-02 ↔ 2 December 2027 ↔ 2027年12月2日；shall↔须/应当） |
| V5-05 | Major | EU 全文仍是人工自证；CK-03 第 3 项对不可抓来源不可执行 | 采纳 | 每来源声明核验路径：可抓→online；不可抓→manual 存证 + 复核频率，CK-03 剔除对不可抓源的抓取项 |
| V5-06 | Major | UNVERIFIED 无输出字段/行为；R2 仍写双人核 | 采纳 | §7.1 增 `unverified:true` + 警告；validate_answer 校验；R2 改写；定义 expired 时 mode |
| V5-07 | Major | 全文快照口径残留 4 处（逐 KU snapshot/anchor/元数据/实名） | 采纳 | 统一 `snapshots/<source_id>.md`；anchor 用 `Art14-1` 形式；元数据清单对齐；实名只进审计存证 |
| V5-08 | Major | `effective_date`/`transition_note` 不受 CK-03 约束 | 采纳 | 新增 CK-16：日期 token 必须能从 excerpt 解析；非日期内容标为作者注 |
| V5-09 | Major | absence 混了 coverage 与 source_silent；CN #17 无条目 | 采纳 | `absence_kind: coverage\|source_silent`；source_silent 扫全文 0 命中；补 CN 条目；措辞与 kind 绑定 |
| V5-10 | Major | mode 重算无算法；金标期望不一致 | 采纳 | 定义 `derive_mode()`（skeleton 覆盖/absence/groups/冲突）；按函数重排 20 题；每个 refuse.reason 至少 1 用例 |
| V5-11 | Major | coverage_note 自由文本 + 手写计数 | 采纳 | `coverage_codes: [sx-…]`；文案由 core 生成；计数脚本生成 |
| V5-12 | Major | not_legal_advice 识别方未定义 | 采纳 | core 内关键词/句式表；`ask` 返回 refuse；定义 `no_llm` 含义 |
| V5-13 | Major | impact CI 文件级粒度 + 命令注入面 | 采纳 | 粒度到 golden 条目（`expected_claim_ku_ids` 反查）；`cmd` 白名单 grc 子命令；输出规范化 |
| V5-14 | Major | PyYAML 加载策略缺失 | 采纳 | `safe_load` + 重复键检测 + 关闭隐式日期/布尔 + wheels 矩阵 + `--require-hashes` |
| V5-15 | Major | 排期无法验证；R2 与弹性方案冲突 | 采纳 | 分项人日（工程 18–22 / 研究 8–10）；固定弹性触发点；R2 统一 |
| V5-16 | Major | 评测自评空间（别名/召回同集） | 采纳 | 留出集（异措辞）；WARN/门禁统一；稳定性测 `--llm`；6 类用例定数量 |
| V5-17 | Minor | GPAI 条款号 53–55 vs 51–56；ku_id/locator 对齐 | 采纳 | 统一 Art.51–56；`gsk-eu-art26-5` = `Art.26(6)` |
| V5-18 | Minor | determine 已移出但 §8 整节仍在 | 采纳 | §8 移到 `docs/backlog/determine-v02.md`，正文一行指针 |
| V5-19 | Minor | log.md date 校验方向与 rev4 倒序冲突 | 采纳 | 按 rev4 倒序：`date ≤ 上一行`；追加性用 git diff 仅新增行 |
| V5-20 | Major | 全文快照"不再分发"与公开仓库冲突 | **用户裁定** | A 快照不进发布包/公开仓库；B 允许随包并写明许可 |
| V5-21 | Minor | 版本/自检残留；round-3 分支含 docs/review 触发 review-guard | 采纳 | 清理 v0.1/v0.2 残留；review-guard 允许 `docs/review/ccc-report.md` 或删除该副本 |

## 条件清单（CCC 8 条）对应

1. V5-01/02 → 接口与结论词表（W1 前定）
2. V5-03/04 → 对账与跨语言规范化
3. V5-05–09/20 → 快照/日期/absence/再分发
4. V5-10–12 → mode 函数/coverage_codes/识别方
5. V5-13/14 → CI 粒度/YAML 策略
6. V5-15/16 → 排期/留出集
7. 所有"需作者核实" → Digital Omnibus 日期、Service Desk 可抓、PyYAML wheel、版权结论

## 下一步

- 两个政策项（V5-01、V5-20）需用户裁定；
- 裁定后出 **v0.6**，重跑 72+ 检查，再请 CCC 复审（Round 6）。
