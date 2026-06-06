# Ch1 보완 — eq#29 줄나눔 + §6(통계역학) 학부 초년생 접근성 Plan

**Date**: 2026-06-06 · **Author**: Claude · **챕터**: A(Ch1 Accessibility 보완) · **Phase**: A.0~A.5 · **Step**: 1~?
**대상**: `Claude/docs/graphite_ica_ch1.tex` (879줄·19p·GREEN; R.0~R.9 로 Claude+Codex 동시 확정결함 0 완료본)
**트리거**: 사용자 — (1) 29번식 PDF서 잘림(줄나눔 필요), (2) §1~5 는 따라가기 좋으나 §6 으로 넘어가며 \emph{통계역학}이 갑자기 섞여 어려움 — 학부 초년생(통계역학 미수강 다수) 눈높이로 쉽게 풀 것, 그 사이 \emph{새 절} 삽입 가능.

---

## Summary

**목표**: 완료본 Ch1 을 두 축으로 보완한다. (A) **eq#29(=eq:superpose) 줄나눔** + 잘리는 식 전수 교정. (B) **§5(barrier)→§6(dist) 전이 + §6 의 통계역학 내용**을 \emph{학부 1~2학년}(통계역학 무지식 전제) 이 따라갈 수 있게 풀어 쓴다 — 필요하면 §5 와 §6 사이에 \emph{통계 도구 입문} 신규 절 삽입.

**왜**: §1~5 는 열역학+약간의 동역학이라 매끄럽지만, §6 은 \emph{분포 ρ_G·가중 적분·분산 전파·변수 변환·stretched exp} 등 통계역학 도구가 \emph{전제 없이} 등장한다. 통계역학은 학부 4학년/대학원에서 다루고 미수강 졸업이 흔해, 기초조차 없는 독자가 많다. 도구를 \emph{바닥부터} 깔아 줘야 §6 이 닫힌다.

**범위**: §1~5 = \emph{경량 검토}(거의 완벽 — 회귀·잔결함만 확인). §5→§6 전이 + §6 = \emph{본격 보완}(신규 절 + §dist 풀어쓰기). 워크플로 = 기존 확립분(절별 Claude 자체검수 + Codex 적대검토 병행 → Claude 가 타당/오바/구라 판정 → 문제 안 나올 때까지 반복 → 앞 절과 흐름 연결, 전문 재정독·분량 회귀 감시).

---

## Current Ground Truth

**확정 사실**:
- 대상 `graphite_ica_ch1.tex` 879줄·19p·빌드 GREEN. R.0~R.9 완료(`Claude/results/PHASE_R0~R9_*_RESULT.md`, ledger 전 PASS). Claude(자체+독립3인)+Codex(교차모델) 동시 확정결함 0.
- **eq#29 = `eq:superpose`** (`.aux` 검증: 26=sseq,27=keff,28=LqV,**29=superpose**,30=closed,31=simplefit,32=arrhenius). 추정 아님.
- **Overflow(\hbox too wide)**: **L653 eq:superpose 85.9pt**(최대·사용자 지적 식) · L490–495 53.6pt(eq:tailTC 추정) · L158/L162 표 행 미세(7.8/1.5pt) · L763 7.7pt(arrhenius 유도).
- **절 구조(현재)**: 서·§1 notation·§2 stage·§3 eqpeak·§4 lag·§5 barrier·§6 dist·§7 synth·§8 overlap·§9 falsify. 신규 절 삽입 시 \ref/\eqref/\label 자동 갱신(수동 재번호 불요).
- **§6(dist) 통계역학 요소**: (a) ρ_G(G) 배리어 분포·정규화·용량가중, (b) eq:superpose 가중 적분(앙상블 중첩), (c) 분산 전파 σ_G/RT(Var[ln(L_V/L_{V,0})]), (d) rigorbox 변수변환·자코비안, (e) stretched exponential(연속 지수합).

**작업 이력 참조(워크플로)**: `PHASE_R0~R9_RESULT.md` — 절별 iterate-until-clean(Codex 확정결함 0 선언까지) + Codex 판정 재검(valid/overreach/구라) + 절간 비약(G-flow) + 전문 재정독·분량 회귀 감시 + 결과/ledger 디스크 기록.

**미확인(A.0서 확정)**: 신규 절의 정확한 범위·배치(신규 §6 vs §dist 확장); §6 풀어쓰기의 구체 입도; L490–495 식 정체.

---

## Phase Range

| Phase | 이름 | Steps | 핵심 | 게이트 |
|---|---|---:|---|---|
| **A.0** | 전제·인벤토리·설계 | 1–4 | §barrier 끝~§dist 끝 전문 재정독 + eq#29/overflow 확정 + 신규 절 설계(개념·입도) + Decision 확정 | 정독·설계 확정 |
| **A.1** | 식 줄나눔(가독) | 5–7 | eq:superpose(#29) multiline + L490–495·표 행 overflow 교정 + 빌드 | overflow 0(주요식) |
| **A.2** | §1~5 경량 검토 | 8–11 | §1~5 Claude+Codex 회귀·잔결함 확인(거의 무수정 예상) | 확정결함 0 |
| **A.3** | 신규 절 — 통계 도구 입문(초년생) | 12–18 | 분포/밀도·가중 평균(앙상블)·분산과 지수 증폭·변수변환·연속 지수합 — 1~2학년 수학으로 바닥부터 | 절별 iterate-until-clean + G-undergrad |
| **A.4** | §6(dist) 풀어쓰기 + 전이 연결 | 19–25 | §dist 의 ρ_G·eq:superpose·분산전파·rigorbox 를 신규 절 도구로 쉽게 재서술; §5→신규→§6 비약 0 | 절별 iterate-until-clean + G-flow |
| **A.5** | 하류 정합 + 전영역 적대 + 빌드 | 26–30 | 삽입 후 §7+ 참조·번호 정합 + Codex 교차모델 + Claude 적대 전영역 + 최종 빌드 | Codex DOCUMENT CLEAN + GREEN |

**정지 5조건**(GO 후 A.5까지 연속): Decision Gate / 새 의존성 / FAIL gate / 사용자 stop / 두 통제문서 모순(→더 제한적).

**절별 게이트(A.3·A.4 핵심)**: G-local(물리·무비약·차원) · G-flow(앞 절 정합·비약 0) · **G-undergrad**(통계역학 무지식 1~2학년이 앞 식+본문만으로 따라가나 — 본 보완의 1급 렌즈) · G-build · G-review(Codex 적대 → Claude 판정 → 반복) · **G-recovery**(컴팩션·세션 재개 직후 재정독 — §X 의무).

**★ Anti-compaction 의무**: 컴팩션(컨텍스트 요약)·세션 연속 \emph{직후}에는 새 편집 전에 §X 재정독 프로토콜을 \emph{반드시} 실행한다(컴팩션 = 누락·환각 최대 취약점 — 사용자 명시).

---

## Non-goals

- §1~5 \emph{본문 재작성}(경량 확인만 — "거의 완벽" 존중, 과수정 금지).
- 충전 branch·Ch2~5·피팅 부록 상세.
- eq 값·물리 결론·핵심 결과식(logistic·eqpeak·simplefit·LqV·superpose 적분형) \emph{변경}(가독 줄나눔·서술 풀어쓰기만; 수식 내용 보존).
- 사용자 기호·라벨·식번호 임의 변경(P5). Workflow 등 권한팝업 도구(Agent only). Codex/ tex 읽기/쓰기.

---

## Implementation Changes

| 종류 | 경로 | 의도 |
|---|---|---|
| 수정 | `graphite_ica_ch1.tex` | eq:superpose multiline·overflow 교정 / §dist 풀어쓰기 |
| 신규 | `graphite_ica_ch1.tex` 내 \section{통계 도구…}\label{sec:stattools} | §5~§6 사이 입문 절(Decision 승인 시) |
| 신규 | `Claude/results/PHASE_A0~A5_*_RESULT.md` + `PHASE_A0-A5_EXECUTION_LEDGER.md` | Phase별 result 11항목 + 12-col ledger |
| 계획 | 본 파일 | 11-section |
| 동반 | `Codex/` 거울 | 커밋 시 동반(수정 X) |

**문건 보호**: 이전 result·ledger·R.* 산출물 덮어쓰기 금지(Addendum/Supersession/Correction).

---

## Phase A.0 — 전제·인벤토리·설계

- **S1** §barrier 끝(L513~620)·§dist(L622~679) \emph{전문 재정독} + §7 synth 도입부 — §6 이 §5 에서 무엇을 받고 §7 로 무엇을 넘기는지 매핑.
- **S2** eq#29=eq:superpose·overflow(L490–495·L158/162·L763) 정체 확정(.aux/log 대조 완료, 식 본문 확인).
- **S3** \emph{통계 도구 입문 절 설계}: (a) 분포/밀도 ρ(히스토그램→연속, 정규화, 용량가중) (b) 가중 평균=앙상블(∫ρ·값, 기댓값 직관) (c) 분산·지수 증폭(Var(aX)=a²Var X, σ_G→σ_G/RT, exp 가 퍼짐 키움) (d) 변수변환·밀도보존(ρ_G dG=A_L dL, 자코비안) (e) 연속 지수합→stretched. 각 1~2학년 수학(미적분·기초확률)으로, 물리 연결.
- **S4** Decision 확정(신규 절 vs §dist 확장; eq#29 분할형) + result/ledger.
- **gate**: 정독 커버리지·설계 확정. **다음 조건**: Decision 승인.

## Phase A.1 — 식 줄나눔(가독)

- **S5** eq:superpose(#29) multiline: 본 적분식 1줄 / 정의(L_V(G), r_a(G)) 별 줄(`aligned`/`split` 또는 정의를 박스 밖 문장으로). 잘림 0.
- **S6** L490–495(53.6pt)·표 행 L158/162·L763 overflow 교정(줄나눔/`\!`/열폭).
- **S7** 빌드 + overflow 재측정(주요식 0). result.
- **gate**: G-build + Overfull(주요 디스플레이식) 0.

## Phase A.2 — §1~5 경량 검토

- **S8~S10** §1~5 절별 Claude 자체검수 + Codex 적대(회귀·잔결함만). 발견 시 Claude 판정 후 최소 교정.
- **S11** result + ledger.
- **gate**: §1~5 확정결함 0(거의 무수정 예상).

## Phase A.3 — 신규 절: 통계 도구 입문 (초년생)

- **S12~S17** 설계(S3) 5 도구를 절로 작성 — 각 도구: \emph{왜 필요(물리 동기)} → \emph{쉬운 개념(직관·간단 예)} → \emph{식} → \emph{본 문제 연결}. step-function 금지·무비약·인용(교과서) 유지.
- **S18** 절별 iterate-until-clean(Codex 적대 → 판정 → 반복) + G-undergrad(초년생 추적) + result/ledger.
- **gate**: 절별 5-게이트(G-undergrad 포함) 확정결함 0.

## Phase A.4 — §6(dist) 풀어쓰기 + 전이 연결

- **S19~S23** §dist 의 ρ_G·eq:superpose·분산전파·rigorbox·boundbox 를 신규 절 도구를 \emph{인용}해 쉽게 재서술(수식 보존, 직관·연결 보강). §5 끝→신규 절→§6 \emph{비약 0} 확인.
- **S24** 전이 매끄러움(G-flow) + 하류 §7 와의 정합.
- **S25** 절별 iterate-until-clean + result/ledger.
- **gate**: 절별 5-게이트 + §5→신규→§6→§7 흐름 비약 0.

## Phase A.5 — 하류 정합 + 전영역 적대 + 빌드

- **S26** 신규 절 삽입 후 전 문서 \ref/\eqref/식·절 번호 정합(undefined/중복 0).
- **S27** Codex 교차모델 전영역 적대 패스 → Claude 판정 → 반복(DOCUMENT CLEAN까지).
- **S28** Claude 독립 적대(필요 시) + 분량 회귀 감시(신규 절로 증가 정상).
- **S29~S30** 최종 빌드 GREEN + result + ledger + 사용자 Decision Gate.
- **gate**: Codex DOCUMENT CLEAN + GREEN·undefined 0.

---

## Implementation Interfaces

**§E eq:superpose 줄나눔(안)**: 박스 안을 두 줄로 —
```
dQ/dV_n|tail = Q_j ∫_0^∞ ρ_G(G) [r_a(G)/L_V(G)] exp[-(V_n-V_a)/L_V(G)] dG   (s(V_n-V_a)≥0),
        L_V(G)=|dV_n/dq|_{q_a} L_q(G),   r_a(G)≡r_j(q_a;G).
```
(`aligned` 로 `=` 정렬, 둘째 줄 정의. 수식 내용·라벨 eq:superpose 보존.)

**§T 신규 절 골격(통계 도구)**: 5 소절 — 분포/밀도 · 가중 평균(앙상블) · 분산과 지수 증폭 · 변수변환(자코비안) · 연속 지수합(stretched). 각 "동기→직관→식→연결". 초년생 기준.

**§G 절별 5-게이트**: G-local · G-flow · **G-undergrad**(통계역학 무지식 1~2학년 추적 가능) · G-build · G-review(Codex 적대→Claude 판정→반복).

**§R Result 11항목 · Ledger 12-col**(기존 양식).

**§X Anti-compaction 재정독 프로토콜(★ 사용자 명시 — 컴팩션 = 누락·환각 최대 취약점)**: 컴팩션·세션 연속(Continue) \emph{직후}, 또는 매 Phase 재진입 시, \emph{새 편집 한 줄도 하기 전에} 다음 5단계를 순서대로 실행하고 통과해야 한다 —
1. **직전 result 정독**: `Claude/results/PHASE_A*_RESULT.md`(가장 최근) Read — 무엇을 어디까지 했나 \emph{정확 확인}(기억·추정 절대 금지).
2. **ledger Next Step 확인**: `PHASE_A0-A5_EXECUTION_LEDGER.md` 의 다음 cumulative step·gate.
3. **작업 부위 tex 전문 재정독**: 컴팩션 이전 \emph{작업 중이던 절}을 \emph{현재 파일 상태}로 처음부터 끝까지 재정독 — 마지막 편집이 제자리에 있고 훼손·누락 0 인지, 직전 단계 결과가 실제 반영됐는지.
4. **계획 대조**: 본 계획서 해당 Phase step 과 1:1 대조 — 건너뛴 step·미반영 Decision 없나.
5. **분량 대조**: 직전 대비 줄수/문단/식 수 \emph{급감 없나}(급감 = 누락 신호 → 이전 버전 재정독·재작업, 사용자 명시). git/이전 빌드 줄수와 비교.
→ 5단계 통과 결과를 그 Phase result 의 \emph{Read Coverage} 에 기록(재정독 사후 증명). 통과 못하면 새 작업 진입 금지.

---

## Test Plan

- **빌드**: xelatex GREEN(`!`0·undefined 0·dup 0). **Overfull**: eq:superpose 등 주요 디스플레이식 0(log 재측정).
- **참조 정합**: 신규 절 삽입 후 \ref/\eqref 전수 해상·식/절 번호 자동 정합(중복·미정의 0).
- **G-undergrad 검수**: "통계역학 안 배운 1~2학년" 렌즈 — 신규 절·§6 을 그 시각으로 검수(직관 누락·전제 점프 탐지). Codex + Claude.
- **흐름 비약**: §5→신규→§6→§7 절간 G-flow.
- **Codex 교차모델**: A.5 DOCUMENT CLEAN. **분량 회귀 감시**: 신규 절로 줄수 증가(감소=누락 신호).
- **★ Anti-compaction(§X)**: 컴팩션·재개 직후 매번 5단계 재정독(직전 result·ledger·작업 절 tex 전문·계획 대조·분량 대조) 실행 + result Read Coverage 에 증거 기록. 미실행 시 그 Phase gate FAIL.

---

## Assumptions

- A1: eq#29=eq:superpose 확정(.aux). A2: 신규 절 삽입 권고(Decision 대기) — 미승인 시 §dist 확장으로 대체. A3: §1~5 거의 무수정(경량). A4: 신규 절 삽입은 \ref 자동 정합이라 하류 깨짐 0(A.5서 검증).

---

## Decisions Required (평문, 무응답 시 권고값)

- **D-newsection**: §5(barrier)와 §6(dist) \emph{사이}에 신규 \section{통계 도구 입문}(→ dist 가 §7 로 자동 밀림) 삽입. **권고: 그대로**(사용자 "새 절 들어가도 좋다" + 통계 도구를 §6 직전 just-in-time 제공이 "도구는 쓰기 직전" 원칙과 정합). 대안: §dist 도입부를 소절로 확장(번호 불변).
- **D-eq29**: eq:superpose 를 `aligned` 2줄(적분식 / 정의)로 분할. **권고: 그대로.**
- **D-scope**: §1~5 경량 확인·§6+ 본격 보완. **권고: 그대로.**
- **D-undergrad렌즈**: 절별 게이트에 G-undergrad(초년생 추적) 1급 추가. **권고: 그대로.**

---

## Correction History

| 일자 | 변경 |
|---|---|
| 2026-06-06 (A v1) | Ch1 완료본 보완 계획 신설 — eq#29(eq:superpose, .aux 검증) 줄나눔 + §6 통계역학 학부 초년생 접근성(신규 절 삽입 권고). 워크플로 = R.0~R.9 확립분(절별 Claude+Codex 적대 iterate-until-clean + 판정 + G-flow + G-undergrad + 재정독·회귀감시). §1~5 경량·§6+ 본격. |
| 2026-06-06 (A v2) | 사용자 첨언 반영 — **§X Anti-compaction 재정독 프로토콜**(컴팩션·재개 직후 5단계 의무 재정독: 직전 result·ledger·작업 절 tex 전문·계획 대조·분량 대조) + G-recovery 게이트 신설. 컴팩션 = 누락·환각 최대 취약점. |
