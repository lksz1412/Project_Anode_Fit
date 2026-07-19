# V1 공개 데이터 조사 — 흑연·LCO·흑연+Si 반쪽셀 (v1.0.24)

> 병렬 리서치 2창(흑연·LCO) + 마스터 검증. 정직 원칙: 실재·다운로드 확인된 것만 "발견".

## 요약 판정
| 화학 | 공개 실측 반쪽셀 데이터 | 판정 |
|---|---|---|
| **흑연** | **Zenodo 20086298** (GITT/p-OCV C/50, raw V-Q, CC-BY) | ✅ 확보 |
| **흑연+Si 블렌드** | **Zenodo 20086298** (SiGr 3종 동일 셋) | ✅ 확보 |
| **LCO** | **없음** (실측 반쪽셀 저율/GITT/다온도 = 0건) | ✗ 공백 |

## D-1 (확보) — Zenodo 20086298 (SINTEF/EU IntelLiGent)
- "Half-Cell OCV of Several Li-Ion Active Materials under Various Protocols". DOI 10.5281/zenodo.20086298. CC-BY 4.0·로그인 불필요.
- **반쪽셀 vs Li**: 흑연(Gr) · Si · **Si-흑연 블렌드(SiGr 3종)** · 양극(LNMO/LFP/NMC — **LCO 아님**).
- 프로토콜: **GITT(C/50, 150분 rest)** · **pseudo-OCV(C/50)** · 각 hold 변형. raw V-Q 시계열(parquet).
- 컬럼: Test Time/s · Current/A · Voltage/V · Cycle · Step · Cumulative Capacity/Ah.
- 파일: 95개(15.6GB). **p-OCV는 ~3MB(소형)**, GITT는 ~340MB. metadata.csv(19KB).
- **한계: 상온 단일** (다온도 없음).

## LCO — 공백 (정직)
실측 LCO 반쪽셀 저율/GITT/다온도 공개 데이터 **0건**. 확인:
- 다운로드 가능 LCO = 전부 **풀셀 노화**(CALCE CS2/CX2·NASA·Oxford·Mendeley Diao2019) — 반쪽셀 아님·음극신호 혼재.
- LCO 열역학(엔트로피·∂φ/∂T: Hudak2014·Świderska2019·Reynier) = 논문 그림/유료, 기계판독 데이터셋 아님.
- Materials Project = **계산(DFT) OCV**, 실측 아님(형상 baseline만).

## ★업데이트 (V2c/V3 확장 조사 — 2026-07-19) : 공백이 일부 메워짐
추가 리서치 2창으로 이전 "공백" 판정을 갱신:
| 축 | 이전 판정 | 갱신 |
|---|---|---|
| 율속①(0.05–3C) | 사내 필요 | **공개 확보**: Zenodo **20323533**(DLR BAK 흑연-SiOx 음극 반쪽셀, delith 율속 1:2:5:10:20, CSV) → V3 검증 완료 |
| T-의존(다온도) | 사내 필요 | **부분 공개**: Zenodo **5171874**(O'Regan 2022 WMG, 흑연-SiOx dU/dT 엔트로피·다온도 OCP, 독립그룹) |
| LCO | 공백 | **여전히 실측 반쪽셀 0건**. 대리: (a) 동일 20086298 내 **NMC111/532 반쪽셀**(층상 R-3m 유사체 — V2c 검증, ⚠LCO아님), (b) **Materials Project mp-24850**(LiCoO2 계산 OCV 형상, API키 필요), (c) Reimers&Dahn1992·Ohzuku1994(그림→디지타이즈) |
| 추가 흑연-SiOx | — | Zenodo **15520717**(LG MJ1 음극 GITT, parquet) |

**제외(풀셀 함정)**: Zenodo 7235857(Imperial)·4032561(Chen2020) — "SiGr 음극" 라벨이나 실제 풀셀.

## 검증 스코프 함의 (갱신)
- **공개데이터로 가능(확대)**: 흑연·Si·블렌드 평형②③·피크높이(M-제거 평형절반)·**율속①(20323533)**·양극식(NMC 대리)·부분 T(5171874).
- **여전히 공개 불가 → 회사 데이터**: (a) **LCO 고유** 실측(NMC는 구조 대리일 뿐), (b) 회사 표준 매트릭스 그대로(GITT/0.05/0.1/0.2C × 15/23/35/45°C 동일 전극) = 사내 스크립트 적용.

## Sources
- https://zenodo.org/records/20086298 (D-1 흑연·Si·블렌드·NMC 확보)
- https://zenodo.org/records/20323533 (율속① 확보) · https://zenodo.org/records/5171874 (O'Regan T-의존) · https://zenodo.org/records/15520717 (MJ1 GITT)
- https://legacy.materialsproject.org/materials/mp-24850/ (LCO 계산 OCV) · Reimers&Dahn 1992 DOI 10.1149/1.2221184 (그림)
- 제외: batteryarchive.org·Zenodo 7235857·4032561 (전부 풀셀)
