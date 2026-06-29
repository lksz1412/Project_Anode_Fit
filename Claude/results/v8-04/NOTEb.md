# NOTEb — v8-04b.tex (v8-04 증분 정정판)

> v8-04.tex 의 결함 정정 증분판. 원본(v8-04.tex·v8-04.pdf·NOTE.md) 불가침 — 별도 파일로 산출.
> 작업 sub 역할: 방향성 4건 보완 + 부호 8항 재확인 + 회귀 self-test 실완료. REVIEW1.md 미열람(지시).

## 1. 정정 4건 (방향성 그대로 반영)

### Fix 1 — N8 D-PEAK 물리 정정 (L905 부근, eq:peakshape 직후)
- **원본 결함**: "L_V 작으면 ρ=e^{-Δgrid/L_V}→0 이라 ξ_lag→ *한 칸 뒤처진* ξ_eq 가 되고 (ξ_eq−ξ_lag)/L_V 가 종으로 환원" — 물리적으로 틀림.
- **정정 근거(코드 `_causal_lowpass` L100-118)**: 점화식 `lag[i]=ρ·lag[i-1]+(1-ρ)·src[i]`.
  - ρ→0(작은 L_V): `lag[i]→src[i]` = **같은 칸** ξ_eq (한 칸 뒤처짐이 아님) ⇒ (ξ_eq−ξ_lag)/L_V → 0 (퇴화, peak 소멸).
  - ρ→1(L_V≫Δgrid): ξ_lag 가 ξ_eq 의 매끄러운 저역통과 ⇒ 작은 차/L_V 가 이산 미분 →dξ_eq/dV 종에 접근.
  - 곧 **종 환원은 반대 극한**(큰 L_V)이고, 작은 L_V 에서 평형식 eq:eqpeak 로의 환원은 *저역통과 극한이 아니라* 코드의 **명시 분기 스위치 eq:branch**(`lag_len_V < min_lag_grid_steps*grid_step`)가 담당. 분기의 동기가 바로 이 퇴화 회피.
- **검증**(self-test D-PEAK): 작은 L_V→ρ=2.1e-9, |lag−src|=1.5e-11(→0, 같은 칸 확인); 큰 L_V→ρ=0.967, (s−lag)/L_V vs bell corr=0.84(→종 접근). 정정문 정확.
- 본문 텍스트는 "접근/닮음"으로 적절히 hedge(corr 0.84 와 정합 — 과장 없음).

### Fix 2 — fig:overshoot (3건)
- **(a) 하드코딩 식번호 오류**: 내부 라벨 "Eq.(1.18)=(1.16)" 틀림. 실제 번호 = eq:Veq, eq:gpp.
  - 검산(라벨 순차 카운트): eq:gpp=1.10, eq:Veq=원본 1.13(eq:isotherm 추가 후 1.14). 원본의 "1.18=1.16"=eq:Ubranch=eq:dUhys 로 무관한 식 가리킴 → 명백한 오류.
  - **정정**: `Eq.~\eqref{eq:Veq}\,$\Rightarrow$\,Eq.~\eqref{eq:gpp}` 로 교체 → 번호 drift 영구 차단(eq:isotherm 추가로 번호가 1.13→1.14 로 밀렸어도 자동 정합 — 이 강건성이 \eqref 채택의 정당성).
- **(b) 분기 라벨 상하 뒤바뀜**: 원본 "rising(delith)"@(0.30,−0.55)·"falling(lith)"@(0.70,+0.55) → lobe 와 어긋남.
  - 물리: delithiation(xi:0→) = 저-xi 측 상승 가지, 극대 xs-=0.2113(상부 lobe); lithiation(xi:1→) = 고-xi 측 하강, 극소 xs+=0.7887(하부 lobe).
  - **정정**: rising(delith)@(0.34,+0.70)[상부]·falling(lith)@(0.66,−0.70)[하부]. 수치 검증으로 lobe 정합 확인.
- **(c) fig:hysloop 과 base 곡선 byte-동일(중복)**: 두 그림 모두 Ω=4RT, 17점 coordinate 완전 동일(diff IDENTICAL 확인).
  - **정정**: fig:overshoot base 곡선을 **Ω=3RT** 로 차별화(extrema ±0.415, xs=0.2113/0.7887). 이점 셋 — (i) byte 중복 해소, (ii) fig:doublewell(Ω=3RT, 같은 spinodal) 과 정합해 "신규 3그림" 일관, (iii) fig:hysloop(Ω=4RT, 더 깊은 과주행)은 gap 도해 역할 유지. 캡션에 Ω 차이·spinodal 일치 명시.

### Fix 3 — eq:Veq 다리 inline (D-VEQ)
- **원본**: "정지점 조건에 상호작용 합류 → 평형 등온선 [implicit] → V_eq 풀면 [box]" 점프.
- **정정**: 중간식 eq:isotherm 추가 — (i) g_j(ξ) 1차 미분 g'_j(ξ)=RT ln[ξ/(1−ξ)]+Ω(1−2ξ) 명시, (ii) 평형에서 g'_j=sF(V_eq−U_j) 묶음(eq:isotherm), (iii) 양변 sF 나눔·이항 → eq:Veq=U_j+(1/sF)g'_j. 한 단계도 안 건너뜀.
- 부작용: 식 번호 eq:Veq 이후 +1 밀림 — 문서 전체 `\eqref` 자동 정합(하드코딩 잔존 0, grep 확인).

### Fix 4 — orphan bib 인용
- bazant2013·dreyer2010 가 thebibliography 에만 있고 본문 \cite 0 → orphan.
- **정정**: dreyer2010 = §sec:hys 도입(삽입전극 히스 열역학 기원); bazant2013 = §sec:hys g(ξ) 도입(비평형 열역학 기반 반응속도론 — 평형·속도 통합 틀). 둘 다 주제 적합. grep 으로 본문 인용 확인.

## 2. 부호 사슬 8항 재확인 (브리프 §7, v11 코드 대조 — 전건 PASS)
1. U_j(T)=(−ΔH+TΔS)/F, ΔG=−sFU: 발열 ΔH<0→중심 상승. ✓
2. ξ_eq=logistic[σ_d(V−U)/w]: 방전 V↑→ξ↑. ✓
3. dξ/dV=σ_d ξ(1−ξ)/w, peak=|·|≥0 방향불변. ✓
4. ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d, U_dis>U_chg. ✓
5. χ_d 충전 1−χ, ΔH_a^eff=ΔH_a−χ_dΩ. ✓
6. ∂lnL_q/∂V: A 컷상수 → 운영 미분 0, 부등식<0 은 동기. ✓
7. 꼬리 충전 격자역전 ξ[::-1]…[::-1], 충전 dQ/dV 방전 거울(양수). ✓
8. 분극 V_n=V_app−σ_d|I|R_n, 방전 측정>내부. ✓
정정으로 부호 사슬 영향 없음(D-PEAK 는 환원 메커니즘 귀속 정정, 부호 불변).

## 3. 회귀 self-test — 10R 실완료 (대기 아님, 실제 코드 실행)
실행: `python selftest_v8_04b.py` against `Anode_Fit_v11_final.py` (numpy 2.4.3, T=298.15K).
- **R1** 히스 분기 방향: u=0.7661(문서 0.766 ✓), ΔU_hys=86.69 mV(문서 86.7 ✓), V_dis−V_chg=+86.69 mV>0 ✓.
- **R2** 히스 문턱: Ω=2RT=4957.6 → ΔU_hys=0.0000 mV exact ✓; Ω=2RT+1 → 0.0002 mV(연속) ✓.
- **R3** |I|→0 환원·방향불변: L_q∝|I|(ratio=1.000e6 정확) ✓; peak σ_d 불변(peak_d=peak_c=9.7309) ✓; mirror 잔차 1.78e-15 ✓; 모든 peak≥0 ✓.
- **R4** L_q 동결: A 가 V 무관 상수 → L_q 동일 → 운영 d/dV=0 PASS ✓.
- **D-PEAK 보강**: 작은 L_V ρ=2.1e-9 lag≈같은칸(|lag−src|=1.5e-11); 큰 L_V ρ=0.967 corr 0.84 → Fix 1 정정문 수치 검증.

### 10-round 가변-청크 검수 추이 (청크 스킴·렌즈 로테이션)
| R | 청크/렌즈 | 결함 | 처리 |
|---|----------|------|------|
| 1 | 통독·물리 적대검산(D-PEAK) | ρ 극한 귀속 오류 확인 | Fix1 |
| 2 | 식블록·번호 정합(fig:overshoot) | 하드코딩 1.18=1.16 오류 | Fix2a, \eqref |
| 3 | 그림·시각(라벨 lobe) | 분기 라벨 상하 swap | Fix2b |
| 4 | 그림 데이터 byte 대조 | overshoot=hysloop 곡선 중복 | Fix2c, Ω=3RT |
| 5 | 유도 사슬 G-derive(eq:Veq) | 다리 점프 | Fix3, eq:isotherm |
| 6 | bib·인용 완결성 | orphan 2건 | Fix4 |
| 7 | 번호 drift 전수(grep (1.NN)) | 본문 하드코딩 0(헤더만) | clean |
| 8 | 수치 falsifiable(self-test 실행) | R1-R4 전건 PASS | PASS |
| 9 | 직전수정 새결함(eq:isotherm orphan?·라벨 충돌) | 참조됨·undefined 0 | clean |
| 10 | 빌드 불변·G-usable(3-pass) | undefined ref/cite 0 | PASS |
수렴: R9·R10 연속 0 신규결함.

## 4. 빌드 (xelatex 3-pass, MiKTeX)
- pass1 exit0(20p) → pass2 exit0(22p) → pass3 exit0(22p, "rerun" 해소).
- **Undefined reference/citation = 0**. 잔여 warning 3건 = `Font shape ... undefined`(한글 italic fallback) — **원본 v8-04 final.log 와 동일 baseline**(신규 아님).
- 산출: `v8-04b.pdf`(22p, 395 KB). `\eqref{eq:Veq}`·`\eqref{eq:gpp}` 도해 내 라이브 번호 정합.

## 5. 산출물·보존
- 신규: `v8-04b.tex`(86438B, +2854 증분), `v8-04b.pdf`(22p), `NOTEb.md`(본 파일).
- 불가침 유지: `v8-04.tex`(83584B)·`v8-04.pdf`·`NOTE.md` 무변경. REVIEW1.md 미열람.
- 빌드 로그: `buildb_pass1/2/3.log`.
