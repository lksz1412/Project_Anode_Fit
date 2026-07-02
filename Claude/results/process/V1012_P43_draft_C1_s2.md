# V1012 Phase 4.3 draft C1 — step 2/3 restart (peak/decomp only)

> 대상 원천: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`
> 대상 절: `sec:lco-peak`(L1220--1232) 및 `sec:lco-decomp`(L1715--1765)
> 계승: `Claude/results/process/V1012_P43_draft_C1_s1.md` 의 step 1(center/hys) 완료 판단
> 산출물 성격: finalizer 편입용 supplement 초안. `.tex`/코드 수정 없음.

## 0. 확인 범위와 경계

- `sec:lco-peak`는 L1220 헤더 아래 L1221--1232의 줄글 결론을 대상으로 한다.
- `sec:lco-decomp`는 L1715 헤더 아래 L1716--1754의 분해 및 이중계산 설명을 사슬형으로 재작성하는 후보다. L1756--1765의 `Ch2/P4 코드 구현 예고`는 이번 사슬의 직접 교체 대상이 아니라 보존 후보로 둔다.
- 주변 근거로 `eq:xieq`(L787--788), `eq:eqpeak`(L1203--1210), `eq:sum`(L1679--1682), `tab:lco-staging`(L325--348), `eq:dSe`/`eq:dSemolar` 및 부호 설명(L1025--1065)을 확인했다.
- 불가침: `sec:lco-center`, `sec:lco-hys`, `sec:lco-electronic`, `sec:lco-Se`, `sec:lco-gate`, forward 코드, 수치값, 부호 규약은 수정하지 않는다.
- 이번 초안은 새 물리 개념을 추가하지 않는다. 이미 원문에 있는 LCO 세 전이, logistic 평형 peak, config/vib/electronic 슬롯, `Z_\mathrm{config}\cdot Z_\mathrm{elec}` 가산성, 이중계산 금지 규칙만 사슬형으로 정리한다.

## 1. `sec:lco-peak` supplement

### 위치

- 헤더 보존: L1220 `\subsection{LCO dQ/dV peak — 양극 영역의 세 봉우리}\label{sec:lco-peak}`
- 교체 후보: L1221--1232의 줄글
- 전제 보존: 식~`\eqref{eq:eqpeak}` 및 `peak_shape = ksi_eq * (1 - ksi_eq) / w`는 흑연 절의 결과식 그대로 사용한다.
- 수치 보존: T1 `\sim`3.90 V, T2 `\sim`4.05 V, T3 `\sim`4.17--4.20 V, T1 온도 이동률과 `T^2` 위치 이동 설명은 원문 값과 문장을 보존한다.

### LaTeX 사슬

```latex
\textbf{(a) 출발 — LCO 세 전이의 평형 점유.}
LCO 에서도 평형 peak 의 출발점은 흑연과 같은 평형 점유다. 표~\ref{tab:lco-staging}
의 세 전이를
\[
\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}
\]
로 두면, 각 전이는 식~\eqref{eq:xieq} 의 같은 logistic 을 받는다:
\begin{equation}
\xi_{\eq,j}^{\mathrm{LCO}}(V,T)
=\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d})/w_j]},
\qquad
j\in\mathcal J_\mathrm{LCO}.
\label{eq:lco-xieq-peak}
\end{equation}
여기서 $U_j^{\,d}$ 는 \S\ref{sec:lco-center}$\cdot$\S\ref{sec:lco-hys} 에서
이미 정해진 방향별 중심이고, $w_j$ 는 \S\ref{sec:width}$\cdot$\S\ref{sec:broadening}
의 폭이다. 전극이 LCO 로 바뀌어도 peak 모양을 만드는 변수는 새로 생기지 않는다.

\textbf{(b) 연산 — 평형 점유를 전압으로 미분.}
식~\eqref{eq:lco-xieq-peak} 에
\[
z_j=\frac{\sigma_d(V-U_j^{\,d})}{w_j}
\]
를 두면 식~\eqref{eq:belliden} 의 종 항등식이 그대로 적용된다:
\[
\frac{\dd \xi_{\eq,j}^{\mathrm{LCO}}}{\dd z_j}
=\xi_{\eq,j}^{\mathrm{LCO}}(1-\xi_{\eq,j}^{\mathrm{LCO}}).
\]
연쇄율 $\dd z_j/\dd V=\sigma_d/w_j$ 를 곱하면
\begin{equation}
\frac{\dd \xi_{\eq,j}^{\mathrm{LCO}}}{\dd V}
=\frac{\sigma_d}{w_j}\,
\xi_{\eq,j}^{\mathrm{LCO}}(1-\xi_{\eq,j}^{\mathrm{LCO}}),
\qquad
\left|\frac{\dd \xi_{\eq,j}^{\mathrm{LCO}}}{\dd V}\right|
=\frac{\xi_{\eq,j}^{\mathrm{LCO}}(1-\xi_{\eq,j}^{\mathrm{LCO}})}{w_j}.
\label{eq:lco-dxidv-peak}
\end{equation}
따라서 방향 부호 $\sigma_d$ 는 미분 부호에는 남지만, 관측 peak 모양에는 절댓값으로
들어가 양수다.

\textbf{(c) 중간식 — 세 전이의 선형 합산.}
전하 보존식의 선형 합산은 식~\eqref{eq:sum} 과 같다. 그러므로 LCO 평형 성분은
\begin{equation}
\left(\frac{\dd Q}{\dd V}\right)_{\mathrm{LCO}}^\eq
=C_\bg+\sum_{j\in\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}}
Q_j\,\frac{\xi_{\eq,j}^{\mathrm{LCO}}(1-\xi_{\eq,j}^{\mathrm{LCO}})}{w_j}.
\label{eq:lco-eqsum-peak}
\end{equation}
즉 코드의 \code{peak\_shape} 는 LCO 에서도 전이별로
\[
\mathrm{peak\_shape}_j
=\frac{\xi_{\eq,j}^{\mathrm{LCO}}(1-\xi_{\eq,j}^{\mathrm{LCO}})}{w_j}
\]
이고, 전체 dQ/dV 는 $Q_j$ 를 곱한 뒤 세 전이를 더한 것이다.

\textbf{(d) 박스 — LCO peak 의 중심, 높이, 면적.}
\begin{equation}
\boxed{\;
\begin{aligned}
\mathrm{center}_j &= U_j^{\,d},\\
\mathrm{height}_j^\mathrm{net} &=
\max_V\left[Q_j\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}\right]
=\frac{Q_j}{4w_j},\\
\mathrm{area}_j^\mathrm{net} &=
\int Q_j\left|\frac{\dd\xi_{\eq,j}}{\dd V}\right|\dd V
=Q_j.
\end{aligned}
\qquad
j\in\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}\;}
\label{eq:lco-peak-box}
\end{equation}
따라서 LCO 하프셀은 양극 전위 영역에 세 봉우리를 남긴다: T1 은
$\sim$3.90 V 의 MIT plateau, T2 는 $\sim$4.05 V, T3 는
$\sim$4.17--4.20 V 의 order--disorder 봉우리다. 폭은 흑연과 같은
$w_j=n_jRT/F$ 꼴이지만, LCO 의 두-상 전이에서는 \S\ref{sec:broadening}
의 현상학적 broadening 폭으로 읽는다. T1 의 위치는 전자항이
$\Delta S_{\rxn,1}^\mathrm{cat}$ 를 통해 $U_1(T)$ 의 온도 이동에 기여하므로
(식~\eqref{eq:lco-dUdT}), 다온도 dQ/dV 에서 관측 신호는
$\partial U_1/\partial T$ 가 $T$ 에 선형으로 커지는 것이다
($\Delta S_{e,1}\propto T$, \S\ref{sec:lco-Se}); 위치 자체는 선형이 아니라
$T^2$ 이동을 갖는다. 도핑은 \S\ref{sec:lco-hys} 대로 봉우리를
smear$\cdot$shift 시킨다.
```

### 원문 대비

- 원문 L1221--1222의 `eq:eqpeak` 적용 결론을 (a)--(d) 사슬로 풀었다.
- 원문의 세 양 `위치 = 중심`, `순높이 = Q_j/(4w_j)`, `면적 = Q_j`는 박스에 모았다.
- 원문 L1223--1224의 T1/T2/T3 전위 숫자와 성격은 그대로 유지했다.
- 원문 L1225--1228의 폭 지위와 order--disorder 날카로움은 박스 뒤 문장으로 유지했다.
- 원문 L1228--1232의 T1 전자항 관측 신호는 전자엔트로피 절을 새로 설명하지 않고 참조만 유지했다.

### 논리 감사

- 선형성: `eq:sum`의 `C_\bg+\sum_jQ_j[peak_shape_j]` 구조만 사용했다. LCO 세 봉우리는 서로소 전이의 선형 합이다.
- 부호: `\sigma_d`는 `d\xi/dV`에는 들어가지만 peak 모양은 절댓값이므로 양수다. 원문과 동일하다.
- 결과식: 중심 `U_j^{\,d}`, 높이 `Q_j/(4w_j)`, 면적 `Q_j`는 흑연 `eq:eqpeak`에서 직접 온다.
- 수치: T1/T2/T3 전위와 `T^2` 설명 외 새 수치 없음.
- 신규개념 금지: 새 물리 항, 새 broadening 메커니즘, 새 전자항 유도 없음.

## 2. `sec:lco-decomp` supplement

### 위치

- 헤더 보존: L1715 `\subsection{LCO $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해 — config + vib + electronic}\label{sec:lco-decomp}`
- 교체 후보: L1716--1754의 분해 및 이중계산 설명
- 보존 후보: L1756--1765 `Ch2/P4 코드 구현 예고(두 설계 항목)` 문단은 이번 step의 직접 재작성 대상 밖이다.
- 필수 라벨: `\label{eq:lco-decomp}` 재사용. 후속 참조가 `sec:lco-center`, `sec:lco-Se`, `sec:lco-code`, 요약표에 있으므로 삭제/변경 금지.

### LaTeX 사슬

```latex
\textbf{(a) 출발 — 전체 엔트로피 슬롯은 하나다.}
흑연에서 합산식~\eqref{eq:sum} 과 중심식~\eqref{eq:Uj} 에 들어가는
$\Delta S_{\rxn,j}$ 는 한 덩이로 작용했다. LCO 에서도 코드 경로와 결과식은
바뀌지 않는다. 바뀌는 것은 그 한 슬롯의 내부 독해다:
\[
\Delta S_{\rxn,j}^\mathrm{cat}
\quad\hbox{is evaluated before}\quad
\frac{\partial U_j}{\partial T}
=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]
따라서 분해는 새 peak 식이 아니라, $U_j(T)$ 에 들어가기 전의
$\Delta S_{\rxn,j}^\mathrm{cat}$ 를 세 자유도 몫으로 읽는 bookkeeping 이다.

\textbf{(b) 연산 — 분배함수의 가산성.}
LCO T1 MIT 부근에서도 리튬 자리 배열(config)과 전도 전자 밴드 점유(electronic)는
서로 다른 자유도다. 이중계산 문제가 생기는 두 몫만 떼어, 선도 차수에서
두 부분계의 분배함수를
\begin{equation}
Z_j^{\mathrm{config+elec}}
\simeq Z_{\mathrm{config},j}\,Z_{\mathrm{elec},j}
\label{eq:lco-Z-factor}
\end{equation}
로 인수분해하면,
\[
F_j^{\mathrm{config+elec}}=-k_BT\ln Z_j^{\mathrm{config+elec}}
=F_{\mathrm{config},j}+F_{\mathrm{elec},j}
\]
이고
\[
S_j^{\mathrm{config+elec}}
=-\frac{\partial F_j^{\mathrm{config+elec}}}{\partial T}
=S_{\mathrm{config},j}+S_{\mathrm{elec},j}.
\]
이 연산은 config 와 electronic 을 ``더해도 되는가''에 대한 근거일 뿐이다.
vib 는 별도 phonon baseline 슬롯으로 더해지며, 같은 엔트로피를 두 번 세지
않는다는 보장은 아래 슬롯 정의가 맡는다.

\textbf{(c) 중간식 — 세 슬롯의 정의.}
forward 슬롯에 들어가는 몰당 삽입 반응 엔트로피는
\begin{equation}
\Delta S_{\rxn,j}^\mathrm{cat}(x,T)
=\Delta S_j^\mathrm{config}
+\Delta S_j^\mathrm{vib}
+\Delta S_{e,j}^{\,\mathrm{mol}}(x,T).
\label{eq:lco-decomp-mid}
\end{equation}
여기서 세 슬롯은 서로 다른 양을 받는다.
\[
\Delta S_j^\mathrm{config}
\equiv \Delta S_j^0
\quad\hbox{(봉우리 중심 표준값)}
\]
이다. 봉우리 내부 조성 의존
$R\ln[(1-\xi)/\xi]$ 는 \S\ref{sec:dist}$\cdot$\S\ref{sec:width} 의 logistic 이
이미 담고 있으므로, config 슬롯에 다시 넣지 않는다.
\[
\Delta S_j^\mathrm{vib}
\quad\hbox{is the phonon baseline}
\]
이며, 흑연의 음의 baseline 과 같은 자리다. 마지막으로
\[
\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)
=N_A\,\frac{\partial S_e}{\partial x}\Big|_T
\]
는 \S\ref{sec:lco-Se} 의 몰당 전자항이다. 이 항은 삽입 기준에서
MIT 게이트의 음의 골로 들어가며, T1 에서만 켜진다.

\textbf{(d) 박스 — LCO 엔트로피 분해와 이중계산 금지식.}
\begin{equation}
\boxed{\;
\Delta S_{\rxn,j}^\mathrm{cat}(x,T)=
\underbrace{\Delta S_j^0}_{\substack{\mathrm{config}\\\mathrm{center\ value}}}
+
\underbrace{\Delta S_j^\mathrm{vib}}_{\substack{\mathrm{phonon}\\\mathrm{baseline}}}
+
\underbrace{\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)}_{\substack{\mathrm{MIT\ gate}\\\mathrm{electronic\ trough}}}
\;}
\label{eq:lco-decomp}
\end{equation}
\begin{equation}
\boxed{\;
\Delta S_j^\mathrm{config}\ \hbox{contains center } \Delta S_j^0\ \hbox{only},
\qquad
R\ln\frac{1-\xi_{\eq,j}}{\xi_{\eq,j}}\ \hbox{belongs to the logistic peak},
\qquad
\Delta S_{e,j}^{\,\mathrm{mol}}\ \hbox{belongs to the MIT gate only}.
\;}
\label{eq:lco-no-double-count}
\end{equation}
곧 config 슬롯은 봉우리 중심 표준값, electronic 슬롯은 MIT 게이트 골,
vib 슬롯은 phonon baseline 이다. config 의 봉우리 내부 조성 의존과 electronic 의
MIT 게이트를 같은 측정 엔트로피에 중복 배정하지 않는다. 이 세 몫의 합이
식~\eqref{eq:lco-dUdT} 의
$\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$ 를 통해
LCO $U_j(T)$ 의 온도 이동을 정하고, 그 $U_j(T)$ 가 흑연과 같은
합산식~\eqref{eq:sum} 으로 dQ/dV 에 들어간다. 연속
$\Delta S(x)$$\cdot$$g(E_F)(x)$$\cdot$도핑 shift 의 정밀값은
1차 문헌에 없으므로(갭 G1$\cdot$G2$\cdot$G4), 표~\ref{tab:lco-staging}
$\cdot$식~\eqref{eq:ggate} 의 초기값을 우리 코인 하프셀 데이터로
round-trip 피팅해 식별한다.
```

### 원문 대비

- 원문 L1716--1718의 "식과 코드 경로는 그대로, 내부 분해만 추가"를 (a) 출발로 분리했다.
- 원문 L1732--1741의 `Z=Z_config\cdot Z_elec` 가산성 논리를 (b) 연산으로 명시했다. `vib`는 원문 슬롯의 phonon baseline 으로만 유지하고, config/electronic 이중계산 사슬에는 끼우지 않았다.
- 원문 L1720--1723의 `eq:lco-decomp`는 (d) 박스에서 라벨을 재사용한다.
- 원문 L1727--1731의 config 이중계산 금지는 `center \Delta S_j^0 only`와 logistic 내부항 분리로 박스화했다.
- 원문 L1744--1748의 electronic 설명은 MIT 게이트의 음의 골, 삽입 기준, 몰당 환산, T1 한정만 유지했다.
- 원문 L1750--1754의 dQ/dV 연결과 round-trip 피팅 원칙은 박스 뒤 문장으로 유지했다.
- L1756--1765의 코드 구현 예고는 이번 교체 블록 밖 보존 후보로 둔다. 이번 산출물은 `.tex`와 코드를 수정하지 않는다.

### 논리 감사

- 선형성: `S=-\partial F/\partial T`와 `\ln(Z_config Z_elec)`의 합만 사용했다. 교차항을 새 모델로 만들지 않는다.
- 물리: config는 리튬 자리 점유 배열, vib는 phonon baseline, electronic은 전도 전자 밴드 점유다. 원문 자유도 구분 그대로다.
- 결과식: `eq:lco-decomp`의 세 항 합을 유지한다.
- 부호: electronic은 삽입 기준 `\Delta S_{e,j}^{mol}<0`인 MIT 게이트 골이다. 부호 뒤집기 없음.
- 수치: `0.47/1.49` J/(mol K), `1.1 k_B/atom`, `0.18 k_B/atom`, `-46` J/(mol K) 같은 기존 수치는 새 박스 안에 직접 추가하지 않았다. 필요한 경우 원문 `sec:lco-Se`와 표 참조로 보존한다.
- 신규개념 금지: 새 residual 항, 새 fitting parameter, 새 전자엔트로피 절 문장 없음.

## 3. 라벨 및 삽입 주의

- `eq:lco-decomp`는 기존 라벨 재사용 필수다.
- 신설 후보 라벨은 `eq:lco-xieq-peak`, `eq:lco-dxidv-peak`, `eq:lco-eqsum-peak`, `eq:lco-peak-box`, `eq:lco-Z-factor`, `eq:lco-decomp-mid`, `eq:lco-no-double-count`다. 실제 편입 전 finalizer가 `rg "\\label\\{eq:lco-"`로 충돌을 재확인해야 한다.
- `sec:lco-peak`의 수식 사슬은 `eq:eqpeak`와 `eq:sum`의 LCO 대입형이다. 새 peak 물리를 만들지 않는다.
- `sec:lco-decomp`의 수식 사슬은 `eq:lco-decomp`의 설명 구조 변경이다. 전자엔트로피 본유도(`sec:lco-Se`)는 참조만 하고 손대지 않는다.
- `\Omega_j`, `U_j^{\,d}`, `w_j`, `Q_j`, `\sigma_d`, `\Delta S_{e,j}^{\,\mathrm{mol}}` 표기는 현 v1.0.12 원문 표기를 유지한다.

## 4. 3줄 요약

1. `peak`는 `\xi_{\eq,j}\to d\xi/dV\to\sum_{j\in\{T1,T2,T3\}}Q_j\,peak_shape_j` 사슬로 풀고, 중심 `U_j^{\,d}`, 높이 `Q_j/(4w_j)`, 면적 `Q_j`를 박스화했다.
2. `decomp`는 `Z=Z_config\cdot Z_elec` 가산성에서 출발해 config 중심값, vib baseline, electronic MIT 게이트 골의 슬롯 정의로 닫고, 이중계산 금지식을 박스화했다.
3. `.tex`/코드 수정 없이 이 Markdown 하나만 작성했으며, 전자엔트로피 본유도와 수치/부호/물리 결과식은 불변으로 두었다.
