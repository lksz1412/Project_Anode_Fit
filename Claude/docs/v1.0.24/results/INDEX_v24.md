# INDEX — v1.0.24 산출물 색인

> 반영 버전: @3 Si Frumkin·@5 stage-2L·LCO 전자항 토글·#7·#1. 시작점 = HANDOVER_v24.md.

## 문건 (3 챕터, 빌드 산출 PDF)
| 파일 | 내용 | 신규 소절 |
|---|---|---|
| `ch1_graphite_v1.0.24.{tex,pdf}` | 흑연 dQ/dV 이론+Part T 열특성 (91p) | **§1.5.4** stage-2L 엔트로피 온도분리(`ch1_sec05b_gr2L.tex`) + 6-gallery 해상도 사다리 |
| `ch2_lco_v1.0.24.{tex,pdf}` | LCO 양극 (28p) | **§2.6.1** per-peak Ω·#7·전자항 토글(`ch1_sec16b_lcoomega.tex`) |
| `ch3_si_v1.0.24.{tex,pdf}` | Si·혼합음극 (20p) | **§3.2.5** Si-host Frumkin 커널(`ch3v22_sec02b_sifr.tex`) |
| `_sections/` (57 파일) | 절 원본 (신규 3 포함) | — |
| `_sections/ch{1,3}v22_bib.tex` | 서지 (신규 schmitt2022·artrith2018·verbrugge2017) | — |

## 코드
| 파일 | 내용 |
|---|---|
| `Anode_Fit_v1.0.24.py` | 반영 4건: `GRAPHITE_STAGING_XRD_v1024`(@5)·`_regsol_dqdv`+equilibrium 분기(@3)·`LCOCathodeDQDV(include_electronic_entropy)`(토글)·`func_L_q` 단위주석(#1). **+감사 정정**(regsol 용량 `wi=Q/xg.size`·주석 다수) **+6-gallery opt-in** `GRAPHITE_STAGING_MSMR6_LIT`(IMPROVEMENT #1). 기본 4전이 경로 bit-exact. |
| `test_gates_v1024.py` | 회귀 게이트(G1 bit-exact·G2·G3·n(T)·R6 블렌드). |
| `test_gates_v1024_reflect.py` | 반영 게이트 4종(@5·토글·@3·#1). |
| `test_gates_v1024_selfconsistent.py` | 부록 E 자기일관 게이트 5종(동결 bit-exact·전달함수 잔차). |
| `CODE_GUIDE_v24.md` | **코드 이해 가이드** — 구조도·플로우차트(mermaid)·평형 커널분기·옵션 전수·사용법 복붙예·상수·변수/기호 사전. |
| `FITTING_GUIDE.md` | 피팅 절차 가이드(파라미터 tier·초기값·경계·수렴·역식별 사슬). |

## 공개 실측 검증 + 전수 감사 (R4 후 강화, `Claude/results/comp_v24/`)
| 파일 | 내용 |
|---|---|
| `FIT_CHECK_v1024.md` | 공개 실측 dQ/dV 피팅 재현(@3/@5 실경로): 흑연 0.9731·Si 0.9944·블렌드 0.9848·LCO 0.94–0.9999. 정직 한계. |
| `final_fit_sintef.png`·`v24_sintef_fit.py` | SINTEF 실측 흑연·Si·블렌드 피팅 그림·스크립트. |
| `sintef_data/{gr,si,sigr}.csv`·`SOURCES.md` | SINTEF Zenodo 20086298 delith 세그먼트 **영구보존**(재다운로드 불필요). |
| `AUDIT_v1024_DOC_CODE.md` | **전수 doc↔code 정합 감사**(6에이전트+재검증): BUG 0, 코드버그 1 수정·주석/문서 다수 정정. |
| `IMPROVEMENT_DIRECTIONS.md` | 모델 개선 후보 랭크(#1 전이 4→6·#2 비대칭폭·#4 정칙용액) — 실측 검증·P5 선택. |
| `DATA_REGISTRY.md`·`fit_registry.md` | 실측 피팅 데이터 레지스트리(출처·결과·파라미터 분포). |

## 마감·검증 문서 (`results/`)
| 파일 | 내용 |
|---|---|
| `HANDOVER_v24.md` | **시작점** — 무엇을·핵심결과(정직)·사용법·한계. |
| `MERGE_READINESS_v24.md` | 10항 게이트(10/10 PASS · R4 후 공개실측+전수감사로 강화). |
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
