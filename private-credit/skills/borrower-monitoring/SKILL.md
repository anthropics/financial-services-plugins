# Borrower Monitoring

This skill fires automatically when performing quarterly portfolio monitoring, updating borrower tracking, evaluating credit trajectory, managing watchlists, or preparing for management calls.

---

## Quarterly Monitoring Workflow — Step by Step

This is the complete workflow from the moment a borrower's quarterly package arrives to the moment the review is ready for IC or portfolio review.

### Step 1: Receive and Review the Package

Open the borrower's quarterly financial package. Read through the first time quickly to get a sense of what is being reported:
- What financial statements are included?
- Is there MD&A or management commentary?
- Is the compliance certificate included or separate?
- What data is available vs. what is missing?

### Step 2: Extract and Update the Quarterly Model

Working top-down through the P&L, balance sheet, and cash flow statement (per the quarterly-package-extraction skill):
- Enter the latest quarter's financial data into your quarterly Excel model
- Update all analysis sections within the model based on the new quarterly information
- Follow the existing template mapping from prior quarters

### Step 3: Note Questions During Processing

As you enter data and update the model, questions will naturally arise:
- Discrepancies between the financials and the compliance cert
- Unexpected trends or movements you cannot explain
- New line items or reclassifications
- Deviations from budget or from the prior quarter

Compile these into a quarterly questions list as you work. Do not stop processing to investigate each one — note it and keep going. The questions list will be addressed in Step 6.

### Step 4: Populate the Quarterly Presentation

After the model is updated, build the full quarterly review package (typically PowerPoint):
- MD&A narrative discussing the quarter's financial performance
- Revenue and margin discussion with trend context
- Cash flow and liquidity discussion
- Covenant compliance summary
- Narrate each section of the model — do not just paste numbers without commentary
- Add any supplementary analysis performed outside the borrower's reporting:
  - Industry analysis or market developments
  - Public company comparable valuations (EV multiples, trading levels)
  - Estimated enterprise value for the borrower based on current comps

### Step 5: First Pass Complete

At this point you have:
- Updated quarterly model
- Draft quarterly presentation with MD&A
- List of questions from processing

### Step 6: Resolve Questions

Send the compiled questions list to the management team, the agent (administrative agent for the facility), or whoever manages the relationship. Seek answers to every question on the list.

Sources for answers:
- Direct management call or email exchange
- Agent or servicer (for facility-level questions)
- Additional research (industry data, public filings, news)
- Sponsor (for PE-backed borrowers)

### Step 7: Incorporate Answers and Finalize

Once questions are answered:
- Update the model if answers require adjustments (reclassifications, additional data points)
- Update the quarterly presentation with the additional context
- Incorporate management commentary into the MD&A narrative
- Update comps and supplementary analysis if new information warrants changes

### Step 8: Done

The quarterly review is complete when:
- Financial data is extracted and entered into the quarterly model
- All model analysis is updated for the latest quarter
- Questions identified during processing have been answered
- Answers are incorporated into both the model and the presentation
- The quarterly review package is ready for IC or portfolio review meeting

---

## Credit Trajectory Evaluation

### Evaluate Each Line Item Independently

Credit trajectory is not a single number — it is an assessment of direction across multiple financial dimensions. Evaluate each independently because they can send conflicting signals:

- **Revenue trajectory:** Growing, stable, or declining? What is the rate of change?
- **Cost of goods sold / Gross profit trajectory:** Are margins expanding, compressing, or stable? Is the company spending more to generate each dollar of revenue?
- **Operating expense trajectory:** Is OpEx growing faster than revenue? Which categories are driving it?
- **EBITDA trajectory:** Combining the above — is the bottom line improving or deteriorating?
- **Cash flow trajectory:** Is the business converting EBITDA to cash effectively? Are working capital or capex trends changing the cash conversion story?

### Conflicting Signals

Revenue can be growing while margins deteriorate. EBITDA can be stable while cash flow declines (due to working capital consumption or increased capex). The credit story is built from the combination of these individual trends, not from any single metric.

When signals conflict, the analysis must explain why:
- "Revenue up 8% YoY driven by new customer acquisition, but EBITDA margin compressed 200bps due to sales team investment. Management guided to margin recovery in H2 as the sales team matures."
- "EBITDA stable at $15M but free cash flow declined 30% due to a $3M increase in working capital driven by extended receivable terms on two new enterprise contracts."

### How Many Quarters to Call a Trend

- **1 quarter:** Not a trend. An observation.
- **2 quarters:** Not a trend. A data point. Worth noting but not actionable as a trajectory.
- **3-4 quarters:** A trend. You can describe the trajectory with confidence and should adjust your forward view accordingly.

---

## Watchlist Criteria

### Two Categories Drive Watchlist Placement

**Category 1: EBITDA and Leverage Deterioration**

| Performance vs. Plan | Classification | Action |
|---|---|---|
| 10-15% below plan | Watch closely | Heightened monitoring. More detailed questions. Track trajectory. |
| 20-25% below plan | Watchlist | Approaching covenant levels. Formal watchlist designation. Active IC flagging. |
| Covenant breach | Watchlist / Workout | 100% on watchlist. May require workout classification depending on severity and cure options. |

The borrower should be on the watchlist **before** a covenant breach, not after. The purpose of the watchlist is early identification. If a breach is the first time a borrower appears on the watchlist, the monitoring process failed.

Exception: A sudden, unexpected large decline within a single period that causes an immediate breach without prior warning signs. This happens but should be rare.

**Category 2: Cash Flow and Liquidity**

Even if revenue is acceptable and leverage has not deteriorated significantly:
- Insufficient cash flow generation → watchlist
- Thin liquidity with no access to additional sources (fully drawn revolver, no additional capacity) → watchlist
- Upcoming maturity with no clear refinancing path → watchlist

Cash flow and liquidity can deteriorate independently of EBITDA — working capital consumption, capex spikes, or one-time cash outlays can drain liquidity while the P&L looks fine.

### Three-Tier System

| Tier | Criteria | Response |
|---|---|---|
| **Watch closely** | Performance 10-15% off expectations. Early signs of deterioration. | Extra scrutiny on quarterly review. Deeper management questions. Track trajectory quarter by quarter. |
| **Watchlist** | Close to covenant breach (within 5-10% headroom). Performance 20-25% off plan. Liquidity thinning. | Formal IC flagging. Increased monitoring frequency if possible. Proactive engagement with management on remediation. Assessment of cure rights and amendment options. |
| **Workout** | Covenant breached. Significant performance deterioration. Liquidity crisis. | Active remediation plan. Amendment or waiver negotiations. Restructuring considerations. Frequent (monthly or more) updates to IC. |

### What Gets a Borrower Off the Watchlist

Sustained improvement over multiple quarters (3+ quarters of trend reversal), covenant headroom rebuilt to comfortable levels (>20%), liquidity restored, and the underlying cause of deterioration addressed — not just temporarily masked.

---

## Management Call Questions

### What Makes a Good Question

A good management call question demonstrates that the analyst understands the business and the financials. After receiving the answers, the analyst should be able to answer any question IC might ask about the borrower's performance, trends, and key credit considerations.

### Two Dimensions of Questions

**Financial questions — driven by the numbers:**
- Identify discrepancies between periods or between financials and cert
- Identify trends that cannot be explained from the available data
- Dig into specifics: "AR days extended from 45 to 58 over two quarters — is this a change in collection terms, customer mix shift, or concentration in a few large receivables?"
- Unpack margin movements: "Gross margin compressed 300bps QoQ — is this COGS inflation, product mix shift, pricing pressure, or something else?"
- Follow the cash: "Working capital consumed $2M this quarter vs. generating $500K last quarter — what drove the swing?"

**Narrative questions — driven by the business story:**
- Understand the story behind the numbers: why is revenue up, why is margin down, why is leverage higher or lower
- Probe specific events: "Revenue includes a $1.5M contract win with [Customer] — is this recurring or project-based?"
- Track management's narrative consistency: are they telling the same story quarter over quarter? If guidance from Q2 said margin recovery by Q4 and margins are still compressing, ask specifically what changed.

### Second-Order Thinking

The most common problem with junior analyst questions is that they stop at the first-order observation:
- Bad: "EBITDA margin declined this quarter."
- Good: "EBITDA margin declined 250bps QoQ. Gross margin was flat, so the compression is coming from OpEx. SG&A grew 15% while revenue grew 3%. Is this the sales team investment you discussed in Q2, or is there a new expense driver? And when should we expect the revenue contribution from this investment to materialize?"

The second version shows the analyst traced the margin compression to its source, linked it to prior management commentary, and is asking a forward-looking question about when the investment pays off.

### Prior Quarter Context Is Mandatory

Every quarter, the analyst must refresh on the prior quarter's:
- Financial performance and trends
- MD&A and management commentary
- Questions asked and answers received
- Any commitments or guidance management provided

Compare the current quarter's numbers and narrative to the prior quarter. Track whether management is delivering on what they said. If they guided to margin recovery and margins continued to decline, that is a question.

When monitoring many portfolio companies, it is easy to forget details from the prior quarter. This is why written question logs and MD&A notes are essential — they provide continuity.

---

## Performing Credit vs. Watchlist Credit

The workflow is the same. The difference is scrutiny and depth.

**Performing credit (shelf credit):**
- Standard quarterly review process
- Check-the-box questions if the business is performing well
- Less time investment per quarter — the company is doing fine, acknowledge it, update the model, move on

**Watchlist credit:**
- Same process, significantly more scrutiny
- Sharper, more detailed questions on every financial line item
- More questions overall — dig into everything, not just the headlines
- Must understand the answers to all components — no surface-level acceptance
- Track management responses with more rigor — are they delivering on commitments?
- Higher priority in portfolio review — present with more detail and urgency to IC
