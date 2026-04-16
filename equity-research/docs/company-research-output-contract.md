# Company Research Output Contract

This document defines the required output structures for the company research report agent.

## Output Types

### Output A: Full report success

Must contain:

- company name
- report type
- summary findings
- Feishu Doc URL
- source/scope note

May also contain:

- internal markdown artifact reference

Must not contain by default:

- formal rating
- target price

### Output B: Degraded analysis success

Must contain:

- company name
- degraded status
- current conclusions
- missing-data disclosure
- next-step or missing-input note

If a degraded note is delivered successfully in Feishu, it must also contain:

- Feishu Doc URL

### Output C: Clarification required

Must contain:

- reason the task cannot proceed
- exact clarification needed

## Full Report Artifact Requirements

The artifact must include:

- the approved Chinese section structure (§1-§9)
- `数据来源与口径说明`
- risk section with severity classification (高/中/低)

### Analytical Structure Requirements (by report type)

#### Class A (首次覆盖) — all required unless degraded

| Structure | Requirement |
|-----------|-------------|
| 核心财务摘要表 (§5.1) | 必填。至少 7 行指标 × 2 年数据，每行有来源列 |
| 运营 KPI (§5.3) | 必填。至少 2 个核心 KPI 含历史趋势 |
| 可比公司表 (§7.5.1) | 必填。至少 3 家可比公司 + 选择理由。数据不足时标注"数据不足，无法建立可比框架" |
| 情景分析表 (§7.5.3) | 必填。Bull/Base/Bear 含概率权重和核心假设。数据不足时标注原因 |
| 风险矩阵 (§8.1) | 必填。按严重性×概率分层 |
| 反证与下行风险 (§8.2) | 必填。至少一条与核心结论相反的反证线索 |
| 行内引用 | 正文 ≥ 10 处行内引用 |
| 首页指标快照 | 必填。关键财务指标 + Bull/Base/Bear 一行摘要 |

#### Class B (公司更新/财报点评) — 简化

| Structure | Requirement |
|-----------|-------------|
| 核心财务摘要表 (§5.1) | 必填。可只含最新 1-2 期 |
| 运营 KPI (§5.3) | 推荐 |
| 可比公司表 (§7.5.1) | 可选 |
| 情景分析表 (§7.5.3) | 可选 |
| 风险矩阵 (§8.1) | 推荐 |
| 行内引用 | 正文 ≥ 5 处行内引用 |

#### Class C/D (一般分析/快速简报) — 最低

| Structure | Requirement |
|-----------|-------------|
| 核心财务摘要表 (§5.1) | 推荐 |
| 行内引用 | 正文 ≥ 3 处行内引用 |

### Degradation Rules for Analytical Structures

When required data is unavailable:

- The structure itself must still appear in the report
- Content is replaced with explicit degradation note: "当前证据不足以完成此分析，缺失：[具体数据项]"
- The structure must not be silently omitted

The user-facing artifact for successful report runs must be a Feishu Doc.
Local markdown is an internal artifact, not the primary delivery surface.

## Summary Requirements

The summary must include:

- 3-5 key findings at most
- no exaggerated recommendation wording
- a scope or evidence note
- the Feishu Doc URL for successful report runs

## Completion Gate

An output passes contract review only if:

- it matches one of the defined output types
- required fields are present
- prohibited default items are absent
- successful report responses include a usable Feishu Doc URL
