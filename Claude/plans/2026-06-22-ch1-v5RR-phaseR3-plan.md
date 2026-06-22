# Phase R3 상세 플랜 — N회 가변-청크 수렴 (V5RR)

> 마스터 = MASTER ROADMAP. 수렴 = 연속 2R 확정결함 0. Phase 끝 commit+push.

## 목표
R1(절별)·R2(수식별) 위에서 렌즈·청크를 새로 돌려 잔결함 사냥 + R1/R2 수정의 새 결함 0 확인 → 수렴.

## Steps
- **R3a (Step 23, 검수 sub ×2 + master 병렬)**:
  - 시각 sub: pdftoppm 로 v5.pdf 전 식·그림 페이지 렌더 판독(잘림·겹침·overfull 0, R1/R2 편집 줄 렌더 정상).
  - 홀리스틱 sub: v5 전체 통독(G-follow end-to-end) + **R1/R2 편집 6영역**(§1.8 꼬리·§1.4 chisum·§1.9 LqV·§1.7 eqpeak·§1.15 dHeff·§1.12 Ifuse) 재검(새 결함·깨진 참조·의미 변질 0).
  - master 직접: 인용-사실(bib 사용 정합) + v5↔v3 보존 최종 spot.
- **R3b (Step 24, master)** — R3a 확정 결함(있으면) 수정 → 재빌드. 0이면 수렴 라운드 1.
- **R3c (Step 25, master)** — fresh 재확인(편집 영역 직접 재정독) → 연속 2R 0 확인 → 수렴.
- **Step 26 (master)** — R3 result+ledger, Gate R3, commit+push.

## Gate R3
연속 2R 확정결함 0 · build 0/0/0 40p · comment 15/15 · 편집영역 렌더 정상.

## Assumptions
R1/R2가 이미 다회 검수에 해당 → R3는 수렴 확인 위주(렌즈 전환 시각·홀리스틱·인용). 새 결함 발견 시 step 연장.
