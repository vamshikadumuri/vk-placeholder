# OWASP Coverage and Tooling — Slide Data and Methodology

**Slide:** "OWASP coverage and Tooling" — AI Red Teaming Deck
**Data as of:** 20 August 2026
**Tooling baseline:** garak 0.15.1 (5 Jun 2026) · PyRIT 0.11.0 (Feb 2026)
**Owner:** Vamshi — Enterprise Data Platform, DBS

---

## 1. Header boxes (corrected)

| Box | Text to use | Sub-line |
|---|---|---|
| 1 | **OWASP Top 10 for LLM Applications 2026** — LLM01–LLM10 | Model, prompt, RAG and application behaviour · published 4 Aug 2026 |
| 2 | **OWASP Top 10 for Agentic Applications (2026)** — ASI01–ASI10 | Goals, memory, tools, identity and autonomy · released 9 Dec 2025 |
| 3 | **OWASP MCP Top 10 — Beta (Phase 3)** — MCP01:2025–MCP10:2025 | Servers, tool metadata, authorization and context · next release Oct 2026 |

**Changes from the current slide**

- Box 2 title corrected. There is no list called "OWASP Agentic Top 10 2026". The published name is *OWASP Top 10 for Agentic Applications*, 2026 edition, released 9 December 2025 by the OWASP GenAI Security Project. Governance reviewers cross-check titles against the source document; a wrong title reads as a sourcing error even when the content is right.
- Box 1 dated. The 2026 LLM list is two weeks old at time of writing. Showing the publication date pre-empts "is this the 2025 list?" from the floor.
- Box 3 status made explicit. "2025 Beta" was accurate but ambiguous. MCP01–MCP10 carry a `:2025` suffix while the project sits in Phase 3 (beta and pilot testing). Phase 5 schedules the next release for October 2026, which is the expiry date on this box.

---

## 2. Verified capability-to-scope mapping (corrected)

Legend: **DIRECT** = packaged test or scenario ships with the tool · **CUSTOM** = adapter or scenario needed · **GAP / OTHER CONTROLS** = not a red-team test; belongs to platform, SDLC or governance controls.

| OWASP risk area | Representative tests | garak | PyRIT |
|---|---|---|---|
| LLM01 / ASI01 / MCP06 | Prompt injection, goal hijack, intent-flow subversion | DIRECT | DIRECT |
| LLM02 / LLM08 / ASI06 / MCP01 / MCP10 | Data leakage, system-prompt and tool-schema extraction, context poisoning and over-sharing | DIRECT ² | CUSTOM |
| LLM10 / ASI05 / MCP05 | Unsafe output handling, code and command execution | DIRECT | CUSTOM |
| LLM07 / ASI08 / ASI09 | Misinformation, unsafe advice, human-agent trust exploitation | DIRECT ³ | DIRECT ³ |
| LLM03 / ASI02 / ASI03 / MCP02 / MCP07 | Tool misuse, excessive agency, privilege and authorization | DIRECT ¹ | CUSTOM |
| ASI10 / MCP03 / MCP09 | Tool poisoning, rogue agents, shadow servers | CUSTOM | CUSTOM |
| LLM04–LLM06 / LLM09 / ASI04 / ASI07 / MCP04 / MCP08 | Supply chain, model poisoning, unbounded consumption, vector and embedding, inter-agent transport, audit and telemetry | GAP / OTHER CONTROLS | GAP / OTHER CONTROLS |

**Footnotes (put these at 8pt under the table)**

1. garak ≥ 0.15.0 (1 May 2026) ships the Agent-breaker probe, which tests tools exposed by the target system. This cell was CUSTOM on the previous version of the slide and is now DIRECT.
2. Model-and-endpoint layer only. MCP01 is covered to the extent secrets leak *through* the model; secret storage, rotation and server configuration are platform controls, not probe targets.
3. Covers the misinformation and trust-exploitation surface on a single agent. ASI08 cascade propagation across a multi-agent graph needs a scenario harness and is not packaged in either tool.
4. Neither tool ships MCP-protocol-native probes as of August 2026. Every MCP cell above is reached through the agent's model endpoint, not by scanning the MCP server itself.

---

## 3. Phase banner (corrected)

> **Phase 1 | garak** — packaged probes plus multi-turn GOAT and Agent-breaker, for broad black-box baselining
> **Phase 2 | PyRIT** — adaptive orchestration and bespoke agent/MCP scenarios where packaged probes stop

The previous banner described garak as single-turn packaged probes and reserved multi-turn entirely for PyRIT. That split stopped being true in May 2026 when garak 0.15.0 added the multi-turn GOAT probe. The Phase 1 / Phase 2 sequencing still holds — the distinction is now *packaged versus bespoke*, not *single-turn versus multi-turn*.

---

## 4. How this data was generated

### 4.1 Sources

Every taxonomy code and description was read from primary sources, not from secondary summaries or from model recall.

| Item | Source | Retrieved |
|---|---|---|
| LLM01–LLM10 (2026) and the 2025→2026 renumbering | OWASP GenAI Security Project, *Top 10 for LLM Applications 2026*, published 4 Aug 2026 | 20 Aug 2026 |
| LLM→ASI crosswalk | Appendix A of the same document, which maps each 2026 entry to nine other frameworks | 20 Aug 2026 |
| ASI01–ASI10 | OWASP GenAI Security Project, *Top 10 for Agentic Applications* (2026 edition), released 9 Dec 2025 | 20 Aug 2026 |
| MCP01–MCP10 and project phase | `owasp.org/www-project-mcp-top-10` project page, including the road map section | 20 Aug 2026 |
| garak capability | NVIDIA/garak GitHub release notes, v0.13.0 through v0.15.1 | 20 Aug 2026 |
| PyRIT capability | PyRIT release notes and the Cloud Security Alliance evaluation of PyRIT for agentic red teaming (Jun 2026) | 20 Aug 2026 |

### 4.2 Grading rule

Each cell was assigned by asking one question: **can a tester produce evidence for this risk without writing new code?**

- **DIRECT** — a named probe, attack or orchestrator ships with the tool and its output is scorable as-is. Example: garak's `promptinject` and `latentinjection` for LLM01.
- **CUSTOM** — the tool has the primitives but the scenario has to be built. Example: PyRIT for tool misuse. The CSA evaluation is explicit that PyRIT does not natively model agent state, authorization or tool execution; agent constructs in a PyRIT test are simulated through prompting, so authorization findings need a purpose-built target and scorer.
- **GAP / OTHER CONTROLS** — no meaningful red-team surface at the model endpoint. Supply chain, telemetry and vector-store hygiene are answered by provenance tracking, logging and access control, and claiming red-team coverage for them would be misleading.

The rule matters more than the individual cells. Reviewers will challenge specific gradings; having a stated test lets you defend or concede a cell without the whole table losing credibility.

### 4.3 Completeness check

The previous version of the slide left five risks unmapped: ASI06, ASI07, ASI08, ASI10 and MCP03. MCP03 Tool Poisoning was the most exposed omission — it is the most frequently cited MCP risk in the field, with a publicly documented malicious server incident behind it, and its absence from a slide headed "verified" invites the obvious question.

The corrected table accounts for all thirty codes: 10 LLM, 10 ASI, 10 MCP. Where a risk is not testable, it appears in the GAP row rather than being dropped. A visible "not covered, and here is why" is defensible; a silent omission is not.

### 4.4 Deviations from OWASP's own crosswalk

Appendix A of the 2026 LLM document maps LLM02 and LLM08 primarily to ASI06, and LLM07 primarily to ASI08 with ASI09 secondary. Both are now reflected in the table. Two deliberate deviations remain:

- **LLM10 is grouped with ASI05, not ASI02.** OWASP's appendix maps LLM10 to ASI02 Tool Misuse. Grouping by *test method* rather than by OWASP's primary counterpart puts improper output handling next to unexpected code execution, because the same probes exercise both. Worth stating aloud if challenged.
- **LLM06 sits in the GAP row.** OWASP maps it to ASI02, which would place it in the tool-misuse row. Neither tool has a packaged denial-of-wallet or resource-exhaustion probe, so grading it DIRECT alongside genuine tool-misuse coverage would overstate the position.

### 4.5 Refresh triggers

This slide expires on any of the following:

- **October 2026** — MCP Top 10 Phase 5 release. Codes may be renumbered or re-scoped; the beta caveat comes off the header box.
- **MCP Top 10 Phase 4 final release** — timing unannounced, could land before October.
- **Any garak minor release.** The Agent-breaker precedent shows a single release can flip a cell from CUSTOM to DIRECT. Check release notes each cycle.
- **Any PyRIT release adding native agent-state or tool-execution modelling.** This would move most of the PyRIT column and change the Phase 1 / Phase 2 rationale.

Re-verify against primary sources at each trigger. The taxonomy codes are stable enough to cite between triggers; the tooling column is not.
