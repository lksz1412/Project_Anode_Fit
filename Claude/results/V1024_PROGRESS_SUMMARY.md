# v1.0.24 완성도 검증 캠페인 — 진행 요약 (2026-07-19)

> 문건·코드(v1.0.23) **무수정** 원칙 하에 실측 검증만 수행. 전 산출물 `Claude/results/comp_v24/`.
> 상세: `PHASE_V*_RESULT.md`(단계별) · `DATA_REGISTRY.md`(피팅 원장) · `IMPROVEMENT_DIRECTIONS.md`(개선).

## A. 검증한 것 (문건이 실측을 설명하는가)
| 단계 | 대상 | 결과 |
|---|---|---|
| V2 | 흑연 평형 브로드닝(②③) | 실측 두-상 near-delta FWHM 3.5–4mV=0.14–0.16·RT/F(§7 정합). 출하 `equilibrium()` 피팅 R²=0.95(2셀). **M-factor 제거 근거(평형) 실증** — dV/dQ 높이=폭 문제, stretch 불요. |
| V2b | 흑연+Si 블렌드 합성식(§3.5) | blend=흑연host+Si host 가산 R²=0.94–0.98. 흑연 피크 위치 불변. **고Si f_Si=0.776≈metadata 0.755**. |
| V2c | 다중화학(10셀)+양극 | 순수 Si **R²=0.998**. 흑연 U_j 전조성 불변. **NMC 양극 R²=0.99**(⚠LCO 구조대리). 문건식=**MSMR 정확 동형**(w_j=ω_j·RT/F). |
| V3 | 유한율속①(Zenodo 20323533) | 전류↑→피크 broaden·lower(191→3, ~10mA washout)+분극 shift 20mV/mA(V_n=V−|I|Rn). ① 정성 확인. |
| V5 | 모델 vs 데이터(통계) | 공개셋 R²-단조율 상관 r=0.21(약)→이 깨끗한 데이터선 잔차=**모델**(두-상 near-delta) 지배. |

## B. 만든 도구 (재사용 인프라)
1. **BDD 스무딩 포팅** `bdd_smoothing.py` — 사용자 BDD/99_Backend 방법론: 다척도 중앙차분 median slope
   + **웨이블릿 denoise(핵심, soft-threshold 피크보존)** + 왕복공간 savgol 앙상블 + 적응 단/광폭.
   노이즈(±5mV V wobble)서 단일 savgol 대비 **1.8× 정확**(`wavelet_denoise_check.png`).
2. **마스터 피팅 레지스트리** `v24_master_fit.py`→`fit_registry.{md,csv,json}` — 출처 DOI/URL 포함 전건 기록,
   데이터 추가 시 자동 갱신.
3. **파라미터 분포** `param_distributions.png`·`param_dist_stats.md` — 조건별 피팅변수 분포.
4. **개선방향 실측검증** — 전이 4→6(+0.2%)·비대칭폭(+1%): 잔차=near-delta(MSMR 한계, #4 정칙용액이 실해법).

## C. 핵심 발견
- **문건식 = MSMR**(Verbrugge/Baker) — w_j=ω_j·RT/F. 코드가 LCO절에 명시한 매핑을 문헌·실측이 흑연 확인.
- **U_j(전위중심) 셀·조성 무관 매우 일관**(2→1=0.102±0.002V·4→3=0.225±0.0015V) — 스테이징 위치 화학불변.
- **w_j 이봉 분리**: 두-상(≈2mV≪RT/F)·solid-solution/shoulder(≈13–18mV) = MSMR ω_j 스펙트럼 실측.
- **M-factor**: 평형은 폭으로 설명(제거 근거)·유한율속은 ①+분극으로 설명 → 문건이 두 영역 다 설명.
- **각짐**(사용자 지적)=그림 격자 아티팩트(모델 해석적 매끈, `gr_angular_diag.png`).
- **웨이블릿 denoise**(사용자 지적): 포팅 충실했으나 유효경로 누락→BDD 위치로 수정·기본 ON.

## D. 데이터 지형 (조사 5창 종합)
- **확보·피팅**: 흑연·Si·SiGr×3·NMC(Zenodo 20086298)·율속(20323533). = 현재 레지스트리 12셀+율속.
- **신규 확보 대기**(3창 결과, 피팅 예정): **LCO=PyBaMM Marquis2019**(Doyle/Garcia Dualfoil 반쪽셀 실측
  분석곡선) · 흑연 OCP 다종(Ecker·Enertech·Chen·PyBEP×2·'alawa) · Si(SiNC 4입도·Si-graphene·MJ1 GITT).
- **여전히 공백**: LCO 고유 실측 raw(계산/디지타이즈 대리만)·회사 표준 매트릭스(사내).

## E. 정직한 한계
- 두-상 near-delta 피크는 해상도의존·MSMR finite-w 로 delta 재현 불가(구조한계) → R²~0.95 천장.
- 저Si f_Si 과대(축퇴)·B/SiGr c2 저품질(R²=0.83)·NMC≠LCO.
- 공개데이터=상온·(대부분)C/50 → 다온도·회사 조건은 사내 스크립트.

## F. 다음 (사용자 지시 대기/기본)
1. 신규 확보 데이터셋(LCO·흑연 OCP 다종·Si 다종) 레지스트리 추가·피팅 → N 확대·분포 보강.
2. 모델 vs 데이터: 노이즈 큰 데이터셋(코인셀類) 확보 시 웨이블릿 효과·데이터문제 비중 재판정.
3. (사용자 결정) 개선 #2 비대칭폭·#4 정칙용액 문건 반영 / v1.0.24 기본값 개선.
