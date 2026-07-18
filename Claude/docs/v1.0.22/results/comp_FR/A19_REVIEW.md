# A19_REVIEW — Ch2 LCO §2.4 삼분해(ch1_sec14_lcodecomp.tex) · §2.5 전자항(ch1_sec15_lcoelec.tex) 심층 검토

- 검토 창: FR-A19 (v1.0.22 대공사, BRIEF_FR_A.md 규율 준수 — 보고 전용)
- 대상: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch1_sec14_lcodecomp.tex` (144행)
  · `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch1_sec15_lcoelec.tex` (387행)
  — 두 파일 전문 정독 완료. 파일명은 ch1_* 이나 소속은 ch2_lco_v1.0.22.tex 빌드(역사적 파일명).
- 검토 4관점: ①내용 보완 ②논리 오류(재계산·재유도) ③더 쉬운 설명 ④산문→수식 간결화
- 상태: 진행 중 — 발견 검증 완료분부터 즉시 append.

## 발견 표

| ID | 파일:행 | 유형 | 등급 | 현행(축자) | 제안(완성 LaTeX) | 근거 |
|----|---------|------|------|------------|------------------|------|

★표기 규약: 현행·제안이 개행/파이프를 포함해 표 셀에 축자 보존이 불가하므로, 인덱스 표(요지)+발견별 상세 블록(코드펜스 안 **축자 원문**·**완성 LaTeX 제안**)의 2단 구성으로 기록한다. 기계 매칭은 상세 블록의 코드펜스를 사용할 것.

| ID | 파일:행 | 유형 | 등급 | 현행(요지→상세) | 제안(요지→상세) | 근거(요지) |
|----|---------|------|------|------------------|------------------|------------|
| A19-01 | ch1_sec15_lcoelec.tex:348, 363-364 | 논리 | H | "게이트 중심 x̄=x_MIT=0.85" + (b)표 행 라벨 | 좌표 구분 명시 재서술(수치 전량 보존) | x̄=탈리튬화 분율(eq:sm-mc-balance) ≠ x=Li 함량(eq:ggate). 문서 자체 매핑 eq:lco-xmap 적용 시 두 행의 게이트 역할이 역전 |
| A19-02 | ch1_sec15_lcoelec.tex:377-378 | 논리 | H | verifybox (ii) "전자항 유무가 계수를 바꾸지 않는다(국소성 확인)" | 동결 상수의 무국소성 사실대로 재서술 | 구현 직접 구동 반증: off 시 −0.312→−0.035 mV/K(ΔH 고정)/+0.054(재보정) — 어느 규약에서도 대폭 변화 |
| A19-03 | ch1_sec15_lcoelec.tex:345-346 | 보완 | M | "기준온도 동결 근사(§lco-Se-units — T_ref 상수 오프셋…)" | 조성 동결(x_center) 병기 + 정처 포인터 §lco-code | 동결 근사의 정의·조성 동결은 §17 소관. x-동결 누락이 (a)-(c) 오독의 뿌리 |
| A19-04 | ch1_sec15_lcoelec.tex:14-15 | 논리/보완 | M | "흑연·LiC6 모두 전도성이 좋아 … g(E_F) 가 크게 바뀌지 않아" | 절대 규모 논거로 교체 | 반정금속→금속: 상대 변화는 큼. 옳은 논거는 g·Δg 의 절대 규모가 LCO 게이트(13 e/eV/atom) 대비 작다는 것 |
| A19-05 | ch1_sec15_lcoelec.tex:329-330 | 설명 | M | 그림 caption "작지만(게이트 골 몰당 ≈−46 …)" | '작다'의 술어를 적분 방출량에 재배정 | −46 J/(mol K)는 슬롯 지배 규모(시연 T1 +6 압도, 흑연 −16 의 ~3배). 본문 자체 '세 양의 구분' 규율과 충돌 |
| A19-06 | ch1_sec15_lcoelec.tex:174-179 | 보완 | M | eq:dSe 박스(∂g/∂x) | 전미분 자격 명시 한 문장 추가 | "g'(E_F)·dE_F/dx 항 누락?"이라는 독자 질문 선제 — 게이트가 전미분을 현상학화함을 명시 |
| A19-07 | ch1_sec15_lcoelec.tex:208-212 | 수식화 | M | ★부호 규약 닫는 논리(산문 사슬) | 한 줄 함의 사슬 display 수식 | 4단 인과가 산문 3행에 분산 — 수식 1행으로 정확·간결 |
| A19-08 | ch1_sec15_lcoelec.tex:199-201 | 수식화 | M | 몰당 게이트형 닫힌식(인라인·무번호) | 번호 있는 식으로 승격(신규 라벨 제안) | 이후 3곳(§lco-Se-scale·U1T2 문단·§lco-worked)이 이 닫힌꼴을 3중 식번호 조합으로 참조 — 단일 라벨화 |
| A19-09 | ch1_sec14_lcodecomp.tex:20-27 | 보완 | M | eq:lco-Sadd (⟹ 부분) | Li 금속측 상수 흡수 한 문장 추가 | 삼분해는 양극측 부분몰만 — 상대극 Li(s) 몰엔트로피는 x-무관 상수로 ΔS⁰ 슬롯 흡수됨을 명시해야 Reynier 다리(실측 ΔS 등치)가 정밀해짐 |
| A19-10 | ch1_sec14_lcodecomp.tex:117-118, 124 | 보완 | M | ★4.2/9.0 "원문 정량 대조 확인 필요" flag | flag 해소 문구로 교체(0.18 flag 는 유지) | 하이쿠 서치: 원문 초록 축자 확인 "as large as 9.0 kB/atom"·"4.2 kB/atom within the 'O3'" — 값·단위 정합. 0.18 은 초록 미등장 → flag 유지 |
| A19-11 | ch1_sec15_lcoelec.tex:124-127 | 설명 | M | (c) 동결 정당화 문장(순환 서술) | 비순환 재서술(협폭+완만 → O(T³) 각주 포인터) | "표준 처방이라 정당"은 순환 — 실근거는 협폭·g 완만·홀짝 상쇄(각주에 이미 존재) |
| A19-12 | ch1_sec15_lcoelec.tex:19-20 | 설명 | M | "x 가 ~0.94 아래로 내려가면 Co⁴⁺ 정공이 생겨" | 정공 생성(x<1 즉시)과 금속화(0.94 경계) 분리 | 자체 bgbox 의 불순물 준위 기작과 정합화 — 정공은 x<1 부터 존재하되 국소화, 0.94 는 비국소화 개시 |
| A19-13 | ch1_sec15_lcoelec.tex:205-208 | 설명 | L | "MIT 전 구간 적분 ≈1.1 k_B(… 항등)" | 게이트 잔차 괄호 주석 | logistic 은 x=1 에서 4.7% 잔차 → 적분 = 끝점의 95.3%(1.053 vs 1.106 k_B). '항등'은 완전 닫힘 이상화에서만 정확 |
| A19-14 | ch1_sec15_lcoelec.tex:160-169 | 수식화 | L | 신뢰 등급 3구성요소(산문) | 3행 미니표 | 함수형/anchor/연속곡선 × tier × 근거의 3×3 구조가 표에 정확히 맞음 |
| A19-15 | ch1_sec14_lcodecomp.tex:56-58 | 수식화 | L | ★스코프 주의(산문) | 2행 대조 미니표 | 성분(슬롯) vs 총합(상수)의 장 간 기호 충돌 경고는 표가 오독 방지에 유리 |

---

### A19-01 (H·논리) — §lco-worked 의 좌표 등치 오류: x̄(탈리튬화 분율) ≠ x(Li 함량)

**파일:행** `ch1_sec15_lcoelec.tex:348-350` 및 `:363-364` (b)표 행 라벨.

**현행(축자, :348-350)**
```latex
\textbf{(a) 슬롯 산술 --- 게이트 중심.} 게이트 중심 $\bar x=x_\mathrm{MIT}=0.85$ 에서
식~\eqref{eq:dSegate} 의 골 깊이는 $\Delta S_e=-45.7$ J/(mol\,K)(\S\ref{sec:lco-Se-scale} 의 검산값
그대로)이고, T1 슬롯의 유효 반응 엔트로피와 그 기울기 몫은
```
**현행(축자, :363-364)**
```latex
\bar x=0.50\ (\text{게이트 밖}) & 3.9243 & -0.312 & (-0.328/+0.015)\\
\bar x=0.85\ (\text{게이트 중심}) & 4.0095 & -0.128 & (-0.215/+0.087)
```

**문제.** (i) `eq:sm-mc-balance` 의 x̄ 는 **탈리튬화 분율**(ΣQ_jξ_j=Qx̄, ch1_sec02b_part0.tex:331-344 축자 확인)이고, 게이트 파라미터 x_MIT≈0.85 는 **Li 함량**(§lco-why: "x=1 절연체", 2상역 x≈0.75–0.94; `eq:lco-xmap` 의 x 도 동일)이다 — 서로 **반평행 좌표**인데 "게이트 중심 x̄=x_MIT=0.85" 로 등치했다. (ii) 문서 자체 매핑 `eq:lco-xmap`(x=0.94−0.19·ξ_eq,1)을 시연 세트에 적용하면(구현 구동, U₁(298,eff)=3.9300): x̄=0.50 ⟹ U_oc=3.9242, ξ_eq,1=0.4522, **x=0.854 → σ(1−σ)=0.2496 = 게이트 중심**(최대 0.25 의 99.8%); x̄=0.85 ⟹ ξ_eq,1=0.9341, **x=0.762 → σ(1−σ)=0.126**(금속측, ΔS_e^국소=−23.1 J/(mol K)) — 즉 두 행의 라벨 "(게이트 밖)/(게이트 중심)" 이 문서 자신의 매핑 하에서 **역전**된다. (iii) 수치가 그대로 재현되는 이유는 구현(`Anode_Fit_v1.0.22.py:931-934`)이 게이트를 `x_center=0.85` **동결 상수**(−45.678 J/(mol K), V·x̄ 무관)로 넣기 때문이지, x̄=0.85 가 게이트 중심이어서가 아니다. tier-C 시연 면책은 파라미터 **값**에 대한 것이지 좌표 의미론에는 미치지 않는다.

**제안(완성 LaTeX — 수치·표 전량 보존, 서술만 교체).** :348-350 을
```latex
\textbf{(a) 슬롯 산술 --- 동결 조성 $=$ 게이트 중심.} 현행 모델은 전자항을 동결 조성
$x_\mathrm{center}{=}x_\mathrm{MIT}$ 에서 평가한 $V$-무관 상수로 T1 슬롯에 넣으므로(\S\ref{sec:lco-code}
단일-기준 근사), 슬롯에 실리는 값은 게이트 중심 조성 $x{=}x_\mathrm{MIT}{=}0.85$(Li 함량)의 골 깊이
식~\eqref{eq:dSegate} $\Delta S_e=-45.7$ J/(mol\,K)(\S\ref{sec:lco-Se-scale} 의 검산값 그대로)이다 ---
아래 $\bar x$ 는 전하 보존 좌표(탈리튬화 분율, 식~\eqref{eq:sm-mc-balance})로 게이트의 조성 좌표
$x$(Li 함량)와 \emph{다른 축}이며, 좌표 매핑 \S\ref{sec:lco-code} 식~\eqref{eq:lco-xmap} 으로는
$\bar x{=}0.50$ 근방이 T1 창 중앙($\xi_{\eq,1}{\approx}0.45$, $x{\approx}0.85$)에 대응한다. T1 슬롯의
유효 반응 엔트로피와 그 기울기 몫은
```
로, :363-364 의 행 라벨을
```latex
\bar x=0.50\ (\text{T1 창 중앙, }\xi_{\eq,1}{\approx}0.45) & 3.9243 & -0.312 & (-0.328/+0.015)\\
\bar x=0.85\ (\text{T1 창 후반$\cdot$T3 활성, }\xi_{\eq,1}{\approx}0.93) & 4.0095 & -0.128 & (-0.215/+0.087)
```
로 교체. (c) 의 수치·부호 반전 서술은 동결-상수 모델의 사실로서 그대로 유효(보존).

**근거.** ①`eq:sm-mc-balance` 원문(ΣQ_jξ_j=Qx̄, ξ=탈리튬화 진행률) ②`eq:lco-xmap` 원문(x_hi,1=0.94, x_lo,1=0.75) ③구현 구동 재현: (b)(c) 전 수치 일치(−0.312/−0.128/+0.160/4.1008 V/U_oc 이동 −91 mV) + 매핑값 x(0.50)=0.854/x(0.85)=0.762 ④U_oc 가 x̄ 에 단조증가(3.9243<4.0095)라는 표 자체가 x̄=Li 함량 해석(단조감소 요구)과 모순 — x̄ 는 탈리튬화 분율일 수밖에 없음.

---

### A19-02 (H·논리) — verifybox (ii) "국소성 확인" 주장은 구현 구동으로 반증됨

**파일:행** `ch1_sec15_lcoelec.tex:377-378`.

**현행(축자)**
```latex
(ii) 게이트 밖($\bar x{=}0.50$)에서는 전자항 유무가 계수를
바꾸지 않는다(게이트 폭 $\Delta x_\mathrm{MIT}{=}0.05$ 밖 --- 국소성 확인).
```

**문제(재계산 반증).** 같은 시연 세트로 v1.0.22 구현을 직접 구동한 결과(검증 로그 V-A):

| 상태 | x̄=0.50: U_oc / 완전식 | x̄=0.85: U_oc / 완전식 |
|------|------------------------|------------------------|
| 전자항 ON | 3.9242 V / **−0.312** mV/K | 4.0095 V / −0.128 mV/K |
| OFF(ΔH 고정 — (c)와 동일 규약) | 4.0426 V / **−0.035** mV/K | 4.1008 V / +0.160 mV/K |
| OFF(U(298) 재보정) | 3.9243 V / **+0.054** mV/K | 4.0095 V / +0.107 mV/K |

x̄=0.50 에서 전자항 on/off 는 계수를 −0.312↔−0.035(ΔH 고정) 또는 −0.312↔+0.054(재보정)로 **대폭·부호까지** 바꾼다 — (c)가 쓴 것과 동일한 off 규약(ΔH 고정: x̄=0.85 에서 +0.160/4.1008 V 재현 확인)에서도 성립. 이유: 동결 상수 전자항은 x̄-국소성이 원천적으로 없고(V·x̄ 무관 상수), x̄=0.50 에서 T1 가중이 74.8%로 **지배적**(전이별 가중 74.8/24.3/1.0%, 슬롯 −0.411 mV/K)이기 때문. "게이트 폭 밖"이라는 근거 자체가 A19-01 의 좌표 오독(오히려 x̄=0.50 이 매핑상 게이트 중심)에 기대고 있다. ※(i)·(iii)은 구동 재현으로 참 확인 — (ii)만 허위.

**제안(완성 LaTeX — (ii) 대체).**
```latex
(ii) 동결 근사(\S\ref{sec:lco-code})의 전자항은 $V$-무관 상수라 조성 국소성이 \emph{없다} ---
$\bar x{=}0.50$ 에서도 T1 슬롯(가중 $\approx75\%$)에 $-45.7$ J/(mol\,K) 가 실려 있으며, 끄면 계수가
$-0.312\to-0.035$ mV/K(ΔH 고정 규약)로 크게 변한다. 게이트의 조성 국소성($\bar x$ 축 아닌 $x$ 축,
식~\eqref{eq:lco-SeV} 의 $z_e(V)$)은 조성-국소 평가를 도입하는 round-trip 피팅 단계의 검증 항목이다.
```

**근거.** 구현 `LCOCathodeDQDV._effective_dS_rxn`(py:918-935) 은 `func_dSe_molar(tr['x_center'],...)` 를 **무조건 가산**(x̄ 인자 부재 — 시그니처상 국소성 불가능). `entropy_coefficient_x` 구동 수치 상표. (b)의 보고치 −0.312(단순식 −0.328)가 이미 T1 슬롯의 −0.411 mV/K 를 74.8% 가중으로 포함 — "게이트 밖"이라던 점에서 전자항이 계수의 주성분. 추정(참고): 구판 시연은 중간 dict 에 x_MIT=0.50 을 배정했었다는 구현 주석(py:872-873) — (ii)는 그 시절 좌표의 화석일 가능성.

---

### A19-03 (M·보완) — 동결 근사 서술에서 조성 동결(x_center) 누락

**파일:행** `ch1_sec15_lcoelec.tex:344-346`.

**현행(축자)**
```latex
크기의 감각이지 실측 예측이 아니다. 전자항은 기준온도 동결 근사(\S\ref{sec:lco-Se-units} ---
$T_\mathrm{ref}$ 상수 오프셋; 다온도 $T^2$ 곡률은 식~\eqref{eq:U1T2} 소관)로 들어간다. $T=298.15$ K.
```

**문제.** 동결은 **이중**(T_ref 온도 동결 + x_center 조성 동결 — §17 원문: "조성도 $x{=}x_\mathrm{center}$ 로 동결해 $V$-무관 상수")인데 온도 동결만 언급되고, 포인터도 동결 근사를 정의하지 않는 §lco-Se-units 로 향한다(그 소절은 단위·부호·T-의존·T² 계수 소관). 조성 동결 누락이 (a)-(c)의 "게이트 중심" 오독(A19-01)과 (ii) 국소성 착시(A19-02)의 서술적 뿌리.

**제안(완성 LaTeX)**
```latex
크기의 감각이지 실측 예측이 아니다. 전자항은 이중 동결 근사 --- 기준온도 $T_\mathrm{ref}$ 동결($T^2$
곡률은 식~\eqref{eq:U1T2} 소관)에 더해 조성도 $x{=}x_\mathrm{center}$ 로 동결한 $V$-무관 상수
오프셋(\S\ref{sec:lco-code} 단일-기준 근사; 단위$\cdot$부호 규약은 \S\ref{sec:lco-Se-units}) --- 로
들어간다. $T=298.15$ K.
```

**근거.** §17(ch1_sec17_msmr.tex:150-153) 축자: "\emph{현행 모델}은 $\Delta S_e$ 를 $T_\mathrm{ref}$ 에서 동결한 상수 오프셋(단일-기준 근사 --- 조성도 $x{=}x_\mathrm{center}$ 로 동결해 $V$-무관 상수)"; 구현 py:878 `'x_center': 0.85` · py:933. tab:lco-staging caption 도 동일 서술.

---

### A19-04 (M·논리/보완) — 흑연 무전자항 논거의 부정확: "g(E_F) 가 크게 바뀌지 않아"

**파일:행** `ch1_sec15_lcoelec.tex:14-15`.

**현행(축자)**
```latex
삽입 반응의 전체 엔트로피 변화는 ``리튬 자리 배열''(config)$\cdot$``격자 진동''(vib)$\cdot$``전자 준위 점유''
(electronic) 세 자유도의 합이며, 흑연에서는 셋째 몫이 작다 --- 흑연$\cdot$$\mathrm{LiC_6}$ 모두 전도성이 좋아
충방전 동안 $g(E_F)$ 가 크게 바뀌지 않아 전자 분포의 엔트로피 \emph{변화}가 거의 없다. LCO 는 다르다:
```

**문제.** 흑연은 반정금속(semimetal)이라 $g(E_F)$ 가 극소이고 LiC$_6$ 는 금속 — 리튬화로 $g(E_F)$ 의 **상대** 변화는 크다(0 근방→유한). 전자항이 무시되는 실제 이유는 **절대 규모**: 흑연 계열의 $g$·$\Delta g$ 가 LCO 금속상의 $g_{\max}\!\approx\!13$ e/eV/atom 대비 한 자릿수 이상 작아, $\Delta S_e=\tfrac{\pi^2}{3}k_B^2T\,\Delta g$ 가 LCO 게이트 골의 수 % 에 그친다는 것. "모두 전도성이 좋아 … 크게 바뀌지 않아"는 전제(반정금속)와도, 결론의 옳은 근거와도 어긋난다.

**제안(완성 LaTeX)**
```latex
삽입 반응의 전체 엔트로피 변화는 ``리튬 자리 배열''(config)$\cdot$``격자 진동''(vib)$\cdot$``전자 준위 점유''
(electronic) 세 자유도의 합이며, 흑연에서는 셋째 몫이 작다 --- 흑연(반정금속)도 $\mathrm{LiC_6}$(금속)도
$g(E_F)$ 의 \emph{절대 규모}가 작아(LCO 금속상 $g_{\max}\!\approx\!13$ e/eV/atom 의 한 자릿수 이상 아래),
충방전에 따른 $g(E_F)$ 변화가 실어 나르는 전자 엔트로피 $\propto\Delta g$ 도 그만큼 작다. 절연체$\to$금속으로
$g$ 가 $0\!\to\!13$ 으로 켜지는 LCO 는 다르다:
```
(서지 보강 후보: 흑연/LiC$_6$ $g(E_F)$ 정량값 1차 문헌 — §서치 하이쿠-2 결과에 따름; 검증분 없으면 수치 인용 없이 위 문형 유지.)

**근거.** 반정금속 흑연의 $g(E_F)\to$ 극소는 표준 사실(전제 "전도성이 좋아"와 상충). 규모 논거는 본문 자체 식~\eqref{eq:Se}·\eqref{eq:dSe} 에서 직접 따라나옴($\Delta S_e\propto\Delta g$). 결론("흑연 전자항≈0")은 보존 — 논거만 교정.

---

### A19-05 (M·설명) — 그림 caption 의 "작지만( … ≈−46 J/(mol K))" 술어 오배정

**파일:행** `ch1_sec15_lcoelec.tex:329-330` (caption).

**현행(축자)**
```latex
$x_\mathrm{MIT}$ 에서 $\sigma(1-\sigma)$ 가 최대): 전이 중심의 \emph{국소
봉우리}다 --- 작지만(게이트 골 몰당 $\approx-46$ J/(mol\,K), \S\ref{sec:lco-Se-scale}) MIT 구간에만 켜지는 게이트라 config 단독으로 대체 불가.
```

**문제.** −46 J/(mol K)는 '작은' 양이 아니라 이 문서 안에서 **가장 큰 슬롯 규모**다(흑연 −16 의 ~3배; 시연 T1 의 +6 을 압도해 유효 슬롯 −39.7 로 뒤집음 — §lco-worked (a)). '작다'가 정당한 대상은 적분 방출량(≈1.1 k_B/atom)과 O3 부분몰(≈0.18 k_B/atom)이고, 골 깊이는 1/Δx≈20 증폭 탓에 크다 — 본문 '세 양의 구분'이 정확히 이 혼동을 금지("한자리에 섞지 않는다")하는데 caption 이 어긴다.

**제안(완성 LaTeX)**
```latex
$x_\mathrm{MIT}$ 에서 $\sigma(1-\sigma)$ 가 최대): 전이 중심의 \emph{국소
봉우리}다 --- 적분 방출량은 작지만($\approx1.1\,k_B$/atom) 골 깊이는 게이트 미분 증폭($1/\Delta x_\mathrm{MIT}$)으로 몰당 $\approx-46$ J/(mol\,K) 에 이르러(\S\ref{sec:lco-Se-scale} 세 양의 구분) MIT 구간 T1 슬롯을 지배하며, config 단독으로 대체 불가.
```

**근거.** §lco-Se-scale 자체 수치(1.1 k_B·0.18 k_B·−46)와 §lco-worked (a)(+6−45.7=−39.7). '세 양의 구분' 규율 자기일관.

---

### A19-06 (M·보완) — eq:dSe 의 ∂g(E_F,x)/∂x 가 전미분임을 명시

**파일:행** `ch1_sec15_lcoelec.tex:174-179` (eq:dSe 박스 직후 보강).

**현행(축자)**
```latex
\begin{equation}
\boxed{\;\Delta S_{e,j}(x,T)\;\equiv\;\frac{\partial S_e}{\partial x}\Big|_T
=\frac{\pi^2}{3}\,k_B^2\,T\,\frac{\partial g(E_F,x)}{\partial x}\;\;(<0\ \text{at MIT, 삽입 기준})\;}
\label{eq:dSe}
\end{equation}
로 정의한다.
```

**문제.** 밴드 이론 독자는 "삽입이 전자를 채우니 $E_F(x)$ 이동항 $g'(E_F)\,\dd E_F/\dd x$ 가 따로 있어야 하지 않나"를 묻게 된다. 본문 의도는 $g(E_F,x)\equiv g\!\big(E_F(x),x\big)$ 의 **전미분**을 게이트 하나로 현상학화하는 것(§lco-gate)이나 명시가 없다.

**제안(완성 LaTeX — "로 정의한다." 문장 교체)**
```latex
로 정의한다. 여기서 $g(E_F,x)$ 는 조성 의존 Fermi 준위에서 평가한 $g\big(E_F(x),x\big)$ 이고
$\partial g/\partial x$ 는 그 \emph{전미분} --- 밴드 재구성 몫과 $E_F(x)$ 이동 몫($g'\,\dd E_F/\dd x$)을
게이트~\eqref{eq:ggate} 가 한꺼번에 현상학화하므로 별도 항이 더 붙지 않는다.
```

**근거.** Sommerfeld 유도의 $g(E_F)$ 는 $E_F$ 에서의 값 — 조성 미분 시 두 채널이 자동 포함되는 구조를 한 줄로 닫아 독자 질문 선제. 게이트 현상학("이 미시 기작 전체를 … $g(E_F,x)$ 하나로 현상학화" — §lco-why bgbox)과 정합.

---

### A19-07 (M·수식화) — ★부호 규약 닫는 논리의 산문 사슬 → 함의 사슬 수식

**파일:행** `ch1_sec15_lcoelec.tex:208-212`.

**현행(축자)**
```latex
닫는 논리는 --- 삽입($x\!\uparrow$)
으로 금속$\to$절연체라 $g(E_F)$ 가 $g_{\max}\!\to\!0$ 으로 \emph{감소}하므로 $\partial g/\partial x<0$, 따라서
식~\eqref{eq:dSe} 의 $\Delta S_{e,j}=+\partial S_e/\partial x<0$ --- MIT 구간에서 전이당(삽입당) 전자 엔트로피가
\emph{음의 골}이고, 그 절댓값 $|\Delta S_{e,j}|=-\partial S_e/\partial x>0$ 이 탈리튬화 시 방출되는 봉우리다
```

**제안(완성 LaTeX — 산문 유지 + 한 줄 사슬 병기)**
```latex
닫는 논리는 한 줄 사슬로 닫힌다:
\begin{equation*}
x\uparrow\ (\text{삽입})\ \Longrightarrow\ \text{금속}\to\text{절연체}\ \Longrightarrow\
\frac{\partial g}{\partial x}<0\ \xRightarrow{\ \eqref{eq:dSe}\ }\ \Delta S_{e,j}<0,
\qquad |\Delta S_{e,j}|=-\frac{\partial S_e}{\partial x}>0\ (\text{탈리튬화 방출 봉우리}),
\end{equation*}
```
(이후 "--- MIT 구간에서 …" 이하 기존 문장은 보존.)

**근거.** 부호 논쟁이 잦은 지점(삽입/탈리튬 기준·골/봉우리 이중 표현)을 기계 검증 가능한 형태로 고정 — P3-2 류 '식 중심' 규율과 정합. `\xRightarrow` 는 amsmath 표준.

---

### A19-08 (M·수식화) — 몰당 게이트형 닫힌식의 식번호 승격

**파일:행** `ch1_sec15_lcoelec.tex:199-201`.

**현행(축자)**
```latex
이를 대입한 게이트형 몰당 닫힌식은 $\Delta S_{e,j}^{\,\mathrm{mol}}=-\tfrac{\pi^2}{3}R(k_BT/e_V)(g_{\max}/
\Delta x_\mathrm{MIT})\sigma(1-\sigma)$ 이며(게이트 파라미터 $g_{\max}\cdot x_\mathrm{MIT}\cdot\Delta x_\mathrm{MIT}$
와 logistic $\sigma$ 의 정의는 다음 소절 \S\ref{sec:lco-gate} 가 닫는다 --- 여기서는 그 닫힌꼴을 미리 제시),
```

**문제/이득.** 이 닫힌꼴이 실제 계산의 최종 사용식인데 무번호 인라인이라, 이후 §lco-Se-scale("식~eq:dSegate·eq:gunit 의 몰당 닫힌식으로")·★T² 문단("식~eq:dSemolar·eq:gunit 의 몰당 나눗셈 형")·§17("몰당 나눗셈 형(식~eq:dSegate·eq:gunit·eq:dSemolar)")이 매번 2–3개 식번호 조합으로 지칭한다.

**제안(완성 LaTeX — 신규 라벨 제안 표기)**
```latex
이를 대입한 게이트형 몰당 닫힌식은
\begin{equation}
\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)=-\frac{\pi^2}{3}\,R\,\frac{k_BT}{e_V}\,
\frac{g_{\max}}{\Delta x_\mathrm{MIT}}\,\sigma(1-\sigma)
\qquad[\text{J/(mol\,K)}]
\label{eq:dSemolgate}% 신규 라벨 제안
\end{equation}
이며(게이트 파라미터 $g_{\max}\cdot x_\mathrm{MIT}\cdot\Delta x_\mathrm{MIT}$
와 logistic $\sigma$ 의 정의는 다음 소절 \S\ref{sec:lco-gate} 가 닫는다 --- 여기서는 그 닫힌꼴을 미리 제시),
```
(이후 참조들은 `\eqref{eq:dSemolgate}` 단일 지칭으로 단순화 가능 — 참조 교체는 후속 선택.)

**근거.** 구현 `func_dSe_molar`(py:176-192)가 정확히 이 식 — 문서↔구현 1:1 대조(부록 B 원칙)에도 단일 라벨이 유리.

---

### A19-09 (M·보완) — 삼분해와 측정 ΔS 사이의 Li 금속측 상수 몫 명시

**파일:행** `ch1_sec14_lcodecomp.tex:20-27` (eq:lco-Sadd 직후 보강).

**현행(축자)**
```latex
\begin{equation}
S_j=S_j^\mathrm{config}+S_j^\mathrm{vib}+S_j^{e}\ (+\,S_j^{\times}\!\approx\!0)
\;\Longrightarrow\;
\Delta S_{\rxn,j}^\mathrm{cat}(x,T)=\frac{\partial S_j^\mathrm{config}}{\partial x}
+\frac{\partial S_j^\mathrm{vib}}{\partial x}
+\frac{\partial S_j^{e}}{\partial x}.
\label{eq:lco-Sadd}
\end{equation}
```

**문제.** 하프셀 삽입 반응(Li(s)→Li(host))의 $\Delta S_{\rxn,j}$ 에는 상대극 Li 금속의 몰엔트로피 $-s_{\mathrm{Li(s)}}$ 가 들어가는데, 우변은 양극측 부분몰 세 몫만이다. 이대로면 ⟹ 가 등식으로 읽혀 상대극 몫이 증발한 듯 보이고, srcbox 의 Reynier 등치(실측 $\Delta S=F\,\dd U/\dd T$ 는 Li 금속측 포함)와의 정합 질문이 남는다. 실제로는 $x$-무관 상수라 $\Delta S_j^0$(중심 표준값) 슬롯에 흡수되는 구조 — 한 줄 명시가 필요.

**제안(완성 LaTeX — 식 직후 문장 추가)**
```latex
(상대극 Li 금속의 몰엔트로피 몫 $-s_{\mathrm{Li(s)}}$ 는 $x$-무관 상수라 우변의 조성 미분에 나타나지
않고 중심 표준값 $\Delta S_j^0$ 슬롯으로 흡수된다 --- 삼분해가 가르는 것은 $x$-의존 구조이고, 절대
기준선은 슬롯 상수의 몫이다.)
```

**근거.** Part 0 결선(ch1_sec02a:84, ch1_sec02b:156 — Li 금속 저장조가 $\mu$ 고정)에는 있으나 삼분해 근방(grep 확인)엔 무언급. Reynier 실측치(하프셀 vs Li)와 슬롯의 점대점 대조 시 상수 오프셋의 소재를 못박아야 '부호·척도 수준 대조' 원칙이 정밀해짐.

---

### A19-10 (M·보완) — Reynier 4.2/9.0 k_B flag 의 해소(초록 축자 확인)·0.18 flag 유지

**파일:행** `ch1_sec14_lcodecomp.tex:117-118` (및 :124 의 0.18 flag 는 유지).

**현행(축자)**
```latex
곧 본문이 $U_j(T)$ 온도 이동으로 슬롯에 싣는 $\Delta S_{\rxn,j}$ 가 Reynier 가 평형전압 온도의존으로
\emph{읽어낸} 바로 그 양이다. 이 실측 분해가 본문 슬롯 규칙의 두 주장을 뒷받침한다 --- (i) O3 에서
config 가 지배(조성추세 대부분)이고, (ii) 전자항이 없으면 config 단독으로 MIT 엔트로피 거동을 못 그린다
(원 논문: MIT 서 electronic$\cdot$config 변화가 \emph{비등 중요}). 척도는 O3 상 내 변화 최대
$\approx4.2\,k_B$/atom, 전 구간 최대 $\approx9.0\,k_B$/atom 이다(★두 수치는 원문 정량 대조 확인 필요 --- 방법$\cdot$분해는 검증분).
```

**해소 근거(하이쿠 서치, §서치).** 원문 초록에서 축자 확인: "measured changes in the entropy of the lithiation reaction **as large as 9.0 k_B/atom**" · "**as large as 4.2 k_B/atom within the 'O3' layered hexagonal structure** of LixCoO2" — 값·단위(k_B/atom)·귀속(O3 내/전체) 모두 본문과 정합. 아울러 (i) "configurational entropy … account for **most** of the compositional trend"(>½ 주장 지지), (ii) "changes of the electronic and configurational entropy … **of comparable importance** for this metal--insulator transition"(비등 중요 축자), phonon 몫 "account for much of the **negative** entropy of lithiation"(음의 baseline 지지)도 초록 수준 확인.

**제안(완성 LaTeX — ★괄호만 교체)**
```latex
척도는 O3 상 내 변화 최대
$\approx4.2\,k_B$/atom, 전 구간 최대 $\approx9.0\,k_B$/atom 이다(두 수치$\cdot$단위는 원문 초록 축자
대조로 확인 --- ``as large as 4.2 [9.0] $k_B$/atom''; 방법$\cdot$분해도 검증분).
```
(0.18 k_B/atom flag(:124)는 **유지** — 초록 미등장, 본문 전문 대조 필요. 판별 산술 참고: 0.18 k_B/atom = 1.50 J/(mol K) ↔ $F^{-1}$ 환산 0.016 mV/K — 측정 가능 규모라 본문 tier B 유지와 정합.)

**근거.** RV 기지 flag 의 심화·해소 지시 이행 — 검증 경로는 §서치(하이쿠-1, ASU Pure 미러의 초록 메타데이터; APS 원문은 403). 초록 수준 확인이므로 tier 승급 판단은 마스터 몫(본 창은 근거만 제출).

---

### A19-11 (M·설명) — Sommerfeld 동결 정당화 문장의 순환 서술 해소

**파일:행** `ch1_sec15_lcoelec.tex:124-127`.

**현행(축자)**
```latex
여기서 한 가정을 명시한다 --- 표준 Sommerfeld 처방대로 상태밀도 $g(E)$ 를 그 좁은 열폭($\sim k_BT$) 안에서 $E_F$
근방의 \emph{상수} $g(E_F)$ 로 동결하며($g(E)\approx g(E_F)$), 이 동결이 정당한 까닭은 적분에 기여하는 띠가 폭
$\sim k_BT$ 로 좁고 축퇴 극한 $k_BT\!\ll\!E_F$ 에서는 그 좁은 창 안에서 $g(E)$ 의 에너지 의존이 선도 차수로
무시되는 금속 전자기체의 표준 Sommerfeld 근사이기 때문이다.
```

**문제.** "동결이 정당한 까닭은 … 표준 Sommerfeld 근사이기 때문" — 정당성의 근거로 그 근사의 이름을 되돌려주는 순환 문형. 실근거(협폭 + $g$ 완만 + 홀짝 상쇄로 첫 보정 $\mathcal O(T^3)$)는 바로 뒤 ★유효 경계·각주에 이미 있다.

**제안(완성 LaTeX)**
```latex
여기서 한 가정을 명시한다 --- 표준 Sommerfeld 처방대로 상태밀도 $g(E)$ 를 그 좁은 열폭($\sim k_BT$) 안에서 $E_F$
근방의 \emph{상수} $g(E_F)$ 로 동결한다($g(E)\approx g(E_F)$). 정당성은 두 사실에서 온다 --- 적분 기여가
폭 $\sim k_BT$ 창에 국한되고($k_BT\!\ll\!E_F$ 축퇴 극한), 그 창 안에서 $g(E)$ 의 에너지 의존이 선도
차수에서 무시된다(첫 보정이 대칭 상쇄로 $\mathcal O(T^3)$ 에서야 시작 --- ★유효 경계와 각주).
```

**근거.** 실근거를 앞당겨 비순환화 — 각주의 $\mathcal O(T^3)$ 유도(재유도 검증: $S_e=k_B^2T\!\int\!g(E_F{+}k_BT\zeta)\hat s\,\dd\zeta$ Taylor 전개에서 $g'$ 항이 $\int\zeta\hat s=0$ 으로 소거, 수치 $-9.6\times10^{-13}$)와 정합.

---

### A19-12 (M·설명) — 정공 생성 시점과 금속화 경계의 분리

**파일:행** `ch1_sec15_lcoelec.tex:19-20`.

**현행(축자)**
```latex
탈리튬화로 $x$ 가 $\sim$0.94 아래로 내려가면 Co$^{4+}$ 정공이 생겨 $t_{2g}$ 띠에 전도 전자가 열려
\emph{금속}이 된다($g(E_F)\!\to\!$유한)\cite{menetrier1999,motohashi2009}.
```

**문제.** 정공(Co⁴⁺)은 $x<1$ 이면 즉시 생긴다 — 같은 절의 bgbox 가 정확히 그 정공이 "Li 빈자리에 속박된 불순물 준위로 띠간극 안에 갇히"다가 임계 농도에서 비국소화한다고 설명한다. 0.94 는 정공 '생성' 경계가 아니라 금속화·2상 개시 경계 — 본문 두 문장이 서로 다르게 읽힌다.

**제안(완성 LaTeX)**
```latex
탈리튬화는 $x<1$ 부터 Co$^{4+}$ 정공을 심지만(희박 정공은 아래 bgbox 의 불순물 준위로 국소화),
$x$ 가 $\sim$0.94 아래로 내려가면 정공이 비국소화해 $t_{2g}$ 띠에 전도가 열려
\emph{금속}이 된다($g(E_F)\!\to\!$유한)\cite{menetrier1999,motohashi2009}.
```

**근거.** bgbox 자체 서술("탈리튬화가 만드는 정공은 … 불순물 준위로 띠간극 안에 갇히고")·Marianetti 초록 확인("for dilute Li-vacancy concentrations, the vacancy binds its hole and forms impurity states") — 본문·박스 정합화.

---

### A19-13 (L·설명) — "적분 ≈1.1 k_B … 항등"의 게이트 잔차 주석

**파일:행** `ch1_sec15_lcoelec.tex:205-208`.

**현행(축자)**
```latex
탈리튬화($x\!\downarrow$, 본 장 LCO 충전 주 진행) 시 전자 엔트로피가 방출되며, 그 방출량은 게이트가 스스로
예측하는 MIT 전 구간 적분 $\int|\partial S_e/\partial x|\,\dd x\approx1.1\,k_B$/atom(완전 metal 끝점 $S_e$ 와
항등)이고,
```

**제안(완성 LaTeX)**
```latex
탈리튬화($x\!\downarrow$, 본 장 LCO 충전 주 진행) 시 전자 엔트로피가 방출되며, 그 방출량은 게이트가 스스로
예측하는 MIT 전 구간 적분 $\int|\partial S_e/\partial x|\,\dd x\approx1.1\,k_B$/atom(완전 metal 끝점 $S_e$ 와
항등 --- 정확히는 게이트의 $x{=}1$ 잔차 $\approx5\%$ 만큼 아래: $S_e(0)-S_e(1)\approx0.95\,S_e(0)$)이고,
```

**근거.** 재계산: $1-\sigma(3)=0.0474$ → 적분 $=1.053\,k_B$ vs 끝점 $1.106\,k_B$(95.3%). 그림이 이미 "게이트 잔차 ≈5%"를 표기하므로 본문도 동기화 — '항등'은 완전 닫힘 이상화에서만 정확.

---

### A19-14 (L·수식화) — 신뢰 등급 3구성요소의 표화

**파일:행** `ch1_sec15_lcoelec.tex:160-169` (★세 구성요소의 신뢰 등급 분리 문단).

**현행(축자, 첫 문장)**
```latex
\textbf{★세 구성요소의 신뢰 등급 분리(허위 정밀 금지).}
식~\eqref{eq:Se} 를 한 등급으로 뭉개지 않도록 이를 이루는 세 구성요소 --- \emph{식의 함수형}$\cdot$\emph{끝점
anchor 값}$\cdot$\emph{조성에 따른 연속 곡선} --- 을 갈라 신뢰 등급을 따로 매긴다.
```

**제안(완성 LaTeX — 문단 말미 요약표 병기; 산문 보존)**
```latex
\begin{center}\footnotesize
\begin{tabular}{@{}llll@{}}
\hline
구성요소 & 내용 & tier & 근거 \\
\hline
함수형 & $S_e=\tfrac{\pi^2}{3}k_B^2T\,g(E_F)$ & A & 교과서 Sommerfeld(동결 $g\!\approx\!g(E_F)$) \\
끝점 anchor & $g(E_F)\!\approx\!13$ e/eV/atom ($x{=}0$) & A(한 점) & \cite{motohashi2009} \\
연속 곡선 & $g(E_F,x)$ (MIT 관통) & 없음(갭 G2) & \S\ref{sec:lco-gate} 모델 가정 $\to$ 피팅 위임 \\
\hline
\end{tabular}
\end{center}
```

**근거.** 3×(내용·tier·근거) 구조가 표에 정확히 맞고, '허위 정밀 금지' 규율(구성요소별 tier)의 기계 확인이 쉬워짐. G2 는 정직 공백으로 유지(메움 제안 아님).

---

### A19-15 (L·수식화) — sec14 ★스코프 주의의 대조 표화

**파일:행** `ch1_sec14_lcodecomp.tex:56-58`.

**현행(축자)**
```latex
★스코프 주의 --- 여기 슬롯 분해는 \emph{중심 표준값} $\Delta S^0_j$ 의 성분 나누기이고, 흑연 장의 열특성
파트(Chapter 1 Part T)가 같은 기호 $\Delta S^0_j$ 로 부르는 것은 그 \emph{전이 전체 상수}(성분 미분해)
쪽이다: 두 장을 오갈 때 성분(슬롯)과 총합(상수)을 혼동하면 이중계산이 된다.
```

**제안(완성 LaTeX — 산문 보존 + 미니표 병기)**
```latex
\begin{center}\footnotesize
\begin{tabular}{@{}lll@{}}
\hline
기호 사용처 & $\Delta S^0_j$ 의 의미 & 층위 \\
\hline
본 절(LCO 삼분해) & 성분 슬롯의 \emph{중심 표준값}(config 몫 등) & 성분(분해 후) \\
Chapter 1 Part T & 전이 \emph{전체 상수}(성분 미분해 총합) & 총합(분해 전) \\
\hline
\end{tabular}
\end{center}
```

**근거.** 같은 기호의 장 간 의미 충돌은 표 대조가 오독 방지에 가장 강함 — P3-7(명칭 혼동 방지) 정신.

<!-- FINDINGS-APPEND -->

## 검증 로그 (축별, 완료 즉시 append)

<!-- VERIFY-APPEND -->

## 서치 (하이쿠 서브에이전트 위임 — doi 실검증분만)

<!-- SEARCH-APPEND -->

## 등급별 정리

<!-- SUMMARY-APPEND -->
