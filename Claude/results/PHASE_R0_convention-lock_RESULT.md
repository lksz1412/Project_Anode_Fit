# Phase R.0 — 규약 잠금·전제검증 Result

**Date**: 2026-06-03 · **Plan**: `Claude/plans/2026-06-03-ch1-rerevision2-foundation-first-plan.md` · **Step Range**: 1–5

## Summary
Ch1 `graphite_ica_ch1.tex` 의 근본 결함(ξ_j 규약 모순)을 본문 손대기 전 잠갔다. Claude 손유도 + Codex `/codex:adversarial-review` 교차로 부호·보존 foundation 사슬을 검증하고, Codex 의 과잉 주장을 가려냈다. 최종 logistic·peak 공식은 전부 정확하며, 결함은 *유도 사슬의 정직성*(ξ를 점유율 θ인 양 사용)에 한정됨을 확정. 최종식 보존하며 유도만 정직화하는 surgical fix 로 확정.

## Step Range
Steps 1–5 (R.0). 다음 cumulative step = 6 (R.1).

## Inputs
- `Claude/docs/graphite_ica_ch1.tex` 전문(L1–803) 재정독(이번 세션, 추정 금지).
- Codex adversarial review (codex:codex-rescue, --fresh) — C1~C5 + 추가 hidden flip 판정.

## Read Coverage
- `graphite_ica_ch1.tex` L1–803 **전문 정독**(2 페이지 분할: L1–472, L473–803).
- 핵심 정독 구간: L129–172(notation), L182–222(stage/charge), L243–330(lattice-gas·eqcond·logistic), L375–382(dUdT), L398–445(relax·tail), L599–602(superpose), L675–709(simplefit·식별순서).

## 잠근 규약 (LOCKED)
- **θ_j ∈ [0,1]** = 전이 j 부격자 Li 점유율(분율). 방전(탈리튬화) 시 1→0 감소.
- **ξ_j = 1 − θ_j** = 방전(탈리튬화) 진행률, 0→1 증가. (전하균형 Q_j ξ_j = 전달 용량 — 보존.)
- **lattice-gas 화학퍼텐셜은 θ_j(점유율)의 켤레**: μ_Li(θ_j) = μ⁰ + RT ln[θ_j/(1−θ_j)] + Ω_j(1−2θ_j).
- **반쪽반응(삽입 기준 평형)**: Li⁺ + e⁻ + [ ] ⇌ Li_(graphite), μ̃_{e⁻} = μ⁰_{e⁻} − FV_n.
- **s = +1**(방전), s_I = +1. 전위 4종 V_n/V_app/V_drive/V_{n,OCV}, 반쪽전지 기준.

## 잠근 유도 (honest, hidden flip 0) — R.1 에서 본문 반영
1. eq:mu → **μ_Li(θ_j) = μ⁰ + RT ln[θ_j/(1−θ_j)] + Ω_j(1−2θ_j)** (θ로).
2. eqcond → 정직한 평형 balance: **μ_Li(θ_eq,j) = μ̃_{Li⁺} + μ⁰_{e⁻} − FV_n = −sF(V_n − U_j⁰) + μ⁰** 형(부호 **음(−)**; μ_Li 는 V_n↑ 시 감소 — 물리 정합). 상수 흡수 후 RT ln[θ_eq/(1−θ_eq)] + Ω_j(1−2θ_eq) = −sF(V_n − U_j), **U_j ≡ U_j⁰ − μ⁰/(sF)** (문서 L305 보존; Codex 의 +μ⁰/(sF) 불채택).
3. 이상 Ω=0, **θ_eq = 1 − ξ_eq 치환(부호 명시적 flip)**: RT ln[(1−ξ_eq)/ξ_eq] = −sF(V_n−U_j) ⇒ RT ln[ξ_eq/(1−ξ_eq)] = +sF(V_n−U_j) ⇒ **ξ_eq = 1/(1+exp[−s(V_n−U_j)/w_j])**, w_j=RT/F. ← eq:logistic(L315)와 **정확히 동일**(보존).
4. 따라서 eq:dxidV·eq:eqpeak·온도식 등 **downstream 전부 불변**(최종 ξ_eq 동일). 유도 사슬만 정직화.

## Execution Evidence — Codex 판정 + Claude 재판정 (4-tier)
| 항목 | Codex | **Claude 재판정(확정)** | 조치 |
|---|---|---|---|
| C1 ξ_j↔θ_j | CONFIRM (+U_j 부호 패치) | **확정**(근본). U_j 패치는 **구라/오바**(재유도로 L305 형 재현) → 불채택 | θ_j 도입·유도 정직화(R.1) |
| C2 dUdT 방향 | CORRECT(ΔS 미정의) | **확정**(라벨 결함). ΔG_j=−sF U_j=삽입 방향과 정합 | ΔS_j="삽입 반응 엔트로피" 라벨(식 보존) |
| C3 tail r_a | CONFIRM | **확정**. r_{a,j}=ξ_eq(q_a)−ξ(q_a), 0<r_{a,j}<1 | eq:simplefit 진폭 ×r_{a,j}, notation 추가(R.3) |
| C5 \|V_n−V_a\| | "simplefit엔 절댓값 없음=과확장" | **Codex 옳음**. eq:tail(L451)에만 한정 | eq:tail 단방향 도메인 1줄(R.2) |
| eq:relax L398 | "occupancy 호칭 잔존" | **확정**(C1 전파). 식 구조 정확, 단어 라벨만 | (1−ξ_j)=아직 탈리튬화 안 된 분율 등 라벨 수정(R.2) |
| eq:superpose L600 | "r_a(G) 누락" | **확정(MEDIUM)**. ∝식이나 C3 일관성 | 적분 안 r_a(G) 추가(R.3) |

## Validation (R.0 gate)
- **G-convention(부호 닫힘)**: PASS — 손유도가 hidden flip 0 으로 logistic 재현, Codex 와 핵심 합치.
- **Codex 교차**: PASS — C1·C3 CONFIRM 합치. C2·C5 는 Codex 가 라벨/범위 정밀화(수용). U_j 부호 하위주장은 Claude 재유도로 반증(불채택, 근거 기록).
- **전제검증**: PASS — "ξ_j=진행률" 전제가 lattice-gas 구간(L244)에서 깨짐을 인벤토리 대조로 확인.

## Gate
**PASS_CONVENTION_LOCK**. (조건: 손유도 flip 0 + Codex 합치 + U_j 반증 근거 기록.)

## Confirmed Non-Changes (의도적 보존)
- eq:logistic(L315)·eq:dxidV(L343)·eq:eqpeak(L356)·eq:dUdT 식 형태·온도식: 최종 결과 정확 → **불변**.
- U_j = U_j⁰ − μ⁰/(sF): 보존(Codex 패치 불채택).
- 사용자 기호 s·s_I·U_j·w_j·χ·Q_j·라벨·식번호: P5 보존.

## Open Issues / Decision Queue
- C11(lag r_j ↔ 속도 r_j± 기호 충돌): P5(기호 임의변경 X)와 충돌 가능 → R.2 도달 시 "개명 vs 각주 명시" 판단(개명은 사용자 확인 후). 현재 기본값 = **개명 보류, 각주로 구분 명시**.
- git 리포 여부 미확인 → audit 페어는 result+audit 문건으로 운용(commit 페어는 git 확인 후).

## Next
R.1 (Steps 6–14): §notation θ_j 도입 → §stage 정합 → §eqpeak eq:mu/eqcond/solve 정직화(C1) + dUdT 라벨(C2). 절별 5-게이트 + 편집 후 Codex 병행 검토.
