# Portfolio AI Readiness

description: Scan the portfolio for the highest-leverage AI opportunities and rank where to deploy operating-partner time. Ingests quarterly updates and financials across multiple portfolio companies, identifies quick wins at each, and stacks them into a single ranked action list. Use during quarterly portfolio reviews, annual planning, or when deciding which companies get AI investment first. Triggers on "AI readiness", "AI opportunity scan", "where should we deploy AI", "AI across the portfolio", "AI quick wins", or "which portcos are ready for AI".

## Workflow

### Step 1: Connect to Portfolio Data

First, ask the user where the portfolio materials live. Don't assume — offer the options:

- **MCP servers** — data room, SharePoint, Google Drive, or a portfolio-ops database if one is connected
- **Local files** — a folder path on disk with quarterly decks, financials, board packs
- **File uploads** — drag PDFs, PowerPoint, or Excel directly into the conversation

Once connected, pull quarterly updates, board decks, and financials for the portfolio (or a subset). For each company, extract: sector, revenue, headcount by function, tech stack mentioned, and any AI/automation initiatives already in flight.

If the user provides a single company, still run the scan but skip the cross-portfolio ranking.

Ask up front if not obvious from materials:
- Hold period remaining per company (AI payback matters less 12 months from exit)
- Whether any portco has already deployed something that worked

### Step 2: Per-Company Scan

For each company, answer three gate questions. All three yes → **Go**. Any no → **Wait** with a note on what unblocks it.

1. **Is the data there?** Can they produce a clean input for the use case — customer list, invoice feed, contract repository — without a 6-month data project first?
2. **Is there an owner?** Someone on the management team who will drive this, not a sponsor who will "support" it.
3. **Can we pilot in 30 days?** One team, one workflow, off-the-shelf tooling. If the answer starts with "first we'd need to...", it's not a quick win.

Then identify the top 2-3 leverage points. Look for these patterns in the cost structure and operations:

**Back Office (usually fastest to pilot)**
- Invoice processing, AP/AR matching, expense categorization
- Contract abstraction — vendor agreements, leases, customer MSAs
- Month-end close: reconciliations, flux commentary, lender reporting first drafts

**Revenue / Front Office**
- RFP and proposal first drafts — big lever if revenue is project-based
- Sales call summaries and CRM hygiene
- Customer support ticket triage and first-response drafting
- Quoting for configured / complex products

**Operations (sector-dependent)**
- SOP and quality documentation generation
- Scheduling and dispatch (field services, logistics)
- Code generation and review (software portcos)

For each leverage point, capture in one line: what it replaces, FTE-hours/week saved (assume 30-50%, not 100%), and whether it's buy-off-the-shelf or needs a light build.

### Step 3: Rank Across the Portfolio

Stack every leverage point from every company into one list. Rank by:

1. **Dollar impact** — annualized EBITDA contribution (cost out + revenue lift, net of tool cost)
2. **Speed to value** — months to first measurable result
3. **Probability** — discount for data quality, change management risk, management team capability

Tiebreaker: favor opportunities with <18 months of hold period remaining — those need to move now or not at all.

Output the stack:

| Rank | Company | Opportunity | Est. EBITDA ($) | Months to Value | Gate | First Step |
|---|---|---|---|---|---|---|
| 1 | | | | | Go | |
| 2 | | | | | Go | |
| 3 | | | | | Wait — [blocker] | |

### Step 4: Find the Replays

The highest-leverage move in a portfolio is running one successful play at multiple companies. Scan for:

- **Same sector, same function** — two healthcare services portcos with manual prior-auth? One implementation, two deployments.
- **Same tool, different company** — if one portco already has a working invoice-processing setup, flag every other portco with >$Xm in AP volume as a fast follower.
- **Shared vendor leverage** — three portcos buying the same tool is a pricing conversation.

List each replay with the lead company (who proves it) and follower companies (who copy it).

### Step 5: Output

One page for the operating partner, structured for a portfolio review:

1. **Top 5 across the portfolio** — the ranked table from Step 3, with owner and 30-day first step
2. **Replays** — 2-3 playbooks that hit multiple companies at once
3. **Go / Wait by company** — one line each; for Waits, what unblocks them
4. **What we're NOT doing** — the opportunities that looked good on paper but failed a gate; saves the operating partner from relitigating them every quarter
5. **Aggregate EBITDA contribution** — total portfolio-wide AI opportunity, split Year 1 quick wins vs. Years 2-3 scale

## Important Notes

- **Rank by dollars, not excitement.** A boring AP automation that saves $400k at a $40m revenue company beats a flashy customer-facing chatbot every time.
- **The binding constraint is almost always data, not models.** If a company can't produce a clean customer list, AI isn't the first project — a data cleanup is. Say so plainly.
- **Off-the-shelf first.** Custom builds are slow, expensive, and fragile for companies without engineering depth. Favor tools they can buy and deploy.
- **Ownership is the real gate.** A quick win with no internal owner dies in 90 days. If no one on the management team wants it, mark it Wait regardless of the dollar size.
- **Hold period drives urgency.** A company 3 years from exit can afford a foundational data project. A company 12 months out needs something that shows up in the LTM EBITDA for the CIM — or skip it.
- **Failed pilots are signal.** If management already tried something and it didn't stick, find out why before proposing the same thing again.
