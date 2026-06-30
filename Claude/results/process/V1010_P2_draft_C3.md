# V1010 P2 Draft C3 — Ch1 교과서화 supplement

> 역할: Anode_Fit v1.0.10 P2 챕터1 9종 경쟁 드래프트 C3.  
> 범위: supplement 초안만 작성. 기존 Ch1 `.tex`, 코드, P1 result, research 원문 수정 없음.  
> 출력 목적: Ch1을 코드 플로우차트에 1:1로 대응하는 물리화학 교과서로 정련하기 위한 보완안.

## 0. 실제 검독 범위

| 구분 | 파일 | 실제 확인 범위 | 사용 방식 |
|---|---|---:|---|
| 작업 지시 | `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/p2_codex_C3.txt` | 전문 | 산출 형식·금지 사항·품질 기준 |
| 프로젝트 지침 | `D:/Projects/Project_Anode_Fit/CLAUDE.md`, `Codex/AGENTS.md` | 전문 | 작업 경계·전문 검독·Claude 출력 예외 확인 |
| 마스터·ledger | `Claude/plans/2026-07-01-v1010-code-doc-sync-bdd-fitting-plan.md`, `Claude/results/process/V1010_EXECUTION_LEDGER.md` | 전문 | P2 위치와 P1 앵커 확인 |
| 대상 Ch1 | `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` | 1-1866행 전문 | Ch1 절·식 번호 근거 |
| 코드 앵커 | `Claude/results/process/V1010_P1_code-audit_RESULT.md` | 1-445행 전문, 4분할 재확인 | 24심볼·12식·피팅 인벤토리 |
| broadening 설계 | `Claude/results/research/broadening_w_design.md` | 전문 | v3-v9 요소 통합 기준 |
| radius/origin 판정 | `Claude/results/research/radius/ORIGIN_VERDICT.md` | 전문 | size/PSD 배제와 apparent-U 재해석 |

## 1. Ch1 ↔ 코드 1:1 coverage 매트릭스

### 1.1 전체 판정

Ch1 v1.0.10은 코드의 주 물리 흐름 N0-N9를 대체로 따라간다. 핵심 식의 coverage는 높다. 특히 분극, 평형 중심, 정규용액 히스테리시스, logistic 점유, 평형 peak, 컷 affinity, `L_q -> L_V`, 인과 꼬리, 충전 격자 역전, 합산·역보간은 모두 절과 식 번호가 있다.

그러나 P1 기준 "코드 플로우차트 24심볼"로 보면 교과서 본문에 남은 gap이 있다. gap은 세 부류다.

1. 코드 구현 세부이나 Ch1에서 독자가 같은 코드를 짤 때 필요한 다리: 생성자 가드, `n` 우선순위, `equilibrium`의 T 스칼라 제한, `n_work` 해상도 의존, `L_V` 직접 지정 우회, silent-off 조건.
2. 코드에는 있으나 물리 본문에는 넣지 않아도 되는 engineering/dead surface: `_finite*`, `_build_seed_L_V`, `func_U_j_hys` dead helper, self-test.
3. Ch1에는 있으나 현재 P1 코드에는 없는 이론 선기술: LCO 양극, electronic entropy, MSMR 동형, LCO 전이표. 이는 과잉 오류가 아니라 P4 구현 예정의 이론 선기술이다.

### 1.2 코드 step별 매트릭스

| P1 코드 step / 심볼 | 코드 물리 의미 | Ch1 대응 절·식 | coverage | 누락·과잉 판정 |
|---|---|---|---|---|
| `curve`, `_direction_to_sigma` | direction -> `sigma_d`, c-rate -> `|I|` | §1.1 `sec:notation`, 식 `eq:n0map`; §1.12 facade, 표 `tab:nodemap` | 충실 | direction 문자열 처리·오류 조건은 코드 표면으로만 남음. 본문에 1문장 bridge 권고. |
| `dqdv` N1 분극 | `V_n=V_app-sigma_d |I| R_n` | §1.2 `sec:pol`, 식 `eq:vn`; signcheck S8 | 충실 | 코드 line 표에서 P1은 L408, Ch1 표는 L412로 적혀 있어 line-number drift 가능. 식 대응은 충실. |
| 작업 격자 | padding, `n_work=max(2048,2|V_n|)`, `T_work` 보간 | §1.2, 식 `eq:vwork`; §1.12 재현 6단계 | 부분 | `n_work`가 꼬리/평형 분기 문턱 `nu Delta_grid`를 바꾸는 해상도 의존 bridge가 약함. |
| `func_U_j` | `U_j=(-dH+T dS)/F` | §1.3 `sec:center`, 식 `eq:Uj`; LCO §`sec:lco-center` | 충실 | 없음. |
| `func_U_j_hys` | 원형 히스 helper, 미호출 dead code | Ch1 직접 대응 없음 | 코드-only | Ch1에 넣을 필요는 낮지만, supplement/appendix에 "legacy uncalled helper"로 구분 필요. |
| `func_dU_hys` | spinodal gap `Delta U_hys` | §1.4 `sec:hys`, 식 `eq:spinodal`, `eq:dUhys`; signcheck S4 | 충실 | 없음. |
| `func_U_branch` | `U_j^d=U_j+1/2 sigma h_eta gamma Delta U_hys` | §1.4, 식 `eq:Ubranch`, `eq:center`; signcheck S4 | 충실 | 코드 gate는 `gamma != 0 and Omega > 0`; 물리 gap은 `Omega <= 2RT -> 0`. 둘의 관계를 한 문장 더 명시 권고. |
| `func_w`, `_n_factor`, `_width` | `w=nRT/F`, `n` 우선, `w` fallback | §1.5 `sec:width`, 식 `eq:wbase`; §1.7 broadening | 부분+중요 bridge 있음 | Ch1은 `n=1`이면 `w` fallback 비활성임을 말하지만, 코드 우선순위와 fitting implication을 표 `tab:inputs` 옆에 더 또렷하게 둘 필요. |
| `func_ksi_eq` | logistic 점유 | §1.5, 식 `eq:xieq`; §1.5 분포 관점 `eq:fermifn`; signcheck S2 | 충실 | 없음. |
| `equilibrium` | 평형 peak only, 히스·동역학 없음, T 스칼라 | §1.6 `sec:eqpeak`, 식 `eq:eqpeak`; §1.12 facade | 부분 | `equilibrium`이 T 배열 미지원이라는 구현 제한이 Ch1에 없음. P1 보완 2를 Ch1 appendix 또는 codebox로 추가. |
| broadening/w 이중지위 | 단상 `w`=평형 예측, 두-상 `w`=현상학적 폭 | §1.5, §1.7 `sec:broadening`, 식 `eq:ensavg`; broadening 설계 전문 | 충실 | ORIGIN_VERDICT와 최종 Ch1이 일부 다름: ORIGIN은 size kinetic 분산을 강하게 지지했지만, 최종 설계는 사용자 결정으로 size/PSD를 제외하고 non-size `eta` 분포만 남김. Ch1의 현재 판단을 유지. |
| `func_chi_d` | 방전 `chi`, 충전 `1-chi` | §1.8 `sec:lag`, 식 `eq:chid`; signcheck S5 | 충실 | 피팅 bound `[0,1]`는 수식에는 있으나 코드 가드 부재가 matrix에 별도 표시되어야 함. |
| `func_dH_a_eff` | `dH_a_eff=dH_a-chi_d Omega` | §1.8, 식 `eq:dHeff`; signcheck S5 | 충실 | 없음. |
| `_resolve_lag_length` A | `A=min(z_cut n RT, A_cap RT)` | §1.8, 식 `eq:Acut`; P1 z_cut docstring 정정 | 충실 | `abs(n)` 사용과 `n<=0` 피팅 가드 부재를 codebox로 분리 권고. |
| `func_L_q` | Eyring + detailed balance -> `L_q` | §1.8, 식 `eq:Lq`, `eq:kuniv`, `eq:Lqfull` | 충실 | 없음. |
| `L_V=|dV/dq| L_q` | 전압축 지연 길이 | §1.8, 식 `eq:LV` | 충실 | `dVdq_qa` 누락 시 silent tail-off, 직접 `L_V` 지정 시 물리 파라미터 우회가 본문에 부족. |
| `_causal_lowpass` | 지수 기억, DC gain 1 | §1.9 `sec:tail`, 식 `eq:memory`, `eq:lowpass` | 충실 | DC gain=1과 면적보존을 더 직접 연결하면 코드 충실도 상승. |
| peak branch | 작은 `L_V`면 평형 peak, 그 외 꼬리 | §1.9, 식 `eq:branch` | 충실 | 문턱 진폭 불연속은 설명됨. 해상도 의존은 보강 필요. |
| 충전 격자 역전 | `lowpass(x[::-1])[::-1]` | §1.9, 식 `eq:reversal`; signcheck S7 | 충실 | 없음. |
| 합산·역보간 | `Cbg + sum Q_j peak_shape`, `np.interp` | §1.10 `sec:sum`, 식 `eq:sum`; §1.12 재현 6단계 | 충실 | `Cbg` callable finite 미검은 구현/피팅 주의로 별도 gap. |
| `GRAPHITE_STAGING_LIT` | 4전이 초기값 | §1.10, 표 `tab:staging`; §1.12 입력표 | 충실 | `w` fallback inert와 `n=1` 고정의 피팅상 의미를 표 주석으로 강화 권고. |
| `_build_seed_L_V` | seed diagnostic only | §1.12 표 `tab:inputs` seed 조건 | 부분 | seed가 dqdv 물리에 미사용이라는 distinction이 본문에 약함. |
| `_finite*`, `__init__` guards | fail-fast numeric guards | §1.12 표 `tab:inputs` | 부분 | 물리교과서 본문보다는 "구현 contract" 박스가 필요. |
| `__main__` self-test | guard/curve/hys/override 검증, 면적 assert 부재 | Ch1 부호 self-test §`sec:signcheck` 일부 | 부분 | 면적=Q assert 부재는 P4 테스트 후보. Ch1엔 "교재식 검산"으로 면적보존을 충분히 둠. |
| LCO `LCO_STAGING_LIT` | P4 예정 양극 전이 dict | §1.1 LCO map, 표 `tab:lco-staging`; §1.11-1.12 | 문건-only | 현재 코드에는 없음. 과잉이 아니라 P4 구현 예고. 파일 내에서 "현재 코드 미구현/P4" 표기를 더 명시해야 함. |
| LCO electronic entropy | Sommerfeld + MIT gate | §1.5+ `sec:lco-electronic`, 식 `eq:Se`, `eq:dSe`, `eq:dSemolar`, `eq:ggate`, `eq:dSegate` | 문건-only | 이론 선기술. 단위·부호·tier를 더 안정화해야 함. |
| 발열/q_rev | Ch2/P3 대상 | Ch1에는 직접 구현 없음 | 범위 밖 | 현재 코드도 없음. Ch1에서는 전자항이 Ch2 가역발열로 이어짐만 예고하면 충분. |

## 2. 누락 유도·다리 보완 초안

아래 문단들은 Ch1 본문에 직접 이식 가능한 supplement 초안이다. 원 Ch1 본문을 대체하지 않고, 각 절의 codebox 또는 짧은 subsection으로 끼워 넣는 형식을 가정한다.

### 2.1 구현 contract 박스 — 입력 가드와 실패 조건

삽입 위치 권고: §1.12 `전체 입력 인자와 기본값` 직후.

> **구현 contract.** 위 표의 기호는 물리식의 독립변수이지만, 코드는 이 독립변수가 수치적으로 유한하고 분모가 양수라는 조건을 먼저 검사한다. 온도 `T`, 용량 `Q_cell`, 폭 계수 `n_j`, 지연 길이에 들어가는 양의 분모는 `>0`이어야 하고, 전류 크기와 저항처럼 부호가 정해진 양은 `>=0`이어야 한다. 이 검사는 새 물리식이 아니라 식의 정의역을 보존하는 fail-fast 조건이다. 예를 들어 `w_j=n_jRT/F`에서 `n_j<=0`이면 폭이 0 또는 음수가 되어 `Q_j xi(1-xi)/w_j`가 발산하거나 음의 peak를 만든다. 따라서 피팅 wrapper는 `n_j>0`, `0<=chi<=1`, `dVdq_qa>0`인 동역학 전이, 유한한 `C_bg(V)`를 명시 constraint로 둔다.

이 박스는 P1의 F1-F4와 Ch1 입력표를 연결한다. 특히 "코드가 모두 guard한다"가 아니라 "코드 guard와 피팅 wrapper guard를 분리"해야 한다.

### 2.2 `n` 우선순위와 `w` fallback bridge

삽입 위치 권고: §1.5 `폭 w_j`의 이중지위 선언 직후 또는 표 `tab:staging` 주석.

식은 하나다.

\[
w_j=\frac{n_jRT}{F}.
\]

그러나 입력 dict에는 `n`과 `w`가 둘 다 있을 수 있다. 이때 코드의 우선순위는

\[
n_j=
\begin{cases}
\texttt{tr['n']} & \texttt{'n'}\in\texttt{tr},\\
\texttt{tr['w']}F/(RT) & \texttt{'n'}\notin\texttt{tr},\ \texttt{'w'}\in\texttt{tr},\\
1 & \text{otherwise}.
\end{cases}
\]

따라서 현재 `GRAPHITE_STAGING_LIT`처럼 `n=1.0`과 `w=0.020/0.016/0.014/0.012 V`가 함께 있으면 실제 폭은 `w` 값이 아니라 `RT/F=25.7 mV`이다. `w`는 `n` 키를 제거하거나 피팅 wrapper가 `n=wF/(RT)`로 변환할 때만 살아난다. 이 사실은 물리식의 변화가 아니라 입력 priority의 문제이며, two-phase 폭을 현상학적 자유 파라미터로 fit하려면 `n_j`를 직접 fit하거나 `w` 입력을 `n`으로 환산해 넣어야 한다.

### 2.3 `equilibrium`과 `dqdv`의 온도 인자 차이

삽입 위치 권고: §1.12 facade 설명 직후.

`dqdv`는 \(T\)가 스칼라면 \(T_\work\equiv T\), 배열이면 \(T(V_\app)\)를 \(V_\work\) 위로 보간한다. 반면 `equilibrium(V_n,T)`는 `T`를 양의 스칼라로 검사한 뒤 평형 peak만 합산한다. 따라서

\[
\mathrm{equilibrium}: T\in\mathbb R_+,\qquad
\mathrm{dqdv}: T\in\mathbb R_+\ \text{or}\ T(V_\app).
\]

이는 평형 열역학의 제한이 아니라 현재 helper API의 구현 제한이다. 비등온 평형 기준선이 필요하면 `dqdv`의 \(T_\work\) 보간 경로와 같은 방식으로 `equilibrium`을 확장해야 한다. 현 Ch1 본문에서는 비등온 식이 \(U_j(T_\work)\)로 닫히므로, "식은 배열 T에 대응하지만 `equilibrium` convenience method는 스칼라 T만 받는다"라고 구분한다.

### 2.4 `L_V` 분기 문턱의 해상도 의존

삽입 위치 권고: §1.9 `peak 모양`의 식 `eq:branch` 직후.

식 `eq:branch`의 문턱은 \(L_{V,j}<\nu\Delta_\mathrm{grid}\)이다. 그런데 \(\Delta_\mathrm{grid}\)는 물리 상수가 아니라 작업 격자의 수치 간격이다.

\[
\Delta_\mathrm{grid}
\simeq
\frac{(1+p_\mathrm{lo}+p_\mathrm{hi})(\max V_n-\min V_n)}
{\max(n_{\work,\min},2N_V)-1}.
\]

따라서 같은 물리 \(L_{V,j}\)라도 사용자가 넣은 전압 점 수 \(N_V\)가 커지면 \(\Delta_\mathrm{grid}\)가 작아지고, 문턱 \(\nu\Delta_\mathrm{grid}\)도 작아진다. 어떤 grid에서는 평형 branch로 접히던 작은 꼬리가, 더 촘촘한 grid에서는 꼬리 branch로 살아날 수 있다. 이는 물리 모델의 새 자유도가 아니라 수치 branch의 해상도 의존이다. 피팅 비교에서는 전압 격자와 `n_work_min`, `min_lag_grid_steps`를 고정하거나, branch 전환 전후의 면적과 peak 높이를 회귀 gate로 확인해야 한다.

### 2.5 `L_V` 직접 지정과 silent-off 조건

삽입 위치 권고: §1.8 `L_q` 평가와 전압축 환산 뒤.

동역학 지연 길이 resolver의 실제 우선순위는 다음이다.

\[
L_{V,j}=
\begin{cases}
\texttt{tr['L\_V']} & \texttt{'L\_V'}\ \text{직접 지정},\\
0 & |I|\le0\ \text{or}\ \texttt{'dH\_a'}\notin\texttt{tr},\\
|\dd V/\dd q|_{q_a}\,L_{q,j} & \text{otherwise}.
\end{cases}
\]

따라서 `L_V`를 직접 지정하면 \(\Delta H_a,\Delta S_a,\chi_d,\Omega,z_\mathrm{cut},dVdq_qa\) 경로를 모두 우회한다. 이것은 초벌 피팅에서 꼬리 길이를 안정적으로 관측하기 위한 유용한 우회로지만, 물리 파라미터를 동시에 fit하면 과식별을 만든다. 또한 `dH_a`가 없으면 \(L_V=0\)으로 떨어지고, `dVdq_qa`가 0 또는 누락이면 계산된 \(L_V\)도 0이므로 꼬리가 조용히 꺼진다. "동역학 전이"로 선언한 항은 `dH_a`와 양의 `dVdq_qa`를 함께 가져야 한다.

### 2.6 면적보존 다리 — lowpass DC gain과 peak 면적

삽입 위치 권고: §1.9 또는 §1.10 합산 직전.

평형 branch에서 면적은 치환적분으로 닫힌다.

\[
\int_{-\infty}^{\infty}Q_j\frac{\xi_\eq(1-\xi_\eq)}{w_j}\,\dd V
=Q_j\int_0^1 \dd\xi=Q_j.
\]

꼬리 branch도 같은 DC 면적을 목표로 한다. `_causal_lowpass`는 계수 \([1-\rho]/[1,-\rho]\)의 1차 필터이고,

\[
H(1)=\frac{1-\rho}{1-\rho}=1
\]

이므로 충분히 넓은 격자에서 상수/저주파 성분을 보존한다. 따라서 \((\xi_\eq-\xi_\mathrm{lag})/L_V\)는 peak를 뒤로 늘리되, 잘린 경계가 없으면 전이 총량 \(Q_j\)를 보존한다. 실제 finite grid에서는 꼬리가 전압창 밖으로 나가면 면적 손실이 생기므로 `grid_pad_lo/hi`와 전압 범위가 면적 gate의 일부가 된다.

### 2.7 legacy/dead helper의 위치

삽입 위치 권고: 본문이 아니라 supplement appendix.

`func_U_j_hys`는 원형 보존을 위해 남아 있지만 현재 `dqdv`는 이를 호출하지 않고 `func_dU_hys`와 `func_U_branch`를 쓴다. 따라서 교과서 본문은 `eq:dUhys`, `eq:Ubranch`만 따라가면 된다. 단, 외부 사용자가 `func_U_j_hys`를 직접 호출하면 인자명 `s`와 실제 경로의 `sigma_d`가 섞일 수 있고, `last_eta`, `last_rest`, `partial_hys=1`은 현재 물리 경로에 영향을 주지 않는다. 이 항목은 본문 수식의 누락이 아니라 legacy API 주의다.

## 3. v3-v9 교과서 요소 통합 권고

### 3.1 현재 유지해야 할 spine

Ch1의 현재 spine은 유지한다.

\[
\mathrm{N0}\to\mathrm{N1}\to\mathrm{N2}\to\mathrm{N3}\to\mathrm{N4/N5}\to
\mathrm{N6}\to\mathrm{N7}\to\mathrm{N8}\to\mathrm{N9}.
\]

이 순서가 P1 코드 flow와 가장 잘 맞는다. 보강은 새 장을 만들지 말고 각 노드의 codebox/verifybox로 넣는다. 특히 N7-N8의 `A -> chi_d -> dH_a_eff -> L_q -> L_V -> lowpass` 사슬은 현재도 교과서형 유도가 좋으므로, 위의 silent-off·해상도·면적보존 bridge만 추가하면 된다.

### 3.2 broadening/w 설계의 최종 정렬

`broadening_w_design.md`와 Ch1 최종본 사이의 중요한 차이를 명시해야 한다. 초기 설계에는 "집합 다입자 통계역학"을 `rho(U_j)` 전이전위 분포로 쓰는 문장이 있었고, `ORIGIN_VERDICT.md`에는 size kinetic 분산이 강한 기작으로 정리되어 있다. 그러나 Ch1 v1.0.10의 최종 정책은 다음으로 정렬되어 있다.

1. dilute 및 4L-3L: 평형 단일입자 자체가 logistic/Frumkin형 종이다.
2. LiC12 및 LiC6 two-phase: 평형 plateau 내부는 delta에 가깝고, 실측 폭은 유한율속 꼬리, plateau edge의 RT/F 폭, non-size apparent-U 분포가 만든다.
3. 분포하는 것은 평형 \(U_j\)가 아니라 \(U_\app=U_j+\eta\)이다.
4. 입자 size/PSD convolution은 본 Ch1 모델에 넣지 않는다.
5. \(\rho(U_\app)\) 역산은 ill-posed이므로 하지 않는다.

이 정렬이 가장 안전하다. ORIGIN_VERDICT의 size kinetic 기작은 "물리적으로 가능한 중요 기작"으로는 남지만, 사용자 결정에 따라 이번 Ch1의 모델·문건 범위에서는 제외된 것이다. 따라서 최종 Ch1은 size 기작을 삭제한 것이 아니라 "본 장의 현상학적 폭 \(w_j\)가 흡수하는 외부 요인으로도 명시하지 않고, 후속/범위 밖으로 둔다"라고 정돈해야 한다.

## 4. LCO 이론 정련안

### 4.1 현재 Ch1 LCO 이론의 타당한 골격

현재 Ch1의 LCO 통합은 방향이 맞다.

1. 삽입형 전극 공통 골격: \(U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F\), \(w_j=n_jRT/F\), \(\xi_\eq\) logistic, \(Q_j\xi(1-\xi)/w\) peak는 전극을 가리지 않는다.
2. LCO는 전이 파라미터를 양극 영역으로 바꾸는 두 번째 전극이며, 하프셀 기준 부호를 유지한다.
3. T1 MIT에는 흑연에 없는 electronic entropy가 들어가고, Sommerfeld 식 \(S_e=(\pi^2/3)k_B^2Tg(E_F)\)로 함수형을 닫는다.
4. \(g(E_F,x)\)의 연속 곡선은 1차 문헌 anchor가 부족하므로 MIT-logistic gate를 모델 가정으로 두고 fit한다.
5. 코드 구현은 현재 P1 코드에 없고 P4에서 수행한다.

따라서 "LCO가 코드에 없으니 Ch1에서 삭제"가 아니라 "P4 구현 예정 이론이므로 현재 코드 coverage 표에서 planned extension으로 분리"가 맞다.

### 4.2 LCO 전자 엔트로피 단위 사슬 보강

현재 식 `eq:dSe`와 `eq:dSemolar`는 핵심을 담고 있지만, 독자가 단위에서 멈추지 않도록 eV-to-J 환산을 식 안에 한 번 더 드러내는 편이 좋다. \(g\)를 \(\mathrm{states/eV/atom}\)으로 둘 때,

\[
S_e^\mathrm{atom}(T,x)
=\frac{\pi^2}{3}k_B^2T\,g_J(E_F,x),
\qquad
g_J(E_F,x)=\frac{g_{\mathrm{eV}}(E_F,x)}{e_\mathrm{V}},
\]

여기서 \(e_\mathrm{V}=1.602176634\times10^{-19}\,\mathrm{J/eV}\)이고 \(g_J\)의 단위는 \(\mathrm{states/J/atom}\)이다. 삽입 기준 부분몰 전자 엔트로피는

\[
\Delta S_{e}^{\mathrm{mol}}(x,T)
=N_A\frac{\partial S_e^\mathrm{atom}}{\partial x}\Big|_T
=\frac{\pi^2}{3}Rk_BT\,
\frac{1}{e_\mathrm{V}}\,
\frac{\partial g_{\mathrm{eV}}(E_F,x)}{\partial x}.
\]

이 식을 쓰면 \(N_Ak_B=R\), \(k_BT/e_\mathrm{V}\)가 eV 단위 열에너지로 바뀌어 단위가 바로 닫힌다.

MIT gate를

\[
g_{\mathrm{eV}}(E_F,x)=g_{\max}\{1-\sigma[(x-x_\mathrm{MIT})/\Delta x_\mathrm{MIT}]\}
\]

로 두면

\[
\frac{\partial g_{\mathrm{eV}}}{\partial x}
=-\frac{g_{\max}}{\Delta x_\mathrm{MIT}}\sigma(1-\sigma)<0
\]

이고, 따라서 삽입 기준

\[
\boxed{
\Delta S_{e}^{\mathrm{mol}}(x,T)
=-\frac{\pi^2}{3}R
\left(\frac{k_BT}{e_\mathrm{V}}\right)
\frac{g_{\max}}{\Delta x_\mathrm{MIT}}
\sigma(1-\sigma)<0
}
\]

이다. 이 닫힌식은 현재 `eq:dSegate`의 단위 보강판이다. 탈리튬화 기준 방출량은 \(-\Delta S_e^\mathrm{mol}>0\)로 그리면 된다.

### 4.3 LCO 전자항이 \(U(T)\)에 들어가는 방식

Ch1은 이미 "전자항은 \(\Delta S_e\propto T\), 따라서 \(\partial U/\partial T\)가 \(T\)-선형이고 \(U\) 이동은 \(T^2\)"라고 적는다. 이를 한 식으로 보강하면 좋다.

삽입 기준 총 엔트로피를

\[
\Delta S_{\rxn,1}^\mathrm{cat}(T)
=\Delta S_0^\mathrm{config}+\Delta S_0^\mathrm{vib}
+a_eT,
\]

\[
a_e(x)=
-\frac{\pi^2}{3}R
\frac{k_B}{e_\mathrm{V}}
\frac{g_{\max}}{\Delta x_\mathrm{MIT}}\sigma(1-\sigma)
\]

로 두면,

\[
\frac{\partial U_1}{\partial T}
=\frac{\Delta S_0^\mathrm{config}+\Delta S_0^\mathrm{vib}}{F}
+\frac{a_e}{F}T.
\]

따라서 기준온도 \(T_0\)에서의 중심을 \(U_1(T_0)\)로 놓을 때

\[
U_1(T)=U_1(T_0)
+\frac{\Delta S_0^\mathrm{config}+\Delta S_0^\mathrm{vib}}{F}(T-T_0)
+\frac{a_e}{2F}(T^2-T_0^2).
\]

이 식은 P4 코드 구현의 직접 설계 사양이 된다. 즉 `func_U_j`의 단순 선형 \(T\Delta S\) 슬롯만으로는 \(\Delta S_e\propto T\)일 때 \(T^2\) 누적을 정확히 표현하려면 \(U_j(T)\) 계산을 확장해야 한다. 단, P2에서는 이론 보강만 하고 코드 변경은 P4로 예고한다.

### 4.4 LCO dQ/dV peak 교과서 문단

삽입 위치 권고: §1.6 `LCO dQ/dV peak`.

LCO 양극의 하프셀 dQ/dV는 흑연과 같은 미분 규칙으로 닫힌다.

\[
\left(\frac{\dd Q}{\dd V}\right)_j^\eq
=Q_j\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j},
\qquad
\xi_{\eq,j}=\frac{1}{1+\exp[-\sigma_d(V-U_j^d)/w_j]}.
\]

다른 것은 \(U_j\)의 위치와 \(\Delta S_{\rxn,j}\)의 내용이다. 흑연은 \(0.085-0.210\,\mathrm{V}\) 영역의 staging 전이를 쓰고, LCO는 \(3.90\), \(4.05\), \(4.17-4.20\,\mathrm{V}\) 근방 전이를 쓴다. T1은 MIT이므로

\[
\Delta S_{\rxn,1}^\mathrm{cat}
=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}+\Delta S_{e,1}^\mathrm{mol}(x,T)
\]

가 되고, T2/T3는 electronic gate를 끄고 order-disorder config/vib 중심값만 쓴다. 이 차이가 dQ/dV에서 보이는 신호는 T1 peak의 온도 이동률이다. \(T\)를 바꾸었을 때 T1만 \(\partial U/\partial T\)의 기울기가 \(T\)-의존을 갖고, T2/T3는 상수 \(\Delta S/F\)에 가까운 선형 이동을 보인다. 이 비교가 LCO electronic entropy의 관측 gate다.

### 4.5 P4 구현 예고 문구

Ch1의 LCO 절마다 다음 boundary 문장을 넣어야 과잉 판정이 사라진다.

> 현재 `Anode_Fit_v1.0.10.py`는 흑연 음극 전용 forward 모델이며, `LCO_STAGING_LIT`, cathode branch, electronic entropy, heat term은 아직 구현되어 있지 않다. 본 절은 P4 코드 개정에서 구현할 이론 사양을 먼저 고정하는 문건 선행 단계다. 따라서 현재 코드와의 1:1 coverage 표에서는 LCO 항을 "planned extension"으로 분리하고, P4에서 파라미터 dict와 \(U_j(T,x)\) 평가 경로를 추가한 뒤 다시 1:1 검수한다.

## 5. 부호·차원·극한 적대 검산

| 항목 | 검산 | 판정 |
|---|---|---|
| \(w=nRT/F\) | \(RT/F=[J/mol]/[C/mol]=V\), \(n\) 무차원 | 통과 |
| \(U=(-\Delta H+T\Delta S)/F\) | \([J/mol]/[C/mol]=V\), \(\partial U/\partial T=\Delta S/F\) | 통과 |
| logistic | \(\sigma_d(V-U)/w\) 무차원, \(\xi\in(0,1)\) | 통과 |
| 평형 peak | \(Q\,\xi(1-\xi)/w=[C]/[V]=C/V\), 면적 \(Q\) | 통과 |
| 히스 gap | \((2/F)(\Omega u-2RT\operatorname{artanh}u)\), \(J/mol\) -> V | 통과 |
| spinodal 극한 | \(\Omega\le2RT\Rightarrow u\) 비실수, 코드·문건 모두 gap 0 | 통과 |
| `gamma=0` 또는 `Omega=0` | center \(=U_j\), 분기 없음 | 통과 |
| \(L_q\) | \(T_*=(I/Q)h/k_B\)는 K, 모든 log 인자 무차원 | 통과 |
| \(L_V\) | \(|dV/dq|L_q\)는 V, 꼬리 peak는 \(1/V\) | 통과 |
| 충전 역전 | 시간 진행이 \(V\downarrow\)라 grid reverse 필요 | 통과 |
| LCO \(\Delta S_e^\mathrm{mol}\) | \(R(k_BT/eV)g\) -> J/(mol K) | 보강식 적용 시 통과 |
| LCO 부호 | 삽입 \(x\uparrow\): metal -> insulator, \(g\downarrow\), \(\partial g/\partial x<0\), \(\Delta S_e<0\) | 통과 |

## 6. 추가 후보

실제 수정은 하지 않았고, master 체리픽 단계 후보로만 남긴다.

| 후보 | 위치 | 이유 | 변경 종류 |
|---|---|---|---|
| 구현 contract 박스 추가 | §1.12 `tab:inputs` 뒤 | P1 F1-F4를 Ch1 입력 정의역과 연결 | 문건 보강 |
| `n`/`w` 우선순위 수식 추가 | §1.5 또는 `tab:staging` 주석 | 현재 `w` fallback inert 오독 차단 | 문건 보강 |
| `equilibrium` T 스칼라 제한 표기 | §1.12 facade | 식과 helper API의 차이 명시 | 문건 보강 |
| branch threshold 해상도 의존 추가 | §1.9 `eq:branch` 뒤 | P1 보완 3 반영 | 문건 보강 |
| `L_V` 직접 지정/silent-off priority 추가 | §1.8 `eq:LV` 뒤 | 피팅 과식별과 silent tail-off 방지 | 문건 보강 |
| lowpass DC gain -> 면적보존 bridge | §1.9 또는 §1.10 | 코드 `_causal_lowpass`와 면적보존 연결 강화 | 문건 보강 |
| LCO 전자항 단위 보강식 | §1.5+ `sec:lco-electronic` | eV/J, per atom/mol 혼동 차단 | 문건 보강 |
| LCO \(U(T)\)의 \(T^2\) 누적식 | §1.11 또는 §1.12 | P4 구현 사양으로 직접 사용 가능 | 문건 보강 |
| P4 구현 예고 문장 | LCO 각 절 첫/끝 | 현재 코드 부재와 이론 선기술 경계 명확화 | 문건 보강 |

## 7. 최종 판정

확정:
- Ch1 v1.0.10은 P1의 주 물리식 12개와 N0-N9 코드 spine을 대부분 충실히 설명한다.
- 현재 가장 중요한 보완은 새 물리식이 아니라 code contract와 fitting-practical bridge다.
- broadening/w 이중지위는 Ch1 최종본 기준으로 이미 강하게 정리되어 있으며, size/PSD 기계장치는 이번 Ch1 범위 밖이다.
- LCO 이론은 현재 코드에는 없는 planned extension이나, P2에서 문건 선행으로 정련하는 것이 마스터 계획과 일치한다.

미결:
- LCO MIT gate의 \(g(E_F,x)\) 연속 곡선은 문헌 anchor 한 점과 물리 가정으로 둔 피팅 대상이다.
- LCO \(U_j(T,x)\)의 \(T^2\) 누적을 P4 코드에서 `func_U_j` 확장으로 둘지, LCO 전용 center evaluator로 둘지는 P4 설계 결정이다.
- `equilibrium`의 배열 T 지원 여부와 `n<=0`, `chi` bound, `dVdq_qa` schema guard는 P4 코드 개정 또는 fitting wrapper에서 결정해야 한다.

근거 미발견:
- 현재 P1 코드에는 LCO/cathode/electronic entropy/heat term 구현이 없다.
- Ch1 본문만으로는 `Cbg` callable의 finite 검증, `L_V` direct override와 물리 파라미터 동시 지정 정책이 완전히 닫히지 않는다.
- `Dahn 1995`는 non-size structural disorder의 존재 예시로는 쓸 수 있으나, inter-particle \(\rho(U_\app)\) 형상의 직접 정량 근거로는 부족하다.
