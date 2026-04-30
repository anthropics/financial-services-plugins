# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A plugin marketplace for Claude Cowork and Claude Code targeting financial services roles. Each top-level subdirectory is a standalone plugin. There is no build system — all plugin content is markdown and JSON files that take effect immediately on edit.

## Key Files

| File | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Registers all plugins in the marketplace with name, source path, and description |
| `<plugin>/.claude-plugin/plugin.json` | Plugin metadata: name, version, description, author |
| `<plugin>/commands/*.md` | Slash commands — invoked as `/<plugin>:<command-name>` |
| `<plugin>/skills/<name>/SKILL.md` | Skills — loaded automatically when trigger conditions match; must have YAML frontmatter with `name` and `description` |
| `<plugin>/.mcp.json` | MCP server connections for that plugin |
| `<plugin>/hooks/hooks.json` | Event-driven automation hooks |
| `<plugin>/.claude/<plugin>.local.md` | Per-user config (gitignored); `.local.md.example` files show the expected shape |

## Plugin Architecture

**financial-analysis** is the core plugin and provides all MCP data connectors (Daloopa, Morningstar, S&P Global, FactSet, Moody's, MT Newswires, Aiera, LSEG, PitchBook, Chronograph, Egnyte). All other plugins are add-ons that assume financial-analysis is installed first.

**partner-built/** contains plugins maintained by external data partners (LSEG, S&P Global) — treat these as externally owned.

**claude-in-office** is different from the financial workflow plugins — it's an enterprise deployment wizard for provisioning the Claude Office add-in against Vertex AI, Bedrock, or an LLM gateway.

## Skill Structure

Skills under `skills/<name>/` can contain three optional subdirectories:
- `scripts/` — executable Python/bash scripts Claude can run directly
- `references/` — markdown docs loaded into context during skill execution
- `assets/` — templates/files used in output (not loaded into context)

Skills require YAML frontmatter at the top of `SKILL.md`:
```yaml
---
name: skill-name
description: When and how to invoke this skill (trigger conditions matter here)
---
```

## Command Frontmatter

Commands support these frontmatter fields:
```yaml
---
description: Short description shown in the command picker
argument-hint: "[company name or ticker]"
---
```

## Tooling

**Scaffold a new skill** (in any plugin's `skills/` directory):
```bash
python3 financial-analysis/skills/skill-creator/scripts/init_skill.py <skill-name> --path <plugin>/skills
```

**Validate a skill's structure and frontmatter:**
```bash
python3 financial-analysis/skills/skill-creator/scripts/quick_validate.py <path-to-skill-dir>
```

**Install Python dependencies** (needed by DCF model scripts and ib-check-deck):
```bash
pip install -r financial-analysis/skills/dcf-model/requirements.txt
```

**Build a customized claude-in-office manifest:**
```bash
node claude-in-office/scripts/build-manifest.mjs <out.xml> key=value [key=value ...]
# e.g.: node claude-in-office/scripts/build-manifest.mjs acme.xml gateway_url=https://llm.acme.com
```

**Validate the generated manifest:**
```bash
npx -y office-addin-manifest validate manifest.xml
```

## Per-User Configuration

Plugins with a `.claude/<plugin>.local.md.example` file support user-specific settings. Copy the example file to `.claude/<plugin>.local.md` (gitignored) to activate it. The investment-banking plugin uses this for banker identity, coverage sectors, active mandates, and deal parameters.

## Adding a New Plugin

1. Create `<plugin-name>/.claude-plugin/plugin.json` with name, version, description, author
2. Add at least one of: `commands/`, `skills/`, `hooks/hooks.json`, `.mcp.json`
3. Register the plugin in `.claude-plugin/marketplace.json` with its source path and description
