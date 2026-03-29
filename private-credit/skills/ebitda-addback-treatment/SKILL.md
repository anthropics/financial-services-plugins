# EBITDA Add-Back Treatment

This skill fires automatically when working with EBITDA calculations, addback analysis, compliance certificate reconciliation, or any workflow that requires bridging from reported to adjusted EBITDA.

---

## The EBITDA Waterfall — Build-Up Order

Always build EBITDA from the bottom up. Start with Net Income and add back each component to verify you can reach Reported EBITDA before layering credit agreement adjustments.

### Step 1: Build to Reported EBITDA

```
Net Income
+ Income Tax Expense (use actual tax, not provision adjustments)
+ Depreciation & Amortization
+ Interest Expense
= Reported EBITDA
```

This number should tie to whatever the borrower labels as "EBITDA" or "Operating EBITDA" in their financials. If it does not, investigate before proceeding. Common causes of mismatch: the borrower may include or exclude items below the operating line differently than you expect (FX gains/losses, other income/expense, non-cash impairments).

### Step 2: Layer Credit Agreement Adjustments

From Reported EBITDA, apply the adjustments permitted under the credit agreement. The compliance certificate will itemize these if the borrower provides a detailed cert. Categories typically include:

```
Reported EBITDA
+ Non-cash charges (stock-based comp, non-cash rent, impairments)
+ Permitted restructuring / transformation addbacks (subject to caps)
+ Management fees (if not already above the line)
+ Transaction / M&A costs
+ Pro forma acquisition EBITDA (for tuck-ins during the LTM period)
+ Run-rate cost savings / synergies (subject to credit agreement terms)
+ Other permitted addbacks per credit agreement
= Adjusted EBITDA (Covenant Compliance EBITDA)
```

### Step 3: Track on an LTM Basis

Best practice is to track Reported EBITDA on a rolling LTM basis and then layer adjustments separately. This lets you:
- See the trend in the underlying business before adjustments
- Identify when new adjustments are introduced or existing ones change materially
- Verify that LTM Adjusted EBITDA ties to the compliance certificate

If the LTM build-up does not tie to the cert, investigate. Do not assume an error — it is usually an explainable difference (see reconciliation challenges below).

### Sanity Check: Cash Flow Statement Cross-Reference

As a secondary verification, calculate EBITDA from the cash flow statement:

```
Net Income (from CFS)
+ Income Taxes (add back)
+ Interest Expense (add back)
+ Depreciation & Amortization (add back from CFS)
= EBITDA (CFS-derived)
```

Compare this to your P&L-derived Reported EBITDA. They should be close. Differences arise from non-cash items classified differently between the P&L and CFS, but this is a useful gut check on magnitude.

---

## Reconciliation Challenges

### Worst-Case Reporting

Some borrowers provide only: Revenue → Gross Profit → Adjusted EBITDA. No detail on operating expenses, no D&A breakout, no interest or tax detail. When you receive this:
- You cannot independently build to Reported EBITDA
- You cannot strip adjustments to see underlying performance
- Flag this as a reporting limitation and note that independent verification of EBITDA adjustments is not possible with the information provided
- Push for more detailed reporting in management calls or through the agent

### Acquisitions in the LTM Period

When a borrower completes an acquisition during the LTM period, the compliance cert will include a pro forma adjustment for the acquired company's pre-acquisition EBITDA. This acquired EBITDA figure is usually itself adjusted (the acquired company's adjusted EBITDA, not reported). You will not be able to independently decompose this into the acquired company's revenue, expenses, and addbacks on a historical basis.

**How to handle:**
- Accept the pro forma acquired EBITDA as presented on the cert — it is CFO-signed
- Note it as a line item in your tracking: "Acquired EBITDA — [Company Name] — $X.XM"
- In your internal analysis, be clear about how much of total Adjusted EBITDA comes from organic operations vs. pro forma acquisition contribution
- Track whether acquired EBITDA contributions are growing, stable, or declining in subsequent quarters as the acquisitions are fully integrated and the PF period rolls off

### COGS-Level Adjustments

Some addback categories include amounts that sit within cost of goods sold. The borrower reports gross profit as a single line (net of these), then lists the full addback amount on the compliance cert. A portion of the cert addback is already reflected in gross profit, which can create an apparent mismatch.

**How to handle:**
- If the P&L shows gross profit only (no COGS detail), accept that you cannot fully decompose the addback between COGS and OpEx
- Note the limitation
- Focus on whether the total addback amount per the cert is reasonable, not whether you can allocate it across P&L sections

### New Adjustments Applied Retroactively

Borrowers may introduce a new addback category in Q3 and apply it retroactively to Q1 and Q2 for LTM calculation purposes. This causes your prior quarterly spreads to not tie to the new LTM cert.

**How to handle:**
- Update your tracking to include the new category
- Note when it was introduced and the retroactive amount
- Flag if the retroactive application is material (>5% of EBITDA)

---

## Cash vs. Non-Cash: Critical Distinction

When evaluating a borrower's true cash flow generation ability, you must understand which EBITDA adjustments are cash and which are non-cash.

- **Non-cash addbacks** (stock-based comp, non-cash rent, impairments): These inflate Adjusted EBITDA but do not represent additional cash the business generates. Reported EBITDA, which already includes these non-cash items as expenses, may be a better proxy for the business's true cash-generating capacity.
- **Cash addbacks** (restructuring charges actually paid, transaction costs, management fees paid in cash): These represent real cash outflows that the credit agreement permits to be added back for covenant purposes, but the cash still left the building.

**Rule:** When assessing the borrower's ability to service debt, generate free cash flow, and maintain liquidity, always distinguish between cash and non-cash adjustments. Adjusted EBITDA per the cert is the right number for covenant compliance. It is not necessarily the right number for assessing debt service capacity.

---

## Addback Caps

Credit agreements typically impose caps on certain addback categories. Common structures:

- **Dollar cap:** "Non-recurring charges capped at $2M per annum"
- **Percentage of EBITDA cap:** "Restructuring charges capped at 15% of LTM EBITDA"
- **Basket cap:** "Total permitted addbacks (excluding pro forma acquisition adjustments) capped at 25% of EBITDA"

### How to Handle

- Pull caps from the credit agreement at close and record them in your tracking
- The compliance certificate will usually state the applicable cap
- CFOs manage to the caps and are aware of them — this is not an area where analysts need to police
- If adjustments exceed the cap, the borrower will likely request an amendment to increase it
- Note the cap and the current utilization level for reference, but do not flag unless the borrower appears to be structuring around the cap (splitting adjustment categories to avoid triggering)

---

## Push-Back Framework

You cannot change what the borrower reports on their compliance certificate. Push-back happens in two places: (1) conversations with the management team, and (2) internal credit discussions when you assess the borrower's true free cash flow generation capacity.

### When to Highlight and Potentially Exclude

Apply this framework to each addback category:

| Condition | Action |
|---|---|
| Same addback appearing at similar levels for 3-4 consecutive quarters | Not one-time. Highlight. Consider excluding from internal FCF view. |
| Single category > 5% of EBITDA | Noteworthy. Highlight. Investigate what is included. |
| Single category > ~$500K on a $15-20M EBITDA business | Definitely highlight. May exclude if you believe it is not legitimate. |
| Single category < ~$100K on a $15-20M EBITDA business | Immaterial. Ignore unless pattern across multiple small categories. |
| Multiple categories individually < 5% but aggregating to > 10-15% | Flag the aggregate. Individually small does not mean collectively immaterial. |

### Most Abused Addback Category

**"Restructuring / Transformation / Operational Improvement / M&A Expenses"** — This category is the most broadly defined in most credit agreements. Companies can classify a wide range of expenses under these labels. Key watchpoints:
- Is the dollar amount consistent quarter over quarter? If so, it is a run-rate cost, not a one-time charge.
- Are new initiatives continually being added as old ones are supposedly completed?
- Can management specifically identify the projects, their expected cost, and their expected completion date?

### Tracking Realization

A good analyst tracks addback realization across quarters:
- What adjustments were flagged as temporary or one-time?
- Have they rolled off, or are they persisting?
- Are new adjustments replacing old ones at similar dollar levels?
- If "restructuring" was $1.5M in Q1 and $1.4M in Q4, with different underlying projects cited each quarter, the total dollar exposure has not actually declined — the company is spending at a run-rate pace and relabeling.

Flag this trend and notify if new adjustments are coming on or existing ones are trending higher instead of rolling off as expected.

---

## Run-Rate Synergies and Cost Savings

### Credit Agreement Governs

The credit agreement specifies the permitted realization window for run-rate synergies and cost savings — typically 12 to 24 months from the date of the action giving rise to the synergy. Do not apply a different timeline than what the agreement specifies unless it has been amended.

### Tracking Realization vs. Projection

When the borrower projects the same synergies quarter after quarter without visible P&L improvement:
- Ask specifically: What has been actioned? What is on the come?
- For actioned items: When will the impact appear in reported financials?
- For on-the-come items: What is the timeline and what milestones must be hit?
- Track projected synergies vs. actual realized savings on a quarterly basis
- If the gap between projected and realized is not closing, flag it — the synergies may not materialize

### Pro Forma Acquisition Synergies (Roll-Ups)

For acquisition-intensive businesses, pro forma synergies layer on top of pro forma acquired EBITDA. Each tuck-in may come with its own synergy estimate. Track:
- Which acquisitions have associated synergy projections
- What the dollar amount is per acquisition
- Whether realized synergies are appearing in the P&L as the acquisitions integrate
- The total aggregate synergy number vs. what has been achieved

This is especially important for roll-up businesses where EBITDA can include multiple layers of pro forma adjustments and synergies from acquisitions at different stages of integration.
