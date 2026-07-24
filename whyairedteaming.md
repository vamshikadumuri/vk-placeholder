# Why AI Red Teaming Is a Must — Even With Guardrails and Model Evaluations

*A plain-language case for business buy-in*

---

## The one idea

> **Guardrails and model evaluations tell you the model *usually behaves*.
> Red teaming tells you whether your *actual deployed system can be broken by someone actively trying*.**
>
> An attacker only cares about the second question.

We are not choosing between these. We already do evals and guardrails, and we should. Red teaming is the missing third layer that measures whether those controls actually hold when a motivated adversary pushes on them.

---

## The 30-second version

- A **model evaluation** tests the model *alone, in a lab, on generic benchmarks*.
- **Guardrails** are filters we bolt on to catch the obvious bad stuff.
- But our app is not just a model. It is a model **plus tools, memory, retrieval, data access, and the power to take real actions** — look up an account, send a message, move money.
- The dangerous failures live in *how those pieces interact* — which neither a lab benchmark nor a static filter ever looks at.
- **Red teaming is penetration testing for AI systems.** No security team says "we have a firewall, so skip the pen test." Guardrails are the firewall; red teaming is the skilled adversary we pay to actually break in.

---

## Why these are three *different* questions

Each layer answers a different question and misses different things. This is the core of the pitch.

```mermaid
flowchart TD
    subgraph EVAL["🧪 Model Evaluation"]
        E1["Tests the MODEL alone"]
        E2["Generic, lab benchmarks"]
        E3["Question: is this model,<br/>by itself, reasonably safe?"]
    end

    subgraph GUARD["🛡️ Guardrails"]
        G1["Filters bolted on top"]
        G2["Block KNOWN bad patterns"]
        G3["Question: did we catch<br/>the obvious bad stuff?"]
    end

    subgraph RED["🎯 Red Teaming"]
        R1["Tests the WHOLE deployed system"]
        R2["An adversary who adapts"]
        R3["Question: can someone actively<br/>trying actually break OUR app?"]
    end

    EVAL -.->|"necessary,<br/>not sufficient"| GUARD
    GUARD -.->|"necessary,<br/>not sufficient"| RED

    style EVAL fill:#e8f0fe,stroke:#4285f4
    style GUARD fill:#fef7e0,stroke:#f9ab00
    style RED fill:#fce8e6,stroke:#ea4335
```

---

## The gap that guardrails and evals never see

The model is one small box. The *system* is everything around it — and that is where the money-losing failures happen.

```mermaid
flowchart TB
    subgraph SYSTEM["OUR ACTUAL DEPLOYED AGENT"]
        direction TB
        MODEL["🤖 The Model"]
        TOOLS["🔧 Tools & Actions<br/>(transfer, send, delete)"]
        MEM["🧠 Memory & State"]
        RET["📚 Retrieval / Knowledge"]
        DATA["🗄️ Customer Data & Accounts"]

        MODEL --- TOOLS
        MODEL --- MEM
        MODEL --- RET
        MODEL --- DATA
    end

    EVALBOX["🧪 Model evals test<br/>ONLY this box"] -.-> MODEL
    GUARDBOX["🛡️ Guardrails wrap<br/>the text going in/out"] -.-> MODEL
    REDBOX["🎯 Red teaming tests<br/>the ENTIRE system<br/>and how the pieces interact"] ==> SYSTEM

    style MODEL fill:#e8f0fe,stroke:#4285f4,stroke-width:2px
    style SYSTEM fill:#f8f9fa,stroke:#5f6368,stroke-width:2px
    style EVALBOX fill:#e8f0fe,stroke:#4285f4
    style GUARDBOX fill:#fef7e0,stroke:#f9ab00
    style REDBOX fill:#fce8e6,stroke:#ea4335,stroke-width:2px
```

**The point:** a model that scores "safe" on public benchmarks can still be steered into leaking *our* customer data through *our* retrieval setup, or misusing a tool *we* connected. That risk is invisible to a test that only looks at the model.

---

## Why guardrails + evals aren't enough on their own

**1. Guardrails are static; attackers adapt.**
A filter blocks known patterns. A real adversary keeps rephrasing — across multiple turns, with role-play, encoding, or persuasion — until something slips through.

```mermaid
flowchart LR
    A["Attacker sends<br/>a request"] --> B{"Guardrail:<br/>known bad<br/>pattern?"}
    B -->|"Yes"| C["🚫 Blocked"]
    C --> D["Attacker rephrases:<br/>role-play, split it up,<br/>persuade, encode..."]
    D --> A
    B -->|"No — looks<br/>innocent"| E["✅ Passes through"]
    E --> F["💥 Harmful action<br/>or data leak"]

    style C fill:#e6f4ea,stroke:#34a853
    style E fill:#fce8e6,stroke:#ea4335
    style F fill:#fce8e6,stroke:#ea4335,stroke-width:2px
    style D fill:#fef7e0,stroke:#f9ab00
```

The filter only has to fail **once**. The attacker gets unlimited tries.

**2. Evals test the model, not our app.**
Public benchmarks say nothing about how *our* specific tools, data, and connections can be abused.

**3. Agents can *act*, so the risk is bigger than "says something bad."**
The failure that matters isn't a rude sentence — it's an **unauthorized transfer, deleted records, or one customer's agent reaching into another customer's data.** Content filters don't catch permission- and action-level failures at all.

**4. "We have guardrails" is a claim, not a measurement.**
We don't know how good a control is until someone tries to beat it. Red teaming turns "we think we're covered" into a number.

---

## The analogy that lands

| Layer | Everyday equivalent |
|---|---|
| Model evaluation | Checking the engine works on a test bench |
| Guardrails | Installing the **seatbelts** |
| **Red teaming** | The **crash test** |

> You would never ship a car having installed seatbelts but *never crash-tested it*.
> An agent that moves money or touches customer data is a car we're putting customers in.

---

## These layers are complementary, not competing

This is defense in depth. Each layer catches what the previous one misses. Red teaming doesn't replace evals or guardrails — it **validates them**.

```mermaid
flowchart LR
    T["Threats &<br/>Attackers"] --> L1
    L1["🧪 Evals<br/>catch weak<br/>base models"] --> L2
    L2["🛡️ Guardrails<br/>catch known<br/>bad patterns"] --> L3
    L3["🎯 Red Teaming<br/>catches what<br/>slips past both"] --> SAFE["✅ Assured,<br/>deployable<br/>agent"]

    style L1 fill:#e8f0fe,stroke:#4285f4
    style L2 fill:#fef7e0,stroke:#f9ab00
    style L3 fill:#fce8e6,stroke:#ea4335
    style SAFE fill:#e6f4ea,stroke:#34a853,stroke-width:2px
```

---

## What red teaming actually gives us (the measurable output)

Instead of an assertion of safety, we get **evidence**: how often attacks succeed with guardrails **off** vs **on**, and the **residual risk** that remains even with everything switched on.

```mermaid
flowchart LR
    subgraph OFF["Guardrails OFF"]
        O["Attack Success Rate:<br/>___% (high)"]
    end
    subgraph ON["Guardrails ON"]
        N["Attack Success Rate:<br/>___% (lower)"]
    end
    OFF ==>|"The gap = how much<br/>our guardrails buy us"| ON
    ON ==>|"Whatever's left =<br/>residual risk to govern"| RES["📋 Residual risk,<br/>documented &<br/>auditable"]

    style OFF fill:#fce8e6,stroke:#ea4335
    style ON fill:#fef7e0,stroke:#f9ab00
    style RES fill:#e6f4ea,stroke:#34a853,stroke-width:2px
```

> ⚠️ **Insert our own measured figures here** (e.g. BankBot A/B results). Do not present illustrative numbers to governance — every figure should be traceable to a specific run and methodology.

---

## The business case for funding it

- **Governance and regulators increasingly expect it.** *Demonstrable* adversarial testing with an audit trail — not just an assertion that controls exist.
- **Finding a flaw ourselves is far cheaper than an attacker (or a headline) finding it.** One exploited agent in a bank is financial loss, a regulatory breach, and a reputational hit at once.
- **It's what lets us scale AI *safely*.** A repeatable assurance process means we can confidently say "yes, deploy" — instead of blocking every agent out of fear.

---

## Real incidents (illustrative)

- **Freysa** — an AI agent was explicitly instructed *never* to release its funds (that instruction *is* a guardrail). People kept talking to it until one message convinced it to pay out anyway. *Static instruction vs. adaptive persuasion — persuasion won.*
- **EchoLeak** — a crafted email could quietly pull data out of an AI assistant *even with protections in place*. The hole was in **how the pieces fit together**, not the model itself.

> 📌 *Cite primary sources for exact dates/figures before presenting these to governance.*

---

## For the governance audience: this maps to recognised standards

Red teaming isn't a bespoke exercise — it exercises the failure modes that industry frameworks already name:

- **OWASP LLM Top 10** — prompt injection, sensitive-data disclosure, and related risks
- **OWASP Agentic Top 10** — agent-specific failures: excessive agency, tool misuse, authorization gaps
- **MITRE ATLAS** — a shared catalogue of real-world adversary techniques against AI systems

Testing against these gives us a **coverage-to-taxonomy map** — evidence that our assurance is systematic, not ad hoc.

---

## One line to close the pitch

> **Guardrails are the seatbelt. Red teaming is the crash test.**
> For an agent that moves money or touches customer data, that's not optional.
