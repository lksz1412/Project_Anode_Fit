# Chapter 1 Activation-Barrier Spectrum Plan

> **For agentic workers:** Implement this plan directly. Use archived work only as non-canonical history. Academic terms should remain in English while explanatory prose is Korean.

**Goal:** Rewrite Chapter 1 from zero around the correct object: an activation free-energy barrier distribution mapped into a rate constant distribution, then into a relaxation-length spectrum whose kernel integral produces the observed ICA tail.

**Architecture:** Activation barrier is valid and central. The invalid model is a step-function completion model where a state jumps from 0 to 1 after crossing a threshold. Chapter 1 must keep phase progress continuous through kinetic ODEs and use spectrum integration for stretched tails.

**Tech Stack:** LaTeX, Markdown review records, static TeX checks.

---

## Locked Target System

- System: lithium-ion battery graphite negative electrode.
- Observable: incremental capacity analysis (ICA), \(dQ/dV\), specifically a phase-transition-related peak tail.
- Observed trend: low temperature gives a longer post-peak tail; higher temperature gives a shorter tail.
- Proposed physics: activation free-energy barrier and present electrode-potential assistance control the rate constant spectrum; the observed tail is a relaxation-kernel integral over a spectrum of modes.
- Forbidden error: step-function completion, threshold jump, or sudden \(0\to1\) phase completion.

## Adopted ChatGPT-Work Philosophy

Retain the useful working philosophy from the prior ChatGPT process:

- paper-grade physical meaning first;
- all assumptions must be explicit and defensible by theory/literature or clearly labeled reduced-model assumptions;
- no hidden logical jumps;
- no fitting convenience disguised as physics;
- undergrad-followable derivation with every equation transition explained.

## Required Core Chain

```text
activation free-energy barrier distribution
-> rate constant distribution
-> relaxation-length spectrum
-> exponential kernel integral
-> observed ICA tail
```

## Deliverables

| File | Purpose |
|---|---|
| `Codex/results/PHASE_001_ACTIVATION_BARRIER_SPECTRUM_BASELINE.md` | baseline and correction record |
| `Codex/results/graphite_ica_chapter1_activation_barrier_spectrum_v1.tex` | rewritten Chapter 1 |
| `Codex/results/PHASE_002_CH1_SPECTRUM_LOGIC_REVIEW_10PASS.md` | 10-pass review |
| `Codex/results/PHASE_003_CH1_SPECTRUM_HANDOVER.md` | final handover |

## Gate Conditions

- The manuscript must use `activation free-energy barrier`, `rate constant`, `kinetic lag`, `relaxation-length spectrum`, `kernel integral`, `state variable`, `equilibrium target`, `ICA`, and `DVA` as English academic terms.
- The manuscript must not use a step function for phase completion.
- The manuscript must distinguish barrier distribution from observed tail shape.
- The manuscript must derive a single-mode exponential only as a local kernel, then integrate over modes.
- Static checks must pass for labels, refs, braces, environments, and banned step-function completion patterns.

