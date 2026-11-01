# CCC Round-6 处置（v0.6 终态）

> 报告：`docs/review/ccc-report-v06.md`（绑定 v0.6 `206da0cd…`，verified）
> 结论：**B 有条件通过 ｜ Block 1 / Major 11 / Minor 4**。
> 本轮不再改设计（goal 结束）；下表如实记录"已落/未落/延后"，供恢复时直接执行。

## V6-01（Block）：处置表与正文不符 → 本表更正

CCC 指出 9 项标"采纳"但正文无对应文字。**以本表为准**：

| V5 项 | 此前写法 | 正文实际 | 更正状态 |
|---|---|---|---|
| V5-04 跨语言规范化 | 采纳 | §7.1 仍写"与 sentence 语言一致"，无映射表 | **未落 → v0.7** |
| V5-05 核验路径/CK-03 第 3 项 | 采纳 | §5.3 CK-03 原样 | **未落 → v0.7** |
| V5-06 R2/expired | 采纳 | R2 仍写"双人核"；derive_mode 无 expired | **部分 → v0.7** |
| V5-07 锚点/元数据/实名 | 采纳 | `#Art.14(1)`、`excerpt_hash`、`R-2 / 张三` 仍在 | **未落 → v0.7** |
| V5-12 关键词/no_llm | 采纳 | 无关键词表、无 no_llm 定义 | **未落 → v0.7** |
| V5-15 人日分项 | 采纳 | §10 仍"20–24 人日" | **未落 → v0.7** |
| V5-16 稳定性/用例数 | 采纳 | 未改 | **未落 → v0.7** |
| V5-18 §8 移 backlog | 采纳 | §8 整节仍在正文 | **未落 → v0.7** |
| V5-21 版本残留 | 采纳 | "升 v0.2"、"v0.1" 表头仍在 | **未落 → v0.7** |

> 今后规则：处置表每行必须有 `§号 + 引文`，由脚本核对引文存在；否则不得标"已落"。

## 其余发现处置（恢复后 v0.7）

| # | 级别 | 处置 |
|---|---|---|
| V6-02 | Major | **转用户裁定**：英文 KU 的中文候选句来源（A 英文原文+中文固定框架 / B 经核验译文字段） |
| V6-03 | Major | 结论词表改闭合文件 + 模式匹配（"你们/贵司"+"适用/合规"）；例外改 `verbatim:true` 标记；补 #7 正例 |
| V6-04 | Major | token 改 HMAC 或服务端记录 `(answer_id, hash)`；指标二选一；`grc verify-answer` |
| V6-05 | Major | 候选句加 `required/order`；validate 校验必选句与顺序 |
| V6-06 | Major | 拆 `scope_note_codes` 与 `coverage_codes`；refusal 判定顺序；统一 #4；定义 expired |
| V6-07 | Major | 统一 §4.2.1 与 §7.4 入参/错误码；清理 §0/§7.2/§7.3 旧"LLM 措辞"；定义 no_llm |
| V6-08 | Major | 锚点 `art14-1`；C1/§6.1 去 `excerpt_hash`；示例去实名；样例 snapshot_ref 对齐 |
| V6-09 | Major | CK-03 执行环境/密文存放；按来源写 online/manual；剔除不可抓源第 3 项 |
| V6-10 | Major | CK-14 改 `absence_kind`/`absence_terms` + 全文 0 命中；补 CN 条目 |
| V6-11 | Major | 分项人日（工程 16–19 / 研究 8–10）；R2 改单人；用例数量 |
| V6-12 | Major | 检查 evidence 随包附数据文件或 sha256 清单 |
| V6-13 | Minor | §8 移 backlog；版本残留清理 |
| V6-14 | Minor | coverage 计数生成；#1 补全 coverage_codes |
| V6-15 | Minor | R10 增 var/answers 例外；并发用例 |
| V6-16 | Minor | evidence.cmd 单条 grc 或定义解析 |

## 结论

架构与方向被 CCC 认可；当前 **Block 只有"文档与声明不同步"**，不是设计缺陷。恢复后先做 v0.7（纯文档/规格收紧，约 0.5–1 人日），再请 CCC 做 Round-7 或由用户批准 W1-0。
