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

> ⚠ **정정(2026-07-20)**: 아래 로지스틱 표는 **기본 로지스틱 커널(bit-exact baseline)** 결과다. 이는
> `equilibrium()` 의 `if tr.get('kernel')=='regsol'`(코드 line 588) 분기를 **타지 않는다** — 전이를
> `{'U','w','Q'}` 로만 만들었기 때문. 따라서 **@3(Si Frumkin regsol)·@5(흑연 5-feature)를 시험하지 않은
> baseline** 이다. 이전 판에서 "블렌드가 문건 Ch3v22 Frumkin 두-상 물리를 지지"라 적은 **주장은 철회한다**:
> 0.42 V 급준 peak 는 Frumkin Ω>2RT 두-상이 아니라 **임의의 좁은 로지스틱 전이(w=0.006)** 로 잡은 것이라
> @3 물리를 검증한 바 없다. 데이터=리포 `sintef_data/`(영구보존). @3/@5 regsol 재피팅 = 아래 별도 절.

**로지스틱 baseline(대조군, @3/@5 미태움)** — `python3 v24_sintef_fit.py` 의 대조 경로:

| 데이터셋 | 화학 | 전이(흑연/Si) | R²(로지스틱 baseline) |
|---|---|---:|---:|
| 흑연 반쪽셀 | graphite | 4 / 0 | 0.9521 |
| 실리콘 반쪽셀 | Si | 0 / 3 | 0.9899 |
| 흑연+Si 블렌드 | Gr+Si | 4 / 3 | 0.9930 (f_Si=0.74) |

- 이 값들은 **baseline 곡선-형상 재현력**만 말한다(로지스틱 MSMR 이 깨끗한 실측을 잘 맞춤). @3/@5 검증 아님.

## 결과 — @3/@5 반영식(regsol 커널) 실제 태운 재피팅
> `v24_sintef_fit.py`(regsol 경로): Si=`'kernel':'regsol'`+Ω 자유(a-Si 고용체 Ω<2RT + c-Li₁₅Si₄ 두-상 Ω>2RT),
> 흑연=@5 5-feature stage-2L. **Ω/RT 출력으로 두-상(>2)·고용체(<2) 자발 분류를 증거로 남긴다.**
> (재피팅 실행/집계 후 이 절에 R²·Ω/RT 표와 정직 판정 기재 — 로지스틱 대비 개선/악화 나란히.)

## 광의 근거 (기존 20셀 레지스트리 — `fit_registry.md`)
이미 SINTEF Zenodo 20086298(CC-BY-4.0 실측 pOCV)·PyBaMM OCP 로 20셀 피팅 완료:
흑연 0.95–0.97 · **순수 Si 0.997–0.998** · SiGr 0.83–0.98 · NMC(층상 대리) 0.994–0.995.
(원 raw 자료는 스크래치 휘발 — 결과·파라미터 분포는 레지스트리에 보존. 본 재현은 그중 재취득 가능분을 최종 코드로 재실행.)

## 정직한 한계 (남은 것 = Task #38)
- 본 검증은 **단일온도 평형 OCP** dQ/dV 피팅이다(정적 곡선 형상 = 잘 맞음, R² 0.94–0.9999).
- **아직 안 된 것**: @5 stage-2L **온도 분리(0.30 mV/℃)**·@3 **유한율속 꼬리**의 검증은 **다온도·다율속(T/I-swept) 반쪽셀 데이터**가 필요하다 — 위 공개 OCP 셋엔 없다(전부 단일 T 평형). 회사 GITT/율속/온도 매트릭스 데이터로 닫는다.
- 흑연 2→1 near-delta(≈0.09 V) 정점은 약간 underfit — MSMR 유한폭이 델타를 못 내는 구조 한계(문건 IMPROVEMENT_DIRECTIONS §4 명시, 데이터 아님).
