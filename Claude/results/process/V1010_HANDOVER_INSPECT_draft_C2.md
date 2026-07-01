# V1010 handover integrity inspection draft — C2

## Scope and read ledger

- Role: C2, FIX_LIST implementation tracking.
- Base prompt full read: `handover_inspect_base.txt` lines 1-23. Key constraints: diagnosis only, no source edits, evidence by record/code/TeX lines, problem-first union/refute/weakest-one/no empty pass (line 1); SPEC is version history/FIX_LIST/HANDOVER lineage (lines 3-4); output format and weakest-one/version-transition judgement required (line 23).
- Plan full read: `Claude/plans/2026-07-06-v1010-handover-integrity-inspection-plan.md` lines 1-34. Key checkpoints: FIX_LIST tracking is explicit item 7 (line 23), bell is not a defect (lines 20, 26), source freeze/no edits (line 34).
- FIX_LIST full read:
  - `Claude/results/builds/v9/v9-00_spine/FIX_LIST_v911.md` lines 1-20.
  - `Claude/results/builds/ch1v10/v10-00_spine/FIX_LIST_v1011.md` lines 1-34.
  - `Claude/results/builds/ch2_v4/v4-00_spine/FIX_LIST_v411.md` lines 1-29.
- Current v1.0.10 full read:
  - `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` lines 1-1937. Initial tool truncation gaps were narrowed and re-read at lines 247-274, 733-781, 1199-1300, 1729-1765.
  - `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` lines 1-750.
- Corresponding version artifacts partially checked for item evidence:
  - `Claude/results/builds/v9/v9-11/v9-11.tex` and `.log`.
  - `Claude/results/builds/ch1v10/v10-11/v10-11.tex` and `.log`.
  - `Claude/results/builds/ch2_v4/v4-11/v4-11.tex` and `.log`.
- Not performed: code file full read, PDF visual inspection, external Crossref verification, fresh LaTeX build. Current `docs/v1.0.10` build log was not found in the searched paths.

## Findings

### [LOW] v9 FIX_LIST A3-1 overfull fix was not actually completed in v9-11 and the same source sentence is still present in v1.0.10

- SPEC: `FIX_LIST_v911.md` line 17 requires A3-1, `line 1485-1488 Overfull 22.6pt(조판) -> 정정(>20pt 유일)`.
- Version evidence: `Claude/results/builds/v9/v9-11/v9-11.log` line 1487 still reports `Overfull \hbox (22.55423pt too wide) in paragraph at lines 1521--1524`; the corresponding source is `v9-11.tex` lines 1521-1523.
- v10 preservation evidence: `Claude/results/builds/ch1v10/v10-11/v10-11.log` line 1490 still reports the same `22.55423pt` overfull at source lines 1722-1725; source text is `v10-11.tex` lines 1722-1724.
- v1.0.10 evidence: the same paragraph is still present in current Ch1 at `graphite_ica_ch1_v1.0.10.tex` lines 1807-1809.
- What failed to hand over: this is a FIX_LIST item that was neither actually cleared in the target version nor materially changed by v1.0.10. It is not physics-breaking, but it invalidates the “A3-1 fixed” claim.
- Why it matters: G-follow only. It is a layout/readability defect, not a G-derive physics defect.
- Lens: FIX_LIST implementation tracking; version-transition actual-fix check.

### [MED] v1.0.10 public metadata/header labels still expose older version labels

- SPEC: base prompt requires v1.0.10 handover integrity against the historical SPEC, with v1.0.10 current files as target (`handover_inspect_base.txt` lines 3-4, 16, 23). Plan line 21 includes v10 -> v1.0.10 two-axis degradation.
- Current Ch1 evidence: the file announces v1.0.10 at `graphite_ica_ch1_v1.0.10.tex` line 3 and date line 100, but PDF metadata/header still say Chapter 1 `(v9)` at lines 71 and 73.
- Current Ch2 evidence: the file path is v1.0.10, but internal header/title metadata still say `graphite_ica_ch2_v5.tex` / `(v5)` at lines 2, 35, and 37.
- What failed to hand over: the document body mostly preserves the intended technical content, but reader-facing PDF metadata/header still advertise older internal version identities. This weakens the v1.0.10 handover surface.
- Why it matters: G-follow and handover traceability. A reader can mistake the frozen release for v9/v5 material even though Ch1 line 100 says v1.0.10.
- Lens: v10 -> v1.0.10 preservation/packaging integrity. This is not a FIX_LIST item, but it is a handover integrity defect.

### [REFUTED / not counted as defect] v1011 fly2020 “Stroe 추가” instruction is superseded by later in-file Crossref correction

- SPEC: `FIX_LIST_v1011.md` line 30 says `fly2020 = Fly·Schaltz·Stroe 3인인데 bibitem 2인 -> Stroe 추가`.
- Version/current evidence: v10-11 and v1.0.10 instead state Crossref-confirmed `A. Fly and R. Chen` two-author metadata, with the old Schaltz/Stroe interpretation marked as an error: current Ch1 comment lines 29-31 and bibliography line 1932.
- Judgement: literal FIX_LIST line 30 was not implemented, but the later artifact refutes the premise. Do not flag this as missing handover unless an external bibliographic check contradicts the in-file Crossref note.
- Lens: refute requirement; false-positive prevention.

## Item tracking

### FIX_LIST_v911 -> Ch1 v9-11 -> v1.0.10

| Item | SPEC line | Target/current evidence | Judgement |
|---|---:|---|---|
| F1: Sommerfeld `g(E)≈g(E_F)` assumption | 6 | Current Ch1 lines 965-968 explicitly state the `g(E)` freezing assumption and why it is standard. v9-11 lines 917-920 contain the same content. | Preserved |
| F3: nodemap/code plug-in must refer to molar `eq:dSemolar` | 7 | Current Ch1 molar bridge lines 1023-1027; plug-in lines 1757-1760; nodemap line 1851 cites `eq:dSemolar`. | Preserved |
| F8: config/electronic additive orthogonality | 8 | Current Ch1 lines 1707-1715 separate additive orthogonality from no-double-counting. | Preserved |
| F2: tier separation | 9 | Current Ch1 lines 1001-1006 split function form, anchor point, and continuous curve tiers. | Preserved |
| A2-L1: MSMR direction factor `f <-> -sigma_d` | 13 | Current Ch1 lines 1747-1752 explicitly map `f` to `-\sigma_d`. | Preserved |
| A2-2: LCO `+80` vs `Delta S_e<0` coexistence | 14 | Current Ch1 lines 501-508 state electronic term is a small negative correction and does not flip total positive scale. | Preserved |
| A3-1: Overfull >20pt fixed | 17 | v9-11 log line 1487 and v10-11 log line 1490 still show 22.55423pt; current source sentence remains at Ch1 lines 1807-1809. | Not actually fixed; carried forward as source risk |

### FIX_LIST_v1011 -> Ch1 v10-11 -> v1.0.10

| Item | SPEC line | Current evidence | Judgement |
|---|---:|---|---|
| D1: `rho` identity as apparent-U/eta, not equilibrium `U_j` distribution | 6-12 | Current Ch1 lines 1275-1297 and keybox lines 1341-1351. | Preserved |
| D2: Dahn `x_max=1-P` is intra-particle capacity example, not inter-particle rho proof | 14-15 | Current Ch1 lines 1323-1325 and bibliography line 1933. | Preserved |
| D3: no indiscriminate LCO application | 17-18 | Current Ch1 lines 1263-1265 limit graphite-specific mechanism and mark LCO as general eta distribution/tier C assumption. | Preserved |
| D4: separate kinetic `L_V` from ensemble eta average | 20-22 | Current Ch1 lines 1244-1248 and 1289-1293 separate finite-rate skew from ensemble average. | Preserved |
| D5: width fallback/transition mapping | 20-22 | Current Ch1 lines 733-743 separate initial all-two-phase Omega guesses from expected fitted SS/two-phase split. | Preserved |
| A2: w_eff removed, electronic entropy byte-preserved intent | 24-25, 34 | Current Ch1 body uses w dual status and broadening; `w_eff` appears only in historical header comments (lines 19-20, 32), not as a live equation/helper in Ch1. Electronic entropy block is present lines 953-1165 and decomposition lines 1690-1727. | Preserved in substance |
| D9: `fig:broadening` referenced | 29 | Current Ch1 section starts at line 1218, figure label at 1390, and textual references/caption occur at lines 1242 and 1380-1389. | Preserved |
| D1/D2/D3 bibliography fixes | 30-31 | fly2020 is refuted/superseded as above; rsc2021 and dahn1995 are completed at current lines 1931 and 1933. | Preserved/refuted as applicable |

### FIX_LIST_v411 -> Ch2 v4-11 -> v1.0.10

| Item | SPEC line | Current evidence | Judgement |
|---|---:|---|---|
| A1-H1: vib/electronic intermediate derivation or Ch1 reference | 7, 22 | Current Ch2 vib derivation lines 359-374; electronic derivation and Ch1 reference lines 381-399. | Preserved |
| A1-L1/A2-D1: remove/restate “선두차수까지다” | 8, 13, 23 | Current Ch2 states complete expression matches FD at lines 486-493 and lines 687-692; `선두차수` not found in current Ch2. | Preserved |
| A3-D1: TikZ node Korean -> English ASCII | 18, 24 | Search found no `\node` line containing Hangul in current Ch2; inspected figure nodes at lines 258-289 and 497-520 are English/math. | Preserved |
| A3-D2: remove dangling “파생 I” | 19, 25 | `파생 I` not found in current Ch2. | Preserved |
| w_eff/config/known physics invariant | 26, 29 | v4-11 still had live `w_eff` body at lines 531-570, but current v1.0.10 Ch2 replaced it with w dual-status/broadening reference at lines 539-568. `w_eff` remains only in historical comments lines 3 and 8. | v1.0.10 supersedes v4-11; no live defect |

## Integrity-preserved areas

- Broadening restoration: preserved. Current Ch1 includes transition split, 3 mechanisms, Dreyer plateau layer, apparent-U/eta broadening layer, forward-only averaging, no rho inversion, and size/radius exclusion (lines 1218-1352; figure/caption lines 1380-1390). This matches base prompt line 9 and plan lines 17, 20.
- D-PEAK correction: preserved and not a bell false positive. Current Ch1 explicitly states `L_V >> Delta_grid` is the derivative-like limit, `L_V -> 0` is not a smooth bell limit, and the branch switch handles small `L_V` (lines 1555-1560, 1573-1593, 1901-1906). This matches base prompt lines 7 and 10.
- Electronic entropy: preserved in substance. Current Ch1 retains Sommerfeld derivation, tier separation, molar conversion, MIT gate, negative insertion-basis `Delta S_e`, T-linear entropy/T^2 potential contribution, and additive orthogonality (lines 953-1165, 1690-1727).
- Ch2 statistics chapter: preserved after v1.0.10 supersession. Current Ch2 is a distribution/statistical thermodynamics chapter from partition function to occupation distribution to config/vib/electronic entropy to reversible heat (lines 66-100, 110-205, 208-421, 430-685, 637-730).

## Weakest one

Weakest confirmed point: `FIX_LIST_v911` A3-1. It is only LOW severity, but it is the cleanest “SPEC says fixed, version log says still present, current source still carries the same paragraph” case. The physics content is not damaged; the problem is handover truthfulness and G-follow polish.

## Version-transition judgement

- v8 -> v9: improved and preserved for C2 scope. v9 electronic entropy fixes F1/F2/F3/F8 are visible in v9-11 and v1.0.10. One LOW build-polish item (A3-1 overfull) was not actually cleared.
- v9 -> v10: improved. v10 broadening restoration and v1011 D1-D5 are visible in current Ch1. No bell false positive: current bell/merged peak is consistent with apparent-U/eta and current `n=1` behavior.
- v10 -> v1.0.10: technically preserved in body content, but packaging/header labels are weak: Ch1 still exposes v9 in metadata/header and Ch2 exposes v5.
- Ch2 v4 -> v1.0.10: v411 core corrections are preserved, and v1.0.10 supersedes live `w_eff` with the later w dual-status/broadening framing.

## Five-line summary

1. Focus: FIX_LIST_v911/v1011/v411 item-by-item implementation and v1.0.10 preservation against Ch1/Ch2 TeX.
2. Confirmed handover defects: 2 total; one LOW FIX_LIST actual-fix failure, one MED release-label/metadata integrity issue.
3. Most severe: stale v9/v5 metadata/header in v1.0.10 because it affects reader-facing handover identity, not physics.
4. Two-axis judgement: G-derive largely preserved; G-follow mostly preserved but weakened by overfull carryover and stale version labels.
5. False-positive self-check: bell/merged broad peak, `n=1` default, and apparent-U/eta broadening are not flagged as defects.
