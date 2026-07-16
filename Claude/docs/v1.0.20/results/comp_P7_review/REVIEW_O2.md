# REVIEW_O2 — v1.0.20 독립 검수 (검수자 O2)

> 담당 청크: ch1_sec06_eqpeak · ch1_sec07_broadening · ch1_sec08_lag · ch1_sec09_tail · ch1_sec10_sum · ch1_appA_signcheck · ch1_appB_codemap
> 검수 3축: ① 신본 자체 결함 · ② v1.0.19 대비 regression · ③ 신설 다리(P3 §7 U3 / §10 U4 / P6 appB "가역 발열") 물리·서지 정확성
> 렌즈: G-follow · G-usable · G-derive · 절별 refute 1회 · 가장 약한 1곳 지목
> 신본 폴더: /home/user/Project_Anode_Fit/Claude/docs/v1.0.20/_sections/
> 구본(대조 read-only): /home/user/Project_Anode_Fit/Claude/docs/v1.0.19/_sections/
> 발견 형식: | # | 위치(파일:행) | 심각도(H/M/L) | 축(①/②/③) | 발견 | 근거 | 제안 |

---

(정독 진행 중 — 파일별 발견분 순차 append)

### ch1_sec06_eqpeak.tex (전문 정독 완료, 43행)

**대조**: v1.0.20 = v1.0.19 바이트 동일 → regression 없음(축②).
**재유도 검산(전건 통과)**: (b) 종 항등식 $\dd\xi_\eq/\dd z=e^{-z}/(1+e^{-z})^2=\xi_\eq(1-\xi_\eq)$ ✓; (c) 연쇄율 $\dd z/\dd V=\sigma_d/w_j$ ✓; (d) 순높이 $Q_j/(4w_j)$($\xi=\tfrac12$ 에서 $\tfrac14$) ✓; 면적 $=Q_j$($\int_0^1\dd\xi=1$) ✓; 30-32행 $\gamma_j\ne0$ 잔존극한 단서 정확.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O2-1 | ch1_sec06:5,32 | L | ① | 평형 peak 모양을 5행·32행은 아래첨자 없는 $w$ 로($\xi_\eq(1-\xi_\eq)/w$), 나머지 전부 $w_j$ 로 표기 | rubric B5(새 기호/표기 일관). 물리 무해, 표기 일관성만 | 5·32행 $w\to w_j$(전이 특정성 유지) 또는 "일반 폭 $w$" 명시 |
| O2-2 | ch1_sec06:4,20-35 | L | ① | 절 제목·도입은 "평형 peak"인데 결과식 eq:eqpeak 은 $z=\sigma_d(V-U_j^{\,d})/w_j$ 로 **분기중심 $U_j^{\,d}$** 에 peak 을 놓아(위치$=U_j^{\,d}$, 33행), 진짜 가역 평형중심 $U_j$ 와는 $\gamma_j\to0$ 에서만 일치 | refute 시도: "평형"과 $U_j^{\,d}$ 중심 충돌 → 그러나 30-32행이 "$\gamma_j\ne0$ 이면 히스테리시스 잔존극한, $U_j$ 중심과 $\gamma_j\to0$ 에서만 일치"로 **명시 해소**. 결함 아님, guarded 지위. G-follow상 학부생 혼동 여지만 | 유지 가(P6 판정 관용). 원하면 도입 1문장에 "여기 평형=$|I|\to0$ 잔존극한" 못 박기 |

### ch1_sec07_broadening.tex (전문 정독 완료, 306행)

**대조(축②)**: v1.0.19 대비 변경 **정확히 2곳** — (a) 25행 "staging **문헌**의 상평형" → "staging **상도표**의 상평형" + `\cite{dahn1991,ohzuku1993}` 추가(U3); (b) 70행 `\cite{dreyer2010}` → `\cite{dreyer2010,dreyer2011}`(C-010). 나머지 전 행 동일 — 자산 유실·문장 훼손·수치 변화 없음.
**축③ 신설 다리 검증(정확)**: U3 귀속 정확 — dahn1991 = "Phase diagram of Li$_x$C6"(PRB 44,9170) = 문자 그대로 **staging 상도표**; ohzuku1993 = "Formation of Li-Graphite Intercalation Compounds…"(JES 140,2490) = **실측 staging plateau**. "실측 plateau·staging 상도표의 상평형" 주장에 두 문헌 실제 내용 걸맞음(원장 DRAFT_existing 24-25행 대조). 문헌→상도표 어휘 교체는 dahn1991 실제 내용에 맞춘 **정밀화**(과잉 일반화 아님). dreyer2011 = many-particle 히스테리시스/상전이 동반 논문 → (iii-a) 순차전환 평탄역 주장에 적정 병기.
**재유도 검산(전건 통과)**: logistic 분산 $\pi^2w_j^2/3$ ✓; FWHM $2\ln(3+2\sqrt2)w_j\approx3.53w_j$($n{=}1$,298K→90.6mV≈91) ✓; $\sigma_\mathrm{int}=\pi w_j/\sqrt3=1.81w_j$ ✓; $\sigma_\mathrm{sym}=1.81w_j\sqrt{1+1.25^2}=2.90w_j$ ✓; 유효 scale $\sigma_\mathrm{sym}\sqrt3/\pi=1.60w_j$ ✓; Gibbs-Thomson $\Delta U=2\gamma V_m/(Fr)$ 차원 [V] ✓·수치 0.75mV(1μm)/0.20mV(PSD) ✓; $\Delta U(30\mathrm{nm})\approx25$mV ✓; $\tau(5\mu m)=r^2/D=6{\times}10^2$–$2.5{\times}10^4$s ✓.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O2-3 | ch1_sec07:49-53 | M | ① | 두-상 폭 $w_j$ 의 **이중 역할 미분리**: 49-51행은 폴백 0.014/0.012 V 를 "$n_j{<}1$ 이면 잔여 폭이 $RT/F$ 미만이라 **내재 ② 폭**"으로 읽어 25.7 mV 와 "모순 없음"이라 하고, 121-122행·keybox 는 같은 피팅 $w_j$ 를 "**②⊗③ 총량 흡수**"(분산 가법 → 총폭 $\ge$ 내재)로 규정. 14 mV $<$ 25.7 mV 를 총폭으로 보면 ② 하한과 충돌, 내재로 보면 ③ broadening(본 절 논지)이 이 두 전이서 소멸 | eq:widthbudget $\sigma_\mathrm{sym}^2{=}(\pi^2/3)(n_jRT/F)^2{+}\sigma_\eta^2$ 은 첫항을 내재로 씀. 51-53행 "현재 $n_j{=}1$ 고정→25.7mV, 14/12mV 는 직접지정 폴백"으로 **능동 수치충돌은 무마**되나, 0.014V 가 내재②인지 총②⊗③ 인지 문면상 미봉합. 절이 122행서 "②③ 분리는 $\sigma_\eta$ 독립측정 없이는 비유일"을 인정하므로 물리오류는 아님 | 사전존재(v1.0.19 동일 — regression 아님). 49-53행에 "폴백 $w_j$ 는 ②③ 비분리 유효폭, $n_j$ 는 유효 다중도" 1구 삽입해 내재/총 혼동 차단 |
| O2-4 | ch1_sec07:17 | L | ①/③ | 17행 "이들[Li 흑연 dilute·4L→3L·3L→2L]은 plateau 없는 연속 등온선이라\cite{rsc2021}" — rsc2021 은 **포타슘**(K) 삽입 흑연 상전이 논문(원장: "…potassium intercalated graphite") | 이종(K vs Li)계 anchor. 직후 절이 leviaurbach1999(Li Frumkin)로 폭 근거 별도 제시하므로 rsc2021 은 staging L-stage 연속성 유비 인용. V1 등재키·사전존재(regression 아님). K→Li 구조주장 전용은 경미 과인용 소지(?) | rsc2021 을 "staging 위상진화 일반"으로 한정하거나 Li 전용 연속상 anchor 병기 검토(위험 대비 이득 낮음 — 유지 가) |
| O2-5 | ch1_sec07:207,215 | L | ① | 207행 "전형 마이크론 흑연 $r=1$–$15\,\mu$m", 209행 $\Delta U(1\,\mu\mathrm m)$ 는 $r_{\min}{=}1\mu$m, 그러나 215행 PSD 예시는 $r_{\min}/r_{\max}=3/15\mu$m 로 $r_{\min}{=}3\mu$m | 절대 이동 상한(1μm)과 PSD 산포 예시(3μm) 의 $r_{\min}$ 불일치. 용도가 달라 의도적일 수 있으나 문면상 값 상이. 수치·결론 무영향(둘 다 "$\ll w$") | 사전존재. 209행을 "$r=1\mu$m(최소)에서" 명시하거나 PSD 예시도 1μm 로 통일 |

### ch1_sec08_lag.tex (전문 정독 완료, 129행)

**대조(축②)**: v1.0.20 = v1.0.19 바이트 동일 → regression 없음.
**재유도 검산(전건 통과)**: eq:Lq $L_{q,j}=|I|/(Q_\cell k_j)$ 계수 역수 ✓; $k_j=r_j^+(1+e^{-\mathcal A/RT})$ detailed balance ✓; **$z_\mathrm{cut}=4.357$ 독립 재유도**: logistic 미분종 5% 컷 $4u/(1+u)^2{=}0.05\Rightarrow u^2{-}78u{+}1{=}0\Rightarrow u{=}0.0128\Rightarrow z{=}{-}\ln u{=}4.357$ ✓; $A_\mathrm{cap}{=}4.0$→$4e^{-4}/(1+e^{-4})^2{=}7.1\%$ ✓; 5%분기 $n_j<4.0/4.357{=}0.918$ ✓; eq:dHeff $\Delta H_a^\eff{=}\Delta H_a{-}\chi_d\Omega$ (깊은꼬리 $\xi\to1$서 $-\Omega(1{-}2\xi)\to+\Omega$ 흡수) 부호·계수 ✓; $T_*{=}|I|h/(Q_\cell k_B)$ 차원 [K] ✓; eq:Lqfull=eq:Lqmid2 항등 ✓; $L_q\propto|I|\Rightarrow L_V\to0$($|I|\to0$) ✓.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O2-6 | ch1_sec08:106-109 | L | ① | 전압축 환산 기울기를 **세 표기 혼용** — 106행 "컷점 **OCV** 기울기", 107행 "$\dd V_n/\dd q$", eq:LV(109행) "$\lvert\dd V/\dd q\rvert_{q_a}$" | 프로젝트 검수 P3-①($V_n$/$V_{n,OCV}$/$V$ 구분 일관성). 셋이 컷점서 같은 양인지(OCV 준평형 vs 내부전위 $V_n$ vs 표기 $V$) 문면 미명시. 물리 결과엔 무영향이나 규범 축 | 사전존재(regression 아님). eq:LV 와 106-107행을 한 기호($V_n$ 또는 OCV)로 통일 또는 "컷점서 $V_n{\approx}V_{n,OCV}$" 1구 |
| O2-7 | ch1_sec08:39 | L | ① | 39행 "logistic 미분 종의 5% 폭이 중심에서 $\pm z_\mathrm{cut}\,RT/F$ 규모" — 실제 전압 반폭은 $z_\mathrm{cut}w_j{=}z_\mathrm{cut}n_jRT/F$ 로 $n_j$ 누락(직후 $\mathcal A{=}z_\mathrm{cut}n_jRT$ 는 $n_j$ 정확 포함) | "규모"가 scale 진술로 완화하고 기본 $n_j{=}1$ 서 $RT/F{=}w_j$ 라 무해하나, 엄밀 폭은 $n_j$ 배(?) | 사전존재. "$\pm z_\mathrm{cut}w_j$" 로 적으면 $\mathcal A$ 식과 자동 정합 |
| O2-8 | ch1_sec08:112-117 | L | ① | (weakest 후보) $\partial\ln L_q/\partial V$ 를 "실현값 $=0$(컷 동결 스칼라)"과 "$<0$(물리적 동기)"로 이중 사용 | refute: $L_q$ 가 상수인지 $V$-단조인지 모순처럼 보임 → 그러나 113-116행이 "동결 전 국소 구동력 단조성이 컷 규칙 정당성, 동결 후 실현 미분 0"으로 **명시 분리**. guarded, 결함 아님. G-follow 부담만 | 유지 가. 원하면 "동결 전/후" 라벨 명시 강화 |

### ch1_sec09_tail.tex (전문 정독 완료, 245행)

**대조(축②)**: v1.0.20 = v1.0.19 바이트 동일(diff 무출력) → regression 없음.
**재유도 검산(전건 통과, 특별 지시 "방향 반전 부호" 포함)**: 적분인자 eq:intfactor ✓; 일반해 eq:memory ✓; $q_0\to-\infty$ 소멸(유계 $r_j$·$L_q{>}0$) ✓; 부분적분 eq:lag-byparts·경계항($u{=}V$서 $\xi_\eq(V)$, $u\to-\infty$서 0) ✓; eq:lag 커널 규격화 $\int_0^\infty(1/L_V)e^{-w/L_V}dw{=}1$ ✓; **eq:tail-limit 지배수렴** ($|\dd\xi_\eq/\dd V|\le1/(4w_j)$ 지배함수 $e^{-t}/(4w_j)$ 적분가능 → 극한·적분 교환) ✓; **방향 반전 독립 재유도**: 충전 $q\!\uparrow\!\Leftrightarrow\!V\!\downarrow$ 라 과거가 높은 $V$쪽, $L_q{=}L_V/|\dd V/\dd q|$·$q{-}q'{=}(V'{-}V)/|\dd V/\dd q|$ 환산 → 커널 $e^{-(u-V)/L_V}$·구간 $[V,+\infty)$ (eq:reversal 하단분기) 부호 정확 ✓; 두 방향 $r_j\ge0$(q축서 $\xi_\eq$ 진행 단조증가) → peak 양수 ✓. 그림 평형종 좌표 재계산 일치(V=0.6→0.2288, V=1.2→0.1779, 정점 0.25@0).

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O2-9 | ch1_sec09:156-166 | L | ① | (weakest 후보) 충전 분기 커널·구간 반전을 "과거의 방향이 뒤집힌다"는 **물리적 mirror 논증**으로 닫음(163-165행 "같은 부분적분을 뒤집힌 커널·구간에 반복") — 음의 $\dd V/\dd q$ Jacobian 을 명시적으로 전개하지 않음 | refute 후 독립 재유도로 결과는 **정확** 확인($L_q{=}L_V/|\dd V/\dd q|$ 환산 시 지수부호·구간 일치). 유도 자족성(G-derive)상 명시 change-of-variables 1줄이 있으면 완결. 물리오류 아님 | 사전존재(regression 아님). eq:reversal 앞에 "충전 $\dd V/\dd q{<}0$ 대입" 1줄 추가 검토(선택) |

### ch1_sec10_sum.tex (전문 정독 완료, 63행)

**대조(축②)**: v1.0.19 대비 변경 **1곳(27-29행, U4 완화)** — 구본 "Ohzuku 보고 ≈0.125 V 와 15 mV 시료 의존 편차 안의 배치값(tier C --- **문헌 간 5-15 mV 편차가 통상적**)" → 신본 "Ohzuku 보고 ≈0.125 V`\cite{ohzuku1993}` 에서 15 mV 떨어진 배치값 --- 본 표의 두 anchor 출처`\cite{dahn1991,ohzuku1993}` 사이에서도 ... 시료·측정 조건에 따라 어긋나므로 ... tier C 로 분류". 나머지 동일.
**축③ U4 검증(정확)**: 무근거 일반화 "**문헌 간 5-15 mV 편차가 통상적**"(전 문헌 범용 주장) **제거 확인** → 두 표 anchor 출처(dahn1991·ohzuku1993) 시료의존 편차로 **범위 한정 재서술**. 과잉 일반화 재발 없음. CITATION_BASELINE U4 처리(Step 40)와 정합.
**재유도 검산(전건 통과)**: eq:sum 보존식 $V$-미분 ✓; 표 $U{=}(-\Delta H{+}298.15\Delta S)/F$ 네 전이 ±1mV(4→3=0.2109 자리수경계 명시 정확·2L→2=0.1203·2→1=0.0853) ✓; $L_V$ 규모 $10^{-10}$–$10^{-8}$V 독립 재계산(2→1: $\Delta H_a^\eff{=}33500$→$L_V{\approx}5{\times}10^{-10}$; 4→3: 45000→$5{\times}10^{-8}$) ✓; 가시꼬리 문턱 $\Delta H_a{\approx}80$kJ/mol 재계산 ✓; 45-48행 "$n$ 우선→균일 25.7mV, 폴백은 $n$ 제거 시 대안폭" **명료 서술**(sec07 O2-3 혼동의 정답 프레이밍) ✓.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O2-10 | ch1_sec10:28-29 | L | ③ | U4 재서술이 "두 anchor 출처 사이에서도 같은 전이의 보고 전위가 어긋난다"를 **맥락으로 단언** — 그러나 표는 각 전이를 단일 출처에 anchor(3→2L 은 Ohzuku만), dahn↔ohzuku 동일 전이 head-to-head 수치는 미제시. 실제 15mV 는 배치값(0.140) vs Ohzuku(0.125) offset | 완화 자체는 **개선 확정**(범용 "통상적" 삭제). 잔여: "인스턴스"라기보다 시료의존성 일반서술. 두 문헌 모두 흑연 staging 보고라 명제는 사실적·정직 hedging | 유지 가. 엄밀히 하려면 "배치값을 Ohzuku 보고서 15mV 옮긴 초기값(시료의존 범위 내)"로 단일출처 offset임을 명시 |

### ch1_appA_signcheck.tex (전문 정독 완료, 90행)

**대조(축②)**: v1.0.20 = v1.0.19 바이트 동일(diff 무출력) → regression 없음.
**재유도 검산(전건 통과)**: R1 $u{=}\sqrt{1{-}2RT/\Omega}{=}0.766$·$\Delta U^\hys{=}(2/F)[\Omega u{-}2RT\,\mathrm{artanh}\,u]{=}86.7$mV(artanh 0.766=1.011 재계산) ✓; R2 $\Omega{=}2RT$→$u{=}0$→$\Delta U^\hys{=}0$ 연속 ✓; R4 $\mathcal A$ 컷상수·실현미분 0(S6 일관) ✓; R5 지배수렴 극한(sec09 정합) ✓; R6 $\Delta S_\rxn^\mathrm{cat}{=}F\,\dd U/\dd T{=}96485{\times}0.83{\times}10^{-3}{=}80.1$J/(mol·K)·30K창 $\Delta U{=}24.9$mV≈25 ✓. S1–S8 정성 사슬 기준명제 정합.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O2-11 | ch1_appA:82-83 | L | ① | R6 에서 단전극 전위를 82행 "$\dd\phi/\dd T$", 83행 "$F\,\dd U/\dd T$"로 기호 전환($\phi$↔$U$) — $\phi$ 는 국소 정의 없이 등장 | P3-①(전위 기호 일관). tier-B swiderska 값서 $\dd U/\dd T{=}\dd\phi/\dd T$ 로 동일시(정합). 흑연 부록에 LCO(R6) 전방참조라 $\phi$ 는 §lco-center 정의 의존 | 사전존재. R6 를 $U$(또는 $\phi$) 한 기호로 통일 또는 "$\phi{\equiv}$단전극 OCP" 1구 |

### ch1_appB_codemap.tex (전문 정독 완료, 158행 — 특별 축)

**대조(축②)**: v1.0.19 대비 변경 **2곳** — (78행) "가역**열**" → "가역 **발열**"(P6 정정, 어구 "발효 시 폭·가역 발열 config 계수" 중 발열 부분만 교체); (97행) MIT 게이트 행에 "(출처·tier 는 \S\ref{sec:lco-gate})" 병기(U11). 나머지 동일 — 주변 문장 훼손 없음.
**축③ P6 "가역 발열" 검증(정확)**: 78행 정정 rubric C2("가역열 금지, v1.0.17 결정")와 정합, 문장("발효 시 폭·가역 발열 config 계수에 동반 전파") 문법·의미 **온전**. 전 _sections 스윕 결과 "가역열" 잔존 **0건** → 정정 완결·straggler 없음.
**U11 검증**: 97행 "\S\ref{sec:lco-gate}" 참조 라벨 실재(ch1_sec15:185 `\label{sec:lco-gate}`) → \ref 해소 정상.
**특별 축 대조(전건 정합)**: \eqref 참조 본문 정합 — tab:symcode $\xi_\mathrm{lag}$→eq:lag ✓, tab:inputs w→eq:wbase·dS_a→eq:Lqfull·Omega/gamma→eq:dUhys/Ubranch·z_cut/A_cap 기본값 4.357/4.0→eq:Acut ✓, tab:nodecode N8→eq:lag/reversal·N1 $V_n{=}V_\mathrm{in}{-}\sigma_d|I|R_n$→appA S8 정합 ✓; 회귀 서술 N2 스니펫 $U(298){=}0.0853$V→tab:staging 2→1(0.085) ✓. 기본값(n=1·dVdq_qa=0·dS_a=0·seed I=0.1/Q=1) sec08·sec10 정합.
**Ch2 appB 상충 검사(충돌 없음)**: Ch1 appB 는 "구현 대응표"(현존 v1.0.19 코드 역방향 조회), Ch2 appB 는 "doc-leads 요구명세"(코드 개정 회귀 기준) — **번호/스탠스 차이는 P6 판정 완료 항목**. 요구 충돌 없음: 양측 동일 $\bar x$ 진입점(solve_U_oc·entropy_coefficient_x·reversible_heat_x, Ch1 132-135행이 "요구명세는 Ch2 부록 B"로 명시 위임), 동일 가역 발열 부호($\dot Q_\rev{=}-IT\,\partial U_\oc/\partial T$, 방전 발열 +), 동일 θ_E-부재 bit-exact 하위호환, 동일 두-상 폭 자유피팅 규정.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O2-12 | ch1_appB:9 vs 23-24 | L | ① | 9행 "\code{dqdv}(물리 부호 $s$ 직접 입력)" 이 기호 "$s$"를 코드 파라미터 명으로 사용 — 그러나 tab:symcode(23-24행)는 "코드 \code{s} 파라미터는 방향 부호 $\sigma_d$ 를 받는 자리라 유도-전용 $s$($\equiv{+}1$)와 별개"로 분리. 9행이 가드보다 14행 앞서 "$s$"를 노출 | rubric B5(기호 충돌 각주 가드). 물리-$s$(항상 +1)와 코드 param \code{s}(=$\sigma_d$) 충돌. tab:symcode 가 해소하나 9행에서 선노출 | 사전존재(regression 아님). 9행을 "방향 부호($\sigma_d$)를 코드 인자 \code{s} 로 직접 입력"으로 명확화 |
| O2-13 | ch1_appB:5 | L | ① | 5행 코드 파일명 "\code{Anode\_Fit\_v1.0.19.py}" 를 v1.0.20 문건이 참조(구현 버전 stale) | REFERENCE_LEDGER: numverif2026 "코드 버전 표기는 P8 갱신" — **알려진 P8 이연 항목**(P7 결함 아님). doc-leads 하 코드가 문건에 후행하는 것은 정합 | P8 에서 버전 문자열 갱신(현 단계 무조치 정당) |


