# HGEN Council — Investment Debate

description: Run a structured debate between 10 legendary investors (Buffett, Soros, Dalio, Lynch, Graham, Burry, Munger, Livermore, Templeton, Druckenmiller) on any stock or investment opportunity. Each investor presents bull and bear cases from their unique philosophy, then votes. Produces a majority-vote verdict with conviction score. Triggers on "debate [TICKER]", "HGEN [TICKER]", "what would Buffett think about", "investment council", "10 investors", or "expert debate".

## Workflow

### Step 1: Parse the Investment Opportunity

Summarize the investment thesis in 1-2 sentences:
- Ticker or asset name
- Current price and recent context
- User's initial thesis (if provided)

### Step 2: Run the 10-Investor Debate

For each investor, present in sequence:
- **BULL CASE**: Why they would buy (3 specific reasons aligned with their philosophy)
- **BEAR CASE**: Why they would not buy or would sell (2 specific risks)
- **VERDICT**: STRONG BUY (+2), BUY (+1), HOLD (0), SELL (-1), STRONG SELL (-2)
- **QUOTE**: One sentence summary of their take

The 10 investors and their focus:
1. Warren Buffett — moat, management quality, intrinsic value
2. George Soros — reflexivity, macro feedback loops, inflection points
3. Ray Dalio — risk parity, portfolio stress tests, all-weather resilience
4. Peter Lynch — growth at reasonable price, business understandability
5. Benjamin Graham — margin of safety, statistical intrinsic value
6. Michael Burry — contrarian mismatch, asymmetric payoffs
7. Charlie Munger — mental models, incentive alignment, business quality
8. Jesse Livermore — price action, trend momentum, volume confirmation
9. John Templeton — maximum pessimism, geographic diversification
10. Stanley Druckenmiller — macro overlay, currency tailwinds, trend transitions

### Step 3: Consensus Analysis

- Total vote tally (e.g., +8 out of +20 possible)
- Consensus: STRONG BUY / BUY / HOLD / SELL / STRONG SELL
- Key agreements and disagreements between investors
- Critical question for the user to answer themselves

### Step 4: Final Recommendation

- **RECOMMENDATION**: BUY / HOLD / SELL
- **Conviction Level**: HIGH / MEDIUM / LOW
- Best case (if bulls are right): outcome, timeline, upside
- Worst case (if bears are right): outcome, timeline, downside
- Action plan for both scenarios
- Watch list criteria: signals that would flip the verdict

## Output Format

```
INVESTMENT DEBATE: [TICKER] @ $[PRICE]
══════════════════════════════════════════════════

THESIS: [1-2 sentence summary]

─────────────────────────────────────────────────

INVESTOR 1: WARREN BUFFETT
Bullish: [3 bullet points]
Bearish: [2 bullet points]
Verdict: [STRONG BUY / BUY / HOLD / SELL / STRONG SELL]
Vote: [+2 / +1 / 0 / -1 / -2]
"[1 sentence quote in Buffett's voice]"

[...repeat for investors 2-10...]

─────────────────────────────────────────────────

CONSENSUS VOTE: [total]/20
Final: [STRONG BUY / BUY / HOLD / SELL / STRONG SELL]
Highest conviction bull: [name]
Biggest bear: [name]
Key disagreement: [what they disagree on]
Critical question: "[the one question you must answer]"

─────────────────────────────────────────────────

RECOMMENDATION: [BUY / HOLD / SELL] | Conviction: [HIGH/MED/LOW]
Best case: [outcome if bulls right]
Worst case: [outcome if bears right]
Watch: [signal that flips verdict]
```
