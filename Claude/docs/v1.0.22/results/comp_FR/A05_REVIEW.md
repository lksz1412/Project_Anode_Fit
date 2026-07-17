# A05_REVIEW — ch1_sec04_hys.tex (§4 히스테리시스 분기 중심 N3) 심층 검토

- 검토 창: FR-A05 (v1.0.22 대공사)
- 대상: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch1_sec04_hys.tex` (전문 정독, 336행 전량)
- 소속 빌드: `ch1_graphite_v1.0.22.tex` (Ch1 흑연 81p; `\externaldocument{ch2_lco_v1.0.22}` xr 확인)
- 규율: 보고 전용 — 소스 수정 X · git 조작 X · `Codex/` 접근 X. P5(이름·구조 보존 — 개정은 제안만) 준수. GS-1/GS-2(Ch3 Si 정직 공백)와 본 절 무관 확인 — 본 보고의 어떤 제안도 GS 공백을 메우지 않음.
- 행 번호 기준: 2026-07-17 08:29 판 (파일 mtime).
- 상태: 검토 완료본 (서치 절만 하이쿠 서브 결과 대기 → 도착 후 §7 갱신)

---

## 1. 검증 로그 (재계산·재유도 — 관점② 의무 수행 기록)

전 수식·전 그림 좌표·전 참조를 독립 재계산/원문 대조했다. 요약:

**수식 사슬 (전량 재유도 일치)**
- eq:gpp: d²/dξ²[ξlnξ+(1-ξ)ln(1-ξ)] = 1/[ξ(1-ξ)], d²/dξ²[Ωξ(1-ξ)] = -2Ω → g''=RT/[ξ(1-ξ)]-2Ω ✓ (Part 0 eq:sm-thresh 유도와 동일).
- eq:spinodal: ξ²-ξ+RT/2Ω=0 → ξ=½(1±√(1-2RT/Ω)) ✓.
- eq:Veq: eq:eqcond(μ=μ⁰-sF(V-U), ch1_sec03_center.tex:33-37 원문 확인) + eq:mu(μ_Li(θ)-μ⁰=f'(θ), ch1_sec02b_part0.tex:41 원문 확인) + 우함수 대칭 f(1-ξ)=f(ξ)(ch1_sec02b_part0.tex:44-52) → μ⁰+f'(1-ξ)=μ⁰-sF(V-U) → f'(ξ)=sF(V_eq-U_j). μ⁰ 상쇄 논거 정확함 ✓ (θ-좌표 선형 몫 μ⁰θ 의 미분 μ⁰ 가 양변에서 소거).
- eq:hyssub: ξ_s^±=(1±u)/2 → odds=(1±u)/(1∓u), (1-2ξ)=∓u ✓.
- eq:hysdiff: ln[(1-u)/(1+u)]-ln[(1+u)/(1-u)]=-4 artanh u, [u-(-u)]=2u ✓.
- eq:dUhys(s=+1): ΔU=(2/F)[Ωu-2RT artanh u] ✓. 양수성: Ω=2RT/(1-u²) 대입 → u/(1-u²)=u+u³+… > artanh u=u+u³/3+… (u∈(0,1)) → ΔU>0 ✓.
- Taylor 정해: (2/F)[2RT(u+u³)-2RT(u+u³/3)]=(8RT/3F)u³ ✓. 함정 재현: 상수 대입 (2/F)[2RTu-2RT(u+u³/3)]=-(4RT/3F)u³ ✓ (부호 반전 재확인). u³=(1-T/T_c)^{3/2}∝(T_c-T)^{3/2}, T_c=Ω/2R ✓ (C¹-매끄러운 소멸 ✓).
- eq:hyssym: 로그 몫 합 0 + (1-2ξ) 몫 합 0 → 평균=U_j ✓. 따름: γ=h=1 에서 U_j+½ΔU=V_eq(ξ_s^-) 정확히 (A05-13 참조).
- eq:Ubranch/eq:center: 코드 `func_dU_hys`(Ω≤2RT→0 가드)·`func_U_branch`·branch 가드 `gamma != 0.0 and Omega > 0.0`·`U_j + func_U_branch(T_rep, 0.0, …)` (Anode_Fit_v1.0.22.py:140-154, 551-556) — 문서 서술("U_j 자리에 0 대입해 shift 분만…배열 중심에 더한다" 포함)과 문자 그대로 일치 ✓.

**그림 수치 (재계산 일치 — 표본 전수준)**
- fig:doublewell(Ω=3RT): (0.5, 0.057)→계산 0.05685 ✓, (0.07,-0.058)→-0.05834 ✓, (0.24,-0.004)→-0.00388 ✓, spinodal (0.2113,-0.0155)→-0.01568 ✓. 끝단 (0.03,-0.041)→실제 -0.0474 등 소편차 있으나 캡션이 "개형"(정성)임을 명시하고 수치 정확판은 fig:sm-gxi 로 위임 — fig:sm-gxi 좌표는 재계산 정확 일치 확인((0.213,-0.0149)→-0.01493 ✓).
- fig:hysgap (a): 무차원 gap 2[ωu-2artanh u] — ω=2.02→0.00266 ✓, 2.05→0.01046 ✓, 2.1→0.02940 ✓, 2.5→0.31122 ✓, 3→0.83019 ✓(마커 0.830 ✓), 3.5→1.44884 ✓, 4→2.13137 ✓(마커 2.131 ✓), 5→3.61892 ✓, 6→5.21289 ✓. 연성 개시 (8/3)u³: ω=2.5→0.23851 ✓, 3→0.51320 ✓, 3.5→0.74820 ✓. 오답 곡선 -(4/3)u³: ω=3→-0.25660 ✓.
- fig:hysgap (b): 298.15 K 교점 — Ω=13000→102.79 mV ✓(표기 102.8), 10000→56.00 ✓, 8000→28.31 ✓, 6000→6.23 ✓(표기 6.2). 곡선 점 표본: (13000, 240 K)→125.38 ✓, (13000, 300 K)→102.12 ✓(표기 102.101), (10000, 590 K)→0.362 ✓(표기 0.36), (6000, 340 K)→1.16 ✓(표기 1.163, 반올림 차 0.003). T_c=Ω/2R: 781.8/601.4/481.1/360.8 K ✓(눈금·태그 782/601/481/361 ✓). 끝점 (781.5 K, 0.001 mV) — (T_c-T)^{3/2} 극한식으로 0.0014 mV ✓.
- fig:hysloop(Ω=4RT): y=ln[ξ/(1-ξ)]+4(1-2ξ) — (0.015,-0.3046) ✓, (0.03,0.2839) ✓, (0.1464,1.0657) ✓, (0.5,0) ✓, (0.8536,-1.0657) ✓. u=√½ ✓, gap=2.1314 RT/F ✓. mV 환산: 298.15 K→54.76→54.8 ✓ / 298.00 K→54.73→54.7 (A05-07). 방전 상승가지→극대 ξ_s^-, 충전 하강가지→극소 ξ_s^+ 의 방향 배정 — dV/dξ=g''/sF 부호 추적으로 재확인 ✓. binodal(y=0 비자명근) ξ_b≈0.0213 — 굵은 과주행 화살표 시점(0.03)이 준안정 구간 안 ✓.
- appA R1 교차: Ω=12000, 298.15 K → u=0.76607, ΔU=86.68 mV ✓ (부록 표기 86.7 일치).

**참조·인계 정합 (전건 원문 대조)**
- eq:mu/eq:gxi/eq:sm-thresh/sec:sm-mf/fig:sm-gxi (ch1_sec02b_part0.tex) ✓ — Ω>0=동종 인력 부호 규약(:27) ✓, "우함수 대칭이 §hys 1계 미분 논거의 뿌리"(:52) 상호 지시 ✓, fig:sm-mu 의 ±1.066 거울 관계 서술과 정합 ✓.
- eq:eqcond (ch1_sec03_center.tex:36) ✓. tab:staging (ch1_sec10_sum.tex:31-43) — Ω 초기값 6000/8000/10000/13000 J/mol 이 fig:hysgap(b) 4곡선·전이명과 1:1 ✓.
- eq:lco-dope (ch1_sec13_lcohys.tex:209) — xr 외부참조로 해소(ch1 드라이버 :8 externaldocument 확인); 내용(도핑 Ω↓→gap 문턱 소멸, 흑연 Taylor 극한 재사용) ✓.
- §broadening(iii-a) (ch1_sec07_broadening.tex:68-74) — "N 입자 앙상블 평탄역 경로" 전방 포인터 내용 일치 ✓; srcbox "부호만 대조" 규정과 본 절 "부호가 일치한다" 주장 정합 ✓. sec:tail(꼬리 방향 반전) ✓. h_{η,j}·γ_j·T_rep·σ_d·s 기호표(ch1_sec01_n0n1.tex:47-70) ✓.
- 상분리 부록(appendix_phase_separation.tex): "준안정 영역 --- 핵생성" 절(app:nucleation:400)·"본문과의 연결" 절(app:link:469) 실재 ✓; ΔG*=16πγ³/3Δg_v², exp(-ΔG*/k_BT), binodal 근방 |Δg_v|→0 발산(:417-427) — 본 절 요약과 일치 ✓; γ[J/m²] 별개 기호·부록 ξ=본문 θ 여집합 고지(:57-59, :404) — 본 절 유의 문장과 쌍방 일치 ✓.
- 서지: dreyer2010(10.1038/nmat2730)·dreyer2011(10.1007/s00161-010-0178-1) — ch1v22_bib.tex:17-18 수록, V1020 원장 V1 등재(dreyer2010 은 master spot-check 7건에 포함)·V1021→V1022 승계 선언 확인 ✓.

**P3 관련**: 이 절 소관 항목(전달식 정합 P3-6: eq:Ubranch/eq:center→eq:xieq(§5)·LCO §13 대입형·spine N3 상자) 충돌 무발견. V_n 위계 침범 없음(평가 전위는 §5 에서 V_n 으로 명시).

---

## 2. 발견 표

> 현행 열의 축자 원문은 표 아래 **§3 축자 블록**에 개행 포함 그대로 수록(markdown 표 셀의 개행 제약 때문 — 기계 매칭은 §3 블록 사용). 표 셀에는 첫 조각만 표시.

| ID | 파일:행 | 유형 | 등급 | 현행(축자 — §3 블록 참조) | 제안(완성 LaTeX — §4 블록 참조) | 근거 |
|----|---------|------|------|---------------------------|----------------------------------|------|
| A05-01 | ch1_sec04_hys.tex:38-39 | 논리 | M | `$u_j$ 가 실수가 되는 조건 $\Omega_j>2RT$ 가 …` [§3.1] | `$u_j$ 가 $(0,1)$ 구간의 실수가 되는 조건 …` [§4.1] | Ω_j<0(Part 0 이 명시 허용하는 반발·교대 정렬, ch1_sec02b_part0.tex:27-28)이면 1-2RT/Ω>1 로 u_j 는 **실수**(>1) — "실수가 되는 조건=Ω>2RT" 는 전 정의역에서 거짓. "(0,1) 구간의 실수" 로 좁히면 전 Ω 에서 정확한 iff (0<Ω≤2RT: 허수 / Ω≤0: u>1 로 [0,1] 밖 / Ω>2RT: u∈(0,1)). 재계산 검증. |
| A05-02 | ch1_sec04_hys.tex:107-108 | 논리 | M | `$\Omega_j\le2RT$ 면 gap 은⏎정확히 $0$ 이다(제곱근이 허수가 되는 영역의 명시 분기)` [§3.2] | `…(0<\Omega_j\le2RT$ 는 제곱근 허수, $\Omega_j\le0$ 은 …)` [§4.2] | A05-01 과 동근: Ω_j≤0 하위경우는 제곱근이 허수가 아니라 u_j>1 (artanh 정의역 밖·이중웰 부재). 코드 가드는 한 조건 `Omega <= two_RT` 로 두 경우를 이미 함께 처리(Anode_Fit_v1.0.22.py:143-144) — 문서 괄호만 하위경우를 오기술. |
| A05-03 | ch1_sec04_hys.tex:236 (eq:hyssym 직후) | 보완 | M | `--- 분기는 $U_j$ 대칭이다.` [§3.3] | Maxwell 전위=U_j 한 줄 폐합 문장 추가 [§4.3] | 본 절이 "평형 전환점(Maxwell 전위)"(:16)·fig:hysloop 파선 라벨 `Maxwell $V_\eq{=}U_j$`(:302)·캡션 "Maxwell plateau(y=0)"(:330-331) 세 곳에서 **Maxwell 전위가 곧 U_j** 임을 사용하나, 절 안에는 그 근거가 없음(eq:hyssym 은 spinodal 중점 대칭까지만). 부록 app:maxwell (c)(:380-381)는 대칭 특수화를 μ 언어(기함수→μ*=μ(½))로만 주고 "그 값이 곧 $U_j$" 라는 전위 번역(μ(½)=f'(½)=0 → eq:eqcond 로 $V_\eq=U_j$)은 부록·본문 어디에도 안 적혀 있음. 우함수 대칭 → V_eq-U_j 가 ξ=½ 기함수 → 등면적 수평선=U_j 로 한 줄에 닫힘(재유도 확인). |
| A05-04 | ch1_sec04_hys.tex:68-73 | 설명·수식화 | M | `\textbf{(a) 출발 --- 비단조 평형 전위 곡선.} …` [§3.4] | 부호 사슬을 display 로 편 대체문 [§4.4] | 현행은 (i) 결과 등식이 먼저, 근거가 뒤 (ii) 3연쇄 부호 사슬 f'(1-ξ)=-f'(ξ)=-g_j'(ξ) 와 μ⁰ 상쇄가 산문 괄호 안 — 본 절 최고 난도 문장. 재유도 결과 논리 자체는 정확(검증 로그) — display 한 줄이면 상쇄 지점이 눈에 보임. 아울러 g_j' 표기가 여기서 '직선 몫 뗀 조성 몫 미분(=f')' 의 뜻으로 쓰임(eq:gxi 의 g_j^0 는 ξ-직선 몫 포함 — Part 0 :46-47)을 명시화. 내용 삭제 없음(어순 재배열+시각화). |
| A05-05 | ch1_sec04_hys.tex:249-251 | 보완 | M | `$h_{\eta,j}$ 는 완전 cycle 을 전제한 분기가 …` [§3.5] | h_{η,j}∈[0,1] 범위·자유도 지위 명시 [§4.5] | "spinodal gap 은 그 피팅값이 넘을 수 없는 열역학 상한" 주장이 성립하려면 곱 h_ηγ≤1 이 필요한데 γ_j∈[0,1] 만 명시되고 h_{η,j} 의 범위는 본문·기호표(ch1_sec01:69 "기본 1")·코드 어디에도 없음. 또 같은 소절 안 "(b)(c) 한 자유도로" 와 "두 인자 모두 값은 피팅이 정하며" 사이 자유도 셈 긴장 — h 는 부분 cycle 데이터가 있을 때만 여는 프로토콜 보정임을 한 절로 해소. |
| A05-06 | ch1_sec04_hys.tex:223-224 (fig:hysgap 캡션 말미) | 보완 | M | `점선 수직선은 $298.15$ K, 그 교점 수치는 spinodal 상한 gap 이며 …` [§3.6] | 실측 흑연 히스 gap 문헌 anchor 문장 후보 [§4.6] | 절 전체가 상한(6.2~102.8 mV @298.15 K)만 주고 **실측 흑연 stage plateau 영전류 갈림의 크기 스케일**(문헌 보고 수~수십 mV)이 어디에도 없어, 독자가 γ_j 의 현실 스케일(실측/상한)을 가늠할 수 없음. 서지 후보는 §7 서치 절(하이쿠 검증분) — **원장(V1022_REFERENCE_LEDGER) 등재 절차 통과 후에만 \cite 부여** 전제의 후보 제안. |
| A05-07 | ch1_sec04_hys.tex:329 (fig:hysloop 캡션) | 논리(수치 표기) | L | `(식~\eqref{eq:dUhys}; $298$ K 에서 $54.8$ mV)` [§3.7] | `(식~\eqref{eq:dUhys}; $298.15$ K 에서 $54.8$ mV)` | 2.13137·RT/F = 54.76 mV(298.15 K)→54.8 ✓ / 298.00 K 는 54.73→**54.7**. 같은 절 fig:hysgap 은 298.15 K 로 표기 — 수치 54.8 의 실제 평가 온도로 통일(§3 의 U(298) 관행은 수식에 298.15 명시라 사정 다름). |
| A05-08 | ch1_sec04_hys.tex:81-82, 89 | 설명 | L | `…logit 인자와⏎$(1-2\xi)$ 인자가 …` / `--- 곧 두 끝점에서 logit 인자가 서로 역수다.` [§3.8] | odds 몫 명명으로 정정 [§4.8] | 표준 정의 logit=ln[ξ/(1-ξ)] 기준이면 "서로 역수" 인 것은 로그가 아니라 그 안의 odds 몫 ξ/(1-ξ) (로그끼리는 부호 반대 같은 크기 — eq:hysdiff 직후 산문이 이미 그렇게 말함). eq:hyssub 가 표시하는 양도 odds. 명명만 정밀화하면 두 서술이 정확히 이음. |
| A05-09 | ch1_sec04_hys.tex:78-80 | 보완 | L | `이고 $\Omega_j>2RT$ 면 비단조다 --- 방전은 …` [§3.9] | 과주행 근거(CNT) 전방 포인터 한 구 추가 [§4.9] | 이 시점 독자 질문 "왜 binodal 에서 갈라지지 않고 가지에 머무나"의 답(핵생성 지수 억제)이 두 소절 뒤(§4.3 CNT 문단)에 있음 — 전방 포인터 한 구로 선제. |
| A05-10 | ch1_sec04_hys.tex:39 | 보완 | L | `이 문턱을 넘지 못하면($\Omega_j\le2RT$) 분기 gap 은 정확히 0 이다(식~\eqref{eq:dUhys} 참조).` [§3.10] | 문턱 수치 2RT≈4.96 kJ/mol 과 표 Ω 대조 병기 [§4.10] | 2×8.314×298.15=4957.6 J/mol (appA R2 의 4958 과 일치). tab:staging Ω 6~13 kJ/mol 이 전건 문턱 위임을 §4 자리에서 즉시 읽게 함(§7 :24 의 같은 취지 서술과 정합). |
| A05-11 | ch1_sec04_hys.tex:5-6 | 논리(개시문 정밀) | L | `평형 중심 $U_j$ 는 상호작용 $\Omega_j$ 와 분기 인자 $\gamma_j$ 가 있으면 …` [§3.11] | 조건을 Ω_j>2RT·γ_j≠0 로 정밀화 [§4.11] | "있으면" 은 0<Ω_j≤2RT(gap≡0 — 이동 없음) 를 포함해 과대 서술. 결과값은 eq:center 가드+gap 0 으로 옳으므로 L — 개시 선언만 문턱과 정합화. |
| A05-12 | ch1_sec04_hys.tex:223, 329-330 | 설명 | L | `실측 분기는 $\gamma_j$ 배 안쪽이다` / `실측 분기는⏎$\gamma_j$ 만큼 안쪽` [§3.12] | `$h_{\eta,j}\gamma_j$ 배(완전 cycle $h_{\eta,j}{=}1$ 에서 $\gamma_j$ 배)` [§4.12] | eq:Ubranch 의 실측 gap = h_ηγΔU — 기본 h=1 에서만 γ 배. 두 캡션 동일 사안. |
| A05-13 | ch1_sec04_hys.tex:245 | 설명 | L | `$\gamma_j=1$ 이 spinodal 상한, $\gamma_j\to0$ 이 히스 소멸, …` [§3.13] | γ=1 ⇒ 분기 중심=spinodal 극값 전위 명시 [§4.13] | eq:hyssym(평균=U_j)+eq:dUhys(차=ΔU) ⇒ U_j+½ΔU=V_eq(ξ_s^-) 정확 성립(재유도) — "½" 의 기하적 의미와 γ=1 의 뜻이 한 절로 명시됨. |
| A05-14 | ch1_sec04_hys.tex:269-276 | 설명 | L | eq:center cases (`\gamma_j\ne0 \text{ 이고 } \Omega_j>0`) [§3.14] | 갈래 라벨 주석 한 줄 [§4.14] | 첫 갈래 조건(코드 가드 거울 `gamma!=0 and Omega>0`)은 0<Ω_j≤2RT 도 포함하나 그때 ΔU(T_rep)=0 이라 둘째 갈래와 같은 값 — 물리 문턱(Ω>2RT)과 코드 가드의 차이가 값 불변임을 주석으로. 코드 대조 완료(값 전 구간 일치). |

**H 등급: 0건** — 수식 유도·부호·그림 수치·코드 대응·서지 귀속에서 H 급 오류를 찾지 못함 (검증 범위는 §1 로그).

---

## 3. 현행 축자 블록 (기계 매칭용 — 개행 포함 원문 그대로)

### §3.1 (A05-01) ch1_sec04_hys.tex:38-39
```latex
$u_j$ 가 실수가 되는 조건 $\Omega_j>2RT$ 가 상분리(따라서 히스테리시스)의 문턱이며($g''<0$ 구간이 생겨 한 전위에 여러
$\xi$ --- 그림~\ref{fig:doublewell}), $\Omega_j\le2RT$ 면 갈라짐이 없다.
```

### §3.2 (A05-02) ch1_sec04_hys.tex:107-108
```latex
$\Omega_j\le2RT$ 면 gap 은
정확히 $0$ 이다(제곱근이 허수가 되는 영역의 명시 분기).
```

### §3.3 (A05-03) ch1_sec04_hys.tex:236
```latex
--- 분기는 $U_j$ 대칭이다.
```

### §3.4 (A05-04) ch1_sec04_hys.tex:68-73
```latex
\textbf{(a) 출발 --- 비단조 평형 전위 곡선.} 평형 조건~\eqref{eq:eqcond}($\mu=\mu^0-sF(V-U)$, 배치 몫 자유에너지 기울기 $=$ 전기화학 구동력)에 의해 자유에너지~\eqref{eq:gxi} 의 1계 미분이 곧 평형 전위에 묶인다
($g_j'(\xi)=RT\ln[\xi/(1-\xi)]+\Omega_j(1-2\xi)=sF(V_\eq-U_j)$). 1차(직선) 몫을 뗀 식~\eqref{eq:gxi} 가 \emph{1계} 미분에서도
옳은 근거는 Part 0 이 세운 조성 몫의 우함수 대칭(\S\ref{sec:sm-mf}: $f(1-\xi)=f(\xi)$, 따라서 $f'(1-\xi)=-f'(\xi)$)이다
--- 식~\eqref{eq:mu} 의 $\mu_\mathrm{Li}(\theta)-\mu^0=f'(\theta)$
에 $\theta=1-\xi$ 를 넣으면 $\mu_\mathrm{Li}-\mu^0=f'(1-\xi)=-f'(\xi)=-g_j'(\xi)$ 가 되고, 뗀 선형 몫이 남긴 상수 $\mu^0$ 가
식~\eqref{eq:eqcond} 양변에서 상쇄돼 선형항 없이도 위 등식이 성립한다.
```

### §3.5 (A05-05) ch1_sec04_hys.tex:249-251
```latex
$h_{\eta,j}$ 는 완전 cycle 을 전제한 분기가 부분 cycle 이력에서 덜 벌어지는 것을
담는 보정 인자다. 두 인자 모두 값은 피팅이 정하며, spinodal gap $\Delta U_j^\hys$ 는 그 피팅값이 넘을 수
없는 열역학 상한을 준다.
```

### §3.6 (A05-06) ch1_sec04_hys.tex:223-224
```latex
점선 수직선은 $298.15$ K, 그 교점 수치는 spinodal 상한 gap 이며 실측 분기는 $\gamma_j$ 배 안쪽이다
(식~\eqref{eq:Ubranch}).
```

### §3.7 (A05-07) ch1_sec04_hys.tex:328-330 (해당 구 포함 문장)
```latex
전위 차가 spinodal 상한 gap $\Delta U_j^\hys=2.131\,RT/F$(식~\eqref{eq:dUhys}; $298$ K 에서 $54.8$ mV), 실측 분기는
$\gamma_j$ 만큼 안쪽(식~\eqref{eq:Ubranch}).
```

### §3.8 (A05-08) ch1_sec04_hys.tex:81-82, 89
```latex
식~\eqref{eq:spinodal} 의 $\xi_{s,j}^\pm=\tfrac12(1\pm u_j)$ 를 식~\eqref{eq:Veq} 의 두 비상수 항에 넣으면, logit 인자와
$(1-2\xi)$ 인자가 두 끝점에서 각각
```
```latex
--- 곧 두 끝점에서 logit 인자가 서로 역수다.
```

### §3.9 (A05-09) ch1_sec04_hys.tex:78-80
```latex
이고 $\Omega_j>2RT$ 면 비단조다 --- 방전은 $\xi\!\approx\!0$ 에서 상승 가지를 극대 $\xi_{s,j}^-$ 까지, 충전은 $\xi\!\approx\!1$
에서 극소 $\xi_{s,j}^+$ 까지 과주행하므로(전위 곡선의 극값이 $\dd V_\eq/\dd\xi=g_j''/sF=0$, 곧 spinodal 과 같은 점 ---
그림~\ref{fig:hysloop}), 두 극값의 전위 차가 분기 gap 의 spinodal 상한이다.
```

### §3.10 (A05-10) ch1_sec04_hys.tex:39
```latex
이 문턱을 넘지 못하면($\Omega_j\le2RT$) 분기 gap 은 정확히 0 이다(식~\eqref{eq:dUhys} 참조).
```

### §3.11 (A05-11) ch1_sec04_hys.tex:5-6
```latex
평형 중심 $U_j$ 는 상호작용 $\Omega_j$ 와 분기 인자 $\gamma_j$ 가 있으면 방향별 분기 중심 $U_j^{\,d}$ 로 이동한다
(그렇지 않으면 $U_j$ 그대로).
```

### §3.12 (A05-12) ch1_sec04_hys.tex:223 / 329-330
```latex
그 교점 수치는 spinodal 상한 gap 이며 실측 분기는 $\gamma_j$ 배 안쪽이다
```
```latex
실측 분기는
$\gamma_j$ 만큼 안쪽(식~\eqref{eq:Ubranch})
```

### §3.13 (A05-13) ch1_sec04_hys.tex:245
```latex
$\gamma_j=1$ 이 spinodal 상한, $\gamma_j\to0$ 이 히스 소멸, $h_{\eta,j}$ 가 부분 cycle 보정(기본 $1$)이다.
```

### §3.14 (A05-14) ch1_sec04_hys.tex:269-276
```latex
\begin{equation}
\mathrm{center}=
\begin{cases}
U_j+\tfrac12\sigma_d h_{\eta,j}\gamma_j\Delta U_j^\hys(T_\rep) & \gamma_j\ne0 \text{ 이고 } \Omega_j>0\\[2pt]
U_j & \text{그 외(분기 없음)}.
\end{cases}
\label{eq:center}
\end{equation}
```

---

## 4. 제안 LaTeX 블록 (완성형 — 대체·보강만, 삭제 없음)

### §4.1 (A05-01) — :38-39 대체
```latex
$u_j$ 가 $(0,1)$ 구간의 실수가 되는 조건 $\Omega_j>2RT$ 가 상분리(따라서 히스테리시스)의 문턱이며($g''<0$ 구간이 생겨 한 전위에 여러
$\xi$ --- 그림~\ref{fig:doublewell}), $\Omega_j\le2RT$ 면 갈라짐이 없다($\Omega_j\le0$ 의 교대 정렬 쪽은 $u_j>1$ 로
근~\eqref{eq:spinodal} 이 $[0,1]$ 밖 --- 식~\eqref{eq:sm-thresh} 의 단상 판정 그대로).
```

### §4.2 (A05-02) — :107-108 대체
```latex
$\Omega_j\le2RT$ 면 gap 은
정확히 $0$ 이다($0<\Omega_j\le2RT$ 는 제곱근이 허수, $\Omega_j\le0$ 은 $u_j>1$ 로 $\mathrm{artanh}$ 정의역 밖$\cdot$이중웰 부재
--- 두 경우를 하나의 명시 분기 $\Omega_j\le2RT$ 로 묶는다).
```

### §4.3 (A05-03) — :236 "--- 분기는 $U_j$ 대칭이다." 직후 보강(추가 문장)
```latex
같은 대칭이 Maxwell 전위도 닫는다 --- $f'(1-\xi)=-f'(\xi)$ 에 의해 $V_{\eq,j}(1-\xi)-U_j=-\big[V_{\eq,j}(\xi)-U_j\big]$
(기함수)라, 등면적 구성의 수평선은 $V_\eq=U_j$ 에 놓인다(일반 구성은 부록 \emph{상분리의 열역학} Maxwell 절).
서두의 ``평형 전환점(Maxwell 전위)''과 그림~\ref{fig:hysloop} 의 파선($y{=}0$)이 이로써 절 안에서 근거를 갖는다.
```

### §4.4 (A05-04) — :68-73 대체 (내용 전량 보존·어순 재배열)
```latex
\textbf{(a) 출발 --- 비단조 평형 전위 곡선.} 평형 조건~\eqref{eq:eqcond}($\mu=\mu^0-sF(V-U)$, 배치 몫 자유에너지
기울기 $=$ 전기화학 구동력)에 식~\eqref{eq:mu} 의 $\mu_\mathrm{Li}(\theta)-\mu^0=f'(\theta)$ 를 $\theta=1-\xi$ 로 넣고,
Part 0 이 세운 조성 몫의 우함수 대칭(\S\ref{sec:sm-mf}: $f(1-\xi)=f(\xi)$, 따라서 $f'(1-\xi)=-f'(\xi)$)을 쓰면
\begin{equation*}
\underbrace{\mu^0+f'(1-\xi)}_{\text{좌변 }=\ \mu_\mathrm{Li}}
=\underbrace{\mu^0-sF(V_\eq-U_j)}_{\text{우변 --- 식~\eqref{eq:eqcond}}}
\quad\Longrightarrow\quad
f'(\xi)=sF(V_\eq-U_j)
\end{equation*}
--- 양변의 $\mu^0$(뗀 선형 몫이 미분에 남긴 상수)가 상쇄되므로, 1차(직선) 몫을 뗀 식~\eqref{eq:gxi} 의 1계 미분
$g_j'(\xi)=f'(\xi)=RT\ln[\xi/(1-\xi)]+\Omega_j(1-2\xi)$ 가 선형항 없이 곧 평형 전위에 묶인다.
```

### §4.5 (A05-05) — :249-251 대체
```latex
$h_{\eta,j}$ 는 완전 cycle 을 전제한 분기가 부분 cycle 이력에서 덜 벌어지는 것을
담는 보정 인자다($h_{\eta,j}\in[0,1]$, 완전 cycle $=1$ 기본 --- 부분 cycle 데이터가 있을 때만 여는 프로토콜 보정이라
전이당 피팅 자유도는 여전히 $\gamma_j$ 하나다). 두 인자 모두 값은 피팅이 정하며, 곱이 $h_{\eta,j}\gamma_j\le1$ 이라
spinodal gap $\Delta U_j^\hys$ 는 그 피팅값이 넘을 수 없는 열역학 상한을 준다.
```

### §4.6 (A05-06) — fig:hysgap 캡션 말미 보강(추가 문장; \cite 는 원장 등재 후 부여)
```latex
실측 흑연 stage plateau 의 영전류 갈림은 문헌 보고 수$\sim$수십 mV 급으로 이 상한 안쪽이다
(서지 검증$\cdot$원장 등재 후 인용 부여 --- tier B anchor 예정).
```
※ 후보 서지는 §7 서치 절 표 — V1 원장 절차(검증→등재→인용) 통과 전 \cite 금지.

### §4.8 (A05-08) — :81-82 해당 구·:89 대체
```latex
식~\eqref{eq:spinodal} 의 $\xi_{s,j}^\pm=\tfrac12(1\pm u_j)$ 를 식~\eqref{eq:Veq} 의 두 비상수 항에 넣으면, 로그 안의
odds 몫 $\xi/(1-\xi)$ 와 $(1-2\xi)$ 인자가 두 끝점에서 각각
```
```latex
--- 곧 두 끝점에서 odds 몫이 서로 역수(따라서 로그는 부호 반대 같은 크기)다.
```

### §4.9 (A05-09) — :80 "spinodal 상한이다." 직후 보강(추가 구)
```latex
(가지에 그때까지 머무는 미시 근거 --- 핵생성 지수 억제 --- 는 \S\ref{sec:hys-branch} 끝의 CNT 문단이 잇는다)
```

### §4.10 (A05-10) — :39 대체
```latex
이 문턱을 넘지 못하면($\Omega_j\le2RT$ --- $298.15$ K 에서 $2RT\approx4.96$ kJ/mol; 표~\ref{tab:staging} 의
$\Omega_j$ 초기값 $6$--$13$ kJ/mol 은 네 건 모두 문턱 위) 분기 gap 은 정확히 0 이다(식~\eqref{eq:dUhys} 참조).
```

### §4.11 (A05-11) — :5-6 대체
```latex
평형 중심 $U_j$ 는 상호작용이 문턱을 넘고($\Omega_j>2RT$) 분기 인자 $\gamma_j\ne0$ 이면 방향별 분기 중심 $U_j^{\,d}$ 로
이동한다(그렇지 않으면 $U_j$ 그대로 --- $0<\Omega_j\le2RT$ 는 식~\eqref{eq:dUhys} 의 gap $0$ 으로 같은 결과).
```

### §4.12 (A05-12) — 두 캡션 해당 구 대체
```latex
실측 분기는 $h_{\eta,j}\gamma_j$ 배(완전 cycle $h_{\eta,j}{=}1$ 에서 $\gamma_j$ 배) 안쪽이다
```
```latex
실측 분기는 $h_{\eta,j}\gamma_j$ 만큼 안쪽(완전 cycle 은 $\gamma_j$ 배 --- 식~\eqref{eq:Ubranch})
```

### §4.13 (A05-13) — :245 대체
```latex
$\gamma_j=1$ 이 spinodal 상한 --- 이때 분기 중심이 정확히 spinodal 극값 전위에 앉는다
($U_j^{\dis}=V_{\eq,j}(\xi_{s,j}^-)$, $U_j^{\chg}=V_{\eq,j}(\xi_{s,j}^+)$ --- 식~\eqref{eq:hyssym} 의 대칭 그대로) ---,
$\gamma_j\to0$ 이 히스 소멸, $h_{\eta,j}$ 가 부분 cycle 보정(기본 $1$)이다.
```

### §4.14 (A05-14) — eq:center 직후 본문 보강(추가 문장)
```latex
첫 갈래의 조건은 구현 가드의 거울이라 $0<\Omega_j\le2RT$ 도 첫 갈래에 들지만, 그때 $\Delta U_j^\hys(T_\rep)=0$
이라 둘째 갈래와 같은 값이다 --- 분기 유무의 물리 문턱은 어디까지나 $\Omega_j>2RT$ 다.
```

---

## 5. 등급별 정리

- **H (0건)**: 없음.
- **M (6건)**: A05-01·02 (문턱 조건의 Ω≤0 하위경우 오기술 — 수식↔산문 정밀), A05-03 (Maxwell=U_j 무근거 사용 — 한 줄 폐합 보강), A05-04 (최난도 문장 display 화 — 설명·수식화), A05-05 (h_η 범위 미명시로 '열역학 상한' 주장의 전제 누락 + 자유도 셈 긴장), A05-06 (실측 스케일 anchor 부재 — γ_j 가늠 불가).
- **L (8건)**: A05-07 (54.8 mV 의 평가 온도 표기), A05-08 (logit/odds 명명), A05-09 (CNT 전방 포인터), A05-10 (문턱 수치 병기), A05-11 (개시문 조건 정밀), A05-12 (γ 배 → h·γ 배), A05-13 (γ=1 기하 명시), A05-14 (eq:center 갈래 라벨 주석).

**추가 후보 (P5 — 수정 제안 아님, 보고만)**: 대칭 정규용액이 강제하는 U_j 대칭 분기(방전·충전 등거리 ½씩)는 실측 비대칭 루프(방향별 이탈점 상이)를 담지 못함 — 필요 시 방향별 γ_j^{dis}/γ_j^{chg} 확장이 자연스러운 자리라는 점만 기록(모델 차원 증가라 현행 '전이당 한 계수' 설계 의도와 상충 — 사용자 결정 사안).

---

## 6. 무발견 축 (검토했으나 문제 없음 — 명시)

1. **수식 유도 전량** (eq:gpp→eq:spinodal→eq:Veq→eq:hyssub→eq:hysdiff→eq:dUhys→Taylor 정·오 전개→u³∝(T_c-T)^{3/2}→eq:hyssym→eq:Ubranch→eq:center): 독립 재유도 전건 일치. 특히 ★Taylor 함정 문단은 정답(+8/3)·오답(-4/3) 양쪽을 재현 계산으로 확인 — 본문 주장 그대로.
2. **부호 체계**: σ_d=+1 방전=탈리튬화=중심 상향, U^dis>U^chg — 실측 갈림 방향(dreyer2010)과의 '부호만 대조' 규정(§7 srcbox) 준수 확인. appA S4·R1 과 수치까지 일치(86.7 mV 재계산 ✓).
3. **그림 3장 수치 좌표**: fig:doublewell(개형 선언·수치판 위임 명시), fig:hysgap (a)(b) 전 anchor·T_c 눈금·298.15 K 교점 4건·근임계 끝점, fig:hysloop 곡선·spinodal 점·gap — 재계산 전건 일치 (A05-07 표기 1건 제외).
4. **참조 실재·내용 정합**: eq:mu·eq:gxi·eq:sm-thresh·eq:eqcond·tab:staging·eq:lco-dope(xr 해소 확인)·§broadening(iii-a)·§tail·부록 두 절 제목·γ[J/m²]/ξ 기호 충돌 고지 — 전건 원문 대조 일치. 깨진 참조 0.
5. **서지 귀속**: dreyer2010·dreyer2011 — bib 수록·DOI 표기·원장 V1(승계 체인 V1020→V1022) 확인. 오귀속 무발견.
6. **코드 정합**: eq:dUhys/eq:Ubranch/eq:center ↔ func_dU_hys/func_U_branch/branch 가드·T_rep — 문자 그대로 일치(가드 조건까지). 문서↔코드 불일치 0.
7. **P3 소관 항목**: 전달식(→§5 eq:xieq·LCO §13·spine N3) 충돌 무발견; V_n 위계 침범 무발견; 명칭 혼동(ver.N/Chapter) 해당 없음.
8. **P5**: 기존 기호·라벨·식 번호 변경 제안 없음(본 보고의 제안은 전부 산문 대체·보강; 신규 라벨 불요).

---

## 7. 서치 절 (하이쿠 서브에이전트 — doi 실검증분만, 2026-07-17)

서브에이전트(model: haiku)가 Crossref API(`api.crossref.org/works/<DOI>`) 실조회로 검증한 후보만 수록.
**전건 후보 지위** — 본문 \cite 부여는 V1 원장 절차(검증→등재→인용) 통과 후에만 가능. 기억 서지 0건(전량 세션 내 Crossref 조회분).

| 슬롯 | 제안 key | 확정 서지(Crossref 추출 그대로) | DOI | 검증 방법 | 서브가 직접 확인한 내용 | 본문 대응 자리 |
|------|---------|--------------------------------|-----|-----------|--------------------------|----------------|
| A(흑연 실측 히스) | mercer_hys2021 | M. P. Mercer, C. Peng, C. Soares, H. E. Hoster, D. Kramer, "Voltage hysteresis during lithiation/delithiation of graphite associated with meta-stable carbon stackings," *J. Mater. Chem. A* **9**(1) 492–504 (2021) | 10.1039/D0TA10403E | Crossref API 조회 | 흑연 음극 충방전 전위 히스테리시스 실험·계산 보고(메타스테이블 스택킹 경로; 고온에서도 잔존 성분 확인 — 서브 열람 기준) | A05-06 anchor 1순위 (fig:hysgap 캡션 보강; §4 의 '준안정 가지' 그림과 기작 서술까지 맞닿음) |
| A(흑연 실측 히스) | jahn_hys2024 | L. Jahn, P. Mößle, F. Röder, M. A. Danzer, "A physically motivated voltage hysteresis model for lithium-ion batteries using a probability distributed equivalent circuit," *Commun. Eng.* **3** (2024) | 10.1038/s44172-024-00221-4 | Crossref API 조회 | 흑연 OCV 히스테리시스 약 **10 mV** 규모 언급 + 부분 사이클 path dependence(서브가 PMC 본문에서 확인) | A05-06 의 "수~수십 mV" 수치 스케일 근거 후보; h_{η,j} 부분 cycle 서술의 실측 근거 겸용 |
| B(부분 cycle 모델) | plett_ekf2_2004 | G. L. Plett, "Extended Kalman filtering for battery management systems of LiPB-based HEV battery packs," *J. Power Sources* **134**(2) 262–276 (2004) | 10.1016/j.jpowsour.2004.02.032 | Crossref API 조회 | one-state 히스테리시스 상태변수 h 모델 원전(권·호·쪽 = Part 2 범위) — ★등재 시 부제 "Part 2. Modeling and identification" 포함 여부 원문 재확인 요 | h_{η,j}(부분 cycle 인자) 문장의 모델링 계보 anchor 후보 |
| B(부분 cycle 모델) | yu_asymhys2022 | P. Yu, S. Wang, C. Yu, W. Shi, B. Li, "Study of hysteresis voltage state dependence in lithium-ion battery and a novel asymmetric hysteresis modeling," *J. Energy Storage* **51** 104492 (2022) | 10.1016/j.est.2022.104492 | Crossref API 조회 | 비대칭 히스테리시스 연산자·minor loop 특성(서브 열람 기준) | §5 '추가 후보'(방향별 γ 비대칭 확장)의 문헌 존재 증거 후보 |
| B(부분 cycle 모델) | he_hysmodel2020 | Y. He, R. He, B. Guo, Z. Zhang, S. Yang, X. Liu, X. Zhao, Y. Pan, X. Yan, S. Li, "Modeling of Dynamic Hysteresis Characters for the Lithium-Ion Battery," *J. Electrochem. Soc.* **167**(9) 090532 (2020) | 10.1149/1945-7111/ab8b96 | Crossref API 조회 + IOP 랜딩 | Prandtl–Ishlinskii play 연산자 중첩으로 major/minor loop 포착(서브가 IOP 랜딩에서 확인) | h_{η,j} 한 계수 보정의 '더 정밀한 대안 계열' 존재를 밝히는 각주 후보 |

서브 보고의 실패/제외: 출판사 원문 페이지 다수 403/리다이렉트(RSC·ScienceDirect·ResearchGate·Nature 등) — Crossref API 로 대체 검증 완료. 원문 전문(full-text) 대조는 미수행(아래 4-tier '미검증' 참조).

**통합 판단(FR-A05)**: A05-06 제안문("실측 수~수십 mV")은 jahn_hys2024 의 ~10 mV(흑연)와 정합 — 다만 이 수치는 서브의 랜딩/본문 열람 보고이므로, 등재 절차에서 원문 수치·조건(온도·전극 구성) 확인 후 tier 배정할 것. mercer_hys2021 은 §4 의 열역학 기원 서술(준안정 가지)과 같은 대상계라 anchor 적합도 최상. B 슬롯 3건은 h_{η,j} 문장(A05-05)의 계보 각주용 — 본문 골격(전이당 한 계수)을 바꾸지 않는 선에서만.

---

## 8. 말미 4-tier (확정/추정/미검증/무발견)

- **확정** (재계산·원문 대조로 검증): §1 검증 로그 전 항목; 발견 A05-01·02·07 의 수치·논리 근거; 참조·코드·서지 정합 판정.
- **추정** (합리 추론 — 검증 불완전): A05-05 의 h_{η,j}∈[0,1] 이 설계 의도라는 판단(기호표 '기본 1'과 상한 주장에서 역산한 추론 — 설계자 확인 필요); A05-06 의 "실측 수~수십 mV" 스케일(§7 jahn_hys2024 의 ~10 mV 보고와 정합하나 서브의 랜딩/본문 열람 수준 — 원문 수치 확정은 등재 절차 몫); 추가 후보(비대칭 γ 확장)의 필요성은 데이터 의존.
- **미검증**: dreyer2010/2011 **논문 전문 내용** 자체(서지·원장 지위만 확인 — 본문 주장 대조는 '부호만 대조' 규정 범위 안이라 별도 전문 검증 불요 판단); tikz 렌더 픽셀 결과(좌표 수치만 재계산 — PDF 시각 확인은 본 창 범위 밖); §7 후보 5건의 **전문(full-text) 내용**(Crossref 서지 필드 검증만 완료 — 출판사 원문 다수 403; plett_ekf2_2004 부제 포함 여부 재확인 필요 표기).
- **무발견 축**: §6 명시 8개 축.
