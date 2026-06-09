# Ch1·Ch2 통합·완결성 계획 v2 — 절 재작성 수준 · keep/cut 확정

## Summary
박사님 지적(6-09): 보강분이 앞뒤 단절·미사용 "댕글링" — \emph{교과서로 못 쓸} orphan. 본 계획은 \textbf{각 추가분을 살릴지(살리면 \emph{절을 다시 쓰는 수준}으로 spine에 완전 통합) / 버릴지(제거) 확정}하고, 그 결정대로 절을 \emph{재작성}한다. 패치(연결 한 줄) 아님 — \textbf{KEEP 항목은 앞이 도입·뒤가 사용하도록 절 구조를 다시 짜고, CUT 항목은 깨끗이 제거}. 결과는 모든 문장이 흐름의 일부이고 downstream에서 쓰이는 완결 교과서. 방식 = 절 단위·챕터 단위 루프(절마다 빌드·정합), 최대 effort, NO Workflow, master 직접 손검, Codex 적대검수, result/ledger, auto-commit. spine = Ch1 eq:master(최종 피팅식)·S1–S4, Ch2 eq:hys\_master·§9/§10 피팅.

## Current Ground Truth — keep/cut 결정표 (audit 확정, 박사님 확인 대상)
**판정 기준**: 앞 도입(직전이 동기) · 뒤 사용(최종식·피팅·뒤 절·진단이 인용/대입/환원). 둘 다면 KEEP, 한쪽이면 \emph{재작성으로 양쪽 채움}, 둘 다 불가면 CUT.

### Ch1 (대체로 통합 — 약한 고리 절 재작성, CUT 없음)
| 추가분 | 앞 | 뒤 | 결정·조치 |
|---|---|---|---|
| §3 "최종식과 연결" thread | ✓ | ✓ master 평형항 | KEEP |
| §4 stretched→§dist 다리 | ✓ | ✓ §6/§7 | KEEP |
| §8 worked example(FWHM 91·높이) | ✓ | △ 3×3 예시뿐 | **KEEP+재작성**: master 파라미터 표/S1이 이 수치 규모를 \emph{명시 인용}(피팅 anchor) |
| §8 3×3 칸별 walkthrough | ✓ | ✓ 표 설명 | KEEP |
| §9 융합 worked | ✓ | △ | **KEEP+재작성**: OCV-anchored 절차(S$_1'$~)가 융합 개시 기준을 \emph{사용} |
| §11 경쟁기전 진단표 | ✓ | △ | **KEEP+재작성**: falsify (i)(ii) 본문이 표 행을 \emph{명시 참조}하며 전개 |

### Ch2 (orphan 다수 — CUT/TRIM 확정)
| 추가분 | 앞 | 뒤 | 결정·조치 |
|---|---|---|---|
| §2.2 g''(eq:hys_gpp) | ✓ | ✓ §4 slope | KEEP |
| §2.2 T_c=Ω/2R | ✓ | ✓ §4·§5·§8 | KEEP |
| §2.2 미시기원 z[ε_AB..] | ✓ | △ Ω 동기 | KEEP(축약·Ω 정의로 흡수) |
| §2.2 common tangent | ✓ | ✓ binodal=가역기준 | KEEP |
| §2.2 **lever rule $f^+$** | ✓ | ✗ 미사용 | **CUT**(두-상 분율 어디도 안 씀) |
| §2.2 vdW/Maxwell | ✓ | △ §4 | **KEEP+재작성**: §4 비단조 전위가 vdW·Maxwell을 \emph{명시 도구}로 사용(평탄=가역기준 도출) |
| §2.3 **CNT 식 $\Delta G^\ast\propto\gamma_s^3/\Delta g^2$** | ✓ | ✗ 정성만 | **TRIM**(정성 핵생성 장벽만 남기고 식·$r^\ast$ 제거; 단 $\gamma_j$ 근거로 §5가 \emph{명시 인용}하면 핵심 1줄 KEEP) |
| §2.4 Dreyer 풍선 | ✓ | △ §5 다입자 | KEEP(§5 $\gamma_j$ 분산에 연결) |
| §6 수치 예제 | ✓ | ✓ ΔU_hys | KEEP |
| §7 **과전압 3분해(ohmic·ct·확산)** | ✓ | ✗ Ch2 피팅 lumped $R_n$ | **TRIM**(Ch2는 lumped $R_n$; 3분해는 Ch3 §5가 담당 → Ch2서 1줄로 축약, 중복 제거) |
| §8 **Preisach/FORC/hysteron** | ✓ | ✗ 부분cycle 범위밖 | **TRIM**(return-point memory + $h_j$ 보간만 — §9 major-loop 보간에 연결; FORC·hysteron 엘라보 제거) |
| §10 식별성(Ω/γ 3온도) | ✓ | ✓ 피팅 | KEEP |

**CUT/TRIM 확정 후보**: lever rule(CUT) · CNT 식(TRIM) · Ch2 과전압 3분해(TRIM) · Preisach/FORC(TRIM). → Decisions Required 에서 박사님 확인.

## Phase Range
| Phase | 이름 | Steps | 대상 |
|---|---|---:|---|
| K0 | keep/cut 확정(박사님 GO/조정) | 1 | 결정표 |
| K1.x | Ch1 절 재작성 통합(§8·§9·§11) | 2–9 | KEEP 강화(뒤 사용처 신설) |
| K1.v | Ch1 빌드·정합·커밋 | 10–11 | |
| K2.x | Ch2 절 재작성 통합/제거(§2·§7·§8) | 12–22 | CUT/TRIM + KEEP 재작성 |
| K2.v | Ch2 빌드·Codex·커밋 | 23–25 | |

## Non-goals
- 새 \emph{물리} 추가 금지(통합·제거·사용처 신설). 정확성 확인 유도·식·식번호·인계 번호 보존.
- CUT는 \emph{미사용 orphan}만 — 정확 물리 손실 X. 단일문건 규율·NO Workflow·챕터 통째 배치 X.

## Implementation Changes
- 수정: `graphite_ica_ch1.tex`·`graphite_ica_ch2.tex`(절 재작성 Edit). 빌드 pdf.
- Result: `PHASE_INTEG_RESULT.md`(항목별 앞 도입·뒤 사용 위치 또는 CUT 사유). Ledger: `PHASE_INTEG_LEDGER.md`.

## Phase K0 — keep/cut 확정
- **Step 1.** 위 결정표를 박사님이 확정(GO 또는 특정 CUT/TRIM 항목 "살려라" 지정 → 그 항목은 사용처 신설로 KEEP). 그 전엔 K1 착수 X(load-bearing). \emph{"결정표대로 GO" 시 표 그대로 확정하고 즉시 K1.1}.
- **Gate GK0:** 항목별 KEEP/CUT/TRIM 최종 확정 기록.

## Phase K1.x — Ch1 절 재작성 통합
- **Steps 2–9.** §8: worked example 수치를 \emph{최종식 파라미터 표/S1 anchor}가 인용하도록 §8.3/§master 재작성(예시→피팅 규모 근거). §9: 융합 개시 기준을 OCV-anchored S$'$ 절차가 \emph{입력으로 사용}하도록 재작성. §11: 진단표를 falsify 본문이 행별로 끌어 전개(표=논리의 뼈대). 절마다 빌드·앞 절 정합.
- **Gate GK1.x:** 각 KEEP 항목이 \emph{뒤 사용처에서 실제 인용}됨(grep \eqref/\S\ref/표 참조), 앞 도입 자연, 라벨·식 보존, 빌드 clean.

## Phase K1.v — Ch1 빌드·커밋
- **Steps 10–11.** 2-pass 0/0; "Ch1 orphan 0" 재확인; 커밋·푸쉬.

## Phase K2.x — Ch2 절 재작성 통합/제거
- **Steps 12–22.**
  - §2.2: lever rule \textbf{CUT}; common tangent·vdW는 \emph{binodal=가역 평형 기준}·§4 도구로 \emph{쓰이게} 재작성; 미시기원 축약.
  - §2.3: CNT를 \emph{$\gamma_j$ 의 물리적 근거}로 §5 boundbox가 명시 인용하게 1줄로 \textbf{TRIM}(식 제거, 정성+연결 유지).
  - §2.4: Dreyer를 §5 $\gamma_j$ 분산에 연결.
  - §7: 과전압 3분해 \textbf{TRIM}(lumped $R_n$ 1줄; 상세는 Ch3 인계 언급 없이 제거 — Ch2 spine은 $R_n$ 만).
  - §8: Preisach/FORC \textbf{TRIM} → return-point memory + $h_j$ 가 \emph{§9 major-loop 보간을 뒷받침}하게 최소화.
  - 절마다 빌드·앞 절·Ch1 정합.
- **Gate GK2.x:** CUT 항목 제거 확인(grep 0), KEEP 항목 뒤 사용처 인용 확인, 단일문건 규율, 라벨·식·인계 보존, 빌드 clean.

## Phase K2.v — Ch2 빌드·Codex·커밋
- **Steps 23–25.** 2-pass 0/0; "Ch2 orphan 0" 재확인; Codex foreground(통합 물리 무손상·연결 타당·orphan 0·CUT 부작용 0); result+ledger; 커밋·푸쉬.

## Implementation Interfaces
- 처리 단위 = 결정표 1행. KEEP = 절 재작성으로 앞 도입+뒤 사용 양 고리; CUT = 제거; TRIM = 핵심만+연결.
- "뒤 사용" 실체 = 최종식 항·파라미터 표·피팅 단계·진단·환원검산이 그 결과를 \eqref/\S\ref/수치로 인용.
- Result 11항목·Ledger 12-col.

## Test Plan
- 빌드 2-pass 0/0. 결정표 전 항목 {KEEP-통합 검증 / CUT-제거 검증}. 각 KEEP의 앞·뒤 위치 result 명시(완결성 증명). 라벨·식번호·인계 grep 보존. 단일문건 규율 grep. Codex foreground 1회.

## Assumptions
- A1: CUT/TRIM으로 \emph{양이 줄 수도} 있음 — 완결성이 양보다 우선(박사님 "교과서를 저따위로 쓰면 고소"). "양 늘린 건 좋다"는 \emph{쓰이는 한}에서 유지.
- A2: CUT은 미사용 장식/중복만; 정확 물리·인계는 보존.

## Decisions Required (Phase K0 — GK0)
- **D-1 CUT 확정**: lever rule(\textbf{CUT}). 동의? 아니면 두-상 dQ/dV 분율 설명에 사용처 신설해 KEEP?
- **D-2 TRIM 확정**: (a) CNT 식→정성, (b) Ch2 과전압 3분해→lumped, (c) Preisach/FORC→return-point+$h_j$. 각 동의? 특정 항목 "완전 살려라"면 사용처 신설로 KEEP.
- \emph{권고 = 표대로(lever rule CUT · 나머지 TRIM)}. "결정표대로 GO" 시 그대로 실행.

## Correction History
- 2026-06-09 v1→v2: 박사님 "거의 다시 쓰는 수준·살릴지 버릴지 확정·제대로 작성·교과서를 저따위로 쓰면 고소" 수용. v1의 막연한 "연결 한 줄"을 \textbf{절 재작성 수준 + 항목별 keep/cut 확정표}로 격상. orphan(lever rule·CNT식·Ch2 3분해·Preisach)을 CUT/TRIM 확정, KEEP은 뒤 사용처 신설로 완전 통합. GK0 확정 시 K1→K2 절별 연속.
