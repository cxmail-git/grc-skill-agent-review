# grc-skill-agent-review — CCC 设计评审包（v0.2 分支）

- 仓库：https://github.com/cxmail-git/grc-skill-agent-review
- **当前分支：`design-v0.2`**（`main` 保留 v0.1 送审版）
- 可见性：Public（只含设计文档、公开法规摘录、预演评审记录；无密钥、无个人数据）
- 被评对象：`02-design-v0.2.md`
- 评审协议：`01-review-brief.md`；先读 `CLAUDE.md`
- 预演记录：`05-pre-review-report.md`（34 条，非 CCC 正式报告）+ `06-pre-review-resolution.md`（处置表）

## CCC 4 步

1. 用 GitHub 账号 `cxmail-git` 登录 CCC，授权 Claude GitHub App 访问本仓库（public 通常也要授权一次）。
2. 新建 cloud session → 仓库 `cxmail-git/grc-skill-agent-review` → **分支 `design-v0.2`**。
3. 粘贴：

   > 请先读 `CLAUDE.md` 与 `01-review-brief.md`，严格按该协议评审 `02-design-v0.2.md`。`05/06` 是预演评审及处置表（非 CCC 正式报告）；请重点复核 v0.2 是否真修好 F-01/F-02/F-03/F-04/F-05/F-06/F-07，并给出你自己的独立判定。你只做评审，不写代码、不改文件。

4. 若它试图改文件/提交：回 `Review only. Do not modify files. Follow CLAUDE.md.`

## 评审结束后

报告贴回作者会话，或落到本地 `docs/review/ccc-report.md`；作者逐条处置 → v0.3 → 用户按 `04-approval-checklist.md` 批准 → W1-0 → W1。
