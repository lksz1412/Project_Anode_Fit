# Phase 057BF 발화 주체·승인 상태 분리 결과

정본일: 2026-07-28  
대상 단계: Phase 057 Steps 21.1–21.5  
기준 커밋: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

## 판정

`PASS_P057_ACTOR_SEPARATION`

50개 관찰 문건의 provisional finding 404개를 연속 ID
`INTENT-PROV-0001`–`0404`로 추출했다. 모든 record 자체의 작성 주체는
이번 Codex 재감사의 `REVIEW_FINDING`이다. 각 record가 주로 논의하는
대상 주체를 별도 `referenced_actor`로 분리했다.

## 두 층의 actor 모델

| 층 | 의미 |
|---|---|
| `record_actor` | 이 문장을 누가 작성·판정했는가 |
| `referenced_actor` | 이 문장이 주로 누구의 요구·제안·검토·구현을 다루는가 |

이 구분이 없으면 Codex가 “과거 문건은 사용자가 이렇게 원했다고 기록했다”고
판정한 문장이 곧바로 사용자의 직접 발언으로 둔갑한다.

| referenced actor | provisional finding 수 |
|---|---:|
| `USER_REQUIREMENT` | 43 |
| `MODEL_PROPOSAL` | 24 |
| `IMPLEMENTED_STATE` | 45 |
| `REVIEW_FINDING` | 292 |
| 합계 | 404 |

43개의 `USER_REQUIREMENT` 참조도 우선 `REPOSITORY_REPORTED`다.
이번 대화에서 직접 재확인된 항목만
`PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md`에서
`DIRECT_CURRENT`로 승격했다.

## 사용자 요구의 현재 승인 상태

현재 직접 재확인된 17개 방향을 별도 등록했다. 핵심은 다음과 같다.

1. v1.0.10–v1.0.25.2 전 범위 재감사 선행
2. v1.0.25.2 최신, v1.0.26 제외
3. 원본·main 불가침, branch-only, 잦은 commit/push
4. theory는 물리·화학만, 구현 정보는 companion
5. code는 theory의 계산 가능한 논리를 100% 반영
6. 대학원 교재의 친절함과 review 논문의 깊이
7. doped high-voltage LCO·graphite·Si·blend 공개 데이터
8. 저온·유한전류 peak lowering/broadening과 T–I–U barrier
9. 임의 cap/clip/softplus/threshold 금지
10. fit 성공과 phase/material identification 분리
11. phase/step/ledger/handover 기반 compaction 복구

## 사용자 승인 없이 구현 상태로 흘러간 후보

다음 항목은 사용자 승인 근거를 발견하지 못했거나, 승인 범위보다 구현의
과학적 지위가 커진 사례다. “사용자가 반대했다”는 뜻이 아니라
`NO_DIRECT_USER_APPROVAL_FOUND`다.

- skew-logistic의 α를 empirical observation shape가 아니라
  equilibrium susceptibility·entropy·reversible heat 경로까지 공유한 것
- 7-gallery skew를 default로 뒤집은 것
- legacy 회귀를 위해 gate가 default를 먼저 바꾼 것
- 1C 예제에서 equilibrium과 거의 겹치는 응답을 유한전류 물리의 완료로
  보고한 것
- fixed grid, pad cap, clamp, hard threshold를 물리 closure와 한 문맥에 둔 것
- regular-solution equilibrium code 삭제 뒤 Ω를 다른 역할에 남긴 채
  “이론–코드 완결”로 부른 것
- in-sample BIC·R² 우세를 phase mechanism의 권위로 확장한 것

이 항목은 Phase 058–067에서 실제 source와 behavior를 다시 검증한 뒤
`PRESERVE`, `EMPIRICAL_ONLY`, `CORRECT`, `REJECT`를 부여한다.

## 해결되지 않은 사용자 우려

다음은 `OPEN_USER_CONCERN`이다.

- 과거 전 버전의 물리 신뢰성과 문건–코드 실제 일치
- 실제 fit을 유지하면서 물리적 지위를 정직하게 재구성하는 방법
- 저온·유한전류에서 peak 높이·폭·위치 변화의 원인 분해
- 전극 전위·온도·전류가 장벽과 상전이율에 들어가는 유도
- doped high-voltage LCO와 다온도·다전류 공개 데이터의 외부 검증
- graphite/Si/blend의 phase, gallery, basis component 구분
- theory-only 문건에서 code token·내부 작업사 완전 제거

## 사용자 정정 뒤 남은 stale 상태

1. v1.0.25.2 안의 “v1.0.25.1 현행 최신” 제목
2. theory lineage의 함수명·key·gate·bit-exact·code map
3. 7-gallery default 마감 선언 뒤 legacy4로 복구된 이력
4. 최종 source 변경 전의 30/30·GREEN 자기보고
5. “코드 반영 완결”, “문건 코드 이야기 배제 완료” 선언
6. 패배한 Ω fit을 graphite phase 판정으로 이전한 문장
7. 서로 다른 specimen/protocol을 통제 비교처럼 서술한 report

## 기계 산출물

- extractor:
  `Codex/work/v1010_v1025_2_reaudit/extract_phase057_provisional_findings.py`
- ledger:
  `Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json`
- source observation documents: 50
- findings: 404
- 연속 ID: 0001–0404, gap 0, duplicate 0
- deterministic SHA-256:
  `e55b20c6c207e905c63db3cc8fe2ba3c6b83a31a48256d21d2d404af20299877`

각 finding은 source path, physical line range, 원문 block SHA-256,
actor basis와 전문 body를 보존한다.

## 다음 단계

Phase 057 Step 22에서 43개 repository-reported user topic과
17개 direct-current 방향을 변수·부호·좌표·장 구조·문체·코드 경계·피팅
목표의 결정 계보로 통합한다. 과거 특정 patch의 사용자 승인과 현재 endgame의
영구 원칙을 분리한다.
