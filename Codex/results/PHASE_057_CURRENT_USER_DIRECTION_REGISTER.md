# Phase 057 현재 사용자 방향 등록부

정본일: 2026-07-28  
상태: `DIRECT_CURRENT_USER_DIRECTION`  
적용 범위: v1.0.10–v1.0.25.2 재감사 및 이후 endgame 작업

## 증거 등급

- `DIRECT_CURRENT`: 이번 대화에서 사용자가 직접 지시·재확인한 사항.
- `REPOSITORY_CORROBORATED`: 과거 저장소 이력에도 같은 방향이 반복됨.
- `HISTORICAL_SCOPE_ONLY`: 특정 과거 버전의 국소 작업 범위였으며
  endgame의 영구 제약은 아님.

이 문서는 대화의 축어 transcript가 아니라 현재 지시의 보수적 요약이다.
과거 모델 문건의 “사용자 발언” 표기와 혼합하지 않는다.

## 현재 변경 불가 방향

| ID | 현재 사용자 방향 | 등급 | 과거 계보 연결 |
|---|---|---|---|
| UDIR-01 | 새 물리·코드 작업 전에 v1.0.10부터 v1.0.25.2까지 전체 이력과 작성 의도를 다시 제대로 감사한다. | `DIRECT_CURRENT` | Phase 055–057 전체 |
| UDIR-02 | v1.0.25.2가 최신 과학 기준선이며 v1.0.26은 미완성·비권위 상태로 제외한다. | `DIRECT_CURRENT` | INTENT-PROV-0376, 0378 |
| UDIR-03 | 원본, main, 기존 이론·코드를 건드리지 않고 전용 branch에서만 작업한다. | `DIRECT_CURRENT` | INTENT-PROV-0354 |
| UDIR-04 | 중간 산출물은 자주 commit하고 원격에 push해 작업 이력을 보존한다. | `DIRECT_CURRENT` | INTENT-PROV-0181, 0354 |
| UDIR-05 | 최종 이론 문건에는 코드 설명을 배제하고 물리·화학 논리만 둔다. 코드 정보는 지정 companion에만 둔다. | `DIRECT_CURRENT`, `REPOSITORY_CORROBORATED` | INTENT-PROV-0030, 0139, 0203, 0244, 0380, 0394 |
| UDIR-06 | 코드는 이론 문건에서 채택한 물리·화학 논리를 100% 반영해야 하며, 코드를 기준으로 이론을 사후 수정하지 않는다. | `DIRECT_CURRENT`, `REPOSITORY_CORROBORATED` | INTENT-PROV-0006, 0014, 0277, 0314, 0346 |
| UDIR-07 | 문건은 이공계 대학원 교재처럼 친절하고 상세하며, 수식 사이 유도 다리를 생략하지 않는다. | `DIRECT_CURRENT`, `REPOSITORY_CORROBORATED` | INTENT-PROV-0026, 0111 |
| UDIR-08 | 문건은 review 논문에 준하는 깊이와 강한 1차 문헌 조사를 가져야 한다. | `DIRECT_CURRENT`, `REPOSITORY_CORROBORATED` | INTENT-PROV-0047, 0111 |
| UDIR-09 | 실제 공개 LIB 데이터로 doped high-voltage LCO, graphite, Si, graphite+Si를 설명하고 피팅할 수 있어야 한다. | `DIRECT_CURRENT`, `REPOSITORY_CORROBORATED` | INTENT-PROV-0257, 0347, 0403 |
| UDIR-10 | 핵심 관찰은 저온일수록, 무전류보다 정전류일 때 dQ/dV peak가 낮아지고 broadening된다는 것이다. 모델은 이를 재현·설명해야 한다. | `DIRECT_CURRENT` | INTENT-PROV-0219, 0351 |
| UDIR-11 | 상전이 활성화 장벽과 peak 응답은 온도, 전류, 전극 전위의 영향을 물리·전기화학적으로 받아야 한다. 전류를 근거 없는 독립 경험변수로 넣지 않는다. | `DIRECT_CURRENT` | INTENT-PROV-0174, 0253, 0351 |
| UDIR-12 | 임의 cap, clip, clamp, softplus, 근거 없는 threshold·grid guard·사후 smoothing을 물리로 위장하지 않는다. | `DIRECT_CURRENT`, `REPOSITORY_CORROBORATED` | INTENT-PROV-0286 |
| UDIR-13 | 실제 fit 성공을 존중하되 curve basis, phase, gallery, 재료 성분과 물리 상수의 식별을 혼동하지 않는다. | `DIRECT_CURRENT` | INTENT-PROV-0050, 0347, 0401–0403 |
| UDIR-14 | 마스터 phase 목차, phase별 세부 step 계획, step별 이력과 active handover로 auto-compaction 후에도 복구 가능하게 작업한다. | `DIRECT_CURRENT`, `REPOSITORY_CORROBORATED` | INTENT-PROV-0181 |
| UDIR-15 | v1.0.21–v1.0.23의 Fable 작업보다 더 나은 이론 문건과 그 이론을 따르는 코드의 완결을 목표로 한다. 모델 명성보다 실제 산출물과 검증으로 비교한다. | `DIRECT_CURRENT` | INTENT-PROV-0175, 0352 |
| UDIR-16 | 데이터에서 실제로 작동하는 피팅 능력을 잃지 않는다. 경험적 성공분은 물리적 지위를 낮춰 보존하거나 새 물리 계층에 연결한다. | `DIRECT_CURRENT` | INTENT-PROV-0047, 0347 |
| UDIR-17 | 원본 파일명 유지 같은 과거 국소 결정은 그 버전의 역사로 보존하되 새 endgame 구조의 과학 설계를 묶는 절대 제약으로 자동 승계하지 않는다. | `DIRECT_CURRENT` 해석 경계 | INTENT-PROV-0325, 0326 |

## 과거 국소 결정과 현재 endgame 방향의 구분

- v1.0.25의 “전문 재작성 아님, 국소 패치”는 그 당시 사용자 범위다
  (INTENT-PROV-0345). 이번 endgame은 사용자가 새로 전 범위 재감사와
  완결 작업을 요청했으므로 그 국소 범위에 묶이지 않는다.
- v1.0.25에서 regsol 구현 삭제를 승인한 이력은 보존한다
  (INTENT-PROV-0348). 그러나 최종 이론에서 regular-solution 자유에너지를
  검토하거나 더 엄밀한 상전이 모델을 채택하는 것까지 금지한 결정은 아니다.
- “theory=regsol, fitting=logistic”의 과거 승인 이력은 존재하지만
  (INTENT-PROV-0379), 현재의 100% 이론–코드 단일 논리 요구를 충족하지
  못하므로 최종 architecture로 자동 승계하지 않는다.

## 해결 전 사용자 우려

1. v1.0.23 이후뿐 아니라 v1.0.10 이후 작업 전체의 신뢰성.
2. 실제 데이터에서 작동하는 조건과 문건의 물리·코드가 정말 일치하는지.
3. 저온·유한전류 peak lowering/broadening의 메커니즘 분해.
4. 전위·온도·전류에 따른 상전이 장벽의 물리적 유도와 식별.
5. doped high-voltage LCO를 포함한 실제 공개 데이터 검증.
6. graphite/Si/blend의 phase·gallery·curve basis 혼동 제거.
7. 과거 PASS와 GREEN이 보지 못한 default·외부 타당성의 재검증.
8. 최종 이론 문건에서 code token과 작업사 흔적의 완전 분리.

이 항목들은 Phase 069의 새 작업 착수 gate까지 `OPEN_USER_CONCERN`으로
유지한다.
