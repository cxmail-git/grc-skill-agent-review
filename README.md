# grc-skill-agent-review — CCC 设计评审包（公开仓库）

- 仓库：https://github.com/cxmail-git/grc-skill-agent-review
- 可见性：**Public**（只含设计文档、公开法规摘录与上游缺陷报告；无密钥、无个人数据）
- 被评对象：`02-design-v0.1.md`（sha256 `bdad6ced…866e6460`，33,407 B）
- 评审协议：`01-review-brief.md`（务必先读 `CLAUDE.md`）

## 在 Claude Code Cloud 里怎么用（4 步）

1. 打开 CCC，用 GitHub 账号 `cxmail-git` 登录；如首次使用，授权 Claude 的 GitHub App 访问本仓库（public 仓库通常也需要授权一次）。
2. 新建 cloud session → 选择仓库 `cxmail-git/grc-skill-agent-review` → 分支 `main`。
3. 在会话里粘贴：

   > 请先读仓库根目录的 `CLAUDE.md` 与 `01-review-brief.md`，然后严格按该协议评审 `02-design-v0.1.md`。你只做评审，不写代码、不改文件；输出用协议 §6 的模板，并逐条回答 §4 的 10 个必答问题。

4. 若它试图改文件/提交/跑命令：回 `Review only. Do not modify files. Follow CLAUDE.md.`

## 评审结束后

把 CCC 的完整报告贴回作者会话（或落到本地 `docs/review/ccc-report.md`）。作者会逐条处置 → 设计 v0.2 → 用户批准 → W1。

## 包内文件

见 `MANIFEST.md`。核心四件：评审协议、设计、契约摘要、KU 计划与样例；`attachments/` 为按需核对的上游材料。
