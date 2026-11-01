# 用户批准清单（v0.3 → 开工前）

> 用法：CCC 复审回传、作者完成处置、设计升 v0.3 后，逐项确认。任一项不满足 → 不批准。
> 标"条件通过"时须写明条件、责任人与截止日。

## 1. 输入完整性

- [ ] CCC 报告原件已存档（`docs/review/ccc-report.md`，未编辑）
- [ ] 处置表逐条对应（`docs/review/ccc-findings-resolution.md`，无遗漏编号）
- [ ] 设计 v0.3 与 v0.2 的 diff 已生成
- [ ] 所有 Block 有结论（采纳并改 / 反驳+证据 / 转用户裁定）

## 2. CCC 判定核对

- [ ] 总裁定：A / B / C：______
- [ ] 若 C：任一 Block 未关闭 → 不批准
- [ ] 若 B：条件清单全部有责任人 + 截止日
- [ ] 一票否决项（若有）：______

## 3. 关键变更定稿

- [ ] **C1** 快照：snapshot 唯一真值；CK-03 五态；发布门禁四字段（verified_by/evidence_ref/page_digest/verified_at）+ 过期重算
- [ ] **C2** 语言：`sentences[]` + `translations[].claim_ids` 纳入 binder
- [ ] **C3** 非 KU 表：catalog/rules/profiles/**scope_exclusions**；CK-14 可执行
- [ ] **C4** locator：7 形态正则全文；CK-01 逐字实现
- [ ] **C5** 答案：claim + sentence_map + translations；frame 排除 DF-1~6
- [ ] **C6** applies_from 规则级 + basis_ku；五态（含 applies_later）

## 4. 十个必答问题

- [ ] CCC 全部作答，无跳过
- [ ] "最大单点风险"与"只能砍一件事"的取舍我认可

## 5. 风险接受（签字项）

- [ ] R1 摘录快照：3 周只承诺"发布前核验"，不承诺周检
- [ ] R3 适用性判定：五态 + 免责 + 不评分；不构成法律意见
- [ ] R4 LLM 幻觉：抽取优先 + binder 句级校验 + `--no-llm` 兜底
- [ ] R7 版权：只存摘录 + 链接 + 署名

## 6. 范围与排期

- [ ] 52 KU（EU 32 + CN 20）/ 20 金标 + 5 独立负例 / 双域 / 不做对比
- [ ] 排期二选一：**A** 2 人并行（工程 + GRC 研究）；**B** 1 人则 `determine` 移 v0.4
- [ ] W1-0：publish 态样例过 CK + 一次 ask，产物入 evidence
- [ ] W1 第一件事：导入契约后修 N-11（2 子项 + 2 错误码 + 1 反例）

## 7. 最终决定

- [ ] **A · 批准**（冻结 spec v1.0 → W1-0 → W1）
- [ ] **B · 有条件批准**（条件：____｜责任人：____｜截止：____）
- [ ] **C · 不批准**（原因：____）

签字：__________ ｜ 日期：__________
