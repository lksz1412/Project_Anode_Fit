# V1012 Phase 4.3 Draft C3 — Step 3/3 supplement (plug-in·MSMR·H-2)

> 대상: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`, `Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex`  
> 출력 성격: `.tex` 편입 전 supplement. **`.tex`/코드 수정 없음.**  
> Step 1 완료 범위(`center`·`hys`)는 `Claude/results/process/V1012_P43_draft_C3_s1.md`, Step 2 완료 범위(`peak`·`decomp`)는 `Claude/results/process/V1012_P43_draft_C3_s2.md` 기준으로 둔다.

## 0. 확인 범위와 불가침

- 직접 확인한 v1.0.12 원문 범위:
  - Ch1 `sec:lco-electronic`: L945--1183.
  - Ch1 `sec:lco-decomp` 및 `sec:lco-code`: L1715--1792.
  - Ch1 node map L1860--1882, `eq:lco-dUdT` L483--488, `eq:xieq` L785--789, `eq:eqpeak` L1189--1212, `eq:sum` L1672--1684.
  - Ch1 `tab:lco-staging` tier-C placeholder 설명: L317--335.
  - Ch2 `ssec:logistic`: L140--166.
  - Ch2 `ssec:weff` 파생 C: L540--568.
  - Ch2 `sec:revheat` 종합식 폭 설명: L676--686.
  - `Claude/results/process/FABLE_REAUDIT_C4_note.md`: L1--68 전체.
- 불가침:
  - `.tex`/코드 수정 없음.
  - 물리·결과식·부호·수치 불변. `g_{\max}=13`, `x_\mathrm{MIT}\approx0.85`, `\Delta x_\mathrm{MIT}\approx0.05`, T1/T2/T3 전위 anchor, `0.47/1.49` J/(mol K), `-46` J/(mol K), `T^2` 누적계수의 `1/2`를 새 값으로 바꾸지 않음.
  - 신규 개념 도입 없음. 기존 `\xi_\eq`, `x=x(\xi_{\eq,1})`, `\Delta S_e^{mol}`, `\Delta S_{\rxn}^\mathrm{cat}`, `U_j(T)`, `eq:sum`, MSMR 대응만 선형 사슬로 재배열한다.

---

## 1. `sec:lco-decomp` 말미 — 전자항 plug-in forward 사슬

### 1.1 위치

- 기준 위치: Ch1 L1750--1754의 `\Delta S_{\rxn,j}^\mathrm{cat}` 합이 `\partial U_j/\partial T`와 dQ/dV로 들어간다는 결론.
- 연결 위치: Ch1 L1756--1765의 `★Ch2/P4 코드 구현 예고`.
- 보존 라벨: `eq:lco-decomp`, `eq:dSemolar`, `eq:dSegate`, `eq:ggate`, `eq:U1T2`, `eq:lco-dUdT`, `eq:xieq`, `eq:sum`.
- 성격: 기존 결론을 `x=x(\xi_{\eq,1}(V))\to\Delta S_{e,1}(V,T)\to\Delta S_{\rxn,1}(V,T)\to U_1(T)\to dQ/dV` 순서로 펼치는 문안. `sec:lco-electronic` 본문 자체는 수정 대상 아님.

### 1.2 LaTeX

```latex
\textbf{★전자항 plug-in forward 사슬(tier-C 구현 가드).}
T1 MIT 전자항은 별도 peak 를 추가하지 않고, T1 의 반응 엔트로피 슬롯을
전압 격자 위에서 평가해 기존 forward 사슬에 넣는 한 줄 보강이다. 먼저
식~\eqref{eq:xieq} 의 T1 평형 진행률을 조성 좌표로 되돌린다:
\[
\xi_{\eq,1}(V,T)
=\frac{1}{1+\exp[-\sigma_d(V-U_1^{\,d})/w_1]},
\qquad
x_1(V,T)=x_{1,\mathrm{hi}}
-(x_{1,\mathrm{hi}}-x_{1,\mathrm{lo}})\,\xi_{\eq,1}(V,T).
\]
여기서 $x_{1,\mathrm{hi}}\approx0.94$, $x_{1,\mathrm{lo}}\approx0.75$ 는 T1 MIT
발현 구간의 조성 anchor 이며, 이 affine 대응은 코드 시연값이 아니라
round-trip 으로 정합할 \emph{tier-C 구현 매핑}이다.

그 조성을 식~\eqref{eq:ggate}$\cdot$\eqref{eq:dSemolar} 에 대입하면
전압 격자 위의 몰당 전자 엔트로피가 된다:
\[
\sigma_{\mathrm{MIT}}(V,T)
\equiv
\sigma\!\left(\frac{x_1(V,T)-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}}\right),
\]
\[
\Delta S_{e,1}^{\,\mathrm{mol}}(V,T)
=-\frac{\pi^2}{3}\,R\,\frac{k_BT}{e_V}\,
\frac{g_{\max}}{\Delta x_\mathrm{MIT}}\,
\sigma_{\mathrm{MIT}}(V,T)
\bigl[1-\sigma_{\mathrm{MIT}}(V,T)\bigr]
\quad(<0,\ \text{삽입 기준}).
\]
이 항은 식~\eqref{eq:lco-decomp} 의 T1 슬롯에만 더한다:
\[
\Delta S_{\rxn,1}^{\mathrm{cat}}(V,T)
=\Delta S_1^{\mathrm{config}}
+\Delta S_1^{\mathrm{vib}}
+\Delta S_{e,1}^{\,\mathrm{mol}}(V,T),
\qquad
\Delta S_{e,j}^{\,\mathrm{mol}}=0\quad(j=\mathrm{T2,T3}).
\]
그 다음 경로는 흑연과 동일하다:
\[
\frac{\partial U_1}{\partial T}
=\frac{\Delta S_{\rxn,1}^{\mathrm{cat}}}{F}
\quad\Longrightarrow\quad
U_1(T)
\quad\Longrightarrow\quad
\xi_{\eq,1}(V,T)
\quad\Longrightarrow\quad
\left(\frac{\dd Q}{\dd V}\right)_1
=Q_1\frac{\xi_{\eq,1}(1-\xi_{\eq,1})}{w_1}.
\]
따라서 전체 forward 출력은 식~\eqref{eq:sum} 그대로
\[
\boxed{\;
\frac{\dd Q}{\dd V}
=C_\bg+\sum_{j\in\{\mathrm{T1,T2,T3}\}}
Q_j\,\mathrm{peak\_shape}_j,\qquad
\mathrm{peak\_shape}_j=\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}\; .}
\]

\textbf{$T^2$ 누적계수 가드.}
전자항의 명시적 Sommerfeld 인자는 $\Delta S_{e,1}^{\,\mathrm{mol}}\propto T$ 이므로,
$\Delta S_{\rxn,1}^{\mathrm{cat}}=\Delta S_0+a_eT$ 로 읽히는 국소 평가에서는
\[
U_1(T)=U_1(T_0)+\frac{\Delta S_0}{F}(T-T_0)
+\frac{a_e}{2F}(T^2-T_0^2)
\]
가 식~\eqref{eq:U1T2} 의 올바른 누적형이다. 즉 forward plug-in 은
$T\Delta S_e/F$ 를 한 번에 곱해 넣지 않으며, 전자항으로 새 peak\_shape 를 만들지도 않는다.
``전자항 $\to U_1(T)$ 이동 $\to$ 기존 logistic peak'' 순서만 허용된다.
```

### 1.3 원문 대비

- 원문 L1750--1751은 세 몫의 합이 `\partial U_j/\partial T`를 거쳐 dQ/dV에 들어간다고만 닫는다. 위 문안은 같은 결론을 `x_1(V,T)` 좌표 매핑부터 `eq:sum`까지 forward 순서로 펼친다.
- 원문 L1757--1760의 "조성 함수인 전자항을 전압 격자에서 평가하려면 `x\leftrightarrow\xi_{\eq,1}(V)` 매핑이 필요"하다는 문장을 실제 수식 사슬로 바꾼다.
- 원문 L1761--1765의 round-trip 가드는 유지한다. 특히 `x_1(V,T)` 매핑과 전자항의 다온도 `T^2` 곡률은 `tab:lco-staging` L331--335의 tier-C placeholder/round-trip 피팅 과제와 같은 지위로 둔다.
- `eq:lco-decomp`의 config+vib+electronic 구조, 삽입 기준 `\Delta S_e<0`, 몰당 환산, `N_A` 누락 가드는 그대로 둔다.

### 1.4 논리 감사

- 선형: `\Delta S_{\rxn,1}^{cat}` 슬롯에 전자항을 더한 뒤 `\partial U_1/\partial T=\Delta S/F`로 보내고, dQ/dV는 기존 `C_\bg+\sum_jQ_j peak_shape_j` 선형 합을 유지한다.
- 물리: 전자 자유도는 MIT 게이트로만 켜지고, 리튬 자리 config 봉우리 내부 항은 logistic이 이미 담으므로 이중계산하지 않는다.
- 결과식: peak 모양은 여전히 `\xi(1-\xi)/w`; 전자항은 새 peak가 아니라 T1 중심의 온도 이동 경로다.
- 부호: 삽입 기준 `\partial g/\partial x<0`라 `\Delta S_{e,1}^{mol}<0`; `\partial U/\partial T=\Delta S/F` 부호는 Ch1 규약과 동일하다.
- 수치 불변: `g_{\max}`, `x_\mathrm{MIT}`, `\Delta x_\mathrm{MIT}`, MIT 조성 범위, 전자항 골 깊이 수치를 새로 산출하지 않는다.
- 신규개념 금지: `x=x(\xi_{\eq,1})`는 원문 L1759--1760의 구현 매핑을 식으로 적은 것일 뿐, 별도 상태방정식이나 새 broadening 항이 아니다.

---

## 2. `sec:lco-code` — MSMR 동형 사슬

### 2.1 위치

- 기준 위치: Ch1 L1767 `\subsection{forward 코드의 LCO 일반화 ...}\label{sec:lco-code}` 이후 L1768--1792.
- 교체 후보: L1768--1780의 MSMR 동형 설명과 L1781--1789의 두 변경점 문단.
- 보존 라벨: `eq:msmr`.
- 성격: 기존 "구조가 동형" 결론을 `MSMR식 → 정규화 → 대응대입(f=-\sigma_d) → \xi_{\eq,j} → peak 박스` 순서로 명시.

### 2.2 LaTeX

```latex
\textbf{(a) 출발 — MSMR 종 식.}
MSMR 모델\cite{msmr2024}은 전이 $j$ 의 양극 조성 몫을
\begin{equation}
x_j=\frac{X_j}{1+\exp[\,f(U-U_j^0)/\omega_j\,]}
\label{eq:msmr}
\end{equation}
로 둔다. 여기서 $X_j$ 는 전이 용량 몫, $U_j^0$ 는 중심, $\omega_j$ 는 폭,
$f=\pm1$ 은 진행 방향을 정하는 부호 인자다.

\textbf{(b) 정규화 — 용량 몫을 떼어 logistic 종만 남기기.}
MSMR 종을 $X_j$ 로 나누면
\[
\hat x_j\equiv\frac{x_j}{X_j}
=\frac{1}{1+\exp[\,f(U-U_j^0)/\omega_j\,]}.
\]
이 식의 물리적 크기 몫은 $X_j$ 에 있고, 곡선 모양은 정규화 종 $\hat x_j$ 에 있다.

\textbf{(c) 대응대입 — Ch1 logistic 과 같은 지수 만들기.}
Ch1 forward 종은 식~\eqref{eq:xieq}
\[
\xi_{\eq,j}(V,T)
=\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d})/w_j]}
\]
이다. 두 지수를 같은 자리로 맞추면
\[
U\leftrightarrow V,\qquad
U_j^0\leftrightarrow U_j^{\,d},\qquad
\omega_j\leftrightarrow w_j,\qquad
X_j\leftrightarrow Q_j,\qquad
f=-\sigma_d.
\]
따라서
\[
\hat x_j
\xrightarrow[\omega_j\to w_j,\;U_j^0\to U_j^{\,d},\;f\to-\sigma_d]{U\to V}
\xi_{\eq,j}(V,T).
\]
방향 인자 비교는 지수의 부호 비교 한 번으로 끝난다: MSMR 은
$+f(U-U_j^0)$ 를 쓰고, Ch1 은 $-\sigma_d(V-U_j^{\,d})$ 를 쓰므로
$f=-\sigma_d$ 다.

\textbf{(d) 박스 — MSMR 정규화 종에서 peak 로.}
\[
\boxed{\;
x_j=X_j\hat x_j,\qquad
\hat x_j\equiv\xi_{\eq,j},\qquad
X_j\leftrightarrow Q_j,\qquad
\left(\frac{\dd Q}{\dd V}\right)_j^\eq
=Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}\; .}
\]
그러므로 LCO 일반화는 새 곡선 클래스를 만들지 않는다. 전이 dict 를
\code{GRAPHITE\_STAGING\_LIT} 에서 \code{LCO\_MSMR\_LIT} 로 바꾸고,
T1 의 $\Delta S_{\rxn}$ 슬롯에 몰당 전자항~\eqref{eq:dSemolar} 을 더하면
식~\eqref{eq:sum} 의 같은 합산 루프가 LCO peak 를 그린다.

\textbf{$T^2$ 및 tier-C 가드.}
MSMR 동형은 logistic 종의 함수형 대응만 보장한다. T1 전자항의
$\Delta S_e\propto T$ 를 $U_1(T)$ 로 누적할 때는 식~\eqref{eq:U1T2} 의
$\tfrac12(T^2-T_0^2)$ 가드를 유지하고, \code{LCO\_MSMR\_LIT} 의 시연값과
전자항 dict 재정렬은 \emph{tier-C placeholder} 로 남긴다. 동형성은
초기값의 문헌 신뢰도를 승격하지 않는다.
```

### 2.3 원문 대비

- 원문 L1768--1779는 MSMR과 Ch1 logistic의 대응을 한 문단으로 설명한다. 위 문안은 같은 대응을 `x_j/X_j` 정규화 뒤 지수 부호 비교로 분해한다.
- 원문 L1775--1778의 `f\leftrightarrow-\sigma_d` 결론은 유지하되, 왜 `-`가 붙는지 `+f(U-U_j^0)` 대 `-\sigma_d(V-U_j^d)` 비교로 명시한다.
- 원문 L1782--1788의 두 변경점(전이 파라미터 교체, 전자항 plug-in)은 박스 뒤 결론으로 유지한다.
- 원문 L1790--1792의 "파라미터 +1 항 외 구조 변경 없음"은 더 좁게, "새 곡선 클래스 없음"으로 보존한다.

### 2.4 논리 감사

- 선형: `x_j=X_j\hat x_j`의 용량 몫은 Ch1의 `Q_j\xi_j`와 같은 구조라 `eq:sum` 선형 합에 그대로 들어간다.
- 물리: MSMR은 양극 전이별 logistic species 표기이고, Ch1은 transition logistic 표기다. 대응은 함수형 동형이지 LCO 수치값 검증이 아니다.
- 결과식: 대응 후 peak 결과는 기존 `eq:eqpeak`의 `Q_j\xi(1-\xi)/w_j`와 동일하다.
- 부호: `f=-\sigma_d`는 두 지수의 계수를 비교한 결과다. peak 모양은 절댓값 미분이므로 방향 부호가 면적·높이를 음수로 만들지 않는다.
- 수치 불변: `X_j`, `U_j^0`, `\omega_j`를 새 숫자로 제시하지 않고 기존 `LCO_MSMR_LIT` 초기값/피팅 철학만 유지한다.
- 신규개념 금지: MSMR 정규화는 원문 `eq:msmr`의 `X_j`를 나눈 대수 조작일 뿐, 별도 MSMR fitting theory를 추가하지 않는다.

---

## 3. Ch2 H-2 — `ssec:logistic` keybox 정정문안

### 3.1 위치

- 기준 위치: Ch2 L161--166 `keybox`.
- 충돌 근거:
  - `FABLE_REAUDIT_C4_note.md` L24--38: `w_j=n_jRT/F` 열적 스케일링 지위의 구조적 자기모순.
  - Ch2 L163: `w_j=n_jRT/F`를 "임의 모수가 아니라"라고 단정.
  - Ch2 L547--560 및 L683--685: 두-상 흑연 staging 폭은 평형 예측 `nRT/F`가 아니라 다온도 dQ/dV로 피팅하는 현상학적 자유 폭이라고 서술.
  - note L30--38: 파생 A의 부동소수점 정밀도 일치와 코드 `func_w(T,n)=nRT/F`는 `w_j(T)` 선형 열적 스케일링을 전제로 할 때만 성립.
- 목표: `ssec:logistic`에는 단상(`\Omega\le2RT`) 한정어와 파생 A 검증 전제를 넣어, 파생 C의 두-상 현상학적 자유폭 서술과 모순되지 않게 한다.

### 3.2 LaTeX

```latex
\begin{keybox}
Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라
\emph{격자기체 점유 분포의 여집합}(탈리튬화 진행률 $=1-\theta$)이다.
다만 이 keybox 의 ``분배함수가 정하는 열적 폭'' 주장은
\emph{이상/단상 평형 종}($\Omega\le2RT$, 균질 고용체 또는 상분리 문턱 이하)에
한정한다. 이 경우 자리당 기준 폭은 $w=RT/F$ 이고, 코드가 쓰는 전이별 폭
$w_j=n_jRT/F$ 는 같은 열적 스케일링을 폭 다중도 $n_j$ 로 늘린 구현형이다.
따라서 $n_j$ 또는 기준온도의 $w_j$ 는 피팅될 수 있어도, 파생 A 의
부동소수점 정밀도 검증은 $\partial w_j/\partial T=n_jR/F$,
곧 $w_j(T)=n_jRT/F$ 의 온도 의존을 전제로 한 검증이다.

반대로 $\Omega>2RT$ 의 두-상 staging 전이에서 실측 유한 폭은
\S\ref{ssec:weff} 의 파생 C 처럼 평형이 예측하는 $nRT/F$ 폭이 아니라
broadening 이 정하는 현상학적 피팅 폭이다. 그러므로 이 문단은
두-상 폭의 물리적 기원을 확정하지 않으며, 두-상 폭을 $nRT/F$ 평형 예측으로
역산하지 않는다. ★표기: $\theta=$ Li 점유율(만충서 1),
$\xi=1-\theta=$ 탈리튬화 진행률(희박서 1); 둘은 같은 점유 분포의 두 이름이다.
Chapter 2 는 이 분포를 결론이 아니라 출발점으로 삼아 엔트로피를 쌓는다.
\end{keybox}
```

### 3.3 원문 대비

- 원문 L162--164의 "logistic 폭 `w=RT/F`, 전이별 `w_j=n_jRT/F`는 임의 모수가 아니라 분배함수가 정하는 열적 폭"이라는 단정 앞에 `이상/단상 평형 종(\Omega\le2RT)` 한정어를 붙인다.
- 원문이 `sec:revheat`와 코드 `func_w`를 근거로 삼던 부분은, "파생 A의 수치 검증은 `w_j(T)=n_jRT/F`를 전제로 할 때만 성립"으로 좁힌다.
- 파생 C의 두-상 문장(L547--560, L683--685)은 그대로 살린다. 즉 두-상 실측 폭은 평형 `nRT/F` 예측값이 아니라 broadening이 정하는 현상학적 피팅 폭이다.
- `\theta`와 `\xi` 표기 설명, Chapter 2가 점유 분포에서 엔트로피를 쌓는다는 마지막 문장은 보존한다.

### 3.4 논리 감사

- 선형: H-2 정정은 폭의 지위 문장만 좁히며, `eq:logistic`, `eq:revheat` 종합식, `g_j=\xi(1-\xi)/w_j` 구조는 바꾸지 않는다.
- 물리: 단상(`\Omega\le2RT`)은 평형 점유 분포의 열적 폭을 말할 수 있고, 두-상(`\Omega>2RT`)은 plateau/broadening 때문에 실측 폭의 지위가 달라진다.
- 결과식: 파생 A 검증은 `w_j(T)=n_jRT/F` 전제 아래의 검증으로 명시된다. 전제를 빼면 note L33--38처럼 완전식/단순식 오차 패턴이 자리바꿈하므로, 무조건 PASS로 읽히지 않는다.
- 부호: H-2는 폭 지위 정정이므로 `\sigma_d`, `\xi=1-\theta`, `\mu`--`V` 부호를 건드리지 않는다.
- 수치 불변: `\Omega=2RT` 임계, `RT/F`, `n_jR/F`, note의 오차 규모를 새로 계산하지 않는다.
- 신규개념 금지: "단상 한정"과 "파생 A 검증 전제"는 note가 지적한 내부 모순을 해소하는 범위이며, 새 폭 모델이나 새 코드 경로를 제안하지 않는다.

---

## 4. 3줄 요약

1. Step 3/3은 Ch1 `sec:lco-decomp` 말미의 T1 전자항을 `x=x(\xi_{\eq,1}(V))\to\Delta S_e(V,T)\to\Delta S_{\rxn}(V,T)\to U_1(T)\to dQ/dV` forward 사슬로 풀었고, 전자항 새 peak 금지와 `T^2` 누적계수 가드를 명시했다.
2. `sec:lco-code`의 MSMR 동형은 `eq:msmr` 정규화 뒤 `U\to V`, `X_j\to Q_j`, `\omega_j\to w_j`, `f=-\sigma_d`를 대입해 Ch1 `\xi_{\eq,j}`와 `Q_j\xi(1-\xi)/w` peak 박스로 닫았다.
3. Ch2 H-2는 `ssec:logistic`의 `w_j=n_jRT/F` 단정을 단상(`\Omega\le2RT`)과 파생 A 검증 전제로 제한해, 파생 C의 두-상 현상학적 자유폭 서술과 내부 모순을 일원화했다.
