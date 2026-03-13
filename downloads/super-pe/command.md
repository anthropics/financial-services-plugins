---
description: Full PE deal lifecycle — sourcing, screening, diligence, IC memo, returns, unit economics, portfolio monitoring, and value creation
argument-hint: "[stage, company name, or 'full process']"
---

Load the `super-pe` skill for end-to-end private equity workflows.

If a specific stage is mentioned (e.g., "source deals in healthcare", "screen this CIM", "prep for management meeting", "write IC memo", "model returns", "analyze unit economics", "check portfolio performance", "build value creation plan"), focus on that stage.

If the user says "full process" or "end to end," run the Deal Context intake first, then proceed through stages in order, carrying data forward between stages.

If a company or deal is provided without a specific stage, ask which stage(s) to run.

If no context is provided, present the available stages and ask where to start.

Always check for deal context before executing any stage. If context was gathered in a prior stage, reuse it — do not re-ask.
