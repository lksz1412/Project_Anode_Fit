# v1.0.24 최종 코드 — 공개 실측 dQ/dV 피팅 재현 검증

> 재현: `python3 v24_final_fit_check.py` (main/Anode_Fit_v1.0.24.py 로드). 산출 = `final_fit_check.png`.
> 모델 = 출하 `equilibrium()` 자유폭 MSMR(`{U,w,Q}` 전이). dQ/dV 추출 = BDD 스무딩(`bdd_smoothing.py`). 피팅 = `scipy.curve_fit`.

## 결과 (최종 코드로 재실행)

| 데이터셋 | 화학 | 출처 | 전이 | 창내점 | **R²** |
|---|---|---|---:|---:|---:|
| 흑연 Chen2020 (LG M50) | graphite | PyBaMM 표준 공표 OCP(peer-reviewed 실측 fit) | 4 | 416 | **0.9678** |
| LCO O3 Ramadass2004 | LCO(O3) | 리포 `lco_data/` 실측 OCP | 3 | 580 | **0.9999** |
| LCO O2 Carlier2002 JES Fig4a | LCO(O2) | 리포 `lco_data/` 디지타이즈 실측 | 3 | 700 | **0.9392** |

- **흑연 0.968** = 기존 레지스트리(`fit_registry.md`) Chen2020 값 0.965 와 일치 → **@3/@5/토글 반영이 baseline 피팅을 깨지 않음** 확인.
- **LCO O3 0.9999** = 반쪽셀 OCP 거의 완벽 재현.
- **LCO O2 0.939** = 세 주 peak(≈4.02/4.15/4.41 V) 포착, 가장자리 미세 feature 3-전이 밖(정직).

## 결과 — SINTEF 공개 **실측 raw**(Zenodo 20086298) 흑연·실리콘·흑연+Si 블렌드
> 재현: `python3 v24_sintef_fit.py`. 산출 = `final_fit_sintef.png`. 위 OCP 공식(평활) 이 아닌 **실측 pOCV raw**(C/50·RT, 양전류 delith 세그) 를 BDD 로 dQ/dV 화 후 자유폭 MSMR 피팅.

| 데이터셋 | 화학 | 전이(흑연/Si) | 창내점 | **R²** |
|---|---|---:|---:|---:|
| 흑연 반쪽셀 | graphite | 4 / 0 | — | **0.9521** |
| 실리콘 반쪽셀 | Si | 0 / 3 | — | **0.9899** |
| 흑연+Si 블렌드 | Gr+Si | 4 / 3 | — | **0.9930** (f_Si=0.74) |

- **블렌드 = 흑연 host 4전이 + Si host 3전이 가산** → 성분 분해(그림: 흑연 파선 + Si 점선) 가 물리적으로 깨끗이 분리.
- **핵심**: 블렌드 0.42 V 급준 peak 는 **c-Li₁₅Si₄ 결정화(첫 사이클 two-phase, sharp)** feature — 별도 급준 Si 전이(w=0.006)로 잡아야 R²가 0.847→**0.993** 로 상승. 이는 **문건 Ch3v22 Si 물리(Frumkin+two-phase 혼재)를 실측이 지지**함을 뜻한다.
- **흑연 0.952** = 위 Chen2020 OCP-fit(0.968)·레지스트리(0.95–0.97) 와 정합. 남는 잔차 = 2→1 near-delta(모델 유한폭 한계, 데이터 아님).
- **실리콘 0.990** = 비정질 broad 고용체를 3전이로 충실 재현(레지스트리 순수 Si 0.997–0.998 대역).

## 광의 근거 (기존 20셀 레지스트리 — `fit_registry.md`)
이미 SINTEF Zenodo 20086298(CC-BY-4.0 실측 pOCV)·PyBaMM OCP 로 20셀 피팅 완료:
흑연 0.95–0.97 · **순수 Si 0.997–0.998** · SiGr 0.83–0.98 · NMC(층상 대리) 0.994–0.995.
(원 raw 자료는 스크래치 휘발 — 결과·파라미터 분포는 레지스트리에 보존. 본 재현은 그중 재취득 가능분을 최종 코드로 재실행.)

## 정직한 한계 (남은 것 = Task #38)
- 본 검증은 **단일온도 평형 OCP** dQ/dV 피팅이다(정적 곡선 형상 = 잘 맞음, R² 0.94–0.9999).
- **아직 안 된 것**: @5 stage-2L **온도 분리(0.30 mV/℃)**·@3 **유한율속 꼬리**의 검증은 **다온도·다율속(T/I-swept) 반쪽셀 데이터**가 필요하다 — 위 공개 OCP 셋엔 없다(전부 단일 T 평형). 회사 GITT/율속/온도 매트릭스 데이터로 닫는다.
- 흑연 2→1 near-delta(≈0.09 V) 정점은 약간 underfit — MSMR 유한폭이 델타를 못 내는 구조 한계(문건 IMPROVEMENT_DIRECTIONS §4 명시, 데이터 아님).
