# Company Research Request Classification

This document defines how incoming user requests are classified for the company research report agent.

## Supported Classes

### Class A: Initiating coverage

Use when the user asks for:

- 首次覆盖
- initiation
- initiating coverage
- 深度报告
- 完整公司研究报告

Default output:

- full initiation-style draft

Mandatory analytical structures (see output-contract for details):

- 核心财务摘要表 (§5.1)
- 运营 KPI (§5.3)
- 可比公司表 (§7.5.1) — 至少 3 家可比公司
- 情景分析表 (§7.5.3) — Bull/Base/Bear
- 风险矩阵 (§8.1) — 按严重性×概率分层
- 反证与下行风险 (§8.2)
- 行内引用 ≥ 10 处
- 首页关键指标快照

Data insufficient: structure must still appear with explicit degradation note, not be omitted.

### Class B: Earnings review / company update

Use when the user asks for:

- 财报点评
- 业绩点评
- 更新观点
- based on latest earnings
- update note

Default output:

- update-style report draft

### Class C: General company analysis

Use when the user asks for:

- 分析一下某公司
- 看一下这家公司
- 给我一个公司研究初稿

Default output:

- standard company analysis draft
- use the approved Chinese template

### Class D: Clarification required

Use when:

- company identity is unclear
- request does not specify a company
- request is too vague to determine whether the user wants a report or a brief note

Default output:

- ask one concise clarification question

## Priority Rules

If multiple classes seem possible, use this order:

1. explicit earnings/update request -> Class B
2. explicit initiation/deep report request -> Class A
3. general company analysis request -> Class C
4. unclear request -> Class D

## Default Behavior

If the user only says:

- `分析一下 {company}`

then default to:

- Class C: General company analysis

Do not assume initiating coverage unless the request clearly implies a full initiation-style report.

## Completion Gate

Classification is complete only if:

- exactly one class is chosen
- the corresponding output path is clear
- ambiguity has been surfaced if necessary
