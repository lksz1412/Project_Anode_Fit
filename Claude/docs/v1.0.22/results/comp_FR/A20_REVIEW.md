# A20_REVIEW — v1.0.22 심층 검토 FR-A20 (신 Ch2 §2.6 lcopeak + §2.7 msmr)

- 대상: `Claude/docs/v1.0.22/_sections/ch1_sec16_lcopeak.tex`(§2.6, 68행) + `ch1_sec17_msmr.tex`(§2.7, 177행)
- 검토 창: FR-A20 (보고 전용 — 본문 무수정). 4관점(보완/논리/설명/수식화) 전부 적용.
- 최중요 지시 항목: 흑연 골격 xr 수신의 정확성 · 재모수화 대수(eq:br-msmr-1/eq:lco-msmrmap) · msmr 계보 다리(srcbox) · eq:lco-xmap.
- 검증 방법: 참조 라벨 전수 역추적(Ch1 xr 5종 + Ch2 로컬 전건 원문 대조) · 전 수식 재유도/재계산(아래 무발견 축에 명세) · 코드(`Anode_Fit_v1.0.22.py`) 동결 근사 구현 대조 · comp_R3 다리 원안(`br_msmr_lineage.tex`) 축자 대조 · 서지는 하이쿠 서브에이전트 검증(§서치).
- 상태: **본판 v2 (서치 절 통합 완료)**.

---

## 0. 발견 색인 (등급순)

| ID | 파일:행 | 유형 | 등급 | 요지 |
|---|---|---|---|---|
| A20-H1 | ch1_sec16_lcopeak.tex:62–66 | 논리 | H | T1 온도 신호의 방향 서술 오류 — "이동률이 T 에 선형으로 **커지는**" ↔ 실제는 $a_e<0$ 라 선형으로 **내려감**(§2.5 자기 신호 서술 "고온 외삽이 선형 외삽보다 낮아지는"과 상충) |
| A20-M1 | ch1_sec17_msmr.tex:52–53 | 논리(참조 오귀속) | M | srcbox 내 "(본문 §17.1(c))" — v1.0.21 구 번호 하드코딩. 신 Ch2 에선 §2.7.1 로 컴파일되어 존재하지 않는 절 번호가 인쇄됨 → `\S\ref{sec:lco-code-msmr}(c)` 로 |
| A20-M2 | ch1_sec17_msmr.tex:150–154 | 보완 | M | $x_\mathrm{center}$ 기호가 본문 어디에도 미정의(코드 dict 키 `'x_center'` 로만 존재) — 정의 괄호 필요 |
| A20-M3 | ch1_sec17_msmr.tex:154–156 | 보완 | M | 고정점 순환의 셋째 호($U_1$ 이 다시 $x$ 를 참조) 누락 — 순환 서술이 사슬 2/3 에서 끊김 (P3-3 순환 의존 표시 의무 관련) |
| A20-M4 | ch1_sec16_lcopeak.tex:53–55 | 논리(과대 주장) | M | "분기 gap 도 흑연보다 키운다" — 비교 우위는 $\Omega_j^\mathrm{cat}>\Omega_j^\mathrm{graphite}$ 조건부(문서 자신이 $\Omega^\mathrm{cat}$ 미배정 선언). 단조성 $\dd\Delta U^{\hys}/\dd\Omega=2u/F>0$ 을 명기하면 조건부로 정확해짐 |
| A20-M5 | ch1_sec17_msmr.tex:55–61 | 보완 | M | srcbox 가정 차 목록에 배경항 부재(순정 MSMR 엔 $Q_\bg$/$C_\bg$ 대응물 없음) 미기재 |
| A20-M6 | ch1_sec17_msmr.tex:131–137 | 보완 | M | eq:lco-SeV 의 $z_e$ 는 매핑 포화로 $[-2.0,+1.8]$ 유계 — 전자항이 "창 밖 $\approx0$" 로 죽지 않고 골의 42–49% 로 잔존(곡선엔 무해하나 §2.5 의 "창 밖 $\approx0$" 서술과 좌표계가 달라 독자 질문 예상) |
| A20-M7 | ch1_sec17_msmr.tex:103–110 | 설명 | M | eq:lco-msmrpeak 의 $\omega_j$ 가 재모수화(전압 차원) 읽기임이 "$|f|=1$" 한 마디에만 실림 — 원계열 무차원 $\omega_j$ 로 읽으면 차원이 어긋나는 함정 명시 필요 |
| A20-M8 | ch1_sec17_msmr.tex:155–159 | 보완 | M | 고정점 1회 갱신의 수축 근거 부재 — 루프 이득 상한 $\lesssim0.2<1$ 한 줄 보강 가능(수렴의 수치 확인 위임 문장은 유지) |
| A20-M9 | ch1_sec17_msmr.tex:150–154 | 수식화 | M | 동결(현행) vs 정밀형 대비가 긴 산문+중첩 괄호 — 3행 소표로 간결화 가능 |
| A20-L1 | ch1_sec17_msmr.tex:18–22 | 설명 | L | 재모수화 문장 1문 4중 괄호 — 2문 분할 재서술안 |
| A20-L2 | ch1_sec16_lcopeak.tex:10–15 | 설명 | L | eq:lco-charge 합 지표 혼용($j\in\mathcal J_\mathrm{LCO}$ ↔ $\sum_{j=1}^{3}$) — eq:lco-J 로 동치이나 통일 여지 |
| A20-L3 | ch1_sec16_lcopeak.tex:8–15 | 보완 | L | §2.6 전체가 전위를 $V$ 로 적음 — 흑연 골격의 "평가 전위 $=V_n$" 규정(eq:xieq 아래) 수신을 한 줄 명시하면 P3-1(V 위계) 가드 강화 |
| A20-L4 | ch1_sec17_msmr.tex:92–95 | 보완 | L | 계수비교가 1차 계수만 언급 — 상수항 비교가 $U_j^0=U_j^{\,d}$(중심 슬롯 대응)도 함께 고정함을 한 줄 보완 |
| A20-L5 | ch1_sec17_msmr.tex:46–51 | 설명 | L | eq:br-msmr-1 화살표 아래첨자 "$\omega_j\mapsto w_j=n_jRT/F$" — 본문 규정은 $\omega_jRT/F$(와 $n_j\leftrightarrow\omega_j$ 동일시). $\omega_jRT/F$ 로 적으면 자기완결 |
| A20-L6 | ch1_sec16_lcopeak.tex:42–49 | 보완 | L | eq:lco-eqpeak 의 $C_\bg$ 가 LCO 하프셀 자체 배경 입력(흑연 값 아님)임을 괄호 명시 여지 |

---

## 1. H 등급 (논리/물리 오류)

### A20-H1 — T1 온도 신호의 방향 서술 오류
- 파일:행 = `ch1_sec16_lcopeak.tex:62–66` · 유형 = 논리 · 등급 = **H**

현행(축자):
```latex
\textbf{T1 의 온도 신호.} T1 의 위치는 \S\ref{sec:lco-electronic} 의 전자항이 $\Delta S_{\rxn,1}^\mathrm{cat}$ 를 통해 $U_1(T)$ 의
\emph{온도 이동}에 기여하므로(식~\eqref{eq:lco-dUdT}), 다온도 dQ/dV 에서 T1 peak 의 \emph{온도 이동률}
$\partial U_1/\partial T$ 가 $T$ 에 선형으로 커지는 것이 전자항의 관측 신호이며($\Delta S_{e,1}\propto T$ ---
위치 이동은 $\propto T^2$, 식~\eqref{eq:U1T2}$\cdot$\S\ref{sec:lco-Se}), 도핑은 \S\ref{sec:lco-hys} 대로 peak 를 smear$\cdot$shift 시킨다($\Omega$ 는
gap$\cdot$smear 슬롯, $U_j^\mathrm{cat}$ 이동은 별도 슬롯).
```

제안(완성 LaTeX):
```latex
\textbf{T1 의 온도 신호.} T1 의 위치에는 \S\ref{sec:lco-electronic} 의 전자항이 $\Delta S_{\rxn,1}^\mathrm{cat}$ 를 통해 $U_1(T)$ 의
\emph{온도 이동}으로 기여하므로(식~\eqref{eq:lco-dUdT}), 다온도 dQ/dV 에서 T1 peak 의 \emph{온도 이동률}
$\partial U_1/\partial T$ 에 $T$ 에 선형인 음의 전자 몫($\Delta S_{e,1}^{\,\mathrm{mol}}/F<0$, 삽입 기준)이 더해져 이동률이 $T$ 를 따라
선형으로 \emph{내려가는} 것 --- 곧 $U_1(T)$ 의 음의 $T^2$ 곡률로 고온 외삽이 선형 외삽보다 낮아지는 것 --- 이 전자항의 관측 신호이며($\Delta S_{e,1}\propto T$ ---
위치 이동은 $\propto T^2$, 식~\eqref{eq:U1T2}$\cdot$\S\ref{sec:lco-Se}), 도핑은 \S\ref{sec:lco-hys} 대로 peak 를 smear$\cdot$shift 시킨다($\Omega$ 는
gap$\cdot$smear 슬롯, $U_j^\mathrm{cat}$ 이동은 별도 슬롯).
```

근거(재유도):
1. §2.5 식 eq:U1T2 앞 정의로 $\Delta S_{\rxn,1}^\mathrm{cat}(T)=\Delta S_0+a_eT$, 전자 기울기 $a_e=-\tfrac{\pi^2}{3}R(k_B/e_V)(g_{\max}/\Delta x_\mathrm{MIT})\sigma(1-\sigma)$ 는 **명시적으로 $<0$**(ch1_sec15_lcoelec.tex:219–222).
2. 따라서 $\partial U_1/\partial T=[\Delta S_0+a_eT]/F$ 의 $T$-미분은 $a_e/F<0$ — 이동률은 $T$ 에 **선형으로 감소**한다. "선형으로 커진다"는 대수 부호가 반대다(크기 $|a_eT|$ 로 읽어도 주어가 "$\partial U_1/\partial T$"라 성립하지 않음 — §2.2 verifybox 기저 $+80$ 과 골 $-46$ 의 합 $+34>0$ 인 창 중심에서도 이동률 자체는 $T$ 상승 시 줄어든다).
3. §2.5 자신의 식별 신호 서술과 상충: "고온 외삽이 선형 외삽보다 낮아지는 것이 전자항의 식별 신호다"(ch1_sec15_lcoelec.tex:234), "전자 기여 $\partial U_j/\partial T|_e=\Delta S_{e,j}/F\propto T$ 가 $T$ 에 선형"(부호 중립 서술, 같은 파일 215–216). 제안문은 이 두 서술과 정합.
4. 겸사: 주술 호응("T1 의 위치는 … 기여하므로" → "T1 의 위치에는 … 기여하므로")도 함께 교정(별건 L 을 흡수).

---

## 2. M 등급 (의미·이해 실질 개선)

### A20-M1 — srcbox 의 구판 절 번호 하드코딩 "(본문 §17.1(c))"
- 파일:행 = `ch1_sec17_msmr.tex:52–53` · 유형 = 논리(참조 오귀속) · 등급 = M

현행(축자):
```latex
곧 식~\eqref{eq:lco-msmrmap} 의 1:1 대응이며, 계수비교 한 줄($f/\omega_j=\sigma_d/w_j$)이 방향 인자
$f=+\sigma_d$ 를 유일하게 고정한다(본문 §17.1(c)). \emph{방법 요지} --- Verbrugge 등은 삽입 전극 OCV 를
```

제안(완성 LaTeX):
```latex
곧 식~\eqref{eq:lco-msmrmap} 의 1:1 대응이며, 계수비교 한 줄($f/\omega_j=\sigma_d/w_j$)이 방향 인자
$f=+\sigma_d$ 를 유일하게 고정한다(본문 \S\ref{sec:lco-code-msmr}(c)). \emph{방법 요지} --- Verbrugge 등은 삽입 전극 OCV 를
```

근거: v1.0.22 재편으로 이 파일은 Ch2 마스터(`ch2_lco_v1.0.22.tex`, `\thesection=2.\arabic{section}`)의 7번째 절 = **§2.7** 로 조립된다(마스터 20–29행). "§17.1" 은 v1.0.21 구 Ch1 단일장 시절 번호로, 컴파일 PDF 에 존재하지 않는 절 번호가 인쇄된다. 라벨 `sec:lco-code-msmr`(같은 파일 12행)로 걸면 재편 무관 live 번호가 된다. 이 문자열은 comp_R3 다리 원안(`results/comp_R3/E_bridges/br_msmr_lineage.tex:44`)에서 축자 이월된 것 — 원안 자체가 구번호 기준이므로 마스터 통합 시 원안도 동보정 대상(참고).

### A20-M2 — $x_\mathrm{center}$ 미정의 기호
- 파일:행 = `ch1_sec17_msmr.tex:150–154` · 유형 = 보완 · 등급 = M

현행(축자):
```latex
전자항이 $\propto T'$ 라 이 적분의 닫힌형이 식~\eqref{eq:U1T2} 의 $T^2$ 곡률이고, \emph{현행 모델}은
$\Delta S_e$ 를 $T_\mathrm{ref}$ 에서 동결한 상수 오프셋(단일-기준 근사 --- 조성도 $x{=}x_\mathrm{center}$ 로
동결해 $V$-무관 상수)
으로 넣으므로 $U_1(T)\approx U_1(T_\mathrm{ref})+[\Delta S_{\rxn,1}^\mathrm{cat}(x_\mathrm{center},T_\mathrm{ref})/F]
(T-T_\mathrm{ref})$ 의 \emph{선형} $U(T)$ 가 된다(동결 근사의 결과 --- 다온도 $T^2$ 곡률은 round-trip 피팅 단계 과제).
```

제안(완성 LaTeX — 첫 등장 괄호에 정의 삽입, 나머지 불변):
```latex
전자항이 $\propto T'$ 라 이 적분의 닫힌형이 식~\eqref{eq:U1T2} 의 $T^2$ 곡률이고, \emph{현행 모델}은
$\Delta S_e$ 를 $T_\mathrm{ref}$ 에서 동결한 상수 오프셋(단일-기준 근사 --- 조성도 $x{=}x_\mathrm{center}$,
곧 전이별로 지정하는 동결 조성 입력(T1 시연값은 게이트 중심 $x_\mathrm{MIT}{=}0.85$)으로
동결해 $V$-무관 상수)
으로 넣으므로 $U_1(T)\approx U_1(T_\mathrm{ref})+[\Delta S_{\rxn,1}^\mathrm{cat}(x_\mathrm{center},T_\mathrm{ref})/F]
(T-T_\mathrm{ref})$ 의 \emph{선형} $U(T)$ 가 된다(동결 근사의 결과 --- 다온도 $T^2$ 곡률은 round-trip 피팅 단계 과제).
```

근거: $x_\mathrm{center}$ 는 두 대상 절과 §2.1–2.5·Ch2 기호표(`ch2v22_notation.tex`) 어디에도 정의가 없고, 구현(`Anode_Fit_v1.0.22.py:878` `'x_center': 0.85`, `:933` `func_dSe_molar(tr['x_center'], T_ref, …)`)에서만 뜻이 확정된다. "본 장만으로 재현" 원칙(흑연 §1.10 선언과 동격)상 본문 자체 정의가 필요. P5(이름 보존)에 따라 기호 교체가 아닌 정의 괄호 추가로 제안.

### A20-M3 — 고정점 순환의 셋째 호 누락
- 파일:행 = `ch1_sec17_msmr.tex:154–156` · 유형 = 보완 · 등급 = M

현행(축자):
```latex
평가 순서 주의 --- 식~\eqref{eq:lco-xmap} 이
$\xi_{\eq,1}$ 을, $\xi_{\eq,1}$ 이 $U_1$ 을 참조하는 고정점 구조이나, 동결 근사는 순환이 없고, 정밀형도
전자항 제외 중심으로 $\xi_{\eq,1}^{(0)}$ 을 먼저 평가해 1회 갱신하는 것을 초기 근사로 채택한다
```

제안(완성 LaTeX):
```latex
평가 순서 주의 --- 식~\eqref{eq:lco-xmap} 이
$\xi_{\eq,1}$ 을, $\xi_{\eq,1}$ 이 $U_1$ 을, $U_1$ 이 다시 전자항(식~\eqref{eq:lco-SeV}$\cdot$\eqref{eq:lco-U1V})을 통해
$x(\xi_{\eq,1})$ 을 참조하는 닫힌 고리의 고정점 구조이나, 동결 근사는 순환이 없고, 정밀형도
전자항 제외 중심으로 $\xi_{\eq,1}^{(0)}$ 을 먼저 평가해 1회 갱신하는 것을 초기 근사로 채택한다
```

근거: 순환은 $x\leftarrow\xi_{\eq,1}\leftarrow U_1\leftarrow\Delta S_{e,1}(x)$ 의 세 호가 있어야 닫히는데 현행은 두 호만 적어 "고정점"의 성립 이유가 문장 안에서 보이지 않는다. P3-3(순환 의존이 **어느 식·어느 변수**에서 생기는지 표시 의무)의 완결 — 두 대상 절에서 유일한 self-consistent 고리이므로 세 호 전부를 식 번호로 명시하는 편이 규약 정합적.

### A20-M4 — "분기 gap 도 흑연보다 키운다"의 조건부화 + 단조성 근거
- 파일:행 = `ch1_sec16_lcopeak.tex:53–55` · 유형 = 논리(과대 주장) · 등급 = M

현행(축자):
```latex
문헌\cite{xia2007,reynier2004,motohashi2009} 그대로다(\S\ref{sec:lco-map}). order--disorder 의 큰 $\Omega_j^\mathrm{cat}$($>2RT$ 로 피팅될 경우)는
(i) plateau(두-상) 성격을 강화해 평형 peak 를 델타에 가깝게 하고(실측 폭은 $w_j$ 가 현상학적으로 담음 ---
\S\ref{sec:broadening}), (ii) 분기 gap(식~\eqref{eq:lco-dUhys})도 흑연보다 키운다.
```

제안(완성 LaTeX):
```latex
문헌\cite{xia2007,reynier2004,motohashi2009} 그대로다(\S\ref{sec:lco-map}). order--disorder 의 큰 $\Omega_j^\mathrm{cat}$($>2RT$ 로 피팅될 경우)는
(i) plateau(두-상) 성격을 강화해 평형 peak 를 델타에 가깝게 하고(실측 폭은 $w_j$ 가 현상학적으로 담음 ---
\S\ref{sec:broadening}), (ii) 분기 gap(식~\eqref{eq:lco-dUhys} --- $\Omega$ 에 단조증가,
$\dd\Delta U_j^{\hys,\mathrm{cat}}/\dd\Omega_j^\mathrm{cat}=2u_j^\mathrm{cat}/F>0$)도 $\Omega_j^\mathrm{cat}$ 이 흑연 값보다
크게 피팅되는 만큼 흑연보다 키운다.
```

근거(재계산): $\Delta U^{\hys}=\tfrac2F[\Omega u-2RT\,\mathrm{artanh}\,u]$, $u=\sqrt{1-2RT/\Omega}$ 에서 $\dd u/\dd\Omega=RT/(\Omega^2u)$, $1-u^2=2RT/\Omega$ 이므로 $\Omega\,\dd u/\dd\Omega$ 와 $\tfrac{2RT}{1-u^2}\dd u/\dd\Omega$ 가 정확 상쇄, $\dd\Delta U/\dd\Omega=2u/F>0$ — gap 이 $\Omega$ 에 단조증가. 따라서 "흑연보다 크다"는 $\Omega_j^\mathrm{cat}>\Omega_j^{\text{(흑연)}}$ 일 때만 따라 나오는데, §2.3 two-phase calibration(ch1_sec13_lcohys.tex:34–39)은 LCO $\Omega^\mathrm{cat}$ 을 **미배정**(수치 열 없음·$\Omega{=}0$ 취급)으로 선언하므로 현행 단정은 문서 자신의 지위 선언보다 강하다. 괄호 "$>2RT$ 로 피팅될 경우"는 gap$>0$ 만 보장하고 흑연 대비 우위는 보장하지 않음. 제안은 단조성(검증된 대수)을 명기해 비교를 조건부로 정확화 — 기존 문장 구조·자산 보존.

### A20-M5 — MSMR 가정 차 목록에 배경항 부재 미기재
- 파일:행 = `ch1_sec17_msmr.tex:55–61`(srcbox 가정 차 문단 끝) · 유형 = 보완 · 등급 = M

현행(축자):
```latex
세웠고, Baker--Verbrugge 가 이를 다공 전극 다반응 정식화로 확장하며 MSMR 로 명명했다. \emph{가정 차}
--- 원계열 MSMR 은 방향 없는 \emph{평형 등온선}이고 폭이 무차원 $\omega_j$(지수의 $F/RT$ 항상 양)이나,
본문은 $F/RT$ 를 폭에 흡수($\omega_j\!\mapsto\!w_j$, 전압 차원)하고 방향 부호 $f=+\sigma_d$ 를 남겨
충$\cdot$방전을 재배선하며, 순정 MSMR 에 없는 히스테리시스 분기($\gamma_j$, \S\ref{sec:lco-hys})와 T1
전자 엔트로피 항(\S\ref{sec:lco-electronic})을 추가로 얹는다 --- \emph{함수형 동형이지 물리량 동일이
아니다}($x_j/X_j$ 는 리튬화 점유, $\xi$ 는 탈리튬화 진행률).
```

제안(완성 LaTeX — 마지막 문장 뒤 한 문장 추가, 기존 문구 불변):
```latex
세웠고, Baker--Verbrugge 가 이를 다공 전극 다반응 정식화로 확장하며 MSMR 로 명명했다. \emph{가정 차}
--- 원계열 MSMR 은 방향 없는 \emph{평형 등온선}이고 폭이 무차원 $\omega_j$(지수의 $F/RT$ 항상 양)이나,
본문은 $F/RT$ 를 폭에 흡수($\omega_j\!\mapsto\!w_j$, 전압 차원)하고 방향 부호 $f=+\sigma_d$ 를 남겨
충$\cdot$방전을 재배선하며, 순정 MSMR 에 없는 히스테리시스 분기($\gamma_j$, \S\ref{sec:lco-hys})와 T1
전자 엔트로피 항(\S\ref{sec:lco-electronic})을 추가로 얹는다 --- \emph{함수형 동형이지 물리량 동일이
아니다}($x_j/X_j$ 는 리튬화 점유, $\xi$ 는 탈리튬화 진행률). 또한 순정 MSMR 의 총합 $x=\sum_jx_j$ 는 자리 보존으로
전 조성을 종이 소진하는 반면, 본문 보존식~\eqref{eq:lco-charge} 에는 종(class) 밖 저장인 배경항 $Q_\bg$($C_\bg$)가
따로 얹힌다 --- 배경 슬롯은 MSMR 에 대응물이 없는 Ch1 측 추가다.
```

근거: §2.7(b) 는 전하 보존식과의 "같은 구조(용량-가중 logistic 합)"를 주장하는데(70–72행), 실제 구조 차이 하나(배경항)가 가정 차 목록에서 빠져 있다. 흑연 §1.6 bgbox 검산 (iv) 가 "비전이 배경 $C_\bg$ 는 클래스 밖 저장"으로 이미 성격을 규정했으므로(ch1_sec06_eqpeak.tex:72–73), 대응물 부재를 한 줄 명기하면 "동형" 주장의 경계가 정확해진다. 다리 박스의 자족성(제거 용이 블록) 유지 — 박스 내부 추가라 독립성 불변.

### A20-M6 — eq:lco-SeV 의 창끝 포화(전자항이 0 으로 죽지 않음) 주의 부재
- 파일:행 = `ch1_sec17_msmr.tex:131–137`(식 eq:lco-SeV 직후) · 유형 = 보완 · 등급 = M

현행(축자):
```latex
\begin{equation}
\Delta S_{e,1}^{\,\mathrm{mol}}(V,T)
=-\frac{\pi^2}{3}\,R\,\frac{k_BT}{e_V}\,\frac{g_{\max}}{\Delta x_\mathrm{MIT}}\,
\sigma\!\big(z_e(V)\big)\big[1-\sigma\!\big(z_e(V)\big)\big],
\qquad z_e(V)=\frac{x(\xi_{\eq,1}(V))-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}}.
\label{eq:lco-SeV}
\end{equation}
```

제안(완성 LaTeX — 식 뒤에 괄호 문장 추가, 식 자체 불변):
```latex
\begin{equation}
\Delta S_{e,1}^{\,\mathrm{mol}}(V,T)
=-\frac{\pi^2}{3}\,R\,\frac{k_BT}{e_V}\,\frac{g_{\max}}{\Delta x_\mathrm{MIT}}\,
\sigma\!\big(z_e(V)\big)\big[1-\sigma\!\big(z_e(V)\big)\big],
\qquad z_e(V)=\frac{x(\xi_{\eq,1}(V))-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}}.
\label{eq:lco-SeV}
\end{equation}
(창끝 포화 주의 --- 매핑~\eqref{eq:lco-xmap} 이 $x\in[x_{\mathrm{lo},1},x_{\mathrm{hi},1}]$ 에 포화하므로
$z_e\in[-2.0,+1.8]$ 로 유계이고 $\sigma(1-\sigma)$ 는 창 끝에서 $\approx0.11$--$0.12$ 로 남아 이 $V$-형
전자항은 0 으로 죽지 않는다 --- \S\ref{sec:lco-electronic} 의 ``창 밖 $\approx0$'' 은 전 조성축 $x$ 기준
서술이고, $V$-축에서 T1 창 밖의 이 잔존은 $U_1$ 의 온도 이동에만 들어가며 T1 몫 자체가
$\xi_{\eq,1}(1-\xi_{\eq,1})\to0$ 으로 소멸해 곡선에는 나타나지 않는다.)
```

근거(재계산): $x_{\mathrm{hi},1}{=}0.94$, $x_{\mathrm{lo},1}{=}0.75$, $x_\mathrm{MIT}{=}0.85$, $\Delta x_\mathrm{MIT}{=}0.05$ 로 $z_e$ 극값은 $(0.94{-}0.85)/0.05{=}{+}1.8$, $(0.75{-}0.85)/0.05{=}{-}2.0$. $\sigma(1.8)[1{-}\sigma(1.8)]=0.8581\times0.1419=0.122$, $\sigma(-2.0)[1{-}\sigma(-2.0)]=0.1192\times0.8808=0.105$ — 골 최대 $1/4$ 대비 42–49%, 몰당 $-19$~$-22$ J/(mol K) 잔존. §2.5 의 "게이트 골, 창 밖 $\approx0$"(ch1_sec14_lcodecomp.tex:48 · ch1_sec12_lcocenter.tex:102–103 "창 밖에서 $\approx0$")은 $x$-축 서술이라 $V$-축 매핑형과 좌표계가 다르고, 그 간극을 독자가 물을 지점이다(수치 검증한 무해성 논거까지 제시). 동결 근사(현행 구현)에는 영향 없음 — 정밀형 전용 주의.

### A20-M7 — eq:lco-msmrpeak 의 $\omega_j$ 파라미터화 명시
- 파일:행 = `ch1_sec17_msmr.tex:101–110` · 유형 = 설명 · 등급 = M

현행(축자):
```latex
\textbf{(d) 박스 --- MSMR$\to$평형 peak 변환 폐쇄.}
대응표~\eqref{eq:lco-msmrmap} 아래에서 MSMR 종별 미분용량과 Ch1 평형 peak 은 같은 식이다:
\begin{equation}
\boxed{\;Q_j\Big|\frac{\dd(x_j/X_j)}{\dd U}\Big|
=Q_j\,\frac{\theta_j^{\mathrm{MSMR}}(1-\theta_j^{\mathrm{MSMR}})}{\omega_j}
\;\equiv\;Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}
\quad(\text{식~\eqref{eq:lco-eqpeak} 의 피가수})\;,}
\label{eq:lco-msmrpeak}
\end{equation}
($|f|=1$; $\theta(1-\theta)=\xi(1-\xi)$ --- 여집합 불변).
```

제안(완성 LaTeX — 식 불변, 뒤 괄호만 확장):
```latex
\textbf{(d) 박스 --- MSMR$\to$평형 peak 변환 폐쇄.}
대응표~\eqref{eq:lco-msmrmap} 아래에서 MSMR 종별 미분용량과 Ch1 평형 peak 은 같은 식이다:
\begin{equation}
\boxed{\;Q_j\Big|\frac{\dd(x_j/X_j)}{\dd U}\Big|
=Q_j\,\frac{\theta_j^{\mathrm{MSMR}}(1-\theta_j^{\mathrm{MSMR}})}{\omega_j}
\;\equiv\;Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}
\quad(\text{식~\eqref{eq:lco-eqpeak} 의 피가수})\;,}
\label{eq:lco-msmrpeak}
\end{equation}
($|f|=1$ --- 여기 $\omega_j$ 는 재모수화된 \emph{전압 차원} 폭($=w_j$)이다; 원계열 표기(무차원 $\omega_j$·$f{=}F/RT$)로 적으면
같은 양이 $Q_j(f/\omega_j)\theta(1-\theta)$ 다. $\theta(1-\theta)=\xi(1-\xi)$ --- 여집합 불변).
```

근거(재유도): $\theta=[1+e^{+f(U-U_j^0)/\omega_j}]^{-1}$ 의 미분은 $|\dd\theta/\dd U|=(|f|/\omega_j)\theta(1-\theta)$. 중간 변 "$\theta(1-\theta)/\omega_j$" 는 $|f|{=}1$(재모수화) 읽기에서만 성립하고, 원계열 무차원 $\omega_j$ 로 읽으면 차원부터 어긋난다($1/\omega_j$ 는 무차원 — dQ/dV 가 못 됨). 이 절은 eq:msmr 을 원계열 표기로 출발시켰으므로(18–19행) 어느 시점부터 $\omega_j$ 가 전압 차원으로 바뀌는지 독자가 추적해야 하는데, 그 스위치가 "$|f|=1$" 두 글자에만 실려 있다. 한 줄 명시로 두 표기의 등가까지 보인다.

### A20-M8 — 고정점 1회 갱신의 수축 상한 보강(선택)
- 파일:행 = `ch1_sec17_msmr.tex:155–159` · 유형 = 보완 · 등급 = M

현행(축자):
```latex
$\xi_{\eq,1}$ 을, $\xi_{\eq,1}$ 이 $U_1$ 을 참조하는 고정점 구조이나, 동결 근사는 순환이 없고, 정밀형도
전자항 제외 중심으로 $\xi_{\eq,1}^{(0)}$ 을 먼저 평가해 1회 갱신하는 것을 초기 근사로 채택한다(되먹임
이동 $|\Delta S_e^{\,\mathrm{mol}}|/F\times|T-T_\mathrm{ref}|\approx0.47\,\mathrm{mV/K}\times30\,\mathrm K
\approx14$ mV $\lesssim w_1$ --- 폭 이하 스케일이라 보정이 작다는 상한이며, 수렴 여부 자체는 round-trip
피팅 단계에서 수치 확인한다).
```

제안(완성 LaTeX — 기존 괄호 문장 유지, 각주 하나 추가):
```latex
$\xi_{\eq,1}$ 을, $\xi_{\eq,1}$ 이 $U_1$ 을 참조하는 고정점 구조이나, 동결 근사는 순환이 없고, 정밀형도
전자항 제외 중심으로 $\xi_{\eq,1}^{(0)}$ 을 먼저 평가해 1회 갱신하는 것을 초기 근사로 채택한다(되먹임
이동 $|\Delta S_e^{\,\mathrm{mol}}|/F\times|T-T_\mathrm{ref}|\approx0.47\,\mathrm{mV/K}\times30\,\mathrm K
\approx14$ mV $\lesssim w_1$ --- 폭 이하 스케일이라 보정이 작다는 상한이며, 수렴 여부 자체는 round-trip
피팅 단계에서 수치 확인한다)\footnote{수축 상한 한 줄: 되먹임 한 바퀴의 이득은 연쇄율 곱으로
$\big|\tfrac{\partial U_1^{\text{(갱신)}}}{\partial U_1}\big|
\le\tfrac{|T-T_\mathrm{ref}|}{F}\cdot\underbrace{\tfrac{4|\Delta S_e^{\,\mathrm{mol}}|_{\max}}{6\sqrt3}}_{|\partial\Delta S_e/\partial z_e|_{\max}}
\cdot\tfrac{x_{\mathrm{hi},1}-x_{\mathrm{lo},1}}{\Delta x_\mathrm{MIT}}\cdot\tfrac{1}{4w_1}
\approx0.2<1$($30$ K·$w_1{=}RT/F$ 기준)이라 반복이 수축이고, 1회 갱신의 잔차는 $\lesssim0.2\times14\ \mathrm{mV}\approx3$ mV 다.}.
```

근거(재계산): 고리 $U_1\to\xi_{\eq,1}\to x\to z_e\to\Delta S_e\to U_1$ 의 인자별 상한 — $|\partial\xi/\partial U|\le1/(4w_1)=9.73\,\mathrm V^{-1}$, $|\partial x/\partial\xi|=0.19$, $|\partial z/\partial x|=1/0.05=20$, $|\partial(\sigma(1{-}\sigma))/\partial z|\le1/(6\sqrt3)=0.0962$ ⟹ $|\partial\Delta S_e/\partial z|\le4\times45.7\times0.0962=17.6$ J/(mol K), $|\partial U_1/\partial\Delta S_e|=|T{-}T_\mathrm{ref}|/F=3.11\times10^{-4}$ V/(J/(mol K)). 곱 $=3.11\times10^{-4}\times17.6\times3.8\times9.73=0.20$. 기존의 "수치 확인 위임" 문장을 대체하지 않고(존치) 상한만 보강 — 위임 자체는 정직 공백 유지.

### A20-M9 — 동결 vs 정밀형 대비의 표 수식화
- 파일:행 = `ch1_sec17_msmr.tex:150–159` · 유형 = 수식화 · 등급 = M

현행(축자 — 대상 산문, M2 인용부와 동일 구간 + 후속 문장):
```latex
으로 넣으므로 $U_1(T)\approx U_1(T_\mathrm{ref})+[\Delta S_{\rxn,1}^\mathrm{cat}(x_\mathrm{center},T_\mathrm{ref})/F]
(T-T_\mathrm{ref})$ 의 \emph{선형} $U(T)$ 가 된다(동결 근사의 결과 --- 다온도 $T^2$ 곡률은 round-trip 피팅 단계 과제). 평가 순서 주의 --- 식~\eqref{eq:lco-xmap} 이
```

제안(완성 LaTeX — 산문 뒤 보조 소표 추가, 산문 불변; 신규 라벨 제안 표기 `tab:lco-freeze` ):
```latex
으로 넣으므로 $U_1(T)\approx U_1(T_\mathrm{ref})+[\Delta S_{\rxn,1}^\mathrm{cat}(x_\mathrm{center},T_\mathrm{ref})/F]
(T-T_\mathrm{ref})$ 의 \emph{선형} $U(T)$ 가 된다(동결 근사의 결과 --- 다온도 $T^2$ 곡률은 round-trip 피팅 단계 과제).
두 층위를 한눈에 갈라 두면:
\begin{center}\footnotesize
\begin{tabular}{@{}lll@{}}
\hline
 & 동결(현행 구현) & 정밀형(round-trip 과제) \\
\hline
전자항 평가점 & $(x_\mathrm{center},\,T_\mathrm{ref})$ 상수 & $\big(x(\xi_{\eq,1}(V)),\,T\big)$ 연속(식~\eqref{eq:lco-SeV}) \\
$U_1(T)$ 꼴 & $T$-선형(위 식) & $T^2$ 곡률(식~\eqref{eq:U1T2}) \\
$V$-의존$\cdot$순환 & 없음 & 고정점 --- $\xi_{\eq,1}^{(0)}$ 평가 후 1회 갱신 \\
\hline
\end{tabular}
\end{center}
평가 순서 주의 --- 식~\eqref{eq:lco-xmap} 이
```

근거: 동결/정밀형의 3중 차이(평가점·$U_1(T)$ 함수형·순환 유무)가 150–159행 산문에 중첩 괄호로 흩어져 있어 독자가 재조립해야 한다. 표 3행이면 기계적으로 갈린다. 기존 산문은 전부 존치(보조 표만 추가) — P5 보존 정합.

---

## 3. L 등급 (문체·소소)

### A20-L1 — 재모수화 문장 분할(설명)
- 파일:행 = `ch1_sec17_msmr.tex:18–22` · 유형 = 설명 · 등급 = L

현행(축자):
```latex
여기서 $X_j$ 는 종(전이) $j$ 의 용량 분율, $U_j^0$ 는 종 중심 전위다. 원계열 MSMR 의 지수 인자
$f=F/RT$(항상 양)$\cdot$무차원 폭 $\omega_j$ 를 본 장은 $F/RT$ 를 폭에 흡수($\omega_j\mapsto\omega_jRT/F$,
전압 차원)해 방향 부호 $f=\pm1$ 만 지수에 남기도록 재모수화하며, 이는 폭 슬롯 대응이 흑연
식~\eqref{eq:wbase} 의 $w_j=n_jRT/F$($n_j\leftrightarrow$무차원 $\omega_j$)와 동형임을 드러낸다(정식
대응은 아래 식~\eqref{eq:lco-msmrmap}).
```

제안(완성 LaTeX):
```latex
여기서 $X_j$ 는 종(전이) $j$ 의 용량 분율, $U_j^0$ 는 종 중심 전위, 지수 인자는 $f=F/RT$(항상 양),
폭은 무차원 $\omega_j$ 다. 본 장은 $F/RT$ 를 폭에 흡수해 $\omega_j\mapsto\omega_jRT/F$(전압 차원)로
재모수화한다 --- 그러면 지수에는 방향 부호 $f=\pm1$ 만 남고, 폭 슬롯은 흑연 식~\eqref{eq:wbase} 의
$w_j=n_jRT/F$ 와 동형이 된다($n_j\leftrightarrow$무차원 $\omega_j$; 정식 대응은 아래
식~\eqref{eq:lco-msmrmap}).
```

근거: 1문 4중 괄호 → 2문. 내용·기호 불변, 흐름(원계열 정의 → 재모수화 → 동형)이 시간순으로 펼쳐짐.

### A20-L2 — eq:lco-charge 합 지표 혼용
- 파일:행 = `ch1_sec16_lcopeak.tex:10–15` · 유형 = 설명 · 등급 = L

현행(축자):
```latex
\begin{equation}
Q_\cell\,q=Q_\bg+\sum_{j\in\mathcal J_\mathrm{LCO}}Q_j^\mathrm{cat}\,\xi_j
\;\Longrightarrow\;
\frac{\dd Q}{\dd V}=C_\bg+\sum_{j=1}^{3}Q_j^\mathrm{cat}\,\frac{\dd\xi_j}{\dd V}.
\label{eq:lco-charge}
\end{equation}
```

제안(완성 LaTeX):
```latex
\begin{equation}
Q_\cell\,q=Q_\bg+\sum_{j\in\mathcal J_\mathrm{LCO}}Q_j^\mathrm{cat}\,\xi_j
\;\Longrightarrow\;
\frac{\dd Q}{\dd V}=C_\bg+\sum_{j\in\mathcal J_\mathrm{LCO}}Q_j^\mathrm{cat}\,\frac{\dd\xi_j}{\dd V}
\qquad(\mathcal J_\mathrm{LCO}=\{1,2,3\},\ \text{식~\eqref{eq:lco-J}}).
\label{eq:lco-charge}
\end{equation}
```

근거: 한 식 안에서 좌변 합은 $j\in\mathcal J_\mathrm{LCO}$, 우변 합은 $j=1..3$ — eq:lco-J(=\{T1,T2,T3\}, $j$=1,2,3 번호 부여)로 동치라 오류는 아니나, 같은 식에서 지표 표기가 갈리면 "다른 집합인가" 하는 순간적 의심을 만든다. 어느 쪽으로든 통일 + 동치 근거 괄호가 낫다(제안은 집합 표기 통일안 — $\sum_{j=1}^3$ 통일도 등가).

### A20-L3 — §2.6 의 평가 전위 $V$ 와 $V_n$ 위계 한 줄 수신
- 파일:행 = `ch1_sec16_lcopeak.tex:8–9` · 유형 = 보완 · 등급 = L

현행(축자):
```latex
\textbf{(a) 출발 --- 전하 보존식을 LCO 전이 집합으로.} 흑연 \S\ref{sec:eqpeak} 의 출발점인 전하 보존식은
전극을 가리지 않으므로, 전이 집합만 $\mathcal J_\mathrm{LCO}$(식~\eqref{eq:lco-J})로 바꿔 그대로 적는다:
```

제안(완성 LaTeX):
```latex
\textbf{(a) 출발 --- 전하 보존식을 LCO 전이 집합으로.} 흑연 \S\ref{sec:eqpeak} 의 출발점인 전하 보존식은
전극을 가리지 않으므로, 전이 집합만 $\mathcal J_\mathrm{LCO}$(식~\eqref{eq:lco-J})로 바꿔 그대로 적는다
(평가 전위도 흑연과 동일 --- 식~\eqref{eq:xieq} 아래 규정대로 내부 전위 $V_n$ 이며, 이하 $V$ 로 약기):
```

근거: 흑연 골격은 "평가 전위는 \S sec:pol 의 내부 전위 $V_n$"(ch1_sec05_width.tex:286)을 명시하는데 §2.6–2.7 은 전부 맨 $V$ 표기다. 오류는 아니나(전극-중립 골격 xr 수신), P3-1($V_n$ 위계 일관성) 게이트에서 물을 지점이라 한 줄 수신 명시가 안전하다.

### A20-L4 — 계수비교의 상수항 귀결($U_j^0=U_j^{\,d}$) 한 줄
- 파일:행 = `ch1_sec17_msmr.tex:92–95` · 유형 = 보완 · 등급 = L

현행(축자):
```latex
가 1:1 로 읽힌다 --- 방향 인자 대응 $f=+\sigma_d$ 는 두 지수가 \emph{모든} $U$ 에서 일치할 것을 요구하는
항등식의, 이 pairing 하에서의 유일해다(계수비교 한 줄: 두 지수 $-f(U-U_j^0)/\omega_j$ 와
$-\sigma_d(V-U_j^{\,d})/w_j$ 가 모든 $U$ 에서 같으려면 $U$ 의 1차 계수가 같아야 하므로
$f/\omega_j=\sigma_d/w_j$ 이고, 폭 슬롯 대응 $\omega_j\leftrightarrow w_j$ 아래에서 $f=+\sigma_d$ 만 남는다).
```

제안(완성 LaTeX):
```latex
가 1:1 로 읽힌다 --- 방향 인자 대응 $f=+\sigma_d$ 는 두 지수가 \emph{모든} $U$ 에서 일치할 것을 요구하는
항등식의, 이 pairing 하에서의 유일해다(계수비교 한 줄: 두 지수 $-f(U-U_j^0)/\omega_j$ 와
$-\sigma_d(V-U_j^{\,d})/w_j$ 가 모든 $U$ 에서 같으려면 $U$ 의 1차 계수가 같아야 하므로
$f/\omega_j=\sigma_d/w_j$ 이고, 폭 슬롯 대응 $\omega_j\leftrightarrow w_j$ 아래에서 $f=+\sigma_d$ 만 남는다;
같은 항등식의 상수항 비교는 $U_j^0=U_j^{\,d}$ --- 중심 슬롯 대응 --- 도 함께 고정한다).
```

근거(재유도): 전 $U$ 항등 ⟹ 1차 계수 $f/\omega_j=\sigma_d/w_j$ **및** 상수항 $fU_j^0/\omega_j=\sigma_dU_j^{\,d}/w_j$ ⟹ (1차 결과 대입) $U_j^0=U_j^{\,d}$. 현행은 중심 대응을 pairing 가정으로만 두는데, 같은 계수비교가 이를 유도로도 돌려주므로 한 줄이면 대응표~eq:lco-msmrmap 의 중심 슬롯이 가정에서 귀결로 승격된다.

### A20-L5 — eq:br-msmr-1 화살표 아래첨자의 자기완결
- 파일:행 = `ch1_sec17_msmr.tex:46–51` · 유형 = 설명 · 등급 = L

현행(축자):
```latex
\begin{equation}
\frac{f\,(U-U_j^0)}{\omega_j}\ \xrightarrow[\ \omega_j\mapsto w_j=n_jRT/F\ ]{\ f=F/RT\ \text{흡수}\ }\
\frac{\sigma_d\,(V-U_j^{\,d})}{w_j},
\qquad (U,U_j^0,\omega_j,X_j,f)\ \leftrightarrow\ (V,U_j^{\,d},w_j,Q_j,\sigma_d),
\label{eq:br-msmr-1}
\end{equation}
```

제안(완성 LaTeX):
```latex
\begin{equation}
\frac{f\,(U-U_j^0)}{\omega_j}\ \xrightarrow[\ \omega_j\mapsto w_j=\omega_jRT/F\,(=n_jRT/F,\ n_j\leftrightarrow\omega_j)\ ]{\ f=F/RT\ \text{흡수}\ }\
\frac{\sigma_d\,(V-U_j^{\,d})}{w_j},
\qquad (U,U_j^0,\omega_j,X_j,f)\ \leftrightarrow\ (V,U_j^{\,d},w_j,Q_j,\sigma_d),
\label{eq:br-msmr-1}
\end{equation}
```

근거: 본문 규정(19–21행)은 "$\omega_j\mapsto\omega_jRT/F$" 이고 $n_j\leftrightarrow\omega_j$ 는 별도 동일시다. 화살표 아래에 $n_j$ 만 적으면 박스(자족적이어야 하는 srcbox) 안에서 $n_j$ 의 출처가 끊긴다. 괄호로 둘을 함께 적으면 자기완결.

### A20-L6 — eq:lco-eqpeak 의 $C_\bg$ 전극별 입력 명시
- 파일:행 = `ch1_sec16_lcopeak.tex:42–49` · 유형 = 보완 · 등급 = L

현행(축자):
```latex
\textbf{(d) 박스 --- LCO 하프셀 3-전이 평형 dQ/dV.} (b)를 (a)에 넣으면 양극 전위 영역의 평형 기준선이 닫히며
\begin{equation}
\boxed{\;\Big(\frac{\dd Q}{\dd V}\Big)^{\eq}_\mathrm{LCO}(V,T)
=C_\bg+\sum_{j=1}^{3}Q_j^\mathrm{cat}\,
\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j},
\qquad \xi_{\eq,j}=\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j]}\;.}
\label{eq:lco-eqpeak}
\end{equation}
```

제안(완성 LaTeX — 식 불변, 직후 산문 한 구 추가):
```latex
\textbf{(d) 박스 --- LCO 하프셀 3-전이 평형 dQ/dV.} (b)를 (a)에 넣으면 양극 전위 영역의 평형 기준선이 닫히며
\begin{equation}
\boxed{\;\Big(\frac{\dd Q}{\dd V}\Big)^{\eq}_\mathrm{LCO}(V,T)
=C_\bg+\sum_{j=1}^{3}Q_j^\mathrm{cat}\,
\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j},
\qquad \xi_{\eq,j}=\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j]}\;.}
\label{eq:lco-eqpeak}
\end{equation}
($C_\bg$ 는 같은 배경 슬롯의 LCO 하프셀 입력값이다 --- 흑연 값의 재사용이 아니다.)
```

근거: 골격은 전극-중립(§2.1 (5))이나 슬롯 **값**은 전극별이라는 규약이 전이 파라미터에는 명시되고($Q^\mathrm{cat}$ 등 첨자) 배경 $C_\bg$ 에는 첨자도 언급도 없다. 독자가 "흑연 배경 상수가 양극 영역까지 이어지는가"를 물을 지점.

---

## 4. 서치 절 — 하이쿠 서브에이전트 서지 검증 (기억 서지 금지·검증분만)

지시대로 서지 확인은 하이쿠 서브 서치 2기로 수행했다(H-A: MSMR 계보 3키 / H-B: LCO anchor 3키). 방법 = doi.org 리졸브·Crossref API 필드 대조·출판사 랜딩 확인. **아래 표는 서브에이전트가 실제 리졸브해 확인 보고한 검증분만** 싣는다(미확인분은 미검증으로 4-tier 에 분리).

### 4.1 MSMR 계보 3키 (H-A 결과) — 전건 확인

| key | 검증 항목 | 결과 | 방법 |
|---|---|---|---|
| msmr_origin2017 | DOI 10.1149/2.0341708jes → JES **164**(11) E3243–E3253 (2017), 제목 "Thermodynamic Model for Substitutional Materials: Application to Lithiated Graphite, Spinel Manganese Oxide, Iron Phosphate, and Layered Nickel-Manganese-Cobalt Oxide", 저자 Mark Verbrugge·Daniel Baker·Brian Koch·Xingcheng Xiao·Wentian Gu(이니셜 없는 byline) | **일치**(bib 표기·"흑연·스피넬·인산철·층상 산화물 한 틀" 서술과 정합 — 층상 산화물=NMC) | Crossref+doi.org 리졸브 |
| bakerverbrugge2018 | DOI 10.1149/2.0771816jes → JES **165**(16) A3952–A3964 (2018), 제목 "Multi-Species, Multi-Reaction Model for Porous Intercalation Electrodes: Part I. Model Formulation and a Perturbation Solution for Low-Scan-Rate, Linear-Sweep Voltammetry", 저자 D. R. Baker·M. W. Verbrugge | **일치** — "Multi-Species, Multi-Reaction" 문구가 제목에 등장(명명 원전 주장과 정합); 2017 원전 제목에는 MSMR 문구 없음(bib 주석과 정합) | Crossref+doi.org 리졸브 |
| msmr2024 | DOI 10.1149/2754-2734/ad7d1c → **ECS Advances 3, 042501 (2024)**, 제목 "Quantifying the Temperature Dependence of the Multi-Species, Multi-Reaction Model. Part 1: Parameterization for a Meso-Carbon Micro-Bead Graphite" + Part 2: JES **171**(10) 103505, DOI 10.1149/1945-7111/ad70d9 | **일치** — "엔트로피·온도 의존 파라미터화가 뒤따랐다" 계보 문장과 정합(온도 의존 파라미터화 = dU/dT 경유 엔트로피) | Crossref+doi.org 리졸브 |

- 명명 계보 리스크 점검(H-A 추가 질의): "multi-species, multi-reaction" 명칭이 2018 이전 문헌 제목/초록에 선행 사용된 흔적은 확인되지 않음(검색 한도 내) — 본문 "명명했으며" 서술 유지 가능. 단 2017 원전 **본문 내** 표현까지의 전문 대조는 접근 한계로 미수행(아래 4-tier 미검증).
- eq:msmr 함수형($x_j=X_j/[1+\exp(f(U-U_j^0)/\omega_j)]$, $f=F/RT$) 자체의 원문 대조는 프로젝트 원안 주석(comp_R3 `br_msmr_lineage.tex` 8–12행)이 이미 "PyBaMM MSMR 구현 문서 경유 형태·정의 일치, 원 논문 식번호 직접 대조 미완(경미)" 로 기록 — H-A 재확인에서도 2차 출처(구현 문서·리뷰) 수준 일치까지만 재확인(1차 원문 식번호 대조는 여전히 미완, 아래 미검증 항).

### 4.2 LCO anchor 3키 (H-B 결과) — 전건 확인

| key | 검증 항목 | 결과 | 방법 |
|---|---|---|---|
| xia2007 | DOI 10.1149/1.2509021 → JES **154**(4) A337–A342 (2007), Xia·Lu·Meng·Ceder, LCO 박막 상전이·고전압 거동 | **일치** — §2.6 "LCO 하프셀 세 peak" 창(∼3.9/4.05/4.17 V)의 anchor 역할과 정합 | Crossref+doi.org 리졸브 |
| reynier2004 | DOI 10.1103/PhysRevB.70.174304 → PRB **70**, 174304 (2004), "Entropy of Li intercalation in Li$_x$CoO$_2$" | **일치** — 엔트로피 삼분해·O3 질서상 anchor 로서의 인용과 정합 | Crossref+doi.org 리졸브 |
| motohashi2009 | DOI 10.1103/PhysRevB.80.165114 → PRB **80**, 165114 (2009), "Electronic phase diagram of the layered cobalt oxide system Li$_x$CoO$_2$ ($0\le x\le1$)" | **일치** — 전자 상도표·T1 창 anchor 인용과 정합 | Crossref+doi.org 리졸브 |

- 세 peak 전위 수치(∼3.90/4.05/4.17–4.20 V)의 **원문 내 수치 대조**는 초록·공개 페이지 수준에서 4.05/4.17 V 쌍(질서 전이)과 MIT 2상역 언급까지 확인(H-B 보고) — 전문(figure) 수치 대조는 접근 한계로 미검증분에 분리. 표~tab:lco-staging 의 tier 표기("1차 문헌에서 읽은 출발점·초기값")와 상충 없음.
- 프로젝트 원장 대조: 6키 전부 v1.0.20 원장 V1 등재(spot-check 이력: msmr_origin2017·xia2007 포함 7건 전건 일치 — `V1020_REFERENCE_LEDGER.md:4`) → 하이쿠 재검과 상호 정합. 신규 등재 제안 없음(두 절의 서지 필요는 기존 V1 키로 충족 — 원장 규율상 신규 키 불요가 결론).

---

## 5. 무발견 축 (검토했으나 문제 없음 — 재유도/재계산 완료 명세)

1. **xr 수신 정확성(최중요 지시)**: 두 절의 참조 전수(§2.6 = 라벨 21종, §2.7 = 라벨 30종) 역추적 — Ch1 측 5종(eq:xieq·eq:belliden·eq:wbase·eq:sum·tab:staging + sec:eqpeak/width/broadening)은 Ch1 마스터 입력 파일에, 나머지는 Ch2 로컬(§2.1–2.6)에 전부 정의·중복 없음. 수신형태도 원형과 일치: eq:xieq 의 $\xi_{\eq}=[1+e^{-\sigma_d(V-U^{\,d})/w}]^{-1}$ 에 $U^{\,d}\mapsto U^{\,d,\mathrm{cat}}$ 대입(§2.6(b)), eq:belliden $\dd\xi/\dd z=\xi(1-\xi)$·연쇄율 $\sigma_d/w_j$, eq:wbase $w=nRT/F$, eq:lco-Ubranch $U^{\,d,\mathrm{cat}}=U^\mathrm{cat}+\tfrac12\sigma_dh_\eta\gamma\Delta U^{\hys}$ — 전부 원문 그대로. (A20-M1 의 "§17.1(c)" 하드코딩 1건만 예외.)
2. **§2.6 대수 전건 재유도 일치**: eq:lco-charge 미분( $C_\bg+\sum Q\,\dd\xi/\dd V$ ), eq:lco-belliden($|\sigma_d|=1$ 절댓값 처리 포함), eq:lco-peakobs(위치 $=U^{\,d,\mathrm{cat}}$·순높이 $Q/4w$·면적 $Q$ — $\int_0^1\dd\xi=1$ 치환적분), eq:lco-eqpeak 조립. 흑연 §1.6 (a)–(d) 구조와의 대응도 1:1.
3. **§2.7 재모수화 대수(최중요 지시) 전건 재유도 일치**: eq:msmr→eq:lco-msmrnorm($\theta=x_j/X_j$, $\xi=1-\theta$ 지수 부호), eq:lco-comp($1-\xi^{(\sigma_d)}=\xi^{(-\sigma_d)}$), 계수비교 $f/\omega_j=\sigma_d/w_j$ ⟹ $f=+\sigma_d$ 유일성(pairing 하), 오류 경로 재현(점유=진행률 직접 등치 시 $f=-\sigma_d$ — 본문 가드 그대로), eq:lco-msmrpeak($|\dd\theta/\dd U|=(|f|/\omega)\theta(1-\theta)$, $\theta(1-\theta)=\xi(1-\xi)$ 여집합 불변). 차원 정합: $f/\omega_j$ [1/V] $=\sigma_d/w_j$ [1/V]. 원계열 $f=F/RT>0\leftrightarrow\sigma_d{=}{+}1$(탈리튬화 슬롯) 해석 일관.
4. **eq:lco-xmap(최중요 지시)**: 선형보간의 끝점 배정($\xi{=}0\leftrightarrow x_{\mathrm{hi},1}{=}0.94$, $\xi{=}1\leftrightarrow x_{\mathrm{lo},1}{=}0.75$)이 탈리튬화-형 진행률 규약(eq:lco-sigmaslot·§2.1)과 정합($x$ 감소 방향), 표~tab:lco-staging 의 T1 조성창과 일치, $x_\mathrm{MIT}{\approx}0.85$ 창 내부($\xi{=}\tfrac12\mapsto x{=}0.845$), tier C 선언 정직. 매핑 자체 무발견(경계 거동은 A20-M6 보완).
5. **전자항 plug-in 사슬 수치 전건 재계산 일치**: eq:lco-SeV = eq:dSegate×eq:gunit×eq:dSemolar 몰당 나눗셈형 조립 정확(유도 대조); 골 깊이 $-\tfrac{\pi^2}{3}R(k_BT/e_V)(g_{\max}/\Delta x)\tfrac14=-45.7$ J/(mol K)@298.15 K(§2.5 검산값·코드 시연 재현), $0.47$ mV/K$\,\times30$ K$\,=14$ mV$\,\lesssim w_1$, $N_A$ 누락 $\sim10^{23}$ 배($N_A=6.02\times10^{23}$), $e_V$ 곱셈 오용 $1/e_V^2=3.9\times10^{37}$ 배 — 전부 수치 재현. eq:lco-U1V = §2.2 Kirchhoff 적분형(eq:lco-kirchhoff)의 $V$-인수판, $T^2$ 곡률 $\tfrac12$ 인자 = eq:U1T2 와 정합. 사슬 박스 eq:lco-plugin 의 화살표 라벨-내용 대응 전건 확인.
6. **동결 근사 서술 = 구현 일치**: `Anode_Fit_v1.0.22.py:918–935` `_effective_dS_rxn` 이 $(x_\mathrm{center},T_\mathrm{ref}{=}298.15)$ 동결 상수 오프셋 — §2.7 "현행 모델" 서술과 정확 일치(docstring 의 "T-무관·선형 U(T)·다온도 과제 분리"까지 동일 취지).
7. **다리(srcbox) 원안 대조**: comp_R3 `br_msmr_lineage.tex` 와 통합본 축자 일치(드리프트 없음 — "§17.1(c)" 이월 포함, A20-M1 참조). 대응표 7행 내용·"방법 요지/가정 차" 구획이 P3-5 의 4항목(서지·사용 위치·수학 구조·변수 매핑·가정 차) 요건 충족. srcbox 자족성(제거 용이) 유지 확인.
8. **명칭 위계(P3-7)**: 두 절의 "Ch1/Chapter 1" 지칭·역사적 파일명(ch1_sec16/17)·신 구조(§2.6/2.7) 사이 혼동 서술 없음(A20-M1 외). "ver.N" 표기 자체는 두 절에 등장하지 않음.
9. **폭 이중지위·two-phase calibration 정합**: §2.6 "폭의 지위" 문단이 §1.5 이중지위·§1.7 broadening·§2.3 two-phase calibration(미배정·피팅 판정 위임)과 상충 없이 헤지됨("최종 지위 판정은 피팅된 $\Omega$" 괄호 존재). Ω/config 혼동 가드(§2.3)와도 무충돌.
10. **분기·방향 부호**: eq:lco-Ubranch 의 $\sigma_d$ 슬롯 수신(§2.6(b) 괄호)·"탈리튬화 가지 위" 기하 — §2.1 규약과 1:1. 종 $\xi(1-\xi)$ 의 방향 불변 서술 3곳(§2.6(b)·§2.7(c)·§2.1) 상호 일관.
11. **서지 사용처 정합**: §2.6 의 \cite{xia2007,reynier2004,motohashi2009} 는 표~tab:lco-staging anchor 의 재인용으로 위치 적절; §2.7 의 3키 계보 배치(원전→명명→온도 파라미터화) 는 bib 주석·원장 판정과 일치. 두 절에서 원장(V1) 밖 키 사용 없음.
12. **GS-1/GS-2(정직 공백)**: 두 절은 Ch3 소관 공백(GS-1 기계 히스·GS-2 블렌드 비가산)과 무접점 — 침해 제안 없음. G1–G3(Ch2 문헌 공백) 관련 서술도 "피팅 위임" 지위 그대로 존중(본 보고 제안 중 공백을 값으로 메우는 것 없음).

---

## 6. 말미 4-tier 분류

- **확정**(재유도·원문 대조로 닫힘): A20-H1(부호·방향 상충 — $a_e<0$ 원문 명시와 §2.5 신호 서술 대조), A20-M1(마스터 조립·라벨 존재 확인), A20-M2($x_\mathrm{center}$ 전 파일 grep 무정의 + 코드 정의 확인), A20-M4 의 단조성 대수($\dd\Delta U/\dd\Omega=2u/F$), A20-M6 의 수치($z_e$ 유계·잔존 42–49%), A20-M8 의 이득 상한($\approx0.20$), 무발견 축 1–12 전건.
- **추정**(개선 이득 판단이 주관 섞임 — 채택은 마스터 몫): A20-M3·M5·M7·M9 의 보강 필요성, L 전건(L1–L6), A20-M8 의 "각주로 실을 가치"(상한 자체는 확정, 지면 대비 이득은 추정).
- **미검증**(접근 한계 — 정직 표기): (i) msmr_origin2017 **원문 내** eq:msmr 식번호·기호 1:1 대조(프로젝트 원안도 "미완(경미)" 기록 — 2차 출처 일치까지만), (ii) 2017 원전 본문 안에 "multi-species, multi-reaction" 문구가 선행 등장하는지의 전문 대조(명명 원전 주장은 제목 수준에서 지지), (iii) xia2007/motohashi2009 **본문 figure** 의 peak 전위 수치 직접 대조(초록·공개 수준 정합까지 확인), (iv) 고정점 정밀형의 실제 수렴(문서 스스로 round-trip 위임 — A20-M8 은 상한 보강일 뿐 수치 확인 대체 아님).
- **무발견 축**: §5 의 1–12(각 항목에 검토 방법 명기).

## 7. 부수 관찰 (대상 밖 — 마스터 참고용, 제안 아님)

- `ch1_sec14_lcodecomp.tex:124` 에도 같은 유형의 구번호 하드코딩 "본문 §15"(신 구조 §2.5) 존재 — A20-M1 과 동일 계열, 담당 창 확인 요망.
- comp_R3 원안 `br_msmr_lineage.tex:44` 의 "§17.1(c)" — A20-M1 채택 시 원안 파일 동보정 여부는 마스터 판단(원안은 결과물 보존 원칙상 존치가 기본일 듯).
- §2.1 `ch1_sec11_lcointro.tex:168` 의 "MSMR 모델\cite{msmr_origin2017,msmr2024}은 **양극** 조성을…" — msmr2024 는 흑연(MCMB) 파라미터화 논문이라 "양극" 문장의 인용 짝으로는 msmr_origin2017 단독이 더 정확(§2.7 의 계보 배치는 정확함). 대상 밖이라 발견표에 넣지 않음.
