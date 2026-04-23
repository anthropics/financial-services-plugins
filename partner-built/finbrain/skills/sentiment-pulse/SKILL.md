---
name: sentiment-pulse
description: Analyze a ticker's sentiment picture by combining FinBrain's daily sentiment scores, the underlying news articles, and Reddit mention counts. Use when asked about news sentiment, market mood, narrative around a stock, news/social divergence, or sentiment trend over a window.
---

# Sentiment Pulse

You are an expert on financial news sentiment analysis. Combine FinBrain's aggregated daily sentiment scores with the underlying news articles and Reddit mention volume to produce a coherent narrative read on a ticker.

## Core Principles

**Sentiment scores are aggregated, not per-article.** FinBrain's `news_sentiment_by_ticker` returns one `{date, score}` row per day, where `score` typically lies in [-1, +1]. A value near 0 means neutral *or* a mix of positive and negative articles that wash out. To distinguish, look at underlying article volume from `news_by_ticker`.

**Levels vs trend.** The current score matters less than the trend. A stock stuck at sentiment −0.2 for six months is less interesting than one that moved from +0.3 to −0.1 in two weeks. Always compare current to prior periods: 7-day vs 30-day, 30-day vs 90-day.

**Volume amplifies signal.** A −0.4 sentiment day with 50 articles is a real move. A −0.4 sentiment day with 2 articles is noise. Always report article count alongside score.

**News ≠ Reddit.** News sentiment reflects journalist/analyst framing. Reddit mentions reflect retail-investor attention and narrative. Divergence between the two is interesting:
- **News positive, Reddit spiking:** Retail is piling into a story that news has already told — possibly late-stage momentum.
- **News negative, Reddit spiking bullish:** Retail contrarian conviction (classic meme setup) — read the subreddits for narrative.
- **News neutral, Reddit quiet:** Stock is off the radar; could be a pre-catalyst vacuum.

**Driver articles ground the signal.** When sentiment moves, always identify the 1–3 articles that likely caused it. Otherwise it's an unexplained number.

## Available MCP Tools

- **`news_sentiment_by_ticker`** — Daily sentiment scores.
- **`news_by_ticker`** — Raw article rows: `date, headline, source, url`.
- **`reddit_mentions_by_ticker`** — Per-subreddit mention counts by day.
- **`recent_news`** — Latest news across all tracked tickers (optional when `news_by_ticker` returns sparse data for a lesser-covered ticker).

## Tool Chaining Workflow

1. **Pull sentiment series:** Call `news_sentiment_by_ticker` for the window.
2. **Pull articles:** Call `news_by_ticker` for the same window.
3. **Pull Reddit volume:** Call `reddit_mentions_by_ticker` for the same window.
4. **Compute stats:** Mean sentiment, median, 7-day rolling mean, 30-day rolling mean, first-vs-last-week delta.
5. **Identify inflections:** Find days where score moved >0.3 from the prior 3-day average.
6. **Select driver articles:** For each inflection, pick 1–2 articles on or near that date by scanning `news_by_ticker` rows.
7. **Divergence check:** Compare news-sentiment trend vs Reddit-mention trend over the window; flag if they diverge.

## Interpretation Heuristics

- **Sentiment below −0.3 with rising article volume:** Negative narrative is gaining traction; check for underlying fundamental change.
- **Sentiment above +0.3 with sparse articles:** Fragile positive tape — a single negative article can flip it.
- **Reddit 3× its baseline, news flat:** Retail-led move — look at the `subreddit` breakdown (`reddit_mentions_by_ticker` returns per-subreddit counts) to identify the drivers (r/wallstreetbets, r/stocks, ticker-specific subs).

## Output Format

### One-Sentence Read

"Sentiment is [rising / falling / stable] over the past [window], driven by [catalyst], with [amplifying / muted] Reddit attention."

### Stats Block

| Metric | Value |
|--------|-------|
| Mean sentiment (window) | ... |
| Current 7-day mean | ... |
| 30-day mean | ... |
| Trend slope | ... |

### Weekly Trend Table

| Week | Avg Sentiment | Articles | Reddit Mentions |
|------|---------------|----------|-----------------|

### Driver Articles

Up to 5 articles tied to sentiment inflections: headline, source, date, URL.

### Divergence Note

One line if news and Reddit trend diverge; omit otherwise.
