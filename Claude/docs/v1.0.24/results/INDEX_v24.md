# INDEX — v1.0.24 산출물 색인

> 반영 버전: @3 Si Frumkin·@5 stage-2L·LCO 전자항 토글·#7·#1. 시작점 = HANDOVER_v24.md.

## 문건 (3 챕터, 빌드 산출 PDF)
| 파일 | 내용 | 신규 소절 |
|---|---|---|
| `ch1_graphite_v1.0.24.{tex,pdf}` | 흑연 dQ/dV 이론+Part T 열특성 (89p) | **§1.5.4** stage-2L 엔트로피 온도분리(`ch1_sec05b_gr2L.tex`) |
| `ch2_lco_v1.0.24.{tex,pdf}` | LCO 양극 (27p) | **§2.6.1** per-peak Ω·#7·전자항 토글(`ch1_sec16b_lcoomega.tex`) |
| `ch3_si_v1.0.24.{tex,pdf}` | Si·혼합음극 (19p) | **§3.2.5** Si-host Frumkin 커널(`ch3v22_sec02b_sifr.tex`) |
| `_sections/` (57 파일) | 절 원본 (신규 3 포함) | — |
| `_sections/ch{1,3}v22_bib.tex` | 서지 (신규 schmitt2022·artrith2018·verbrugge2017) | — |

## 코드
| 파일 | 내용 |
|---|---|
| `Anode_Fit_v1.0.24.py` | 반영 4건: `GRAPHITE_STAGING_XRD_v1024`(@5)·`_regsol_dqdv`+equilibrium 분기(@3)·`LCOCathodeDQDV(include_electronic_entropy)`(토글)·`func_L_q` 단위주석(#1). 기본 경로 bit-exact. |
| `test_gates_v1024.py` | 회귀 게이트(G1 bit-exact·G2·G3·n(T)·R6 블렌드). |
| `test_gates_v1024_reflect.py` | 반영 게이트 4종(@5·토글·@3·#1). |

## 마감·검증 문서 (`results/`)
| 파일 | 내용 |
|---|---|
| `HANDOVER_v24.md` | **시작점** — 무엇을·핵심결과(정직)·사용법·한계. |
| `MERGE_READINESS_v24.md` | 9항 게이트(9/9 PASS). |
| `REFLECT_SEED_TABLE.md` | R0 사양 원천(@3/@5/토글/#1/#7 확정물리·값·서지). |
| `PHASE_R0/R1/R2/R3_RESULT.md` | 단계별 Result(11항). |
| `V1024_REFLECT_EXECUTION_LEDGER.md` | 실행 원장(12-col, R0–R4). |
| `snapshot_v1024_R0.json` | R0 구조 스냅샷. |
| `reflect_curves.png`·`v1024_reflect_curves.py` | 신규 기능 곡선 물리타당성(매끈·단일봉·토글). |
| `comp_R1/W1..W9/` | R1 경쟁저작 9창(체리픽 base=W9)+AUTHOR_BRIEF. |

## 근거 (`Claude/results/comp_v24/`, 반영 前 조사)
- `T_SPLIT_FINDING.md`+`T_split.png` (stage-2L 재현 0.271 mV/℃), `LCO_DIAGNOSIS.md`, `CODEX_REVIEW_VERIFICATION.md`(#1·#7), `GRAPHITE_STAGING_XRD.md`, `SESSION_AUDIT_v1024.md`, ablation/regsol/lco png·json.

## 계획서
- `Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md` (11-section).

## 빌드
`xelatex -interaction=nonstopmode` 3-pass, **ch1 먼저**(xr), 그다음 ch2·ch3. (헬퍼: scratchpad `build_v1024.sh`.)
