---
description: Sentiment trend for a ticker with daily sentiment scores, news article evidence, and Reddit attention context
argument-hint: "<ticker> [lookback_days]"
---

# Sentiment Pulse

> This command uses FinBrain's news sentiment, news, and Reddit tools. See [CONNECTORS.md](../CONNECTORS.md) for the full tool reference.

Build a ticker's sentiment picture by combining aggregated daily sentiment scores, the underlying news articles, and Reddit mention counts.

See the **sentiment-pulse** skill for interpreting sentiment score ranges and reconciling news mood with Reddit attention.

## Workflow

### 1. Gather Inputs

Ask the user for:
- Ticker (required)
- Optional lookback window in days (default 90)

### 2. Pull Sentiment Time Series

Call `news_sentiment_by_ticker` with the ticker and `date_from` set to today minus the lookback. Use `limit` equal to the lookback in days.

### 3. Pull News Articles

Call `news_by_ticker` with the same parameters. Use `limit` of 200 so articles cover the window.

### 4. Pull Reddit Mentions

Call `reddit_mentions_by_ticker` with the same parameters. Use `limit` of 500 to cover multi-subreddit daily counts.

### 5. Compute the Pulse

- **Sentiment level** — mean and median score across the window; current 7-day vs 30-day comparison.
- **Sentiment trend** — linear slope (or simple first-vs-last-week delta) to detect improvement or deterioration.
- **Volume** — article count and total Reddit mentions per week.
- **Divergence** — periods where sentiment and Reddit mentions move in opposite directions (e.g., retail-driven narrative that news hasn't yet caught up to).

### 6. Surface Driver Articles

Pick up to 5 articles that likely drove sentiment moves — one from each notable sentiment inflection (sharp up or down day). Include headline, source, date, and URL.

### 7. Synthesize

Report the current sentiment reading (with 30-day context), the trend direction, mention-volume trend, any divergence, and the driver articles. Close with a one-sentence read: "Sentiment is rising / falling / stable, driven by X, with Y Reddit amplification."

## Output Format

Lead with the one-sentence read. Follow with a small stats block (mean, 7-day vs 30-day, trend slope), a weekly table of sentiment + article count + Reddit mentions, and the driver-articles list.
