# Graphite ICA tail 이론 8종 — 학부생-가독 재유도 재구성 (RB-series) Plan

**Date**: 2026-05-30 · **상태**: 계획(설계도). **사용자 GO 대기.** 플랜모드 미사용(문서 기반, `feedback_no_auto_plan_mode`).
**양식**: 표준 11-section (`feedback_plan_template_11sections`) + cumulative step + Phase 단위 5-stage 실행루프(`feedback_phase_execution_loop`).
**구조 규칙(사용자 수차례 지시)**: **챕터 안에서 Phase 로 나눈다 → Phase 달성을 위해 세부 step 으로 쪼갠다 → step 번호는 Phase·챕터 무관하게 전체 단조 누적.**

---

## §0.A 다루는 시스템 (System under study)

**물리계**: 리튬이온전지 **흑연(graphite) 음극** (반쪽셀; Ch1 기본 = 방전=탈리튬화 branch).
**관측량**: **ICA $dQ/dV$** + 역수 **DVA $dV/dQ$**.
**현상**: Li intercalation staging 전이($4\!\to\!3\!\to\!2\mathrm L\!\to\!2\!\to\!1$)가 $dQ/dV$ 에 peak 를 남김(관측 $N_p\approx3\!\sim\!4$).
**설명할 핵심 관찰**: ICA peak 의 \emph{꼬리}가 **저온일수록 길어져 다음 peak 와 겹치고**, 고온이면 짧다. **C-rate 가 크면 겹침 심화.**
**설명 전략(열역학 무대 + 동역학 주역)**: 평형 열역학만으론 안 됨($w=RT/F$ 저온서 좁아져 관찰과 반대) → 꼬리 주역은 동역학(lag);
$V_n$ 은 전하보존식의 해(무대); 꼬리 깊이는 relaxation-length spectrum.
**최종 목표**: 관찰을 grounded·무비약 물리로 설명하는 **피팅 가능한 닫힌 논리식**.

## §0.B 방향성 규약 표준 (사용자 제시 = RB 6 원칙, 절대 기준)

| # | 원칙 | 의미 |
|---|------|------|
| 방향-1 | **학부생 가독** | 논문 수준 논리를 학부 2~3학년 지식(열역학·전기화학·미적분·선형대수)+본문 도입 개념만으로 재현 가능하게 |
| 방향-2 | **수식 흐름 보존 + 재유도** | 통합본의 수식 흐름(식 순서·역할)은 가져가되 각 식을 물리 타당성 검증하며 다시 유도 |
| 방향-3 | **가정·논리 문제 시 재작성** | 가정·논리에 문제(특히 무근거 무리한 가정) 발견 시 그 지점부터 \emph{논리를 다시 작성}. 필요 시 해당 장 백지화 (5-30 정정: "멈춤"이 아니라 "재작성") |
| 방향-4 | **계산편의 비약 배제** | 실무·계산 편의용 과도한 비약(임의 cap·clip·step·근거없는 임계값) 금지 |
| 방향-5 | **근거 논문 필수** | 모든 가정식은 논문·교과서 기반. ref 문건 수준 이상의 grounding bibliography |
| 방향-6 | **챕터 하나씩** | 한 장씩 진행·수정. 매 장 끝 = Decision Gate(사용자 검토) 후 다음 장 |

**★ 5-30 경고(사용자 명시)**: 폰 작업물에 \emph{논문·교과서에 입각하지 않은 무리한 가정}이 있을 수 있다. 본 작업의 1차 임무 =
각 가정의 grounding 진위 판정. 무근거 가정 발견 시 방향-3(재작성). 폰의 "통과" 자기보고를 신뢰하지 않는다(Phase A 가 Ch6 FLAGGED 허위 적발).

## §0.C 산출물 구조 — 8종 (사용자 명시 의존 트리)

```
Ch1  열역학 무대 + 극판 전위에 의한 배리어 낮춤 (최대한 심플) → relaxation → spectrum → 피팅식
 ├─ Ch2  (Ch1 이용)  전지 가역 반응열 해석으로 확장
 └─ Ch3  (Ch1 기반)  전기화학 반응속도론 반영 → 시각 확장 + 논리의 더 넓은 일반화
      ├─ Ch4  (Ch3 이용)  전지 가역 반응열 해석으로 확장
      └─ Ch5  (Ch3 기반)  충방전 히스테리시스 데이터 해석으로 확장
Ch6  (부록 성격)  유도된 수식을 피팅에 어떻게 이용하는가 — 실무적 내용  [5-30: 기존 내용 기반 먼저 검토]
refs 위 전체의 근거 논문·교과서 모음
─────────────────────────────────────────
합본(full)  내부 7종(Ch1~6 + refs)을 전부 싸는 통합본 1종      → 총 8종
```

---

## Summary

폰 통합본 8종(Ch1~6 standalone + refs + full)의 \textbf{수식 흐름을 골격으로 보존}하되, 모든 식을 \textbf{학부생 가독·무비약으로
재유도}하고 \textbf{모든 가정을 논문/교과서 + 검증 DOI 로 grounding}하며 \textbf{계산편의 비약·무근거 가정을 배제}한다.
무근거 무리한 가정 발견 시 해당 논리를 \textbf{재작성}(방향-3). **챕터마다 Phase 로 나누고, Phase 달성을 위해 step 을 쪼개며,
step 번호는 전체 단조 누적**한다. 산출 = 재구성 8종(`graphite_ica_chN_rebuilt.tex`×6 + `refs_rebuilt` + `full_rebuilt`)
+ 통합 Assumption Ledger(근거+DOI). 매 챕터 끝 Decision Gate(사용자 검토) 후 다음 챕터.

## Current Ground Truth

**확인된 사실**:
- 폰 브랜치(`origin/claude/chapter-1-physics-logic-WD1R5`) 통합본 8종 + body + 진단/ledger 를 로컬 합류, 작업 브랜치 `rb-rebuild-2026-05-30` 에 wip 커밋(59 파일, 손실방지). 원본·통합본 보존.
- 빌드 정합(Phase B): label 충돌 0(239개 고유), 매크로/환경/cite 미정의 0, standalone↔body 무손실 md5 일치.
- 의존 구조 일치(각 장 서두 확인): Ch2←Ch1, Ch3←Ch1(zoom-in), Ch4←Ch3, Ch5←Ch3 모두 사용자 의도와 동일.
- `_local_only/JCP_147(14)_144111_(2017)...pdf` 존재(사용자 PhD; gitignore 로 push 제외 확인) = Plan A closure Refs6/7 원천.

**확인된 문제(Phase A 장별 + Phase B 장간 적대 재검수)**:
- Assumption Ledger \emph{본체 부재}(전 장 — 방향-3·5 정면 공백).
- 학부 무비약 표방하나 숨은 전제 다수(closure 동결, $s_\phi$, 구동전위 $V_n$ vs $V_{n,\drive}$, $n^\eff$).
- Ch6 FLAGGED \emph{허위 보고}(flagbox 0건, $\varepsilon_\mathrm{tol}$ 근거 전무).
- grounding 공백(JCP2017 미등재, `newman`≡`newman2004` 중복키, dead bibitem 3).
- cross-chapter 결함: $s_\phi$·$V_{n,\drive}$·$n^\eff$·keystone 처리 장마다 미묘하게 갈림(§Implementation Interfaces 규약으로 동결 예정).

**미확인 사항**: Ch6 의 사용자 의도(피팅 실무) vs 현재(수치해법+검증) 강조점 차 → **5-30 결정: 기존 내용 기반 먼저 검토, 결과 보고 후 재작업/수정 여부 결정.** JCP2017 원문 직접 read 여부(Decisions D1).

## Phase Range

> **읽는 법**: Phase ID = `<챕터>.<Phase>` (챕터 안에서 Phase 로 나눔). Step = 전체 단조 누적(Phase·챕터 무관). 각 챕터 = 5-stage 루프(골격추출→grounding감사→무비약재유도→적대검증→수정·재작성·ledger). 최소 기준점이며 무근거 가정 발견 시 step 확장 가능(`feedback_step_granularity_flexibility`).

| Phase | 이름 | Step 범위 | 산출물 |
|---|---|---|---|
| **0.1** | Foundation — cross-chapter 규약 동결 | 1–5 | `RB_CHARTER.md` |
| **0.2** | Foundation — references dossier(전건 DOI web 검증) | 6–12 | `RB_REFERENCES_DOSSIER.md` |
| **0.3** | Foundation — 통합 AL 번호체계 + notation bible + 가독 gate 정의 | 13–16 | `RB_AL_MASTER.md`(골격) |
| **1.1** | Ch1 — 골격추출 + 가정 전수 목록 | 17–20 | `RB_LEDGER_CH1.md`(S1) |
| **1.2** | Ch1 — grounding 감사(무근거 가정 적발) | 21–25 | ledger(S2) + AL-CH1 |
| **1.3** | Ch1 — 무비약 재유도(열역학 무대 + 극판전위 배리어 낮춤) | 26–33 | `graphite_ica_ch1_rebuilt.tex`(초안) |
| **1.4** | Ch1 — 적대검증(다중 렌즈 + 가독) | 34–38 | 검증 보고 |
| **1.5** | Ch1 — 수정·재작성 + result(11항목) + Decision Gate | 39–42 | `..._ch1_rebuilt.tex`(확정) + `RB_LEDGER_CH1.md` |
| **2.1–2.5** | Ch2 — (Ch1 이용) 전지 가역 반응열 해석 확장 [5-stage] | 43–62 | `..._ch2_rebuilt.tex` + ledger |
| **3.1–3.5** | Ch3 — (Ch1 기반) 전기화학 반응속도론 일반화 [5-stage] | 63–88 | `..._ch3_rebuilt.tex` + ledger |
| **4.1–4.5** | Ch4 — (Ch3 이용) 전지 가역 반응열 해석 확장 [5-stage] | 89–110 | `..._ch4_rebuilt.tex` + ledger |
| **5.1–5.5** | Ch5 — (Ch3 기반) 충방전 히스테리시스 해석 확장 [5-stage] | 111–132 | `..._ch5_rebuilt.tex` + ledger |
| **6.1** | Ch6 — 기존 내용 골격추출 + 검토(5-30: 검토 우선) | 133–137 | 검토 보고 |
| **6.2** | Ch6 — grounding 감사 + 검토 결과 보고 → **Decision Gate(더 할지/수정할지)** | 138–141 | `RB_LEDGER_CH6_review.md` |
| **6.3** | Ch6 — (조건부) 피팅 실무 중심 재유도·수정 | 142–146 | `..._ch6_rebuilt.tex` + ledger |
| **7.1** | 통합 — refs 문건 확정(통합 AL + bibliography) | 147–150 | `refs_rebuilt.tex` |
| **7.2** | 통합 — 재구성 full 통합본 | 151–153 | `..._full_rebuilt.tex` |
| **7.3** | 통합 — cross-chapter 최종 정합 + 빌드 검증 | 154–157 | `RB_LEDGER_INTEGRATION.md` |

## Non-goals

- 신규 물리 발명(흐름 보존 원칙; 단 무근거 가정의 재작성은 In-scope).
- 실험 데이터 피팅 \emph{실행} / solver 코드 구현(P1; 수치 스킴의 이론 서술은 허용).
- 3D thermal PDE / full-cell 상세(통합본 범위 따름).
- `Codex/` 하위 산출물 read(양 모델 독립성; 운용지침만 예외).
- **사용자 승인 전 금지**: 폰 원본·통합본 \emph{덮어쓰기}(재구성본은 `_rebuilt` 신규); main 머지; push.

## Implementation Changes

생성:
- `Claude/results/RB_CHARTER.md`(규약 동결), `RB_REFERENCES_DOSSIER.md`(근거+DOI), `RB_AL_MASTER.md`(통합 ledger).
- `Claude/docs/graphite_ica_ch1~6_rebuilt.tex`(재구성 6장), `refs_rebuilt.tex`, `graphite_ica_full_rebuilt.tex`.
- `Claude/results/RB_LEDGER_CH1~6.md`(장별 result 11항목), `RB_LEDGER_INTEGRATION.md`, `RB_EXECUTION_LEDGER.md`(12-col 누적).
수정: 없음(원본 보존). 모든 산출은 `_rebuilt`/`RB_` 신규.
working copy: `Claude/work/`(필요 시 재유도 스크래치).

## Phase 0 — Foundation (규약·근거·체계 동결; step 1–16)

- **Phase 0.1 (step 1–5)** cross-chapter 규약 동결. 입력: Phase A/B 결함표. 산출: `RB_CHARTER.md`.
  step1 $s_{\phi,j}$ 부호 인자 정의(Ch3 명시형 기준) / step2 구동전위 $V_{n,\drive}$ 기준 + 기본 $=V_n$ / step3 $n_j^\eff=RT/(Fw_j)$ 위계(Ch4 일반형/Ch2 특수형) / step4 keystone(Level A=Level B detailed-balance 극한, 한정어 필수) / step5 통합 AL 번호체계 규칙.
  gate: 5개 규약이 "확인 가능한 조건"으로 1행씩 기술(G-cross 기준 확정). 중단: 규약 충돌 시 사용자 보고. 다음: 0.2.
- **Phase 0.2 (step 6–12)** references dossier. step6–10 = 장별 anchor 문헌 수집(§Implementation Interfaces 표) / step11 공백 보강 / step12 **전건 DOI web 실측 검증**. 산출: `RB_REFERENCES_DOSSIER.md`.
  gate: 모든 anchor 가 DOI 또는 ISBN/장·페이지로 검증(G-ground 입력). 중단: 핵심 가정에 문헌 근거 부재 → FLAGGED 후보로 표기, 사용자 보고. 다음: 0.3.
- **Phase 0.3 (step 13–16)** 통합 AL 번호체계 골격 + notation bible(ver↔Chapter, $\theta\leftrightarrow\xi$) + 학부-가독·무비약 gate 정의서. 산출: `RB_AL_MASTER.md`(골격).
  gate: AL 번호 충돌 0, notation 매핑 누락 0. 다음: Phase 1.1.

## Phase 1 — Chapter 1 (열역학 무대 + 극판전위 배리어 낮춤; step 17–42)

5-stage 루프. Ch1 은 **최대한 심플**(사용자 명시): 평형 열역학 베이스 + 극판 전위에 따른 배리어 낮춤 위주.
- **1.1 골격추출(17–20)**: consolidated_ch1 + _body_ch1 전수 정독 → 핵심식 순서/역할 + 가정 전수 목록 + 본 장 입력 결함(closure 동결·JCP2017). gate: 핵심식 흐름 목록화(G-flow). 산출: `RB_LEDGER_CH1.md`(S1).
- **1.2 grounding 감사(21–25)**: 각 가정 → 논문/교과서 근거 확정 + DOI + tier. \emph{무근거 무리한 가정 적발}(방향-3 트리거). gate: G-ground·G-noungrounded. 산출: AL-CH1.
- **1.3 무비약 재유도(26–33)**: 전하보존 $\to\xi_\eq\to$ 유효배리어 $\Delta G_\eff=\Delta G_a-\chi\mathcal A\to$ 완화 $\to L(G)\to A_L\to$ kernel $\to$ 피팅식. 매 단계 차원·부호·극한·grounding 검산. gate: G-noleap·G-dim·G-noconvleap. 산출: `graphite_ica_ch1_rebuilt.tex`(초안).
- **1.4 적대검증(34–38)**: 병렬 다중 렌즈(①물리·차원 재유도 ②LaTeX ③논리 chain ④grounding·DOI ⑤학부-가독·무비약 ⑥무근거 가정 감사). adversarial verify. gate: G-undergrad. 산출: 검증 보고.
- **1.5 수정·재작성+gate(39–42)**: 확정 결함 수정(무근거 가정은 재작성). result 11항목. **Decision Gate**: 사용자에 `ch1_rebuilt.tex` 제시. 중단: 사용자 검토 대기(방향-6). 다음: 사용자 GO 시 Phase 2.1.

## Phase 2 — Chapter 2 ((Ch1 이용) 전지 가역 반응열 해석; step 43–62)

5-stage(2.1 골격추출 43–45 / 2.2 grounding 46–49 / 2.3 재유도 50–55 / 2.4 적대검증 56–59 / 2.5 수정·gate 60–62).
초점: Ch1 상태변수($V_n,\xi_j,k_j$) 위에서 \emph{전지 가역 반응열}(평형 전위 온도계수 $\partial U/\partial T$, $q_\rev$/$q_\irr$)로 확장.
내 `chapter2_CLAUDE_criticalfix`(reaction-entropy·비가역열) salvage 정합. gate: 위 6렌즈 + G-cross($s_\phi$·$\eta$ 규약). Decision Gate 후 Phase 3.

## Phase 3 — Chapter 3 ((Ch1 기반) 전기화학 반응속도론 일반화; step 63–88)

5-stage(3.1 63–66 / 3.2 67–71 / 3.3 72–79 / 3.4 80–84 / 3.5 85–88).
초점: Ch1 의 Level A(mobility) 완화를 forward/backward $r^\pm$(Level B, $\chi=\beta$)로 \emph{zoom-in}, 시각·논리 일반화. detailed balance·BV·$R_n\ne R_\ct$. keystone 한정 재유도(Level A=Level B detailed-balance 극한). Decision Gate 후 Phase 4.

## Phase 4 — Chapter 4 ((Ch3 이용) 전지 가역 반응열 해석; step 89–110)

5-stage(4.1 89–91 / 4.2 92–95 / 4.3 96–101 / 4.4 102–105 / 4.5 106–110).
초점: Ch3 $r^\pm$ 로부터 transition-level entropy production → 거시 $\sum n^\eff I_j\eta_j$ 정합. $\eta$·$s_\phi$ 규약 적용(Phase A CRITICAL 해소). Decision Gate 후 Phase 5.

## Phase 5 — Chapter 5 ((Ch3 기반) 충방전 히스테리시스; step 111–132)

5-stage(5.1 111–113 / 5.2 114–117 / 5.3 118–125 / 5.4 126–129 / 5.5 130–132).
초점: Ch3 위에서 signed current/branch, metastable target, $\Delta V_\obs\ne\Delta V_\hys$, $q_\hys$. branch 부호 \emph{유도} 명시(Phase A HIGH 해소). Decision Gate 후 Phase 6.

## Phase 6 — Chapter 6 (피팅 실무 부록; step 133–146) — 5-30: 기존 내용 검토 우선

- **6.1 기존 내용 골격추출+검토(133–137)**: 현재 consolidated_ch6(수치해법 DAE/solver + 검증) 전수 정독 → 피팅 실무 관점 검토. gate: G-flow.
- **6.2 grounding 감사 + 보고 → Decision Gate(138–141)**: FLAGGED 허위($\varepsilon_\mathrm{tol}$ 근거)·P1 점검. **검토 결과를 사용자에 보고 → 더 작업할지/수정할지 사용자 결정**(5-30 사용자 명시). 산출: `RB_LEDGER_CH6_review.md`.
- **6.3 (조건부) 재유도·수정(142–146)**: 사용자가 재작업 GO 시에만. 피팅 실무 중심 재구성, 수치해법은 피팅 보조로 종속. 미GO 시 skip.

## Phase 7 — 통합 (refs + full + 정합; step 147–157)

- **7.1 refs 확정(147–150)**: dossier 기반 통합 AL ledger + bibliography 문건. `newman` 중복키·dead bibitem 정리.
- **7.2 full 통합본(151–153)**: 재구성 6장 + refs 병합. preamble 매크로/환경 union, 키 dedupe.
- **7.3 최종 정합+빌드(154–157)**: cross-chapter 규약 일관 재확인, label 충돌 0 / 미정의 0, standalone↔통합 무손실, xelatex 빌드. 산출: `RB_LEDGER_INTEGRATION.md`. gate: 전 Gate 종합.

## Implementation Interfaces

**Phase ID·Step 규약**: Phase = `<챕터>.<n>`; Step = 전체 누적(1→157, Phase·챕터 무관). 이어받기 = 직전 ledger `Next Step`.

**Cross-chapter 동결 규약(Phase 0.1 산출, 전 장 상속)**:
1. $s_{\phi,j}$: $\mathcal A_j=s_{\phi,j}n_j^\eff F(V_{n,\drive}-U_j)$ 명시형. $\eta_j,q_\irr$ 부호 전 장 동일.
2. 구동전위: dissipation force 기준 $=V_{n,\drive}$; 기본 $V_{n,\drive}=V_n$($\eta_{n,\drive}=0$), 강구동은 BOUNDED.
3. $n_j^\eff=RT/(Fw_j)$: Ch4 일반형 $\sum n^\eff I_j\eta_j$ / Ch2 특수형($n^\eff=1$).
4. keystone: Level A = Level B 의 detailed-balance 극한($\xi_\ss\to\xi_\eq$). 무조건 "A=B" 금지.
5. AL: 통합 단일 ledger, 연속 번호, 각 항목 = 가정 + tier + cite + DOI.

**Anchor 근거 표(Phase 0.2 검증 대상)**: Ch1=Newman/Eyring1935/Evans-Polanyi1938/McKinnon1983/Bazant2013/Plonka/Macdonald2000/Lindsey1980/Marcus1956/JCP2017 · Ch2=Bernardi1985/Rao1997/Reynier2004/Thomas-Newman2003/deGroot-Mazur · Ch3=Bard-Faulkner/Newman/Schnakenberg1976 · Ch4=deGroot-Mazur/Onsager1931/Prigogine1967 · Ch5=Dreyer2010/Sethna1993 · Ch6=Brenan1996/Hindmarsh2005/Dubarry2022.

**AL ledger row 양식**: `| AL-# | 가정 진술 | tier(GROUNDED/BOUNDED/FLAGGED) | 근거 cite | DOI(검증) | 사용 장·식 |`.
**Result 문건**: `feedback_phase_execution_loop` 11항목(Read Coverage 필수). **Execution ledger**: 12-col.

## Test Plan

- 매 식 **차원분석**; 핵심식 **독립 재유도**(adversarial agent, 외부지식 차단); **극한/점근** 일치; **2법칙**($\sigma\ge0$); **부호 convention** 전장 일관; **DOI web 실측**; **학부-가독 재현**(agent 가 본문 전제만으로 boxed 결과 재현); **LaTeX 빌드**(xelatex/kotex, 매 Decision Gate PDF 검토).
- 각 Phase S4 = 병렬 6렌즈 검증, 발견은 adversarial verify(독립 다수결) 확정 후 수정.
- 통합(7.3): full 빌드 label 충돌 0 / 미정의 0 + standalone↔통합 무손실 대조.
- **Gate 목록(verifiable only)**: G-flow(핵심식·순서 보존) / G-noleap("자명/clearly" 0건) / G-undergrad(외부지식 없이 재현) / G-ground(가정=AL+cite+DOI) / G-noungrounded(무근거 가정 0, 발견 시 재작성 기록) / G-dim(차원) / G-noconvleap(cap/clip/step/임의임계값/solver 0) / G-cross(동결 규약 일치) / G-latex(컴파일 무결) / G-honest(검수 3-tier, 보고-파일 일치).

## Assumptions

- A1: 통합본 의존 구조(Ch2←Ch1 등)는 사용자 의도와 일치(서두 확인) → 전체 백지화 불필요, 장 단위 재작성. (검증: 각 장 1.1 골격추출에서 재확인)
- A2: 폰 dossier(`PHASE_DIAG_REFS67_DOSSIER.md`)는 2차 근거; JCP2017 원문 재확인은 D1 따름.
- A3: Ch6 는 검토 결과에 따라 재작업 범위 확정(현재는 기존 내용 검토만 확정).
- A4: 빌드 환경(xelatex/kotex)은 사용자 측; 본 작업은 빌드 무결성을 정적 검수 + 사용자 PDF 확인으로 검증.

## Decisions Required (사용자 — 평문, 무응답 시 권고값)

- **D1 (JCP2017 원문)**: `_local_only/` PDF 직접 read 허용? **권고: 허용**(Plan A closure grounding 1차 원천; 가장 정확). 불허 시 dossier 2차 근거만 사용.
- **D2 (산출 파일명)**: `graphite_ica_chN_rebuilt.tex` 신규, 원본 보존. **권고: 그대로.**
- **D3 (내 Ch2 열·entropy 본 흡수)**: 통합본 Ch2 기준 + `chapter2_CLAUDE_criticalfix` salvage. **권고: 흡수.**
- **D4 (진행)**: 매 챕터 Decision Gate 후 다음. **권고: 그대로(방향-6).**
- **D5 (Ch6)**: **해소** — 5-30 사용자 지시 "기존 내용 기반 먼저 검토, 결과 보고 후 결정". Phase 6.1–6.2 검토 → Gate.
- **D6 (백지화 범위)**: 장 단위 재작성, 전체 백지화는 사용자 명시 시만. **권고: 그대로.**

## Correction History

| 일자 | 변경 |
|---|---|
| 2026-05-30 (v1) | 최초 작성. 8종 흐름 기준 + Phase A/B 결함. (오류: 비표준 섹션명, 1챕터=1Phase) |
| 2026-05-30 (v2) | §0.A 시스템·§0.B 방향규약·§0.C 8종 트리 서두 고지. 방향-3 "멈춤→재작성" 정정. |
| 2026-05-30 (v3) | **사용자 지적 2건 정정**: (1) **표준 11-section 양식 정확 준수**(Summary/Current Ground Truth/Phase Range/Non-goals/Implementation Changes/Phase N/Implementation Interfaces/Test Plan/Assumptions/Decisions Required/Correction History — 임의 섹션명 제거). (2) **Phase 입도 교정**: 챕터마다 5 Phase(`<챕터>.<n>`), Phase 달성 위해 step 분할, **step 전체 단조 누적(1→157)**. Ch6 = 기존 내용 검토 우선(D5 해소). |
