# Credit Memo Generation — Custom Data Sources Configuration
# ─────────────────────────────────────────────────────────────────────
# HOW TO USE:
# This file lets you configure which data sources the plugin uses
# and in what priority order. It also lets you plug in your own
# internal systems and premium data subscriptions.
#
# The plugin works without this file (falls back to free public sources).
# Add this file to unlock premium sources and internal integrations.
#
# ⚠️  SECURITY NOTE:
# Never store API keys or passwords directly in this file.
# Keys belong in config.local.md (which is private to your session).
# This file only references key NAMES and source settings — not key VALUES.
# ─────────────────────────────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════
# SECTION 1 — SOURCE PRIORITY ORDER
# ═══════════════════════════════════════════════════════════════════
# Defines the order in which the plugin tries sources for financial data.
# Higher priority sources are tried first. If a source fails or returns
# no data, the plugin automatically falls back to the next source.
#
# Available source IDs (use these exact names):
#   sec_edgar         — SEC EDGAR public filings API (free; requires User-Agent)
#   serpapi           — SerpApi search (requires SERPAPI_KEY in config.local.md)
#   bloomberg         — Bloomberg Terminal API (requires BLOOMBERG_KEY)
#   refinitiv         — Refinitiv / LSEG Eikon API (requires REFINITIV_KEY)
#   factset           — FactSet API (requires FACTSET_KEY + FACTSET_USER)
#   sp_capital_iq     — S&P Capital IQ (requires SP_CAPITAL_IQ_KEY)
#   pitchbook         — PitchBook (private companies; requires PITCHBOOK_KEY)
#   stock_analysis    — stockanalysis.com (free; public companies)
#   macrotrends       — macrotrends.net (free; historical data)
#   discoverci        — discoverci.com (free; company intelligence)
#   internal_db       — Your organisation's internal financial database
#   internal_ratings  — Your organisation's internal credit rating system
#   sharepoint        — SharePoint document library (requires SHAREPOINT config)
#   box               — Box.com (requires BOX_KEY)
#   google_drive      — Google Drive (requires GOOGLE_DRIVE_KEY)
#   upload            — User-uploaded documents (always available; no config needed)

FINANCIAL_DATA_PRIORITY=sec_edgar,bloomberg,refinitiv,factset,sp_capital_iq,stock_analysis,macrotrends,serpapi
RATINGS_DATA_PRIORITY=bloomberg,refinitiv,sp_capital_iq,serpapi
INDUSTRY_DATA_PRIORITY=bloomberg,refinitiv,factset,sp_capital_iq,serpapi
NEWS_DATA_PRIORITY=bloomberg,serpapi
PRIVATE_CO_PRIORITY=upload,pitchbook,sp_capital_iq,internal_db,serpapi


# ═══════════════════════════════════════════════════════════════════
# SECTION 2 — PREMIUM DATA PROVIDERS
# ═══════════════════════════════════════════════════════════════════
# Uncomment and configure the providers you have subscriptions for.
# Add the corresponding API keys to config.local.md (NOT here).

## Bloomberg Terminal API
# BLOOMBERG_ENABLED=true
# BLOOMBERG_KEY_NAME=BLOOMBERG_KEY
# Bloomberg unlocks: real-time prices, full financials, ratings, news, M&A data
# API docs: https://www.bloomberg.com/professional/support/api-library/

## Refinitiv / LSEG Eikon
# REFINITIV_ENABLED=true
# REFINITIV_KEY_NAME=REFINITIV_KEY
# Refinitiv unlocks: financial statements, estimates, credit data, news feeds
# API docs: https://developers.refinitiv.com/

## FactSet
# FACTSET_ENABLED=true
# FACTSET_KEY_NAME=FACTSET_KEY
# FACTSET_USER_NAME=FACTSET_USER
# FactSet unlocks: standardized financials, estimates, ownership data
# API docs: https://developer.factset.com/

## S&P Capital IQ
# SP_CAPITAL_IQ_ENABLED=true
# SP_CAPITAL_IQ_KEY_NAME=SP_CAPITAL_IQ_KEY
# Capital IQ unlocks: private company data, M&A comps, credit scores
# API docs: https://developer.spglobal.com/

## PitchBook (private companies)
# PITCHBOOK_ENABLED=true
# PITCHBOOK_KEY_NAME=PITCHBOOK_KEY
# PitchBook unlocks: private company financials, VC/PE deal data
# API docs: https://docs.pitchbook.com/


# ═══════════════════════════════════════════════════════════════════
# SECTION 3 — INTERNAL DATABASE / API
# ═══════════════════════════════════════════════════════════════════
# Connect your organisation's own financial database or internal API.
# The plugin will query this FIRST (highest priority) for any company
# that exists in your internal system.

## Internal Financial Database
# INTERNAL_DB_ENABLED=true
# INTERNAL_DB_TYPE=rest_api                # Options: rest_api, sql, mcp
# INTERNAL_DB_ENDPOINT=https://your-internal-api.yourcompany.com/financials
# INTERNAL_DB_KEY_NAME=INTERNAL_DB_API_KEY # Key stored in config.local.md
#
# If using an MCP connector instead:
# INTERNAL_DB_TYPE=mcp
# INTERNAL_DB_MCP_SERVER=your-mcp-server-name
#
# What the plugin expects from your internal API (JSON format):
#   {
#     "company_id": "...",
#     "fiscal_years": [{"year": 2024, "revenue": ..., "ebitda": ...}],
#     "existing_facilities": [{"type": "...", "amount": ..., "maturity": "..."}]
#   }

## Internal Relationship / CRM Data (e.g. Salesforce)
# CRM_ENABLED=true
# CRM_TYPE=salesforce                      # Options: salesforce, dynamics, hubspot, mcp
# CRM_MCP_SERVER=salesforce-mcp            # MCP server name if using MCP connector
# Enables: relationship history, existing facilities, account officer notes


# ═══════════════════════════════════════════════════════════════════
# SECTION 4 — INTERNAL CREDIT RATING SYSTEM
# ═══════════════════════════════════════════════════════════════════
# If your organisation has its own credit rating system, configure it here.
# The plugin will pull the internal rating and display it alongside
# Moody's / S&P / Fitch ratings in the output.

## Internal Rating API
# INTERNAL_RATINGS_ENABLED=true
# INTERNAL_RATINGS_TYPE=rest_api           # Options: rest_api, lookup_table, mcp
# INTERNAL_RATINGS_ENDPOINT=https://your-ratings-api.yourcompany.com/ratings
# INTERNAL_RATINGS_KEY_NAME=INTERNAL_RATINGS_KEY

## Static Lookup Table (for smaller organisations without a ratings API)
# Use this if you rate borrowers manually and store ratings in a file.
# Create a file at config/internal-ratings.csv with columns:
#   company_name, internal_rating, rating_date, analyst, rationale
# INTERNAL_RATINGS_TYPE=lookup_table
# INTERNAL_RATINGS_FILE=config/internal-ratings.csv

## Rating Scale Definition (required if using internal ratings)
# INTERNAL_RATING_SCALE=AAA,AA+,AA,AA-,A+,A,A-,BBB+,BBB,BBB-,BB+,BB,BB-,B,CCC,D
# INTERNAL_RATING_PASSING_THRESHOLD=BBB-   # Ratings at or above this = investment grade


# ═══════════════════════════════════════════════════════════════════
# SECTION 5 — DOCUMENT MANAGEMENT (PRIVATE COMPANY UPLOADS)
# ═══════════════════════════════════════════════════════════════════
# For private companies, the plugin can fetch documents directly from
# your document management system instead of requiring manual upload.

## SharePoint
# SHAREPOINT_ENABLED=true
# SHAREPOINT_TENANT=yourcompany.sharepoint.com
# SHAREPOINT_SITE=CreditTeam
# SHAREPOINT_LIBRARY=BorrowerDocuments
# SHAREPOINT_KEY_NAME=SHAREPOINT_CLIENT_SECRET
# MCP connector (if available): connect Microsoft SharePoint via MCP registry

## Box
# BOX_ENABLED=true
# BOX_KEY_NAME=BOX_API_KEY
# BOX_FOLDER_ID=your-folder-id

## Google Drive
# GOOGLE_DRIVE_ENABLED=true
# GOOGLE_DRIVE_KEY_NAME=GOOGLE_DRIVE_KEY
# GOOGLE_DRIVE_FOLDER_ID=your-folder-id


# ═══════════════════════════════════════════════════════════════════
# SECTION 6 — DATA FRESHNESS POLICY
# ═══════════════════════════════════════════════════════════════════
# Override default freshness thresholds if your organisation has
# different data quality standards.

## Maximum data age before stale warning (in days)
# FRESHNESS_QUARTERLY_FINANCIALS_DAYS=180   # Default: 180 (6 months)
# FRESHNESS_ANNUAL_FINANCIALS_DAYS=548      # Default: 548 (18 months)
# FRESHNESS_CREDIT_RATINGS_DAYS=365         # Default: 365 (12 months)
# FRESHNESS_INDUSTRY_DATA_DAYS=730          # Default: 730 (24 months)
# FRESHNESS_NEWS_MINIMUM_WINDOW_DAYS=30     # Default: 30 (must cover last 30 days)

## Block generation if data is too stale (vs. just warn)
# FRESHNESS_BLOCK_ON_STALE=false            # Default: false (warn only)


# ═══════════════════════════════════════════════════════════════════
# SECTION 7 — OUTPUT & BRANDING
# ═══════════════════════════════════════════════════════════════════
# Customise the output documents with your organisation's branding.

# ORGANISATION_NAME=Acme Capital Partners
# ORGANISATION_LOGO=config/logo.png         # PNG, max 300×100px recommended
# DOCUMENT_FOOTER_TEXT=Prepared by Acme Capital Partners Credit Team
# CONFIDENTIAL_LABEL=STRICTLY CONFIDENTIAL  # Default: CONFIDENTIAL — FOR INTERNAL USE ONLY
# WATERMARK_TEXT=CONFIDENTIAL               # Default: CONFIDENTIAL
# PRIMARY_COLOR=#1F3864                     # Default: Navy (#1F3864)
# ACCENT_COLOR=#2E75B6                      # Default: Blue (#2E75B6)
