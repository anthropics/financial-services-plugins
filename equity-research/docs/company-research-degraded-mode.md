# Company Research Degraded Mode Policy

This document defines how the company research report agent must behave when evidence is incomplete, stale, or conflicting.

The purpose is to prevent fabricated confidence and keep the output honest and useful.

## Principle

If the agent lacks the evidence needed for a full report, it must downgrade the output rather than improvise.

## When To Trigger Degraded Mode

Trigger degraded mode when any of the following is true:

- the company cannot be uniquely identified
- there is no current official disclosure source
- current financial data is missing
- source conflicts affect core facts
- peer group cannot be established with reasonable support
- valuation inputs are missing or unreliable

## Section-Level Degradation (Class A initiating coverage)

Not all evidence gaps require full-report degradation. The following triggers cause **section-level degradation** while the overall report can remain Level A:

| Trigger | Affected section | Degradation behavior |
|---------|-----------------|---------------------|
| Comparable company data unavailable | §7.5.1 可比公司法 | Section appears with note: "数据不足，无法建立可比框架。缺失：[具体数据项]" |
| Only 1 fiscal year of financial data | §5 财务分析 | Section appears with reduced table (1 year only), note: "仅获取1个完整财年数据，趋势分析受限" |
| Revenue breakdown unavailable | §4 业务与竞争力分析 | Section notes: "收入结构未披露，以下分析基于合并口径" |
| Scenario assumptions lack quantitative basis | §7.5.3 情景分析 | Section appears with qualitative-only scenarios, note: "定量数据不足，仅提供定性情景描述" |
| Operating KPI historical data unavailable | §5.3 运营 KPI | Section notes: "核心运营指标历史数据不可得，无法展示趋势" |

**Rule: Sections must never be silently omitted.** A degraded section with an explicit data-gap note is always preferred over a missing section.

## Output Levels

### Level A: Full report allowed

Conditions:

- sufficient primary disclosure exists
- current financial data exists
- source conflicts are minor or resolved

Output:

- full draft report
- source appendix
- standard summary

### Level B: Analysis note only

Conditions:

- company is identifiable
- some official information exists
- but evidence is insufficient for a full report

Output:

- short-form company analysis note
- missing-data disclosure
- no strong valuation conclusion

### Level C: Clarification required

Conditions:

- company identity unclear
- disclosure unavailable
- request too ambiguous

Output:

- request clarification
- list missing inputs
- do not generate report content

## Mandatory Degraded Disclosures

Whenever degraded mode is triggered, the output must state:

- what information is missing
- why that matters
- what was still possible to analyze
- what the user can provide or what source needs to be added

## Forbidden In Degraded Mode

Do not output:

- formal rating
- target price
- precise unsupported financial projections
- unsupported peer conclusions
- fake certainty language

Avoid:

- `明确将`
- `必然`
- `确定会`
- `强烈看好`

Prefer:

- `当前证据不足以支持`
- `需继续补充`
- `现阶段判断偏审慎`
- `以下结论仅基于有限公开信息`

## Minimum Templates By Mode

### Level B template

Must include:

1. `当前可得结论`
2. `已确认事实`
3. `暂无法确认的关键问题`
4. `需补充的数据或资料`
5. `初步风险提示`

### Level C template

Must include:

1. `当前无法开始完整分析`
2. `原因`
3. `需要补充的信息`

## Completion Gate

If degraded mode is triggered, the task is complete only if:

- the correct downgraded format was used
- the missing-data disclosure is explicit
- no prohibited output appears
