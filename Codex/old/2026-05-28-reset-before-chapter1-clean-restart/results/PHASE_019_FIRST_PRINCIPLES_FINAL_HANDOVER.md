# Phase 019 — First-Principles Final Handover

## Summary

The first-principles Chapter 1 redo is complete as a `.tex` deliverable.

Canonical output:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_first_principles_final.tex`

Gate result: `PASS_FIRST_PRINCIPLES_FINAL_HANDOVER`

## Created Artifacts

| Artifact | Purpose |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-first-principles-chapter1-redo-plan.md` | redo plan |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_015_019_FIRST_PRINCIPLES_LEDGER.md` | execution ledger |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_015_FIRST_PRINCIPLES_BASELINE.md` | equation policy baseline |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_016_FIRST_PRINCIPLES_DERIVATION.md` | first-principles derivation note |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_017_EQUATION_ORIGIN_AUDIT.md` | no-copy logic audit |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_018_FINAL_TEX_RESULT.md` | final TeX result |
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_first_principles_final.tex` | final Chapter 1 TeX |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_019_FIRST_PRINCIPLES_FINAL_HANDOVER.md` | this handover |

## Final Manuscript Metadata

| Item | Value |
|---|---|
| Lines | 446 |
| SHA256 | `55707E79469612B397DA1393197B022796A21CCE48C4E12832943070FD7F7A06` |
| Format | LaTeX `.tex` |
| PDF | not generated |

## Verification Evidence

| Check | Result |
|---|---|
| Brace balance | PASS |
| Label/ref consistency | PASS |
| Forbidden hygiene markers | PASS |
| TeX engine availability | `xelatex`, `pdflatex`, `tectonic` not found |
| Git status checked | PASS with safe-directory override |

Git status note:

- `Codex/` is untracked because this workspace output is new.
- `Claude/docs/graphite_ica_chapter1.tex` appears modified in git status, but Codex did not modify the Claude folder during this chain.
- Git also reports permission warnings for the user global ignore file; this does not affect the created Codex artifacts.

## Scientific Output State

The manuscript now starts with convention definitions:

- analysis potential coordinate `varphi`;
- branch charge/capacity coordinate `Q`;
- scan speed `v_Q`;
- ICA/DVA definitions;
- tail direction;
- assisting potential sign;
- units.
- explicit rate and tail-length units.

Additional hardening after the first handover is recorded in:

`D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_FINAL_LOGIC_HARDENING_AUDIT.md`

The core result is:

```tex
L_Q=\frac{v_Q}{k},
\qquad
k(T,\psi)=k_{\att}(T)\exp[-B(T,\psi)/(RT)],
```

therefore:

```tex
L_Q(T,\psi)
=
\frac{v_Q}{k_{\att}(T)}
\exp[B(T,\psi)/(RT)].
```

The barrier is built from:

```tex
G_{\raw}^{\ddagger}(T,\psi)
=
G_0^{\ddagger}(T)-\alpha z_{\mathrm{eff}}F\psi,
\qquad
B(T,\psi)=\max[G_{\raw}^{\ddagger}(T,\psi),0].
```

Interpretation:

- lower temperature lengthens the tail when the net rate decreases;
- higher temperature shortens the tail when the net rate increases;
- favorable present electrode potential lowers the effective barrier and shortens the tail;
- ICA inherits the kinetic tail through the local incremental storage relation.

## Recovery Instructions

After any context compaction or session restart:

1. Open this handover.
2. Open `PHASE_015_019_FIRST_PRINCIPLES_LEDGER.md`.
3. Open `PHASE_016_FIRST_PRINCIPLES_DERIVATION.md` and `PHASE_017_EQUATION_ORIGIN_AUDIT.md`.
4. Verify the final manuscript hash if exact continuity matters.
5. Do not return to the invalidated manuscript as a base.

## Gate

Gate: `PASS_FIRST_PRINCIPLES_FINAL_HANDOVER`

Status: PASS

Reason:

- new first-principles plan was created and executed;
- final TeX output was created as a new file;
- static verification passed;
- PDF generation limitation is recorded;
- recovery path is recorded.
