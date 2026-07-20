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

## 광의 근거 (기존 20셀 레지스트리 — `fit_registry.md`)
이미 SINTEF Zenodo 20086298(CC-BY-4.0 실측 pOCV)·PyBaMM OCP 로 20셀 피팅 완료:
흑연 0.95–0.97 · **순수 Si 0.997–0.998** · SiGr 0.83–0.98 · NMC(층상 대리) 0.994–0.995.
(원 raw 자료는 스크래치 휘발 — 결과·파라미터 분포는 레지스트리에 보존. 본 재현은 그중 재취득 가능분을 최종 코드로 재실행.)

## 정직한 한계 (남은 것 = Task #38)
- 본 검증은 **단일온도 평형 OCP** dQ/dV 피팅이다(정적 곡선 형상 = 잘 맞음, R² 0.94–0.9999).
- **아직 안 된 것**: @5 stage-2L **온도 분리(0.30 mV/℃)**·@3 **유한율속 꼬리**의 검증은 **다온도·다율속(T/I-swept) 반쪽셀 데이터**가 필요하다 — 위 공개 OCP 셋엔 없다(전부 단일 T 평형). 회사 GITT/율속/온도 매트릭스 데이터로 닫는다.
- 흑연 2→1 near-delta(≈0.09 V) 정점은 약간 underfit — MSMR 유한폭이 델타를 못 내는 구조 한계(문건 IMPROVEMENT_DIRECTIONS §4 명시, 데이터 아님).
