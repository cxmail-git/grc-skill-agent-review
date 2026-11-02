# 术语标准 v1.0 · Reviewer 检查清单

> 对象：`docs/standards/terminology-standard.md`
> 来源：AI-GRC-Consultant 00（v3.1）+ 10（r4）
> 只读评审；不改文件；每条给 `文件/节/行` 或引文。

## Q1 来源保真

00 的原义（Requirement/Compliance Obligation/Compliance/Risk/Finding/Evidence/Control/Measure/Applicability Determination）是否被准确转述？有无把 ISO/IIA 原文复制进来（版权）？

## Q2 本项目取用

- 是否清楚区分「原义」与「本项目取用」？
- `Risk` 是否采用 NIST AI 100-1，而非 CNSSI 单独负面定义？
- `Compliance` 是否明确“不输出结论”？
- `Applicability Determination` 是否明确“不采用”（D-003）？

## Q3 项目术语

`T-KU / T-SCOPE / T-SCOPE-ID / T-CLAIM / T-SENT / T-ANSWER / T-FINAL / T-TOKEN / T-VERIFY / T-UNVER / T-PAGE / T-RHASH / T-KHASH / T-COV / T-CLARIFY / T-MCP / T-EVAL` 是否与当前代码/设计一致？
（重点：30 字段 `scope_id`、clarify/resolve_clarify、scope_time、CK-08 锚定）

## Q4 裸词与同名异指

§6 禁用表是否覆盖 Control/Measure/Action/Rule/Obligation/Requirement/Finding/Risk/Evidence？
`Scope (GRC Skill Agent)` 与 KU `scope_in/scope_out` 是否区分？
`Verification` vs `validate_answer` vs `Eval` 是否区分？

## Q5 分层边界

L0/L1/LJ 与 L2–L4 out-of-scope 的划分是否诚实？是否把本项目说成租户 GRC 平台？

## Q6 映射

NIST/OSCAL/Probo/Nexus/EU/CN 映射是否有误并/过度承诺（如“导出兼容”）？

## Q7 写作规则

“评估 vs 判定”、体系标注、双语、证据等级、copyright 是否可执行？

## Q8 缺失

W2 已实现的 Scope/Clarify/MCP 是否都有术语落点？还缺哪些词（如 `Scope time`、`reference-only`、`resolve_clarify`）？

## Q9 与 v0.9 一致

术语标准与 `docs/specs/...v0.9.md`、`kb/scopes.yaml`、`schema.py` 是否有冲突？

## Q10 总裁定

A/B/C + 条件；只列真实 Block/Major，引用不出降 Pending。
