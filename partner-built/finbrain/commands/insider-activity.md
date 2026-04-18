---
description: SEC Form 4 insider activity for a ticker — officer and director buys and sells with cluster detection and dollar-weighted flow
argument-hint: "<ticker> [lookback_days]"
---

# Insider Activity

> This command uses FinBrain's insider transactions tool. See [CONNECTORS.md](../CONNECTORS.md) for the full tool reference.

Analyze SEC Form 4 insider transactions for a ticker: who is buying, who is selling, how much, and whether clusters of activity suggest informed conviction.

See the **insider-activity** skill for Form 4 transaction-code semantics and cluster-buying heuristics.

## Workflow

### 1. Gather Inputs

Ask the user for:
- Ticker (required)
- Optional lookback window in days (default 180)

### 2. Pull Insider Transactions

Call `insider_transactions_by_ticker` with the ticker and `date_from` set to today minus the lookback. Use `limit` of 500.

### 3. Aggregate

Compute:
- Total transactions (count, split by buy vs sell)
- Total USD value of buys vs sells (net dollar flow)
- Top 5 insiders by total dollar value, each with role (`relationship`) and net direction
- Transaction-type distribution (open-market buy/sell, option exercise, planned sale, gift, etc.)

### 4. Detect Clusters

Flag any 30-day window where 3+ distinct insiders bought on the open market. Open-market buys (rather than option exercises or planned 10b5-1 sales) are the highest-conviction signal. Report date range, insider names, and total dollar value.

Similarly flag 30-day windows with 3+ distinct open-market sells by C-suite officers — these can precede negative news but may also reflect diversification.

### 5. Filter Noise

Exclude or footnote:
- 10b5-1 planned sales (pre-scheduled, low signal)
- Option exercises with immediate sale (tax optimization, low signal)
- Small gifts or trust-related transfers

The high-signal category is **discretionary open-market purchases by officers/directors**.

### 6. Synthesize

Present the net-dollar-flow summary, top-insiders table, cluster flags, and a read-through paragraph: is insider sentiment bullish (cluster buying, low selling), bearish (heavy officer selling, no buys), or mixed?

## Output Format

Lead with the net-flow line ($X M bought vs $Y M sold, net). Follow with the top-insiders table, cluster-flag list, transaction-type breakdown, and interpretation paragraph.
