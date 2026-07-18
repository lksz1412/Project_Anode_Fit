# AUD-4 독립 적대적 코드 검수 — v1.0.22 R6 `BlendedAnodeDQDV`

- 대상: `Anode_Fit_v1.0.22.py` (`BlendedAnodeDQDV`·`from_wt`·Si 케이스셋)·`test_gates_v1022.py` R6 게이트
- 대조 명세: `_sections/ch3v22_sec03_blend.tex`(eq:blend-dqdv·eq:blend-balance·환산 각주)·`ch3v22_sec02_cases.tex`(tab:si-cases·fig 캡션)
- 방법: 소스 정독 + scratchpad 독립 실행(읽기·python 만; 소스 무수정). 게이트 exit 0 은 기지 → **게이트가 못 잡는 결함**에 집중.
- 판정 요약: **치명 0 · 실질 correctness 결함 0 · 게이트공백(비치명) 3 · 경미 라벨 1**. 명세 5개 항목 전부 코드와 **일치**.

## 판정표

| 항목 | 판정 | 근거(실행 결과) |
|---|---|---|
| 1. eq:blend-dqdv 구현 일치 | **일치** | `equilibrium = gr_host(C_bg+Σ_gr Qξ(1−ξ)/w) + si_host(0+Σ_si …)` = `C_bg+Σ_host Σ_j`. `max|equilibrium −(C_bg+gr_contrib+si_contrib)| = 0.00e+00`. |
| 1. 공통-μ 실체(눈속임 여부) | **일치(실체)** | `solve_U_oc` 이 pooled 이중합을 **한 U_oc**로 풂: xbar 0.1~0.9 에서 `Σ_host Σ_j Q_j ξ(U_oc)=Q·x̄`, resid ≤1.4e-13. pooled 근 0.15969 ≠ gr단독 0.10896 ≠ si단독 0.36157 → 분리풀이 아닌 **진짜 결합근**. 두 host 항상 동일 V 배열 평가. |
| 2. `from_wt` 환산 정확성 | **일치** | `f_Si=m·q_Si/[m·q_Si+(1−m)q_gr]` 코드 line 1232-1233 그대로. elemental(q=1000): m=0.1/0.2/0.3 → f_Si=0.229991/0.401929/0.535332 = 문서 0.230/0.402/0.535. Q=0.97/1.26/1.62/2.09 재현(0.970/1.260/1.622/2.088). |
| 3. C_bg 이중가산 없음 | **일치** | 원거리 V=[5,10]서 `equilibrium=[0.05,0.05]`(=C_bg 1회, 2×아님). `si_host.Cbg=0.0`, `gr_host.Cbg=0.05`. |
| 3. C_bg 설계 "유일구성" 주장 | **일치(주장 생존)** | 깨기 시도: si_host 도 C_bg 담게 하면 `max|d|=5.0e-02`로 bit-exact 붕괴. split a=0.5/0.0 은 array_equal=False(누산순서차 1e-15). **오직 (gr=C_bg, si=0)** 만 graphite-alone 과 누산순서까지 동일 → 엄격 array_equal 유일. 추가로 `host_contributions` 정확성(gr 서 full C_bg 차감)도 동일 구성 요구. 주장 성립. (단서 아래 N1) |
| 4. R6-G1 bit-exact 견고성 | **일치** | f_Si=0 서 72개 파라미터조합(x·Rn·use_dH_eff·C_bg·si_case) × {equilibrium·dqdv(±s,I)·curve·solve_U_oc} **worst diff = 0.00e+00**. si=0 항이 순수 0 배열이라 `x+0.0=x` 부동소수점 항등 → 우연 아님. |
| 4. R6-G3 용량보존 견고성 | **일치** | C_bg∈{0,0.05,0.3} × f_Si∈{0…0.99} 전부 `∫(dQ/dV−C_bg)dV = Q` rel ≤2.2e-9 (≪1e-6). ∫ξ(1−ξ)/w=1 구조상 성립. C_bg 이중가산 시 rel≫1e-6 → G3 가 실제로 판별. |
| 4. R6-G2 연속성 견고성 | **일치** | n=60→960 세분화 max-step 비 = 0.502/0.501/0.500/0.500 (Lipschitz 0.5 수렴). 촘촘히 해도 유지. |
| 4. 게이트 무의미 assert 여부 | **일치(무의미 없음)** | G1 `array_equal`+effectiveness(f_Si=0.3 이 곡선 1.479 변경)·G2 곡선동일시 nan→FAIL·G3 실적분 대조·coverage NotImplementedError 실호출 — 전부 실질 검사. |
| 5. 엣지 fail-fast | **일치** | f_Si=1.0/1.5/−0.1/nan/inf·si_case 오타·from_wt m≥1/음수·q_Si<0·q_gr=0·(f_Si>0 & ΣQ_si=0) 전부 ValueError. f_Si=0 은 정상 빌드(bit-exact 경로). 조용한 오답 없음. |
| 5. Si 케이스 파라미터 vs 문서 | **일치** | elemental U0.30/0.45·w0.060/0.050, sic U0.30/0.42·w0.050, siox U0.30(placeholder)/w0.090 = fig 캡션 일치. q_Si=1000/1710/3117 = tab:si-cases. 코드에 없는 수치 창작 없음. |
| 5. SiOₓ 공백 정직성 | **일치** | `SI_CASE_GAPS['siox']` 2건 등재, f_Si>0·siox 만 "확인 필요" 경고 발효(elemental/sic·f_Si=0 무경고). |
| 5. GS-1/GS-2 차단 | **일치** | `plastic_hysteresis_loop()`·`nonadditive_correction()` 둘 다 `NotImplementedError`. |

## 게이트공백·단서 (비치명, correctness 영향 없음 — 전부 독립 확인 완료)

**N1 — C_bg 유일성 주장의 근거 정밀화(주장 자체는 참).**
페이블이 든 두 근거 중 "**C_bg 전극 1회 가산**" 은 사실 **split 불변**이다: a·C_bg(gr)+(1−a)·C_bg(si) 어떤 a 든 원거리 총배경 = C_bg 1회로 동일([0.05,0.05] 확인). 구성을 실제로 고정하는 것은 (i) **엄격 array_equal bit-exact**(graphite-alone 과 누산순서 일치 → si=0 강제) 와 (ii) **`host_contributions` 정확성**(gr 서 full C_bg 차감 전제)이다. 즉 결론(유일 구성)은 참이나 "1회 가산" 하나로는 유일성이 안 나온다. 코드는 올바른 구성 채택 — **결함 아님**, 근거 서술의 정밀도 문제.

**N2 — R6-G1/G3 이 si_case='sic' 단일 케이스만 게이트.**
bit-exact·용량보존을 'sic' 로만 검증. 독립 실행으로 elemental·siox 도 f_Si=0 bit-exact(worst 0.0)·보존 성립 확인 → **숨은 결함 없음**. 게이트 커버리지가 좁을 뿐.

**N3 — 중심식 eq:blend-balance 의 f_Si>0 잔차가 게이트에 없음.**
R6-G1 은 solve_U_oc 를 f_Si=0 bit-exact 로만 본다. f_Si>0 결합근이 실제로 이중합=Q·x̄ 를 푸는지는 게이트 밖. 독립 확인 resid ≤1.4e-13 → **성립**. 중심식 검증이 base solve_U_oc(타 게이트) + pooling 에 위임됨.

**N4 — 경미: R6-G2 라벨.** 게이트가 `si_case='sic'`(q=3117)로 스윕해 f_Si 최대 0.782 를 찍으면서 출력엔 "(doc: wt%→f_Si≈0–0.7)"(=elemental 기준) 표기. 값·판정엔 무영향, 라벨만 느슨.

**N5 — 참고(문서와 무모순): `from_wt` 기본 si_case='sic'.**
fig:blend-family 재현엔 반드시 `si_case='elemental'` 필요(문서 캡션이 명시). 기본값으로 `from_wt(0.1)` 호출 시 q_Si=3117 적용돼 f_Si=0.482(≠0.230). 캡션이 elemental 을 명시하므로 **문서-코드 불일치 아님**, 순진한 이식 시 footgun.

## 결론
명세 대조 5항목(eq:blend-dqdv·eq:blend-balance·from_wt·C_bg 설계·Si 케이스셋) 전부 코드와 **일치**하며, 공통-μ 는 **실체(결합근)**로 눈속임 아님. 게이트 4종은 실질 검사(무의미 assert 없음)이고 견고. 페이블의 C_bg "유일 구성" 주장은 **깨기 시도에도 생존**. **치명 결함 0.** 남은 것은 게이트 커버리지 공백 3건(비치명, 독립 확인으로 배후 결함 부재)·경미 라벨 1건뿐.
