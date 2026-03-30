# Claude for Office — Direct Cloud Setup

Admin tooling for configuring the Claude Office add-in to call your own cloud
(Vertex AI, Bedrock, or an LLM gateway) instead of Anthropic's API.

## Install

```bash
claude plugin marketplace add anthropics/financial-services-plugins
claude plugin install claude-in-office@financial-services-plugins
```

Then inside the session: `/claude-in-office:setup`

## Commands

| Command | What it does |
|---|---|
| `/claude-in-office:setup` | Interactive wizard — provisions cloud resources, admin consent, writes manifest |
| `/claude-in-office:manifest` | Generate the customized add-in manifest XML |
| `/claude-in-office:consent` | Azure admin consent URL for the add-in's app registration |
| `/claude-in-office:update-user-attrs` | Write per-user config via Microsoft Graph extension attributes |
