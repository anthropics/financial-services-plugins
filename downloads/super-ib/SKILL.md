# Super IB

description: End-to-end investment banking deal execution skill — from pitch to close, including deal marketing, financial modeling, presentation QC, and spreadsheet tools. Combines pitch deck creation, CIM drafting, teaser writing, buyer list building, merger modeling, process letters, deal tracking, strip profiles, datapack building, deck checking, deck refreshing, PPT template creation, spreadsheet auditing, and data cleaning into a single unified workflow. Use for any IB workflow, or when a task spans multiple deal execution stages. Triggers on "super ib", "full deal execution", "IB workflow", "run the full IB process", "end to end banking", or when the user's request touches multiple IB workstreams.

## Overview

This skill orchestrates the **complete investment banking deal lifecycle** plus quality-control and productivity tools. Each module can be used independently or chained together for full deal execution.

```
Deal Execution Pipeline:

  Pitch → Marketing → Process → Diligence → Modeling → Close
    │        │           │          │           │
  Pitch    Teaser     Process    Data Room   Merger
  Deck     CIM       Letter     Datapack    Model
  Strip    Buyer
  Profile  List

Quality & Productivity Tools (available at any stage):
  ├── IB Deck Checker — QC any presentation
  ├── Deck Refresh — Update numbers across slides
  ├── PPT Template Creator — Create reusable slide templates
  ├── Audit Spreadsheet — Formula and model integrity checks
  └── Clean Data — Normalize messy spreadsheet data
```

---

## Module 1: Pitch Deck

Populate investment banking pitch deck templates with data from source files.

### Reference Standards
- **Formatting**: Visual hierarchy, text/bullets/tables/charts, alignment, font consistency
- **Calculations**: CAGR, multiples, growth rates, consensus methodology, rounding
- **XML**: PowerPoint XML patterns for tables, shapes, arrows
- **Templates**: Content mapping for common slide types

### Workflow

**Phase 1: Data Extraction**
1. Create backup of original template
2. Identify all source materials (Excel, CSV, PDF, Word, web)
3. Extract and validate data points against original sources
4. Standardize units and currency
5. Verify calculations against formula standards

**Phase 2: Content Mapping**
1. Visually review the template structure and style
2. Map source data to template sections
3. Identify placeholder guidance boxes
4. Note data gaps or mismatches

**Phase 3: Template Population**
1. Remove/reformat placeholder boxes — colored instruction boxes show WHAT to create, not HOW to format
2. Populate each section (content first)
3. Apply formatting to match template style
4. Create tables as actual table objects (NEVER pipe/tab-separated text)
5. Create arrows/shapes as PowerPoint objects
6. Insert company logo if provided

**Phase 4: Validate -> Fix -> Repeat**
```bash
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 150 presentation.pdf slide
```
Check: text readability, actual table objects, proper sizing, bullet consistency, font matching, content boundaries, no placeholder formatting, cross-slide consistency.
Max 3 fix cycles — then document remaining issues and escalate.

**Phase 5: Final Quality Checklist**
- Data accuracy (figures match sources, calculations verified, same figures identical across slides)
- Content mapping (all sections populated, no bracket placeholders, footnotes complete)
- Formatting (contrast, table objects, sizing, bullets, fonts, boundaries)
- Template compliance (instruction boxes removed, style matches, logo present)
- Always recommend user validate in PowerPoint before distribution

### Critical Anti-Patterns (NEVER DO)
1. **Don't populate INTO placeholder boxes** — delete colored instruction boxes, create new content with production formatting
2. **Don't create text-based "tables"** — use actual table objects, never pipe/tab separators
3. **Don't inherit placeholder contrast** — production slides use dark text on light backgrounds

### Quick Reference
- Bullet symbols: checkmark (included), x (excluded), bullet (neutral), dash (sub-bullets)
- Max 6-7 bullets per box, max 2 lines per bullet
- Vertically stacked boxes: identical left margin, width, text start
- Horizontally adjacent boxes: identical top position, height

---

## Module 2: CIM Builder

Structure and draft Confidential Information Memorandums for sell-side M&A processes.

### CIM Structure

**I. Executive Summary** (2-3 pages) — Overview, 5-7 investment highlights, financial summary, transaction overview
**II. Company Overview** (3-5 pages) — History, mission, products/services, business model, differentiators
**III. Industry Overview** (3-5 pages) — TAM/SAM/SOM, trends, competitive landscape, regulatory, barriers to entry
**IV. Growth Opportunities** (2-3 pages) — Organic levers, M&A, operational improvements, white space
**V. Customers & Sales** (3-5 pages) — Customer overview, concentration, retention, GTM, pipeline
**VI. Operations** (2-3 pages) — Org structure, key personnel, facilities, technology, supply chain
**VII. Financial Overview** (5-8 pages) — Historical IS (3-5 years), revenue analysis, EBITDA bridge, BS, CF, capex, working capital, forecast
**VIII. Appendix** — Detailed financials, customer list, product catalog, management bios

### Drafting Guidelines
- Tone: Professional, factual, compelling but not hyperbolic
- Support every claim with data ("Revenue grew at 15% CAGR from 2021-2024")
- Length: 40-60 pages total
- Include confidentiality disclaimer
- Investment highlights should address: growth potential, margin profile, defensibility

---

## Module 3: Teaser

Draft anonymous one-page company teasers for sell-side processes.

### Structure
- **Header**: Deal code name, sector descriptor, confidentiality notice
- **Company Description** (2-3 sentences): What they do without naming them, market position, geography
- **Investment Highlights** (4-6 bullets): Leadership, revenue quality, growth, margins, management, synergy potential
- **Financial Summary**: Revenue, growth CAGR, EBITDA, margin, employees
- **Transaction Overview**: What's offered, timeline, contact info

### Anonymization Checklist
- No company/brand/product names
- No specific city (use region)
- No named customers or partners
- Revenue ranges if sector is small
- No logos or identifiable imagery

---

## Module 4: Buyer List

Build a universe of potential acquirers for sell-side M&A processes.

### Strategic Buyers
- **Direct competitors**: Market share gain, scale
- **Adjacent players**: Product extension, cross-sell, new market
- **Vertical integrators**: Supply chain control, margin capture
- **Platform builders**: Tuck-in, capability fill

Assess: Strategic fit, financial capacity, M&A track record, likelihood, priority (A/B/C)

### Financial Sponsors
- **Platform investors**: New platform in sector
- **Add-on buyers**: Portfolio companies that could bolt-on the target
- **Growth equity**: Minority vs. majority

Assess: Fund size, sector focus, portfolio overlap, recent activity, priority

### Prioritization
- Tier 1 (5-10): Highest fit, contact first
- Tier 2 (10-15): Good fit, second wave
- Tier 3 (10-20): Lower probability, if process needs broadening

### Contact Mapping (Tier 1)
- Decision maker, relationship status, preferences/constraints, best approach channel

---

## Module 5: Merger Model

Build accretion/dilution analysis for M&A transactions.

### Inputs
- Acquirer: Share price, shares outstanding, LTM/NTM EPS, P/E, cost of debt, tax rate, cash, debt
- Target: Share price (if public), shares outstanding, EPS/net income, EV
- Deal terms: Offer price/premium, cash vs. stock mix, new debt, synergies + phase-in, fees, close date

### Analysis
1. **Purchase Price**: Offer price, premium, equity value, EV, implied multiples
2. **Sources & Uses**: New debt, cash, new equity vs. purchase price, refinancing, fees
3. **Pro Forma EPS** (Year 1-3): Standalone vs. pro forma with synergies, foregone interest, new interest, intangible amortization
4. **Sensitivities**: Accretion/dilution vs. synergies & premium; vs. cash/stock mix
5. **Breakeven Synergies**: Minimum for EPS-neutral in Year 1

### Important Notes
- Show both GAAP and adjusted EPS
- Include purchase price allocation (goodwill, intangible amortization)
- Synergy phase-in: Year 1 often only 25-50% of run-rate
- Don't forget foregone interest income and new interest expense

---

## Module 6: Process Letter

Draft process letters and bid instructions for sell-side M&A.

### Letter Types
1. **Initial process letter**: Sent with teaser/CIM — process overview, timeline, IOI requirements
2. **IOI instructions**: Valuation range, consideration form, financing certainty, diligence requirements, timeline to close, conditions, buyer description
3. **Final bid letter**: SPA markup, committed financing, remaining diligence, exclusivity terms, regulatory analysis, key personnel terms, evaluation criteria
4. **Management meeting invitation**: Logistics, attendees, agenda, ground rules, materials, follow-up process

---

## Module 7: Deal Tracker

Track multiple live deals with milestones, deadlines, action items, and status updates.

### Deal Setup
- Deal name/code, client, type, role, size, stage, team, key dates
- Stages: Pre-mandate -> Engaged -> Marketing -> IOI -> Diligence -> Final bids -> Signing -> Close

### Milestone Tracking
Track: Engagement letter, CIM/teaser drafted, buyer list approved, teaser distributed, NDAs, CIM distributed, IOI deadline, shortlist, management meetings, data room, final bid deadline, exclusivity, confirmatory DD, signing, regulatory approval, close

### Action Items
| Action | Deal | Owner | Due Date | Priority | Status |
|--------|------|-------|----------|----------|--------|

### Weekly Deal Review
Per deal: Status update, key developments, upcoming milestones, blockers, next week's action items
Pipeline: Active deals by stage, at-risk deals, new mandates, expected closings

---

## Module 8: Strip Profile

Create professional 1-4 slide company strip profiles for pitch books and deal materials.

### Workflow
1. Clarify: Single or multi-slide, focus areas
2. Research: Filings (BamSEC, SEC EDGAR), market data, consensus estimates, recent news
3. Required metrics: Revenue, EBITDA, margins, EPS, FCF (+/-3 years), valuation multiples, ownership, segment mix
4. Build slide-by-slide with quadrant layouts, verify each visually before proceeding

---

## Module 9: Datapack Builder

Build professional financial data packs from CIMs, SEC filings, or other sources.

### Essential Rules
- **Financial data** (money): Currency format with $ — $#,##0.0 for millions, negatives as $(123.0)
- **Operational data** (counting): Number format, no $ — #,##0
- **Percentages**: 0.0% format, display as 15.0% not 0.15
- **Years**: Text format to prevent comma insertion (2024 not 2,024)

### Critical Success Factors
- Trace every number to source document with page reference
- Formula-based calculations exclusively (no hardcoded values)
- Cross-check all subtotals and totals
- Verify BS balances and CF ties

---

## Module 10: IB Deck Checker

Quality-check any investment banking presentation across four dimensions.

### Workflow
1. Extract text from every slide with slide-level attribution
2. Run number consistency checks (normalize units, categorize values, flag conflicts)
3. Check data-narrative alignment (claims supported by data, plausibility checks)
4. Language polish (IB register, no casual phrasing, consistent terminology)
5. Visual and formatting QC (sources, axis labels, typography, number/date formatting, footnotes)

### Output Categories
- **Critical**: Number mismatches, factual errors, data contradicting narrative — blocks client delivery
- **Important**: Language, missing sources, terminology drift — should fix
- **Minor**: Font sizes, spacing, date formats — polish

---

## Module 11: Deck Refresh

Update numbers across an existing presentation — quarterly refreshes, earnings updates, comp rolls.

### Four-Phase Process

**Phase 1 — Get the data**: Pasted mapping, uploaded Excel, or raw new values. Ask about derived numbers (growth rates, percentages).

**Phase 2 — Read everything, find everything**: Every slide, every variant ($485M, $0.485B, $485,000,000, 485 on chart axes, footnotes). Where numbers hide: text boxes, table cells, chart data labels, chart source data, footnotes, speaker notes.

**Phase 3 — Present the plan, get approval**: Show every instance, what it becomes. Flag derived values that may be stale (growth rates, market shares). **This is an approval gate — don't edit until user confirms.**

**Phase 4 — Execute, preserve, report**: Smallest possible change. Text: preserve font/size/color/bold. Tables: change cell only. Charts: update underlying data, not just labels. Check for overflow from longer numbers. Report what changed and what was flagged but not changed.

---

## Module 12: PPT Template Creator

Create reusable PPT template SKILLS (not presentations) from user-provided PowerPoint templates.

### Workflow
1. User provides template (.pptx or .potx)
2. Analyze: Extract layouts, placeholders, positions, content area boundaries
3. Initialize skill structure
4. Add template to assets/
5. Write self-contained SKILL.md with all placeholder positions, content areas, and code examples
6. Generate sample presentation to validate

### Key: Find the OBJECT placeholder's y position to determine where content actually starts (not subtitle end position).

---

## Module 13: Audit Spreadsheet

Audit formulas and data for accuracy, from quick checks to full financial model integrity audits.

### Scopes
- **Selection**: Just the selected range — formula errors, hardcodes, inconsistencies
- **Sheet**: Full active sheet
- **Model**: Full workbook + financial model integrity checks

### Formula-Level Checks (all scopes)
Formula errors, hardcodes inside formulas, inconsistent formulas, off-by-one ranges, pasted-over formulas, circular references, broken cross-sheet links, unit/scale mismatches, hidden rows/tabs

### Model Integrity Checks (model scope)
- **Structural**: Input/formula separation, color convention, tab flow, date consistency, units
- **Balance Sheet**: Assets = Liabilities + Equity (every period), RE rollforward, goodwill flow
- **Cash Flow**: Ending cash = BS cash, CFO+CFI+CFF = delta cash, D&A match, capex/PP&E tie, WC signs
- **Income Statement**: Revenue build ties, tax calculation, share count
- **Circular references**: Intentional (interest -> debt -> cash -> interest) vs. accidental
- **Reasonableness**: Growth rates, margin norms, terminal value dominance, hockey sticks, edge cases

### Model-Type-Specific Bugs
- **DCF**: Wrong discount period, terminal value not discounted, book vs. market WACC, interest in FCF, tax shield double-count
- **LBO**: Debt paydown vs. cash sweep, PIK accrual, management rollover, exit EBITDA (LTM vs NTM), Day 1 fees
- **Merger**: Wrong share count, synergy phasing, PPA balance, foregone interest, fees in S&U
- **3-Statement**: WC sign errors, depreciation vs PP&E, debt maturity schedule, dividends exceeding NI

### Output
| # | Sheet | Cell/Range | Severity | Category | Issue | Suggested Fix |
Critical / Warning / Info severity levels. Report first, fix only on request.

---

## Module 14: Clean Data

Clean messy spreadsheet data — trim whitespace, fix casing, convert numbers-as-text, standardize dates, remove duplicates.

### Issues Detected
Whitespace, inconsistent casing, numbers stored as text, mixed date formats, duplicates, blanks, mixed types, encoding issues, formula errors

### Approach
- Profile each column (dominant type, outliers)
- Propose fixes before changing anything
- Prefer formulas in helper columns (TRIM, VALUE, UPPER, DATEVALUE) over hardcoded overwrites
- Confirm destructive operations (dedup, fill blanks, overwrite) with user
- Apply category by category with samples between each

---

## Cross-Module Integration

When running a full deal, modules chain naturally:

| Phase | Modules Used |
|-------|-------------|
| **Win the mandate** | Pitch Deck + Strip Profile |
| **Market the deal** | Teaser + CIM + Buyer List + Process Letter |
| **Run the process** | Deal Tracker + Management Meeting logistics |
| **Support diligence** | Datapack Builder + Audit Spreadsheet + Clean Data |
| **Evaluate & model** | Merger Model |
| **QC before sending** | IB Deck Checker + Deck Refresh |
| **Ongoing** | Deal Tracker for pipeline management |

**To use**: Describe what you need. If your request spans multiple modules, the skill orchestrates them. If you need a single module, it executes just that one.
