---
description: "Base / Downside / Stress case comparison with covenant breach flagging"
argument-hint: "<attached model or financial data>"
---

# /private-credit:scenario-analysis

Produces a Base / Downside / Stress case comparison table showing key credit metrics across cases, flags the quarter where covenants breach, and calculates liquidity runway per case.

---

## Trigger

User invokes `/private-credit:scenario-analysis` with a financial model or sufficient financial data to project forward. The user should specify the business type and key risk factors so the downside and stress cases can be tailored to the specific deal.

---

## Required Inputs

| Input | Required? | Notes |
|---|---|---|
| Financial model or current financials | **Yes** | Need a starting point for projections (revenue, EBITDA, debt, cash) |
| Debt terms (quantum, pricing, amortization) | **Yes** | Required for interest expense and debt service calculations |
| Covenant schedule (thresholds, step-downs) | **Yes** | Required to flag breach quarters |
| Business description or risk profile | **Yes** | Downside/stress assumptions must be tailored to the specific business |
| Sponsor/vendor base case (if available) | Recommended | Starting point for the lender base case |

---

## Case Construction

### Base Case

If the sponsor/vendor case is available, use it as the starting point. The sponsor case is typically sandbagged — it is a conservative version of their realistic expectations, used as the basis for covenant setting.

Options:
- **Use sponsor case as-is** if it appears reasonable
- **Build a lender case** by adjusting around the edges: a few percentage points less aggressive on revenue growth, slightly less FCF generation, marginally higher operating expenses. Not a fundamentally different view — a more conservative tilt.

### Downside Case

**Assumptions must be derived from the specific risk profile of the business.** Do not apply generic percentage haircuts. Identify the most relevant downside scenario for this business:

| Business Profile | Downside Scenario |
|---|---|
| **Cyclical** (manufacturing, construction, industrials) | Model a full down-cycle. Anchor revenue decline to how this sector performed in 2008-2009. |
| **Customer concentrated** (top customer >15-20% of revenue) | Model loss of the top customer. Revenue impact + margin impact + working capital impact. |
| **Supplier dependent** (favorable contract, single-source) | Model loss of the supply relationship. Margins compress to industry standard. |
| **Acquisition dependent** (roll-up strategy) | Model a pause in acquisitions. Organic growth only. No PF EBITDA additions. Integration costs continue. |
| **Discretionary / consumer-facing** | Model a demand pullback anchored to 2008-2009 recession impact on comparable businesses. |
| **No specific risk driver** | Model a general economic recession. Revenue decline of 10-20% over 4-6 quarters with margin compression. Anchor to historical sector performance. |

### Stress Case

More severe than the downside. Combines multiple adverse factors:
- Revenue decline (larger than downside)
- Margin compression (on top of revenue decline)
- Working capital deterioration (cash consumption increases)
- Test: does the business survive? What breaks first?

### Recovery Assumptions

Recovery is not always V-shaped:
- **Cyclical downturn:** Typically V-shape or U-shape. Revenue declines then recovers over 2-4 quarters. Model the recovery to pre-downturn levels or close to it.
- **Structural impairment** (technology disruption, permanent market shift): The business may not recover to prior levels. Model a "new normal" at a lower base.
- **Customer loss:** Partial or full replacement over 4-8 quarters depending on the business's ability to acquire new customers.

Show both the trough and the recovery trajectory in the output.

---

## Output: Comparison Table

### Metrics to Show (Across All Three Cases)

Only include metrics relevant to the specific business. Do not show gross profit for a business where it is not a meaningful driver.

**Standard metrics (always include):**

| Metric | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| **Revenue** | | | |
| Base | | | |
| Downside | | | |
| Stress | | | |
| **EBITDA** | | | |
| Base | | | |
| Downside | | | |
| Stress | | | |
| **Total Debt** | | | |
| Base | | | |
| Downside | | | |
| Stress | | | |
| **Net Leverage** | | | |
| Base | | | |
| Downside | | | |
| Stress | | | |
| Covenant Threshold | | | |
| **Free Cash Flow** | | | |
| Base | | | |
| Downside | | | |
| Stress | | | |
| **Liquidity** | | | |
| Base | | | |
| Downside | | | |
| Stress | | | |

If quarterly granularity is available and relevant (especially for identifying the specific quarter of covenant breach), show quarterly rather than annual.

**Deal-specific additions** (include when relevant):
- EBITDA margin (if margin compression is a key feature of the downside)
- FCCR (if fixed charge coverage is a tested covenant)
- LTV (if enterprise value is available and relevant)

### Covenant Breach Flagging

For each case, identify:
- **Does a covenant breach occur?** Yes or No
- **Which covenant breaches first?** (typically net leverage)
- **In which quarter?** Specific quarter (e.g., "Q3 2027")
- **Leverage at breach:** The actual leverage level when the covenant trips

Present as a leverage bridge showing the quarterly progression from current to breach:

```
Downside — Leverage Bridge:
Q4 2025: 4.02x (current) → Q1 2026: 4.25x → Q2 2026: 4.48x → Q3 2026: 4.62x [BREACH at 4.50x threshold]
```

Do not include cure analysis in the breach flagging. Keep it to the factual leverage progression.

### Liquidity Runway

Calculate liquidity for each case at each period:

```
Beginning Cash Balance
  +/- Free Cash Flow Generated
  +/- Mandatory Amortization (if not already in FCF)
  +/- Revolver Draws or Repayments
  +/- Additional Capital Sources (new debt, equity injection)
  - Upcoming Maturities (if within the projection period)
= Ending Liquidity (Cash + Available Revolver Capacity)
```

Present liquidity at each period. Flag the quarter where liquidity reaches its trough in each case and state the dollar amount.

For the stress case specifically, state: "Liquidity runway: [X] months / quarters from trough before liquidity is exhausted" — if the stress case leads to a liquidity crisis.

---

## Narrative Summary

Close with a brief (3-5 sentence) comparison across cases:

- **Base case:** Summarize the deleveraging path and FCF trajectory. "Base case projects deleveraging from X.Xx to Y.Yx by Year 3 with $ZM cumulative FCF."
- **Downside case:** Summarize what happens. "Downside case models [scenario]. Leverage peaks at X.Xx in [quarter], [breaching / approaching] the covenant threshold. The company [generates / consumes] $XM of FCF at trough. Recovery to base case levels by [quarter]."
- **Stress case:** Summarize the extreme outcome. "Stress case combines [factors]. Covenant breach occurs in [quarter] at X.Xx leverage. Liquidity reaches $XM at trough in [quarter], representing [X] months of runway."

State the assumptions for each case clearly. The value is in well-thought-out, business-specific inputs — not generic percentage haircuts applied to a template.
