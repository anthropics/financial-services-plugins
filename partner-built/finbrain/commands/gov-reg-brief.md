---
description: One-shot government and regulatory footprint for a ticker — Congressional trades, corporate lobbying, and federal contracts in a single brief
argument-hint: "<ticker> [lookback_days]"
---

# Government & Regulatory Brief

> This command uses FinBrain's Government & Regulatory tools: Congressional trades, corporate lobbying filings, and federal contract awards. See [CONNECTORS.md](../CONNECTORS.md) for the full tool reference.

Produce a consolidated brief on a ticker's government and regulatory exposure by combining Congressional trading disclosures, corporate lobbying activity, and federal contract awards.

See the **gov-reg-brief** skill for interpretation guidance on what clusters of activity mean.

## Workflow

### 1. Gather Inputs

Ask the user for:
- Ticker (required)
- Optional lookback window in days (default 365)
- Optional benchmark/peer ticker for comparison

### 2. Pull Congressional Trades

Call `house_trades_by_ticker` and `senate_trades_by_ticker` with the ticker and `date_from` set to today minus the lookback window.

Aggregate by politician, party (if inferable from roster), chamber, and trade type (buy vs sell). Count disclosures and dollar-range midpoints.

### 3. Pull Corporate Lobbying

Call `corporate_lobbying_by_ticker` with the same ticker and lookback.

Aggregate by quarter: total income (paid to registrants) and expenses (company's own lobbying team), top 3 registrants, top issue codes, and top government entities targeted.

### 4. Pull Federal Contracts

Call `government_contracts_by_ticker` with the same ticker and lookback, using `limit: 200` (keeps the payload aligned with other tools; large payloads slow the LLM even when the API is fast).

Aggregate by awarding agency (top 5), NAICS category, and total award value. Note the largest single award and its description.

### 5. Synthesize the Brief

Present four sections:
1. **Summary line** — one-sentence takeaway (e.g., "LMT shows heavy federal-contract concentration, modest Congressional trading flow, and top-decile lobbying spend").
2. **Congressional activity** — table of top traders and aggregate buy/sell counts, with any notable cluster flagged.
3. **Lobbying footprint** — quarterly spend trend, top registrants, top issue codes.
4. **Federal contracts** — total award value, top agencies, largest award, NAICS summary.

If a peer ticker was provided, include a side-by-side comparison row for each section.

## Output Format

Lead with the summary line, then the three data sections in the order above. Keep it scannable — tables preferred over prose where comparisons matter.
