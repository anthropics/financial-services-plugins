# Company Research Model Layering Strategy

This document defines the recommended model allocation for each workflow step.

## Principle

Different workflow steps have different cognitive demands. Allocate model capability where it matters most (analytical reasoning, structured writing), and use cost-efficient models for mechanical tasks (retrieval, classification, checklist comparison).

## Model Allocation by Workflow Step

| Step | Task | Cognitive demand | Recommended model tier | Notes |
|------|------|-----------------|----------------------|-------|
| 1 | Request classification | Low (pattern matching) | Standard | Qwen3-Max or equivalent |
| 2 | Recency and authority gate | Low (date/source comparison) | Standard | Qwen3-Max or equivalent |
| 3 | Evidence collection | Medium (tool calling accuracy) | Standard | Tool calling reliability is key; Qwen3-Max or Kimi K2.5 |
| 4 | Fact Pack | Low (structured extraction) | Standard | Qwen3-Max or equivalent |
| 4.5 | Analysis Kit Construction | **High** (financial reasoning, peer selection, risk analysis) | **Reasoning** | DeepSeek-R1 or Kimi K2.5 thinking mode. This step requires financial modeling logic and multi-factor comparison |
| 5 | Investment View Pack | High (judgment synthesis) | Reasoning or Strong writing | Based on Analysis Kit, needs analytical coherence |
| 6 | Body Draft | **High** (structured writing under constraints) | **Strong writing** | Must follow template structure precisely while maintaining quality prose. Needs long-context capability |
| 7 | Front Page Summary | Medium (distillation) | Strong writing | Extract key points from body, maintain Goldman-style format |
| 8 | Verification | Low (checklist comparison) | Standard | Mechanical checklist evaluation |
| 9 | Delivery preparation | Low (API calling) | Standard | Feishu Doc creation is tool-based |

## Model Tier Definitions

| Tier | Characteristics | Current options in staging |
|------|----------------|----------------------|
| Standard | Good tool calling, cost-efficient, fast | Qwen3-Max (DashScope) |
| Reasoning | Strong logical reasoning, thinking mode | DeepSeek-R1 (Volcengine), Kimi K2.5 thinking |
| Strong writing | High quality prose, long context, structure adherence | Kimi K2.5, GLM-4.7 (Volcengine) |

## Cost Optimization Notes

- Steps 1-4 and 8-9 are high-frequency, low-complexity — use the cheapest reliable model
- Step 4.5 is the highest-value reasoning step — invest in model quality here
- Step 6 requires the longest output — consider models with favorable output token pricing
- If budget is constrained, prioritize upgrading Step 4.5 and Step 6 first

## Implementation Notes

- Model selection is configured via `models.json` in the agent runtime
- Current runtime uses a single model for all steps
- Multi-model routing requires OpenClaw's per-step model override capability (verify availability before implementing)
- If per-step override is not available, use the strongest available model for all steps as the default
