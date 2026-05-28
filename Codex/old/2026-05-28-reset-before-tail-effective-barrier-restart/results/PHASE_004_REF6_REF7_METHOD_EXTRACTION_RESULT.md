# Phase 004 - Ref. 6/7 Method Extraction Result

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-anode-dqdv-thermodynamic-fit-development-plan.md`

Ledger: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_007_EXECUTION_LEDGER.md`

Method Notes: `D:\Projects\Project_Anode_Fit\Codex\results\ref6_ref7_method_notes.md`

Date: 2026-05-27

## Summary

Phase 004 identified refs. 6 and 7 in the user's JCP paper and extracted the method role they play in that paper.

Gate result: `PASS_REF6_REF7_METHOD_SOURCE`

Main finding:

- Ref. 6 is the 2011 JCP communication on a propagator for diffusive dynamics of an interacting molecular pair.
- Ref. 7 is the 2013 JCP paper on accurate rates for diffusion-influenced bimolecular reactions with long-range reactivity.
- In the 2017 paper, refs. 6/7 are invoked for a solution method for Fredholm integral equations of the second kind.
- The operational pattern is a ratio-closure method: rewrite the second-kind integral equation into a formally exact expression containing an unknown ratio, then approximate that ratio using a simpler reference problem.
- For graphite, this should be imported as a self-consistent integral-equation closure strategy, not as a direct physical analogy.

## Step Range

| Planned Steps | Actual Steps | Status |
|---:|---:|---|
| 44-59 | 44-59 | PASS |

## Inputs

| Role | Path / Source | Status |
|---|---|---|
| User paper | `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` | read full text extraction pages 1-10 |
| Phase 003 dependency audit | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_003_VER1_DEPENDENCY_AUDIT_RESULT.md` | used |
| Ref. 6 metadata | Digital Jiphyeonjeon; Son Research Lab list | checked |
| Ref. 7 metadata | Ewha Pure; Son Research Lab list | checked |

## Files Created

| Path | Purpose |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\results\ref6_ref7_method_notes.md` | Bibliography, citation context, method extraction, and graphite-transfer caution |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_004_REF6_REF7_METHOD_EXTRACTION_RESULT.md` | This Phase 004 result |

## Read / Inspection Coverage

| Source | Required Range | Actual Range | Status | Notes |
|---|---:|---:|---|---|
| JCP 147, 144111 PDF | enough to identify refs. 6/7 and method context | pages 1-10 | READ_FULL_TEXT | `pypdf` reported 10 pages and extracted text for every page |
| References section | ref. 6 and ref. 7 entries | page 10 | checked | Local PDF gives authors, journal, volume, article, year but not titles |
| In-text citation scan | every use of refs. 6/7 | pages 2, 5, 8 | checked | Three citation contexts found |
| Equation context | Eq. (32)-(39), Eq. (59)-(63) | pages 5, 8 | method-level checked | Exact glyph transcription should be visually verified before final LaTeX |

## Execution Evidence

### PDF Extraction

Bundled Python `pypdf` was available and reported:

```text
pages 10
full_chars 36680
```

Initial local tool availability:

```text
pdftotext/pdfinfo not available in shell
bundled Python pypdf available
```

### Refs. 6/7 Citation Contexts

| Page | Evidence Type | Interpretation |
|---:|---|---|
| 2 | introduction sentence around `solution method6,7` | refs. 6/7 are the method basis for Fredholm second-kind treatment |
| 5 | text after Eq. (32), `Refs. 6 and 7` | Eq. (32) is the direct method entry point |
| 8 | results discussion, method utility | numerical agreement supports the method in the long-range sink case |

No additional `6,7` or `Refs. 6 and 7` citation was found by text extraction.

## Bibliographic Result

| Ref | Exact Identification | DOI / Link |
|---:|---|---|
| 6 | Sangyoub Lee, Chang Yun Son, Jaeyoung Sung, Song-Ho Chong, "Communication: Propagator for diffusive dynamics of an interacting molecular pair," J. Chem. Phys. 134(12), 121102 (2011). | `10.1063/1.3565476` |
| 7 | Chang Yun Son, Jaehoon Kim, Ji-Hyun Kim, Jun Soo Kim, Sangyoub Lee, "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity," J. Chem. Phys. 138(16), 164123 (2013). | `10.1063/1.4802584` |

## Extracted Method

The method used in the 2017 paper has four mathematical moves:

1. Reduce the steady-state physical problem to a second-kind integral equation for the unknown observable.
2. Rewrite the equation into a formally exact reciprocal expression containing an unknown ratio of the same observable evaluated at two coordinates.
3. Approximate the unknown ratio using a simpler reference problem whose solution is already known.
4. Insert the reference ratio to obtain a closed approximate analytic expression, then validate against direct numerical solution.

In the 2017 paper, the reference problem is the delta-function reaction sink with contracted reactivity matched to the long-range sink.

## Graphite Relevance

The graphite ver.1 issue is:

```text
xi_j -> charge balance -> V_n -> xi_eq/k_j -> dxi_j/dq or dxi_j/dt -> xi_j
```

Refs. 6/7 do not directly provide graphite thermodynamics. They provide a way to keep a feedback-containing integral equation from becoming a naive divergent fixed-point iteration.

The candidate import is:

- write the `xi_j` dynamics as an integral equation after the charge-balance root solve for `V_n`;
- isolate the unknown feedback correction in a ratio/correction functional;
- choose a reference path, such as equilibrium/quasi-static charge-balance or a frozen-kinetic baseline;
- use the reference ratio/correction as closure;
- verify the result against direct DAE/root-solve integration.

## Validation

| Check | Result | Evidence |
|---|---|---|
| PDF page count verified by parser | PASS | `PdfReader` reports 10 pages |
| PDF text extracted for all pages | PASS | pages 1-10 inspected |
| Ref. 6 identified | PASS | local ref list plus external title/DOI metadata |
| Ref. 7 identified | PASS | local ref list plus external title/DOI metadata |
| In-text citation contexts located | PASS | pages 2, 5, 8 |
| Method extracted without over-mapping | PASS | method notes distinguish Fredholm source from graphite Volterra-like q update |
| Exact equation visual verification | PARTIAL | text extraction used; exact equation glyphs require later visual cross-check before final LaTeX transcription |

## Gate

Gate: `PASS_REF6_REF7_METHOD_SOURCE`

Gate conditions:

| Condition | Status |
|---|---|
| refs. 6 and 7 identified exactly | PASS |
| in-text use of refs. 6/7 recorded | PASS |
| method role extracted from the user's paper | PASS |
| external bibliographic titles/DOIs checked because local PDF lacked titles | PASS |
| no claim that the physical geminate-pair theory directly equals graphite dQ/dV | PASS |

## Confirmed Decisions

| Item | Status | Evidence |
|---|---|---|
| refs. 6/7 are about Fredholm second-kind integral-equation methods | 확정 | user PDF pages 2 and 5; external metadata |
| the local 2017 paper uses a reference-ratio closure | 확정 | user PDF page 5, Eq. (33)-(39) context |
| graphite mapping must be mathematical, not physical | 확정 | mismatch between geminate-pair separation probability and LIB graphite charge balance |

## Open Issues / Decision Queue

| ID | Type | Item | Status | Next |
|---|---|---|---|---|
| R67-ISS-001 | source depth | Full original PDFs for refs. 6 and 7 were not in the local folder and were not fully read | open | Only retrieve if Phase 005 needs details beyond the method already shown in the 2017 paper |
| R67-ISS-002 | equation fidelity | pypdf text can distort equation glyphs | open | Visually verify any equation copied into final LaTeX |
| R67-ISS-003 | mapping | Graphite q-domain dynamics are Volterra-like after ODE integration, while refs. 6/7 are Fredholm second-kind sources | confirmed | Phase 005 must map the closure pattern, not force equation identity |

## Next

Proceed to Phase 005 Step 60:

- map the ref. 6/7 ratio-closure pattern onto the `xi_j` / `V_n` feedback loop;
- define the reference path and residual checks;
- decide what enters the Chapter 1 development specification.
