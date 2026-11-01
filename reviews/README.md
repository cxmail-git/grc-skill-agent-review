# CCC ↔ DSH 同步协议（review bus）

> 目的：把"我产出 → CCC 评审 → 我处置 → 你批准"变成**仓库内的可审计状态机**，双方不需要访问对方会话。

## 分支与目录

| 对象 | 谁写 | 用途 |
|---|---|---|
| `main` | 仅用户合并 | 最新冻结设计（CCC 评审对象） |
| `design-vX.Y` | DSH | 设计提案 |
| `review/round-N` | **CCC** | 评审输出，只允许 `reviews/round-N/**` |
| `reviews/round-N/REQUEST.md` | DSH | 本轮送审说明（绑定 commit/hash） |
| `reviews/round-N/report.md` + `report.yaml` | **CCC** | 人读 + 机读报告 |
| `reviews/round-N/resolution.md` | DSH | 逐条处置（采纳/反驳/转裁定） |
| `reviews/round-N/APPROVED` 或 PR label `status:approved` | 用户 | 批准 |

## 状态机

`SUBMITTED → REVIEWED → TRIAGED → APPROVED → FROZEN`

- **SUBMITTED**：DSH push `design-vX.Y` + 开 PR/Issue，写 `REQUEST.md`（含 `design_commit` / `design_sha256` / `package_sha256`）。
- **REVIEWED**：CCC push `review/round-N`（或 Issue 评论），写 `report.md` + `report.yaml`；报告必须引用请求里的三个 hash。
- **TRIAGED**：DSH 写 `resolution.md`，每条 F-xx 给 `accept|reject|user-decides` + 证据 + 落点 commit。
- **APPROVED**：用户写 `APPROVED`（姓名/日期）或加 label。
- **FROZEN**：DSH 打 tag `design-vX.Y-frozen`。

## 硬规则

1. CCC 只能写 `reviews/round-N/**`；CI（`.github/workflows/review-guard.yml`）对 `review/round-*` 分支检查 diff，越界即失败（`REVIEW_WRITE_OUT_OF_SCOPE`）。
2. 报告与 `REQUEST.md` 的三个 hash 不一致 → `REVIEW_STALE`，作废重审。
3. 报告文件只增不改；处置写 `resolution.md`，不改报告。
4. 没有 `report.yaml` 时，Issue 评论也算有效（人读），但**评论必须以 `# CCC Review Report` 开头**（或含 `总裁定` / `verdict:`），否则视为作者评论、不进入归档；DSH 处置时补机器摘要。
5. 评审会话 ID 只作参考，不是同步通道。

## 传输回退

1. CCC push `review/round-N`（主）
2. CCC 在 GitHub Issue 评论报告（备）
3. 用户粘贴（兜底）
