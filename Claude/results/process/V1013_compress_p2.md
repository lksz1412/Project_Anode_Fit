# v1.0.13 산문 압축 제안 — Part II 2절 (sec:lco-electronic · sec:lco-peak)

**대상 파일**: `D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.13\graphite_ica_ch1_v1.0.13.tex` (읽기 전용 정독, 미수정)
**대상 범위**: `\subsection{...}\label{sec:lco-electronic}`(L2223–2459, 내부 `\subsubsection` lco-why·lco-Se·lco-gate 포함) · `\subsection{...}\label{sec:lco-peak}`(L2461–2525)
**형식**: 원문(verbatim 인용) → 교체문 + 근거 + 물리 보존 선언. 모든 `\begin{equation}...\end{equation}` 블록은 **무변경**(라벨·본문 100% 보존) — 아래 어떤 교체문도 수식 환경 안쪽을 건드리지 않는다.

---

## 0. 방법 및 원칙 적용 방식

1. **물리 최우선**: 모든 수치(예: `−16` J/(mol·K), `0.085` V, `≈1.1 k_B`/atom, `≈0.18 k_B`/atom, `≈−46` J/(mol·K), `π²/3`, `13` e/eV/atom, `x_MIT≈0.85`, `Δx_MIT≈0.05` 등), 모든 부호(`<0`,`>0`, `∂g/∂x<0` 등), tier 라벨(tier A/B/C), 인용(`\cite{...}`)은 교체문에 **전량** 재기입한다. 어느 교체문도 수식·상수·인용을 삭제하지 않는다.
2. **압축 기법**: (i) 인과·귀결 관계의 문장 쌍을 접속어(`~이며`, `~하므로`, em-dash)로 병합, (ii) "곧/요컨대" 류 재진술·요약 문장을 선행 문장 말미에 흡수, (iii) 순수 메타·수사 문장(물리 내용 없음)만 전량 삭제 — 이번 대상에서 해당하는 문장은 정확히 1개(§1.0 참조).
3. **구조 보존**: `\textbf{(a) 출발}` / `\textbf{(b) 연산}` / `\textbf{(c) 중간식}` / `\textbf{(d) 박스}` 및 `★` 라벨 단락 경계는 유지한다 — 라벨을 넘나드는 병합은 하지 않았다(G-usable: 독자가 라벨로 다시 찾아올 수 있어야 함).
4. **방향 규약 재설명**: `\S\ref{sec:lco-direction}`(Part II 도입, L1874, 식~`eq:lco-sigmaslot`)에 이미 완전히 정의된 σ_d 부호 대응(LCO 충전↦+1 등)을 sec:lco-peak 안에서 재서술하는 단락(★방향 슬롯)은 포인터로 축소했다(§2.2).
5. **그림 캡션 제외**: `fig:lco-electronic`의 tikzpicture 및 캡션(L2426–2456)은 산문 "절 문장 수" 집계·압축 대상에서 제외했다 — 캡션은 이미 최소 서술이며 도식 해석에 필수적이라 임의 압축 시 그림 판독성 손상 위험이 절 문장 감축 이득보다 크다고 판단했다(아래 §4 최약점 참조).
6. **문장 카운트 규칙**: 마침표(`다./이다./한다.` 등 종결어미) 기준. `[eq]`를 문법적으로 관통하는 한 문장(``~하면\n[식]\n가 ~이다.'')은 1문장으로 계산.

---

## 1. sec:lco-electronic — 절 도입부 (L2225–2231)

**원문**:
```
지금까지 $\Delta S_{\rxn,j}$ 는 배치(configurational)와 격자진동(vibrational) 두 몫이면 닫혔다 — 흑연은 그 둘로 충분하다.
LCO 양극은 한 몫이 더 있다: \emph{전자(electronic) 엔트로피}. 흑연은 충방전 동안 전자구조 변화가 미미해(반금속$\cdot$전도성
변화 작음) 전자항을 무시할 수 있지만, LCO 는 $x\!\downarrow$ 에서 절연체$\to$금속 천이(MIT)를 겪어 Fermi 준위 상태밀도
$g(E_F)$ 가 $0$ 에서 유한값으로 켜진다 — 이 전자 분포의 변화가 엔트로피에 들어온다. \textbf{이 대비(흑연=전자항 0,
LCO=MIT 로 필수)가 통합 챕터의 교육 가치다.} 이 절은 그 항을, \S\ref{sec:dist} 의 ``점유 분포'' 언어를 전자 준위로
옮겨 Fermi--Dirac 분포에서 한 단계씩 유도하고, 1차 문헌에 연속 곡선이 없는 빈자리를 ★\emph{MIT-logistic 게이트}라는
모델 가정으로 메우되 그 가정을 물리로 정당화한다.
```

**교체문**:
```
지금까지 $\Delta S_{\rxn,j}$ 는 배치$\cdot$격자진동 두 몫이면 흑연에서 닫혔으나, LCO 양극은 전자(electronic) 엔트로피
몫이 하나 더 있다 — 흑연은 충방전 중 전자구조 변화가 미미해 전자항을 무시하지만, LCO 는 $x\!\downarrow$ 에서
절연체$\to$금속 천이(MIT)를 겪어 Fermi 준위 상태밀도 $g(E_F)$ 가 $0$ 에서 유한값으로 켜지므로 이 변화가 엔트로피에
들어온다. 이 절은 \S\ref{sec:dist} 의 점유 분포 언어를 전자 준위로 옮겨 Fermi--Dirac 분포에서 이 항을 유도하고,
1차 문헌에 없는 연속 곡선의 빈자리를 ★\emph{MIT-logistic 게이트}라는 모델 가정으로 메우되 그 가정을 물리로
정당화한다.
```

**근거**: 원문 문장4 "이 대비가 통합 챕터의 교육 가치다"는 물리량·수식·부호와 무관한 편집 메타 발언(교재 구성 의도 서술)이라 삭제 — 이 절 전체에서 유일한 **전량 삭제** 대상. 문장1+2+3(무엇이 닫혔나/LCO 는 무엇이 더 있나/왜 흑연은 무시하고 LCO 는 못 하나)은 하나의 인과 사슬이라 병합.
**물리 보존 선언**: config/vib 닫힘 서술, LCO 전자엔트로피 존재, 흑연 무시 근거, MIT 메커니즘($x\downarrow$, 절연체→금속, $g(E_F)$ 0→유한), §sec:dist 연결, 유도 계획(Fermi–Dirac → MIT-logistic 게이트 → 정당화) 전량 보존. 수치·인용 없음(정성 로드맵 단락).
**문장 수**: 5 → 2 (**60%** 감축)

---

## 2. `\subsubsection{...}\label{sec:lco-why}` (L2233–2241)

**원문**:
```
삽입 반응의 전체 엔트로피 변화는 ``리튬 자리가 어떻게 배열되나''(config)$\cdot$``격자가 어떻게 진동하나''(vib)$\cdot$
``전자가 어떤 준위를 어떻게 점유하나''(electronic) 세 자유도의 합이다. 흑연에서는 셋째 몫이 작다 — 흑연$\cdot$
$\mathrm{LiC_6}$ 모두 전도성이 좋아 충방전 동안 $g(E_F)$ 가 크게 바뀌지 않으므로, 전자 분포의 엔트로피 \emph{변화}가
거의 없다. LCO 는 다르다: $x{=}1$($\mathrm{LiCoO_2}$)은 Co$^{3+}$($t_{2g}^6$ low-spin, 닫힌 껍질)라 \emph{전기 절연체}
($g(E_F)\!\approx\!0$)이고, 탈리튬화로 $x$ 가 $\sim$0.94 아래로 내려가면 Co$^{4+}$ 정공이 생겨 $t_{2g}$ 띠에 전도 전자가
열려 \emph{금속}이 된다($g(E_F)\!\to\!$유한)\cite{menetrier1999,motohashi2009}. 이 절연체$\to$금속 천이(MIT)가 $x\approx0.75$--$0.94$
의 2상역에서 일어나며(\S\ref{sec:lco-hys} 의 T1), 그 구간에서만 전자 분포가 켜지므로 전자 엔트로피 \emph{변화}도 그
구간에 국소한다. 곧 ``전자항이 켜지는 게이트''는 MIT 의 직접 결과다.
```

**교체문**:
```
삽입 반응의 전체 엔트로피 변화는 ``리튬 자리 배열''(config)$\cdot$``격자 진동''(vib)$\cdot$``전자 준위 점유''
(electronic) 세 자유도의 합이며, 흑연에서는 셋째 몫이 작다 — 흑연$\cdot$$\mathrm{LiC_6}$ 모두 전도성이 좋아
충방전 동안 $g(E_F)$ 가 크게 바뀌지 않아 전자 분포의 엔트로피 \emph{변화}가 거의 없다. LCO 는 다르다:
$x{=}1$($\mathrm{LiCoO_2}$)은 Co$^{3+}$($t_{2g}^6$ low-spin, 닫힌 껍질)라 \emph{전기 절연체}($g(E_F)\!\approx\!0$)이고,
탈리튬화로 $x$ 가 $\sim$0.94 아래로 내려가면 Co$^{4+}$ 정공이 생겨 $t_{2g}$ 띠에 전도 전자가 열려 \emph{금속}이
된다($g(E_F)\!\to\!$유한)\cite{menetrier1999,motohashi2009}. 이 MIT 는 $x\approx0.75$--$0.94$ 의 2상역에서
일어나며(\S\ref{sec:lco-hys} 의 T1) 그 구간에서만 전자 분포가 켜지므로 전자 엔트로피 \emph{변화}도 그 구간에
국소한다 — 곧 ``전자항이 켜지는 게이트''는 MIT 의 직접 결과다.
```

**근거**: 문장1(세 자유도 정의)+문장2(흑연 무시 근거)를 인과절로 병합. 문장4(MIT 구간 국소화)+문장5(게이트=MIT 직접결과, "곧" 재진술)를 em-dash 로 병합. 문장3(핵심 화학, Co³⁺/Co⁴⁺ 전이)은 수치·인용 밀도가 높아 원문 그대로 유지.
**물리 보존 선언**: 세 자유도 명칭 전량, 수치($x=1$, $\sim$0.94, $x\approx0.75$–$0.94$), 산화상태(Co³⁺ $t_{2g}^6$ low-spin, Co⁴⁺), $g(E_F)$ 0→유한, 인용 `menetrier1999`·`motohashi2009` 전량 보존.
**문장 수**: 5 → 3 (**40%** 감축)

---

## 3. `\subsubsection{...}\label{sec:lco-Se}` (L2243–2359)

### 3.1 (a) 출발 (L2244–2249)

**원문**:
```
\S\ref{sec:dist} 에서 흑연 리튬 자리의 평형 점유가 Fermi-함수형
이었듯, LCO 의 전도 전자도 에너지 준위 $E$ 를 Fermi--Dirac 분포로 점유한다:
[식~\eqref{eq:fd}]
($E_F$ = Fermi 준위). 입자 0/1 배타 점유라는 구조가 식~\eqref{eq:fermifn} 의 리튬 자리 점유와 \emph{같다} — 다만 자리가
``리튬 흡착 자리''가 아니라 ``전자 에너지 준위''다.
```

**교체문**:
```
\S\ref{sec:dist} 에서 흑연 리튬 자리의 평형 점유가 Fermi-함수형이었듯, LCO 의 전도 전자도 에너지 준위 $E$ 를
Fermi--Dirac 분포로 점유하며($E_F$=Fermi 준위):
[식~\eqref{eq:fd}]
입자 0/1 배타 점유라는 구조가 식~\eqref{eq:fermifn} 의 리튬 자리 점유와 \emph{같다} — 다만 자리가 ``리튬 흡착
자리''가 아니라 ``전자 에너지 준위''다.
```

**근거**: $E_F$ 정의 괄호문을 도입절에 흡수.
**물리 보존 선언**: Fermi–Dirac 정의식, §sec:dist·식~eq:fermifn 연결, "0/1 배타 점유" 동형성 진술 전량 보존.
**문장 수**: 3 → 2 (33%)

### 3.2 (b) 연산 (L2251–2254)

**원문**:
```
이 분포의 엔트로피는 두 상태
점유의 정보 엔트로피를 모든 준위에 합한 것이다($-k_B\sum[f\ln f+(1-f)\ln(1-f)]$, 식~\eqref{eq:fd} 를 자리당 점유로 본
\S\ref{sec:hys} 의 $S_\mathrm{mix}$ 와 같은 꼴). 축퇴 전자기체($k_BT\!\ll\!E_F$)에서 이 합은 Fermi 준위 근방의 좁은
열폭($\sim k_BT$)에만 기여가 살아 Sommerfeld 전개로 닫힌다.
```

**교체문**:
```
이 분포의 엔트로피는 두 상태 점유의 정보 엔트로피를 모든 준위에 합한 것이며($-k_B\sum[f\ln f+(1-f)\ln(1-f)]$,
식~\eqref{eq:fd} 를 자리당 점유로 본 \S\ref{sec:hys} 의 $S_\mathrm{mix}$ 와 같은 꼴), 축퇴 전자기체($k_BT\!\ll\!E_F$)
에서 이 합은 Fermi 준위 근방의 좁은 열폭($\sim k_BT$)에만 기여가 살아 Sommerfeld 전개로 닫힌다.
```

**근거**: 같은 논증 흐름의 두 단계를 "~이며"로 인과 병합.
**물리 보존 선언**: 정보 엔트로피 정의식, §sec:hys $S_\mathrm{mix}$ 대응, 축퇴 조건 $k_BT\ll E_F$, Sommerfeld 전개 진입 전량 보존.
**문장 수**: 2 → 1 (50%)

### 3.3 (c) 중간식 (L2254–2268)

**원문**:
```
\emph{여기서 한 가정을 명시한다} — 표준 Sommerfeld 처방대로 상태밀도 $g(E)$ 를 그 좁은 열폭($\sim k_BT$) 안에서
$E_F$ 근방의 \emph{상수} $g(E_F)$ 로 동결한다($g(E)\approx g(E_F)$). 이 동결이 정당한 까닭은, 적분에 기여하는 띠가
폭 $\sim k_BT$ 로 좁고 축퇴 극한 $k_BT\!\ll\!E_F$ 에서는 그 좁은 창 안에서 $g(E)$ 의 에너지 의존이 선도 차수로
무시되기 때문이다 — 이것이 금속 전자기체의 표준 Sommerfeld 근사다. 이 동결 아래 표준 Sommerfeld 적분
$\int(-\partial f/\partial E)(E-E_F)^2\dd E=\tfrac{\pi^2}{3}(k_BT)^2$ 가
전자 \emph{비열}을 먼저 닫는다 — 내부에너지 $U_e=\int E\,g(E)f\,\dd E$ 의 온도 미분에서 $g(E_F)$ 를 적분 밖으로 빼
이 적분을 대입하면
$C_e=\partial U_e/\partial T=\tfrac{\pi^2}{3}k_B^2T\,g(E_F)$($T$-선형 전자 비열, 금속의 표준 결과)다. 엔트로피는 이
비열을 $S_e=\int_0^T (C_e/T')\,\dd T'$ 로 적분한 것이고, $C_e/T'=\tfrac{\pi^2}{3}k_B^2g(E_F)$ 가 $T'$ 무관 상수라
적분이 곧바로 닫혀 ($S_e=\tfrac{\pi^2}{3}k_B^2 g(E_F)\int_0^T\dd T'$)
[식~\eqref{eq:Se}]
로 닫힌다($g(E_F,x)$ = 자리당 Fermi 준위 상태밀도).
```

**교체문**:
```
여기서 한 가정을 명시한다 — 표준 Sommerfeld 처방대로 상태밀도 $g(E)$ 를 그 좁은 열폭($\sim k_BT$) 안에서 $E_F$
근방의 \emph{상수} $g(E_F)$ 로 동결하며($g(E)\approx g(E_F)$), 이 동결이 정당한 까닭은 적분에 기여하는 띠가 폭
$\sim k_BT$ 로 좁고 축퇴 극한 $k_BT\!\ll\!E_F$ 에서는 그 좁은 창 안에서 $g(E)$ 의 에너지 의존이 선도 차수로
무시되는 금속 전자기체의 표준 Sommerfeld 근사이기 때문이다. 이 동결 아래 내부에너지 $U_e=\int E\,g(E)f\,\dd E$ 의
온도 미분에 표준 Sommerfeld 적분 $\int(-\partial f/\partial E)(E-E_F)^2\dd E=\tfrac{\pi^2}{3}(k_BT)^2$ 를 대입하면
전자 \emph{비열} $C_e=\partial U_e/\partial T=\tfrac{\pi^2}{3}k_B^2T\,g(E_F)$($T$-선형, 금속의 표준 결과)이 먼저
닫히고, 이를 $S_e=\int_0^T (C_e/T')\,\dd T'$ 로 적분하면($C_e/T'=\tfrac{\pi^2}{3}k_B^2g(E_F)$ 가 $T'$ 무관 상수라
적분이 곧바로 닫혀)
[식~\eqref{eq:Se}]
로 닫힌다($g(E_F,x)$ = 자리당 Fermi 준위 상태밀도).
```

**근거**: 가정 서술+정당화를 "~하며, ~때문이다" 인과절로 병합; 비열 유도+엔트로피 적분을 "~이 먼저 닫히고, 이를 ~하면 ~로 닫힌다" 단일 흐름으로 병합. 유도 4단계(동결 가정→정당화→$C_e$→$S_e$)의 순서·내용은 그대로, 문장 경계만 축소.
**물리 보존 선언**: 동결 근사 $g(E)\approx g(E_F)$, Sommerfeld 적분 $=\tfrac{\pi^2}{3}(k_BT)^2$, $C_e=\tfrac{\pi^2}{3}k_B^2Tg(E_F)$($T$-선형 언급 포함), $U_e$ 정의, $S_e$ 적분 전개, 식~eq:Se 전량 보존.
**문장 수**: 4 → 2 (50%)

### 3.4 ★직접 엔트로피 경로(교차검증) (L2269–2282)

**원문**:
```
같은 결과를 비열을
거치지 않고 정보 엔트로피에서 곧장 닫아 둘을 맞대어 본다. 분포~\eqref{eq:fd} 의 엔트로피는
$S_e=-k_B\int g(E)\,[f\ln f+(1-f)\ln(1-f)]\,\dd E$ 이고, 무차원 변수 $\zeta\equiv(E-E_F)/k_BT$ 와 엔트로피 핵
$s(\zeta)\equiv-[f\ln f+(1-f)\ln(1-f)]\ge0$ 를 두면 $s(\zeta)$ 는 $\zeta=0$ 대칭의 종이며 표준 Fermi 적분 항등식
$\int_{-\infty}^{\infty}s(\zeta)\,\dd\zeta=\pi^2/3$ 를 만족한다. 동결 $g\approx g(E_F)$ 아래 $\dd E=k_BT\,\dd\zeta$ 를
넣으면
[식~\eqref{eq:Sedirect}]
가 되어 비열 경로의 식~\eqref{eq:Se} 와 한 항등식 $\int s(\zeta)\,\dd\zeta=\pi^2/3$ 으로 일치한다 — 두 경로의 합치가
함수형의 교차검증이다(부호 — $s(\zeta)\ge0$, $g\ge0$ 이라 $S_e\ge0$; 극한 $T\to0$ 또는 $g(E_F)\to0$ 에서 $S_e\to0$).
```

**교체문**:
```
같은 결과를 비열 없이 정보 엔트로피에서 곧장 닫아 맞대어 보면, 분포~\eqref{eq:fd} 의 엔트로피
$S_e=-k_B\int g(E)\,[f\ln f+(1-f)\ln(1-f)]\,\dd E$ 는 무차원 변수 $\zeta\equiv(E-E_F)/k_BT$ 와 엔트로피 핵
$s(\zeta)\equiv-[f\ln f+(1-f)\ln(1-f)]\ge0$ 로 $\zeta=0$ 대칭의 종이 되며 표준 Fermi 적분 항등식
$\int_{-\infty}^{\infty}s(\zeta)\,\dd\zeta=\pi^2/3$ 를 만족한다. 동결 $g\approx g(E_F)$ 아래 $\dd E=k_BT\,\dd\zeta$
를 넣으면
[식~\eqref{eq:Sedirect}]
가 되어 비열 경로의 식~\eqref{eq:Se} 와 한 항등식 $\int s(\zeta)\,\dd\zeta=\pi^2/3$ 으로 일치한다 — 두 경로의
합치가 함수형의 교차검증이다(부호 — $s(\zeta)\ge0$, $g\ge0$ 이라 $S_e\ge0$; 극한 $T\to0$ 또는 $g(E_F)\to0$ 에서
$S_e\to0$).
```

**근거**: 도입 문장("곧장 닫아 맞대어 본다")을 다음 문장 앞절에 흡수. 등식 유도 흐름(무차원 변수 정의→항등식→대입→합치 결론)은 그대로.
**물리 보존 선언**: 직접 적분식, $\zeta$·$s(\zeta)$ 정의, Fermi 적분 항등식 $\pi^2/3$, 식~eq:Sedirect, 두 경로 일치, 부호 검산($S_e\ge0$)·극한($T\to0$, $g(E_F)\to0$) 전량 보존.
**문장 수**: 4 → 2 (50%)

### 3.5 ★Sommerfeld 동결의 유효 경계 (L2283–2288)

**원문**:
```
위 동결 $g\approx g(E_F)$ 의 정확형은 상태밀도의 에너지 의존을 담은 보정항
$\propto g'(E_F)\cdot(k_BT)^2$ 를 포함하며(Mott 항), 그 상대 크기는 $\mathcal O[(k_BT/E_F)^2]$ 다. LCO 금속상은
$E_F\sim$ eV, $k_BT@300\,\mathrm K\approx0.026$ eV 라 $k_BT/E_F\sim0.03$ 으로 보정이 무시할 수준이다. 다만 MIT 천이
\emph{중심}에서는 $g(E_F)$ 가 0 에서 켜지며 $E_F$ 근방 상태밀도가 급변하므로, 동결 가정은 완전 metal 끝점에서 가장
견고하고 천이 중심에서 가장 약하다 — forward 모델이 천이를 게이트 폭 $\Delta x_\mathrm{MIT}$ 로 매끄럽게 보간하므로 이
약화는 피팅 폭에 흡수된다.
```

**교체문**:
```
위 동결 $g\approx g(E_F)$ 의 정확형은 상태밀도의 에너지 의존을 담은 보정항 $\propto g'(E_F)\cdot(k_BT)^2$
(Mott 항, 상대 크기 $\mathcal O[(k_BT/E_F)^2]$)를 포함하나, LCO 금속상은 $E_F\sim$ eV, $k_BT@300\,\mathrm K
\approx0.026$ eV 라 $k_BT/E_F\sim0.03$ 으로 보정이 무시할 수준이다. 다만 MIT 천이 \emph{중심}에서는 $g(E_F)$
가 0 에서 켜지며 $E_F$ 근방 상태밀도가 급변하므로, 동결 가정은 완전 metal 끝점에서 가장 견고하고 천이 중심에서
가장 약하다 — forward 모델이 천이를 게이트 폭 $\Delta x_\mathrm{MIT}$ 로 매끄럽게 보간하므로 이 약화는 피팅 폭에
흡수된다.
```

**근거**: 앞 두 문장을 역접 "~하나, ~수준이다"로 병합.
**물리 보존 선언**: Mott 보정항, $\mathcal O[(k_BT/E_F)^2]$, 수치($E_F\sim$eV, $k_BT@300$K$\approx0.026$eV, $k_BT/E_F\sim0.03$), 유효 경계 판단, 완화 근거(게이트 폭 흡수) 전량 보존.
**문장 수**: 3 → 2 (33% — 목표 미달, §4 최약점 참조)

### 3.6 ★세 구성요소의 신뢰 등급 분리 (L2288–2297)

**원문**:
```
식~\eqref{eq:Se} 를 한 등급으로 뭉개지 않으려면, 그것을 이루는 세 구성요소를 갈라 각각의 신뢰 등급을 따로 매겨야 한다.
세 요소는 \emph{식의 함수형}, \emph{끝점 anchor 값}, \emph{조성에 따른 연속 곡선}이며, 등급은 차례로 다음과 같다.
첫째, 식의 \emph{함수형} $S_e=\tfrac{\pi^2}{3}k_B^2T\,g(E_F)$ 는 교과서 Sommerfeld 표준 결과라 \emph{tier A} 이다(유도된
형태이고, 그 가정은 위 (c) 의 $g\!\approx\!g(E_F)$ 동결이다). 둘째, 완전 metal 의 \emph{단일 anchor} 값
$g(E_F)\!\approx\!13$ e/eV/atom($\mathrm{CoO_2}$, $x{=}0$)은 측정된 끝점이므로 그 \emph{한 점}에서만 \emph{tier A}
이다\cite{motohashi2009}. 셋째, MIT 를 가로지르는 \emph{연속 곡선} $g(E_F,x)$ 는 1차 문헌에 \emph{부재}하여(갭 G2)
신뢰 등급이 없으며, \S\ref{sec:lco-gate} 의 logistic 게이트로 \emph{모델 가정}을 세운 뒤 데이터 피팅에 위임한다.
요컨대 함수형과 anchor 한 점은 tier A 로 견고하고, MIT 천이의 \emph{모양}만이 피팅 대상이다 — 함수형$\cdot$anchor 의
견고함을 천이 곡선의 불확실로 끌어내려 뭉개서는 안 된다.
```

**교체문**:
```
식~\eqref{eq:Se} 를 한 등급으로 뭉개지 않도록 이를 이루는 세 구성요소 — \emph{식의 함수형}$\cdot$\emph{끝점
anchor 값}$\cdot$\emph{조성에 따른 연속 곡선} — 을 갈라 신뢰 등급을 따로 매긴다. 첫째, 함수형
$S_e=\tfrac{\pi^2}{3}k_B^2T\,g(E_F)$ 는 교과서 Sommerfeld 표준 결과라 \emph{tier A} 이며(가정은 위 (c) 의
$g\!\approx\!g(E_F)$ 동결), 둘째, 완전 metal 의 \emph{단일 anchor} 값 $g(E_F)\!\approx\!13$ e/eV/atom
($\mathrm{CoO_2}$, $x{=}0$)도 측정된 끝점인 그 \emph{한 점}에서만 \emph{tier A} 다\cite{motohashi2009}. 셋째,
MIT 를 가로지르는 \emph{연속 곡선} $g(E_F,x)$ 는 1차 문헌에 \emph{부재}하여(갭 G2) 신뢰 등급이 없으며,
\S\ref{sec:lco-gate} 의 logistic 게이트로 \emph{모델 가정}을 세운 뒤 데이터 피팅에 위임한다 — 함수형$\cdot$anchor
의 견고함을 천이 곡선의 불확실로 끌어내려 뭉개서는 안 된다.
```

**근거**: 도입+3요소 열거를 병합. 첫째·둘째의 tier A 판정 문장을 병합. "요컨대" 재진술 문장을 셋째 문장 말미로 흡수하되 그 안의 경계 문구("뭉개서는 안 된다")는 그대로 보존.
**물리 보존 선언**: 세 구성요소 명칭, tier A 판정 2건과 각 근거, 수치 $g(E_F)\approx13$ e/eV/atom($x=0$), 인용 `motohashi2009`, 갭 G2 표기, §sec:lco-gate 위임, 경계 문구 전량 보존.
**문장 수**: 6 → 3 (50%)

### 3.7 (d) 박스 — 전이당 전자 엔트로피 (L2297–2307)

**원문**:
```
forward 모델이
$\Delta S_{\rxn,j}$ 자리에 쓰는 양은 \emph{삽입 반응 엔트로피}다 — 흑연의 \code{GRAPHITE\_STAGING\_LIT}(표~\ref{tab:staging})
가 stage $2\!\to\!1$ 삽입에 $\Delta S_\rxn=-16$ J/(mol\,K)$<0$ 을 넣어 $U(298)\approx0.085$ V 를 round-trip 으로 맞추는
바로 그 슬롯이며(반응식 Li$^+$$+e^-+[\,]\rightleftharpoons$Li, 삽입 방향), 따라서 슬롯의 부호 규약은 \emph{삽입 기준}
($x\!\uparrow$ 당 변화)이다. 전자항도 \emph{같은 삽입 방향}으로 적어, $g(E_F)$ 의 조성 미분에 삽입 방향($x\!\uparrow$)을
실은 전이당 전자 엔트로피를
[식~\eqref{eq:dSe}]
로 정의한다.
```

**교체문**:
```
forward 모델이 $\Delta S_{\rxn,j}$ 자리에 쓰는 양은 \emph{삽입 반응 엔트로피}로 — 흑연의
\code{GRAPHITE\_STAGING\_LIT}(표~\ref{tab:staging})가 stage $2\!\to\!1$ 삽입에 $\Delta S_\rxn=-16$ J/(mol\,K)$<0$
을 넣어 $U(298)\approx0.085$ V 를 round-trip 으로 맞추는 바로 그 슬롯(반응식
Li$^+$$+e^-+[\,]\rightleftharpoons$Li, 삽입 방향; 부호 규약은 \emph{삽입 기준}, $x\!\uparrow$ 당 변화)이며,
전자항도 같은 삽입 방향으로 $g(E_F)$ 의 조성 미분에 부호를 실어 전이당 전자 엔트로피를
[식~\eqref{eq:dSe}]
로 정의한다.
```

**근거**: 슬롯 정의+부호규약 문장과 전자항 정의 문장을 "~이며"로 병합, 표현만 축약.
**물리 보존 선언**: $\Delta S_\rxn=-16$ J/(mol·K)$<0$, $U(298)\approx0.085$V, 반응식, 삽입 기준 부호 규약($x\uparrow$), 식~eq:dSe 전량 보존.
**문장 수**: 2 → 1 (50%)

### 3.8 ★단위 다리 (L2308–2318)

**원문**:
```
식~\eqref{eq:dSe} 의 박스는 \emph{자리당}($k_B^2$ 차원,
원자 1개당) 양이다 — 그러나 forward 슬롯 $\Delta S_{\rxn,j}$ 는 \emph{몰당}(J/(mol\,K), Li 1몰 삽입당) 양이라, 그대로
넣으면 단위가 어긋난다. 자리당 양에 Avogadro 수 $N_A$ 를 곱해 몰당으로 환산하면($N_A k_B^2=R k_B$, 곧 자리당 $k_B$ 한 몫이
몰당 $R$ 로 올라간다)
[식~\eqref{eq:dSemolar}]
가 식~\eqref{eq:lco-decomp} 의 $\Delta S_{e,j}$ 자리에 들어가는 실제 몰당 값이다($g$ 가 e/eV 단위면 eV$\to$J 환산
도 함께 적용).
```

**교체문**:
```
식~\eqref{eq:dSe} 의 박스는 \emph{자리당}($k_B^2$ 차원, 원자 1개당) 양인 반면 forward 슬롯
$\Delta S_{\rxn,j}$ 는 \emph{몰당}(J/(mol\,K), Li 1몰 삽입당) 양이므로, 그대로 넣으면 단위가 어긋나 Avogadro 수
$N_A$ 를 곱해 몰당으로 환산하면($N_A k_B^2=R k_B$, 곧 자리당 $k_B$ 한 몫이 몰당 $R$ 로 올라간다)
[식~\eqref{eq:dSemolar}]
가 식~\eqref{eq:lco-decomp} 의 $\Delta S_{e,j}$ 자리에 들어가는 실제 몰당 값이다($g$ 가 e/eV 단위면 eV$\to$J
환산도 함께 적용).
```

**근거**: 단위 불일치 지적과 환산+결과를 "~이므로 ~하면 ~이다" 단일 인과 흐름으로 병합.
**물리 보존 선언**: 자리당/몰당 차원 구분, 항등식 $N_Ak_B^2=Rk_B$, 식~eq:dSemolar, eV→J 환산 주석 전량 보존.
**문장 수**: 2 → 1 (50%)

### 3.9 ★eV→J 단위 환산식 (L2319–2329)

**원문**:
```
$g$ 의 분모가 eV 이므로 J 단위 상태밀도는 $e_V$ 로
\emph{나눠} 얻는다:
[식~\eqref{eq:gunit}]
이를 대입한 게이트형 몰당 닫힌식은 $\Delta S_{e,j}^{\,\mathrm{mol}}=-\tfrac{\pi^2}{3}R(k_BT/e_V)(g_{\max}/\Delta x_\mathrm{MIT})
\sigma(1-\sigma)$ 이며, 변환에서 $e_V$ 를 곱하면(나눗셈 대신) 결과가 $1/e_V^2$ 배, 곧 $\approx4\times10^{37}$ 배 어긋나므로
P4 코드 구현은 식~\eqref{eq:gunit} 의 \emph{나눗셈} 형을 쓴다. 부호는 환산에 불변이므로($N_A>0,\ e_V>0$) 아래 부호
규약은 자리당$\cdot$몰당 양쪽에 그대로 성립한다.
```

**교체문**:
```
$g$ 의 분모가 eV 이므로 J 단위 상태밀도는 $e_V$ 로 \emph{나눠} 얻는다:
[식~\eqref{eq:gunit}]
이를 대입한 게이트형 몰당 닫힌식은 $\Delta S_{e,j}^{\,\mathrm{mol}}=-\tfrac{\pi^2}{3}R(k_BT/e_V)(g_{\max}/
\Delta x_\mathrm{MIT})\sigma(1-\sigma)$ 이며, 변환에서 $e_V$ 를 곱하면(나눗셈 대신) 결과가 $1/e_V^2$ 배, 곧
$\approx4\times10^{37}$ 배 어긋나므로 P4 코드 구현은 식~\eqref{eq:gunit} 의 \emph{나눗셈} 형을 쓴다 — 부호는
환산에 불변이므로($N_A>0,\ e_V>0$) 아래 부호 규약은 자리당$\cdot$몰당 양쪽에 그대로 성립한다.
```

**근거**: 마지막 문장("부호는 환산에 불변...")을 앞 문장 말미에 em-dash 로 흡수.
**물리 보존 선언**: 나눗셈 vs 곱셈 오류 시 배율 $\approx4\times10^{37}$(P4 코드 구현 경고), 부호 불변성($N_A>0, e_V>0$) 전량 보존.
**문장 수**: 3 → 2 (33%)

### 3.10 ★부호 규약(★최우선 결함 클래스) (L2329–2339)

**원문**:
```
\emph{삽입 기준이며, $\Delta S_{\rxn,j}$ 슬롯(흑연 $2\!\to\!1$
삽입 $-16$ J/(mol\,K))과 일관한다 — 물리적으로 탈리튬화($x\!\downarrow$, 본 문건 LCO 충전 주 진행) 시 전자
엔트로피가 방출된다 — 그 방출량은 게이트가 스스로 예측하는 MIT 전 구간 적분 $\int|\partial S_e/\partial x|\,\dd x\approx1.1\,k_B$/atom(완전 metal 끝점
$S_e$ 와 항등)이며, reynier\cite{reynier2004} 의 O3 총 부분몰 $\approx0.18\,k_B$/atom(config$+$vib$+$전자 총합, tier B)은
전자항 단독량이 아닌 별개 anchor 다(\S\ref{sec:lco-gate} 의 ``세 양의 구분'').} 닫는 논리는 — 삽입($x\!\uparrow$)으로 금속$\to$절연체라 $g(E_F)$ 가 $g_{\max}\!\to\!0$
으로 \emph{감소}하므로 $\partial g/\partial x<0$, 따라서 식~\eqref{eq:dSe} 의 $\Delta S_{e,j}=+\partial S_e/\partial x<0$
— MIT 구간에서 전이당(삽입당) 전자 엔트로피가 \emph{음의 골}이고, 그 절댓값 $|\Delta S_{e,j}|=-\partial S_e/\partial x>0$
이 탈리튬화 시 방출되는 봉우리다(그림~\ref{fig:lco-electronic} 의 파선이 이 양의 방출량 $-\partial g/\partial x$). 흑연에서
삽입 반응 엔트로피 $\Delta S_\rxn$ 이 음의 값으로 슬롯에 들어가듯, LCO MIT 의 전자항도 삽입 기준 음의 값으로 들어가
부호가 일관한다 — 박스$\cdot$프레임 그림$\cdot$분해식(\eqref{eq:lco-decomp})이 모두 같은 삽입-기준 $\Delta S_{e,j}<0$
(탈리튬화 방출 $|\Delta S_{e,j}|>0$)을 가리킨다.
```

**교체문**:
```
\emph{삽입 기준이며}, $\Delta S_{\rxn,j}$ 슬롯(흑연 $2\!\to\!1$ 삽입 $-16$ J/(mol\,K))과 일관한다 — 물리적으로
탈리튬화($x\!\downarrow$, 본 문건 LCO 충전 주 진행) 시 전자 엔트로피가 방출되며, 그 방출량은 게이트가 스스로
예측하는 MIT 전 구간 적분 $\int|\partial S_e/\partial x|\,\dd x\approx1.1\,k_B$/atom(완전 metal 끝점 $S_e$ 와
항등)이고, reynier\cite{reynier2004} 의 O3 총 부분몰 $\approx0.18\,k_B$/atom(config$+$vib$+$전자 총합, tier B)은
전자항 단독량이 아닌 별개 anchor 다(\S\ref{sec:lco-gate} 의 ``세 양의 구분''). 닫는 논리는 — 삽입($x\!\uparrow$)
으로 금속$\to$절연체라 $g(E_F)$ 가 $g_{\max}\!\to\!0$ 으로 \emph{감소}하므로 $\partial g/\partial x<0$, 따라서
식~\eqref{eq:dSe} 의 $\Delta S_{e,j}=+\partial S_e/\partial x<0$ — MIT 구간에서 전이당(삽입당) 전자 엔트로피가
\emph{음의 골}이고, 그 절댓값 $|\Delta S_{e,j}|=-\partial S_e/\partial x>0$ 이 탈리튬화 시 방출되는 봉우리다
(그림~\ref{fig:lco-electronic} 의 파선이 이 양의 방출량 $-\partial g/\partial x$) — 흑연의 음의 $\Delta S_\rxn$
슬롯과 같은 삽입-기준 부호이며, 박스$\cdot$프레임 그림$\cdot$분해식(\eqref{eq:lco-decomp})이 모두 같은
삽입-기준 $\Delta S_{e,j}<0$(탈리튬화 방출 $|\Delta S_{e,j}|>0$)을 가리킨다.
```

**근거**: ★최우선 결함 클래스로 명시 지정된 단락이라 압축을 **의도적으로 보수적**으로 적용 — 3문장 중 마지막 문장(그래프·박스·분해식 간 일관성 재확인)만 앞 문장 말미에 em-dash 로 흡수하고, 부호 도출 사슬(∂g/∂x<0 → ΔS_e,j<0 → 음의 골 → |ΔS_e,j|>0 방출 봉우리) 자체는 문장 경계를 바꾸지 않았다 — 부호 오류가 이 문건에서 최우선 결함으로 취급되는 만큼, 문장 재배열로 인한 논리 사슬 훼손 위험을 감수하지 않기 위함이다.
**물리 보존 선언**: $-16$ J/(mol·K), 삽입 기준, $\approx1.1\,k_B$/atom, `reynier2004`의 $\approx0.18\,k_B$/atom(tier B, 별개 anchor 명시), $\partial g/\partial x<0$, $\Delta S_{e,j}<0$, $|\Delta S_{e,j}|>0$ 등 모든 부호·수치·tier·그림 참조 전량 보존.
**문장 수**: 3 → 2 (**33%, 목표 미달** — §4 최약점 1번 참조)

### 3.11 ★온도 의존 (L2339–2344)

**원문**:
```
식~\eqref{eq:dSe} 는 다른 항과 결정적으로 다르다 —
$\Delta S_{e,j}\propto T$ 이므로 전자 기여 $\partial U_j/\partial T|_e=\Delta S_{e,j}/F\propto T$ 가 \emph{$T$ 에 선형}이다
(상수 $\Delta S_\rxn$ 인 config$\cdot$vib 와 달리). 곧 \emph{$\partial U_1/\partial T$ 의 기울기 자체가 $T$ 에 비례}하며,
이를 적분한 전자항의 $U_1$ 이동은 $\propto T^2$ 다(선형 아님 — 식별 신호는 ``$\partial U/\partial T$ 가 $T$ 에 선형''
이지 ``peak 위치가 $T$ 에 선형''이 아니다). 다온도 피팅에서 전자항만 이 $T$ 의존을 보이며, Ch2 의 가역 발열로 확장할
때 중요하다.
```

**교체문**:
```
식~\eqref{eq:dSe} 는 다른 항과 결정적으로 다르다 — $\Delta S_{e,j}\propto T$ 이므로(상수 $\Delta S_\rxn$ 인
config$\cdot$vib 와 달리) 전자 기여 $\partial U_j/\partial T|_e=\Delta S_{e,j}/F\propto T$ 가 \emph{$T$ 에 선형}이며,
이를 적분한 전자항의 $U_1$ 이동은 $\propto T^2$ 다(선형 아님 — 식별 신호는 ``$\partial U/\partial T$ 가 $T$ 에
선형''이지 ``peak 위치가 $T$ 에 선형''이 아니다). 다온도 피팅에서 전자항만 이 $T$ 의존을 보이며, Ch2 의 가역
발열로 확장할 때 중요하다.
```

**근거**: 문장1(T-선형 서술)과 문장2("곧" 재진술+T² 결론)를 병합, 반복되는 "T-선형" 서술을 1회로 축약.
**물리 보존 선언**: $\Delta S_{e,j}\propto T$, $\partial U_j/\partial T\propto T$, $U_1$ 이동 $\propto T^2$, 식별 신호 문구(이동률 vs 위치 구분) 전량 보존.
**문장 수**: 3 → 2 (33%)

### 3.12 ★$T^2$ 누적계수 (L2346–2358)

**원문**:
```
전자항이 $T$ 선형이므로 T1 의 총 삽입 엔트로피를 상수 몫과 선형 몫으로
적으면 $\Delta S_{\rxn,1}^\mathrm{cat}(T)=\Delta S_0+a_e\,T$ 이고($\Delta S_0=\Delta S_0^\mathrm{config}+\Delta S_0^\mathrm{vib}$
는 $T$ 무관, 전자 기울기 $a_e=-\tfrac{\pi^2}{3}R\,(k_B/e_V)\,(g_{\max}/\Delta x_\mathrm{MIT})\,\sigma(1-\sigma)<0$ 는 식
\eqref{eq:dSemolar}$\cdot$\eqref{eq:gunit} 의 몰당 나눗셈 형). $\partial U_1/\partial T=\Delta S_{\rxn,1}^\mathrm{cat}(T)/F$
를 기준온도 $T_0$ 에서 적분하면
[식~\eqref{eq:U1T2}]
전자항의 $T^2$ 계수는 $a_e/(2F)$ 이며, $\tfrac12$ 인자가 $\int_{T_0}^{T}a_e T'\,\dd T'=\tfrac{a_e}{2}(T^2-T_0^2)$ 에서
나온다 — $T\cdot\Delta S$ 의 단순 곱으로 섞으면 이 $\tfrac12$ 을 잃는다. config$\cdot$vib 는 $T$-선형 항
$\tfrac{\Delta S_0}{F}(T-T_0)$ 만 남기고, 곡률($a_e/(2F)<0$)은 전자항이 단독으로 만든다 — 고온 외삽이 선형 외삽보다
낮아지는 것이 식별 신호다.
```

**교체문**:
```
전자항이 $T$ 선형이므로 T1 의 총 삽입 엔트로피를 상수 몫과 선형 몫으로 적으면
$\Delta S_{\rxn,1}^\mathrm{cat}(T)=\Delta S_0+a_e\,T$ 이고($\Delta S_0=\Delta S_0^\mathrm{config}+
\Delta S_0^\mathrm{vib}$ 는 $T$ 무관, 전자 기울기 $a_e=-\tfrac{\pi^2}{3}R\,(k_B/e_V)\,(g_{\max}/
\Delta x_\mathrm{MIT})\,\sigma(1-\sigma)<0$ 는 식~\eqref{eq:dSemolar}$\cdot$\eqref{eq:gunit} 의 몰당 나눗셈 형).
$\partial U_1/\partial T=\Delta S_{\rxn,1}^\mathrm{cat}(T)/F$ 를 기준온도 $T_0$ 에서 적분하면
[식~\eqref{eq:U1T2}]
전자항의 $T^2$ 계수는 $a_e/(2F)$ 이며, $\tfrac12$ 인자는 $\int_{T_0}^{T}a_e T'\,\dd T'=\tfrac{a_e}{2}
(T^2-T_0^2)$ 에서 나온다($T\cdot\Delta S$ 의 단순 곱으로 섞으면 이 $\tfrac12$ 을 잃는다) — config$\cdot$vib 는
$T$-선형 항 $\tfrac{\Delta S_0}{F}(T-T_0)$ 만 남기고, 곡률($a_e/(2F)<0$)은 전자항이 단독으로 만들며, 고온
외삽이 선형 외삽보다 낮아지는 것이 식별 신호다.
```

**근거**: "1/2 인자 유래" 문장과 "config·vib 선형항+곡률+식별신호" 문장을 em-dash 로 병합(같은 결론의 두 갈래를 한 흐름으로).
**물리 보존 선언**: $\Delta S_{\rxn,1}^\mathrm{cat}(T)=\Delta S_0+a_eT$, $a_e$ 닫힌형과 부호($<0$), 식~eq:U1T2, $T^2$ 계수 $a_e/(2F)$, $1/2$ 인자 유래식, "단순 곱 섞으면 잃는다" 경고, 곡률 부호, 식별 신호(고온 외삽) 전량 보존.
**문장 수**: 4 → 3 (25% — §4 최약점 2번 참조)

### 3.13 lco-Se 소계

| 단락 | 전 | 후 |
|---|---|---|
| (a) 출발 | 3 | 2 |
| (b) 연산 | 2 | 1 |
| (c) 중간식 | 4 | 2 |
| ★직접 엔트로피 경로 | 4 | 2 |
| ★Sommerfeld 유효 경계 | 3 | 2 |
| ★세 구성요소 신뢰 등급 | 6 | 3 |
| (d) 박스 | 2 | 1 |
| ★단위 다리 | 2 | 1 |
| ★eV→J 환산 | 3 | 2 |
| ★부호 규약 | 3 | 2 |
| ★온도 의존 | 3 | 2 |
| ★$T^2$ 누적계수 | 4 | 3 |
| **소계** | **39** | **23** |

**lco-Se 감축률**: (39−23)/39 = **41.0%**

---

## 4. `\subsubsection{...}\label{sec:lco-gate}` (L2360–2459) — ★outlier 절

### 4.1 문헌 부재 → logistic 근사 (L2361–2364)

**원문**:
```
식~\eqref{eq:dSe} 를 쓰려면 $g(E_F,x)$ 의 \emph{연속 곡선}이 필요하나, 1차 문헌엔 그것이 없다 — Motohashi 등\cite{motohashi2009}은
완전 metal($\mathrm{CoO_2}$, $x{=}0$)의 단일 anchor $g(E_F)\!\approx\!13$ e/eV/atom 과 ``$x\!\downarrow$ 로 $g$ 가
켜진다''는 정성 추세만 준다(이것이 갭 G2). 흑연 \code{GRAPHITE\_STAGING\_LIT} 의 ``문헌값=초기값, 데이터로 피팅''
철학을 그대로 적용해, MIT 의 천이를 \emph{logistic 게이트}로 근사한다:
```

**교체문**:
```
식~\eqref{eq:dSe} 를 쓰려면 $g(E_F,x)$ 의 \emph{연속 곡선}이 필요하나 1차 문헌엔 없어(Motohashi
등\cite{motohashi2009}의 완전 metal $\mathrm{CoO_2}$($x{=}0$) 단일 anchor $g(E_F)\!\approx\!13$ e/eV/atom 과
``$x\!\downarrow$ 로 $g$ 가 켜진다''는 정성 추세만 있음 — 이것이 갭 G2), 흑연 \code{GRAPHITE\_STAGING\_LIT} 의
``문헌값=초기값, 데이터로 피팅'' 철학을 그대로 적용해 MIT 의 천이를 \emph{logistic 게이트}로 근사한다:
```

**근거**: 갭 지적 문장과 근사 도입 문장을 "~하나 ~없어(...), ~적용해 ~근사한다" 단일 인과 흐름으로 병합.
**물리 보존 선언**: $g(E_F)\approx13$ e/eV/atom, $x=0$, 인용 `motohashi2009`, 갭 G2 표기, "문헌값=초기값" 철학 문구 전량 보존.
**문장 수**: 2 → 1 (50%)

### 4.2 σ 정의 + 초기값/골 (L2370–2372)

**원문**:
```
($\sigma$ = logistic; $x\!\downarrow$ 로 $g$ 가 $0\!\to\!g_{\max}$ 켜진다). 세 초기값$(g_{\max},x_\mathrm{MIT},
\Delta x_\mathrm{MIT})$ 이 피팅 대상이며, 식~\eqref{eq:dSe} 에 넣으면 삽입 기준 $\Delta S_e(x)\propto\partial\sigma/\partial x<0$
(탈리튬화 방출 $|\Delta S_e|\propto-\partial\sigma/\partial x>0$)가 MIT 부근의 \emph{국소 골}(절댓값 봉우리, 작지만 0 아님)이 된다.
```

**교체문**:
```
($\sigma$=logistic, $x\!\downarrow$ 로 $g$ 가 $0\!\to\!g_{\max}$ 켜짐) 세 초기값$(g_{\max},x_\mathrm{MIT},
\Delta x_\mathrm{MIT})$ 이 피팅 대상이며, 식~\eqref{eq:dSe} 에 넣으면 삽입 기준 $\Delta S_e(x)\propto\partial\sigma
/\partial x<0$(탈리튬화 방출 $|\Delta S_e|\propto-\partial\sigma/\partial x>0$)가 MIT 부근의 \emph{국소 골}
(절댓값 봉우리, 작지만 0 아님)이 된다.
```

**근거**: 독립 문장이던 σ 정의 괄호를 도입절로 흡수.
**물리 보존 선언**: σ 정의, 세 초기값 명칭, 삽입 기준 부호($<0$)와 절댓값 부호($>0$), "작지만 0 아님" 한정어 전량 보존.
**문장 수**: 2 → 1 (50%)

### 4.3 게이트 대입 리드(L2374–2377), 정당화 리드(L2390–2391), (ii) x_MIT(L2395–2396) — **무변경**
이미 각 1문장으로 최소 서술이라 압축하지 않았다(추가 병합 시 물리 내용 손실 없이는 문장 수를 더 줄일 수 없음).

### 4.4 음부호 + 골 + 몰당 환산 (L2385–2388)

**원문**:
```
— 앞에 붙은 음부호(leading $-$)가 삽입 기준 $\Delta S_{e,j}<0$ 을 식 자체로 못박는다($g_{\max},\Delta x_\mathrm{MIT},
\sigma(1-\sigma)$ 모두 양). $x_\mathrm{MIT}$ 에서 $\sigma(1-\sigma)$ 가 최대 $\tfrac14$ 라 골이 가장 깊고, 양쪽으로
지수적으로 죽어 T1 에만 국소화된 종(절댓값 봉우리)이다. 식~\eqref{eq:dSemolar} 의 몰당 환산을 함께 적용하면
$\Delta S_{e,j}^{\,\mathrm{mol}}=N_A\Delta S_{e,j}$ 가 forward 슬롯에 들어간다.
```

**교체문**:
```
— 앞의 음부호가 삽입 기준 $\Delta S_{e,j}<0$ 을 식 자체로 못박으며($g_{\max},\Delta x_\mathrm{MIT},
\sigma(1-\sigma)$ 모두 양), $x_\mathrm{MIT}$ 에서 $\sigma(1-\sigma)$ 가 최대 $\tfrac14$ 라 골이 가장 깊고 양쪽으로
지수적으로 죽어 T1 에만 국소화된 종(절댓값 봉우리)이다 — 식~\eqref{eq:dSemolar} 의 몰당 환산을 적용하면
$\Delta S_{e,j}^{\,\mathrm{mol}}=N_A\Delta S_{e,j}$ 가 forward 슬롯에 들어간다.
```

**근거**: 세 문장(부호 논증/골 형태/몰당 환산)을 두 접속어(~하며, —)로 한 흐름으로 병합.
**물리 보존 선언**: 부호 논증($g_{\max},\Delta x_\mathrm{MIT},\sigma(1-\sigma)$ 모두 양), $\sigma(1-\sigma)$ 최댓값 $1/4$, T1 국소화, 몰당 환산식 $\Delta S_{e,j}^{mol}=N_A\Delta S_{e,j}$ 전량 보존.
**문장 수**: 3 → 1 (67%)

### 4.5 (i) $g_\max=13$ — anchor (L2393–2394)

**원문**:
```
완전 탈리튬 $\mathrm{CoO_2}$ 의 metallic $g(E_F)$ 가 이 값이다\cite{motohashi2009}
(tier A 단일점). 곧 게이트의 ``켜진'' 높이는 측정된 끝점이지 자유 파라미터가 아니다(초기값으로 고정, 도핑 시 소폭 조정).
```

**교체문**:
```
완전 탈리튬 $\mathrm{CoO_2}$ 의 metallic $g(E_F)$ 가 이 값이며(tier A 단일점)\cite{motohashi2009}, 게이트의
``켜진'' 높이는 측정된 끝점이지 자유 파라미터가 아니다(초기값으로 고정, 도핑 시 소폭 조정).
```

**근거**: "곧" 재진술 연결을 등위 접속으로 병합.
**물리 보존 선언**: tier A 단일점, 인용 `motohashi2009`, "측정된 끝점/자유 파라미터 아님" 판정 전량 보존.
**문장 수**: 2 → 1 (50%)

### 4.6 (iii) $\Delta x_\mathrm{MIT}\approx0.05$ — 폭 (L2397–2402)

**원문**:
```
발현 2상역의 조성 폭($\approx0.94{-}0.75=0.19$)을 logistic 의
$\pm2\Delta x$ 유효폭($\approx0.2$)에 맞춘 것이다. 이 폭은 \emph{결함 농도}에 의존한다 — 실제 시료는 산소 결손$\cdot$
양이온 무질서가 MIT 발현 조성을 분산시키므로, step(0폭)이 아니라 유한 폭이 물리적이다. \emph{logistic 을 택한 이유}가
바로 이것이다: (1) 매끄러운 $\partial U_j/\partial T$ 를 주어 Ch2 의 겹침 가중과 일관되고, (2) 결함이 만드는 발현 조성의
분산을 \emph{폭 하나}로 흡수해 데이터로 피팅 가능하게 한다. step 함수는 $\partial g/\partial x$ 가 델타라 비물리적
스파이크를 내고 결함 분산을 담지 못한다.
```

**교체문**:
```
발현 2상역의 조성 폭($\approx0.94{-}0.75=0.19$)을 logistic 의 $\pm2\Delta x$ 유효폭($\approx0.2$)에 맞춘
것으로, 이 폭은 \emph{결함 농도}에 의존한다 — 실제 시료는 산소 결손$\cdot$양이온 무질서가 MIT 발현 조성을
분산시키므로 step(0폭)이 아니라 유한 폭이 물리적이며, \emph{logistic 을 택한 이유}가 바로 이것이다: (1) 매끄러운
$\partial U_j/\partial T$ 를 주어 Ch2 의 겹침 가중과 일관되고, (2) 결함이 만드는 발현 조성의 분산을 \emph{폭
하나}로 흡수해 데이터로 피팅 가능하게 한다 — step 함수는 $\partial g/\partial x$ 가 델타라 비물리적 스파이크를
내고 결함 분산을 담지 못한다.
```

**근거**: 네 문장(폭 설정 근거 / 결함 의존 / logistic 선택 이유 (1)(2) / step 함수 실패)의 논증 순서를 그대로 유지한 채 접속사로 한 문장에 통합. 개별 근거 항목은 삭제 없이 모두 유지.
**물리 보존 선언**: 조성 폭 수치($\approx0.94-0.75=0.19$, $\pm2\Delta x\approx0.2$), 결함 물리(산소 결손·양이온 무질서), logistic 선택 이유 (1)(2) 두 항목 전량, step 함수의 비물리적 실패(델타 스파이크) 전량 보존.
**문장 수**: 4 → 1 (75%)

### 4.7 (iv) 게이트 형태의 자기일관성 (L2403–2405)

**원문**:
```
식~\eqref{eq:ggate} 의 logistic 은 \S\ref{sec:dist} 의 점유 분포(식~\eqref{eq:fermifn})
와 \emph{같은 함수형}이다 — 전자 띠가 열리는 천이를 ``Fermi-함수형 게이트''로 적는 것은 전도 전자 점유 자체가 Fermi--Dirac
(식~\eqref{eq:fd})인 것과 한 언어다. 곧 게이트는 LCO 전자구조의 점유 분포 관점이 자연히 낳는 꼴이다.
```

**교체문**:
```
식~\eqref{eq:ggate} 의 logistic 은 \S\ref{sec:dist} 의 점유 분포(식~\eqref{eq:fermifn})와 \emph{같은 함수형}
이다 — 전자 띠가 열리는 천이를 ``Fermi-함수형 게이트''로 적는 것은 전도 전자 점유 자체가 Fermi--Dirac
(식~\eqref{eq:fd})인 것과 한 언어이며, 게이트는 LCO 전자구조의 점유 분포 관점이 자연히 낳는 꼴이다.
```

**근거**: "곧" 재진술 문장을 앞 문장 말미에 흡수.
**물리 보존 선언**: logistic-점유분포 함수형 동일성, 식~eq:fermifn·eq:fd 연결 전량 보존.
**문장 수**: 2 → 1 (50%)

### 4.8 크기 검산 (L2408–2415)

**원문**:
```
완전 metal 한계의 자리당 전자 엔트로피는 식~\eqref{eq:Se} 로
$S_e/k_B=\tfrac{\pi^2}{3}(k_BT)\,g(E_F)=3.29\times0.0259\ \mathrm{eV}\times13/\mathrm{eV}\approx1.1\,k_B$/atom
($T{=}300$ K)이며, 이 값이 게이트가 스스로 예측하는 MIT 적분 전자 방출량과 항등이다. 한편 O3 영역의 부분몰 차
$\approx0.18\,k_B$/atom\cite{reynier2004} (tier B)는 config$+$vib$+$전자 \emph{총합}의 부분몰량이라, 위 전자 단독 절댓값($1.1$)과
\emph{척도가 다른 양}이다(아래 ``세 양의 구분'' 참조 — 서로의 검산으로 쓰지 않으므로 ``같은 자릿수'' 대조를 하지 않는다). 그
O3 총합은 config 가 지배하고(>$\tfrac12$\cite{reynier2004}, tier A) 전자항은 그중 \emph{작은} 몫이다. 그럼에도 필수인 이유는 크기가 아니라 \emph{게이트}에 있다 —
config 단독으로는 MIT 2상역의 엔트로피 거동을 재현하지 못하고\cite{ml2024} (tier A), 절연체$\to$금속의 전자 자유도가 켜지는
신호는 오직 $\Delta S_e$ 게이트만 담는다. 곧 ``작지만 빠지면 MIT 를 못 그린다''.
```

**교체문**:
```
완전 metal 한계의 자리당 전자 엔트로피는 식~\eqref{eq:Se} 로 $S_e/k_B=\tfrac{\pi^2}{3}(k_BT)\,g(E_F)
=3.29\times0.0259\ \mathrm{eV}\times13/\mathrm{eV}\approx1.1\,k_B$/atom($T{=}300$ K)이며, 이 값이 게이트가
스스로 예측하는 MIT 적분 전자 방출량과 항등이다. 한편 O3 영역의 부분몰 차 $\approx0.18\,k_B$/atom
\cite{reynier2004}(tier B)는 config$+$vib$+$전자 \emph{총합}의 부분몰량이라 위 전자 단독 절댓값($1.1$)과
\emph{척도가 다른 양}이다(아래 ``세 양의 구분'' 참조 — 같은 자릿수 대조를 하지 않는다). 그 O3 총합은 config 가
지배하나(>$\tfrac12$\cite{reynier2004}, tier A), 전자항이 없으면 config 단독으로는 MIT 2상역의 엔트로피 거동을
재현하지 못해\cite{ml2024}(tier A) 절연체$\to$금속의 전자 자유도가 켜지는 신호를 오직 $\Delta S_e$ 게이트만
담는다 — ``작지만 빠지면 MIT 를 못 그린다''.
```

**근거**: "config 지배(작은 몫)" 문장과 "그럼에도 필수인 이유는 게이트" 문장 및 "곧 작지만 빠지면..." 결론 문장을 하나의 역접-귀결 흐름으로 병합. 수치 계산 문장(1.1 k_B)과 척도 구분 문장(0.18 k_B)은 그대로 유지.
**물리 보존 선언**: $S_e/k_B\approx1.1\,k_B$/atom($T=300$K, 계산식 $3.29\times0.0259\times13$ 전량), `reynier2004`의 $\approx0.18\,k_B$/atom(tier B), "척도가 다른 양" 경계, config 지배 비율($>1/2$, tier A), `ml2024` 인용, 결론 문구("작지만 빠지면...") 전량 보존.
**문장 수**: 5 → 3 (40%)

### 4.9 ★세 양의 구분 (L2417–2424)

**원문**:
```
위 크기 논의에 등장하는 세 수치는 \emph{서로 다른 양}이므로 한자리에 섞지
않는다. 첫째, 완전 metal 의 \emph{전체} 자리당 전자 엔트로피 $S_e/k_B=\tfrac{\pi^2}{3}(k_BT)g(E_F)\approx1.1\,k_B$/atom
(식~\eqref{eq:Se}, $x{=}0$ 끝점)은 절대량이다. 둘째, O3 영역의 \emph{부분몰} 차 $\approx0.18\,k_B$/atom\cite{reynier2004}
은 한 조성 구간에서의 변화량 anchor 다. 셋째, 게이트 미분의 \emph{골 깊이}는 식~\eqref{eq:dSegate}$\cdot$\eqref{eq:gunit}
의 몰당 닫힌식으로 천이 중심($\sigma(1-\sigma)=\tfrac14$, $g_{\max}{=}13$, $\Delta x_\mathrm{MIT}{=}0.05$, $T{=}300$ K)에서
$-\tfrac{\pi^2}{3}R(k_BT/e_V)(g_{\max}/\Delta x_\mathrm{MIT})\cdot\tfrac14\approx-46$ J/(mol\,K) 이며, 골 깊이가 부분몰 차보다
큰 것은 $1/\Delta x_\mathrm{MIT}\approx20$ 의 게이트 미분 증폭 때문이다. 곧 절대량$\cdot$부분몰 anchor$\cdot$게이트 골
깊이는 척도가 다른 세 수치로, 어느 하나를 다른 하나의 검산으로 쓰지 않는다.
```

**교체문**:
```
위 크기 논의에 등장하는 세 수치 — 완전 metal 의 \emph{전체} 자리당 전자 엔트로피
$S_e/k_B=\tfrac{\pi^2}{3}(k_BT)g(E_F)\approx1.1\,k_B$/atom(식~\eqref{eq:Se}, $x{=}0$ 끝점, 절대량), O3 영역의
\emph{부분몰} 차 $\approx0.18\,k_B$/atom\cite{reynier2004}(한 조성 구간의 변화량 anchor), 게이트 미분의
\emph{골 깊이}(식~\eqref{eq:dSegate}$\cdot$\eqref{eq:gunit} 의 몰당 닫힌식으로 천이 중심 $\sigma(1-\sigma)=
\tfrac14$, $g_{\max}{=}13$, $\Delta x_\mathrm{MIT}{=}0.05$, $T{=}300$ K 에서 $-\tfrac{\pi^2}{3}R(k_BT/e_V)
(g_{\max}/\Delta x_\mathrm{MIT})\cdot\tfrac14\approx-46$ J/(mol\,K)) — 는 서로 다른 양이므로 한자리에 섞지
않는다. 골 깊이가 부분몰 차보다 큰 것은 $1/\Delta x_\mathrm{MIT}\approx20$ 의 게이트 미분 증폭 때문이며, 어느
하나를 다른 하나의 검산으로 쓰지 않는다.
```

**근거**: 도입 문장("세 수치는 서로 다른 양")과 종결 문장("절대량·부분몰 anchor·게이트 골 깊이는 척도가 다른 세 수치")이 서로 재진술(bookend)이므로 하나로 통합하고, 세 수치의 개별 정의(원문 둘째·셋째·넷째 문장)를 그 통합 문장 안에 열거식으로 흡수했다. 남은 문장은 증폭 배율 설명과 "검산으로 쓰지 않는다"는 잔여 결론만 유지.
**물리 보존 선언**: 세 수치 전량($\approx1.1\,k_B$/atom · $\approx0.18\,k_B$/atom · $\approx-46$ J/(mol·K)), 골 깊이 계산의 모든 대입값($\sigma(1-\sigma)=1/4$, $g_{max}=13$, $\Delta x_{MIT}=0.05$, $T=300$K), 증폭 배율 $1/\Delta x_\mathrm{MIT}\approx20$, 인용 `reynier2004` 전량 보존.
**문장 수**: 5 → 2 (60%)

### 4.10 절 말미(lco-electronic → lco-peak 전환, L2458–2459) — **무변경**
```
이 전자항이 \S\ref{sec:sum} 의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해에서 셋째 성분으로 plug-in 되며(흑연은 이 자리가 0),
forward 코드는 전이 파라미터를 LCO 로 갈아 끼우고 이 항 하나를 더하는 것만으로 LCO 에 적용된다(\S\ref{sec:lco-code}).
```
이미 1문장으로 절 전환 기능만 하는 최소 서술 — 압축하지 않음.

### 4.11 lco-gate 소계

| 단락 | 전 | 후 |
|---|---|---|
| 문헌 부재→근사 | 2 | 1 |
| σ 정의+초기값/골 | 2 | 1 |
| 게이트 대입 리드 | 1 | 1 |
| 음부호+골+몰당 | 3 | 1 |
| 정당화 리드 | 1 | 1 |
| (i) $g_\max$ anchor | 2 | 1 |
| (ii) $x_\mathrm{MIT}$ | 1 | 1 |
| (iii) $\Delta x_\mathrm{MIT}$ | 4 | 1 |
| (iv) 자기일관성 | 2 | 1 |
| 크기 검산 | 5 | 3 |
| ★세 양의 구분 | 5 | 2 |
| 절 말미 | 1 | 1 |
| **소계** | **29** | **15** |

**lco-gate 감축률**: (29−15)/29 = **48.3%** — 지정된 outlier 절에 걸맞게 목표(35%)를 크게 상회, (i)–(iv) 정당화 논거의 뼈대(4개 항목 전량)는 보존.

---

## 5. sec:lco-electronic 전체 소계

| 하위 단위 | 전 | 후 |
|---|---|---|
| 절 도입부 | 5 | 2 |
| lco-why | 5 | 3 |
| lco-Se | 39 | 23 |
| lco-gate | 29 | 15 |
| **합계** | **78** | **43** |

**sec:lco-electronic 감축률**: (78−43)/78 = **44.9%**

---

## 6. sec:lco-peak (L2461–2525)

### 6.1 (a) 출발 (L2462–2469) — **무변경**
```
흑연 \S\ref{sec:eqpeak} 의 출발점인 전하 보존식은
전극을 가리지 않으므로, 전이 집합만 $\mathcal J_\mathrm{LCO}$(식~\eqref{eq:lco-J})로 바꿔 그대로 적는다:
[식~\eqref{eq:lco-charge}]
```
이미 1문장. 압축하지 않음.

### 6.2 ★방향 슬롯 (L2471–2474) — **원칙 ④ 적용 (Part II 포인터화)**

**원문**:
```
이후의 $\sigma_d$ 는 \S\ref{sec:lco-direction} 의 규약(식~\eqref{eq:lco-sigmaslot})대로
세 작용처(분극$\cdot$분기$\cdot$꼬리) 모두에서 ``탈리튬화 진행 $=+1$''로 먹인다 --- LCO 데이터에서는 충전
곡선에 $\sigma_d=+1$, 방전(리튬화$\cdot$전위 하강) 곡선에 $\sigma_d=-1$. 평형 종은 (b)의
$\xi\leftrightarrow1-\xi$ 대칭으로 이 선택에 불변이다.
```

**교체문**:
```
이후 $\sigma_d$ 는 \S\ref{sec:lco-direction} 의 규약(식~\eqref{eq:lco-sigmaslot})을 그대로 따르며, 평형 종은
(b)의 $\xi\leftrightarrow1-\xi$ 대칭으로 이 선택에 불변이다.
```

**근거**: 원칙 ④(방향 규약 재설명은 Part II 도입 포인터로) 직접 적용. LCO 충전/방전과 $\sigma_d=\pm1$ 의 구체 대응은 이미 식~`eq:lco-sigmaslot`(§sec:lco-direction, L1879–1881)에 "LCO 하프셀 --- 충전$\mapsto+1$"으로 명문화되어 있고, 그 절의 "평형 종의 불변" 단락(L1905–1909)이 $\xi\leftrightarrow1-\xi$ 불변성도 이미 진술한다 — 본 절에서 재서술하지 않고 규약 포인터로 대체했다. $\xi\leftrightarrow1-\xi$ 불변 서술은 바로 다음 (b)의 도출에 국소적으로 필요해 남겼다.
**물리 보존 선언**: `\S\ref{sec:lco-direction}`·식~`eq:lco-sigmaslot` 참조는 원문 그대로 인용 유지. 구체 부호값(LCO 충전=+1/방전=-1)은 삭제가 아니라 **인용 대상 식 안에 이미 전량 명시**되어 있어 정보 손실 없음(참조 1회로 확인 가능). $\xi\leftrightarrow1-\xi$ 불변성 진술 보존.
**문장 수**: 3 → 1 (67%)

### 6.3 (b) 연산 (L2476–2490)

**원문**:
```
평형 추종이면 $\dd\xi_j/\dd V$ 에 평형 기울기가
들어간다. LCO 전이 $j$ 의 평형 점유는 흑연 식~\eqref{eq:xieq} 에 분기 중심 $U_j^{\,d,\mathrm{cat}}$
(식~\eqref{eq:lco-Ubranch})을 넣은
$\xi_{\eq,j}=\{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j]\}^{-1}$ 이고,
$z_j\equiv\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j$ 로 종 항등식~\eqref{eq:belliden}
($\dd\xi_\eq/\dd z_j=\xi_\eq(1-\xi_\eq)$)과 연쇄율 $\dd z_j/\dd V=\sigma_d/w_j$ 를 곱하면
[식~\eqref{eq:lco-belliden}]
— $\xi(1-\xi)\ge0$ 라 봉우리 모양은 방향 불변$\cdot$양수이며, $\xi\leftrightarrow1-\xi$($\sigma_d$ 뒤집기)
에 대칭이다.
```

**교체문**:
```
평형 추종이면 $\dd\xi_j/\dd V$ 에 평형 기울기가 들어가며, LCO 전이 $j$ 의 평형 점유는 흑연 식~\eqref{eq:xieq}
에 분기 중심 $U_j^{\,d,\mathrm{cat}}$(식~\eqref{eq:lco-Ubranch})을 넣은
$\xi_{\eq,j}=\{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j]\}^{-1}$ 이고, $z_j\equiv\sigma_d(V-U_j^{\,d,
\mathrm{cat}})/w_j$ 로 종 항등식~\eqref{eq:belliden}($\dd\xi_\eq/\dd z_j=\xi_\eq(1-\xi_\eq)$)과 연쇄율
$\dd z_j/\dd V=\sigma_d/w_j$ 를 곱하면
[식~\eqref{eq:lco-belliden}]
— $\xi(1-\xi)\ge0$ 라 봉우리 모양은 방향 불변$\cdot$양수이며, $\xi\leftrightarrow1-\xi$($\sigma_d$ 뒤집기)에
대칭이다.
```

**근거**: 짧은 도입 문장("평형 추종이면...")을 다음 문장 도입절에 흡수.
**물리 보존 선언**: 평형 점유식, 분기 중심 대입, 종 항등식~eq:belliden, 연쇄율, 식~eq:lco-belliden, 봉우리 모양의 방향 불변·대칭성 전량 보존.
**문장 수**: 2 → 1 (50%)

### 6.4 (c) 중간식 (L2492–2499) — **무변경**
```
식~\eqref{eq:lco-belliden} 하나에서 전이 $j$ 봉우리의 위치$\cdot$
순높이$\cdot$면적이 전부 읽힌다:
[식~\eqref{eq:lco-peakobs}]
```
이미 1문장. 압축하지 않음.

### 6.5 (d) 박스 (L2500–2511)

**원문**:
```
(b)를 (a)에 넣으면 양극 전위 영역의 평형 기준선이 닫힌다:
[식~\eqref{eq:lco-eqpeak}]
흑연이 $\sim$0.085--0.21 V 에 네 봉우리를 남기듯, 이 식은 표~\ref{tab:lco-staging} 의 입력으로 세 봉우리를
남긴다 — T1 의 $\sim$3.90 V(MIT plateau), T2 의 $\sim$4.05 V, T3 의 $\sim$4.17--4.20 V(T2 와 한 쌍의 좁은
order--disorder 봉우리)이며, order--disorder 의 큰 $\Omega_j^\mathrm{cat}$ 가 spinodal gap
(식~\eqref{eq:lco-dUhys})을 키워 T2$\cdot$T3 의 분기를 흑연보다 날카롭게(좁은 한 쌍 peak 로) 만든다.
```

**교체문**:
```
(b)를 (a)에 넣으면 양극 전위 영역의 평형 기준선이 닫히며
[식~\eqref{eq:lco-eqpeak}]
흑연이 $\sim$0.085--0.21 V 에 네 봉우리를 남기듯 이 식은 표~\ref{tab:lco-staging} 의 입력으로 세 봉우리 —
T1 의 $\sim$3.90 V(MIT plateau), T2 의 $\sim$4.05 V, T3 의 $\sim$4.17--4.20 V(T2 와 한 쌍의 좁은
order--disorder 봉우리) — 를 남기고, order--disorder 의 큰 $\Omega_j^\mathrm{cat}$ 가 spinodal gap
(식~\eqref{eq:lco-dUhys})을 키워 T2$\cdot$T3 의 분기를 흑연보다 날카롭게(좁은 한 쌍 peak 로) 만든다.
```

**근거**: 두 문장을 "~닫히며 [식] ~남기고 ~만든다"의 단일 흐름으로 재접속(구조는 유지, 문장 경계만 재배치) — (a)/(c) 등 다른 박스 단락(이미 1문장)과 서술 밀도를 통일.
**물리 보존 선언**: 흑연 대조값($\sim$0.085–0.21V), T1/T2/T3 위치(각각 $\sim$3.90V, $\sim$4.05V, $\sim$4.17–4.20V), order-disorder 쌍봉 성질, spinodal gap 메커니즘(식~eq:lco-dUhys) 전량 보존.
**문장 수**: 2 → 1 (50%)

### 6.6 폭의 지위 (L2513–2517) — **무변경**
```
폭은 흑연과 같은 $w_j=n_jRT/F$(식~\eqref{eq:wbase}) 서식이되, pure-LCO 초기값에서 세
전이 모두 $\Omega_j^\mathrm{cat}>2RT$ 의 두-상 측에 놓이므로 그 폭은 \S\ref{sec:width} 이중지위의
\emph{두-상} 측 — 평형 예측이 아니라 broadening 이 정하는 현상학적 피팅 폭이다(\S\ref{sec:broadening};
어느 지위인지의 최종 판정은 피팅된 $\Omega_j^\mathrm{cat}$ 이 정하며, 도핑으로 $\Omega_j^\mathrm{cat}\le2RT$
로 닫히는 전이는 단상 측의 평형 예측 지위로 넘어간다 — \S\ref{sec:lco-hys} two-phase calibration).
```
이미 1문장(복합문)으로 조밀 — 추가 병합 시 물리 내용 손실 없이는 더 줄일 수 없어 압축하지 않음.

### 6.7 T1 의 온도 신호 (L2519–2524)

**원문**:
```
T1 의 위치는 \S\ref{sec:lco-electronic} 의 전자항이 $\Delta S_{\rxn,1}^\mathrm{cat}$
를 통해 $U_1(T)$ 의 \emph{온도 이동}에 기여하므로(식~\eqref{eq:lco-dUdT}), 다온도 dQ/dV 에서 T1 봉우리의
\emph{온도 이동률} $\partial U_1/\partial T$ 가 $T$ 에 선형으로 커지는 것이 전자항의 관측 신호다
($\Delta S_{e,1}\propto T$, \S\ref{sec:lco-Se} — 위치 자체가 $T$-선형이 아니라 \emph{이동률}이 $T$-선형,
곧 위치 이동은 $\propto T^2$, 식~\eqref{eq:U1T2}). 도핑은 \S\ref{sec:lco-hys} 대로 봉우리를
smear$\cdot$shift 시킨다($\Omega$ 는 gap$\cdot$smear 슬롯, $U_j^\mathrm{cat}$ 이동은 별도 슬롯).
```

**교체문**:
```
T1 의 위치는 \S\ref{sec:lco-electronic} 의 전자항이 $\Delta S_{\rxn,1}^\mathrm{cat}$ 를 통해 $U_1(T)$ 의
\emph{온도 이동}에 기여하므로(식~\eqref{eq:lco-dUdT}), 다온도 dQ/dV 에서 T1 봉우리의 \emph{온도 이동률}
$\partial U_1/\partial T$ 가 $T$ 에 선형으로 커지는 것이 전자항의 관측 신호이며($\Delta S_{e,1}\propto T$,
\S\ref{sec:lco-Se} — 위치 자체가 아니라 \emph{이동률}이 $T$-선형, 곧 위치 이동은 $\propto T^2$,
식~\eqref{eq:U1T2}), 도핑은 \S\ref{sec:lco-hys} 대로 봉우리를 smear$\cdot$shift 시킨다($\Omega$ 는
gap$\cdot$smear 슬롯, $U_j^\mathrm{cat}$ 이동은 별도 슬롯).
```

**근거**: 두 문장(온도 신호 / 도핑 효과)을 "~이며"로 병합 — 둘 다 "T1 봉우리를 무엇이 움직이는가"라는 한 `\textbf{}` 표제 아래의 두 갈래 서술이라 병합해도 단락 경계(구조)는 유지된다.
**물리 보존 선언**: $\Delta S_{e,1}\propto T$, 이동률 vs 위치의 구분($T$-선형 vs $\propto T^2$), 식~eq:U1T2, 도핑의 smear·shift 및 슬롯 분리($\Omega$ vs $U_j^\mathrm{cat}$) 전량 보존.
**문장 수**: 2 → 1 (50%)

### 6.8 sec:lco-peak 소계

| 단락 | 전 | 후 |
|---|---|---|
| (a) 출발 | 1 | 1 |
| ★방향 슬롯 | 3 | 1 |
| (b) 연산 | 2 | 1 |
| (c) 중간식 | 1 | 1 |
| (d) 박스 | 2 | 1 |
| 폭의 지위 | 1 | 1 |
| T1 의 온도 신호 | 2 | 1 |
| **소계** | **12** | **7** |

**sec:lco-peak 감축률**: (12−7)/12 = **41.7%**

---

## 7. 전체 요약

| 절 | 전 문장 | 후 문장 | 감축률 |
|---|---|---|---|
| sec:lco-electronic (절 도입부+lco-why+lco-Se+lco-gate) | 78 | 43 | 44.9% |
| — 그중 lco-gate (outlier) | 29 | 15 | 48.3% |
| sec:lco-peak | 12 | 7 | 41.7% |
| **두 절 합계** | **90** | **50** | **44.4%** |

- 목표(≥35%)를 모든 절/소절에서 상회하되, 예외 2곳: **★부호 규약**(lco-Se, 33%)과 **★$T^2$ 누적계수**(lco-Se, 25%) — 둘 다 "★최우선 결함 클래스" 지정 또는 부호/유도 사슬의 밀도가 높아 문장 병합보다 사슬 보존을 우선한 **의도적** 미달이며, lco-Se 소계 자체는 41.0%로 목표를 상회해 상쇄된다.
- 수식 환경(`\begin{equation}...\end{equation}`, `\boxed{}`, `\label{}`)은 어느 교체문에서도 변경하지 않았다.
- 모든 수치(부호 포함)·tier 라벨·인용은 각 교체문 안에 grep 가능한 형태로 재기입했다 — 임의 확인: `-16`, `0.085`, `13`, `0.85`, `0.05`, `0.94`, `0.75`, `1.1\,k_B`, `0.18\,k_B`, `-46`, `4\times10^{37}`, `0.026`, `0.03`, `tier A`, `tier B`, `motohashi2009`, `menetrier1999`, `reimers1992`, `reynier2004`, `ml2024` 전부 교체문에 잔존.

---

## 8. 최약점 (5줄)

1. **★부호 규약**(sec:lco-electronic §3.10)은 "★최우선 결함 클래스" 지정 단락이라 33%로 의도적 보수 압축 — 목표 35% 미달.
2. **★$T^2$ 누적계수**(§3.12)는 $1/2$ 인자 유도 디테일 보존을 우선해 25%에 그침 — lco-Se 소계(41%)로 상쇄.
3. `fig:lco-electronic` 캡션(L2447–2454)은 산문 압축 대상에서 제외 — 캡션 자체 압축 필요성은 별도 검토 필요.
4. lco-gate (iii) 폭 단락(4→1문장)처럼 4문장을 1개 복합문으로 합친 곳이 여러 건 — 가독성 낭독 검토 없이 채택 시 문장이 다소 길게 느껴질 위험.
5. ★방향 슬롯(sec:lco-peak §6.2)의 재설명 제거는 식~`eq:lco-sigmaslot` 1회 참조에 의존 — 로컬 자기완결성이 약간 감소(G-follow 트레이드오프).
