# V1020 킥오프 조사 ② — v1.0.19 실행 이력·검수 체계·이월 항목 (기획 세션 sub-agent 조사, 2026-07-16)

> 목적: v1.0.20 이 재사용할 검증된 작업 체계의 좌표 + 범위 판단 근거. 디스크 보존본.

## 1. v1.0.19 기록 세트 (`results/process/`)
- `V1019_EXECUTION_LEDGER.md`(마스터 레저) · `V1019_ASSET_CHECKLIST.md`(Ch1 자산 336) · `V1019_CH2_ASSET_CHECKLIST.md`(Ch2 자산 133) · `V1019_UNION_DEFECTS.md`(Ch1 10창 union 24건) · `V1019_CH2_UNION_DEFECTS.md`(CU-1~11) · `V1019_FINAL_REVIEW_UNION.md`(R-P1 5창) · `V1019_CONTINUITY_JUDGMENT.md`(K-P3 연속성) · FABLE_BRIEF 3종.

## 2. v1.0.19 phase 구조 (전 트랙 완결)
- **Ch1 트랙 P1~P5**: 준비(자산 336) → Fable 전면 재작성(61p·구조 재설계 5건) → 10창 검수(union 24) → Fable 최종수정(24/24) → 마감.
- **Ch2 트랙 C-P1~C-P5**: 동일 3단계(자산 133·CU-1 부호 정정 = 사이클 유일 물리 결함·전건 반영).
- **코드·정합 트랙 K/R**: K-P0 수치 재검증(7/7) → K-P1 코드 개정(additive·회귀 13/13 bit-exact) → K-P2 doc↔code 동기 → K-P3 샘플·연속성(불연속 0) → R-P1 3종 정합+완결 검수(5창 RW1~RW5, CRITICAL 물리 0; C = round-trip 데모 부재 → fit_roundtrip_demo.py 신설로 해소) → R-P2 마감.
- ※중간 레저의 "코드 재-sync 이월" 기재는 K/R 트랙이 이후 실제 완료 — 미해결 아님.

## 3. 검수 체계 (v1.0.20 P7 이 재사용)
- **10창 = 9 비-Fable + 1 Fable(물리 적대검산 독립창)**, 창별 3축 = ①신본 결함 ②★이전본 대비 regression/자산 유실 ③구조 재설계 부작용. 규율 = refute + 가장 약한 1곳 + 빈 통과 금지 → master 삼각검증·union → 수정. 고위험 창은 상위 모델 배정.
- **R-P1 5창**: RW1 Ch1↔code / RW2 Ch2↔code / RW3 Ch1↔Ch2+완결성 / RW4 G-follow(학부 추적 가능) / RW5 G-usable(문건만으로 피팅 가능).
- **2대 무결 gate**: 물리·화학·수학 골격 오류 0 + 자산 회귀 0(자산 앵커 `% 자산:` 주석 대조).

## 4. 이월·대기 항목 (v1.0.20 범위 판단)
- **레저 최종(R-P2) 이월 3건** — 전부 물리/실측 확장이라 **v1.0.20(설명·서지 증판) 범위 밖 유지**:
  1) LCO tier-2/3 실측 초기값 2) 다온도 전자항 T-복원(현 T_ref 동결) 3) total heat q_irr 3분해.
- **RW3-11 부록 편입 여부** = 사용자 결정 대기로 기재돼 있으나, v1.0.14 에서 "spinodal 부록 = 별도 문건 유지 확정" 기존 결정 존재 → **별도 유지 유지**(재질의 X).
- **V1018 잔여 후보(M-1~S-3)**: 다수가 v1.0.19 에서 이미 해소(fig:reversal→U-22, Ch2 라벨 노출→CU-3, L_V→U-9). v1.0.20 에서 재등재 전 교차 확인 필수.
- **ROADMAP_future_physics(제안 2~5)**: Ω(ξ)[차기 후보 1순위·침습 HIGH]·Cahn-Hilliard γ_j·Butler-Volmer·PSD — 외부 위임/실측 대기, 범위 밖.
- v1.0.16 물리-데이터 이월(다온도 per-T n 진단·LCO 실측값·서지 재확인 잔여)도 실측 대기 — 범위 밖(서지 재확인 몫만 P1 이 흡수).

## 5. 계획 양식 근거
- plans/INDEX.md 규약: 마스터+페이즈 세부 계획 → 계획 폴더, phase 마다 result+ledger. 양식 = [[feedback_plan_template_11sections]](11-section·누적 step·1챕터=1Phase 금지) + [[feedback_phase_execution_loop]](5단계 루프·Result 11항목·Ledger 12컬럼). 실체 예 = `Claude/plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md`.
- ★v1.0.20 한정 위치 override(사용자 2026-07-16): 계획 = `docs/v1.0.20/plans/`, 이력 = `docs/v1.0.20/results/`.
