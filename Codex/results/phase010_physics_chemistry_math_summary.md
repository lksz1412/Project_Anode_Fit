# Phase 010 Physics, Chemistry, and Mathematics Critic Summary

## Audit identity and boundary

- Role: fresh-context Phase 010 Sol critic for physics, chemistry, mathematics, and directly coupled code fidelity only.
- Project: `D:\Projects\Project_Anode_Fit`.
- Canonical read-only snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`.
- Authorized write directory: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase010`.
- Output population: 35 rows. This is the exact union of the in-scope Critical/High rows in Phase 005, 006, 007, and 009 after excluding `P6-CH2-012`, which is a chapter-structure/self-containment finding outside this critic's physics/chemistry/mathematics boundary.
- Phase 009 rows are preserved as required, but `P9-F001`, `P9-F002`, `P9-F006`, `P9-F007`, and `P9-F008` are explicitly treated as code-fidelity manifestations of already identified scientific root causes, not five new defects.
- No Git command was run. No source, snapshot, Claude, existing Codex result/plan, configuration, test, or repository metadata was changed. The only files created are the two authorized Phase 010 outputs.

## Executive verdict

### Publishable

**No.** The v1.0.23 physics/chemistry/mathematics are not publishable as a quantitatively defensible Chapter 1-3 scientific treatment. Six Critical findings survive direct refutation:

1. Chapter 1 public C-rate/Eyring time units are wrong by exactly 3600.
2. Chapter 1's optional self-consistent ratio is not the complete local detailed-balance closure because it omits the local reverse denominator.
3. Chapter 2 misidentifies Reynier's 0.18 kB/atom electronic state entropy as a total partial-molar entropy.
4. Chapter 2's electronic logistic gate has no source derivation for its composition kernel, width, amplitude uniqueness, or electronic-only interpretation.
5. Chapter 2 code is not composition-local even though the scientific model is written as Delta S_e(x,T).
6. Chapter 2 code freezes Delta S_e at T_ref and therefore does not implement the document's T-squared free-energy integration.

The Chapter 3 equilibrium/additive skeleton contains useful restricted mathematics, but unresolved mass normalization, stress geometry, finite-strain validity, capacity denominators, and exact inverse symmetries prevent publication-grade quantitative interpretation.

### Fit-usable

**Conditionally usable only as a phenomenological forward shape model, not as a validated physical inverse model.** Equilibrium logistic mixtures and the independent-host additive blend can be explored after an external, explicit mass/capacity basis is imposed. The following are not fit-usable for physical inference in the current version:

- resolved finite-rate lag or activation parameters through the public C-rate facade;
- the optional detailed-balance/self-consistency interpretation;
- acquisition-history or reversal fitting with the current voltage-sorted reset state;
- unique per-transition parameters in overlapping finite mixtures;
- LCO electronic gate center, width, amplitude, local composition dependence, or T-squared curvature;
- physical Si mass fraction from normalized blend shape alone;
- stress, partial molar volume, or stress-free centers from the scalar offset alone;
- cross-case Si/SiO/Si-C wt-percent comparisons using the current q defaults.

Synthetic same-model passes do not change this verdict. The shipped self-consistency script passed 5/5, but its principal gate uses its own approximate Picard update as the reference and supplies no empirical or complete-detailed-balance oracle.

### Code-ready

**No for scientific production or parameter inference.** The module imports and several restricted algebraic chains are internally deterministic, but Critical unit, closure, locality, and temperature-integration defects remain. It is code-ready only for explicitly bounded demonstrations that disable unsupported physical interpretations and do not claim experimental validation.

## Finding counts

### By chapter

| Chapter | Rows |
|---|---:|
| 1 | 14 |
| 2 | 12 |
| 3 | 9 |
| **Total** | **35** |

Chapter assignment follows the source audit stream: Phase 005 rows are counted under Chapter 1, Phase 006 under Chapter 2, Phase 007 under Chapter 3, and Phase 009 rows under the chapter named by their content.

### By severity

| Severity | Count |
|---|---:|
| Critical | 6 |
| High | 27 |
| Medium | 2 |
| Low | 0 |
| Info | 0 |

The two Medium rows are critic downgrades of prior High findings after successful partial refutation: `P6-CH2-011` and `P7-CH3-003`.

### By evidence status

| Evidence status | Count |
|---|---:|
| 확정 | 28 |
| 미결 | 0 |
| 근거 미발견 | 3 |
| 추정 | 0 |
| 미검증 | 4 |

### By disposition

| Disposition | Count |
|---|---:|
| AFFIRM | 30 |
| MODIFY | 2 |
| REJECT | 0 |
| UNRESOLVED | 3 |

### Chapter/severity matrix

| Chapter | Critical | High | Medium | Total |
|---|---:|---:|---:|---:|
| 1 | 2 | 12 | 0 | 14 |
| 2 | 4 | 7 | 1 | 12 |
| 3 | 0 | 8 | 1 | 9 |

## Disputed Critical/High rows and resolution

| Critique row | Source row | Resolution |
|---|---|---|
| `P10-PCM-008` | `P5-CH1-010` | **UNRESOLVED / 미검증.** Dahn confirms the staging sequence and Park confirms approximate specimen plateaus, but the exact four voltage anchors were not all recovered from a full primary passage. The local Ohzuku object is HTML mislabeled as PDF. |
| `P10-PCM-012` | `P5-CH1-015` | **UNRESOLVED / 미검증.** Neither +3 to +4 mV/K nor the competing roughly +0.3 mV/K value was promoted to fact because the full primary Part II figure/equation was unavailable; ResearchGate returned HTTP 429. |
| `P10-PCM-022` | `P6-CH2-010` | **UNRESOLVED / 미검증.** The explicit-n derivative is mathematically exact, but no fully retrieved experiment establishes that the fitted two-phase width is equilibrium configurational width rather than aggregate broadening. |
| `P10-PCM-023` | `P6-CH2-011` | **MODIFY; High to Medium.** The general branch-average claim is false without symmetry, but the chapter explicitly states equal-shape linearization and O(Delta U_hys^2) residuals at lines 214-219. The conditional identity is correct; the boxed general reading is not. |
| `P10-PCM-025` | `P7-CH3-003` | **MODIFY; High to Medium.** Common equilibrium potential is exact. The chapter and GS-2 already declare independent-host/additive scope, so factorization is correct inside that restriction; only detached exactness language remains scientifically misleading. |

All six Critical rows were directly recalculated or checked against full available primary text and received `AFFIRM`. No Critical row was rejected or left unresolved.

## Confirmed-correct chains

These are confirmed within their stated assumptions. They are not empirical validation of the complete model.

1. **Logistic equilibrium derivative and area.** For xi=1/(1+exp[-(V-U)/w]), dxi/dV=xi(1-xi)/w and the infinite-domain area is one; transition area is therefore Q. Numerical Chapter 3 integrations recovered code-defined Q within 6.852e-7 relative over the finite audit window.
2. **Frozen-limit memory.** `_causal_memory_ratio(g_eff=0)` is exactly the fixed-L pointwise memory path, and the shipped gate reports array equality. This confirms the reduced algorithm's frozen limit only.
3. **Explicit-n thermal derivative.** For w=nRT/F with constant n, dw/dT=nR/F. At n=1.7, direct finite difference was `1.464870187026e-4 V/K` and code returned `1.464870187076e-4 V/K`.
4. **Regular-solution curvature.** The one-coordinate regular solution gives `g''=RT/[x(1-x)]-2 Omega` and the x=0.5 spinodal condition `Omega=2RT`. This does not establish equivalence to a multi-ECI ordering model.
5. **Sommerfeld integration in the document.** If `Delta S_e=a_e T`, integrating `dU/dT=Delta S_e/F` gives the `a_e T^2/(2F)` term. The factor 1/2 is correct in the document and absent from the frozen runtime path.
6. **Reference-preserving electronic ablation arithmetic.** Re-basing the gate-off T1 enthalpy to `-377397.126219 J/mol` preserves the 298.15 K OCV exactly in the checked model. This confirms the correction to the ablation design, not the gate's physical provenance.
7. **from_wt capacity-fraction algebra.** `f=m q_Si/[m q_Si+(1-m)q_gr]` and its algebraic inverse recover m to floating-point precision when all capacities use a declared commensurate basis.
8. **Independent-host common-potential balance.** With `G_int=0`, pooling host transitions under one potential and adding host responses is mathematically consistent. A common multiplier remains under coupling, but pure-host factorization does not.
9. **Normalized blend shape under global mass rescaling.** Multiplying both host capacities by the same `(1-m)` leaves the normalized curve unchanged; measured deltas were at most `1.776e-15`. This confirms why normalized tests cannot expose the absolute mass-basis defect.
10. **Stress tensor conversion and sign.** Under tension-positive equi-biaxial plane stress, `sigma_h=2 sigma_b/3`; thus `dV/dsigma_h=(3/2)dV/dsigma_b`. Sethuraman's source sign chain is consistent, while the chapter's stress-measure label is not.
11. **Exact inverse symmetries.** Runtime probes confirmed the stress/center transformation to `1.776e-15` and the m/q composition family to `3.553e-15`. These are proofs of non-identifiability, not optimizer pathologies.

## Newly found defects

No additional row was added with `source_finding_id=NEW`. The independent probes did not establish a truly new Critical/High root cause that was not already represented in Phase 005-009. Potentially adjacent observations, such as representative-temperature averaging and FFT helper behavior, already exist below the Critical/High boundary or outside this critic's required population and were not inflated into duplicate findings.

## Conflicts with prior reports

1. Passing `G-E1` through `G-E5` does not close `P5-CH1-005`: the suite validates a reduced same-model update, while the independent nonlinear oracle gives 29.6288% peak error at epsilon=0.25 and a worse corrected result at epsilon=1.
2. Phase 009's exact document-code agreement on the C-rate and ratio paths is not scientific correctness. Those rows are faithful implementations of wrong or incomplete scientific contracts.
3. The strongest reading of `P6-CH2-011` is too severe because the current text already states the symmetry/linearization limitation and second-order residual. The remaining general boxed claim is Medium, not High.
4. The strongest reading of `P7-CH3-003` is too severe because independent-host scope and GS-2 are explicit. Common potential is exact; only unqualified factorization/additivity language is defective.
5. Phase 004's or later snippets about the MCMB Part II magnitude cannot settle the factor-ten conflict. Full primary retrieval failed, so the equation-level number remains 미검증.
6. The final master-plan hash differed from the preliminary capture available during the audit. The current file was therefore re-read lines 1-342 before drafting; the authoritative final hash is the one recorded below.

## Exact mandatory files and ranges read

All ranges in this section were read from first line through last line. Truncated outputs were closed by narrower re-reads.

| File | Range | SHA-256 |
|---|---:|---|
| `D:\Projects\AGENTS.md` | 1-83 | `68E9E237BAF478905844BB6E2FB9608695D6723CABF79FD018BD4402769BCCE0` |
| `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md` | 1-180 | `0EC0C3B153B402773F055AEF45F2C1EDF96943DE6713608820F67763FCCCEB8E` |
| `Codex\plans\2026-07-19-v1010-v1023-ch1-ch3-scientific-audit-master-plan-v2.md` | 1-342, re-read 1-342 after hash recheck | `EF3C23FEAE062D69FA25D47AB6789CBC30163D45499C482B16E88EBA15179AEC` |
| `Codex\results\PHASE_004_SCIENTIFIC_CONVENTION_AND_SOURCE_BASELINE_RESULT.md` | 1-245 | `6B7F7BCAE148F4457B7FBE3F50E6B986A7ABDFA78F27B16EEEE7DDE892284616` |
| `Codex\results\phase004_scientific_convention_registry.csv` | 1-35 | `893FA2C987D5B45A876007BD9C7A9B37D68A77CBD6B92851B08FD60BA571C3EE` |
| `Codex\results\phase004_model_dependency_graph.md` | 1-94 | `C185FF69E30A0392958FC1F7C1341333C1B1D145DEF4E1FE37FE9CFD229F92A0` |
| `Codex\results\phase004_existing_reference_claim_matrix.csv` | 1-94 | `04669194C4AADEB265267166F7D91D48F6BCFA912CBD8566F63F447456490A88` |
| `Codex\results\phase004_additional_literature_source_matrix.csv` | 1-69 | `9351C6E03A1B90FD8FA10AE049717E65FA730ACE0DE058AEC9AEE756F2815834` |
| `Codex\results\PHASE_005_CH1_SCIENTIFIC_AUDIT_AND_STRENGTHENING_RESULT.md` | 1-180 | `04D58F6684A6DB72FFEE7312747201AC887E8F6741C92102FD76F88049D3F1E4` |
| `Codex\work\agent_reports\phase005\P5_ch1_findings.csv` | 1-17 | `304D720C32138350250BDF9B9F9B17FA6B1E48AD9584787D13B54CFBD45495D1` |
| `Codex\results\PHASE_006_CH2_SCIENTIFIC_AUDIT_AND_STRENGTHENING_RESULT.md` | 1-174 | `9C7AE5B87927113CB759AC9B819936E8A7F19F21F8EBE7EA342BCDD15FD08AE6` |
| `Codex\work\agent_reports\phase006\P6_ch2_findings.csv` | 1-21 | `2CDE46AFA9CBD4061E2E122286823A0F916B89D90484B3F72401C7B0380D6E56` |
| `Codex\results\PHASE_007_CH3_SCIENTIFIC_AUDIT_AND_STRENGTHENING_RESULT.md` | 1-179 | `88540D8EDC2BCFD680EC9AC64780BFA6F55F041493BF1A349C166F11BCE7D7AF` |
| `Codex\work\agent_reports\phase007\P7_ch3_findings.csv` | 1-20 | `9F9886A6661759A5EC373904A81D41635404198F5CAB9600EA7967B5C921A8E5` |
| `Codex\results\PHASE_008_TEXTBOOK_REVIEW_THREE_CHAPTER_STRUCTURE_RESULT.md` | 1-167 | `D94D8F5DD8DEC3743BF4911D12B3728B814E3F1CB13ACAEC514B870B62B025AF` |
| `Codex\results\PHASE_009_CH1_CH3_DOC_CODE_FIDELITY_RESULT.md` | 1-160 | `7104640927AB24F8BD32D7519A2863C8B12D07A96DD8F15E808469EBF3310476` |
| `Codex\work\agent_reports\phase009\P9_code_fidelity_findings.csv` | 1-20 | `0C31CD0CB69EB199230E4C8CE391665D135E4B067569DAE8B9721FEA369E0F8A` |
| `Codex\results\equation_code_traceability.csv` | 1-64 | `7F3C247858810236C71A390121185A6435FAC567D1BC4A6BC1643510966B60E4` |
| `Codex\results\scientific_claim_evidence_ledger.csv` | 1-56 | `D1B4DEC8591123C8E427B0424B447D7594B61F1427EC556A215F0F959DA2195F` |
| `Codex\work\phase006\ch2_reynier2004_full_source_check.md` | 1-98 | `E6D78883CE0336931FA5C2BE22362D7429CE8CE653DB4327E407F112881260C3` |
| `Codex\work\phase006\ch2_motohashi2009_full_source_check.md` | 1-50 | `F3EA0449A4A298FDA9717B3AD08CDB74B0E23F5854234E14550CF1550FD4A28A` |
| `Codex\work\phase007\ch3_sethuraman_geometry_source_check.md` | 1-86 | `08143525680F18E42724ABC7A2F6420160D98AFC21CFDF35F8CCF3953640FF3D` |

## Exact pinned source/code files and ranges read

Base for every path below: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914\Claude\docs\v1.0.23`.

| File | Range | SHA-256 |
|---|---:|---|
| `Anode_Fit_v1.0.23.py` | 1-1585 | `0298BB5FDF47ED5FAF2F8301B6D84DC88FD580A69C8E616DAA3942D35CEAE7CF` |
| `test_gates_v1023_selfconsistent.py` | 1-128 | `1417277231EA795515037F470EC160E5077E04D8AB351DF7E85C6467671FCEF4` |
| `test_gates_v1023.py` | 1-626 | `78205FED4F6ED9FF731E11EDDF14F1E871EF15759CB75344F098B8D014173832` |
| `FITTING_GUIDE.md` | 1-137 | `F7CA9038E163CFBA6313F85E0CD4F3095AC2890A9FF9EB6F8AA4A8CDF12409E1` |
| `ch2_lco_v1.0.23.tex` | 1-31 | `70D3D2E6437D4640850007CBB12B29996CAE97C0E9A59AFF543E446D45DDB7F8` |
| `_sections\ch1_sec01_n0n1.tex` | 1-257 | `E040962075E33F1222128E4F86F4D474CA24E970F5285392FAFA904D3C33075D` |
| `_sections\ch1_sec07_broadening.tex` | 1-357 | `38728CD4B7D04F16A8488959C325F8F89EDAA6B37E6796AB81F635D57C79FE0B` |
| `_sections\ch1_sec08_lag.tex` | 1-145 | `A01C5394781F3674FB167846D1ACC05A49C7EC2F4C419C7480A128B1C0747723` |
| `_sections\ch1_sec10_sum.tex` | 1-170 | `5EDCCC997672641F6722CF9EAE80CB93C83345F5CC9CFAA205F500A57C16DE6E` |
| `_sections\ch1_appE_selfconsistent.tex` | 1-212 | `26C1546FCC701D8DEC6847F1AD60CBF0EA2222808FE2AAA396265A7F8641C51C` |
| `_sections\ch1v22_bib.tex` | 1-54 | `1DA789277301FD9418EB5DB578123CF234708B1161FD57193D84B66A5ADEBBAB` |
| `_sections\ch1_sec13_lcohys.tex` | 1-223 | `675AB1E3D1AF817B7D1BC4A1F01BD3E557B6DB893B784983016A0A77F00BB4C6` |
| `_sections\ch1_sec14_lcodecomp.tex` | 1-143 | `EE4404D377D0552C4F940237C89F4B6D3E5210A51D7941C63230C97622F5F389` |
| `_sections\ch1_sec15_lcoelec.tex` | 1-396 | `E3C06FB930E2ED2BA8846DEAD8B5E334904E90B96A890155F3979871F7B7A426` |
| `_sections\ch2_sec01_partition.tex` | 1-149 | `0190A6F3DC8C7AC36E3F86F17E2289307619465E5DAA32EB88A961A0344BD47F` |
| `_sections\ch2_sec02_config.tex` | 1-190 | `E3E47F6F36A84CE89D7EDDB6B14C82564FEEF2232127F64EDFF1FF0B419C030C` |
| `_sections\ch2_sec05_mixing.tex` | 1-245 | `58E8A86BE003B57D64D605396EC2B5C4623379724DDA8DB0C93EE8D9E95BE9DD` |
| `_sections\ch2_sec09_method.tex` | 1-64 | `5AC3F9C31AEA06D0D280A8AA4E08198E52AEA987916B9A042C5A8CA818464367` |
| `_sections\ch3v22_notation.tex` | 1-46 | `95803BFD722FE0E744F19F9F2A24186DEEFCA4A2E85EA5E2B36F67D75AC5F834` |
| `_sections\ch3v22_sec01_map.tex` | 1-132 | `9CD0DD3A59E9ADE09DD1F409BC8FBCEF212C5BADF4B9C13924F8EC7B14DB34EA` |
| `_sections\ch3v22_sec02_cases.tex` | 1-162 | `0C1DE56F0D970D105D9B76A7C2DBD925F4B6CF10C7305B5B81BD067387311E54` |
| `_sections\ch3v22_sec03_blend.tex` | 1-278 | `231C7A2BA10C06BA2493CC812C9CC75500B3E297FA00534E5900112B7366D7A7` |
| `_sections\ch3v22_sec04_mech.tex` | 1-111 | `0A42EA6E16678F790506B8142B686929657B27E1FA9ED2D646A2F03073CAE085` |
| `_sections\ch3v22_sec05_code.tex` | 1-70 | `D12633E5A00DC5C1DEFF10AC0EEA67965EB958F5A20C21724AF2AEA8377B905D` |

## Primary-source coverage

| Source artifact | Coverage actually completed | SHA-256 / retrieval result |
|---|---|---|
| Reynier 2004 author PDF | pages 1-7 of 7, including narrow re-read of pages 4-5 | `8A105185F844757EE12194BBB02D6CFDAD1CCA75776387752B709005E59504A8` |
| Motohashi 2009 PDF | pages 1-29 of 29 | `0C986E2A86E78393EA44AC31D582B6A5FEA57ECA3BB91021F311347884DA2F07` |
| Sethuraman 2010 author PDF | pages 1-21 of 21 | `B061FB42690EA391DB576F3239B25ACF53ED76A81C0381F7BA6D25FCEE6AACAC` |
| Persson 2010 PDF | pages 1-9 of 9 | `0EB4F7D3F61CC472C5B2BB90947B0DD85C50AAAA24C198D37F5DD19370FA7414` |
| Park 2021 PDF | pages 1-10 of 10, with truncated pages re-read individually | `99C81685F36A082376DD85D1BDE794C62AD79F71ACD8657D01562FA3EE56F1E6` |
| Bazant 2013 PDF | pages 1-17 of 17, with figure-heavy page 15 re-read | `C7D08ED617CA966A5B842BC85470A15657A82F447401CCCFB8B3FF7F3695587B` |
| Dreyer 2011 extracted text | lines 1-1587 of 1587 | `13C37AC185A74C11D28CE9FC14C581C45D7BE3F34A045F99387685BEB3E747A1` |
| Ferguson-Bazant 2014 extracted text | lines 1-706 of 706; truncation closures at 160-240 and 560-610 | `20A2B4CEDBD41E2BDEC43C984B575DC40453378A3B370602974B7F3E9D262F28` |
| Ohzuku local object | no PDF pages available; object is HTML despite `.pdf` suffix | `5040569F5E0DAC2C012E9C62C947690700C14397ADD01BD6D5CD861CCD290D62` |
| Dahn official record | full official abstract inspected | sequence supported; exact voltage anchors absent |
| Onuma official RSC HTML | identity and load-bearing K-versus-Li claim sections inspected | K-graphite primary system confirmed |
| Andersen official Nature HTML | composition and capacity-denominator passages inspected | 60% Si composition and 1000-to-600 conversion confirmed |
| Van der Ven official record | abstract/official snippets only | no equation-level ECI-to-Omega adoption |
| MCMB Part II official record | metadata/abstract/indexed snippets only; ResearchGate HTTP 429 | exact entropy magnitude remains 미검증 |

## Calculation and probe command log

Every numerical result used to adjudicate a row was regenerated in a no-write process with `PYTHONDONTWRITEBYTECODE=1` and `python -B`. The long Python probes were sent through stdin and did not create scripts or caches.

### Environment and retrieval probes

| Command or command form | Result |
|---|---|
| Preliminary PowerShell `foreach` PDF-info pipeline | ParserError: empty pipeline element. No scientific result used. The exact pre-compaction command body was not retained in the available tool transcript, so it is not reconstructed by guess. |
| `pdfinfo.cmd <pdf>` wrapper calls | Failed because the wrapper's configured path was not found. No scientific result used. |
| `python -B -c` import of `pypdf.PdfReader` | `ModuleNotFoundError: No module named pypdf`. No scientific result used. |
| Direct Poppler `pdfinfo.exe <pdf>` on the local literature set | Valid page counts recovered for Reynier 7, Motohashi 29, Sethuraman 21, Persson 9, Park 10, Bazant 17, and Dreyer 30; Ohzuku failed because the object is HTML, not PDF. |
| Bounded Reynier read using an assumed `references\Reynier_2004.pdf` path | Path not found. `rg --files` then located the exact cache path under `Codex\work\literature\reynier2004`. |
| ResearchGate MCMB Part II open | HTTP 429; no equation-level value adopted. |

### Chapter 1 probe

Command form:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
@'  # CH1-A through CH1-G: import pinned module; unit, complete-affinity,
    # cropped-state/permutation, DOP853 oracle, width derivative, PSD time,
    # and finite-mixture SVD calculations
'@ | python -B -
```

Results:

| Probe | Result |
|---|---|
| CH1-A hour/second | `L_hour=2.1438479091674980e-07`; `L_second=5.9551330810208413e-11`; ratio `3599.999999999991815`; ln ratio `8.188689124444`. |
| CH1-B complete denominator | Omega/RT 2,3,4,5 errors `13.252803%`, `36.663323%`, `99.932930%`, `271.782301%`. |
| CH1-C cropped history | max state delta `0.148582888`; max peak delta `4.952762931 1/V`; permutation/restoration delta `0`. |
| CH1-D nonlinear DOP853 oracle | epsilon 0.25: frozen `0.527921`, corrected `0.296288` relative Linf peak error. Initial epsilon 1 setup with `g_eff=8,L=0.01` gave very large `312.341672` and `530.473576`; the exact prior setup was rerun below. |
| CH1-E default width derivative | finite `8.616883453126e-5`, code implicit `0`, explicit n=1 `8.616883453387e-5`, all V/K. |
| CH1-F PSD times | r=5 um gives `633.257-25330.296 s` for D `4e-15` to `1e-16 m2/s`; tau15/tau1=`225`. |
| CH1-G mixture SVD | identical kernels rank 1; singular values `4.082482880e2`, `1.739280964e-13`; condition `17.89389417` at 5 mV and `1.134724777` at 100 mV. |

Exact certificate rerun command form:

```powershell
@'  # DOP853, V=-0.5..0.5, 20001 points; cases (g_eff,L)=(2,.01),(4,.02)
'@ | python -B -
```

- epsilon 0.25: frozen `0.527921062`, ratio `0.296288317`.
- epsilon 1.0: frozen `2.208775097`, ratio `2.615123698`.

Exact thermal end-to-end rerun command form:

```powershell
@'  # dH=-F*0.1, x_bar=.25, dt=1e-3; implicit default versus explicit n=1
'@ | python -B -
```

- implicit: finite `-9.46661405376581e-5`, analytic `0`, difference `9.46661405376581e-5 V/K`.
- explicit: finite `-9.46661405376581e-5`, analytic `-9.46661405191571e-5`, difference `1.85009478440371e-14 V/K`.

### Chapter 2 probe

Command form:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
@'  # CH2-A through CH2-J: source-quantity conversion, gate amplitude/locality,
    # T^2 integration, identifiability, ablation, factorization, regular solution,
    # branch average, and explicit-n thermal derivative
'@ | python -B -
```

Results:

| Probe | Result |
|---|---|
| CH2-A Reynier conversion | `0.18R=1.496520000 J/(mol K)` and `0.20R=1.662800000 J/(mol K)`; conversion does not alter state-versus-derivative identity. |
| CH2-B gate arithmetic | center `-45.678261885287 J/(mol K)`; implied endpoint state entropy `9.135652377057 J/(mol K)=1.098827565198R`. |
| CH2-C locality | `_effective_dS_rxn=-39.678261885287 J/(mol K)` at 278.15, 298.15, and 318.15 K; no runtime x argument. |
| CH2-D T-squared difference | exact-frozen `-0.317574009`, `-0.714541519`, `-1.984837553 mV` at absolute Delta T 20,30,50 K. |
| CH2-E gate identifiability | `(13,.05)`, `(26,.10)`, `(6.5,.025)` and translated centers 0.75/0.85/0.95 all give `-45.678261885287`. |
| CH2-F x_bar=.50 ablation | gate on `3.924249955 V, -0.312434776 mV/K`; fixed-dH off `4.042610795 V, -0.034630812`; rebased off same OCV and `+0.053922762`. |
| CH2-G factorization | independent Z=`4`; beta J=1 coupled Z=`3.367879441171`; ratio `0.841969860293`. |
| CH2-H regular solution | at x=.5, g'' is `9915.2764`, `0`, `-4957.6382 J/mol` for Omega/RT 0,2,3. |
| CH2-I branch mean | equilibrium slope .100 plus branch residuals +.300,+.100 gives mean .300; +.300,-.300 recovers .100 mV/K. |
| CH2-J explicit n | n=1.7 finite derivative `1.464870187026e-4`; analytic/expected `1.464870187076e-4 V/K`. |

Reference-preserving x_bar=.85 ablation rerun command form:

```powershell
@'  # instantiate gate on, gate off fixed dH, and gate off with T_ref-rebased dH
'@ | python -B -
```

- on: `Uoc=4.009535354 V`, `dUdT=-0.127657667 mV/K`, `dH1=-391016.1 J/mol`.
- off fixed dH: `Uoc=4.100834215 V`, `dUdT=+0.160354448 mV/K`.
- off rebased: `Uoc=4.009535354 V`, `dUdT=+0.106707636 mV/K`, `dH1=-377397.126218902 J/mol`.

### Chapter 3 probe

First command form:

```powershell
@'  # CH3-A through CH3-H, initial integration call used np.trapz
'@ | python -B -
```

Result: it printed the m=0 and m=0.1 analytical mass ratios, then stopped with `AttributeError: module numpy has no attribute trapz`. No omitted result was inferred.

Corrected rerun command form:

```powershell
@'  # identical CH3-A through CH3-H probe with np.trapezoid
'@ | python -B -
```

Results:

| Probe | Result |
|---|---|
| CH3-A mass basis | code/fixed=`1`, `1.111111111111`, `1.25`, `1.428571428571` at m=0,.1,.2,.3. Integrated relative error at m=.3 `-6.852e-7`; normalized delta `8.882e-16`. |
| CH3-B common potential | same fugacity with independent Z=`4`, coupled Z=`3.367879441171`; factorization difference `18.769097%`. |
| CH3-C stress geometry | measured 100,104,110,125 biaxial maps to 150,156,165,187.5 hydrostatic; theoretical hydrostatic `92.138674` and biaxial `61.425783 mV/GPa`. |
| CH3-D finite strain | 270%: J=3.7, stretch `1.546680374`, engineering `54.668%`, Hencky `43.611%`; 300%: J=4, stretch `1.587401052`. |
| CH3-E capacity basis | ideal 60% Si plus 30% graphite upper bound `2259 mAh/g`; treating 3117 as total exceeds it by `858`. Explicit 1000 per-Si maps to `600` per total at 60% Si. |
| CH3-F stress symmetry | equilibrium and dqdv max delta `1.7763568394e-15`; solve_U_oc delta `0`. |
| CH3-G composition symmetry | f=.6 families `(m,q)=(.1,5022),(.2,2232),(.3,1302)` all Q=`2.425`; curve deltas `0` and `3.553e-15`. |
| CH3-H from_wt inverse | recovered m errors `-1.388e-17`, `0`, and `-5.551e-17` for the three checked cases. |

### Existing self-consistency suite

Command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -B .\test_gates_v1023_selfconsistent.py
```

Result: exit 0, `SELF-CONSISTENT GATES: ALL PASS (5/5)`. Key outputs were G-E1 exact frozen recovery, G-E2 array equality, G-E3 same-update Picard improvement for its checked points, G-E4 relative RMS `3.96e-6`, and G-E5 liveness max difference `0.9400`. This result is retained as same-model behavior only.

`test_gates_v1023.py` was fully read but not executed because its workflow creates temporary variants outside the authorized output-only write boundary.

### Enumeration, hash, and validation probes

| Command or command form | Result |
|---|---|
| `rg -n --no-heading 'Critical|High' <mandatory ledgers>` | Output was truncated at 19,848 tokens; no count was inferred from the truncation. Exact CSV enumeration was then used. |
| `Import-Csv ... | Where severity in Critical,High` on Phase 005/006/007/009 | Recovered source rows; exact automated union below returned 35 after the explicit scientific-boundary exclusion of `P6-CH2-012`. |
| Attempted `[int]$_.probe_id` filter on `ch1_scientific_probe_results.csv` | Failed for string IDs such as `UNIT-01` and `THERM-01`; corrected exact string filter recovered the four THERM-01 rows. |
| Full SHA-256/line-count PowerShell inventory using `Get-FileHash` and `Get-Content.Count` | All listed mandatory and controlling files existed; hashes and ranges are recorded in the tables above. |
| `Get-FileHash` repeat on the master plan | Current authoritative hash `EF3C23FEAE062D69FA25D47AB6789CBC30163D45499C482B16E88EBA15179AEC`; triggered full lines 1-342 re-read. |
| Preliminary `Get-ChildItem` on Phase 010 output directory | Directory did not yet exist. It was then created and only the two authorized outputs were written. |

## Source limitations and unverified items

1. Ohzuku 1993 was not retrieved as a valid PDF. Exact graphite voltage anchors therefore remain 미검증.
2. MCMB Part II full primary text was not retrieved. The +3 to +4 versus roughly +0.3 mV/K conflict remains unresolved; snippets are not equation evidence.
3. Van der Ven's full equation-level cluster-expansion derivation was not locally retrieved. The audit confirms that no inspected source establishes the printed one-Omega equivalence; it does not substitute a new ECI parameterization.
4. No primary experiment was fully retrieved that identifies fitted two-phase logistic width with equilibrium configurational entropy over the code's nRT/F path. That adoption remains 미검증.
5. Onuma and Andersen official HTML passages were used for source identity and explicit composition/denominator statements, not as full-paper equation adoptions beyond those passages.
6. Synthetic ODE, SVD, and invariance probes establish mathematical behavior of the pinned model. They are not empirical validation against company or experimental data.
7. No real-data fit, external validation set, uncertainty calibration, or material-specific stress/composition measurement was supplied or run in this critic task.

## Mechanical validation record

The final validation command parses the CSV with Python's `csv` module, compares the literal header, checks all cells and enums, checks finding/source-ID uniqueness, reconstructs the exact in-scope source-ID union, resolves each semicolon-separated local citation, verifies every cited range against current line count, verifies output scope, and computes SHA-256.

Recorded CSV validation before summary finalization:

- File exists: PASS.
- Row count: 35.
- Exact header: PASS.
- Unique `finding_id`: PASS, 35/35.
- Unique `source_finding_id`: PASS, 35/35.
- In-scope source finding coverage: PASS, exact 35/35; missing 0; extra 0.
- Explicitly excluded non-scientific row: `P6-CH2-012` only.
- Nonblank cells: PASS.
- Severity enums: PASS.
- Evidence-status enums: PASS.
- Disposition enums: PASS.
- Local controlling citations: 124 ranges checked; missing files 0; invalid/out-of-range citations 0.
- CSV SHA-256: `7E6EFFD1A52624C8B1047FCA15DF53E6F9DAEC2FBDE57D4D8E89C4AC2389A8BB`.

Final cross-file validation results are completed after both outputs exist and are recorded below by the final validation patch.

- Final output-file set: PASS; exactly `P10_physics_chemistry_math_critique.csv` and `P10_physics_chemistry_math_summary.md`.
- Final CSV parse/schema/content validation: PASS; 35 rows, exact header, unique IDs, no blank cells, exact prior-ID coverage, and all enums valid.
- Final Markdown required-section validation: PASS; all 14 required audit/report sections and both no-Git/no-source-change declarations are present.
- Final local citation/range validation: PASS; 124 controlling ranges, 0 missing files, 0 malformed or out-of-range citations.
- Final input hash recheck: PASS; 22 mandatory records, 24 pinned source/code files, and 9 local primary artifacts matched the recorded SHA-256 values.
- Final CSV SHA-256: `7E6EFFD1A52624C8B1047FCA15DF53E6F9DAEC2FBDE57D4D8E89C4AC2389A8BB`.
- Summary canonical SHA-256: `533C588C903720398BBAB7A22DB33601346BB317B3C5F0F9726596621F5E9B23`

The canonical summary hash is defined as SHA-256 of this file's UTF-8 bytes after replacing the 64-hex value on the `Summary canonical SHA-256` line with the literal token `P10_SUMMARY_CANONICAL_SHA256`. This makes the reported digest mechanically self-verifiable without the impossible requirement that a file contain its own ordinary byte hash.
