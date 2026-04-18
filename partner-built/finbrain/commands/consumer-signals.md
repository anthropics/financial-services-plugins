---
description: Consumer and employee signals for a ticker — LinkedIn hiring trend, mobile app-store ratings, and Reddit mention volume
argument-hint: "<ticker> [lookback_weeks]"
---

# Consumer Signals

> This command uses FinBrain's LinkedIn, app-ratings, and Reddit tools. See [CONNECTORS.md](../CONNECTORS.md) for the full tool reference.

Assess consumer and employee momentum for a ticker by combining LinkedIn employee/follower trends, iOS/Google Play app performance, and Reddit mention volume.

See the **consumer-signals** skill for interpreting hiring slope, app-store momentum, and when each signal is most relevant.

## Workflow

### 1. Gather Inputs

Ask the user for:
- Ticker (required)
- Optional lookback window in weeks (default 52)

### 2. Pull LinkedIn Metrics

Call `linkedin_metrics_by_ticker` with the ticker and `date_from` set to today minus (weeks × 7). Use `limit` of 200.

### 3. Pull App Ratings

Call `app_ratings_by_ticker` with the same ticker and lookback. If the company is not a consumer-app issuer (e.g., pure B2B industrials), the result may be empty — skip this section gracefully.

### 4. Pull Reddit Mentions

Call `reddit_mentions_by_ticker` with the same parameters. Use `limit` of 500.

### 5. Compute Signals

- **Hiring trend** — employee count slope (% change first-to-last period); positive slope = growth, negative = headcount decline. Also report follower growth.
- **App momentum** — latest iOS and Play scores, change over the window, and install-count trend if available.
- **Attention** — Reddit mentions: current week, 4-week average, and the top subreddits by total mentions over the window.

### 6. Flag Inflections

- Sharp employee-count drops (>5% in a month) often precede layoffs disclosures.
- Sudden app-rating decline (>0.3 point drop over 4 weeks) often signals a bad release or user dissatisfaction.
- Reddit mention spikes >3× the 4-week average warrant checking the underlying subreddit threads for narrative context.

### 7. Synthesize

Present three mini-sections (Hiring, App, Reddit) each with one line of current state and one line of trend. Close with a one-sentence read-through linking the signals: e.g., "Hiring has decelerated while app scores hold — consumer product is steady but growth is cooling."

## Output Format

Three labeled sections with small inline stats blocks and mini-tables as needed. Lead with the one-sentence read if clear signal is present; otherwise state that signals are mixed.
