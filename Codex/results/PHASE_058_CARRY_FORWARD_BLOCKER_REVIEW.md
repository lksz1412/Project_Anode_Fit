# Phase 058 후속 승계 자산·blocker 분리

정본일: 2026-07-28
대상: Phase 058 Step 32.3
기계 register:
`Codex/results/PHASE_058_CARRY_FORWARD_BLOCKER_REGISTER.json`
검산기:
`Codex/work/v1010_v1013_phase058/validate_phase058_carry_forward.py`

## 결론

v1.0.10–v1.0.13의 결과를 후속 계보 감사에 다음처럼 넘긴다.

| 분류 | 수 |
|---|---:|
| carry-forward asset | 11 |
| repair blocker | 13 |
| new-scope blocker | 5 |
| evidence debt | 5 |
| 합계 | 34 |

4축 matrix 26 rows도 각각 이 register의 한 항목에 빠짐없이
연결했다. 29/29 checks가 통과했다.

## 1. Carry-forward asset

다음은 버리지 않고 이후 version에서 보존 여부를 계속 확인한다.

1. 이상 통계역학과 logistic kernel
2. homogeneous regular-solution 자유에너지 대수
3. 전하 보존·peak 면적·용량 계약
4. 전극 반응 방향과 cell label 분리
5. causal relaxation의 reduced-model 출발점
6. entropy coefficient와 reversible heat identity
7. Sommerfeld endpoint와 unit bridge
8. verify-first regression·provenance 원칙
9. 문헌 anchor와 placeholder tiering
10. v1.0.13 scalar span guard
11. claim-disposition·4축 감사 infrastructure

이 중 causal relaxation은 `THEORY_ONLY` 상태로 승계한다. 자산
승계는 현재 구현 또는 외부 데이터 승인을 뜻하지 않는다.

## 2. Repair blocker

정본·생산 코드 전에 반드시 닫아야 하는 13개다.

- C-rate hour–second unit
- convexified nonideal equilibrium
- common-host multi-transition topology
- width와 entropy semantics
- local-state kinetic barrier와 active defaults
- 연속 \(I\to0\) limit
- 연속 numerical handoff
- persistent hysteresis state
- LCO electronic entropy와 transition defaults
- observation·differentiation model
- portable branch-complete failure gates
- artifact layout·provenance
- theory–code separation

각 blocker에는 acceptance criterion을 저장했다. 후속 version이
“해결”을 주장하면 그 criterion을 실제 source, code, test, data에
대조한다.

## 3. New-scope blocker

v1.0.10–13에는 없어서 기존식을 조금 고쳐 닫을 수 없는 영역이다.

- 공개 experimental dataset과 fit pipeline
- silicon 및 graphite–silicon composite
- doped high-voltage LCO chemistry/degradation
- uncertainty·holdout·mechanism ablation
- systematic primary-literature review

이 항목은 Phase 059–066의 후속 계보가 이미 무엇을 추가했는지
확인한 뒤 Phase 069에서 최종 실행 계획으로 확정한다.

## 4. Evidence debt

- 공개 data fit 없음
- LCO default/phase assignment 외부 검증 없음
- bibliography search protocol과 전건 원문 판정 없음
- partial clone 때문에 일부 역사 artifact blob body 부재
- bit-exact 주장의 environment 의존

Evidence debt는 식을 틀렸다고 단정하는 목록이 아니다. 해당 주장을
정본 권위로 승격할 증거가 아직 없다는 목록이다.

## 5. 운영 규칙

Phase 059–066은 repair/evidence 항목이 후속 version에서 실제로
해결됐는지 판정한다. “새 절이 생김”, “test가 실행됨”, “그림이
있음”을 해결로 세지 않는다.

Phase 067은 code·test 전 계보에서 unit, limit, branch, portability를
닫는다. Phase 068은 Claude/Codex fork가 이 blocker를 해결했는지
재판정한다. Phase 069는 전체 계보를 읽은 뒤에만 새 정본·코드
작업 순서를 확정한다.

v1.0.26은 권위나 해결 증거로 사용하지 않는다.
