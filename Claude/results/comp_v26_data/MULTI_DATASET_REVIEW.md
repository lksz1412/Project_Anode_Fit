# 다각 데이터·물리 검토 종합 (v1.0.26 regsol 재검증 준비)

> 작성: 2026-07-27 야간 자율 세션. 목적 = 사용자 지시 "데이터가 잘못된 거 아니냐? 다른 데이터들에 대해서
> 다각적으로 검토해와" + "제대로 데이터 다시 찾아와". 근거 = comp_v24/lit_raw/01·03 + PUBLIC_DATA_SURVEY.

## 1. "개판 피팅"의 진짜 원인 (진단 — 확정)

| 원인 | 근거 |
|---|---|
| **① 데이터 프로토콜이 최악** | 현 `gr.csv` = record 20086298의 4프로토콜 중 **plain pseudo-OCV(C/50)** — 가장 비평형. addendum A2가 이미 실증: 같은 모델로 p-OCV R²=0.977 vs **p-OCV+hold 0.9945**(피크역 RMSE 4.708→2.701). 잔차 상당분 = 모델 결함 아니라 **데이터 비평형 잔여**. |
| **② 방식은 맞았음** | 마스터 ablation은 이미 흑연=regsol(Ω>2RT)·Si=logistic(broad) 소재-정확 구조 + BD 평활(`bdd.dqdv_grid_bdd`) 사용. 즉 dQ/dV 방식·모델 구조는 옳았고, **비평형 데이터가 병목**. |

→ **해결 = 평형 데이터(GITT / p-OCV+hold)로 교체.** BD 평활은 미분만 매끄럽게 하지 안 맞는 걸 맞추지 않음(사용자 지적 정확).

## 2. 소재별 물리 (다각 문헌 합의 — 소재마다 다른 커널)

| 소재 | 물리 | 커널 | 핵심 근거 |
|---|---|---|---|
| **흑연** | **두-상(binodal), 단 marginal** | regsol Ω≈2–2.5RT | Dahn1991(4→3 빼고 전부 first-order)·**Cordoba2024 Ω_a=64.3meV≈2.5RT(유일 실수치 앵커, 2RT 바로 위)**·Persson2010(쌍 해밀토니안 충분) |
| **실리콘(순환 a-Si)** | **연속 고용체(단일상 슬로프)** | broad logistic(큰 ω) | Chevrier-Dahn2009·Artrith2018(a-Si featureless)·Papadopoulos2026. **유일 두-상 = c-Li₁₅Si₄ 1차(~0.43–0.45V spike)** |
| **흑연+Si 블렌드** | **중첩**(흑연 두-상 피크 + Si 슬로프) | 소재별 합 | Tu2024 "clearly a superposition"·Kirkaldy2022(dV/dQ 분리)·Berhaut2023(휴지 공통μ) |

**주의(모델 무결)**: 흑연 Ω는 **창발 유효 파라미터**(탄성+staging), DFT 쌍결합E(Persson 0.41eV·Pande 반발) 아님. Ω_a≈2.5RT만 유효 앵커. → regsol 흑연 Ω는 **2~2.5RT 근방(marginal 두-상)**이 물리적이며, 극단 near-delta 아님.

## 3. 확보 대상 데이터 (다각)

### Primary — Zenodo 20086298 (SINTEF/Flores, CC-BY, 반쪽셀 vs Li, 상온)
- 전극: Gr-AQ-1 · Si-AQ-1 · **SiGr-AQ-1/2/3(블렌드 3조성)**
- 프로토콜 ×4: p-OCV(C/50) · **p-OCV+hold** · **GITT(C/50+150분 rest=진짜 평형)** · GITT+hold
- 컬럼: Test Time/s · Current/A · Voltage/V · Cumulative Capacity/Ah · Cycle · Step (시간 있음 → BD dVdt/dQdt 정식 적용 가능)
- **계획: GITT + p-OCV+hold 다운로드**(dl_sintef.ps1). p-OCV는 소형, GITT ~340MB.

### 교차검증용 (독립 출처 — 다각)
- **Zenodo 15470746** — 흑연/LNMO 전극수준 GITT+quasi-OCV (독립 셀).
- **Hu&Schwartz MSMR 툴** (DOI 10.1149/1945-7111/ac5a1a) — 오픈 Jupyter + 예제데이터 + bootstrap CI. 피팅 프로토콜 벤치마크.
- **LiionDB**(liiondb.com) · **PyBaMM MSMR** — 흑연 MSMR gallery 파라미터 교차확인.
- Zenodo 20323533(DLR 율속) · 5171874(O'Regan 다온도 dU/dT) · 15520717(MJ1 GITT).

### XRD 상수 앵커 (피크 수 판정)
- Fujimoto2022(C/250) = **9피크**(dilute 8→4 세분) → "4전이"는 coarse-graining. 실율서 병합.
- Dahn1991 = staging 4전이·두-상 판정 정본.

## 4. 정직한 갭 (다각 조사가 밝힌 한계)
- **흑연 dQ/dV용 logistic-초과 폐형 커널 제안 논문 없음** → 비대칭은 창시(skew), 문헌 형식 채용 아님.
- **흑연 정칙용액 Ω의 독립(비-fit) RT단위 측정 없음** → 최선 앵커 = Cordoba 평균장 Ω_a≈2.5RT.
- dilute(1′↔4) 형상 지배자 미해결(Mercer2019 비선형 vs Azizi2025 상수 −0.2eV).

## 5. 실행 파이프라인 (준비 완료 — Anthropic 분류기 복구 시 자동)
- `dl_sintef.ps1` — GITT+hold 다운로드(resume·재실행 안전).
- `analyze_sintef.py` — GITT 평형점 추출 + BD dQ/dV + 소재-정확 피팅(흑연 regsol / Si broad / 블렌드 중첩) + 소재별 플롯 + summary.json.
- 차단 사유 = auto-mode 분류기 일시 장애(네트워크·스케줄 도구 전부 게이트). 복구 즉시 1커맨드 실행.

## 6. 재개 커맨드 (분류기 복구 후)
```
powershell -File "D:\Projects\Project_Anode_Fit\Claude\results\comp_v26_data\dl_sintef.ps1"
python "D:\Projects\Project_Anode_Fit\Claude\results\comp_v26_data\analyze_sintef.py"
```
→ out/{graphite,silicon,blend}_dqdv.png + summary.json → HTML 아티팩트 게시.
