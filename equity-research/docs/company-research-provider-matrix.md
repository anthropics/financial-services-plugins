# Company Research Launch Provider Matrix

This document fixes the V1 provider stack for the company research report agent.

The purpose is to remove ambiguity before runtime implementation.

## V1 Launch Scope

Launch market:

- US public equities first

Reason:

- official SEC disclosure is accessible
- transcript and baseline market-data tooling are easier to source
- evidence hierarchy is easier to enforce

## Provider Matrix

### Company filings and structured fundamentals

Primary:

- `sec-edgar-mcp`
  - SEC filings
  - company facts
  - structured regulatory data

Fallback:

- `sec-edgar-toolkit`

### Market and company profile data

Primary:

- `OpenBB`

Use for:

- price history
- company profile
- market context
- baseline fundamentals when available

### Earnings transcripts and event context

Primary:

- `earningscall-python`

Fallback:

- `Octagon MCP Server`

### Supplemental event/news context

Primary:

- OpenClaw web search and fetch

Restriction:

- may supplement context
- may not serve as sole support for core report conclusions

### Citation layer

Primary:

- `rag-citation`

### Artifact export

Primary:

- Feishu Doc for user-facing delivery

Secondary:

- markdown as internal artifact

- `docxtemplater` for editable docx output

## Minimum Data Coverage By Report Type

### Initiating coverage

Required:

- official filing source
- current financial source
- market/profile source
- transcript or equivalent management communication

### Earnings review / company update

Required:

- latest filing or official announcement
- latest period financial data
- recent management communication if available

## Current V1 Choice Summary

- filings: `sec-edgar-mcp`
- filings fallback: `sec-edgar-toolkit`
- market/profile: `OpenBB`
- transcripts: `earningscall-python`
- transcript fallback: `Octagon MCP Server`
- supplementary search: OpenClaw web search
- citations: `rag-citation`
- delivery: Feishu Doc first, markdown internal, docx later

## Out Of Scope For V1

Do not block launch on:

- proprietary paid terminals
- multi-market support
- full real-time pricing infrastructure
- deeply customized valuation databases
