# CCC v0.1 报告处置表（v0.5 基线）

> 报告：`docs/review/ccc-report.md`（对象 v0.1，**REVIEW_STALE**）
> 基线：设计 **v0.5**。状态按 v0.5 实际落点；`N/A` = 因 determine 推迟而不再适用（不是"已修"）。
> 说明：v0.4 定向复核指出"0 条完整关闭"；v0.5 已补 B-01/B-02/B-03 与 8 条未修项。

| # | CCC 发现 | v0.5 状态 | 落点 / 证据 |
|---|---|---|---|
| F-01 | 快照可审计性 | **已修** | Tier A 全文快照 + `verification.yaml` + CK-03 全文子串/定位 |
| F-02 | 译文绑定 | **已修** | `binding_mode=translation` + `verbatim` 原文 + sentence_map |
| F-03 | ask 执行点 | **已修** | 宿主成文 + `answer_id` + `validate_answer` 句内容校验 |
| F-04 | determine 时间维度 | **N/A** | determine 移 backlog（用户 D3）；范围问题只答原文 |
| F-05 | does_not_apply 覆盖 | **N/A** | 同上；ask 带 `coverage_note` |
| F-06 | 容量/排期 | **已修** | 砍 determine；重估 20–24 人日；2 人并行 |
| F-07 | YAML 依赖 | **已修** | `PyYAML==6.0.2` pin + vendor/wheels 离线安装 |
| F-08 | MCP 协议 | **已修** | 协议版本/错误边界/分块/并发测试 |
| F-09 | 跨语言检索/no_ku | **已修** | 每题别名 lint + `no_ku` 阈值 + `catalog.topics` 链 |
| F-10 | 拒答分类 | **部分** | `scope_correction`/partial 子码已加；`not_legal_advice` 仍依赖意图解析 |
| F-11 | 算子不足 | **N/A** | 规则引擎随 determine 移 backlog |
| F-12 | 冲突定义 | **N/A** | 同上 |
| F-13 | 规则字面量绑 ku_hash | **N/A** | 同上；MVP 无规则 YAML |
| F-14 | 影响面 CI | **已修** | 双向 `required_updates ⊆ actual_changed` + 反向探针 |
| F-15 | 第二核验人 | **已修** | 单人 + `UNVERIFIED` 降级 + R11 接受 |
| F-16 | 指标自欺/用例 | **已修** | `expected_facts`（非规则作者）+ 6 类用例 + `--now` |
| F-17 | 金标期望 | **已修** | 单值 mode + 5 拒答 + 负例分列 |
| F-18 | P-n 覆盖/数字 | **已修** | §9.4 P-n 映射表 + 计数脚本 |
| F-19 | N-11 修法 | **已修** | CK-11 五值/subject/date + CK-09 投影 + 反例 |
| F-20 | 元数据两轴 | **已修** | `verification_mode` × `freshness` + 每 KU verification |
| F-21 | EU 上游/primary | **已修** | `amendment_ref`（OJ L 2026/01744）+ 人工核验 |
| F-22 | 样例 KU 双日期 | **已修** | status `transition` + `transition_note` 双日期 |
| F-23 | 页面/规则语言 | **已修** | 页面中文、KU 原文；DF/WS 按语言声明 |
| F-24 | Codex 残留 | **已修** | 移出 G4，标未验证 |
| F-25 | 包路径 | **已修** | MANIFEST + 扁平附件 |
| 用户补充 | 用词"评估" | **已修** | §7 开头 + §8 backlog 注 + 输出契约 |

## 统计

- **已修 19**、**部分 1**（F-10）、**N/A 5**（F-04/05/11/12/13，因 determine 推迟）
- 不再声称"13 条全部关闭"；F-10 的 `not_legal_advice` 识别保留为 v0.2 改进项。
