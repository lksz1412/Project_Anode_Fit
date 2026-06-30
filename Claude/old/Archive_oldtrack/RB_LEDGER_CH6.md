# RB_LEDGER_CH6 — Chapter 6 재구성 Result (Phase 6, step 133–146)

> 자율 진행(사용자 위임). 5-30 지시 = 기존 내용 검토 우선 → 조건부 재유도. Decision Gate → 3렌즈 적대검수 대체.

## 1. Phase·범위
Ch6 = **피팅 실무 부록** — Ch1~5 유도식을 ICA/DVA 데이터 피팅에 이용. 수치해법(DAE/solver) 피팅 보조로 종속. 산출 `graphite_ica_ch6_rebuilt.tex`.

## 2. Read Coverage
draft: `consolidated_ch6.tex`(검토 대상)+`_body_ch6_v2`+Ch1~Ch5 rebuilt+CHARTER+AL_MASTER+DOSSIER 전문. Codex/ 금지. jcp2017 원문 _local_only PDF 는 read 불요(dossier AL-61/62 grounding 사용).

## 3. G-flow (검토 결과 — 사용자 5-30 지시)
consolidated_ch6(수치 DAE/solver+검증 강조) 검토 → **피팅 실무 주역화**: S1~S6 피팅 워크플로·식별성·순차제약을 앞에, 수치 엔진(root/DAE/Plan A/B)을 inner-loop solver 로 종속. index-1 유도화(주장→유도). 다온도 Arrhenius 분해 신설.

## 4. ★ FLAGGED 허위(ε_tol) 정정 — 5-30 지시 핵심
Phase A 적발 확인: consolidated_ch6 의 ε_tol 근거 전무·flagbox 0건(established 위장). 정정: ε_tol=max(ε_disc,ε_noise) 측정 기반 정의 + **특정 수치값 FLAGGED 정직표기**(AL-66). solver tolerance 도 물리 scale 근거화(AL-64).

## 5. Grounding / AL
AL-60~63 기등재 + AL-64~69 신규(`RB_AL_MASTER` 등재). DOI 정확 귀속(brenan/hindmarsh/dubarry/fly/jcp2017/lee/son). orphan bibitem 0(draft가 전건 \cite — 이전 장 교훈 반영). \newcommand{\ref} 치명버그 draft가 제거.

## 6. 적대검수 (3렌즈)
수치·피팅 / 수학 / 정합. **수치·수학 두 agent 독립 CRITICAL 수렴**(Arrhenius 기울기; 정합 agent는 별도 HIGH). 나머지(ε_tol 정정 진정성·cap/clip 격리·수치 종속화·DOI·bibitem)는 통과.

## 7. 발견·정정 (1 CRITICAL[수렴] + 2 HIGH, 삭제 0)
| 등급 | 위치 | 정정 |
|---|---|---|
| **CRITICAL** | eq:ch6_arrhenius 기울기 | "기울기=−ΔH_a/R" 오류 — χ_j A_j/(RT)=(χA/R)(1/T)도 1/T-선형이라 고정 A_j여도 기울기 기여 → **유효** 엔탈피 −(ΔH_a−χA)/R. 순수 ΔH_a는 A→0 외삽/보정. 틀린 boundbox 직관("전위 함께 변할 때만") 정정 + n^eff convention 단서. eq:ch6_arrhenius_slope 신설. AL-69 GROUNDED→BOUNDED |
| HIGH | ∂lnL/∂V_drive | Ch1 ideal-width 형(−χs_φF/RT) 명시 + 일반형(−χs_φ n^eff F/RT=−χs_φ/w_j) 병기 |
| HIGH | §grid 평균장 closure | "numerically exact reference"가 독립완화 closure(Ch1 AL-13 평균장) 하에서만 exact — Ch1이 Ch6로 위임한 협동적 staging 검증 미이행 → **flagbox 승계**(exactness는 이산화오차 한정) |

미정정(LOW): A_eff/j_0n 정의(Ch3 AL-31 귀속 명시됨), max 연산자 구조(수학 agent는 논리 일치 판정, 수치 agent는 ε_noise 단독 주장 — 양론이라 정의 유지).

## 8. 빌드·무결성
tex **842줄**, PDF **19p** → `Claude/results/graphite_ica_ch6_rebuilt.pdf`. env: equation 10/10, begin/end 48/48. 진짜 undefined ref/cite **0**, overfull **0**, `!` 0. orphan bibitem 0.

## 9. CHARTER 준수 (상속장)
s_φ·V_drive·n^eff·keystone·AL 상속 일관. 방향-4: cap/clip/max/min/step 정의식 본문 0(피팅 보조는 practicebox 격리·금지목록 명시), Heaviside는 Ch1 spectrum support 유도분. 본문 비약어 0.

## 10. FLAGGED/BOUNDED 잔존
- FLAGGED: AL-66 ε_tol 수치값(정의는 BOUNDED) + AL-65 독립완화 closure(협동적 staging 검증 미이행, Ch1 위임 승계).
- BOUNDED 다수: AL-62 Plan A broad-kernel 열화·AL-64 tolerance·AL-67 calorimetry·AL-68 식별성·AL-69 Arrhenius 유효엔탈피.

## 11. Next
Phase 7 (통합, step 147–157): refs 문건 확정(통합 AL ledger + bibliography) + full 통합본(Ch1~6+refs 병합) + cross-chapter 최종 정합·빌드 + **bibitem-cite sweep**(Ch3/Ch4 orphan 정리). main 자동 머지.
