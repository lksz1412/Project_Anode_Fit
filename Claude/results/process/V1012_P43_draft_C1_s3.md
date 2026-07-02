# V1012 Phase 4.3 draft C1 — step 3/3 final (plug-in/MSMR/H-2)

> 대상 원천: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`, `Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex`
> 대상 절: Ch1 `sec:lco-decomp` 말미 L1756--1765, Ch1 `sec:lco-code` L1767--1792, Ch2 `ssec:logistic` keybox L161--166
> 근거 노트: `Claude/results/process/FABLE_REAUDIT_C4_note.md` 1--68행 정독
> 계승: `V1012_P43_draft_C1_s1.md` step 1(center/hys), `V1012_P43_draft_C1_s2.md` step 2(peak/decomp) 완료 판단
> 산출물 성격: finalizer 편입용 supplement 초안. `.tex`/코드 수정 없음.

## 0. 확인 범위와 경계

- `V1012_P43_draft_C1_s1.md` 1--289행, `V1012_P43_draft_C1_s2.md` 1--274행을 전문 확인했다.
- Ch1은 전체 파일 1--1964행을 구간 출력으로 확인했으나 일부 500행 단위 출력에는 도구 생략이 있었다. 이번 step 3의 직접 근거 구간인 L1021--1110, L1181--1235, L1715--1792는 좁은 범위로 재확인했다.
- Ch2 `graphite_ica_ch2_v1.0.12.tex`는 1--755행 전체를 3구간으로 확인했다. H-2 직접 대상은 L140--166, 모순 상대항은 파생 C L540--569 및 종합식 L673--689다.
- `FABLE_REAUDIT_C4_note.md`는 1--68행 전체를 확인했다. H-2 핵심 근거는 §2 L24--38 및 요약 L68이다.
- 불가침: `.tex`/코드 실제 수정 없음. 새 물리 항, 새 fitting parameter, 새 self-consistent solver, 새 라벨 체계는 만들지 않는다.

## 1. `sec:lco-decomp` 말미 plug-in supplement

### 위치

- 헤더 보존: L1715 `\subsection{LCO $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해 ...}\label{sec:lco-decomp}`
- step 2 보존: L1716--1754의 decomp 본문은 `V1012_P43_draft_C1_s2.md`가 이미 사슬형으로 정리했다.
- 교체/보강 후보: L1756--1765 `Ch2/P4 코드 구현 예고(두 설계 항목)`
- 목표: 좌표 매핑과 round-trip 가드를 단순 예고가 아니라
  `x=x(\xi_{\eq,1}(V)) -> \Delta S_{e,1}(V,T) -> \Delta S_{\rxn,1}(V,T) -> U_1(T) -> dQ/dV`
  forward 사슬로 보이게 한다.

### LaTeX 사슬

```latex
\textbf{★전자항 plug-in 의 forward 위치.}
식~\eqref{eq:lco-decomp} 을 코드 경로로 옮길 때 새 상태변수나 새 peak 식을
만들지 않는다. 전자항은 T1 의 기존 $\Delta S_{\rxn}$ 슬롯에 들어가기 전,
전압 격자 위에서 조성 좌표만 변환해 평가한다:
\[
V \longmapsto \xi_{\eq,1}(V,T)
\longmapsto x_1(V)\equiv x_1\!\big(\xi_{\eq,1}(V,T)\big).
\]
여기서 $x_1(\xi)$ 는 T1 MIT 전이 구간의 정규화 조성 대응이며, 별도
전이 루프나 self-consistent 해법을 추가한다는 뜻이 아니다. 기존 forward 루프의
T1 평형 점유를 조성 게이트의 입력 좌표로 읽는 것이다.

\textbf{(i) 좌표 대입 — $x$ 게이트를 $V$ 격자로 옮김.}
\S\ref{sec:lco-gate} 의 MIT-logistic 게이트를
\[
z_{\mathrm{MIT},1}(V)
=\frac{x_1(\xi_{\eq,1}(V,T))-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}},
\qquad
\sigma_1(V)=\sigma\!\big(z_{\mathrm{MIT},1}(V)\big)
\]
로 전압 격자에 올린다. 그러면 몰당 전자항은
\begin{equation}
\Delta S_{e,1}^{\,\mathrm{mol}}(V,T)
=-\frac{\pi^2}{3}\,R\,\frac{k_BT}{e_V}\,
\frac{g_{\max}}{\Delta x_\mathrm{MIT}}\,
\sigma_1(V)\,[1-\sigma_1(V)]
\quad(<0,\ \text{삽입 기준})
\label{eq:lco-Se-plugin-V}
\end{equation}
이다. 이는 식~\eqref{eq:dSemolar}$\cdot$\eqref{eq:gunit}$\cdot$\eqref{eq:dSegate}
의 같은 식을 $x=x_1(\xi_{\eq,1}(V,T))$ 로 평가한 것뿐이다. $e_V$ 는 분모로
들어가며, $N_A$ 몰당 환산은 이미 $R=N_Ak_B$ 로 들어가 있다.

\textbf{(ii) 엔트로피 슬롯 — 세 성분의 선형 합.}
T1 의 forward 반응 엔트로피 슬롯은
\begin{equation}
\Delta S_{\rxn,1}^{\mathrm{cat}}(V,T)
=\Delta S_1^\mathrm{config}
+\Delta S_1^\mathrm{vib}
+\Delta S_{e,1}^{\,\mathrm{mol}}(V,T).
\label{eq:lco-dSrxn-plugin}
\end{equation}
config 는 중심 표준값만, vib 는 phonon baseline, electronic 은 MIT 게이트
골만 담당한다. 봉우리 내부 $R\ln[(1-\xi)/\xi]$ 항과 전자 게이트를 같은
측정 엔트로피에 중복 배정하지 않는다.

\textbf{(iii) 중심 이동 — 기존 $U_j$ 슬롯으로만 전달.}
식~\eqref{eq:lco-dUdT} 의 자리는 그대로다:
\begin{equation}
\frac{\partial U_1}{\partial T}(V,T)
=\frac{\Delta S_{\rxn,1}^{\mathrm{cat}}(V,T)}{F}.
\label{eq:lco-dUdT-plugin}
\end{equation}
전자항은 $\Delta S_{e,1}^{\,\mathrm{mol}}\propto T$ 이므로, 기준온도
$T_0$ 에서 적분할 때는 식~\eqref{eq:U1T2} 의 $\tfrac12$ 가 반드시 남는다:
\[
U_1(T)=U_1(T_0)
+\frac{\Delta S_0}{F}(T-T_0)
+\frac{a_e}{2F}(T^2-T_0^2).
\]
따라서 다온도 신호는 ``peak 위치가 $T$-선형''이 아니라
``$\partial U_1/\partial T$ 가 $T$-선형, 위치 이동은 $T^2$'' 이다.

\textbf{(iv) dQ/dV 전달 — peak 식은 불변.}
전자항으로 갱신된 T1 중심은 기존 분기 중심과 평형 점유를 거쳐
\[
U_1(T)\longmapsto U_1^{\,d}(T)
\longmapsto \xi_{\eq,1}(V,T)
\longmapsto
Q_1\,\frac{\xi_{\eq,1}(1-\xi_{\eq,1})}{w_1}
\]
로 들어간다. 곧 전자항은 $dQ/dV$ 에 새 모양 함수를 더하는 것이 아니라,
$\Delta S_{\rxn,1}^{\mathrm{cat}}\to U_1(T)\to\xi_{\eq,1}\to peak$ 의
기존 forward 사슬을 통해 T1 위치 이동과 다온도 곡률을 만든다.

\textbf{round-trip 가드.}
표~\ref{tab:lco-staging} 의 config 값과 식~\eqref{eq:ggate} 의
$(g_{\max},x_\mathrm{MIT},\Delta x_\mathrm{MIT})$ 는 초기값이다. T1
$U_1(298)\approx3.90$ V, 삽입 기준 $\Delta S_{e,1}<0$, 그리고
식~\eqref{eq:U1T2} 의 $T^2$ 이동률을 다온도 LCO 하프셀 데이터에서
round-trip 으로 맞추기 전에는 신뢰값으로 승격하지 않는다.
``현재 코드 시연값''과 표의 물리 anchor 는 계속 tier-C placeholder 로 둔다.
```

### 원문 대비

- 원문 L1756--1765의 두 항목을 `좌표 대입 -> 엔트로피 슬롯 -> 중심 이동 -> dQ/dV` 사슬로 확장했다.
- `x=x(\xi_{\eq,1}(V))` 는 기존 T1 전이의 진행률-조성 대응만 가리킨다. 새 상태변수나 새 solver 를 제안하지 않는다.
- `\Delta S_e` 는 자리당 식이 아니라 몰당 식 `eq:dSemolar`/`eq:gunit`을 사용한다. `e_V` 나눗셈과 `N_A` 환산 가드를 유지한다.
- `T^2` 가드는 `eq:U1T2`의 적분형 `1/2` 인자를 보존하기 위한 문장으로 남긴다.
- tier-C 라벨은 유지한다: 현재 시연값과 물리 anchor 의 차이는 round-trip 피팅 전까지 승격하지 않는다.

### 논리 감사

- 선형성: config/vib/electronic 은 `eq:lco-decomp`의 세 슬롯 선형 합만 사용했다.
- 부호: MIT 전자항은 삽입 기준 음의 골이다. `\Delta S_{e,1}^{mol}<0` 이 `\partial U_1/\partial T` 슬롯에 그대로 들어간다.
- 물리 불변: peak 식, 분기 중심, 폭, 합산식은 새로 만들지 않는다.
- 신규개념 금지: self-consistent solver, residual entropy, additional gate, new broadening channel 없음.

## 2. `sec:lco-code` MSMR 동형 supplement

### 위치

- 헤더 보존: L1767 `\subsection{forward 코드의 LCO 일반화 ...}\label{sec:lco-code}`
- 교체 후보: L1768--1792 전체 문단
- 목표: `MSMR식 -> 정규화 -> 대응대입(f=-\sigma_d) -> \xi_{\eq,j} -> peak 박스` 사슬로 정리한다.

### LaTeX 사슬

```latex
\textbf{(a) 출발 — MSMR 의 전이별 logistic.}
MSMR 모델은 전극 조성을 여러 반응 species 의 logistic 합으로 적는다
\cite{msmr2024}:
\begin{equation}
x_j(U)=\frac{X_j}{1+\exp[\,f_j(U-U_j^0)/\omega_j\,]}.
\label{eq:msmr}
\end{equation}
여기서 $X_j$ 는 전이 용량 몫, $U_j^0$ 는 중심, $\omega_j$ 는 폭,
$f_j=\pm1$ 은 species 방향 인자다.

\textbf{(b) 정규화 — 모양 함수만 떼어냄.}
용량 가중을 분리해
\[
\bar x_j(U)\equiv\frac{x_j(U)}{X_j}
=\frac{1}{1+\exp[\,f_j(U-U_j^0)/\omega_j\,]}
\]
로 쓰면, 남는 것은 Chapter 1 의 전이별 평형 점유와 같은 logistic 모양이다.

\textbf{(c) 대응 대입 — 부호 슬롯.}
Chapter 1 의 평형 점유는
\[
\xi_{\eq,j}(V,T)
=\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d})/w_j]}.
\]
두 지수를 같은 자리끼리 비교하면
\[
U\leftrightarrow V,\qquad
U_j^0\leftrightarrow U_j^{\,d},\qquad
\omega_j\leftrightarrow w_j,\qquad
X_j\leftrightarrow Q_j,\qquad
\boxed{\,f_j=-\sigma_d\,}.
\]
MSMR 식은 $+f_j(U-U_j^0)$ 를 쓰고, Ch1 식은
$-\sigma_d(V-U_j^{\,d})$ 를 쓰므로 방향 인자는 반드시
$f_j=-\sigma_d$ 로 대응한다. 이 대입 뒤
\begin{equation}
\bar x_j(U)\longleftrightarrow\xi_{\eq,j}(V,T).
\label{eq:lco-msmr-xi}
\end{equation}

\textbf{(d) peak 박스 — 같은 종, 같은 면적.}
정규화 logistic 을 전압으로 미분하면
\[
\left|\frac{\partial\bar x_j}{\partial U}\right|
=\frac{\bar x_j(1-\bar x_j)}{\omega_j}
\quad\longleftrightarrow\quad
\left|\frac{\partial\xi_{\eq,j}}{\partial V}\right|
=\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}.
\]
따라서 MSMR species 하나는 Ch1 전이 하나의 peak 와 같은 상자를 갖는다:
\begin{equation}
\boxed{\;
\left(\frac{\dd Q}{\dd V}\right)_j
=Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j},\qquad
\mathrm{center}_j=U_j^{\,d},\quad
\mathrm{height}_j=\frac{Q_j}{4w_j},\quad
\mathrm{area}_j=Q_j\; .}
\label{eq:lco-msmr-peak-box}
\end{equation}
LCO 는 이 상자를 $j\in\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}$ 에 대해
선형 합산한다. T1 만 식~\eqref{eq:lco-decomp} 의 전자항 plug-in 을 받아
$U_1(T)$ 의 다온도 이동을 만든다. 이때 전자항의 관측 가드는 그대로다:
$\Delta S_{e,1}\propto T$ 이므로 $\partial U_1/\partial T$ 는 $T$-선형,
위치 이동은 식~\eqref{eq:U1T2} 의 $T^2$ 이다. 현재 코드 시연값은
표~\ref{tab:lco-staging} caption 의 tier-C placeholder 로 남기며,
round-trip 피팅 전 물리 anchor 로 승격하지 않는다.
```

### 원문 대비

- 원문 L1768--1779의 MSMR 동형 설명을 네 단계로 분해했다.
- `f=-\sigma_d` 는 지수 부호 비교에서 직접 얻은 대응 대입으로 박스화했다.
- 원문 L1781--1788의 두 변경점은 `전이 파라미터 교체`와 `전자항 plug-in`으로 유지하되, peak 박스 뒤 prose로 흡수했다.
- `T^2` 가드와 tier-C placeholder 라벨을 같은 문단에 남겨, current code demo 값이 물리 anchor 로 오독되지 않게 했다.

### 논리 감사

- 선형성: species/transition 별 peak 를 만든 뒤 `\sum_j Q_j[...]` 로 더하는 구조만 사용했다.
- 부호: MSMR 지수 `+f(U-U_j^0)` 와 Ch1 지수 `-\sigma_d(V-U_j^d)`의 비교에서 `f=-\sigma_d`; 임의 부호 변경 없음.
- 물리 불변: MSMR은 새 모델이 아니라 Ch1 logistic transition 식의 동형성 설명으로만 쓴다.
- 신규개념 금지: MSMR parameterization을 새 피팅 알고리즘으로 확장하지 않는다.

## 3. Ch2 H-2 정정문안 — `ssec:logistic` keybox

### 근거

- 현 Ch2 L161--166 keybox 는 `w=RT/F` 및 `w_j=n_jRT/F` 를 "임의 모수가 아니라 단일 자리 2-상태 분배함수가 정하는 분포의 열적 폭"으로 단정한다.
- 같은 파일 파생 C L540--569 및 종합식 L673--689는 두-상 흑연 staging 의 실측 폭을 평형 예측 `nRT/F` 가 아니라 broadening 이 정하는 현상학적 자유 피팅 폭으로 둔다.
- `FABLE_REAUDIT_C4_note.md` §2는 이 둘의 충돌을 H-2로 확정했다. 특히 파생 A의 부동소수점 검증은 실제 코드의 `w_j(T)=n_jRT/F` 열적 스케일링을 전제할 때 성립하고, `w_j`를 `T_ref`에서 동결하면 단순식/완전식의 오차 역할이 뒤바뀐다.
- v1.0.12 Ch2는 파생 C와 종합식이 이미 "두-상 폭은 현상학적 자유 피팅 폭"이라고 고쳐져 있으므로, H-2의 남은 정정 지점은 keybox의 무조건 단정이다.

### 교체 후보 LaTeX

```latex
\begin{keybox}
Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라
\emph{격자기체 점유 분포의 여집합}(탈리튬화 진행률 $=1-\theta$)이다.
다만 logistic 폭의 물리 지위는 전이 종류와 구현 전제에 따라 구분한다.
\emph{단상} 또는 균질 고용체 한계($\Omega\le2RT$)에서는 이상 단일 자리
분배함수가 $w=RT/F$ 의 열적 폭을 주며, 전이별 유효 폭
$w_j=n_jRT/F$ 도 그 열적 스케일을 따르는 평형 예측으로 읽을 수 있다.
반대로 두-상 전이($\Omega>2RT$)의 \emph{실측} $dQ/dV$ 종 폭은
평형 델타가 broadening 으로 펼쳐진 현상학적 자유 피팅 폭이며, 그 지위는
\S\ref{ssec:weff}$\cdot$\S\ref{sec:revheat} 의 파생 C 설명을 따른다.

또한 파생 A 의 finite-difference 검증은 Chapter 1 코드가 실제로
$w_j(T)=n_jRT/F$ 를 사용한다는 전제에서 수행된 검증이다. 만약 두-상
피팅 폭을 기준온도에서 동결하거나 다른 $T$ 의존으로 둔다면,
\eqref{eq:dxidT} 의 $w(T)$ 조각은 그 선택한 $\partial w_j/\partial T$ 에
맞게 다시 평가해야 하며, 자동으로 $R/F$ 항을 갖는다고 단정하지 않는다.
★표기: $\theta=$ Li 점유율(만충서 1), $\xi=1-\theta=$ 탈리튬화
진행률(희박서 1); 둘은 같은 점유 분포의 두 이름이다. Chapter 2 는
이 분포를 결론이 아니라 출발점으로 삼아 엔트로피를 쌓는다.
\end{keybox}
```

### 원문 대비

- L162--164의 "임의 모수가 아니라" 단정을 단상/균질 고용체(`\Omega\le2RT`) 한정으로 좁혔다.
- 파생 C와 충돌하지 않도록 두-상(`\Omega>2RT`) 실측 폭은 현상학적 자유 피팅 폭이라고 같은 keybox 안에서 분리했다.
- 파생 A 수치 검증은 `w_j(T)=n_jRT/F` 구현 전제 위의 검증임을 명시했다.
- 다른 `T` 의존을 택하면 `eq:dxidT`의 `w(T)` 조각도 그에 맞춰 바뀐다는 조건을 넣어, 완전식의 적용 전제를 숨기지 않았다.

### 논리 감사

- 단상과 두-상 폭 지위를 한 문단 안에서 분리해 FABLE H-2 모순을 해소한다.
- 파생 C 본문을 삭제하거나 약화하지 않는다. keybox의 무조건 단정만 좁힌다.
- 파생 A PASS를 일반 물리 명제로 승격하지 않고, 실제 코드 `func_w` 전제의 검증으로 둔다.
- 신규개념 없음: 이미 문서 안에 있는 `\Omega=2RT`, 파생 A, 파생 C, `w_j(T)=n_jRT/F`, 현상학적 자유 피팅 폭만 재배치했다.

## 4. 라벨 및 삽입 주의

- 기존 재사용 라벨: `eq:lco-decomp`, `eq:lco-dUdT`, `eq:msmr`, `eq:xieq`, `eq:eqpeak`, `eq:U1T2`.
- 신설 후보 라벨: `eq:lco-Se-plugin-V`, `eq:lco-dSrxn-plugin`, `eq:lco-dUdT-plugin`, `eq:lco-msmr-xi`, `eq:lco-msmr-peak-box`.
- 실제 편입 전 finalizer는 `rg "\\label\\{eq:lco-" Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex` 로 충돌을 다시 확인해야 한다.
- `\sigma_d` 와 logistic 함수 `\sigma(\cdot)` 가 같은 글자를 쓰므로, 편입 시 `\sigma_1(V)=\sigma(z_{\mathrm{MIT},1})` 문장이 방향 부호와 혼동되지 않는지 확인한다.
- Ch2 H-2는 keybox만 교체 후보로 둔다. 파생 C, 파생 A, 종합식은 이미 H-2 근거를 담고 있으므로 재작성하지 않는다.

## 5. 3줄 요약

1. `sec:lco-decomp` 말미는 `x=x(\xi_{\eq,1}(V)) -> \Delta S_{e,1}^{mol}(V,T) -> \Delta S_{\rxn,1}^{cat}(V,T) -> U_1(T) -> peak` forward 사슬로 정리했다.
2. `sec:lco-code`는 MSMR logistic 을 정규화하고 `f=-\sigma_d` 를 대응 대입해 `\xi_{\eq,j}` 및 `Q_j\xi(1-\xi)/w_j` peak 박스로 닫았다.
3. Ch2 H-2는 `w_j=n_jRT/F` 단정을 `\Omega\le2RT` 단상 한정으로 좁히고, 파생 A 검증이 실제 코드의 열적 스케일링 전제 위에서만 PASS임을 명시하는 정정문안으로 일원화했다.
