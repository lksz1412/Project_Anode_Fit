# A04_REVIEW — ch1_sec03_center.tex (§3 평형 중심 U_j(T), N2) 심층 검토

- 검토 창: FR-A04 (v1.0.22 대공사)
- 대상: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch1_sec03_center.tex` (전 120행 전문 정독)
- 규율 준수: 보고 전용 — 소스 수정 0건 · git 조작 0건 · `Codex/` 접근 0건
- 참조 원문 확인(read-only): `ch1_sec02b_part0.tex`(sec:sm-electro·sec:sm-macro·eq:sm-emu·eq:sm-refbal·eq:sm-muV·eq:sm-eqcond·eq:sm-nernst), `ch1_sec01_n0n1.tex`(tab:notation·s 규약·V_app/V_n·측정 박스), `ch1_sec00_intro.tex`(fig:spine 루프 N0–N9), `ch1_sec10_sum.tex`(tab:staging), `ch1_sec04_hys.tex`(eq:eqcond 인수 방식), `ch1_sec12_lcocenter.tex`(sec:lco-center), `ch1_sec17_msmr.tex`(sec:lco-code·전자항), `ch1_appA_signcheck.tex`, `ch1_appB_codemap.tex`, `ch1v22_bib.tex`, `common_preamble_v1022.tex`(매크로), `V1022_REFERENCE_LEDGER.md`(존재 확인)
- 표기: 발견 표의 현행/제안 열이 길면 표에는 첫 구절만 적고, **축자 원문(개행 포함 그대로)은 각 발견의 상세 블록(fenced) 이 기준**이다 — 기계 매칭은 상세 블록으로 할 것.

---

## 1. 발견 표 (BRIEF 양식)

| ID | 파일:행 | 유형 | 등급 | 현행(축자 — 상세 블록 기준) | 제안(완성 LaTeX — 상세 블록) | 근거 |
|----|---------|------|------|------------------------------|------------------------------|------|
| A04-01 | ch1_sec03_center.tex:30–38 | 논리(수식↔산문 불일치) | **H** | `\textbf{(c) 중간식 --- 상수 덩이를 중심으로 흡수.} 좌변에서 $-FV$ 만 …` | (c) 산문 재작성 — $C\equiv\mu^0+sFU$ 로 정의 명시 | 현행 정의문 "상수 덩이를 $sFU$ 로 정의"를 축자 적용하면 $\mu_\mathrm{Li}=-sF(V-U)$ 가 나와 표시식 \eqref{eq:eqcond} 의 $\mu^0$ 항을 재생하지 못함(재유도로 확정). Part 0 \eqref{eq:sm-eqcond} 의 실제 정의는 $U\equiv(\mu_\mathrm{Li}^\mathrm{metal}-\mu^0)/F$ |
| A04-02 | ch1_sec03_center.tex:30 | 보완 | M | `에서, 전자 항이 $z=-1$ 이라 측정 전위 $V$ 를 통해 …` | 기준극 결선 한 단계의 Part 0 cross-ref 추가 | \eqref{eq:sm-emu} 대로면 $\tilde\mu_{e^-}=\mu_{e^-}-F\phi_M$ — $\phi_M\to V$ 치환과 상수 흡수는 Part 0 \eqref{eq:sm-refbal}–\eqref{eq:sm-muV} 의 기준극 빼기가 근거인데 §3 에는 그 다리가 무언급(독자 질문 "φ가 왜 V 가 되나"에 답 없음) |
| A04-03 | ch1_sec03_center.tex:38 | 논리(용어 정합·P3-1) | M | `여기서 $s$ 는 방전 규약의 고정 부호 $+1$ 이고, …` | "유도 전용 고정 부호($\sigma_d$ 와 별개)"로 정정 + $U$ 환산의 부호 반전 명시 | 마스터표 tab:notation(§1:48)와 §1:32–34 는 $s$ 를 "유도 전용 고정 부호 — 방향에 따라 ±1 로 바뀌는 $\sigma_d$ 와 별개"로 규정. "방전 규약의"는 방전 방향 부호($\sigma_d{=}{+}1$)와 혼동을 유발 — §1 이 세운 방화벽을 흐림. 또 $U_j=-\Delta G_j/sF$ 의 부호 반전이 "환산"에 숨음 |
| A04-04 | ch1_sec03_center.tex:39–40 | 논리(암묵 가정) | M | `또한 $V$ 상승(전자 화학퍼텐셜 하락)$\Rightarrow$ 평형 점유율 하강 …` | 등온선 단조성($\Omega_j<2RT$) 전제 명시 | $V\!\uparrow\Rightarrow\mu_\mathrm{Li}\!\downarrow$ 까지는 식이 주지만 $\Rightarrow\theta_\eq\!\downarrow$ 는 $\partial\mu/\partial\theta>0$(단조 등온선)이 필요. 바로 다음 절(§4)이 다루는 $\Omega_j>2RT$ 비단조에서는 가지별로만 성립 — 전제 없는 일반 주장 |
| A04-05 | ch1_sec03_center.tex:38–39 | 설명 | M | `\textbf{(d) 부호 핵심.} … 곧 전이가 자발 진행할 전위가 양의 중심이다.` | Part 0(§sm-electro:182–183)의 명료한 독법으로 재서술 + $V\lessgtr U_j$ 창 명시 | 현행 문장은 통사가 꼬여("전위가 양의 중심이다") 독자가 막힘. Part 0 동일 지점의 독법("그 전이가 자발일 전위 창이 양수")이 이미 명료 — 결과 사슬 쪽도 같은 수준으로 |
| A04-06 | ch1_sec03_center.tex:57–59 | 보완 | M | `온도 의존은 식~\eqref{eq:Uj} 를 $T$ 로 미분한 …` | $(\Delta H,\Delta S)$ 온도 창 내 상수 전제 명시(§12 의 같은 지적과 정합) | \eqref{eq:Uj} 의 $T$-미분 경로는 $\Delta H,\Delta S$ 상수를 전제(그래서 직선), Gibbs 항등식 경로는 $T$-의존과 무관하게 정확 — 두 경로가 "같은 결과"인 것은 상수 전제 하에서만. §12(sec:lco-center:41)는 이 구분을 명시하는데 원 유도인 §3 이 침묵 |
| A04-07 | ch1_sec03_center.tex:61–62 | 보완 | M | `네 전이의 $U_j(T)$ 직선과 기울기 부호의 갈림은 그림~\ref{fig:UjT} 가 한 장에 보인다.` | 뒤에 1문장 추가 — 전이 중심 $\xi{=}\tfrac12$ 에서 배치·평균장 몫이 함께 0 이라 실측 엔트로피 계수 $\partial U_\oc/\partial T$ 가 곧 $\Delta S_{\rxn,j}/F$ | "다온도 피팅에서 $U_j(T)$ 를 따로 읽어야" 다음의 자연 질문 "$\Delta S_\rxn$ 입력은 어디서 오나"에 §3 이 무응답. \eqref{eq:sm-nernst}·§4 확장에서 $\xi{=}\tfrac12$ 대입으로 재유도 확인(로그·$\Omega(1{-}2\xi)$ 항 동시 소멸). §1 측정 박스·\cite{reynier2003}(DOI 실검증 완료 — §5) 재사용, 신규 서지 불요 |
| A04-08 | ch1_sec03_center.tex:56–57 | 설명 | L | `부호 --- 발열 반응 … 중심을 \emph{올린다}(흡열 아님에 주의).` | 결합 안정성 직관 1구 추가 재서술 | "(흡열 아님에 주의)"가 무엇을 경계하는지 불명 — 왜 발열이 중심을 올리는지(더 안정한 삽입일수록 더 높은 전위까지 자발) 물리 독법을 주면 경고가 자립 |
| A04-09 | ch1_sec03_center.tex:111–113 | 문체(표기 일관) | L | `… $U(298)=(13000-298.15\times16)/96485\approx0.0853$ V …` | $U(298.15\,\mathrm K)$ 로 통일 | 함수 인자는 298, 대입값은 298.15 — 사소 불일치. (수치 자체는 재계산 정합: $8229.6/96485=0.085294$ V ✓) |
| A04-10 | ch1_sec03_center.tex:113–114 | 수식화 | M | `구현 대응은 부록~\ref{sec:appendix-code} 에 둔다.` | 산출 경로 산문(108–111)을 cases 식으로 접어 보강(제안 라벨 `eq:Uj-path`) + LCO 전자항의 T1 스코프 정밀화 | 108–111행 산문의 분기(입력 유무·전극별 유효 $\Delta S$)는 cases 한 식이 더 정확·간결(구현 대응 검산 가능). 또 산문 "LCO 에서는 전자 엔트로피 항이 더해진다"는 §17 원문("T1 전이의 $\Delta S_\rxn$ 평가에")보다 넓게 읽힘 — 식에서 T1 명시 |
| A04-11 | ch1_sec03_center.tex:60–61 | 보완(P3-1) | M | `온도가 배열 $T(V)$(비등온)이면 $U_j$ 도 $V_n$ 점별 배열로 나온다.` | 유도의 $V$(평형·전류 0) ↔ 루프 평가 좌표 $V_n$ 다리 1구 추가 | §3 유도 본문의 $V$ 는 "측정 전위"로 도입되는데 §1 keybox 는 측정=$V_\app$·루프 평가=$V_n$ 로 위계를 세움. 유도의 $V$ 가 루프에서 $V_n$ 자리에 선다는 다리가 없으면 전위 위계(P3-1) 독해가 한 번 끊김 |
| A04-12 | ch1_sec03_center.tex:59–60 | 보완 | L | `$|\Delta S_\rxn|\sim$ 수$\sim$수십 J/(mol\,K) 라 $30$ K 창에서 수 mV 규모로 중심이 이동한다 …` | $\Delta S_\rxn{=}0$ 전이(3→2L)는 불변임을 1구 병기 | 표 tab:staging 의 3→2L 은 $\Delta S{=}0$ — "이동한다" 일반 서술의 예외. 그림 캡션은 명시하는데 본문은 침묵 |

---

## 2. 발견 상세 (축자 현행 + 완성 LaTeX 제안)

### A04-01 (H · 논리 — 산문 정의가 표시식을 재생하지 못함) — :30–38

**현행 (축자):**
```latex
\textbf{(c) 중간식 ---
상수 덩이를 중심으로 흡수.} 좌변에서 $-FV$ 만 전위 의존이고 나머지(Li$^+$ 활동도$\cdot$기준 퍼텐셜)는 주어진 $T$ 에서
상수이므로, 그 상수 덩이를 $sFU$ 로 정의해($s=+1$ 라 $-FV=-sFV$) 묶으면 평형 조건이
\begin{equation}
\mu_\mathrm{Li}(\theta_\eq)\;=\;\mu^0-sF\,(V-U),
\qquad \Delta G_j\;=\;-sF\,U_j
\label{eq:eqcond}
\end{equation}
형태가 된다.
```

**재유도 검증(오류 확정 근거):** 좌변 상수 덩이를 $C$ 라 하면 평형은 $C-sFV=\mu_\mathrm{Li}(\theta_\eq)$. 현행 산문대로 $C\equiv sFU$ 를 대입하면 $\mu_\mathrm{Li}=-sF(V-U)$ — 표시식의 $\mu^0$ 가 나오지 않는다. \eqref{eq:eqcond} 가 성립하려면 $C\equiv\mu^0+sFU$(곧 $U=(C-\mu^0)/F$)여야 하며, 이것이 Part 0 \eqref{eq:sm-eqcond} 의 실제 정의($C=\mu_\mathrm{Li}^\mathrm{metal}$, $U\equiv(\mu_\mathrm{Li}^\mathrm{metal}-\mu^0)/F$, $\Delta G_j\equiv\mu^0-\mu_\mathrm{Li}^\mathrm{metal}$)와 정확히 일치한다. 또한 현행 \eqref{eq:eqcond} 둘째 관계식의 $\Delta G_j$ 는 §3 안에서 기호로 정의된 적이 없다(Part 0 428–429행은 명시). **식 자체는 옳다 — 고칠 것은 산문 정의뿐.**

**제안 (대체 — 식·라벨 불변):**
```latex
\textbf{(c) 중간식 ---
상수 덩이를 중심으로 흡수.} 좌변에서 $-FV$ 만 전위 의존이고 나머지(Li$^+$ 활동도$\cdot$기준 퍼텐셜)는 주어진 $T$ 에서
상수 $C$ 이므로 좌변은 $C-sFV$ 다($s=+1$ 라 $-FV=-sFV$). 이 $C$ 에서 host 기준 $\mu^0$ 를 뗀 나머지를 $sFU$ 로
정의하면 --- $C\equiv\mu^0+sFU$, 곧 $\Delta G_j\equiv\mu^0-C=-sF\,U_j$(Part 0 식~\eqref{eq:sm-eqcond} 은 같은 정의를
$C=\mu_\mathrm{Li}^\mathrm{metal}$ 로 구체화한다) --- 평형 조건이
\begin{equation}
\mu_\mathrm{Li}(\theta_\eq)\;=\;\mu^0-sF\,(V-U),
\qquad \Delta G_j\;=\;-sF\,U_j
\label{eq:eqcond}
\end{equation}
형태가 된다.
```
검산: $C-sFV=\mu^0+sFU-sFV=\mu^0-sF(V-U)$ ✓; $\Delta G_j=\mu^0-C=-sFU_j$ ✓ — 두 표시 관계가 산문에서 문자 그대로 따라 나온다.

### A04-02 (M · 보완 — 전자항 압축 단계의 기원 무언급) — :30

**현행 (축자):**
```latex
에서, 전자 항이 $z=-1$ 이라 측정 전위 $V$ 를 통해 $\tilde\mu_{e^-}=\mu_{e^-}^0-FV$ 로 들어온다.
```

**제안 (대체):**
```latex
에서, 전자 항이 $z=-1$ 이라 측정 전위 $V$ 를 통해 $\tilde\mu_{e^-}=\mu_{e^-}^0-FV$ 로 들어온다(전극 정전
퍼텐셜 $\phi_M$ 이 기준극 결선으로 측정 전위 $V$ 가 되고 결선 상수가 $\mu_{e^-}^0$ 에 흡수되는 한 단계는
Part 0 식~\eqref{eq:sm-refbal}--\eqref{eq:sm-muV} 가 닫아 두었다).
```

**근거:** \eqref{eq:sm-emu}($\tilde\mu\equiv\mu+zF\phi$)를 그대로 적용하면 $\tilde\mu_{e^-}=\mu_{e^-}-F\phi_M$ 이다. $\phi_M\to V$ 는 기준 Li 극의 자기 평형 \eqref{eq:sm-refbal} 을 빼는 조작(→\eqref{eq:sm-muV})의 산물인데, §3 은 이 유도를 "한 단계씩 닫는다"고 선언(:6–7)하면서 이 한 단계만 무근거 축약한다. Part 0 정독을 마친 독자는 넘어가지만, 결과 사슬만 읽는 독자(문서가 명시 허용하는 독법)는 여기서 막힌다. 라벨 실재 확인: `eq:sm-refbal`(sec02b:160)·`eq:sm-muV`(sec02b:169) ✓.

### A04-03 (M · 논리 — $s$ 성격 오기·$U$ 환산 부호 gloss) — :38

**현행 (축자):**
```latex
여기서 $s$ 는 방전 규약의 고정 부호 $+1$ 이고, $U$ 는 비배치 몫 자유에너지를 전위로 환산한 값이다.
```

**제안 (대체):**
```latex
여기서 $s$ 는 유도 전용 고정 부호 $+1$(방향 부호 $\sigma_d$ 와 별개 --- 표~\ref{tab:notation} 규약)이고,
$U$ 는 비배치 몫 반응 자유에너지 $\Delta G_j$ 를 부호 반전해 전위로 환산한 값($U_j=-\Delta G_j/sF$)이다.
```

**근거:** ① 마스터표 tab:notation(§1:48) 원문 = "유도 전용 고정 부호 — 항상 +1(…); **방향에 따라 ±1 로 바뀌는 $\sigma_d$ 와 별개**". §1:32–34 본문도 동일. "방전 규약의 고정 부호"는 방전 방향 규약($\sigma_d$)에 $s$ 를 귀속시키는 표현이라, §1 이 반복 강조한 $s$–$\sigma_d$ 방화벽(P3-1 부호 위계)을 §3 이 스스로 흐린다. ② $U_j=-\Delta G_j/sF$: "환산한 값"에 숨은 부호 반전을 명시해야 (d) 의 "$U_j$ 양 ⇔ $\Delta G_j$ 음" 독법이 한 눈에 닫힌다.

### A04-04 (M · 논리 — 단조성 암묵 가정) — :39–40

**현행 (축자):**
```latex
또한 $V$ 상승(전자 화학퍼텐셜 하락)$\Rightarrow$
평형 점유율 하강, 곧 ``$V$ 를 올리면 탈리튬화''가 이 한 식에 이미 들어 있다(\S\ref{sec:width} 의 logistic 부호로 회수).
```

**재유도:** 식이 직접 주는 것은 $V\!\uparrow\Rightarrow\mu_\mathrm{Li}(\theta_\eq)\!\downarrow$ 까지다. $\Rightarrow\theta_\eq\!\downarrow$ 로 가려면 $\partial\mu_\mathrm{Li}/\partial\theta>0$(등온선 단조)이 필요하고, 이는 $\Omega_j<2RT$ 에서만 무조건 성립한다(\eqref{eq:mu}·\eqref{eq:sm-thresh}). $\Omega_j>2RT$(바로 다음 절 §4 의 주제)에서는 한 $\mu$ 에 세 $\theta$ 가 대응(Part 0 fig:sm-mu 캡션)하므로 안정 가지별로만 성립한다.

**제안 (대체):**
```latex
또한 $V$ 상승(전자 화학퍼텐셜 하락)$\Rightarrow$
평형 점유율 하강, 곧 ``$V$ 를 올리면 탈리튬화''가 이 한 식에 이미 들어 있다(등온선이 단조인 $\Omega_j<2RT$
창 기준 --- $\Omega_j>2RT$ 의 비단조면 안정 가지별로 성립, \S\ref{sec:hys}; \S\ref{sec:width} 의 logistic 부호로 회수).
```

### A04-05 (M · 설명 — 통사가 꼬인 부호 독법) — :38–39

**현행 (축자):**
```latex
\textbf{(d) 부호 핵심.} $\Delta G_j=-sFU_j$ ---
$U_j$ 가 양이면 $\Delta G_j<0$, 곧 전이가 자발 진행할 전위가 양의 중심이다.
```

**제안 (대체 — 어조 동일):**
```latex
\textbf{(d) 부호 핵심.} $\Delta G_j=-sFU_j$ ---
$U_j$ 가 양이면 $\Delta G_j<0$, 곧 그 전이가 자발일 전위 창(vs Li/Li$^+$)이 양수라는 뜻이다: 삽입은
$V<U_j$ 에서, 탈리튬화는 $V>U_j$ 에서 자발이고, $U_j$ 가 그 갈림의 \emph{중심}이다.
```

**근거:** 현행 "전이가 자발 진행할 전위가 양의 중심이다"는 주술 호응이 어긋나 독자가 막히는 문장. Part 0 같은 지점(sec02b:182–183)의 독법("$U_j>0\Leftrightarrow\Delta G_j<0$, 곧 그 전이가 자발일 전위 창이 양수")이 이미 명료하므로 결과 사슬 쪽도 같은 수준으로. 재유도 검증: 삽입 구동력 $=[\mu^0-sF(V-U_j)]-\mu_\mathrm{Li}(\theta)$, 중심 점유 $\theta{=}\tfrac12$ 에서 $\mu_\mathrm{Li}=\mu^0$ 이므로 구동력 $=-sF(V-U_j)>0\Leftrightarrow V<U_j$ ✓ — "갈림의 중심" 표현은 절 제목의 '중심'과도 맞물린다.

### A04-06 (M · 보완 — 직선의 상수 전제 무언급) — :57–59

**현행 (축자):**
```latex
온도 의존은 식~\eqref{eq:Uj} 를
$T$ 로 미분한 $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ 이며, 이는 Gibbs 항등식 $\partial\Delta G/\partial T=-\Delta S$ 와
식~\eqref{eq:eqcond} 의 $\Delta G=-FU$ 를 잇는 것과 같은 결과다.
```

**제안 (대체):**
```latex
온도 의존은 식~\eqref{eq:Uj} 를
$T$ 로 미분한 $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ 이며, 이는 Gibbs 항등식 $\partial\Delta G/\partial T=-\Delta S$ 와
식~\eqref{eq:eqcond} 의 $\Delta G=-FU$ 를 잇는 것과 같은 결과다(항등식 쪽은 $\Delta S$ 의 $T$-의존 여부와
무관하게 정확하고 --- \S\ref{sec:lco-center} 의 같은 지적 --- 직선 $U_j(T)$ 는 입력 $(\Delta H_\rxn,\Delta S_\rxn)$
을 온도 창 안 상수로 두는 전제의 표현이다; $\Delta S_\rxn(T)$ 면 직선이 굽되 점별 기울기 관계는 그대로다).
```

**근거:** \eqref{eq:Uj} 미분 경로는 $(\Delta H,\Delta S)$ 상수를 암묵 전제(그래서 그림 fig:UjT 가 직선), Gibbs 항등식 경로는 전제 불요 — "같은 결과"는 상수 전제 하에서만 등치다. §12(sec:lco-center:41 — "$\Delta S$ 의 $T$-의존 여부와 무관하게 성립하는 정확한 항등식")가 이 구분을 이미 세워 두었으므로, 원 유도인 §3 에 한 구 명시가 두 절의 정합을 닫는다. LCO 전자항의 $T^2$ 곡률(§17 \eqref{eq:U1T2})이 실제로 이 "직선이 굽는" 경우라 예고 가치도 있다.

### A04-07 (M · 보완 — $\Delta S_\rxn$ 입력의 실측 연결 무응답) — :61–62 뒤 추가

**현행 (축자 — anchor):**
```latex
네 전이의 $U_j(T)$ 직선과 기울기 부호의 갈림은
그림~\ref{fig:UjT} 가 한 장에 보인다.
```

**제안 (보강 — anchor 문장 유지 후 1문장 추가):**
```latex
네 전이의 $U_j(T)$ 직선과 기울기 부호의 갈림은
그림~\ref{fig:UjT} 가 한 장에 보인다. 이 기울기는 실측과 곧장 만난다 --- 전이 중심 $\xi=\tfrac12$ 에서는
배치 몫(로그 항)과 평균장 몫($\Omega_j$ 항)이 함께 $0$ 이라(식~\eqref{eq:sm-nernst} 와 그 \S\ref{sec:hys}
확장 공히), 고정 조성에서 온도를 바꿔 재는 전위차 엔트로피법(\S\ref{sec:notation} 의 측정 원리 박스)의
$\partial U_\oc/\partial T$ 가 중심에서 곧 $\Delta S_{\rxn,j}/F$ 다 --- 다온도 피팅의 $\Delta S_\rxn$ 입력을
실측\cite{reynier2003} 에서 출발시킬 수 있는 근거다.
```

**재유도 검증:** $V_\eq(\xi)=U_j+\frac{RT}{sF}\ln\frac{\xi}{1-\xi}+\frac{\Omega_j}{sF}(1-2\xi)$(\eqref{eq:sm-nernst}+§4 확장)에서 $\xi{=}\tfrac12$ 대입: 로그 항 $=0$, $(1-2\xi)=0$ → $V_\eq=U_j$ 정확. $\partial V_\eq/\partial T|_{\xi=1/2}=\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ — $\Omega_j$ 의 $T$-의존조차 $(1-2\xi){=}0$ 에 곱해져 소멸하므로 중심에서는 무전제로 성립 ✓. §1 bgbox(엔트로피 계수 실측 \cite{reynier2003,swiderska2019})와 연결되며 신규 서지 불요(기존 키 재사용 — DOI 실검증은 §5).

### A04-08 (L · 설명) — :56–57

**현행 (축자):**
```latex
부호 --- 발열 반응
$\Delta H_\rxn<0$ 이면 분자 $-\Delta H_\rxn>0$ 이 중심을 \emph{올린다}(흡열 아님에 주의).
```

**제안 (대체):**
```latex
부호 --- 발열 반응
$\Delta H_\rxn<0$ 이면 분자 $-\Delta H_\rxn>0$ 이 중심을 \emph{올린다} --- 삽입이 더 발열일수록(더 안정한
결합일수록) 더 높은 전위까지 삽입이 자발이라는 뜻이니, ``높은 중심 $=$ 흡열''로 오독하지 않도록 주의.
```

**근거:** 현행 괄호 경고는 무엇을 왜 경계하는지 자립적으로 읽히지 않는다. 물리 독법(안정 결합 ↔ 높은 자발 창 상한 $U_j$ — A04-05 의 $V<U_j$ 창과 동일 논리)을 한 구 주면 경고가 저절로 선다. appA 검산표(:24 "흡열 아님")와 충돌 없음(같은 방향 보강).

### A04-09 (L · 문체 — 표기 불일치) — :111–113

**현행 (축자):**
```latex
수치 예시로 stage $2\to1$ 의 초기값
$\Delta H_\rxn=-13000$ J/mol, $\Delta S_\rxn=-16$ J/(mol\,K)를 넣으면
$U(298)=(13000-298.15\times16)/96485\approx0.0853$ V 로 목표 $0.085$ V 와 정합한다.
```

**제안 (대체):**
```latex
수치 예시로 stage $2\to1$ 의 초기값
$\Delta H_\rxn=-13000$ J/mol, $\Delta S_\rxn=-16$ J/(mol\,K)를 넣으면
$U(298.15\,\mathrm K)=(13000-298.15\times16)/96485\approx0.0853$ V 로 목표 $0.085$ V 와 정합한다.
```

**근거:** 함수 인자(298)와 대입값(298.15) 불일치. 수치는 재계산 정합: $298.15\times16=4770.4$, $8229.6/96485=0.085294$ V ✓ (표 tab:staging 의 $U{=}0.085$·§10 의 "$U(298)$ 정합" 서술과도 일치 — §10 쪽 동일 표기는 그쪽 검토 창 소관).

### A04-10 (M · 수식화 — 산출 경로 cases 식) — :113–114

**현행 (축자 — anchor):**
```latex
구현 대응은
부록~\ref{sec:appendix-code} 에 둔다.
```

**제안 (보강 — anchor 앞에 삽입, 신규 라벨 제안 표기 `eq:Uj-path`):**
```latex
같은 경로를 한 식으로 접으면
\begin{equation}
U_j(T)=
\begin{cases}
\bigl(-\Delta H_{\rxn,j}+T\,\Delta S^{\mathrm{eff}}_{\rxn,j}\bigr)/F, & (\Delta H_{\rxn,j},\Delta S_{\rxn,j})\ \text{입력}
\quad(\text{비등온: 배열 } T \text{ 점별}),\\[3pt]
U_j\ \text{직접 입력}, & \text{그 외},
\end{cases}
\qquad
\Delta S^{\mathrm{eff}}_{\rxn,j}=
\begin{cases}
\Delta S_{\rxn,j}, & \text{흑연(항등)},\\[2pt]
\Delta S_{\rxn,j}+\Delta S_{e,1}^{\,\mathrm{mol}}, & \text{LCO T1 전이(\S\ref{sec:lco-code})},
\end{cases}
\label{eq:Uj-path}
\end{equation}
구현 대응은
부록~\ref{sec:appendix-code} 에 둔다.
```

**근거:** 108–111행 산문의 이중 분기(입력 유무 / 전극별 유효 엔트로피)는 cases 한 식이 더 정확·간결하고 부록 코드 대응(appB:75 `U` 또는 `(dH_rxn,dS_rxn)`)과 1:1 검산 가능해진다. 부가 정밀화: 산문 "LCO 에서는 전자 엔트로피 항이 더해진다"는 §17 원문(:118 "**T1 전이의** $\Delta S_\rxn$ 평가에 몰당 전자항") 대비 스코프가 넓게 읽힘 — 식은 문서 자신의 기호 $\Delta S_{e,1}^{\,\mathrm{mol}}$(\eqref{eq:lco-SeV}·\eqref{eq:dSemolar})와 T1 한정을 그대로 쓴다. 기존 산문은 유지(대체 아님·보강)로 P5 충족.

### A04-11 (M · 보완 — 전위 위계 다리, P3-1) — :60–61

**현행 (축자):**
```latex
온도가 배열
$T(V)$(비등온)이면 $U_j$ 도 $V_n$ 점별 배열로 나온다.
```

**제안 (대체):**
```latex
온도가 배열
$T(V)$(비등온)이면 $U_j$ 도 $V_n$ 점별 배열로 나온다(이 절 유도의 $V$ 는 전류 $0$ 의 평형 전위이고, 루프
평가에서 그 자리에 서는 것은 분극을 벗긴 내부 전위 $V_n$ 이다 --- \S\ref{sec:pointwise} 의 점별 원칙).
```

**근거:** §3 유도부는 $V$ 를 "측정 전위"로 도입(:30)하는데, §1 의 위계에서 측정 전위 $=V_\app$, "평형 열역학이 사는 전위" $=V_n$(§1:160–161)이며 keybox(:199–201)는 루프의 모든 물리량이 $V_n$ 위에서 평가된다고 못 박는다. 평형 유도(전류 0)에서는 두 전위가 일치($|I|\to0$ 에서 $V_n=V_\app$, \eqref{eq:vn})하므로 유도 자체는 무결 — 다리 한 구가 없을 뿐이다. P3-1(전위 위계 일관성) 게이트 대응. ($T$ 가 "$V_\app$ 길이 배열"이라는 tab:notation 규정에 맞춰 현행 "$T(V)$" 표기는 유지했다.)

### A04-12 (L · 보완) — :59–60

**현행 (축자):**
```latex
$|\Delta S_\rxn|\sim$ 수$\sim$수십 J/(mol\,K) 라 $30$ K
창에서 수 mV 규모로 중심이 이동한다 --- 다온도 피팅에서 온도마다 $U_j(T)$ 를 따로 읽어야 하는 이유다.
```

**제안 (대체):**
```latex
$|\Delta S_\rxn|\sim$ 수$\sim$수십 J/(mol\,K) 라 $30$ K
창에서 수 mV 규모로 중심이 이동한다($\Delta S_\rxn=0$ 이면 불변 --- 표~\ref{tab:staging} 의 $3\!\to\!2\mathrm L$
이 그 경우다) --- 다온도 피팅에서 온도마다 $U_j(T)$ 를 따로 읽어야 하는 이유다.
```

**근거:** 네 전이 중 하나(3→2L, $\Delta S{=}0$)는 일반 서술의 예외인데 본문은 침묵(그림 캡션만 명시). 수치 재계산: $30$ K 이동 폭 $=30\,\Delta S/F$ → $+29$: $9.0$ mV, $-16$: $5.0$ mV, $-5$: $1.6$ mV, $0$: $0$ — "수 mV" 서술은 비영 전이에서 ✓.

---

## 3. 등급별 정리

**H (1건 — 논리/물리 오류·오귀속):**
- A04-01 — (c) 상수 덩이 정의 산문이 표시식 \eqref{eq:eqcond} 를 재생하지 못함($\mu^0$ 누락). 식은 옳고 산문만 오류 — Part 0 \eqref{eq:sm-eqcond} 정의로 정렬하는 산문 대체 제안.

**M (8건 — 의미·이해 실질 개선):**
- A04-02 — (b) $\phi_M\to V$ 결선 단계의 Part 0 cross-ref 누락(압축 유도의 기원 명시).
- A04-03 — $s$ "방전 규약" 오기(마스터표 "유도 전용"·$\sigma_d$ 방화벽) + $U$ 환산 부호 반전 명시. P3-1.
- A04-04 — "$V\!\uparrow\Rightarrow\theta_\eq\!\downarrow$"의 단조성($\Omega_j<2RT$) 암묵 가정 — §4 비단조와의 경계 명시.
- A04-05 — (d) 통사 꼬인 부호 독법 문장 재서술($V\lessgtr U_j$ 자발 창 + "갈림의 중심").
- A04-06 — 직선 $U_j(T)$ 의 $(\Delta H,\Delta S)$ 상수 전제 명시(§12 의 같은 지적과 정합·§17 $T^2$ 곡률 예고).
- A04-07 — 전이 중심 $\xi{=}\tfrac12$ 에서 실측 엔트로피 계수 $=\Delta S_{\rxn,j}/F$ 연결 1문장(기존 \cite{reynier2003} 재사용).
- A04-10 — 산출 경로 산문의 cases 수식화(제안 라벨 `eq:Uj-path`) + LCO 전자항 T1 스코프 정밀화.
- A04-11 — 유도의 $V$ ↔ 루프 평가 $V_n$ 다리(P3-1 전위 위계).

**L (3건 — 문체):**
- A04-08 — "(흡열 아님에 주의)" 자립화(결합 안정성 직관).
- A04-09 — $U(298)$ vs $298.15$ 표기 통일.
- A04-12 — $\Delta S{=}0$ 전이(3→2L) 예외 1구 병기.

---

## 4. 재계산 검증 기록 (관점 ② 전수 — 무발견 포함)

**(V1) 유도 사슬 재유도.** \eqref{eq:gibbsdef}→\eqref{eq:mudef}→\eqref{eq:eqbalance}: 반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}$ 의 $\delta G=[\tilde\mu_\mathrm{Li}-\tilde\mu_{\mathrm{Li}^+}-\tilde\mu_{e^-}]\dd n=0$ — 생성물−반응물 부호 ✓. \eqref{eq:eqcond}(식 자체)→\eqref{eq:Ujmid}→\eqref{eq:Uj} 이항·부호 ✓($\Delta H-T\Delta S=-FU_j\Rightarrow U_j=(-\Delta H+T\Delta S)/F$). $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ 두 경로(직접 미분·Gibbs 항등식) 일치 ✓(단 상수 전제 구분 → A04-06). Part 0 \eqref{eq:sm-eqcond}·\eqref{eq:sm-nernst} 와 글자 대조 — $U$·$\Delta G_j$ 정의 동일 ✓(산문 층위만 A04-01).

**(V2) 그림 fig:UjT 좌표 전수 재계산** (tab:staging 대입, $U(T)=(-\Delta H+T\Delta S)/F$, mV):

| 전이 | $(\Delta H,\Delta S)$ | $U(268)$ 계산 | 그림 | $U(328)$ 계산 | 그림 | 판정 |
|------|------|------|------|------|------|------|
| 4→3 | $-11700,+29$ | 201.814 | 201.81 | 219.847 | 219.85 | ✓ |
| 3→2L | $-13500,0$ | 139.918 | 139.92 | 139.918 | 139.92 | ✓ |
| 2L→2 | $-13100,-5$ | 121.884 | 121.88 | 118.775 | 118.77 | ✓(반올림 경계 0.005 mV) |
| 2→1 | $-13000,-16$ | 90.293 | 90.29 | 80.344 | 80.34 | ✓ |

범례 기울기: $29/F=0.3006$→"+0.301" ✓ · $5/F=0.0518$→"−0.052" ✓ · $16/F=0.1658$→"−0.166" ✓. 기울기 화살표 2건의 기하 기울기($2.4/8{=}0.300$·$-1.3/8{=}-0.163$) — 해당 직선과 정합 ✓. 캡션 수치 주장("수십 $\mu$V/K$\sim$0.3 mV/K"·"60 K 창 수$\sim$수십 mV"[3.1–18.0 mV]) ✓. 본문 "30 K 창 수 mV"(1.6–9.0 mV) ✓. 범례 상자 위치(y≈156–188)와 4→3(x=293 에서 209.3)·3→2L(139.9) 직선 비중첩 ✓.

**(V3) 수치 예시.** $U=(13000-298.15\times16)/96485=0.085294$ V ✓ ≈0.0853 ✓, 표 목표 0.085 ✓ (표기만 A04-09). 표 4행 전이의 $U(298.15)$ 역검산: 0.2109/0.1399/0.1203/0.0853 — 표 $U$ 열과 ±1 mV 정합, 4→3 만 자리수 경계(§10 캡션 자기 인지와 일치) ✓.

**(V4) 참조 무결성.** `eq:sm-emu`·`sec:sm-ensemble`·`sec:sm-electro`·`sec:sm-macro`·`sec:width`·`sec:hys`·`sec:lco-code`(=§17)·`sec:appendix-code`(=appB)·`tab:staging`(=§10:31) 전 라벨 실재 ✓. §17 이 실제로 "T1 전이 $\Delta S_\rxn$ 에 몰당 전자항 가산"을 수행 ✓(:118·\eqref{eq:lco-SeV}). appB 구현 대응 행 실재 ✓(:75). 매크로 `\eq`·`\rxn`·`\bg`·`\cell`·`\hys` 프리앰블 정의 확인 ✓. "전이 루프 안의 첫 물리량" — fig:spine 에서 N0·N1 은 루프 밖 1회 실행, N2 가 파선 상자(per-transition loop) 첫 노드 ✓. boxed 식 $s$ 소멸 규약(§1:34) — \eqref{eq:Uj} 에 $s$ 없음 ✓(\eqref{eq:eqcond} 는 비박스라 유지 — 규약 정합). §4 전환문("$\mu$ 에 상호작용 몫")은 §4 \eqref{eq:gxi}·$\Omega$ 구조와 정합 ✓.

---

## 5. 서치 절 (하이쿠 서브에이전트 위임 결과 — DOI 실검증분만)

위임: Agent(model: haiku) 1회 — 본 절 인용 사슬의 두 anchor DOI 실검증(crossref fetch). **기억 서지 사용 0건.**

| # | DOI | fetch | 실검증 서지 | bib 원문과 일치 |
|---|-----|-------|-------------|------------------|
| 1 | 10.1016/S0378-7753(03)00285-4 | 성공 | Y. Reynier, R. Yazami, B. Fultz, "The entropy and enthalpy of lithium intercalation into graphite," *J. Power Sources* **119–121**, 850–855 (2003) | **일치**(ch1v22_bib.tex:29 완전 일치) |
| 2 | 10.1103/PhysRevB.44.9170 | 성공 | J. R. Dahn, "Phase diagram of Li$_x$C$_6$," *Phys. Rev. B* **44**(17), 9170–9177 (1991) | **일치**(bib 는 시작 페이지 9170 만 표기 — 실질 일치) |

**Reynier 2003 초록(실확보 원문) 요지와 본문 정합:** 초록 원문 — "*The entropy of intercalation changed sign at higher lithium concentrations*" (저조성 양수 → 고조성 음수 부호 전환; 혼합 성분+진동 성분 경쟁), "*The enthalpy of intercalation into graphite is consistently negative, but becomes less so with higher lithium concentrations*".
- ① tab:staging 의 $\Delta S_\rxn$ 부호 패턴($+29\to0\to-5\to-16$, 리튬화 진행 방향 단조 감소·부호 전환)은 초록의 부호 전환 서술과 **정성 정합** — §10 tier 주석("부호·스케일 anchor, 전이별 정밀값 아님")의 주장 범위 안에서 확인 ✓. A04-07 제안이 이 기존 키를 재사용하는 근거.
- ② 관찰(주의 기록): 초록의 $\Delta H$ 경향("고조성일수록 덜 음수")과 표의 $\Delta H_\rxn$ 배열($-11700$[저조성 쪽] → $-13000$[고조성 쪽])은 방향이 다르다. 단, 문서는 $\Delta H$ 에 대해 reynier2003 anchor 를 **주장하지 않으며**($U(298)$ 정합 역산으로 명시, §10:48–49), $U$ anchor(Dahn/Ohzuku)와 $\Delta S$ 부호를 함께 고정하면 $\Delta H=T\Delta S-FU$ 로 산술 종속된다 — 오귀속 아님. 전이별 1차 대조는 원문 본문 열람이 필요해 본 검토 범위 밖(→ 미검증 tier).

신규 문헌 필요 발견: **없음** — 본 절의 모든 정량 주장은 기존 원장 인용(dahn1991·ohzuku1993·reynier2003, 표 tab:staging 경유)으로 커버되고, 제안(A04-07) 역시 기존 키 재사용으로 충분.

---

## 6. 무발견 축 (검토했으나 문제 없음 — 명시)

- **수치·좌표(관점 ②)**: 그림 fig:UjT 8개 끝점·범례 3개 기울기·화살표 2건·캡션 정량 주장·본문 30 K 추산·수치 예시 — 전수 재계산 일치(§4 V2·V3). 그림-표-본문 3자 정합 무결.
- **부호 사슬**: \eqref{eq:eqbalance} 부호 → \eqref{eq:eqcond}(식) → \eqref{eq:Ujmid} → \eqref{eq:Uj} → $\partial U_j/\partial T$ — 오류 없음. appA 검산표와 충돌 없음.
- **P3-2(전하 보존 중심식)**: 본 절은 U_j 를 파라미터로 산출할 뿐 "OCV 에서 읽는 흐름"으로의 회귀 없음 ✓.
- **P3-7(명칭)**: 본 절에 ver.N 표기 자체가 없어 혼동 소지 없음 ✓ (N2 태그는 spine 루프·§18 표와 일관).
- **P5**: 본 보고서의 전 제안은 대체·보강뿐 — 기존 기호·라벨·식 번호·절 구조 삭제/개명 제안 0건. `eq:Uj-path` 는 신규 라벨 "제안 표기".
- **GS-1/GS-2**: Ch3(Si) 소관 정직 공백 — 본 절과 무관, 메우기 제안 없음.
- **제거 용이 블록**: 본 절에 bgbox 증축분 없음(자산 주석 [A-075]–[A-085]·[V21-R-01] 확인) — 독립성 쟁점 없음.
- **중복 서술**(도입:5–6 ↔ :108–109 북엔드, 본문:59–60 ↔ 캡션:101–102)은 문서 관례(결과 사슬 요약 반복)로 판단 — 삭제 제안은 BRIEF 금지 조항에 따라 내지 않음.

---

## 7. 말미 4-tier

- **확정(재계산·원문 대조로 검증됨)**: A04-01(대수 재유도로 산문↔식 불일치 확정) · A04-03(tab:notation 원문 대조) · A04-04(단조성 필요조건 — \eqref{eq:mu} 비단조 사례로 확정) · A04-09(표기 대조) · §4 재계산 전수 무발견 · §5 DOI 2건 실검증 일치.
- **추정(개선 이득 판단 포함 — 물리·수학은 검증됨, 채택 여부는 마스터 몫)**: A04-02 · A04-05 · A04-06 · A04-07(수학 재유도는 확정, 문장 추가의 편익 판단이 추정) · A04-08 · A04-10 · A04-11 · A04-12.
- **미검증**: tab:staging 전이별 $(\Delta H_\rxn,\Delta S_\rxn)$ 의 문헌 1차 정밀 대조(Reynier 원문 본문 열람 불요건 — 문서 스스로 tier B "전이별 정밀값 아님" 선언과 정합; §5-② $\Delta H$ 경향 관찰만 기록) · 본 절 tikz 의 실제 컴파일 렌더(빌드 미실행 — 보고 전용 규율; 좌표·중첩은 수치로만 검산).
- **무발견 축**: §6 명시 목록 참조.

*(검토 종료 — FR-A04. 이 파일이 유일 산출물이며 소스는 건드리지 않았다.)*
