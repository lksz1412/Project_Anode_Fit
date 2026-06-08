# Ch2 내용 심화 + 구조·표기 수정 계획 (PHASE_CM 이어 Phase 3.x)

## Summary
박사님 지적(6-08): (1) Ch2 절 번호가 챕터에 안 묶여 "11.1"로 뜸, (2) 식 2.13(eq:hys_master_center)이 박스가 길어 칸을 벗어남, (3) **내용이 교과서 치고 너무 짧다(9p), 더 보강 필요**. 본 계획은 (a) 절 번호를 챕터 anchor(Ch2=2.x, Ch1=1.x)로 묶고, (b) 긴 박스식(2.12·2.13)을 다단으로 깨 칸 안에 넣고 양 챕터 overfull hbox 0, (c) **Ch2를 교과서 깊이로 실질 보강** — 정규용액 자유에너지·상분리·핵생성·동역학 분극·기억을 비약 없이 전개하고 수치 예제를 더한다. 정확성 확인 유도는 보존, 추가는 진짜 물리 내용(패딩·disclaimer 적층 금지). 대상: `graphite_ica_ch2.tex`(주), `graphite_ica_ch1.tex`(표기만).

## Current Ground Truth
- Ch2 현재 9p(빌드 clean), 신규 §종합 모델식(sec:hys_master) 포함. 직전 커밋 fe53739.
- Ch2 절: §1 기호 … §11 종합모델식(11 sections). 절번호 flat(1–11) → "11.1" 발생.
- eq:hys_master(2.12)·eq:hys_master_center(2.13) 단일행 박스 → 2.13 overfull(Codex 정의역 가드로 길어짐).
- 핵심 유도(V_eq 2.5·spinodal 2.7·ΔU_hys 2.10·master 2.12/2.13) 손검·Codex 검증 완료(MAJOR 0).
- 이전 ledger `PHASE_CM_EXECUTION_LEDGER.md` Next Step=done(2.8). 본 계획 cumulative step 55부터.

## Phase Range
| Phase | 이름 | Steps | 대상 |
|---|---|---:|---|
| 3.1 | 구조·표기 수정 | 55–58 | Ch1·Ch2 \thesection; 2.12·2.13 다단; overfull 전수 |
| 3.2 | §2.2 정규용액 자유에너지 심화 | 59–63 | sec:hys_bg §2.2 |
| 3.3 | §2.3 상분리·핵생성 심화 | 64–68 | sec:hys_bg §2.3·flagbox |
| 3.4 | §4 spinodal(전위) vdW loop 심화 | 69–72 | sec:hys_spinodal |
| 3.5 | §5 분기·ΔU_hys 준안정·γ_j 심화 | 73–76 | sec:hys_branch |
| 3.6 | §7 동역학 분극 대폭 심화 | 77–81 | sec:hys_pol |
| 3.7 | §8 부분 cycle 기억 심화 | 82–84 | sec:hys_memory |
| 3.8 | 수치 예제(흑연 stage 추정) | 85–87 | 신규 박스/절 |
| 3.9 | 빌드(overfull 0)·Codex·커밋 | 88–90 | 전체 |

## Non-goals
- 정확성 확인 유도(V_eq·spinodal·ΔU_hys·master) 재유도·변경 금지 — 보강은 \emph{앞뒤 물리·동기·중간단계·예제} 추가.
- 패딩·disclaimer 적층·메타발언 금지(교과서 prose). 분량은 물리가 요구하는 만큼.
- 단일문건 규율 유지(§1 Chapter-1 언급 0, 인계/전달/결론 절 신설 X). Ch1만 기반(BV/DFN X).
- 기존 라벨·식 번호 보존(신규만 add). Codex/·Archive_*·zip 미혼입.
- 챕터 통째 배치 작성 금지 — 절 단위.

## Implementation Changes
- 수정: `graphite_ica_ch2.tex`(절별 Edit, 내용 add), `graphite_ica_ch1.tex`(\thesection 1줄).
- 빌드: `graphite_ica_ch1.pdf`·`graphite_ica_ch2.pdf` 재생성.
- Result: `Claude/results/PHASE_CM2_ch2-deepening_RESULT.md`. Ledger: 기존 `PHASE_CM_EXECUTION_LEDGER.md` 에 Phase 3.x 행 추가.

## Phase 3.1 — 구조·표기 수정
- **Steps 55–58.** (a) Ch2 `\renewcommand{\thesection}{2.\arabic{section}}`(완료), Ch1 `{1.\arabic{section}}`; (b) eq:hys_master(2.12)·eq:hys_master_center(2.13)를 `\boxed{\begin{aligned}…\end{aligned}}` 다단으로; (c) 양 챕터 빌드 로그 `Overfull \hbox` 전수 확인·잔여 박스 분해.
- **Gate G3.1:** 빌드 로그 `Overfull \hbox`(>0pt, 본문 수식) 0건; 절 번호 TOC 가 `2.1…2.11`/`1.1…`로; eq 2.12·2.13 박스 텍스트폭 내.
- 중단: 없음. 다음: G3.1 PASS.

## Phase 3.2 — §2.2 정규용액 자유에너지 심화
- **Steps 59–63.** §2.2에 추가: 혼합 엔트로피의 조합론 유도(Ch1 식 1.7 인용 + 본 장 맥락), 평균장 상호작용 enthalpy의 쌍 확률 $\propto\xi(1-\xi)$ 근거, 그 합 $g_j(\xi)$의 \emph{이중 우물} 형태(왜 $\Omega_j$ 크면 가운데 볼록), 공통 접선=두 상 \emph{등화학퍼텐셜}·lever rule, van der Waals 등온선과의 유추.
- **Gate G3.2:** §2.2에 (엔트로피 유도·이중우물·공통접선=등μ·lever rule·vdW 유추) 5요소 문장/식 존재(grep); 추가식 손검(g 대칭·$g''$); 빌드 clean.
- 중단: 없음. 다음: G3.2 PASS.

## Phase 3.3 — §2.3 상분리·핵생성 심화
- **Steps 64–68.** §2.3 확장: binodal(공통접선) vs spinodal(변곡) 자유에너지 기하 명시, 준안정 영역의 \emph{국소 안정·전역 불안정}, 고전 핵생성 이론(critical nucleus·장벽 $\Delta G^*\propto\gamma_s^3/\Delta g^2$) 정성, 장벽 크면 spinodal 과주행. flagbox 다입자(Dreyer): 입자별 순차 전환·평활화를 더 전개.
- **Gate G3.3:** §2.3에 (binodal/spinodal 기하·준안정 물리·핵생성 장벽·과주행) 존재; flagbox 확장; 빌드 clean.
- 중단: 없음. 다음: G3.3 PASS.

## Phase 3.4 — §4 spinodal(전위) vdW loop 심화
- **Steps 69–72.** §4에 추가: 비단조 $V_{\eq,j}(\xi)$가 van der Waals loop 와 동형(전위↔압력, $\xi$↔부피)임을 명시, 음의 기울기=역학적 불안정의 물리, Maxwell 등면적 작도가 binodal(평형 평탄전위)을 줌, 실제 충방전은 그 평탄선이 아니라 분기를 따라감.
- **Gate G3.4:** §4에 vdW/Maxwell 유추·불안정 물리 존재; eq:hys_slope·spinodal 식 불변; 빌드 clean.
- 중단: 없음. 다음: G3.4 PASS.

## Phase 3.5 — §5 분기·ΔU_hys 준안정·γ_j 심화
- **Steps 73–76.** §5에 추가: 준안정 분기 따라가기의 히스테리시스 loop 그림(말), 방전(상승)이 극대 $\xi_s^-$·충전(하강)이 극소 $\xi_s^+$를 \emph{왜} 택하는지(진행 방향 단조성), nucleation이 spinodal 전에 전환시켜 gap 축소($\gamma_j$ 물리), 다입자 평활화의 정량 의미.
- **Gate G3.5:** §5에 (분기 선택 근거·γ_j 물리·다입자) 확장; eq:hys_branchU·hys_dU 불변; 빌드 clean.
- 중단: 없음. 다음: G3.5 PASS.

## Phase 3.6 — §7 동역학 분극 대폭 심화
- **Steps 77–81.** §7(현재 최박)에 추가: 과전압 3원(ohmic $|I|R_n$·전하전달·고체확산) 분해, 충/방전에서 \emph{반대 부호}로 더해짐, kinetic lag가 peak를 진행방향으로 미는 정량(Ch1 $L_{q,j}$·식 1.19), 율 의존($\Delta V_\pol\propto|I|$), GITT 완화로 참/분극 분리 절차, 수치 추정(예 $R_n$·$|I|$ 대입 $\Delta V_\pol$).
- **Gate G3.6:** §7 분량·요소(과전압 분해·부호·kinetic shift·율 의존·GITT·수치) 존재; eq:hys_pol 불변; 빌드 clean.
- 중단: 없음. 다음: G3.6 PASS.

## Phase 3.7 — §8 부분 cycle 기억 심화
- **Steps 82–84.** §8 확장: return-point memory 의 물리(되돌림점이 분기 상태 기억), Preisach/scanning curve 그림(말), first-order reversal curve(FORC) 개념, $h_j$ 보간이 major-loop 양끝을 잇는 방식.
- **Gate G3.7:** §8에 (RPM·Preisach/scanning·FORC·$h_j$ 보간) 존재; 범위 boundbox 유지; 빌드 clean.
- 중단: 없음. 다음: G3.7 PASS.

## Phase 3.8 — 수치 예제(흑연 stage 추정)
- **Steps 85–87.** 신규 \emph{예제 박스}(또는 §종합 모델식 앞): 흑연 한 stage 전이에 대표값($\Omega_j$, $T$, $\gamma_j$) 대입 → $T_{c,j}$, $\xi_s^\pm$, $\Delta U_j^\hys$(mV), 분기 peak 간격, $|I|R_n$ 분극을 수치로 산출해 \emph{식이 실제 mV 규모를 내는지} 보인다.
- **Gate G3.8:** 예제에 (Ω·T·γ 입력 → T_c·ξ_s·ΔU_hys·peak 간격 출력) 수치, 손검(54 mV 류 규모) 일치; 빌드 clean.
- 중단: 없음. 다음: G3.8 PASS.

## Phase 3.9 — 빌드·Codex·커밋
- **Steps 88–90.** xelatex 2-pass 양 챕터, overfull hbox 0·undefined 0; Ch1↔Ch2 정합 재확인; Codex foreground 적대검수(신규 보강분 물리·비약·정합, MAJOR 0, Ch1 원문 대조); result+ledger; ch1·ch2 tex+pdf 명시 스테이징 커밋·푸쉬.
- **Gate G3.9:** 빌드 0 undefined·0 overfull; Codex MAJOR 0(시정 후); Read Coverage; git 해시.
- 중단: Codex FAIL 유지 시(정지조건 #3). 다음: 종합 보고 1회.

## Implementation Interfaces
- 보강 prose = (물리 동기 → 중간단계 빠짐없이 → 검산/극한 → 해석/예제) 4요소. 인라인 cramming 금지(별행).
- 다단 박스: `\boxed{\;\begin{aligned} … \\[3pt] … \end{aligned}\;}`.
- Result 11항목·Ledger 12-col([[feedback_phase_execution_loop]]).

## Test Plan
- 빌드 2-pass: `Overfull \hbox` grep 0(본문 수식폭), undefined 0, 페이지 수 기록(목표 Ch2 ≥14p 실질 보강).
- 추가식 손검(차원·극한·대칭). 단일문건 규율 grep(§1 Chapter-1 0). 라벨 보존 grep.
- Codex 적대검수 foreground 1회(보강분), Ch1 원문 대조.

## Assumptions
- A1: 수치 예제 대표값(예 $\Omega_j\approx4RT$, $T=298$K, $\gamma_j\approx0.5$)은 규모 예시 — 실측 아님 명시.
- A2: 절 번호 anchor(2.x)가 박사님 의도("11.1" 제거). 다른 표기 원하면 조정.
- A3: 보강 목표 Ch2 14–18p(물리가 요구하는 만큼, 인위 분량 X).

## Correction History
- 2026-06-08 v1: 작성. 박사님 "11.1 절·2.13 칸 벗어남·내용 아직 부족(교과서 치고 짧다)" 수용. PHASE_CM(Phase 1–2) 이어 Phase 3.x, cumulative step 55부터. "계획서 세우고 보완까지 쭉 이어서" 지시 → 본 계획 저장 후 Phase 3.1→3.9 연속 실행.
