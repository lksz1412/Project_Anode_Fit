# CODE_IMPL_REPORT — Anode_Fit v1.0.20 코드 실구현 (스트림 2)

- 원칙: **doc-leads** — 문건(v1.0.20 Ch1/Ch2)이 권위, 코드가 문건을 따른다.
- 베이스: `Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py` (1151줄 전문 정독 완료)
- 산출물 A: `Claude/docs/v1.0.20/Anode_Fit_v1.0.20.py`
- 산출물 B: 본 보고서 (단계마다 append)
- 작성 시각: 2026-07-16 (진행 중 갱신)

---

## 0. 입력 정독 확인 (전문 정독 의무)

| # | 파일 | 상태 | 핵심 확인 |
|---|---|---|---|
| 1 | `docs/v1.0.19/Anode_Fit_v1.0.19.py` (1151줄) | 전문 정독 완료 | x̄ 진입점 3종(`solve_U_oc`·`entropy_coefficient_x`·`reversible_heat_x`)·vib Einstein(`_vib_theta/_S_vib/_vib_dU/_vib_dS`)·n(T) 선형 잔여(`_n_factor`/`_dwdT`)가 **이미 v1.0.19 에 구현되어 있음** |
| 2 | `docs/v1.0.20/_sections/ch1_appB_codemap.tex` (157줄) | 전문 정독 완료 | 기호↔식별자 대응표·`n_T1/n_T_ref` 폭 다중도 선형 잔여(부재=상수 n bit-exact, 발효 시 폭·config 동반 전파)·x̄ 진입점 노드행 |
| 3 | `docs/v1.0.20/_sections/ch2_appB_codemap.tex` (69줄) | 전문 정독 완료 | B.1 진입점 명명·B.2 회귀 기준값 표·B.3 θ_E 하위호환(bit-exact)·B.4 입력 규약(s=+1·평형 중심·두-상 자유 폭) |
| 4 | `docs/v1.0.20/_sections/ch2_sec08_synthesis.tex` (144줄) | 전문 정독 완료 | eq:complete 완전식·계산 예제 (a)~(e) 수치·tab:qrev 5점 |
| 5 | `docs/v1.0.20/_sections/ch2_sec05_mixing.tex` (240줄) | 전문 정독 완료 | eq:implicit·eq:implicit_diff·eq:gj·eq:dxidT·eq:dwdT-nT·파생 A srcbox(175점·T1=292.15/T2=298.15·경계 3곳 연속) |
| 6 | `docs/v1.0.20/_sections/ch2_sec04_einstein.tex` (115줄) | 전문 정독 완료 | eq:Svib-einstein·eq:dSvib·eq:dUvib·C-62 수치(−3.74/0/+3.70/+9.14 µV/K @ θ_E=700K) |
| 7 | `docs/v1.0.19/FITTING_GUIDE.md` (135줄) | 전문 정독 완료 | §1.5 폭 4단 사다리·§1.6 θ_E 규약·§6 흑연 회귀 0-diff 게이트 |
| 보조 | `docs/v1.0.19/test_regression_v1019.py`·`results/research/CH2v4/42_numerical_verification.md`·`ch1_sec10_sum.tex(tab:staging)`·`results/RESULT_P0_setup.md` | 정독 완료 | 골든 하네스 재사용법(`ANODEFIT_CODE` env)·파생 A 원 검증 그리드(x̄∈[0.05,0.95]·FD T1=292.15/T2=298.15·해석식 295.15 K 평가·경계 midpoint 0.455/0.645/0.815)·staging 초기값 문건 대조·환경 잡음 P0=4.33e-15 |

## 1. 문건 요구 ↔ v1.0.19 베이스 대조 (구현 갭 진단)

| 요구 (문건) | v1.0.19 베이스 상태 | v1.0.20 조치 |
|---|---|---|
| B.1 `solve_U_oc(x̄,T)` = eq:implicit 유일근 솔버 | 구현됨 (이분법·단조 좌변·자동 괄호) | 승계 (무변경) |
| B.1 `entropy_coefficient_x(x̄,T)` = 근에서의 eq:complete | 구현됨 (`return_terms` 분리 포함) | 승계 (무변경) |
| B.1 `reversible_heat_x(x̄,T,I)` = eq:qrev 출구 | 구현됨 (−I·T·∂U/∂T, T 한 번) | 승계 (무변경) |
| B.1 기존 `entropy_coefficient(V_n,T)` 유지 (하위호환) | 유지됨 | 승계 (무변경) |
| B.3 θ_E Einstein 보정 — 선택적, 미지정 시 두 가산 항등 0 = bit-exact | 구현됨 (`theta_E`/`theta_E_Tref`; eq:Svib-einstein·eq:dSvib·eq:dUvib 식형 일치 확인) | 승계 + G3 수치 증빙 |
| ch1_appB n_j(T)=n_j+n_T1(T−T_ref) — 부재 시 상수 n bit-exact, 발효 시 ∂w/∂T=(R/F)(n(T)+T·dn/dT) 동반 전파 | 구현됨 (`_n_factor`·`_dwdT` — eq:dwdT-nT 식형 일치 확인) | 승계 + 수치 증빙 |
| B.4 평형 ξ_j = s=+1·평형 중심(분기 shift 無) | 준수 (`solve_U_oc`/`equilibrium`/`entropy_coefficient` 모두 `func_ksi_eq` 기본 s=+1·`func_U_branch` 미적용) | 승계 (무변경) |
| B.4 두-상 폭 자유 입력 (강제 nRT/F 금지) | 준수 (`w`|`n` 자유 키; 'w'-단독은 T-동결·config 자동 소거 `_dwdT=0`) | 승계 (무변경) |
| staging 파라미터 = v1.0.19 기존 값 그대로 | `GRAPHITE_STAGING_LIT` = 문건 tab:staging 과 전 항목 일치 확인 (U 0.210/0.140/0.120/0.085 · ΔH −11700/−13500/−13100/−13000 · ΔS +29/0/−5/−16 · Q 0.10/0.12/0.25/0.50 · Ω 6000/8000/10000/13000 · ΔH_a 48000/46000/44000/40000 · dVdq 0.30 · n=1 · w 폴백 0.020/0.016/0.014/0.012 · ΔS_a=0) | 승계 (무변경) |

**진단 결론**: 문건 v1.0.20 부록 B 요구명세는 v1.0.19 구현이 전건 충족 → v1.0.20 = **버전 문자열·헤더 주석만 갱신한 정합 이월**(물리·수치 경로 0 변경). 이 결정이 G1(하위호환 ≤1e-12)을 구조적으로 보장하며, 게이트는 전건 수치 실행으로 증빙한다.

## 2. 구현 항목표 (진행 중 갱신)

| 항목 | 상태 |
|---|---|
| A. `Anode_Fit_v1.0.20.py` 생성 (헤더 v1.0.20·계보 추가·근거 문건 포인터 v1.0.20) | 진행 |
| 게이트 스크립트 `test_gates_v1020.py` (G1/G2/G3 전건 수치 실행) | 대기 |
| G1 실행·증빙 | 대기 |
| G2 실행·증빙 (B.2 전건 + 파생 A 175점 + 경계 3곳) | 대기 |
| G3 실행·증빙 (θ_E bit-exact) | 대기 |

(이하 단계별 append)
