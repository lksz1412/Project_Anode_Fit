# Phase A — 폰 통합본 8종 장별 적대 재검수 Result

> **소급 작성(2026-05-30)**: 본 Phase 는 2026-05-30 세션에서 실행됐으나 result 문건이 즉시
> 저장되지 않았다(사용자 지적). 컴팩션 환각 방지를 위해 대화 기록 기반으로 소급 기록한다.
> 본 문건은 RB 계획서(`2026-05-30-undergrad-rederivation-rebuild-plan.md`) 의 입력 결함표 근거.

## Summary
폰 브랜치(`origin/claude/chapter-1-physics-logic-WD1R5`)에서 가져온 통합본 6장(consolidated_ch1~6)을
독립 적대(adversarial) sub-agent 6개로 각각 전수 정독·재유도 검수. 폰의 "10-pass 통과" 자기검수표가
놓친 결함 다수 적발(CRITICAL 2, HIGH 다수). 빌드는 정합이나 물리 grounding 층에 실질 결함.

## Step Range
RB 계획 이전의 사전 감사 단계(계획서 Current Ground Truth 의 입력). 정식 cumulative step 부여 전
(pre-RB audit). RB 본작업 step 은 Phase 0.1 = step 1 부터.

## Inputs (실제 검수 대상, 전수 정독)
- `Claude/docs/graphite_ica_consolidated_ch1.tex` (886줄)
- `Claude/docs/graphite_ica_consolidated_ch2.tex` (488줄)
- `Claude/docs/graphite_ica_consolidated_ch3.tex` (503줄)
- `Claude/docs/graphite_ica_consolidated_ch4.tex` (434줄)
- `Claude/docs/graphite_ica_consolidated_ch5.tex` (424줄)
- `Claude/docs/graphite_ica_consolidated_ch6.tex` (405줄)
- 대조: `graphite_ica_charge_balance_ver1_rechecked2.tex`, `graphite_ica_chapter1.tex`(Ch1 검수 시)

## Read Coverage
각 sub-agent 가 담당 장 \emph{전수 정독}(head→tail). Ch1 검수 agent 는 대조본 ver1_rechecked2 도
전수. 검수 agent 별 tool_uses·duration 은 대화 로그에 기록(Ch1: 27 tool_uses, Ch3: 80, Ch6: 77 등).

## 장별 발견 결함 (Files 검수 결과 — 핵심)

### Ch1 (CRIT 0 / HIGH 1)
- **[HIGH] closure 비선형성 귀속 오류**: `eq:volterra`+§11 단계0 이 "비선형성은 오직 $\Theta_\eq$ 에"
  라 단언하나 kernel $\mathcal K$($A_L$ 경유)도 $V_n(\Theta)$ 의존 → 동결 가정 누락(§8.1 과 충돌).
- [MED] $Q_p$ 기호표 단위 무차원 오기(실제 C); per-transition spectrum 단일 $A_L$ 붕괴 가정 미명시;
  JCP2017(Refs6/7) bibitem 부재; AL ledger 본체 부재(전 장 공통).

### Ch2 (CRIT 0 / HIGH 5+)
- **내 직전 chapter2 의 CRITICAL(2배감쇠 spectrum 일반화, C1·H1·H2·H3)은 이 consolidated_ch2 엔 부재** → 재발 없음(주장 자체가 다른 버전).
- **[HIGH] $\dot Q_\rlx$ 셋째항 double-counting 미차단**(이 문서 최강조 원칙인데 자기 분해식에 구멍).
- **[HIGH] $q_\irr\ge0$ 양정치성** 다중-transition 항별 부호 비약(de Groot–Mazur 는 합만 보장).
- [MED] $s_{\phi,j}$ 부호 관계식 처리 불일치; h_bg 정의 모호; reynier tier 과대.

### Ch3 (CRIT 0 / HIGH 3)
- **[HIGH] "Level A=Level B" 과대진술**(실제론 정상 target $\xi_\ss=\xi_\eq$ 만 일치, mobility 의 $\mathcal A$-의존은 비대칭).
- **[HIGH] BV $\alpha\leftrightarrow\beta$ 표기오류** → 정합은 $\alpha=1-\beta$.
- **[HIGH] AL-K1/K2/K3 grounding 부재**(정의 0건).
- [MED] Eyring prefactor $k_BT/h$→자유 Arrhenius 완화 불일치; L240 raw Unicode η.

### Ch4 (CRIT 1 / HIGH 4)
- **[CRITICAL] $\eta_j$ 구동전위 $V_n$ vs $V_{n,\drive}$ 한 문서 내 이중정의** → 미시=거시 정합 전제 붕괴.
- **[HIGH] verifybox $s_{\phi,j}$ 누락**(폰 "부호 정정 완료"는 암묵가정 회피, 미해소).
- **[HIGH] "Ch2 가 $n^\eff=1$ 특수형" 주장**이 Ch2(일반 $w_j$)와 모순 → Ch2 발열량 $n^\eff$ 계통오차 가능.
- [HIGH] $s_\bg^{\conv}$ 미정의; [MED] dead bibitem 4, ΔS_j vs ΔS‡ 혼동.

### Ch5 (CRIT 0 / HIGH 3)
- **[HIGH] branch affinity $s_{\phi,j}$ 누락** → 충전 branch 부호 모순(L220 `n^eff I η^b≥0` 유도 부재).
- **[HIGH] $V_{n,\app}$/$V_{n,\drive}$ Ch3 비통일**; **[HIGH] AL 인용 1건뿐**.
- 히스테리시스 자유에너지 비대칭 부호 = 음극전위 기준 물리적으로 옳음(확인). smooth-only 합격.

### Ch6 (CRIT 1 / HIGH 3)
- **[CRITICAL] 폰 "FLAGGED 강등했다" 보고가 허위 — flagbox 사용 0건.** 보고-파일 불일치.
- **[HIGH] $\varepsilon_\mathrm{tol}$ 수렴 임계값 수치·근거 전무**(근거없는 임계값 = GS-4 위반).
- [HIGH] root 유일성 서술 부정확; 수치문헌(brenan/hindmarsh/dubarry) 본문 미인용.
- **P1 준수 확인**(solver 코드·피팅 결과 없음; 이론 스킴 서술에 머묾).

## Validation
각 결함은 담당 agent 의 \emph{직접 재유도/대조 근거}와 함께 보고됨(추측 아님). DOI·차원·부호는
재유도 검산. 다수 agent 가 동일 결함(예: $s_\phi$·$V_{n,\drive}$ 교차결함)에 수렴 → Phase B 에서 확정.

## Gate
PASS (검수 완료). 적발 결함은 RB 계획 입력 결함표(§Current Ground Truth)로 이관.

## Confirmed Non-Changes
- 폰 원본·통합본 \emph{미수정}(검수만). 재구성은 RB Phase 1~ 에서 `_rebuilt` 신규.
- `Codex/` 산출물 미read(독립성 보존).

## Open Issues / Decision Queue
- cross-chapter 공통 뿌리 결함($s_\phi$, $V_n$ vs $V_{n,\drive}$, $n^\eff$) → 장별 수정 금지, RB Phase 0.1 규약 동결로 일괄.
- AL ledger 본체 부재(전 장) → RB Phase 0.3 + 장별 grounding 감사.

## Next
Phase B(장간 정합 + 통합본 빌드 검수). → 본 세션에서 완료(`PHASE_B_*_RESULT.md`).
