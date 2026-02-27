# Signal Engine (Crypto)

## When to use
Trigger when the user asks for: signal, buy/sell decision, edge, confidence, RSI/MACD/ATR-based trade idea, or "what should I do with BTC/ETH".

## Objective
Produce a standardized, auditable signal summary for a given symbol/timeframe:
- market snapshot
- indicator state
- model edge + confidence (if available)
- final signal score (0-100)
- trade intent + risk notes

## Workflow
1) Confirm inputs: symbol, timeframe, and (optional) risk profile.
2) Market snapshot: last price, 24h change, volatility proxy.
3) Indicator read: RSI, MACD, trend proxy (MA/EMA), ATR risk context.
4) Edge + confidence: include the model forecast delta vs spot and a confidence score if the user provides/has a model.
5) Score: combine indicator direction + edge + confidence - risk penalty.
6) Output: provide a strict sectioned report with a final BUY/SELL/HOLD + rationale and risk controls.

## Output format (must follow)
### 1) Inputs
### 2) Market Snapshot
### 3) Indicators
### 4) Edge + Confidence
### 5) Signal Score (0-100) + Rationale
### 6) Trade Intent (BUY/SELL/HOLD) + Risk Notes