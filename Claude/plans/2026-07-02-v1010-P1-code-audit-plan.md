# P1 세부 스텝 계획 — 코드 검증·플로우차트 앵커 (9종 경쟁-체리픽)

> 마스터 = `2026-07-01-v1010-code-doc-sync-bdd-fitting-plan.md` §P1. result = `results/process/V1010_P1_code-audit_RESULT.md`. 대상 = `docs/v1.0.10/Anode_Fit_v1.0.10.py`(흑연 음극 dQ/dV, 695줄). **읽기 전용 분석 — 코드 수정 X**(개정은 P4).

## P1 산출물 (3종, 한 문건으로)
1. **플로우차트 맵**: 입력(생성자 인자·GRAPHITE_STAGING_LIT) → `equilibrium` → `dqdv`(분극 V_n·꼬리 L_V·히스 branch) → `curve`. 각 함수(func_w/U_j/U_j_hys/ksi_eq/L_q/dU_hys/U_branch/dH_a_eff/chi_d + 메서드)별 **물리식 + 코드 줄 근거**.
2. **조건 audit**: "BDD 음극 dQ/dV 물리수식 피팅 함수"로서 충족도·결함(가드 None/0·死코드·시그널/호출체인 정합·면적보존). 흑연 음극 전용(LCO·발열·전자엔트로피 부재) 확정.
3. **피팅 파라미터 인벤토리**: n_j·U_j·Ω_j·dH_a·dS_rxn·χ·L_V·z_cut·dVdq_qa 등 — 각 **역할 + 곡선 어느 영역(peak 위치/폭/꼬리/히스)을 지배** + 초기값 + 자유/고정 초벌.

## 9종 경쟁-체리픽 단계 (master = 본 세션)
- **Step 1 — 9 독립 드래프트**: 3 Sonnet(S1-3) · 3 Opus(O1-3) · 3 Codex(C1-3), 상호 통신 X. 각자 Serena(get_symbols_overview→find_symbol→find_referencing_symbols)로 위 3종 산출 → `results/process/V1010_P1_draft_<id>.md` 저장. **커밋①**(9 드래프트).
- **Step 2 — 검토1(별도 세션) + 보완**: 검토 agent(작업과 다른 세션)가 9 드래프트 교차검증 — 물리식 정확성·맵 누락·파라미터 지배영역 오류·결함 진위. refute+가장약한1곳+빈통과금지. → 보완. **커밋②**(검토1+보완).
- **Step 3 — 검토2 + master 체리픽**: 검토2 후 master 가 9개 장점 통합 → `V1010_P1_map_v10.md`. **커밋③**(체리픽).
- **Step 4 — adversarial 재검수(별도 세션) + finalizer**: 적대 검수(물리식·줄 근거·파라미터 지배영역 삼각검증) → master finalizer → `V1010_P1_code-audit_RESULT.md`(P1 result, 11항목) + ledger 갱신. **커밋④**(adversarial+finalizer).

## Gate (P1 종료)
- 플로우차트 맵 = 코드 전 함수 커버(누락 0)·각 식에 줄 근거. 조건 audit 명령+증거. 파라미터 인벤토리 = 각 파라미터 지배영역 확정(추정/근거미발견 4-tier 표기). result 11항목·Read Coverage 명시.

## 주의
- 검수 = **작업/드래프트와 다른 세션**(Agent, Workflow X). commit = master 전용. 추정 금지(코드 줄 근거). 원본 코드 불변.
