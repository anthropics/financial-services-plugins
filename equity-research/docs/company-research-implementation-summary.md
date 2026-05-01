# Company Research Implementation Summary

This summary collects the paths, runtime artifacts, and documentation that describe the current `company-research` agent in the target runtime.

## Runtime paths

- Agent bootstrap: `<agent_runtime_root>/BOOTSTRAP.md`
- Workspace docs: `<workspace_root>/equity-research/docs/*`
- Report writer helper: `<workspace_root>/scripts/write_report_to_feishu_doc.py`
- Report folder: `<workspace_root>/reports`

## Key documents (repo)

1. `company-research-report-agent-handoff.md`: bot binding notes, redacted live-delivery facts, delivery caveats.
2. `company-research-report-agent-implementation-plan.md`: Function inventory, gating status, verified delivery facts.
3. `company-research-message-gating.md`: Allowed user message types, banned process chatter.
4. `company-research-recency-authority-gate.md`: Authority order, recency checks, high-value retrieval prompt.
5. `company-research-feishu-delivery.md`: Feishu doc delivery sequence and body verification.
6. `company-research-workflow.md`: Updated workflow order (classification → recency gate → evidence → body → verification → delivery).
7. `company-research-regression-suite.md`: Per-function regression requirements plus user-visible transcript expectations.

## Execution pipeline

1. **Classification (A/B/C/D)** – determines template and downstream requirements.
2. **Recency/Authority gate** – high-value retrieval prompt, latest official disclosure check, downgrade rules.
3. **Evidence/Fact Pack** – gather structured sources; respond with data inventory.
4. **Body & Summary** – nine-section Chinese template + valuations/scenarios; apply message gating for final response only.
5. **Delivery** – run `scripts/write_report_to_feishu_doc.py`, verify `verified_block_count > 0`, then send final message with Feishu link.

## Support files

- `AGENTS.md`: enumerates reading order.
- `company-research-request-classification.md`: defines Class A/B/C/D behaviors.
- `company-research-evidence-contract.md`: mandatory evidence thresholds.
- `company-research-output-contract.md`: output structure requirements.
- `company-research-source-hierarchy.md`: source priority.

## Next steps

- Continue to rerun `openclaw sessions cleanup` if old context leaks.
- Use the CLI to regenerate a test document as needed for verification; do not commit live document URLs.
