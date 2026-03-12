# Super PE

description: End-to-end private equity deal lifecycle skill — from sourcing through portfolio monitoring. Combines deal sourcing, deal screening, due diligence checklists, diligence meeting prep, IC memo drafting, returns analysis, unit economics, portfolio monitoring, and value creation planning into a single unified workflow. Use for any PE workflow, or when a task spans multiple stages of the deal lifecycle. Triggers on "super pe", "full deal workflow", "PE workflow", "run the full process", "end to end PE", or when the user's request touches multiple PE workstreams.

## Overview

This skill orchestrates the **complete private equity deal lifecycle**. Use it when you need to work across multiple stages — or invoke any individual stage directly. The stages are designed to feed into each other: sourcing outputs feed screening, screening feeds diligence, diligence feeds IC memo, and so on.

```
Deal Lifecycle:

  Sourcing → Screening → Due Diligence → IC Memo → Close → Portfolio Monitoring
     │           │            │    │          │                    │
     │           │         Checklist │     Returns               Value
     │           │         Meeting   │     Analysis              Creation
     │           │          Prep     │                           Plan
     │           │                   │
     │           │              Unit Economics
     │           │
     └───────────┴── Can loop back at any stage
```

---

## Stage 1: Deal Sourcing

Discover target companies, check CRM for existing relationships, and draft personalized founder outreach emails.

### Workflow

**Step 1: Discover Companies**
- Research and identify potential targets based on user criteria
- Parameters: Sector/industry focus, revenue range, EBITDA range, growth profile, geography, ownership type (founder-owned, PE-backed, corporate carve-out)
- Sources: Web search, industry reports, conference attendee lists, trade publications, competitor landscapes
- Output: Shortlist with name, description, estimated revenue/size, location, founder/CEO name, website, and thesis fit

**Step 2: CRM Check**
- Search email (Gmail) for prior correspondence with the company or founder
- Search Slack for internal mentions or prior discussions
- Ask user: "Have you or your team had any prior contact with [Company]?"
- Flag existing relationships, prior passes, or known context
- Output: For each company — "New", "Existing" (summarize prior contact), or "Previously Passed"

**Step 3: Draft Founder Outreach**
- Tone: Professional but warm — founders respond better to genuine, concise outreach
- Structure: Brief intro, why this company caught your attention (reference something specific), what you're looking for (partnership), soft ask
- Personalization: Reference the company's specific product, recent news, or market position
- Length: 4-6 sentences max
- Voice matching: Study user's prior sent emails to match tone and style
- Subject line: Short and specific, reference the company or sector
- No attachments on first touch, clear but low-pressure CTA

### Important Notes
- Present shortlist for user review before drafting emails
- Never send emails without explicit user approval
- Prioritize quality over quantity — 5 well-researched targets beat 20 generic ones

---

## Stage 2: Deal Screening

Quickly screen inbound deal flow — CIMs, teasers, and broker materials — against the fund's investment criteria.

### Workflow

**Step 1: Extract Deal Facts**
From the provided CIM, teaser, or description, extract:
- Company: Name, location, sector/subsector
- Description: What they do (1-2 sentences)
- Financials: Revenue, EBITDA, margins, growth rate
- Deal type: Platform, add-on, recap, minority, carve-out
- Asking price / valuation: Multiple, enterprise value
- Seller motivation, management plans, key customers, key risks

**Step 2: Screen Against Criteria**

| Criterion | Target | Actual | Pass/Fail |
|-----------|--------|--------|-----------|
| Revenue range | | | |
| EBITDA range | | | |
| EBITDA margin | | | |
| Growth profile | | | |
| Sector fit | | | |
| Geography | | | |
| Deal size / EV | | | |
| Valuation (x EBITDA) | | | |
| Customer concentration | | | |
| Management continuity | | | |

**Step 3: Quick Assessment**
1. Verdict: Pass / Further Diligence / Hard Pass
2. Bull case (2-3 bullets)
3. Bear case (2-3 bullets)
4. Key questions for a first call

**Step 4: Output** — One-page screening memo for partners or IC quick screen.

### Important Notes
- Speed matters — screening should take minutes, not hours
- Be direct about red flags
- Save screening criteria in memory for future deals once confirmed

---

## Stage 3: Due Diligence Checklist

Generate and track comprehensive due diligence checklists tailored to sector, deal type, and complexity.

### Workflow

**Step 1: Scope the Diligence**
- Target company: Name, sector, business model
- Deal type: Platform, add-on, growth equity, recap, carve-out
- Deal size / complexity
- Key concerns to prioritize
- Timeline: LOI / close target dates

**Step 2: Generate Workstream Checklists**

**Financial Due Diligence**
- Quality of earnings (QoE) — revenue and EBITDA adjustments
- Working capital analysis — normalized vs. actual
- Debt and debt-like items
- Capital expenditure (maintenance vs. growth)
- Tax structure and exposure
- Audit history and accounting policies
- Pro forma adjustments (run-rate, synergies)

**Commercial Due Diligence**
- Market size and growth (TAM/SAM/SOM)
- Competitive positioning and market share
- Customer analysis — concentration, retention, NPS
- Pricing power and contract structure
- Sales pipeline and backlog
- Go-to-market effectiveness

**Legal Due Diligence**
- Corporate structure and org chart
- Material contracts (customer, supplier, partnership)
- Litigation history and pending claims
- IP portfolio and protection
- Regulatory compliance
- Employment agreements and non-competes

**Operational Due Diligence**
- Management team assessment
- Organizational structure and key person risk
- IT systems and infrastructure
- Supply chain and vendor dependencies
- Facilities and real estate
- Insurance coverage

**HR / People Due Diligence**
- Org chart and headcount trends
- Compensation benchmarking
- Benefits and pension obligations
- Key employee retention risk
- Culture assessment
- Union/labor agreements

**IT / Technology Due Diligence** (for tech-enabled businesses)
- Technology stack and architecture
- Technical debt assessment
- Cybersecurity posture
- Data privacy compliance (GDPR, CCPA, SOC2)
- Product roadmap and R&D spend
- Scalability assessment

**Environmental / ESG** (where applicable)
- Environmental liabilities
- Regulatory compliance history
- ESG risks and opportunities

**Step 3: Status Tracking**

| Item | Workstream | Priority | Status | Owner | Notes |
|------|-----------|----------|--------|-------|-------|
| QoE report | Financial | P0 | Pending | | |
| Customer interviews | Commercial | P0 | In Progress | | 3 of 10 complete |

Status options: Not Started -> Requested -> Received -> In Review -> Complete -> Red Flag

**Step 4: Red Flag Summary**
- What was found, which workstream, severity (deal-breaker / significant / manageable), mitigant, impact on valuation

**Step 5: Output**
- Excel workbook with tabs per workstream
- Summary dashboard: % complete by workstream, outstanding items, red flags
- Weekly status update format for deal team

### Sector-Specific Additions
- **Software/SaaS**: ARR quality, cohort analysis, hosting costs, SOC2
- **Healthcare**: Regulatory approvals, reimbursement risk, payor mix
- **Industrial**: Equipment condition, environmental remediation, safety record
- **Financial services**: Regulatory capital, compliance history, credit quality
- **Consumer**: Brand health, channel mix, seasonality, inventory management

---

## Stage 4: Diligence Meeting Prep

Prepare for due diligence meetings — management presentations, expert network calls, customer references, and advisor sessions.

### Workflow

**Step 1: Meeting Context**
- Meeting type: Management presentation, expert call, customer reference, advisor check-in, site visit
- Attendees, topic focus, what you already know, key concerns to probe

**Step 2: Generate Question Lists**

#### Management Presentation
**Business Overview (warm-up)**
- Walk us through the founding story and key milestones
- How do you describe the business to someone unfamiliar with the space?
- What are you most proud of? What would you do differently?

**Revenue & Growth**
- Walk us through revenue by customer/segment/geography
- What's driving growth? Price vs. volume vs. new customers
- Sales cycle and win rate trends
- Biggest growth opportunities in the next 3-5 years

**Competitive Positioning**
- Who do you lose deals to and why?
- What's your moat? How defensible is it?
- How do customers evaluate you vs. alternatives?

**Operations & Team**
- Walk us through the org chart — key people
- What roles are you hiring for? What's been hardest to fill?
- What keeps you up at night operationally?

**Financial Deep-Dive**
- Margin bridge — what's changed and why
- One-time or non-recurring items
- Capex — maintenance vs. growth
- Working capital seasonality

**Forward Look**
- Budget/plan for next year
- Assumptions you're most/least confident in
- What would need to go right/wrong to significantly beat/miss plan

#### Expert Network Call
- Market positioning, secular trends, strongest competitors, investor risks, what to diligence most carefully

#### Customer Reference Call
- How did you find them, why did you choose them, alternatives evaluated, strengths/weaknesses, renewal likelihood, price sensitivity

**Step 3: Benchmarks & Context** — Industry growth rates, comparable metrics, data room discrepancies

**Step 4: Red Flags to Probe** — Inconsistencies, concentration signals, management gaps, unusual accounting, missing data room items

**Step 5: Output** — One-page meeting prep doc with objectives, prioritized questions, benchmarks, red flags, follow-up items

### Important Notes
- Lead with open-ended questions
- Don't lead the witness
- Always end with: "What haven't we asked about that we should?"
- Keep to 15-20 questions max for a 60-90 min session

---

## Stage 5: Returns Analysis

Build quick IRR/MOIC sensitivity tables for PE deal evaluation.

### Workflow

**Step 1: Gather Deal Inputs**

Entry: Entry EBITDA, entry multiple, enterprise value, net debt, equity check, fees
Financing: Senior debt (x EBITDA, rate, amortization), sub debt/mezz, total leverage, equity contribution
Operating: Revenue growth rate, EBITDA margin trajectory, capex %, working capital changes, debt paydown
Exit: Hold period, exit multiple, exit EBITDA

**Step 2: Base Case Returns**

| Metric | Value |
|--------|-------|
| Entry EV | |
| Equity invested | |
| Exit EBITDA | |
| Exit EV | |
| Net debt at exit | |
| Exit equity value | |
| **MOIC** | |
| **IRR** | |

Returns waterfall: EBITDA growth contribution, multiple expansion/contraction, debt paydown, fee/expense drag

**Step 3: Sensitivity Tables**
- Entry Multiple vs. Exit Multiple (IRR / MOIC in each cell)
- EBITDA Growth vs. Exit Multiple
- Leverage vs. Exit Multiple
- Hold Period vs. Exit Multiple

**Step 4: Scenario Analysis**

| | Bull | Base | Bear |
|---|------|------|------|
| Revenue CAGR | | | |
| Exit EBITDA margin | | | |
| Exit multiple | | | |
| MOIC | | | |
| IRR | | | |

**Step 5: Output** — Excel workbook with assumptions, returns calculation, formatted sensitivity tables, scenario summary. One-page returns summary for IC deck.

### Key Formulas
- **MOIC** = Exit Equity Value / Equity Invested
- **IRR** = solve for r: Equity Invested x (1 + r)^n = Exit Equity Value
- **Attribution**: Growth = (Exit EBITDA - Entry EBITDA) x Exit Multiple / Equity; Multiple = (Exit Multiple - Entry Multiple) x Entry EBITDA / Equity; Leverage = Debt paydown / Equity

### Important Notes
- Show returns both gross and net of fees/carry
- Account for management rollover and co-invest
- Include dividend recaps or interim distributions if planned
- Don't forget transaction costs (2-4% of EV)
- Consider tax structure (asset vs. stock deal, 338(h)(10))

---

## Stage 6: Unit Economics Analysis

Analyze unit economics for PE targets — ARR cohorts, LTV/CAC, net retention, payback periods, revenue quality.

### Workflow

**Step 1: Identify Business Model**
- SaaS / Subscription: ARR, net retention, cohorts
- Recurring services: Contract value, renewal rates, upsell
- Transaction / usage-based: Revenue per transaction, volume trends, take rate
- Hybrid: Break down by revenue stream

**Step 2: Core Metrics**

#### ARR / Revenue Quality
- ARR bridge: Beginning ARR -> New -> Expansion -> Contraction -> Churn -> Ending ARR
- ARR by cohort (vintage analysis)
- Revenue concentration: Top 10/20/50 customers as % of total
- Revenue by type: Recurring vs. non-recurring vs. professional services
- Contract structure: ACV distribution, multi-year %, auto-renewal %

#### Customer Economics
- CAC: Total S&M spend / new customers acquired
- LTV: (ARPU x Gross Margin) / Churn Rate
- LTV:CAC ratio (target >3x)
- CAC payback period
- Blended vs. segmented (enterprise vs. SMB vs. mid-market)

#### Retention & Expansion
- Gross retention, net retention (NDR), logo churn, dollar churn, expansion rate

#### Cohort Analysis
Build a cohort matrix showing absolute $ and indexed (Year 0 = 100%) views.

#### Margin Waterfall
Revenue -> Gross Profit -> Contribution Margin -> EBITDA with fully loaded unit economics

**Step 3: Benchmarking**
- SaaS Rule of 40: Growth + EBITDA margin > 40%
- Magic Number: Net new ARR / prior period S&M > 0.75x
- NDR: Best >120%, good >110%, concerning <100%
- LTV:CAC: Best >5x, good >3x, concerning <2x
- Gross retention: Best >95%, good >90%, concerning <85%
- CAC payback: Best <12mo, good <18mo, concerning >24mo

**Step 4: Revenue Quality Score**

| Factor | Score (1-5) | Notes |
|--------|-------------|-------|
| Recurring % | | |
| Net retention | | |
| Customer concentration | | |
| Cohort stability | | |
| Growth durability | | |
| Margin profile | | |
| **Overall** | | |

### Important Notes
- Always ask for raw customer-level data if available
- NDR >100% can mask high gross churn — always show both
- Cohort analysis is the single most important view for revenue quality
- Differentiate contracted ARR from recognized revenue
- Evaluate professional services revenue separately

---

## Stage 7: Investment Committee Memo

Draft a structured IC memo synthesizing all prior stages into a professional, IC-ready document.

### Memo Structure

**I. Executive Summary** (1 page)
- Company description, deal rationale, key terms, recommendation, headline returns, top 3 risks and mitigants

**II. Company Overview** (1-2 pages)
- Business description, products/services, customer base, competitive positioning, management team

**III. Industry & Market** (1 page)
- Market size/growth, competitive landscape, secular trends, regulatory environment

**IV. Financial Analysis** (2-3 pages)
- Historical performance, QoE adjustments, working capital, capex

**V. Investment Thesis** (1 page)
- 3-5 pillars, value creation levers, 100-day priorities

**VI. Deal Terms & Structure** (1 page)
- Enterprise value, implied multiples, sources & uses, capital structure, key legal terms

**VII. Returns Analysis** (1 page)
- Base/upside/downside scenarios, IRR and MOIC, key assumptions, sensitivity tables

**VIII. Risk Factors** (1 page)
- Ranked by severity and likelihood, mitigants, deal-breakers

**IX. Recommendation**
- Clear recommendation: Proceed / Pass / Conditional proceed with key conditions

### Output
- Word document (.docx) with professional formatting
- Tables for financials and returns
- All numbers should tie — EBITDA bridges, S&U balances, returns math

### Important Notes
- Be factual and balanced — present both bull and bear cases honestly
- Don't minimize risks — IC members will find them
- Financial tables must tie
- Ask for missing inputs rather than assuming deal terms

---

## Stage 8: Portfolio Monitoring

Track and analyze portfolio company performance against plan.

### Workflow

**Step 1: Ingest Financial Package**
- Accept Excel, PDF, or CSV financial packages
- Extract: Revenue, EBITDA, cash balance, debt outstanding, capex, working capital
- Identify reporting period, compare to prior period and budget/plan

**Step 2: KPI Extraction & Variance Analysis**

Financial KPIs: Revenue vs. budget, EBITDA and margin vs. budget, cash/net debt, leverage ratio, interest coverage, capex vs. budget, FCF
Operational KPIs: Customer count, revenue per customer/employee, backlog/pipeline, churn/retention

**Step 3: Flag & Summarize**
- Green: Within 5% of plan
- Yellow: 5-15% below plan
- Red: >15% below plan or covenant breach risk

Output: Executive summary, KPI table (actual vs. budget vs. prior), red/yellow flags, covenant compliance, questions for management

**Step 4: Trend Analysis** (multiple periods)
- Chart key metrics over time
- Identify trends — accelerating, decelerating, stable
- Compare vs. underwriting case

---

## Stage 9: Value Creation Plan

Structure post-acquisition value creation with revenue, cost, and operational levers mapped to an EBITDA bridge.

### Workflow

**Step 1: Baseline Assessment**
- Current revenue, EBITDA, margins
- Org structure and capabilities
- Management strengths and gaps
- Quick wins identified during diligence

**Step 2: Value Creation Levers**

#### Revenue Growth Levers
- Organic growth: Pricing, volume, market expansion
- Cross-sell / upsell
- New market entry: Geographic, vertical, channel
- Sales force effectiveness
- M&A / add-ons

#### Margin Expansion Levers
- Pricing optimization
- COGS reduction: Procurement, supplier consolidation, automation
- OpEx optimization: Overhead, shared services, offshoring
- Technology investment
- Scale leverage

#### Strategic / Multiple Expansion
- Platform building via add-ons
- Recurring revenue shift
- Market positioning / category leadership
- Management upgrades
- ESG / governance improvements

**Step 3: EBITDA Bridge**

| Lever | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|-------|--------|--------|--------|--------|--------|
| Base EBITDA | | | | | |
| Organic revenue growth | | | | | |
| Pricing | | | | | |
| Add-on M&A | | | | | |
| COGS savings | | | | | |
| OpEx optimization | | | | | |
| Technology investment | | | | | |
| **Pro Forma EBITDA** | | | | | |
| **Margin** | | | | | |

**Step 4: 100-Day Plan**

Days 1-30 (Stabilize & Assess): Management alignment, quick wins, operational assessment, customer communication, KPI dashboards
Days 31-60 (Plan & Initiate): Strategic plan, launch top 3-5 initiatives, add-on pipeline, critical hires, reporting cadence
Days 61-100 (Execute & Measure): First results, first board meeting, progress report, plan adjustments

**Step 5: KPI Dashboard**

| KPI | Current | Year 1 Target | Owner | Frequency |
|-----|---------|---------------|-------|-----------|
| Revenue | | | CEO | Monthly |
| EBITDA | | | CFO | Monthly |
| EBITDA margin | | | CFO | Monthly |
| New customer wins | | | CRO | Weekly |
| Net retention | | | CRO | Monthly |
| Employee turnover | | | CHRO | Monthly |
| Cash conversion | | | CFO | Monthly |

### Important Notes
- Most PE value creation takes 12-24 months to show in financials
- Quick wins matter for momentum but don't over-rotate on cost cuts at expense of growth
- Management buy-in is critical — co-develop the plan
- Add-on M&A is often the largest lever — start pipeline on Day 1
- Pressure-test assumptions with operating partners or industry experts

---

## Cross-Stage Integration

When running multiple stages, data flows forward automatically:

| From | To | What Carries Forward |
|------|----|---------------------|
| Sourcing | Screening | Target company details, initial research |
| Screening | DD Checklist | Deal facts, initial assessment, key concerns |
| Screening | Returns | Financial metrics for quick returns sizing |
| DD Checklist | Meeting Prep | Outstanding items, red flags to probe |
| DD Checklist | Unit Economics | Data room financials for cohort analysis |
| DD + Returns + Unit Econ | IC Memo | All findings synthesized into the memo |
| IC Memo | Value Creation | Investment thesis drives the value creation plan |
| Value Creation | Portfolio Monitoring | KPI targets become the monitoring framework |

**To use**: Simply describe what you need. If your request spans multiple stages, the skill will orchestrate them in sequence. If you need a single stage, it will execute just that stage.
