# Company Research Function-Level Regression Suite

This document records the regression checks required for each function.

## Function 1: Runtime context sync

- workspace files exist
- runtime docs exist
- agent bootstrap file exists

## Function 2: Chinese report template

- all 9 approved sections exist in order
- template includes cautious-style guidance
- no default rating/target-price section exists
- template references example-report-excerpt.md for format demonstrations

## Function 3: Source hierarchy and citation rules

- 5-tier source hierarchy exists
- conflict-resolution order exists
- news-only core conclusion is prohibited

## Function 4: Sector KPI checklist support

- first two sector checklist files exist (consumer, saas)
- AI platform sector checklist exists (sector-kpis-ai-platform.md)
- each checklist contains business questions, KPIs, and risks
- AI platform checklist includes: MAU/DAU, ARPU, retention, API volume, training/inference cost, benchmark scores, burn rate, runway

## Function 5: Degraded mode behavior

- Level A/B/C modes exist
- prohibited degraded-mode outputs are listed
- missing-data disclosure is required
- section-level degradation table exists for Class A (comps, financials, revenue breakdown, scenario, KPI)
- each section-level trigger has specific affected section and degradation note text
- rule: sections must never be silently omitted — degraded with note is always preferred

## Function 6: Feishu delivery contract

- success/degraded/clarification response types exist
- message template exists
- artifact priority is defined
- Feishu Doc is the primary user-facing artifact for successful report delivery
- local path alone is explicitly insufficient for successful delivery

## Function 7: Launch provider selection

- provider matrix exists
- filings/profile/transcript/citation/export stack is fixed

## Function 8: Evidence collection contract

- mandatory evidence list exists
- drafting block conditions exist
- degraded-mode conditions exist
- Class A requires: 2+ fiscal years financials, revenue breakdown, 2+ operating KPIs, 3+ comparable companies
- each new Class A requirement has explicit degraded trigger (Level B / section-level note)
- initiating coverage "Additional Requirements" section lists all upgraded minimums

## Function 8A: Recency and authority gate

- authority ranking exists
- latest official period/date check is required
- stale evidence cannot silently pass as current analysis
- high-value retrieval prompting rule exists

## Function 9: Request classification

- initiation/update/general analysis/clarification classes exist
- priority rules exist
- Class A lists mandatory analytical structures (financial table, comps table, scenario table, risk matrix, counter-evidence, inline citations ≥10, front page snapshot)
- Class A includes degradation rule: structures must appear with data-gap notes, not be omitted

## Function 10: Report generation workflow

- required ordered workflow exists
- front-page-first drafting is prohibited
- recency and authority gate appears before evidence-based drafting
- Step 4.5 (Analysis Kit Construction) exists between Step 4 (Fact Pack) and Step 5 (Investment View Pack)
- Step 4.5 defines 4 mandatory outputs: financial table pre-fill, comparable screening, risk layering, scenario assumptions
- Step 4.5 has a gate: Kit incomplete → must not enter Body Draft
- Step 6 (Body Draft) explicitly requires basing on Analysis Kit, not ad hoc generation

## Function 11: Output contract

- full/degraded/clarification output types exist
- prohibited default rating/target-price output is blocked
- successful report output requires a Feishu Doc URL
- Class A analytical structure requirements exist (financial table, comps table, scenario table, risk matrix, counter-evidence, inline citations ≥10, front page snapshot)
- Class B simplified requirements exist (financial table required, comps/scenario optional, inline citations ≥5)
- Class C/D minimal requirements exist (financial table recommended, inline citations ≥3)
- degradation rules require structures to appear with explicit data-gap notes, not silent omission

## Function 12: OpenClaw company-research agent creation

- runtime agent exists in config
- runtime agent workspace path exists

## Function 13: Feishu routing

- company-research binding exists for Feishu default account
- binding survives gateway restart

## Function 14: Report artifact return path

- `reports/` directory exists
- runtime instructions require local markdown archival output
- runtime instructions require Feishu Doc delivery for successful report runs
- runtime instructions require document URL in reply

## Function 15: Compliance checklist

- checklist exists
- prohibited-output and source checks exist
- citation density section exists with per-class thresholds (A≥10, B≥5, C/D≥3)
- financial table source column completeness check exists
- comps data source attribution check exists
- 2 new fail conditions: Class A citations<5 hard floor, financial table source blanks without N/A

## Function 16: Quality checklist

- checklist exists
- completeness, tone, and artifact checks exist
- Class A analytical depth checks exist: financial table (2yr, 7rows, YoY), valuation (comps≥3, scenarios, degradation), risk (layered, counter-evidence), citations (per-number + ≥10 total), front page (snapshot, B/B/B summary, top risk)
- Class B simplified depth checks exist (financial table, citations≥5, risk present)
- 6 explicit Class A fail conditions defined (no financial table, no B/B/B without explanation, >3 unsourced claims, no comps without explanation, risk not layered, citations<5)

## Function 17: Regression suite itself

- this file exists
- all completed functions are enumerated

## Function 18: End-to-end report generation

- at least one successful report run
- at least one degraded-mode run
- artifact file generated
- successful report delivery returns an openable Feishu Doc URL
- compliance and quality gates checked
- user-visible transcript contains no internal process chatter

## Function 19: Model layering strategy

- model strategy document exists
- every workflow step has a model tier recommendation
- 3 model tiers defined (Standard, Reasoning, Strong writing)
- Step 4.5 and Step 6 are identified as highest-priority for model quality investment

## Quality Regression Cases

These cases verify the quality upgrade changes are effective in generated reports.
Each case has a concrete check method that can be applied to any generated report markdown.

---

### Tier 0: Agent Context Verification (must pass before checking report content)

#### Case Q0-1: Workspace documents read

- Trigger: any report generation session
- Check method: examine session log for file read events
- Pass: session log shows reads of at least: chinese-report-template.md, company-research-workflow.md, company-research-evidence-contract.md, company-research-output-contract.md
- Fail: any of these files not read → agent is not loading upgraded workspace. **Stop here — report quality checks are meaningless if agent didn't read the rules.**
- Known failure mode (2026-03-11 泡泡玛特): zero workspace documents were followed, report matched pre-upgrade quality

#### Case Q0-2: Correct agent routing

- Trigger: any Feishu-initiated report request
- Check method: examine `<runtime_state_root>/agents/company-research/sessions/sessions.json` for the session entry
- Pass: session key contains `agent:company-research:feishu:direct:*`
- Fail: session routed to `default` or another agent → report won't follow company-research rules

---

### Tier 1: Structural Checks (apply to generated report markdown)

#### Case Q1: Financial table exists (Class A)

- Input: Class A initiating coverage report
- Check method: `grep -c '|' §5` — count markdown table rows in financial section
- Pass: §5 contains a markdown table with ≥7 data rows, ≥2 year columns, a "来源" column
- Fail: no markdown table in §5, or table has <5 rows

#### Case Q1-B: Financial table exists (Class B)

- Input: Class B company update report
- Check method: same as Q1 but relaxed
- Pass: §5 contains a markdown table with ≥3 data rows, ≥1 period column, a "来源" column
- Fail: no markdown table in §5 at all
- Known failure (2026-03-11 泡泡玛特 Class B): zero tables in entire report. Financial data scattered as prose ("毛利率：约60%")

#### Case Q2: Valuation framework (Class A)

- Input: Class A initiating coverage report
- Pass: §7.5 contains 可比公司表 (≥3 companies) and 情景分析表 (Bull/Base/Bear), or degradation notes
- Fail: both tables missing without explanation

#### Case Q3: Risk layering

- Input: any report type
- Check method: search §8 for markdown table with "严重性" or "高/中/低" column
- Pass: risk matrix table exists with severity classification
- Fail: risks are a flat bullet list without severity/probability classification
- Known failure (2026-03-11 泡泡玛特): 7 risks listed as equal-weight bullets, no layering, no transmission mechanism

#### Case Q4: Inline citation density (Class A)

- Input: Class A initiating coverage report
- Check method: `grep -c '（来源：' report.md`
- Pass: count ≥ 10
- Fail: count < 5

#### Case Q4-B: Inline citation density (Class B)

- Input: Class B company update report
- Check method: same grep
- Pass: count ≥ 5
- Fail: count < 3
- Known failure (2026-03-11 泡泡玛特 Class B): count = 0. Zero inline citations in entire report.

#### Case Q5: Bull/Base/Bear degradation path

- Input: report where quantitative data is insufficient
- Pass: §7.5 section exists with explicit "数据不足" note
- Fail: §7.5 section completely absent

---

### Tier 2: Data Integrity Checks (detect hallucination and vagueness)

#### Case Q6: No vague approximations as financial data

- Input: any report type
- Check method: count occurrences of "约XX%", "大约", "估计约", "近XX" in §5 financial section
- Pass: every financial number in §5 table has an exact figure (not "约") and a source citation
- Fail: ≥3 financial figures use "约" without source → likely LLM hallucination
- Known failure (2026-03-11 泡泡玛特): "毛利率：约60%""净利率：约15%""海外收入占比：约30%" — all "约", all unsourced, all likely fabricated

#### Case Q7: Data source specificity

- Input: any report type
- Check method: examine §9 数据来源与口径说明
- Pass: §9 lists specific document names with dates/pages (e.g., "泡泡玛特 2025 年中期报告 p.23")
- Fail: §9 only lists generic categories ("公司财报""行业研究报告""新闻媒体报道")
- Known failure (2026-03-11 泡泡玛特): §9 listed 5 generic categories, zero specific documents

#### Case Q8: Financial data period explicit

- Input: any report type
- Check method: search for explicit fiscal period references ("FY2024", "2025H1", "2025Q3")
- Pass: report explicitly states which fiscal period each data point refers to
- Fail: financial data presented without clear period (e.g., "营收增长率：同比+25%" — which period?)
- Known failure (2026-03-11 泡泡玛特): "+25%" with no period specified, "约50亿港元" with no date

---

### Tier 3: Report Type Compliance

#### Case Q9: Class B focuses on incremental change

- Input: Class B company update report
- Check method: compare word count of §2 公司基本面概览 vs §6 当前变化与驱动因素
- Pass: §6 (changes/drivers) is the longest section; §2 (company overview) is brief or references prior report
- Fail: §2 is as long or longer than §6 → report is a full company profile, not an update
- Known failure (2026-03-11 泡泡玛特 Class B): wrote full company overview (founding year, headquarters, channel count) as if it were Class A. §6 was generic, not based on any specific recent event or earnings release.

#### Case Q10: Report does not contain common-knowledge padding

- Input: any report type
- Check method: search for generic industry descriptions that add no analytical value
- Red flags: "Z世代消费崛起""IP经济繁荣""消费升级""线上线下融合" without company-specific data
- Pass: industry commentary is tied to specific data points about the target company
- Fail: ≥3 paragraphs of generic industry narrative without company-specific evidence
- Known failure (2026-03-11 泡泡玛特): §3 行业与市场环境 was entirely generic ("全球潮流玩具市场规模2025年预计达到350亿美元" — unsourced, adds no analytical value)

---

### Tier 4: Delivery Checks

#### Case Q11: Feishu Doc delivery (not inline message)

- Input: any successful report
- Check method: examine Feishu message sent to user
- Pass: user receives a Feishu Doc URL with full report body
- Fail: report delivered as inline Feishu message text (not a doc)
- Known failure (2026-03-11 泡泡玛特): entire report dumped as Feishu chat message, no Feishu Doc created

#### Case Q12: Report saved to workspace

- Input: any successful report
- Check method: `ls reports/` in workspace
- Pass: `reports/{company}_{report_type}_{YYYYMMDD}.md` file exists
- Fail: no file in reports/ directory

## Live Regression Record

### 2026-03-11: Feishu Doc delivery (partial pass)

- focused Feishu Doc creation test succeeded
- existing Apple full report was written into a Feishu Doc (`<redacted_feishu_doc_url>`)
- the Feishu Doc link was sent to the target user through the default Feishu account
- known gap: standard Apple analysis request may still return old summary + local path instead of Feishu Doc URL

### 2026-03-11: 泡泡玛特 Class B company update (FULL FAIL)

Request: "帮我写一份泡泡玛特的公司更新"
Result: Report delivered as inline Feishu message, not Feishu Doc.

| Case | Result | Detail |
|------|--------|--------|
| Q0-1 Workspace docs read | **FAIL (suspected)** | Report shows zero evidence of following upgraded templates/rules |
| Q0-2 Agent routing | **UNVERIFIED** | Need to check session log to confirm routing |
| Q1-B Financial table (Class B) | **FAIL** | Zero markdown tables in entire report |
| Q3 Risk layering | **FAIL** | 7 risks as flat bullet list, no severity classification |
| Q4-B Citations (Class B ≥5) | **FAIL** | 0 inline citations (target: ≥5) |
| Q6 No vague approximations | **FAIL** | "约60%""约15%""约30%" — all unsourced |
| Q7 Data source specificity | **FAIL** | §9 lists only generic categories |
| Q8 Financial period explicit | **FAIL** | "+25% YoY" without specifying which period |
| Q9 Class B incremental focus | **FAIL** | Wrote full company profile instead of update |
| Q10 No common-knowledge padding | **FAIL** | Multiple paragraphs of generic industry narrative |
| Q11 Feishu Doc delivery | **FAIL** | Dumped as inline message |
| Q12 Report saved to workspace | **UNVERIFIED** | Need to check reports/ directory |

**Root cause hypothesis**: Agent did not read upgraded workspace documents. Either (a) session was routed to wrong agent, (b) BOOTSTRAP.md → AGENTS.md reading chain was not followed, or (c) model ignored the workspace instructions. Must verify Q0-1 and Q0-2 before further quality tuning.

### 2026-03-11: 泡泡玛特 Class B (Phase 5.2 retest after 5.1 fix)

Request: "帮我写一份泡泡玛特的公司更新"（session 重置后干净 session）
Result: 报告保存至 workspace，但结构性质量仍未达标。

**改善**：模型执行了 4×web_search + 1×web_fetch + 1×write + 3×feishu_doc（之前为 0 tool call）。数据真实，有具体数字和明确财报期间。

| Case | Result | Detail |
|------|--------|--------|
| Q0-1 Workspace docs read | **可能通过** | 有真实数据和具体财报期间 |
| Q1-B Financial table (Class B) | **FAIL** | 0 个 markdown 表格，财务数据散在正文 |
| Q3 Risk layering | **FAIL** | 5 条风险平级 bullet，无严重性分类 |
| Q4-B Citations (Class B ≥5) | **FAIL** | 0 条（来源：）格式行内引用 |
| Q6 No vague approximations | **改善** | 用了具体数字（138.76亿、204.4%），不再"约XX%" |
| Q7 Data source specificity | **改善** | §9 列出了"泡泡玛特2025年半年度报告" |
| Q8 Financial period explicit | **改善** | 明确标注"2025年上半年" |
| Q9 Class B incremental focus | **FAIL** | 写了完整公司概况（2010年成立、上市历史） |
| Q10 No common-knowledge padding | **FAIL** | §3 有"IP消费崛起""全球化布局"等泛泛描述 |
| Q12 Report saved to workspace | **PASS** | 泡泡玛特_公司研究报告_20260311.md 已存在 |

**结论**：5.1 修复解决了数据来源问题，但 qwen3-max 无法遵守结构性格式规则。决定执行 Phase 5.3（切换为 Claude Sonnet 4）。

### Function 18 status

- Feishu Doc delivery: partially validated (works when explicitly instructed, fails on automatic path)
- 数据来源质量: **已改善**（5.1 修复后不再凭空捏造）
- 结构性质量: **未通过**（qwen3-max 无法生成表格/引用/风险矩阵）
- Next step: Phase 5.3 — 切换 company-research agent 主模型为 Claude Sonnet 4
