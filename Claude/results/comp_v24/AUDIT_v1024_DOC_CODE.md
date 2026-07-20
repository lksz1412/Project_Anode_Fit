# v1.0.24 전수 doc↔code 정합 감사 (6 병렬 에이전트 + 마스터 재검증)

> 사용자 요청: 문건 전체 ↔ `Anode_Fit_v1.0.24.py` 전 함수·상수·**주석** 전수 정합 감사(원 반영작업 시 됐어야 할 검수).
> 방식: 6 소분 병렬 감사(A 흑연·B LCO·C Si/blend·D 코어수학/부록·E 데이터상수·F 코멘트 sanity) → 마스터가 핵심 findings **직접 재검증**(수치 실행) → 정정.
> 방침(사용자): "코드↔문건 맞기만 하면 됨, 코드가 정상이니 문건을 고쳐라." 단 실제 코드버그는 코드 수정.

## 총평
- **곡선·피팅 정확성 BUG = 0건** (전 감사). 실제 계산 경로(equilibrium/dqdv/curve/블렌드/게이트)는 문건과 정합.
- 발견은 **① 잠재 코드버그 1건(regsol 용량, 수정)** + **② 주석·문서화 불일치 다수(정정)** + **③ 사용자 판단 1건**.
- 정정 후 **게이트 전건 GREEN**(G1 bit-exact 0.0·reflect 4/4·self-consistent 5/5·R6 3/3)·**빌드 GREEN**(ch1 89p·ch2 28p·ch3 20p, 0 err·0 undefined ref).

## ① 실제 코드버그 (수정 완료)
- **C-1 `_regsol_dqdv` 용량 비보존**: `wi=Q*(xg[1]-xg[0])` + 1200점 격자 → ∫area=**1.000634·Q**(+0.063%, G3 tol 1e-6 의 634배). Ω·δ 무관 계통오차. 로지스틱 경로는 1.000000 정확 → regsol 한정.
  - **마스터 재검증**: area/Q = 1.000634 (Ω=0/3000/10000 전부) 재현 확인.
  - **수정**: `wi = Q / xg.size` → Σwi=Q 정확. **재검증 area/Q=1.000000**. 로지스틱 경로 bit-exact 불변(G1 0.0e+00). G-R3 면적 1.000634→1.000.
  - 영향: shipped demo(Si 케이스)는 kernel:regsol 미지정=로지스틱이라 무영향. 내 SINTEF 피팅(regsol 사용)의 +0.063%가 제거됨(R² 영향 <0.001).

## ② 주석·문서화 정정 (코드 주석 / 문건 문구)
| ID | 위치 | 문제 | 정정 |
|---|---|---|---|
| D-1/F-3 | py func_L_q:주석 | dH_a^phys 부호 반전(`−RT·ln3600`) — **수치실증 +가 정답**(비율 1.0 vs 7.7e-8) | `+R·T·ln(3600)(≈+20.3kJ/mol)` |
| F-2 | py regsol 헤더 | regsol 분기가 equilibrium() 한 곳뿐(dqdv/entropy/solver 는 로지스틱)인데 미고지 | 스코프 한정 주석 추가 |
| F-4 | py 헤더 line4 | "부록 E만 additive·물리수치 무변경" 부정확(@3/@5/토글/R6 추가·LCO 가역열 기본 변경) | 실제 추가범위+예외 명기 |
| A-1/A-2/E-1/E-2 | py XRD_v1024 헤더 | "두-상 4개" 상성격 과대배정(§7 "2개"·§5b "5-feature 는 상성격 미배정" 위반) + regsol2 배열 출처 오배치 | §7 위임 명시·seed Ω≠물리두상·배열은 tab:staging 4전이 소속 |
| F-1/B-2 | py:1099 토글 | "토글 ON(기본)" 오도(기본 OFF) + getattr fallback True(stale) | "기본 OFF"·fallback False |
| F-7 | py func_dH_a_eff:주석 | "+Ω 흡수" ↔ 식 −χ_d·Ω | "−χ_d·Ω 흡수" |
| F-6 | py z_cut:주석 | "5% 컷" 광고 ↔ A_cap=4.0 clamp 로 실현 z=4.0(≈7%) | clamp 주 추가 |
| A-3 | py:41 | stale 파일명 graphite_ica_ch1_v1.0.21.tex | 현행 마스터 ch1_graphite_v1.0.24.tex 명기 |
| F-5 | py:10 | 소제목 "1.0.21" ↔ release 1.0.24 | "[이력 1.0.21]" 라벨 |
| E-4/F-8 | py:1159 | "Ω=6000<2RT?" 자문자답 오독 | "seed Ω=6000>2RT, Ω/RT=2.42" |
| **B-1** | **doc lcoomega** | **toggle box True "∝T²/eq:U1T2" ↔ 코드 T_ref-동결=선형**(문건 자체 eq:lcoomega-Tref 와도 어긋남) | **True=상수오프셋(선형); ∝T² 는 미구현 타깃** |
| A-4 | doc gr2L:128 | `GRAPHITE_STAGING_XRD`(무접미) | `_v1024` |
| E-3 | doc sec10:133 | U(298) 절삭 210.87/85.29 | 반올림 210.88/85.30 |

## ③ 사용자 판단 필요 (미정정)
- **A-1b XRD_v1024 U-값 재배치**: 코드 `GRAPHITE_STAGING_XRD_v1024` 5값(U=0.210/0.170/0.132/0.116/0.085)이 문건 §5b(d)(iii) 서술("표 4행 {0.210,0.140,0.120,0.085} 라벨 그대로 보존 + 고전위 dilute 1개 추가 = 4+1, 재배치 없음")과 불일치 — 코드는 dilute 를 0.210 슬롯에 넣고 4↔3 을 0.170 으로, 3↔2L/2L↔2 도 −8/−4 mV 이동한 **재유도 사다리**. 커브 무영향(opt-in). **어느 쪽이 의도인가**: (안A) 문건 §5b(d)(iii)를 "재유도 5-feature"로 정정 / (안B) 코드 상수를 "표 4행 보존+dilute"로 재구성. 헤더 상성격 클러스터(②)는 §7 위임으로 이미 정정, U-값 구조만 결정 대기.

## 무조치 (미확인/후보, 정합위반 아님)
- C-2 헤더 ablation 수치(+0.66%p·+1.25%p) — 외부 스크립트 미확인. C-3 eq:sifr-width(3전이 tier-B) vs SI_ELEMENTAL(2전이 tier-C) provenance(문건 tier 구분 명시). E-5 regsol2 배열 외부산출. D-3 `appendix_phase_separation.tex` = 고아 초안(어느 마스터도 미\input). B-3 LCO per-peak Ω "+1.25%p" shipped 미활성(LCO_MSMR_LIT 에 Omega/kernel 부재, 게이트 없음) — 결함 아님, 상태.

## 정합 확인(이상 없음) — 방대
전 함수 수식(func_U_j/ksi_eq/w/L_q 본체·dH_a_eff/chi_d/A·regsol 유도·인과기억·ratio·전달함수 H)·GRAPHITE_STAGING_LIT 32값+U(298) 역산·LCO_MSMR_LIT(전자항 folding 후 3.930 정확)·tab:staging/lco/si 전수·데이터 공백(SI_CASE_GAPS=각주 c/f, 날조 없음)·블렌드 f_Si=0 bit-exact(max|diff|=0.0)·**warnbox(v) Maxwell binodal ↔ _regsol_dqdv 완전정합(직전 세션 sifr 수정 검증됨)**·게이트 전건(self-consistent 5/5·전달함수 잔차 3.96e-6=문건값).
