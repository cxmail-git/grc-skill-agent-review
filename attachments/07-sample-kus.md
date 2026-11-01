# 样例 KU（v0.3）

## gsk-eu-art14.yaml

```yaml
# 样例 KU（格式演示；status=draft，不参与发布门禁）
# v0.2 修正：obligation 文本为 excerpt 连续子串；概念字段与 evidence 用 gap 登记；fingerprint 为格式占位（W1 由 MinHash 计算）
ku_id: gsk-eu-art14
title: "Article 14 — Human oversight"
source_id: reg-eu-ai-act
jurisdiction: EU
instrument_type: regulation
instrument_is_binding: true
obligation_nature: obligation
obligation:
  - id: ob-1
    text: "High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which they are in use."
    subject: provider
    modality: obligation
evidence_requirement: []
applies_to:
  - {subject: provider, stage: develop, scope_type: system, scope_value: high-risk AI systems}
  - {subject: provider, stage: deploy, scope_type: system, scope_value: high-risk AI systems}
status: transition
effective_date: 2027-12-02
transition_note: "Annex III: 2027-12-02；Annex I: 2028-08-02（按 Art.113 合并版）"
verbatim_excerpt: "High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which they are in use."
definition: null
scope_in: null
scope_out: null
common_misreadings: null
published_date: 2024-07-12
source_class: primary
tier: A
confidence: high
source_class_confidence: high
as_of: 2026-10-31
locator: "Art.14(1)"
registry_id: reg-eu-ai-act
snapshot_ref: "snapshots/gsk-eu-art14.md#p1"
first_seen: 2026-10-31T00:00:00-04:00
fingerprint: "minhash96:4c6ea475a7539db34ac421e73efc5f8fd7cb19e6096f79a80be8d625a6a1a7f7e46a1fd06331e9ec19cd6bbe0a8ecb2d"
gap:
  - field: definition
    reason: "样例：概念字段待 W1 结合 concept 页补"
    owner: "R-1 / 待指定"
    due: 2026-11-07
  - field: scope_in
    reason: "样例：范围边界待 W1 核"
    owner: "R-1 / 待指定"
    due: 2026-11-07
  - field: scope_out
    reason: "样例：反范围待 W1 核"
    owner: "R-1 / 待指定"
    due: 2026-11-07
  - field: common_misreadings
    reason: "样例：常见误读待 W1 核"
    owner: "R-2 / 待指定"
    due: 2026-11-07
  - field: evidence_requirement
    reason: "样例：证据要求待 W1 从 Art.14 与 Art.16 义务链推导"
    owner: "R-2 / 待指定"
    due: 2026-11-07

```

## gsk-cn-genai-art7.yaml

```yaml
# 样例 KU（格式演示；status=draft，不参与发布门禁）
# v0.2 修正：obligation 文本均为 excerpt 连续子串；概念字段与 evidence 用 gap 登记；locator 用第 6 形态
ku_id: gsk-cn-genai-art7
title: "第七条"
source_id: reg-cn-genai
jurisdiction: CN
instrument_type: regulation
instrument_is_binding: true
obligation_nature: obligation
obligation:
  - id: ob-1
    text: "使用具有合法来源的数据和基础模型；"
    subject: provider
    modality: obligation
  - id: ob-2
    text: "涉及知识产权的，不得侵害他人依法享有的知识产权；"
    subject: provider
    modality: prohibition
  - id: ob-3
    text: "涉及个人信息的，应当取得个人同意或者符合法律、行政法规规定的其他情形；"
    subject: provider
    modality: obligation
  - id: ob-4
    text: "采取有效措施提高训练数据质量，增强训练数据的真实性、准确性、客观性、多样性；"
    subject: provider
    modality: obligation
  - id: ob-5
    text: "《中华人民共和国网络安全法》、《中华人民共和国数据安全法》、《中华人民共和国个人信息保护法》等法律、行政法规的其他有关规定和有关主管部门的相关监管要求。"
    subject: provider
    modality: obligation
evidence_requirement: []
applies_to:
  - {subject: provider, stage: develop, scope_type: use_case, scope_value: 向境内公众提供生成式人工智能服务的组织、个人}
status: draft
effective_date: 2023-08-15
transition_note: null
verbatim_excerpt: "生成式人工智能服务提供者（以下称提供者）应当依法开展预训练、优化训练等训练数据处理活动，遵守以下规定：（一）使用具有合法来源的数据和基础模型；（二）涉及知识产权的，不得侵害他人依法享有的知识产权；（三）涉及个人信息的，应当取得个人同意或者符合法律、行政法规规定的其他情形；（四）采取有效措施提高训练数据质量，增强训练数据的真实性、准确性、客观性、多样性；（五）《中华人民共和国网络安全法》、《中华人民共和国数据安全法》、《中华人民共和国个人信息保护法》等法律、行政法规的其他有关规定和有关主管部门的相关监管要求。"
definition: null
scope_in:
  - "预训练、优化训练等训练数据处理活动"
scope_out: null
common_misreadings: null
published_date: 2023-07-13
source_class: primary
tier: A
confidence: high
source_class_confidence: high
as_of: 2026-10-31
locator: "第七条"
registry_id: reg-cn-genai
snapshot_ref: "snapshots/gsk-cn-genai-art7.md#art7"
first_seen: 2026-10-31T00:00:00-04:00
fingerprint: "minhash96:79b64ec94fd3ea742d65872c5ddbcf7248d7ca9ef80ca261ef1fc5b002db47cc2ea6fa4825d6b4e1f7db5c08de17cfac"
gap:
  - field: definition
    reason: "样例：概念字段待 W1 补"
    owner: "R-2 / 待指定"
    due: 2026-11-07
  - field: scope_out
    reason: "样例：反范围待 W1 核（Art.2 内部使用例外）"
    owner: "R-2 / 待指定"
    due: 2026-11-07
  - field: common_misreadings
    reason: "样例：常见误读待 W1 核"
    owner: "R-2 / 待指定"
    due: 2026-11-07
  - field: evidence_requirement
    reason: "样例：证据要求待 W1 从 Art.14/17 监督检查范围推导"
    owner: "R-1 / 待指定"
    due: 2026-11-07

```
