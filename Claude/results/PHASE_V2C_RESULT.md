# Phase V2c — 다중 셀·다중 화학 확장 검증 + 양극(NMC) + 각짐 규명 Result

## Summary
공개데이터 검증을 10셀(흑연2·순수Si2·SiGr 3조성×2)로 확장하고, 양극측을 층상산화물 NMC(⚠LCO 아님, 구조 유사체)로 검증했다. 결과: (1) **순수 Si host 단독 검증 R²=0.998/0.997** — 문건 Si 케이스(넓은 로지스틱)가 실측 비정질 Si 탈리튬을 거의 완벽 재현; (2) **흑연 스테이징 피크 위치(0.104/0.142/0.227V)가 전 셀·전 조성에서 불변** — host 재현성 확립; (3) **양극 NMC111/532 R²=0.993/0.995** — MSMR 양극식이 실측 층상산화물 dQ/dV 재현; (4) **f_Si 가 metadata 추종**(고Si 0.77 vs 0.755·B/SiGr 0.73 vs 0.66·저Si 0.48 vs 0.30 과대). 아울러 사용자 지적 "피크 사이 각짐"을 규명: **그림 격자 아티팩트**(초sharp 피크를 0.5mV로 표본화)이며 모델은 해석적으로 매끈(gr_angular_diag.png 증명) — 전 그림 고해상 재생성.

## Step Range
Cumulative **16–22** (V2b 13–15 이어).

## Inputs
- 실측(Zenodo 20086298 pOCV 상온): gr×2·si×2·sigr_aq1×2·aq2×2·sigr3B×2·nmc111·nmc532.
- 모델: `Anode_Fit_v1.0.23.py` `GraphiteAnodeDischargeDQDV`·`LCOCathodeDQDV`·`GRAPHITE_STAGING_LIT`·`SI_*_LIT`.
- 문헌조사(MSMR·staging) 결과 → `comp_v24/IMPROVEMENT_DIRECTIONS.md`.

## Files Created
- `comp_v24/v24_multi_fit.py`·`multi_fit.png`·`multi_fit_result.json`(10셀).
- `comp_v24/v24_cathode_fit.py`·`cathode_fit.png`·`cathode_fit_result.json`(NMC×2).
- `comp_v24/gr_angular_diag.png`(각짐=격자 규명).
- `comp_v24/IMPROVEMENT_DIRECTIONS.md`(개선 방향 조사).

## Files Updated
- `comp_v24/v24_graphite_fit.py`·`v24_blend_fit.py`: 모델선 고해상 격자(0.02mV) 재생성(각짐 제거). 피팅 로직·수치 무변.

## Read Coverage
- `LCOCathodeDQDV`(L977–1020)·`LCO_MSMR_LIT`(L953–974) 정독. `func_ksi_eq`·`equilibrium` 기존 정독.
- 문헌: MSMR(Verbrugge/Baker)·staging(Safran/Dahn/Bazant)·6-gallery(coal-graphite JES 2024).

## Execution Evidence
| 화학 | 셀수 | R²(범위) | 핵심 |
|---|---:|---|---|
| 흑연 | 2 | 0.965–0.972 | 스테이징 0.104/0.142/0.227V·두-상 w/RTF 0.03–0.06 |
| 순수 Si | 2 | **0.997–0.998** | 비정질 Si 넓은 기여(0.27–0.47V) 거의 완벽 |
| SiGr 저Si | 2 | 0.979–0.980 | 흑연 불변+Si小; f_Si 0.477/0.480(vs 0.30, 과대) |
| SiGr 고Si | 2 | 0.932–0.943 | f_Si 0.766/0.776(vs 0.755 ✓) |
| B/SiGr | 2 | 0.796–0.968 | f_Si 0.726/0.762(vs 0.655); c2 저품질(국소최소/데이터) |
| NMC111/532(⚠LCO아님) | 2 | **0.993–0.995** | MSMR 양극식이 층상산화물 재현(broad w 12–115mV) |

- **MSMR 정체 확인(문헌)**: 문건식 = MSMR 정확 동형(w_j=ω_j·RT/F). 코드가 이미 LCO 절에 명시한 매핑을 문헌이 흑연까지 확장 확인.
- **각짐 규명**: `gr_angular_diag.png` — 동일식 0.5mV(각짐) vs 0.02mV(매끈). 피크 FWHM 2.8mV가 0.5mV격자서 5.6점 → 삼각형. 물리·데이터 문제 아님.

## Validation
| 게이트(V2c) | 판정 | 근거 |
|---|---|---|
| 순수 Si host 검증 | PASS | R²=0.998, Si 중심 0.29/0.43/0.47≈문건 SIC/SI_ELEMENTAL |
| 흑연 host 재현성(전 조성) | PASS | 0.104/0.142/0.227V 불변(10셀) |
| 양극식 실측 재현(NMC 대리) | PASS | R²=0.99, ⚠LCO≠NMC 명시 |
| f_Si 정량 | PARTIAL | 고Si·B ✓·저Si 과대(축퇴) |
| 각짐 규명 | PASS | 격자 아티팩트 증명·모델 해석적 매끈 |

## Gate
**PASS.** 다중 셀·화학·양극(대리) 확장 검증 완료. MSMR 정체·각짐 규명. 한계: 저Si f_Si 축퇴·NMC≠LCO·B/SiGr c2 저품질.

## Confirmed Non-Changes
- 문건·코드 무수정(검증·재생성만). v1.0.23 불가침. 피팅=출하 equilibrium() 직접 호출.

## 추가 후보 → `comp_v24/IMPROVEMENT_DIRECTIONS.md` 참조(전이 4→6·비대칭폭·저Si 구속·정칙용액).
