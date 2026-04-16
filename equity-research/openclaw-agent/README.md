# Company Research OpenClaw Agent

Runtime configuration files for the `company-research` OpenClaw agent.

## Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Main workflow rules, structural requirements, multi-model orchestration |
| `BOOTSTRAP.md` | Agent startup behavior, priority rules, delivery constraints |
| `models.json` | LLM provider configuration (API keys use placeholders) |

## Deployment

These files are deployed to the target OpenClaw runtime:

```
AGENTS.md     → <workspace_root>/AGENTS.md
BOOTSTRAP.md  → <agent_runtime_root>/BOOTSTRAP.md
models.json   → <agent_runtime_root>/models.json
```

## Architecture

```
User (Feishu) → OpenClaw Gateway → company-research agent
                                      ├─ Phase 1: Data collection (qwen3-max, web_search)
                                      ├─ Phase 2: Analysis + writing (subagent via sessions_spawn)
                                      └─ Phase 3: Delivery (Feishu Doc creation)
```

## API Key Setup

Replace placeholders in `models.json` before deploying:

- `${KIMI_API_KEY}` — Moonshot AI API key
- `${VOLCENGINE_API_KEY}` — ByteDance Volcengine API key
- `${CLAUDE_PROXY_BASE_URL}` — Claude API proxy URL
- `${CLAUDE_PROXY_API_KEY}` — Claude API proxy bearer token

The `dashscope` provider uses `"inherit"` (inherits from OpenClaw global config).
