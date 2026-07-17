# A02_REVIEW — ch1_sec02a_part0.tex 심층 검토 (FR-A02)

- 검토 창: FR-A02 (v1.0.22 대공사 심층 검토, BRIEF_FR_A.md 규율 준수 — **보고 전용**, 소스 무수정·git 무조작·`Codex/` 미접근)
- 대상: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch1_sec02a_part0.tex` (**전문 정독**, 1–392행 전체)
- 소속 빌드: `ch1_graphite_v1.0.22.tex` — §1.2 Part 0 전반부 (2.1 앙상블 / 2.2 단일 자리 / 2.3 lattice gas)
- 참조 원문 확인(read-only): `ch1_sec02b_part0.tex`(sm-mf·sm-electro·sm-mc·sm-macro 전문), `ch1_sec03_center.tex`(전문), `ch1_sec04_hys.tex`(1–110행: eq:Veq·eq:spinodal), `ch1_sec05_width.tex`(370–411행: sec:dist), `ch1_sec06_eqpeak.tex`(전문), `ch2_sec01_partition.tex`(전문: ssec:site·eq:Z1·eq:muV·eq:Vxi), `ch2_sec03_vibel.tex`(1–80행: eq:Svib_mode), `ch1v22_bib.tex`(해당 5키), `common_preamble_v1022.tex`(박스·매크로), `ch1_graphite_v1.0.22.aux`/`.log`(라벨 해소·경고), `results/V1022_REFERENCE_LEDGER.md` + v1.0.21 원장(승계 확인)
- 표 규칙: 표 안 개행은 `<br>` 로 접합 표기(시각용). **기계 매칭용 축자 전문은 §2 발견 상세의 "현행(축자)" 코드블록이 정본** — 원문 그대로 복사(개행 포함).

---

## 1. 발견 요약 표

| ID | 파일:행 | 유형 | 등급 | 현행(축자 — 요약, 정본은 §2) | 제안(요지 — 완성 LaTeX 는 §2) | 근거(요지) |
|----|---------|------|------|------------------------------|-------------------------------|------------|
| A02-01 | ch1_sec02a_part0.tex:10–18 | 보완 | M | `&\to\ \mu(\theta;\Omega)\ \to\ \xi_\eq\ \text{logistic}\ \to\ G,\ \text{Nernst}` (사슬 박스) + 도착점 목록 3곳 | 사슬 박스에 다클래스 반전 계단 `\sum_jQ_j\xi_{\eq,j}=Q\bar x` 삽입 + 도착점에 `\S\ref{sec:eqpeak}` 추가 | 02b §sm-mc·말미 keybox 사다리(9계단)와 서두 로드맵(7계단) 불일치 |
| A02-02 | ch1_sec02a_part0.tex:227–230 | 보완 | M | `격자 진동의 양자(포논)는 보손이라 진동 엔트로피가 식~\eqref{eq:sm-fdbe} 의 $\bar n$...` | 포논은 개수 비보존 보손 → $\mu=0$ 읽기 한 줄 삽입 | eq:sm-fdbe 는 $\mu$ 든 일반형, 하류(q_k·Svib_mode)는 전부 $\mu=0$ 형 — 다리 부재 |
| A02-03 | ch1_sec02a_part0.tex:83–87 | 보완 | M | `격자의 자리들이 전해질을 통해 Li 저장조(상대극 Li 금속)와 입자를 교환하므로 $\mu$ 가 고정된 대정준 문제이고` | 교환 입자 = 중성 Li(Li⁺+e⁻) 명시 + $\mu$ 손잡이 결선 전방 가드 | Li⁺는 전해질·e⁻는 도선 — "무엇의 $\mu$ 인가"가 02b 전까지 무답 |
| A02-04 | ch1_sec02a_part0.tex:51–56 | 보완 | M | `저장조가 계보다 훨씬 크므로 $S_R$ 을 1차에서 절단해 전개하면` | 2차 항 $\propto 1/C_R$ 소멸 각주 | $\mathcal O(E_i^2)$ 무시 근거(저장조 열용량 발산) 미제시 — 자족성 주장 대비 공백 |
| A02-05 | ch1_sec02a_part0.tex:372–375 | 설명 | M | `본론 \S\ref{sec:dist} 가 말하는 ``kinetic·thermo 두 경로가 한 분포의 두 얼굴''의 평형 쪽 절반이 바로 이것이다` | "평형 쪽 절반" 지시 구조 풀어쓰기(thermo 얼굴=이 분포, kinetic 합류=§width) | 앙상블 동등성(두 평형 경로)과 §dist 이중성(kinetic vs thermo)의 층위가 뒤섞여 읽힘 |
| A02-06 | ch1_sec02a_part0.tex:171–172 | 보완(부호) | M | srcbox 표: `삽입 분율 $x$ ... $\theta$$\cdot$$\xi$ 에 해당` / `$\tfrac{RT}{sF}\ln\tfrac{\xi}{1-\xi}$ 항 ↔ 배치 항 $\tfrac{kT}{e}\ln\tfrac{x}{1-x}$` | 배향 주의 1줄: $x=1-\xi$ 대입 시 두 로그는 부호 반전으로 연결 | 좌표 배향(x=삽입↑, ξ=탈리튬화↑)이 흡수하는 부호 하나가 암묵 — 본 문서 부호 규율(P3·signbox 문화) 대비 명시 필요 |
| A02-07 | ch1_sec02a_part0.tex:63–69 | 수식화 | M | `그 규격화 합이 canonical 분배함수(partition function) $Z=\sum_ie^{-\beta E_i}$, 그 로그가 Helmholtz 자유에너지 $F=-k_BT\ln Z$ 다...` (전부 산문 인라인) | canonical 3종 세트($Z$→$F$→$\mu$)를 번호식 1본으로 표시(신규 라벨 제안 eq:sm-canon) | 4가지 논점이 한 문단 인라인 수식에 압축 — 하류가 되받는 $\mu=\partial F/\partial N$ 이 본문 유일의 비표시 핵심식 |
| A02-08 | ch1_sec02a_part0.tex:250–255 | 수식화 | M | `일반적인 정의는 상태 합 $q(T)=\mathrm{Tr}\,e^{-\beta H_\mathrm{int}}$ 이고 ... $q=\prod_{i=1}^{3}[2\sinh(\beta\hbar\omega_i/2)]^{-1}$...로 닫힌다.` (한 문장) | $q(T)$ 세 층위(Tr→조화 양자곱→고전극한)를 화살표 1식으로 표시(신규 라벨 제안 eq:sm-qforms) | 세 결과가 5행 산문 한 문장에 직렬 — 고전 비등방형($\prod k_BT/\hbar\omega_i$)도 자동 명시됨 |
| A02-09 | ch1_sec02a_part0.tex:38–39 | 설명 | M | `입자 1개를 받아들일 때 엔트로피가 $\mu/T$ 만큼 \emph{감소}하는 값비쌈의 척도다` | $(E,V$ 고정$)$ 조건 + $\mu$ 부호별 읽기 명시 | $\mu<0$ 이면 엔트로피는 증가 — 무조건 "감소"는 초심 독자를 오도(인접 식은 옳음) |
| A02-10 | ch1_sec02a_part0.tex:39–41 | 논리(정밀) | L | `두 계 1,2 가 입자를 교환하면 총 엔트로피 변화가 $\dd S_\mathrm{tot}=\big(\tfrac{\mu_2}{T}-\tfrac{\mu_1}{T}\big)\dd N_1\ge0$` | "같은 온도 $T$ 를 이미 공유한" 전제 명시 | 단일 $T$ 사용은 열평형 선행을 암묵 가정 — 식 자체는 옳으나 전제 은닉 |
| A02-11 | ch1_sec02a_part0.tex:290–293 | 보완 | L | `양자 조화 $q$ 면 영점 에너지를 더한 $\varepsilon_0+\tfrac32\hbar\omega_0$` | 비등방 일반형 $\varepsilon_0+\sum_i\tfrac12\hbar\omega_i$(등방 특수형 병기) | 직전(253–255행)에 비등방 일반형으로 넓힌 뒤 검산은 등방 특수형만 인용 |
| A02-12 | ch1_sec02a_part0.tex:258–260 | 보완(일관) | L | `Part T 의 단일 자리 분배함수(\S\ref{ssec:site}, 식~\eqref{eq:Z1})도 같은 기호 $\Xi_1$ 로 통일한다` | eq:Z1 의 $\varepsilon_0$=유효값 읽기 괄호 1줄 | eq:Z1 표기는 $q$ 인자 없는 원형꼴 — Part T 쪽 명시("유효값으로 읽는다")를 이쪽에서도 상호 참조해야 동일성이 자명 |
| A02-13 | ch1_sec02a_part0.tex:328–330 | 일관(수식↔산문) | L | `모드당 엔트로피~\eqref{eq:Svib_mode} $s_k=k_B[(1+\bar n_k)\ln(1+\bar n_k)-\bar n_k\ln\bar n_k]$` | 라벨식 원표기 $S_{\vib,k}$·$n_k$ 로 인용 정합 | 실제 eq:Svib_mode 는 `S_{\vib,k}=\kB[(1+n_k)\ln(1+n_k)-n_k\ln n_k]` — 기호 2종($s_k$·$\bar n_k$)이 원문과 다름 |
| A02-14 | ch1_sec02a_part0.tex:348–349 | 일관 | L | `($\Delta\mu=\tilde\varepsilon-\mu$ 로 흡수된 표기)` | $\mu\equiv\mu_\mathrm{Li}$ 재선언 1줄 | eq:fermifn 은 $\Delta\mu\equiv\tilde\varepsilon(T)-\mu_\mathrm{Li}$ — 2.2(d′)→2.3 에서 $\mu_\mathrm{Li}$↔$\mu$ 표기 요동 |
| A02-15 | ch1_sec02a_part0.tex:183 | 문체 | L | `$\tilde\varepsilon(T){=}\varepsilon_0{-}\kB T\ln q(T)$` | `\kB`→`k_B`(파일 내 지배 표기 통일; 역방향 통일은 마스터 결정) | 본 파일은 `k_B` 리터럴 22회·`\kB`(roman B) 1회 — 조판상 두 글꼴 혼재 |
| A02-16 | ch1_sec02a_part0.tex:343–344 | 보완 | L | `결정 안에 동등한 삽입 자리가 $M$ 개 있고 서로 상호작용하지 않는다고 하자` | "동등" 가정의 완화처(\S\ref{sec:sm-mc} 클래스 확장) 전방 포인터 | 가정 2 는 완화처 명시(120행), "동등" 가정만 완화처 포인터 부재 |

---

## 2. 발견 상세 (현행 축자 정본 + 완성 LaTeX 제안)

### A02-01 (M, 보완) — 서두 사슬 박스·도착점 목록이 다클래스 반전 계단을 누락

파일:행 `ch1_sec02a_part0.tex:10–18`

현행(축자):
```latex
사슬은
\[
\boxed{\;\begin{aligned}
&\text{미시상태·앙상블}\ \to\ Z,\Xi\ \to\ \theta=\frac{1}{1+e^{\beta(\tilde\varepsilon-\mu)}}\ \to\ \text{lattice gas}\\
&\to\ \mu(\theta;\Omega)\ \to\ \xi_\eq\ \text{logistic}\ \to\ G,\ \text{Nernst}
\end{aligned}\;}
\]
이고, 도착점들이 본론 결과 사슬 --- \S\ref{sec:center} 의 $U_j(T)$, \S\ref{sec:hys} 의 히스테리시스,
\S\ref{sec:width} 의 $\xi_\eq$ --- 의 입력이다.
```

제안(완성 LaTeX):
```latex
사슬은
\[
\boxed{\;\begin{aligned}
&\text{미시상태·앙상블}\ \to\ Z,\Xi\ \to\ \theta=\frac{1}{1+e^{\beta(\tilde\varepsilon-\mu)}}\ \to\ \text{lattice gas}\\
&\to\ \mu(\theta;\Omega)\ \to\ \xi_\eq\ \text{logistic}\ \to\ \textstyle\sum_jQ_j\,\xi_{\eq,j}=Q\bar x\ \to\ G,\ \text{Nernst}
\end{aligned}\;}
\]
이고, 도착점들이 본론 결과 사슬 --- \S\ref{sec:center} 의 $U_j(T)$, \S\ref{sec:hys} 의 히스테리시스,
\S\ref{sec:width} 의 $\xi_\eq$, \S\ref{sec:eqpeak} 의 전하 보존식 --- 의 입력이다.
```

근거: 같은 §2 의 후반부(`ch1_sec02b_part0.tex`)가 §sm-mc 마감문에서 "이로써 사다리에는 logistic 과 Nernst 사이에 ``다클래스 반전'' 계단이 하나 더 놓였다"라 명시하고, 말미 keybox "Part 0 사다리"도 `다클래스 전하 보존 반전~\eqref{eq:sm-mc-balance}` 를 logistic 과 Nernst 사이에 둔다(9계단). 서두 로드맵 박스(v1.0.20 형태, 7계단)만 v1.0.21 의 sm-mc 증축을 반영하지 못해 문서 내 두 사다리가 불일치. 도착점 목록도 sm-mc 의 실제 도착점(§eqpeak N6 보존식 `Q_\cell q=Q_\bg+\sum_jQ_j\xi_j` 의 전이 몫 — 02b (d) 박스가 "글자까지 같고"라 명시)을 누락. P5 준수: 기존 계단 문구는 전부 보존, 삽입·추가만.

### A02-02 (M, 보완) — bgbox: 포논 적용 시 $\mu=0$ 이 되는 이유 부재

파일:행 `ch1_sec02a_part0.tex:227–230` (bgbox 내부)

현행(축자):
```latex
정전$\cdot$입체 반발이라는 \emph{기하}이고 입자도 전자가 아니라 Li 이온이다. 진짜 양자 통계가 일하는 곳은
Part T(\S\ref{sec:vibel})다 --- 격자 진동의 양자(포논)는 보손이라 진동 엔트로피가 식~\eqref{eq:sm-fdbe} 의 $\bar n$
(Bose--Einstein 들뜸수)으로 적히고, 전도 전자는 페르미온이라 electronic 엔트로피가 $f(E)$(Fermi--Dirac
분포)로 적힌다 \cite{mcquarrie1976,ashcroftmermin1976}.
```

제안(완성 LaTeX — bgbox 자족성 유지, 괄호 증분만):
```latex
정전$\cdot$입체 반발이라는 \emph{기하}이고 입자도 전자가 아니라 Li 이온이다. 진짜 양자 통계가 일하는 곳은
Part T(\S\ref{sec:vibel})다 --- 격자 진동의 양자(포논)는 보손이라 진동 엔트로피가 식~\eqref{eq:sm-fdbe} 의 $\bar n$
(Bose--Einstein 들뜸수 --- 단 포논$\cdot$광자처럼 개수가 보존되지 않는 보손은 개수 제약 없이 자유에너지가
최소화되어 평형에서 $\mu=0$ 이므로, $E$ 자리에 모드 에너지 $\hbar\omega$ 만 남은
$\bar n=1/(e^{\beta\hbar\omega}-1)$ 로 읽는다)으로 적히고, 전도 전자는 페르미온이라 electronic 엔트로피가 $f(E)$(Fermi--Dirac
분포)로 적힌다 \cite{mcquarrie1976,ashcroftmermin1976}.
```

근거: 식~\eqref{eq:sm-fdbe} 는 $\mu$ 가 든 일반 BE 형 $\bar n(E)=1/(e^{\beta(E-\mu)}-1)$ 로 유도되는데, 이를 되받는 본문 328행($q_k=[1-e^{-\beta\hbar\omega_k}]^{-1}$·$\bar n_k$)과 Part T `eq:Svib_mode`($n_k=1/(e^{\beta\hbar\omega_k}-1)$, `ch2_sec03_vibel.tex:15`)는 전부 $\mu=0$ 형이다. 그 사이 다리(개수 비보존 → $\mu=0$)가 본문 어디에도 없어, "자족적으로 정리한다"(160–161행)는 배경 박스의 선언 대비 독자 1순위 질문이 무답. 제거 용이 블록(bgbox) 독립성: 증분이 괄호 안 자족 문장이라 유지됨.

### A02-03 (M, 보완) — 교환되는 "입자"의 정체(중성 Li)와 $\mu$ 손잡이 전방 가드

파일:행 `ch1_sec02a_part0.tex:83–87` (2.1 verifybox)

현행(축자):
```latex
극한 검산 --- $\beta\to0$ 이면 $P_i\to$ 등확률(열적 규율 소실), $\beta\to\infty$ 면 $E_i-\mu N_i$ 최소 상태만
남는다. 삽입 전극이 정확히 이 설정이다 --- 격자의 자리들이 전해질을 통해 Li 저장조(상대극 Li 금속)와 입자를
교환하므로 $\mu$ 가 고정된 대정준 문제이고(그림~\ref{fig:sm-reservoir}), 다음 소절이 그 최소 단위(자리
하나)를 푼다.
```

제안(완성 LaTeX — 말미 1문장 추가):
```latex
극한 검산 --- $\beta\to0$ 이면 $P_i\to$ 등확률(열적 규율 소실), $\beta\to\infty$ 면 $E_i-\mu N_i$ 최소 상태만
남는다. 삽입 전극이 정확히 이 설정이다 --- 격자의 자리들이 전해질을 통해 Li 저장조(상대극 Li 금속)와 입자를
교환하므로 $\mu$ 가 고정된 대정준 문제이고(그림~\ref{fig:sm-reservoir}), 다음 소절이 그 최소 단위(자리
하나)를 푼다. 여기서 교환되는 ``입자''는 전해질을 건너는 Li$^+$ 와 외부 회로를 도는 $e^-$ 가 host 안에서
합쳐진 \emph{중성 Li} 이며, 실험자가 이 $\mu$ 를 전위 손잡이로 돌리는 결선($\mu_\mathrm{Li}=\mu^0-sF(V-U)$)은
\S\ref{sec:sm-electro} 가 닫는다.
```

근거: 실제 셀에서 Li⁺ 와 $e^-$ 는 서로 다른 길로 이동하므로 "저장조와 교환되는 입자의 $\mu$"가 어느 종의 것인지는 초심 독자가 반드시 묻는 지점인데, 그 답(중성 Li: `host 안의 Li 는 중성이라 $\tilde\mu_\mathrm{Li}=\mu_\mathrm{Li}$`, 02b `sec:sm-electro` 147–149행)이 두 소절 뒤에야 나온다. 2.2 도입부(112행)의 포인터는 "결선이 받는 입력"만 말하고 입자 정체는 말하지 않음. 제안식 표기는 02b `eq:sm-eqcond` 와 동일 형태라 신규 주장 없음.

### A02-04 (M, 보완) — Taylor 절단(식 sm-taylor)의 2차 항 소멸 근거 각주

파일:행 `ch1_sec02a_part0.tex:51–56`

현행(축자):
```latex
저장조가 계보다 훨씬 크므로 $S_R$ 을 1차에서 절단해 전개하면(식~\eqref{eq:sm-fund} 의 두 도함수 대입)
\begin{equation}
S_R(E_\mathrm{tot}-E_i,\,N_\mathrm{tot}-N_i)
= S_R(E_\mathrm{tot},N_\mathrm{tot})-\frac{E_i}{T}+\frac{\mu N_i}{T}+\mathcal O(E_i^2,N_i^2).
\label{eq:sm-taylor}
\end{equation}
```

제안(완성 LaTeX — 각주 1본 추가):
```latex
저장조가 계보다 훨씬 크므로 $S_R$ 을 1차에서 절단해 전개하면(식~\eqref{eq:sm-fund} 의 두 도함수
대입)\footnote{절단의 근거: 2차 계수가 $\partial^2S_R/\partial E^2=\partial(1/T)/\partial E=-1/(T^2C_R)$ 라
2차 항은 $E_i^2/(2k_BT^2C_R)$ 규모($k_B$ 로 나눈 지수 기준)인데, 저장조 열용량 $C_R$ 는 저장조 크기에
비례해 자라므로 저장조가 계보다 훨씬 큰 극한에서 사라진다($N_i$ 쪽 2차 항도 같은 논리).}
\begin{equation}
S_R(E_\mathrm{tot}-E_i,\,N_\mathrm{tot}-N_i)
= S_R(E_\mathrm{tot},N_\mathrm{tot})-\frac{E_i}{T}+\frac{\mu N_i}{T}+\mathcal O(E_i^2,N_i^2).
\label{eq:sm-taylor}
\end{equation}
```

근거: "훨씬 크므로"만으로는 왜 1차 절단이 정당한지(2차 계수가 저장조 크기 역수로 죽는 구조)가 닫히지 않는다. 본 절의 자족성 선언(6–9행 "통계역학 사전지식 없이도 ... 닫히도록") 기준에서 표준 교과서(예: Hill·McQuarrie)가 명시하는 한 줄이 빠진 곳. 재유도 확인: $\partial(1/T)/\partial E=-T^{-2}\partial T/\partial E=-1/(T^2C_R)$ — 부호·형태 맞음.

### A02-05 (M, 설명) — "평형 쪽 절반" 문장의 지시 구조 풀어쓰기

파일:행 `ch1_sec02a_part0.tex:372–375`

현행(축자):
```latex
한편 식~\eqref{eq:fermifn} 를 $\mu$ 에 대해 뒤집어도($e^{\beta\Delta\mu}=(1-\theta)/\theta$) 같은
식~\eqref{eq:sm-mucount} 가 나온다 --- 대정준 경로(자리 하나의 확률)와 셈법 경로(배치 수의 로그)가 같은
$\mu(\theta)$ 에 닿는 것이 앙상블 동등성이며, 본론 \S\ref{sec:dist} 가 말하는 ``kinetic·thermo 두 경로가 한
분포의 두 얼굴''의 평형 쪽 절반이 바로 이것이다.
```

제안(완성 LaTeX):
```latex
한편 식~\eqref{eq:fermifn} 를 $\mu$ 에 대해 뒤집어도($e^{\beta\Delta\mu}=(1-\theta)/\theta$) 같은
식~\eqref{eq:sm-mucount} 가 나온다 --- 대정준 경로(자리 하나의 확률)와 셈법 경로(배치 수의 로그)가 같은
$\mu(\theta)$ 에 닿는 것이 앙상블 동등성이다. 본론 \S\ref{sec:dist} 의 명제 ``kinetic·thermo 두 경로가 한
분포의 두 얼굴''에서 thermo(평형) 얼굴이 바로 이 분포다 --- 확률로 세든 배치 수로 세든 같은 한 분포에
닿음을 여기서 미리 닫아 두었고, kinetic 얼굴과의 합류는 \S\ref{sec:width} 가 잇는다.
```

근거: §dist(`ch1_sec05_width.tex:376–377`)의 "두 얼굴"은 (i) kinetic(detailed balance) vs (ii) thermo(자유에너지 최소화)의 이중성이고, 여기의 "두 경로"는 둘 다 **평형** 경로(대정준 확률 vs 정준 셈법)다. 층위가 다른 두 이중성이 "평형 쪽 절반이 바로 이것"이라는 한 지시어에 눌려 있어, 검토자도 1차 독해에서 혼동했다(02b (d) 항목 (ii) "\S\ref{sec:dist} 의 명제를 Part 0 이 평형 쪽에서 선결"과 같은 취지임을 명확화). 결과식·주장 무변경 — 지시 구조만 전개.

### A02-06 (M, 보완·부호) — srcbox 대응표: $x$↔$\xi$ 배향이 흡수하는 부호 명시

파일:행 `ch1_sec02a_part0.tex:171–172` (srcbox 표 1·2행)

현행(축자):
```latex
평균 점유 $\langle n\rangle^{0}$ (식~\eqref{eq:sm-bare}) & 삽입 분율 $x$ (자리 점유율 --- 본문 $\theta$$\cdot$$\xi$ 에 해당) \\
$\tfrac{RT}{sF}\ln\tfrac{\xi}{1-\xi}$ 항 (식~\eqref{eq:Veq}) & 배치 항 $\tfrac{kT}{e}\ln\tfrac{x}{1-x}$ \\
```

제안(완성 LaTeX — 표 아래(tabular 닫은 뒤, "방법 요지" 문단 앞)에 1문장 추가; 표 자체는 무수정):
```latex
\emph{배향 주의} --- $x$ 는 삽입 분율(본문 점유율 $\theta$, 곧 $x=1-\xi$)이라 두 배치 항은 좌표
자리바꿈으로 연결된다: $\tfrac{RT}{sF}\ln\tfrac{\xi}{1-\xi}=-\tfrac{RT}{sF}\ln\tfrac{x}{1-x}$ --- 부호
하나가 배향($x$ 증가 $=$ 삽입, $\xi$ 증가 $=$ 탈리튬화)의 차이로 흡수된다.
```

근거: 재계산 — $\xi=1-x$ 대입 시 $\ln[\xi/(1-\xi)]=\ln[(1-x)/x]=-\ln[x/(1-x)]$ (항등, 원문 서지 주장 아님·순수 대수). 표는 "대응"이라 거짓은 아니나, 두 셀을 그대로 등치로 읽으면 부호가 하나 다르다. 본 문서의 부호 규율(P3 검수 문화, 도처의 signbox·"부호 읽기")에 비추어 배향 흡수 부호는 명시가 정합적. 표 1행이 이미 "$\theta$$\cdot$$\xi$ 에 해당"으로 두 좌표를 병기하므로 추가 문장 한 줄로 닫힘.

### A02-07 (M, 수식화) — canonical 3종 세트($Z,F,\mu$)의 표시 수식화

파일:행 `ch1_sec02a_part0.tex:63–69`

현행(축자):
```latex
--- 이 지수가 \emph{Gibbs 인자}다. 입자 교환이 없으면($N_i$ 고정) $e^{-\beta E_i}$ 의 \emph{Boltzmann 인자}로
줄고, 그 규격화 합이 canonical 분배함수(partition function) $Z=\sum_ie^{-\beta E_i}$, 그 로그가 Helmholtz
자유에너지 $F=-k_BT\ln Z$ 다($\langle E\rangle=\partial(\beta F)/\partial\beta$·$S=-\partial F/\partial T$ 가
열역학 관계와 일치함이 이 명명의 근거다). 이 $F$ 는 Faraday 상수 $F$ 와 기호만 같고 문맥으로 갈린다 ---
전자는 $\partial F/\partial T$ 처럼 \emph{미분당하는 자유에너지}, 후자는 $FV$·$RT/F$ 의 전하 환산
곱$\cdot$나눗셈 상수다. 식~\eqref{eq:sm-fund} 의 $\mu$ 를 $F$ 로 옮기면
$\mu=\partial F/\partial N|_{T,V}$ --- \emph{온도·부피를 고정한 채 입자 1개를 더 넣는 자유에너지 비용}이며,
```

제안(완성 LaTeX — 내용 전량 보존, 핵심 사슬만 표시식으로 승격; 신규 라벨 제안 `eq:sm-canon`):
```latex
--- 이 지수가 \emph{Gibbs 인자}다. 입자 교환이 없으면($N_i$ 고정) $e^{-\beta E_i}$ 의 \emph{Boltzmann 인자}로
줄고, 그 규격화 합$\cdot$로그$\cdot$$N$-미분이 canonical 사슬을 이룬다:
\begin{equation}
Z=\sum_ie^{-\beta E_i},\qquad
F=-k_BT\ln Z,\qquad
\mu=\frac{\partial F}{\partial N}\Big|_{T,V}
\label{eq:sm-canon}% 신규 라벨 제안
\end{equation}
--- $Z$ 가 canonical 분배함수(partition function), $F$ 가 Helmholtz 자유에너지다
($\langle E\rangle=\partial(\beta F)/\partial\beta$·$S=-\partial F/\partial T$ 가 열역학 관계와 일치함이 이
명명의 근거이고, 셋째 식은 식~\eqref{eq:sm-fund} 의 $\mu$ 를 $F$ 로 옮긴 것이다). 이 $F$ 는 Faraday 상수
$F$ 와 기호만 같고 문맥으로 갈린다 --- 전자는 $\partial F/\partial T$ 처럼 \emph{미분당하는 자유에너지},
후자는 $FV$·$RT/F$ 의 전하 환산 곱$\cdot$나눗셈 상수다. $\mu=\partial F/\partial N|_{T,V}$ 는
\emph{온도·부피를 고정한 채 입자 1개를 더 넣는 자유에너지 비용}이며,
```

근거: 이 문단은 (i) Boltzmann 특수화, (ii) $Z$·$F$ 정의, (iii) $F$ 기호 충돌 경고, (iv) $\mu=\partial F/\partial N$ 다리의 4논점이 전부 인라인이다. 특히 (iv)는 하류 두 곳(70–71행의 §sm-macro 다리 예고, 02b `eq:sm-mubridge`)이 되받는 핵심인데 본 절에서 유일하게 번호 없는 관계식. (a)→(d) "중간식" 단계의 자기 규칙("(c) 중간식"에 식 번호 부여)과도 정합. 삭제 없음 — 배치 전환만.

### A02-08 (M, 수식화) — $q(T)$ 세 층위의 화살표 1식 정리

파일:행 `ch1_sec02a_part0.tex:250–255`

현행(축자):
```latex
$q(T)$ 는 점유된 이온의 진동 등 국소 자유도의 단일 자리 분배함수다\footnote{이 $q(T)$(단일 자리 내부 분배함수)는 N6--N9 의 정규화 용량 좌표 $q{=}Q/Q_\cell$ 와 다른 양이다 --- 전자는 Part 0 의 국소 열역학량, 후자는 곡선 좌표.}. 일반적인 정의는 상태
합 $q(T)=\mathrm{Tr}\,e^{-\beta H_\mathrm{int}}$ 이고 식~\eqref{eq:partfn} 의 위상공간 적분은 그 고전
극한이다 --- 자리 우물을 3차원 조화 퍼텐셜(진동수 $\omega_0$)로 근사하면 고전 극한에서
$q=(k_BT/\hbar\omega_0)^3$ 이고, 등방 가정(세 방향이 같은 $\omega_0$)을 풀어 데카르트 축마다 다른
진동수를 허용하는 일반형으로 넓히면 양자 상태 합으로는
$q=\prod_{i=1}^{3}[2\sinh(\beta\hbar\omega_i/2)]^{-1}$(축 지표 $i=1,2,3$ 마다 진동수 $\omega_i$)로 닫힌다.
```

제안(완성 LaTeX — 각주·정의 문장 보존, 조화 우물 결과를 표시식으로; 신규 라벨 제안 `eq:sm-qforms`):
```latex
$q(T)$ 는 점유된 이온의 진동 등 국소 자유도의 단일 자리 분배함수다\footnote{이 $q(T)$(단일 자리 내부 분배함수)는 N6--N9 의 정규화 용량 좌표 $q{=}Q/Q_\cell$ 와 다른 양이다 --- 전자는 Part 0 의 국소 열역학량, 후자는 곡선 좌표.}. 일반적인 정의는 상태
합 $q(T)=\mathrm{Tr}\,e^{-\beta H_\mathrm{int}}$ 이고 식~\eqref{eq:partfn} 의 위상공간 적분은 그 고전
극한이다. 자리 우물을 데카르트 축마다 진동수 $\omega_i$($i=1,2,3$)를 갖는 3차원 조화 퍼텐셜로 근사하면
\begin{equation}
q(T)\;=\;\prod_{i=1}^{3}\frac{1}{2\sinh(\beta\hbar\omega_i/2)}
\;\;\xrightarrow[\;k_BT\gg\hbar\omega_i\;]{}\;\;
\prod_{i=1}^{3}\frac{k_BT}{\hbar\omega_i}
\qquad\bigl(\text{등방 }\omega_i\equiv\omega_0:\ (k_BT/\hbar\omega_0)^3\bigr)
\label{eq:sm-qforms}% 신규 라벨 제안
\end{equation}
--- 양자 상태 합이 앞의 곱이고, 고전 극한($2\sinh x\to2x$)이 뒤의 곱이다.
```

근거: 세 결과(일반 Tr·양자 조화곱·고전 극한)가 5행 산문 한 문장에 직렬로 눌려 있어 독자가 관계(무엇이 무엇의 극한인지)를 재구성해야 한다. 화살표 1식이면 (i) 고전 **비등방** 형 $\prod_ik_BT/\hbar\omega_i$ 가 자동으로 명시되고(현행은 고전=등방·양자=비등방만 제시되어 대응이 어긋나 보임), (ii) 하류 291–293행($T\to0$ 검산)·330–334행(영점 기준 규약)이 이 라벨을 참조할 수 있다. 재계산 확인: $2\sinh(\beta\hbar\omega/2)\to\beta\hbar\omega$ ($\beta\hbar\omega\ll1$) ⇒ $k_BT/\hbar\omega$ — 일치.

### A02-09 (M, 설명) — $\mu$ 의 의미 문장: 고정 변수·부호 조건 명시

파일:행 `ch1_sec02a_part0.tex:38–39`

현행(축자):
```latex
여기서 $\mu$ 의 물리적 의미가 이미 보인다 --- 입자 1개를 받아들일 때 엔트로피가 $\mu/T$ 만큼 \emph{감소}하는
값비쌈의 척도다.
```

제안(완성 LaTeX):
```latex
여기서 $\mu$ 의 물리적 의미가 이미 보인다 --- 입자 1개를 받아들일 때($E,V$ 고정) 엔트로피 변화가
$-\mu/T$ 인, 곧 $\mu>0$ 이면 엔트로피가 그만큼 \emph{깎이는} 값비쌈의, $\mu<0$ 이면 오히려 늘어나는
헐값의 척도다.
```

근거: $\partial S/\partial N|_{E,V}=-\mu/T$(식~\eqref{eq:sm-fund}, 재확인)에서 "감소"는 $\mu>0$ 일 때만 성립한다. 결합이 유리한 삽입 문제에서는 관례에 따라 $\mu<0$ 인 경우가 흔하므로, 초심 독자용 앵커 문장으로서 무조건 "감소"는 오도 위험. 고정 변수 $(E,V)$ 도 산문에 명시(인접 식엔 있으나 문장 단독으로도 옳게).

### A02-10 (L, 논리·정밀) — 입자 흐름 논증의 등온 전제 명시

파일:행 `ch1_sec02a_part0.tex:39–41`

현행(축자):
```latex
두 계 1,2 가 입자를 교환하면 총 엔트로피 변화가
$\dd S_\mathrm{tot}=\big(\tfrac{\mu_2}{T}-\tfrac{\mu_1}{T}\big)\dd N_1\ge0$ 이므로 입자는 $\mu$ 가 높은 쪽에서
낮은 쪽으로 흐르고, 정지 조건은 $\mu_1=\mu_2$ --- 화학퍼텐셜의 일치가 곧 입자 교환 평형이다.
```

제안(완성 LaTeX):
```latex
같은 온도 $T$ 를 이미 공유한 두 계 1,2 가 입자를 교환하면 총 엔트로피 변화가
$\dd S_\mathrm{tot}=\big(\tfrac{\mu_2}{T}-\tfrac{\mu_1}{T}\big)\dd N_1\ge0$ 이므로 입자는 $\mu$ 가 높은 쪽에서
낮은 쪽으로 흐르고, 정지 조건은 $\mu_1=\mu_2$ --- 화학퍼텐셜의 일치가 곧 입자 교환 평형이다.
```

근거: 재유도 — $\dd S_\mathrm{tot}=\partial_NS_1\,\dd N_1+\partial_NS_2\,\dd N_2=(-\mu_1/T_1+\mu_2/T_2)\dd N_1$; 인쇄된 단일-$T$ 형태는 $T_1=T_2=T$(열평형 선행)에서만 성립. 등온이 아니면 흐름 판정량은 $\mu/T$ 차. 식은 옳고 전제만 은닉 — 전제 1어절 명시로 닫힘.

### A02-11 (L, 보완) — $T\to0$ 검산의 영점 에너지: 비등방 일반형 병기

파일:행 `ch1_sec02a_part0.tex:290–293` (eq:fermifn verifybox)

현행(축자):
```latex
극한 검산 --- (i) $\beta\to\infty$($T\to0$)에서 $\Delta\mu\gtrless0$ 에 따라 $\theta\to0/1$ 의 계단
($T\to0$ 에서 $\tilde\varepsilon$ 는 점유 상태의 바닥 에너지로 수렴한다 --- 고전 $q$ 면 $k_BT\ln q\to0$
이라 $\varepsilon_0$, 양자 조화 $q$ 면 영점 에너지를 더한 $\varepsilon_0+\tfrac32\hbar\omega_0$ --- 어느
쪽이든 상수라 계단 구조는 동일).
```

제안(완성 LaTeX):
```latex
극한 검산 --- (i) $\beta\to\infty$($T\to0$)에서 $\Delta\mu\gtrless0$ 에 따라 $\theta\to0/1$ 의 계단
($T\to0$ 에서 $\tilde\varepsilon$ 는 점유 상태의 바닥 에너지로 수렴한다 --- 고전 $q$ 면 $k_BT\ln q\to0$
이라 $\varepsilon_0$, 양자 조화 $q$ 면 영점 에너지를 더한 $\varepsilon_0+\sum_i\tfrac12\hbar\omega_i$
(등방이면 $\varepsilon_0+\tfrac32\hbar\omega_0$) --- 어느 쪽이든 상수라 계단 구조는 동일).
```

근거: 재계산 — $q=\prod_i[2\sinh(\beta\hbar\omega_i/2)]^{-1}$ 이면 $\beta\to\infty$ 에서 $q\to e^{-\beta\sum_i\hbar\omega_i/2}$, $\tilde\varepsilon=\varepsilon_0-k_BT\ln q\to\varepsilon_0+\sum_i\hbar\omega_i/2$. 직전 (b′)(253–255행)에서 등방을 명시적으로 "풀어" 비등방 일반형으로 넓혔으므로, 검산이 등방 특수형만 인용하면 일반형과의 정합이 한 걸음 끊긴다. 물리 오류는 아님(등방 특수형 값 자체는 옳음).

### A02-12 (L, 보완·일관) — eq:Z1 통일 선언에 $\varepsilon_0$=유효값 읽기 병기

파일:행 `ch1_sec02a_part0.tex:258–260`

현행(축자):
```latex
위 첨자 없는 $\Xi_1$ 은 내부
자유도까지 포함한 완전한 단일 자리 대정준 분배함수이고, Part T 의 단일 자리 분배함수(\S\ref{ssec:site},
식~\eqref{eq:Z1})도 같은 기호 $\Xi_1$ 로 통일한다.
```

제안(완성 LaTeX):
```latex
위 첨자 없는 $\Xi_1$ 은 내부
자유도까지 포함한 완전한 단일 자리 대정준 분배함수이고, Part T 의 단일 자리 분배함수(\S\ref{ssec:site},
식~\eqref{eq:Z1})도 같은 기호 $\Xi_1$ 로 통일한다(그 식의 $\varepsilon_0$ 은 그 절이 명시하듯 $q(T)$
흡수를 마친 유효값 $\tilde\varepsilon$ 로 읽는 표기라, 두 $\Xi_1$ 은 같은 양이다).
```

근거: `eq:Z1`(`ch2_sec01_partition.tex:21–23`)의 인쇄형은 $\Xi_1=1+e^{-\beta(\varepsilon_0-\mu)}$ — 형태상 본 절의 원형 $\Xi_1^{0}$ 과 같아 보인다. Part T 쪽(같은 파일 41–44행)이 "본 파트 이하의 $\varepsilon_0$ 은 그 흡수를 마친 유효값으로 읽는다"로 닫아 두었으나, 통일 선언을 하는 이쪽에서도 그 읽기를 한 줄 상호 참조해야 "완전한(내부 자유도 포함)" $\Xi_1$ 과 "같은 기호"라는 문장이 즉석에서 자명해진다.

### A02-13 (L, 일관·수식↔산문) — eq:Svib_mode 인용 기호를 원표기와 정합

파일:행 `ch1_sec02a_part0.tex:328–330`

현행(축자):
```latex
$q_k=[1-e^{-\beta\hbar\omega_k}]^{-1}$ 를 식~\eqref{eq:sm-sint} 에 넣으면 Part T 의 모드당 엔트로피~\eqref{eq:Svib_mode}
$s_k=k_B[(1+\bar n_k)\ln(1+\bar n_k)-\bar n_k\ln\bar n_k]$(Bose--Einstein 들뜸수 $\bar n_k$)가 그대로
나온다.
```

제안(완성 LaTeX):
```latex
$q_k=[1-e^{-\beta\hbar\omega_k}]^{-1}$ 를 식~\eqref{eq:sm-sint} 에 넣으면 Part T 의 모드당 엔트로피~\eqref{eq:Svib_mode}
$S_{\vib,k}=k_B[(1+n_k)\ln(1+n_k)-n_k\ln n_k]$(그 절의 들뜸수 $n_k$ 는 식~\eqref{eq:sm-fdbe} 의
Bose--Einstein $\bar n$ 을 모드 $k$ 에서 읽은 값)가 그대로 나온다.
```

근거: 실제 `eq:Svib_mode`(`ch2_sec03_vibel.tex:24`)는 `S_{\vib,k} \;=\; \kB\bigl[(1+n_k)\ln(1+n_k) - n_k\ln n_k\bigr]` — 좌변 기호($S_{\vib,k}$ vs $s_k$)와 들뜸수 표기($n_k$ vs $\bar n_k$)가 인용과 다르다. 라벨 번호로 넘어가 대조하는 독자에게 두 기호가 어긋나 보임. 본 절의 $\bar n$(bgbox 자체 표기)과 Part T 의 $n_k$ 를 잇는 괄호로 두 표기 모두 보존. **핵심 검증(재유도)**: $s_{int}=k_B\partial(T\ln q)/\partial T$ 에 $q=[1-e^{-\beta\hbar\omega}]^{-1}$ 대입 ⇒ $s/k_B=-\ln(1-e^{-y})+y\bar n$ ($y\equiv\beta\hbar\omega$); 항등식 $1-e^{-y}=1/(1+\bar n)$, $y=\ln[(1+\bar n)/\bar n]$ 대입 ⇒ $s/k_B=(1+\bar n)\ln(1+\bar n)-\bar n\ln\bar n$ — **"그대로 나온다" 주장 수식 확인 통과**(본 검토의 최중량 재유도).

### A02-14 (L, 일관) — 2.3 의 $\Delta\mu$ 괄호에서 $\mu$↔$\mu_\mathrm{Li}$ 표기 요동 봉합

파일:행 `ch1_sec02a_part0.tex:348–349`

현행(축자):
```latex
각 인수는 내부 자유도 적분까지 마친 단일 자리 결과~\eqref{eq:partfn} 그대로다
($\Delta\mu=\tilde\varepsilon-\mu$ 로 흡수된 표기):
```

제안(완성 LaTeX):
```latex
각 인수는 내부 자유도 적분까지 마친 단일 자리 결과~\eqref{eq:partfn} 그대로다
($\Delta\mu=\tilde\varepsilon-\mu$ 로 흡수된 표기 --- \S\ref{sec:sm-site} 검산 (iv)대로
$\mu\equiv\mu_\mathrm{Li}$ 는 같은 저장조 화학퍼텐셜이고, 이하 다시 $\mu$ 로 줄여 적는다):
```

근거: 박스 `eq:fermifn`(285–287행)은 $\Delta\mu\equiv\tilde\varepsilon(T)-\mu_\mathrm{Li}$ 로 정의했고, 2.3 은 같은 $\Delta\mu$ 를 $\tilde\varepsilon-\mu$ 로 적는다. 동일성 선언은 verifybox (iv)(296–298행) 안에 있으나 괄호 속이라, 2.3 첫 재등장 지점에서 한 줄 재선언이 기호 위계 일관성(P3-1 유사 취지)에 부합. 의미 오류는 아님(양은 동일).

### A02-15 (L, 문체) — `\kB` 1회 vs `k_B` 22회 조판 혼재

파일:행 `ch1_sec02a_part0.tex:182–183` (srcbox 내부)

현행(축자):
```latex
미시상태를 지정하나(내부 자유도 없음), 본문은 점유 자리에 진동 등 내부 자유도 $q(T)$(식~\eqref{eq:partfn})를
실어 유효 자리에너지 $\tilde\varepsilon(T){=}\varepsilon_0{-}\kB T\ln q(T)$ 로 온도 이동을 허용하고(Part T 의
```

제안(완성 LaTeX — 최소 수정안):
```latex
미시상태를 지정하나(내부 자유도 없음), 본문은 점유 자리에 진동 등 내부 자유도 $q(T)$(식~\eqref{eq:partfn})를
실어 유효 자리에너지 $\tilde\varepsilon(T){=}\varepsilon_0{-}k_BT\ln q(T)$ 로 온도 이동을 허용하고(Part T 의
```

근거: 본 파일은 Boltzmann 상수를 리터럴 `k_B`(이탤릭 B)로 22회 쓰고, 183행 한 곳만 preamble 매크로 `\kB`($k_{\mathrm B}$, 로만 B)를 쓴다 — 같은 절 안에서 같은 상수가 두 글꼴로 조판됨. 최소 수정은 지배 표기로의 통일(위). 단 Part T 파일들은 `\kB` 를 쓰므로, 문서 전역을 `\kB` 로 역통일하는 안은 파일 다수 수정이 필요한 마스터 결정 사항(P5 — 임의 변경 대신 제안만).

### A02-16 (L, 보완) — "동등 자리" 가정의 완화처(다클래스) 전방 포인터

파일:행 `ch1_sec02a_part0.tex:343–344`

현행(축자):
```latex
\textbf{(a) 출발 --- 동등·독립 자리의 집합.} 결정 안에 동등한 삽입 자리가 $M$ 개 있고 서로 상호작용하지
않는다고 하자 --- 이 모형이 \emph{격자기체}(lattice gas)의 이상 극한이다.
```

제안(완성 LaTeX):
```latex
\textbf{(a) 출발 --- 동등·독립 자리의 집합.} 결정 안에 동등한 삽입 자리가 $M$ 개 있고 서로 상호작용하지
않는다고 하자 --- 이 모형이 \emph{격자기체}(lattice gas)의 이상 극한이다(자리가 전이별 클래스로 갈라지는
실제 전극으로의 확장은 \S\ref{sec:sm-mc} 가 닫는다).
```

근거: 가정 2(자리 독립)는 도입 시 완화처를 명시했다(119–120행 "\S\ref{sec:sm-mf} 에서 ... 완화된다"). 반면 2.3 의 "동등" 가정은 완화처(02b §sm-mc "자리 전체는 전이 $j$ ... 별 자리 클래스로 갈라진다") 포인터가 없어, 가정 관리의 대칭이 깨진다. 같은 문서 내 전방 참조는 기존 관행(120행)과 동일.

---

## 3. 등급별 정리

- **H (논리/물리 오류·오귀속): 0건** — §4 재계산 목록의 전 항목 통과. 부호 오류·유도 비약·인과 역전·수식↔산문의 실질 모순 미발견.
- **M (의미·이해 실질 개선): 9건** — A02-01(로드맵↔사다리 불일치), A02-02(포논 $\mu=0$ 다리), A02-03(교환 입자 정체), A02-04(Taylor 절단 근거), A02-05(§dist 지시 구조), A02-06(대응표 배향 부호), A02-07(canonical 3종 표시식), A02-08($q(T)$ 층위 표시식), A02-09($\mu$ 부호 조건).
- **L (문체·국소 일관): 7건** — A02-10(등온 전제), A02-11(비등방 영점), A02-12(eq:Z1 읽기), A02-13(인용 기호 정합), A02-14($\mu_\mathrm{Li}$ 요동), A02-15(`\kB` 혼재), A02-16(동등 가정 포인터).

모든 제안은 **대체·보강**(기존 자산·수식 삭제 없음). A02-07·08 의 신규 라벨(eq:sm-canon·eq:sm-qforms)은 제안 표기.

---

## 4. 논리 축 재계산 검증 목록 (전 항목 통과 — ② 관점 수행 증빙)

1. `eq:sm-fund`: $\dd E=T\dd S-P\dd V+\mu\dd N$ 반전·두 도함수 — 부호 일치.
2. 두 계 입자 흐름: $\dd S_\mathrm{tot}=(\mu_2-\mu_1)\dd N_1/T\ge0$ ⇒ 고$\mu$→저$\mu$ 방향 — 일치(등온 전제는 A02-10).
3. `eq:sm-taylor`: $-\partial_ES_R=-1/T$, $-\partial_NS_R=+\mu/T$ 대입 — 부호 일치.
4. `eq:sm-gibbsfactor`·`eq:sm-gc`: $\partial\ln\Xi/\partial\mu=\beta\langle N\rangle$ 직접 미분 — 일치.
5. `eq:sm-baresum`→`eq:sm-baremid`→`eq:sm-bare`: 두-항 합·확률·로그미분 교차검증·분자분모 나눗셈 — 전부 일치.
6. 원형 verifybox 3극한(β→∞ 계단 방향 0/1 순서, β→0 → ½, μ→±∞ → 1/0 순서) — 일치.
7. `eq:sm-fdbe`: $\Xi_\mathrm F$·$\Xi_\mathrm B$ 로그미분으로 $f(E)$·$\bar n(E)$ 재유도, 기하급수 수렴 조건 $E>\mu$ — 일치.
8. `eq:partfn`: $z_0=1$·$z_1=e^{-\beta\varepsilon_0}q$ 조립 — 일치. 3D 조화 고전 적분 $(2\pi mk_BT)^{3/2}(2\pi k_BT/m\omega_0^2)^{3/2}/h^3=(k_BT/\hbar\omega_0)^3$ — 일치. 양자 1D 합 $\sum e^{-\beta\hbar\omega(n+1/2)}=[2\sinh(\beta\hbar\omega/2)]^{-1}$ — 일치.
9. `eq:sm-occmid`·`eq:sm-epstilde`·`eq:fermifn`: $qe^{-\beta\varepsilon_0}=e^{-\beta\tilde\varepsilon}$ 흡수, logistic 회수 — 일치.
10. eq:fermifn verifybox: (i) $T\to0$ 에서 고전 $k_BT\ln q\to0$·양자 $\tilde\varepsilon\to\varepsilon_0+\sum_i\hbar\omega_i/2$; (ii) $\beta\Delta\mu\to-\ln q$ ⇒ $q\equiv1$ 이면 ½·조화 우물이면 $\theta\to1$; (iii)(iv) 회수 — 전부 일치.
11. `eq:sm-flucres`: $n^2=n$ ⇒ $\mathrm{var}=\theta(1-\theta)$; $\partial\theta/\partial(\beta\mu)=\theta(1-\theta)$ 직접 미분 — 일치(요동–응답 일반 항등식과 정합).
12. `eq:sm-sint`→`eq:Svib_mode` 사슬: $q_k=[1-e^{-\beta\hbar\omega_k}]^{-1}$ 대입 ⇒ $(1+\bar n)\ln(1+\bar n)-\bar n\ln\bar n$ **완전 재유도 통과**(A02-13 근거란 상세).
13. 영점 기준 규약: $[2\sinh(\beta\hbar\omega/2)]^{-1}=e^{-\beta\hbar\omega/2}[1-e^{-\beta\hbar\omega}]^{-1}$ — 인자 $e^{-\beta\hbar\omega/2}$ 확인; $T\ln(e^{-\beta\hbar\omega/2})=-\hbar\omega/(2k_B)$ = 온도 무관 ⇒ 엔트로피 동일 — 본문 주장 정확.
14. `eq:sm-factor`: 곱 인수분해·$\langle N\rangle=M\theta$ — 일치.
15. `eq:sm-Smix`: Stirling 의 $-m$ 항 상쇄($-M+N+(M-N)=0$) 포함 재계산 — 일치.
16. `eq:sm-mucount`: $-T\,\partial S_\mathrm{mix}/\partial N=+k_BT\ln[\theta/(1-\theta)]$; eq:fermifn 반전 경로와 합치(앙상블 동등성 계산 확인) — 일치.
17. `eq:sm-muideal` verifybox: $\theta=\tfrac12$ 에서 $\mu=\mu^0$·$S_\mathrm{mix}$ 자리당 최대 $k_B\ln2$ — 일치.
18. 교차참조 실물 대조: `eq:Veq`·`eq:spinodal`(srcbox 표의 두 항·문턱), `eq:Z1`, `eq:Svib_mode`, `eq:muV`, §center 의 $\mu\equiv\partial G/\partial n|_{T,P}$·$\partial U_j/\partial T=\Delta S_{\rxn,j}/F$, §eqpeak 의 $\xi_\eq(1-\xi_\eq)$ 종·요동 정체 서술, §dist 의 "두 얼굴" 원문 — 전부 인용처 원문과 정합(불일치는 A02-13 표기 층위뿐).
19. 빌드 라벨: `ch1_graphite_v1.0.22.log` 의 undefined 경고 3건은 전부 폰트 셰이프 경고 — 본 절 라벨·참조 미해소 없음(aux 대조).

## 5. 서치 절 (하이쿠 서브에이전트 위임 여부)

**위임 불요 판단 — 신규 문헌 수요 0건.** 본 절의 인용 5키(hill1960·fowler1939·mckinnon1983·mcquarrie1976·ashcroftmermin1976)는 (i) `_sections/ch1v22_bib.tex:12–16` 에 전부 실재하고, (ii) `results/V1022_REFERENCE_LEDGER.md` 의 승계 선언(v1.0.21 원장 전건 승계) + v1.0.21 원장 18행("기존 V1 키(hill1960·mcquarrie1976 등 통계역학 교과서 앵커)")으로 V1 지위가 확인된다. 본 검토의 전 제안은 대수 항등·구조 재배치·기존 라벨 상호 참조만 사용 — 새 서지 주장 없음(A02-06 각주도 원문 인용 없이 좌표 대수만 사용하도록 설계). 따라서 기억 서지 금지 규율 위반 소지 자체가 없음.

## 6. 말미 4-tier

- **확정** (원문 대조·재계산으로 확인): §4 의 1–19 전 항목; A02-01(두 사다리 불일치 — 02b 원문 대조), A02-13(eq:Svib_mode 원표기와 인용 기호 상이 — ch2_sec03_vibel.tex:24 대조), A02-15(`k_B` 22회 vs `\kB` 1회 — grep 계수), A02-14($\mu_\mathrm{Li}$↔$\mu$ 표기 요동 — 행 대조), 인용 5키의 bib 실재.
- **추정** (근거 있는 판단·저자 의도 해석 포함): A02-05(현행 문장도 정독하면 정합 독해가 가능하나 1차 독해 혼동 위험이 크다는 판단), A02-07·08(수식화가 순이득이라는 판단 — 식 번호 재배열 부담은 자동 번호라 경미), A02-02·03·04(독자 질문 1순위라는 우선순위 판단), McKinnon--Haering 등온선의 좌표 배향($x$=삽입 분율) — 표준 교과서 지식과 본문 srcbox 서술로 뒷받침되나 원문 쪽 대조는 미수행.
- **미검증**: mckinnon1983·hill1960 등 원전의 쪽·식 번호 수준 세부(원장 V1 승계 신뢰에 의존); 제안 LaTeX 의 실조판(컴파일은 미실행 — 보고 전용 규율상 소스 무수정); 빌드 PDF 페이지 배치 영향.
- **무발견 축** (검토했으나 문제 없음): ② 논리 오류 축 — **H급 발견 0**: 전 수식 재계산·전 극한 검산·전 부호 읽기 통과(§4). P3 관련 — $V_n$ 위계(본 절 무관여·위반 없음), 전하 보존 중심식 지위(02b 로 위임·서두 반영 누락은 A02-01 로 처리), ver.N↔Chapter 명칭 혼동(본 절 등장 없음) 각각 이상 없음. GS-1/GS-2 정직 공백 관련 제안 없음(무저촉). 자산 마커(A-015~A-046·V20-001/002) 보존과 충돌하는 제안 없음. tikz 그림(fig:sm-reservoir)·캡션 — 물리 서술 정확, 이상 없음.

## 7. 규율 준수 확인

- 보고 전용: 소스 파일·git·`Codex/` 일절 무접촉(read 도 지시 범위 내 파일만). 산출물은 본 파일 1본.
- 조기 저장: 파일 선생성(헤더) 후 본문 완성분으로 갱신.
- 등급·양식: BRIEF 표 양식 + 축자 정본 코드블록(개행 보존) + 등급별 정리 + 4-tier + 무발견 축 명시.
