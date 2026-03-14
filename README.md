# Claude for Financial Services Plugins

Plugins that turn Claude into a specialist for financial services — investment banking, equity research, private equity, and wealth management. Built for [Claude Cowork](https://claude.com/product/cowork), also compatible with [Claude Code](https://claude.com/product/claude-code).

## Why Plugins

Cowork lets you set the goal and Claude delivers finished, professional work. Plugins let you go further: tell Claude how your firm does analysis, which data sources to pull from, how to handle critical workflows, and what slash commands to expose — so your team gets better and more consistent outcomes.

Each plugin bundles the skills, connectors, slash commands, and sub-agents for a specific financial services workflow. Out of the box, they give Claude a strong starting point for helping anyone in that role. The real power comes when you customize them for your firm — your models, your templates, your processes — so Claude works like it was built for your team.

## What is Claude for Financial Services?

Claude for Financial Services is a comprehensive solution built on Claude for Enterprise with specialized capabilities for financial analysis. It connects Claude to the data sources and tools financial professionals use daily — eliminating the need to juggle multiple browser tabs and improving source verification to reduce the risk of errors from manual data gathering.

## End-to-End Workflows

These plugins aren't just a collection of point tools — they enable complete workflows that span research, analysis, modeling, and output creation:

- **Research to Report**: Pull real-time data from MCP providers, analyze earnings results, and generate publication-ready equity research reports — all in a single session
- **Spreadsheet Analysis**: Build comparable company analyses, DCF models, and LBO models as fully functional Excel workbooks with live formulas, sensitivity tables, and industry-standard formatting
- **Financial Modeling**: Populate 3-statement models from SEC filings, cross-check assumptions against peer data, and stress-test scenarios — with blue/black/green color coding conventions built in
- **Deal Materials**: Draft CIMs, teasers, and process letters, then generate pitch deck slides and strip profiles using your firm's branded PowerPoint templates
- **Portfolio to Presentation**: Screen opportunities, run diligence checklists, build IC memos, and track portfolio KPIs — moving seamlessly from data to deliverable

Each workflow connects upstream data sources (via MCP) to downstream outputs (Excel, PowerPoint, Word), so you move from question to finished work product without context-switching.

## Plugin Marketplace

Start with **financial analysis** — the core plugin that provides shared modeling tools and all MCP data connectors. Then add any function-specific plugins to enhance Claude's capabilities for your workflow.

| Plugin | Type | How it helps | Connectors |
|--------|------|-------------|------------|
| **[financial analysis](./financial-analysis)** | Core (install first) | Build comps, DCF models, LBO models, and 3-statement financials. QC presentations and create reusable PPT templates. Provides the shared foundation and all data connectors. | Daloopa, Morningstar, S&P Global, FactSet, Moody's, MT Newswires, Aiera, LSEG, PitchBook, Chronograph, Egnyte |
| **[investment banking](./investment-banking)** | Add-on | Draft CIMs, teasers, and process letters. Build buyer lists, run merger models, create strip profiles, and track live deals through milestones. | — |
| **[equity research](./equity-research)** | Add-on | Write earnings updates and initiating coverage reports. Maintain investment theses, track catalysts, draft morning notes, and screen for new ideas. | — |
| **[private equity](./private-equity)** | Add-on | Source and screen deals, run due diligence checklists, analyze unit economics and returns, draft IC memos, and monitor portfolio company KPIs. | — |
| **[wealth management](./wealth-management)** | Add-on | Prep for client meetings, build financial plans, rebalance portfolios, generate client reports, and identify tax-loss harvesting opportunities. | — |

**41 skills, 38 commands, 11 MCP integrations**

Install these directly from Cowork, browse the full collection here on GitHub, or build your own.

### Partner-Built Plugins

These plugins are built and maintained by our data partners, bringing their financial data and analytics directly into Claude workflows.

| Plugin | Partner | How it helps |
|--------|---------|-------------|
| **[LSEG](./partner-built/lseg)** | [LSEG](https://www.lseg.com/) | Price bonds, analyze yield curves, evaluate FX carry trades, value options, and build macro dashboards using LSEG financial data and analytics. 8 commands covering fixed income, FX, equities, and macro. |
| **[S&P Global](./partner-built/spglobal)** | [S&P Global](https://www.spglobal.com/) | Generate company tearsheets, earnings previews, and funding digests powered by S&P Capital IQ data. Supports multiple audience types (equity research, IB/M&A, corp dev, sales). |

## Getting Started

### Cowork

Install plugins from [claude.com/plugins](https://claude.com/plugins/).

### Claude Code

```bash
# Add the marketplace
claude plugin marketplace add anthropics/financial-services-plugins

# Install the core plugin first (required)
claude plugin install financial-analysis@financial-services-plugins

# Then add function-specific plugins as needed
claude plugin install investment-banking@financial-services-plugins
claude plugin install equity-research@financial-services-plugins
claude plugin install private-equity@financial-services-plugins
claude plugin install wealth-management@financial-services-plugins
```

Once installed, plugins activate automatically. Skills fire when relevant, and slash commands are available in your session:

```bash
/comps [company]                # Comparable company analysis
/dcf [company]                  # DCF valuation model
/earnings [company] [quarter]   # Post-earnings update report
/one-pager [company]            # One-page company profile
/ic-memo [project name]         # Investment committee memo
/source [criteria]              # Deal sourcing
/client-review [client]         # Client meeting prep
```

## How Plugins Work

Every plugin follows the same structure:

```
plugin-name/
├── .claude-plugin/plugin.json   # Manifest
├── .mcp.json                    # Tool connections
├── commands/                    # Slash commands you invoke explicitly
└── skills/                      # Domain knowledge Claude draws on automatically
```

- **Skills** encode the domain expertise, best practices, and step-by-step workflows Claude needs to deliver professional-quality financial work. Claude draws on them automatically when relevant.
- **Commands** are explicit actions you trigger (e.g., `/comps`, `/earnings`, `/ic-memo`).
- **Connectors** wire Claude to the external data sources your workflow depends on — financial data terminals, research platforms, document management, and more — via [MCP servers](https://modelcontextprotocol.io/).

Every component is file-based — markdown and JSON, no code, no infrastructure, no build steps.

## MCP Integrations

All connectors are centralized in the **financial analysis** core plugin and shared across all add-on plugins.

| Provider | URL |
|----------|-----|
| [Daloopa](https://www.daloopa.com/) | `https://mcp.daloopa.com/server/mcp` |
| [Morningstar](https://www.morningstar.com/) | `https://mcp.morningstar.com/mcp` |
| [S&P Global](https://www.spglobal.com/) | `https://kfinance.kensho.com/integrations/mcp` |
| [FactSet](https://www.factset.com/) | `https://mcp.factset.com/mcp` |
| [Moody's](https://www.moodys.com/) | `https://api.moodys.com/genai-ready-data/m1/mcp` |
| [MT Newswires](https://www.mtnewswires.com/) | `https://vast-mcp.blueskyapi.com/mtnewswires` |
| [Aiera](https://www.aiera.com/) | `https://mcp-pub.aiera.com` |
| [LSEG](https://www.lseg.com/) | `https://api.analytics.lseg.com/lfa/mcp` |
| [PitchBook](https://pitchbook.com/) | `https://premium.mcp.pitchbook.com/mcp` |
| [Chronograph](https://www.chronograph.pe/) | `https://ai.chronograph.pe/mcp` |
| [Egnyte](https://www.egnyte.com/) | `https://mcp-server.egnyte.com/mcp` |

> MCP access may require a subscription or API key from the respective provider.

## Making Them Yours

These plugins are starting points. They become much more useful when you customize them for how your firm actually works:

- **Swap connectors** — Edit `.mcp.json` to point at your specific data providers and internal tools.
- **Add firm context** — Drop your terminology, deal processes, and formatting standards into skill files so Claude understands your world.
- **Bring your templates** — Use `/ppt-template` to teach Claude your firm's branded PowerPoint layouts, so every deck matches your style guide.
- **Adjust workflows** — Modify skill instructions to match how your team actually does analysis, not how a textbook says to.
- **Build new plugins** — Follow the structure above to create plugins for workflows we haven't covered yet.

As your team builds and shares plugins, Claude becomes a cross-functional expert. The context you define gets baked into every relevant interaction, so leaders can spend less time enforcing processes and more time improving them.

## Contributing

### Submitting Plugins

**General plugins** should be submitted to the main plugin directory via the [official submission process](https://claude.com/docs/plugins/submit#submitting-your-plugin).

If your plugin is **specific to financial services** and you'd like it listed in this marketplace, host your plugin in your own repository and open a PR that adds an entry to [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json) pointing to it. **Do not** submit PRs containing your plugin's markdown/source files. Note that PRs to this repository are not actively monitored.

**MCP requirement**: Any MCP servers used in your plugin must be listed in the [Claude Connectors Directory](https://claude.com/connectors).

### Other Changes

All other edits to this repository (skills, commands, core plugins) are reserved for repository maintainers.

## License

[Apache License 2.0](./LICENSE)

## Disclaimer

These plugins assist with financial workflows but do not provide financial or investing advice. Always verify conclusions with qualified financial professionals. AI-generated analysis should be reviewed by financial professionals before being relied upon for financial or investment decisions.
