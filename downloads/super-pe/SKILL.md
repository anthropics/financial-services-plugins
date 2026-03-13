---
name: super-pe
description: "End-to-end private equity deal lifecycle skill — from sourcing through portfolio monitoring. Combines deal sourcing, screening, due diligence, IC memo drafting, returns analysis, unit economics, portfolio monitoring, and value creation into a single unified workflow. Use for any PE workflow including 'source deals,' 'screen this CIM,' 'diligence checklist,' 'IC memo,' 'model returns,' 'unit economics,' 'portfolio review,' 'value creation plan,' or when a task spans multiple PE deal stages. Also triggers on 'super pe,' 'PE workflow,' 'full deal process,' 'deal evaluation,' 'investment committee,' or 'LBO returns.'"
---

# Super PE

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

## File Output Standards

Before creating any deliverable file, read the appropriate document creation skill:
- **Excel files** (returns models, sensitivity tables, KPI dashboards, DD trackers): Read `/mnt/skills/public/xlsx/SKILL.md` first. Apply blue/black/green color coding (blue = inputs, black = formulas, green = cross-tab links). Zero formula errors.
- **Word documents** (IC memos, screening memos): Read `/mnt/skills/public/docx/SKILL.md` first. Professional formatting with table of contents, headers, and page numbers.
- **PowerPoint files** (IC deck slides, returns summaries): Read `/mnt/skills/public/pptx/SKILL.md` first.
- **PDF reports** (portfolio monitoring summaries): Read `/mnt/skills/public/pdf/SKILL.md` first.

These skills contain the formatting standards, openpyxl/python-pptx patterns, and quality requirements for professional output. Do not build files without reading them.

---

## Deal Context (Gather Once, Use Everywhere)

Before running any stage, confirm or collect this context. If the user is running multiple stages in sequence, gather this once at the start — it carries through all stages.

> Before we start, I need the deal context:
> 1. **Fund profile**: Fund name, fund size, target check size range, target ownership (control / significant minority / growth)
> 2. **Investment criteria**: Revenue range, EBITDA range, sector focus, geography, deal types (platform, add-on, growth, recap, carve-out)
> 3. **Current deal stage**: Are we starting from scratch (sourcing), or picking up at a specific stage?
> 4. **Available materials**: What do you have? (CIM, teaser, financial model, data room access, management deck, prior memos)
> 5. **Team context**: Who's on the deal team? Who needs to review outputs?
> 6. **Timeline**: Any hard deadlines? (IC date, bid deadline, exclusivity expiration)

If context was provided in a prior conversation or in `.agents/product-marketing-context.md`, read it first and confirm what's known. Only ask for what's missing.

Store confirmed deal context and reuse across stages — do not re-ask for fund criteria when moving from screening to diligence.

---

## Stage 1: Deal Sourcing

Discover target companies, check CRM for existing relationships, and draft personalized founder outreach emails.

### Workflow

**Step 1: Discover Companies**
- Research and identify potential targets based on user criteria
- Parameters: Sector/industry focus, revenue range, EBITDA range, growth profile, geography, ownership type (founder-owned, PE-backed, corporate carve-out)
- Sources: Web search, industry reports, conference attendee lists, trade publications, competitor landscapes
- Output: Shortlist with name, description, estimated revenue/size, location, founder/CEO name, website, and thesis fit

**Step 2: Relationship & Prior Contact Check**

If Gmail integration is connected:
- Search for prior correspondence with the company name, founder name, and domain
- Summarize: last contact date, context, outcome

If Slack integration is connected:
- Search for internal mentions of the company or founder
- Summarize: who discussed it, when, in what context

If neither integration is available:
- Ask directly: "Have you or your team had any prior contact with [Company]? Any prior passes or known context I should know about?"

For each company on the shortlist, output one of:
- **New** — no prior contact found
- **Existing relationship** — [summary of prior contact, who, when, outcome]
- **Previously passed** — [reason if known, date of pass]
- **Unknown** — integrations unavailable, user did not confirm

Do not silently skip this step if tools are unavailable — the relationship status materially affects the outreach approach.

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

Build institutional-quality LBO returns models with sensitivity tables, scenario analysis, and returns attribution. This is the single most important analytical output in a PE process — it determines whether the deal gets done.

### Workflow

**Step 1: Gather Deal Inputs**

Collect in a structured format. Do not proceed with missing inputs — ask for them or clearly state assumptions.

| Category | Input | Value | Source |
|----------|-------|-------|--------|
| **Entry** | Entry EBITDA (LTM, adjusted) | | QoE / screening |
| | Entry multiple (EV / EBITDA) | | Broker guidance / comps |
| | Enterprise value | | Calculated |
| | Net debt at close | | CIM / data room |
| | Transaction fees (% of EV) | | Typically 2-4% |
| | Equity check (EV - net debt - fees funded by debt) | | Calculated |
| **Financing** | Senior debt (x EBITDA) | | Lender terms |
| | Senior rate (fixed or SOFR + spread) | | Lender terms |
| | Senior amortization (% per year) | | Typically 1-5% |
| | Sub debt / mezz (x EBITDA) | | If applicable |
| | Sub rate | | |
| | Total leverage (x EBITDA) | | Calculated |
| | Management rollover (% of equity) | | Deal terms |
| **Operations** | Revenue CAGR (by scenario) | | Diligence / model |
| | EBITDA margin trajectory | | Diligence / model |
| | Capex (% of revenue) | | Historical + plan |
| | Working capital changes | | Diligence |
| | Cash taxes (% of pre-tax) | | Tax diligence |
| **Exit** | Hold period (years) | | Fund strategy |
| | Exit multiple (by scenario) | | Comps / market |

**Step 2: Sources & Uses**

| Sources | Amount | | Uses | Amount |
|---------|--------|-|------|--------|
| Senior debt | | | Enterprise value | |
| Sub debt / mezz | | | Transaction fees | |
| Sponsor equity | | | Financing fees | |
| Management rollover | | | | |
| **Total Sources** | | | **Total Uses** | |

Sources must equal Uses. If they don't balance, flag it before proceeding.

**Step 3: Build the Operating Model**

For each year of the hold period, project:
- Revenue (prior year x (1 + growth rate))
- EBITDA (revenue x margin)
- Less: cash interest (beginning debt x rate)
- Less: cash taxes
- Less: capex
- Less/plus: working capital changes
- = Free cash flow to equity
- Less: mandatory debt amortization
- = Cash flow available for debt paydown / accumulation

Track debt balance: beginning balance - mandatory amort - optional paydown (cash sweep if applicable) = ending balance.

Track cash balance: beginning + FCF after debt service = ending. If cash exceeds a threshold, apply excess to debt paydown or accumulate per deal terms.

**Step 4: Exit Valuation & Returns**

| Metric | Bull | Base | Bear |
|--------|------|------|------|
| Exit year EBITDA | | | |
| Exit multiple | | | |
| Exit enterprise value | | | |
| Less: net debt at exit | | | |
| Exit equity value | | | |
| **Gross MOIC** | | | |
| **Gross IRR** | | | |
| Net MOIC (after fees/carry) | | | |
| Net IRR (after fees/carry) | | | |

**Key formulas:**
- MOIC = Exit equity value / Equity invested
- IRR = rate that solves: Equity invested x (1 + IRR)^n = Exit equity value (for single cash flow; use XIRR for interim distributions)
- For deals with dividend recaps or interim distributions, model each cash flow individually and use XIRR

**Step 5: Returns Attribution Waterfall**

Decompose total returns into the value creation drivers:

| Driver | MOIC Contribution | % of Total Return |
|--------|-------------------|-------------------|
| Revenue growth | | |
| Margin expansion | | |
| Multiple expansion / (contraction) | | |
| Debt paydown (leverage effect) | | |
| Fees and friction (drag) | | |
| **Total MOIC** | | |

**Attribution methodology:**
- Revenue growth contribution = (Exit revenue - Entry revenue) x Exit margin x Exit multiple / Equity invested
- Margin expansion = Entry revenue growth to exit x (Exit margin - Entry margin) x Exit multiple / Equity invested
- Multiple expansion = Entry EBITDA x (Exit multiple - Entry multiple) / Equity invested
- Leverage contribution = Total debt paydown over hold / Equity invested
- Fees = -1 x (transaction fees + financing fees + monitoring fees) / Equity invested

This waterfall answers the IC's core question: "Where are the returns coming from?" If >50% comes from multiple expansion, the deal is a bet on market conditions. If >50% comes from operations (revenue + margin), the deal is an operations story. IC members will challenge this.

**Step 6: Sensitivity Tables**

Build four 2-variable sensitivity grids. Each cell shows IRR and MOIC.

1. **Entry Multiple vs. Exit Multiple** — tests purchase price risk and exit environment
2. **Revenue CAGR vs. Exit Multiple** — tests operating performance x exit
3. **Leverage (x EBITDA) vs. Exit Multiple** — tests capital structure risk
4. **Hold Period vs. Exit Multiple** — tests timing

Format: IRR as percentage, MOIC as multiple. Color code: green (>25% IRR), yellow (15-25%), red (<15%). Highlight the base case cell.

**Step 7: Scenario Summary**

| | Bull | Base | Bear | Downside |
|---|------|------|------|----------|
| Revenue CAGR | | | | |
| Exit EBITDA | | | | |
| Exit margin | | | | |
| Exit multiple | | | | |
| Gross MOIC | | | | |
| Gross IRR | | | | |
| Net MOIC | | | | |
| Net IRR | | | | |

**Downside scenario must be included.** This is not "bad base case" — it's "what happens if the thesis is wrong." Revenue declines, margin compresses, exit multiple contracts. The question is: do we get our money back? If downside MOIC < 1.0x, the deal has loss risk that IC needs to understand.

**Step 8: Output**

- Excel workbook with tabs: Assumptions, Sources & Uses, Operating Model, Returns Summary, Sensitivity Tables, Scenario Comparison
- Apply xlsx skill standards: blue inputs, black formulas, green cross-links, zero errors
- One-page returns summary (Word or slide) for IC deck insertion
- All numbers must tie: S&U balances, debt schedule reconciles to BS, exit EV math is transparent

### Important Notes
- Show returns both gross and net of fees/carry
- Account for management rollover and co-invest in equity check
- Include dividend recaps or interim distributions if planned
- Transaction costs are typically 2-4% of EV — don't forget them
- Tax structure matters: asset deal 338(h)(10) election changes depreciation basis
- Always show the downside case — hiding it doesn't make it go away
- If returns are >30% IRR in the base case, pressure-test the assumptions — either the deal is exceptional or the model is wrong

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

### Quality Gates (Check Before Delivering)

1. **Numbers tie.** EBITDA in the financial analysis section matches the returns analysis. S&U balances. Debt schedule ties to the balance sheet. Entry multiple x entry EBITDA = enterprise value. If any number appears in two places, it must be identical.
2. **Bull and bear are honest.** The bull case is not "everything goes perfectly." The bear case is not "slightly below base." Bull = thesis plays out plus some upside. Bear = thesis partially fails. Downside = thesis is wrong. If bull and bear MOIC are within 0.5x of each other, the scenario analysis is too narrow.
3. **Risks are ranked and mitigated.** Each risk has a severity (deal-breaker / significant / manageable), a probability, and a specific mitigant. "Market risk" is not a risk — "customer concentration: top 3 customers = 45% of revenue" is a risk.
4. **Recommendation is clear.** "Proceed" / "Pass" / "Proceed with conditions." If conditional, name the exact conditions (e.g., "proceed if QoE confirms adjusted EBITDA within 5% of CIM," "proceed contingent on key employee retention agreements").
5. **One-paragraph test.** A senior partner who reads only the executive summary should be able to understand: what the company does, why it's interesting, what the returns look like, and what could go wrong. If the exec summary fails this test, rewrite it.

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

**Step 3B: Industry-Specific Value Creation Playbooks**

Apply the relevant playbook based on the target's business model. These are starting frameworks — customize based on diligence findings.

#### Software / SaaS
- **Revenue**: Price increases (low-hanging — most SaaS companies underprice), product-led expansion, upsell/cross-sell, new verticals, international
- **Retention**: Reduce churn through onboarding improvement, customer success investment, product stickiness features
- **Margins**: Hosting cost optimization (cloud renegotiation, architecture efficiency), G&A leverage as revenue scales, reduce professional services dependency
- **Multiple expansion**: Shift from license to subscription (if not already), improve NRR above 120%, build platform/marketplace dynamics
- **Add-ons**: Acquire complementary products to increase wallet share, acquire customer bases in adjacent verticals
- **Key KPIs to move**: NRR, gross margin, CAC payback, ARR growth rate, Rule of 40

#### Healthcare Services
- **Revenue**: Geographic expansion (de novo + acquisition), payor mix optimization, ancillary service lines, value-based care contracts
- **Margins**: Procurement consolidation, revenue cycle management improvement, labor model optimization (staffing mix, scheduling)
- **Regulatory**: Compliance infrastructure as a competitive advantage, prepare for reimbursement changes
- **Add-ons**: Build density in existing markets before expanding (referral network effects)
- **Key KPIs to move**: Same-store revenue growth, payor mix (commercial vs. government), patient volume, labor cost as % of revenue

#### Industrial / Manufacturing
- **Revenue**: Pricing (cost-plus renegotiation), aftermarket/service revenue (higher margin), new OEM relationships, geographic expansion
- **Margins**: Procurement consolidation, lean manufacturing, automation investment, energy cost reduction, overhead rationalization
- **Capital efficiency**: Working capital reduction (inventory optimization, AR collection), capex discipline (maintenance vs. growth)
- **Add-ons**: Vertical integration (bring outsourced steps in-house), geographic tuck-ins for customer proximity, capability acquisitions
- **Key KPIs to move**: Gross margin, EBITDA margin, revenue per employee, inventory turns, OTD (on-time delivery)

#### Business Services
- **Revenue**: Price increases, new service lines, technology enablement (SaaS layer on top of services), strategic account expansion
- **Margins**: Delivery model optimization (onshore/offshore mix), technology substitution for manual processes, scale leverage
- **Recurring revenue**: Convert project-based to recurring/managed services contracts, build subscription offerings
- **Add-ons**: Acquire capabilities that cross-sell into existing client base, acquire recurring revenue streams
- **Key KPIs to move**: Revenue per employee, utilization rate, contract renewal rate, recurring revenue %, gross margin by service line

#### Consumer / Retail
- **Revenue**: New store/location economics, e-commerce channel, pricing/promotion optimization, new product lines, loyalty program
- **Margins**: Supply chain optimization, private label expansion, labor scheduling optimization, rent renegotiation
- **Brand**: Marketing efficiency (shift to digital, improve ROAS), brand extensions, franchise model
- **Add-ons**: Adjacent brands, geographic roll-ups, vertical integration (manufacturing, distribution)
- **Key KPIs to move**: Same-store sales growth, gross margin, customer acquisition cost, repeat purchase rate, inventory turn

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
