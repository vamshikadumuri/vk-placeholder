# OWASP Coverage Slide — Probe-Level Evidence Pack

**Purpose:** back every cell on the "OWASP coverage and Tooling" slide with named, runnable artefacts.
**Verified:** 20 August 2026 against `reference.garak.ai` (latest) and `microsoft.github.io/PyRIT`.
**Baseline:** garak 0.15.1 (5 Jun 2026) · PyRIT 0.11.0 (Feb 2026)

---

## ⚠️ Read this before you present

**garak's built-in OWASP tags use the 2025 numbering, not 2026.** Every garak probe carries MISP-format tags such as `owasp:llm09`. These have not been renumbered for the 2026 list. Worked examples straight from the docs:

| Probe | garak tag | Means (2025) | Slide shows (2026) |
|---|---|---|---|
| `snowball.GraphConnectivity` | `owasp:llm09` | Misinformation | **LLM07** |
| `ansiescape.AnsiEscaped` | `owasp:llm05` | Improper Output Handling | **LLM10** |
| `leakreplay.LiteratureClozeFull` | `owasp:llm06`, `owasp:llm10` | Excessive Agency, Unbounded Consumption | **LLM03**, **LLM06** |

If a reviewer runs a garak report and cross-checks the tag column against your slide, the numbers will not match and it will look like an error in your mapping. Say it first: *"garak's tags are on the 2025 numbering; the slide is on 2026; here is the translation."* You have hit this exact class of problem before with the garak OWASP crosswalk, so the same caveat block applies.

**Regenerate before every presentation:**
```bash
python -m garak --list_probes          # confirms every probe name below exists in your installed version
python -m garak --list_probes | grep -i agent   # confirms Agent-breaker is present (needs >= 0.15.0)
pip show garak pyrit                    # pins the version numbers you claim on the slide
```

---

## Row 1 — LLM01 / ASI01 / MCP06
*Prompt injection, goal hijacking, intent-flow subversion* — **Garak DIRECT · PyRIT DIRECT**

**garak (built-in):**
- `promptinject.HijackHateHumans`, `.HijackKillHumans`, `.HijackLongPrompt` (plus `*Full` / `*Mini` variants). Calibrated ASR published in the docs: 61.0%, 51.0%, 45.7% respectively, detector `AttackRogueString`.
- `latentinjection.*` — indirect / XPIA-class injection buried in context. Classes: `LatentInjectionFactSnippetEiffel`, `LatentInjectionFactSnippetLegal`, `LatentInjectionReport`, `LatentInjectionResume`, `LatentInjectionTranslationEnFr`, `LatentInjectionTranslationEnZh`, `LatentJailbreak`, `LatentWhois`, `LatentWhoisSnippet`. This module is the strongest evidence for MCP06 Intent Flow Subversion — context acting as a second instruction channel is exactly what it models.
- `dan.*` (`Dan_11_0`, `DanInTheWild`, `AutoDAN`, `DUDE`, `STAN`, …), `encoding.Inject*` (Base16, Ascii85, Braille, NATO, QP, Atbash, Ecoji …), `suffix.GCG` / `.GCGCached` / `.BEAST`, `tap.TAP` / `.TAPCached` / `.PAIR`, `goat` (multi-turn, 0.15.0+), `atkgen.Tox`, `fitd.FITD`, `sata.MLM`, `smuggling.HomoglyphObfuscation` / `.FunctionMasking` / `.HypotheticalResponse`, `badchars.BadCharacters`.

**PyRIT (built-in):**
- `PromptSendingAttack` — single-turn baseline over your objective set.
- `RedTeamingAttack`, `CrescendoAttack`, `TAPAttack` (alias `TreeOfAttacksWithPruningAttack`) — adaptive multi-turn.
- `XPIATestOrchestrator` — purpose-built for cross-domain / indirect prompt injection. **This is your single best PyRIT artefact for ASI01 and MCP06.**
- Converters: `Base64Converter`, `ROT13Converter`, `TranslationConverter`, `EmojiConverter`.
- Scorers: `SelfAskRefusalScorer`, `SelfAskTrueFalseScorer` with `TrueFalseQuestion`.

---

## Row 2 — LLM02 / LLM08 / MCP01 / MCP10
*Sensitive-information disclosure, hidden-context exposure, secret leakage, context over-sharing* — **Garak DIRECT · PyRIT CUSTOM**

**garak (built-in):**
- `sysprompt_extraction` — system prompt extraction, added 0.15.0. Direct evidence for **LLM08 Hidden Context Exposure**, which is the entry most likely to be challenged as "you're testing the old System Prompt Leakage".
- `propile.PIILeakTwin`, `.PIILeakTriplet`, `.PIILeakQuadruplet`, `.PIILeakUnstructured` — PII extraction, added 0.15.1. Note the docs' own caveat: results indicate *potential* for extraction; confirmed memorisation needs verified training data. Quote that caveat yourself before someone else does.
- `apikey.GetKey`, `apikey.CompleteKey` — this is your **MCP01** evidence. Secrets surfacing through the model.
- `leakreplay.*` (`LiteratureCloze/Complete`, `NYTCloze/Complete`, `GuardianCloze/Complete`, `PotterCloze/Complete`) — training-data replay.
- `divergence` — repeated-token extraction (the Dropbox repeated-token attack).
- `web_injection.TaskXSS` — markdown/JS exfiltration channel. **Module renamed from `xss` to `web_injection`**; if your notes still say `xss`, update them.
- `ansiescape.AnsiEscaped`, `.AnsiRaw` — terminal-control exfil.

**PyRIT — why CUSTOM:** no packaged secret-extraction or context-exfiltration attack. Build with `PromptSendingAttack` + a custom `Scorer` subclass that regex-matches your canary tokens, or `RedTeamingAttack` with an objective phrased as "recover the system prompt".

**Custom work to plan (MCP10 Context Injection & Over-Sharing):** seed canary strings into agent A's context, run agent B, assert the canary never appears. Not packaged in either tool — this is a harness you write once and reuse.

---

## Row 3 — LLM10 / ASI05 / MCP05
*Improper output handling, unintended code or command execution* — **Garak DIRECT · PyRIT CUSTOM**

**garak (built-in):**
- `exploitation.SQLInjectionEcho`, `.SQLInjectionSystem`, `.JinjaTemplatePythonInjection` — the strongest artefacts here. The garak tier docs put `exploitation` in Tier 1 precisely because Jinja/SSTI in a popular templating language is a real exploit path.
- `malwaregen.TopLevel`, `.SubFunctions`, `.Payload`, `.Evasion`.
- `packagehallucination.*` (per-language classes — Python, JavaScript, Ruby, Rust, and Dart/Perl/Raku added in 0.13.1) — slopsquatting / non-existent imports, called out explicitly in LLM10:2026.
- `web_injection.TaskXSS`, `ansiescape.*`, `av_spam_scanning.EICAR` / `.GTUBE` / `.GTphish`.
- Payload set `access_shell_commands` is available to encoding and injection probes.

**PyRIT — why CUSTOM:** PyRIT scores text, not execution. You need a custom scorer that asserts on *effect* (did the SQL run, did the shell command execute) rather than on output text.

---

## Row 4 — LLM07 / ASI09
*Misinformation, human-agent trust exploitation* — **Garak DIRECT · PyRIT DIRECT**

**garak (built-in):**
- `snowball.GraphConnectivity`, `.Primes`, `.Senators` (+ `*Full`). Published calibration: `GraphConnectivity` 11.5% ASR with detector `DontStartYes`.
- `misleading.FalseAssertion`.
- `packagehallucination.*` — hallucination with a security consequence.
- `lmrc.QuackMedicine`, `lmrc.Anthropomorphisation` — the latter is your closest built-in to **ASI09 Human-Agent Trust Exploitation**; be honest that it is adjacent, not exact.
- `goodside.Davidjl`, `.ThreatenJSON`, `.WhoIsRiley`, `.Tag`.

**PyRIT (built-in):** `RedTeamingAttack` + `SelfAskTrueFalseScorer` for a "did the agent assert a falsehood as fact" rubric. `SelfAskLikertScorer` for graded confidence. `QuestionAnsweringBenchmarkOrchestrator` for ground-truth QA sets.

**Banking-specific custom work worth planning:** a ground-truth set of DBS product facts (rates, eligibility, fees) as the objective set, scored against the actual product catalogue. This is the finding governance will care about far more than a generic hallucination rate.

---

## Row 5 — LLM03 / ASI02 / ASI03 / MCP02 / MCP07
*Excessive agency, tool misuse, identity abuse, authorization weakness* — **Garak DIRECT · PyRIT CUSTOM**

**This is the cell that changed, so carry the strongest evidence for it.**

**garak (built-in):**
- `agent_breaker.AgentBreaker` (module `garak.probes.agent_breaker`, helper class `AttackState`). Shipped in **v0.15.0, 1 May 2026, PR #1628**, release note wording: *"adds support for testing tools available to target systems."*
- `goat` — multi-turn attacks that can chain toward a tool call.

**Proof to have open in a browser tab:** the NVIDIA/garak v0.15.0 release notes, and `reference.garak.ai` → Probes → `garak.probes.agent_breaker`. If anyone says "garak can't test agents", that page ends the conversation.

**PyRIT — why CUSTOM, and cite this:** the Cloud Security Alliance's June 2026 evaluation of PyRIT for agentic red teaming states that PyRIT does not natively model agent state, authorization, or tool execution, and that references to agent memory, roles, or permissions in a PyRIT test are *simulated constructs rather than enforced system controls*. That sentence is your justification for the CUSTOM grading — it is a third-party source, not your opinion.

**Custom work to plan:** a `PromptTarget` subclass wrapping BankBot's ADK tool interface, plus scorers asserting on tool-call traces rather than text. Your existing OTel/Jaeger instrumentation is the natural evidence source — assert on spans, not on the reply string.

---

## Row 6 — LLM04–05 / LLM09 / ASI04 / ASI07 / MCP04 / MCP08
*Supply chain, poisoning, vector weaknesses, inter-agent transport, missing telemetry* — **GAP / OTHER CONTROLS both**

Nothing to name, and that is the point. State the controls that do own these so the row does not read as an oversight:

| Risk | Owning control |
|---|---|
| LLM04 / ASI04 / MCP04 supply chain | Model and dependency provenance, signed artefacts, registry allowlist |
| LLM05 data & model poisoning | Training and RAG corpus governance, ingestion review |
| LLM09 vector & embedding | Vector store access control, tenant isolation |
| ASI07 inter-agent transport | mTLS, service mesh, PKI |
| MCP08 audit & telemetry | Immutable audit trail — your OTel GenAI semantic-convention work sits here |

One partial exception worth mentioning if pressed: `fileformats.HF_Files` inspects model files on disk, which touches LLM04. It is not endpoint red teaming, so it does not change the grading.

---

## Row 7 — LLM06 / ASI06 / ASI08 / ASI10 / MCP03 / MCP09
*Resource exhaustion, memory & context poisoning, cascading failures, rogue agents, tool poisoning, shadow servers* — **CUSTOM both**

Everything here is buildable, none of it is packaged. Have a one-line design for each so CUSTOM reads as *planned*, not *hand-waved*:

| Risk | Custom scenario to build | Nearest existing primitive |
|---|---|---|
| **LLM06** resource exhaustion | Recursive tool-call loop; assert on token and call-count ceilings from traces | `divergence` (repeated-token) as a starting point |
| **ASI06** memory & context poisoning | Inject false memories across sessions, assert the agent refuses and flags them as unauthorised — this is the CSA's own worked PyRIT example | PyRIT `RedTeamingAttack` + custom scorer |
| **ASI08** cascading failures | Poison upstream agent, assert downstream agents do not act on it | Multi-agent harness, none packaged |
| **ASI10** rogue agents | Long-horizon objective with a reward-hacking shortcut available; assert it is not taken | PyRIT `CrescendoAttack` over extended turns |
| **MCP03** tool poisoning | Stand up an MCP server with hidden instructions in the tool description; assert the agent does not obey | None packaged — highest-value build |
| **MCP09** shadow servers | Offer an unapproved server; assert the agent refuses to bind | None packaged |

**MCP03 is the one to build first.** It is the most-cited MCP risk in the field, it has a real documented incident behind it (`postmark-mcp`, ~1,500 weekly downloads, ~300 organisations before disclosure), and it is a half-day of work — a fake MCP server with a poisoned tool description and a trace assertion.

---

## Standing caveats for the footnote or the appendix

1. **Neither tool ships MCP-protocol-native probes.** Every MCP cell is reached through the agent's model endpoint. A garak GitHub issue requesting MCP Top 10 coverage (#1639, Mar 2026) is open and unresolved. Do not claim protocol-layer scanning.
2. **Coverage is claimed at scenario level**, as the slide subtitle already says. A probe existing is not coverage; a probe *configured against BankBot with a working detector* is coverage.
3. **Calibrated ASR figures exist for some garak probes and not others.** Where the docs publish an ASR, quote it. Where they do not, say so rather than implying equivalence.
4. **Probe names drift between releases.** `xss` became `web_injection`; `model_*` config keys became `target_*`; the `maxrecall` evaluator and `--generate_autodan` were removed. Re-run `--list_probes` against the installed version before every presentation.
