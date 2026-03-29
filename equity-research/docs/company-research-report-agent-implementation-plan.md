# Company Research Report Agent Implementation Plan

This document is the execution plan for delivering the company research report agent from zero to production rollout.

It is written for AI-assisted implementation. Each phase is decomposed into small work packages with:

- objective
- inputs
- file targets
- outputs
- dependencies
- validation
- completion criteria

The goal is not "code written". The goal is "development complete with compliance and test evidence".

## Governing Delivery Model

This project must **not** be delivered through a "minimal closed loop first" strategy.

It must be delivered **function by function**.

For every function:

1. define the function boundary
2. define the regression test set for that function
3. implement only that function
4. run the function's regression tests
5. mark the function complete only if its regression tests pass
6. then move to the next function

Do not bundle multiple unfinished functions into one large integration push.
Do not claim progress from partial end-to-end behavior if the current function has not passed regression.

## Delivery Goal

Deliver a production-usable agent that allows a user to send a company-analysis request through Feishu and receive a company research report first draft generated through OpenClaw.

The report must:

- follow the approved Chinese institutional structure
- use the approved source-priority rules
- avoid formal rating and target-price output by default
- include source and scope disclosure
- pass defined quality and compliance checks

## Current Runtime Status

As of 2026-03-11, the target staging environment has reached an important intermediate state:

- company-research routing from Feishu works
- the default Feishu account is already routed to `company-research`
- local markdown report generation works
- Feishu Doc create/write works
- the existing Apple full report has been successfully written to a Feishu Doc and sent back to the user

However, the default automatic completion path is not fully converged:

- some standard analysis requests still end with the old `reports/...md` summary reply
- therefore "user can open a Feishu Doc for the report" is proven
- but "every successful standard report request automatically returns a Feishu Doc URL" is not yet proven

Future work must preserve this distinction.

## Additional Verified Delivery Facts

The following runtime facts are now verified and should not be rediscovered from scratch:

- the live Feishu bot seen by the user is the default workspace bot
- that bot corresponds to Feishu account id `default`
- `default` is already bound to `company-research` in OpenClaw bindings
- a title-only Feishu doc can still appear as a valid-looking URL if only `create` succeeds
- successful report delivery therefore requires post-write verification, not just URL return

Known documents from live validation:

- invalid/title-only doc: `<redacted_feishu_doc_url_1>`
- verified replacement doc with body: `<redacted_feishu_doc_url_2>`

## Non-Goals For V1

Do not include these in the initial release scope:

- approval workflow
- publishing workflow
- portfolio management workflow
- multi-agent orchestration beyond what is strictly required
- broad multi-market support from day one
- automated investment recommendation output

## System Boundary

V1 system path:

1. User sends a Feishu message
2. OpenClaw routes the request to the company research agent
3. Agent gathers evidence and structured inputs
4. Agent produces report draft artifacts
5. Agent returns summary plus report artifact to Feishu

## Execution Principles

All future AI agents working from this plan must follow these rules:

- keep changes minimal and local
- do not redesign the architecture before checking existing repo capabilities
- finish one function package at a time
- write or identify the verification path before implementation
- do not mark a package complete without evidence
- prefer official disclosure and structured sources over media summaries
- preserve existing plugin and OpenClaw structures unless the user explicitly changes scope
- define the regression suite for the current function before editing files
- do not start the next function until the current function passes regression

## Function Inventory

The project is broken into discrete deliverable functions. They must be completed in order.

1. Runtime context sync
2. Chinese report template
3. Source hierarchy and citation rules
4. Sector KPI checklist support
5. Degraded mode behavior
6. Feishu delivery contract
7. Launch provider selection
8. Evidence collection contract
8A. Recency and authority gate
9. Request classification
10. Report generation workflow
11. Output contract
12. OpenClaw company-research agent creation
13. Feishu routing to the research agent
14. Report artifact return path
15. Compliance checklist
16. Quality checklist
17. Function-level regression suite
18. End-to-end report generation

## Function Package Standard

Every function package must contain:

- function name
- objective
- inputs
- file targets
- outputs
- dependencies
- regression tests
- completion criteria

---

## Function 1: Runtime Context Sync

This function replaces the old "foundation stage" and is complete only when the approved planning files are readable in the runtime environment.

---

### Package 1.1: Create the implementation workspace contract

Objective:
- Establish the canonical working directories and files for the company research agent.

Inputs:
- `equity-research/docs/company-research-report-agent.md`
- `equity-research/docs/company-research-report-agent-handoff.md`
- current OpenClaw deployment structure on the target server

File targets:
- OpenClaw agent workspace files
- implementation tracker document if needed

Outputs:
- confirmed workspace path
- confirmed agent ID
- confirmed bot binding approach

Dependencies:
- none

Validation:
- inspect OpenClaw config
- inspect current agent list
- confirm where the new agent files will live

Completion criteria:
- target OpenClaw agent path is documented
- agent identifier is fixed
- binding strategy is fixed

### Package 1.2: Sync planning context into runtime workspace

Objective:
- Ensure the runtime environment contains the approved design context so future AI runs do not lose it.

Inputs:
- blueprint document
- handoff document

File targets:
- OpenClaw workspace docs
- agent bootstrap or instruction files

Outputs:
- runtime-accessible copies or references to the planning docs

Dependencies:
- Package 1.1

Validation:
- files exist in the runtime workspace
- paths are readable by the agent

Completion criteria:
- runtime workspace contains the approved context documents
- future agents can resume with no hidden assumptions

---

## Function 2: Chinese Report Template

### Package 2.1: Create the Chinese report template

Objective:
- Convert the approved report structure into a concrete reusable template.

Inputs:
- approved section order from the handoff file
- existing initiation template under `equity-research/skills/initiating-coverage/assets/`

File targets:
- new Chinese template file under `equity-research/skills/initiating-coverage/assets/`

Outputs:
- one initiation-style Chinese report template

Dependencies:
- Function 1 complete

Validation:
- template contains all approved sections
- template preserves the cautious Changsheng-style tone
- template does not include default formal rating or target price

Regression tests:
- template file can be loaded from the target path
- template contains all 9 approved sections in order
- template contains no default rating or target-price language

Completion criteria:
- template file exists
- template is referenced by the relevant skill docs
- section ordering matches the approved framework
- status: completed in repository docs, not yet wired into runtime

---

## Function 3: Source Hierarchy And Citation Rules

### Package 3.1: Create the source hierarchy and citation rules

Objective:
- Encode the approved source-priority rules into a reusable instruction file.

Inputs:
- handoff defaults for source ordering and conflict handling

File targets:
- new source hierarchy document under `equity-research/docs/` or relevant skill references

Outputs:
- source-priority rules
- conflict-resolution rules
- citation minimum requirements

Dependencies:
- Function 1 complete

Validation:
- document explicitly ranks source classes
- document defines how to handle conflicting evidence
- document bans news-only core conclusions

Regression tests:
- document contains the 5-tier source ranking
- document contains conflict-resolution order
- document contains a degraded-mode trigger reference

Completion criteria:
- rule file exists
- rule file is referenced from the report workflow docs
- status: completed in repository docs, not yet wired into runtime

---

## Function 4: Sector KPI Checklist Support

### Package 4.1: Create sector KPI checklists

Objective:
- Define the minimum sector-specific analytical lens for the first supported sectors.

Inputs:
- approved research framework
- chosen launch sectors

File targets:
- one checklist file per sector

Outputs:
- KPI checklist for each launch sector
- must-cover issues per sector

Dependencies:
- Function 2 complete

Validation:
- each checklist includes company quality, growth drivers, risks, and valuation considerations

Regression tests:
- first two sector checklist files exist
- each checklist contains business questions, KPI section, and risk section

Completion criteria:
- first two sector checklists exist
- report workflow docs reference them
- status: completed in repository docs, not yet wired into runtime

---

## Function 5: Degraded Mode Behavior

### Package 5.1: Define degraded mode behavior

Objective:
- Encode safe fallback behavior when evidence is missing or conflicting.

Inputs:
- source hierarchy rules
- approved rating boundary

File targets:
- degraded mode policy docs
- workflow references

Outputs:
- degraded-mode decision policy

Dependencies:
- Function 3 complete

Validation:
- policy defines Level A, B, and C behavior
- policy forbids unsupported strong conclusions

Regression tests:
- policy includes the required trigger list
- policy includes the required downgraded output formats

Completion criteria:
- degraded mode rules are explicit, loadable, and testable
- status: completed in repository docs, not yet wired into runtime

---

## Function 6: Feishu Delivery Contract

### Package 6.1: Define the Feishu delivery contract

Objective:
- Standardize what the agent returns to Feishu for success, degraded success, and clarification.

Inputs:
- approved output boundary
- degraded mode policy

File targets:
- delivery spec

Outputs:
- V1 delivery contract

Dependencies:
- Function 5 complete

Validation:
- delivery spec defines success, degraded, and clarification response types

Regression tests:
- delivery spec contains a V1 message template
- delivery spec defines artifact priority and naming rules

Completion criteria:
- the delivery contract is explicit and testable
- status: completed in repository docs, not yet wired into runtime

---

## Function 7: Launch Provider Selection

### Package 7.1: Select launch data providers

Objective:
- Fix the actual provider stack for V1 rather than leaving data as an abstract future dependency.

Inputs:
- approved open-source component shortlist
- market scope for V1

File targets:
- configuration docs
- integration notes

Outputs:
- chosen filing source
- chosen market/profile source
- chosen transcript source

Dependencies:
- Function 1 complete

Validation:
- each required data class has at least one provider
- provider choice aligns with launch market

Regression tests:
- provider matrix exists
- filings, profile/market data, and transcript coverage are all assigned

Completion criteria:
- V1 provider matrix is documented
- no critical evidence class is unassigned

---

## Function 8: Evidence Collection Contract

### Package 8.1: Define evidence collection contract

Objective:
- Standardize what evidence the agent must collect before drafting.

Inputs:
- provider matrix
- source hierarchy rules

File targets:
- evidence collection spec
- workflow reference doc

Outputs:
- required evidence schema for:
  - company profile
  - financial statements
  - recent disclosures
  - industry context
  - peer set

Dependencies:
- Function 7 complete

Validation:
- spec identifies mandatory vs optional evidence
- spec defines missing-data behavior

Regression tests:
- spec includes mandatory evidence list
- spec identifies drafting block conditions

Completion criteria:
- drafting cannot start without minimum evidence thresholds

---

## Function 8A: Recency And Authority Gate

### Package 8A.1: Define recency and authority rules

Objective:
- Prevent stale or low-authority evidence from being presented as current company analysis.

Inputs:
- source hierarchy rules
- latest observed stale-data failure pattern

File targets:
- `equity-research/docs/company-research-recency-authority-gate.md`
- workflow and runtime references

Outputs:
- explicit authority ranking
- latest-period/date checks
- stale-data block conditions
- high-value retrieval prompting rule

Dependencies:
- Functions 3 and 8 complete

Validation:
- rule file exists
- authority order is explicit
- latest-period/date checks are explicit
- high-value retrieval prompt instruction is present

Regression tests:
- file contains authority order
- file contains latest-period/date checks
- file contains stale-data downgrade/block behavior
- file contains the recommended high-value retrieval prompt

Completion criteria:
- recency and authority rule file exists
- workflow references the gate before drafting

---

## Function 9: Request Classification

### Package 9.1: Define request classification logic

Objective:
- Determine how incoming requests are routed to supported report modes.

Inputs:
- output scope

File targets:
- workflow references
- agent instructions

Outputs:
- request classification rules

Dependencies:
- Function 1 complete

Validation:
- supported intents are explicitly mapped

Regression tests:
- classification rules cover initiation, earnings/update, and general company analysis

Completion criteria:
- request routing rules are deterministic and documented

---

## Function 10: Report Generation Workflow

### Package 10.1: Define the report generation workflow

Objective:
- Convert the approved assembly order into an executable workflow.

Inputs:
- approved assembly order
- evidence contract
- Chinese report template

File targets:
- workflow docs
- prompt instructions

Outputs:
- report generation workflow

Dependencies:
- Functions 2, 3, 8, and 9 complete

Validation:
- workflow explicitly uses Fact Pack through Export order
- workflow requires verification before export

Regression tests:
- workflow references all required intermediate outputs
- workflow explicitly forbids front-page-first drafting

Completion criteria:
- report generation workflow is documented and testable

---

## Function 11: Output Contract

### Package 11.1: Define output contracts

Objective:
- Make outputs predictable for runtime handling and testing.

Inputs:
- workflow spec
- delivery contract

File targets:
- output schema docs

Outputs:
- summary contract
- full draft contract
- degraded note contract
- clarification contract

Dependencies:
- Functions 6 and 10 complete

Validation:
- each output defines required and forbidden sections

Regression tests:
- output contracts include all response types
- required sections can be checked deterministically

Completion criteria:
- outputs are fixed enough for regression testing

---

## Function 12: OpenClaw Company-Research Agent Creation

### Package 12.1: Create the OpenClaw company-research agent

Objective:
- Add a dedicated runtime agent for company research.

Inputs:
- OpenClaw deployment structure
- runtime context documents

File targets:
- OpenClaw agent directory
- agent bootstrap files
- workspace files

Outputs:
- dedicated runtime agent

Dependencies:
- Functions 1 through 11 complete in docs

Validation:
- agent appears in config
- workspace is readable

Regression tests:
- agent files exist in the correct path
- config points to the correct workspace and agentDir

Completion criteria:
- runtime agent exists and can be loaded

---

## Function 13: Feishu Routing To The Research Agent

### Package 13.1: Bind Feishu traffic to the research agent

Objective:
- Ensure supported Feishu traffic reaches the correct agent.

Inputs:
- current Feishu configuration
- runtime agent identity

File targets:
- OpenClaw bindings
- runtime config docs

Outputs:
- Feishu routing rule

Dependencies:
- Function 12 complete

Validation:
- routing rule exists in config

Regression tests:
- a test message path is documented
- config shows the intended agent binding

Completion criteria:
- Feishu requests can deterministically hit the research agent

---

## Function 14: Report Artifact Return Path

### Package 14.1: Define and implement the artifact return path

Objective:
- Ensure the agent can return a report artifact in the approved format.

Inputs:
- delivery spec
- output contract

File targets:
- runtime config or scripts
- artifact output docs

Outputs:
- working artifact return path

Dependencies:
- Functions 11, 12, and 13 complete

Validation:
- the artifact format matches the V1 delivery contract

Regression tests:
- artifact naming matches spec
- runtime can surface the artifact reference in the response

Completion criteria:
- report artifacts can be returned in the approved V1 mode

---

## Function 15: Compliance Checklist

### Package 15.1: Create the compliance checklist

Objective:
- Add a report-level compliance gate before a draft is complete.

Inputs:
- source rules
- rating boundary
- report template

File targets:
- compliance checklist doc

Outputs:
- compliance checklist

Dependencies:
- Functions 2, 3, 5, and 11 complete

Validation:
- checklist items are binary and testable

Regression tests:
- checklist includes prohibited-output checks
- checklist includes source disclosure checks

Completion criteria:
- compliance review can block incomplete outputs

---

## Function 16: Quality Checklist

### Package 16.1: Create the quality checklist

Objective:
- Create a separate quality gate from compliance.

Inputs:
- Chinese report template
- output contracts

File targets:
- quality checklist doc

Outputs:
- quality checklist

Dependencies:
- Functions 2 and 11 complete

Validation:
- quality checks are explicit and reviewable

Regression tests:
- checklist covers completeness, evidence, and tone

Completion criteria:
- quality review is testable and separate from compliance

---

## Function 17: Function-Level Regression Suite

### Package 17.1: Define test cases before implementation sign-off

Objective:
- Create the required regression cases for all major functions.

Inputs:
- all function contracts

File targets:
- test plan

Outputs:
- regression suite specification

Dependencies:
- Functions 1 through 16 complete

Validation:
- each function has at least one positive and one failure-path test

Regression tests:
- the test plan itself enumerates function-level regressions

Completion criteria:
- no feature proceeds to sign-off without a regression case

---

## Function 18: End-To-End Report Generation

### Package 18.1: Run end-to-end validation

Objective:
- Validate the final integrated behavior after all individual functions have passed regression.

Inputs:
- all previous functions complete

Outputs:
- E2E run evidence

Dependencies:
- Functions 1 through 17 complete

Validation:
- Feishu trigger works
- agent routes correctly
- report draft is produced
- report passes compliance and quality checks

Regression tests:
- at least one successful report run
- at least one degraded-mode run
- at least one prohibited-output regression

Completion criteria:
- integrated E2E evidence exists after all function-level regressions are complete

---

## Deprecated Stage-Based Reading

If older documents refer to "stages", interpret them through the function inventory above.

Function-by-function delivery takes precedence over any earlier stage-based sequencing.

Inputs:
- V1 output scope

File targets:
- command or workflow reference docs
- agent prompt instructions

Outputs:
- classification rules for:
  - initiating coverage
  - earnings review
  - general company analysis

Dependencies:
- Stage 2 complete

Validation:
- rules clearly map common user requests to supported output paths

Completion criteria:
- the agent has deterministic request routing for supported intents

### Package 4.2: Define the report generation workflow

Objective:
- Convert the approved assembly order into an executable workflow.

Inputs:
- approved assembly order
- evidence contract
- Chinese report template

File targets:
- agent prompt
- workflow docs
- skill references

Outputs:
- step-by-step workflow for:
  - Fact Pack
  - Investment View Pack
  - Body Draft
  - Front Page Summary
  - Verification
  - Export

Dependencies:
- Packages 2.1, 2.2, 3.2

Validation:
- workflow explicitly prevents front-page-first drafting
- workflow requires verification before export

Completion criteria:
- generation pipeline is fully documented for the agent

### Package 4.3: Define output contracts

Objective:
- Make outputs predictable for both runtime handling and testing.

Inputs:
- workflow spec

File targets:
- output schema docs
- prompt instructions

Outputs:
- report summary format
- full report draft format
- source appendix format
- error response format

Dependencies:
- Package 4.2

Validation:
- each output has required sections and forbidden sections

Completion criteria:
- runtime and tests can validate output structure deterministically

---

## Stage 5: Feishu And OpenClaw Integration Layer

### Package 5.1: Create the OpenClaw company-research agent

Objective:
- Add a dedicated runtime agent rather than relying on a general-purpose agent.

Inputs:
- OpenClaw config structure
- agent naming and binding strategy

File targets:
- OpenClaw agent directory
- agent bootstrap / identity files
- OpenClaw config

Outputs:
- dedicated `company-research` agent

Dependencies:
- Stage 1 complete

Validation:
- agent appears in OpenClaw config
- agent workspace is readable

Completion criteria:
- the runtime environment can route requests to the correct agent

### Package 5.2: Bind Feishu traffic to the research agent

Objective:
- Ensure the right Feishu requests reach the right agent.

Inputs:
- current Feishu channel configuration
- agent identity and bot strategy

File targets:
- OpenClaw channel bindings
- bot/account mapping docs

Outputs:
- routing rule from Feishu to `company-research`

Dependencies:
- Package 5.1

Validation:
- route is visible in config
- at least one message path is documented and testable

Completion criteria:
- a Feishu request can deterministically hit the research agent

### Package 5.3: Define report return path

Objective:
- Decide how artifacts are returned to the user in V1.

Inputs:
- output contracts
- Feishu limitations

File targets:
- delivery docs
- runtime prompt or integration notes

Outputs:
- V1 return mode:
  - summary in message
  - full report as markdown/docx/path/link

Dependencies:
- Package 4.3

Validation:
- delivery contract is simple enough for reliable operation

Completion criteria:
- the agent has one supported and testable delivery path

---

## Stage 6: Compliance And Quality Gate Layer

### Package 6.1: Create the compliance checklist

Objective:
- Add an explicit report-level compliance gate before a draft is considered complete.

Inputs:
- source rules
- rating boundary
- report template

File targets:
- compliance checklist doc
- workflow references

Outputs:
- checklist covering:
  - no prohibited rating / target price by default
  - source disclosure present
  - unsupported claims flagged
  - missing-data disclosure present when needed

Dependencies:
- Stage 2 and Stage 4 complete

Validation:
- checklist items are binary and testable

Completion criteria:
- report cannot be marked done without passing the checklist

### Package 6.2: Create the quality checklist

Objective:
- Separate compliance checks from content-quality checks.

Inputs:
- Chinese report template
- workflow

File targets:
- quality checklist doc

Outputs:
- checklist covering:
  - section completeness
  - evidence-backed claims
  - numeric consistency
  - language tone consistency
  - source appendix completeness

Dependencies:
- Stage 2 and Stage 4 complete

Validation:
- checklist supports human review and automated spot checks

Completion criteria:
- report quality is testable against explicit criteria

### Package 6.3: Define test cases before implementation sign-off

Objective:
- Fix the required test scenarios that prove the workflow works.

Inputs:
- output contracts
- compliance checklist
- quality checklist

File targets:
- test plan document

Outputs:
- minimum test suite with:
  - happy path
  - missing-data path
  - prohibited-output path
  - source-conflict path

Dependencies:
- Packages 6.1 and 6.2

Validation:
- each test has inputs, expected behavior, and pass/fail criteria

Completion criteria:
- implementation has a defined test gate before execution begins

---

## Stage 7: End-To-End Validation And Launch Readiness

### Package 7.1: Run end-to-end dry runs

Objective:
- Validate the complete request-to-report path.

Inputs:
- all previous stages complete
- chosen test companies and prompts

Outputs:
- run logs
- generated drafts
- validation results

Dependencies:
- Stages 1-6 complete

Validation:
- Feishu trigger works
- agent routes correctly
- report draft is produced
- report passes compliance and quality checklists

Completion criteria:
- at least one full E2E run passes

### Package 7.2: Run negative-path validation

Objective:
- Confirm the system fails safely.

Inputs:
- missing-data scenarios
- conflicting-source scenarios

Outputs:
- failure-mode results

Dependencies:
- Package 7.1

Validation:
- system does not fabricate missing information
- system explicitly discloses uncertainty
- system avoids prohibited output even under pressure

Completion criteria:
- negative-path behavior is acceptable and documented

### Package 7.3: Launch checklist

Objective:
- Confirm launch readiness with explicit gates.

Inputs:
- all validation results

Outputs:
- final readiness checklist

Dependencies:
- Packages 7.1 and 7.2

Validation:
- all P0 packages complete
- no open blocker on routing, template, data, or compliance

Completion criteria:
- launch recommendation can be made with evidence

---

## Definition Of Done

The project is only considered complete when all of the following are true:

- a dedicated OpenClaw company research agent exists
- the approved planning docs are present in runtime context
- the Chinese report template is implemented
- source hierarchy and citation rules are implemented
- at least one supported data-provider stack is documented and connected
- Feishu can route a request to the correct agent
- the agent can return a report artifact
- compliance checklist exists and passes
- quality checklist exists and passes
- end-to-end tests have been run with recorded results

## Required Evidence For Completion

Every future AI agent working this plan must report:

- commands run
- files changed
- test cases executed
- outputs produced
- pass/fail status
- known gaps

Do not report the project as done without concrete validation evidence.

## Recommended Execution Order For Future AI Agents

If a future AI agent needs a strict next-step order, use:

1. Package 1.1
2. Package 1.2
3. Package 2.1
4. Package 2.2
5. Package 2.3
6. Package 3.1
7. Package 3.2
8. Package 3.3
9. Package 4.1
10. Package 4.2
11. Package 4.3
12. Package 5.1
13. Package 5.2
14. Package 5.3
15. Package 6.1
16. Package 6.2
17. Package 6.3
18. Package 7.1
19. Package 7.2
20. Package 7.3

## Short Continuation Summary

This project must be delivered as a sequence of test-gated work packages, not as a single broad implementation push.

The shortest valid path is:

- establish runtime agent context
- implement template and source rules
- fix provider choices
- define workflow and output contracts
- bind the agent into OpenClaw and Feishu
- create compliance and quality gates
- run end-to-end validation

Nothing is complete until compliance and test evidence exists.
