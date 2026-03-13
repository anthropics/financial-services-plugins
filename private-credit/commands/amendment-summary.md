---
description: "Structured summary of every change in a credit amendment"
argument-hint: "<attached amendment document>"
---

# /private-credit:amendment-summary

Produces a structured, mechanical summary of every change in a credit agreement amendment. Categorizes each change as tightened, loosened, new, or removed.

---

## Trigger

User invokes `/private-credit:amendment-summary` with an amendment document, amended and restated credit agreement, consent letter, or waiver letter attached or referenced.

---

## Required Inputs

| Input | Required? | Notes |
|---|---|---|
| Amendment document | **Yes** | The amendment, consent, waiver, or A&R credit agreement |
| Original credit agreement or prior amendment (if available) | Recommended | Enables comparison to prior terms — helpful but not required since amendments typically state what changed |

---

## What This Command Does

This is a **mechanical extraction and categorization exercise.** It does not assess whether the amendment is borrower-friendly or lender-friendly, does not compare to market terms, and does not provide qualitative judgment on the changes. Those assessments require legal expertise and market data that are outside the scope of this command.

---

## Extraction Framework

Read the amendment document end to end and extract every material change. Categorize each change into one of four classifications:

| Classification | Definition |
|---|---|
| **Tightened** | A term that became more restrictive for the borrower (lower leverage threshold, higher coverage requirement, smaller basket, additional restriction) |
| **Loosened** | A term that became less restrictive for the borrower (higher leverage threshold, lower coverage requirement, larger basket, removed restriction) |
| **New** | A term, covenant, basket, or provision that did not exist before and is being added |
| **Removed** | A term, covenant, basket, or provision that existed before and is being eliminated |

---

## What to Capture

Extract and categorize changes across these categories. Not every amendment will have changes in every category — only include categories that are modified.

### Pricing Changes
- Spread changes (increase or decrease, by how much)
- OID changes
- SOFR floor changes
- Commitment fee changes
- PIK toggle or PIK rate changes
- Call protection or prepayment premium changes

### Structural Changes
- Maturity extension or reduction
- Amortization schedule changes (increased, decreased, holiday)
- New tranches added or existing tranches modified
- Revolver commitment changes (increased, decreased)
- Delayed draw commitments added or modified
- Accordion feature changes

### Financial Covenant Changes
- Maintenance covenant threshold modifications (state old and new levels)
- Step-down schedule modifications (state full revised schedule)
- Test frequency changes
- Covenant holiday or suspension periods
- New financial covenants added
- Existing financial covenants removed

### Incurrence Test Changes
- Leverage levels for restricted payments modified
- Leverage levels for additional debt incurrence modified
- Leverage levels for investments modified

### Basket and Definition Changes
- CapEx basket changes (dollar amount, percentage, or elimination)
- Restricted payment basket changes
- Investment basket changes
- Debt incurrence basket changes
- Permitted acquisition thresholds changed
- Builder basket modifications

### EBITDA / Financial Definition Changes
- Permitted addback modifications (new addbacks, removed addbacks, cap changes)
- Pro forma adjustment methodology changes
- Synergy realization period changes
- Any other defined term modifications that affect financial calculations

### Waivers
- Waiver of any past breach (note the covenant breached, the period, and that it was waived)
- Temporary waivers with expiration dates

### Other Material Changes
- Reporting requirement changes
- Collateral or guarantee modifications
- Change of control definition changes
- Assignment or transfer provision changes
- Any other provisions modified by the amendment

---

## Output Format

### Header

```
AMENDMENT SUMMARY
Borrower: [Name]
Amendment: [Amendment No. X / A&R Credit Agreement / Consent / Waiver]
Effective Date: [Date]
```

### Priority Items (Top of Output)

The most important changes go first — these are what the reader needs within 30 seconds:

1. **Pricing changes** — any change to the cost of borrowing
2. **Structural changes** — maturity, amortization, tranche modifications
3. **Covenant resets** — threshold changes, new covenants, removed covenants

### Categorized Change List

For each change, present:

```
[TIGHTENED / LOOSENED / NEW / REMOVED]

Category: [Pricing / Structure / Covenant / Basket / Definition / Waiver / Other]
Item: [Specific term or provision]
Prior: [Previous term, if applicable]
Revised: [New term]
Section: [Credit agreement section reference, e.g., "Section 7.1(a)"]
```

Group changes by classification (all tightened together, all loosened together, etc.) or by category (all pricing together, all covenants together) — whichever produces a cleaner, more readable output for the specific amendment. For amendments with many changes, grouping by category is typically clearer.

### Summary Count

At the bottom:
```
Total changes: [X]
  Tightened: [X]
  Loosened: [X]
  New: [X]
  Removed: [X]
```

---

## Calibration Notes

- **Extract every material change.** Do not skip minor items — let the reader decide what matters.
- **Use precise language from the amendment.** When the amendment states a specific threshold, basket size, or date, reproduce it exactly. Do not paraphrase numbers.
- **State old and new values side by side.** For every modification, the reader must see what it was and what it is now.
- **Section references matter.** Include the credit agreement section reference for each change so the reader can locate it in the document.
- **No qualitative assessment.** Do not characterize the amendment as "favorable" or "unfavorable." Do not compare to market. Summarize the facts.
