# Phase 057J — v1.0.21 통제 문건 의도 관찰

정본일: 2026-07-28
세부 Step: 19.5A
범위: 4 unique documents, 117 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 네 문건을 첫 행부터 끝 행까지 검독했다.

- `V1021_CHANGE_LOG.md`
- `V1021_EXECUTION_LEDGER.md`
- `V1021_REFERENCE_LEDGER.md`
- `HANDOVER_v1.0.21.md`

이 결과는 당시 기록이 말하는 결정과 자기평가를 복원한다.
해당 자기평가를 곧바로 물리 검증 완료로 승인하지 않는다.

## Provisional Findings

### INTENT-PROV-0066 — v1.0.21은 확장판으로 기획됐다

변경 대장과 실행 원장이 공통으로 기록한 확장축은 다음과 같다.

1. 다클래스 대정준 전하 보존과 요동–응답.
2. TST 배경 유도.
3. A급 그림 5건.
4. 항법판과 기호·의존성 지도.
5. 끝-대-끝 계산 예제와 측정 원리 배경.
6. LCO 한 점 시연.
7. Si 예비 지도와 향후 독립 장의 교두보.

근거:

- change log lines 10–37.
- execution ledger lines 9–18.
- handover lines 7–11.

판정:

- v1.0.20이 품질 보강판이었다면 v1.0.21은 명시적인
  범위 확장판이라는 계보를 `PRESERVE`.
- 다만 “추가됨”과 “실험적으로 검증됨”은 분리한다.

### INTENT-PROV-0067 — 당시 편집 방향과 후속 철회가 함께 기록돼 있다

실행 원장 lines 4–5는 당시 확정 결정으로
항법 적용/미적용 이원 빌드, 일반 보강 top3, Si 독립 Ch3,
그림 보수, 요동–응답 포함, 단독 저작을 적었다.

그러나 handover lines 13–18은 후속 결정으로
B급 그림 반영 취소와 항법판 폐기를 명시한다.

판정:

- 항법판은 v1.0.21 당시에는 의도적으로 구현됐지만
  후속 정본 방향은 제거다.
- “한 번 구현됨”을 영구 보존 결정으로 해석하지 않는다.
- Si를 흑연 식의 단순 파라미터 교체로 흡수하지 않고
  독립 Ch3로 다루려는 방향은 계속 `PRESERVE`.

### INTENT-PROV-0068 — `code matched`는 제한된 자기판정이다

execution ledger line 18은 Q2–Q7 추가분이 신규 계산 거동을
요구하지 않는다고 판단해 변경 함수 0, 게이트 통과를 근거로
`code matched`라 적었다.

동시에 다음 기록도 존재한다.

- Q2 식은 기존 `eq:implicit` 기구현에 기대었다.
- Q6 LCO 시연 수치는 당시 Python 실행으로 재현됐다고 적었다.
- change log line 32는 문건의 한 점 수치를 코드 실행과 직접 연결한다.

판정:

- 이는 “신규 함수가 필요 없었다”는 변경관리 판단으로만 보존한다.
- 문건의 모든 식·부호·단위·제약·적용범위가 코드에 100% 반영됐다는
  증거로는 `UNVERIFIED`.
- Phase 067에서 식별자 수준이 아니라 실제 계산 경로와 테스트를
  다시 대조해야 한다.

### INTENT-PROV-0069 — 현재 사용자의 문건 순수성 규칙과 재대조가 필요하다

당시 v1.0.21은 다음을 문건 자산으로 허용했다.

- 코드맵 부록.
- “코드 실행 재현”을 내세운 LCO 본문 시연.
- doc-leads와 함수명에 기대는 Ch2 연결 설명.

현재 사용자가 재확인한 정본 방향은
이론 문건에는 물리·화학 논리만 두고,
코드는 지정된 제한 구역 외 본문에서 언급하지 않으며,
코드가 문건을 100% 따라야 한다는 것이다.

판정:

- v1.0.21의 계산 예제 자체는 물리적 교육 자산으로 재검토할 수 있다.
- 코드 실행·함수명·구현 대응을 그 예제의 권위 근거로 삼는 표현은
  허용 구역으로 이동하거나 제거할 후보 `CORRECT`.
- 최종 이론 본문은 코드가 없어도 독립적으로 유도·검산 가능해야 한다.

### INTENT-PROV-0070 — 참조 원장은 유용하지만 검증 권위는 재확인이 필요하다

reference ledger는 원장에 등재된 V1 키만 인용하고,
기억 기반 인용을 금지하는 좋은 통제를 기록한다(lines 3–4).
반면 신규·승계 근거에는 WebSearch, WebFetch, Crossref,
출판사 페이지 대조가 혼재하며 다음 조건부 항목도 남겼다.

- `safran1987` 권 번호 재확인.
- `sethuraman_stresspot2010` 쪽 범위 확인.
- `koebbing2024` 인쇄 권·호 확인.
- Si 부분몰 엔트로피 실측 미확보.

판정:

- 인용 전 원장 등재와 load-bearing 주장에 1차 문헌을 병기하는 규칙은
  `PRESERVE`.
- 과거의 “웹 검증” 표시는 이번 끝판 문건의 문헌 검증 완료로
  자동 승계하지 않는다.
- 핵심 식·물성·실험 현상은 원 논문·공식 데이터·정본 서지로
  다시 확인한다.

### INTENT-PROV-0071 — Si의 핵심 공백을 스스로 인정했다

change log line 35와 reference ledger lines 28–37,
handover lines 20–21은 다음을 분명히 한다.

- 전하 보존 골격은 Si에도 앵커로 쓸 수 있다.
- 기계적 히스테리시스는 아직 공백이다.
- Larché–Cahn형 응력–화학퍼텐셜 연결은 후보 이론틀이다.
- Si 부분몰 엔트로피 실측은 확보되지 않았다.
- Si/SiO_x/Si–C와 blend fraction은 후속 작업이다.

판정:

- v1.0.21 Si 부록은 완성 이론이 아니라 bridgehead다.
- 흑연 성분을 Si 상전이로 재명명하는 방식은 이 기록과도 맞지 않는다.
- 독립 재료 물리, chemo-mechanics, 계면·복합체 분배를 포함하는
  별도 계보가 필요하다.

### INTENT-PROV-0072 — 빌드·구조 PASS는 과학·데이터 PASS가 아니다

execution ledger의 gate는 주로 다음을 확인했다.

- PDF 빌드 오류와 undefined reference.
- label/eqblock/bibliography/asset 구조 diff.
- 기존 G1/G2/G3/n(T) 테스트.
- 일부 손계산·좌표 교차 일치.

판정:

- 문건 제작 품질과 변경 통제로서는 유효하다.
- 저온·유한전류 dQ/dV peak lowering/broadening,
  전위 의존 활성화 장벽, LCO/흑연/Si 공개 데이터 설명력을
  검증한 증거는 아니다.
- 실험 데이터 적합성과 식별 가능성은 후속 별도 gate로 둔다.

### INTENT-PROV-0073 — v1.0.21의 자체 검수는 명시적으로 축약됐다

handover lines 10–11은 신설분 7항목만 spot-check했고,
물리 적대 검산과 register 전수 검수를 v1.0.22 R8로 이월했다고
스스로 한정한다.

판정:

- `PASS_V1021_CLOSED`는 제작 phase 종료를 뜻한다.
- 심층 물리 검토 완료라는 해석은 `REJECT`.
- 이번 재감사에서 v1.0.22의 실제 R8 수행과 후속 수정 여부를
  독립 확인한다.

### INTENT-PROV-0074 — LCO 시연은 tier-C와 동결 근사를 벗어나지 못했다

change log line 32와 execution ledger line 16은
LCO 한 점 시연에 슬롯 산술, 반전식, 게이트 on/off를 사용하고,
tier-C 시연과 `T_ref` 동결 근사를 명시한다.
L2/L3/L4/L5는 실측·온도 복원·비가역열·원전 확인 대기로 이월됐다.

판정:

- 시연은 부호·산술 sanity check로만 `PRESERVE`.
- 고전압 도핑 LCO의 조성·온도·율속별 데이터 설명 모델로
  승격하는 것은 `REJECT`.
- 이번 끝판에서는 도핑·산소 redox/구조 안정성·전해질 경계와
  실제 데이터에 대한 별도 근거가 필요하다.

## Coverage Status

- 이 batch의 4 unique 문건, 117행은 `READ`.
- 누적 coverage 반영은 batch JSON 적용 후 107문건, 18,616행이다.
- v1.0.21 snapshot 9문건, 12,211행은 아직 `UNREAD`.

## Next

Step 19.5B:
`snapshot_v1021_q0.json` 1,299행을 연속 구간으로 전문 검독해
v1.0.20 final과 구조 기준선이 실제로 같은지 확인한다.
