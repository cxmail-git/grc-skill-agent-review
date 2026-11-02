# W3-3 20 金标 + 设计 v1.0 · 验收报告（2026-11-02）

## 结论

**通过**：金标 10→20（EU/CN 双域），5 负例保持；设计 v1.0 生成，`check_design` **127 PASS / 0 FAIL**。

## 金标

- 20 题：EU 8 + CN 8 + EU_CN/通用 4（含 5 个固定拒答）；
- 每题补显式法域（D-021），避免 clarify 误入正例；
- 5 独立负例保持。

## eval

| 指标 | 值 |
|---|---|
| golden | 20 |
| mode_ok | **20/20** |
| retrieval top5 | 14/15 |
| citation | 16/16 |
| sentence_map | 16/16 |
| unsupported | 0 |
| host | 15/15 |
| negative | 5/5 |
| host-simulate fail | exit 1 |

## 设计 v1.0

- `docs/specs/2026-10-31-grc-skill-agent-design-v1.0.md`
- 52 KU（EU32+CN20）、8 页、20 金标、术语标准 v1.1、Scope/CK-17/D-021/clarify/CK-08 收口；
- `check_design` 127/0。

## 证据

`evidence/W3-3-cases.json`、`W3-3-run.txt`；全量回归 W1-0~W1-10 + W2-1~W2-8 + W3-1~W3-3 全绿。

## 已知限制

- retrieval 14/15（1 题 top5 未命中期望，未阻断）；
- expected_facts 仍人工核对，未语义匹配；
- CK-08 仍是规则锚定，非语义裁决；
- 设计 v1.0 待 Reviewer 复审；W4 缓冲/发布。

## 下一步

W3 收尾 → 整理 W3 评审包 → W4（复审/发布/spec 冻结）。
