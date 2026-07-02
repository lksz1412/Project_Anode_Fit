# V1.0.12 Phase 4.3 — 작성 드래프트 S2

> 역할: N=10 경쟁 독립 드래프트 중 S2(무통신). **드래프트만(.md supplement) — tex/코드 미수정.** 편입은 Fable master.
> 대상: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`(1965줄, head→tail 전문 정독) ·
> `Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex`(756줄, head→tail 전문 정독).
> 참조: `results/process/V1011_P11_map_v10.md`(P1.1 체리픽 — v1.0.11 대상. **v1.0.12 는 이후 별도로 개정되어 있어
> 줄 번호·본문이 v1.0.11 과 다르다** — 실측 재확인 후 계승, 맹신 금지) · `results/process/V1010_LCO_STYLE_REPORT.md`
> §1(필요한 수식 사슬 표) · `results/process/FABLE_REAUDIT_C4_note.md`(H-2 근거, §2 CRITICAL).
> **작업 방식**: 절 하나씩 선형(정독→수식 사슬 작성→자기검수→앞 절 정합→다음 절). 통째 배치 없음.

## 0. 실측 확인 — 전제 재검증 (맹신 금지)

v1.0.12 는 v1.0.11 대비 이미 한 차례 개정되어 있다(파일 헤더 주석 "H-1 Ch2 연동·H-2 w_j 지위·M-1~M-11·LCO 6절
수식화(P1.1 계승)" 명시). 실측 결과:

- **Ch2 H-1(BW 부호)·M-8(파생D 근사)·M-9(고온코너 한정)**: 이미 반영 완료 확인(`eq:Veq_BW`(ch2 L191)이 FABLE
  감사의 "정정형"과 일치, 파생 D 에 `ΔU_j^hys≪w_j` 선형화 조건 명시(ch2 L587-590), 극한표 고온 코너에 "정성적
  방향만 유효" 한정어 존재(ch2 L620)). **재작업 불필요 — 손대지 않음.**
- **Ch2 H-2(w_j 지위 모순)**: 파생 C(`ssec:weff`, ch2 L540-569)는 이미 단상/두-상 이중지위로 정리되어 있으나,
  §logistic 키박스(ch2 L161-166)는 여전히 무한정 단정 — **모순 잔존, 갈래 2 대상 확정**.
  - `eq:Z1`(ch2 L123-127)은 **비상호작용 단일 자리** 분배함수(항 $\Omega$ 없음)다 — 상호작용 상수 $\Omega$ 를
    아예 담지 않는 이 식이 $\Omega>2RT$ 두-상 영역의 폭까지 예측한다고 읽는 것은 식 자체의 구성 범위를 벗어난
    주장이다. 이는 파생 C 의 broadening 논거(top-down)와 별개로, `eq:Z1` 의 구조(bottom-up)에서도 같은 결론이
    나온다는 \emph{독립 교차검증}이다(§8 논리 감사에서 상술).
- **Ch1 LCO 6절**: `sec:lco-center`(실측 L476)·`sec:lco-hys`(L696)·`sec:lco-peak`(L1220)·`sec:lco-decomp`
  (L1715)·전자항 plug-in(L1756-1765, decomp 절 말미)·MSMR(`sec:lco-code`, L1767) — **전수 실측, (a)(b)(c)(d)
  수식 사슬 미완**(줄글 결론 잔존, V1010 STYLE_REPORT 판정과 부합). V1011 map draft 의 §1(center)·§2(hys)
  본문은 v1.0.11 대상 문안이라 v1.0.12 의 실제 줄 구조·본문과 다름 — **재유도로 재작성**(구조는 계승, 문안은
  신규).
- **라벨 충돌 전수 확인**: 전 파일 `eq:lco-*` grep = `eq:lco-dUdT`(L487, 정의) + `eq:lco-decomp`(L1723, 정의)
  **딱 2개**. `eq:lco-dUdT` 는 L493·498·1229·1750·1790·1877 **6곳**, `eq:lco-decomp` 는 L505·508·1040·1060·
  1729·1738·1761·1785·1879 **9곳**에서 `\eqref` 참조된다 — 아래 신설 12개 라벨은 이 2개와 충돌 0(§7 표).

---

## 1. `sec:lco-center` (실측 L476 헤더, 교체 L477–495, 보존 L496–516 verifybox)

**편입 지시**: L476 헤더·L496–516 verifybox 그대로 두고 L477–495 를 아래로 교체. `eq:lco-dUdT` 라벨은 (d) 박스에
그대로 승계(6곳 다운스트림 참조 유지 — 원문 그대로 \emph{미분 관계식 한 줄}에만 건다, 닫힌형 $U_j^\mathrm{cat}(T)$
자체는 원문처럼 별도 라벨 없이 인라인 유지해 라벨 의미 확장을 피한다).

```latex
\textbf{(a) 출발 — 흑연 유도의 전극-무관성 재확인.} \S\ref{sec:center} 의 두 결과식 — 전기화학 평형 조건
$\Delta G_j=-sFU_j$(식~\eqref{eq:eqcond})와 열역학 정의 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ —
어디에도 ``흑연''을 지목하는 항이 없다: 전자는 삽입 반쪽반응의 전기화학 평형(식~\eqref{eq:eqbalance})에서,
후자는 Gibbs 자유에너지의 정의~\eqref{eq:gibbsdef}에서 나오며 둘 다 host 종에 무관한 항등식이다. LCO 로 넘어갈
때 이 두 식에 실제로 바뀌는 것은 전이 집합과 입력값의 치환뿐이다:
\begin{equation}
j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1,T2,T3}\},\qquad
(\Delta H_{\rxn,j},\Delta S_{\rxn,j})\ \longmapsto\ (\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat}),
\label{eq:lco-jset}
\end{equation}
곧 host 의 화학 정체는 이 두 식 어디에도 새 항으로 들어가지 않고, 상수 $\Delta H_{\rxn,j}^\mathrm{cat}$ 의
\emph{값}으로만 흡수된다.

\textbf{(b) 연산 — 같은 자리에 같은 대입.} 식~\eqref{eq:lco-jset} 의 치환을 식~\eqref{eq:eqcond} 의
$\Delta G_j=-FU_j$($s=+1$)에 그대로 넣으면(식~\eqref{eq:Ujmid} 과 글자 그대로 같은 대입)
\[
\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}=-F\,U_j^\mathrm{cat}(T),
\]
가 된다 — 대입 과정 어디에도 host 항이 끼지 않는다는 (a)의 확인이 이 한 줄에서 재확인된다.

\textbf{(c) 중간식 — 닫힌형과 온도 미분(이중 경로 교차검증).} $U_j^\mathrm{cat}$ 로 이항하면 흑연
식~\eqref{eq:Uj} 와 함수형이 같다:
\[
U_j^\mathrm{cat}(T)=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]
온도 계수는 두 독립 경로가 같은 값에 닿는다(재유도 자기검증). \emph{경로 1(직접 미분)}: $\Delta H^\mathrm{cat}$
는 $T$ 무관, $T\Delta S^\mathrm{cat}$ 의 미분이 $\Delta S^\mathrm{cat}$ 이라 곧장
$\partial U_j^\mathrm{cat}/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$. \emph{경로 2(Gibbs 항등식 경유)}:
$\partial\Delta G_j/\partial T|_P=-\Delta S_{\rxn,j}^\mathrm{cat}$(식~\eqref{eq:gibbsdef} 의 $G\equiv H-TS$ 에서)와
식~\eqref{eq:eqcond} 의 $\Delta G_j=-FU_j^\mathrm{cat}$ 를 $T$ 로 미분한
$\partial\Delta G_j/\partial T=-F\,\partial U_j^\mathrm{cat}/\partial T$ 를 등치하면
\[
-F\,\frac{\partial U_j^\mathrm{cat}}{\partial T}=-\Delta S_{\rxn,j}^\mathrm{cat}
\ \Longrightarrow\
\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]
두 경로 어디에도 host 구분 항이 없다 — 이것이 ``전극 불문''의 수식적 의미다.

\textbf{(d) 박스 — LCO 온도 계수.}
\begin{equation}
\boxed{\;\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}
\qquad(j\in\mathcal J_\mathrm{LCO})\;}
\label{eq:lco-dUdT}
\end{equation}
관계식은 흑연 식~\eqref{eq:Uj} 미분과 부호까지 1:1 이고 바뀌는 것은 값뿐이다 — 양극의 높은 중심
($\sim$3.9--4.2 V)은 분자 $-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양인 데서 오고, $\Delta S_{\rxn,j}^\mathrm{cat}$
는 \S\ref{sec:lco-decomp}(식~\eqref{eq:lco-decomp})에서 config$\cdot$vib$\cdot$전자 세 성분으로 분해된다. LCO
단일전극(coin half-cell, vs Li) 엔트로피 계수의 \emph{대표 스케일}은 $\dd\phi/\dd T\approx+0.83$ mV/K
급이고(곧 $\Delta S_\rxn\approx+0.83\,\mathrm{mV/K}\times F\approx+80$ J/(mol\,K) 규모[tier B], 단 부호$\cdot$
크기는 $x$ 의존이라 전이별 정밀값 아님). 이는 흑연의 $\Delta S_\rxn$(전이별 $+29/0/-5/-16$ J/(mol\,K),
표~\ref{tab:staging})과 \emph{값은 다르나}, 식~\eqref{eq:lco-dUdT} 의 관계는 두 전극에서 동일한 형태로 성립한다.
```

**원 줄글 대비**: 원문(L477-495)은 "유도에 전극 가정이 없다"는 결론을 먼저 서술한 뒤, `eq:lco-dUdT` 미분 식
하나만 박스 없이 제시하고 대표 스케일 산출로 넘어갔다 — (a)출발이 결론으로 시작해 근거(어느 두 식에 host 항이
없는지)가 뒤에 흩어져 있었다. 신규 (a)(b)(c) 는 그 근거를 흑연 식 번호(`eq:eqcond`, `eq:eqbalance`,
`eq:gibbsdef`, `eq:Ujmid`)로 명시하고, 원문에 없던 **이중경로 교차검증**((c) 경로1 직접미분 vs 경로2 Gibbs
항등식 경유)을 추가해 결론을 재유도로 뒷받침한다. (d) 이후 대표 스케일 문단은 원문과 **완전 동일**(수치·부호·
문장 불변, 재배치만). 검산박스(L496-516)는 **무수정**.

**논리 감사(재유도 근거)**:
- *부호*: $\Delta H_\rxn<0$(발열)이면 $-\Delta H_\rxn>0$ 이 중심을 올린다는 흑연 규약과 1:1 — cat 첨자만 다름, 부호 흐름 불변.
- *차원*: $\Delta S_{\rxn,j}^\mathrm{cat}/F$ = [J/(mol·K)]/[C/mol] = J/(K·C) = V/K, $\partial U/\partial T$ 의
  기대 차원과 일치.
- *극한*: $\Delta H^\mathrm{cat}$ 가 $T$ 에 무관하다는 가정 하 두 경로 모두 같은 결과 — 만약 $\Delta H$ 가 $T$
  의존이면 두 경로가 갈릴 것이므로, 이 일치 자체가 "$\Delta H$ 는 $T$ 무관"이라는 표준 가정의 자기검증 역할을 한다.
- *이중계산*: 대표 스케일(+80)과 verifybox 의 전자항(−46, MIT 창 중심 국소값)을 직접 빼는 산법은 **정밀 계산이
  아니라 명시적 sanity 확인**임을 원문(L481-482 "부호·크기 sanity 만 확인한다")이 이미 못박고 있어 이중계산 위험
  없음 — 확인 결과 결함 없음(신규 결함 미발견, 기존 hedging 충분).

---

## 2. `sec:lco-hys` (실측 L696 헤더, 교체 L697–719)

**편입 지시**: L696 헤더 그대로, L697–719 를 아래로 교체. 다음 절 `sec:width`(L722)는 무관.

```latex
\textbf{(a) 출발 — 같은 격자기체 자유에너지, LCO 전이 집합.} \S\ref{sec:hys} 의 격자기체$\cdot$정규용액 유도
(식~\eqref{eq:mu}$\cdot$\eqref{eq:gxi})는 ``동등한 자리에 리튬이 차고 빈다''는 가정 하나만 쓴다 — 이는
$\mathrm{Li}_x\mathrm{CoO_2}$ 의 팔면체 리튬 자리에도 문자 그대로 성립한다. LCO 전이 집합
$\mathcal J_\mathrm{LCO}=\{\mathrm{T1(MIT), T2(OD}_a\mathrm{), T3(OD}_b\mathrm{)}\}$ 의 각 전이 $j$ 에 진행률
$\xi_j$ 를 달아 같은 정규용액 자유에너지를 쓰면
\begin{equation}
g_j^\mathrm{cat}(\xi_j)=g_{0,j}^\mathrm{cat}
+RT\big[\xi_j\ln\xi_j+(1-\xi_j)\ln(1-\xi_j)\big]+\Omega_j^\mathrm{cat}\,\xi_j(1-\xi_j),
\label{eq:lco-gxi}
\end{equation}
이다(식~\eqref{eq:gxi} 와 cat 첨자 외 동일). 새 물리는 넣지 않는다 — 바뀌는 것은 전이별 입력값
$U_j^\mathrm{cat},\Omega_j^\mathrm{cat},\gamma_j,h_{\eta,j}$ 뿐이다.

\textbf{(b) 연산 — 곡률과 spinodal 문턱.} 식~\eqref{eq:lco-gxi} 를 두 번 $\xi_j$ 로 미분하면(식~\eqref{eq:gpp}
와 동일 대수)
\begin{equation}
\frac{\partial^2 g_j^\mathrm{cat}}{\partial\xi_j^2}=\frac{RT}{\xi_j(1-\xi_j)}-2\Omega_j^\mathrm{cat},
\label{eq:lco-gpp}
\end{equation}
이고 $g_j''^\mathrm{cat}=0$ 의 근이(식~\eqref{eq:spinodal} 과 동일 근의 공식)
\begin{equation}
\xi_{s,j}^{\mathrm{cat},\pm}=\tfrac12\big(1\pm u_j^\mathrm{cat}\big),\qquad
u_j^\mathrm{cat}=\sqrt{1-\frac{2RT}{\Omega_j^\mathrm{cat}}}\qquad(\Omega_j^\mathrm{cat}>2RT).
\label{eq:lco-spinodal}
\end{equation}
$\Omega_j^\mathrm{cat}\le2RT$ 면 $u_j^\mathrm{cat}$ 이 실수가 아니라 그 전이의 spinodal gap 은 없다(흑연 코드
분기와 동일 판정 — \code{if Omega <= 2RT: return 0.0}).

\textbf{(c) 중간식 — 평형 전위 곡선과 극값 차.} 식~\eqref{eq:Veq} 형태에 LCO 값을 넣으면($s=+1$)
\begin{equation}
V_{\eq,j}^\mathrm{cat}(\xi)=U_j^\mathrm{cat}
+\frac{RT}{F}\ln\frac{\xi}{1-\xi}+\frac{\Omega_j^\mathrm{cat}}{F}(1-2\xi),
\label{eq:lco-Veq}
\end{equation}
이고 두 spinodal 끝점(식~\eqref{eq:lco-spinodal})을 대입하면(식~\eqref{eq:hyssub}$\cdot$\eqref{eq:hysdiff} 와
동일 대수 — logit 인자가 두 끝점에서 서로 역수, $(1-2\xi)$ 항은 $\mp u_j^\mathrm{cat}$) 상수 $U_j^\mathrm{cat}$
가 상쇄되고
\[
\Delta U_{j}^{\hys,\mathrm{cat}}=V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^{\mathrm{cat},-})-V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^{\mathrm{cat},+})
=\frac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\operatorname{artanh}u_j^\mathrm{cat}\big].
\]
\emph{대칭점 검산(자기검증)}: 두 끝점의 \emph{평균}을 취하면 로그 몫과 $(1-2\xi)$ 몫이 각각 부호 반대로
상쇄되어 $\tfrac12[V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^{\mathrm{cat},-})+V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^{\mathrm{cat},+})]
=U_j^\mathrm{cat}$(식~\eqref{eq:hyssym} 과 동일 대수) — 분기가 $U_j^\mathrm{cat}$ 대칭이라는 흑연의 대칭성이
LCO 에도 host-무관하게 성립함을 재확인한다.

\textbf{(d) 박스 — LCO 전이별 gap 과 분기 중심.}
\begin{equation}
\boxed{\;
\Delta U_j^{\hys,\mathrm{cat}}(T)=
\begin{cases}
\dfrac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\operatorname{artanh}u_j^\mathrm{cat}\big],
& \Omega_j^\mathrm{cat}>2RT,\\[4pt]
0, & \Omega_j^\mathrm{cat}\le2RT,
\end{cases}
\quad u_j^\mathrm{cat}=\sqrt{1-\dfrac{2RT}{\Omega_j^\mathrm{cat}}}\;}
\label{eq:lco-dUhys}
\end{equation}
\begin{equation}
\boxed{\;U_j^{\,d,\mathrm{cat}}=U_j^\mathrm{cat}
+\tfrac12\sigma_d h_{\eta,j}\gamma_j\,\Delta U_j^{\hys,\mathrm{cat}}(T)\;}
\label{eq:lco-Ubranch}
\end{equation}
흑연 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 의 LCO 대입형이다. 방전($\sigma_d=+1$)은 분기 중심을 위로,
충전($\sigma_d=-1$)은 아래로 옮긴다 — $U_j^{\dis,\mathrm{cat}}>U_j^{\chg,\mathrm{cat}}$.

\textbf{(T2$\cdot$T3) order--disorder.} $x\approx0.5$ 부근 monoclinic 초격자를 이루는 T2($\sim$4.05 V,
hex$\to$monoclinic)$\cdot$T3($\sim$4.17--4.20 V, monoclinic$\to$hex)는 동종 이웃 인력 $\Omega_j^\mathrm{cat}>0$
이 만드는 상분리의 LCO 사례다. 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 $j=2,3$ 을 넣으면 그대로
열린다. \textbf{★혼동 가드(Ω vs config ΔS).} 정렬의 charge-order 엔트로피 변화($\approx0.47$ J/(mol\,K)@$x{=}
\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$ [tier A, Motohashi\cite{motohashi2009}])는 \emph{엔트로피}
값으로 식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$ 슬롯(곧 $U_j^\mathrm{cat}(T)$ 의 온도 이동)에
들어가지, spinodal 문턱을 정하는 \emph{상호작용 에너지} $\Omega_j^\mathrm{cat}$[J/mol]가 \emph{아니다} — 둘은
차원부터 다른 양(J/(mol\,K) 대 J/mol)이므로 ``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 다리를 놓지 않고
$\Omega_j^\mathrm{cat}$ 는 gap 을 정하는 별도 피팅 파라미터로 둔다(수치 날조 금지 — $\Omega_j^\mathrm{cat}$
자체의 값은 여기서 특정하지 않는다).

\textbf{(T1) MIT 2상역.} T1($\sim$3.90 V, $x\approx0.94$--$0.75$, 절연체$\to$금속)의 구조적 2상 공존도 같은
정규용액 문턱을 받아 $u_1^\mathrm{cat}=\sqrt{1-2RT/\Omega_1^\mathrm{cat}}$, $\Delta U_1^{\hys,\mathrm{cat}}$,
$U_1^{\,d,\mathrm{cat}}$ 이 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 그대로 열린다. \textbf{★이중계산
방지 슬롯 분리.} MIT 고유의 전자 자유도는 이 히스 gap 에 새 항으로 섞지 않는다 — 그 항은 이미
$\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}+\Delta S_{e,1}^\mathrm{mol}(x,T)$
(식~\eqref{eq:lco-decomp})를 통해 $U_1^\mathrm{cat}(T)$ 의 온도 이동(식~\eqref{eq:lco-dUdT})에 들어간다. 곧 두
몫이 서로 다른 슬롯에 산다:
\begin{equation}
\boxed{\;
\underbrace{\Delta U_1^{\hys,\mathrm{cat}}\ (\text{구조적 2상역})\ \Leftarrow\ \Omega_1^\mathrm{cat}}_{\text{정규용액 히스 gap (이 절)}}
\quad\Big\|\quad
\underbrace{\partial U_1^\mathrm{cat}/\partial T\ \Leftarrow\ \Delta S_{e,1}^\mathrm{mol}(x,T)}_{\text{전자 엔트로피 (\S\ref{sec:lco-electronic})}}\;}
\label{eq:lco-mit}
\end{equation}
이 분리가 config 2상역과 전자 엔트로피를 이중계산하지 않는 경계다.

\textbf{도핑 보정(우리 시료).} Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox$\cdot$전자항을 보존하되 order--
disorder$\cdot$MIT 상전이를 억제한다 — 정규용액 틀에서 이는 pure-LCO 초기값 $\Omega_j^\mathrm{cat,pure}$ 를
도핑 피팅값 $\Omega_j^\mathrm{cat,dop}$ 로 낮추는 입력 변화다. 식~\eqref{eq:lco-dUhys} 의 문턱 극한은(흑연
식~\eqref{eq:dUhys} 아래 Taylor 극한과 동일 대수, $u\to0$ 일 때 $\operatorname{artanh}u=u+u^3/3+\cdots$)
\begin{equation}
\Omega_j^\mathrm{cat,dop}\to2RT^+\ \Longrightarrow\
u_j^\mathrm{cat,dop}\to0,\quad
\Delta U_j^{\hys,\mathrm{cat,dop}}\to\frac{8RT}{3F}\big(u_j^\mathrm{cat,dop}\big)^3\to0,
\label{eq:lco-dope}
\end{equation}
($T_{c,j}=\Omega_j^\mathrm{cat}/2R$), 이고 $\Omega_j^\mathrm{cat,dop}\le2RT$ 로 피팅되는 전이는 같은 식 안에서
gap 이 0 으로 닫힌다 — 상전이 억제에 따른 히스 축소$\cdot$peak smear 의 수식 표현이며, 풀린 몫은
\S\ref{sec:broadening} 의 broadening 폭이 더 크게 담는다(그래파이트 두-상 전용인 (iii-a) Dreyer 순차전환
메커니즘은 LCO 로 옮기지 않고 일반 $\eta$ 산포로만 다룬다는 \S\ref{sec:broadening}(a) 의 범위 한정과 정합).
```

**원 줄글 대비**: 원문(L697-719)은 세 문단(T2·T3, T1, 도핑) 모두 "같은 정규용액 틀을 그대로 적용한다"는
결론을 서술하되 $\Omega_j^\mathrm{cat}$ 를 spinodal 식에 실제로 대입한 중간식이 전무했다(V1010 STYLE_REPORT
"Ω_j spinodal 대입 중간식 전무" 판정과 정확히 부합). 신규 (a)-(d)는 그 대입을 실제로 수행해 `eq:lco-gxi
→eq:lco-gpp→eq:lco-spinodal→eq:lco-Veq→eq:lco-dUhys/eq:lco-Ubranch` 사슬로 닫고, 원문에 없던 **대칭점 검산**
((c) 말미)을 추가했다. T2·T3/T1/도핑 문단의 물리·수치(0.47/1.49, 도핑 서술)는 원문과 동일 — 다만 T1 문단에
원문에 없던 **명시적 슬롯분리 박스**(`eq:lco-mit`)를 신설해 "두 몫을 분리"라는 원문 서술(L712-713)을 식으로
못박았다. Ω vs config ΔS 혼동 가드는 원문에 암묵적으로만 있던 것을 명시적 경고 문장으로 승격.

**논리 감사(재유도 근거)**:
- *부호*: $\Delta U_j^{\hys,\mathrm{cat}}\ge0$(극대$>$극소, $u\in(0,1)$ 에서 $\Omega u>2RT\,\operatorname{artanh}u$
  는 흑연과 동일 부등식 — host 무관 대수이므로 재확인만 필요, 재확인 완료).
- *차원*: $\Omega_j^\mathrm{cat}u_j^\mathrm{cat}$ 의 차원 J/mol, $2RT\operatorname{artanh}u$ 의 차원 J/mol — 합을
  $F$[C/mol]로 나누면 J/C=V, $\Delta U_\hys$ 의 기대 차원과 일치.
- *극한*: $\Omega_j^\mathrm{cat}\to2RT^+$ 에서 $u\to0$, $\Delta U_\hys\to(8RT/3F)u^3\to0$ — 연속(불연속 없음),
  도핑이 상전이를 완전히 눌렀을 때 히스가 매끈히 사라진다는 물리와 일치.
- *detailed balance/대칭*: spinodal 두 끝점 평균 $=U_j^\mathrm{cat}$ (재유도로 확인, (c) 말미) — 분기가 중심
  대칭이라는 요구를 만족.
- *이중계산*: T1 슬롯분리 박스(`eq:lco-mit`)로 구조적 2상역(Ω 경로)과 전자 엔트로피(§lco-electronic 경로)가
  겹치지 않음을 명시 — 재확인 결과 결함 없음.
- *범위 한정*: 도핑 문단 말미에 §broadening(a)의 "(iii-a) Dreyer 메커니즘은 흑연 두-상 전용, LCO 는 일반 η
  산포만"이라는 기존 범위 한정을 명시적으로 재확인 — LCO 에 그래파이트-특정 메커니즘을 잘못 확장하는 것을
  차단(신규 결함 발견은 아니고, 기존의 올바른 범위 한정을 본 절에서도 어기지 않도록 교차 확인).

---

## 3. `sec:lco-peak` (실측 L1220 헤더, 교체 L1221–1232)

**편입 지시**: L1220 헤더 그대로, L1221–1232 를 아래로 교체. 다음 소절 `sec:broadening`(L1234, 미접촉).

```latex
\textbf{(a) 출발 — 전하보존 미분은 전극 불문.} \S\ref{sec:eqpeak} 의 평형 peak 박스(식~\eqref{eq:eqpeak})는
전하보존식의 직접 미분(식~\eqref{eq:belliden} 의 종 항등식 경유)에서 나오며, 그 유도 어디에도 host 항이 없다
(\S\ref{sec:lco-center} (a)의 논거와 같은 형식 — 전하보존$\cdot$logistic 미분은 전이의 물리적 정체를 몰라도
성립하는 항등식). 따라서 LCO 세 전이 $j\in\{\mathrm{T1,T2,T3}\}$ 에 그대로 적용된다.

\textbf{(b) 연산 — 세 전이에 대입.} 전이별 중심 $U_j^{\,d,\mathrm{cat}}$(식~\eqref{eq:lco-Ubranch})와 폭 $w_j$
(식~\eqref{eq:wbase}, 이중지위는 (d) 참조)를 식~\eqref{eq:eqpeak} 에 넣으면
\begin{align*}
\Big(\frac{\dd Q}{\dd V}\Big)^\eq_\mathrm{T1}&=Q_\mathrm{T1}\,\frac{\xi_{\eq,\mathrm{T1}}(1-\xi_{\eq,\mathrm{T1}})}{w_\mathrm{T1}},\\
\Big(\frac{\dd Q}{\dd V}\Big)^\eq_\mathrm{T2}&=Q_\mathrm{T2}\,\frac{\xi_{\eq,\mathrm{T2}}(1-\xi_{\eq,\mathrm{T2}})}{w_\mathrm{T2}},\\
\Big(\frac{\dd Q}{\dd V}\Big)^\eq_\mathrm{T3}&=Q_\mathrm{T3}\,\frac{\xi_{\eq,\mathrm{T3}}(1-\xi_{\eq,\mathrm{T3}})}{w_\mathrm{T3}}.
\end{align*}

\textbf{(c) 중간식 — LCO 영역 합산.} 식~\eqref{eq:sum} 을 LCO 세 전이로 국한하면
\[
\Big(\frac{\dd Q}{\dd V}\Big)_\mathrm{LCO}=C_\bg^\mathrm{cat}+\sum_{j\in\{\mathrm{T1,T2,T3}\}}
Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}.
\]

\textbf{(d) 박스 — 세 봉우리의 위치$\cdot$높이$\cdot$면적.}
\begin{equation}
\boxed{\;\Big(\frac{\dd Q}{\dd V}\Big)_\mathrm{LCO}
=\sum_{j\in\{\mathrm{T1,T2,T3}\}}Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}\;,\qquad
\text{위치}=U_j^{\,d,\mathrm{cat}},\ \ \text{순높이}=\frac{Q_j}{4w_j},\ \ \text{면적}=Q_j\;.}
\label{eq:lco-peaksum}
\end{equation}
흑연이 $\sim$0.085--0.21 V 에 네 봉우리를 남기듯, LCO 하프셀은 \emph{양극 전위 영역}에 세 봉우리를 남긴다 — T1
의 $\sim$3.90 V(MIT plateau), T2 의 $\sim$4.05 V, T3 의 $\sim$4.17--4.20 V(한 쌍의 좁은 order--disorder 봉우리).
폭은 흑연과 같은 $w_j=n_jRT/F$ 이며, LCO 의 세 전이 \emph{모두} $\Omega_j^\mathrm{cat}>2RT$ 의 두-상이라(표~
\ref{tab:lco-staging}) 그 폭은 \S\ref{sec:width} 이중지위의 \emph{두-상} 측 — 평형 예측이 아니라 broadening
이 정하는 현상학적 피팅 폭이다(\S\ref{sec:broadening}; 단 그래파이트 두-상 전용 (iii-a) Dreyer 메커니즘은
LCO 로 옮기지 않고 일반 $\eta$ 산포만 적용 — \S\ref{sec:broadening}(a) 범위 한정 그대로). order--disorder 의
큰 $\Omega$ 가 spinodal gap 을 키워 T2$\cdot$T3 의 분기를 흑연보다 날카롭게(좁은 한 쌍 peak 로) 만든다. T1 의
위치는 \S\ref{sec:lco-electronic} 의 전자항이 $\Delta S_{\rxn,1}^\mathrm{cat}$ 를 통해 $U_1(T)$ 의 \emph{온도
이동}에 기여하므로(식~\eqref{eq:lco-dUdT}), 다온도 dQ/dV 에서 T1 봉우리의 \emph{온도 이동률}
$\partial U_1/\partial T$ 가 $T$ 에 선형으로 커지는 것이 전자항의 관측 신호다($\Delta S_{e,1}\propto T$,
\S\ref{sec:lco-Se} — 위치 자체가 아니라 \emph{이동률}이 $T$-선형, 위치 이동은 $\propto T^2$, 식~\eqref{eq:U1T2}).
도핑은 \S\ref{sec:lco-hys} 대로 봉우리를 smear$\cdot$shift 시킨다.
```

**원 줄글 대비**: 원문(L1221-1232)은 위치$\cdot$순높이$\cdot$면적을 문장으로만 서술("표~lco-staging 의 LCO
전이로 읽힌다")하고 세 전이 각각의 peak 식을 실제로 쓰지 않았다. 신규 (a)-(d)는 그 세 식을 명시적으로 전개하고
합산식(`eq:lco-peaksum`, 신설)으로 닫는다 — V1010 STYLE_REPORT 의 "ΣQ_j peak_shape→center/height/area 박스"
요구를 정확히 충족. T1 온도이동률·도핑 서술은 원문과 동일(수치·인용 불변, 위치만 (d) 안으로 재배치).

**논리 감사(재유도 근거)**:
- *부호*: peak 모양 $\xi(1-\xi)/w\ge0$ — 방향 불변(흑연과 동일 항등식, host 무관 재확인).
- *차원*: 순높이 $Q_j/(4w_j)$ — [C]/[V] = C/V(미분용량 단위), 면적 $Q_j$[C] — $\int_0^1\dd\xi=1$ 치환적분
  (식~\eqref{eq:belliden})으로 원문과 동일 확인.
- *이중계산*: T1 위치의 온도이동을 다시 폭$\cdot$면적에 중복 반영하지 않음 — 온도이동은 중심 $U_1^{d,\mathrm{cat}}$
  자리에만, 전자항은 §lco-decomp 슬롯에만(교차 확인, 결함 없음).
- *범위*: broadening (iii-a) Dreyer 메커니즘을 LCO 로 확장하지 않는다는 재확인 — §2 와 동일 점검, 중복이지만
  두 절 모두에서 어기지 않았는지 각각 확인해야 하므로 반복 검산 유지(§3 방법론 원칙).

---

## 4. `sec:lco-decomp` (실측 L1715 헤더, 교체 L1716–1754)

**편입 지시**: L1715 헤더 그대로, L1716–1754 를 아래로 교체(기존 `eq:lco-decomp` 박스$\cdot$itemize 는 (d)로
**내용 완전 동일 재수록** — 9곳 다운스트림 `\eqref{eq:lco-decomp}` 참조 유지).

```latex
\textbf{(a) 출발 — 세 자유도의 (근사) 직교성.} 흑연에서 합산식~\eqref{eq:sum} 에 들어가는 $\Delta S_{\rxn,j}$
는 평형 중심 $U_j(T)$ 를 통해 한 덩이로 작용했다. LCO 에서는 이 한 덩이가 세 통계역학적 자유도 — 리튬 자리
\emph{배열}(config)$\cdot$격자 \emph{진동}(vib)$\cdot$전도 전자 \emph{밴드 점유}(electronic) — 의 합임을 명시한다.
세 부분계가 (근사) 독립이면 전체 분배함수가 인수분해된다: $Z\approx Z_\mathrm{config}\cdot Z_\mathrm{vib}\cdot
Z_\mathrm{elec}$.

\textbf{(b) 연산 — 인수분해에서 가법성으로.} 자유에너지 $F=-k_BT\ln Z$ 와 엔트로피 $S=-\partial F/\partial T$
의 정의를 인수분해에 적용하면 $\ln Z=\ln Z_\mathrm{config}+\ln Z_\mathrm{vib}+\ln Z_\mathrm{elec}$ 이므로
$F=F_\mathrm{config}+F_\mathrm{vib}+F_\mathrm{elec}$, 곧
\[
S=S_\mathrm{config}+S_\mathrm{vib}+S_\mathrm{elec}
\]
이 독립(직교) 부분계의 표준 가법성이다 — 교차항은 진짜 독립일 때 정확히 0. MIT 부근에서 리튬 정렬과 전자 밴드
채움이 다소 결합하나, 이 결합(교차) 몫은 선도 차수에서 무시되며(약결합 근사), 그 차수에서 가법성이 성립한다
(\emph{가산성}만의 근거 — ``과대계상 없음''은 별도로 (d)의 이중계산 금지 규칙이 담당한다).

\textbf{(c) 중간식 — 부분몰(삽입당) 형태로.} 삽입 1몰당 변화로 옮기면
\[
\Delta S_{\rxn,j}^\mathrm{cat}(x,T)=\frac{\partial S}{\partial x}\Big|_j
=\Delta S_j^\mathrm{config}+\Delta S_j^\mathrm{vib}+\Delta S_{e,j}^{\,\mathrm{mol}}(x,T),
\]
이고, config 슬롯은 \S\ref{sec:dist} 의 격자기체 점유 분포가 이미 자동 생성하는 봉우리 \emph{중심} 표준값만
받는다(봉우리 \emph{내부}의 $x$-의존은 logistic 자체가 담아 별도로 더하지 않음 — 흑연의 파생 B 와 같은 이중
계산 방지 규칙).

\textbf{(d) 박스 — LCO 삽입 반응 엔트로피 분해.}
\begin{equation}
\boxed{\;\Delta S_{\rxn,j}^\mathrm{cat}(x,T)=\underbrace{\Delta S_j^\mathrm{config}}_{\text{logistic }w=RT/F\text{ 가 담음}}
+\underbrace{\Delta S_j^\mathrm{vib}}_{\text{음의 baseline}}
+\underbrace{\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)}_{\text{MIT 게이트, 삽입 기준 }<0,\ \propto T\ (\text{몰당 식~\eqref{eq:dSemolar}})}\;.}
\label{eq:lco-decomp}
\end{equation}
세 몫의 역할과 \emph{이중계산 방지}는 다음과 같다.
\begin{itemize}[leftmargin=1.4em,itemsep=2pt]
\item \textbf{config.} O3 영역에서 LCO $\Delta S$ 를 지배($>\tfrac12$\cite{reynier2004}, tier A)하며, 기존
Ch1 logistic 이 이를 \emph{자동 생성}한다 — 봉우리 중심의 표준값 $\Delta S_j^0$ 에 봉우리 내부 항
$R\ln[(1-\xi)/\xi]$ 가 격자기체 점유 분포(\S\ref{sec:dist})에서 따라 나온다. \textbf{★이중계산 금지(B).} 따라서
식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$ 자리에는 봉우리 \emph{중심 표준값} $\Delta S_j^0$ 만
넣는다 — 봉우리 내부 조성 의존은 logistic 이 이미 담고 있어 두 번 더하면 안 된다(표~\ref{tab:lco-staging} 의
config 값 = 중심 표준값으로 읽음). \textbf{★가법성 정당화(T1 MIT, 직교 자유도).} 두 가지를 구분해 못박는다.
\emph{(가) 가산성} — config(리튬 자리 \emph{점유 배열}의 자유도)와 $\Delta S_{e,j}$(전도 전자 \emph{밴드 점유}의
자유도)는 서로 다른 자유도라 통계역학적으로 \emph{근사적으로 직교}한다: 두 부분계가 독립인 극한에서 전체
분배함수가 $Z=Z_\mathrm{config}\!\cdot\!Z_\mathrm{elec}$ 로 인수분해되어 $S=S_\mathrm{config}+S_\mathrm{elec}$
가 교차항(잔차) $0$ 으로 가산된다(위 (a)(b)의 재유도). \emph{(나) 무이중계산} — 두 항의 합이 측정 $\Delta S$ 를
\emph{초과하지 않음}은 직교성이 아니라 위 ★이중계산 금지(B) 규칙이 보장한다: config 슬롯에 봉우리
\emph{중심값}만, elec 슬롯에 MIT 게이트 \emph{골}만 넣어 각 항이 자기 자유도의 몫만 채우므로, 같은 엔트로피를
두 번 세지 않는다. 곧 직교성은 ``더해도 되는가''(가산성)를, 이중계산 금지 규칙은 ``과대 계상 없는가''(무초과)를
각각 보장한다.
\item \textbf{vib.} 고-$x$ 의 phonon 음의 baseline 으로, Ch1 흑연과 동형이다(흑연 표~\ref{tab:staging} 의 음의
$\Delta S_\rxn$ 에 대응). 별도 식 변화 없음.
\item \textbf{electronic.} \S\ref{sec:lco-electronic} 의 신규 항 $\Delta S_{e,j}(x,T)<0$(닫힌식~\eqref{eq:dSegate},
몰당 환산 식~\eqref{eq:dSemolar} 로 $\Delta S_{e,j}^{\,\mathrm{mol}}=N_A\Delta S_{e,j}$ 가 이 자리에 들어감;
\emph{삽입 기준} — $\Delta S_{\rxn,j}$ 슬롯과 일관, 부호 뒤집기 없음; MIT 창 통과 시 게이트 적분 방출
$\approx1.1\,k_B$/atom — Reynier 의 $0.18\,k_B$/atom 은 \emph{총 부분몰} 실측으로 별개 양이다).
흑연엔 0, LCO 는 T1 의 MIT 게이트에서만 켜진다. 셋 중 유일하게 $\propto T$ 라, 다온도 피팅에서 다른 둘과 분리
식별된다.
\end{itemize}
이 세 몫의 합이 식~\eqref{eq:lco-dUdT} 의 $\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$ 를 통해 LCO
$U_j(T)$ 의 온도 이동을 정하고, 그 $U_j(T)$ 가 흑연과 \emph{같은} 합산식~\eqref{eq:sum} 으로 dQ/dV 에 들어간다.
연속 $\Delta S(x)$$\cdot$$g(E_F)(x)$$\cdot$도핑 shift 의 정밀값은 1차 문헌에 없으므로(갭 G1$\cdot$G2$\cdot$G4),
표~\ref{tab:lco-staging}$\cdot$식~\eqref{eq:ggate} 의 초기값을 우리 코인 하프셀 데이터로 round-trip 피팅해
식별한다 — 흑연 ``문헌 초기값 + 데이터 피팅'' 철학 그대로이며, 허위 정밀을 피해 tier 를 병기한다.
```

**원 줄글 대비**: 원문(L1716-1754)은 이미 박스$\cdot$itemize$\cdot$가법성 논거를 갖춘 상당히 완성도 높은
절이었다(V1010 STYLE_REPORT 판정 "분해 박스는 있으나 ... 이중계산·직교가산이 줄글 검산" — 결과는 있으나 도출
과정이 없었다는 뜻). 신규 (a)(b)(c)는 원문이 서술로만 주장한 "$Z=Z_\mathrm{config}\cdot Z_\mathrm{elec}$"
인수분해를 실제로 $F=-k_BT\ln Z\to S=-\partial F/\partial T$ 경로로 재유도해 $S=S_\mathrm{config}+S_\mathrm{vib}+
S_\mathrm{elec}$ 가 \emph{나오는 이유}를 보인다(vib 를 명시적으로 인수분해에 포함시켜 세 자유도 전부를
일관되게 다룸 — 원문은 vib 를 인수분해 논거에서 빠뜨리고 config·elec 만 언급했었다). (d) 박스$\cdot$itemize
는 \textbf{원문과 완전 동일}(한 글자도 변경 없음 — 라벨$\cdot$수치$\cdot$인용 전부 보존).

**논리 감사(재유도 근거)**:
- *가산성 재유도*: $\ln Z=\sum\ln Z_i\Rightarrow F=\sum F_i\Rightarrow S=\sum S_i$ — 독립 부분계의 표준
  통계역학 항등식(교과서 수준), 직접 재현해 정합 확인. 원문이 vib 를 인수분해 서술에서 누락했던 점을
  보완(vib 도 독립 자유도이므로 포함이 타당 — 결함은 아니고 서술 누락, 물리적 결론 자체는 원문과 동일).
- *이중계산*: config 슬롯=중심값만, elec 슬롯=게이트 골만 — 재확인, 결함 없음(파생 B 흑연 규칙과 동형).
- *차원*: $\Delta S_j^\mathrm{config},\Delta S_j^\mathrm{vib},\Delta S_{e,j}^{\mathrm{mol}}$ 모두 J/(mol·K) —
  합산 이전에 차원 일치 확인(단위 다리는 §lco-Se 에서 이미 검증된 것을 재확인만).
- *결함 탐색*: (a)의 "직교" 주장이 verifybox(§lco-center L507-515)의 "+80−46≈+34" sanity 산법과 스케일이
  다른 양을 섞는 것은 아닌지 교차 점검 — §lco-electronic 의 "★세 양의 구분"(L1139-1146)이 이미 이 세 수치를
  섞지 말라 경고하며, §lco-center verifybox 는 스스로 "sanity"로 한정하고 있어 이중잣대나 결함은 아님(§1
  논리감사에서 이미 확인, 여기서는 정합성 재확인만).

---

## 5. 전자항 plug-in (실측 L1756–1765, `sec:lco-decomp` 절 말미)

**편입 지시**: L1755 공백줄$\cdot$L1767 `sec:lco-code` 헤더는 그대로, L1756–1765 를 아래로 교체.

```latex
\textbf{(a) 출발 — 좌표를 잇는다: $x=x(\xi_{\eq,\mathrm{T1}}(V,T))$.} 식~\eqref{eq:dSegate} 의 전자 엔트로피
게이트 $\Delta S_{e,1}(x,T)$ 는 \emph{조성} $x$ 의 함수인데, forward 코드 \code{dqdv} 는 \emph{전압} 격자
위에서 돈다. 두 좌표는 T1 전이 자체의 평형 진행률 $\xi_{\eq,\mathrm{T1}}(V,T)$(식~\eqref{eq:xieq}, $j=\mathrm{T1}$)
로 잇는다 — $\xi_{\eq,\mathrm{T1}}$ 이 $0\to1$ 로 나아가는 것이 T1 구간의 조성이 표~\ref{tab:lco-staging} 의
범위($x\approx0.94\to0.75$)를 따라 나아가는 것과 같은 진행이므로, 그 구간 안에서
\[
x(\xi_{\eq,\mathrm{T1}})\ =\ x_\mathrm{start}-(x_\mathrm{start}-x_\mathrm{end})\,\xi_{\eq,\mathrm{T1}},
\qquad \{x_\mathrm{start},x_\mathrm{end}\}=\{0.94,\,0.75\}
\]
가 \emph{가장 단순한 candidate}(아핀 사상)다. \textbf{★이 사상의 지위 — 예시, 확정 아님.} 원문(구현 예고
단락)은 이 좌표 매핑을 ``별도 상태 변수 또는 전이 진행률 매핑''으로만 열어두고 구체 함수형을 확정하지 않았다
— 위 아핀형은 표~\ref{tab:lco-staging} 에 이미 실린 T1 의 $x$-범위 두 끝점만 쓴 예시적 구성이며, 실제 구현
선택(아핀 vs 비선형 매핑)은 다온도 round-trip 피팅 단계의 과제로 \emph{남긴다}(추정 금지 원칙 — 이 문건은
사상이 \emph{존재}한다는 사실과 합성 순서만 못박고, 구체 함수형을 신뢰값으로 승격하지 않는다).

\textbf{(b) 연산 — 게이트에 대입.} $x(\xi_{\eq,\mathrm{T1}}(V,T))$ 를 닫힌식~\eqref{eq:dSegate}$\cdot$
\eqref{eq:dSemolar} 에 대입하면 전자 엔트로피가 전압$\cdot$온도의 함수로 닫힌다:
\[
\Delta S_{e,1}^{\,\mathrm{mol}}(V,T)=N_A\cdot\Big[-\frac{\pi^2}{3}k_B^2T\,\frac{g_\mathrm{max}}{\Delta x_\mathrm{MIT}}
\,\sigma(z)\big(1-\sigma(z)\big)\Big]_{z=[x(\xi_{\eq,\mathrm{T1}}(V,T))-x_\mathrm{MIT}]/\Delta x_\mathrm{MIT}}.
\]

\textbf{(c) 중간식 — 분해식에 넣어 온도 이동으로.} 식~\eqref{eq:lco-decomp} 에 넣으면
$\Delta S_{\rxn,1}^\mathrm{cat}(x,T)=\Delta S_0+\Delta S_{e,1}^{\,\mathrm{mol}}(x,T)$($\Delta S_0=\Delta S_1^\mathrm{config}
+\Delta S_1^\mathrm{vib}$, $T$ 무관 상수), 이를 식~\eqref{eq:lco-dUdT} 의 $\partial U_1/\partial T=\Delta
S_{\rxn,1}^\mathrm{cat}(T)/F$ 에 넣어 $T_0$ 에서 적분하면 이미 유도된 식~\eqref{eq:U1T2} 의
\[
U_1(T)=U_1(T_0)+\frac{\Delta S_0}{F}(T-T_0)+\frac{a_e}{2F}(T^2-T_0^2)
\]
로 닫힌다($a_e$ 는 식~\eqref{eq:U1T2} 정의와 동일).

\textbf{(d) 박스 — plug-in 전체 사슬과 두 설계 항목.}
\begin{equation}
\boxed{\;
\xi_{\eq,\mathrm{T1}}(V,T)\ \xrightarrow{\ x\text{-map}\ }\ x
\ \xrightarrow{\ \eqref{eq:dSegate},\eqref{eq:dSemolar}\ }\ \Delta S_{e,1}^{\,\mathrm{mol}}(x,T)
\ \xrightarrow{\ \eqref{eq:lco-decomp}\ }\ \Delta S_{\rxn,1}^\mathrm{cat}(x,T)
\ \xrightarrow{\ \eqref{eq:lco-dUdT},\eqref{eq:U1T2}\ }\ U_1(T)
\ \xrightarrow{\ \eqref{eq:sum}\ }\ \frac{\dd Q}{\dd V}\;}
\label{eq:lco-plugin}
\end{equation}
본 분해를 forward 코드로 옮기는 다음 단계는 두 가지를 명시해 둔다. \emph{(i) 좌표 매핑}은 위 (a)의 지위대로
구현 선택으로 남긴다. \emph{(ii) round-trip 가드.} 식~\eqref{eq:lco-decomp} 의 config 중심 표준값 $\Delta S_j^0$
(Motohashi\cite{motohashi2009} $\approx0.47/1.49$ J/(mol\,K), T2/T3)은 아직 round-trip 으로 실증되지 않은
\emph{초기값}이므로(신뢰값 아님), 흑연 $\Delta S_\rxn{=}-16$ J/(mol\,K) 의 round-trip 절차와 동격으로 — T1
위치 $U_1(298)\approx3.90$ V 와 $\partial U_1/\partial T$ 의 부호$\cdot$기울기(다온도 이동률)를 self-test 로
맞추어 — 검증한 뒤에 신뢰값으로 승격한다.
```

**원 줄글 대비**: 원문(L1756-1765)은 "본 분해를 forward 코드로 옮기는 다음 단계는 두 가지를 명시해 둔다"로
시작해 (i)(ii) 항목을 서술했으나, T1 의 $\Delta S_e$ 가 실제로 dQ/dV 까지 이어지는 \emph{합성 사슬}은 문장으로
지목만 하고 식으로 잇지 않았다(V1010 STYLE_REPORT "'T1 ΔS_rxn 에 몰당 전자항 더하는 한 줄' 결론" 판정과 부합).
신규 (a)-(d)는 $\xi_{\eq,\mathrm{T1}}\to x\to\Delta S_{e,1}\to\Delta S_{\rxn,1}^\mathrm{cat}\to U_1(T)\to
\dd Q/\dd V$ 사슬을 실제 식 대입으로 닫아(`eq:lco-plugin`, 신설 스키마 박스) 요구된 forward 사슬을 완성한다.
(i)(ii) 항목 서술은 원문과 동일(구현 선택 지위·round-trip 가드 문장 불변) — (a)의 아핀 좌표 사상만 \textbf{신규
추가}(원문에 없던 명시 함수형, "예시·확정 아님"으로 명확히 한정).

**논리 감사(재유도 근거)**:
- *추정 금지 준수*: (a)의 아핀 사상은 원문이 미확정으로 남긴 것을 \emph{추측해 채우지 않고}, "가장 단순한
  candidate"·"예시, 확정 아님"으로 명시적으로 한정했다 — 표~\ref{tab:lco-staging} 에 \emph{이미 실린} 두
  끝점 수치(0.94, 0.75)만 사용, 새 수치 발명 없음.
- *부호*: $\xi_{\eq,\mathrm{T1}}\uparrow$(탈리튬화 진행) $\Rightarrow x\downarrow$(리튬 함량 감소) — 아핀
  사상의 부호(음의 기울기)가 이 물리와 일치.
- *차원*: 사슬 끝단까지 각 화살표가 기존에 이미 차원 검증된 식(`eq:dSegate`, `eq:dSemolar`, `eq:lco-decomp`,
  `eq:lco-dUdT`, `eq:U1T2`, `eq:sum`)만 인용 — 새 차원 문제 도입 없음(재확인 완료).
- *이중계산*: T1 온도이동(§lco-center 대표 스케일)과 본 절의 $\Delta S_{e,1}(x,T)$ 대입이 같은 $\Delta S_0$
  자리를 두 번 채우지 않도록 (c)에서 $\Delta S_0=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}$(전자항
  제외)로 명시 — 결함 없음.

---

## 6. MSMR — `sec:lco-code` (실측 L1767 헤더, 교체 L1768–1792)

**편입 지시**: L1767 헤더 그대로, L1768–1792 를 아래로 교체(`eq:msmr` 라벨은 (a)에서 그대로 승계 — L1879
테이블 참조 유지).

```latex
이 통합의 실용적 결론은 ``같은 코드가 LCO 를 그린다''이다.

\textbf{(a) 출발 — MSMR 식.} multiphase species reaction(MSMR) 모델\cite{msmr2024}은 양극 전위를 전이별
logistic 의 합으로 적는다:
\begin{equation}
x_j=\frac{X_j}{1+\exp[\,f(U-U_j^0)/\omega_j\,]}.
\label{eq:msmr}
\end{equation}

\textbf{(b) 연산 — 정규화.} 용량 가중을 나누어 정규화 점유 $\hat x_j\equiv x_j/X_j\in[0,1]$ 를 두면
\[
\hat x_j=\frac{1}{1+\exp[\,f(U-U_j^0)/\omega_j\,]}.
\]

\textbf{(c) 중간식 — 대응표 대입.} MSMR 의 $f$ 는 종별 부호 인자 $\pm1$ 이고, 식~\eqref{eq:msmr} 의 지수는
$+f(U-U_j^0)$ 인 반면 Ch1 식~\eqref{eq:xieq} 의 지수는 $-\sigma_d(V-U_j^{\,d})$ 이다 — 두 지수가 같은 자리를
채우므로 $f=-\sigma_d$(방향 인자 대응)이고, 나머지 대응 $X_j\leftrightarrow Q_j$, $U_j^0\leftrightarrow
U_j^{\,d}$, $\omega_j\leftrightarrow w_j$, $U\leftrightarrow V$ 를 (b)에 대입하면
\[
\hat x_j=\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d})/w_j]}.
\]

\textbf{(d) 박스 — 폐쇄: $\hat x_j\equiv\xi_{\eq,j}$, MSMR 미분 $=$ 흑연 peak 박스.} 위 우변은 식~
\eqref{eq:xieq} 의 $\xi_{\eq,j}(V,T)$ 와 \emph{글자 그대로 같다}:
\begin{equation}
\boxed{\;\hat x_j\ \equiv\ \xi_{\eq,j}(V,T)\;}
\label{eq:lco-msmrid}
\end{equation}
곧 MSMR 은 새 함수가 아니라 Ch1 logistic 의 재표기다. 미분도 그대로 닫힌다 — $x_j=X_j\hat x_j=Q_j\xi_{\eq,j}$
이므로 $\dd x_j/\dd U=Q_j\,\dd\xi_{\eq,j}/\dd V=Q_j\,\sigma_d\,\xi_{\eq,j}(1-\xi_{\eq,j})/w_j$(식~
\eqref{eq:belliden} 의 종 항등식과 연쇄율, \S\ref{sec:eqpeak}(b)(c)와 동일 대수), 절댓값을 취하면
\[
\Big|\frac{\dd x_j}{\dd U}\Big|=Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}
\]
로 식~\eqref{eq:eqpeak}(및 LCO 특화형 \eqref{eq:lco-peaksum})과 \emph{완전히 같다} — MSMR$\to\xi_{\eq,j}
\to$peak 박스의 사슬이 대수로 닫힌다(V1010 STYLE_REPORT 가 지적한 ``변환 사슬 미폐쇄''를 여기서 메운다). 따라서
Ch1 의 곡선 클래스(\code{func\_ksi\_eq}$\cdot$\code{func\_U\_j}$\cdot$합산~\eqref{eq:sum})는 \emph{구조 변경 0}
으로 LCO 에 적용되며, 바뀌는 것은 단 둘이다:
\begin{enumerate}[label=(\roman*),leftmargin=2.2em,itemsep=1pt]
\item \textbf{전이 파라미터 교체} — \code{GRAPHITE\_STAGING\_LIT} $\to$ \code{LCO\_MSMR\_LIT}(표~
\ref{tab:lco-staging}): $(\Delta H_\rxn,\Delta S_\rxn,Q,\Omega,\Delta H_a,\dots)$ 값을 양극 영역으로. 코드의
전이 dict 키 구조는 동일하다.
\item \textbf{전자 엔트로피 항 plug-in} — T1 전이의 $\Delta S_{\rxn}$ 평가에 \S\ref{sec:lco-decomp} 말미
plug-in 사슬(식~\eqref{eq:lco-plugin})의 $\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)=N_A\,\partial S_e/\partial x$
를 더하는 한 줄(식~\eqref{eq:lco-decomp}). \textbf{★단위 주의} — forward 슬롯 $\Delta S_{\rxn,j}$ 는
J/(mol\,K) 라, 자리당 식~\eqref{eq:dSe}(자리당 엔트로피 차원 $k_B$)가 아니라 \emph{$N_A$ 를 곱한} 몰당
식~\eqref{eq:dSemolar} 를 넣어야 한다($N_A$ 배 누락 시 전자항이 $\sim10^{23}$ 배 과소). $g(E_F,x)$ 는
식~\eqref{eq:ggate} 의 게이트로, 초기값 3개를 피팅 인자로 노출.
\end{enumerate}
$\partial U_j/\partial T\leftarrow\Delta S_{\rxn,j}^\mathrm{cat}/F$ 의 경로(식~\eqref{eq:lco-dUdT})는 흑연과
동일하다 — 곧 ``파라미터 +1 항'' 외에 구조 변경이 없다. 이것이 ``흑연 forward 교과서가 LCO 양극까지 한 틀로
닫힌다''의 코드 측 증거이며, 본 챕터가 두 전극을 한 프레임으로 통합한 까닭이다.
```

**원 줄글 대비**: 원문(L1768-1792)은 MSMR 대응표(f=-σ_d 등)를 서술하고 "구조가 동형"이라 결론지었으나
동형성을 실제 대수로 끝까지 닫지 않았다 — $\hat x_j$ 가 $\xi_{\eq,j}$ 와 \emph{같다는 등식}과 그 미분이
`eq:eqpeak` 와 \emph{같다는 등식}이 명시적으로 유도되지 않은 채 "구조 동형"이라는 정성 진술로 남아 있었다
(V1010 STYLE_REPORT "변환 사슬 미폐쇄" 판정과 부합). 신규 (a)-(d)는 정규화$\to$대응대입$\to$항등식 확인
$\to$미분까지 닫아 `eq:lco-msmrid`(신설)로 못박는다. (i)(ii) 항목 서술은 원문과 사실상 동일(단위 주의 문장
불변) — (ii)만 새 plug-in 박스(`eq:lco-plugin`, §5)를 명시적으로 가리키도록 다리를 놓았다.

**논리 감사(재유도 근거)**:
- *부호*: $f=-\sigma_d$ 대응이 원문 그대로 유지되고, 그 대응을 대입한 결과가 정확히 `eq:xieq` 와 부호까지
  일치(대수 재계산 확인, 어긋남 없음).
- *차원*: $\hat x_j,\xi_{\eq,j}$ 모두 무차원, $\dd x_j/\dd U$ 는 $Q_j$[C]$\times$무차원/$w_j$[V] = C/V — 미분
  용량 차원, `eq:eqpeak` 와 일치.
- *극한/특수해*: $\hat x_j\equiv\xi_{\eq,j}$ 항등식이 모든 $U,T$ 에서 성립(치환일 뿐 근사 아님) — 이는
  "동형"이 근사가 아니라 \emph{엄밀한 재표기}임을 확정한다(원문의 "구조가 동형"이라는 다소 약한 진술을 "항등"
  으로 격상 — 물리·수치는 불변, 진술의 엄밀도만 강화).
- *결함 탐색 결과*: 이 절의 재유도에서 새로운 물리 결함은 발견되지 않았다 — 원문의 정성적 주장이 대수적으로
  정확히 성립함을 확인(폐쇄 자체가 목적이었고, 폐쇄 결과가 기존 결론과 완전히 일치).

---

## 7. 신설 라벨 목록 + 충돌 검증(전수 grep 근거, §0)

| 라벨 | 절 | 위치 | 충돌 검증 |
|---|---|---|---|
| `eq:lco-jset` | center (a) | 신설 | 전수 grep(§0) 결과 기존 2개(`eq:lco-dUdT`,`eq:lco-decomp`) 외 없음 |
| `eq:lco-dUdT` | center (d) | **재사용(필수)** | 원문 L487 그대로, 6곳 `\eqref` 유지(§0) |
| `eq:lco-gxi` | hys (a) | 신설 | 상동 |
| `eq:lco-gpp` | hys (b) | 신설 | 상동 |
| `eq:lco-spinodal` | hys (b) | 신설 | 상동 |
| `eq:lco-Veq` | hys (c) | 신설 | 상동 |
| `eq:lco-dUhys` | hys (d) | 신설 | 상동 |
| `eq:lco-Ubranch` | hys (d) | 신설 | 상동 |
| `eq:lco-mit` | hys T1 | 신설 | 상동 |
| `eq:lco-dope` | hys 도핑 | 신설 | 상동 |
| `eq:lco-peaksum` | peak (d) | 신설 | 상동 |
| `eq:lco-plugin` | plug-in (d) | 신설 | 상동 |
| `eq:lco-msmrid` | MSMR (d) | 신설 | 상동 |
| `eq:lco-decomp` | decomp (d) | **재사용(필수)** | 원문 L1723 그대로, 9곳 `\eqref` 유지(§0) |

신설 12개 + 재사용 2개 = 14개 전부 `eq:lco-*` 프리픽스. finalizer 는 번호를 조정해도 되나 `eq:lco-dUdT`·
`eq:lco-decomp` 재사용만은 불변(합계 15곳 다운스트림 `\eqref` load-bearing).

---

## 8. 갈래 2 — H-2 정정문안 (`graphite_ica_ch2_v1.0.12.tex`)

### 8.1 위치 A: `ssec:logistic` 키박스(실측 L161–166, 교체)

**근거**: FABLE_REAUDIT_C4_note §2 CRITICAL — §logistic 이 "$w=n_jRT/F$ 임의 모수 아님"을 무한정 단정, 파생
C(§ssec:weff, L540-569)는 이미 단상/두-상 이중지위로 갈라놓아 \emph{같은 챕터 안에서} 모순.

**독립 재유도 확인(추가 근거)**: `eq:Z1`(L123-127)은 \emph{비상호작용 단일 자리} 대정준 분배함수
$Z_1=1+e^{-\beta(\varepsilon_0-\mu)}$ 다 — 상호작용 모수 $\Omega$ 가 이 식 어디에도 없다. $\Omega$ 가 도입되는
곳은 §ssec:BW(식~\eqref{eq:BW}, L183-186)의 \emph{다자리 평균장} 자유에너지이며, 그로부터 나오는 등온선
(`eq:Veq_BW`, L191)이 $\Omega>2RT$ 에서 비단조가 되어 상분리를 만든다(§ssec:BW L195-203). 곧 `eq:Z1` 은
구성상 $\Omega=0$(단상) 극한만 담는 식이라, 이 식 하나로 "임의 모수가 아니다"를 $\Omega>2RT$ 두-상까지
정당화하는 것은 \emph{식 자체의 적용 범위를 벗어난 주장}이다 — 이는 파생 C 의 broadening 논거(top-down: 실측
폭의 기원 분석)와는 \emph{독립적인 경로}(bottom-up: `eq:Z1` 의 구성 범위 분석)로 같은 결론(단상 한정)에
도달하는 교차검증이다.

**교체 텍스트**:
```latex
\begin{keybox}
Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라 \emph{격자기체 점유 분포의 여집합}(탈리튬화
진행률 $=1-\theta$)이다. \textbf{★단상 한정(H-2).} 아래 진술은 \emph{단상}($\Omega_j\le2RT$, 균질 고용체)에
한정된다 — logistic 폭 $w=RT/F$ 는(자리당 $n_j{=}1$ 기준; 전이별 유효 폭 $w_j=n_jRT/F$ 는 \S\ref{sec:revheat}
$\cdot$코드 \texttt{func\_w}) 이 영역에서 임의 모수가 아니라 단일 자리 2-상태 분배함수~\eqref{eq:Z1} 가 정하는
분포의 열적 폭이며, 이는 \emph{검증 가능한 평형 예측}이다(Ch1 \S\ref{sec:width} 폭 이중지위의 단상 측과 정합).
\textbf{두-상($\Omega_j>2RT$, 상분리 — 흑연 staging 전이가 여기 속함, \S\ref{ssec:weff} 파생 C)에서는 같은
결론이 성립하지 않는다}: 식~\eqref{eq:Z1} 은 애초에 \emph{비상호작용 단일 자리}(상호작용 모수 $\Omega$ 부재)
분배함수라 $\Omega>2RT$ 의 상분리 물리를 담지 않으므로, 이 식으로 두-상 폭까지 ``임의 모수 아님''이라 단정하는
것은 근거식의 적용 범위를 벗어난다. 그 영역의 $w_j$ 는 \S\ref{ssec:weff}$\cdot$Ch1 \S\ref{sec:broadening} 가
정하는 \emph{현상학적 자유 피팅 파라미터}다 — 코드 \texttt{func\_w} 가 두 경우 모두에 \emph{같은 함수형}을
계산상 쓰는 것은 구현의 편의(피팅 자유도를 $n_j$ 하나로 통일)이지, 두-상에서도 이 절의 열적-폭 \emph{유도}가
성립한다는 뜻이 \emph{아니다}(파생 A 수치검증의 전제 — \S\ref{ssec:overlap} 참조). ★표기: $\theta=$ Li
점유율(만충서 1), $\xi=1-\theta=$ 탈리튬화 진행률(희박서 1); 둘은 같은 점유 분포의 두 이름이다. Chapter 2 는
이 분포를 결론이 아니라 출발점으로 삼아 엔트로피를 쌓는다.
\end{keybox}
```

### 8.2 위치 B: 파생 A `srcbox`(실측 L485–496, 말미에 문장 추가 — 전면 교체 아님)

**근거**: "파생 A 수치검증의 전제(현행 코드 w=n_jRT/F 강제) 명시" — 파생 A 는 4-전이 흑연 staging 파라미터로
검증했는데 그 중 2개(2L→2·2→1)는 두-상이다. 이 검증이 확인하는 것은 "코드가 실제로 계산하는 함수형을 놓고
유한차분과 해석적 미분이 서로 정합한다"는 \emph{구현 자기정합성}이지, "그 함수형(n_jRT/F)이 두-상에서 물리적
으로 옳다"는 \emph{독립 검증}이 아니다 — 후자는 파생 C 의 몫이다.

**추가 텍스트**(기존 srcbox 마지막 문장 "곧 ... 자동 생성된다." 뒤에 신설 문단으로 삽입, 기존 문장은 무수정):
```latex
\textbf{★전제 명시(H-2).} 이 검증은 코드가 \emph{실제로 계산하는} $w_j(T)=n_jRT/F$ 함수형(전이 종류 무관하게
강제)을 전제로 유한차분과 해석적 미분의 \emph{내부 정합}(같은 함수형을 미분해도 같은 답이 나오는가)을 확인한
것이다 — 두-상 전이(그래파이트 staging 4건 중 2건, $2\mathrm L\!\to\!2\cdot2\!\to\!1$)에 대해서도 $w_j$ 가
\emph{이 함수형으로 강제}되어 있다는 \emph{구현 전제} 위에서 성립하는 자기정합성 검증이지, $n_jRT/F$ 가
두-상의 \emph{물리적으로 옳은} 평형 폭임을 독립적으로 입증하는 것은 \emph{아니다}(그 지위 판정은
\S\ref{ssec:weff} 파생 C 가 별도로 맡는다 — \S\ref{ssec:logistic} 키박스의 두-상 한정과 정합).
```

**원 줄글 대비**: 두 위치 모두 물리·부호·수치(0.47/1.49 등 ch1 값과 무관, ch2 는 이 수치를 다루지 않음)
불변 — H-1(BW 부호)·M-8(파생D)·M-9(고온코너)는 이미 v1.0.12 에 반영되어 있어 \emph{손대지 않았다}(§0 확인).
키박스는 "무한정 단정"에서 "단상 한정 + 두-상 예외 명시"로, srcbox 는 "검증 결과만 서술"에서 "검증 결과 +
그 전제의 인식론적 지위 명시"로 바뀐다 — 둘 다 \emph{추가 설명}이지 기존 결론(PASS, 175점 부동소수점 일치
등)의 \emph{철회나 수치 변경이 아니다}.

**논리 감사(재유도 근거)**:
- *내적 정합*: 키박스(신)와 파생 C(L540-569, 무수정)가 이제 같은 언어(단상=평형예측, 두-상=현상학적 피팅)를
  쓴다 — 챕터 내부 모순 해소, 재확인 완료.
- *Ch1 정합*: 신규 키박스 문구 "검증 가능한 평형 예측"·"현상학적 자유 피팅 파라미터"가 Ch1 §width(L741-746)
  의 표현과 축자적으로 일치하도록 맞춤 — 챕터간 용어 통일(사용자 요구 "Ch1 이중지위와 챕터 간 정합" 충족).
  Ch1 파일은 \emph{무수정}(이 문건은 Ch2 supplement 만 생성).
- *독립 교차검증*: `eq:Z1` 의 비상호작용 구성(bottom-up)과 파생 C 의 broadening 논거(top-down)가 같은
  한정("단상에서만 유효")에 수렴 — 두 경로가 일치하므로 정정 방향의 신뢰도가 단일 논거보다 높다.
  이는 FABLE_REAUDIT_C4_note 의 지적(top-down 만 제시)에 bottom-up 논거를 추가한 것으로, **신규 발견**은
  아니고 기존 결론의 \emph{독립 재확인}이다.
- *물리 불변*: eq:Veq_BW·파생 D 선형화 조건·고온 코너 한정 등 이미 존재하는 다른 부분은 일절 건드리지 않음
  (H-1/M-8/M-9 재작업 금지 확인, §0).

---

## 9. 5줄 요약

1. **수식화 커버**: LCO 6절(center·hys·peak·decomp·plug-in·MSMR) 전건 실측 L번호로 (a)(b)(c)(d) 사슬 완성 —
   center 는 이중경로 온도미분 교차검증, hys 는 spinodal 대입+대칭점 검산+슬롯분리박스, peak 는 3봉우리 합산박스
   (`eq:lco-peaksum` 신설), decomp 는 분배함수 인수분해 재유도(박스 자체는 무변경), plug-in 은 ξ→x→ΔS_e→ΔS_rxn→
   U(T)→dQ/dV 전체 사슬(`eq:lco-plugin` 신설), MSMR 은 대응대입→항등식(`eq:lco-msmrid`)→미분까지 폐쇄.
2. **논리결함 발견여부**: Branch 1(LCO 6절) 자체에서는 신규 물리 결함 미발견(재유도 결과 원문 결론과 전부
   정합) — §1·§4 에서 점검한 "스케일 다른 수치 혼합" 우려는 원문이 이미 "sanity"로 적절히 hedging, 결함 아님으로
   확인. Branch 2(H-2)의 결함은 기지(FABLE 감사 CRITICAL#2, 챕터 내부 모순) — 본 드래프트는 `eq:Z1` 의
   비상호작용 구성이라는 독립 bottom-up 논거로 그 정정 방향을 교차검증했다.
3. **물리 불변 확인**: 6절 전부 기존 결과식·부호·수치(0.47/1.49 config ΔS, +29/0/-5/-16, +80/-46, 6곳/9곳
   다운스트림 참조 등) 무변경 — `eq:lco-dUdT`·`eq:lco-decomp` 라벨 재사용, 신설 12개 라벨은 전수 grep 충돌 0.
   H-2 는 물리·수치 무변경, 인식론적 지위(단상/두-상 한정)만 명시화.
4. **최약점**: (i) plug-in 절 (a)의 $x(\xi_{\eq,\mathrm{T1}})$ 아핀 좌표 사상은 표에 이미 실린 두 끝점만
   쓴 \emph{예시}로 명확히 한정했으나, 다른 9개 경쟁 드래프트가 다른(또는 무) 사상을 제시할 경우 Fable
   master 의 조정이 필요하다 — 신뢰값 아님을 재차 강조.
   (ii) `eq:lco-peaksum`·`eq:lco-plugin`·`eq:lco-msmrid` 3개 신설 박스는 기존 결과의 \emph{조합/재표기}이지
   독립된 새 물리가 아니므로 finalizer 가 원치 않으면 인라인 문장으로 격하해도 내용 손실이 없다.
5. 전체적으로 본 드래프트는 "결과 불변 + 사슬 완성 + 두 독립 논거(교차검증)"를 원칙으로 삼았으며, 유일하게
   \emph{신규 텍스트로 실질 판단이 개입한 지점}은 plug-in 좌표 사상(§5 (a))과 H-2 키박스 문구(§8.1)이므로
   Fable master 는 이 두 곳을 우선 검토하기를 권한다.
