# Company Research Report Agent Blueprint

This document defines a practical way to turn the existing `equity-research` and `financial-analysis` plugins into a company research report agent with minimal custom infrastructure.

The goal is not to build a generic finance chatbot. The goal is to produce reviewable company research reports with a repeatable workflow, source traceability, and a clear split between what this repo already does well and what should be connected from external tools.

## Objective

Support two high-value equity research workflows first:

- Initiating coverage
- Company update / earnings review

Both workflows should produce a structured draft that an analyst can review, edit, and export. The agent should optimize for:

- Faster first draft creation
- Consistent report structure
- Clear evidence for key claims
- Tight linkage between model outputs and written conclusions

## What This Repo Already Provides

This repository already contains the core workflow skeleton for a research-report agent:

- `equity-research/skills/initiating-coverage`
  - A 5-task initiation workflow
  - Report template guidance
  - Quality checklist
- `equity-research/skills/earnings-analysis`
  - Earnings update workflow
- `equity-research/commands/initiate.md`
  - User-facing initiation command
- `equity-research/commands/earnings.md`
  - User-facing earnings command
- `financial-analysis/commands/comps.md`
  - Comparable companies workflow
- `financial-analysis/commands/dcf.md`
  - DCF workflow

Use these as the default control plane:

- `equity-research` owns report logic and report-writing workflow
- `financial-analysis` owns valuation, model-building, and shared data connectors

## Do Not Rebuild These Pieces

Use the repo's existing structure as-is:

- Plugin manifest and command model
- Skill-based workflow decomposition
- Task-level separation for initiation reports
- Valuation subflows for `comps` and `dcf`
- Final QC checklist structure

That means the first version should be implemented by extending documentation, templates, and connector choices, not by replacing the current plugin architecture.

## Report Framework To Adopt

Do not invent a report format from scratch. Use a hybrid institutional structure derived from publicly visible sell-side and buy-side report patterns:

- Goldman Sachs style for the front page
  - Put rating / target price / valuation summary first
  - Lead with 3-4 high-information investment bullets
  - Show key operating and valuation metrics on page 1
- CICC and broader Chinese sell-side style for the body
  - `Investment thesis / event view`
  - `Company overview`
  - `Industry and competition`
  - `Business-line deep dives`
  - `Financial analysis`
  - `Forecast and valuation`
  - `Risks`
- Fund-style internal research checklist for completeness
  - Business model
  - Market space
  - Competitive position
  - Growth drivers
  - Governance and incentives
  - Risks and disconfirming evidence

This approach copies the structure and sequencing, not protected report text or proprietary layouts.

## Report Assembly Model

Do not draft the final report in one pass. Assemble it in the following order:

1. `Fact Pack`
   - Company profile
   - Historical financials
   - Segment mix
   - Peer set
   - Industry data
   - Source list
2. `Investment View Pack`
   - Thesis pillars
   - Variant view
   - Catalysts
   - Key risks
   - Core assumptions
3. `Body Draft`
   - Company, industry, operations, financials, valuation
4. `Front Page Summary`
   - Rating / valuation summary
   - Top bullet points
   - Key metrics table
5. `Verification`
   - Source coverage
   - Numeric consistency
   - Cross-file consistency with the model
6. `Export`
   - DOCX first
   - PDF optional

This ordering matters. The front page should be written last so it reflects the actual analysis and model outputs.

## Open-Source Components To Reuse

The repo intentionally leaves connector choice open. To minimize custom engineering, connect proven open-source components instead of building bespoke data pipelines.

### Filing and structured fundamentals

- `sec-edgar-mcp`
  - SEC filings, company facts, XBRL-aligned fundamentals
  - Good default for US public companies
  - <https://github.com/stefanoamorelli/sec-edgar-mcp>
- `sec-edgar-toolkit`
  - Lower-level filing extraction and XBRL tooling
  - <https://github.com/stefanoamorelli/sec-edgar-toolkit>

### Market data and company profile

- `OpenBB`
  - Unified market data interface with multiple providers
  - Good fit for company profile, price history, and baseline fundamentals
  - <https://github.com/OpenBB-finance/OpenBB>

### Earnings transcripts and event context

- `Octagon MCP Server`
  - Filings, transcripts, market intelligence
  - <https://github.com/OctagonAI/octagon-mcp-server>
- `earningscall-python`
  - Transcript retrieval
  - <https://github.com/EarningsCall/earningscall-python>

### Citation support

- `rag-citation`
  - Adds citations to generated outputs
  - <https://github.com/rahulanand1103/rag-citation>

### Document export

- `docxtemplater`
  - Best fit when a team needs editable Word output
  - <https://github.com/open-xml-templating/docxtemplater>
- `pandoc`
  - Best fit when Markdown-first output is acceptable
  - <https://pandoc.org/>

## What Still Needs Firm-Specific Customization

Do not overbuild. The remaining custom layer should be thin and explicit.

### Must customize

- Chinese report templates
  - Initiating coverage
  - Company update
  - Earnings review
- Sector-specific KPI lists
  - Example: SaaS, consumer, industrials, healthcare
- Rating and target-price language
- Risk disclosure language
- Source-priority rules
  - Official filings first
  - Earnings calls and IR materials second
  - News and third-party commentary last

### Do not customize in V1 unless required

- New plugin architecture
- New valuation engines
- Custom chart renderer
- Fully autonomous multi-agent orchestration

## Recommended Mapping Into This Repo

Keep the existing workflow, but adapt the content layer.

### Extend `equity-research/skills/initiating-coverage`

Use it as the main skeleton for first-time coverage. Adjust:

- report section names
- front-page wording
- source and citation standards
- Chinese output expectations

### Extend `equity-research/skills/earnings-analysis`

Use it for shorter update notes. Keep the same evidence-first discipline, but reduce report length and chart count.

### Reuse `financial-analysis`

Use existing `comps` and `dcf` flows to populate:

- valuation tables
- price target logic
- scenario analysis
- sensitivity discussion

## Suggested V1 Scope

Keep the blast radius small.

- Market: one market first
  - US equities is easiest because of SEC and transcript tooling
- Industries: two sectors max
- Outputs:
  - initiation report
  - earnings review
- Valuation:
  - comps required
  - DCF optional

## Minimal Deliverable Contract

For the first deployable version, require:

- one report draft
- one linked valuation workbook
- one source appendix
- one QC pass

Do not claim completion if:

- key claims lack sources
- model numbers do not reconcile with report numbers
- valuation section is missing peer rationale

## Documentation Follow-Ups

The next documentation steps should be:

1. Adapt initiation and earnings workflow docs to the Chinese framework and source rules
2. Create OpenClaw runtime files for the target deployment
3. Connect the selected provider stack for the launch market
4. Validate the first Feishu end-to-end run

## Handoff

For future context compression or agent switching, read:

- `equity-research/docs/company-research-report-agent-handoff.md`
- `equity-research/docs/company-research-report-agent-implementation-plan.md`
- `equity-research/docs/company-research-source-hierarchy.md`
- `equity-research/docs/company-research-degraded-mode.md`
- `equity-research/docs/company-research-feishu-delivery.md`
- `equity-research/skills/initiating-coverage/assets/chinese-report-template.md`

## Summary

The shortest path is:

- keep the current Anthropic plugin structure
- reuse the repo's existing initiation and valuation workflows
- adopt an institutional report structure instead of inventing one
- connect open-source data and citation components
- customize only the report language, source rules, and sector logic

That yields a company research report agent with minimal new infrastructure and a much smaller maintenance surface area than a custom-built solution.
