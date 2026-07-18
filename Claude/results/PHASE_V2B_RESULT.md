# Phase V2b — 흑연+Si 블렌드 평형 브로드닝·합성식(§3.5) 검증 Result

## Summary
Si-흑연 블렌드 반쪽셀 near-equilibrium 실측(Zenodo 20086298 pOCV, 상온, 2조성: SiGr-AQ-1 저Si·SiGr-AQ-2 고Si)에 대해 문건 블렌드 **합성식**(§3.5: blend dQ/dV = 흑연 host + Si host, 공통 V축 가산)을 출하 코드 `BlendedAnodeDQDV.equilibrium` 구성(=`GraphiteAnode(gr).eq + GraphiteAnode(si).eq`)으로 검증했다. 결과: **합성식 확증** — (1)흑연 스테이징 sharp 피크가 순수흑연과 **동일 위치**(0.10/0.14/0.225 V)로 블렌드에서 불변, (2)Si 는 0.29–0.46 V 넓은 기여로 가산되며 Si 함량 증가 시 커짐, (3)고Si 조성에서 피팅 용량분율 **f_Si=0.776 ≈ metadata 유도 0.75**(정량 부합). R²=0.979(저Si)/0.943(고Si). 한계: 저Si 조성은 Si 기여가 약·넓어 f_Si 과대추정(0.477 vs 0.30) = baseline 흡수 축퇴.

## Step Range
Cumulative **13–15** (V2 8–12 이어).

## Inputs
- 실측: `zenodo_gr/sigr_aq1_pocv.parquet`(SiGr-AQ-1, theo 510 mAh/g, ~4 wt%Si→f_Si≈0.30)·`sigr_aq2_pocv.parquet`(SiGr-AQ-2, theo 1150, ~24 wt%Si→f_Si≈0.75). Zenodo 20086298, 상온 pOCV.
- 모델: `Anode_Fit_v1.0.23.py` `BlendedAnodeDQDV`(L1207–1328: `__init__`·`from_wt`·`equilibrium`)·`GRAPHITE_STAGING_LIT`·`SIC_LIT`.
- V2 흑연 피팅 초기값(`gr_fit_result.json`).

## Files Created
- `results/comp_v24/v24_blend_fit.py`·`blend_fit.png`(2조성 real vs FIT + 흑연/Si 성분 분해)·`blend_fit_result.json`.

## Files Updated
- (없음 — 검증 phase. 코드·문건 무수정.)

## Read Coverage
- `BlendedAnodeDQDV.__init__`(용량 배분 Q_Si=f_Si·Q/(1−f_Si)·Q_gr 무재스케일)·`from_wt`(C-052 wt%→f_Si)·`equilibrium`(gr.eq+si.eq) 정독.
- metadata SiGr 행(wt%·theo capacity)·2 pOCV parquet 로드.

## Execution Evidence
**블렌드 = 흑연 host + Si host 분해(출하 equilibrium() 합성)**:
| 조성 | R² | U_gr(V) 피크 | Si U(V) | f_Si(fit) | f_Si(expected) |
|---|---:|---|---|---:|---:|
| SiGr-AQ-1(저Si) | 0.979 | 0.224/0.140/0.100(+shoulder) | 0.43·0.44(broad) | 0.477 | 0.30 |
| SiGr-AQ-2(고Si) | 0.943 | 0.226/0.141/0.103(+shoulder) | 0.289·0.459 | **0.776** | **0.75** |

- **흑연 host 불변**: 두 블렌드 모두 스테이징 피크 U=0.10/0.14/0.225 V — 순수흑연 V2(0.104/0.1415/0.227)와 동일. → §3.5 "흑연 Q 무재스케일·host 불변" 코드 계약이 실측과 정합.
- **Si 가산·함량의존**: 저Si=0.43 V 소형 bump / 고Si=0.29–0.46 V 대형 기여(비정질 Si 탈리튬 영역). Si 함량↑ → Si 성분 면적↑ (그림).
- **정량 f_Si(고Si)**: 피팅 0.776 ≈ wt%→f_Si 유도 0.75(오차 3%) — C-052 wt%↔용량분율 환산·합성식 정량 검증.
- **폭 기제 동일**: 블렌드 내 흑연 피크도 w/(RT/F)=0.04–0.09(두-상 sharp) — V2 흑연과 동일 브로드닝 기제.

## Validation
| 게이트(V2b) | 판정 | 근거 |
|---|---|---|
| 합성식 가산성(blend=gr+si) | PASS | R²=0.94–0.98, 성분 분해 물리적(흑연 sharp+Si broad) |
| 흑연 host 위치 불변 | PASS | 블렌드 스테이징 U=순수흑연과 동일(0.10/0.14/0.225) |
| Si 함량의존·영역 | PASS | Si 0.29–0.46 V(비정질 Si)·함량↑→기여↑ |
| f_Si 정량(고Si) | PASS | fit 0.776 ≈ metadata 0.75 |
| f_Si 정량(저Si) | **CONDITIONAL** | fit 0.477 vs 0.30 — 약·넓은 Si 기여 baseline 흡수 축퇴 |

## Gate
**PASS.** 블렌드 합성식(§3.5)·wt%↔f_Si 환산(C-052) 실측 확증(고Si 정량). 한계: 저Si f_Si 축퇴·공개데이터=상온/C-50(율①·T 미검증).

## Confirmed Non-Changes
- 코드·문건 무수정. v1.0.23 불가침. 피팅=출하 `equilibrium()` 합성 직접 호출.
- 원자료 원본 미변조.

## 추가 후보 (실행 X — 사용자 결정 대상)
1. **저Si f_Si 축퇴**: 약한 Si 기여가 baseline 과 축퇴 → f_Si 과대. Si host U 를 알려진 비정질 Si 탈리튬 중심(≈0.30/0.45 V)으로 약구속하거나, Si 와 별개의 전극 baseline(Cbg(V)) 항 분리 → 저Si 분해 안정화. (사용자 결정)
2. **`SIC_LIT` 기본 중심**(U=0.30/0.42) 은 실측 고Si Si 중심(0.29/0.46)과 근사 부합 — 기본값 현실성 양호(흑연 대비). 미세 갱신 후보이나 필수 아님.
3. **율①·다온도**: 흑연과 동일 — 공개데이터 부재, 사내 스크립트 패키지.
