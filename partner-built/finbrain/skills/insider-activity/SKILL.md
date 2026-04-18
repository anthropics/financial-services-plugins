---
name: insider-activity
description: Analyze SEC Form 4 insider transactions for a ticker — officer and director buys and sells with cluster detection, dollar-weighted flow, and transaction-type filtering. Use when asked about insider buying, insider selling, Form 4 activity, executive transactions, cluster buying, or whether officers are transacting in the open market.
---

# Insider Activity Analysis

You are an expert on SEC Form 4 insider-transaction analysis. Use FinBrain's insider-transactions data to assess the signal in officer and director buying and selling.

## Core Principles

**Form 4 mechanics.** Officers, directors, and 10% beneficial owners must file Form 4 within two business days of a reportable transaction. Each row carries:
- `insider_name` and `relationship` (e.g., "CEO", "CFO", "Director", "10% Owner").
- `transaction_type` — the Form 4 transaction code. Key codes: `P` (open-market purchase, highest signal), `S` (open-market sale), `A` (grant/award), `M` (option exercise), `F` (tax withholding), `G` (gift).
- `price`, `shares`, `usd_value`, `total_shares` (post-transaction holdings), plus a direct `sec_form4_link` to the underlying filing.

**Open-market purchases are the highest-conviction signal.** An officer writing a personal check to buy stock on the open market (`P` code) has put their own capital at risk. This is rarer and more informative than any other transaction type.

**Filter out noise.** Most Form 4 flow is *not* high-signal:
- `M`/`F` pairs: option exercise plus immediate tax withholding. Mechanical.
- `A`: equity comp grant. Not a conviction event.
- Planned 10b5-1 sales: pre-scheduled trades (often to diversify or fund tax obligations). FinBrain's `transaction_type` may or may not distinguish these — err on the side of noting that `S` transactions include both discretionary and planned sales.
- `G`: gifts. Charitable or estate-related, not market-conviction.

The high-signal category is **discretionary open-market purchases (`P`) by named executives or directors**, and to a lesser extent **discretionary, non-planned open-market sales (`S`) by C-suite officers**.

**Clusters amplify signal.** One CEO buying 1,000 shares is interesting. Three C-suite officers buying within 30 days is a strong signal. Five directors buying simultaneously is a rare-and-meaningful event — almost always preceded by a perceived undervaluation or a known upcoming catalyst.

**Dollar-weighted is better than count-weighted.** One $2M purchase by the CFO means more than ten $5K purchases by directors. Always report net dollar flow alongside counts.

**Officer role context matters.** CEO/CFO/COO buys are highest signal. Director buys are medium (they may have less day-to-day visibility). Consultant or "other" designations are lower signal.

## Available MCP Tools

- **`insider_transactions_by_ticker`** — Form 4 filings with fields listed above.
- **`screener_insider_trading`** — Cross-ticker ranked list.

## Tool Chaining Workflow

1. **Pull transactions:** Call `insider_transactions_by_ticker` over the requested window (default 180 days).
2. **Categorize:** Split into open-market buys (`P`), open-market sells (`S`), option exercises (`M`), grants (`A`), tax withholdings (`F`), gifts (`G`), other.
3. **Aggregate by insider:** For the top 5 named insiders by dollar value, show role, buy-count, sell-count, net dollar.
4. **Detect clusters:** Any 30-day window with ≥3 distinct insiders making open-market buys (or separately, ≥3 distinct C-suite officers making open-market sells). Report the cluster window, participants, and combined dollar.
5. **Compute net flow:** Sum of `P` usd_value minus sum of `S` usd_value. Report as "$XM net bought" or "$YM net sold".
6. **Synthesize:** Lead with net flow, then cluster flags, then the filtered breakdown.

## Interpretation Heuristics

- **Cluster `P` buying by multiple officers:** Strong bullish signal — rarely happens without conviction.
- **Heavy `S` selling concentrated in one officer:** Often diversification, especially if that officer has recently vested large grants. Less bearish than cluster selling.
- **All activity is `M`+`F`:** No real signal — mechanical comp flows.
- **Recent 10% owner buying:** Activist or strategic investor building a stake. Cross-check 13D/13G filings for more context.

## Output Format

### Net Flow Summary

One line: "$XM bought vs $YM sold over the past <window> → net <bought|sold> $ZM."

### Top Insiders

| Insider | Role | Buys | Sells | Net $M |
|---------|------|------|-------|--------|

### Cluster Flags

Each cluster: window dates, direction (buy/sell), participants, combined dollar.

### Transaction-Type Breakdown

| Code | Description | Count | $M |
|------|-------------|-------|----|
| P | Open-market purchase | ... | ... |
| S | Open-market sale | ... | ... |
| M/F | Option exercise + tax | ... | ... |
| A | Equity comp grant | ... | ... |
| Other | ... | ... | ... |

### Read-Through

One paragraph on whether insider sentiment is bullish, bearish, or mixed, with explicit attention to whether signal is discretionary (high) or mechanical (low).
