#!/usr/bin/env python3
"""
Assign app_context_role (primary | backdrop) to every promptfoo plugin.

Principle: WHERE DOES THE HARM LIVE?
  - primary  : in the app's own logic / data / permissions (app IS the attack surface)
  - backdrop : in the CONTENT the model produces (app is only a delivery vehicle)

Usage:
  promptfoo redteam plugins --ids 2>/dev/null | python3 classify_app_context_role.py
  # or paste IDs (one per line) into plugins.txt:
  python3 classify_app_context_role.py < plugins.txt

Output: YAML mapping + a REVIEW list of plugins you should confirm by hand.
"""
import sys, re

# --- Confident rules, evaluated most-specific first ------------------------

# Content-harm families: the output text is the harm.
BACKDROP_PREFIX = ("harmful:", "bias:")
BACKDROP_EXACT = {
    "harmful", "hate", "toxicity", "profanity", "insults", "politics",
    "religion", "radicalization", "self-harm", "graphic-content",
    "sexual-content", "hallucination", "misinformation", "overreliance",
    "imitation", "gender-bias",
}

# App-native families: logic / data / permissions is the harm.
PRIMARY_PREFIX = ("pii:", "agentic:")
PRIMARY_EXACT = {
    "bola", "bfla", "rbac", "debug-access", "shell-injection",
    "sql-injection", "ssrf", "prompt-extraction", "indirect-prompt-injection",
    "cross-session-leak", "divergent-repetition", "excessive-agency",
    "hijacking", "tool-discovery", "memory-poisoning", "reasoning-dos",
    "system-prompt-override", "ascii-smuggling", "pii", "harmful:privacy",
}

# Domain packs are MIXED — default them, but always surface for review.
DOMAIN_PREFIXES = ("financial:", "medical:", "telecom:", "legal:", "insurance:")
# best-guess default for a domain plugin unless its ID clearly signals content
DOMAIN_CONTENT_SIGNALS = ("hallucination", "misinformation", "bias", "disclaimer",
                          "misinfo", "anthropomorph")

def classify(pid: str):
    p = pid.strip().lower()
    if not p:
        return None
    # explicit privacy override (content-shaped but app-data harm)
    if p == "harmful:privacy":
        return ("primary", False)
    if any(p.startswith(x) for x in BACKDROP_PREFIX) or p in BACKDROP_EXACT:
        return ("backdrop", False)
    if any(p.startswith(x) for x in PRIMARY_PREFIX) or p in PRIMARY_EXACT:
        return ("primary", False)
    if any(p.startswith(x) for x in DOMAIN_PREFIXES):
        role = "backdrop" if any(s in p for s in DOMAIN_CONTENT_SIGNALS) else "primary"
        return (role, True)   # review = True
    # custom / policy / intent / unknown → app-shaped by default, flag it
    return ("primary", True)

def main():
    ids = [l for l in (sys.stdin.read().splitlines()) if l.strip()]
    if not ids:
        print("No plugin IDs on stdin. Pipe `promptfoo redteam plugins --ids` in.",
              file=sys.stderr)
        sys.exit(1)
    rows, review = {}, []
    for pid in ids:
        r = classify(pid)
        if r is None:
            continue
        role, needs_review = r
        rows[pid.strip()] = role
        if needs_review:
            review.append(pid.strip())

    print("# app_context_role mapping (generated)")
    print("app_context_role:")
    for pid in sorted(rows):
        flag = "   # REVIEW" if pid in review else ""
        print(f"  {pid}: {rows[pid]}{flag}")

    print(f"\n# {len(rows)} plugins classified — "
          f"{sum(v=='primary' for v in rows.values())} primary, "
          f"{sum(v=='backdrop' for v in rows.values())} backdrop")
    if review:
        print(f"\n# {len(review)} need a human confirm (domain packs / custom):")
        for pid in sorted(review):
            print(f"#   {pid} -> {rows[pid]} (default guess)")

if __name__ == "__main__":
    main()
