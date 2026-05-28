# Phase 009 — Claude v4 Chapter 1 vs Codex Rebuilt Chapter 1 Comparison

Date: 2026-05-28

## 0. Scope And Evidence

This comparison uses the latest Claude and Codex Chapter 1 artifacts observed in this session.

| Item | Path | Lines | SHA256 prefix | Coverage |
|---|---|---:|---|---|
| Claude v4 Chapter 1 | `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_chapter1.tex` | 623 | `DCBF024399BB9E52...` | full read lines 1-623 |
| Codex rebuilt Chapter 1 | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v1.tex` | 910 | `8FE3F247B7E7F50E...` | full read in Phase 008, metadata rechecked here |
| Codex 10-pass review | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_CH1_REBUILD_LOGIC_REVIEW_10PASS.md` | n/a | n/a | used as verification record |

Claude static inventory:

| Check | Result |
|---|---|
| begin/end environment count | PASS, `begin=35`, `end=35` |
| brace count | PASS, `open_braces=572`, `close_braces=572` |
| label/ref inventory | PASS, 36 labels, 18 refs, no missing refs |
| cite/bib inventory | PASS, 20 cited keys, 20 bibitems, no missing or uncited bibitems |
| banned model scan | only negative/guardrail uses found; no adopted Heaviside completion equation |

## 1. High-Level Verdict

Claude v4 is no longer the earlier single-length manuscript. It has now absorbed the Codex spectrum idea and is a stronger compact manuscript scaffold than before.

Main verdict:

- Claude v4 is stronger as a publication-style synthesis document.
- Codex rebuilt v1 is stronger as a conservative, undergraduate-followable derivation with fewer unverified methodological jumps.
- The decisive remaining difference is refs 6/7: Claude makes refs 6/7 a load-bearing closure method; Codex keeps refs 6/7 as a method boundary until applicability to the graphite Volterra/spectrum equation is explicitly verified.

Therefore:

```text
Best paper draft scaffold: Claude v4
Best logically conservative foundation: Codex rebuilt v1
Best next canonical version: hybrid, but downgrade Claude's refs 6/7 closure from "load-bearing closed-form" to "candidate closure requiring validation" unless the Fredholm/Volterra mapping is proven.
```

## 2. What Claude v4 Now Does Better

### 2.1 It Has Absorbed The Correct Tail Core

Claude v4 now centers the same corrected chain that Codex previously emphasized:

```text
barrier distribution
-> relaxation-length spectrum
-> kernel integral
-> observed stretched tail
```

It explicitly states that the single exponential is only a local kernel and that the observed tail comes from spectrum integration. This fixes the main weakness of Claude's older single-length Chapter 1.

### 2.2 It Is More Manuscript-Like

Claude v4 has a sharper paper-like structure:

- abstract with the entire argument compressed;
- user verbatim section;
- hypothesis H1-H6;
- grounded spine S1-S14;
- notation table;
- graphite staging section;
- fitting parameter table;
- grounding audit;
- DOI-rich bibliography.

Codex is longer and more pedagogical, but Claude is closer to a concise paper draft.

### 2.3 It Has Stronger Grounding Metadata

Claude's AL system is valuable:

- GROUNDED / BOUNDED / FLAGGED tiers;
- explicit AL references;
- AGP self-check;
- non-unique inverse warning;
- falsification/null-result rules.

Codex has the same caution conceptually, but it does not tag every assumption with AL-# in the manuscript body.

### 2.4 It Gives A More Direct Fitting Interface

Claude gives an explicit evaluation sequence:

```text
k(G,T,psi)
-> L(G)
-> A_L
-> kernel integral
-> refs 6/7 closure
-> dQ/dV_n
```

It also lists parameters and suggested experiments. This is useful for the later fitting stage.

### 2.5 It Uses Normalized Coordinate Cleanly

Claude uses normalized charge coordinate \(q=Q_\ext/Q_\cell\) and derives:

```tex
L = |I| / (Q_cell k)
```

as dimensionless length in \(q\). This is clean for comparing different cells or capacities.

Codex uses dimensional \(Q\) and \(L=v_Q/k\), which is also correct but less normalized.

## 3. Claude v4 Main Risks

### 3.1 Refs 6/7 Are Over-Promoted

This is the most important issue.

Claude says refs 6/7 are:

- `load-bearing` for Chapter 1;
- a `closed-form` closure;
- the closure of the spectrum integral;
- a fitting model component.

It also correctly admits that refs 6/7 are Fredholm-oriented and the present equation may be Volterra-like. But the manuscript then still uses the closure as if it belongs in the core deliverable.

This is not necessarily wrong, but it is not yet fully proven inside the chapter. The risk is:

```text
methodological candidate -> treated as load-bearing closure
```

Codex avoids this by placing refs 6/7 as a method boundary:

```text
useful if a matching Fredholm/self-consistent integral is derived and validated;
not imported as core physics yet.
```

Given the user's priority of no logical leap, Claude's closure section should be downgraded unless a separate proof validates the mapping.

### 3.2 Kernel Integral To Evolution Integral Jump Needs More Derivation

Claude defines the observed tail kernel:

```tex
dTheta_tail/dq ~= integral A_L(L) (1/L) exp[-(q-q_a)/L] dL
```

Then it introduces a more general kernel:

```tex
K(q,q') = integral A_L(L) (1/L) exp[-(q-q')/L] dL
```

and uses it in:

```tex
Theta(q)=Theta_0+int K(q,q')[Theta_eq(q')-Theta(q')]dq'
```

This is plausible, but it is not fully derived. The manuscript jumps from a post-peak tail-response kernel to a self-consistent evolution kernel. That jump needs a derivation or a validity statement.

Codex does not make this jump; it stops at the local ODE, Volterra boundary, and tail kernel.

### 3.3 "Closed-Form" Language Is Too Strong

Claude repeatedly says `closed-form`. However, the closure uses a ratio ansatz and is marked as validation-tier. The safer wording is:

```text
candidate analytic closure / ratio-closure approximation
```

not:

```text
closed-form 논리식
```

unless validation against direct integration is actually done.

### 3.4 It Is Less Undergraduate-Followable

Claude is compact and dense. It is good as a paper scaffold, but many transitions are compressed:

- lattice-gas derivation is summarized rather than shown step-by-step;
- forward/backward rate derivation is compact;
- charge-balance to ICA mapping is compressed;
- spectrum closure is introduced quickly.

Codex is slower, longer, and easier to follow from first principles.

## 4. What Codex Rebuilt v1 Does Better

### 4.1 It Is More Logically Conservative

Codex never treats refs 6/7 as proven closure for the graphite spectrum equation. It says the method is a guardrail and future method candidate unless a matching integral equation is derived.

This better fits the user's strongest requirement:

```text
논리 비약 없음
검증하지 않은 방법론을 완료처럼 쓰지 않음
```

### 4.2 It Separates Target, State, And Rate More Explicitly

Codex derives:

```tex
dxi/dt = k(xi_eq - xi)
```

from forward/backward rates:

```tex
dxi/dt = (1-xi)r_+ - xi r_-
xi_eq = r_+/(r_+ + r_-)
k = r_+ + r_-
```

This makes the no-double-counting logic clearer:

- \(\xi_\eq\) is the target;
- \(\xi\) is the actual state;
- \(k\) is mobility;
- barrier lowering modifies \(k\), not \(\xi\) directly.

Claude states the same idea but more compactly.

### 4.3 It Gives A More Transparent Thermodynamic Build

Codex writes the chemical potential equation and ideal logistic derivation more explicitly:

```tex
mu = mu0 + RT ln[xi/(1-xi)] + Omega(1-2xi)
```

then derives:

```tex
xi_eq = 1/(1+exp[-s(V_n-U)/w_T])
```

and differentiates it to show why homogeneous equilibrium width alone cannot explain low-temperature long tail.

Claude gives this too, but in abbreviated form and intentionally does not commit to an equilibrium shape.

### 4.4 It Handles \(V_n\) / \(V_app\) More Carefully

Codex has a fuller measured-voltage bridge:

```tex
V_app = V_p - V_n - IR_Omega - eta_tr - eta_ct
```

and explicitly warns about double-counting equilibrium shift, kinetic acceleration, and polarization shift.

Claude uses:

```tex
V_{n,app}=V_n+s_I |I|R_n
```

which is concise but less complete as a warning structure.

### 4.5 It Is Better For Teaching The Logic

Codex is 910 lines and slower. That is not as elegant, but it better satisfies:

```text
대학교 학부생 수준의 지식으로도 논리 전개를 따라갈 수 있게
```

Claude is closer to a compressed journal draft; Codex is closer to a derivation note.

## 5. Codex Rebuilt v1 Main Weaknesses

### 5.1 It Is Less Polished As A Manuscript

Codex lacks:

- user verbatim section;
- H1-H6 hypothesis block;
- S1-S14 grounded spine;
- AL-# assumption tags;
- fitting parameter table;
- DOI-rich bibliography;
- compact manuscript voice.

### 5.2 It Is Conservative About Refs 6/7

This is logically safer, but if the project goal is to actively exploit the user's refs 6/7 in Chapter 1, Codex is underdeveloped. It only says where refs 6/7 should be used later.

### 5.3 It Has Less Graphite-Specific Staging Detail

Codex mentions graphite staging but does not give the same compact staging sequence and peak-fusion framing as Claude:

```text
stage 4 -> 3 -> 2L -> 2 -> 1
effective transition j = 1..N_p
```

This should be imported from Claude.

### 5.4 Bibliography Needs Upgrade

Codex has fewer references and less DOI detail. Claude's bibliography is more publication-ready.

## 6. Requirement-By-Requirement Comparison

| Requirement | Claude v4 | Codex rebuilt v1 | Better |
|---|---|---|---|
| Correct spectrum-tail core | Yes, now strong | Yes, strong | Tie |
| No step-function state completion | Yes | Yes | Tie |
| Activation barrier retained | Yes | Yes | Tie |
| Electrode-potential assistance | Strong, compact | Strong, expanded | Tie |
| Undergraduate-followable derivation | Moderate | Strong | Codex |
| Manuscript compactness | Strong | Moderate | Claude |
| Assumption grounding tags | Strong | Moderate | Claude |
| Ref 6/7 integration | Strong but risky | Safe but underused | Depends |
| No unverified method overclaim | Risk present | Strong | Codex |
| Fitting readiness | Stronger | Moderate | Claude |
| Falsification protocol | Strong | Strong but less tabular | Claude |
| Bibliography polish | Strong | Moderate | Claude |
| \(V_n/V_app\) separation | Good | More explicit | Codex |

## 7. Recommended Canonical Direction

The best canonical Chapter 1 should not simply choose Claude or Codex. It should use:

### Keep From Claude

- user verbatim / motivation block;
- hypothesis H1-H6;
- grounded spine S1-S14;
- AL assumption-status system;
- graphite staging section;
- normalized \(q\) coordinate;
- fitting parameter table;
- DOI-rich bibliography;
- compact summary and AGP audit.

### Keep From Codex

- slower derivation of target/state/rate separation;
- explicit forward/backward rate derivation;
- explicit lattice-gas derivation and derivative;
- careful \(V_n/V_app\) bridge;
- strict statement that refs 6/7 are not yet proven as core closure unless Fredholm/Volterra applicability is validated;
- full explanation that the local single exponential is only a kernel.

### Fix Before Canonicalizing Claude v4

Claude v4 should change:

```text
Refs 6/7 propagator = load-bearing closed-form closure
```

to:

```text
Refs 6/7 propagator = candidate ratio-closure method for self-consistent integral formulations;
usable as core only after deriving the matching equation class and validating against direct integration.
```

It should also add a derivation step justifying how the post-peak kernel \(\mathcal K(q,q')\) becomes the evolution kernel in the self-consistent equation.

## 8. Final Judgment

Claude v4 is currently the better manuscript-shaped synthesis.

Codex rebuilt v1 is currently the safer logical foundation.

For the user's stated priority, "논리 비약 없이 완전한 이론 배경", Codex's caution on refs 6/7 is important and should not be discarded. For the user's longer-term goal, "논문이나 특허로 발전", Claude's structure and grounding system should be imported.

Final recommendation:

```text
Use Claude v4 as the structural template,
but replace/downgrade its refs 6/7 closure claim with Codex's more conservative method-boundary logic
until a dedicated validation phase proves the closure.
Then merge Codex's expanded derivation into Claude's compact manuscript shell.
```

