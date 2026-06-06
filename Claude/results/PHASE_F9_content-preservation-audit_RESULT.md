# Phase F.9 — 내용 누락·왜곡 정밀 감사(신규-track vs 구-track) Result

**Date**: 2026-06-06 · **트리거**: 사용자 "내용이 많이 사라진 느낌 — 포맷 정제 이외에 진짜 누락·왜곡·생략이 있었는지 과거 파일·커밋 기록 찾아 확인"

## 결론 요약(4-tier)
- **확정 ①**: \emph{교과서 포맷 정제(W·F 라운드)는 내용 누락 0}. 38식·11절·48라벨 전부 보존, 문서는 오히려 \emph{증가}(R.9 879줄 → 현재 924줄, §6 신설). 포맷 라운드 결백.
- **확정 ②**: "많이 사라진 느낌"의 실체 = \emph{신규-track(924줄)이 구-track `ch1_rebuilt`(1635줄)의 절반}. 단 이는 포맷 정제 때문이 \emph{아니라}, **06-03 from-scratch 재작성(사용자 "blank-page clean-spine rebuild" 지시)** 시 \emph{구-track 의 거대한 Appendix B(흡수된 구 Ch6)를 신규-track 에 싣지 않았기 때문**.
- **확정 ③**: 그 Appendix B 재료는 \emph{삭제된 게 아니라 archive 에 보존**됨. 신규-track 본문은 "부록"을 2회 참조하나 그 부록이 현재 파일에 없음.
- **결정 필요**: Appendix B(피팅 워크플로·수치 closure) + DVA 를 신규 구조에 \emph{이식}할지, 의도적으로 분리 유지할지.

## 증거

### A. 신규-track 내부(R→A→W→F): 누락 0
- 수식 라벨 **38개 전부**·절 **11개 전부**·라벨 48 = 보존(F.7 감사).
- 줄 궤적: R.9 879 → A 971(+§6) → W 958 → F 924. \emph{R.9 대비 +45줄(순증가)}. 페이지 19→21→20→19 = A 추가(+2p)/W·F 군더더기·스캐폴딩 제거(−2p). 물리 silent 누락 0.
- §6(stattools) W 재서술도 5식(density·norm·wavg·varprop·jacobian) 전부 보존.
- git diff 104f28f→f63b0b7(커밋된 register 라운드) = 격식 문구만, 수식·논리 불변.

### B. 신규-track(924줄) vs 구-track ch1_rebuilt(1635줄) — topic 대조
| 구-track 보유 | 신규-track | 판정 |
|---|---|---|
| 핵심 도출(charge·logistic·Eyring·barrier·spectrum·kernel·falsify) | **전부 보유**(+§6 통계절·§overlap 다전이·eqpeak 3결과 \emph{신규 추가}) | 핵심 물리 완비·오히려 확장 |
| 자기참조 결합 → **Volterra 적분식** | 없음 — \emph{forward-only 예측}으로 대체(역산 금지, OCV-anchor) | \emph{방법론 재설계}(누락 아님; 순환 의존은 implicit charge-balance 로 정직 표기, 공선형 8회·순환 3회·식별 7회 언급) |
| **closure Plan A/B**·g-grid·Fredholm·**DAE 수치엔진** | 없음(grep 0) | Appendix B 영역 — 미포함 |
| **S1~S6 피팅 워크플로 구현**(수치) | 식별 \emph{순서} S1~S4 개념만(§synth) — 상세 구현 없음 | Appendix B 영역 — 미포함 |
| identifiability 상세·GITT/Arrhenius/C-rate \emph{피팅 절차} 절 | GITT 4·Arrhenius 9회 \emph{참조}만, 상세 절차는 "부록"으로 deferral | Appendix B 영역 — 미포함 |
| **calorimetry·발열** 항 | 없음(grep 0) | 미포함 |
| **DVA(dV/dQ)** | 없음(grep 0; 신규는 ICA/dQ/dV 전용) | scope: ICA 전용 |
| 충전·full-cell 확장 | 경계 주(out-of-scope)로만 4회 언급 | scope 경계 명시 |

### C. 구 Appendix B 재료 보존 위치(삭제 아님)
- `Claude/docs/Archive_old/graphite_ica_ch1_appendixB_fitting.tex` (909줄)
- `Claude/docs/Archive_rebuilt/graphite_ica_ch1_rebuilt.tex` (1635줄, 본문+Appendix B)
- `Claude/docs/Archive_old/graphite_ica_consolidated_ch1.tex` (886줄) 등 + git 이력(구-track 커밋 다수)

## 판정
- 포맷 정제로 인한 누락·왜곡·생략 = **없음**(확정).
- 신규-track 은 구-track 의 **핵심 물리 도출을 완비**(일부는 더 확장: §6·§overlap·eqpeak 3결과)했고, 자기참조 closure 는 \emph{forward-only 로 의도적 재설계}.
- 구-track 의 **Appendix B(피팅 워크플로 S1~S6 구현·Volterra/DAE 수치 closure·identifiability 상세·GITT/Arrhenius/C-rate 피팅·calorimetry·full-cell 확장·assumption ledger) + DVA** 가 신규-track 에 미포함 — archive 에 보존. 본문은 "부록" 참조하나 부록 미첨부.

## 결정 필요(사용자)
구 Appendix B + DVA 를:
- (가) 신규 Ch1 의 \emph{부록}(또는 별도 챕터)으로 \emph{이식·교과서화} — 본문 "부록" 참조가 실체를 갖게 됨, 또는
- (나) 의도적 분리 유지(신규 Ch1 = 핵심 도출 전용, 피팅/수치는 별도 트랙).

## Read Coverage
- 신규-track 전문(F.0~F.8) + 구-track ch1_rebuilt 섹션 구조 정독 + topic grep 대조 + zip/archive/git 이력 전수 탐색.
