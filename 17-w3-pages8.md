# W3-2 页面扩到 8 页 · 验收报告（2026-11-02）

## 结论

**通过**：页面从 4 扩到 **8 页 / 11 派生块**，覆盖 EU+CN；`grc validate` **0 errors / 0 warnings**；CK-06/07/09/10 + CK-08 锚定全绿；`refs.json` 8 页 / 9 KU。

## 页面

| 页面 | class | 块 | 引用 |
|---|---|---|---|
| concept-human-oversight | concept | 1 | EU art14 |
| concept-training-data | concept | 1 | CN art7 |
| entity-high-risk-ai-system | entity | 2 | EU art6-2/6-3 |
| overview-eu-ai-act | overview | 1 | EU art2 |
| overview-cn-genai | overview | 1 | CN art2 |
| source-reg-eu-ai-act | source | 1 | EU art2 |
| source-reg-cn-genai | source | 1 | CN art2 |
| topic-content-labeling | topic | 3 | CN label art3/4/10 |

## 校验

| 检查 | 结果 |
|---|---|
| pages / blocks | 8 / 11 |
| classes | concept 2、entity 1、overview 2、source 2、topic 1 |
| validate | 0 errors / 0 warnings |
| compile --check | 0 |
| page validator | 0 |
| refs 双向 | 8 pages / 9 KUs；0 errors |
| CK-08 锚定 | 所有义务/否定段落带 `[[gsk-…]]` + 领域术语 |

## 证据

`evidence/W3-2-cases.json`、`W3-2-run.txt`。

全量回归 W1-0~W1-10 + W2-1~W2-8 + W3-1/W3-2 全绿；eval 10/10、negative 5/5、host 5/5。

## 已知限制

- 无 comparison 页（当前 52 KU 跨法域对比留 W4）；
- 页面叙事仍是最小 editorial pass；
- 20 金标仍 10，W3-3 扩；设计 v1.0 待 W3 收尾。

## 下一步

W3-3：20 金标 + 5 负例 + 设计 v1.0。
