# Ch1 v6 — 플로우차트-순서 재조립 (MASTER ROADMAP)

> 본 문서 = 마스터 플랜. 각 Phase 착수 시 상세 플랜, step 마다 result, Phase 끝 commit+push. [[feedback_plan_template_11sections]].

## 1. Summary
사용자 지시(6-22): BD_Display `Lib_LKS_BatteryData_99_Anode_Fit.py`(이 문건 기반 코드)의 **계산 플로우차트 순서대로 v3~v5 문건을 v6 으로 재조립**한다.
- **point 0**: 실험 시작값 U_j·H_j·S_j·H_a,j·S_a,j 는 사내 충당(있다고 가정). 코드 완성도 검토(`BD/Claude/results/ANODE_FIT_code_completeness_review.md` 완료)를 반영한 **시작값→유도 사슬**을 v6 도입에 둔다.
- **point 1**: 플로우차트 순서로 재배열.
- **point 2**: 전혀 상관없는 토픽만 배제.
- **point 3**: 순서를 바꿔도 수식 전개 논리(선행식 의존) 무너지면 안 됨 — V5RR 의존그래프가 가드.
- **point 4**: 재조립이지 요약 아님. 완성도 ≥ 현재(낮추지 않음).

기준 베이스 = **v5**(`graphite_ica_ch1_Opus_v5.tex`, V5RR 검증판·97식·§1.18 배제). v6 = 신규 파일, v5 불가침.

## 2. Current Ground Truth
- 플로우차트(코드 파이프라인, BD 코드 헤더에 코멘트로 추가 완료): 입력 시작값 → [A]V_n(1.45) → [B]작업격자 → [C]C_bg(1.43) → 전이루프{[D]분기중심 U^d(1.91←1.88,spinodal 1.40) → [E]ξ_eq(1.27) → [F]L_V=|dV/dq|·L_q(1.69,T* 1.68) → [G]dξ_j/dV: 저율 ξ_eq(1−ξ_eq)/w(1.50/1.51) 또는 지연 (ξ_eq−ξ_j)/L_V(1.54→1.57/1.58→1.76)} → [H]합산(1.82) → [I]보간. 별도 equilibrium()=|I|→0(1.51).
- V5RR 의존그래프(`V5RR_baseline_map.md §4`) = point 3 가드(97식 선행집합).
- v5 절: §1.1 기호 / §1.2 rate / §1.3 thermo / §1.4 fwdrev / §1.5 regsol / §1.6 charge / §1.7 eqpeak / §1.8 lag / §1.9 potbranch / §1.10 tempbranch / §1.11 synth / §1.12 overlap / §1.13 hys / §1.14 hyspol / §1.15 master / §1.16 falsify / §1.17 code.

## 3. ★ 플로우차트-순서 재배열 설계 (point 1+3 핵심)
코드 파이프라인 순서로 절을 재배치하되 **각 절의 선행식이 모두 앞에 오도록**(의존그래프 검증). 핵심 이동 = **§1.13 히스테리시스(분기중심)를 §1.5 직후·§1.6 앞으로** — 코드가 전이루프 첫 단계에서 branch_center 를 계산하기 때문. 의존 안전: §1.13(식 1.84~1.91)은 isotherm(1.29)·gpp(1.39)·spinodal(1.40) = 전부 §1.5 에만 의존, §1.6/§1.7/lag 불요 → 앞으로 이동 가능.

| v6 Part | 내용(기존 절) | 플로우차트 단계 | 의존 검증 |
|---|---|---|---|
| **A. 시작값** | [신규] U_j·(H_j,S_j)·w_j·Q_j·(H_a,j,S_a,j) 입력 + §1.1 기호표 | 입력 | 정의(선행 없음) |
| **B. 평형 점유 뿌리** | §1.2 rate→§1.3 thermo→§1.4 fwdrev | [E] ξ_eq | 1.1~1.27 자기완결 |
| **C. 상분리·분기중심** | §1.5 regsol→§1.13 hys | [D] U^d | 1.84~1.91←§1.5만 ✓(이동 안전) |
| **D. 관측축·평형 peak** | §1.6 charge→§1.7 eqpeak | [A]V_n·[G]저율 | 1.42~1.52←§1.4 ✓ |
| **E. 동역학 기억길이** | §1.8 lag→§1.9 potbranch→§1.10 tempbranch | [F] L_q/L_V | 1.53~1.74←§1.4/§1.7 ✓ |
| **F. 닫힌식·합산** | §1.11 synth→§1.12 overlap | [G]지연·[H]합산 | 1.75~1.83←D,E ✓ |
| **G. 통합식·관측 gap** | §1.15 master→§1.14 hyspol | [I]·관측 | 1.92~1.97←§1.7/§1.13 ✓ |
| **H. 검증·코드** | §1.16 falsify→§1.17 code | 반증·구현 | 전체 ✓ |

절 번호 체계는 재배열 순서로 1.1~1.17 재부여(라벨 sec:* 보존 → \ref 자동). 식 라벨 eq:* 보존 → \eqref 자동(식 번호는 등장 순서로 재계산되나 라벨 참조라 무손상).

## 4. point 2 — 배제 분석 (보수적)
v5 정독 결과 **"전혀 상관없는 토픽" = 사실상 0**(v5 는 이미 이 dQ/dV 모델에 한정·§1.18 stacking 은 기배제). falsify(§1.16)·Marcus λ 한계·입자분포(KWW)·관측 gap 분해는 전부 *같은 모델*의 검증·유효범위·확장이라 **관련 있음 → 보존**(point 4 완성도). → **배제 0 가정**으로 시작, 재조립 중 진짜 곁가지 발견 시 개별 보고 후 배제(요약 금지).

## 5. Phase Range
| Phase | 이름 | 산출 |
|---|---|---|
| **V6.0** | 본 plan + Part A 시작값 절 설계 | 재배열 맵·시작값 절 초안 |
| **V6.1** | 재조립(절 블록 이동 + Part A 삽입) → v6.tex 빌드 GREEN | v6.tex |
| **V6.2** | 의존·정합 검수(point 3): 재배열 후 모든 식이 선행식 뒤에 오는지 + \eqref/\ref 0 undefined + 절간 다리 재봉합 | 정합 |
| **V6.3** | N회 가변-청크 검수(완성도 ≥ v5 확인·point 4) 수렴 | 검수 |
| **V6.4** | 종합 게이트·RESULT·commit+push | 완료 |

## 6. Non-goals
- v5(및 v3·v4) 수정·덮어쓰기 X(v6 신규). §1.18 X. 새 물리 X(시작값 도입은 *기존 식의 입력 명시*이지 새 유도 아님). 요약·완성도 저하 X(point 4). BD 코드 추가변경 X(Task A 완료).

## 7. Implementation
- 신규 `Claude/docs/graphite_ica_ch1_Opus_v6.tex`(+pdf). 신규 `PHASE_V6_*`. 게이트 = build_gate Opus_v6 0/0/0·comment_gate(코드 절 식번호 재계산 반영 — 재배열로 번호 바뀌면 comment_gate 템플릿/코드 주석 동기 필요·점검)·undefined 0.
- Anode_Fit 버전 산출물 = 자동 commit+push([[feedback_anode_fit_auto_commit_push]]). Codex/ 동반.

## 8. Test Plan
빌드 2-pass undefined 0 · ★의존 검증(재배열 후 식 N 의 선행집합이 전부 앞 — 의존그래프 대조) · 완성도 대조(v5 의 97식·표·figure·코드 v6 에 전부 존재, 누락 0) · 시각 렌더.

## 9. Assumptions
- A1 베이스=v5(검증판). A2 플로우차트=BD 코드 파이프라인(헤더 코멘트). A3 배제≈0(보수적, point 4 우선). A4 §1.17 코드 절은 BD 실코드가 아닌 문건 내 예시 코드(v5 verbatim) 유지 — 단 ★재배열로 식 번호가 바뀌면 그 절 주석 (1.x) 와 comment_gate 동기 필요. A5 "진행해줘"=GO 무중단.

## 10. Decisions
- D1 §1.13 이동(분기중심 앞으로) — 기본값: 이동(코드 순서+의존 안전). D2 배제 — 기본값: 0(보수적). D3 식 번호 재계산 — 기본값: 등장순 재부여(라벨 참조라 안전), 코드 절 주석·comment_gate 동기. D4 Part A 시작값 절 — 기본값: §1.1 기호표를 흡수·확장(시작값→유도 표), 새 물리 아님.

## 11. Correction History
- (최초) v6 트랙은 V5RR(d3ee0c5 수렴) 위에서 연다. v5 불가침 베이스. 플로우차트는 BD 코드(Task A 코멘트)에서 확정.
