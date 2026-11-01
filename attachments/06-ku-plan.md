# KU 拆分计划（53 条：EU 33 + CN 20）

> 状态：**W1 输入草案**（不是最终 KU）。每条在 W1 按 29 字段填写、逐字抄录 `verbatim_excerpt`、做 Tier A 核验。
> 来源版本：EU = consolidated 2026-07-27；CN = 暂行办法 2023-08-15 / 标识办法 2025-09-01。
> `obligation_nature` 为初判，W1 按原文复核；`locator` 的 CN 形态见设计 §5.2 C4（新增第 6 形态）。

## EU AI Act（32）

| # | ku_id | locator | 标题 | nature | 备注（W1 抄录位置） |
|---|---|---|---|---|---|
| 1 | gsk-eu-art2 | Art.2 | 适用范围与域外效力 | definition | Art.2(1)(a)-(c) |
| 2 | gsk-eu-art5-ab | Art.5(1)(a)-(b) | 操纵/利用脆弱性 | prohibition | 两条合并为 1 KU |
| 3 | gsk-eu-art5-ba | Art.5(1)(ba) | 生成真实人物影像（omnibus 新增） | prohibition | 抓取上线日 2026-12-02 |
| 4 | gsk-eu-art5-bb | Art.5(1)(bb) | 儿童性虐待材料（omnibus 新增） | prohibition | 同上 |
| 5 | gsk-eu-art5-c | Art.5(1)(c) | 社会评分 | prohibition | |
| 6 | gsk-eu-art5-d | Art.5(1)(d) | 犯罪风险预测 | prohibition | |
| 7 | gsk-eu-art5-e | Art.5(1)(e) | 人脸抓取建库 | prohibition | |
| 8 | gsk-eu-art5-f | Art.5(1)(f) | 工作/教育场景情绪推断 | prohibition | |
| 9 | gsk-eu-art5-g | Art.5(1)(g) | 生物特征分类 | prohibition | |
| 10 | gsk-eu-art5-h | Art.5(1)(h)+Art.5(2) | 执法实时远程生物识别 | prohibition | 含例外与授权 |
| 11 | gsk-eu-art6-1 | Art.6(1) | 产品安全法下的高风险 | definition | Annex I |
| 12 | gsk-eu-art6-2 | Art.6(2) | Annex III 高风险 | definition | |
| 13 | gsk-eu-art6-3 | Art.6(3) | 例外：不构成高风险 | definition | 需画像判定 |
| 14 | gsk-eu-annex3-a | Annex III 1–4 | 生物识别/基础设施/教育/就业 | definition | 分类清单 A |
| 15 | gsk-eu-annex3-b | Annex III 5–8 | 基本服务/执法/移民/司法 | definition | 分类清单 B |
| 16 | gsk-eu-art8 | Art.8 | 合规总则 | obligation | |
| 17 | gsk-eu-art9 | Art.9 | 风险管理体系 | obligation | |
| 18 | gsk-eu-art10 | Art.10 | 数据与数据治理 | obligation | |
| 19 | gsk-eu-art11 | Art.11 | 技术文档 | obligation | Annex IV |
| 20 | gsk-eu-art12 | Art.12 | 日志记录 | obligation | |
| 21 | gsk-eu-art13 | Art.13 | 向部署者提供信息/说明 | obligation | |
| 22 | gsk-eu-art14 | Art.14 | 人工监督 | obligation | 样例见 `sample-kus/` |
| 23 | gsk-eu-art15 | Art.15 | 准确性/鲁棒性/网络安全 | obligation | |
| 24 | gsk-eu-art16 | Art.16 | 提供者义务清单 | obligation | (a)-(l) 可拆子项 |
| 25 | gsk-eu-art26-1 | Art.26(1)-(2) | 部署者：按说明使用 + 指派监督 | obligation | |
| 26 | gsk-eu-art26-2 | Art.26(3)-(6) | 部署者：监控/事件/记录 | obligation | |
| 27 | gsk-eu-art26-3 | Art.26(7)-(9) | 部署者：告知/工人代表 | obligation | |
| 28 | gsk-eu-art27 | Art.27 | 基本权利影响评估（FRIA） | obligation | |
| 29 | gsk-eu-art43 | Art.43 | 合格评定 | obligation | 第三方 vs 内控 |
| 30 | gsk-eu-art50-1 | Art.50(1) | 与自然人交互的披露 | obligation | |
| 31 | gsk-eu-art50-2 | Art.50(2) | 合成内容标识 | obligation | |
| 32 | gsk-eu-art50-34 | Art.50(3)-(4) | 情绪识别/生物分类披露、深伪 | obligation | |
| 33 | gsk-eu-art113 | Art.113 | 生效与适用时间线 | definition | 合并版日期 |

> 计数：上表 33 行（含 Art.113）；CN 13 + 7 = 20；合计 **53**。

## CN《生成式人工智能服务管理暂行办法》（13）

| # | ku_id | locator | 标题 | nature |
|---|---|---|---|---|
| 1 | gsk-cn-genai-art2 | 第二条 | 适用范围；内部研发/使用不适用 | definition |
| 2 | gsk-cn-genai-art4 | 第四条 | 内容底线（禁止生成内容） | prohibition |
| 3 | gsk-cn-genai-art7 | 第七条 | 训练数据处理五项规定 | obligation（样例） |
| 4 | gsk-cn-genai-art8 | 第八条 | 数据标注规则与质量评估 | obligation |
| 5 | gsk-cn-genai-art9 | 第九条 | 内容生产者责任、服务协议 | obligation |
| 6 | gsk-cn-genai-art10 | 第十条 | 适用人群/场合/用途、未成年人 | obligation |
| 7 | gsk-cn-genai-art11 | 第十一条 | 输入与使用记录保护 | obligation |
| 8 | gsk-cn-genai-art14 | 第十四条 | 违法内容处置与报告 | obligation |
| 9 | gsk-cn-genai-art17 | 第十七条 | 安全评估 + 算法备案 | obligation |
| 10 | gsk-cn-genai-art20 | 第二十条 | 境外向境内提供的处置 | obligation |
| 11 | gsk-cn-genai-art21 | 第二十一条 | 法律责任（转致 + 警告/通报/改正） | obligation |
| 12 | gsk-cn-genai-art22 | 第二十二条 | 用语定义 | definition |
| 13 | gsk-cn-genai-art24 | 第二十四条 | 施行日期 | definition |

## CN《人工智能生成合成内容标识办法》（7）

| # | ku_id | locator | 标题 | nature |
|---|---|---|---|---|
| 1 | gsk-cn-label-art3 | 第三条 | 生成合成内容 / 显式 / 隐式标识定义 | definition |
| 2 | gsk-cn-label-art4 | 第四条 | 显式标识要求 | obligation |
| 3 | gsk-cn-label-art5 | 第五条 | 隐式标识（元数据/水印） | obligation |
| 4 | gsk-cn-label-art6 | 第六条 | 传播平台核验与提示 | obligation |
| 5 | gsk-cn-label-art7 | 第七条 | 应用分发平台核验 | obligation |
| 6 | gsk-cn-label-art9 | 第九条 | 无显式标识的申请与 6 个月日志 | obligation |
| 7 | gsk-cn-label-art10 | 第十条 | 用户主动声明与禁止篡改 | obligation |

## 合计与验收

- EU 33 + CN 20 = **53**（设计写"约 50"，+6%）；若 W1 超时，先合并 Art.5 的 (a)(b) 与 (ba)(bb) 两组、再砍 Art.26(7)-(9)。
- 每条 KU 的准入：29 字段齐、`verbatim_excerpt` 逐字、`locator` 命中 6 形态之一、`applies_to` 结构化、Tier A 双人核。
- 20 金标必须由这批 KU 可答或可拒（映射见 `source-map.md` §5）。
