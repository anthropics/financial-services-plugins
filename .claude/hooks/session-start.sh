#!/bin/bash
set -euo pipefail

# Only run in remote (web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Install Python dependencies for DCF model and other financial analysis scripts
pip install -r "${CLAUDE_PROJECT_DIR}/financial-analysis/skills/dcf-model/requirements.txt" --quiet
