#!/usr/bin/env python3
"""
Assign app_context_role (primary | backdrop) to every promptfoo plugin.

Principle: WHERE DOES THE HARM LIVE?
  primary  : app's own mechanics — access, tools/agency, memory, retrieval provenance,
             side-effects (app IS the attack surface; trace-layer / P3-P4 grading)
  backdrop : the CONTENT the model produces (app is a delivery vehicle; text-layer P1-P2)

v2 changes vs v1:
  - dataset plugins -> backdrop (curated content probes)
  - discrimination / teen-safety / fair-housing families -> backdrop
  - domain packs resolved by signal (content vs access) instead of defaulting to primary
  - provenance / agentic mechanics added to primary
  - fallback for a truly unknown id -> UNKNOWN (review), no silent 'primary'
"""
import sys

BACKDROP_PREFIX = ("harmful:", "bias:", "teen-safety:", "realestate:")
PRIMARY_PREFIX  = ("pii:", "agentic:")

# Curated-dataset plugins: harm is the injected content -> backdrop
DATASET = {"aegis","beavertails","cyberseceval","donotanswer","harmbench","pliny",
           "toxic-chat","unsafebench","vlguard","vlsu","xstest","harmbench"}

BACKDROP_EXACT = DATASET | {
    "hate","toxicity","profanity","insults","politics","religion","radicalization",
    "self-harm","graphic-content","sexual-content","hallucination","misinformation",
    "overreliance","imitation","competitors","contracts","unverifiable-claims",
    "model-identification","off-topic","rag-source-attribution","gender-bias",
}

PRIMARY_EXACT = {
    "bola","bfla","rbac","debug-access","shell-injection","sql-injection","ssrf",
    "prompt-extraction","indirect-prompt-injection","cross-session-leak",
    "divergent-repetition","excessive-agency","hijacking","tool-discovery",
    "memory-poisoning","reasoning-dos","system-prompt-override","ascii-smuggling",
    "special-token-injection","pii","harmful:privacy","harmful:privacy-violations",
    # provenance / agentic mechanics
    "rag-poisoning","rag-document-exfiltration","data-exfil","cca","mcp","goal-misalignment",
}

DOMAIN_PREFIXES = ("financial:","medical:","telecom:","legal:","insurance:",
                   "pharmacy:","ecommerce:","coppa","ferpa")

# Within a domain pack, these ID substrings mean the harm is CONTENT -> backdrop
DOMAIN_CONTENT = ("hallucination","misinformation","misinfo","counterfactual","sycophancy",
                  "impartiality","defamation","anchoring","incorrect-knowledge","off-label",
                  "prioritization-error","calculation-error","dosage","drug-interaction",
                  "disclaimer","ai-disclosure","specialized-advice","discrimination",
                  "steering","bias","body-ideals","dangerous-content","dangerous-roleplay")
# these mean the harm is app mechanics / data-access -> primary
DOMAIN_ACCESS  = ("disclosure","data-leakage","confidential","phi","cpni","pci-dss",
                  "account-takeover","unauthorized","fraud","location","law-enforcement",
                  "access-control","audit-tampering","cyber","order-fraud",
                  "price-manipulation","compliance-bypass","controlled-substance",
                  "misconduct","sox","japan-fiea","tcpa","accessibility-violation")

def classify(pid: str):
    p = pid.strip().lower()
    if not p:
        return None
    if p in ("harmful:privacy","harmful:privacy-violations"):
        return ("primary", False)
    if p in DATASET:                       return ("backdrop", False)
    if any(p.startswith(x) for x in BACKDROP_PREFIX) or p in BACKDROP_EXACT:
        return ("backdrop", False)
    if any(p.startswith(x) for x in PRIMARY_PREFIX) or p in PRIMARY_EXACT:
        return ("primary", False)
    if any(p.startswith(x) for x in DOMAIN_PREFIXES):
        if any(s in p for s in DOMAIN_CONTENT): return ("backdrop", False)
        if any(s in p for s in DOMAIN_ACCESS):  return ("primary", False)
        return ("primary", True)           # genuine domain ambiguity -> review
    return ("primary", True)               # unknown -> review (guess primary, but flag)

def main():
    ids = [l for l in sys.stdin.read().splitlines() if l.strip()]
    rows, review = {}, []
    for pid in ids:
        r = classify(pid)
        if not r: continue
        role, rev = r
        rows[pid.strip()] = role
        if rev: review.append(pid.strip())
    print("app_context_role:")
    for pid in sorted(rows):
        print(f"  {pid}: {rows[pid]}" + ("   # REVIEW" if pid in review else ""))
    print(f"\n# {len(rows)} classified — {sum(v=='primary' for v in rows.values())} primary, "
          f"{sum(v=='backdrop' for v in rows.values())} backdrop, {len(review)} to review")

if __name__ == "__main__":
    main()
