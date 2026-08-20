# OWASP Coverage and Tooling — Final Slide Data (v2)

**Slide:** "OWASP coverage and Tooling" — AI Red Teaming Deck, DBS
**Data verified:** 20 August 2026
**Tooling baseline:** garak 0.15.1 (5 Jun 2026) · PyRIT 0.11.0 (Feb 2026)
**Supersedes:** v1 methodology file, and the Copilot-revised slide of 20 Aug 2026

---

## 1. Header boxes

| Box | Title | Codes | Sub-line |
|---|---|---|---|
| 1 | OWASP LLM Top 10 2026 | LLM01–LLM10 | Model, prompt, RAG and application behaviour |
| 2 | **OWASP Top 10 for Agentic Applications (2026)** | ASI01–ASI10 | Goals, memory, tools, identity and autonomy |
| 3 | OWASP MCP Top 10 2025 Beta | MCP01–MCP10 | Servers, tool metadata, authorization and context |

**Only box 2 changes.** The current slide reads "OWASP Agentic Top 10 2025". The list was released 9 December 2025 but is designated the **2026** edition — OWASP publishes it as "Top 10 for Agentic Applications for 2026". Dating it 2025 is the single most checkable error on the slide, because a reviewer who opens the OWASP page sees a different year in the title.

Boxes 1 and 3 are correct as they stand. The LLM 2026 list was published 4 August 2026; the MCP list is genuinely still in beta (Phase 3, pilot testing).

---

## 2. Verified capability-to-scope mapping

| OWASP risk area | Representative tests | Garak | PyRIT |
|---|---|---|---|
| LLM01 / ASI01 / MCP06 | Prompt injection, goal hijacking, intent-flow subversion | DIRECT | DIRECT |
| LLM02 / LLM08 / MCP01 / MCP10 | Sensitive-information disclosure, hidden-context exposure, secret leakage and context over-sharing | DIRECT | CUSTOM |
| LLM10 / ASI05 / MCP05 | Improper output handling and unintended code or command execution | DIRECT | CUSTOM |
| LLM07 / ASI09 | Misinformation and human-agent trust exploitation | DIRECT | DIRECT |
| LLM03 / ASI02 / ASI03 / MCP02 / MCP07 | Excessive agency, tool misuse, identity abuse and authorization weakness | **DIRECT** | CUSTOM |
| LLM04–05 / LLM09 / ASI04 / ASI07 / MCP04 / MCP08 | Supply-chain compromise, data and model poisoning, vector weaknesses, inter-agent transport and missing telemetry | GAP / OTHER CONTROLS | GAP / OTHER CONTROLS |
| LLM06 / ASI06 / ASI08 / ASI10 / MCP03 / MCP09 | Resource exhaustion, memory and context poisoning, cascading failures, rogue agents, tool poisoning and shadow servers | CUSTOM | CUSTOM |

**Legend:** DIRECT = packaged test or scenario · CUSTOM = adapter or scenario needed · GAP / OTHER CONTROLS = not a red-team test

**Footnote (8pt, under the table):** garak ≥ 0.15.1 (Jun 2026), PyRIT 0.11.0. Neither tool ships MCP-protocol-native probes; MCP coverage is reached through the agent's model endpoint, not by scanning the MCP server.

---

## 3. Phase banner

> **Phase 1 – Garak** — packaged probes plus multi-turn GOAT and Agent-breaker for broad black-box baselining
> **Phase 2 – PyRIT** — bespoke agent and MCP scenarios where packaged probes stop

Drop "repeatable packaged probes" and "adaptive, multi-turn orchestration". Framing garak as single-turn and reserving multi-turn for PyRIT stopped being accurate in May 2026, when garak 0.15.0 added the multi-turn GOAT probe. The Phase 1 / Phase 2 sequencing still holds — the distinction is now **packaged versus bespoke**, not single-turn versus multi-turn.

---

## 4. Changes from the Copilot-revised slide

Four edits. Everything else in that version stands.

| # | Change | Why |
|---|---|---|
| 1 | Header box 2: "2025" → "(2026)" | The Agentic list is the 2026 edition, released Dec 2025. Copilot appears to have replaced the edition year with the release year. |
| 2 | Row 5, Garak: CUSTOM → **DIRECT** | garak 0.15.0 (1 May 2026) shipped the **Agent-breaker** probe, which tests tools available to the target system. That is precisely the tool-misuse and excessive-agency surface. Verifiable in the NVIDIA/garak release notes. |
| 3 | Row 5 text: "identify abuse" → "identity abuse" | ASI03 is *Identity and Privilege Abuse*. Typo. |
| 4 | Swap ASI06 and MCP03 out of the GAP row into the CUSTOM row; swap ASI07 and MCP08 the other way | See §5.2. |

---

## 5. How the data was generated

### 5.1 Sources

Every code and description was read from a primary source on 20 Aug 2026 — not from secondary summaries and not from model recall.

| Item | Source |
|---|---|
| LLM01–LLM10 (2026) and the 2025→2026 renumbering | OWASP GenAI Security Project, *Top 10 for LLM Applications 2026*, published 4 Aug 2026 |
| LLM→ASI crosswalk | Appendix A of the same document |
| ASI01–ASI10 | OWASP GenAI Security Project, *Top 10 for Agentic Applications* (2026 edition), released 9 Dec 2025 |
| MCP01–MCP10 and project phase | `owasp.org/www-project-mcp-top-10` |
| garak capability | NVIDIA/garak GitHub release notes, v0.13.0 → v0.15.1 |
| PyRIT capability | PyRIT release notes; Cloud Security Alliance, *Evaluating PyRIT for Agentic AI Red Teaming* (Jun 2026) |

### 5.2 Grading rule

Each cell answers one question: **can a tester produce evidence for this risk without writing new code?**

- **DIRECT** — a named probe or attack ships with the tool and its output is scorable as-is. Example: garak `promptinject` and `latentinjection` for LLM01; garak `Agent-breaker` for LLM03/ASI02.
- **CUSTOM** — the primitives exist, the scenario does not. Example: PyRIT for tool misuse. The CSA evaluation states plainly that PyRIT does not natively model agent state, authorization or tool execution — agent constructs in a PyRIT test are simulated through prompting, so authorization findings need a purpose-built target and scorer.
- **GAP / OTHER CONTROLS** — no meaningful red-team surface at the model endpoint. Provenance tracking, transport security, logging and access control answer these.

**This rule is what drives edit #4.** Two items in the GAP row are genuinely testable and two in the CUSTOM row are not:

- **MCP03 Tool Poisoning** → CUSTOM. Stand up a tool whose description carries hidden instructions and observe whether the agent obeys. That is a scenario, not a control. It is also the most-cited MCP risk in the field, so grading it a gap invites the obvious challenge.
- **ASI06 Memory & Context Poisoning** → CUSTOM. The CSA PyRIT evaluation uses false-memory insertion as its worked example: inject distorted memories, check whether the agent refuses and flags them as unauthorised.
- **ASI07 Insecure Inter-Agent Communication** → GAP. Transport downgrade and MITM are network and PKI controls, not model-endpoint probes.
- **MCP08 Lack of Audit and Telemetry** → GAP. You cannot red-team absent logging. Immutable audit trails are a platform control.

The rule matters more than any individual cell. Reviewers will challenge specific gradings; a stated test lets you concede one cell without the table losing credibility.

### 5.3 Completeness

All thirty codes appear exactly once: 10 LLM, 10 ASI, 10 MCP. Risks that are not testable appear in the GAP row rather than being dropped. A visible "not covered, and here is why" is defensible in a governance review; a silent omission is not.

### 5.4 Deliberate deviations from OWASP's crosswalk

Appendix A of the 2026 LLM document maps LLM02 and LLM08 primarily to ASI06, and LLM07 primarily to ASI08 with ASI09 secondary. This table groups by **test method** instead, which is the right axis for a tooling slide:

- **ASI06 sits with the poisoning scenarios**, not with row 2's disclosure probes, because poisoning memory and extracting hidden context are different tests even where OWASP links them.
- **ASI08 Cascading Failures sits in the CUSTOM row**, not with LLM07. Cascade propagation across a multi-agent graph needs a scenario harness; it is not exercised by misinformation probes.
- **LLM10 groups with ASI05**, though OWASP maps it to ASI02, because the same output-handling and code-execution probes cover both.

Say this aloud if challenged. The deviation is defensible; being caught unaware of it is not.

---

## 6. Refresh triggers

| Trigger | Expected | Impact |
|---|---|---|
| MCP Top 10 Phase 5 release | **October 2026** | Codes may be renumbered or re-scoped; beta caveat comes off box 3. Hard expiry on this slide. |
| MCP Top 10 Phase 4 final release | Unannounced, could precede October | Same |
| Any garak minor release | ~6 weekly | Agent-breaker set the precedent: one release flipped a cell from CUSTOM to DIRECT. Read the notes each cycle. |
| PyRIT release adding native agent-state or tool-execution modelling | Unannounced | Would move most of the PyRIT column and change the Phase 1 / Phase 2 rationale entirely. |

Taxonomy codes are stable enough to cite between triggers. The tooling column is not — re-verify it against release notes before every re-presentation.
