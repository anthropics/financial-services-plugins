# Company Research Source Hierarchy And Citation Rules

This document defines the mandatory evidence hierarchy for the company research report agent.

Use it whenever the agent gathers facts, resolves conflicting evidence, cites sources, or decides whether a report can proceed.

## Core Principle

Official and auditable sources outrank narrative and media sources.

Do not let a lower-priority source override a higher-priority source without explicit justification.

## Source Priority

Use this ranking unless the user explicitly overrides it.

### Tier 1: Official regulatory and company disclosure

Highest priority:

- annual reports
- quarterly reports
- prospectuses
- exchange announcements
- SEC filings
- company IR presentations
- official press releases
- formal shareholder materials

Use for:

- company facts
- financial results
- segment definitions
- risk disclosures
- management commentary that appears in official materials

### Tier 2: Auditable or official-market reference data

Second priority:

- exchange market data
- official index providers
- official reference pricing
- custody or settlement reference entities
- structured company facts from regulatory datasets

Use for:

- share price history
- market cap
- benchmark data
- official corporate action reference

### Tier 3: Public management communication

Third priority:

- earnings calls
- conference remarks
- investor day transcripts
- management interviews on official channels

Use for:

- strategy interpretation
- near-term commentary
- management framing of current performance

Do not let this tier override formal filings on hard facts.

### Tier 4: Market and industry data providers

Fourth priority:

- OpenBB-backed market sources
- transcript providers
- sector datasets
- external industry data services

Use for:

- peer screens
- market context
- industry benchmarks
- non-core supplementary metrics

### Tier 5: News and media coverage

Lowest priority:

- financial news
- interviews republished by media
- secondary market commentary
- third-party summaries

Use for:

- event awareness
- timeline support
- supplementary context only

News must not be the sole basis for a core report conclusion.

## Conflict Resolution

If sources disagree, resolve in this order:

1. latest formal filing or exchange/company announcement
2. notes to financial statements and official attachments
3. public management remarks on official or transcripted channels
4. structured provider data
5. media interpretation

If the conflict remains unresolved:

- say the evidence is inconsistent
- name the conflicting sources
- avoid precise unsupported claims
- downgrade the report if the conflict affects a core conclusion

## Mandatory Citation Rules

Every report draft must contain:

- a `数据来源与口径说明` section
- explicit source disclosure for major financial and factual claims
- source disclosure for valuation inputs and peer-selection rationale

### Claims that must cite a source

The following require explicit attribution:

- revenue, profit, margin, cash flow, debt, and other financial figures
- company history facts when not universally known
- customer concentration or business mix claims
- TAM, market share, or industry growth claims
- management quotations or management positioning
- catalyst statements tied to specific events or filings
- unusual or controversial claims

### Claims that may use lighter attribution

The following can use section-level attribution if supported by nearby evidence:

- high-level business description
- plain-language summaries of product positioning
- non-controversial synthesis based on already cited material

## Citation Format Rules

For V1, the minimum acceptable standard is:

- cite source type
- cite source name
- cite source date when available

Preferred examples:

- `来源：公司2025年年报`
- `来源：公司2025Q4业绩会纪要`
- `来源：深交所公告，2026-03-01`
- `来源：SEC 10-K filed on 2026-02-18`

If hyperlinks are available, preserve them in the exported artifact where practical.

## Prohibited Evidence Behavior

Do not:

- cite news as the only support for a core company conclusion
- treat unsourced market rumor as evidence
- fill missing values with confident fabricated estimates
- let transcript rhetoric override hard numbers from filings

## Minimum Evidence Threshold Before Drafting

Do not produce a full report draft unless the agent has, at minimum:

- one primary company disclosure source
- one current financial source
- one company or market context source
- one risk-oriented source or evidence set

If these are missing, switch to degraded mode.

## Degraded Mode Trigger

Switch to degraded mode if any of the following are true:

- no current primary disclosure can be found
- financial figures are stale or inconsistent
- the company cannot be confidently identified
- only media summaries are available for critical claims

In degraded mode:

- produce a limited analysis
- disclose what is missing
- avoid strong valuation or investment conclusions

## Completion Gate

A report draft does not pass evidence review unless:

- source priority has been respected
- conflicting evidence is either resolved or disclosed
- the source appendix exists
- major financial and factual claims are attributable
