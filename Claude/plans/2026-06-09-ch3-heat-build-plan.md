# Chapter 3 (발열) 신규 작성 계획 — 절 단위 루프 · 최대 effort

## Summary
Ch3 = **흑연 음극의 발열**(heat generation): Ch1에서 \emph{입력}이던 온도 $T$ 가 실제로는 음극이 스스로 내는 열에서 \emph{생성}됨을 다룬다 — "$T$ 는 어디서 오는가". 내용 = \textbf{가역 entropic 열}($I\,T\,\partial U/\partial T$, Ch1 의 $\partial U_j/\partial T=\Delta S_j/sF$ 위)과 \textbf{비가역 소산열}($I\,\eta$, 분극$\cdot$지연), 그리고 \textbf{열 수지}($mc_p\dot T=Q_\mathrm{gen}-Q_\mathrm{loss}$)와 \textbf{$T\leftrightarrow$peak 되먹임}. 도착점 = Ch1/Ch2처럼 \emph{한 줄의 피팅 가능한 $Q_\mathrm{gen}$ 모델식 + 열 수지 + 데이터→파라미터→$T(t)$ 예측}. 작업은 박사님 누적 피드백 그대로: **절 단위 루프(절마다 빌드·정합), 최대 effort, NO Workflow(순차 master), 단일문건 규율, 부모-only 의존, 교과서 깊이+worked example, master 직접 손검, Codex 적대검수, result/ledger, auto-commit+push.** 파일 = `graphite_ica_ch3.tex`(신규), 절 번호 3.x, 식 3.x.

## Current Ground Truth
**확인된 사실(정찰 완료):**
- `Claude/docs/`: ch1.tex(24p, 완료)·ch2.tex(11p, 완료)·ch4.tex(반응속도론, 존재). **ch3.tex 없음** → 신규.
- ch4.tex 헤더: "Chapter 4 = 전기화학 반응속도론(미래 DFN 모듈). Ch1 기반."
- 의존 트리 메모리(`feedback_anode_fit_chapter_dependency_tree`)는 **swap 이전(stale)**: "new Ch2=반속, Ch3=발열(반속 기반), Ch4=히스" — 그러나 실제 파일은 박사님이 Ch2↔Ch4 swap → 현재 Ch2=히스·Ch4=반속. 따라서 메모리의 "발열=반속 기반"은 swap 후 "Ch4 기반"이 되어 \emph{번호 역전}(Ch3가 Ch4에 의존).
- 구 발열 장(`old/pre-restructure-2026-06-07-5ch/docs/graphite_ica_ch2.tex`) = 박사님 의도 범위: "가역 entropic 열 + 비가역 소산열을 **Ch1**(전하보존 1.1·logistic 1.11·완화 1.16) 위에서 유도", 동기 "Ch1에선 $T$ 입력이나 음극이 스스로 발열→$T$ 되먹임". (단 ver.N 파생일 수 있어 \emph{내용 포팅 금지}, 범위·동기만 참조.)
- Ch1 이 보유(인계만): $\partial U_j/\partial T=\Delta S_j/(sF)$(식 1.15, \emph{가역열 핵심}), $R_n$·$V_\app=V_n+s_I|I|R_n$(1.3), 완화 $L_{q,j}$(1.19), $V_n$·$V_{n,\OCV}$. Ch2: $R_n$ 분극·히스테리시스 loop. Ch4: 반응 과전압 $\eta_j$·$R_\mathrm{ct}$.

**미확인(Decision Gate D-0):** Ch3 의 \emph{부모 의존}(아래 Decisions Required).

**기존 결정(불변):** ver.3/ver.5 포팅 금지·발명 금지·단일문건 규율·부모-only 의존·Ch1 보유분 재유도 금지(인계만). 브랜치 `rb-rebuild-2026-05-30`, 직전 `5c5cbbe`.

## Phase Range
| Phase | 이름 | Steps | 절 |
|---|---|---:|---|
| 3.0 | Decision Gate — 의존·범위 확정 | 1 | (전제) |
| 3.1 | §서론 — $T$는 입력이 아니라 생성된다 | 2–3 | 서론 |
| 3.2 | §1 기호와 규약 | 4–5 | notation |
| 3.3 | §2 배경 — 에너지 수지·가역/비가역 분해(Bernardi) | 6–9 | bg |
| 3.4 | §3 가역 entropic 열 $q_\rev$ | 10–13 | rev |
| 3.5 | §4 비가역 소산열 $q_\irr$ | 14–17 | irr |
| 3.6 | §5 전이별 발열과 dQ/dV 연결 | 18–20 | perpeak |
| 3.7 | §6 열 수지와 국소 $T(t)$ | 21–24 | balance |
| 3.8 | §7 $T\leftrightarrow$peak 자기일관 되먹임 | 25–28 | feedback |
| 3.9 | §8 파라미터화 + §9 데이터→예측 | 29–32 | param/fit |
| 3.10 | §10 종합 모델식 — 한 줄 | 33–36 | master |
| 3.11 | 빌드·전수정합·Codex·커밋 | 37–39 | 전체 |

## Non-goals
- ver.3/ver.5/구 발열 장 \emph{내용 포팅 금지}(범위·동기만 참조, 본문은 신규 작성). 발명 금지(임의 모델 추가 X).
- Ch1 보유 결과(∂U_j/∂T·R_n·완화·logistic) \emph{재유도 금지} — 식 번호로 인계만.
- 단일문건 규율: §기호와규약에 "Chapter N" 언급 0, 인계-recap/전달(transmit)/논문식 결론 절 0(마지막은 \emph{도착 산출식}). 이전 장 식은 쓰이는 자리서 식 (1.x)/(2.x) inline만.
- DFN 수준 시뮬레이션 금지(박사님 목표 = \emph{피팅 가능}한 환원 열 모델). 공간 분해(1D 두께 방향) 도입은 Decision Gate 승인 시에만.
- 챕터 통째 배치 작성 금지(절 단위). Codex/·Archive·zip 미혼입. NO Workflow(순차 master 루프).

## Implementation Changes
- 신규: `Claude/docs/graphite_ica_ch3.tex`(절별 작성), 빌드 `graphite_ica_ch3.pdf`.
- Result: `Claude/results/PHASE_CH3_RESULT.md`(절별 누적). Ledger: `Claude/results/PHASE_CH3_EXECUTION_LEDGER.md`(12-col).

## Phase 3.0 — Decision Gate: 의존·범위 확정 (GATE_D0)
- **Step 1.** 아래 Decisions Required(D-0a/b/c)를 박사님이 확정. 그 전엔 §1+ 착수 X(load-bearing 전제 — `feedback_plan_premise_verification`). \emph{단, 박사님이 "권고안대로 GO" 하면 D-0a=A·D-0b=포함·D-0c=경량 채택하고 즉시 3.1로}.
- **Gate G3.0:** D-0a(부모)·D-0b(Ch2/Ch4 인계 범위)·D-0c(자기일관 방법론) 각 확정 기록.

## Phase 3.1 — §서론
- **Steps 2–3.** Ch1에서 $T$ 가 입력이었음(w_j=RT/F·Arrhenius)을 짚고, 실제론 음극이 발열→국소 $T$→되먹임을 동기로. 도착점(한 줄 $Q_\mathrm{gen}$ 식·열 수지·$T(t)$ 예측) thread. 앞 장 식은 (1.x) inline.
- **Gate G3.1:** 서론에 동기+도착점 thread 존재(grep), 단일문건 규율(Chapter-N 언급 0), 빌드 clean.

## Phase 3.2 — §1 기호와 규약
- **Steps 4–5.** 신규 기호 표만: $Q_\mathrm{gen}$(W or W/mol), $q_\rev,q_\irr$, $\eta$(과전압), $c_p$(열용량), $h$(대류계수)·$A_s$(면적)·$T_\amb$, $m$(질량), $\tau_\Th$(열 시상수) 등 + 상수. Chapter-N 언급 0.
- **Gate G3.2:** §1 새 기호 표만, Chapter-N 0(grep), 단위 일관, 빌드 clean.

## Phase 3.3 — §2 배경: 에너지 수지·가역/비가역 분해
- **Steps 6–9.** 1법칙(전극 제어부피): 입력 전기일 − 저장 화학에너지 = 열. Bernardi 분해 $Q_\mathrm{gen}=I(V_\app-V_{n,\OCV})-I\,T\,\dfrac{\partial V_{n,\OCV}}{\partial T}$ 유도(비약 0): 첫 항=과전압 소산(비가역, $\ge0$), 둘째=entropic(가역, 부호 가변). 차원·부호 검산.
- **Gate G3.3:** Bernardi 분해 식 유도(중간단계)·부호·차원 손검 기록, 빌드 clean.

## Phase 3.4 — §3 가역 entropic 열 $q_\rev$
- **Steps 10–13.** $q_\rev=-I\,T\,\partial V_{n,\OCV}/\partial T$. $\partial V_{n,\OCV}/\partial T$ 를 Ch1 의 전이별 $\partial U_j/\partial T=\Delta S_j/(sF)$(식 1.15)와 평형 가중 $\dd\xi_{\eq,j}/\dd V$ 로 전개(인계, 재유도 X). 충/방전 부호(발열 vs 흡열), 전이별 기여. worked example(대표 $\Delta S_j$→mV·K$^{-1}$→W).
- **Gate G3.4:** $q_\rev$ 가 Ch1 1.15 위에서 전개·부호·worked 수치 손검, 빌드 clean.

## Phase 3.5 — §4 비가역 소산열 $q_\irr$
- **Steps 14–17.** $q_\irr=I\,\eta$, $\eta=V_\app-V_{n,\OCV}$. 분해: ohmic $I^2R_n$(Ch1 1.3) + 완화/지연 소산(Ch1 1.19 꼬리) + (D-0b 승인 시) 반응 과전압 $\eta_j$(Ch4)·히스테리시스 loop 손실(Ch2). $\eta I\ge0$ 항상 발열 검산. worked example.
- **Gate G3.5:** $q_\irr$ 분해·$\ge0$·worked 수치, 인계 범위 D-0b 준수, 빌드 clean.

## Phase 3.6 — §5 전이별 발열과 dQ/dV 연결
- **Steps 18–20.** 발열을 전이 $j$ 별로($q_\rev,j+q_\irr,j$) 묶어 dQ/dV peak 구조와 연결: peak 진행 중 entropic 열이 어디서 부호를 바꾸는지, 꼬리(지연)가 어디서 소산을 키우는지.
- **Gate G3.6:** 전이별 발열·dQ/dV 연결 서술·정합, 빌드 clean.

## Phase 3.7 — §6 열 수지와 국소 $T(t)$
- **Steps 21–24.** $mc_p\dfrac{\dd T}{\dd t}=Q_\mathrm{gen}-hA_s(T-T_\amb)$(Newton 냉각). 열 시상수 $\tau_\Th=mc_p/(hA_s)$, 정상상태 $\Delta T_\infty=Q_\mathrm{gen}/(hA_s)$. 차원·극한($h\to\infty$ 등온, $h\to0$ 단열) 검산. worked example(0.2C $Q_\mathrm{gen}$→$\Delta T$).
- **Gate G3.7:** 열 수지 ODE·$\tau_\Th$·$\Delta T_\infty$·극한·worked 손검, 빌드 clean.

## Phase 3.8 — §7 $T\leftrightarrow$peak 자기일관 되먹임
- **Steps 25–28.** $T$ → Ch1 의 $w_j(T)=RT/F$·$k_j(T)$ → peak·$\eta$ → $Q_\mathrm{gen}$ → $T$ 의 닫힌 loop. 약/강 되먹임 판정, 안정성. (D-0c 승인 시) 박사님 JCP 147(14)144111 ref 6,7 자기일관 방법론을 P3 7항목 양식으로 기록·매핑. 폭주(열 runaway) 경계는 정성.
- **Gate G3.8:** 되먹임 loop 식·안정성 조건·(ref 6,7 채택 시 7항목) 기록, 빌드 clean.

## Phase 3.9 — §8 파라미터화 + §9 데이터→예측
- **Steps 29–32.** 피팅 파라미터: Ch1 기지 $\{U_j,\partial U_j/\partial T,R_n,k_j\}$ + 신규 \emph{열} $\{c_p, hA_s\}$($T_\amb$ 기지). 데이터→파라미터: $\partial U_j/\partial T$=전위측정(potentiometric entropy)·$c_p,hA_s$=열량계/온도 transient(ARC·등온). 예측: 임의 율·$T_\amb$서 $T(t)$.
- **Gate G3.9:** 파라미터 표·데이터 매핑·비순환 순서, 빌드 clean.

## Phase 3.10 — §10 종합 모델식 — 한 줄
- **Steps 33–36.** 신규 절: \textbf{master} $Q_\mathrm{gen}=I[(V_\app-V_{n,\OCV})-T\,\partial V_{n,\OCV}/\partial T]$ + 열 수지 $mc_p\dot T=Q_\mathrm{gen}-hA_s(T-T_\amb)$ (boxed) + 파라미터 표 + 데이터→파라미터→$T(t)$ 예측 결론 박스. 환원검산(등온 극한·$I\to0$). 단일문건 규율(결론 아닌 도착 산출식).
- **Gate G3.10:** master 식 boxed·파라미터·데이터·예측 4요소·환원검산 손검, 빌드 clean.

## Phase 3.11 — 빌드·Codex·커밋
- **Steps 37–39.** xelatex 2-pass overfull 0·undefined 0; Ch1↔Ch3 인계식(1.3·1.15·1.19) 원문 대조; Codex foreground 적대검수(발열 물리·Bernardi 부호·자기일관, MAJOR 0, Ch1 원문 대조); result+ledger; ch3 tex+pdf 명시 스테이징 커밋·푸쉬.
- **Gate G3.11:** 빌드 0/0, Codex MAJOR 0(시정 후), Ch1 인계 대조표, git 해시.

## Implementation Interfaces
**IF-1 (Ch3 발열 master):**
$$\boxed{\;Q_\mathrm{gen}=\underbrace{I\,(V_\app-V_{n,\OCV})}_{q_\irr\ge0\ \text{(과전압 소산)}}\;-\;\underbrace{I\,T\,\frac{\partial V_{n,\OCV}}{\partial T}}_{q_\rev\ \text{(가역 entropic)}}\;,\qquad
mc_p\frac{\dd T}{\dd t}=Q_\mathrm{gen}-hA_s(T-T_\amb)\;}$$
$V_\app-V_{n,\OCV}=\eta$(과전압; ohmic $|I|R_n$ + 완화 지연 + 옵션 $\eta_j$), $\dfrac{\partial V_{n,\OCV}}{\partial T}=\sum_j\dfrac{\partial U_j}{\partial T}\dfrac{\dd\xi_{\eq,j}}{\dd q}\Big/\dfrac{\dd V_{n,\OCV}}{\dd q}$ 류(Ch1 식 1.15 위). 파라미터: Ch1 기지 $\{U_j,\partial U_j/\partial T,R_n,k_j\}$ + 신규 $\{c_p,hA_s\}$.
**IF-2 (Result/Ledger):** `feedback_phase_execution_loop` 11항목·12-col.

## Test Plan
- 빌드 2-pass: overfull 0·undefined 0, 페이지 수.
- **손검(master 직접)**: Bernardi 분해 부호·차원, $q_\irr\ge0$, 등온/단열 극한, $\tau_\Th$·$\Delta T_\infty$ 차원, worked example 수치 재현.
- 단일문건 규율 grep(Chapter-N 0, 인계/전달/결론 절 0). Ch1 인계식(1.3/1.15/1.19) 원문 대조표.
- Codex foreground 적대검수 1회(발열 물리), Ch1 원문 대조. Read Coverage.

## Assumptions
- A1: Ch3 = \emph{lumped}(집중) 열 모델(공간 균일 $T$) — DFN式 공간 분해 X(피팅 목표). 분해는 D-0 승인 시만.
- A2: $\eta=V_\app-V_{n,\OCV}$ 가 비가역 소산 전부를 담는다(Bernardi 표준). $c_p,hA_s$ 는 유효(셀/전극) 집중값.
- A3: worked example 대표값(예 $\partial U_j/\partial T\sim-0.1$ mV/K, $R_n$, 0.2C)은 규모 예시(실측 아님) 명시.

## Decisions Required (Phase 3.0 — GATE_D0)
> 항목당 내용·근거·영향 명시(`feedback_decision_request_clarity`). 박사님 "권고안대로 GO" 시 권고로 확정.
- **D-0a (부모 의존):**
  - \textbf{(A) 권고 — Ch1 기반}: 가역열=∂U_j/∂T(1.15), 비가역열=R_n·완화(1.3/1.19). 구 발열 장과 동일, 피팅 모델에 충분, 번호 역전 없음.
  - (B) Ch4(반속) 기반: 비가역열의 과전압을 BV $\eta_j$ 로 — 메모리 "반속 기반"이나 \emph{Ch3→Ch4 forward 의존}(번호 역전; 재배열 필요).
  - (C) Ch1+Ch2+Ch4 다부모: 가역(Ch1)+히스 손실(Ch2)+반응 과전압(Ch4) — "부모-only" 규율과 충돌.
  - \emph{권고 A}. 단 비가역열에 Ch4 $\eta_j$·Ch2 히스 손실을 \emph{쓰이는 자리 inline 인계}로 옵션 추가(D-0b).
- **D-0b (Ch2/Ch4 인계 범위):** 비가역열 $q_\irr$ 에 (i) Ch1 $R_n$+완화만, (ii) +Ch2 히스테리시스 loop 손실, (iii) +Ch4 반응 과전압 $\eta_j$. \emph{권고 (ii)+(iii) 옵션 inline}(부모는 Ch1, 형제는 point-of-use 인용).
- **D-0c (자기일관 방법론):** $T\leftrightarrow$peak 되먹임에 박사님 JCP 147(14)144111 ref 6,7 자기일관 방법(CLAUDE.md P1/P3)을 (i) 경량(정성 안정성), (ii) 정식(7항목 매핑·수치해법) 중. \emph{권고 (i) 경량 — 본 장은 발열 유도, 정식 자기일관 수치는 후속/피팅 장}.

## Correction History
- 2026-06-09 v1: 작성. 박사님 "Ch3 상세 계획서, 누적 작업방식·피드백 참고". 정찰로 의존 트리 메모리 stale(swap 전) 적발 → 구 발열 장(Ch1 기반)·물리(Bernardi)로 재baseline. 의존을 Decision Gate D-0로 명시(추측 금지, `feedback_plan_premise_verification`). 누적 피드백(절 단위 루프·최대 effort·NO Workflow·단일문건·교과서 깊이·master 식·Codex·손검·result/ledger·auto-commit) 전부 반영. GATE_D0 확정(또는 "권고대로 GO") 시 3.1부터 마지막까지 연속.
