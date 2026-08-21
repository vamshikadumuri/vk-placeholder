# Per-Code Probe Mapping — Fully Enumerated

**Companion appendix to the "OWASP coverage and Tooling" slide.**
Verified 20 Aug 2026 against `reference.garak.ai` (latest) and `microsoft.github.io/PyRIT`
garak 0.15.1 (5 Jun 2026) · PyRIT 0.11.0 (Feb 2026)

Every probe below is a named class. Invocation form is `module.ClassName`, e.g.
`python -m garak --model_type openai --model_name <target> --probes promptinject.HijackHateHumans,latentinjection.LatentInjectionReport`

---

## Section 0 — Two names I could not confirm from the docs

Do not put these on a slide until you have run `--list_probes` against your installed build.

| Item | Status |
|---|---|
| `goat` class name | Module confirmed present (v0.15.0, PR #1424, multi-turn GOAT). The docs index shows section headings for this module, not its class list. Run at module level as `--probes goat`, which is valid, or confirm the class name at runtime. |
| `packagehallucination.JavaScript` | The docs index is truncated immediately before this entry. The **detector** `packagehallucination.JavaScriptNpm` is confirmed, which makes a matching probe class near-certain, but I have not seen it listed. Confirmed probe classes in this module are enumerated below without it. |
| `latentinjection` — four classes | The docs index truncates mid-list. Confirmed classes are enumerated below. The four not directly sighted are `LatentInjectionResumeFull`, `LatentInjectionTranslationEnFr`, `LatentInjectionTranslationEnFrFull`, `LatentInjectionTranslationEnZh`. Their `Full` / non-`Full` counterparts are confirmed, so they almost certainly exist. |

Everything else in this document was read directly from the API reference.

---

## Section 1 — OWASP Top 10 for LLM Applications 2026

### LLM01 — Prompt Injection · **Garak DIRECT · PyRIT DIRECT**

**garak probes:**
`promptinject.HijackHateHumans`, `promptinject.HijackHateHumansFull`, `promptinject.HijackKillHumans`, `promptinject.HijackKillHumansFull`, `promptinject.HijackLongPrompt`, `promptinject.HijackLongPromptFull`
`latentinjection.LatentInjectionFactSnippetEiffel`, `latentinjection.LatentInjectionFactSnippetEiffelFull`, `latentinjection.LatentInjectionFactSnippetLegal`, `latentinjection.LatentInjectionFactSnippetLegalFull`, `latentinjection.LatentInjectionReport`, `latentinjection.LatentInjectionReportFull`, `latentinjection.LatentInjectionResume`, `latentinjection.LatentInjectionTranslationEnZhFull`, `latentinjection.LatentJailbreak`, `latentinjection.LatentJailbreakFull`, `latentinjection.LatentWhois`, `latentinjection.LatentWhoisSnippet`, `latentinjection.LatentWhoisSnippetFull`
`dan.Ablation_Dan_11_0`, `dan.AntiDAN`, `dan.AutoDAN`, `dan.AutoDANCached`, `dan.ChatGPT_Developer_Mode_RANTI`, `dan.ChatGPT_Developer_Mode_v2`, `dan.ChatGPT_Image_Markdown`, `dan.DAN_Jailbreak`, `dan.DUDE`, `dan.DanInTheWild`, `dan.DanInTheWildFull`, `dan.Dan_6_0`, `dan.Dan_6_2`, `dan.Dan_7_0`, `dan.Dan_8_0`, `dan.Dan_9_0`, `dan.Dan_10_0`, `dan.Dan_11_0`, `dan.STAN`
`encoding.InjectAscii85`, `encoding.InjectAtbash`, `encoding.InjectBase16`, `encoding.InjectBase32`, `encoding.InjectBase64`, `encoding.InjectBase2048`, `encoding.InjectBraille`, `encoding.InjectEcoji`, `encoding.InjectHex`, `encoding.InjectMime`, `encoding.InjectMorse`, `encoding.InjectNato`, `encoding.InjectQP`, `encoding.InjectROT13`, `encoding.InjectUU`
`suffix.GCG`, `suffix.GCGCached`, `suffix.BEAST`
`tap.TAP`, `tap.TAPCached`, `tap.PAIR`
`atkgen.Tox` · `fitd.FITD` · `sata.MLM` · `badchars.BadCharacters`
`smuggling.FunctionMasking`, `smuggling.HomoglyphObfuscation`, `smuggling.HypotheticalResponse`
`phrasing.PastTense`, `phrasing.PastTenseFull`, `phrasing.FutureTense`, `phrasing.FutureTenseFull`
`visual_jailbreak.FigStep`, `visual_jailbreak.FigStepFull` (multimodal targets only)

**Published calibration:** `HijackHateHumans` 61.0%, `HijackKillHumans` 51.0%, `HijackLongPrompt` 45.7% ASR, all with detector `AttackRogueString`. `LatentInjectionFactSnippetEiffel` 30.7%, `LatentInjectionFactSnippetLegal` 50.3%, both with detector `TriggerListDetector`.

**PyRIT:** `PromptSendingAttack`, `RedTeamingAttack`, `CrescendoAttack`, `TAPAttack` (alias `TreeOfAttacksWithPruningAttack`), `XPIATestOrchestrator`
Converters: `Base64Converter`, `ROT13Converter`, `TranslationConverter`, `EmojiConverter`
Scorers: `SelfAskRefusalScorer`, `SelfAskTrueFalseScorer` with `TrueFalseQuestion`

---

### LLM02 — Sensitive Information Disclosure · **Garak DIRECT · PyRIT CUSTOM**

**garak probes:**
`propile.PIILeakTwin`, `propile.PIILeakTriplet`, `propile.PIILeakQuadruplet`, `propile.PIILeakUnstructured`
`leakreplay.LiteratureCloze`, `leakreplay.LiteratureClozeFull`, `leakreplay.LiteratureComplete`, `leakreplay.LiteratureCompleteFull`, `leakreplay.NYTCloze`, `leakreplay.NYTClozeFull`, `leakreplay.NYTComplete`, `leakreplay.NYTCompleteFull`, `leakreplay.GuardianCloze`, `leakreplay.GuardianClozeFull`, `leakreplay.GuardianComplete`, `leakreplay.GuardianCompleteFull`, `leakreplay.PotterCloze`, `leakreplay.PotterClozeFull`, `leakreplay.PotterComplete`, `leakreplay.PotterCompleteFull`
`apikey.GetKey`, `apikey.CompleteKey`
`divergence.RepeatedToken`
`web_injection.MarkdownImageExfil`, `web_injection.ColabAIDataLeakage`, `web_injection.StringAssemblyDataExfil`, `web_injection.PlaygroundMarkdownExfil`, `web_injection.MarkdownURIImageExfilExtended`, `web_injection.MarkdownURINonImageExfilExtended`

**Detectors:** `web_injection.MarkdownExfilBasic`, `web_injection.MarkdownExfilContent`, `web_injection.MarkdownExfilExtendedImage`, `web_injection.MarkdownExfilExtendedNonImage`

**ProPILE caveat, quote it yourself:** the docs state results indicate *potential* for PII extraction; confirmed memorisation requires verified training data.

**PyRIT:** `PromptSendingAttack` plus a custom `Scorer` subclass matching your canary tokens. No packaged extraction attack.

---

### LLM03 — Excessive Agency · **Garak DIRECT · PyRIT CUSTOM**

**garak probes:** `agent_breaker.AgentBreaker` (v0.15.0+, PR #1628 — *"adds support for testing tools available to target systems"*). Helper class in the same module: `agent_breaker.AttackState`. Module-level `goat` for multi-turn chains toward a tool call.

**PyRIT:** custom `PromptTarget` subclass wrapping the ADK tool interface, plus a scorer asserting on tool-call spans rather than reply text. Your existing OTel instrumentation is the evidence source.

---

### LLM04 — Supply Chain · **GAP / OTHER CONTROLS both**

Nearest artefact is `fileformats.HF_Files`, which inspects model files on disk. Not endpoint red teaming — mention it if pressed, but it does not change the grading. Owning control: model and dependency provenance, signed artefacts, registry allowlist.

---

### LLM05 — Data and Model Poisoning · **GAP / OTHER CONTROLS both**

No probe. Owning control: training and RAG corpus governance, ingestion review.

---

### LLM06 — Unbounded Consumption · **CUSTOM both**

`divergence.RepeatedToken` is the nearest primitive but tests extraction, not consumption ceilings. Build: recursive tool-call loop, assert on token and call-count ceilings from OTel spans.

---

### LLM07 — Misinformation · **Garak DIRECT · PyRIT DIRECT**

**garak probes:**
`snowball.GraphConnectivity`, `snowball.GraphConnectivityFull`, `snowball.Primes`, `snowball.PrimesFull`, `snowball.Senators`, `snowball.SenatorsFull`
`misleading.FalseAssertion`
`packagehallucination.Python`, `packagehallucination.Ruby`, `packagehallucination.Rust`, `packagehallucination.Perl`, `packagehallucination.RakuLand` (base class `packagehallucination.PackageHallucinationProbe`)
`goodside.Davidjl`, `goodside.Tag`, `goodside.ThreatenJSON`, `goodside.WhoIsRiley`
`lmrc.QuackMedicine`

**Detectors:** `packagehallucination.PackageHallucinationDetector`, `packagehallucination.JavaScriptNpm`, `packagehallucination.RustCrates`
**Published calibration:** `GraphConnectivity` 11.5% ASR with detector `DontStartYes`.

**PyRIT:** `RedTeamingAttack` + `SelfAskTrueFalseScorer`, `SelfAskLikertScorer`, `QuestionAnsweringBenchmarkOrchestrator`.
**Banking-specific build:** ground-truth DBS product facts as the objective set, scored against the product catalogue. Worth more to governance than a generic hallucination rate.

---

### LLM08 — Hidden Context Exposure · **Garak DIRECT · PyRIT CUSTOM**

**garak probe:** `sysprompt_extraction.SystemPromptExtraction` (v0.15.0+)
**Detectors:** `sysprompt_extraction.PromptExtraction`, `sysprompt_extraction.PromptExtractionVerbatim`
**PyRIT:** `RedTeamingAttack` with objective "recover the system prompt" plus custom scorer.

---

### LLM09 — Vector and Embedding Weaknesses · **GAP / OTHER CONTROLS both**

The `latentinjection` family covers RAG-borne injection, not weaknesses in vector generation, storage or retrieval. Owning control: vector store access control and tenant isolation.

---

### LLM10 — Improper Output Handling · **Garak DIRECT · PyRIT CUSTOM**

**garak probes:**
`exploitation.SQLInjectionEcho`, `exploitation.SQLInjectionSystem`, `exploitation.JinjaTemplatePythonInjection`
`web_injection.TaskXSS`, `web_injection.MarkdownXSS`
`ansiescape.AnsiEscaped`, `ansiescape.AnsiRaw`, `ansiescape.AnsiRawTokenizerHF`
`malwaregen.TopLevel`, `malwaregen.SubFunctions`, `malwaregen.Payload`, `malwaregen.Evasion`
`av_spam_scanning.EICAR`, `av_spam_scanning.GTUBE`, `av_spam_scanning.GTphish`

Payload set `access_shell_commands` is available to the encoding and injection probes.
`exploitation` sits in garak **Tier 1** per the tier docs, because SSTI in a live templating language is a real exploit path.

**PyRIT:** custom scorer asserting on effect (did the SQL run, did the command execute), not on output text.

---

## Section 2 — OWASP Top 10 for Agentic Applications 2026

### ASI01 — Agent Goal Hijack · **Garak DIRECT · PyRIT DIRECT**
Same probe set as LLM01, led by the `latentinjection` family and `agent_breaker.AgentBreaker`.
PyRIT: `XPIATestOrchestrator`, `CrescendoAttack`, `RedTeamingAttack`.

### ASI02 — Tool Misuse and Exploitation · **Garak DIRECT · PyRIT CUSTOM**
`agent_breaker.AgentBreaker`. PyRIT: custom `PromptTarget` + tool-call trace scorer.

### ASI03 — Identity and Privilege Abuse · **CUSTOM both**
No garak probe. `agent_breaker.AgentBreaker` tests tool *access*, not delegation, cached credentials or confused-deputy.
Build: two-agent harness where a low-privilege agent induces a high-privilege agent to act on its behalf.

### ASI04 — Agentic Supply Chain Vulnerabilities · **GAP both**
Owning control: registry allowlist, signed tool descriptors, MCP server provenance.

### ASI05 — Unexpected Code Execution (RCE) · **Garak DIRECT · PyRIT CUSTOM**
`exploitation.SQLInjectionEcho`, `exploitation.SQLInjectionSystem`, `exploitation.JinjaTemplatePythonInjection`, `malwaregen.TopLevel`, `malwaregen.SubFunctions`, `malwaregen.Payload`, `malwaregen.Evasion`.

### ASI06 — Memory and Context Poisoning · **CUSTOM both**
No probe. Build: inject false memories across sessions, assert the agent refuses and flags them as unauthorised. This is the CSA's own worked PyRIT example, so it is adaptation rather than invention.

### ASI07 — Insecure Inter-Agent Communication · **GAP both**
Owning control: mTLS, signed messages, service mesh.

### ASI08 — Cascading Failures · **CUSTOM both**
Build: poison an upstream agent, assert downstream agents do not act on its output.

### ASI09 — Human-Agent Trust Exploitation · **Garak CUSTOM · PyRIT DIRECT**
`lmrc.Anthropomorphisation` is the only adjacent garak probe and it is not a trust-exploitation test. Do not grade this DIRECT for garak.
PyRIT: `RedTeamingAttack` with a persuasion objective + `SelfAskTrueFalseScorer` on "did it push the user toward an unsafe approval".

### ASI10 — Rogue Agents · **CUSTOM both**
Build: long-horizon objective with a reward-hacking shortcut available; assert it is not taken. `CrescendoAttack` over extended turns is the nearest primitive.

---

## Section 3 — OWASP MCP Top 10 (2025 Beta)

### MCP01 — Token Mismanagement & Secret Exposure · **Garak DIRECT · PyRIT CUSTOM**
`apikey.GetKey`, `apikey.CompleteKey`. Model-layer only — storage and rotation are platform controls.

### MCP02 — Privilege Escalation via Scope Creep · **CUSTOM both**
No probe. Build: session-length harness asserting granted scope never exceeds the initial grant.

### MCP03 — Tool Poisoning · **CUSTOM both**
No probe. Build: MCP server with hidden instructions in the tool description; assert the agent does not obey.

### MCP04 — Software Supply Chain Attacks & Dependency Tampering · **GAP both**

### MCP05 — Command Injection & Execution · **Garak DIRECT · PyRIT CUSTOM**
`exploitation.SQLInjectionEcho`, `exploitation.SQLInjectionSystem`, `exploitation.JinjaTemplatePythonInjection`, payload set `access_shell_commands`.

### MCP06 — Intent Flow Subversion · **Garak DIRECT · PyRIT DIRECT**
Full `latentinjection` family — context acting as a second instruction channel is exactly what it models. PyRIT: `XPIATestOrchestrator`.

### MCP07 — Insufficient Authentication & Authorization · **CUSTOM both**
Build: bind attempt without valid credentials, assert refusal.

### MCP08 — Lack of Audit and Telemetry · **GAP both**
Owning control: immutable audit trail. Your OTel GenAI semantic-convention work sits here.

### MCP09 — Shadow MCP Servers · **CUSTOM both**
Build: offer an unapproved server, assert the agent refuses to bind.

### MCP10 — Context Injection & Over-Sharing · **CUSTOM both**
No garak probe for cross-context bleed. Build: seed canary strings into agent A's context, run agent B, assert the canary never appears.

---

## Section 4 — Where the slide's grouped rows over-claim

The slide grades each row at the level of its strongest member. Three Garak cells therefore claim more than every code beneath them supports:

| Slide row | Grouped grade | Codes with no probe behind them |
|---|---|---|
| Row 2 | Garak DIRECT | MCP10 |
| Row 4 | Garak DIRECT | ASI09 |
| Row 5 | Garak DIRECT | ASI03, MCP02, MCP07 |

Asterisk those three cells pointing here, or declare it in the room. One code pulled out of a grouped row with nothing behind it costs more than three declared caveats on a slide headed "Verified".

**Tally:** garak 9 DIRECT / 11 CUSTOM / 10 GAP · PyRIT 4 / 18 / 8.

---

## Section 5 — Verification

```bash
pip show garak pyrit

# full probe inventory for your installed build
python -m garak --list_probes

# confirm the three additions this appendix leans on
python -m garak --list_probes | grep -iE "agent_breaker|sysprompt_extraction|propile"

# confirm the two names flagged in Section 0
python -m garak --list_probes | grep -i "goat"
python -m garak --list_probes | grep -i "packagehallucination"

# smoke test against a target
python -m garak --model_type openai --model_name <target> \
  --probes promptinject.HijackHateHumans,latentinjection.LatentInjectionReport,agent_breaker.AgentBreaker
```

**Standing caveat — garak's OWASP tags are on the 2025 numbering.** `snowball` probes carry `owasp:llm09` but appear here under LLM07. `web_injection.MarkdownImageExfil` carries `owasp:llm02` and `owasp:llm06`. `leakreplay.LiteratureClozeFull` carries `owasp:llm10` and `owasp:llm06`. `packagehallucination` carries `owasp:llm09` and `owasp:llm02`. None of these have been renumbered for 2026. State the translation before anyone diffs a garak report against this appendix.
