# V1.0.13 P5 검수 라운드 4 — 검수자 A 보고서

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` **L1–1000** (서론·N0·Part 0 전체·N1·N2·N3 초입; 문장 완결을 위해 L1009 까지 정독)
- 코드 대조: `Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py`
- 청크 스킴: **라인·부호 창**(~80줄 창 14개) — 창마다 ±부호·지수 부호·첨자/윗첨자·부등호 방향·분모/분자 위치·화살표/증감 프로즈 전수 점검 + 렌즈 ⑧(R1–R3 수정분 재정독)
- 역할 제한 준수: 검수 의견만, tex/코드 수정 0

---

## 지적 사항

### [HIGH] L370–371 — Helmholtz $F$ vs Faraday $F$ 구분 문구의 위치 서술이 반대 (분자/분모 오류)

- **원문(L369–371)**: "($\langle E\rangle=\partial(\beta F)/\partial\beta$·$S=-\partial F/\partial T$ 가 열역학 관계와 일치함이 이 명명의 근거다; 이 $F$ 는 Faraday 상수 $F$ 와 기호만 같고 문맥으로 갈린다 — **전자는 미분 분모**, 후자는 전하 환산 곱)"
- **무엇이**: 전자(= Helmholtz $F$)는 바로 그 문장의 $\partial(\beta F)/\partial\beta$·$\partial F/\partial T$ 에서 모두 **미분의 분자**(피미분량)에 놓인다. 미분 분모는 $\beta$·$T$ 다. 반대로 이 문건에서 **분모**에 상습 출현하는 쪽은 Faraday $F$($w=RT/F$ L672, $U_j=(\cdots)/F$ L912). 즉 이 구분 규칙을 그대로 적용하면 독자는 $RT/F$ 의 $F$ 를 Helmholtz 로 오인하게 된다 — 구분 문구가 구분을 정확히 거꾸로 안내한다.
- **비고**: 이 문구는 R1–R3 수정 삽입분("L370 F 구분 문구")으로, 렌즈 ⑧(직전 수정의 새 결함) 적중.
- **수정안**: "전자는 미분 분모" → "전자는 미분의 분자(피미분 자유에너지 — $\partial F/\partial T$ 처럼 미분당하는 쪽), 후자는 전하 환산 인자($FV$·$RT/F$ 의 곱·나눗셈 상수)".

### [MED] L516 — "본론 표의 $\Omega_j$·$\Omega_j^\mathrm{cat}$" 중 $\Omega_j^\mathrm{cat}$ 는 어떤 표에도 없음 (문서 내 자기모순)

- **원문(L516)**: "본론 표의 $\Omega_j$·$\Omega_j^\mathrm{cat}$ [J/mol]이 정확히 이 슬롯이다."
- **무엇이**: $\Omega_j$ 는 N0 기호 표(L243)에 있으나, $\Omega_j^\mathrm{cat}$ 는 문서 내 5개 표(L223·L1804·L1886·L2765·L2823) 어디에도 열/행으로 실려 있지 않다. 오히려 L2118 이 명시적으로 "표~\ref{tab:lco-staging} 는 LCO $\Omega_j^\mathrm{cat}$ 의 수치 열을 싣지 않으며"라고 못박아, L516 의 "본론 표의 …$\Omega_j^\mathrm{cat}$" 주장과 정면 모순된다.
- **수정안**: "본론 표의 $\Omega_j$ 와 Part II 의 $\Omega_j^\mathrm{cat}$(표 밖 — 피팅 배정 전제, \S\ref{sec:lco-intro} 이하)이 정확히 이 슬롯이다" 류로 귀속 정정.

### [LOW] L209–210 — R1–R3 삽입분 "격자 역전이 지지 \emph{방향}을 가른다"의 '지지' 가 문서 유일 출현·미정의

- **원문(L209–211)**: "꼬리($\mathrm N7\cdot\mathrm N8$ — 방향별 전달계수 $\chi_d$ 가 꼬리 \emph{길이}를, 격자 역전이 지지 \emph{방향}을 가른다)"
- **무엇이**: '지지'(인과 기억 커널의 support)는 전 문서에서 이 한 곳에만 출현(grep 확인 — L149 의 "사라지지"는 무관)하고, N8 절(\S\ref{sec:tail})도 이 용어를 쓰지 않는다. N0 시점의 독자는 '지지 방향'을 해독할 수 없다(G-follow). 문법 자체는 병렬 구조("A가 X를, B가 Y를 가른다")로 성립 — 삽입이 인접 문장을 깨지는 않음.
- **수정안**: "격자 역전이 기억이 딛는 \emph{과거 방향}을 가른다" 또는 "인과 기억의 진행 \emph{방향}을 가른다" 로 자체 완결 표현 사용.

### [LOW] L984 캡션 — fig:doublewell 좌표가 근사(정성)인데 캡션에 그 표시가 없음 (형제 그림과 rigor 비대칭)

- **원문**: 내부 주석 L968 "% double-well free energy g(xi) for Omega=3RT (qualitative shape, normalized)" vs 캡션 L984 "격자기체 자유에너지 $g_j(\xi)$ (식~\eqref{eq:gxi}, $\Omega_j=3RT$; 신규 그림)."
- **무엇이**: 형제 그림 fig:sm-gxi(L582)·fig:sm-mu(L613)·fig:sm-occ(L753)는 "좌표는 식 그대로의 수치 평가"를 명시하는데, 이 그림만 침묵. 실제 좌표는 근사다 — 검산: $\xi=0.03$ 플롯 $-0.041$ vs 식값 $-0.0474$(오차 0.006), spinodal 점 $y=-0.0155$ vs 식값 $-0.0157$(fig:sm-gxi L572 는 $-0.0157$ 사용). $\xi=0.5$ 의 $0.057$·$\xi=0.24$ 의 $-0.004$ 등 중앙부는 정확.
- **수정안**: 캡션에 "(개형 — 정성 곡선; 수치 정확 버전은 그림~\ref{fig:sm-gxi} 의 $\Omega=3RT$ 곡선)" 류 한정어 추가, 또는 좌표를 식 평가값으로 교체.

### [NOTE] L846 — "격자 점 수엔 카디널리티 표기를 쓴다"의 어휘 모호

- **원문(L846)**: "($\mathrm{len}(\cdot)$ 는 배열 원소 개수 — 이 문건에서 $|\cdot|$ 는 물리량 크기 전용이라 격자 점 수엔 카디널리티 표기를 쓴다; …)"
- **무엇이**: 통상 '카디널리티 표기'는 $|\cdot|$ 를 가리키는데, 본문은 $|\cdot|$ 를 피하려고 $\mathrm{len}(\cdot)$ 를 쓰면서 그것을 '카디널리티 표기'라 부른다 — 한 번 더 읽어야 풀리는 자기지시. "격자 점 수엔 $\mathrm{len}(\cdot)$ 를 쓴다" 로 직서하면 충분.

### [NOTE] L677 — "자리당 $k_BT\!\cdot\!e$ 가 몰당 $RT\!\cdot\!F$ 로 한꺼번에 환산"의 $\cdot$ 가 곱으로 오독 여지

- **원문(L677)**: "(자리당 $k_BT\!\cdot\!e$ 가 몰당 $RT\!\cdot\!F$ 로 한꺼번에 환산)"
- **무엇이**: 의도는 쌍(pair) 나열($k_BT\mapsto RT$, $e\mapsto F$)인데 $\cdot$ 는 이 문서 전반에서 곱셈/나열 겸용이라 곱 $k_BTe$ 로 읽힐 수 있다. "자리당 $(k_BT,\,e)$ 가 몰당 $(RT,\,F)$ 로" 병기 권고.

### [NOTE] L219 — "분기 중심 $\pm\tfrac12\sigma_d(\cdots)$"의 $\pm$ 는 장식적 중복

- **원문(L219–220)**: "분기 중심 $\pm\tfrac12\sigma_d(\cdots)$ 는 방전$\cdot$충전이 반대로 갈리고"
- **무엇이**: 실식(fig:spine L171·코드 `func_U_branch` L151)은 고정 $+\tfrac12\sigma_d h_\eta\gamma\,\Delta U_\hys$ — 부호는 $\sigma_d=\pm1$ 이 이미 나른다. 접두 $\pm$ 는 독립된 추가 부호로 오독될 수 있다(부호-창 관점의 결벽 지적). "$+\tfrac12\sigma_d(\cdots)$ 는 $\sigma_d$ 를 따라 방전·충전이 반대로 갈리고" 권고.

---

## 검산 수행 내역 (PASS 확인 — 근거 요약)

**부호·식 사슬(전수)**
- $\dd S$ 전개(L336)→$\partial S/\partial N=-\mu/T$(L339)→Taylor $-E_i/T+\mu N_i/T$(L358)→Gibbs 인자 $e^{-\beta(E_i-\mu N_i)}$(L364)→$\Xi$·$\langle N\rangle=k_BT\,\partial\ln\Xi/\partial\mu$(L379–384): 전 단계 부호 정합 확인.
- eq:partfn(L415)→eq:sm-occmid(L424)→eq:fermifn(L431, 분모·분자 $e^{-\beta\Delta\mu}$ 나눗셈)·극한(L434–435: $\Delta\mu\gtrless0\to\theta\to0/1$, $\mu\to\pm\infty\to\theta\to1/0$ — 순서쌍 정합)·요동 $\partial\theta/\partial(\beta\mu)=+\theta(1-\theta)$(L444, 직접 미분 재검산 일치).
- $S_\mathrm{mix}$(L469)→$\mu=\varepsilon+k_BT\ln[\theta/(1-\theta)]$(L475, $\partial S_\mathrm{mix}/\partial n$ 직접 재계산 일치)→역변환 $e^{\beta\Delta\mu}=(1-\theta)/\theta$(L478) 일치.
- 평균장: $\theta^2=\theta-\theta(1-\theta)$ 분해와 $\Omega\equiv-\tfrac z2N_Au$(L511) — $u<0\Rightarrow\Omega>0$(인력→상분리, L514) 부호 정합. eq:mu(L527)·eq:gxi(L535)·$g''=RT/[\xi(1-\xi)]-2\Omega_j$(L541·L951)·문턱 $\Omega_j\le2RT\Leftrightarrow g''\ge0$(L545, 최솟값 $4RT$ 재검산)·$T_c=\Omega_j/2R$(L546) 전부 정합.
- 전기화학 연결: workbal−refbal 차감(L633−L641)→$\mu_\mathrm{Li}-\mu^\mathrm{metal}_\mathrm{Li}=-FV$(L649) 재유도 일치; $U\equiv(\mu^\mathrm{metal}_\mathrm{Li}-\mu^0)/F$(L655) 대입 시 eq:sm-eqcond(L658) 항등 성립; logistic 지수 $+sF(V-U)/RT$($\theta_\eq$)·$-sF(V-U)/RT$($\xi_\eq$)(L670–671) 부호쌍 정합; 평형비 $e^{sF(V-U)/RT}$(L687) 일치; Nernst $V_\eq=U_j+\tfrac{RT}{sF}\ln\tfrac{\xi}{1-\xi}$(L787) 역변환 일치.
- N1: eq:vapppol→eq:vn 이항(L816→L829) 부호 보존; 방전 $V_n<V_\app$/충전 $V_n>V_\app$(L833) 프로즈-식 정합.
- N2: eq:Ujmid→eq:Uj(L905→L912) 분자 부호 정리 정확; $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$(L917) Gibbs 항등식 경유 재검산 일치; $U(298)=(13000-298.15\times16)/96485=0.08530$ V(L927–928) 산술 재계산 일치; $\Delta S=16$, 30 K 창 → 4.97 mV = "수 mV"(L918) 정합.
- N3 초입: $g''=0\Rightarrow\xi^2-\xi+RT/(2\Omega_j)=0$→$\xi_{s,j}^\pm=\tfrac12(1\pm u_j)$, $u_j=\sqrt{1-2RT/\Omega_j}$(L954–959) 근의 공식 재검산 일치; eq:Veq(L999) 및 극대 $\xi_s^-$/극소 $\xi_s^+$ 과주행 서술(L1002–1004) — $g''$ 부호 구간으로 극값 종류 확인; logit 끝점 $(1\pm u)/(1\mp u)$(L1008) 상하 부호 정합.

**그림 수치 좌표(스팟 검산)**
- fig:sm-gxi: $f(0.5)/RT=-0.6931/-0.4431/-0.1931/-0.0681/+0.0569$($\Omega=0/1/2/2.5/3RT$) 전부 식값 일치; spinodal $\xi_s^\pm=0.2113/0.7887$·$f=-0.0157$ 일치.
- fig:sm-mu: $\theta=0.02$ 에서 $-3.892/-1.972/-0.0518$($\Omega/RT=0/2/4$) 일치; 극값 $\theta_s^\pm=0.1464/0.8536$, $\pm1.0657$ 일치; "V_eq 곡선은 $\theta=1-\xi$·부호 반전 거울"(L616) — $1-2\theta=-(1-2\xi)$ 항등으로 확인.
- fig:sm-occ: (a) $T_0/2\cdot T_0\cdot2T_0$ 곡선 $x=-1$ 에서 $0.8808/0.7311/0.6225$ 일치; (b) $w=23.1/25.7/28.3$ mV(268.15/298.15/328.15 K) 재계산 일치, $V=0.08$ 의 $\xi_\eq$ 3값·$\theta_\eq(0)=0.9647$ 일치.
- fig:staging: 갤러리 채움 {1,5}/{1,4}/{1,3,5}/{1,3,5}/{1..6} — stage 4/3/2L/2/1 주기 정합(층선 7개·갤러리 6개 기하 확인).

**코드 대조(문건 주장 ↔ py 원문)**
- `V_n = V_in - sigma_d * I_abs * self.Rn`(py L437) = tex L832 인용 그대로.
- `func_U_j` `(-dH_rxn + T*dS_rxn)/F`(py L80) = eq:Uj·tex L915.
- N2 seam: py L462–463 `func_U_j(T_work, tr['dH_rxn'], self._effective_dS_rxn(tr, T_work))`·흑연 base 항등 반환(py L554) = tex L923–926 codebox 서술 정합 (R-fix 확인).
- v_span floor: py L440 `max(v_hi - v_lo, self.v_span_floor)`·기본 1e-6(py L258) = tex L847 (R-fix 확인). `n_work = max(2048, 2·len)`(py L441·L257)·패딩 0.15/0.15(py L256)·`T_rep=mean(T_work)`(py L455) = tex L846–848.
- 분기 중심 `U_j + 0.5*sigma_d*h_eta*gamma*dU_hys`(py L151) = fig:spine L171·표 L245–247; `if Omega <= two_RT: return 0.0`(py L140–141) = tex L962–963.
- $\chi_d$: `chi if sigma_d >= 0 else 1-chi`(py L166) = 표 L250; $\Delta H_a^\eff=$`dH_a - chi_d*Omega`(py L158) = 표 L253; $\mathcal A=$`min(z_cut*n*R*T, A_cap*R*T)`(py L360) = 표 L251; z_cut 4.357·A_cap_RT 4.0(py L255) = 표 L257–258.
- `GRAPHITE_STAGING_LIT` 4건 U=0.210/0.140/0.120/0.085(py L712–734) = tex L299; stage 2→1 dH=−13000·dS=−16(py L735) = codebox L927; Ω 초기값 6000–13000 > 2RT(298 K)=4958 J/mol — 헤더 주석 L23 "전부>2RT" 정합.
- 폭 역산 `n = w*F/(R*T)`(py L306) = 표 L237 "n=wF/RT".

**R1–R3 수정분 재정독(렌즈 ⑧ — 담당 구간 내 12건)**
- L209 σ_d 작용처 확장: 문법 성립·셋 열거가 signbox(L702)·item(i)(L684–685)와 3중 일치 — 단 '지지' 용어는 [LOW] 지적.
- L226(현 L227) s 행: "본론 결과-사슬 boxed 식에서 s=1 소멸(Part 0 박스는 명시 유지)" — eq:Uj(무 s)·eq:sm-logistic/nernst(유 s) 실태와 일치. PASS.
- L291(현 L292) stage1 {1..6}: 기하 정합. PASS.
- L370 F 구분 문구: **[HIGH] 결함 — 위 지적 1**.
- L416(현 L418–419) Z 대정준 문구: 문법·물리 정합. PASS.
- L444 βµ 미분: 직접 재검산 일치. PASS.
- Part 0 item(i) 여집합 relabel(L681–685): $\mathrm{logistic}[-x]=1-\mathrm{logistic}[x]$ 항등·종 불변 서술 정확, 작용처 3중 일치. PASS.
- signbox 작용처(L698–703): 부호 사슬 $V\!\uparrow\Rightarrow\mu\downarrow\Rightarrow\theta\downarrow,\xi\uparrow$ 정합. PASS.
- fig:sm-occ 캡션 괄호 이동(L753–754): 문법·물리 정합. PASS.
- eq:sm-mubridge $P\Delta v\ll RT,FV$(L768): 존재·문법 정합. PASS.
- N2 codebox seam 문구(L924–926): 코드 정합. PASS.
- eq:vwork v_span_floor 문구(L847–848): 코드 정합. PASS.

**라벨 무결성**: 이동 편입 라벨 eq:partfn(L416)·eq:fermifn(L432)·eq:mu(L528)·eq:gxi(L536) 각 1회만 정의(중복 0 — 헤더 L308 "원위치 정의 삭제 필수" 이행 확인). 담당 구간이 참조하는 전방 라벨(sec:eqpeak/dist/width/signcheck/sum/tail/lco-intro/lco-code·fig:hysloop/broadening 등) 전부 실재.

---

## 가장 약한 1곳

**L370–371 의 $F$ 구분 문구**. 부호·위치를 다루는 문장이 위치를 거꾸로 서술("미분 분모")해, 구분 규칙을 적용할수록 오히려 $RT/F$ 의 Faraday $F$ 를 Helmholtz 로 오인시킨다. R1–R3 에서 삽입된 문장 자체의 결함이라 이후 라운드가 "존재 확인"만 하면 계속 통과해 버리는 위치이기도 하다.

## 물리 불변 확인

- $\Delta\mu=+sF(V-U)$ (즉 $\mu^0-\mu_\mathrm{Li}=+sF(V-U)$): L658·L676–677·L893 전 출현 일치 — **PASS**
- $s=+1$ 관례(유도 전용 고정 부호·$\sigma_d$ 와 분리): L227·L655–656·L788·L891·L903 일관 — **PASS**
- $w=RT/F$: L672·L701·L756·L793·py `func_w`(L76) 일관 — **PASS**

## Coverage 선언 (창 분할 — 빠짐 없음)

| 창 | 줄 범위 | 내용 |
|---|---|---|
| W1 | L1–128 | 헤더 주석·preamble·매크로 |
| W2 | L129–196 | 서론·관측·fig:spine |
| W3 | L197–263 | N0 본문·부호 규약·기호 표 |
| W4 | L264–333 | fig:staging·Part 0 도입·eq:sm-S |
| W5 | L334–406 | eq:sm-fund→eq:sm-gc·fig:sm-reservoir |
| W6 | L407–492 | 단일 자리→lattice gas (partfn·fermifn·flucres·Smix·mucount·muideal) |
| W7 | L493–555 | 평균장 (sm-omega·gtheta·eq:mu·eq:gxi·sm-thresh) |
| W8 | L556–620 | fig:sm-gxi·fig:sm-mu 좌표 검산 |
| W9 | L621–704 | 전기화학 연결 (emu→eqcond→logistic·item i–iii·signbox) |
| W10 | L705–760 | fig:sm-occ 좌표 검산 |
| W11 | L761–805 | sm-macro (mubridge·nernst·keybox) |
| W12 | L806–860 | N1 (vapppol·vn·vwork·keybox) |
| W13 | L861–933 | N2 (gibbsdef→eqcond→Ujmid→Uj·codebox) |
| W14 | L934–1000 | N3 초입 (gpp·spinodal·fig:doublewell·eq:Veq; L1009 까지 문장 완결 정독) |

L1–1000 사이 미점검 줄 없음(창 경계 연속).

## 5줄 요약 (오적발 자기표시)

1. 확정 결함은 HIGH 1건(L370 "미분 분모" — 분자/분모 반전, R-fix 삽입문 자체)·MED 1건(L516 $\Omega_j^\mathrm{cat}$ "본론 표" 귀속 — L2118 과 자기모순)이며 둘 다 원문 인용·교차 근거 확보.
2. LOW 2건(L210 '지지' 고아 용어·L984 정성 그림 미표시)은 G-follow/rigor 비대칭 지적 — 문체 재량으로 기각될 여지 있음(오적발 후보).
3. NOTE 3건(L846 카디널리티 어휘·L677 $\cdot$ 오독·L219 장식적 $\pm$)은 결벽 수준 — 기각되어도 물리 무손실(오적발 후보).
4. 부호 사슬·부등호·첨자·분수 방향은 14창 전수에서 상기 외 결함 0 — 그림 4종 좌표 수치 검산·코드 12개 항목 대조 전부 일치.
5. 물리 불변 3종($\Delta\mu=+sF(V-U)$·$s=+1$·$w=RT/F$) 전부 PASS, R1–R3 수정분 12건 중 11건 PASS·1건(L370)이 금회 HIGH.
