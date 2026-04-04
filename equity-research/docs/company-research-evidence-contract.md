# Company Research Evidence Collection Contract

This document defines the minimum evidence package required before the agent may draft a report.

It separates:

- mandatory evidence
- optional evidence
- drafting block conditions
- degraded-mode trigger conditions

## Core Principle

Drafting starts only after the minimum evidence threshold is met.

If the threshold is not met, the agent must switch to degraded mode or request clarification.

## Mandatory Evidence

### Company identity

Required:

- company legal or commonly accepted name
- ticker if public and available
- market or listing venue when relevant

Drafting block:

- company identity is ambiguous

### Primary company disclosure

Required:

- at least one official disclosure source

Examples:

- 10-K
- 10-Q
- annual report
- quarterly report
- exchange announcement
- official IR presentation

Drafting block:

- no current primary disclosure is available

### Current financial evidence

Required:

- at least one current financial evidence source

Examples:

- latest filing financials
- official results release
- structured current company facts

Drafting block:

- no current financial evidence exists

### Financial depth (Class A initiating coverage)

Required:

- at least 2 complete fiscal years of revenue, profit, and cash flow data
- latest period (quarterly or semi-annual) key metrics
- if unlisted, at least prospectus or funding round financial summary

Examples:

- FY2023 + FY2024 annual reports with income statement, balance sheet, cash flow
- latest quarterly filing (10-Q / semi-annual report)
- pre-IPO prospectus financials

Drafting block:

- zero fiscal years of structured financial data available

Degraded trigger:

- only 1 fiscal year available → report degrades to Level B (analysis note), explicitly labeled

### Revenue breakdown

Required (Class A):

- revenue split by business line, geography, or customer type

Degraded trigger:

- revenue breakdown unavailable → §4 must note "收入结构未披露，以下分析基于合并口径"

### Operating KPIs

Required (Class A):

- at least 2 core operating KPIs with historical data (2+ periods)
- KPIs should reference `sector-kpis-{sector}.md` when available

### Comparable company data (Class A)

Required:

- at least 3 comparable companies identified
- core valuation multiples for each (EV/Revenue, EV/EBITDA, P/E as applicable)

Degraded trigger:

- comparable data unavailable → valuation section must note "无法建立可比框架" with specific missing data items, not be omitted

### Company or market context

Required:

- at least one context source

Examples:

- company profile
- market profile data
- official company presentation
- official management communication

### Risk-oriented evidence

Required:

- at least one risk-oriented source or evidence set

Examples:

- filing risk factors
- recent risk disclosure
- material event disclosure

## Optional Evidence

Useful but not strictly required for every report:

- earnings transcript
- external industry dataset
- peer market data
- external event/news support

## Additional Requirements By Report Type

### Initiating coverage

Required minimum:

- primary disclosure (at least one official source)
- financial depth: 2+ fiscal years revenue/profit/cash flow + latest period
- revenue breakdown by segment/geography/customer
- 2+ core operating KPIs with historical trend
- 3+ comparable companies with valuation multiples
- market/profile context
- management communication or equivalent
- risk-oriented evidence

Recommended:

- earnings transcript
- industry dataset for sector context

### Earnings review / company update

Recommended minimum:

- latest results source
- recent company announcement or filing
- current financial evidence

## Drafting Block Conditions

The agent must not generate a full report draft if:

- company identity is unclear
- official disclosure is unavailable
- financial evidence is missing
- core facts are materially conflicting and unresolved

## Degraded-Mode Conditions

The agent may produce only a downgraded note if:

- company identity is clear
- some official evidence exists
- but the full-report threshold is not met

## Required Evidence Output Structure

Before drafting, the agent should be able to produce:

1. company identity summary
2. source inventory
3. current financial evidence summary
4. context evidence summary
5. risk evidence summary
6. evidence gaps

## Completion Gate

Evidence collection is complete only if:

- mandatory evidence is present or the run has explicitly switched to degraded mode
- the source inventory is explicit
- drafting block conditions have been checked
