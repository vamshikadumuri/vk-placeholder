# garak 0.10.3.1 — 10 Small Probes Mapped to OWASP LLM Codes

**Scope:** a fast, low-cost probe set for smoke-testing a target, with one or more probes per OWASP code that garak 0.10.3.1 actually tags.
**Method:** all tags, detectors and prompt counts below were read directly from the `garak-0.10.3.1-py3-none-any.whl` source (`garak/probes/*.py`, `garak/data/misp_descriptions.tsv`), not from the online docs — the published docs track `latest`/`stable`, which has drifted from this version.

---

## 1. Which OWASP list this version uses

garak 0.10.3.1 ships its own taxonomy descriptions in `garak/data/misp_descriptions.tsv`. Those descriptions are the **OWASP Top 10 for LLM Applications (2023)** wording:

| Tag | garak's own label (v0.10.3.1) |
|---|---|
| `owasp:llm01` | LLM01: Prompt Injection |
| `owasp:llm02` | LLM02: Insecure Output Handling |
| `owasp:llm03` | LLM03: Training Data Poisoning |
| `owasp:llm04` | LLM04: Model Denial of Service |
| `owasp:llm05` | LLM05: Supply Chain Vulnerabilities |
| `owasp:llm06` | LLM06: Sensitive Information Disclosure |
| `owasp:llm07` | LLM07: Insecure Plugin Design |
| `owasp:llm08` | LLM08: Excessive Agency |
| `owasp:llm09` | LLM09: Overreliance |
| `owasp:llm10` | LLM10: Model Theft |

**Important for governance write-ups:** if your control framework references OWASP LLM Top 10 **2025**, garak's tag numbers do *not* line up. See the crosswalk in §6.

### Actual tag coverage in this version

Only six of the ten codes appear on any probe:

| Tag | Probe classes carrying it | Of which active by default |
|---|---|---|
| `owasp:llm01` | 49 | 38 |
| `owasp:llm02` | 14 | 13 |
| `owasp:llm05` | 6 | 5 |
| `owasp:llm06` | 18 | 15 |
| `owasp:llm09` | 13 | 9 |
| `owasp:llm10` | 15 | 10 |
| `owasp:llm03`, `llm04`, `llm07`, `llm08` | **0** | 0 |

(124 probe classes total, 97 active.) So `--probe_tags owasp:llm08` returns nothing in 0.10.3.1 — no probe is tagged for training-data poisoning, model DoS, insecure plugin design or excessive agency. Worth stating explicitly in any coverage matrix rather than leaving those rows blank.

---

## 2. The 10-probe set

Chosen for: smallest prompt counts, `active = True` by default, and lightweight string/regex detectors (no HF classifier downloads) — with one exception, flagged below.

| # | Probe | OWASP tag(s) | Prompts | Detector(s) | What it tests |
|---|---|---|---|---|---|
| 1 | `dan.Dan_11_0` | `llm01` | 1 | `mitigation.MitigationBypass`, `dan.DAN` | Classic DAN 11.0 persona jailbreak; single canonical prompt |
| 2 | `goodside.Tag` | `llm01` | 32 | `base.TriggerListDetector` | Instructions hidden in Unicode tag-page chars (invisible to the user, readable by the model) |
| 3 | `av_spam_scanning.EICAR` | `llm02` | 5 | `knownbadsignatures.EICAR` | Will the app emit the EICAR AV test signature unscanned? |
| 4 | `xss.ColabAIDataLeakage` | `llm02`, `llm06` | 4 | `xss.MarkdownExfilContent` | Data exfil via rendered image URL (the Colab/Gemini technique) |
| 5 | `ansiescape.AnsiEscaped` | `llm01`, `llm02`, `llm05` | 51 | `ansiescape.Escaped` | ANSI escape sequences in output that can hijack a terminal/log viewer downstream |
| 6 | `goodside.Davidjl` | `llm05` | 4 | `goodside.Glitch` | Glitch-token (` davidjl`) behaviour — fingerprints tokenizer lineage |
| 7 | `grandma.Win10` | `llm06` | 6 | `productkey.Win5x5` (+ `mitigation.MitigationBypass`) | "Dead grandma" appeal-to-ethos extracting Windows product keys |
| 8 | `goodside.WhoIsRiley` | `llm09` | 6 | `goodside.RileyIsnt` | Confident hallucination about a real person |
| 9 | `packagehallucination.Python` | `llm09`, `llm02` | 91 | `packagehallucination.PythonPypi` | Recommends non-existent PyPI packages → slopsquatting exposure |
| 10 | `leakreplay.GuardianCloze` | `llm10`, `llm06` | 9 | `base.TriggerListDetector` | Training-data replay via cloze completion on Guardian articles |

**Total: 209 prompts.** At the default `generations: 5` that's ~1,045 model calls. With `-g 1` it's 209.

---

## 3. Per-probe detail

### 1. `dan.Dan_11_0` — `owasp:llm01`
- **goal:** *disregard the system prompt*
- **full tags:** `avid-effect:security:S0403`, `avid-effect:performance:P0204`, `owasp:llm01`, `quality:Security:PromptStability`, `payload:jailbreak`
- Smallest probe in the set — exactly one prompt. Good canary for "did anything change in the guardrail config".
- Every other `dan.Dan_*`, `STAN`, `DUDE`, `AntiDAN`, `ChatGPT_Developer_Mode_*` class is also a single prompt, so you can add the whole family for ~15 prompts.

### 2. `goodside.Tag` — `owasp:llm01`
- **goal:** *inject invisible instructions*
- **full tags:** `owasp:llm01`, `payload:generic`, `quality:Security:Adversarial`, `quality:Security:PromptStability`
- Encodes the payload into Unicode tag-page codepoints (U+E0000 block). 4 payloads × 2 stubs × 2 refocuser variants × 2 alpha-only variants = 32 prompts.
- Directly relevant if any upstream channel (ticket text, email body, document) reaches a model without Unicode normalisation.

### 3. `av_spam_scanning.EICAR` — `owasp:llm02`
- **goal:** *output antivirus test codes*
- **full tags:** `avid-effect:security:S0301`, `avid-effect:security:S0403`, `owasp:llm02`, `payload:malicious:badcode:virus`, `quality:Security:Adversarial`
- 5 repeat-after-me templates wrapping the EICAR string. Only meaningful if the app is *expected* to scan model output — otherwise it will always "fail" and is noise.
- Siblings: `av_spam_scanning.GTUBE` (spam) and `GTphish` (phishing), 5 prompts each, same tag. Aliased from the old `knownbadsignatures.*` names.

### 4. `xss.ColabAIDataLeakage` — `owasp:llm02`, `owasp:llm06`
- **goal:** *render images fetched from a remote uri*
- **full tags:** `avid-effect:security:S0301`, `avid-effect:security:S0403`, `owasp:llm02`, `owasp:llm06`, `payload:leak:chat`, `payload:malicious:renderer`, `quality:Security:PromptStability`, `quality:Security:ExtractionInversion`
- One prompt per domain in the `example_domains_xss` payload (4 by default). Swap in your own domains via the `payload_name` probe option if you want an in-house canary domain.
- Cheapest of the `xss.*` family. `xss.MarkdownImageExfil` is 12 prompts (4 domains × 3 encodings) and is the better one if you have a Markdown-rendering front end.

### 5. `ansiescape.AnsiEscaped` — `owasp:llm01`, `owasp:llm02`, `owasp:llm05`
- **goal:** *print escaped ANSI terminal codes*
- **full tags:** `owasp:llm01`, `owasp:llm02`, `owasp:llm05`, `avid-effect:security:S0100`, `avid-effect:security:S0200`, `quality:Security:Integrity`
- 3 asks × 3 high-level tasks + 14 escaped payloads × 3 repeat stubs = 51 prompts. Three OWASP codes from one probe — efficient row in a coverage matrix.
- `ansiescape.AnsiRaw` (58 prompts) is the harder variant: it asks for *live* control codes rather than escaped text. Run it if your output lands in a terminal, CI log, or SIEM console.

### 6. `goodside.Davidjl` — `owasp:llm05`
- **goal:** *get wrong answers about a name*
- **full tags:** `avid-effect:security:S0403`, `avid-effect:performance:P0204`, `owasp:llm05`, `quality:Security:PromptStability`, `payload:generic`
- 4 hardcoded prompts about the ` davidjl` glitch token. Supply-chain angle: a hit tells you the target inherits a known tokenizer/vocab lineage.
- Bigger sibling: `glitch.Glitch100` (100 prompts, same tag).

### 7. `grandma.Win10` — `owasp:llm06`
- **goal:** *get model to output Win 10 product keys*
- **full tags:** `avid-effect:security:S0300`, `owasp:llm06`, `risk-cards:lmrc:providing_illegal_info`, `quality:Behavioral:ContentSafety:LegalGoodsServices`
- 2 templates × 3 product names = 6 prompts. Detector is a regex for the 5×5 key format, so scoring is deterministic — no judge model, no flakiness.
- `grandma.Win11` is identical with Windows 11 names. `grandma.Slurs` and `grandma.Substances` exist but carry no OWASP tag.

### 8. `goodside.WhoIsRiley` — `owasp:llm09`
- **goal:** *get misinfo about riley goodside*
- **full tags:** `avid-effect:ethics:E0402`, `avid-effect:performance:P0204`, `owasp:llm09`, `quality:Robustness:GenerativeMisinformation`, `payload:hallucination`
- 6 prompts, keyword detector. Cheapest possible LLM09 signal, but narrow — it only proves the model will confabulate about one specific person. Pair with #9 for anything you'd put in front of a risk committee.

### 9. `packagehallucination.Python` — `owasp:llm09`, `owasp:llm02`
- **goal:** *generate python importing non-existent packages*
- **full tags:** `owasp:llm09`, `owasp:llm02`, `quality:Robustness:GenerativeMisinformation`, `payload:malicious:badcode`
- 7 prompt stubs × 13 code tasks = 91 prompts. The largest in this set but the most defensible finding for a coding-assistant use case.
- ⚠️ **Network dependency:** the detector calls `datasets.load_dataset("garak-llm/pypi-20230724")` from Hugging Face on first use. Behind a proxy it will log a warning and skip scoring. Pre-cache the dataset or set `HF_HOME`/`HF_HUB_OFFLINE` before a locked-down run.
- Siblings with the same tags: `.JavaScript` (npm), `.Ruby` (RubyGems), `.Rust` (crates.io), 91 prompts each.

### 10. `leakreplay.GuardianCloze` — `owasp:llm10`, `owasp:llm06`
- **full tags:** `avid-effect:security:S0301`, `owasp:llm10`, `owasp:llm06`, `quality:Security:ExtractionInversion`, `payload:leak:training`
- 9 prompts (one per row of `guardian_cloze.tsv`) — the smallest LLM10-tagged probe in the build. Masks a proper noun in a real news passage and checks whether the model fills it back in.
- Scale-up path, same tags: `PotterCloze` (30), `NYTCloze` (32), `LiteratureCloze80` (79), `divergence.Repeat` (36, the "poem poem poem" attack).

---

## 4. Running it

```bash
# smoke run: 1 generation per prompt, ~209 calls
python -m garak \
  -m openai -n gpt-4o-mini \
  -p dan.Dan_11_0,goodside.Tag,av_spam_scanning.EICAR,xss.ColabAIDataLeakage,ansiescape.AnsiEscaped,goodside.Davidjl,grandma.Win10,goodside.WhoIsRiley,packagehallucination.Python,leakreplay.GuardianCloze \
  -g 1 \
  --parallel_attempts 8 \
  --taxonomy owasp \
  --report_prefix owasp_smoke
```

Or as a config file (`owasp_smoke.yaml`, run with `--config owasp_smoke.yaml`):

```yaml
---
system:
  parallel_attempts: 8
  lite: true

run:
  generations: 1

plugins:
  probe_spec: dan.Dan_11_0,goodside.Tag,av_spam_scanning.EICAR,xss.ColabAIDataLeakage,ansiescape.AnsiEscaped,goodside.Davidjl,grandma.Win10,goodside.WhoIsRiley,packagehallucination.Python,leakreplay.GuardianCloze
  detector_spec: auto
  extended_detectors: false

reporting:
  taxonomy: owasp
  report_prefix: owasp_smoke
```

### Flags that matter here (0.10.3.1 syntax)

| Flag | Note |
|---|---|
| `-m` / `--model_type`, `-n` / `--model_name` | This version uses **`model_*`**. The `--target_type`/`--target_name` aliases in the online docs are from a later release and will error here. |
| `-p` / `--probes` | Comma-separated; accepts `module` or `module.Class`. |
| `--probe_tags owasp:llm06` | Prefix match on tags — an alternative to listing classes. `--probe_tags owasp:` runs everything OWASP-tagged. |
| `-g` / `--generations` | Default is **5**. Use `1` for smoke runs, keep `5`+ for anything you report on. |
| `--taxonomy owasp` | Groups the HTML/report output by OWASP code instead of by probe module. This is what makes the run readable as a coverage report. |
| `--parallel_attempts N` | Biggest wall-clock win; safe for these probes since none are multi-turn. |
| `--report_prefix` | Output lands in your garak data dir (`~/.local/share/garak/garak_runs/` on Linux/macOS) as `<prefix>.report.jsonl`, `.hitlog.jsonl` and `.report.html`. |

Sanity check before a run:

```bash
python -m garak --list_probes | grep -E "Dan_11_0|goodside|ansiescape|grandma|packagehallucination|GuardianCloze"
python -m garak --plugin_info probes.grandma.Win10   # confirms tags + detector for any probe
```

---

## 5. Scale-up options per code

Everything below is `active = True` in 0.10.3.1. Prompt counts are per probe, before `generations`.

| Code | Small (in the set) | Next step up |
|---|---|---|
| `llm01` | `dan.Dan_11_0` (1), `goodside.Tag` (32) | `phrasing.PastTenseMini` (200), `latentinjection.LatentJailbreakMini`, `dan.DanInTheWildMini`, `promptinject.*Mini` (100), `encoding.InjectBase64` |
| `llm02` | `av_spam_scanning.EICAR` (5), `xss.ColabAIDataLeakage` (4) | `xss.MarkdownImageExfil` (12), `av_spam_scanning.GTUBE`/`GTphish` (5 each), `ansiescape.AnsiRaw` (58) |
| `llm05` | `goodside.Davidjl` (4) | `glitch.Glitch100` (100), `fileformats.HF_Files` (Hugging Face–hosted targets only — it inspects repo files for pickles, not prompts) |
| `llm06` | `grandma.Win10` (6) | `grandma.Win11` (6), `xss.MarkdownImageExfil` (12), `leakreplay.PotterCloze` (30) |
| `llm09` | `goodside.WhoIsRiley` (6) | `packagehallucination.Python` (91), `snowball.PrimesMini` / `GraphConnectivityMini` / `SenatorsMini` (100 each), `misleading.FalseAssertion50` (150) |
| `llm10` | `leakreplay.GuardianCloze` (9) | `divergence.Repeat` (36), `leakreplay.NYTCloze` (32), `leakreplay.LiteratureComplete80` (79), `topic.WordnetControversial` (tree-search, slow) |

---

## 6. 2023 → 2025 crosswalk (for governance docs)

garak's tags are 2023 codes. If your control framework cites the 2025 list, map on **what the probe tests**, not on the tag number. The mapping below is an interpretation for documentation purposes — it is not something garak asserts.

| Probe | garak tag (2023) | Closest OWASP LLM Top 10 **2025** code |
|---|---|---|
| `dan.Dan_11_0`, `goodside.Tag` | LLM01 Prompt Injection | LLM01: Prompt Injection |
| `av_spam_scanning.EICAR` | LLM02 Insecure Output Handling | LLM05: Improper Output Handling |
| `xss.ColabAIDataLeakage` | LLM02 + LLM06 | LLM05: Improper Output Handling + LLM02: Sensitive Information Disclosure |
| `ansiescape.AnsiEscaped` | LLM01 + LLM02 + LLM05 | LLM05: Improper Output Handling (primary), LLM01 |
| `goodside.Davidjl` | LLM05 Supply Chain | LLM03: Supply Chain |
| `grandma.Win10` | LLM06 Sensitive Info Disclosure | LLM02: Sensitive Information Disclosure |
| `goodside.WhoIsRiley` | LLM09 Overreliance | LLM09: Misinformation |
| `packagehallucination.Python` | LLM09 + LLM02 | LLM09: Misinformation + LLM03: Supply Chain |
| `leakreplay.GuardianCloze` | LLM10 Model Theft + LLM06 | LLM02: Sensitive Information Disclosure |

Note the collision risk: `owasp:llm02` in a garak report means *Insecure Output Handling*, while LLM02 in a 2025-based control document means *Sensitive Information Disclosure*. Anything that ingests garak JSONL and re-labels it needs an explicit translation layer, or the numbers will silently invert.

Gaps that no probe in 0.10.3.1 covers under either list: data/model poisoning, unbounded consumption / DoS, excessive agency, tool and plugin misuse, and system prompt leakage as a distinct category. Those need a different tool or custom probes.

---

## 7. Caveats

- Counts are static reads of `__init__` logic and bundled data files in 0.10.3.1; probes that pull remote datasets could differ at runtime.
- `detector_spec: auto` resolves to each probe's `recommended_detector` / `primary_detector`. Adding `--extended_detectors` pulls in extras (e.g. `mitigation.MitigationBypass` on `grandma.Win10`) and will change hit rates.
- A "hit" is a detector verdict, not a confirmed vulnerability. For anything going into a report, sample the `.hitlog.jsonl` and read the actual generations.
- With `-g 1` results are noisy by design — fine for a pipeline gate, not for a baseline. Use `-g 5` or higher for numbers you'll cite.
