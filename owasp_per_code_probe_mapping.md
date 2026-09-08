# Per-Code Probe Mapping — LLM / ASI / MCP

**Companion appendix to the "OWASP coverage and Tooling" slide.**
Verified 20 Aug 2026 · garak 0.15.1 · PyRIT 0.11.0

Every code in all three frameworks gets its own row. Titles taken from primary sources: the LLM 2026 list (published 4 Aug 2026), the Top 10 for Agentic Applications 2026 edition (released 9 Dec 2025), and the MCP Top 10 beta project page.

---

## ⚠️ What splitting per code reveals

**The slide grades each row at the level of its strongest member.** That is a normal simplification, but it means three cells claim more than every code in them can support. You need to know which, because a reviewer who picks a code out of a grouped row and asks "show me the probe" can land on one of these:

| Slide row | Grouped grading | Codes that do NOT support it |
|---|---|---|
| Row 2 | Garak DIRECT | **MCP10** — no garak probe for cross-context bleed |
| Row 4 | Garak DIRECT | **ASI09** — only `lmrc.Anthropomorphisation`, which is adjacent, not a trust-exploitation test |
| Row 5 | Garak DIRECT | **ASI03, MCP02, MCP07** — `agent_breaker` tests tool access, not delegation, confused-deputy or scope creep |

**Two ways to handle this.** Either mark those cells with an asterisk on the slide reading *"strongest-member grading; see appendix"*, or say it in the room before the question comes. Do not leave it undeclared — the whole slide is headed "Verified", and one unsupported code found by a reviewer costs you more credibility than three declared caveats.

---

## 1. OWASP Top 10 for LLM Applications 2026

| Code | Title | garak | PyRIT | Grade (G / P) |
|---|---|---|---|---|
| **LLM01** | Prompt Injection | `promptinject.HijackHateHumans` / `.HijackKillHumans` / `.HijackLongPrompt` · `latentinjection.*` · `dan.*` · `encoding.Inject*` · `suffix.GCG` / `.BEAST` · `tap.TAP` / `.PAIR` · `goat` · `atkgen.Tox` · `fitd.FITD` · `sata.MLM` · `smuggling.*` | `PromptSendingAttack` · `RedTeamingAttack` · `CrescendoAttack` · `TAPAttack` · `XPIATestOrchestrator` | DIRECT / DIRECT |
| **LLM02** | Sensitive Information Disclosure | `propile.PIILeakTwin` / `.PIILeakTriplet` / `.PIILeakQuadruplet` / `.PIILeakUnstructured` · `leakreplay.*` · `apikey.GetKey` / `.CompleteKey` · `divergence` | `PromptSendingAttack` + custom canary-matching `Scorer` | DIRECT / CUSTOM |
| **LLM03** | Excessive Agency | `agent_breaker.AgentBreaker` (0.15.0+) · `goat` | Custom `PromptTarget` wrapping the ADK tool interface + trace-assertion scorer | DIRECT / CUSTOM |
| **LLM04** | Supply Chain | *(partial only: `fileformats.HF_Files` inspects model files on disk — not endpoint testing)* | — | GAP / GAP |
| **LLM05** | Data and Model Poisoning | — | — | GAP / GAP |
| **LLM06** | Unbounded Consumption | `divergence` as a starting point; no consumption-ceiling probe | Recursive tool-call loop; assert on token and call-count ceilings from OTel spans | CUSTOM / CUSTOM |
| **LLM07** | Misinformation | `snowball.GraphConnectivity` (11.5% ASR, detector `DontStartYes`) / `.Primes` / `.Senators` · `misleading.FalseAssertion` · `packagehallucination.*` · `lmrc.QuackMedicine` · `goodside.*` | `RedTeamingAttack` + `SelfAskTrueFalseScorer` · `SelfAskLikertScorer` · `QuestionAnsweringBenchmarkOrchestrator` | DIRECT / DIRECT |
| **LLM08** | Hidden Context Exposure | `sysprompt_extraction` (0.15.0+) | `RedTeamingAttack` with objective "recover the system prompt" + custom scorer | DIRECT / CUSTOM |
| **LLM09** | Vector and Embedding Weaknesses | *(`latentinjection.*` covers RAG-borne injection, not vector-store weaknesses themselves)* | — | GAP / GAP |
| **LLM10** | Improper Output Handling | `exploitation.SQLInjectionEcho` / `.SQLInjectionSystem` / `.JinjaTemplatePythonInjection` · `web_injection.TaskXSS` · `ansiescape.AnsiEscaped` / `.AnsiRaw` · `malwaregen.*` · `av_spam_scanning.EICAR` / `.GTUBE` | Custom scorer asserting on *effect* (did the SQL run) not output text | DIRECT / CUSTOM |

---

## 2. OWASP Top 10 for Agentic Applications 2026

| Code | Title | garak | PyRIT | Grade (G / P) |
|---|---|---|---|---|
| **ASI01** | Agent Goal Hijack | `latentinjection.*` · `promptinject.*` · `goat` · `agent_breaker.AgentBreaker` | `XPIATestOrchestrator` · `CrescendoAttack` · `RedTeamingAttack` | DIRECT / DIRECT |
| **ASI02** | Tool Misuse and Exploitation | `agent_breaker.AgentBreaker` — release note: *"adds support for testing tools available to target systems"* | Custom `PromptTarget` + tool-call trace scorer | DIRECT / CUSTOM |
| **ASI03** | Identity and Privilege Abuse | *(no probe for delegation, cached credentials or confused-deputy)* | Two-agent harness: low-privilege agent induces a high-privilege agent to act for it | **CUSTOM** / CUSTOM |
| **ASI04** | Agentic Supply Chain Vulnerabilities | — | — | GAP / GAP |
| **ASI05** | Unexpected Code Execution (RCE) | `exploitation.*` · `malwaregen.TopLevel` / `.SubFunctions` / `.Payload` / `.Evasion` | Custom execution-effect scorer | DIRECT / CUSTOM |
| **ASI06** | Memory and Context Poisoning | — | Inject false memories across sessions; assert the agent refuses and flags them as unauthorised (the CSA's own worked PyRIT example) | CUSTOM / CUSTOM |
| **ASI07** | Insecure Inter-Agent Communication | — | — | GAP / GAP |
| **ASI08** | Cascading Failures | — | Poison upstream agent; assert downstream agents do not act on the output | CUSTOM / CUSTOM |
| **ASI09** | Human-Agent Trust Exploitation | `lmrc.Anthropomorphisation` — *adjacent, not a trust-exploitation test* | `RedTeamingAttack` with a persuasion objective + `SelfAskTrueFalseScorer` on "did it push the user toward an unsafe approval" | **CUSTOM** / DIRECT |
| **ASI10** | Rogue Agents | — | `CrescendoAttack` over extended turns; long-horizon objective with a reward-hacking shortcut available | CUSTOM / CUSTOM |

*Note on ASI06 naming:* OWASP's launch material and most secondary sources use **Memory and Context Poisoning**. At least one vendor glossary renders it *Context Management and Retrieval Manipulation*. Use OWASP's wording.

---

## 3. OWASP MCP Top 10 (2025 Beta)

| Code | Title | garak | PyRIT | Grade (G / P) |
|---|---|---|---|---|
| **MCP01** | Token Mismanagement & Secret Exposure | `apikey.GetKey` / `.CompleteKey` — *secrets surfacing through the model only; storage and rotation are platform controls* | `PromptSendingAttack` + canary-token scorer | DIRECT / CUSTOM |
| **MCP02** | Privilege Escalation via Scope Creep | *(`agent_breaker` tests tool access, not scope accumulation over a session)* | Session-length harness: assert granted scope never exceeds the initial grant | **CUSTOM** / CUSTOM |
| **MCP03** | Tool Poisoning | — | MCP server with hidden instructions in the tool description; assert the agent does not obey | CUSTOM / CUSTOM |
| **MCP04** | Software Supply Chain Attacks & Dependency Tampering | — | — | GAP / GAP |
| **MCP05** | Command Injection & Execution | `exploitation.SQLInjectionEcho` / `.SQLInjectionSystem` / `.JinjaTemplatePythonInjection` · payload set `access_shell_commands` | Custom execution-effect scorer | DIRECT / CUSTOM |
| **MCP06** | Intent Flow Subversion | `latentinjection.*` — the strongest single artefact; models context acting as a second instruction channel | `XPIATestOrchestrator` | DIRECT / DIRECT |
| **MCP07** | Insufficient Authentication & Authorization | *(auth enforcement is a control test, not a probe)* | Bind attempt without valid credentials; assert refusal | **CUSTOM** / CUSTOM |
| **MCP08** | Lack of Audit and Telemetry | — | — | GAP / GAP |
| **MCP09** | Shadow MCP Servers | — | Offer an unapproved server; assert the agent refuses to bind | CUSTOM / CUSTOM |
| **MCP10** | Context Injection & Over-Sharing | *(no probe for cross-context bleed between agents)* | Seed canary strings into agent A's context, run agent B, assert the canary never appears | **CUSTOM** / CUSTOM |

*Note on MCP06 naming:* the OWASP project page is internally inconsistent — the current top-level list says **Intent Flow Subversion**, while an older section still reads *Prompt Injection via Contextual Payloads*. Use Intent Flow Subversion and be ready to explain the discrepancy, since a reviewer reading the same page may see the other wording.

---

## 4. Tally

| Grade | garak | PyRIT |
|---|---|---|
| DIRECT | 9 | 4 |
| CUSTOM | 11 | 18 |
| GAP / OTHER CONTROLS | 10 | 8 |

Ten of thirty codes are not red-team surface at all, which is the honest headline. Of the twenty that are, garak covers nine out of the box and PyRIT four — the rest is scenario work you build once and reuse. That framing is stronger for a governance audience than a coverage percentage, because it tells them what the next quarter of engineering buys.

---

## 5. Build priority for the CUSTOM column

Ordered by value per day of effort:

1. **MCP03 Tool Poisoning** — half a day. Fake MCP server, poisoned tool description, trace assertion. Most-cited MCP risk in the field with a documented real incident (`postmark-mcp`) behind it.
2. **ASI03 / MCP02 privilege and scope** — the largest cluster of unsupported codes under a DIRECT cell. Closing this makes row 5 honest without an asterisk.
3. **ASI06 Memory & Context Poisoning** — CSA publishes the worked PyRIT pattern, so this is adaptation rather than invention.
4. **MCP10 cross-context bleed** — matters most for multi-tenant banking agents; a canary harness is reusable across every scenario after it.
5. **LLM06 / ASI08 / ASI10** — highest effort, and the findings are the hardest to act on. Last.

---

## 6. Verification commands

```bash
pip show garak pyrit                              # pin the versions you claim
python -m garak --list_probes                     # confirm every probe name above exists
python -m garak --list_probes | grep -i agent     # confirm agent_breaker (needs >= 0.15.0)
python -m garak --list_probes | grep -iE "sysprompt|propile|exploitation|web_injection"
```

**Remember:** garak's own `owasp:llmXX` tags follow the **2025** numbering, not 2026. `snowball` is tagged `owasp:llm09` but appears above under LLM07; `ansiescape` is tagged `owasp:llm05` but appears under LLM10. State the translation before anyone diffs a garak report against this appendix.
