# Company Research Recency And Authority Gate

This document defines when evidence is too stale or too weak to support a current company analysis report.

The purpose is to stop the agent from generating 2026-facing reports from outdated or low-authority material.

## Core Rule

For a current company analysis report, the agent must prefer the newest authoritative evidence first.

If the newest authoritative evidence cannot be found, the agent must not quietly proceed as though the report is current.

## Authority Order

Use this order unless the user explicitly changes it:

1. official company disclosure
2. exchange or regulator disclosure
3. official company IR / results presentation / management communication
4. auditable market or fundamentals provider
5. news and third-party summaries

Rules:

- core conclusions must not rely only on tier 5 sources
- financial conclusions must not rely only on media summaries
- if tier 1-3 evidence conflicts with tier 5, trust tier 1-3

## Recency Checks

Before drafting a current report, explicitly determine:

1. latest formal reporting period available
2. latest disclosure date available
3. latest management communication date available, if any
4. latest price/market snapshot date used

## Drafting Rules By Evidence Age

### Current full report allowed

Allowed only if:

- the latest formal reporting period is identified
- at least one current official disclosure is used
- current financial evidence exists for the latest available period

### Degraded or historical note only

Use degraded mode or explicitly historical framing if:

- only older reporting periods are available
- latest official disclosure cannot be located
- the report would otherwise present stale facts as current

Required wording:

- `以下判断基于截至 {date} 的公开资料`
- `当前未取到更新至更近披露期的正式资料`

### Full report blocked

Block a current deep report if:

- no official disclosure is available
- the latest available data is materially stale for the requested purpose
- only media summaries exist for core claims

## High-Value Retrieval Prompting Rule

When asking the LLM to search or retrieve, force it to prioritize high-value evidence.

Use prompting that makes the model explicitly prefer:

- newest official filings
- newest exchange announcements
- newest official IR/results materials
- newest management remarks
- only then secondary context

Recommended instruction:

`优先检索最新且最有价值的资料。先找公司正式披露、交易所公告、年报/中报/季报、业绩会和官方IR材料；再找可复核市场数据；最后才补充新闻和二手解读。若拿不到最新正式披露期资料，不要把旧资料包装成当前结论，必须明确写出截至日期和缺口。`

## Required Pre-Draft Output

Before drafting, the agent should be able to state:

- latest reporting period used
- latest disclosure date used
- primary authoritative sources used
- stale or missing evidence gaps

## Completion Gate

The recency and authority gate is satisfied only if:

- latest official period/date checks were performed
- source authority order was followed
- stale evidence was either disclosed, downgraded, or blocked
