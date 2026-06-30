# 작업계획서 — 코드 그래프 검증 + 코드·문건 1.0.10 통일 + 총체 검수

> 사용자: "코드로 그래프 그려 정상 개형 보여줘 + 의견 + 문건/코드 총체 정합 + 코드도 문건과 동일 버전(★1.0.10)으로 통일." 밤새 무중단 완수(아침 검토). GO 불요(사용자 "작업계획서 세운 뒤 작업해와·다 진행해놔").

## 1. Summary
재작업 산출(Ch1 v10·코드 v12·Ch2 v5)이 *실제로 정상 작동*하는지 **코드로 dQ/dV 그래프를 그려 검증**(radius `fig_bell_vs_spike.png` 식)하고, **코드·문건이 서로 정합**(문건 broadening/w 현상학·전이 분류와 코드 거동 일치)한지 총체 점검한 뒤, ★**코드와 문건을 동일 버전 1.0.10 으로 통일**(라벨·파일명·INDEX). 결과 = 그래프 이미지 + 내 의견 + 정합 verdict.

## 2. Current Ground Truth
- 코드 v12(`results/code/Anode_Fit_v12.py`, 695줄): use_w_eff(면적보존 버그) 제거·v11 거동 동일(diff 0)·단일 LiC₆ 면적 0.495≈Q·FWHM 42.3mV 종(round-trip 검증됨).
- Ch1 v10(`docs/Ch1_v10/graphite_ica_ch1_v10.tex`, 34p): broadening 3기작(L_V+내재+집합 통계역학 apparent-U=U_j+η)·w 현상학적 자유 피팅·사이즈 제외·two-phase=LiC₁₂·LiC₆ 2개. 모델 = 단일 유효입자+L_V(다입자 모델 X).
- Ch2 v5: w_eff 제거·통계열역학 본체.
- radius 샘플: `results/research/radius/fig_bell_vs_spike.png`(3패널: 기본 종/단일 LiC₆ 종/w_eff 깨진 종) — 비교 기준.
- ★버전: 사용자 "여전히 1.0.10" — 코드·문건 동일 1.0.10 통일.

## 3. Phase Range
| Phase | 이름 | Steps |
|---|---|---|
| G1 | 그래프 생성(코드 v12 → dQ/dV plots) + 정상 개형 검증 | 1–4 |
| G2 | 코드·문건 정합 점검(모델·w·전이·broadening) | 5–8 |
| G3 | ★버전 1.0.10 통일(코드·문건 라벨·파일명·INDEX) | 9–11 |
| G4 | 총체 검수(문건 정확·코드 정확·정합 — adversarial) | 12–14 |
| G5 | 종합 + 그래프·의견 제시본 | 15–16 |

## 4. Non-goals
- ★다입자/PSD convolution 모델 코드화 X(DG3·사이즈 제외). 코드는 단일 유효입자+L_V 유지(문건 모델과 일치). 집합 통계역학은 *문건 설명*.
- 코드 *기능* 대수정 X — v12 가 이미 정상(검증됨). 본 작업 = 검증·정합·버전 통일.
- v11 원본 불가침(1.0.10 은 v12 기반 새 파일). 이전 result·radius 산출 불변.

## 5. Implementation Changes
- 그래프: `results/code/plot_dqdv.py`(플로팅 스크립트) → `results/code/figs/`(PNG: 전이별 종·full dQ/dV·온도 비교·radius 식 패널).
- 버전: `results/code/Anode_Fit_v1.0.10.py`(=v12 + 헤더 1.0.10) · `docs/Ch1_v1.0.10/graphite_ica_ch1_v1.0.10.tex`(=v10 + 버전 라벨 1.0.10). INDEX·matched 표기.
- 종합 `results/process/GRAPH_VERIFY_RESULT.md`(그래프·의견·정합 verdict).

## 6. Phase 상세 (5-stage)
### G1 (1–4) 그래프 생성·검증
- `plot_dqdv.py`: Anode_Fit(1.0.10) import → (a) 단일 LiC₆ 평형 peak(종·FWHM·면적) (b) full dQ/dV 4전이+꼬리(종·매끄러움) (c) 충/방전 히스(분기) (d) 온도 비교(폭 RT/F 추종) (e) ★radius 식 패널(기본 종 / 단일 LiC₆ 종 — w_eff 없으니 깨진 패널 대신 정상만). PNG 저장. **Gate**: 모든 그래프 종모양(뾰족이·깨짐 0)·면적 보존·실행 0-error·실측-급 개형.
### G2 (5–8) 코드·문건 정합
- 코드 거동 ↔ Ch1 v10 서술 대조: ① 단일 유효입자+L_V(다입자 X) 일치 ② w=현상학적 자유 피팅(use_w_eff 없음) 일치 ③ 전이 분류(코드 Ω 초기값 전부>2RT=거친 추정 / 문건 two-phase=2개) — 코드 주석에 명기 ④ broadening 기작(L_V·내재 RT/F)이 코드에 실재(집합 통계역학은 설명-only). **Gate**: 모델·w·전이·기작 4항 정합·불일치 0(있으면 코드 주석/문건 註로 해소).
### G3 (9–11) ★버전 1.0.10 통일
- 코드: v12 → `Anode_Fit_v1.0.10.py`(헤더 버전 1.0.10·문건 동기 명기). 문건: Ch1 v10 → 버전 라벨 1.0.10(title/header)·`docs/Ch1_v1.0.10/`. Ch2 v5 도 1.0.10 동기(또는 Ch2 별도 — 사용자 "코드=문건 동일버전"은 Ch1·코드 핵심). INDEX matched. **Gate**: 코드·문건 버전 라벨 1.0.10 일치·파일명·INDEX 정합·이전 v 보존.
### G4 (12–14) 총체 검수 (adversarial)
- ① 문건 정확(broadening 물리·집합 통계역학 중심상수↔η·사이즈 제외·w_eff 0) ② 코드 정확(면적 보존·use_w_eff 0·v11 거동) ③ ★정합(코드 거동 = 문건 주장) ④ 그래프 정상. refute 우선. **Gate**: CRIT/HIGH 0·정합 확인.
### G5 (15–16) 종합·제시
- 그래프 이미지(경로)·내 의견(정상 작동 여부·개형 평가)·정합 verdict·1.0.10 통일 확인. 커밋·푸시. **Gate**: 아침 검토 패키지 완비.

## 7. Implementation Interfaces
- 플로팅 = matplotlib(Anode_Fit import, equilibrium()/curve()/dqdv). 검증 = 실제 실행(추측 0). 통일 = 파일 복사·라벨(원본 v 보존). 검수 = Agent adversarial. milestone commit+push(Anode_Fit 자동). sub commit/push 금지.

## 8. Test Plan
- 그래프: 종모양(뾰족이 0)·면적=Q 보존·매끄러움·온도 RT/F·히스 분기·실행 0-error.
- 정합: 코드 모델=문건 모델(단일입자+L_V·w 현상학·다입자 X)·전이 분류 주석.
- 버전: 1.0.10 라벨 코드·문건 일치.
- 총체: 문건 broadening/집합통계역학/사이즈제외/w_eff 0·코드 정확·그래프 정상.

## 9. Assumptions
- 코드 v12 가 이미 정상(round-trip 검증)이라 그래프도 정상 기대. 집합 통계역학은 설명-only(코드 모델 변경 불요). 버전 1.0.10=사용자 지정 현행. matplotlib 가용.

## 10. (Decision Gate 없음 — 사용자 "다 진행해놔")

## 11. Correction History
- 2026-07-01 신규. 사용자: 그래프 검증+의견+총체 정합+코드·문건 1.0.10 통일, 밤새 완수. GO 불요(자러감·다 진행).
