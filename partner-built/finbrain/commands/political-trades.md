---
description: Deep dive into US Congressional (House and Senate) stock disclosures for a ticker, with politician-level breakdown and timing analysis
argument-hint: "<ticker> [lookback_days]"
---

# Political Trades Analysis

> This command uses FinBrain's Congressional trading tools. See [CONNECTORS.md](../CONNECTORS.md) for the full tool reference.

Analyze US House and Senate stock transactions in a ticker — who traded, how much, when, and whether the pattern suggests coordinated activity or leads news events.

See the **political-trades** skill for STOCK Act disclosure mechanics and the 45-day reporting lag.

## Workflow

### 1. Gather Inputs

Ask the user for:
- Ticker (required)
- Optional lookback window in days (default 365)

### 2. Pull House Trades

Call `house_trades_by_ticker` with the ticker and `date_from` set to today minus the lookback window. Use `limit` of 500.

### 3. Pull Senate Trades

Call `senate_trades_by_ticker` with the same parameters.

### 4. Aggregate and Analyze

Merge both datasets and compute:
- Total disclosures (count, split by chamber)
- Top 10 politicians by disclosure count, each with their buy/sell split and dollar-range midpoint sum
- Trade-type distribution (purchase, sale, exchange, etc.)
- Time-series histogram by month to spot clusters
- Note any transaction dated within 45 days (often reported late — flag for potential recent activity)

### 5. Flag Noteworthy Patterns

Surface:
- **Cluster buying** — 3+ politicians buying the same ticker in a 30-day window
- **Cluster selling** — 3+ politicians selling within 30 days (often precedes bad news)
- **Committee overlap** — if the user asks, cross-reference with relevant committee assignments (mention qualitatively; FinBrain does not provide committee data directly)
- **Party skew** — if one party dominates, note it

### 6. Synthesize

Present the top-politicians table, chamber split, cluster flags, and a one-paragraph interpretation tying the pattern back to any concurrent news, earnings, or legislative events the user should look into.

## Output Format

Lead with the count + cluster-flag summary, then the top-politicians table, then the time-series histogram (ASCII bar chart is fine), then the interpretation paragraph.
