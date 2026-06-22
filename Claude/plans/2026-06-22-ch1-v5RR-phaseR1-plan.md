# Phase R1 상세 플랜 — 절별 루핑 (V5RR)

> 마스터 = MASTER ROADMAP. baseline = V5RR_baseline_map.md. Phase 끝 commit+push.

## 목표
§1.1~§1.17 절별(절=청크) 재검토: (a) 물리·화학·수리 건전성 (b) v5↔v3 보존(누락·왜곡 0) (c) 절내 정합(산문 압축 후에도 도입·전개·닫힘 유지, orphan 0). + 빌드 결함(overfull 2) 봉합.

## Steps
- **Step 5 (master)** — overfull OF1(§1.8 L980)·OF2(§1.17 L1838) 봉합(내용 불변 문장 분할) → 재빌드 overfull 0 확인.
- **Step 6–10 (검수 sub ×5, 병렬)** — 절 그룹 분담, 각 head→tail 정독:
  - sub A: §1.1·§1.2·§1.3 (기호규약·근본속도식·열역학다리)
  - sub B: §1.4·§1.5 (평형유도·상분리)
  - sub C: §1.6·§1.7·§1.8 (관측축·평형peak·꼬리)
  - sub D: §1.9·§1.10·§1.11·§1.12 (전위가지·온도가지·합성·겹침)
  - sub E: §1.13·§1.14·§1.15·§1.16·§1.17 (히스테리시스·분극·통합·반증·코드)
  렌즈 = 물리·화학·수리 건전성 + v5↔v3 보존 + 절내 정합. refute+가장약한1곳+빈통과금지. v3 해당 줄범위 제공해 대조.
- **Step 11 (master)** — 삼각검증(sub 지적 ↔ baseline ↔ 본문 직접) → 확정 결함만 v5 직접 수정 → 재빌드 → ledger.
- **Step 12 (master)** — R1 result + ledger, Gate R1, commit+push.

## Gate R1
overfull 0 회복 · 절별 보존 감사 PASS(누락·왜곡 확정결함 수정) · build_gate Opus_v5 0/0/0 · comment_gate 15/15.

## Assumptions
절별 sub 지적은 master 삼각검증 후에만 수정(빈 통과·과잉수정 방지). v3 자체 물리는 기준(D2) — v5 변환결함만 수정.
