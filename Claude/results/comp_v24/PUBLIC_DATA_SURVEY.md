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

## 검증 스코프 함의 (정직)
- **공개데이터로 가능**: 흑연·블렌드의 **상온 평형/앙상블 브로드닝(②③)·피크 높이(M-제거 핵심)** 검증.
- **공개데이터로 불가 → 회사 데이터(사내)**: (a) LCO 전체, (b) 율 시리즈 ①(0.05/0.1/0.2C), (c) T-의존(15/23/35/45°C). Zenodo는 C/50·상온뿐.
- → 제작한 검증 스크립트를 사내에서 회사 데이터에 그대로 적용하는 경로.

## Sources
- https://zenodo.org/records/20086298 (D-1 확보)
- batteryarchive.org(전부 풀셀)·calce.umd.edu·Materials Project(계산)·Mendeley c35zbmn7j8(풀셀)
