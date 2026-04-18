---
name: screener-workflows
description: Run cross-ticker screens across FinBrain's alt-data categories (Congressional trades, federal contracts, sentiment, LinkedIn, app ratings, Reddit, news, insider trading) and compose multi-signal rankings. Use when asked to screen the market for alt-data signals, find tickers with the most political trading, rank by sentiment, surface top Reddit-mentioned stocks, identify insider-buying leaders, or build a cross-signal watchlist.
---

# FinBrain Cross-Ticker Screener Workflows

You are an expert on composing cross-ticker screens using alternative-data signals. Use FinBrain's `screener_*` family to surface tickers ranked by any single alt-data category, and combine screens for multi-signal watchlists.

## Core Principles

**Each screener returns a different row shape.** CONNECTORS.md documents them; normalize to a uniform top-N ranking per signal before presenting.

**Market vs region filters are signal-dependent.** Some screeners (`screener_sentiment`, `screener_linkedin`, `screener_app_ratings`) require a `market` or `region` filter. Others (`screener_house_trades`, `screener_senate_trades`, `screener_insider_trading`, `screener_government_contracts`) return latest disclosures across all tracked tickers and don't accept those filters. When the user asks for a filter the tool doesn't accept, note the limitation and offer to post-filter the results.

**Discovery first.** If the user hasn't named a market or region, call `available_markets` and/or `available_regions` to offer a menu rather than guessing.

**Rankings beat raw lists.** A screener result is only useful if you turn it into a ranked table. Know the right ranking axis per signal (see below).

**Multi-signal screens are the killer workflow.** The true power of this plugin is composing screens: e.g., "Top 20 tickers with cluster senator buying AND rising LinkedIn headcount AND no negative sentiment inflection." Build these by intersecting two or three single-signal top-50s.

## Available MCP Tools

See [CONNECTORS.md](../../CONNECTORS.md) for the full list. The skill operates over the `screener_*` family:

- `screener_house_trades` — rank by disclosure count per ticker.
- `screener_senate_trades` — rank by disclosure count per ticker.
- `screener_government_contracts` — rank by total award value (use returned `summary.total_value`).
- `screener_sentiment` — rank by latest score (both extremes informative).
- `screener_news` — rank by article count per ticker.
- `screener_linkedin` — rank by employee-count growth %.
- `screener_app_ratings` — rank by latest iOS+Play combined score and separately by 4-week change.
- `screener_reddit_mentions` — rank by total mentions (use returned `summary.top_mentioned`).
- `screener_insider_trading` — rank by net dollar flow (buys minus sells).

Plus discovery:
- `available_markets` / `available_regions` for valid filter values.

## Tool Chaining Workflow (Single-Signal)

1. **Parse signal.** Confirm the user's requested category maps to one of the `screener_*` tools.
2. **Resolve filter.** If the tool accepts `market`/`region` and the user didn't specify, call `available_markets` / `available_regions` and offer a menu.
3. **Dispatch.** Call the screener with the filter, `limit` of 200, `format: "json"`.
4. **Rank.** Apply the per-signal ranking axis listed above.
5. **Present top 15.** For signals where both extremes matter (sentiment, insider flow, app-rating change), offer the bottom 15 as a follow-up.
6. **Suggest follow-ups.** For interesting tickers, suggest the matching per-ticker command (e.g., `/finbrain:political-trades NVDA`).

## Tool Chaining Workflow (Multi-Signal)

1. Clarify the signals and the join logic ("AND" vs "OR") with the user.
2. Call each screener at `limit` of 500 to ensure the top-N overlap is meaningful.
3. Intersect the top-100 of each result set by ticker.
4. Score each intersection ticker by summing normalized ranks (lower sum = better).
5. Present the combined top 15 with each contributing signal's rank and metric value.

## Interpretation Heuristics

- **Top-1 tickers in government-contracts screen are usually defense/aerospace** — low surprise, but confirms the data is working. Filter them out if the user wants non-obvious names.
- **High Reddit mentions with negative sentiment:** Often meme/contrarian setups. Worth a deep dive with `/finbrain:sentiment-pulse` to confirm the narrative.
- **High insider net buy + rising LinkedIn headcount:** Coherent bullish alt-data profile.
- **Cluster senator buying + rising lobbying spend on a shared issue code:** Rare signal that rewards investigation.

## Output Format

### Signal & Filter

Line 1: signal name, filter applied, result count.

### Ranked Table

Top 15 with 2–3 columns most relevant to the signal.

### Follow-Up Suggestions

2–3 per-ticker command suggestions for the most interesting names on the top list.
