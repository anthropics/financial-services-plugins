---
name: credit-memo-risk-assessment
description: Performs comprehensive risk assessment for credit decisions. Covers external credit ratings (Moody's, S&P, Fitch), internal rating ingestion, liquidity risk, leverage, legal/litigation, operational risks, default history, and collateral. Reads internal rating from config.local.md or prompts user for it. Claude draws on this skill automatically during Credit Memo generation.
---

# Risk Assessment Skill

## Overview
Risk assessment synthesizes all quantitative and qualitative signals into a structured credit risk view. The goal is not to list risks — it is to assess their materiality, probability, and combined impact on the borrower's ability to repay.

---

## Internal Rating Ingestion

### Reading Internal Rating
At the start of risk assessment, check for an internal rating via three sources (in priority order):

**Source 1 — User provided during intake:**
If the user entered an internal rating in Step 2 of the generate command, use that directly.

**Source 2 — config.local.md:**
Check for `INTERNAL_RATING_SCALE` in config. If present, ask user:
```
Your organization has an internal rating scale configured: [SCALE]
Does this borrower have an internal rating? If yes, please provide:
  - Internal rating: [e.g., 4 / BBB / Category B]
  - Rated by: [e.g., Credit Risk Team]
  - Rating date: [e.g., Q3 2024]
  - Key rationale: [optional]
```

**Source 3 — Uploaded document:**
If user uploaded a credit assessment document, extract internal rating from it and tag: `[FROM UPLOAD]`.

**If no internal rating available:**
Note: *"Internal rating not provided. External agency ratings used as primary reference."*

### Internal Rating Display
When internal rating is available, show it prominently alongside external ratings:

| Agency | Rating | Scale | Outlook | Date |
|---|---|---|---|---|
| **Internal** | **[Rating]** | **[Your Scale]** | **[Outlook]** | **[Date]** |
| Moody's | Baa2 | Aaa–C | Stable | Dec 2023 |
| S&P Global | BBB | AAA–D | Stable | Nov 2023 |
| Fitch | BBB- | AAA–D | Negative Watch | Oct 2023 |

**Convergence/Divergence Commentary:**
Write a specific paragraph if internal and external ratings diverge by more than one notch:
*"The internal rating of [X] [is broadly consistent with / is more conservative than / is more optimistic than] the external agency consensus of [Y]. [Explain the divergence and which view is more credible based on available data]."*

---

## Section 1: External Credit Ratings Analysis

### Data Collection (uses SERPAPI_KEY if configured):
```
Search queries:
"{company}" Moody's credit rating outlook 2024
"{company}" S&P Global issuer rating 2024
"{company}" Fitch rating action downgrade upgrade
"{company}" credit rating history upgrade downgrade timeline
```

### Rating Comparison Table:
Include full rating scale reference with company position marked:

**Investment Grade:**
```
Moody's:  Aaa | Aa1 Aa2 Aa3 | A1 A2 A3 | [Baa1 Baa2★ Baa3]
S&P:      AAA | AA+ AA  AA- | A+ A  A- | [BBB+ BBB★ BBB-]
          ←─── STRONGER ──────────────── WEAKER ───►
```

**Speculative Grade (flag prominently if borrower is here):**
```
⚠️  Moody's:  Ba1 Ba2 Ba3 | B1 B2 B3 | Caa1 Caa2 Caa3 | Ca | C
⚠️  S&P:      BB+ BB  BB- | B+ B  B- | CCC+ CCC  CCC- | CC | C | D
```

### Rating Commentary:
Write 3 paragraphs:
1. Current rating summary and what it implies for credit risk
2. Rating trajectory (improving, stable, deteriorating) and primary drivers
3. Rating triggers — specific events that would cause an upgrade or downgrade

---

## Section 2: Liquidity Risk Analysis

### Key Liquidity Metrics:
| Metric | Value | Industry Avg | Threshold | Signal |
|---|---|---|---|---|
| Current Ratio | X.Xx | ~2.0x | >1.0x | 🟢/🟡/🔴 |
| Quick Ratio | X.Xx | ~1.0x | >0.5x | 🟢/🟡/🔴 |
| Cash Ratio | X.Xx | ~0.5x | >0.2x | 🟢/🟡/🔴 |
| Operating CF / Current Liab | X.Xx | — | >0.4x | 🟢/🟡/🔴 |
| Days Cash on Hand | XX days | — | >30 days | 🟢/🟡/🔴 |

> 📊 *[Embed: chart_ratios_dashboard.png — Key Financial Ratios Dashboard]*

Write an interpretation paragraph referencing the visual:
*"As illustrated in the ratio dashboard above, [Company] shows [strong/adequate/concerning] liquidity. [Specific observation about current ratio trend and what it means for near-term debt service]. [Any mitigants or aggravators]."*

---

## Section 3: Leverage & Debt Risk

### Leverage Metrics:
| Metric | Value | Threshold | Signal | Trend |
|---|---|---|---|---|
| Total Debt ($M) | | — | — | ↑/↓/→ |
| Net Debt ($M) | | — | — | ↑/↓/→ |
| Debt / Equity | X.Xx | <2.0x | 🟢/🟡/🔴 | ↑/↓/→ |
| Net Debt / EBITDA | X.Xx | <3.5x | 🟢/🟡/🔴 | ↑/↓/→ |
| Interest Coverage | X.Xx | >3.0x | 🟢/🟡/🔴 | ↑/↓/→ |
| Debt / Revenue | X.Xx | <1.0x | 🟢/🟡/🔴 | ↑/↓/→ |

> 📊 *[Embed: chart_balance_sheet.png — Balance Sheet Composition (3-Year)]*

Write a paragraph on debt structure: senior vs. subordinated, fixed vs. floating, maturity profile, covenant status, and whether the proposed loan increases leverage to concerning levels.

---

## Section 4: Legal & Litigation Risk

### Data Collection:
Use SerpApi with key for enhanced news search:
```
Google News endpoint: engine=google_news&q="{company}"+lawsuit+litigation&tbs=qdr:y2
Additional searches:
  "{company}" SEC investigation enforcement action
  "{company}" regulatory fine penalty
  "{company}" class action lawsuit settlement
```

### Litigation Summary Table:
| Case | Nature | Status | Potential Exposure | Materiality |
|---|---|---|---|---|
| [Case name] | [e.g., Employment class action] | Pending | $Xm | 🟢/🟡/🔴 |
| [Case name] | [e.g., IP dispute] | Settled | $Xm | 🟢 Resolved |

Write a paragraph assessing whether litigation exposure is material relative to the company's EBITDA and cash position, and whether any cases represent existential risk.

---

## Section 5: Operational Risk

Assess the following operational risk factors:
1. **Customer concentration**: Does any single customer represent >10% of revenue?
2. **Supplier concentration**: Is the company dependent on a small number of suppliers?
3. **Geographic concentration**: Is revenue concentrated in high-risk geographies?
4. **Technology/cyber risk**: Has the company experienced breaches? Are systems modern?
5. **ESG/sustainability risk**: Are there environmental liabilities or regulatory exposure?
6. **Business continuity**: Does the company have documented BCM/BCP plans?

---

## Section 6: Default History

Search for:
- Prior defaults or near-defaults in the last 10 years
- Debt restructurings, covenant waivers, or forbearance agreements
- Credit watch or rating withdrawal history
- Any payment delays disclosed in filings

Note: Even a historical default that was resolved may indicate risk culture issues. Comment on the circumstances and whether they are likely to recur.

---

## Section 7: Collateral Analysis

If collateral has been offered:
| Collateral Item | Type | Estimated Value | Liquidity | LTV Ratio |
|---|---|---|---|---|
| [e.g., Property] | Real estate | $Xm | Low | X.X% |
| [e.g., Receivables] | Financial | $Xm | High | X.X% |
| [e.g., Inventory] | Physical | $Xm | Medium | X.X% |

Assess: Is the collateral sufficient to cover the loan in a default scenario? What is the recovery rate assumption by collateral type?

---

## Section 8: Overall Risk Summary

### Risk Heat Map
| Risk Dimension | Level | Trend | Key Driver |
|---|---|---|---|
| Credit Rating | 🟢/🟡/🔴 | ↑/↓/→ | [1 line] |
| Liquidity | 🟢/🟡/🔴 | ↑/↓/→ | [1 line] |
| Leverage | 🟢/🟡/🔴 | ↑/↓/→ | [1 line] |
| Legal / Litigation | 🟢/🟡/🔴 | ↑/↓/→ | [1 line] |
| Operational | 🟢/🟡/🔴 | ↑/↓/→ | [1 line] |
| Default History | 🟢/🟡/🔴 | ↑/↓/→ | [1 line] |
| Collateral Coverage | 🟢/🟡/🔴 | — | [1 line] |
| **Overall Risk** | **🟢/🟡/🔴** | — | — |

> 📊 *[Embed: chart_credit_ratings.png — Credit Rating Scale Visual]*

### Risk Narrative:
Write a 3–paragraph synthesis:
1. Dominant risk factors and their combined effect
2. Key mitigants and why they do or do not offset the risks
3. Risk conditions recommended for the loan structure (covenants, reporting, triggers)
