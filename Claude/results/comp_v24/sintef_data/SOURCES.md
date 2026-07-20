# SINTEF 공개 실측 데이터 — 영구 보존 (재다운로드 불필요)

> 사용자 지적("받았던 데이터들을 저장을 안하니 매번 찾느라 리소스 낭비"): 스크래치는 세션 종료 시 휘발되므로
> 피팅이 실제 소비하는 **delith 세그먼트 (V, Q)** 를 리포에 CSV 로 영구 보존한다. 원 parquet(8MB) → 추출 CSV(760KB).

## 출처
- **데이터셋**: SINTEF (EU IntelLiGent 프로젝트), Zenodo record **20086298**, 라이선스 **CC-BY-4.0**.
- **원 parquet URL**: `https://zenodo.org/records/20086298/files/<key>?download=1`
  - `gr` = 흑연 반쪽셀 · `si` = 실리콘 반쪽셀 · `sigr` = 흑연+Si 블렌드 반쪽셀
- **측정 조건**: 반쪽셀 pOCV, C/50, 상온(RT≈25℃). 단일 온도·단일 율속(평형 근사).

## 추출 규약 (parquet → CSV)
- parquet 컬럼: `Current / A`, `Voltage / V`, `Cumulative Capacity / Ah`.
- **delith(탈리튬화) 세그먼트** = 양전류(`I > 1e-9`) 연속 최장 구간만 취함(충·방 혼재 배제).
- `Q_mAh = (Cumulative Capacity / Ah)×1000`, 세그 시작점을 0 으로 이동.
- 산출 컬럼: `V_vs_Li` [V], `Q_mAh` [mAh].

## 파일
| 파일 | 셀 | 점수 | V 범위 [V] | Q 범위 [mAh] |
|---|---|---:|---|---|
| `gr.csv`   | 흑연 반쪽셀 | 16827 | 0.086–1.000 | 0.00–2.12 |
| `si.csv`   | 실리콘 반쪽셀 | 10831 | 0.048–1.000 | 0.00–1.90 |
| `sigr.csv` | 흑연+Si 블렌드 | 16735 | 0.046–1.000 | 0.00–3.82 |

재현: `v24_sintef_fit.py` 가 이 CSV 를 우선 로드(스크래치 parquet 없어도 재실행 가능).
