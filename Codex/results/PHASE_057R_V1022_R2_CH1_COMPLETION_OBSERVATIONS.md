# Phase 057R — v1.0.22 R2 Ch1 completion 관찰

정본일: 2026-07-28
세부 Step: 19.6C
범위: 12 unique documents, 811 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 R2 계획·경쟁 초안·마스터 채택 기록을 첫 행부터 끝 행까지
검독했다.

- `PLAN_R2_ch1_completion.md`
- `comp_R2/BRIEF_A.md`
- `comp_R2/BRIEF_B.md`
- `comp_R2/BRIEF_C.md`
- `comp_R2/C_statmech/REMOVAL_CHECK.md`
- `comp_R2/CHERRYPICK_R2.md`
- `comp_R2/B_bridges/BRIDGE_DRAFTS.md`
- `comp_R2/B_bridges/BRIDGE_TARGETS.md`
- `comp_R2/B_bridges/BRIDGE_RISK.md`
- `comp_R2/A_seams/SEAM_PLAN.md`
- `comp_R2/A_seams/MISC_8ITEMS.md`
- `comp_R2/A_seams/W_RULE.md`

최초 4문건 묶음 출력에서 중간 truncation을 확인한 뒤,
영향받은 `SEAM_PLAN.md`, `MISC_8ITEMS.md`, `W_RULE.md`를 더 작은
구간 또는 개별 출력으로 다시 읽었다.

## Provisional Findings

### INTENT-PROV-0111 — 사용자는 문헌 결론이 아니라 유도 다리를 원했다

`BRIEF_B.md`는 사용자 지시를 다음 작업으로 번역했다.

1. 우리 식과 논문 식의 변수 대응 또는 중간 등치식.
2. 논문이 그 식을 얻은 방법 요지.
3. 논문 전제와 현재 문건 전제의 차이.

판정:

- “교과서처럼 따라갈 수 있고 리뷰 논문처럼 원전과 연결되는 문건”이라는
  현재 사용자 방향의 명시적 선행 기록으로 `PRESERVE`.
- 최종 원고에서 인용은 이름표가 아니라
  `문제→전제→유도→식→적용범위→검증` 사슬을 가져야 한다.
- 단, 아래 원문 검증 미완료 상태는 그대로 승계하지 않는다.

### INTENT-PROV-0112 — R2 문헌 다리는 채택됐지만 원문 검증은 크게 미완료였다

R2는 흑연/열특성 load-bearing 다리 8개를 선별했고 마스터가 전부
채택 또는 축소·병합 채택했다. 그러나 검증 수준은 다음과 달랐다.

- Bazant 2013: 원문 식 번호까지 대조 완료.
- Dreyer 2010/2011, McKinnon 1983, Bernardi 1985:
  방법은 확인했으나 정확 닫힌식 또는 식 번호는 `확인 필요`.
- Weppner–Huggins 1977:
  OCV 측정 대응만 사용하고 확산식은 미확인.
- Baek–Pilon 2022, Allart 2018, Reynier 2003:
  식을 재현하지 않고 제목·주제 또는 정성 경향 수준으로 연결.

판정:

- 당시의 정직한 `확인 필요` 표시는 `PRESERVE`.
- 마스터 채택·빌드 PASS를 원문 물리 검증 완료로 읽는 것은 `REJECT`.
- 최종 문헌 조사에서는 각 load-bearing 식을 primary source에서
  직접 확인하고, 정확 식·조건·단위·좌표·실험법까지 source ledger에
  묶어야 한다.

### INTENT-PROV-0113 — R2의 대부분은 모델 확장이 아니라 구조·교육 편집이었다

R2 작업량의 큰 부분은 다음이었다.

- T1/T2/T3 장·파트 참조 78곳 전환.
- “본 문건/이 문건” 29곳의 장/파트/본서 scope 정리.
- 중복 부록 A/B를 C/D로 재번호하고 label을 부여.
- 장 서론·마감·divider와 인용 다리 위치 조정.
- 원전 다리의 중복·기호 충돌·자산 인접 위험 완화.

CLT와 CNT 블록도 새 피팅 파라미터 0, 기존 식/label 변경 0,
통삭제 가능이라는 조건으로 추가됐다.

판정:

- R2를 “Ch1 물리모델 완결”보다
  “재편 뒤 구조·교육적 연결 마감”으로 분류한다.
- 빌드 80/23/5쪽, 자산 357, 구조 PASS는 편집 gate이며
  저온·전류 의존 dQ/dV 설명력의 데이터 gate가 아니다.

### INTENT-PROV-0114 — CLT 설명은 forward 폭 모형의 제한된 근거다

CLT 블록은 독립적인 다수 `η` 원천, 비지배 조건과 Lindeberg 한정에서
종형 분포와 분산 가법을 설명한다. 문건 자체도 다음을 경계한다.

- 단일 지배 원천이면 Gaussian 회수가 보장되지 않음.
- 입자 크기 분포와 동일시하지 않음.
- forward 평균이지 역산 가능한 유일 분해가 아님.
- 자리 점유 요동의 분산과 apparent-voltage 이질성 분산은 다른 양.

판정:

- Gaussian broadening을 사용할 수 있는 한정된 관측 모형 근거로
  `THEORY_ONLY`.
- 모든 온도·전류·재료 broadening의 보편 원인으로 승격하거나,
  총폭만으로 각 원천을 식별하는 것은 `REJECT`.
- 최종 코드는 분포 선택을 고정 진리보다 검증 가능한 관측-model
  family로 다뤄야 한다.

### INTENT-PROV-0115 — CNT 링크는 핵생성 지연을 연결하지만 전류 의존 장벽을 닫지 않는다

CNT 링크는 준안정 가지에서
`exp(-ΔG*/k_BT)` 억제가 지속되는 동안 과주행이 생긴다는
정성 연결을 제공한다. 동시에 다음 한계가 있다.

- 부록이 독립 컴파일이라 live 수식 참조가 아니라 서술형 연결.
- `γ`와 `γ_j`, 부록 `ξ`와 본문 `ξ`의 충돌을 피하려고
  상세식을 본문 링크에서 부르지 않음.
- 새 동역학 식·피팅 파라미터를 도입하지 않음.
- 온도·전류·전위에 따른 실제 유효 장벽 및 핵생성률 폐쇄는 없음.

판정:

- “준안정성→핵생성 장벽→과주행”의 배경 연결로 `PRESERVE`.
- 이를 사용자가 관찰한 저온·정전류 peak 저하/폭 증가를 닫는
  완성 동역학으로 간주하는 것은 `REJECT`.
- 최종 이론은 열역학 구동력, 계면/탄성 에너지, 전기화학 구동,
  전류로 정해지는 경로와 시간창을 분리한 뒤 결합해야 한다.

### INTENT-PROV-0116 — “문건이 권위, 코드가 추종” 원칙은 과거에도 명시됐다

`W_RULE.md`는 `ch2_appB`의 선언을
“본서가 권위이며 코드는 이후 본서에 맞춰 개정된다”로 바꾸도록
명시한다. 또 장 자체로 곡선을 재현할 수 있어야 한다는 선언을
여러 위치에서 유지했다.

판정:

- 물리·화학 문건이 source of truth이고 코드가 그 논리를
  구현한다는 현재 사용자 제약과 일치하므로 `PRESERVE`.
- 그러나 현재의 더 강한 경계에 따라 함수명, 실행법, 코드 회귀값은
  이론 본문이 아니라 지정된 구현 대응 구역으로 제한해야 한다.
- “재현 코드를 짤 수 있다”는 선언은 실제 식-코드 trace와 시험으로
  확인되기 전까지 자기선언일 뿐이다.

### INTENT-PROV-0117 — 경쟁 초안과 채택안의 actor를 분리해야 한다

R2는 Opus 세 창이 초안을 만들고 Fable master가
`CHERRYPICK_R2.md`에서 채택·기각·축소·삽입 위치 변경을 결정했다.
예를 들면 다음과 같다.

- CLT 단락형은 기각, 무라벨 box형 채택.
- Weppner와 Baek–Pilon 다리는 병합.
- Bernardi 다리는 중복 설명을 축소.
- Bazant 다리 위치는 BV 중간이 아니라 TST 유도 뒤로 이동.
- 부록 C/D 재번호와 78개 seam 전환은 마스터가 집행.

판정:

- `BRIEF_*`, seam/bridge 초안의 제안 자체를 정본 결정으로
  인용하지 않는다.
- 후속 원고와 change log에서 실제 집행 여부를 확인한 뒤에만
  `adopted`로 승격한다.

## Coverage Status

- 이 batch의 12문건, 811행은 `READ`.
- 누적 coverage 반영 후 목표는 136문건, 33,506행이다.
- v1.0.22 잔여 목표는 81문건, 14,176행이다.

## Next

Step 19.6D:
R3 Ch2 completion 경쟁 brief·seam·LCO bridge 11문건 595행을
전문 검독해 고전압 LCO 관련 근거의 실제 깊이와 채택 범위를 확인한다.
