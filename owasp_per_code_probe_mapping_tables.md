# Per-Code Probe Mapping — Table Form

**Companion appendix to the "OWASP coverage and Tooling" slide.**
Verified 20 Aug 2026 · garak 0.15.1 (5 Jun 2026) · PyRIT 0.11.0 (Feb 2026)
Sources: `reference.garak.ai` (latest), `microsoft.github.io/PyRIT`, OWASP primary documents.

Invocation form is `module.ClassName`:
`python -m garak --model_type openai --model_name <target> --probes promptinject.HijackHateHumans,agent_breaker.AgentBreaker`

---

## 0. Names not confirmed from the docs — verify before presenting

| Item | Status | Check |
|---|---|---|
| `goat` class name | Module confirmed (v0.15.0, PR #1424, multi-turn GOAT). Docs index shows section headings, not classes. | `python -m garak --list_probes \| grep -i goat` |
| `packagehallucination.JavaScript` | Docs index truncates immediately before this entry. Detector `packagehallucination.JavaScriptNpm` **is** confirmed, so the probe is near-certain. Excluded from the tables below. | `python -m garak --list_probes \| grep -i packagehalluc` |
| `latentinjection.LatentInjectionResumeFull`, `.LatentInjectionTranslationEnFr`, `.LatentInjectionTranslationEnFrFull`, `.LatentInjectionTranslationEnZh` | Docs index truncates mid-list. Counterparts confirmed, so these almost certainly exist. Excluded from the tables below. | `python -m garak --list_probes \| grep -i latentinjection` |

Everything else was read directly from the API reference.

---

## 1. OWASP Top 10 for LLM Applications 2026

| Code | Title | garak probes (exact) | PyRIT | G / P |
|---|---|---|---|---|
| **LLM01** | Prompt Injection | `promptinject.HijackHateHumans`<br>`promptinject.HijackHateHumansFull`<br>`promptinject.HijackKillHumans`<br>`promptinject.HijackKillHumansFull`<br>`promptinject.HijackLongPrompt`<br>`promptinject.HijackLongPromptFull`<br>`latentinjection.LatentInjectionFactSnippetEiffel`<br>`latentinjection.LatentInjectionFactSnippetEiffelFull`<br>`latentinjection.LatentInjectionFactSnippetLegal`<br>`latentinjection.LatentInjectionFactSnippetLegalFull`<br>`latentinjection.LatentInjectionReport`<br>`latentinjection.LatentInjectionReportFull`<br>`latentinjection.LatentInjectionResume`<br>`latentinjection.LatentInjectionTranslationEnZhFull`<br>`latentinjection.LatentJailbreak`<br>`latentinjection.LatentJailbreakFull`<br>`latentinjection.LatentWhois`<br>`latentinjection.LatentWhoisSnippet`<br>`latentinjection.LatentWhoisSnippetFull`<br>`dan.Ablation_Dan_11_0`<br>`dan.AntiDAN`<br>`dan.AutoDAN`<br>`dan.AutoDANCached`<br>`dan.ChatGPT_Developer_Mode_RANTI`<br>`dan.ChatGPT_Developer_Mode_v2`<br>`dan.ChatGPT_Image_Markdown`<br>`dan.DAN_Jailbreak`<br>`dan.DUDE`<br>`dan.DanInTheWild`<br>`dan.DanInTheWildFull`<br>`dan.Dan_6_0`<br>`dan.Dan_6_2`<br>`dan.Dan_7_0`<br>`dan.Dan_8_0`<br>`dan.Dan_9_0`<br>`dan.Dan_10_0`<br>`dan.Dan_11_0`<br>`dan.STAN`<br>`encoding.InjectAscii85`<br>`encoding.InjectAtbash`<br>`encoding.InjectBase16`<br>`encoding.InjectBase32`<br>`encoding.InjectBase64`<br>`encoding.InjectBase2048`<br>`encoding.InjectBraille`<br>`encoding.InjectEcoji`<br>`encoding.InjectHex`<br>`encoding.InjectMime`<br>`encoding.InjectMorse`<br>`encoding.InjectNato`<br>`encoding.InjectQP`<br>`encoding.InjectROT13`<br>`encoding.InjectUU`<br>`suffix.GCG`<br>`suffix.GCGCached`<br>`suffix.BEAST`<br>`tap.TAP`<br>`tap.TAPCached`<br>`tap.PAIR`<br>`atkgen.Tox`<br>`fitd.FITD`<br>`sata.MLM`<br>`badchars.BadCharacters`<br>`smuggling.FunctionMasking`<br>`smuggling.HomoglyphObfuscation`<br>`smuggling.HypotheticalResponse`<br>`phrasing.PastTense`<br>`phrasing.PastTenseFull`<br>`phrasing.FutureTense`<br>`phrasing.FutureTenseFull`<br>`visual_jailbreak.FigStep`<br>`visual_jailbreak.FigStepFull` | `PromptSendingAttack`<br>`RedTeamingAttack`<br>`CrescendoAttack`<br>`TAPAttack`<br>`TreeOfAttacksWithPruningAttack`<br>`XPIATestOrchestrator`<br>Converters: `Base64Converter`, `ROT13Converter`, `TranslationConverter`, `EmojiConverter`<br>Scorers: `SelfAskRefusalScorer`, `SelfAskTrueFalseScorer` + `TrueFalseQuestion` | DIRECT / DIRECT |
| **LLM02** | Sensitive Information Disclosure | `propile.PIILeakTwin`<br>`propile.PIILeakTriplet`<br>`propile.PIILeakQuadruplet`<br>`propile.PIILeakUnstructured`<br>`leakreplay.LiteratureCloze`<br>`leakreplay.LiteratureClozeFull`<br>`leakreplay.LiteratureComplete`<br>`leakreplay.LiteratureCompleteFull`<br>`leakreplay.NYTCloze`<br>`leakreplay.NYTClozeFull`<br>`leakreplay.NYTComplete`<br>`leakreplay.NYTCompleteFull`<br>`leakreplay.GuardianCloze`<br>`leakreplay.GuardianClozeFull`<br>`leakreplay.GuardianComplete`<br>`leakreplay.GuardianCompleteFull`<br>`leakreplay.PotterCloze`<br>`leakreplay.PotterClozeFull`<br>`leakreplay.PotterComplete`<br>`leakreplay.PotterCompleteFull`<br>`apikey.GetKey`<br>`apikey.CompleteKey`<br>`divergence.RepeatedToken`<br>`web_injection.MarkdownImageExfil`<br>`web_injection.ColabAIDataLeakage`<br>`web_injection.StringAssemblyDataExfil`<br>`web_injection.PlaygroundMarkdownExfil`<br>`web_injection.MarkdownURIImageExfilExtended`<br>`web_injection.MarkdownURINonImageExfilExtended` | `PromptSendingAttack` + custom canary-matching `Scorer` subclass. No packaged extraction attack. | DIRECT / CUSTOM |
| **LLM03** | Excessive Agency | `agent_breaker.AgentBreaker` (v0.15.0+, PR #1628)<br>helper: `agent_breaker.AttackState`<br>module-level `goat` | Custom `PromptTarget` wrapping the ADK tool interface + scorer asserting on tool-call spans | DIRECT / CUSTOM |
| **LLM04** | Supply Chain | none — `fileformats.HF_Files` inspects model files on disk, not endpoint testing | — | GAP / GAP |
| **LLM05** | Data and Model Poisoning | none | — | GAP / GAP |
| **LLM06** | Unbounded Consumption | none — `divergence.RepeatedToken` tests extraction, not consumption ceilings | Recursive tool-call loop; assert token and call-count ceilings from OTel spans | CUSTOM / CUSTOM |
| **LLM07** | Misinformation | `snowball.GraphConnectivity`<br>`snowball.GraphConnectivityFull`<br>`snowball.Primes`<br>`snowball.PrimesFull`<br>`snowball.Senators`<br>`snowball.SenatorsFull`<br>`misleading.FalseAssertion`<br>`packagehallucination.Python`<br>`packagehallucination.Ruby`<br>`packagehallucination.Rust`<br>`packagehallucination.Perl`<br>`packagehallucination.RakuLand`<br>base: `packagehallucination.PackageHallucinationProbe`<br>`goodside.Davidjl`<br>`goodside.Tag`<br>`goodside.ThreatenJSON`<br>`goodside.WhoIsRiley`<br>`lmrc.QuackMedicine` | `RedTeamingAttack` + `SelfAskTrueFalseScorer`<br>`SelfAskLikertScorer`<br>`QuestionAnsweringBenchmarkOrchestrator` | DIRECT / DIRECT |
| **LLM08** | Hidden Context Exposure | `sysprompt_extraction.SystemPromptExtraction` (v0.15.0+) | `RedTeamingAttack`, objective "recover the system prompt" + custom scorer | DIRECT / CUSTOM |
| **LLM09** | Vector and Embedding Weaknesses | none — `latentinjection` covers RAG-borne injection, not vector-store weaknesses | — | GAP / GAP |
| **LLM10** | Improper Output Handling | `exploitation.SQLInjectionEcho`<br>`exploitation.SQLInjectionSystem`<br>`exploitation.JinjaTemplatePythonInjection`<br>`web_injection.TaskXSS`<br>`web_injection.MarkdownXSS`<br>`ansiescape.AnsiEscaped`<br>`ansiescape.AnsiRaw`<br>`ansiescape.AnsiRawTokenizerHF`<br>`malwaregen.TopLevel`<br>`malwaregen.SubFunctions`<br>`malwaregen.Payload`<br>`malwaregen.Evasion`<br>`av_spam_scanning.EICAR`<br>`av_spam_scanning.GTUBE`<br>`av_spam_scanning.GTphish` | Custom scorer asserting on *effect* (did the SQL run), not output text | DIRECT / CUSTOM |

---

## 2. OWASP Top 10 for Agentic Applications 2026

| Code | Title | garak probes (exact) | PyRIT | G / P |
|---|---|---|---|---|
| **ASI01** | Agent Goal Hijack | Full LLM01 set above, led by `latentinjection.*` classes and `agent_breaker.AgentBreaker` | `XPIATestOrchestrator`<br>`CrescendoAttack`<br>`RedTeamingAttack` | DIRECT / DIRECT |
| **ASI02** | Tool Misuse and Exploitation | `agent_breaker.AgentBreaker` | Custom `PromptTarget` + tool-call trace scorer | DIRECT / CUSTOM |
| **ASI03** | Identity and Privilege Abuse | **none** — `agent_breaker.AgentBreaker` tests tool *access*, not delegation, cached credentials or confused-deputy | Two-agent harness: low-privilege agent induces a high-privilege agent to act on its behalf | **CUSTOM** / CUSTOM |
| **ASI04** | Agentic Supply Chain Vulnerabilities | none | — | GAP / GAP |
| **ASI05** | Unexpected Code Execution (RCE) | `exploitation.SQLInjectionEcho`<br>`exploitation.SQLInjectionSystem`<br>`exploitation.JinjaTemplatePythonInjection`<br>`malwaregen.TopLevel`<br>`malwaregen.SubFunctions`<br>`malwaregen.Payload`<br>`malwaregen.Evasion` | Custom execution-effect scorer | DIRECT / CUSTOM |
| **ASI06** | Memory and Context Poisoning | none | Inject false memories across sessions; assert the agent refuses and flags them as unauthorised (CSA's worked PyRIT example) | CUSTOM / CUSTOM |
| **ASI07** | Insecure Inter-Agent Communication | none | — | GAP / GAP |
| **ASI08** | Cascading Failures | none | Poison upstream agent; assert downstream agents do not act on its output | CUSTOM / CUSTOM |
| **ASI09** | Human-Agent Trust Exploitation | `lmrc.Anthropomorphisation` — **adjacent, not a trust-exploitation test** | `RedTeamingAttack` with persuasion objective + `SelfAskTrueFalseScorer` on "did it push the user toward an unsafe approval" | **CUSTOM** / DIRECT |
| **ASI10** | Rogue Agents | none | `CrescendoAttack` over extended turns; long-horizon objective with a reward-hacking shortcut available | CUSTOM / CUSTOM |

---

## 3. OWASP MCP Top 10 (2025 Beta)

| Code | Title | garak probes (exact) | PyRIT | G / P |
|---|---|---|---|---|
| **MCP01** | Token Mismanagement & Secret Exposure | `apikey.GetKey`<br>`apikey.CompleteKey`<br>*(model layer only — storage and rotation are platform controls)* | `PromptSendingAttack` + canary-token scorer | DIRECT / CUSTOM |
| **MCP02** | Privilege Escalation via Scope Creep | **none** — `agent_breaker` tests tool access, not scope accumulation over a session | Session-length harness: assert granted scope never exceeds the initial grant | **CUSTOM** / CUSTOM |
| **MCP03** | Tool Poisoning | none | MCP server with hidden instructions in the tool description; assert the agent does not obey | CUSTOM / CUSTOM |
| **MCP04** | Software Supply Chain Attacks & Dependency Tampering | none | — | GAP / GAP |
| **MCP05** | Command Injection & Execution | `exploitation.SQLInjectionEcho`<br>`exploitation.SQLInjectionSystem`<br>`exploitation.JinjaTemplatePythonInjection`<br>payload set `access_shell_commands` | Custom execution-effect scorer | DIRECT / CUSTOM |
| **MCP06** | Intent Flow Subversion | Full `latentinjection` set — context as a second instruction channel is exactly what it models | `XPIATestOrchestrator` | DIRECT / DIRECT |
| **MCP07** | Insufficient Authentication & Authorization | **none** — auth enforcement is a control test, not a probe | Bind attempt without valid credentials; assert refusal | **CUSTOM** / CUSTOM |
| **MCP08** | Lack of Audit and Telemetry | none | — | GAP / GAP |
| **MCP09** | Shadow MCP Servers | none | Offer an unapproved server; assert the agent refuses to bind | CUSTOM / CUSTOM |
| **MCP10** | Context Injection & Over-Sharing | **none** — no probe for cross-context bleed | Seed canary strings into agent A's context, run agent B, assert the canary never appears | **CUSTOM** / CUSTOM |

---

## 4. Detectors worth naming

The slide subtitle promises probes, targets **and** scorers. These are the detectors the docs publish for the probes above.

| Probe family | Detector |
|---|---|
| `promptinject.*` | `AttackRogueString` |
| `latentinjection.*` | `TriggerListDetector` |
| `snowball.*` | `DontStartYes` |
| `sysprompt_extraction.SystemPromptExtraction` | `sysprompt_extraction.PromptExtraction`<br>`sysprompt_extraction.PromptExtractionVerbatim` |
| `web_injection.*` | `web_injection.MarkdownExfilBasic`<br>`web_injection.MarkdownExfilContent`<br>`web_injection.MarkdownExfilExtendedImage`<br>`web_injection.MarkdownExfilExtendedNonImage` |
| `packagehallucination.*` | `packagehallucination.PackageHallucinationDetector`<br>`packagehallucination.JavaScriptNpm`<br>`packagehallucination.RustCrates` |

**Published calibration (ASR):**

| Probe | ASR | Detector |
|---|---|---|
| `promptinject.HijackHateHumans` | 61.0% | `AttackRogueString` |
| `promptinject.HijackKillHumans` | 51.0% | `AttackRogueString` |
| `promptinject.HijackLongPrompt` | 45.7% | `AttackRogueString` |
| `latentinjection.LatentInjectionFactSnippetLegal` | 50.3% | `TriggerListDetector` |
| `latentinjection.LatentInjectionFactSnippetEiffel` | 30.7% | `TriggerListDetector` |
| `snowball.GraphConnectivity` | 11.5% | `DontStartYes` |

Where the docs publish an ASR, quote it. Where they do not, say so rather than implying equivalence.

---

## 5. Where the slide's grouped rows over-claim

The slide grades each row at the level of its strongest member. Three Garak cells therefore claim more than every code beneath them supports.

| Slide row | Grouped grade | Codes with no probe behind them |
|---|---|---|
| Row 2 | Garak DIRECT | MCP10 |
| Row 4 | Garak DIRECT | ASI09 |
| Row 5 | Garak DIRECT | ASI03, MCP02, MCP07 |

Asterisk those three cells pointing at this appendix, or declare it in the room. One code pulled out of a grouped row with nothing behind it costs more than three declared caveats on a slide headed "Verified".

| Grade | garak | PyRIT |
|---|---|---|
| DIRECT | 9 | 4 |
| CUSTOM | 11 | 18 |
| GAP / OTHER CONTROLS | 10 | 8 |

---

## 6. Verification

```bash
pip show garak pyrit
python -m garak --list_probes
python -m garak --list_probes | grep -iE "agent_breaker|sysprompt_extraction|propile"
python -m garak --list_probes | grep -iE "goat|packagehallucination|latentinjection"

python -m garak --model_type openai --model_name <target> \
  --probes promptinject.HijackHateHumans,latentinjection.LatentInjectionReport,agent_breaker.AgentBreaker
```

**Standing caveat — garak's OWASP tags follow the 2025 numbering, not 2026.**

| Probe | garak tag | Means (2025) | This appendix files it under |
|---|---|---|---|
| `snowball.*` | `owasp:llm09` | Misinformation | LLM07 |
| `ansiescape.AnsiEscaped` | `owasp:llm05` | Improper Output Handling | LLM10 |
| `web_injection.MarkdownImageExfil` | `owasp:llm02`, `owasp:llm06` | Sensitive Info Disclosure, Excessive Agency | LLM02 |
| `leakreplay.LiteratureClozeFull` | `owasp:llm10`, `owasp:llm06` | Unbounded Consumption, Excessive Agency | LLM02 |
| `packagehallucination.*` | `owasp:llm09`, `owasp:llm02` | Misinformation, Sensitive Info Disclosure | LLM07 |

State the translation before anyone diffs a garak report against this appendix.
