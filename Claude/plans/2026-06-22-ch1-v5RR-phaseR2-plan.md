# Phase R2 상세 플랜 — ★수식별 루핑 (V5RR 핵심)

> 마스터 = MASTER ROADMAP. 입력 = V5RR_baseline_map.md §4 의존 그래프. Phase 끝 commit+push.

## 목표 (사용자 핵심 강조)
식 N(1.1~1.97) 각각을, 그 식이 의존하는 **관련 모든 선행식**(직전이 아니라 의존집합 전부)에 대해 **물리·화학·수리적 전개 타당성**을 적대 재유도로 검증. 4판정: (i)물리 (ii)화학 (iii)수리(대수 한 단계씩·부호·차원·극한·근사) (iv)선행식 정합(인용 선행식과 변수·가정 일치, 숨은 flip/순환 0).

## Steps (식 97개를 의존 클러스터 7로 분담)
- **Wave A (Step 13–16, 검수 sub ×4 병렬)**:
  - C1: 1.1–1.18 (Eyring 근본속도→Gibbs/μ(θ)→전기화학 평형 eqcond)
  - C2: 1.19–1.32 (affinity→BV→detailed balance→정지점→logistic→isotherm→weff)
  - C3: 1.33–1.51 (g(ξ)·공통접선·spinodal·omegaaxis→전하보존·V_n·dQdV·eqpeak)
  - C4: 1.52–1.63 (dUdT + 지연ODE·기억적분·꼬리 전 사슬)
- **Wave B (Step 17–20, 검수 sub ×3 + Codex 교차)**:
  - C5: 1.64–1.74 (유효장벽 keff·∂lnL_q/∂V→Arrhenius·입자분포·중첩)
  - C6: 1.75–1.83 (닫힌식·면적보존·kinshift→다전이 합산·융합)
  - C7: 1.84–1.97 (비단조 V_eq·spinodal 대입→gap 닫힌꼴·임계멱·분극분해→통합식 master/hysmaster·dHeff·logslopeT)
  - **Codex(codex:rescue)**: 부호-임계 사슬 독립 적대 재유도(1.19–1.41 평형/상분리 + 1.84–1.97 히스 부호) — 교차모델.
- **Step 21 (master)** — 삼각검증(sub↔Codex↔본문 직접 재유도) → 확정 결함만 v5 직접 수정 → 재빌드 → ledger.
- **Step 22 (master)** — R2 result+ledger, Gate R2, commit+push.

## Gate R2
97 식 전부 (i)~(iv) 판정 완료(미판정 0) · 확정 결함 수정·재빌드 0/0/0 · comment 15/15 · 약점3(1.95/1.75/1.83) 처리 결론.

## Assumptions
선행집합은 baseline 그래프 기준이되 sub가 누락 선행 발견 시 추가 보고. v3 자체 물리결함은 D2(보존+추정 보고), v5 변환결함만 수정. Codex는 파일 수정 금지(검토 의견만).
