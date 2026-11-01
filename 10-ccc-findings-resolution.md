# CCC v0.1 报告处置表（v0.3 基线 → v0.4 计划）

> 报告：`docs/review/ccc-report.md`（对象 v0.1，**REVIEW_STALE**；仍逐条处置）
> 基线：设计 v0.3（已含两轮预演修复）；标记 `已修/部分/未修` 指 **v0.3 当前状态**。
> 处置口径：`已修`（无需动）/ `v0.4`（本轮改）/ `用户裁定`（需你拍板）。

| # | CCC 发现 | v0.3 状态 | 处置 |
|---|---|---|---|
| F-01 | offline 同义反复；manual 无存证；Tier A 应全文快照 | **部分**（manual 有 evidence_ref/双人字段；offline 禁发布；但无第二核验人、无全文快照） | **用户裁定**：A 全文快照（Tier A）/ B 摘录+存证+第二核验人 |
| F-02 | 译文 span 非英文字段子串 | **已修**（`binding_mode=translation`、`verbatim` 绑原文、`sentence_map`） | — |
| F-03 | ask 执行点未定义（LLM 在哪跑） | **未修** | v0.4：明确 A 骨架返回 / B 校验入口（用户裁定） |
| F-04 | determine 无时间维度、聚合规则 | **已修**（`applies_later`、`applies_from`、`currently_in_force`、`evaluated_at`） | — |
| F-05 | does_not_apply 对覆盖无感知；义务清单 vs #20 | **已修**（`no_rule_matched` + `coverage_note`；#20 仍 refuse） | — |
| F-06 | 容量/排期不自洽 | **未修**（仅写 2 人硬前提） | **用户裁定**：A 2 人 / B 砍 determine |
| F-07 | 零第三方依赖 vs YAML 存储 | **未修**（仍写零依赖） | **用户裁定**：允许 pin PyYAML / 改 JSON |
| F-08 | MCP 协议细节 | **已修**（协议版本、错误边界、分块、并发测试） | — |
| F-09 | 跨语言检索/链式 KU/no_ku 阈值 | **部分**（retrieval_expect、bigram；无 no_ku 阈值/别名 lint/链展开） | v0.4：补阈值 + 别名 lint + 主题链 |
| F-10 | 拒答分类重叠；--no-llm 识别 | **部分**（scope_correction、partial 三义；not_legal_advice 仍靠意图） | v0.4：规则化关键词 + partial 子码 |
| F-11 | 算子不足（any/all/not、字段对字段、CN 字段） | **部分**（intersects/contains_all/judgement） | v0.4：补 any/all/not + `field_ref` + CN 字段 |
| F-12 | 冲突定义/priority 平局 | **部分**（求值顺序已定；冲突定义未写死） | v0.4：冲突仅同 KU 反结论；平局 insufficient |
| F-13 | 规则 YAML 承载法律事实、无 ku_hash 绑定 | **未修** | v0.4：每条 when 引用 `{ku_id, field, ku_hash}` + 字面量 lint |
| F-14 | 影响面 CI 方向 | **已修**（双向 `required_updates ⊆ actual_changed`） | — |
| F-15 | 5 分钟指标排除真瓶颈；第二核验人无人 | **部分**（R1 收窄；第二核验人未定） | **用户裁定**：指定第二核验人/角色码 |
| F-16 | 指标可自欺；缺 expected_facts/6 类用例 | **部分**（独立脚本、frame 比例、检索召回） | v0.4：`expected_facts` + 6 类用例 + `--now` |
| F-17 | 金标期望不一致 | **已修**（单值 mode、5 拒答题、负例分列） | — |
| F-18 | P-1~P-7 部分吸收；数字手写 | **部分**（数字统一 52/32/20；P-6/P-7 未映射） | v0.4：P-n→步骤/人/错误码表 |
| F-19 | N-11 修法缺失 | **未修**（仅声明） | v0.4：A8 最小修法（CK-11/CK-09 子项+错误码+反例） |
| F-20 | 元数据落点/两轴混淆 | **部分**（每 KU snapshot；五态仍混 mode×freshness） | v0.4：拆 `verification_mode` 与 `freshness` 两轴 |
| F-21 | EU 上游检测/primary 标注 | **部分**（R1 已收窄） | v0.4：registry 记修订法令 OJ；primary 依据说明 |
| F-22 | 样例 KU status/双日期 | **部分**（draft；规则级双日期） | v0.4：样例改 `status: transition` + 双日期落点示例 |
| F-23 | 页面语言/DF 规则语言未定义 | **未修** | v0.4：页面中文、KU 原文；DF/WS 按语言声明 |
| F-24 | Codex 残留 | **已修**（移出 G4） | — |
| F-25 | 包内路径不可达/1.4 顺序 | **已修**（MANIFEST、1.4 已移位） | — |
| 用户补充 | 结论用词"评估"替代"判定" | **未修** | v0.4：输出/文档/ skill 统一"评估" |

## 汇总

- **已修 9**：F-02、F-04、F-05、F-08、F-14、F-17、F-24、F-25（+ F-01 部分）
- **v0.4 可改 12**：F-03、F-09、F-10、F-11、F-12、F-13、F-16、F-18、F-19、F-20、F-21、F-22、F-23、用户补充
- **需你裁定 5**：F-01 快照策略、F-03 ask 执行点、F-06 排期、F-07 YAML 依赖、F-15 第二核验人

## 结论

CCC 报告对象是 v0.1，**不能作为 v0.3 的通过依据**；但其中 12 条仍适用于 v0.3，已排入 v0.4。等你裁定 5 项后，我出 v0.4 并开 round-4 复审。
