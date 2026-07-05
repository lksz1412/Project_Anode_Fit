# V1015 P1 RESULT — 앵커·증판 (2026-07-05)

> 마스터 = `../../plans/2026-07-05-v1015-code-doc-sync-master-plan.md`(rev.2). Phase P1(Steps 1–4). 성격 = 비파괴 앵커. 다음 = P2 Fable 물리 논리 6종 검토·보고.

## 1. Phase 목표
격자 퇴출·점별 재아키텍처의 **앵커 확립**: v1.0.15 증판 + baseline gate(격자 아키텍처 마지막 기준선) + 격자 의존 전수 맵 + dead/essential·피팅 파라미터 인벤토리. 코드·문건 무변경(복제·버전 문자열만).

## 2. 작업 내용 (Steps 1–4)
- **S1 증판**: `docs/v1.0.14/` 소스 14개 → `docs/v1.0.15/` 복제(빌드산물 .aux/.log/.out/.toc/.pdf·__pycache__·HANDOVER 제외). 버전 태그 파일 rename(`Anode_Fit_v1.0.15.py`·`graphite_ica_ch1/ch2_v1.0.15.tex`·`sample_test_v1015.py`·`graph_suite_v1015.py`·`sample_test_v1015.png`·`figs/graph_suite_v1015.png`). 기능적 경로 패치(하드코딩 절대경로·import·출력경로 → v1.0.15). 버전 문자열 정밀 패치 = **현행 선언만 1.0.15**(release·pdftitle·\lhead·\date·문건-코드 matched·파일명 참조), **이력 전부 보존**(계보 체인 …1.0.13→1.0.14→1.0.15·"v1.0.14 R2 정정"·"루프 B"·"pre-v1.0.14 demo"·"Part 0/II 신설 v1.0.14 P2.1"·appendix "Step 7" provenance·"v1.0.14 신설 가드"). blind replace 없이 literal 타깃(py 23건·tex 14건).
- **S2 baseline gate**: 아래 §5.
- **S3 격자 의존 전수 맵**: 아래 §6.
- **S4 인벤토리**: 아래 §7.

## 3. 산출물
- `docs/v1.0.15/`(14 소스 + 빌드 pdf/figs) — 자립 검증됨.
- 본 RESULT + `V1015_EXECUTION_LEDGER.md`.

## 4. Read Coverage
Ch1 `graphite_ica_ch1_v1.0.15.tex`(3445줄, Explore agent 전문 매핑)·Ch2(795줄, Explore agent 전문+갭)·코드 `Anode_Fit_v1.0.15.py`(dqdv L400–518·헤더 L1–164·heat L520–730·보존구역 L74–132 직접 정독)·plans(v1010 마스터·v1013 마스터·Fable v1015)·results(V1013/V1014)·V1014_EXECUTION_LEDGER·스킬 `competition-cherrypick-authoring`·세션 로그 f45f576c(격자 논의 스킴).

## 5. 게이트 결과 (전 green ✓)
| 항목 | 결과 |
|---|---|
| 회귀 `test_regression_graphite.py`(무인자 verify) | 13/13 bit-exact PASS ✓ |
| Ch1 빌드(xelatex 2-pass) | 0-err / 57p / undefined 0 / overfull>10pt 0 ✓ |
| Ch2 빌드 | 0-err / 14p / overfull>10pt 0 ✓ |
| appendix 빌드 | 0-err / 8p / overfull>10pt 0 ✓ |
| demo_lco_heat / sample_test / graph_suite | 전부 DONE(v1.0.15 figs 재생성) ✓ |

## 6. S3 — 격자 의존 전수 맵 (퇴출 대상 + 처분 초벌)
**코드 `Anode_Fit_v1.0.15.py`** (라인 = v1.0.14 복제라 동일):
| 위치 | 항목 | 처분(Step) |
|---|---|---|
| L257–278 생성자 | grid_pad_lo/hi·n_work_min·min_lag_grid_steps·v_span_floor | 제거(S21) |
| L400–518 `dqdv` | V_work linspace(L451)·grid_step(L452)·T_work np.interp(L458)·ν 스위치(L499)·_causal_lowpass(L508/510)·dqdv_out np.interp(L517) | 점별 재구현(S20) |
| L113 `_causal_lowpass` | 격자 lfilter 점화식 — dqdv 만 호출 → 재아키텍처 후 dead | 삭제(S21) |
| L83 `func_U_j_hys` | 이미 dead(func_dU_hys+func_U_branch 대체) | 삭제(S21) |

**문건 Ch1 `graphite_ica_ch1_v1.0.15.tex`** (라인 = v1.0.14, P3 편집 시 ±이동):
| 위치 | 항목 | 처분(Step) |
|---|---|---|
| §1.3 L964–987 | eq:vwork 작업 격자 절 | 연속형 재서술(S12) |
| §1.9 L1993 | eq:memory 연속 적분형(이미 유도) | 계산 정본 승격(S9) |
| §1.9 L1999 | eq:lowpass 이산 점화식 | 이력 각주 강등(S9) |
| §1.9 L2053–2069 | eq:branch 분기 스위치 + 23% 점프 | 제거→L_V→0 극한 유도(S10) |
| §1.9 L2066 | ν 각주 | 삭제(S10) |
| L2192 | staging 주석 "$L_V\ll\nu\Delta_\mathrm{grid}$" | 연속형 언어(S12) |
| L183/209 | spine 그림 라벨 | 연속형(S12) |
| 부록 A L3259 | R5(이산형 매끈환원 부정·스위치 필요) | 재유도(S11) |
| 부록 B L3353 | tab:inputs 격자 파라미터 행 | 제거(S12) |
| L3138 | keybox 6단계 (2)V_work·(5)ν | 갱신(S12) |
| FITTING_GUIDE | ν 행·문턱 70–74 kJ/mol(ν·Δ_grid 기반) | 소거·재산출(S13) |

## 7. S4 — dead/essential + 피팅 파라미터 인벤토리
**essential(활성 — 유지 + P5 정확성 재검산)**: func_w·func_U_j·func_ksi_eq·func_L_q(L372 활성)·func_dU_hys·func_U_branch·func_dH_a_eff·func_chi_d·func_dSe_molar·GRAPHITE_STAGING_LIT·LCO_MSMR_LIT·equilibrium·curve·entropy_coefficient·reversible_heat·irreversible_heat·_effective_dS_rxn·_resolve_lag_length·_build_seed_L_V·_chi_and_dH_eff·LCOCathodeDQDV.
**dead(P5 S21 삭제)**: `_causal_lowpass`(dqdv 재구현 후 orphan)·`func_U_j_hys`(이미 orphan).
**피팅 파라미터(격자 제거 후 잔존 핸들)**: n_j·U_j(dH_rxn/dS_rxn)·Ω(Omega)·gamma·h_eta·dH_a·χ(chi)·z_cut·A_cap_RT·dVdq_qa·Q_j·w·Rn·Cbg·L_V(파생). **제거**: grid_pad_lo/hi·n_work_min·v_span_floor·min_lag_grid_steps.

## 8. 결정 사항
- dead 삭제 확정(사용자). 골든 재정초는 P5(등가 3종 검증 후). 격자 서술 교정 theory-first(P3 → P5).

## 9. 이월 / 노트
- appendix `\date` "(본문 편입 여부는 검토 후 결정)"은 사용자 별도유지 확정으로 stale — Fable 별도문건 content라 버전 패치서 제외, P7에서 정리 여부 판단.
- Ch1 문건 grid-point 라인은 P3 편집 진행 중 이동 — 각 Step 착수 시 재확인.

## 10. 검증(명령+결과)
`python test_regression_graphite.py` → GRAPHITE 0-DIFF PASS ✓ / `xelatex` ch1·ch2·appendix → 0-err ✓ / 잔재 grep: 현행 오선언 0(잔존 '1.0.14' 전건 이력 확인).

## 11. 다음 단계
**P2** = Fable 물리 논리 6종(Codex 3 + Opus 3) 독립 검토 → union → 공통=진짜·단독=master(Opus) 재검 → `V1015_P2_PHYSICS_REVIEW.md` 보고(자동수정 X, Decision Gate). 대상 = Ch1·Ch2 물리·화학 논리(격자 퇴출로 바뀔 §1.9/R5 제외).
