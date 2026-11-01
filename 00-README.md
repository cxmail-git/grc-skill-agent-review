# 评审包说明（v0.2 送 CCC）

## 包里有什么

| 文件 | 作用 | 必读 |
|---|---|---|
| `01-review-brief.md` | **评审协议**：边界、D1–D9、10 必答问题、输出格式 | ✅ |
| `02-design-v0.2.md` | **被评对象**（v0.2，已回应预演 34 条） | ✅ |
| `03-contract-digest.md` | 29 字段 / CK / WS / DF / EX / 7 形态 locator 摘要 | ✅ |
| `05-pre-review-report.md` | 预演评审报告（7 Block / 18 Major），**非 CCC 正式报告** | ✅ |
| `06-pre-review-resolution.md` | 预演发现处置表（采纳/部分采纳/反驳） | ✅ |
| `04-approval-checklist.md` | 用户批准清单（CCC 之后用） | 否 |
| `attachments/05-source-map.md` | 来源核实：版本/生效日/条款地图/抓取可行性 | 按需 |
| `attachments/06-ku-plan.md` | KU 拆分计划（52 条：EU 32 + CN 20） | 是 |
| `attachments/07-sample-kus.md` | 样例 KU 两份（29 字段 + gap + 逐字义务） | 是 |
| `attachments/rev4-ku-schema.md` / `rev4-wiki-schema.md` | 上游字段/页面契约全文 | 按需 |
| `attachments/08-defect-clustering.md` | 上游五轮缺陷聚类与根因 | 按需（D8） |

## CCC 侧操作（v0.2）

1. 方式 A：在 CCC 新建 cloud session → 选仓库 `cxmail-git/grc-skill-agent-review` → **分支 `design-v0.2`**。
2. 方式 B：直接上传 `grc-skill-agent-design-v0.2-ccc-review.zip`。
3. 开场白：
   > 请先读 `01-review-brief.md`，按该协议评审 `02-design-v0.2.md`。`05/06` 是预演评审及其处置表（非 CCC 正式报告）；请重点复核 v0.2 是否真的修好 F-01/F-02/F-03/F-04/F-05/F-06/F-07，并给出你自己的独立判定。你只做评审，不写代码、不改文件。

## 评审结束后

1. 把 CCC 报告原样存到 `docs/review/ccc-report.md`；
2. 作者逐条处置（采纳/反驳+证据/转用户裁定）→ `ccc-findings-resolution.md`；
3. 设计升 v0.3（或直接 1.0），交用户按 `04-approval-checklist.md` 批准；
4. 批准后 W1-0（契约干跑）→ 修 N-11 → scaffold。

## 注意

- 本包**不含作者的推荐/定级**；`05/06` 是上一轮独立预演的记录，供你核对"修没修"，不构成你的结论。
- 每条发现必须带位置（§）+ 判据/反例 + 修法；"已修"不算证据，要给可复跑判据。
