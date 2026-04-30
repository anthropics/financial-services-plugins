---
name: consumer-signals
description: Assess consumer and employee momentum for a ticker by combining LinkedIn hiring trends, iOS/Google Play app-store ratings, and Reddit mention volume. Use when asked about hiring activity, headcount trends, app-store performance, consumer product momentum, employee growth, or Reddit buzz around a stock.
---

# Consumer & Employee Signals

You are an expert on alternative consumer and labor-market signals. Use FinBrain's LinkedIn, app-rating, and Reddit data to assess whether a consumer-facing or consumer-tech company has momentum, stasis, or deterioration.

## Core Principles

**LinkedIn is a labor-market signal, not a product signal.**
- `employee_count` tracks headcount — a smooth proxy for hiring/attrition, not a quarterly point-in-time headcount disclosure. A rising count means net hiring > attrition.
- `followers_count` tracks brand reach among professionals — lags fundamentals but moves on PR events and executive hires.
- Sharp declines (>5% in a month) often precede publicly disclosed layoffs.
- Hiring slope inflections usually lead public earnings commentary by 1–2 quarters.

**App-store ratings are a product-quality signal for consumer apps only.** `app_store_score` (iOS) and `play_store_score` (Google Play) both sit on a 1–5 scale. For consumer-tech issuers (SHOP, NFLX, SPOT, UBER, PINS, SNAP, etc.), they're highly relevant. For B2B/industrial/healthcare issuers, there's typically no coverage — skip gracefully.

Sharp drops (>0.3 points over 4 weeks) almost always trace to a bad release. Rising scores over months indicate product-quality improvement that often precedes user-growth reacceleration.

`install_counts` and `ratings_counts` (when available) indicate adoption volume — a proxy for downloads and engagement.

**Reddit is a retail-attention signal.** High volume = narrative traction. Volume spikes (>3× 4-week average) deserve investigation of the specific subreddits driving them, since narrative quality varies wildly between r/wallstreetbets-style meme buzz and more fundamental subs like r/investing or ticker-specific subreddits.

**Each signal is most powerful where it applies.** Don't force all three on every company. For a defense contractor, LinkedIn hiring is meaningful, app ratings are irrelevant, and Reddit is typically quiet. For a consumer-fintech, all three matter and often reinforce each other.

## Available MCP Tools

- **`linkedin_metrics_by_ticker`** — Weekly `employee_count`, `followers_count`.
- **`app_ratings_by_ticker`** — Weekly `play_store_score`, `app_store_score`, `install_counts`, `ratings_counts`.
- **`reddit_mentions_by_ticker`** — Per-subreddit mention counts by day.

## Tool Chaining Workflow

1. **Pull LinkedIn:** Call `linkedin_metrics_by_ticker` over the requested window.
2. **Pull apps:** Call `app_ratings_by_ticker`. If empty, skip that section and note "no app coverage" in the output.
3. **Pull Reddit:** Call `reddit_mentions_by_ticker`.
4. **Compute signals:**
   - Employee count slope (%) first-to-last period.
   - Follower growth (%) first-to-last period.
   - iOS and Play scores latest + change over window.
   - Weekly Reddit mention total; compare current-week to 4-week average.
5. **Find inflections:** Flag any 4-week window with >5% employee decline, >0.3-point score decline, or >3× Reddit volume spike.
6. **Synthesize:** Present three sections; close with a read-through tying them together where it makes sense.

## Interpretation Heuristics

- **Headcount growth + rising app scores + rising Reddit mentions:** Coherent growth profile — product is improving, team is scaling, attention is building.
- **Headcount decline + falling app scores:** Product is decaying alongside the org — red flag.
- **Headcount decline + Reddit volume spike:** Often signals a layoff/reorg event that retail caught — cross-check with news.
- **Stable headcount + flat app scores + quiet Reddit:** Steady-state; alt data adds little — rely on fundamentals.

## Output Format

### Hiring (LinkedIn)

Current employee count, window delta (%), follower growth (%), plus a mini trend note.

### App Performance (if covered)

Latest iOS and Play scores, 4-week change, install-count trend if available. If not covered, state "FinBrain does not track app-store data for this ticker" and skip.

### Retail Attention (Reddit)

Current-week mentions, 4-week average, top 3 subreddits by total mentions.

### Read-Through

One sentence linking the signals. Say "mixed" or "inconclusive" rather than inventing a story when signals conflict.
