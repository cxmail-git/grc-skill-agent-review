# CCC Review Round 4 — 设计 v0.4

> 说明：Round 3 的报告自述对象为 v0.1（见 `09-ccc-report-v0.1-subject.md`），按协议判 `REVIEW_STALE`；本轮请求复审 **v0.4**（已吸收该报告 + 用户 5 项裁定）。

- design: `v0.4`
- branch: `design-v0.4`
- design_sha256: `5910809da595a27984232d28b3c0fef4ca60080d7bc43605404a0d16b86c3c57`
- package_sha256: `6da01875cd72f97011c0f1d90141db20be7eed9ba03d728a60ac9193dd34dce1`
- 用户裁定：determine 推迟；Tier A 全文快照；宿主成文 + validate_answer；PyYAML；单人核验 UNVERIFIED
- 评审协议：`01-review-brief.md`
- 报告路径（任选）：push 分支 `review/round-4` 的 `reviews/round-4/report.md` + `report.yaml`；或 Issue 评论
- 只写 `reviews/round-4/**`，不改设计/代码

## 重点复核

1. 砍 determine 后 G1/G2/G4/G5 是否仍成立；
2. 全文快照 + verification.yaml + UNVERIFIED 是否可审计；
3. 宿主成文 + validate_answer 是否守住 citation；
4. CCC v0.1 报告中 F-03/F-09/F-10/F-11/F-12/F-13/F-16/F-18/F-19/F-20/F-21/F-22/F-23 哪些已关闭；
5. 结论用词是否统一为"评估"。
