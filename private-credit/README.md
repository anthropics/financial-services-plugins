# Private Credit Plugin

A Claude plugin for analysts and portfolio managers at direct lending funds. Encodes the domain expertise, workflows, and judgment frameworks used in private credit — from CIM screening through quarterly portfolio monitoring.

Built for [Claude Cowork](https://claude.com/product/cowork), also compatible with [Claude Code](https://claude.com/product/claude-code).

> **Disclaimer:** This plugin assists with private credit workflows but does not provide investment, financial, or legal advice. All outputs — including covenant calculations, credit assessments, and investment recommendations — should be reviewed by qualified professionals before use in investment decisions, regulatory filings, or committee presentations.

## Who This Is For

- **Credit analysts** doing quarterly monitoring, model updates, and borrower analysis
- **Portfolio managers** reviewing covenant compliance and credit trajectory
- **Investment professionals** screening deals, writing IC memos, and running scenarios
- **Operations teams** processing amendments and tracking covenant schedules

Works best for middle-market direct lending ($50M–$500M deal size), leveraged finance, ABL, and specialty lending workflows.

## What's Included

### Skills (auto-fire when relevant)

Skills encode domain knowledge Claude draws on automatically — no slash command needed.

| Skill | What it covers |
|-------|---------------|
| **Covenant Compliance** | Maintenance vs. incurrence testing, compliance cert as source of truth, step-down schedule lookup, headroom analysis (≥20% comfortable, 10–20% elevated, <10% flag), cross-checking financials against cert |
| **EBITDA Add-Back Treatment** | GAAP-to-Adjusted EBITDA waterfall, permitted addbacks per credit agreement, pro forma acquisition adjustments, cap mechanics, push-back framework for management's numbers, addback realization tracking |
| **Credit Memo Standards** | IC memo structure and section order, minimum content bar, advocacy tone calibration, merit/risk framework, base and downside case presentation standards |
| **Quarterly Package Extraction** | Extraction order (P&L → BS → CF), label-matching logic, compliance cert vs. financials reconciliation, handling acquisitions and restatements, common data quality issues |
| **Borrower Monitoring** | Full quarterly workflow (receive → update → narrate → question → deliver), credit trajectory evaluation, watchlist criteria (3-tier: watch closely / watchlist / workout), management call question development |
| **Credit Model Standards** | LBO-based model structure, tab organization, FCF waterfall construction (exact line-item order), case methodology (base / downside / stress), credit statistics, debt schedule roll-forward |

### Commands (user-triggered)

| Command | What it produces |
|---------|-----------------|
| `/private-credit:cim-screen` | Pass / Pursue / More Info assessment from a CIM or teaser with supporting credit analysis |
| `/private-credit:ic-memo` | Full investment committee memo in private credit format (requires CIM + model + term sheet) |
| `/private-credit:quarterly-review` | Covenant compliance table, variance summary with MD&A narrative, management call questions |
| `/private-credit:covenant-check` | Comprehensive covenant snapshot: maintenance tests with headroom, incurrence levels, restricted baskets, step-down schedule, cure rights |
| `/private-credit:amendment-summary` | Structured summary of every change in an amendment, categorized as tightened / loosened / new / removed |
| `/private-credit:scenario-analysis` | Base / Downside / Stress case comparison table with covenant breach flagging and liquidity runway |

## Plugin Structure

```
private-credit/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── amendment-summary.md
│   ├── cim-screen.md
│   ├── covenant-check.md
│   ├── ic-memo.md
│   ├── quarterly-review.md
│   └── scenario-analysis.md
├── skills/
│   ├── borrower-monitoring/SKILL.md
│   ├── covenant-compliance/SKILL.md
│   ├── credit-memo-standards/SKILL.md
│   ├── credit-model-standards/SKILL.md
│   ├── ebitda-addback-treatment/SKILL.md
│   └── quarterly-package-extraction/SKILL.md
├── LICENSE
└── README.md
```

## Installation

```bash
# From the marketplace
/plugin install private-credit@claude-plugin-directory

# Or from GitHub
/plugin marketplace add accretive-ai/private-credit-plugin
/plugin install private-credit@accretive-ai
```

Once installed, skills activate automatically when Claude detects relevant context (financial data, credit agreements, borrower packages). Commands are available via `/private-credit:command-name`.

## Optional MCP Connectors

This plugin works standalone — paste or upload financial data and documents directly. For live data integration, add MCP servers to a `.mcp.json` file in the plugin directory:

- **PitchBook** — Private equity and deal data for comparable transactions
- **Moody's** — Credit ratings and company financial data
- **FactSet** — Financial data, analytics, and market benchmarks
- **S&P Global / Kensho** — Capital IQ financial data

See [MCP documentation](https://modelcontextprotocol.io/) for connector setup.

## Customization

These skills and commands encode general private credit best practices. They become more powerful when customized for your firm:

- **Adjust covenant severity rankings** — Edit `covenant-compliance/SKILL.md` to match your firm's headroom thresholds and escalation criteria
- **Add your EBITDA definition** — Modify `ebitda-addback-treatment/SKILL.md` with your standard permitted addbacks and cap structures
- **Match your IC memo format** — Update `credit-memo-standards/SKILL.md` with your firm's section order, required exhibits, and tone preferences
- **Configure watchlist criteria** — Adjust thresholds in `borrower-monitoring/SKILL.md` to match your fund's risk rating framework
- **Set variance callout thresholds** — Modify `quarterly-review.md` to match what your IC considers material

## About

Built by [Accretive AI](https://goaccretive.ai). The team behind Accretive AI has billions invested and decades of experience across leveraged finance, ABL, and special situations.

## License

Apache-2.0 — see [LICENSE](LICENSE) for details.
