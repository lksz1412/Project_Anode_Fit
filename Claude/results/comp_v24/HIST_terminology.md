# HIST_terminology — 용어(terminology) 결정 이력 + directive registry 전수 (comp_v24 검토 sub)

> 목적: F-10(전문용어 억지 한글화 금지·일본식 번역투 배제·본문 한글 prose + 학술용어 영어 원어)의 **과거 확정 용어 결정·용어 레지스트리·directive registry** 전수 추출. 이번 용어 정리가 과거 결정과 정합하고, 이미 확정된 용어를 재-litigate 하지 않도록.
> 경계: **읽기·요약만** (tex/코드/계획서 무수정). 모든 항목 file:line 근거. 4-tier = 【확정】(원문 직접 확인) / 【근거 미발견】 / 【추정】 / 【미검증】.
> 작성 2026-07-22. 대상 = `Claude/` 산하 plans/·results/·docs/ + 전역 memory `feedback_communication_style.md`(읽기 허용분).

---

## 0. 핵심 결론 (한 문단)

용어 정책의 **원칙 자체는 v1.0.13 이전부터 확정·안정**돼 있다(글로벌 memory `feedback_communication_style` = "본문 한글 prose + 학술/기술 용어 영어 원어 + 한글 번역 강요 X", 2026-05-28 사용자 명시). 이 원칙을 문건에 적용한 **용어 레지스트리는 딱 하나** 존재: `V1013_TERMS_POLICY.md`(용어 27 + 약자 18, 2026-07-03). **directive registry(D-1~D-30)는 존재하나 전부 문건 구조·의존·워크플로 지시이고 terminology 지시는 0건**. 결정적으로 **이번 F-10 의 6개 표적어(요동·양성·정준·대정준·음함수·섭동) 중 어느 것도 V1013_TERMS_POLICY 에 등재돼 있지 않다** — 통계역학 절(Part 0/Part T)이 그 레지스트리 작성 이후 유입·확장됐기 때문. 즉 대부분 **미결(신규 결정)**이며, 다만 **대정준/grand canonical 만은 이미 "대정준(grand canonical)" 병기형으로 문건에 정착**(V1013 R7 확인)돼 있어 F-10 기본값(정준·대정준 = 국내 교과서 표준 유지)과 정합한다.

---

## 1. 확정된 용어 정책 원칙 (through-line — 전 시대 일관) 【확정】

| 시점 | 출처(file:line) | 원칙 원문 요지 |
|---|---|---|
| 2026-05-28(기원) | `scratchpad/portable_config/global/memory/feedback_communication_style.md:26-32` | **Rule 3 "한글 prose + 영어 학술 용어"**: 연결 prose 는 한글, 학술/기술 용어(academic/technical terms)는 **영어 원어 그대로**. **한글 번역 학술 용어를 강요하지 말 것.** 예 "활성화 자유 에너지"→"activation free energy". 단 "꼬리(tail)"·"피크(peak)"처럼 사용자가 직접 한글로 쓰는 일상어는 한글 유지(영어 병기 허용). **Why**: 사용자 명시 "학부부터 모든 학술 용어를 영어로 배워 한글 변환 학술 용어는 잘 모르겠다." |
| 2026-05-28 | 같은 파일 :19-23 | **Rule 2 "영어 두문자어 병기"**: 두문자어(약자)는 **첫 출현에 한 줄 설명 병기**, 반복 시 생략 가능. |
| 2026-07-02(사용자 지적 7건) | `Claude/results/V1013_RESULT.md:11` (목표 ④) | "**약자 원어 병기 + 일본식 번역어 제거(한글 서술 베이스 유지)**" — F-10 의 "일본식 번역투 배제"가 **이미 v1.0.13 단계에서 명시 지적**됨. |
| 2026-07-03(레지스트리 원칙문) | `Claude/results/process/V1013_TERMS_POLICY.md:6` | "서술 베이스 한글 유지 + 물리·화학·수학 전문 명사는 **영어 원어로 치환**. 이미 굳은 일상어/조어는 유지 가능(근거 명시). 이미 영어 원어인 것은 유지." |
| 2026-07-22(F-10 재지시) | `Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md:166-172` | "억지 한글화하니 더 헷갈림(예 요동·양성). 문단은 국문, 용어 억지 한글화 X, **특히 일본어 기반 번역 단어(쓰레기 같은) 금지**." |
| 2026-07-22(현 계획 명문화) | `Claude/plans/2026-07-22-v1024-feedback-revision-plan.md:19` (Current Ground Truth f) | "**F-10 = 기존 상시 규칙**(`communication_style`: 본문 한글 prose + 학술/기술 용어 영어 원어·한글 번역 강요 X)." → F-10 을 신규가 아닌 **기존 상시 규칙의 재적용**으로 자리매김. |

**판정**: 용어 정책의 방향은 5개 시대 문건에서 **모순 없이 일관**. F-10 은 새 정책이 아니라 **미이행분 재적용**. 【확정】

---

## 2. Directive Registry (누적 사용자 지시 목록) 【확정 — 단, terminology 지시 0건】

**존재하는 유일한 directive registry** = `Claude/plans/2026-06-08-ch2-directive-registry-revision-plan.md:9-49` — **D-1~D-30** (사용자 "지금까지 내가 지시한 작업 방향성을 전부 취합" 분노 수용해 작성).

- 그룹 A(통합 문건, D-1~D-7)·B(의존 구조, D-8~D-12)·C(내용·양식 품질, D-13~D-20)·D(작업 방식, D-21~D-26)·E(파일·아카이브, D-27~D-30).
- **terminology 관련 조항: 0건.** D-1~D-30 은 전부 문건 구조(단일 통합문건·인계/전달 절 금지)·의존 트리·발명 금지·워크플로. **용어 한글화/영문 병기/일본식 calque 를 다루는 지시는 이 레지스트리에 없음.**
- 간접 연동만: `:40` **D-23**(박사님 명시 지시 그대로 실행 — 임의 판단 대체·재질의 금지), `:41` **D-24**(지적한 항목 다시 반복 금지) — F-10 재발("이력 무시") 방지 논리의 상위 근거.

> 추가 확인: v1.0.14 이후 **누적 directive registry 문서는 갱신·재작성되지 않음** — grep 결과 D-1~D-30 형식의 통합 지시 레지스트리는 2026-06-08 판이 마지막. 이후는 버전별 계획서(11-section)·result·ledger 로 지시를 흡수. 【확정】(2026-06-08 이후 신규 directive registry 파일 【근거 미발견】)

---

## 3. 확정 용어 레지스트리 = V1013_TERMS_POLICY (용어 27 + 약자 18) 【확정】

출처: `Claude/results/process/V1013_TERMS_POLICY.md` (전문). **표만 산출 — 당시 .tex 0 byte 변경**(:5). 처분(유지/병기/치환) 요지:

### 3a. "한글 유지(치환 불요)" 확정어 — 재-litigate 대상 아님

| 용어 | 처분 | 근거 line |
|---|---|---|
| 전이(轉移, transition) | **유지** — 굳은 학술 표준어(210줄 반복). 전량 영어 치환 시 가독성 저해 | :15 |
| 과전압(overpotential) | **유지** — 정착 표준 전기화학어 | :26 |
| 히스테리시스(hysteresis) | **유지** — 음차 정착 표준어 | :27 |
| 무질서(disorder)·다중도(multiplicity)·되먹임(feedback)·배경(background)·활성화 장벽(activation barrier) | **유지** — 표준 번역, 코드 대응 명확 | :32-39 |
| 축퇴(degenerate/degeneracy) | **유지** — 표준 고체물리 번역어(축퇴 전자기체) | :35 |
| 겉보기(apparent, $U_\app$)·초격자(superlattice)·Maxwell 공통접선 | **유지**(선택 병기) | :29,:30,:34 |
| 상분리(phase separation) | **유지** + 최초 1회 병기 권고 | :17 |

### 3b. "병기 보강" 확정어(한글 유지 + 첫 출현 영문 병기)

정규용액(regular solution):5 · 격자기체(lattice gas):6 · 이중웰(double-well):7 · 배치(configurational/config):9 · 작업 격자(grid, ≠lattice):10 · 평탄역(plateau):11 · 코너(corner case):12 · 히스(축약 선언):15 · pairing(짝짓기):18.

### 3c. "치환(통일)" 확정어

- **배리어 → 장벽**(:21, #8) — 문서 지배 어휘 "장벽"으로 통일. (R7 A-5 에서 잔재 1건 L1421 추가 적발)

### 3d. 약자 병기(18종) — 첫 출현 완전형 병기 요구

ICA(완비 모범):48 / MIT=insulator-to-metal transition:49 / OD:50 / MSMR:51 / GITT·OCV·OCP·SOC·DFT(전량 미병기 → 병기 필요):52-56 / **FD 이중 의미 충돌**(Fermi–Dirac vs finite difference, ch2, 최우선 플래그):57 / BW·KWW·PSD·P4·G1-4·tier A/B/C:58-65.

### 3e. 치환 금지 구역 5범주 【확정】 (:69-77)

① 수식 내부 전체 ② `\code{...}` 코드 식별자 ③ `\bibitem{...}` 서지 ④ `%` 주석 라인 ⑤ `\label/\ref/\eqref/\cite` 키. — **용어 치환 시 이 구역은 원문 보존.** (F-10 집행 시 그대로 승계할 경계.)

> **R7 검수(2026-07-03)로 위 레지스트리가 실제 적용·검증됨**: `V1013_REVIEW_R7_A.md`(ch1, 21건 — 약자 병기 역전 4건 등, PASS/FAIL 표 :131-152) · `_R7_B.md`(ch2 + 챕터 간, MIT 확장형 챕터 간 불일치·$g_j$ 3중 충돌) · `_R7_C.md`(R6 수정분 재검). → 레지스트리는 **살아있는 감사 기준**으로 기능. 【확정】

---

## 4. 과거 용어 관련 사용자 지시·재지시 (날짜·요지) 【확정】

| 날짜 | 성격 | 요지 | file:line |
|---|---|---|---|
| 2026-05-28 | 원천 지시 | 학술 용어 영어 원어 유지, 한글 번역 강요 금지 | `feedback_communication_style.md:31` |
| 2026-06-08 | **분노** | "내 지시란 지시는 전부 무시 / 전부 취합해 수정 계획" → directive registry D-1~D-30 신설 (단 terminology 무관) | `2026-06-08-ch2-directive-registry-revision-plan.md:3,:123` |
| 2026-07-02 | 지적(7건 중 ④) | "약자 원어 병기 + 일본식 번역어 제거(한글 서술 베이스 유지)" | `V1013_RESULT.md:11` |
| 2026-07-22 | **재지시(분노 어조)** | "억지 한글화 더 헷갈림(요동·양성)·일본어 기반 번역 단어(쓰레기 같은) 금지" — **동일 취지 2회째 지적** | `USER_FEEDBACK_v1024_READING.md:166` |

**핵심**: "일본식 번역어 제거"는 **2026-07-02 → 2026-07-22 재발 지적**. F-11 과 함께 "이력 무시" 프로세스 실패의 사례군에 속함(용어 정책이 신규 통계역학 절 저작 시 미승계). 【추정 — 재발 인과는 계획서 Correction History `2026-07-22-...:188` 의 F-11 진단과 동형이나 F-10 자체엔 명시 인과 없음】

---

## 5. F-10 표적어와 과거 결정의 겹침 (이미 결정 vs 미결) — ★핵심

F-10 표적: 요동·양성·정준·대정준·음함수·섭동(+ 유일근). 빈도(전 챕터 grep, `USER_FEEDBACK_v1024_READING.md:169`): 요동 47·양성 10·정준 50·대정준 44·음함수 29·섭동 5.

| 표적어 | 과거 레지스트리 등재? | 과거 결정 상태 | 근거 | 현 F-10 기본값(D6) |
|---|---|---|---|---|
| **요동**(fluctuation) | **아니오** | **미결** — V1013 Part 0 신설 시 "요동-응답" 소절로 유입됐으나 용어 처분 없음 | 유입: `V1013_RESULT.md:14`("요동-응답"). 레지스트리 미등재: `V1013_TERMS_POLICY.md` 전문 grep 무매치 | 요동→fluctuation(첫 병기) `plan:202` |
| **양성**(positivity) | **아니오** | **미결** — 레지스트리 무등재. blend 절(v1.0.23/24 신규)에서 "요동 양성 유일근" calque | 사례: `USER_FEEDBACK_...:168`(ch3v22_sec03_blend 91·96행) | 양성→positivity(또는 "양의") |
| **음함수**(implicit function) | **아니오** | **미결** — 레지스트리 무등재 | `V1013_TERMS_POLICY.md` 무매치 | 음함수→implicit function |
| **섭동**(perturbation) | **아니오** | **미결** — 레지스트리 무등재 | `V1013_TERMS_POLICY.md` 무매치 | 섭동→perturbation |
| **정준**(canonical) | 부분(usage만) | **부분 정착** — 문건이 이미 canonical/grand canonical 영문 사용 | R7: grand canonical 영문형 사용(`V1013_REVIEW_R7_A.md:92`) | **유지**(국내 교과서 표준) `plan:202` |
| **대정준**(grand canonical) | 부분(병기 정착) | **사실상 결정됨** — "**대정준(grand canonical)**" 병기형이 문건에 정착 | ch1:384·ch2:116 병기 완비(`V1013_REVIEW_R7_A.md:92,:111`; `_R7_B.md:31` "grand-canonical L116") | **유지**(국내 교과서 표준) |
| 유일근(unique root) | 아니오 | **미결** | `USER_FEEDBACK_...:168` calque 예시 | (D6 미명시 — 결정 필요) |

**정리**:
- **이미 결정(재-litigate 금지)**: 대정준/정준 = **한글 유지 + 영문 병기** 방향이 문건 정착 + F-10 D6 기본값과 **정합**. (분배함수도 D6 에서 표준 유지: `plan:202`.)
- **미결(신규 결정 필요)**: 요동·양성·음함수·섭동·유일근 — **과거 어떤 레지스트리·검수에서도 처분된 적 없음.** 통계역학/blend 절 유입어라 V1013 레지스트리(흑연/LCO 중심) 사각지대. → **재-litigate 아님, 최초 결정.** 【확정 — 무등재는 `V1013_TERMS_POLICY.md` 전문 및 R7_A/B 전문 grep 무매치로 확인】
- **주의(정합성)**: 통계역학 절은 이미 lattice gas·grand-canonical·Bragg–Williams·Bose–Einstein·Fermi–Dirac–Sommerfeld 등 **영문 원어 + 한글 병기** 관례로 서술됨(`V1013_REVIEW_R7_B.md:31,:26`). 요동/음함수/섭동을 영문 전환할 때 이 기존 병기 관례와 **동일 스킴**으로 맞추면 정합. 【추정】

---

## 6. 표기 규약: "첫 등장 영문 병기" 확정 여부 【확정】

- **확정**. 근거 3중:
  1. `feedback_communication_style.md:19-23` — 약자 첫 출현 한 줄 병기(반복 시 생략).
  2. `V1013_TERMS_POLICY.md` 전반 — "**최초 출현** 병기" 처분이 표준(예 :14,:18,:19,:20).
  3. `V1013_REVIEW_R7_A.md:136-150` — 약자 병기가 **2회째 출현에 남으면 FAIL("역전")** 로 판정(MSMR·SOC·OCV·tier 4건 FAIL). 즉 "첫 등장 병기"는 **강제 게이트**, "역전"은 결함 클래스.
- 현 계획 승계: `2026-07-22-...:157`(TERM_DECISION_TABLE 열 규약) + `:159`("첫 등장 영문 병기") + `:109`(치환 시 첫 등장 영문 병기 규약).
- **미결 세부**: 표(longtable 기호표)의 bare 노출을 "표는 축약 관례"로 허용할지 여부는 R7_A 가 오적발 위험으로 표시(:159 항 4) — 경계 사례로 남음. 【확정(규약) / 미결(표 예외)】

---

## 7. 인접하나 F-10 아닌 것 (혼동 방지) 【확정】

- `V1014_TONE_AUDIT.md`(79건) = **F-04(문체·register) 계열**이지 F-10(용어) 아님. "값어치→화학퍼텐셜"·"옷"·"환율"·"먹인다" 등은 **구어·은유 제거**(register)이고 일본식 calque 제거(terminology)와 층위가 다름. 단 경계 중첩 존재(예 `:30` "값어치"→"화학퍼텐셜"는 학술어 복원 성격). 현 계획도 F-04 와 F-10 을 FB3 한 Phase 로 묶되 **구분 유지**(`plan:106,:167`).
- `2026-06-06-ch1-sec6-statmech-accessibility-plan.md`·`2026-06-06-ch1-sec8-10-comprehension-bridge-plan.md` = **접근성·논리 다리** 계획으로 **용어 결정 무관**(전문 확인). 통계역학 절 신설의 배경일 뿐 terminology 처분 없음.

---

## 8. 4-tier 요약

- 【확정】: (1) 용어 정책 원칙 전 시대 일관(§1). (2) directive registry = D-1~D-30 뿐이며 terminology 지시 0건(§2). (3) 용어 레지스트리 = V1013_TERMS_POLICY 27+18, 치환금지 5구역, R7 검증(§3). (4) 요동·양성·음함수·섭동 = 레지스트리 무등재 = 미결(§5). (5) 대정준(grand canonical) 병기 정착(§5). (6) 첫 등장 병기 = 강제 게이트, 역전 = 결함(§6). (7) 일본식 번역어 제거 = 2026-07-02·07-22 2회 지적(§4).
- 【추정】: F-10 재발 인과(신규 절 미승계)는 F-11 진단과 동형이나 F-10 자체 명시 없음(§4). 통계역학 절 기존 영문 병기 관례와의 정합 권장(§5).
- 【근거 미발견】: 2026-06-08 이후 갱신된 누적 directive registry 문서(§2). 요동/양성/음함수/섭동/유일근에 대한 과거 명시 처분(§5). 정준/대정준을 "일본식 calque"로 규정하거나 영문 전환하기로 한 과거 결정(오히려 유지 방향 정착).
- 【미검증】: 현 v1.0.24 tex 본문에서 6개 표적어의 실제 문맥별 용법(빈도만 인용, 문맥 정독은 FB0 인벤토리 소관 — 본 검토 범위 밖). blend 절(ch3v22_sec03) "요동 양성 유일근" 원문 라인 직접 열람은 미실시(계획서 인용 :168 신뢰).

---

## Read Coverage

- **전문 정독**: `feedback_communication_style.md`(35줄) · `V1013_TERMS_POLICY.md`(91줄) · `V1013_REVIEW_R7_A.md`(160줄)·`_R7_B.md`(198줄)·`_R7_C.md`(105줄) · `V1013_RESULT.md`(51줄) · `V1014_TONE_AUDIT.md`(201줄) · `2026-06-08-ch2-directive-registry-revision-plan.md`(124줄) · `2026-07-03-v1013-P3-P6-compress-terms-review-plan.md`(38줄) · `2026-07-22-v1024-feedback-revision-plan.md`(205줄) · `USER_FEEDBACK_v1024_READING.md`(207줄, F-10 :165-176 정독) · `2026-06-06-ch1-sec6-statmech-accessibility-plan.md`(176줄) · `2026-06-06-ch1-sec8-10-comprehension-bridge-plan.md`(62줄) · `Claude/plans/INDEX.md`(53줄).
- **grep 전수**: 전역 `TERMS_POLICY|terminology`(17파일) · `요동|양성|정준|대정준|음함수|섭동|일본|calque|한글화|억지`(plans 16 + results 100파일 파일목록) · `directive|registry|레지스트리`(15파일) · `일본|calque|쓰레기`(내용 60줄) · `directive registry/standing rule`(47파일).
- **미열람(범위 밖)**: v1.0.24 `_sections/*.tex` 본문 원문(용어 실용법 문맥) — FB0 TERM_DECISION_TABLE 인벤토리 단계 소관. Codex 산출물(CLAUDE.md P2 경계 준수 — 미열람).
