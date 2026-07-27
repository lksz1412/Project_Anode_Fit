# Phase 057F — v1.0.20 P2–P6 사용자 의도 관찰

정본일: 2026-07-28
세부 Step: 19.4B
범위: 21 unique documents, 815 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 묶음을 첫 행부터 끝 행까지 검독했다.

- P2 Part 0: plan, author brief, result, step log, pick judgment 5본 185행.
- P3 graphite: plan, result, step log 3본 116행.
- P4 LCO: plan, author brief, result, step log, pick judgment 5본 183행.
- P5 Ch2: plan, result, step log 3본 109행.
- P6 convention: plan, result, step log 3본 119행.
- P7 review의 plan과 step log 2본 103행.

P2+P3 최초 일괄 출력에서 `STEP_LOG_P2.md` 중간이 truncation되어
1–34행을 별도로 다시 읽었다. 나머지는 논리 묶음별 출력으로 전문을 확인했다.

## Provisional Findings

### INTENT-PROV-0034 — 계획보다 전문 정독과 물리 판정이 우선

P3 plan은 §9의 기억 꼬리에 KWW 계보를 추가하려 했다.
그러나 `STEP_LOG_P3.md:6-10`과 `RESULT_P3_graphite.md:3-7`은
전문 정독 결과 현행 모델이 stretched exponential이 아니라
1계 선형 완화의 단일 지수 커널임을 확인하고 그 계획을 기각했다.

P4도 처음에는 LCO 수식사슬 대보강을 계획했지만,
`STEP_LOG_P4.md:6-12`는 §15의 Sommerfeld 유도가 이미 닫혀 있고
실제 공백은 MIT의 배경 다리라고 범위를 정정했다.

판정: 작업 원칙 `PRESERVE`.
계획서는 실행 순서를 고정하지만, 읽기 전 세운 물리 가설을 권위화하지 않는다.
전문 정독과 재유도가 계획을 뒤집을 수 있어야 한다.

### INTENT-PROV-0035 — LCO는 미시 기작과 현상학 게이트를 구분

P4 author brief `:9-30`은 다음 구분을 하드 가드로 둔다.

- 완전 리튬화 LiCoO2의 저스핀 \(t_{2g}^6\) 상태는 band insulator.
- 탈리튬화 뒤 상관 물리는 host 전체를 단순 Mott insulator로 부르는 것이 아니라
  Li vacancy에 결합한 impurity level의 Mott transition 가설로 설명.
- 문헌 기작은 “유일하게 확정된 기작”으로 과장하지 않음.
- 계산 모델은 미시 기작 전체를 \(g(E_F,x)\) 게이트로 현상학화하므로
  “왜”와 “어떻게 계산하는가”를 분리.

P4 result `:3-36`은 이 배경을 추가했지만,
기존 수식과 LCO tier-2/3, 다온도 복원은 범위 밖으로 유지했다.

판정:

- band/Mott/impurity-Mott의 분류와 미시기작↔현상학 폐쇄 분리는 `PRESERVE`.
- \(g(E_F,x)\) logistic gate의 정량 타당성과 도핑 고전압 LCO 일반화는
  `UNVERIFIED`.

### INTENT-PROV-0036 — 자립 교재는 과거 작업사를 지워야 함

P6 result `:39-41`은 제목의 “재작성” 꼬리를 D1 위반 후보로 남겼다.
P7 step log `:63-66`은 사용자 결정으로 이를 포함한 여섯 곳의
과거 버전·초안·계보 표지를 제거했다고 기록한다.

이는 검증 이력의 삭제가 아니다.
작업 이력은 plan/result/ledger에 남기고,
독자 대면 이론 본문은 현재 물리만으로 자립하게 한다.

판정: `USER_REQUIREMENT`, `PRESERVE`.

### INTENT-PROV-0037 — 확장판과 품질 정정판의 계보 분리

P7 step log `:63-66`은 사용자의 다섯 결정을 기록한다.

1. 확장 전건은 v1.0.21로 분리해 원본을 보존.
2. 배경 box는 본문 유지.
3. 문서 이력 표지를 제거.
4. 통계역학 확장 두 건을 v1.0.21에서 진행.
5. LCO 확장과 Si 이론 접목을 v1.0.21에서 기획.

v1.0.20에는 자립성 정정 B-008과 교과서 표준식의 수식화 B-009만 남겼다.

판정:

- v1.0.20의 역할을 설명·품질 정정판으로 보는 것은 `PRESERVE`.
- Si/LCO/새 동역학의 과학적 계보는 v1.0.21 이후에서 별도 판정.

### INTENT-PROV-0038 — “수식 불변” gate는 적용 물리의 재검증을 회피함

P2–P6의 result들은 반복해서 eqblock diff 0,
라벨·자산 보존과 빌드 성공을 gate로 사용한다.
이는 설명 보강판의 회귀 방지에는 합리적이다.

그러나 P4 result `:35-36`은 LCO의 기존 수식사슬을 완결로 판정하면서도
실측 tier-2/3, 다온도 전자항, 비가역열을 이월한다.
따라서 “문서 내부 수식사슬이 닫힘”과
“공개 실험 데이터를 설명하는 재료 모델이 닫힘”은 다르다.

판정:

- 편집 불변성은 `INTERNAL_CONSISTENCY`.
- 실험 적합성은 `UNVERIFIED`.
- 최종 작업에서는 원형 식 보존 자체를 gate로 삼지 않고,
  문헌·차원·극한·실험 식별성을 통과한 식만 보존한다.

### INTENT-PROV-0039 — 다중 검토는 반론 생성 장치이지 과학 권위가 아님

P2/P4 pick judgment와 P7 plan/step log는 여러 독립 초안을 비교해
기호 충돌, 인용 범위, 문장 다리와 오류 후보를 찾는 데 유용했다.
P7은 단독 지적을 master 재정독·재유도 후에만 채택하도록 했다.

반면 같은 기록에는 API 실패, 부분 산출, 모델 가중치,
“완주 본수”가 품질 proxy로 쓰인 흔적도 있다.
모델 수나 합의 수는 물리 증명의 대체물이 아니다.

판정:

- 독립 반론 수집은 `PRESERVE`.
- 채택 판정은 원전, 재유도, 실제 코드와 데이터 증거에만 기반.
- Fable/Opus/Claude/Codex 이름이나 다수결을 권위로 사용하는 것은 `REJECT`.

## Conflicts to Carry Forward

1. \(\bar{x}\) charge balance와 Ch2의 bare grand-canonical derivation이
   실제 다상 전극에서 유일한 \(U_{\mathrm{oc}}\)를 보장하는지.
2. LiCoO2의 insulating/metallic regime과 도핑 안정화 기작을
   하나의 logistic \(g(E_F,x)\)로 묶는 적용 범위.
3. \(\gamma_j\), \(h_\eta\)가 독립적인 물리량인지,
   관측 장치·수송·입자 ensemble 효과를 흡수한 경험량인지.
4. 단일 지수 기억 커널을 유지할지,
   실제 rate/relaxation 데이터가 barrier distribution 또는
   fractional/KWW 확장을 요구하는지.
5. “Ch2 D7 위반 없음” 판정은 문서 구조 판정이며,
   구성·진동·전자 엔트로피 결합의 재료별 타당성은 별도다.

## Coverage Status

- 이 batch의 21문건은 `READ`.
- 누적 Phase 057 coverage: 59문건, 3,158행.
- v1.0.20 잔여: 44문건, 15,341행.
- 아직 Phase 057 최종 `VERIFIED`가 아니다.

## Next

Step 19.4C:
P7 독립 review, interchapter/code/statmech/general 방향 보고서,
triage와 review result 16문건 2,567행을 전문 검독한다.
