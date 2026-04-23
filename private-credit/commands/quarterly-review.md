---
description: "Produce covenant table, variance summary, and management questions from quarterly package"
argument-hint: "<attached quarterly financials>"
---

# /private-credit:quarterly-review

Produces a covenant compliance table, variance summary with MD&A narrative, and management call questions from a borrower's quarterly financial package.

---

## Trigger

User invokes `/private-credit:quarterly-review` with a borrower's quarterly financial package (Excel and/or PDF) and compliance certificate attached or referenced. The existing credit model for the borrower should also be available.

---

## Required Inputs

| Input | Required? | Notes |
|---|---|---|
| Quarterly financial package (Excel or PDF) | **Yes** | P&L, balance sheet, cash flow statement for the current quarter |
| Compliance certificate | **Yes** | May be inline with financials or a separate document (PDF) |
| Existing credit model for this borrower | **Yes** | The model being updated with the new quarter's data |
| Prior quarter's review (if available) | Recommended | Enables trend tracking and narrative continuity |
| Annual budget (if available) | Recommended | Enables vs. budget variance analysis |

---

## Output 1: Updated Financial Summary

### Variance Analysis Framework

Apply comparisons in this order:

**1. Quarterly Performance — Year-over-Year**
Compare the current quarter to the same quarter in the prior year. Never do quarter-over-quarter unless it is specifically relevant to the deal (e.g., a seasonal business where sequential comparison is meaningful).

**2. Quarterly Performance — vs. Budget**
Compare the current quarter to the budgeted quarter (if budget is available).

**3. Year-to-Date — vs. Prior Year and vs. Budget**
YTD actual vs. prior year YTD. YTD actual vs. budgeted YTD.

**4. LTM — vs. Annual Budget or Prior LTM**
Rolling LTM vs. the annual budget. Rolling LTM vs. the prior period's LTM.

### Variance Callout Thresholds

| Line Item | Callout Threshold | Notes |
|---|---|---|
| **Revenue** | Always call out | Revenue is the most important line item. Note the variance regardless of magnitude, even if the dollar change is <5%. |
| **Gross profit (dollars)** | ≥ 5% dollar change | Below 5% dollar change YoY, not worth calling out unless part of a multi-quarter trend. |
| **Gross margin (percentage)** | Any notable movement | Margin percentage point changes are always significant. A 500bps swing (e.g., 45% → 40%) is massive and must be highlighted. Do not confuse the 5% dollar threshold with margin points — a 2-3 percentage point margin move is material even if the dollar change is small. |
| **EBITDA (dollars)** | ≥ 5% dollar change | Same threshold as gross profit on the dollar amount. |
| **EBITDA margin (percentage)** | Any notable movement | Same as gross margin — percentage point swings are always significant. A 200-300bps compression or expansion warrants a callout and explanation. |
| **Operating expense categories** | ≥ 5% dollar change | Call out which category is driving the variance (SG&A, R&D, sales & marketing, G&A). |
| **Working capital items** | ≥ 5% dollar change or notable trend | AR days, inventory days, AP days — call out if trending in a direction over multiple quarters. |
| **Capex** | ≥ 10% dollar change | Higher threshold — capex is lumpier by nature. |
| **Free cash flow** | Always call out | FCF is a critical credit metric. Note the variance regardless of magnitude. |

### MD&A Narrative

Write a narrative summary of the quarter's performance. This is not a table — it is a written analysis that explains the numbers.

Structure:
1. **Revenue:** What happened this quarter? YoY comparison, vs. budget. What drove the result? Organic growth, acquisition contribution, new customer wins, customer losses, pricing changes.
2. **Margins:** Gross margin and EBITDA margin trends. If margins moved, explain why — COGS changes, OpEx changes, which categories.
3. **Cash flow and liquidity:** FCF this quarter. Working capital dynamics. Cash balance and revolver availability. Any notable cash events (distributions, capex spikes, acquisition payments).
4. **Credit metrics:** Leverage trend. Coverage ratio trend. Any movement toward or away from covenant thresholds.
5. **Notable items:** Acquisitions, restatements, new line items, management commentary themes, anything unusual.

**For items that are unexpected or material (>20-30% variance), both weave into the narrative AND flag separately** so the analyst does not miss them.

---

## Output 2: Covenant Compliance Table

### Table Structure

Columns progress left to right by quarter: Q1, Q2, Q3, Q4, etc.

Rows for each covenant:

```
[Covenant Name]
  Covenant Level (threshold)     [step-down schedule values per quarter]
  Actual Level                   [calculated from financials / cert]
  Cushion (%)                    [headroom percentage]
```

Repeat for each financial maintenance covenant (typically net leverage, FCCR, and any others per the credit agreement).

### What to Include

- **Current quarter actuals** from the compliance certificate (source of truth)
- **Prior quarters** (4-8 quarters of history for trend visibility)
- **Covenant thresholds** including any step-downs that have taken effect
- **Upcoming step-downs** — show the threshold for the next 2-4 quarters even though actuals are blank. The reader should see tightening ahead.
- **Headroom percentage** calculated as: (Actual - Threshold) / Threshold for "max" covenants (leverage); (Actual - Threshold) / Threshold for "min" covenants (coverage). Express as a positive percentage when in compliance.

### Headroom Flags

Apply the headroom framework from the covenant-compliance skill:
- ≥ 20%: No flag
- 10-20%: Note "elevated attention"
- < 10%: Flag "tight — flag to IC"

Note the trajectory: improving, stable, or deteriorating.

### Equity Cure Rights

Add a footnote: total cure rights under the agreement, number used, number remaining.

---

## Output 3: Management Call Questions

### Target Length

Less than one page. More than 1-2 questions, fewer than 20. Typically 6-12 questions depending on the quarter.

### Categorization

Group questions by category. Order categories by priority:

1. **Financial** — questions driven by the numbers (variances, trends, discrepancies)
2. **Strategic** — questions about business direction, market positioning, growth initiatives
3. **Operational** — questions about execution, cost management, integration (for acquisitions)
4. **Acquisition** — questions about tuck-in pipeline, integration progress, synergy realization (for roll-ups)

Within each category, rank by importance — most critical question first.

### Question Quality Standards

Every question must demonstrate that the analyst understands the business and the financials. Apply second-order thinking:

**Bad:** "EBITDA margin declined this quarter."
This is an observation, not a question. It does not demonstrate analytical depth.

**Good:** "EBITDA margin compressed 250bps YoY. Gross margin was roughly flat, so the compression is in OpEx. SG&A grew 15% vs. 3% revenue growth — is this the sales team investment discussed in Q2? What is the expected timeline for revenue contribution from the new hires?"
This traces the margin compression to its source, links to prior management commentary, and asks a forward-looking question.

### Prior Quarter Context

Every question list must be informed by the prior quarter's:
- Financial performance and trends
- MD&A and management commentary
- Questions asked and answers received
- Commitments or guidance management provided

If management guided to margin recovery by Q4 and margins are still compressing, ask specifically what changed. If a new initiative was announced in Q2, ask for a status update.

Track the management team's narrative for consistency. If the story changes quarter over quarter without explanation, that is a question.

---

## "Done" Checklist

The quarterly review is complete when:

- [ ] Financial data extracted from the quarterly package and entered into the credit model
- [ ] All model analysis sections updated for the latest quarter
- [ ] Variance analysis complete (YoY, vs. budget, YTD, LTM)
- [ ] MD&A narrative written covering revenue, margins, cash flow, credit metrics, notable items
- [ ] Covenant compliance table updated with current quarter actuals and headroom
- [ ] Material unexpected items flagged both in narrative and as standalone callouts
- [ ] Management call questions compiled, categorized, and ranked
- [ ] Questions reference prior quarter context and management commitments
- [ ] Package is ready for IC or portfolio review meeting
