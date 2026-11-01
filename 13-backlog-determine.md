# determine（v0.2 产品版本 backlog）

> 从设计 v0.7 正文移出，避免被当作 MVP 规格实现。原样保留如下。

## 8. 适用性评估（`determine`，v0.4 推迟到 v0.2）

> **D3 裁定**：`determine` 不进入 3 周 MVP。以下 §8.1–8.4 保留为 **v0.2 产品版本 backlog**；MVP 中范围类问题（#8/#14/#16）由 `ask` 按 KU 原文回答，并带 `coverage_note`，**不输出适用/不适用结论**。
> 用词（用户要求）：对外结论统一用"**评估**"，不用"判定"。

### 8.1 输入画像（profile，v0.3 闭合值域）

```yaml
jurisdiction: EU | CN | OTHER          # OTHER → out_of_scope（可表达 SG/US）
role: provider | deployer | importer | distributor | user
entity: company | public_authority | research | individual
system:
  is_ai_system: true
  is_general_purpose: false
  domains: [biometrics, critical_infra, education, employment, essential_services, law_enforcement, migration, justice, other]
  use_cases: [social_scoring, real_time_rbi, emotion_recognition, biometric_categorisation, facial_scraping, predictive_policing, education_scoring, employment_scoring]
org: {size: sme | large}
timeline: {placing_on_market: 2026-12-01, in_service: 2026-12-01}
judgements:                              # 定性判断由用户自答（N-09/F-06）
  - {id: art6_3_no_material_influence, question: "系统是否未实质性影响决策结果？", answer: true|false|unknown}
```

**值域**：`domains` / `use_cases` 为闭合枚举；同义词映射由 `rules/synonyms.yaml` 负责（大小写/别名归一），映射缺失 → `INVALID_INPUT`。

### 8.2 输出（v0.3）

```json
{
  "verdict": "applies|applies_later|no_rule_matched|insufficient_info|out_of_scope",
  "applies_from": [
    {"scope":"Annex III","date":"2027-12-02","basis_ku":"gsk-eu-art113","basis_locator":"Art.113(c)(i)"},
    {"scope":"Annex I","date":"2028-08-02","basis_ku":"gsk-eu-art113","basis_locator":"Art.113(c)(ii)"}
  ],
  "currently_in_force": false,
  "evaluated_at": "2026-10-31",
  "findings": [
    {"rule_id":"eu-hr-annex3-01","ku_id":"gsk-eu-art6-2","locator":"Art.6(2)",
     "basis_verbatim":"…","reason_code":"USE_CASE_HIT",
     "obligations":[{"ku_id":"gsk-eu-art26-2","locator":"Art.26(2)","text":"…","basis":"obligation[0].text"}]}
  ],
  "listed_obligations_from_source": [{"ku_id":"…","locator":"…","text":"…","basis":"…"}],
  "coverage_note": "本库未收录 Art.43 合格评定细则。",
  "missing_fields": ["system.domains"],
  "citations": [{"ku_id":"…","locator":"…","verbatim":"…","verification":"manual","verified_by":"R-2"}],
  "freshness": {"oldest_verified_at":"2026-10-31","expired_ku_ids":[]},
  "as_of": "2026-10-31",
  "verification": "manual",
  "verified_by": "R-2",
  "disclaimer": "本评估仅基于所收录来源与所提供画像，不构成法律意见；最终适用性以监管解释/司法认定为准。"
}
```

**语义**：`applies` 命中且已生效；`applies_later` 命中但 `currently_in_force=false`；`no_rule_matched` **库内**未命中（不是法律上不适用，必须给 `coverage_note`）；`insufficient_info` 缺字段或 judgement=unknown；`out_of_scope` 法域/对象超范围。`findings[].basis_verbatim` 必须是 KU 字段连续子串（binder 同规则）。

### 8.3 规则引擎（v0.3）

```yaml
# rules/applicability-eu.yaml（单条）
- id: eu-hr-annex3-01
  ku_ids: [gsk-eu-art6-2, gsk-eu-annex3-1]
  jurisdiction: EU
  when:
    - {field: system.use_cases, op: intersects, value: [real_time_rbi, biometric_categorisation]}
  judgement_required:
    - {id: art6_3_no_material_influence, question: "是否未实质性影响决策结果？"}
  exceptions:
    - {id: ex-art6-3, when: [{field: judgements.art6_3_no_material_influence, op: eq, value: true}], basis_ku: gsk-eu-art6-3}
  obligations_from: [gsk-eu-art26-1, gsk-eu-art26-2]
  priority: 50            # 0–100，整数
  applies_from:
    - {scope: Annex III, date: 2027-12-02, basis_ku: gsk-eu-art113, basis_locator: Art.113(c)(i)}
```

**求值顺序**：`exceptions`（命中⇒规则不适用）→ `priority` 高者胜 → 同 priority 异结论 ⇒ `insufficient_info`（列规则 id）。**禁止**脚本表达式、禁止在规则里写死 judgement 答案。`--explain` 固定输出：规则 id / 命中项 / 例外 / 结论 / 依据 KU。

### 8.4 边界（写死）

- 不输出"合规/不合规/风险分值"；
- 画像缺字段 → `insufficient_info`，不得猜测；
- `out_of_scope`：法域未收录（如 SG/US）或对象非 AI 系统；
- 所有输出必带免责声明；MVP 不含 `determine`，`SKILL.md` 禁止输出适用/不适用结论（v0.2 再恢复）。

---

