# V1012 Phase 4.3 Draft C3 — Step 2/3 supplement (peak·decomp only)

> 대상: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`  
> 범위: `sec:lco-peak`(L1220--1232) · `sec:lco-decomp`(L1715--1766)  
> 출력 성격: `.tex` 편입 전 supplement. **`.tex`/코드 수정 없음.**  
> Step 1 완료 범위(`center`·`hys`)는 `Claude/results/process/V1012_P43_draft_C3_s1.md` 기준으로 두고, 본 파일은 Step 2의 두 절만 다룬다.

## 0. 확인 범위와 불가침

- 직접 확인한 v1.0.12 원문 범위:
  - `sec:width`의 `eq:xieq` 및 분포 다리: L722--944.
  - `sec:eqpeak` 및 `sec:lco-peak`: L1184--1233.
  - `sec:lco-electronic`: L945--1183. 단, 전자 엔트로피 절은 참조 라벨·부호·온도 의존만 대조했고 본문 수정 대상으로 삼지 않는다.
  - `sec:sum` 및 `sec:lco-decomp`: L1672--1766.
  - LCO 전이표 `tab:lco-staging`: L301--356.
- 불가침:
  - `sec:lco-electronic`, `sec:lco-Se`, `sec:lco-gate`, 코드 절은 수정 대상 아님.
  - 물리·결과식·부호·수치 불변. T1/T2/T3 전위, config 수치, 전자항 부호, `\Delta S_e\propto T` 판단을 새 값으로 바꾸지 않음.
  - 신규 개념 도입 없음. 기존 `\xi_\eq`, `w_j`, `Q_j`, `U_j^{\,d}`, `\Delta S_{\rxn,j}^\mathrm{cat}`, `Z_\mathrm{config}\cdot Z_\mathrm{elec}` 논리를 선형 사슬로 재배열한다.

---

## 1. `sec:lco-peak`

### 1.1 위치

- 헤더 보존: L1220 `\subsection{LCO dQ/dV peak — 양극 영역의 세 봉우리}\label{sec:lco-peak}`.
- 교체 후보: L1221--1232의 줄글 결론.
- 근거식 보존: `eq:xieq`(L787--788), `eq:eqpeak`(L1203--1210), `eq:sum`(L1679--1682).
- 다음 경계: L1234 `\subsection{평형 델타가 실측 종이 되는 까닭 ...}\label{sec:broadening}`.

### 1.2 LaTeX 사슬

```latex
\textbf{(a) 출발 — LCO 세 전이의 평형 점유.}
LCO 양극 절에서도 평형 peak 의 출발점은 \S\ref{sec:width} 의 같은 logistic 점유다.
전이 집합을
\[
\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}
\]
로 두면 각 전이의 평형 진행률은
\[
\xi_{\eq,j}(V,T)
=\frac{1}{1+\exp[-z_j]},\qquad
z_j\equiv \frac{\sigma_d\big(V-U_j^{\,d,\mathrm{cat}}\big)}{w_j},
\qquad j\in\mathcal J_\mathrm{LCO}.
\]
여기서 LCO 로 바뀌는 것은 중심 $U_j^{\,d,\mathrm{cat}}$ 와 전이별 입력값뿐이고,
식~\eqref{eq:xieq} 의 함수형은 그대로다.

\textbf{(b) 연산 — $\xi_{\eq,j}$ 를 전압으로 미분.}
식~\eqref{eq:belliden} 의 logistic 미분 항등식
\[
\frac{\dd\xi_{\eq,j}}{\dd z_j}
=\xi_{\eq,j}(1-\xi_{\eq,j})
\]
에 연쇄율
\[
\frac{\dd z_j}{\dd V}=\frac{\sigma_d}{w_j}
\]
을 곱하면
\[
\frac{\dd\xi_{\eq,j}}{\dd V}
=\frac{\sigma_d}{w_j}\xi_{\eq,j}(1-\xi_{\eq,j}).
\]
따라서 코드가 쓰는 양의 peak 모양은 방향 부호를 제거한
\[
\mathrm{peak\_shape}_j(V,T)
\equiv
\left|\frac{\dd\xi_{\eq,j}}{\dd V}\right|
=\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}
\]
이다.

\textbf{(c) 중간식 — 용량 가중 선형 합.}
전하 보존식에서 온 합산식~\eqref{eq:sum} 에 LCO 세 전이만 넣으면 평형 기준선은
\[
\left(\frac{\dd Q}{\dd V}\right)_{\mathrm{LCO}}^{\eq}
=C_\bg+\sum_{j\in\mathcal J_\mathrm{LCO}}Q_j\,
\mathrm{peak\_shape}_j(V,T)
=C_\bg+\sum_{j\in\{\mathrm{T1,T2,T3}\}}
Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}.
\]
T1 은 $\sim3.90$ V MIT plateau, T2 는 $\sim4.05$ V, T3 는
$\sim4.17$--$4.20$ V 의 order--disorder 봉우리로 읽는다
(표~\ref{tab:lco-staging}).

\textbf{(d) 박스 — 위치, 순높이, 면적.}
\begin{equation}
\boxed{\;
\mathrm{center}_j=U_j^{\,d,\mathrm{cat}},\qquad
\mathrm{height}_j^{\mathrm{net}}
=Q_j\,\max_V \mathrm{peak\_shape}_j
=\frac{Q_j}{4w_j},\qquad
\mathrm{area}_j^{\mathrm{net}}
=Q_j\int \left|\frac{\dd\xi_{\eq,j}}{\dd V}\right|\dd V
=Q_j\;}
\end{equation}
최대값은 $\xi_{\eq,j}=\tfrac12$ 곧 $V=U_j^{\,d,\mathrm{cat}}$ 에서
$\xi_{\eq,j}(1-\xi_{\eq,j})=\tfrac14$ 이기 때문에 나온다. 면적은
$\int|\dd\xi_{\eq,j}|=1$ 이므로 배경 차감 전이 용량 $Q_j$ 다.
T1 의 전자항은 이 peak 식에 새 peak\_shape 를 더하지 않고,
\S\ref{sec:lco-electronic} 의 $\Delta S_{e,1}^{\mathrm{mol}}(x,T)$ 가
식~\eqref{eq:lco-dUdT} 를 통해 $U_1^{\,d,\mathrm{cat}}(T)$ 의 온도 이동을
바꾸는 경로로만 들어간다.
``$\partial U_1/\partial T$ 가 $T$ 에 선형''이고, 위치 누적 이동은
식~\eqref{eq:U1T2} 처럼 $\propto T^2$ 성분을 갖는다는 원문 판단을 유지한다.
```

### 1.3 원문 대비

- 원문 L1221--1222의 "평형 peak 식은 전극을 가리지 않고 위치·높이·면적이 읽힌다"를 (a) `\xi_{\eq,j}` 출발식, (b) `d\xi/dV`, (c) `\sum Q_j peak_shape`, (d) 위치·높이·면적 박스로 분해했다.
- 원문 L1223--1224의 T1/T2/T3 전위값은 그대로 유지했다. 새 전위값이나 새 전이 이름을 만들지 않았다.
- 원문 L1225--1228의 폭·두-상·order--disorder 날카로움 설명은 `w_j`와 `peak_shape_j`의 지위 설명으로만 연결했다. `\Omega_j` 값을 새로 산출하지 않았다.
- 원문 L1228--1232의 T1 전자항 설명은 전자 엔트로피 절의 내용을 재작성하지 않고, `U_1(T)` 이동 경로와 `\partial U_1/\partial T` 식별 신호만 보존했다.

### 1.4 논리 감사

- 선형성: `C_\bg+\sum_jQ_j peak_shape_j`는 보존식 미분의 직접 결과이므로 LCO 세 전이를 더하는 데 새 물리 가정이 추가되지 않는다.
- 부호: `d\xi/dV`에는 `\sigma_d`가 들어가지만 `peak_shape=|d\xi/dV|`로 쓰므로 peak 높이와 면적은 방향 불변·비음수다.
- 차원: `\xi(1-\xi)`는 무차원, `w_j`는 V이므로 `peak_shape`는 1/V, `Q_j peak_shape`는 용량/V다. 면적 적분은 `Q_j`로 돌아간다.
- 결과식: 중심 `U_j^{\,d,\mathrm{cat}}`, 순높이 `Q_j/(4w_j)`, 면적 `Q_j`는 원문 L1221--1222 및 L1213--1215와 동일하다.
- 전자항 불가침: T1 전자항은 `sec:lco-electronic`의 엔트로피 슬롯을 통해 중심 온도 이동에만 반영된다. `peak_shape` 자체에 전자항 봉우리를 별도로 더하지 않는다.

---

## 2. `sec:lco-decomp`

### 2.1 위치

- 헤더 보존: L1715 `\subsection{LCO $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해 — config + vib + electronic}\label{sec:lco-decomp}`.
- 교체 후보: L1716--1754의 줄글 결론 및 itemize 설명. 단, `eq:lco-decomp` 라벨은 하류 참조가 있으므로 유지해야 한다.
- 보존 후보: L1756--1766의 Ch2/P4 코드 구현 예고는 Step 2 범위에서는 수정 대상이 아니다.
- 참조만 확인: `sec:lco-Se`·`sec:lco-gate`의 `eq:dSemolar`, `eq:dSegate`, `eq:ggate`, `eq:U1T2`.

### 2.2 LaTeX 사슬

```latex
\textbf{(a) 출발 — config 와 electronic 의 가산성 자리.}
LCO 의 삽입 반응 엔트로피는 하나의 숫자처럼 $U_j(T)$ 에 들어가지만,
그 내부에는 리튬 자리 배열(config), 격자진동(vib), 전도 전자(electronic)의
세 성분이 있다. T1 MIT 부근에서 config 와 electronic 을 더해도 되는 최소
근거는 두 자유도를 서로 다른 부분계로 분리하는 근사다:
\[
Z_j \simeq Z_{\mathrm{config},j}\,Z_{\mathrm{elec},j}.
\]
그러면
\[
F_j=-RT\ln Z_j
\simeq -RT\ln Z_{\mathrm{config},j}
-RT\ln Z_{\mathrm{elec},j}
=F_{\mathrm{config},j}+F_{\mathrm{elec},j},
\]
따라서
\[
S_j=-\left(\frac{\partial F_j}{\partial T}\right)
\simeq S_{\mathrm{config},j}+S_{\mathrm{elec},j}.
\]
이는 ``더해도 되는가''에 대한 가산성 근거일 뿐이고, 같은 엔트로피를 두 번 세지
않는다는 보장은 아래 슬롯 정의가 맡는다.

\textbf{(b) 연산 — 세 슬롯의 정의.}
식~\eqref{eq:lco-dUdT} 에 들어가는 LCO 삽입 반응 엔트로피 슬롯을
\[
\Delta S_{\rxn,j}^{\mathrm{cat}}(x,T)
=
\Delta S_{j,\mathrm{slot}}^{\mathrm{config}}
+\Delta S_j^{\mathrm{vib}}
+\Delta S_{e,j}^{\mathrm{mol}}(x,T)
\]
로 둔다. 여기서 각 슬롯의 뜻은 다음처럼 고정한다:
\[
\Delta S_{j,\mathrm{slot}}^{\mathrm{config}}
\equiv \Delta S_j^0
\quad\text{(봉우리 중심 표준값만)},
\]
\[
\Delta S_{e,j}^{\mathrm{mol}}(x,T)
\equiv
\begin{cases}
\text{식~\eqref{eq:dSemolar}$\cdot$\eqref{eq:dSegate} 의 MIT 게이트 골},
& j=\mathrm{T1},\\
0,& j=\mathrm{T2},\mathrm{T3}.
\end{cases}
\]
T2/T3 의 $\approx0.47/1.49$ J/(mol\,K)는 config 중심 표준값의 초기값이고,
T1 의 electronic 은 삽입 기준 음의 MIT 게이트 골이다. vib 는 원문처럼 고-$x$
phonon 음의 baseline 슬롯으로 둔다.

\textbf{(c) 중간식 — logistic 내부 조성항과 게이트 골의 분리.}
config 의 봉우리 내부 조성 의존은 이미 \S\ref{sec:width} 의 logistic 과
\S\ref{sec:eqpeak} 의 미분 종에 들어 있다:
\[
\xi_{\eq,j}(V,T)\longrightarrow
\frac{\dd\xi_{\eq,j}}{\dd V}
\longrightarrow
\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}.
\]
따라서 $\Delta S_{j,\mathrm{slot}}^{\mathrm{config}}$ 에 다시
$R\ln[(1-\xi_j)/\xi_j]$ 형 봉우리 내부 항을 넣으면 같은 리튬 자리 배열 엔트로피를
두 번 세게 된다. 반대로 electronic 슬롯은 리튬 자리 배열이 아니라
\S\ref{sec:lco-electronic} 의 전자 밴드 점유가 만드는 MIT 게이트 골이므로,
config 중심값과 다른 자유도에 속한다.

\textbf{(d) 박스 — 분해식과 이중계산 금지식.}
\begin{equation}
\boxed{\;
\Delta S_{\rxn,j}^{\mathrm{cat}}(x,T)
=
\underbrace{\Delta S_j^0}_{\text{config 중심 표준값}}
+\underbrace{\Delta S_j^{\mathrm{vib}}}_{\text{phonon baseline}}
+\underbrace{\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)}_{\text{T1 MIT 게이트 골}}\;}
\label{eq:lco-decomp}
\end{equation}
\begin{equation}
\boxed{\;
\Delta S_{j,\mathrm{slot}}^{\mathrm{config}}=\Delta S_j^0,\qquad
R\ln\frac{1-\xi_j}{\xi_j}\notin
\Delta S_{j,\mathrm{slot}}^{\mathrm{config}},\qquad
\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)\notin
\Delta S_{j,\mathrm{slot}}^{\mathrm{config}}\;}
\end{equation}
첫 금지항은 logistic 이 이미 담은 봉우리 내부 config 조성 의존의 재삽입을 막고,
둘째 금지항은 MIT 전자 게이트 골을 config 중심값에 흡수하지 못하게 막는다.
이 슬롯 분리는 과대계상을 막는 규칙이지, MIT 부근의 config--electronic 교차 엔트로피를
새로 모델링한다는 뜻은 아니다.
```

### 2.3 원문 대비

- 원문 L1716--1724의 `eq:lco-decomp` 박스는 보존하되, 각 항의 의미를 (a) 가산성, (b) 슬롯 정의, (c) logistic 내부 항과 전자 게이트 골 분리, (d) 이중계산 금지식으로 재배열했다.
- 원문 L1727--1731의 config 설명은 `\Delta S_j^0` 중심 표준값만 슬롯에 넣는 규칙으로 명시했다. 봉우리 내부 조성 의존은 logistic이 이미 담는다는 판단을 유지했다.
- 원문 L1732--1741의 `Z=Z_\mathrm{config}\cdot Z_\mathrm{elec}` 논거는 자유에너지와 엔트로피 가산성 식으로 풀었다. 동시에 원문처럼 이 논거가 교차항을 포착하거나 한계짓는 것은 아니라고 남겼다.
- 원문 L1744--1749의 electronic 설명은 기존 `sec:lco-electronic` 라벨을 참조하는 데 그쳤다. 전자 엔트로피 절의 닫힌식, 부호, 수치, 그림 설명은 재작성하지 않았다.
- 원문 L1750--1754의 "합이 `\partial U/\partial T`와 dQ/dV로 들어간다"는 결론은 유지하되, 이 Step 2 문안에서는 코드 구현 예고(L1756--1766)를 확장하지 않았다.

### 2.4 논리 감사

- 가산성: `Z\simeq Z_config Z_elec`이면 `F=F_config+F_elec`, `S=S_config+S_elec`가 되므로 config와 electronic을 더하는 근거는 있다. 단, 이 근사는 교차 엔트로피를 0으로 두는 선도 차수 가정이다.
- 이중계산: `\Delta S_j^0`는 중심 표준값, `R\ln[(1-\xi)/\xi]`는 logistic 내부 조성 의존, `\Delta S_e^{mol}`은 전자 밴드 MIT 게이트 골로 슬롯을 분리했다. 같은 항을 두 슬롯에 넣지 않는 금지식이 명시됐다.
- 부호: electronic은 원문과 같이 삽입 기준 음의 골(`\Delta S_e<0`)이고, 탈리튬화 방출량은 그 절댓값이다. 부호 뒤집기 없음.
- 수치: T2/T3 config 초기값 `0.47/1.49` J/(mol K), T1 MIT 범위·게이트, `1.1 k_B/atom`, `0.18 k_B/atom`, `-46` J/(mol K) 등 전자항 절의 수치는 새로 계산하거나 바꾸지 않았다.
- 결과식: 분해된 합은 여전히 `\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F`로 중심 온도 이동에 들어가고, 그 중심이 기존 `eq:sum`의 dQ/dV 선형 합에 들어간다. peak 식이나 코드 루프 구조를 바꾸지 않는다.

---

## 3. 3줄 요약

1. Step 2/3은 v1.0.12의 `sec:lco-peak`와 `sec:lco-decomp`만 다뤘고, `.tex`/코드는 수정하지 않았다.
2. `peak`는 `\xi_{\eq,j}` → `d\xi/dV` → `\sum_{j\in\{\mathrm{T1,T2,T3}\}}Q_j peak_shape_j` → center/height/area 박스로 선형화했다.
3. `decomp`는 `Z\simeq Z_\mathrm{config}Z_\mathrm{elec}` → config 중심 `\Delta S_j^0`·electronic MIT 게이트 골 슬롯 → 이중계산 금지 박스로 정리했다.
