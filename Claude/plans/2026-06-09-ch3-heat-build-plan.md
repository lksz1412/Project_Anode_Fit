# Chapter 3 (발열) 신규 작성 계획 v2 — Ch1+Ch2 기반 · 완전 재작성 · 절 단위 루프 · 최대 effort

## Summary
Ch3 = **흑연 음극의 발열**(heat generation), **Ch1 + Ch2 위에 완전 재작성**. Ch1에서 \emph{입력}이던 $T$ 가 실제로는 음극이 스스로 내는 열에서 \emph{생성}된다("$T$ 는 어디서 오는가"). 발열은 세 갈래:
1. **가역 entropic 열** $q_\rev=-I\,T\,\partial V_{n,\OCV}/\partial T$ — Ch1 의 $\partial U_j/\partial T=\Delta S_j/(sF)$(식 1.15) 위.
2. **히스테리시스 소산열** $q_\hys=I\sum_j\tfrac12\gamma_j\Delta U_j^\hys$ — \textbf{Ch2 의 분기 갈림(ΔU_hys)이 가역 OCV 위·아래로 갈려 생기는 \emph{율 무관}(I→0 잔존) 열역학적 소산}. \textbf{본 장이 Ch2 위에 서는 핵심 이유.}
3. **분극 소산열** $q_\pol=I\,\eta_\pol$($\eta_\pol=|I|R_n+$완화 지연) — Ch2 분극, 율 의존(I→0 소멸).
그 위에 **열 수지** $mc_p\dot T=Q_\mathrm{gen}-hA_s(T-T_\amb)$ 와 **$T\leftrightarrow$peak/gap 자기일관 되먹임**($T$ 가 $w_j,k_j$ 뿐 아니라 $\Omega_j$ 통해 $\Delta U_j^\hys$ 까지 바꿈; $T_{c,j}=\Omega_j/2R$). 도착점 = Ch1/Ch2처럼 \emph{한 줄의 피팅 가능한 $Q_\mathrm{gen}$ 모델식 + 열 수지 + 데이터→파라미터→$T(t)$ 예측}.
방식 = 박사님 누적 피드백 그대로: **완전 재작성(구 발열 장 포팅 금지)·전문 검수(Ch1·Ch2 인계식 전수 원문 대조)·절 단위 루프(절마다 빌드·정합)·최대 effort·NO Workflow(순차 master)·단일문건 규율·부모-only 의존·교과서 깊이+worked example·master 직접 손검·Codex 적대검수·result/ledger·auto-commit+push.** 파일 = `graphite_ica_ch3.tex`(신규), 절 3.x, 식 3.x.

## Current Ground Truth
**확인된 사실(정찰 완료):**
- `Claude/docs/`: ch1.tex(24p, 완료·max-effort 검증)·ch2.tex(11p, 완료·max-effort 검증)·ch4.tex(반응속도론, 존재). **ch3.tex 없음** → 신규.
- **박사님 결정(6-09, 본 지시): Ch3 = Ch1+Ch2 기반 재편성, 완전 재작성, 전문 검수.** 의존 트리 1→2→{3,4}와 정합(Ch3 부모=Ch2, 전이적 Ch1). Ch4(반속)는 \emph{형제}라 의존 X.
- 구 발열 장(`old/.../graphite_ica_ch2.tex`)은 **Ch1 기반에 그쳐 재편성 대상** — 박사님 "지금은 Ch1 기반으로만 작성되어 있을 것, Ch1·2 기반으로 재편성." 범위·동기만 참조, \emph{내용 포팅 금지}.
- Ch1 인계(재유도 X, 원문 대조): $\partial U_j/\partial T=\Delta S_j/(sF)$(1.15, \emph{가역열 핵심}), $V_\app=V_n+s_I|I|R_n$(1.3), $V_{n,\OCV}$·$\dd\xi_{\eq,j}/\dd V$(1.13), 완화 $L_{q,j}$(1.19).
- Ch2 인계(재유도 X, 원문 대조): 분기 중심 $U_j^{\dis/\chg}=U_j\pm\tfrac12\gamma_j\Delta U_j^\hys$·$\Delta U_j^\hys=\tfrac{2}{sF}[\Omega_j u_j-2RT\,\mathrm{artanh}\,u_j]$(2.x)·$T_{c,j}=\Omega_j/2R$·$\Delta V_\pol=2|I|R_n$·가역 기준(binodal/mean) $V_{n,\OCV}^\rev$·loop 면적 $\oint V\dd q$.

**기존 결정(불변):** ver.3/ver.5 포팅 금지·발명 금지·단일문건 규율·부모-only(Ch4 형제 의존 X)·Ch1/Ch2 보유분 재유도 금지(인계만). 브랜치 `rb-rebuild-2026-05-30`, 직전 `3a2a7af`.

## Phase Range
| Phase | 이름 | Steps | 절 | 기반 |
|---|---|---:|---|---|
| 3.1 | §서론 — $T$는 생성된다 + 히스가 열원 | 1–2 | 서론 | Ch1·Ch2 |
| 3.2 | §1 기호와 규약 | 3–4 | notation | — |
| 3.3 | §2 배경 — 에너지 수지·세 갈래 분해(Bernardi+히스) | 5–9 | bg | Ch1·Ch2 |
| 3.4 | §3 가역 entropic 열 $q_\rev$ | 10–13 | rev | Ch1(1.15) |
| 3.5 | §4 \textbf{히스테리시스 소산열} $q_\hys$ (율 무관) | 14–18 | hys | Ch2(ΔU_hys·loop) |
| 3.6 | §5 분극 소산열 $q_\pol$ (율 의존) | 19–22 | pol | Ch2(R_n)·Ch1(1.19) |
| 3.7 | §6 전이별 발열·dQ/dV·분기 연결 | 23–25 | perpeak | Ch1·Ch2 |
| 3.8 | §7 열 수지와 국소 $T(t)$ | 26–29 | balance | — |
| 3.9 | §8 $T\leftrightarrow$peak/gap 자기일관 되먹임 | 30–33 | feedback | Ch1·Ch2 |
| 3.10 | §9 파라미터화 + §10 데이터→예측 | 34–37 | param/fit | — |
| 3.11 | §11 종합 모델식 — 한 줄 | 38–41 | master | — |
| 3.12 | 빌드·전수정합(Ch1·Ch2)·Codex·커밋 | 42–44 | 전체 | — |

## Non-goals
- **완전 재작성** — 구 발열 장·ver.3/ver.5 \emph{내용 포팅 금지}(범위·동기만, 본문 신규). 발명 금지.
- Ch1·Ch2 보유 결과(∂U_j/∂T·ΔU_hys·R_n·logistic·완화) \emph{재유도 금지} — 식 번호 인계만(쓰이는 자리 inline).
- **Ch4(반속) 의존 금지**(형제). 반응 과전압 BV 도입 X — 비가역열은 Ch2 의 $R_n$·분기·loop 로 충분(피팅 목표).
- 단일문건 규율: §기호규약 Chapter-N 0, 인계-recap/전달/논문식 결론 절 0(마지막은 도착 산출식).
- DFN式 공간 분해 금지(lumped 열 모델). 챕터 통째 배치 작성 금지(절 단위). Codex/·Archive·zip 미혼입. NO Workflow.

## Implementation Changes
- 신규: `Claude/docs/graphite_ica_ch3.tex`(절별), 빌드 `graphite_ica_ch3.pdf`.
- Result: `Claude/results/PHASE_CH3_RESULT.md`(절별 누적, Read Coverage에 Ch1·Ch2 대조 행 범위 명시). Ledger: `PHASE_CH3_EXECUTION_LEDGER.md`(12-col).

## Phase 3.1 — §서론
- **Steps 1–2.** (a) Ch1에서 $T$ 입력이었음, 실제론 발열→국소 $T$→되먹임. (b) \textbf{충방전 히스테리시스(Ch2)가 가역 OCV 위·아래로 갈려 그 차가 \emph{율 무관} 열로 소산}됨을 동기에 명시(Ch2 위에 서는 이유). 도착점(한 줄 $Q_\mathrm{gen}$·열 수지·$T(t)$) thread. 앞 장 식 (1.x)/(2.x) inline.
- **Gate G3.1:** 서론에 (발열 동기 + 히스 열원 + 도착점 thread) 존재(grep), Chapter-N 언급 0, 빌드 clean.

## Phase 3.2 — §1 기호와 규약
- **Steps 3–4.** 신규 기호: $Q_\mathrm{gen},q_\rev,q_\hys,q_\pol$, $\eta_\hys,\eta_\pol$, $c_p,h,A_s,T_\amb,m,\tau_\Th$, $V_{n,\OCV}^\rev$(가역 기준). Chapter-N 0.
- **Gate G3.2:** 새 기호 표만, Chapter-N 0(grep), 단위 일관, 빌드 clean.

## Phase 3.3 — §2 배경: 에너지 수지·세 갈래 분해
- **Steps 5–9.** 1법칙(전극 제어부피)→Bernardi $Q_\mathrm{gen}=I(V_\app-V_{n,\OCV}^\rev)-I\,T\,\partial V_{n,\OCV}^\rev/\partial T$, \emph{가역 기준을 Ch2 의 참 평형}(binodal/mean, gap-less)으로 둠. 그러면 $V_\app-V_{n,\OCV}^\rev=\eta_\hys+\eta_\pol$ 로 \textbf{히스(율 무관)+분극(율 의존)}이 자연 분리. 차원·부호($q_\irr\ge0$) 검산.
- **Gate G3.3:** Bernardi+히스 분리 유도(중간단계)·부호·차원 손검, Ch2 가역 기준 정합, 빌드 clean.

## Phase 3.4 — §3 가역 entropic 열 $q_\rev$
- **Steps 10–13.** $q_\rev=-I\,T\,\partial V_{n,\OCV}^\rev/\partial T$, $\partial V^\rev/\partial T$ 를 Ch1 전이별 $\partial U_j/\partial T$(1.15)·평형 가중으로 전개(인계). 충/방전·발열 vs 흡열 부호, worked example(대표 $\Delta S_j$→W).
- **Gate G3.4:** Ch1 1.15 위 전개·부호·worked 손검, 빌드 clean.

## Phase 3.5 — §4 히스테리시스 소산열 $q_\hys$ (본 장 핵심, 율 무관)
- **Steps 14–18.** 분기 이탈 $\eta_{\hys,j}=V_\app^b-V_{n,\OCV}^\rev=\tfrac12\gamma_j\Delta U_j^\hys$(Ch2 2.x)에서 $q_\hys=I\sum_j\tfrac12\gamma_j\Delta U_j^\hys$. \emph{단위 전하당} $\tfrac12\gamma_j\Delta U_j^\hys$ 라 율 무관(I→0 잔존). 한 cycle loop 면적 $\oint V\dd q=\sum_j\gamma_j\Delta U_j^\hys Q_j$ 와 등가 검산. $\Delta U_j^\hys(\Omega_j,T)$ 의 $T$ 의존(가열→gap↓→히스열↓, $T_{c,j}=\Omega_j/2R$). worked example(γΔU_hys≈32 mV→W).
- **Gate G3.5:** $q_\hys$=Ch2 ΔU_hys 위 유도·loop 면적 등가·율 무관·$T$ 의존·worked 손검, Ch2 식 원문 대조, 빌드 clean.

## Phase 3.6 — §5 분극 소산열 $q_\pol$ (율 의존)
- **Steps 19–22.** $q_\pol=I\,\eta_\pol$, $\eta_\pol=|I|R_n$(Ch2 분극, 1.3 형) + 완화 지연 소산(Ch1 1.19 꼬리). $\ge0$·$I\to0$ 소멸. 히스(율 무관)와 \emph{분리}됨을 강조(데이터서 율 외삽으로 가름 — Ch2 §분극 논리 인계). worked example.
- **Gate G3.6:** $q_\pol$ 분해·율 의존·히스와 분리·worked 손검, 빌드 clean.

## Phase 3.7 — §6 전이별 발열·dQ/dV·분기 연결
- **Steps 23–25.** 발열을 전이 $j$·분기 $b$ 별로 묶어 dQ/dV peak·분기 구조(Ch1 peak + Ch2 분기 갈림)와 연결: entropic 열 부호 전환 위치, 히스열이 분기 갈림에 비례, 꼬리 소산.
- **Gate G3.7:** 전이별·분기별 발열·dQ/dV 연결·Ch1·Ch2 정합, 빌드 clean.

## Phase 3.8 — §7 열 수지와 국소 $T(t)$
- **Steps 26–29.** $mc_p\dot T=Q_\mathrm{gen}-hA_s(T-T_\amb)$, $\tau_\Th=mc_p/(hA_s)$, $\Delta T_\infty=Q_\mathrm{gen}/(hA_s)$. 등온($h\to\infty$)·단열($h\to0$) 극한·차원·worked example(0.2C→$\Delta T$).
- **Gate G3.8:** 열 수지 ODE·$\tau_\Th$·$\Delta T_\infty$·극한·worked 손검, 빌드 clean.

## Phase 3.9 — §8 $T\leftrightarrow$peak/gap 자기일관 되먹임
- **Steps 30–33.** $T$ → Ch1 $w_j(T),k_j(T)$ \emph{및} Ch2 $\Omega_j/T$ 통한 $\Delta U_j^\hys(T)$ → peak·$\eta_\hys$·$\eta_\pol$ → $Q_\mathrm{gen}$ → $T$ 닫힌 loop. 약/강 되먹임·안정성(가열→히스열↓ 음의 되먹임 vs 분극열 양의 되먹임). (D-0c 경량) 정성 안정성; 정식 자기일관 수치(JCP ref 6,7)는 피팅/후속 장 표기. 열 runaway 경계 정성.
- **Gate G3.9:** 되먹임 loop 식(히스·분극 두 경로)·안정성 정성·정합, 빌드 clean.

## Phase 3.10 — §9 파라미터화 + §10 데이터→예측
- **Steps 34–37.** 피팅 파라미터: Ch1·Ch2 기지 $\{U_j,\partial U_j/\partial T,\Omega_j,\gamma_j,R_n,k_j\}$ + 신규 \emph{열} $\{c_p,hA_s\}$. 데이터→파라미터: $\partial U_j/\partial T$=전위측정 entropy·$\Omega_j,\gamma_j$=저율 충방전 gap(Ch2)·$c_p,hA_s$=열량계/온도 transient(ARC·등온). 비순환 순서. 예측: 임의 율·$T_\amb$서 $T(t)$.
- **Gate G3.10:** 파라미터 표·데이터 매핑·비순환·예측, 빌드 clean.

## Phase 3.11 — §11 종합 모델식 — 한 줄
- **Steps 38–41.** master(IF-1) boxed + 열 수지 + 파라미터 표 + 데이터→파라미터→$T(t)$ 예측 결론 박스 + 환원검산(히스 0=$\Omega\le2RT$, 등온, $I\to0$=히스만 잔존). 단일문건 규율(도착 산출식).
- **Gate G3.11:** master 4요소·환원검산(특히 \emph{$I\to0$서 $q_\hys$ 만 잔존} 손검), 빌드 clean.

## Phase 3.12 — 빌드·Codex·커밋
- **Steps 42–44.** 2-pass overfull 0·undefined 0; \textbf{Ch1·Ch2 인계식 전수 원문 대조표}(1.3·1.13·1.15·1.19·2.x ΔU_hys·R_n); Codex foreground 적대검수(Bernardi 부호·히스열 율무관·되먹임, MAJOR 0, Ch1·Ch2 원문 대조); result+ledger; ch3 tex+pdf 커밋·푸쉬.
- **Gate G3.12:** 빌드 0/0, Codex MAJOR 0(시정 후), Ch1·Ch2 인계 대조표, git 해시.

## Implementation Interfaces
**IF-1 (Ch3 발열 master, Ch1+Ch2 기반):**
$$\boxed{\;Q_\mathrm{gen}=I\Big[\underbrace{\textstyle\sum_j\tfrac12\gamma_j\Delta U_j^\hys}_{\eta_\hys\ \text{(히스, 율무관)}}+\underbrace{|I|R_n+\text{lag}}_{\eta_\pol\ \text{(분극, 율의존)}}\Big]-\underbrace{I\,T\,\frac{\partial V_{n,\OCV}^\rev}{\partial T}}_{q_\rev\ \text{(가역 entropic)}}\;,\quad
mc_p\dot T=Q_\mathrm{gen}-hA_s(T-T_\amb)\;}$$
$\Delta U_j^\hys=\tfrac{2}{sF}[\Omega_j u_j-2RT\,\mathrm{artanh}\,u_j]$(Ch2), $\partial V_{n,\OCV}^\rev/\partial T$=Ch1 $\partial U_j/\partial T$(1.15) 평형 가중. 파라미터: Ch1·Ch2 기지 $\{U_j,\partial U_j/\partial T,\Omega_j,\gamma_j,R_n,k_j\}$ + 신규 $\{c_p,hA_s\}$.
**IF-2 (Result/Ledger):** `feedback_phase_execution_loop` 11항목·12-col, Read Coverage에 Ch1·Ch2 대조 범위.

## Test Plan
- 빌드 2-pass: overfull 0·undefined 0, 페이지 수.
- **손검(master 직접)**: Bernardi 부호·차원, $q_\hys$ 율 무관(I→0 잔존)·loop 면적 등가, $q_\pol$ I→0 소멸, $q_\rev$ 부호, $\tau_\Th$·$\Delta T_\infty$ 차원, 되먹임 부호, worked example 수치 재현.
- **전문 검수**: Ch1·Ch2 인계식(1.3/1.13/1.15/1.19/ΔU_hys/R_n) \emph{전수 원문 대조표}.
- 단일문건 규율 grep. Codex foreground 1회. Read Coverage(Ch1·Ch2 대조 행 명시).

## Assumptions
- A1: lumped 열 모델(공간 균일 $T$). DFN 공간 분해 X.
- A2: 가역 기준 $V_{n,\OCV}^\rev$ = Ch2 의 참 평형(binodal/Maxwell mean, gap-less). 그 위 분기 이탈이 히스 소산.
- A3: $q_\hys$ = 분기 이탈 $\tfrac12\gamma_j\Delta U_j^\hys$ × $I$ — 단위 전하당 율 무관(Ch2 열역학 히스의 발열 표현). loop 면적 $\oint V\dd q=\sum\gamma_j\Delta U_j^\hys Q_j$ 와 한 cycle 등가.
- A4: worked example 대표값(∂U_j/∂T·Ω_j·R_n·0.2C)은 규모 예시(실측 아님) 명시.

## Decisions Required (경량 — D-0a/b 확정됨)
- **D-0a (부모): 확정 = Ch1+Ch2**(박사님 6-09 지시). Ch4 형제 의존 X.
- **D-0b (비가역열 범위): 확정 = Ch1 $R_n$+완화 + Ch2 히스 loop**(Ch4 BV X).
- **D-0c (자기일관): 권고 (i) 경량**(정성 안정성; 정식 ref 6,7 수치는 피팅/후속 장). 박사님 (ii) 정식 원하면 §8에 7항목 매핑 추가.

## Correction History
- 2026-06-09 v1→v2: 박사님 "Ch3는 Ch1+2 기반 재편성, 완전 재작성, 전문 검수" 수용. v1의 Decision Gate D-0a(부모 미정)를 \textbf{Ch1+Ch2로 확정}, 비가역열을 \textbf{히스테리시스 소산(Ch2 ΔU_hys, 율 무관) + 분극(율 의존)}으로 재편(v1은 분극 위주). 가역 기준을 Ch2 참 평형으로. Ch4 형제 의존 명시 배제. 누적 피드백(절 단위 루프·최대 effort·NO Workflow·단일문건·교과서 깊이·master 식·Codex·손검·전수 원문 대조·result/ledger·auto-commit) 전부 반영. GO 시 3.1부터 마지막까지 연속.
