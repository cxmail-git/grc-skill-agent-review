# 评审包说明（v0.3 送 CCC）

## 包里有什么

| 文件 | 作用 | 必读 |
|---|---|---|
| `01-review-brief.md` | **评审协议**：边界、D1–D9、10 必答、输出格式 | ✅ |
| `02-design-v0.3.md` | **被评对象**（v0.3 = v0.1 + 两轮预演处置） | ✅ |
| `03-contract-digest.md` | 29 字段 / CK / WS / DF / EX / 7 形态 locator | ✅ |
| `05/06` | v0.1 预演报告 + 处置（34 条） | ✅ |
| `07/08` | v0.2 复审报告 + 处置（5 Block / 22 条） | ✅ |
| `04-approval-checklist.md` | 用户批准清单 | 否 |
| `attachments/05-source-map.md` | 来源核实 | 按需 |
| `attachments/06-ku-plan.md` | KU 计划（52：EU 32 + CN 20） | 是 |
| `attachments/07-sample-kus.md` | 样例 KU 两份（29 字段 + gap + 逐字义务） | 是 |
| `attachments/rev4-*.md` | 上游契约全文 | 按需 |
| `evidence/` | locator 检查 + v0.3 一致性检查（46 PASS / 0 FAIL） | 是 |

## CCC 操作

1. 新建 cloud session → 仓库 `cxmail-git/grc-skill-agent-review` → **分支 `design-v0.3`**。
2. 或直接上传 `grc-skill-agent-design-v0.3-ccc-review.zip`。
3. 开场白：
   > 请先读 `01-review-brief.md`，按协议评审 `02-design-v0.3.md`。`05–08` 是两轮预演评审及处置（非 CCC 正式报告）；请重点复核 v0.3 是否真修好 5 个 Block（F-04、F-07、N-01、N-02、N-03）与 C1–C6 条件，并给出你自己的独立判定。只做评审，不写代码、不改文件。

## 评审结束后

CCC 报告 → `docs/review/ccc-report.md` → 作者逐条处置 → v0.4/1.0 → 用户按 `04-approval-checklist.md` 批准 → W1-0 → W1。

## 注意

- 本包不含作者推荐定级；`05–08` 是历史评审记录，供核对"修没修"，不构成 CCC 结论。
- "已修"不算证据：每条结论要给可复跑判据（正则/脚本/反例）。
