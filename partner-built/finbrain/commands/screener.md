---
description: Cross-ticker screens across FinBrain's alt-data categories — Congressional trades, government contracts, sentiment, LinkedIn, app ratings, Reddit, news, insider trading
argument-hint: "<signal> [market|region] [limit]"
---

# FinBrain Cross-Ticker Screener

> This command uses FinBrain's `screener_*` tools. See [CONNECTORS.md](../CONNECTORS.md) for the full tool reference.

Run a cross-ticker screen on any FinBrain alt-data category. The user picks the signal; this command dispatches to the matching `screener_*` tool, normalizes results, and ranks them usefully.

See the **screener-workflows** skill for composing multi-signal screens and ranking tickers across alt-data categories.

## Workflow

### 1. Parse the Signal

Accept one of these signal names:

| Signal | Tool |
|--------|------|
| `house-trades` | `screener_house_trades` |
| `senate-trades` | `screener_senate_trades` |
| `government-contracts` | `screener_government_contracts` |
| `sentiment` | `screener_sentiment` (requires market or region) |
| `news` | `screener_news` |
| `linkedin` | `screener_linkedin` (requires market or region) |
| `app-ratings` | `screener_app_ratings` (requires market or region) |
| `reddit-mentions` | `screener_reddit_mentions` |
| `insider-trading` | `screener_insider_trading` |

If the user's input doesn't match, list the valid signal names and ask.

### 2. Resolve Filter

For signals that accept `market` or `region`, check the user's input. If missing but required, call `available_markets` and `available_regions` to offer a menu.

### 3. Dispatch

Call the matching `screener_*` tool with the parsed parameters. Default `limit` to 200 unless the user specified otherwise. Use `format: "json"` for in-context processing.

### 4. Rank and Normalize

Each `screener_*` tool returns a different row shape (see CONNECTORS.md). Normalize into a uniform top-N ranking:

- `house-trades`, `senate-trades` → rank by disclosure count per ticker within the result window.
- `government-contracts` → rank by total award value (use the returned `summary.total_value` when available).
- `sentiment` → rank by latest score (both most-positive and most-negative worth surfacing).
- `news` → rank by article count per ticker.
- `linkedin` → rank by employee-count growth % (latest vs first row per ticker).
- `app-ratings` → rank by latest combined iOS+Play score, and separately by score change.
- `reddit-mentions` → rank by total mentions (use the returned `summary.top_mentioned`).
- `insider-trading` → rank by net dollar flow (buys minus sells).

### 5. Present

Show the top 15 by the primary rank with the 2–3 most-relevant columns for that signal. Offer a "show bottom 15" follow-up for signals where both extremes matter (sentiment, app-ratings, insider flow).

### 6. Suggest a Follow-Up

For any ticker on the top list, suggest the matching per-ticker command: e.g., if `house-trades` surfaces NVDA at the top, propose `/finbrain:political-trades NVDA` for the deep dive.

## Output Format

Lead with the signal name, filter applied, and result count. Follow with the ranked table. End with 2–3 suggested follow-up commands.
