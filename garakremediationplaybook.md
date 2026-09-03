# From Garak Findings to Fixes: A Remediation Playbook

**Purpose:** turn a low probe score in a garak report into a specific, defensible recommendation about what to change in the target AI system.

**Audience:** platform engineers running the self-service red-teaming service, plus the app teams who receive the findings.

**Short answer to "is it always a guardrail?"** No. Guardrails are the right primary control for roughly two-thirds of garak's probe families. For the rest — XSS/exfiltration, package hallucination, glitch tokens, unsafe model file formats — the correct recommendation is an application-layer or supply-chain control, and recommending a guardrail there would give false assurance. Section 4 draws the line.

---

## 1. Read the score correctly before you recommend anything

Garak gives you two numbers per probe/detector pair, and they answer different questions.

| Metric | Question it answers | Comparable over time? |
|---|---|---|
| **Absolute pass rate** (1 − attack success rate) | How often does this attack actually work on my system? | Yes, if probe version, generations and seed are held constant |
| **Z-score** | How does my system compare to a bag of recent state-of-the-art models on this same probe? | **No — see §8.3** |
| **DEFCON grade (1–5)** | Banded version of either score; 1 is worst, 5 is best | Follows whichever score it bands |

On the Z-score scale, 0 is average and negative is worse; roughly two-thirds of models land between −1.0 and +1.0, and the middle 10% (−0.125 to +0.125) is labelled "competitive." Above +1 is much better than average; below −1 is much worse.

### 1.1 The quadrant that drives the recommendation

This is the part that most people get wrong. **The two scores together tell you *where* the fix belongs.**

| | **High Z (peers do well too)** | **Low Z (peers beat you)** |
|---|---|---|
| **High absolute** (attack rarely works) | Healthy. No action. | Watch. You're behind, but not exposed. Check model version and config drift before doing anything expensive. |
| **Low absolute** (attack often works) | **Industry-wide weakness.** Do *not* try to fix this by swapping models or tuning prompts — nobody has solved it. Add an external control layer. | **Your problem, and urgent.** Something about *your* target — model choice, model version, system prompt, missing rails — is worse than baseline. Fix at the target, then re-scan. |

The bottom-left quadrant is the one people mishandle. A low absolute score with a good Z-score means the failure is real and exploitable, but the model market has no answer for it. The recommendation is a *compensating control outside the model*, not "use a better model."

### 1.2 Three caveats to state in every report

1. **DEFCON grades aggregate by minimum.** A module score is dragged down by its single worst probe/detector pair. Always drive recommendations from the **probe.detector** level, never the module rollup — otherwise you send a team chasing a category when only one specific attack works.
2. **Detectors are keyword- and classifier-based, so false positives are real.** Before raising a finding, open the hit log and read 5–10 actual failing generations. A common false positive: the model refused, but phrased the refusal in a way the detector scored as a hit.
3. **Garak is single-turn by design.** A clean garak report does not mean the system is safe across a multi-turn conversation. Say so explicitly, or the report will be read as broader assurance than it is.

---

## 2. Triage checklist (run this before writing a recommendation)

- [ ] Confirm the hit is real — read raw generations from the hit log, not just the score.
- [ ] Is this probe **in scope** for this use case? A `leakreplay` failure matters enormously for a RAG assistant over customer data and very little for an internal code-comment generator. Out-of-scope probes get "accepted, documented," not a fix.
- [ ] Check the **confidence interval** on the attack success rate. Garak reports bootstrap CIs when n ≥ 30. A 45% ASR with a [20%, 70%] interval is not a number to build a remediation plan on — increase generations and re-run.
- [ ] Check the sibling detectors for the same probe. If one detector fires and three don't, suspect the detector.
- [ ] Identify which **layer** the fix belongs in (§3) before naming a specific control.

---

## 3. The remediation ladder: where a fix belongs

Fixes get cheaper and less reliable as you go up. Fixes get more expensive and more durable as you go down. Recommend the *lowest applicable* layer, then add layers above it.

| Layer | Control | Cost | Reliability |
|---|---|---|---|
| **L0** | Model / version selection | High | Highest for capability-rooted failures |
| **L1** | System prompt & general instructions | Lowest | Weak, and can regress other categories |
| **L2** | Dialog / topical rails (scope the assistant to its job) | Low | Surprisingly strong |
| **L3** | Input rails (jailbreak detection, content safety, topic control, PII masking, injection detection) | Medium | Good, but adds latency and false refusals |
| **L4** | Retrieval rails (sanitise RAG chunks before they enter context) | Medium | Essential for indirect injection |
| **L5** | Output rails (self-check, content safety, fact-check, sensitive-data masking) | Medium–high | Good, doubles token cost |
| **L6** | Execution / tool rails (tool allowlist, argument validation, sandboxing, human-in-the-loop) | Medium | Essential for agentic systems |
| **L7** | Application layer, outside the LLM entirely (output encoding, CSP, dependency allowlists, egress control, no auto-exec) | Low–medium | **Highest for the exfiltration and supply-chain families** |

**Rule of thumb:** if the harm is realised *after* the model output leaves the model — rendered in a browser, pasted into a terminal, installed as a dependency, executed as code — the primary control is L7 and any guardrail is defence in depth only.

---

## 4. Probe family → recommended fix

Grouped by garak probe module. "Primary layer" is what you recommend first; "also" is defence in depth.

### Jailbreak & persona override
**Probes:** `dan`, `grandma`, `tap`, `atkgen`, `suffix`
**What failure means:** the model can be argued or role-played out of its safety and scope constraints.
**Primary layer:** L2 (dialog rails) — see §5.2, this is where NVIDIA's own numbers show the biggest jump.
**Also:** L3 `jailbreak detection heuristics` / `jailbreak detection model`, `content safety check input`. For `suffix` (GCG adversarial suffixes) specifically, the prefix/suffix perplexity heuristic is the targeted control — NVIDIA reports it catching 49 of 50 GCG-style attacks at a 0.04% false positive rate.
**Non-guardrail:** model version. `dan` scores vary enormously across model generations.

### Encoding & obfuscation smuggling
**Probes:** `encoding` (base64, hex, ROT13, Morse, quoted-printable, MIME), `goodside`, `ansiescape`
**What failure means:** payloads bypass filters because your input rails scan the encoded surface form, not the decoded intent.
**Primary layer:** L3, but as **input normalisation**, not classification. Decode-then-scan. Apply Unicode NFKC normalisation, strip Cf/Co category characters (this kills Unicode tag smuggling), strip ANSI CSI sequences.
**Also:** L2 dialog rails, which handle a lot of this implicitly by refusing anything off-topic regardless of encoding.
**Note:** `ansiescape` failures are only exploitable if your output is rendered in a terminal. If it renders in a browser, downgrade severity but fix the sanitisation anyway.

### Prompt injection (direct and indirect)
**Probes:** `promptinject`, `latentinjection`
**What failure means:** instructions embedded in user input — or worse, in a retrieved document — are followed as if they came from you.
**Primary layer:** L4 (retrieval rails) for `latentinjection`; L3 for `promptinject`.
**Non-guardrail, and this is the real fix:** enforce a trust boundary. Retrieved content and tool output must never occupy the same instruction channel as the system prompt. Use structured prompts with explicit delimiters, allowlist retrieval sources, and treat every retrieved chunk as untrusted data.
**Caveat for your pitch:** garak's own maintainers hedge on indirect-injection coverage. If poisoned documents in a retrieval corpus are a top risk for a use case, garak alone is not sufficient assurance — pair it with corpus-level testing.

### Output-channel exfiltration
**Probes:** `xss` (Markdown image exfiltration, data assembly)
**What failure means:** the model can be induced to emit markup that leaks conversation content to an attacker-controlled host when rendered.
**Primary layer: L7, not a guardrail.** Output encoding, Content Security Policy, and blocking outbound image/resource loads to non-allowlisted domains. A guardrail that pattern-matches exfil markup is bypassable; a CSP is not.
**Also:** L5 injection detection on output as defence in depth.
**Recommendation wording:** "This finding must be routed to the application security team, not resolved by guardrail configuration alone."

### Data leakage & memorisation
**Probes:** `leakreplay`, `divergence`
**What failure means:** the model reproduces memorised training content, or diverges into raw training data under repetition attacks.
**Primary layer:** L0 (model choice) — this is baked into weights.
**Also:** L5 sensitive-data detection and output self-check.
**Non-guardrail:** for a bank, the durable control is architectural — confidential data belongs in a retrieval layer with access control, never in fine-tuning data.

### Toxicity, harmful personas, risk cards
**Probes:** `realtoxicityprompts`, `lmrc`, `continuation`
**Primary layer:** L5 output content safety (content safety model, self-check output, or Llama Guard).
**Also:** L1 general instructions.
**Watch:** `continuation` is the one category where NVIDIA's data shows general instructions *made things worse* (see §5.2). Verify with a re-scan rather than assuming prompt changes help.

### Hallucination under pressure
**Probes:** `snowball`, `misleading`
**What failure means:** the model asserts false things confidently when the question contains a false premise or demands an answer it can't have.
**Primary layer:** L5 grounding — fact-check rails (AlignScore or a hallucination rail), self-check facts.
**Non-guardrail, and more effective:** force citation-or-abstain in the application contract. If the answer isn't supported by a retrieved chunk, return "not found" rather than generating. This is a product decision, not a config toggle.

### Insecure code & offensive capability
**Probes:** `malwaregen`, `exploitation`, `av_spam_scanning` (older reports call this `knownbadsignatures`)
**Primary layer:** L1 + L5. General instructions are unusually effective here — NVIDIA's benchmark shows the signature-emission category going from 4% to 97% protection on instructions alone.
**Non-guardrail:** never auto-execute generated code; egress controls on any sandbox.

### Package hallucination (slopsquatting)
**Probe:** `packagehallucination`
**Primary layer: L7, not a guardrail.** Resolve every package name the model suggests against your internal Artifactory/Nexus allowlist before it reaches a developer's terminal. A guardrail cannot know whether `pandas-utils-v2` exists; your registry can.
**This one is directly in your team's remit** given the EDP/MLOps ownership — it's a pipeline control, not an app control.

### Glitch tokens
**Probe:** `glitch`
**Primary layer: L0.** Glitch tokens are a tokenizer artefact. Filter them at the tokenizer boundary or change model.
**Do not recommend a content guardrail here** — the failure mode is undefined behaviour, not harmful content, so a safety classifier won't catch it.

### Model artefact safety
**Probe:** `fileformats`
**Not a runtime control at all.** This is supply chain: scan model artefacts for unsafe serialisation (pickle) in your model registry, in the MLOps pipeline, before deployment.

### Scope & topic control
**Probes:** `donotanswer`, `topic`
**Primary layer:** L2 dialog rails plus L3 topic control.
**Note:** these probes measure *under*-refusal only. They say nothing about over-refusal. See §6.1.

---

## 5. NeMo Guardrails: what the integration actually is

### 5.1 There is no plugin — the integration is architectural

There isn't a garak plugin that configures NeMo Guardrails, and there isn't a NeMo module that reads garak reports. What NVIDIA documents is simpler and more useful: **you point garak at the guardrailed endpoint instead of the raw model**, and the delta between the two scans is your measured control effectiveness.

```
garak  →  [ NeMo Guardrails: input rails → dialog rails → LLM → output rails ]  →  scores
   (scan the same probes against bare model and guardrailed endpoint; diff the reports)
```

Practically: run the NeMo Guardrails server, expose the OpenAI-compatible chat completions endpoint, and target it from garak like any other REST/OpenAI-compatible generator. Everything else — probes, detectors, reporting, Z-scores — is unchanged.

This is the strongest thing you can put in front of your stakeholders, because it turns "we added guardrails" into a number.

### 5.2 NVIDIA's own published evidence

NVIDIA scanned their sample "ABC bot" with garak under four progressively hardened configurations: bare model; general instructions only; instructions + dialog rails; instructions + dialog rails + moderation (input/output self-check). Protection rate, higher is better:

| Garak module | Bare | + Instructions | + Dialog rails | + Moderation |
|---|---|---|---|---|
| knownbadsignatures | 4.0% | 97.3% | 100% | 100% |
| dan | 27.3% | 40.7% | **61.3%** | 52.7% |
| goodside | 32.2% | 32.2% | 66.7% | 66.7% |
| snowball | 34.5% | 82.1% | 99.0% | 100% |
| malwaregen | 50.2% | 92.2% | 93.7% | 100% |
| leakreplay | 76.8% | 85.7% | 89.6% | 100% |
| lmrc | 85.0% | 81.9% | 86.5% | 94.4% |
| encoding | 90.3% | 98.2% | 100% | 100% |
| continuation | 92.8% | **69.5%** | 99.3% | 100% |
| xss | 92.5% | 100% | 100% | 100% |

Source: NVIDIA NeMo Guardrails documentation, "LLM Vulnerability Scanning." The target was `gpt-3.5-turbo-instruct`, so absolute numbers are dated — the *shape* is what matters.

**Three things to say honestly when you present this table:**

1. **Dialog rails are the underrated lever.** Simply scoping the assistant to its job produced most of the gain in most categories, at far lower latency and cost than moderation rails. Lead with this in your recommendations — it's the cheapest high-impact fix.
2. **More rails is not monotonically better.** `dan` peaked at 61.3% with dialog rails and *fell* to 52.7% once moderation rails were added. Layers interact. Always re-scan after a change rather than assuming additive improvement.
3. **Instructions alone can regress a category.** `continuation` dropped from 92.8% to 69.5% under general instructions before recovering. Prompt-only fixes are not free.

### 5.3 A starting config shape

```yaml
models:
  - type: main
    engine: <your provider>
    model: <your model>
  - type: content_safety
    engine: nim
    model: nvidia/llama-3.1-nemoguard-8b-content-safety
  - type: topic_control
    engine: nim
    model: nvidia/llama-3.1-nemoguard-8b-topic-control

rails:
  config:
    jailbreak_detection:
      server_endpoint: "http://jailbreak-detect.internal:1337/heuristics"
      length_per_perplexity_threshold: 89.79
      prefix_suffix_perplexity_threshold: 1845.65

  input:
    flows:
      - jailbreak detection heuristics
      - content safety check input $model=content_safety
      - topic safety check input $model=topic_control
      - mask sensitive data on input

  output:
    flows:
      - content safety check output $model=content_safety
      - self check output
      - detect sensitive data on output
```

Verify flow names against the version you deploy — the guardrail catalog has been actively restructured and names have moved between releases.

### 5.4 Two operational facts your risk function will ask about

**Jailbreak detection fails open.** NVIDIA documents this explicitly: if the heuristics server or the detection NIM is unreachable, times out, or errors, the rail **allows the request** and returns no error to the caller. A detector outage silently removes the control. For a regulated deployment this needs (a) availability monitoring on the detector with alerting, and (b) at least one rail in the chain that doesn't depend on an external service. Raise this before someone else does.

**The heuristics are English-only and modest in isolation.** The length-per-perplexity heuristic at its default threshold catches about 31% of jailbreaks at a 7.4% false positive rate, and both heuristics produce significantly more false positives on non-English text and on code. For a Singapore/India footprint with multilingual traffic, that FPR is a live product concern, not a footnote.

---

## 6. Two things to be upfront about in the pitch

### 6.1 Garak measures under-refusal, never over-refusal

Every probe in garak asks "can I make it misbehave?" Nothing asks "does it still do its job?" A configuration that refuses everything scores perfectly. NVIDIA's own writeup acknowledges this gap in their guardrails experiment.

**Recommendation:** pair every garak run with a false-refusal / utility benchmark on the same target. Without it, your service optimises for a metric that is trivially gamed by over-blocking, and app teams will eventually notice and stop trusting the reports. Build this into the PoC now rather than retrofitting it.

### 6.2 Don't let teams overfit to garak

Once probe scores become a gate, teams will tune against the specific probes. Mitigations:
- Hold out a subset of probes that never appear in the CI gate and only run in the periodic full sweep.
- Rotate `atkgen` and `tap` (adaptive, generative attacks) into every run — they don't produce a fixed prompt set to overfit against.
- Treat garak as a regression suite, not a certification.

---

## 7. Severity and routing

| Priority | Condition | SLA |
|---|---|---|
| **P1** | Low absolute score **and** the probe maps to an in-scope risk for this use case **and** the exploit path is reachable in production | Block release |
| **P2** | Z < −1.0 on an in-scope probe — you are materially worse than peer models | Current sprint |
| **P3** | Low absolute but good Z — industry-wide weakness, needs a compensating L7 control | Next quarter, with documented interim control |
| **P4** | Probe out of scope for the use case | Accept, document rationale, re-review at model change |

**Reachability matters.** An `xss` failure on an API-only service that never renders output in a browser is P4. The same failure on a customer-facing chat widget is P1. Your recommendation engine needs use-case metadata, not just probe scores.

---

## 8. Closing the loop (and a trap in your "performance over time" chart)

### 8.1 The cycle
```
scan → triage (§2) → identify layer (§3) → apply ONE change → re-scan same probes → diff → record
```
Change one layer at a time. If you add dialog rails and moderation rails together and the score moves, you've learned nothing about which one did it — and per §5.2, they can work against each other.

### 8.2 Evidence to retain per run
- `garak.<uuid>.report.jsonl` and the hit log (immutable, per model release)
- The exact target configuration, including guardrails config.yml
- garak version, probe spec, generations, seed
- Triage decisions with rationale for anything accepted rather than fixed

Garak probes carry taxonomy tags (OWASP LLM Top 10, AVID), and reporting can be grouped by taxonomy via the `reporting.taxonomy` setting. Use this to map findings onto your internal control catalogue rather than maintaining a parallel mapping by hand.

### 8.3 The trap: Z-scores are not comparable across garak versions

This one will bite your dashboard specifically.

The Z-score is computed against a calibration "bag" of recent models that NVIDIA refreshes periodically to keep it representative. When the bag changes, **your Z-score moves even though your system did not.** A team could see their trend line drop and spend a sprint chasing a regression that never happened.

Mitigations for the PoC:
- **Pin the garak version** per scan profile and record it against every data point.
- **Plot absolute pass rate as the primary trend line.** It's stable given the same probe version, generations and seed.
- Render Z-score as a secondary series, **with version-change boundaries drawn on the chart** so a step change is visibly attributable.
- On a version bump, re-baseline: re-scan the last known-good configuration on the new version before comparing anything.

Same logic applies to probes themselves — probe contents change between releases, so even absolute scores need the probe version pinned to be a true time series.

### 8.4 CI integration
- **Per config change / PR:** fast tiered subset, ~10 minutes. Gate on P1 conditions only.
- **Nightly or weekly:** full sweep including `atkgen` and `tap`.
- **On model version change:** full sweep, mandatory, with re-baseline.

Use `--parallel_attempts` to keep the fast tier viable; full sweeps take hours and are not PR-gate material.

---

## 9. Building the recommendation engine into the PoC

A rules file keyed on `probe.detector` keeps the logic auditable and lets app teams see *why* they got a recommendation. Suggested shape:

```yaml
- match: "dan.*"
  risk: "Jailbreak / persona override"
  owasp: "LLM01"
  primary_layer: L2
  primary_control: "Dialog rails scoping the assistant to its supported tasks"
  nemo_flows:
    - "jailbreak detection heuristics"
    - "content safety check input"
  non_guardrail_control: "Review base model version; dan resistance varies sharply by generation"
  severity_base: high
  applicable_when: ["conversational", "customer_facing"]
  notes: "Adding moderation rails on top of dialog rails has been observed to reduce dan protection. Re-scan after any change."

- match: "xss.*"
  risk: "Data exfiltration via rendered output"
  owasp: "LLM02"
  primary_layer: L7
  primary_control: "Output encoding + CSP + outbound resource allowlist"
  nemo_flows: ["injection detection"]
  non_guardrail_control: "Route to AppSec. Guardrail config alone does not close this."
  severity_base: critical
  applicable_when: ["renders_markdown", "browser_rendered"]
  notes: "Downgrade to low if output is never rendered in a browser or terminal."
```

Three design notes:
1. **`applicable_when` is what makes the output credible.** Recommendations that ignore the use case get ignored by app teams.
2. **Emit the quadrant (§1.1) alongside the recommendation.** "Low absolute, high Z — this is an industry-wide weakness, add a compensating control rather than changing models" is a far more useful sentence than a red badge.
3. **Link every recommendation to the specific failing generations** in the hit log. Teams fix what they can see.

---

## 10. Suggested next experiments

1. **Reproduce the NVIDIA ladder on one of your own targets.** Bare → instructions → dialog rails → full rails, same probe set, four garak reports. This is your single most persuasive artefact and it costs one afternoon.
2. **Measure the false-refusal cost of each rung.** Run a utility/benign-request set alongside. Without this, §6.1 is a hole in the pitch.
3. **Measure the latency and token cost of each rung.** Input and output rails add model calls; the jailbreak heuristics server adds roughly 100ms on GPU and 2s on CPU per NVIDIA's own figures. Finance and platform teams will both ask.
4. **Test the fail-open path deliberately.** Take the detector offline and confirm what your system does. Document it.

---

## References

- Garak reporting and score interpretation — https://reference.garak.ai/en/stable/reporting.html
- Garak calibration and Z-scores — https://reference.garak.ai/en/stable/reporting.calibration.html
- NeMo Guardrails, LLM Vulnerability Scanning (the garak benchmark) — https://docs.nvidia.com/nemo/guardrails/evaluation/llm-vulnerability-scanning
- NeMo Guardrails, Jailbreak Protection (heuristics, thresholds, fail-open behaviour) — https://docs.nvidia.com/nemo/guardrails/configure-guardrails/guardrail-catalog/jailbreak-protection
- NeMo Guardrails, Guardrail Catalog — https://docs.nvidia.com/nemo/guardrails/configure-guardrails/guardrail-catalog
- Garak repository — https://github.com/NVIDIA/garak
