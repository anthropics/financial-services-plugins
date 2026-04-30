# FinBrain Alternative Data Plugin

Bring FinBrain's alternative datasets into Claude workflows — Congressional trades, corporate lobbying, federal contract awards, news sentiment, LinkedIn and app-store signals, Reddit mentions, and insider transactions.

## What This Plugin Does

FinBrain specializes in alternative data that isn't well covered by traditional fundamentals providers. This plugin packages FinBrain's MCP tools into 8 workflows organized around three product tiers.

### Tier 1 — Government & Regulatory (flagship)

- **Congressional trades** — Personal stock disclosures from the US House and Senate (STOCK Act filings).
- **Corporate lobbying** — Quarterly lobbying filings: registrants, income, expenses, issue codes, targeted agencies.
- **Federal contracts** — USAspending.gov award records: amount, awarding agency, NAICS, start/end dates.

### Tier 2 — Social & Consumer Intelligence

- **News sentiment** — Aggregated daily sentiment scores plus raw article flow.
- **LinkedIn metrics** — Employee count and follower trends (hiring signals).
- **App-store ratings** — iOS App Store and Google Play Store scores, install counts, ratings counts.
- **Reddit mentions** — Ticker mention counts across subreddits (retail attention).

### Tier 3 — Insider Trading

- **SEC Form 4** — Officer and director transactions with dollar-weighted flow and cluster detection.

## Commands

| Command | Tier | Description |
|---------|------|-------------|
| `/finbrain:gov-reg-brief` | 1 | One-shot government and regulatory footprint: Congressional trades, lobbying spend, federal contract awards |
| `/finbrain:political-trades` | 1 | Deep dive into House and Senate disclosures with politician-level breakdown |
| `/finbrain:corporate-lobbying` | 1 | Quarterly lobbying filings: registrants, issue codes, targeted agencies |
| `/finbrain:government-contracts` | 1 | Federal contract awards with agency, NAICS, and dollar amounts |
| `/finbrain:sentiment-pulse` | 2 | Sentiment trend with news-article and Reddit evidence |
| `/finbrain:consumer-signals` | 2 | LinkedIn hiring trend, app-store scores, Reddit mentions |
| `/finbrain:insider-activity` | 3 | SEC Form 4 digest — buys vs sells by officer, cluster detection |
| `/finbrain:screener` | all | Cross-ticker screens across Tier 1–3 categories |

## Skills

Each command is backed by a corresponding skill that provides the domain knowledge for interpreting FinBrain data:

| Skill | Domain Knowledge |
|-------|-----------------|
| `gov-reg-brief` | Reading government exposure holistically across trading, lobbying, contracts |
| `political-trades` | STOCK Act disclosure mechanics, 45-day reporting lag, committee-membership cross-reference |
| `corporate-lobbying` | Lobbying Disclosure Act filings, issue-code taxonomy, registrant concentration |
| `government-contracts` | USAspending data model, NAICS categorization, agency concentration risk |
| `sentiment-pulse` | Sentiment scoring interpretation, reconciling news mood with Reddit attention |
| `consumer-signals` | Hiring-trend signals, app-store momentum, retail-attention interpretation |
| `insider-activity` | Form 4 transaction codes, cluster-buying heuristics, officer-role context |
| `screener-workflows` | Building cross-ticker screens and composing alt-data ranks |

## Integrations

This plugin connects to the **FinBrain MCP Server** via the [`finbrain-mcp`](https://pypi.org/project/finbrain-mcp/) Python package. See [CONNECTORS.md](CONNECTORS.md) for the complete tool reference.

## Prerequisites

Unlike most partner plugins in this marketplace (which connect to hosted HTTP MCP servers), the FinBrain MCP runs **locally** via stdio. You need:

1. **Python 3.10+**
2. **The `finbrain-mcp` package** on your PATH:

   ```bash
   pip install --upgrade finbrain-mcp
   ```

3. **A FinBrain API key** — sign up at [finbrain.tech](https://finbrain.tech). You can either put it in the MCP client config's `env` block (recommended — most deterministic) or export it as the `FINBRAIN_API_KEY` environment variable.

**Tip:** On Windows especially, putting the key in the client-config `env` block is more reliable than the environment variable approach, because MCP clients don't always inherit the user's ambient environment.

## Installation

### Claude Code

```bash
claude plugin marketplace add anthropics/financial-services-plugins
claude plugin install finbrain@financial-services-plugins
```

Make sure `FINBRAIN_API_KEY` is exported in the shell where you run `claude`:

```bash
export FINBRAIN_API_KEY="your-key-here"
```

### Claude Desktop

Edit the config file (create it if it doesn't exist):

- **macOS** — `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows** — `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux** — `~/.config/Claude/claude_desktop_config.json`

Add the FinBrain server:

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "finbrain-mcp",
      "env": { "FINBRAIN_API_KEY": "your-key-here" }
    }
  }
}
```

**Quit and fully reopen Claude Desktop** after saving — the config is only read at startup.

**macOS fallback — full path:** If Claude Desktop reports that it can't launch `finbrain-mcp`, the app's search PATH may not include the directory where pip installed the script. Find the absolute path and use it in `command`:

```bash
which finbrain-mcp    # macOS / Linux
# (Windows: where finbrain-mcp)
```

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "/full/path/to/finbrain-mcp",
      "env": { "FINBRAIN_API_KEY": "your-key-here" }
    }
  }
}
```

### VS Code

1. Open the Command Palette (`Cmd`/`Ctrl` + `Shift` + `P`) → **"MCP: Open User Configuration"**. That opens your `mcp.json` file.
2. Add the server under the `servers` key:

   ```json
   {
     "servers": {
       "finbrain": {
         "command": "finbrain-mcp",
         "env": { "FINBRAIN_API_KEY": "your-key-here" }
       }
     }
   }
   ```

3. In Copilot Chat, enable **Agent Mode** to use MCP tools.

### Docker (alternative to pip)

If you'd rather not install the Python package directly, build the Docker image from the [finbrain-mcp](https://github.com/ahmetsbilgin/finbrain-mcp) repo:

```bash
docker build -t finbrain-mcp:latest .
```

Then point your MCP client at the container instead of the pip command:

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "finbrain-mcp:latest"],
      "env": { "FINBRAIN_API_KEY": "your-key-here" }
    }
  }
}
```

### Windows environment variable tips

If you prefer the env-var path over the client-config `env` block:

```powershell
# PowerShell (current session only)
$env:FINBRAIN_API_KEY="your-key-here"

# Persistent across processes (fully quit and reopen the MCP client after)
setx FINBRAIN_API_KEY "your-key-here"
```

## Example Workflows

Once installed, you can invoke commands explicitly or ask questions in natural language — the skills will fire automatically.

- "Show me the government & regulatory footprint for LMT" → `gov-reg-brief` skill surfaces Congressional trades, lobbying spend, and federal contract awards in one pass.
- "What's been happening with sentiment and hiring at SHOP?" → `sentiment-pulse` and `consumer-signals` skills combine news-sentiment trend and LinkedIn employee-growth data.
- "Any cluster insider buying at TSLA this quarter?" → `insider-activity` skill pulls SEC Form 4 filings and highlights multi-officer purchases within a short window.

## Troubleshooting

- **"FinBrain API key not configured"** — `FINBRAIN_API_KEY` is not exported in the environment `claude` was launched from, or is not present in the MCP client `env` block. Set it and restart the client.
- **`finbrain-mcp: command not found`** — The package is installed in a different Python environment than the one on your PATH. Run `which finbrain-mcp` to confirm, and `pip show finbrain-mcp` to locate the install.
- **Tool calls return empty results for a ticker** — Call `available_tickers` first to confirm the ticker is in FinBrain's coverage. International tickers may require a suffix (e.g., `BMW.DE`).
- **Outdated data** — Call `health` to confirm the server is reachable, then `pip install --upgrade finbrain-mcp` to pick up the latest SDK.

## License

MIT — see the [finbrain-mcp repository](https://github.com/ahmetsbilgin/finbrain-mcp) for the full license text.
