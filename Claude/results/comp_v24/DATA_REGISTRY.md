# v1.0.24 실측 피팅 데이터 레지스트리 (출처·데이터·피팅·분포)

> 사용자 요청: 공개 실측을 최대한 많은 케이스로 피팅하고, **출처·데이터·피팅결과를 전부 기록**하며,
> **조건별 피팅변수 분포**를 정리한다. BDD 프로젝트의 dQ/dV 스무딩 방법론을 반영한다.
> 본 문건 = 그 마스터 기록. 데이터 추가 시 `v24_master_fit.py` 재실행 → 표·분포 자동 갱신.

## 1. dQ/dV 추출 = BDD 스무딩 방법론 반영 (`bdd_smoothing.py`)
사용자 지적("savgol 단독은 왜곡")대로, `BatteryData_Display/Lib_LKS_BatteryData_99_Backend.py`의
스무딩 방법론을 포팅해 표준 추출기로 채택:
- **다척도 중앙차분 median slope**(dMSMCD): 여러 window 폭의 slope 를 nanmedian → 단일창 편향·노이즈 강건.
- **왕복공간 savgol 앙상블**: `median[ savgol(x), 1/savgol(1/x) ]` (여러 window) → **단일 savgol 의 피크
  눌림·dV/dQ↔dQ/dV 왕복 편향 완화**(핵심 anti-왜곡).
- **적응 단/광폭 블렌드**: 피크 위치(|1/dVdQ| 큰 곳)=광폭 부드럽게·평지=단폭 보존.
- **웨이블릿 denoise**(WLD, 순환이동 앙상블·다 wavelet) 옵션.
- 피팅용 안정판 `dqdv_grid_bdd(V,Q)`: 균일 V격자에서 위 두 핵심을 적용(두-상 plateau 시간특이 회피).
- 비교 `bdd_vs_savgol.png`: BDD 는 두-상 피크를 더 충실히 보존(savgol 은 ~200 으로 눌림; 실제는 near-delta).

## 2. 데이터 출처 (전 데이터셋 provenance)
자동 표 = `fit_registry.md`(전 셀 출처·피팅 전건) · `fit_registry.csv`(기계판독). 현재 스냅샷 = 12셀,
공개데이터 확보에 따라 증설 중. 확보/조사 출처 전체는 `PUBLIC_DATA_SURVEY.md` 참조.

| 출처 | DOI/URL | 화학 | 조건 |
|---|---|---|---|
| SINTEF (EU IntelLiGent) | Zenodo 20086298 | 흑연·Si·SiGr×3·NMC111/532 | pOCV C/50·25℃ |
| DLR BAK N21700 | Zenodo 20323533 | 흑연-SiOx 음극 | delith 율속 5수준(V3) |
| (조사·확보 예정) | 20323533·5171874·15520717·mp-24850·Reimers&Dahn 등 | 추가 흑연/Si/LCO | 율속·온도·양극 |

## 3. 피팅 결과 (전건 → `fit_registry.md`)
모델 = 출하 `equilibrium()` 직접('w'만=자유폭 MSMR). 흑연=host, Si=host 가산, 양극=LCOCathode.
현재 12셀 R² 요약: 흑연 0.95–0.96 · 순수Si **0.997–0.998** · SiGr 0.83–0.98 · NMC(양극) **0.994–0.995**.

## 4. 조건별 파라미터 분포 (`param_distributions.png` · `param_dist_stats.md`)
전 anode 셀(10) 흑연 스테이징 피크 파라미터 분포:

| 피크 | N | U 평균(V) | U std | w 평균(mV) | w 범위(mV) | 성격 |
|---|--:|--:|--:|--:|---|---|
| 2→1 (0.10) | 8 | 0.1021 | 0.0023 | 2.62 | 1.5–4.4 | 두-상 sharp(≪RT/F) |
| 3→2L (0.14) | 15 | 0.1407 | 0.0037 | 12.9 | 1.5–39 | sharp+shoulder 혼합 |
| 4→3 (0.22) | 8 | 0.2251 | 0.0015 | 1.91 | 1.8–2.1 | 두-상 sharp |

**핵심 관찰**:
- **U_j(전위 중심)는 셀·조성 무관 매우 일관**(std 1.5–3.7 mV) — 스테이징 위치가 화학 불변임을 정량 확인.
- **w_j 는 두-상(≈2 mV≪RT/F)·shoulder(≈13–18 mV) 로 이봉 분리** — MSMR ω_j 스펙트럼(질서↔무질서) 실측.
- **f_Si 피팅 vs metadata**: 고Si·B 계열 y=x 근접(0.72–0.89), 저Si 과대(0.50 vs 0.30, baseline 축퇴).
- Si host U 는 0.28–0.47 V(비정질 Si), w 넓음(10–230 mV, solid-solution).

## 5. 확장 프로토콜 (데이터 추가 시)
1. 원자료를 스크래치(공개 URL)에서 받아 `zenodo_gr/` 또는 지정 폴더에.
2. `v24_master_fit.py` 의 `DATASETS` 레지스트리에 행 추가(label·file·chem·role·theo·cond·NG·NS·win·**source**).
3. 재실행 → `fit_registry.{md,csv,json}`·`param_distributions.png`·`param_dist_stats.md` 자동 갱신.
4. 새 조건(율속·온도)이면 `cond` 에 명기 → 분포가 조건축으로 확장.

## 5b. ★모델 문제 vs 데이터 문제 판정 (사용자 핵심 질문 — `quality_vs_r2.png`)
20셀 R² vs 데이터 품질(밀도 pts/mV·V단조율) 통계 결과 — **두 요인 모두 실재, 데이터 품질이 결정적일 때 있음**:
| 데이터 유형 | 예 | 밀도 | R² | 잔차 원인 |
|---|---|---:|---:|---|
| **sparse 실측 GCD** | SiFLG_S300 | 0.2/mV | **0.55** | ★**데이터**(sparse·noisy) — 순수 Si(clean)는 0.998인데 급락 |
| sparse 실측 GCD | SiFLG_S450 | 0.6/mV | 0.89 | 데이터(sparse) |
| clean 고밀도 실측 | SINTEF Si | 15–17/mV | **0.998** | (거의 완벽) |
| clean 고밀도 실측 | SINTEF 흑연 | 63/mV | 0.95 | **모델**(두-상 near-delta, MSMR 한계) |
| digitize OCP(평활) | Ecker/Chen/PyBEP | 0.1–4/mV | 0.96–0.99 | (평활곡선이라 양호) |
- **판정**: **데이터가 나쁘면(sparse Si-graphene) R²가 0.55로 붕괴 = 데이터 문제**(사용자 직관 실증). **데이터가
  깨끗하면(SINTEF·OCP) R²=0.95–0.998이고 남는 잔차는 모델**(두-상 near-delta). 즉 사용자 말대로 실무 데이터에선
  데이터 품질이 흔한 원인이고, 문건식 자체는 깨끗한 데이터를 잘 설명한다(둘 다 참).
- 도구: 밀도·단조율이 레지스트리에 자동 기록 → 네 노이즈 데이터 넣으면 즉시 데이터문제 비중 판정.

## 6. 한계·정직
- 두-상 near-delta 피크 높이는 해상도 의존(모델 finite-w 로 delta 재현 불가 — MSMR 구조 한계, IMPROVEMENT_DIRECTIONS §4).
- 저Si f_Si 축퇴·B/SiGr c2 저품질(R²=0.83, 국소최소/데이터) = 개별 플래그.
- NMC = LCO 구조 대리(층상 R-3m)일 뿐, LCO 고유 feature 아님.
