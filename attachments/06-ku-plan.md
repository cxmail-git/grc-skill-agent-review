# KU 拆分计划（52 条：EU 32 + CN 20）· v0.2

> W1 输入草案；每条在 W1 按 29 字段填写、逐字抄录、Tier A 核验。
> v0.2 修正：**单 locator（禁区间）**，按预演 F-01/F-08 改为 7 形态可表达的值；未收录项登记 `scope_exclusions.yaml`。
> 来源版本：EU = consolidated 2026-07-27；CN = 暂行办法 2023-08-15 / 标识办法 2025-09-01。

## EU AI Act（32）

| # | ku_id | locator | 标题 | nature |
|---|---|---|---|---|
| 1 | gsk-eu-art2 | Art.2 | 适用范围与域外效力 | definition |
| 2 | gsk-eu-art5-d | Art.5(1)(d) | 犯罪风险预测禁止 | prohibition |
| 3 | gsk-eu-art5-c | Art.5(1)(c) | 社会评分禁止 | prohibition |
| 4 | gsk-eu-art5-e | Art.5(1)(e) | 人脸抓取建库禁止 | prohibition |
| 5 | gsk-eu-art5-f | Art.5(1)(f) | 工作/教育情绪推断禁止 | prohibition |
| 6 | gsk-eu-art5-g | Art.5(1)(g) | 生物特征分类禁止 | prohibition |
| 7 | gsk-eu-art5-h | Art.5(1)(h) | 执法实时远程生物识别禁止 | prohibition |
| 8 | gsk-eu-art5-ba | Art.5(1)(ba) | 生成真实人物影像（omnibus 新增） | prohibition |
| 9 | gsk-eu-art6-1 | Art.6(1) | 产品安全法下的高风险 | definition |
| 10 | gsk-eu-art6-2 | Art.6(2) | Annex III 高风险 | definition |
| 11 | gsk-eu-art6-3 | Art.6(3) | 例外：不构成高风险 | definition |
| 12 | gsk-eu-annex3-1 | Annex III point 1 | 生物识别类高风险 | definition |
| 13 | gsk-eu-annex3-3 | Annex III point 3 | 教育类高风险 | definition |
| 14 | gsk-eu-annex3-4 | Annex III point 4 | 就业类高风险 | definition |
| 15 | gsk-eu-annex3-5 | Annex III point 5 | 基本服务类高风险 | definition |
| 16 | gsk-eu-art8 | Art.8 | 合规总则 | obligation |
| 17 | gsk-eu-art9 | Art.9 | 风险管理体系 | obligation |
| 18 | gsk-eu-art10 | Art.10 | 数据与数据治理 | obligation |
| 19 | gsk-eu-art11 | Art.11 | 技术文档 | obligation |
| 20 | gsk-eu-art12 | Art.12 | 日志记录 | obligation |
| 21 | gsk-eu-art13 | Art.13 | 向部署者提供信息 | obligation |
| 22 | gsk-eu-art14 | Art.14 | 人工监督 | obligation |
| 23 | gsk-eu-art15 | Art.15 | 准确性/鲁棒性/网络安全 | obligation |
| 24 | gsk-eu-art16 | Art.16 | 提供者义务清单 | obligation |
| 25 | gsk-eu-art26-1 | Art.26(1) | 部署者：按说明使用 | obligation |
| 26 | gsk-eu-art26-2 | Art.26(2) | 部署者：指派人工监督 | obligation |
| 27 | gsk-eu-art26-5 | Art.26(6) | 部署者：日志保存 | obligation |
| 28 | gsk-eu-art27 | Art.27 | 基本权利影响评估 | obligation |
| 29 | gsk-eu-art50-1 | Art.50(1) | 与自然人交互的披露 | obligation |
| 30 | gsk-eu-art50-2 | Art.50(2) | 合成内容标识 | obligation |
| 31 | gsk-eu-art50-3 | Art.50(3) | 情绪/生物分类披露 | obligation |
| 32 | gsk-eu-art113 | Art.113 | 生效与适用时间线 | definition |

**未收录（登记 `scope_exclusions.yaml`）**：Art.5 其余项（a/b/bb）；Annex III 其余类别（2/6/7/8）；Art.17/19/43/49/99；GPAI 章 Art.51–56。

## W2-5：EU 32 已全部入库（2026-11-01）

W1-7 的 20 条 + W2-5 的 12 条 = EU 32；CN 20 中目前仅 art7，其余留 W3。

## W1-7 入选 20（EU）

`Art.2`、`Art.5(1)(c/d/e/f/g/h/ba)`、`Art.6(1/2/3)`、`Annex III point 1/3/4/5`、`Art.8/9/10/11/14`。其余 12 条 EU 留 W2。

## CN《生成式人工智能服务管理暂行办法》（13）

| # | ku_id | locator | 标题 | nature |
|---|---|---|---|---|
| 1 | gsk-cn-genai-art2 | 第二条 | 适用范围；内部研发/使用不适用 | definition |
| 2 | gsk-cn-genai-art4 | 第四条 | 内容底线 | prohibition |
| 3 | gsk-cn-genai-art7 | 第七条 | 训练数据处理 | obligation |
| 4 | gsk-cn-genai-art8 | 第八条 | 数据标注规则 | obligation |
| 5 | gsk-cn-genai-art9 | 第九条 | 内容生产者责任、服务协议 | obligation |
| 6 | gsk-cn-genai-art10 | 第十条 | 适用人群/场合/用途、未成年人 | obligation |
| 7 | gsk-cn-genai-art11 | 第十一条 | 输入与使用记录保护 | obligation |
| 8 | gsk-cn-genai-art14 | 第十四条 | 违法内容处置 | obligation |
| 9 | gsk-cn-genai-art17 | 第十七条 | 安全评估 + 算法备案 | obligation |
| 10 | gsk-cn-genai-art20 | 第二十条 | 境外向境内提供的处置 | obligation |
| 11 | gsk-cn-genai-art21 | 第二十一条 | 法律责任 | obligation |
| 12 | gsk-cn-genai-art22 | 第二十二条 | 用语定义 | definition |
| 13 | gsk-cn-genai-art24 | 第二十四条 | 施行日期 | definition |

## CN《人工智能生成合成内容标识办法》（7）

| # | ku_id | locator | 标题 | nature |
|---|---|---|---|---|
| 1 | gsk-cn-label-art3 | 第三条 | 生成合成内容/显式/隐式标识定义 | definition |
| 2 | gsk-cn-label-art4 | 第四条 | 显式标识要求 | obligation |
| 3 | gsk-cn-label-art5 | 第五条 | 隐式标识（元数据/水印） | obligation |
| 4 | gsk-cn-label-art6 | 第六条 | 传播平台核验与提示 | obligation |
| 5 | gsk-cn-label-art7 | 第七条 | 应用分发平台核验 | obligation |
| 6 | gsk-cn-label-art9 | 第九条 | 无显式标识申请 + 6 个月日志 | obligation |
| 7 | gsk-cn-label-art10 | 第十条 | 用户主动声明、禁止篡改 | obligation |

## 合计与门禁

- EU 32 + CN 20 = **52**；20 金标必须由这批 KU 可答/可拒（映射见 `source-map.md` §5）。
- 每条准入：29 字段齐、`verbatim_excerpt` 逐字、`obligation[].text` 为 excerpt 连续子串（否则 `paraphrase: true` 且禁入 citation）、locator 命中 7 形态、Tier A 双人核。
- 区间值（如 `Art.26(1)-(2)`）**禁止**；已按款拆。
