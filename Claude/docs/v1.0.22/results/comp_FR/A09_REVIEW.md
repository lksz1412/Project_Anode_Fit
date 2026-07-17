# A09_REVIEW — FR-A09 심층 검토 (§8 동역학 지연 길이 L_V(N7) + §9 인과 기억 꼬리(N8))

- 검토 창: FR-A09 (v1.0.22 대공사, BRIEF_FR_A.md 준수 — **보고 전용**: 소스 무수정·git 무조작·`Codex/` 미접근)
- 대상: `Claude/docs/v1.0.22/_sections/ch1_sec08_lag.tex` (132행, 전문 정독) · `ch1_sec09_tail.tex` (245행, 전문 정독)
- 참조 원문(read-only 확인): `ch1_sec05_width.tex`(eq:bv·eq:db·eq:logisticsolve·eq:tst-box·운동방정식·eq:xieq)·`ch1_sec06_eqpeak.tex`(eq:belliden·eq:eqpeak)·`ch1_sec07_broadening.tex`(세 출처 ①·eq:widthbudget)·`ch1_sec01_n0n1.tex`(sec:notation·sec:pol·sec:pointwise·tab:notation)·`ch1_sec02b_part0.tex`(eq:mu)·`ch1_sec10_sum.tex`(전달식 수용부 5–7행)·`ch1_appA_signcheck.tex`(S5–S7·R3–R5)·`ch1v22_bib.tex`·`Anode_Fit_v1.0.22.py`(func_L_q·func_chi_d·func_dH_a_eff·_chi_and_dH_eff·_resolve_lag_length·dqdv 진행 방향 정렬)
- 4관점 전부 수행: ①내용 보완(빡세게) ②논리 오류(재계산·재유도 — §V 검증 로그) ③더 쉬운 설명 ④산문→수식 간결화
- 규율 확인: GS-1/GS-2(정직 공백)는 본 절 무관 — 메움 제안 없음. 모든 제안은 대체·보강(삭제 없음). 서지 신규 후보는 §S 후보 표로만(V1 원장 존중 — 반영 여부는 마스터 소관). P5: 기존 라벨·기호·식 번호 무변경 — 신규 라벨은 "제안" 표기.
- 상태: **최종본** (수치 검증 §V·문헌 서치 §S 통합 완료)

---

## 발견 총괄 표 (BRIEF 양식 — 현행 열은 원문 축자 부분열, 전문 축자·완성 LaTeX 는 아래 상세 절)

| ID | 파일:행 | 유형 | 등급 | 현행(축자 — 부분열) | 제안(요지) | 근거 |
|----|---------|------|------|-----------|-----------------|------|
| A09-H1 | ch1_sec08_lag.tex:27–31·89–90 | 논리 | H | `r_j^+\simeq k_0\,e^{-(\Delta G_{a,j}^\eff-\chi_d\mathcal A_j)/RT}` | eq:kuniv 의 $\mathcal A_j$(첨자형) 표기를 정리 — 기호표의 N7 정의($-\Omega_j(1-2\xi_j)$ 포함) 하에서 $\Delta G^\eff$ 와의 병용은 $\chi_d\Omega_j$ **이중계산**으로 읽히고, §8.4 는 같은 문장 안에서 괄호 $\mathcal A_j$↔지수 $\mathcal A$ 를 무언 치환 | §V-1 재유도·tab:notation·§8.3:63–65·코드 func_L_q(단일 적용) |
| A09-M1 | ch1_sec08_lag.tex:38–39 | 논리 | M | `logistic 미분 종의 $5\%$\n폭이 중심에서 $\pm z_\mathrm{cut}\,RT/F$ 규모라` | `$\pm z_\mathrm{cut}\,w_j=\pm z_\mathrm{cut}\,n_jRT/F$` — 같은 문장의 결론 $\mathcal A=z_\mathrm{cut}n_jRT$ 와 $n_j$ 정합 | §V-2: $F\cdot z_\mathrm{cut}RT/F=z_\mathrm{cut}RT\ne z_\mathrm{cut}n_jRT$ |
| A09-M2 | ch1_sec09_tail.tex:40 | 설명(오참조) | M | `하한 $-\infty$ 가 곧 \S\ref{sec:pol} 이 말한 ``자연 경계''다` | `\S\ref{sec:pointwise}` 로 정정 — "자연 경계"는 sec:pointwise 제목·본문에만 존재 | grep 전수: sec:pol(분극)에 문구 부재; `ch1_sec01_n0n1.tex:186` |
| A09-M3 | ch1_sec09_tail.tex:96–99 | 보완(비약) | M | `넣으면 각 전이의 기여는 ``평형 전환율에서\n지연의 변화율을 뺀 것''이 된다. \textbf{(d) 박스.}` | 박스 직전에 지연 ODE 의 V-축 형태 대입 1줄: $\dd\xi_j/\dd V=\dd\xi_{\eq,j}/\dd V-\dd r_j/\dd V=r_j/L_{V,j}$ | §V-3: 이 대입 없이는 박스 $r_j/L_{V,j}$ 가 유도되지 않음 |
| A09-M4 | ch1_sec08_lag.tex:109–110 | 설명+수식화 | M | `꼬리 진폭이\n용량축 $1/L_q$ 와 분모 $\dd V_n/\dd q$ 가 묶여 전압축 길이로 정리되는 것이다` | 비문 — 연쇄율 $\dd\xi_j/\dd V=(\dd\xi_j/\dd q)(\dd q/\dd V)=r_j/(L_{q,j}|\dd V/\dd q|)$ 로 대체 | §V-3 (M3 과 같은 항등) |
| A09-M5 | ch1_sec08_lag.tex:5–6·38 | 설명(용어) | M | `평형\n목표 $\xi_\eq$ 를 점유가 즉시 따라가지 못하고` · `컷은 점유 $\xi_\eq$ 자체가 아니라` | "점유"→"진행률"(2건) — §1 규약($\theta$=점유·$\xi$=진행률, P5) | `ch1_sec01_n0n1.tex:24–26` 규약 충돌 |
| A09-M6 | ch1_sec08_lag.tex:42–43 | 보완 | M | `\qquad z_\mathrm{cut}=4.357,\ A_\mathrm{cap}=4.0\ (\text{기본}).` | $A_\mathrm{cap}$ 근거 1문장(같은 컷-분율 족 $z{=}4\approx7\%$ + $n_j$ 큰 전이에서 동결 구동력 폭주로 $L_q$ 소멸 방지) | 독자 질문 미답; §V-2($\mathrm{sech}^2 2=7.07\%$) |
| A09-M7 | ch1_sec08_lag.tex:115–120 | 논리(숨은 조건) | M | `$V\!\uparrow\Rightarrow\n\mathcal A\!\uparrow\Rightarrow$ 유효 장벽$\downarrow\Rightarrow L_q\downarrow$(꼬리 짧아짐)` | 단조성 성립 조건 $\chi_d>1/(1+e^{\mathcal A/RT})\approx e^{-\mathcal A/RT}$($=0.018$ @ $4RT$) 반문장 병기 | §V-4 재계산: $\partial\ln L_q/\partial\mathcal A=-[\chi_d-\frac{1}{1+e^{\mathcal A/RT}}]/RT$ |
| A09-M8 | ch1_sec09_tail.tex:55–56 | 설명(식별 암묵) | M | `$r_j\equiv\xi_{\eq,j}-\xi_{\mathrm{lag},j}$(\S\ref{sec:lag} 의 정의)와` | §8 정의는 $r_j\equiv\xi_{\eq,j}-\xi_j$ — "$\xi_j$=이 적분값, 그것을 $\xi_\mathrm{lag}$ 로 명명" 식별 명시 | `ch1_sec08_lag.tex:12` 원 정의와 불일치 |
| A09-M9 | ch1_sec09_tail.tex:89–91 (fig:relaxode 캡션) | 논리(자구) | M | `이 차분이 평형 종의 미분으로 매끈히 수렴하는` | `평형 진행률의 미분(평형 종)으로` + 참조를 `\S\ref{sec:tail-peakshape}` 로 — "평형 종의 미분"은 2계 미분 지칭 | eq:tail-limit 극한값 $=\dd\xi_\eq/\dd V=$ 평형 종 자체 |
| A09-M10 | ch1_sec08_lag.tex:36–37 | 논리(엄밀성) | M | `컷점은 원천\n$\dd\xi_\eq/\dd q$ 가 정점의 일정 분율(약 $5\%$)로 떨어지는 좌표이고` | 컷 기준을 V-축 종 $\dd\xi_\eq/\dd V$ 로 명시(코드 구현 일치) 또는 "$|\dd V/\dd q|$ 국소 상수 근사 하 동치" 한정 | q-축 5% 점은 Jacobian 따라 이동; 코드는 스캔 없이 $\mathcal A$ 직접 설정 |
| A09-M11 | ch1_sec08_lag.tex:36 | 보완 | M | `$L_q$ 는 전이당 한 점(꼬리 컷점 $q_a$)에서 \emph{상수로 동결}된다.` | 동결의 구조적 대가 1문장: $L_q$ 상수여야 §9 적분인자가 지수 커널 합성곱으로 닫힘 | §9:11–12 유도 전체가 상수성 의존(§V-5) |
| A09-M12 | ch1_sec08_lag.tex:100–106 | 보완 | M | `\qquad T_*\equiv\frac{|I|\,h}{Q_\cell\,k_B}.` | 워크드 넘버($1$C: $T_*{\approx}1.3{\times}10^{-14}$ K, $L_q{\sim}10^{-2}$ 에 $\Delta H_a^\eff{\sim}89$ kJ/mol) + "$\Delta H_a\cdot\Delta S_a$ 는 유효(coarse-grained) 파라미터" 가드 | §V-6 수치; 스케일 감각·전제 공시 부재 |
| A09-M13 | ch1_sec08_lag.tex:38–40 | 수식화 | M | `($z_\mathrm{cut}=4.357$\n--- 이 $5\%$ 컷에 대응하는 선택값)다` | 폐형 병기: $4\xi_\eq(1-\xi_\eq)=\mathrm{sech}^2(z/2)$, $z(c)=2\,\mathrm{artanh}\sqrt{1-c}$ ($c{=}0.05\Rightarrow4.357$) | §V-2 재계산 4.3567 일치 — "선택값" 출처의 식화 |
| A09-M14 | ch1_sec09_tail.tex:169–179 | 수식화(보강) | M | (eq:reversal 두 분기 박스 — 축자는 상세 절) | 보강 remark: 통합형 $\xi_{\mathrm{lag},j}(V)=\int_0^\infty\xi_{\eq,j}(V-\sigma_dL_{V,j}t)e^{-t}\dd t$ (제안 라벨 eq:reversal-unified) — 거울성·극한·평균 지연 $=L_{V,j}$ 가 한 줄씩 | §V-7·§V-8 재유도 |
| A09-M15 | ch1_sec08_lag.tex:55–56 | 보완 | M | `\textbf{(b)(c) 방향별 선택.} 방향별 전달 계수는` | "왜 충전이 $1-\chi$ 인가" 1문장(같은 장벽을 반대쪽에서 넘으므로 정방향 분율이 여집합) + 합-1↔DB 인과 방향을 §5 와 정렬 | (b)(c) 단계가 선언만 있고 논거 부재; `ch1_sec05_width.tex:28` |
| A09-L1 | ch1_sec08_lag.tex:5 | 설명 | L | `이 절(N7--N9)은` | `이 절부터 \S\ref{sec:sum} 까지(N7--N9)는` | 단수 "이 절" vs 범위 N7–N9 |
| A09-L2 | ch1_sec08_lag.tex:24 | 설명 | L | `근본식의 세 인자가` | `운동방정식~\eqref{eq:Lqmid} 의 세 인자($|I|\cdot Q_\cell\cdot k_j$)가` | "근본식"은 `_sections` 전체에서 이 1회만 등장(정의처 부재) |
| A09-L3 | ch1_sec08_lag.tex:55–56 | 설명 | L | `($\chi+\chi'=1$, 식~\eqref{eq:db} detailed balance 가 강제)` | §5 는 역방향 서술(합-1 이 DB 를 강제) — 동치이나 인과 표기 정렬(M15 제안이 함께 해소) | `ch1_sec05_width.tex:28` |
| A09-L4 | ch1_sec08_lag.tex:74 | 설명 | L | `단, 이 보강을 적용하지 않으면 보강 없이 $\Delta H_a$ 를 그대로 쓴다.` | 동어반복 정리 + 107–109행과 중복 한쪽 정리 | 자구 |
| A09-L5 | ch1_sec08_lag.tex:122 | 설명 | L | `$I\le0$ 이거나` | `전류 입력이 비양수($I\le0$ --- 구현 가드)이거나` | $|I|$ 규약과 표면 충돌; 코드 `if I <= 0` 대응 |
| A09-L6 | ch1_sec09_tail.tex:74–79 (fig:relaxode) | 설명(그림) | L | `node[above,font=\scriptsize] {$\xi$};` (세로축; 곡선 도식 높이 2.0) | 세로축 눈금 1 표기 or 캡션 "세로 임의 눈금" 1구 — $\xi\in[0,1]$ 유계 논증과의 시각 충돌 예방 | 본문 31행 `$|r_j|<1$` 유계가 유도 하중 |
| A09-L7 | ch1_sec09_tail.tex:188–190 | 설명 | L | `충전 $\dd Q/\dd V$ 는 방전의 거울이고` | `(거울의 중심은 각 전이의 분기 중심 $U_j^{\,d}$ --- 분기 시 전곡선은 $\Delta U_j^\hys$ 만큼 어긋난 거울)` 한정 | fig:reversal 은 $U{=}0$ 단일 중심 예시; §V-8 거울 증명은 전이별 |
| A09-L8 | ch1_sec08_lag.tex:28–29 | 설명(전방참조) | L | `-\chi_d\mathcal A_j)/RT}` (eq:kuniv 내 $\chi_d\cdot{}^\eff$) | §8.3 정의 선행 사용 — `($\chi_d\cdot\Delta H^\eff$ 는 \S\ref{sec:lag-chid})` 포인터 (H1 제안에 흡수 가능) | 전방 참조 무포인터 |
| A09-L9 | ch1_sec08_lag.tex:25–26·32·66–69 | 논리(ε) | L | `괄호 인자 $(1+e^{-\mathcal A_j/RT})$ 가 역방향 몫의 전부다` | 동결·심층꼬리 근사의 ε 각주(선택): DB 괄호 이상-$\mathcal A$ 사용 오차 $L_q$ 비 $0.984$; 심층꼬리 $+\Omega$ 의 컷점 실값 $\tanh(2)\Omega=0.964\Omega$ | §V-1ε 수치 |
| A09-L10 | ch1_sec08_lag.tex:6–7 | 설명 | L | `사슬\n$\mathcal A\to\chi_d\to\Delta H_a^\eff\to L_q\to L_V$ 를` | 본문 절 순서($L_q$ 정의 선행)와 사슬 표기 정렬 반괄호 | 절 구성 순서와 불일치 |

**건수: H 1 · M 15 · L 10 (계 26)**

---

## H 등급 상세 (논리/물리 오류·오귀속) — 1건

### A09-H1 — eq:kuniv 의 $\mathcal A_j$ 표기가 기호표 정의 하에서 $\chi_d\Omega_j$ 이중계산으로 읽힘 (+ §8.4 의 무언 치환)

- 파일:행 = `ch1_sec08_lag.tex:25–33` (식 eq:kuniv) 및 `ch1_sec08_lag.tex:89–96` (§8.4 (a)–(c))
- 유형 = 논리(기호 정의 충돌 — 수식↔기호표 불일치) · 등급 = **H**
- 현행(축자, 25–33행):

```latex
$L_{q,j}$ 는 요구($|I|/Q_\cell$)와 공급($k_j$)의 비 그 자체다 --- 근본식의 세 인자가 전부 이 한 양을 통해 꼬리로
들어온다. 완화 속도 $k_j$ 는 평형 근방 선형 완화에서 정$\cdot$역 속도의 합이다 --- detailed balance~\eqref{eq:db} 로
$r_j^-=r_j^+e^{-\mathcal A_j/RT}$ 이므로
\begin{equation}
k_j=r_j^++r_j^-=r_j^+\big(1+e^{-\mathcal A_j/RT}\big),
\qquad r_j^+\simeq k_0\,e^{-(\Delta G_{a,j}^\eff-\chi_d\mathcal A_j)/RT}\ (k_0=k_BT/h),
\label{eq:kuniv}
\end{equation}
이고, 괄호 인자 $(1+e^{-\mathcal A_j/RT})$ 가 역방향 몫의 전부다($\mathcal A\gtrsim3RT$ 면 $1$로 수렴한다). 이 두 인자가
아래 $L_q$ 평가식의 분모와 forward 지수를 각각 채운다.
```

- 현행(축자, 89–90행):

```latex
\textbf{(a) 출발 --- 정$\cdot$역 합과 Eyring prefactor.} 식~\eqref{eq:kuniv} 의 $k_j=r_j^+(1+e^{-\mathcal A_j/RT})$ 와
$r_j^+\simeq k_0e^{-(\Delta G_a^\eff-\chi_d\mathcal A)/RT}$($k_0=k_BT/h$)을 식~\eqref{eq:Lq} 의 $L_{q,j}=|I|/(Q_\cell k_j)$
```

- 문제(재유도 — §V-1): 기호 마스터표(`ch1_sec01_n0n1.tex:74–76`)는 **첨자형** $\mathcal A_j$ 를 "유도용 일반 구동력 … **N7 일반형은 $-\Omega_j(1-2\xi_j)$ 가 더해짐**", **무첨자** $\mathcal A$ 를 "꼬리 컷점에 동결한 값"으로 정의하고, §8.3(63–64행)도 N7 의 $\mathcal A_j=sF(V-U_j)-\Omega_j(1-2\xi_j)$ 를 명시한다. 이 정의로 eq:kuniv 을 읽으면 심층 꼬리($-\Omega(1-2\xi)\to+\Omega$)에서 지수가
  $-(\Delta G_a-\chi_d\Omega-\chi_d\mathcal A_\text{이상}-\chi_d\Omega)/RT$
  가 되어 $\chi_d\Omega$ 가 **두 번** 빠진다 — 옳은 몫은 한 번($\Delta G^\eff$ **또는** $\mathcal A_j$ 완전형 중 한쪽)이다. §8.3(64–65행)의 "이 상수 몫은 … 장벽으로만 흡수되고 … 이중계산이 없다"는 산문 규정, 그리고 코드(`func_L_q` 에 동결 이상-$\mathcal A$ 하나 + `func_dH_a_eff` 단일 적용)와 어긋나는 것은 **eq:kuniv 의 인쇄 표기뿐**이다. 추가로 §8.4(89–90행)는 한 문장 안에서 괄호 인자에 $\mathcal A_j$, 지수에 $\mathcal A$ 를 섞어 쓴 뒤 eq:Lqmid2 부터 둘 다 무첨자로 옮긴다 — 치환 선언이 없다.
- 제안(대체 LaTeX — eq:kuniv 를 bare $\Delta G_a$ + 일반 $\mathcal A_j$ 로 통일하고, 흡수는 §8.3 이 명시 수행):

```latex
% (1) eq:kuniv 대체 — 25–33행 자리
완화 속도 $k_j$ 는 평형 근방 선형 완화에서 정$\cdot$역 속도의 합이다 --- detailed balance~\eqref{eq:db} 로
$r_j^-=r_j^+e^{-\mathcal A_j/RT}$ 이므로
\begin{equation}
k_j=r_j^++r_j^-=r_j^+\big(1+e^{-\mathcal A_j/RT}\big),
\qquad r_j^+\simeq k_0\,e^{-(\Delta G_{a,j}-\chi_d\mathcal A_j)/RT}\ (k_0=k_BT/h),
\label{eq:kuniv}
\end{equation}
이고, 괄호 인자 $(1+e^{-\mathcal A_j/RT})$ 가 역방향 몫의 전부다($\mathcal A\gtrsim3RT$ 면 $1$로 수렴한다).
$\mathcal A_j$ 의 상호작용 몫을 장벽으로 흡수해 지수를 $\Delta G_{a,j}^\eff-\chi_d\mathcal A$(동결$\cdot$이상 몫
$\mathcal A$)로 가르는 것은 \S\ref{sec:lag-chid} 가 한다 --- 이 두 인자가 아래 $L_q$ 평가식의 분모와
forward 지수를 각각 채운다.
```

```latex
% (2) §8.3 (d) 박스 직전(69행 "유효값이 된다:" 앞) — 흡수를 식 한 줄로 명시(A09-M15·산문→수식 겸용)
\begin{equation*}
\mathcal A_j^{(d)}=\sigma_d\big[sF(V_n-U_j)-\Omega_j(1-2\xi_j)\big]
\;\xrightarrow{\ \xi_j\to(1+\sigma_d)/2\ }\;
\underbrace{\mathcal A}_{\text{이상 몫 --- 컷 판정~\eqref{eq:Acut}}}\;+\;\underbrace{\Omega_j}_{\text{장벽 흡수}},
\qquad
r_j^{+}=k_0e^{-[\Delta G_{a,j}-\chi_d(\mathcal A+\Omega_j)]/RT}
=k_0e^{-[\Delta G_{a,j}^{\eff}-\chi_d\mathcal A]/RT},
\end{equation*}
```

```latex
% (3) §8.4 89–90행 대체 — 괄호·지수 기호 통일 + 동결 선언
\textbf{(a) 출발 --- 정$\cdot$역 합과 Eyring prefactor.} 식~\eqref{eq:kuniv} 의 정$\cdot$역 합을 컷 동결
값으로 평가하면 $k_j=r_j^+(1+e^{-\mathcal A/RT})$, $r_j^+\simeq k_0e^{-(\Delta G_a^\eff-\chi_d\mathcal A)/RT}$
($k_0=k_BT/h$; $\mathcal A_j\to\mathcal A$ 동결과 $\Omega$ 몫의 장벽 흡수는 \S\ref{sec:lag-cut}$\cdot$\S\ref{sec:lag-chid})
--- 이를 식~\eqref{eq:Lq} 의 $L_{q,j}=|I|/(Q_\cell k_j)$
```

- 근거: `ch1_sec01_n0n1.tex:74–76`(기호표) · `ch1_sec08_lag.tex:63–65`(이중계산 금지 산문) · `Anode_Fit_v1.0.22.py:49–51·158–161·404–447`(구현은 단일 적용 — $A=\min(z_\mathrm{cut}nRT,A_\mathrm{cap}RT)$ 하나가 괄호·지수 공용, $\Delta H^\eff$ 별도 1회) · 재유도 §V-1. **결과식 eq:Lqfull·eq:LV 및 코드는 옳다** — 결함은 eq:kuniv/§8.4 의 표기 층위이나, 마스터 기호표로 읽으면 물리 오류(이중계산)가 되는 인쇄형이라 H 로 분류.

---

## M 등급 상세 (의미·이해 실질 개선) — 15건

### A09-M1 — 컷 반폭 표기에서 $n_j$ 누락 (수식↔산문 불일치)
- 파일:행 = `ch1_sec08_lag.tex:38–39` · 유형 = 논리 · 등급 = M
- 현행(축자):

```latex
컷은 점유 $\xi_\eq$ 자체가 아니라 그 \emph{미분} $\dd\xi_\eq/\dd q$ 의 $5\%$ 기준이며, logistic 미분 종의 $5\%$
폭이 중심에서 $\pm z_\mathrm{cut}\,RT/F$ 규모라 그곳의 구동력은 $\mathcal A=z_\mathrm{cut}\,n_jRT$($z_\mathrm{cut}=4.357$
--- 이 $5\%$ 컷에 대응하는 선택값)다.
```

- 문제(재유도 — §V-2): 폭 $w_j=n_jRT/F$ 인 일반화 logistic 의 $5\%$ 점은 $V-U=\pm z_\mathrm{cut}w_j=\pm z_\mathrm{cut}n_jRT/F$ 이고, 그때 구동력이 $F\cdot z_\mathrm{cut}w_j=z_\mathrm{cut}n_jRT$ 다. 현행 "$\pm z_\mathrm{cut}RT/F$"(= $n_j{=}1$ 특수형)로는 결론의 $n_j$ 가 유도되지 않는다.
- 제안(대체 LaTeX — "점유"→"진행률" 정정(M5)도 함께 반영):

```latex
컷은 진행률 $\xi_\eq$ 자체가 아니라 그 \emph{미분}의 $5\%$ 기준이며, logistic 미분 종의 $5\%$
폭이 중심에서 $\pm z_\mathrm{cut}\,w_j=\pm z_\mathrm{cut}\,n_jRT/F$ 라 그곳의 구동력은
$\mathcal A=F\cdot z_\mathrm{cut}w_j=z_\mathrm{cut}\,n_jRT$($z_\mathrm{cut}=4.357$
--- 이 $5\%$ 컷에 대응하는 선택값)다.
```

### A09-M2 — "자연 경계" 출처 오참조 (sec:pol → sec:pointwise)
- 파일:행 = `ch1_sec09_tail.tex:40` · 유형 = 설명(오참조) · 등급 = M
- 현행(축자):

```latex
--- 하한 $-\infty$ 가 곧 \S\ref{sec:pol} 이 말한 ``자연 경계''다. \textbf{(b) 연산 --- 부분적분.}
```

- 문제: "자연 경계"는 `ch1_sec01_n0n1.tex:186` 의 소절 제목("점별 평가 원칙 --- 자연 경계가 여는 여유", `\label{sec:pointwise}`)과 그 본문(189–191행: "하한 $u\to-\infty$(방전) 또는 상한 $u\to+\infty$(충전)를 여는 적분")에만 있다. `sec:pol`(분극, N1)에는 이 문구가 없다 — 독자가 분극 소절에서 헛찾게 되는 오참조. (선례: A08-L5 의 참조 위치 정정 — 다만 본 건은 문구가 지시 소절에 아예 부재라 한 단계 무겁게 M.)
- 제안(대체 LaTeX):

```latex
--- 하한 $-\infty$ 가 곧 \S\ref{sec:pointwise} 가 말한 ``자연 경계''다. \textbf{(b) 연산 --- 부분적분.}
```

### A09-M3 — peak 모양 박스로 가는 마지막 대입(지연 ODE) 생략 (유도 비약)
- 파일:행 = `ch1_sec09_tail.tex:96–99` · 유형 = 보완 · 등급 = M
- 현행(축자):

```latex
\textbf{(a)(b)(c) 출발$\cdot$연산$\cdot$중간식.} 진행률은 어디서나 $\xi_j=\xi_{\eq,j}-r_j$ 이고(지연
$r_j$ 는 식~\eqref{eq:lag} 이 전 구간 결정), 그 미분 $\dd\xi_j/\dd V=\dd\xi_{\eq,j}/\dd V-\dd r_j/\dd V$
를 보존식 $\dd Q/\dd V=C_\bg+\sum Q_j\,\dd\xi_j/\dd V$ 에 넣으면 각 전이의 기여는 ``평형 전환율에서
지연의 변화율을 뺀 것''이 된다. \textbf{(d) 박스.}
```

- 문제(재유도 — §V-3): "평형 전환율에서 지연의 변화율을 뺀 것"에서 박스 $r_j/L_{V,j}$ 로 건너뛴다. 연결 고리는 지연 방정식~eq:Lq 의 V-축 형태 $\dd r_j/\dd V=\dd\xi_{\eq,j}/\dd V-r_j/L_{V,j}$ 를 대입해 평형 몫이 상쇄되는 한 줄인데, 이 한 줄이 없다(부호 사슬의 축이 되는 상쇄임에도).
- 제안(대체 LaTeX — "된다." 뒤에 삽입):

```latex
지연 방정식~\eqref{eq:Lq} 의 $V$-축 형태 $\dd r_j/\dd V=\dd\xi_{\eq,j}/\dd V-r_j/L_{V,j}$
(컷점 동결 기울기로 옮긴 식~\eqref{eq:LV} 의 좌표)를 대입하면 평형 몫이 정확히 상쇄되어
$\dd\xi_j/\dd V=r_j/L_{V,j}$ --- 남는 것은 지연 그 자체다. \textbf{(d) 박스.}
```

### A09-M4 — $L_q\to L_V$ 환산 문장 비문 (산문→수식 대체)
- 파일:행 = `ch1_sec08_lag.tex:109–110` · 유형 = 설명+수식화 · 등급 = M
- 현행(축자):

```latex
전압축으로 옮기면, 컷점 OCV 기울기를 곱한다 --- 꼬리 진폭이
용량축 $1/L_q$ 와 분모 $\dd V_n/\dd q$ 가 묶여 전압축 길이로 정리되는 것이다:
```

- 문제: "꼬리 진폭이 … $1/L_q$ 와 분모 $\dd V_n/\dd q$ 가 묶여"는 주어·술어가 어긋난 비문이고, 어떤 양의 분모인지 불명. 실제 내용은 연쇄율 한 줄이다.
- 제안(대체 LaTeX):

```latex
전압축으로 옮기면, 컷점 OCV 기울기를 곱한다 --- 전이 기여의 연쇄율
$\dd\xi_j/\dd V=(\dd\xi_j/\dd q)(\dd q/\dd V)=(r_j/L_{q,j})\big/\,\lvert\dd V/\dd q\rvert_{q_a}$ 에서
$1/L_{q,j}$ 와 Jacobian $\lvert\dd V/\dd q\rvert_{q_a}$ 가 한 전압축 길이로 묶이는 것이다:
```

### A09-M5 — "점유" ↔ "진행률" 용어 혼용 2건 (P5 이름 보존)
- 파일:행 = `ch1_sec08_lag.tex:5–6` 및 `:38` · 유형 = 설명(용어) · 등급 = M
- 현행(축자, 5–6행):

```latex
유한 전류에서는 평형
목표 $\xi_\eq$ 를 점유가 즉시 따라가지 못하고 뒤처진다 --- 그 지연이 peak 의 꼬리다.
```

- 문제: §1(`ch1_sec01_n0n1.tex:24–26`)이 $\theta$=점유율, $\xi$=진행률로 규약을 세웠고 §5(sec:dist)도 "점유 $\theta_\eq$ 와 진행률 $\xi_\eq$ 를 가르는 … 여집합 교환"을 명시한다. §8 의 두 곳("점유가 즉시 따라가지 못하고", "컷은 점유 $\xi_\eq$")은 $\xi$ 를 점유로 불러 규약과 충돌.
- 제안(대체 LaTeX — 5–6행분; 38행분은 A09-M1 제안에 반영됨):

```latex
유한 전류에서는 평형
목표 $\xi_\eq$ 를 진행률이 즉시 따라가지 못하고 뒤처진다 --- 그 지연이 peak 의 꼬리다.
```

### A09-M6 — $A_\mathrm{cap}=4.0$ 의 근거 문장 부재
- 파일:행 = `ch1_sec08_lag.tex:41–48` · 유형 = 보완 · 등급 = M
- 현행(축자, 46–48행):

```latex
기본 상태($n_j{=}1$)에서는 $z_\mathrm{cut}n_jRT=4.357RT>A_\mathrm{cap}RT=4.0RT$ 라 상한이 걸려 실효
컷은 $z=4.0$(정점의 약 $7\%$)이고, $5\%$ 컷 분기는 $n_j<A_\mathrm{cap}/z_\mathrm{cut}\approx0.92$ 로
피팅될 때 활성화된다.
```

- 문제: 상한이 "왜 있어야 하고 왜 $4.0$ 인가"에 답이 없다(독자 질문 미답). 물리적으로는 (i) $z{=}4$ 도 같은 컷-분율 족($\mathrm{sech}^2 2\approx7\%$ — §V-2)이고, (ii) $n_j$ 큰(넓은) 전이에서 동결 구동력 $z_\mathrm{cut}n_jRT$ 가 $n_j$ 에 비례해 자라 $e^{-\chi_d\mathcal A/RT}$ 로 $L_q$ 를 지수적으로 꺼뜨리는 폭주를 막는 안전 상한이다.
- 제안(보강 LaTeX — 48행 "활성화된다." 뒤):

```latex
상한의 지위도 컷과 같은 족이다 --- $z{=}4.0$ 은 정점의 약 $7\%$ 컷이라 ``컷 분율''의 언어 안에 있고,
$n_j$ 가 큰(넓은) 전이에서 동결 구동력이 $n_j$ 에 비례해 자라며 $e^{-\chi_d\mathcal A/RT}$ 로
$L_q$ 를 지수적으로 꺼뜨리는 폭주를 막는 안전 상한이다.
```

### A09-M7 — "$\mathcal A\!\uparrow\Rightarrow L_q\downarrow$" 단조성의 숨은 조건
- 파일:행 = `ch1_sec08_lag.tex:115–120` · 유형 = 논리(숨은 조건) · 등급 = M
- 현행(축자):

```latex
\emph{부호의 핵심} --- $\mathcal A$ 가 전이당 컷 상수로 동결되므로, \emph{실현되는} 미분은
$\partial\ln L_q/\partial V=0$ 이다(전이당 한 스칼라). 부등식 $\partial\ln L_q/\partial V<0$ 은 \emph{물리적 동기}로 읽어야
한다 --- 만일 $\mathcal A$ 를 컷에 동결하지 않고 국소 구동력 $\mathcal A=\sigma_dF(V_n-U)$ 로 두면, 방전
기준($\sigma_d=+1$; 충전은 진행 방향 $V\!\downarrow$ 를 따라 같은 단조성) $V\!\uparrow\Rightarrow
\mathcal A\!\uparrow\Rightarrow$ 유효 장벽$\downarrow\Rightarrow L_q\downarrow$(꼬리 짧아짐)이고, 이 단조성이 ``꼬리 컷점을
원천 정점의 일정 분율로 잡는다''는 컷 규칙의 정당성이다.
```

- 문제(재계산 — §V-4): $L_q\propto e^{-\chi_d\mathcal A/RT}/(1+e^{-\mathcal A/RT})$ 에서
  $\partial\ln L_q/\partial\mathcal A=-\big[\chi_d-\tfrac{1}{1+e^{\mathcal A/RT}}\big]/RT$.
  단조 하강은 $\chi_d>1/(1+e^{\mathcal A/RT})\approx e^{-\mathcal A/RT}$ 일 때만 성립한다(컷 $\mathcal A=4RT$ 에서 문턱 $0.018$). $\chi$ 는 피팅 자유라 $\chi_d=\chi$ 또는 $1-\chi$ 가 이 문턱 아래로 갈 수 있고, 그 극단에서는 역방향 몫 회복이 forward 이득을 이겨 부등식이 뒤집힌다. 같은 무조건 서술이 appendix S6·R4 에도 있다(그쪽은 본 창 대상 밖 — 지적만 이월).
- 제안(보강 LaTeX — "(꼬리 짧아짐)이고," 뒤 괄호 삽입):

```latex
(정확히는 $\partial\ln L_q/\partial\mathcal A=-\big[\chi_d-\tfrac{1}{1+e^{\mathcal A/RT}}\big]/RT$ 라
$\chi_d>1/(1+e^{\mathcal A/RT})\approx e^{-\mathcal A/RT}$ --- 컷 $\mathcal A{=}4RT$ 에서 $0.018$ ---
일 때 단조 하강이고, 기본 $\chi{=}0.5$ 는 이를 넉넉히 만족한다)
```

### A09-M8 — $\xi_{\mathrm{lag}}$ 와 §8 의 $\xi_j$ 식별이 암묵 (정의 오인용)
- 파일:행 = `ch1_sec09_tail.tex:55–56` · 유형 = 설명(식별 암묵) · 등급 = M
- 현행(축자):

```latex
\textbf{(d) 박스 --- 지연 진행률.} $r_j\equiv\xi_{\eq,j}-\xi_{\mathrm{lag},j}$(\S\ref{sec:lag} 의 정의)와
식~\eqref{eq:lag-mid} 를 나란히 두면 지연 진행률이 닫힌 적분으로 떨어진다:
```

- 문제: §8 의 실제 정의는 $r_j\equiv\xi_{\eq,j}-\xi_j$(`ch1_sec08_lag.tex:12`)이고 §9 자신도 28행에서 "$r_j=\xi_{\eq,j}-\xi_j$"로 쓴다. 현행 인용문은 §8 이 $\xi_\mathrm{lag}$ 로 정의한 것처럼 읽혀 오인용이며, $\xi_{\mathrm{lag},j}=\xi_j$(운동방정식 해의 꼬리 문맥 이름)라는 식별 자체가 어디에도 명시되지 않는다.
- 제안(대체 LaTeX):

```latex
\textbf{(d) 박스 --- 지연 진행률.} \S\ref{sec:lag} 의 정의 $r_j\equiv\xi_{\eq,j}-\xi_j$ 와
식~\eqref{eq:lag-mid} 를 나란히 두면 $\xi_j$ 가 곧 닫힌 적분으로 떨어진다 --- 이 인과 기억 적분값을
지연 진행률 $\xi_{\mathrm{lag},j}$ 로 명명한다($\xi_{\mathrm{lag},j}=\xi_j$, 운동방정식 해의 꼬리 문맥 이름):
```

### A09-M9 — fig:relaxode 캡션 "평형 종의 미분" (극한 대상 오기) + 소절 참조 모호
- 파일:행 = `ch1_sec09_tail.tex:87–92` (캡션) · 유형 = 논리(자구) · 등급 = M
- 현행(축자, 해당부):

```latex
둘의 차 $r=\xi_\eq-\xi_\mathrm{lag}$ 가 지연이고, peak 모양
$(\xi_\eq-\xi_\mathrm{lag})/L_V$(식~\eqref{eq:peakshape})는 이 차를 길이로 나눈 것이다. $L_{V,j}\to0$
에서 이 차분이 평형 종의 미분으로 매끈히 수렴하는 논증(식~\eqref{eq:tail-limit})은 본문 \S\ref{sec:tail}
다음 소절이 닫는다.
```

- 문제(재유도): eq:tail-limit 의 극한값은 $\dd\xi_{\eq}/\dd V=\xi_\eq(1-\xi_\eq)/w$ — 그 자체가 "평형 종"이다. "평형 종의 미분"은 종의 미분(2계 미분)을 지칭하게 되어 틀린 자구. 또한 "\S\ref{sec:tail} 다음 소절"은 렌더 시 "§9 다음 소절"로 읽혀 §9.2 인지 §10 인지 모호.
- 제안(대체 LaTeX):

```latex
둘의 차 $r=\xi_\eq-\xi_\mathrm{lag}$ 가 지연이고, peak 모양
$(\xi_\eq-\xi_\mathrm{lag})/L_V$(식~\eqref{eq:peakshape})는 이 차를 길이로 나눈 것이다. $L_{V,j}\to0$
에서 이 차분이 평형 진행률의 미분(평형 종)으로 매끈히 수렴하는 논증(식~\eqref{eq:tail-limit})은
\S\ref{sec:tail-peakshape} 가 닫는다.
```

### A09-M10 — 컷 정의의 좌표축(q-축 원천 vs V-축 종) 불일치
- 파일:행 = `ch1_sec08_lag.tex:36–37` · 유형 = 논리(엄밀성) · 등급 = M
- 현행(축자):

```latex
$L_q$ 는 전이당 한 점(꼬리 컷점 $q_a$)에서 \emph{상수로 동결}된다. \textbf{(a) 출발 --- 컷의 정의.} 컷점은 원천
$\dd\xi_\eq/\dd q$ 가 정점의 일정 분율(약 $5\%$)로 떨어지는 좌표이고,
```

- 문제(재유도): 컷을 용량축 원천 $\dd\xi_\eq/\dd q=(\dd\xi_\eq/\dd V)(\dd V/\dd q)$ 의 $5\%$ 로 정의하면, $\dd V/\dd q$ 가 전이 창에서 변할 때 $5\%$ 점이 Jacobian 을 따라 이동해 $z_\mathrm{cut}$ 환산(38–39행 — V-축 logistic 종 기준)과 어긋난다. 구현(`_resolve_lag_length`)은 스캔 없이 $\mathcal A=\min(z_\mathrm{cut}nRT,A_\mathrm{cap}RT)$ 를 직접 쓰므로 실질 정의는 V-축 종 기준이다.
- 제안(대체 LaTeX — 둘 중 택1; ①이 구현 일치로 권장):

```latex
% ① 정의를 V-축 종으로 명시
\textbf{(a) 출발 --- 컷의 정의.} 컷점은 종
$\dd\xi_\eq/\dd V$ 가 정점의 일정 분율(약 $5\%$)로 떨어지는 좌표이고(용량축 원천 $\dd\xi_\eq/\dd q$ 기준과는
컷점 근방에서 $|\dd V/\dd q|$ 를 상수로 보는 동결 규약~\eqref{eq:LV} 아래 같은 컷),
```

```latex
% ② 현행 유지 + 한정 반문장
컷점은 원천
$\dd\xi_\eq/\dd q$ 가 정점의 일정 분율(약 $5\%$)로 떨어지는 좌표이고($|\dd V/\dd q|$ 를 컷점 근방
상수로 보는 동결 규약 아래 V-축 종의 $5\%$ 점과 일치),
```

### A09-M11 — "상수 동결"의 구조적 필연(지수 커널 폐형) 미명시
- 파일:행 = `ch1_sec08_lag.tex:36` (연동: `ch1_sec09_tail.tex:11–12`) · 유형 = 보완 · 등급 = M
- 현행(축자, §9:11–13):

```latex
\textbf{(a) 출발 --- 1계 선형 ODE.} 지연 방정식~\eqref{eq:Lq} 는 1계 선형이라 적분인자 $e^{q/L_{q,j}}$ 로
닫힌 해를 갖는다.
```

- 문제: 적분인자가 $e^{q/L_{q,j}}$ 한 짝으로 닫히는 것은 $L_{q,j}$ 가 $q$-상수일 때뿐이다(비상수면 $\exp[\int\dd q/L_q(q)]$ — 커널이 전이당 한 스칼라가 아니게 됨). 곧 §8 의 동결은 근사 선택이 아니라 §9 폐형(지수 커널 합성곱 eq:memory·eq:lag)의 **구조 조건**인데, 이 인과가 명시돼 있지 않다("동역학 계산을 우회"라는 힌트뿐).
- 제안(보강 LaTeX — `ch1_sec08_lag.tex:36` "동결된다." 뒤):

```latex
동결은 단순화 취향이 아니라 구조 조건이다 --- $L_{q,j}$ 가 $q$-상수여야 \S\ref{sec:tail} 의 적분인자가
$e^{q/L_{q,j}}$ 한 짝으로 닫혀 기억 적분이 지수 커널 합성곱(전이당 스칼라 하나)이 된다
(비상수면 커널이 $\exp[-\!\int\!\dd q/L_q(q)]$ 로 벌어진다).
```

### A09-M12 — $T_*$ 스케일 워크드 넘버·유효 파라미터 가드 부재
- 파일:행 = `ch1_sec08_lag.tex:100–106` · 유형 = 보완 · 등급 = M
- 현행(축자, 박스식 직후 대응부 없음 — 삽입 위치 기준 106행 뒤):

```latex
L_{q,j}=\frac{T_*}{T}\,\frac{\exp\!\big[(\Delta H_{a,j}^\eff-T\Delta S_{a,j})/RT\big]}{1+e^{-\mathcal A/RT}}
\,e^{-\chi_d\mathcal A/RT},
\qquad T_*\equiv\frac{|I|\,h}{Q_\cell\,k_B}.
```

- 문제(수치 — §V-6): $1$C 에서 $T_*\approx1.33\times10^{-14}$ K, $T_*/T\approx4.5\times10^{-17}$ 이다. 곧 $L_q\sim10^{-2}$ 가 되려면 지수가 $\sim10^{16}$ 을 메꿔야 하고 $\Delta H_a^\eff\approx36RT\approx89$ kJ/mol 급이 필요하다. 이 스케일 감각이 없으면 독자는 (i) prefactor 가 천문학적으로 작은 이유, (ii) 피팅 $\Delta H_a$ 가 왜 그 크기로 나오는지 가늠할 수 없다. 아울러 $k_0=k_BT/h$ 는 **자리(미시) 시도빈도**이므로 셀 수준 완화율에 그대로 쓰는 순간 $\Delta H_a\cdot\Delta S_a$ 는 수송·조대화 몫을 흡수한 **유효 파라미터**가 된다는 가드가 본문에 없다(§5 TST 박스는 미시 기원만 담당).
- 제안(보강 LaTeX — eq:Lqfull 직후):

```latex
크기 감각 --- $1$C($|I|/Q_\cell=1/3600$ s$^{-1}$)에서 $T_*\approx1.3\times10^{-14}$ K,
$T_*/T\approx4.5\times10^{-17}$($298$ K)이라, $L_q\sim10^{-2}$(용량의 수 \%)에는
$\Delta H_{a}^\eff-T\Delta S_{a}-\chi_d\mathcal A\approx34RT$ --- $\chi_d\mathcal A{=}2RT$ 면
$\Delta H_a^\eff\approx36RT\approx89$ kJ/mol --- 이 필요하다. $k_0=k_BT/h$ 가 \emph{자리} 시도빈도인
채로 셀 수준 완화율에 쓰이므로, 여기의 $\Delta H_a\cdot\Delta S_a$ 는 수송$\cdot$조대화 몫까지 흡수한
\emph{유효}(coarse-grained) 활성화 파라미터로 읽는다.
```

### A09-M13 — $z_\mathrm{cut}=4.357$ 의 폐형 미제시 (산문→수식화)
- 파일:행 = `ch1_sec08_lag.tex:38–40` · 유형 = 수식화 · 등급 = M
- 현행(축자): A09-M1 블록과 동일(38–40행 — "이 $5\%$ 컷에 대응하는 선택값").
- 문제/이득: $4.357$ 이 어디서 오는 수인지 본문에 식이 없다. 종의 분율은 닫힌 꼴 $4\xi_\eq(1-\xi_\eq)=\mathrm{sech}^2(z/2)$ 를 따르므로 분율 $c$ 의 컷은 $z(c)=2\,\mathrm{artanh}\sqrt{1-c}$ — $c{=}0.05$ 에서 정확히 $4.3565$(§V-2), $z{=}4$ 에서 $c=\mathrm{sech}^2 2=7.07\%$. 한 식으로 $z_\mathrm{cut}$·$A_\mathrm{cap}$ 두 수의 출처가 닫힌다.
- 제안(보강 LaTeX — 각주 또는 40행 뒤 괄호):

```latex
\footnote{종의 정점 대비 분율은 $4\xi_\eq(1-\xi_\eq)=\mathrm{sech}^2(z/2)$ 로 닫히므로 분율 $c$ 의 컷은
$z(c)=2\,\mathrm{artanh}\sqrt{1-c}$ 다 --- $c=0.05\Rightarrow z_\mathrm{cut}=4.357$,
역으로 $z=A_\mathrm{cap}=4.0\Rightarrow c=\mathrm{sech}^2 2\approx7\%$.}
```

### A09-M14 — eq:reversal 두 분기의 통합형 remark (산문→수식화 보강)
- 파일:행 = `ch1_sec09_tail.tex:169–186` · 유형 = 수식화(보강 — 기존 박스 유지) · 등급 = M
- 현행(축자, 박스):

```latex
\begin{equation}
\boxed{\;
\xi_{\mathrm{lag},j}(V)=
\begin{cases}
\dfrac{1}{L_{V,j}}\displaystyle\int_{-\infty}^{V} \xi_{\eq,j}(u)\,e^{-(V-u)/L_{V,j}}\,\dd u
& \sigma_d=+1\ (\text{방전})\\[12pt]
\dfrac{1}{L_{V,j}}\displaystyle\int_{V}^{+\infty} \xi_{\eq,j}(u)\,e^{-(u-V)/L_{V,j}}\,\dd u
& \sigma_d=-1\ (\text{충전})
\end{cases}\;}
\label{eq:reversal}
\end{equation}
```

- 이득(재유도 — §V-7·§V-8): 치환 $t=|V-u|/L_{V,j}$ 로 두 분기가 한 식이 되고, (i) $\sigma_d$ 의 역할("과거의 방향 선택")이 즉시 읽히며 (ii) 충$\cdot$방전 거울성($\xi_{\eq}$ 의 중심 반사에서 두 분기 맞교환 — §V-8 수치 확인)과 (iii) $L_{V,j}\to0$ 극한(eq:tail-limit)이 각각 한 줄 검산이 된다. 커널 1차 모멘트 $\int_0^\infty te^{-t}\dd t=1$ 이므로 평균 지연이 정확히 $L_{V,j}$ 라는 해석도 공짜로 얻는다.
- 제안(보강 LaTeX — 박스 직후 181행 "된다." 뒤에 remark 로 추가; 신규 라벨은 제안 표기):

```latex
두 분기는 치환 $t=|V-u|/L_{V,j}$ 로 한 식이 된다:
\begin{equation}
\xi_{\mathrm{lag},j}(V)=\int_0^\infty \xi_{\eq,j}\big(V-\sigma_d L_{V,j}\,t\big)\,e^{-t}\,\dd t
\label{eq:reversal-unified}% (제안 라벨)
\end{equation}
--- $\sigma_d$ 는 ``과거''의 방향을 고르는 일 말고는 아무것도 하지 않는다. 이 형태에서
$L_{V,j}\to0$ 극한(식~\eqref{eq:tail-limit})과 충$\cdot$방전 거울성(중심 반사 $V\to2U_j^{\,d}-V$ 에서
두 분기가 맞교환)이 각각 한 줄 검산이 되고, $\int_0^\infty t\,e^{-t}\dd t=1$ 이라 평균 지연은
정확히 $L_{V,j}$ 다.
```

### A09-M15 — eq:chid "(b)(c) 방향별 선택"의 논거 문장 부재
- 파일:행 = `ch1_sec08_lag.tex:55–61` · 유형 = 보완 · 등급 = M
- 현행(축자):

```latex
\textbf{(a) 출발 --- 합-1 제약.} 전이상태가 정$\cdot$역 장벽을 비대칭으로 가르는 분율 $\chi\in[0,1]$ 의 합-1 제약
($\chi+\chi'=1$, 식~\eqref{eq:db} detailed balance 가 강제)에서, \textbf{(b)(c) 방향별 선택.} 방향별 전달 계수는
```

- 문제: (b)(c) 단계가 케이스 식 선언뿐 — "왜 충전이 $1-\chi$ 인가"의 물리 한 문장(같은 장벽을 반대쪽에서 넘으므로 정방향이 받는 분율이 여집합으로 뒤집힘)이 없다. 아울러 "eq:db 가 강제"는 §5(28행: "합-1 제약이 강제한 결과" — 합-1→DB)와 인과 방향이 반대로 적혀 있다(동치라 오류는 아니나 정렬 — A09-L3).
- 제안(대체 LaTeX):

```latex
\textbf{(a) 출발 --- 합-1 제약.} 전이상태가 정$\cdot$역 장벽을 비대칭으로 가르는 분율 $\chi\in[0,1]$ 의 합-1 제약
($\chi+\chi'=1$ --- 이 분할이 detailed balance~\eqref{eq:db} 를 담보한다)에서, \textbf{(b)(c) 방향별 선택.}
충전은 같은 장벽을 반대쪽에서 넘으므로 \emph{정방향}이 구동력에서 받는 분율이 여집합으로 뒤집힌다 ---
방향별 전달 계수는
```

---

## L 등급 상세 (문체·표시) — 10건

### A09-L1 — "이 절(N7--N9)" 단복수 불일치
- `ch1_sec08_lag.tex:5` · 현행(축자): `이 절(N7--N9)은 \S\ref{sec:broadening} 세 출처 중 ①(유한율속 비대칭 꼬리)에 대한 답이다.`
- 제안: `이 절부터 \S\ref{sec:sum} 까지(N7--N9)는 \S\ref{sec:broadening} 세 출처 중 ①(유한율속 비대칭 꼬리)에 대한 답이다.`

### A09-L2 — "근본식" 지칭 대상 부재
- `ch1_sec08_lag.tex:24` · 현행(축자): `$L_{q,j}$ 는 요구($|I|/Q_\cell$)와 공급($k_j$)의 비 그 자체다 --- 근본식의 세 인자가 전부 이 한 양을 통해 꼬리로` (다음 행 `들어온다.`)
- 문제: "근본식"은 `_sections` 전체에서 이 1회만 등장 — 무엇을 가리키는지 정의처가 없다(의도는 운동방정식의 세 물리 인자 $|I|\cdot Q_\cell\cdot k_j$ 로 보임).
- 제안: `--- 운동방정식~\eqref{eq:Lqmid} 의 세 인자($|I|\cdot Q_\cell\cdot k_j$)가 전부 이 한 양을 통해 꼬리로 들어온다.`

### A09-L3 — 합-1↔detailed balance 인과 방향 표기 (§5 와 정렬)
- `ch1_sec08_lag.tex:55–56` · 현행(축자): `($\chi+\chi'=1$, 식~\eqref{eq:db} detailed balance 가 강제)` — §5:28 은 `($\chi+(1-\chi)=1$ 합-1 제약이 강제한 결과)` 로 역방향. 동치이나 두 절이 화살표를 반대로 그린다.
- 제안: A09-M15 의 대체문("이 분할이 detailed balance~\eqref{eq:db} 를 담보한다")이 함께 해소.

### A09-L4 — 동어반복 문장 + 107–109행과 중복
- `ch1_sec08_lag.tex:74` · 현행(축자): `단, 이 보강을 적용하지 않으면 보강 없이 $\Delta H_a$ 를 그대로 쓴다.`
- 제안: `이 흡수 보강은 선택 사양이다 --- 끄면 $\Delta H_{a,j}^\eff=\Delta H_{a,j}$ 로 둔다(구현 스위치 use\_dH\_eff).` (107–109행의 "암묵 전제 명시"와 이중 서술이므로 한쪽은 참조로 축약 권장 — 삭제 아님, 축약 대체.)

### A09-L5 — "$I\le0$" 표기와 $|I|$ 규약의 표면 충돌
- `ch1_sec08_lag.tex:122` · 현행(축자): `그 값을 쓰고, $I\le0$ 이거나 활성화 엔탈피 입력이 없거나 컷점 OCV 기울기 $|\dd V/\dd q|_{q_a}$ 가`
- 제안: `그 값을 쓰고, 전류 입력이 비양수($I\le0$ --- 구현 가드)이거나 활성화 엔탈피 입력이 없거나 컷점 OCV 기울기 $|\dd V/\dd q|_{q_a}$ 가` (본문 전역이 $|I|$ 크기 규약인데 이 한 곳만 부호 있는 $I$ — 구현 가드임을 밝히면 충돌 해소. 코드 `_resolve_lag_length: if I <= 0 … return 0.0` 대응.)

### A09-L6 — fig:relaxode 세로축 눈금 부재 (곡선 도식 높이 2.0)
- `ch1_sec09_tail.tex:74–79` · 현행(축자, 축·곡선 선언부):

```latex
\draw[-{Latex[length=1.4mm]}] (-0.1,0) -- (-0.1,2.4) node[above,font=\scriptsize] {$\xi$};
% target xi_eq: smooth rising sigmoid to 2
\draw[densely dashed,thick] plot[smooth] coordinates {(0,0.10) (0.3,0.18) (0.6,0.36) (0.9,0.74) (1.2,1.24) (1.5,1.62) (1.8,1.82) (2.1,1.92) (2.4,1.96) (2.7,1.98) (3.0,1.99) (3.3,2.0)};
```

- 문제: 눈금이 없어 문면상 틀리진 않으나, $\xi$ 축 곡선이 도식 높이 $2.0$ 까지 오르는 그림은 본문이 유도 하중으로 쓰는 유계 $0<\xi_\eq<1\cdot|r_j|<1$(§9:31·49행)과 시각적으로 부딪힐 여지가 있다.
- 제안(택1): ① 축에 눈금 1 표기(`\draw (-0.14,2.0)--(-0.06,2.0) node[left,font=\scriptsize]{$1$};` — $y{=}2.0$ 을 $\xi{=}1$ 로 캘리브레이션) ② 캡션 말미 "(좌표는 기억 적분의 도식 평가다.)" 를 "(좌표는 기억 적분의 도식 평가 --- 세로는 임의 눈금이다.)" 로.

### A09-L7 — "충전은 방전의 거울" 의 중심 한정
- `ch1_sec09_tail.tex:188–190` · 현행(축자): `\emph{부호 결과} ---\n충전 $\dd Q/\dd V$ 는 방전의 거울이고, 꼬리는 진행상 나중에 지나는 전위 쪽으로 늘어진다(방전은 높은\n$V$, 충전은 낮은 $V$ 쪽으로).`
- 제안: `(방전은 높은 $V$, 충전은 낮은 $V$ 쪽으로; 거울의 중심은 각 전이의 분기 중심 $U_j^{\,d}$ --- 분기($\gamma_j\ne0$)면 충$\cdot$방전 곡선 전체는 $\Delta U_j^\hys$ 만큼 어긋난 거울이다).` — fig:reversal 은 $U{=}0$ 단일 중심 예시라 히스 분기 시 오독 예방(§V-8 거울 증명은 전이별 중심 반사).

### A09-L8 — eq:kuniv 의 $\chi_d\cdot\Delta G^\eff$ 전방 사용 무포인터
- `ch1_sec08_lag.tex:28–29` · 현행: eq:kuniv 이 $\chi_d$(정의 §8.3 eq:chid)·$\Delta G^\eff$(갈라 적기 §8.4) 를 정의 전에 사용.
- 제안: A09-H1 대체안 채택 시 자동 해소(bare $\Delta G_a$ + "$\S\ref{sec:lag-chid}$ 가 한다" 포인터 포함). 현행 유지 시 최소한 `($\chi_d$ 는 \S\ref{sec:lag-chid}, 갈라 적기는 \S\ref{sec:lag-LV})` 괄호 추가.

### A09-L9 — 동결·심층꼬리 근사의 ε 미공시 (선택 각주)
- `ch1_sec08_lag.tex:25–26·32·66–69` · 현행(축자, 32행): `이고, 괄호 인자 $(1+e^{-\mathcal A_j/RT})$ 가 역방향 몫의 전부다($\mathcal A\gtrsim3RT$ 면 $1$로 수렴한다).`
- 내용(수치 — §V-1ε): (i) 엄밀 DB 는 상호작용 몫까지 실은 전체 구동력 기준 — 이상-$\mathcal A$ 사용의 오차는 괄호 안 미소량($\Omega{=}2RT$ 예: $1.018\to1.002$, $L_q$ 비 $0.984$). (ii) 심층꼬리 상수 몫 $+\Omega$ 의 컷점 실값은 $\tanh(2)\,\Omega=0.964\,\Omega$($3.6\%$ 차). 모두 동결 규약의 ε 이며 결론 불변 — 공시용 각주 1개면 족하다.
- 제안(각주): `\footnote{동결 규약의 ε --- 엄밀한 detailed balance 는 상호작용 몫까지 실은 전체 구동력 기준이나 컷($\mathcal A{=}4RT$)에서 그 차이는 괄호 인자 안 미소량이고($L_q$ 비 $0.984$, $\Omega{=}2RT$ 예), 심층꼬리 몫 $+\Omega$ 의 컷점 실값도 $\tanh(2)\,\Omega=0.964\,\Omega$ 다 --- 모두 결론 불변.}`

### A09-L10 — 도입 사슬 순서와 절 구성 순서 불일치
- `ch1_sec08_lag.tex:6–7` · 현행(축자): `이 절은 그 지연을 전이당 하나의 길이 $L_{V,j}$ 로 닫는다 --- 사슬\n$\mathcal A\to\chi_d\to\Delta H_a^\eff\to L_q\to L_V$ 를, 운동방정식의 보편형에서 한 단계씩 닫는다.`
- 문제: 실제 절 순서는 $L_q$(정의, §8.1)→$\mathcal A$(§8.2)→$\chi_d\cdot\Delta H^\eff$(§8.3)→$L_q$(평가)$\to L_V$(§8.4).
- 제안: `--- 사슬 $\mathcal A\to\chi_d\to\Delta H_a^\eff\to L_q\to L_V$ 를, 운동방정식의 보편형($L_q$ 의 정의 --- \S\ref{sec:lag-Lq} 선행)에서 한 단계씩 닫는다.`

---

## §V 검증 로그 (재계산·재유도 — 스크립트 `scratchpad/a09_verify.py`, numpy 수치적분 $t\in[0,60]$, $6\times10^5$ 분점)

- **V-1 (H1 재유도).** 기호표의 N7 $\mathcal A_j$(= $sF(V-U_j)-\Omega_j(1-2\xi_j)$)로 eq:kuniv 을 읽으면 심층꼬리에서 지수 $-(\Delta G_a-2\chi_d\Omega-\chi_d\mathcal A_\text{이상})/RT$ — $\chi_d\Omega$ 2회 차감. 옳은 짝은 (bare $\Delta G_a$, 완전 $\mathcal A_j$) 또는 ($\Delta G^\eff$, 동결 이상 $\mathcal A$) 뿐. 코드 `func_L_q(T,I,Q_cell,dH_a_use,dS_a,chi_d,A)` 는 후자 — 단일 적용 확인.
  - V-1ε: $2\xi-1|_{z=4}=\tanh 2=0.9640$(심층꼬리 $+\Omega$ 대비 $-3.6\%$); DB 괄호 이상 vs 완전($\Omega{=}2RT$): $1.01832$ vs $1.00248$, $L_q$ 비 $0.98445$.
- **V-2 (컷 수치).** $z_\mathrm{cut}=2\,\mathrm{artanh}\sqrt{0.95}=4.35654$ (본문 $4.357$ ✓); $z{=}4$ 분율 $=\mathrm{sech}^2 2=7.065\%$ (본문 "약 $7\%$" ✓); $5\%$ 분기 문턱 $n_j<4.0/4.3565=0.9182$ (본문 $\approx0.92$ ✓). 폭 $w_j$ 일반화 시 반폭은 $z_\mathrm{cut}w_j$ — 본문 38행의 $\pm z_\mathrm{cut}RT/F$ 는 $n_j$ 누락(M1).
- **V-3 (사슬 항등).** $\dd\xi/\dd t=k(\xi_\eq-\xi)$ ÷ $\dd q/\dd t=|I|/Q_\cell$ → eq:Lqmid → eq:Lq($L_q=|I|/Q_\cell k$) ✓. $k=r^+(1+e^{-\mathcal A/RT})$, $r^+=k_0e^{-(\Delta G^\eff-\chi_d\mathcal A)/RT}$ 대입 → eq:Lqmid2 → 앞 인자 $T_*/T$ 분리 → eq:Lqfull ✓(차원: $[|I|/Q_\cell]=1/$s, $[h/k_BT]=$s — 무차원 ✓). V-축: $\dd r/\dd V=\dd\xi_\eq/\dd V-r/L_V$ 대입 시 $\dd\xi_j/\dd V=r/L_V$ — eq:peakshape 박스 ✓ (이 대입 한 줄이 본문 §9:96–99 에 생략 — M3·M4).
- **V-4 (단조성 조건).** $\partial\ln L_q/\partial(\mathcal A/RT)=-\chi_d+1/(1+e^{\mathcal A/RT})$; $\mathcal A=4RT$ 에서 $1/(1+e^4)=0.01799$ — $\chi_d>0.018$ 필요(M7). 기본 $\chi=0.5$ 는 충족.
- **V-5 (평형 극한).** eq:tail-limit-sub 치환 재유도 ✓(constant $\int_0^\infty e^{-t}\dd t=1$); 차분 경로($[\xi_\eq(V)-\xi_\eq(V\mp Lt)]/L\to\pm t\,\dd\xi_\eq/\dd V$, $\int_0^\infty te^{-t}\dd t=1$)와 합치 ✓. DCT 전제 3종(점별수렴·연속·지배함수 $e^{-t}/(4w)$ 적분가능) ✓. 수치: $L{=}0.01$ 에서 $P(0)=0.24999\to0.25$ ✓. 충전 분기 극한 $=-\dd\xi_\eq/\dd V=+\xi_\eq(1-\xi_\eq)/w$ ✓("같은 양의 종·$\sigma_d$ 불변" 본문 주장 ✓).
- **V-6 ($T_*$ 스케일).** $T_*(1\mathrm C)=(1/3600)h/k_B=1.333\times10^{-14}$ K; $T_*/T=4.47\times10^{-17}$; $L_q=0.02$·$\Delta S_a{=}0$·$\chi_d\mathcal A{=}2RT$ 역산 $\Delta H^\eff=35.75\,RT=88.6$ kJ/mol (M12 워크드 넘버).
- **V-7 (fig:reversal 방전 곡선 전수 재계산).** $P(V)=\int_0^\infty e^{-t}\,\xi_\eq(1-\xi_\eq)|_{V-1.5t}\,\dd t$($w{=}1$)를 그림의 방전 좌표 23점 전부와 대조 — **최대 편차 $4.8\times10^{-5}$**. 정점 재탐색: $V^*=1.012$, $P^*=0.19551$ — 캡션 $({+}1.01w,\,0.196)$·주석 $0.1955$ ✓. "GENUINE numeric" 선언이 사실임을 확인.
- **V-8 (충전 분기·거울).** eq:reversal 하단 분기를 $q$-영역 해 $r(q)=\int_{-\infty}^{q}e^{-(q-q')/L_q}\dd\xi_\eq$ 에서 독립 재유도(변수 치환 + 부분적분, 경계항 $u{=}V$: $\xi_\eq(V)$·$u\to+\infty$: $0$) — 본문 (c) 서술과 일치 ✓. 해석적 거울성 $r_c(V)=r_d(2U-V)$ 증명 ✓ + 수치: $P_\mathrm{chg}(-1.0)=0.19550=P_\mathrm{dis}(+1.0)$, $P_\mathrm{chg}(0)=0.16473=P_\mathrm{dis}(0)$, $P_\mathrm{chg}(2.4)=0.03254=P_\mathrm{dis}(-2.4)$ ✓. 충전 $r\ge0$(과거 $u>V$ 에서 $\xi_\eq(u)\le\xi_\eq(V)$ — 가중평균 논거) ✓. 커널 1차 모멘트 $=1$(평균 지연 $=L_V$) ✓.
- **V-9 (코드 정합).** `Anode_Fit_v1.0.22.py`: 기본값 `z_cut=4.357`·`A_cap_RT=4.0`·`use_dH_eff=True`; $\mathcal A=\min(z_\mathrm{cut}|n|RT,\,A_\mathrm{cap}RT)$; 가드(`I<=0`·`dH_a is None`·`dVdq_qa` 기본 $0\Rightarrow L_V{=}0$·`L_V` 직접 지정 우회); 충전은 진행 방향 재정렬(`order[::-1]`) 후 인과 적분 — 본문 §8:120–123·§9 eq:reversal 서술과 전부 일치. 본문 51–52행("$\sigma_d$ 를 $\min$ 안에 넣으면 충전에서 상한이 음수")은 코드 주석의 "원본 버그 정정" 이력과 부합.

---

## §S 문헌 서치 (haiku 서브에이전트 — Crossref API 검증분만; 기억 서지 배제)

서브에이전트가 Crossref(`api.crossref.org/works/<doi>`)로 서지 전항 일치를 확인한 후보 7건. **반영 여부는 마스터·V1 원장 소관 — 아래는 후보 표일 뿐이다.** 검증은 서지 층위(제목·저자·저널·연도·DOI)까지이며 본문 내용 정독은 미수행(tier 배정 불가 — 전부 "후보").

| # | 서지 (저자, 제목, 저널, 연도) | DOI | 검증 방법 | 대응 주장 | 본 창 소견 |
|---|---|---|---|---|---|
| 1 | Fly & Chen, "Rate dependency of incremental capacity analysis (dQ/dV) as a diagnostic tool for lithium-ion batteries", *J. Energy Storage* 29, 101329 (2020) | 10.1016/j.est.2020.101329 | Crossref 전항 일치 | ①(율속 꼬리) | **기존 인용과 동일** — `ch1v22_bib.tex:26` fly2020(동일 DOI). 신규 아님 — §7 에서 이미 ① 근거로 사용 중. §8–§9 에 문헌 추가가 꼭 필요하지는 않음을 방증 |
| 2 | Bharathraj, Adiga, Mayya, "An exact solution for rest-period voltage relaxation in Li-ion batteries…", *iScience* 28(11), 113769 (2025) | 10.1016/j.isci.2025.113769 | Crossref 전항 일치 | (b)(1차 완화) | rest 완화 폐형해 — eq:memory 류 1계 완화 맥락 후보(간접) |
| 3 | Fernando, Kuipers, Angenendt, Kairies, Dubarry, "Voltage relaxation characterization methods in lithium-ion batteries", *Measurement: Energy* 3, 100013 (2024) | 10.1016/j.meaene.2024.100013 | Crossref 전항 일치 | (b) | 전압 완화 특성화 방법론 — §8 완화율 담론의 측정 대응 후보 |
| 4 | Kato, Kobayashi, Miyashiro, "Differential voltage curve analysis of a lithium-ion battery during discharge", *J. Power Sources* 398, 49–54 (2018) | 10.1016/j.jpowsour.2018.07.043 | Crossref 전항 일치 | ①(DVA 비대칭) | 방전 중 DVA peak 이동·비대칭 관측 후보 — §9 꼬리 방향 실측 대응으로 유망 |
| 5 | Hosen 외, "Impact of relaxation time on electrochemical impedance spectroscopy characterization…", *World Electr. Veh. J.* 12(2), 77 (2021) | 10.3390/wevj12020077 | Crossref 전항 일치 | (b)(간접) | EIS rest-time 논문 — 본 절과의 적합도 낮음, **제외 권고** |
| 6 | Bloom 외, "Differential voltage analyses of high-power, lithium-ion cells", *J. Power Sources* 139, 295–303 (2005) | 10.1016/j.jpowsour.2004.07.021 | Crossref 전항 일치 | ①(DVA 고전) | DVA 원류 — 배경 인용 후보(직접 근거는 아님) |
| 7 | Olson, López, Dickinson, "Differential Analysis of Galvanostatic Cycle Data from Li-Ion Batteries: Interpretative Insights and Graphical Heuristics", *Chem. Mater.* 35(4), 1487–1513 (2023) | 10.1021/acs.chemmater.2c01976 | Crossref 전항 일치 | ①(해석 리뷰) | dQ/dV·dV/dQ 해석 리뷰 — 유한율속 왜곡 판독 문맥으로 **최유망 후보** |
| — | (탈락) | — | 검증 실패분 없음(서브에이전트 보고) | — | — |

소견: §8–§9 는 자족 유도 절이라 신규 인용이 필수는 아니며(① 의 문헌 근거는 §7 의 fly2020 이 이미 담당), 굳이 보강한다면 #7(해석 리뷰)·#4(방전 DVA 비대칭 실측) 2건이 §9 의 "꼬리는 진행상 나중에 지나는 전위 쪽" 실측 대응 각주 후보다. #2·#3·#5 는 적합도 낮음(완화 일반론) — 채택 비권고.

---

## 4-tier 정리 (feedback_confirmed_items_policy)

- **확정(재계산·원문 대조로 입증):** H1(기호표-수식 충돌 재유도 §V-1 + 코드 대조), M1(§V-2), M2(grep 전수 — 문구 부재), M3·M4(§V-3 항등), M7(§V-4 미분 재계산), M8(원문 정의 대조), M9(극한 대상 — eq:tail-limit 자체), L2(grep 전수). 수치 검증 통과 항목(그림 좌표·정점·거울·극한·컷 상수)도 확정.
- **추정(합리적 판단·개선 제안 성격):** M5·M6·M10·M11·M12·M13·M14·M15, L1·L3–L10 — 오류 단정이 아니라 이해·엄밀성·공시 개선이며 채택은 저자 판단.
- **미검증:** (i) PDF 렌더 층(참조 번호의 실제 표시 — 소스 라벨 층위만 검증), (ii) fig:relaxode 의 lagged 곡선 좌표 정밀도(캡션이 "도식 평가"로 선언 — 검증 불요 판단), (iii) §S 후보 문헌의 본문 내용 적합성(서지 검증까지만 — 내용 정독 미수행), (iv) appA S6·R4 의 동일 숨은 조건(M7)은 본 창 대상 밖이라 지적만 이월.

## 무발견 축 (검토했으나 문제 없음)

- **부호 사슬(②논리 핵심):** eq:Lqmid→eq:Lq→eq:Lqmid2→eq:Lqfull→eq:LV 전 단계 재유도 일치(차원 포함). §8.3 심층꼬리 부호(방전 $\xi\to1$·충전 $\xi\to0$ 에서 상호작용 몫 공히 $+\Omega$) 재유도 일치. eq:chid·eq:dHeff·방향표($\chi{=}0.5$ 합류) 일치.
- **§9 유도 전체:** 적분인자(eq:intfactor)·일반해(eq:memory)·$q_0\to-\infty$ 소멸 논거·부분적분 경계항(eq:lag-byparts)·커널 규격화·치환(eq:tail-limit-sub)·지배수렴(전제 3종)·eq:tail-limit — 전부 독립 재유도로 확인. 충전 분기(eq:reversal)를 $q$-영역 해에서 독립 재유도 — 본문과 일치. $r_j\ge0$ 양방향 논거 성립.
- **그림 수치(②):** fig:reversal "GENUINE numeric" 좌표 23점 전수 재계산 — 최대 편차 $5\times10^{-5}$, 정점 $(\pm1.01w, 0.1955)$·거울성·평형 종 좌표 모두 정확.
- **P3 관련:** P3-2(전하 보존식 중심 유지 — §9:98 보존식 경유 ✓)·P3-3(신규 순환 의존 없음 — 꼬리 사슬은 $\xi_\eq\to r\to$peak 의 feed-forward ✓)·P3-6(전달식 — eq:peakshape·eq:tail-limit 이 §10:5–7 수용부와 정합 ✓)·P3-7(본 두 절에 ver.N 표기 없음 ✓). $V_n$ 위계(P3-1)는 §5 의 "평가 전위는 $V_n$" 선언 아래 전장 공통 약기 $V$ 사용 — 본 절 고유 결함 아님(§8:117 은 $V_n$ 명기 ✓).
- **코드 정합(§V-9):** 기본값·가드·우회·방향 처리 전부 본문 서술과 일치 — 텍스트↔구현 불일치는 H1 의 eq:kuniv 표기 층위 하나뿐.
- **eq:Acut 크기·방향 분리 설계**("$\sigma_d$ 를 $\min$ 안에 넣으면 음수 상한" 논거)와 **$|I|\to0$ 환원 사슬**($L_q\propto|I|$·R3·eq:tail-limit)— 자기일관 확인.

## 결론 한 줄

부호·유도·수치는 견고하다(그림 좌표까지 전수 재현) — 결함은 eq:kuniv 한 곳의 기호 층위(H1: 기호표 정의로 읽으면 $\chi_d\Omega$ 이중계산)와, 컷 반폭 $n_j$ 누락(M1)·오참조(M2)·유도 마지막 대입 생략(M3) 등 이해·정합 층위에 몰려 있고, 전부 국소 자구·1줄 보강으로 닫힌다.
