# Phase R0 상세 플랜 — Baseline & 식 의존 그래프 (V5RR)

> master plan = `2026-06-22-ch1-v5-comprehensive-rereview-MASTER.md`. 본 Phase 끝 commit+push.

## 목표
R1·R2 가 소비할 **권위 baseline** 산출: 빌드 결함 진단 + v5↔v3 식 97개 대응표 + ★식 의존 그래프 + §1.18 누출 점검 + 변환 변동 인벤토리.

## Steps
- **Step 1 (master 직접)** — v5 overfull 2건(L979–981, L1836–1840) 영역 정독 → 원인·수정안 확정(내용 불변 줄바꿈/폭). §1.1 기호표 정독 → §1.18 기호(ψ·B·κ·ξ_c·ξ_open/close·ΔV_stack) 누출 0 확인. sec:stacking·eq:xistack 등 참조 0 grep 확인.
- **Step 2 (매핑 sub, 병렬 1)** — v5 전문 + v3 전문 head→tail 정독 → (a) 식 97개 v5↔v3 1:1 대응표(verbatim/변형 + 변동 내용) (b) ★의존 그래프(식별 선행식 집합) (c) 승격 중간식(무번호 equation*) 목록·삽입 위치 (d) figure 목록. return 만(파일쓰기 X).
- **Step 3 (master)** — Step 1+2 통합 → `Claude/results/V5RR_baseline_map.md` 작성(§B 형식). 매핑 sub 결과 spot-check(무작위 8식 선행식 직접 확인).
- **Step 4 (master)** — R0 result 저장(PHASE_V5RR_ROUNDS_RESULT 에 R0 섹션) + ledger 행. **Gate R0**: 97 식 전부 대응·선행식 배정(미배정 0) + 빌드 결함 목록화 + §1.18 누출 0. commit+push.

## Gate R0
97/97 식 대응·선행식 배정 완료 · overfull 2 원인·수정안 확정 · §1.18 누출 0 · baseline_map.md 생성.

## Assumptions
매핑 sub 의 의존 그래프는 R2 적대 재유도의 *입력 가설* — master spot-check 후 R2 에서 식별 전수 검증되므로 R0 단계 sub 위임 정당(최종 판정 아님).
