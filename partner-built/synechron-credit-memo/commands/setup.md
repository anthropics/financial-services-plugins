---
name: setup
description: Configure API keys and validate Credit Memo plugin connectivity. Run this first after installation or after updating your config.local.md keys.
---

# Command: /credit-memo:setup

## Purpose
Validate API key configuration, test connectivity to all data sources, and display a readiness summary. Run this after first install or whenever you update your API keys.

---

## Trigger
- `/credit-memo:setup`
- "Set up credit memo plugin"
- "Check my API keys"
- "Validate credit memo configuration"

---

## Execution Steps

### STEP 0 — Invoke Guardrails (Layer 1)
Invoke `guardrails` skill (Layer 1: Session Initialization) — this displays the one-time session disclaimer and checks key format validity before proceeding with connectivity tests.

### STEP 1 — Check for config.local.md
Look for `config/config.local.md` in the plugin folder.

**If not found:**
```
⚠️  CONFIG FILE NOT FOUND
─────────────────────────────────────────────────────────────
No config.local.md found. The plugin will work in limited mode
(lower rate limits, some endpoints unavailable).

TO ADD API KEYS:
1. Open: config/config.template.md
2. Copy it and save as: config/config.local.md
3. Fill in your SERPAPI_KEY and SEC_EDGAR_KEY
4. Run /credit-memo:setup again

CONTINUING WITHOUT KEYS...
─────────────────────────────────────────────────────────────
```

**If found:** Proceed to Step 2.

---

### STEP 2 — Validate Key Formats

**SERPAPI_KEY validation:**
- Check: key is present and not a placeholder (`YOUR_SERPAPI_KEY_HERE`)
- Check: key looks like a valid hex string (64 characters)
- Do NOT expose the key value in output — only confirm presence

**SEC_EDGAR_KEY validation:**
- Check: key is present and not a placeholder (`YourOrganizationName contact@youremail.com`)
- Check: key contains a space (i.e., appears to be `OrgName email@domain`) — NOT a hex string
- If the value looks like a hex hash, warn the user:
  ```
  ⚠️  SEC EDGAR KEY FORMAT ISSUE
  Your SEC_EDGAR_KEY appears to be a hex string. SEC EDGAR requires
  a User-Agent in the format: "OrganizationName contact@email.com"
  Example: Acme Bank analyst@acmebank.com
  Please update config.local.md with the correct format.
  ```

---

### STEP 3 — Test Connectivity (Lightweight)

Run one test call per source — do NOT run full data collection:

| Source | Test Query | Expected Response |
|---|---|---|
| SEC EDGAR | Fetch Apple Inc. (AAPL) company info from EDGAR | Company name + CIK returned |
| SerpApi | Single search: "Apple Inc revenue 2023" | Results returned |
| Stock Analysis | Fetch AAPL financials page | Page accessible |
| Macrotrends | Fetch AAPL revenue page | Page accessible |

---

### STEP 4 — Display Readiness Report

```
✅ CREDIT MEMO PLUGIN — SETUP REPORT
══════════════════════════════════════════════════════════
CONFIGURATION
  Config file      : ✅ Found (config/config.local.md)
  SERPAPI_KEY      : ✅ Configured  [100 searches/month on free tier]
  SEC_EDGAR_KEY    : ✅ Configured  [User-Agent format: valid]
  Internal Ratings : ⚠️  Not configured  [Optional — see config.template.md]

CONNECTIVITY
  SEC EDGAR        : ✅ Connected   [Apple Inc. — CIK: 0000320193]
  SerpApi          : ✅ Connected   [Results returned in 0.8s]
  Stock Analysis   : ✅ Accessible
  Macrotrends      : ✅ Accessible
  DiscoverCI       : ✅ Accessible
  Spherical Insights: ✅ Accessible

PLUGIN VERSION   : v1.0.0
══════════════════════════════════════════════════════════
✅ Plugin is ready. Run /credit-memo:generate to start.
══════════════════════════════════════════════════════════
```

If any source fails connectivity, show:
```
  [Source]         : ❌ Unreachable  [Will use fallback sources]
```
And note that the plugin will continue using available sources — no source is required.

---

## Notes
- This command makes only lightweight test calls — it does not consume significant API quota
- API keys are never echoed or logged in output
- If all sources fail, advise user to check internet connectivity
