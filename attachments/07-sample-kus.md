# 样例 KU（两份，YAML）

> 用于检验 29 字段与 locator 第 6 形态；W1 会重抄并做 Tier A 核验。

## gsk-eu-art14.yaml

```yaml
# 样例 KU：EU AI Act Art.14(1) 人工监督（29 字段 + gap 登记对象）
# 用途：证明 29 字段格式可落地；不是最终数据（W1 重抄 + Tier A 双人核）
ku_id: gsk-eu-art14
title: "Regulation (EU) 2024/1689 — Article 14(1) human oversight"
source_id: reg-eu-ai-act
jurisdiction: EU
instrument_type: regulation
instrument_is_binding: true
obligation_nature: obligation
obligation:
  - id: ob-1
    text: "High-risk AI systems shall be designed and developed, including with appropriate human-machine interface tools, so that they can be effectively overseen by natural persons during the period in which they are in use."
    subject: provider
    modality: obligation
evidence_requirement:
  - id: ev-1
    text: "Human-machine interface tools and oversight measures documented in the technical documentation."
    artefact: "technical documentation (Annex IV)"
    frequency: per_placing_on_market
applies_to:
  - subject: provider
    stage: develop
    scope: high-risk AI systems
  - subject: provider
    stage: deploy
    scope: high-risk AI systems
status: in_force
effective_date: 2027-12-02
transition_note: null
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
snapshot_ref: "snapshots/eu-ai-act-art14.md#p1"
first_seen: 2026-10-31T00:00:00-04:00
fingerprint: "minhash96:pending-w1"
# gap 是登记对象，不属于 29 字段
gap: []

```

## gsk-cn-genai-art7.yaml

```yaml
# 样例 KU：CN 生成式 AI 暂行办法 第七条 训练数据（29 字段 + gap 登记对象）
# 注意：locator 使用设计 §5.2 C4 新增的第 6 形态「中国条款式」
ku_id: gsk-cn-genai-art7
title: "生成式人工智能服务管理暂行办法 第七条（训练数据处理）"
source_id: reg-cn-genai
jurisdiction: CN
instrument_type: regulation
instrument_is_binding: true
obligation_nature: obligation
obligation:
  - id: ob-1
    text: "使用具有合法来源的数据和基础模型。"
    subject: provider
    modality: obligation
  - id: ob-2
    text: "涉及知识产权的，不得侵害他人依法享有的知识产权。"
    subject: provider
    modality: prohibition
  - id: ob-3
    text: "涉及个人信息的，应当取得个人同意或者符合法律、行政法规规定的其他情形。"
    subject: provider
    modality: obligation
  - id: ob-4
    text: "采取有效措施提高训练数据质量，增强训练数据的真实性、准确性、客观性、多样性。"
    subject: provider
    modality: obligation
  - id: ob-5
    text: "遵守网络安全法、数据安全法、个人信息保护法等法律、行政法规的其他有关规定和有关主管部门的相关监管要求。"
    subject: provider
    modality: obligation
evidence_requirement:
  - id: ev-1
    text: "训练数据来源、规模、类型、标注规则等说明材料（监督检查时提供）。"
    artefact: training_data_register
    frequency: on_request
applies_to:
  - subject: provider
    stage: develop
    scope: 向境内公众提供生成式人工智能服务的组织、个人
status: in_force
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
snapshot_ref: "snapshots/cn-genai-art7.md#art7"
first_seen: 2026-10-31T00:00:00-04:00
fingerprint: "minhash96:pending-w1"
gap: []

```
