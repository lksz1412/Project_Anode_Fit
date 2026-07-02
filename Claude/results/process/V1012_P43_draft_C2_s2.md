# V1012 Phase 4.3 draft C2 s2 — peak/decomp supplement

대상: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`

범위: `sec:lco-peak`(L1220--1232), `sec:lco-decomp`(L1715--1765) 두 절만.  
출발점: `V1012_P43_draft_C2_s1.md`의 형식과 v1.0.12 원문 줄 위치를 대조했다.  
금지 준수: `.tex`/코드 수정 없음, `sec:lco-electronic` 본문 불가침, 물리/결과식/부호/수치 불변, 신규 개념 추가 없음. 전자항은 기존 `\eqref{eq:dSemolar}`/`\eqref{eq:dSegate}`/`\eqref{eq:ggate}` 경로만 참조한다.

읽은 범위:
- `V1012_P43_draft_C2_s1.md`: 전체.
- `graphite_ica_ch1_v1.0.12.tex`: L301--356, L945--1182, L1184--1233, L1672--1766, L1794--1852 직접 확인.

---

## 1. `sec:lco-peak`

### 위치

- 현재 헤더: L1220 `\subsection{LCO dQ/dV peak — 양극 영역의 세 봉우리}\label{sec:lco-peak}`
- 현재 줄글 후보 범위: L1221--1232.
- 직접 근거: 평형 peak 일반식 L1189--1215 `eq:belliden`, `eq:eqpeak`; LCO 전이 표 L325--348 `tab:lco-staging`; 합산식 L1678--1682 `eq:sum`.
- 보존할 수치: T1 `\sim3.90 V`, T2 `\sim4.05 V`, T3 `\sim4.17--4.20 V`, `Q_j/(4w_j)`, 면적 `Q_j`, `w_j=n_jRT/F`.

### LaTeX 사슬

```latex
\textbf{(a) 출발 — LCO 전이별 평형 진행률.}
LCO 하프셀의 세 전이는 같은 전극-중립 logistic 을 쓴다. 전이 집합을
\[
\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}
\]
로 두면, 각 전이의 평형 진행률은 식~\eqref{eq:xieq} 의 LCO 대입형이다:
\begin{equation}
\xi_{\eq,j}(V,T)=
\frac{1}{1+\exp\!\big[-\sigma_d(V-U_j^{\,d,\mathrm{cat}}(T))/w_j\big]},
\qquad j\in\mathcal J_\mathrm{LCO}.
\label{eq:lco-xieq-peak}
\end{equation}
여기서 $U_j^{\,d,\mathrm{cat}}$ 는 \S\ref{sec:lco-center}$\cdot$\S\ref{sec:lco-hys} 가 정한
방향별 중심이고, $w_j$ 는 흑연과 같은 폭 슬롯이다.

\textbf{(b) 연산 — logistic 미분에서 peak 모양으로.}
$z_j=\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j$ 라 두면 식~\eqref{eq:belliden} 의 항등식으로
\[
\frac{\dd\xi_{\eq,j}}{\dd z_j}=\xi_{\eq,j}(1-\xi_{\eq,j}),
\qquad
\frac{\dd z_j}{\dd V}=\frac{\sigma_d}{w_j}.
\]
따라서
\begin{equation}
\frac{\dd\xi_{\eq,j}}{\dd V}
=\frac{\sigma_d}{w_j}\xi_{\eq,j}(1-\xi_{\eq,j}),
\qquad
\text{peak\_shape}^{\eq}_j
=\Big|\frac{\dd\xi_{\eq,j}}{\dd V}\Big|
=\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}.
\label{eq:lco-peakshape}
\end{equation}
미분에는 $\sigma_d$ 가 한 번 들어오지만, peak 모양은 절댓값이라 충방전 방향에 대해 양수다.

\textbf{(c) 중간식 — 세 봉우리의 선형 합.}
전하 보존식의 미분은 전이별 기여를 선형으로 더한다. 그러므로 LCO 평형 기준선은
\begin{equation}
\left(\frac{\dd Q}{\dd V}\right)_{\mathrm{LCO}}^{\eq}
=C_\bg+\sum_{j\in\mathcal J_\mathrm{LCO}}Q_j\,\text{peak\_shape}^{\eq}_j
=C_\bg+\sum_{j\in\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}}
Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}.
\label{eq:lco-peak-sum}
\end{equation}
이 합은 식~\eqref{eq:sum} 의 LCO 세 전이 제한형이며, T1 은 $\sim$3.90 V, T2 는
$\sim$4.05 V, T3 는 $\sim$4.17--4.20 V 의 양극 전위 영역에 놓인다.

\textbf{(d) 박스 — 중심, 높이, 면적.}
\begin{equation}
\boxed{\;
\begin{aligned}
V_{\mathrm{center},j}&=U_j^{\,d,\mathrm{cat}}(T),\\
H_j^{\eq}&=\max_V\{Q_j\,\text{peak\_shape}^{\eq}_j\}
=\frac{Q_j}{4w_j},\\
A_j^{\eq}&=\int Q_j\,\text{peak\_shape}^{\eq}_j\,\dd V
=Q_j\int_0^1\dd\xi_{\eq,j}=Q_j,
\end{aligned}
\qquad j\in\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}\;}
\label{eq:lco-peak-observables}
\end{equation}
폭은 흑연과 같은 $w_j=n_jRT/F$ 슬롯을 쓰며, LCO 의 두-상 전이는 \S\ref{sec:broadening} 의
현상학적 피팅 폭으로 읽는다. T1 의 전자항은 새 peak 식을 만들지 않고,
$\Delta S_{\rxn,1}^\mathrm{cat}$ 를 통해 $U_1^{\,d,\mathrm{cat}}(T)$ 의 온도 이동에만 들어간다.
```

### 원문 대비

- 현재 L1221--1222의 “평형 peak 식은 LCO에도 그대로 적용” 결론을 `\xi_{\eq,j}` 정의, 미분, `peak_shape`, 세 전이 합산, 관측량 박스 순서로 풀었다.
- 현재 L1222의 위치/높이/면적 문장을 `eq:lco-peak-observables` 박스로 분리했다. 결과값은 `U_j^d`, `Q_j/(4w_j)`, `Q_j` 그대로다.
- 현재 L1223--1224의 T1/T2/T3 전위 수치는 같은 자리에서 유지했다.
- 현재 L1225--1228의 폭/두-상/broadening 설명은 박스 뒤 해설로 보존하되, 새 broadening 모델이나 역산 개념을 추가하지 않았다.
- 현재 L1228--1232의 T1 전자항 설명은 “peak 식 변경 없음, 중심 온도 이동 슬롯만 영향”으로 좁혀 적었다. `sec:lco-electronic` 본문은 참조만 한다.

### 논리 감사

- 루핑 선형성: `j\in{T1,T2,T3}` 루프 안에서 `peak_shape_j`를 만들고 `\sum Q_j peak_shape_j`로 더하므로 L1678--1682 `eq:sum`과 일치한다.
- 물리 불변: LCO를 새 전극으로 넣을 뿐 logistic, 폭, 전하 보존식, 합산식은 흑연 N6/N9와 같은 골격이다.
- 결과식 불변: `peak_shape=\xi_\eq(1-\xi_\eq)/w`, 중심 `U_j^d`, 높이 `Q_j/(4w_j)`, 면적 `Q_j` 모두 L1189--1215와 동일하다.
- 부호 불변: `\dd\xi/\dd V`에는 `\sigma_d`가 있으나 peak는 절댓값으로 양수다. L1212--1215의 방향 불변 설명과 충돌하지 않는다.
- 수치 불변: T1/T2/T3 전위, `0.47/1.49` 같은 엔트로피 수치, 전자항 anchor 수치는 새로 만들지 않았다.
- 신규개념 금지: 기존 `\xi_\eq`, `peak_shape`, `Q_j`, `w_j`, `U_j^d`, `C_\bg`, `\mathcal J_\mathrm{LCO}` 표기만 사용했다.

---

## 2. `sec:lco-decomp`

### 위치

- 현재 헤더: L1715 `\subsection{LCO $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해 — config + vib + electronic}\label{sec:lco-decomp}`
- 현재 줄글/식 후보 범위: L1716--1765.
- 직접 근거: 전자 엔트로피 절 L945--1182의 `eq:dSemolar`, `eq:dSegate`, `eq:ggate`, `fig:lco-electronic`; LCO 전이 표 L325--348; 중심식 연결 L1750--1751.
- 보존할 수치/규약: T2/T3 config 중심 표준값 `\approx0.47/1.49 J/(mol\,K)`, 전자항 삽입 기준 `<0`, MIT 게이트 T1 only, 몰당 환산 `\eqref{eq:dSemolar}`.

### LaTeX 사슬

```latex
\textbf{(a) 출발 — 서로 다른 자유도의 분배함수.}
LCO 의 엔트로피 슬롯은 같은 $\Delta S_{\rxn,j}^\mathrm{cat}$ 로 들어가지만,
config 와 electronic 은 서로 다른 자유도다. 선도 차수에서 두 부분계의 교차항을 무시하면
\begin{equation}
Z_j^\mathrm{cat}\simeq
Z_{j,\mathrm{config}}\cdot Z_{j,\mathrm{elec}}
\qquad(\text{vib 는 별도 baseline 슬롯}).
\label{eq:lco-Zfact}
\end{equation}
따라서 $S=k_B\partial(T\ln Z)/\partial T$ 의 가산성으로
\[
S_j^\mathrm{cat}\simeq S_{j,\mathrm{config}}+S_{j,\mathrm{elec}}
\quad(\text{그리고 }S_{j,\mathrm{vib}}\text{ baseline}).
\]
이 식은 ``더할 수 있음''만 말하며, 같은 엔트로피를 두 번 세지 않는 규칙은 아래 슬롯 정의가 따로 정한다.

\textbf{(b) 연산 — 세 슬롯의 정의.}
LCO forward 슬롯에 들어가는 총 반응 엔트로피는 기존 식~\eqref{eq:lco-decomp} 처럼
\begin{equation}
\Delta S_{\rxn,j}^\mathrm{cat}(V,T)=
\Delta S_{j,\mathrm{slot}}^\mathrm{config}
+\Delta S_j^\mathrm{vib}
+\Delta S_{e,j,\mathrm{slot}}^{\,\mathrm{mol}}(V,T).
\label{eq:lco-decomp-slot}
\end{equation}
각 슬롯은 다음처럼 좁게 정의한다:
\[
\Delta S_{j,\mathrm{slot}}^\mathrm{config}\equiv\Delta S_j^0
\quad(\text{봉우리 중심 표준값만}),
\]
\[
\Delta S_{e,j,\mathrm{slot}}^{\,\mathrm{mol}}(V,T)=
\begin{cases}
\Delta S_{e,1}^{\,\mathrm{mol}}\!\big(x(\xi_{\eq,1}(V)),T\big), & j=\mathrm{T1},\\
0, & j=\mathrm{T2},\mathrm{T3}.
\end{cases}
\]
config 슬롯의 $\Delta S_j^0$ 는 표~\ref{tab:lco-staging} 의 중심 표준값이며,
electronic 슬롯은 \S\ref{sec:lco-electronic} 의 MIT 게이트 \emph{골}을 몰당 환산해 넣은 값이다.

\textbf{(c) 중간식 — logistic 내부항과 게이트 골을 분리.}
config 의 봉우리 내부 조성 의존
\[
R\ln\frac{1-\xi_{\eq,j}}{\xi_{\eq,j}}
\]
은 식~\eqref{eq:xieq} 와 식~\eqref{eq:belliden} 의 logistic 이 이미 만든다. 그러므로 이 항을
$\Delta S_{j,\mathrm{slot}}^\mathrm{config}$ 에 다시 넣지 않는다. 반대로 전자 슬롯은
식~\eqref{eq:dSegate}$\cdot$\eqref{eq:dSemolar} 의 삽입 기준 음의 골만 받는다:
\[
\Delta S_{e,1}^{\,\mathrm{mol}}(x,T)<0,\qquad
|\Delta S_{e,1}^{\,\mathrm{mol}}|\text{ 는 MIT 게이트 중심에서 국소 최대}.
\]
즉 config 는 중심 표준값, electronic 은 T1 게이트 골이다. 두 슬롯은 같은 값을 나눠 갖지 않는다.

\textbf{(d) 박스 — 이중계산 금지식.}
\begin{equation}
\boxed{\;
\begin{aligned}
\Delta S_{\rxn,j}^\mathrm{cat}(V,T)
&=\underbrace{\Delta S_j^0}_{\text{config: 중심 표준값만}}
+\underbrace{\Delta S_j^\mathrm{vib}}_{\text{baseline}}
+\underbrace{\Delta S_{e,j,\mathrm{slot}}^{\,\mathrm{mol}}(V,T)}_{\text{electronic: MIT 게이트 골만}},\\[2pt]
\Delta S_{j,\mathrm{slot}}^\mathrm{config}
&\equiv\Delta S_j^0
\quad\text{and not}\quad
\Delta S_j^0+R\ln\frac{1-\xi_{\eq,j}}{\xi_{\eq,j}},\\[2pt]
\Delta S_{e,j,\mathrm{slot}}^{\,\mathrm{mol}}(V,T)
&=
\begin{cases}
\Delta S_{e,1}^{\,\mathrm{mol}}\!\big(x(\xi_{\eq,1}(V)),T\big)<0, & j=\mathrm{T1},\\
0, & j=\mathrm{T2},\mathrm{T3}.
\end{cases}
\end{aligned}
\;}
\label{eq:lco-no-double-count}
\end{equation}
이 합이 식~\eqref{eq:lco-dUdT} 의
$\partial U_j^\mathrm{cat}/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$ 로 들어가고,
그 중심이 같은 합산식~\eqref{eq:sum} 의 LCO peak 위치를 정한다.
```

### 원문 대비

- 현재 L1716--1724의 분해 박스는 유지하되, 그 앞에 `Z_config \cdot Z_elec` 가산성 출발점을 둬 “왜 더할 수 있는가”를 먼저 닫았다.
- 현재 L1725--1741의 config 설명과 이중계산 방지를 `slot definition -> no-double-count box`로 선형화했다.
- 현재 L1727--1731의 “config는 중심 표준값만”을 박스의 둘째 줄로 못박았다. `R\ln[(1-\xi)/\xi]`는 logistic 내부항이라 슬롯에 다시 넣지 않는다는 원문 의미를 보존했다.
- 현재 L1744--1748의 electronic 설명은 T1 only, 삽입 기준 `<0`, 몰당 `eq:dSemolar`, MIT 게이트 골이라는 기존 내용만 가져왔다.
- 현재 L1750--1754의 중심식/round-trip 연결은 박스 뒤 문장으로 유지했다.
- 현재 L1756--1765의 Ch2/P4 코드 구현 예고는 이 스텝의 재작성 핵심이 아니므로 수식 사슬에 섞지 않았다. 좌표 매핑은 전자 슬롯 정의의 `x(\xi_{\eq,1}(V))`로만 반영했다.

### 논리 감사

- 루핑 선형성: `j=T1,T2,T3`별로 같은 `\Delta S_{\rxn,j}^\mathrm{cat}` 슬롯을 만들고, T1만 electronic이 nonzero다. 이는 표 L341--343 및 L1748과 일치한다.
- 물리 불변: config와 electronic의 가산성은 원문 L1732--1738의 직교 자유도 설명을 `Z` 인수분해로 앞세운 것이다. vib는 기존 baseline 슬롯으로 남겼다.
- 결과식 불변: 총합은 기존 `eq:lco-decomp`의 `config + vib + electronic` 그대로이며, 이후 `\partial U/\partial T=\Delta S/F` 연결도 L1750--1751과 같다.
- 부호 불변: electronic은 삽입 기준 `<0`, T1 MIT 게이트 골로만 들어간다. 부호 뒤집기나 탈리튬화 기준 재정의는 없다.
- 수치 불변: `0.47/1.49 J/(mol K)`, `g_max=13`, `x_MIT`, `\Delta x_MIT`, `-46 J/(mol K)` 등 전자절 수치를 새로 계산하거나 변경하지 않았다. 본 절에서는 기존 참조만 사용한다.
- 신규개념 금지: `Z` 인수분해는 원문 L1734--1738의 “분배함수 인수분해”를 앞으로 이동한 것이며 새 모델이 아니다. indicator 함수 같은 새 표기 대신 cases만 사용했다.
- 전자엔트로피 절 불가침: `sec:lco-electronic`의 식과 문장은 수정 대상이 아니며, decomp는 그 결과값을 slot으로 받기만 한다.

---

## 3줄 요약

1. `sec:lco-peak`는 `\xi_{\eq,j}`에서 `\dd\xi/\dd V`, `peak_shape_j`, `\sum_{j\in{T1,T2,T3}}Q_j peak_shape_j`로 이어지고, 중심/높이/면적을 `U_j^d`, `Q_j/(4w_j)`, `Q_j` 박스로 닫는 사슬로 정리했다.
2. `sec:lco-decomp`는 원문의 `Z=Z_config\cdot Z_elec` 가산성 설명을 출발점으로, config는 중심 `\Delta S_j^0`, electronic은 T1 MIT 게이트 골만 받는 슬롯 정의와 이중계산 금지 박스로 정리했다.
3. 두 절 모두 원문 수치·부호·물리·결과식은 바꾸지 않았고, 전자엔트로피 절은 참조만 했으며 TeX/코드 파일은 수정하지 않았다.
