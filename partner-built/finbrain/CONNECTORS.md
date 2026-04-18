# Connectors

This plugin connects to the **FinBrain MCP Server**, which exposes FinBrain's alternative datasets — Congressional trading, corporate lobbying, federal contract awards, news sentiment, LinkedIn and app-store signals, Reddit mentions, insider trades, and more.

Unlike most partners in this marketplace, the FinBrain MCP runs **locally via stdio** (the `finbrain-mcp` PyPI package) and requires a one-time `pip install` plus a `FINBRAIN_API_KEY` environment variable. See the top-level [README](README.md) for installation steps.

## How Commands Reference Tools

Commands in this plugin reference MCP tools by their exact tool name (e.g., `house_trades_by_ticker`, `corporate_lobbying_by_ticker`). The tools below are organized by tier — commands and skills in this plugin focus on Tier 1–3.

## Tool Categories

| Category | Tier | Tools |
|----------|------|-------|
| Government & Regulatory | 1 | `house_trades_by_ticker`, `senate_trades_by_ticker`, `corporate_lobbying_by_ticker`, `government_contracts_by_ticker`, `screener_house_trades`, `screener_senate_trades`, `screener_government_contracts` |
| Social & Consumer Intelligence | 2 | `news_by_ticker`, `news_sentiment_by_ticker`, `recent_news`, `screener_news`, `screener_sentiment`, `linkedin_metrics_by_ticker`, `screener_linkedin`, `app_ratings_by_ticker`, `screener_app_ratings`, `reddit_mentions_by_ticker`, `screener_reddit_mentions` |
| Insider Trading | 3 | `insider_transactions_by_ticker`, `screener_insider_trading` |
| Availability / Health | utility | `health`, `available_markets`, `available_tickers`, `available_regions` |
| Also available (not covered by commands/skills) | — | `predictions_by_market`, `predictions_by_ticker`, `options_put_call`, `screener_put_call_ratio`, `analyst_ratings_by_ticker`, `recent_analyst_ratings`, `screener_analyst_ratings` |

## Complete Tool Reference

All per-ticker tools accept `ticker` (required), optional `date_from` / `date_to` (ISO `YYYY-MM-DD`), a `limit` cap, and a `format` flag (`json` or `csv`). All screener tools accept an optional `market` (e.g., "S&P 500") or `region` filter, plus `limit` and `format`.

### Government & Regulatory (Tier 1 — flagship)

- **`house_trades_by_ticker`** — US House of Representatives stock transactions. Returns `{date, representative, trade_type, amount_min, amount_max, amount_exact, amount_raw}` per disclosure. Use for politician-level breakdown of House trading activity in a ticker.
- **`senate_trades_by_ticker`** — US Senate stock transactions. Same shape as House (with `senator` field). Use for Senate-side disclosures; often lags disclosure by the statutory 45-day reporting window.
- **`corporate_lobbying_by_ticker`** — Quarterly lobbying filings. Returns `{date, filing_uuid, quarter, client_name, registrant_name, income, expenses, issue_codes[], government_entities[]}`. Use to size a company's K-Street footprint, identify registrants (lobbying firms) and targeted agencies, and track issue-code themes.
- **`government_contracts_by_ticker`** — Federal contract awards from USAspending.gov. Returns `{award_id, award_amount, award_type, awarding_agency, awarding_sub_agency, recipient_name, start_date, end_date, description, naics_code, naics_description, contract_award_type}`. Use to measure federal revenue exposure, agency concentration, and NAICS classification.
- **`screener_house_trades`** — Cross-ticker House trades ranked by recency. Returns `{ticker, name, date, politician, trade_type, amount}` rows. No `market`/`region` filter — returns latest disclosures across all tracked tickers.
- **`screener_senate_trades`** — Cross-ticker Senate trades. Same shape as `screener_house_trades`.
- **`screener_government_contracts`** — Federal contract awards across all tickers, with an additional `summary` block (`total_contracts`, `total_tickers`, `total_value`). Use to rank sector/ticker exposure to federal spending.

### Social & Consumer Intelligence (Tier 2)

- **`news_by_ticker`** — Recent news articles for a ticker. Returns `{date, headline, source, url}` per article. Use for raw headline flow.
- **`news_sentiment_by_ticker`** — Aggregated daily sentiment scores for a ticker. Returns `{date, score}` per day (score typically in [-1, 1]). Use to build sentiment time series and detect regime changes.
- **`recent_news`** — Latest news across all tracked stocks. Accepts optional `market` / `region` filter. Returns `{ticker, name, date, headline, source, url}` rows.
- **`screener_news`** — Cross-ticker news feed (same shape as `recent_news`). Use when scanning headline flow at the market or region level.
- **`screener_sentiment`** — Cross-ticker sentiment snapshot (latest score per ticker). Requires `market` or `region`. Returns `{ticker, name, date, score}`.
- **`linkedin_metrics_by_ticker`** — Employee count and follower trends from LinkedIn. Returns `{date, employee_count, followers_count}`. Use for hiring-trend signals and audience growth.
- **`screener_linkedin`** — Cross-ticker LinkedIn data. Requires `market` or `region`. Returns `{ticker, name, date, employee_count, followers_count, job_count}`.
- **`app_ratings_by_ticker`** — Mobile app performance across iOS App Store and Google Play Store. Returns `{date, play_store_score, app_store_score, install_counts, ratings_counts}` per week. Use for consumer-product momentum (relevant to consumer tech, fintech, games).
- **`screener_app_ratings`** — Cross-ticker app ratings. Requires `market` or `region`. Returns `{ticker, name, date, app_store_score, play_store_score}`.
- **`reddit_mentions_by_ticker`** — Ticker mention counts across subreddits. Returns `{date, subreddit, mentions}` rows. Use for retail-investor attention and narrative tracking.
- **`screener_reddit_mentions`** — Cross-ticker Reddit mentions with a `summary` block (`top_mentioned`, `subreddit_names`). Use to rank trending tickers by Reddit attention.

### Insider Trading (Tier 3)

- **`insider_transactions_by_ticker`** — SEC Form 4 insider filings. Returns `{date, insider_name, relationship, transaction_type, price, shares, usd_value, total_shares, sec_form4_date, sec_form4_link}`. Use to analyze officer/director buying and selling, cluster activity, and dollar-weighted flow.
- **`screener_insider_trading`** — Cross-ticker insider trades. Returns `{ticker, name, date, insider_name, relationship, transaction_type, shares, total_value}`. Use to rank tickers by recent insider conviction.

### Availability / Health (utility)

- **`health`** — Server health and version info. Returns `{ok, error, mcp_version, sdk}`. Call first if tool calls unexpectedly fail.
- **`available_markets`** — Lists every market FinBrain tracks (e.g., "S&P 500", "Russell 2000", "DAX 40"). Use to discover valid `market` filter values.
- **`available_tickers`** — Lists tracked tickers for a given `dataset` (`"daily"` or `"monthly"`). Use to confirm a ticker is in coverage before batching calls.
- **`available_regions`** — Lists regions grouped by market. Use to discover valid `region` filter values.

### Also available (not covered by commands/skills)

These tools are exposed by the MCP server but are intentionally **not** wired into this plugin's commands or skills — they overlap with fundamentals/analytics providers already present in the Financial Services marketplace. They can still be invoked directly if needed.

- **`predictions_by_market`** — Market-wide AI price predictions (short/mid/long horizon) with confidence intervals.
- **`predictions_by_ticker`** — Single-ticker price forecast time series (10-day daily or 12-month monthly).
- **`options_put_call`** — Per-ticker put/call ratio and volume time series.
- **`screener_put_call_ratio`** — Cross-ticker put/call ratio snapshot.
- **`analyst_ratings_by_ticker`** — Per-ticker Wall Street analyst ratings and price targets.
- **`recent_analyst_ratings`** — Latest analyst actions across all tracked stocks.
- **`screener_analyst_ratings`** — Cross-ticker analyst-rating snapshot.
