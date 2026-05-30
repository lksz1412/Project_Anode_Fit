# 학부생-가독 재유도 재구성 계획 — Graphite ICA tail 이론 8종 (RB-series)

**Date**: 2026-05-30 · **상태**: 계획(설계도). **사용자 GO 대기.** 플랜모드 미사용(문서 기반, `feedback_no_auto_plan_mode`).
**양식**: 표준 11-section (`feedback_plan_template_11sections`) + cumulative step + 매 phase 5-stage 루프(`feedback_phase_execution_loop`).
**상위 chain**: `2026-05-29-consolidation-roadmap.md`(폰) → `PHASE_DIAG_INTENT_GAP_RESULT.md` → 본 RB 계획.

---

## §0.A 다루는 시스템 (System under study)

**물리계**: 리튬이온전지 **흑연(graphite) 음극** (반쪽셀 기준; Ch1 기본 = 방전=탈리튬화 branch).
**관측량**: **ICA(Incremental Capacity) $dQ/dV$** + 역수 **DVA(Differential Voltage) $dV/dQ$**.
**현상**: Li intercalation staging 전이($4\!\to\!3\!\to\!2\mathrm L\!\to\!2\!\to\!1$)가 $dQ/dV$ 에 peak 를 남김(관측 $N_p\approx3\!\sim\!4$).
**설명할 핵심 관찰** (전 장이 놓지 않는 단일 끈):
> ICA peak 의 \emph{꼬리}가 **저온일수록 길어져 다음 peak 와 겹치고**, 고온이면 짧다. **C-rate 가 크면 겹침 심화.**

**설명 전략 (열역학 무대 + 동역학 주역)**: 평형 열역학만으론 안 됨($w=RT/F$ 는 저온서 좁아져 관찰과 반대)
→ 꼬리 주역은 동역학(lag); 내부 전위 $V_n$ 은 전하보존식의 해(무대); 꼬리 깊이는 relaxation-length spectrum.
**최종 목표**: 관찰을 grounded·무비약 물리로 설명하는 **피팅 가능한 닫힌 논리식**.

## §0.B 방향성 규약 표준 (사용자 제시 = RB 6 원칙, 2026-05-30 명시; 절대 기준)

| # | 원칙 | 의미 |
|---|------|------|
| **방향-1** | **학부생 가독** | 논문 수준 논리를 학부 2~3학년 지식(열역학·전기화학·미적분·선형대수)+본문 도입 개념만으로 재현 가능하게 |
| **방향-2** | **수식 흐름 보존 + 재유도** | 통합본의 수식 흐름(식 순서·역할)은 가져가되 각 식을 물리 타당성 검증하며 다시 유도 |
| **방향-3** | **가정·논리 문제 시 재작성** | 가정·논리에 문제(특히 무근거 무리한 가정)가 발견되면 그 지점부터 \emph{논리를 다시 작성}. 필요 시 해당 장 백지화 재전개 (← 5-30 사용자 정정: "멈춤"이 아니라 "재작성") |
| **방향-4** | **계산편의 비약 배제** | 실무·계산 편의를 위한 과도한 비약(임의 cap·clip·step·근거없는 임계값) 금지 |
| **방향-5** | **근거 논문 필수** | 모든 가정식은 논문·교과서 기반. 마지막 ref 문건 수준 이상의 grounding bibliography 갖춤 |
| **방향-6** | **챕터 하나씩** | 한 장씩 진행·수정. 매 장 끝 = Decision Gate(사용자 검토) 후 다음 장 |

**★ 5-30 추가 경고 (사용자 명시)**: 가져온 폰 작업물에는 \textbf{논문·교과서에 입각하지 않은 무리한 가정}이 들어있을 수 있다.
→ 본 작업의 1차 임무 = 각 가정의 grounding 진위 판정. 무근거 가정 발견 시 방향-3 적용(논리 재작성). 폰 산출물의 "통과"
자기보고를 신뢰하지 않는다(Phase A 가 Ch6 FLAGGED 허위 보고를 이미 적발).

## §0.C 산출물 구조 — 8종 (사용자 명시 의존 트리)

```
Ch1  열역학 무대 + 극판 전위에 의한 배리어 낮춤 (최대한 심플) → relaxation → spectrum → 피팅식
 ├─ Ch2  (Ch1 이용)  전지 가역 반응열 해석으로 확장
 └─ Ch3  (Ch1 기반)  전기화학 반응속도론 반영 → 시각 확장 + 논리의 더 넓은 일반화
      ├─ Ch4  (Ch3 이용)  전지 가역 반응열 해석으로 확장
      └─ Ch5  (Ch3 기반)  충방전 히스테리시스 데이터 해석으로 확장
Ch6  (부록 성격)  유도된 수식을 피팅에 어떻게 이용하는가 — 실무적 내용
refs 위 전체의 근거 논문·교과서 모음
─────────────────────────────────────────
합본(full)  내부 7종(Ch1~6 + refs)을 전부 싸는 통합본 1종      → 총 8종
```

**현재 통합본과의 대조 (백지화 판정용)**: 각 장 서두 확인 결과 의존 구조는 \emph{일치}
(Ch2←Ch1, Ch3←Ch1, Ch4←Ch3, Ch5←Ch3 모두 현재 통합본과 동일). **단 Ch6 강조점 상이**: 사용자 의도 = "피팅 실무 부록",
현재 통합본 = "수치해법(DAE/solver)+검증 중심". → Decision D5. 의존 구조가 맞으므로 \emph{전체 백지화는 불필요},
장별 재유도에서 무근거 가정 발견 시 \emph{해당 장 단위} 백지화(방향-3).

---

## 1. Summary

폰 통합본 8종(Ch1~6 standalone + refs + full)의 \textbf{수식 흐름을 골격으로 보존}하되, 모든 식을 \textbf{학부생 가독·무비약으로
재유도}하고 \textbf{모든 가정을 논문/교과서 + 검증 DOI 로 grounding}하며 \textbf{계산편의 비약·무근거 가정을 배제}한다.
무근거 무리한 가정 발견 시 해당 논리를 \textbf{재작성}(방향-3). 산출 = 재구성 8종(`graphite_ica_chN_rebuilt.tex` ×6 +
`refs_rebuilt` + `full_rebuilt`) + 통합 Assumption Ledger(근거+DOI). 챕터 하나씩, 매 장 Decision Gate.

## 2. Context / Background

- **선행 상태**: 폰 브랜치(`origin/claude/chapter-1-physics-logic-WD1R5`)에서 전 6장 "원본 밀도 재작성 + 통합본" 작업물을
  로컬로 가져옴(staged). 빌드는 정합(Phase B: label 충돌 0, 매크로/환경/cite 미정의 0, standalone↔body 무손실 md5 일치).
- **확인된 문제(Phase A 장별 + Phase B 장간 적대 재검수)**: (i) Assumption Ledger \emph{본체 부재}(전 장 — 방향-3·5 정면 공백),
  (ii) 학부 무비약 표방하나 숨은 전제 다수(closure 동결, $s_\phi$, 구동전위 $V_n$ vs $V_{n,\drive}$),
  (iii) Ch6 FLAGGED \emph{허위 보고}(flagbox 사용 0건, $\varepsilon_\mathrm{tol}$ 근거 전무),
  (iv) 과대주장(2배감쇠 일반화는 내 직전 chapter2 검수에서 적발·정정; consolidated Ch2 는 해당 주장 부재),
  (v) grounding 공백(JCP2017 미등재, `newman`≡`newman2004` 중복키, dead bibitem).
- **왜 필요한가**: 통합본이 표방한 표준(GS-1~4)을 \emph{실제로는 미집행}. 사용자 방향-1~6 = 그 표준의 실집행 요구.
  특히 5-30 경고(무근거 무리한 가정 잠재)로 grounding 감사가 1차 임무가 됨.

## 3. Objective / Success Criteria

완료 정의(측정 가능):
- **O1**: 8종 재구성 산출 — Ch1~6 재유도본 + refs + full. 각 장 빌드 무결(xelatex/kotex, eqref/cite/label resolve, 중복 0).
- **O2 (방향-1)**: 독립 재유도 agent 가 \emph{외부지식 없이} 각 boxed 결과를 본문 전제만으로 재현 (G-undergrad 통과).
- **O3 (방향-3·5)**: 모든 본문 가정식이 AL 항목 + 근거 cite + \emph{web 검증 DOI}(또는 정직 FLAGGED). 무태그 established 0건.
- **O4 (방향-2)**: 핵심식 흐름(§6 spine) 순서·역할 보존, 각 단계 차원·부호·극한·2법칙 검산 통과.
- **O5 (방향-4)**: cap/clip/step/max/min/Heaviside 정의식 0; 근거없는 수치 임계값 0; solver 구현 0(P1).
- **O6 (방향-3)**: 무근거 가정 발견 건마다 재작성 내역이 ledger 에 기록(발견→재작성→재검증).
- **O7**: cross-chapter 규약($s_\phi$·$V_{n,\drive}$·$n^\eff$·keystone·AL번호) 전 장 일관(G-cross).

## 4. Scope

- **In**: Ch1~6 각각 — 골격추출 / 가정 전수 grounding 감사 / 무비약 재유도 / 적대검증(가독 포함) / 수정·재작성·ledger.
  통합 references dossier(DOI 검증). 통합 AL ledger. 재구성 full 통합본.
- **Out**: 신규 물리 발명(흐름 보존 원칙; 단 무근거 가정 재작성은 In); 실험 데이터 피팅 \emph{실행}(P1);
  solver 코드 구현(P1); 3D thermal PDE; full-cell 상세(통합본 범위 따름); Codex 산출물 참조.

## 5. Inputs / References

- **기준 골격**: `Claude/docs/graphite_ica_consolidated_ch1~6.tex`, `_body_ch1~6_v2.tex`, `_full.tex`, `_bib_merged_v2.tex`.
- **결함 입력**: 본 세션 Phase A 6 보고 + Phase B 2 보고(요지 §9 입력 결함표).
- **원천 근거**: `_local_only/` JCP 147(14)144111(2017) PDF(사용자 PhD; Plan A closure Refs6/7 원천) — **Decision D1**.
- **폰 진단**: `PHASE_DIAG_INTENT_GAP_RESULT.md`, `..._SALVAGE_LEDGER.md`, `..._REFS67_DOSSIER.md`, `consolidation-roadmap.md`.
- **정합 참조**: `graphite_ica_chapter2_CLAUDE_criticalfix_5-29.tex`(내 직전 열·entropy 적대검수본 — Ch2 salvage 소스).
- **양식 근거**: `_claude/memory/feedback_plan_template_11sections.md`, `..._phase_execution_loop.md`, `..._gate_design_principle.md`,
  `..._document_protection_addendum_pattern.md`, `..._full_file_read_required.md`.
- **금지**: `Codex/` 하위 산출물 read(양 모델 독립성; 운용지침만 예외).

## 6. Phase Breakdown (cumulative step RB-001~; 최소 기준점, 유연 확장 가능)

각 장 Phase = **5-stage 루프** (S1 골격추출 → S2 grounding 감사 → S3 무비약 재유도 → S4 적대검증 → S5 수정·재작성·ledger)
+ Decision Gate. 실행은 Workflow(ultracode)로 stage 내 다중 렌즈 병렬화. 산출물은 각 step 끝에 명시.

| Phase | step | 내용 | 산출물 |
|---|---|---|---|
| **RB-P0** Foundation | RB-001~003 | §7 cross-chapter 규약 동결($s_\phi$/$V_{n,\drive}$/$n^\eff$/keystone/AL번호) | `RB_CHARTER.md` |
| | RB-004~009 | grounding references dossier: 전 장 anchor 문헌 + 공백 보강, **전건 DOI web 검증**(환각 금지) | `RB_REFERENCES_DOSSIER.md` |
| | RB-010~012 | 통합 AL 번호 체계 + 학부-가독·무비약 gate 정의서 + notation bible | `RB_AL_MASTER.md`(골격) |
| **RB-P1** Ch1 | RB-013~020 | S1~S2: 골격추출(전하보존~피팅식 흐름) + 가정 전수 grounding 감사(무근거 가정 적발) | `RB_LEDGER_CH1.md`(S1-2) |
| | RB-021~030 | S3~S4: 무비약 재유도(열역학 무대 + 극판전위 배리어 낮춤, 최대한 심플) + 적대검증 | `graphite_ica_ch1_rebuilt.tex`(초안) |
| | RB-031~035 | S5: 수정·재작성 + result(11항목) + Decision Gate | `..._ch1_rebuilt.tex`(확정) + ledger |
| **RB-P2** Ch2 | RB-036~050 | 5-stage: Ch1 이용 → 전지 가역 반응열 해석 확장(내 열·entropy salvage 정합) | `..._ch2_rebuilt.tex` + ledger |
| **RB-P3** Ch3 | RB-051~068 | 5-stage: Ch1 기반 → 전기화학 반응속도론 일반화(Level A↔B 한정 재유도) | `..._ch3_rebuilt.tex` + ledger |
| **RB-P4** Ch4 | RB-069~083 | 5-stage: Ch3 이용 → 전지 가역 반응열 해석 확장($\eta$·$s_\phi$ 규약) | `..._ch4_rebuilt.tex` + ledger |
| **RB-P5** Ch5 | RB-084~098 | 5-stage: Ch3 기반 → 충방전 히스테리시스 해석(branch 부호 유도) | `..._ch5_rebuilt.tex` + ledger |
| **RB-P6** Ch6 | RB-099~110 | 5-stage: 부록 — 유도식의 피팅 실무 이용(D5 강조점 정정; FLAGGED 정직화, P1) | `..._ch6_rebuilt.tex` + ledger |
| **RB-P7** 통합 | RB-111~120 | refs 문건 확정 + 재구성 full 통합본 + 통합 AL ledger 병합 + cross 최종 정합 + 빌드 | `refs_rebuilt.tex` + `..._full_rebuilt.tex` + `RB_LEDGER_INTEGRATION.md` |

## 7. Gates (verifiable only — `feedback_gate_design_principle`)

매 장 통과 조건(전부 확인 가능):
- **G-flow**: 골격 핵심식 전부 존재 + 인과 사슬 순서 보존(대조).
- **G-noleap**: 모든 유도 단계에 명시 근거(앞 식 번호/AL/대수). "자명/clearly/보일 수 있다" 0건(scan).
- **G-undergrad**: 독립 재유도 agent 가 외부지식 없이 각 boxed 결과를 본문 전제만으로 재현(agent 재현).
- **G-ground**: 모든 가정식이 AL 항목 + 근거 cite + 검증 DOI(또는 정직 FLAGGED). 무태그 established 0건(대조).
- **G-noungrounded(★5-30)**: 논문/교과서 근거 없는 "무리한 가정" 0건. 발견 시 방향-3 재작성 완료 기록(대조).
- **G-dim**: 모든 식 차원 정합(검산).
- **G-noconvleap**: cap/clip/step/max/min/Heaviside 정의식 0; 근거없는 수치 임계값 0; solver 구현 0(P1)(scan).
- **G-cross**: $s_\phi$·$V_{n,\drive}$·$n^\eff$·keystone·AL번호 가 §RB-P0 동결 규약과 일치(대조).
- **G-latex**: 컴파일 무결(eqref/cite/label resolve, 중복 0, 환경 balance)(검산).
- **G-honest**: 검수표 3-tier(통과/조건부/미확정), 보고-파일 일치(대조).

## 8. Test / Validation Plan

- 매 식 **차원분석**; 핵심식 **독립 재유도**(adversarial agent, 외부지식 차단); **극한/점근** 일치; **2법칙**($\sigma\ge0$);
  **부호 convention** 전장 일관; **DOI web 실측**; **학부-가독 재현** 테스트(agent 가 본문만으로 재현); **LaTeX 빌드**(사용자 환경 xelatex/kotex, 매 Gate PDF 검토).
- 각 장 S4 = 병렬 다중 렌즈: ① 물리·차원 재유도 ② LaTeX ③ 논리 chain ④ grounding·DOI ⑤ 학부-가독·무비약 ⑥ **무근거 가정 감사(5-30)**.
  발견은 adversarial verify(독립 다수결)로 확정 후 수정.
- 통합(RB-P7): full 빌드 label 충돌 0 / 미정의 0 재확인 + standalone↔통합 무손실 대조.

## 9. Risks / Mitigations

| ID | 위험 | 완화 |
|---|---|---|
| R1 | 재유도가 흐름식을 \emph{오류}로 판정 | 방향-3: 그 지점부터 논리 재작성(해당 장 백지화 가능). 재작성 내역 ledger 기록. 사용자엔 Gate 에서 보고 |
| R2 | 무근거 무리한 가정 잠재(5-30 경고) | S2 grounding 감사를 1차 임무화. 무근거→FLAGGED→재작성. 폰 "통과" 자기보고 불신 |
| R3 | 가정에 문헌 근거 부재 | 환각 cite 금지. 정직 FLAGGED(Ch6 $\varepsilon_\mathrm{tol}$ 교훈) |
| R4 | DOI 환각 | RB-P0 dossier 에서 전건 web 검증 |
| R5 | 학부-가독 vs 논문-깊이 긴장 | 전제부터 쌓기로 양립(방향-1 + GS-2) |
| R6 | 6장 대규모·장기 | 매 장 Gate + 사용자 검토로 scope 관리(방향-6). cumulative step + ledger 추적 |
| R7 | Ch6 강조점 divergence(피팅실무 vs 수치해법) | D5 로 사용자 확정 후 진행 |
| R8 | 결과 문건 보호 | 폰 원본·통합본 보존, 재구성본은 `_rebuilt` 신규(`feedback_document_protection_addendum_pattern`) |

## 10. Decision Queue (사용자 — 평문, 무응답 시 권고값 진행)

- **D1 (JCP2017 PDF)**: Plan A closure(Ch1/Ch6) grounding 위해 사용자 JCP147(14)144111(2017) PDF 의 `_local_only/` 존재/제공 여부.
  **권고값**: `PHASE_DIAG_REFS67_DOSSIER.md`(폰이 PDF 보고 작성) 를 2차 근거로 사용, 원문 재확인은 제공 시.
- **D2 (산출 파일명)**: 재구성본 = `graphite_ica_chN_rebuilt.tex`(신규), 원본·통합본 보존. **권고값**: 그렇게.
- **D3 (내 Ch2 열·entropy 본)**: 통합본 Ch2(발열 연결, Ch1 기반) 기준 + 내 `chapter2_CLAUDE_criticalfix` 의 reaction-entropy·비가역열 결과를
  salvage 흡수. **권고값**: 흡수(통합본 흐름 우선).
- **D4 (진행 방식)**: 매 장 Gate 에서 사용자 검토 후 다음 장. **권고값**: 그렇게(방향-6).
- **D5 (Ch6 성격)**: 사용자 의도 = "피팅 실무 부록", 현재 통합본 = "수치해법+검증 중심". **권고값**: 사용자 의도 따라 \emph{피팅 실무 중심}으로
  재구성하고, 현재 Ch6 의 수치해법(DAE/solver) 부분은 피팅에 필요한 한도로 축약·종속. (전면 폐기 아님 — 피팅 보조로 격하)
- **D6 (백지화 범위)**: 의존 구조가 일치하므로 전체 백지화 불필요 권고. 단 장별 재유도 중 무근거 가정 발견 시 \emph{해당 장 단위} 백지화(방향-3).
  **권고값**: 장 단위 재작성, 전체 백지화는 사용자 명시 시만.

## 11. Correction History

| 일자 | 변경 |
|---|---|
| 2026-05-30 (v1) | RB 계획 최초 작성. 통합본 8종 흐름 기준 + Phase A/B 결함 입력. GS-1~5, cross-chapter 규약, 8 Phase. |
| 2026-05-30 (v2) | 사용자 정정 반영 전면 재작성: (a) 방향-3 = "멈춤"→"논리 재작성"; (b) 산출 8종 구조 명시(내부 7종=Ch1~6+refs, 합본 1종) + 의존 트리(Ch2←Ch1, Ch3←Ch1, Ch4←Ch3, Ch5←Ch3); (c) Ch1=심플 열역학+극판전위 배리어 낮춤, Ch6=피팅 실무 부록(D5); (d) 5-30 경고(무근거 무리한 가정)→S2 grounding 감사 1차 임무화 + G-noungrounded gate; (e) 11-section 표준 양식 준수; (f) §0.A 시스템·§0.B 방향 규약 서두 고지; (g) 현재 통합본 의존구조 대조(일치, 전체 백지화 불필요·장단위 재작성). |
