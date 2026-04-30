# Credit Memo Generation — API Keys Configuration Template
# ─────────────────────────────────────────────────────────────────────
# HOW TO USE:
# 1. Copy this file and rename the copy to: config.local.md
# 2. Replace the placeholder values below with your real API keys
# 3. config.local.md is for your private use only — never share it
# 4. Claude reads config.local.md automatically at session start
# 5. The plugin works without keys (lower rate limits; some features restricted)
#
# After setup, run /credit-memo:setup to verify connectivity.
# ─────────────────────────────────────────────────────────────────────

## SERP API  (optional but recommended)
SERPAPI_KEY=YOUR_SERPAPI_KEY_HERE

# Get your key free at: https://serpapi.com/dashboard
# Free tier: 100 searches/month | Paid: 5,000–100,000/month
# Without key: standard web search with lower rate limits
# With key: unlocks Google Finance, Google News, Google Scholar, Bing News

## SEC EDGAR User-Agent  (optional but recommended)
# IMPORTANT: This is NOT a password or API key.
# The SEC requires a courtesy User-Agent in the format:
#   "OrganizationName contact@youremail.com"
# Example: SEC_EDGAR_KEY=Acme Credit Team analyst@acmebank.com
SEC_EDGAR_KEY=YourOrganizationName contact@youremail.com

# Without a User-Agent: limited to 10 req/sec, no full-text search
# With a valid User-Agent: higher rate limits + EDGAR full-text search

## OPTIONAL: Premium Data Source API Keys
# These keys are referenced by config/data-sources.md (where you configure
# which sources to enable and in what priority order).
# BLOOMBERG_KEY=YOUR_BLOOMBERG_KEY_HERE
# REFINITIV_KEY=YOUR_REFINITIV_KEY_HERE
# FACTSET_KEY=YOUR_FACTSET_KEY_HERE
# FACTSET_USER=YOUR_FACTSET_USERNAME_HERE
# SP_CAPITAL_IQ_KEY=YOUR_SP_CAPITAL_IQ_KEY_HERE
# PITCHBOOK_KEY=YOUR_PITCHBOOK_KEY_HERE

## OPTIONAL: Internal Systems
# INTERNAL_DB_API_KEY=YOUR_INTERNAL_DB_KEY_HERE
# INTERNAL_RATINGS_KEY=YOUR_INTERNAL_RATINGS_KEY_HERE
# SHAREPOINT_CLIENT_SECRET=YOUR_SHAREPOINT_SECRET_HERE

## Internal Credit Rating Scale  (optional)
# Define your organization's internal rating scale so it appears
# alongside Moody's / S&P / Fitch ratings in the output.
# Examples:
#   INTERNAL_RATING_SCALE=AAA,AA,A,BBB,BB,B,CCC,D
#   INTERNAL_RATING_SCALE=1,2,3,4,5,6,7,8,9,10
#   INTERNAL_RATING_SCALE=Green,Amber,Red
# INTERNAL_RATING_SCALE=YOUR_SCALE_HERE
