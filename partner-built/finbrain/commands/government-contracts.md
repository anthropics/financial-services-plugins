---
description: Federal contract awards for a ticker — agency concentration, NAICS classification, and dollar exposure to US government spending
argument-hint: "<ticker> [lookback_years]"
---

# Government Contracts Analysis

> This command uses FinBrain's federal contract awards tool. See [CONNECTORS.md](../CONNECTORS.md) for the full tool reference.

Measure a company's exposure to US federal spending by analyzing contract awards from USAspending.gov.

See the **government-contracts** skill for USAspending data semantics and agency-concentration heuristics.

## Workflow

### 1. Gather Inputs

Ask the user for:
- Ticker (required)
- Optional lookback window in years (default 3)

### 2. Pull Contract Awards

Call `government_contracts_by_ticker` with the ticker and `date_from` set to today minus (lookback_years × 365 days). Use `limit` of 200 — keeps the payload aligned with other tools in this plugin and fits comfortably in the LLM context. If the response's `series_total` is materially larger than 200 and the user wants deeper history, page by narrowing `date_from`/`date_to` rather than raising the limit (large payloads slow the LLM even when the API is fast).

### 3. Aggregate Totals

Compute:
- Total contract value (sum of `award_amount`)
- Number of awards
- Average award size
- Largest single award (with description and awarding agency)

### 4. Agency Concentration

Rank awarding agencies (and sub-agencies when material) by total dollar value. Report:
- Top 5 agencies with dollar share of total
- Whether any single agency represents >50% of the total (concentration risk)

### 5. NAICS Classification

Group awards by `naics_code` / `naics_description`. Report the top 5 NAICS categories by dollar value. This reveals whether the company is winning its core-business work or expanding into adjacent categories.

### 6. Time Trend

Bucket awards by fiscal year (October–September). Report the year-over-year trend in award count and total value. Flag any year with >50% growth or decline.

### 7. Synthesize

Present the totals, top agencies, top NAICS, and FY trend. Close with a one-paragraph read-out: is this a core revenue stream or incidental? Is exposure concentrated in one agency? Is the book of business growing?

## Output Format

Lead with the dollar-total summary line. Follow with four tables (Totals, Top agencies, Top NAICS, FY trend) and the interpretation paragraph. Dollar amounts in USD millions.
