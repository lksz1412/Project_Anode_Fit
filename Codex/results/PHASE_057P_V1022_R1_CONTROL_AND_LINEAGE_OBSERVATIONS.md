# Phase 057P — v1.0.22 R1 통제·계보 관찰

정본일: 2026-07-28
세부 Step: 19.6A
범위: 7 unique documents, 477 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 문건을 첫 행부터 끝 행까지 검독했다.

- `PLAN_R1_reorg.md`
- `V1022_CHANGE_LOG.md`
- `V1022_EXECUTION_LEDGER.md`
- `V1022_REFERENCE_LEDGER.md`
- `PLAN_RA_lineage_audit.md`
- `AUDIT_LINEAGE_v19_v22.md`
- `R1B_SWEEP_LIST.md`

긴 table row도 생략하지 않았으며, 최초 묶음 출력이 truncation된 뒤
해당 문건들을 더 작은 구간으로 다시 읽었다.

## Provisional Findings

### INTENT-PROV-0096 — 사용자는 무인지 축소·왜곡을 명시적으로 금지했다

`PLAN_RA_lineage_audit.md` lines 3–4와
`AUDIT_LINEAGE_v19_v22.md` line 3은 사용자 지시를 다음처럼 기록한다.

- 오류 수정은 인정.
- 로그된 의도 변경도 인정.
- 인지하지 못한 생략·축소·왜곡은 문제.
- 모든 계보 변화는 오류 수정, 의도 변경, 미로그 변화 중 하나로 귀속.

판정:

- 이번 v1.0.10–v1.0.25.2 재감사의 핵심 방향으로 `PRESERVE`.
- 이후 새 이론 작업도 삭제·재배치·수정의 이유와 대체 위치를
  claim/asset 단위로 기록해야 한다.

### INTENT-PROV-0097 — v1.0.22 재편의 본래 목적은 재료별 책임 분리였다

R1 계획은 v1.0.21을 다음 구조로 재조립했다.

1. Ch1: graphite 곡선 + 공통 통계역학 + 열특성.
2. Ch2: LCO 추가 텀.
3. Ch3: Si·혼합 음극.
4. 독립 phase-separation appendix.

섹션 파일은 이력 보존을 위해 유지하고 master input만 재조립했다.
임시 navigation 판은 제거하고 장별 기호표와 bibliography로 기능을
흡수했다.

판정:

- 물질별로 “공통 골격 / 재료 고유 물리 / 적용 한계”를 나누는
  방향은 `PRESERVE`.
- Ch2를 단순히 “Ch1에 추가 텀만”으로 제한하는 구조는
  고전압 도핑 LCO의 독립 구조·전자·산소·계면 물리를 담기에
  충분한지 다시 판정해야 한다.

### INTENT-PROV-0098 — 당시 `미로그 변화 0`은 산문 전수 재독 결론이 아니다

RA 보고는 자산 tag, label, equation hash, 총량 감소를 기계 감사해
미귀속 소멸·변경 0을 보고했다. 이 결과는 구조 보존 증거로 유효하다.

그러나 같은 보고 line 59는 다음을 명시한다.

- 산문 왜곡 전수 재독은 감사 범위 밖.
- 자산·기존 검수·diff 체계의 간접 보증에 의존.
- 일부 tag 미부착 문장층은 v1.0.19 검수 기록에 의존.

판정:

- “label/equation/tag 관점에서 미로그 손실 0”은 `PRESERVE`.
- 보고 서두의 더 넓은 “모든 소멸·변경, 의미 훼손 없음” 문구를
  산문 전체의 직접 검증으로 읽는 것은 `REJECT`.
- 이번 재감사가 고유 문건 전행 검독을 다시 수행하는 이유가 된다.

### INTENT-PROV-0099 — 후속 심층 검토가 이전 PASS 뒤의 실질 결함을 다수 발견했다

v1.0.22 change log는 초기 R1/RA/R2/R3/R5/RV의 PASS 뒤에도
FR과 AUD가 다음과 같은 물리·수학·좌표 오류를 고쳤다고 기록한다.

- `eq:kuniv`의 장벽 항 이중 차감 제거(C-044).
- TST 고전 극한과 reduced partition 설명 정정(C-046).
- 완전식과 `eq:weighted`의 환원 관계 정정(C-041).
- 화학퍼텐셜 기준 상수 분해 설명 정정(C-042).
- Einstein 흡수 상수와 식별 근거 정정(C-045).
- LCO `x`와 `\bar x` 좌표 혼동 및 무국소 상수 주장 정정(C-048).
- Si `a-Si/c-Si`, two-phase slope/plateau, 질량/용량 분율 정정(C-049).
- 최종 AUD에서도 wt%, 데이터 구간, LCO 수치, 주석 잔재 정정(C-056).

판정:

- 초기 build/structure/H0 표시는 과학적 최종성을 뜻하지 않았다.
- 사용자가 v1.0.23 이후뿐 아니라 v1.0.10부터 재감사를 요구한 판단은
  기록상 타당하다.
- 최신 한 번의 “H0”도 독립 재유도·코드·데이터 검증 없이는
  권위로 승격하지 않는다.

### INTENT-PROV-0100 — v1.0.22는 Si/blend의 첫 실질 이론·코드 확장이다

change log A-015/A-017과 execution ledger R5/R6는 처음으로 다음을
명시한다.

- 공통 전위의 blend charge-balance.
- `f_Si→0` 회수.
- blend dQ/dV.
- Larché–Cahn형 stress–potential coupling.
- Si/SiO_x/Si–C case set.
- `BlendedAnodeDQDV`, `from_wt`, 보존·연속·bit-exact gates.

동시에 다음 한계도 적는다.

- case 수치는 tier-C 시연값.
- SiO_x 공백은 placeholder와 warning.
- GS-1/GS-2는 `NotImplementedError`.
- 공통-μ 가산성은 1차 근사이며 실제 host 전환의 비가산성 가능.

판정:

- v1.0.21 bridgehead와 달리 v1.0.22가 Si/blend의 첫 구현 버전이다.
- 그러나 완성된 Si 물리모델이 아니라 명시적 공백을 가진
  제한적 1차 구현으로 `EMPIRICAL_ONLY/UNVERIFIED`.

### INTENT-PROV-0101 — 질량분율과 용량분율 혼동은 실제로 발생했다

change log C-049, C-052, C-056은 다음 수정 연쇄를 기록한다.

1. 10–30 wt%가 내부 capacity fraction `f_Si≈0.3–0.7`에 대응함을 명시.
2. 사용자 결정으로 외부 sweep 좌표를
   `m_Si∈[0,0.30]` 질량분율로 고정.
3. 내부 전하 보존에는 capacity fraction을 유지.
4. 후속 AUD에서 상한을 case별 약 0.54–0.78로 정정.
5. 실험 커버도 0–30 연속이 아니라 0–20 연속 + 30 단일점으로 정정.

판정:

- 외부 제조 좌표와 내부 전기화학 가중 좌표를 명확히 분리하는
  규칙은 `PRESERVE`.
- 최종 코드에는 단위·basis가 타입/필드 이름과 변환식에 드러나야 한다.
- 데이터가 없는 20–30 wt% 구간을 “커버됨”으로 표현하지 않는다.

### INTENT-PROV-0102 — 문헌 검색 모델의 실패가 문헌 부재로 오인될 뻔했다

execution ledger R4는 저비용 검색이 SiO_x/Si–C/Si entropy/blend
네 축에서 0건을 냈지만, 상위 검색으로 승급한 뒤 22건을 찾았다고
명시한다. 따라서 0건은 문헌 부재가 아니라 query breadth 실패였다.

판정:

- 검색 결과 0을 물리적 증거 부재로 단정하지 않는다.
- 최종 문헌 조사는 검색어 확장, citation chaining,
  primary-source 확인을 함께 사용한다.
- 과거 `V1`의 DOI/Crossref 서지 확인과
  load-bearing 물리 주장·정량값의 원문 검증을 분리한다.

### INTENT-PROV-0103 — 문건-코드 경계는 부록으로 제한하려는 의도가 있었다

R1은 Ch1에 곡선 코드맵과 열특성 코드 요구명세 부록을 함께 두었다.
`R1B_SWEEP_LIST.md` lines 48–52, 91–94는 이 구역이
본문을 코드 언급 없이 읽게 하면서 구현 대응을 제공하려는
의도였음을 보여 준다.

판정:

- “이론 본문은 코드 없이 자립, 구현 대응은 제한된 부록” 구조는
  현재 사용자 제약과 양립 가능하므로 보존 후보.
- 다만 본문·그림 캡션·worked example에서 함수명이나 실행 결과를
  권위 근거로 쓴 흔적은 별도 제거/이동 검토가 필요하다.

### INTENT-PROV-0104 — `bit-exact` gate에도 물리적 설계 선택이 숨어 있다

change log A-017은 `f_Si=0` bit-exact와 배경 1회 가산을 동시에
만족시키기 위해 `C_bg`를 graphite host에 담는 구성을
“유일 구성”으로 선택했다고 기록한다.

판정:

- 수치 회귀 gate로서는 유효하다.
- 배경이 물리적으로 graphite에만 속한다는 뜻인지,
  전극 공통 측정 배경을 구현상 한 번만 더하는 장치인지 구분해야 한다.
- 최종 문건의 관측 모델과 코드 ownership를 Phase 067에서 대조한다.

### INTENT-PROV-0105 — v1.0.22의 PASS는 범위별 과정 상태다

execution ledger는 R1–R9, FR, AUD를 모두 PASS로 닫았지만,
같은 기록에 다음이 남는다.

- 병합 빌드 금지.
- tier-C, placeholder, NotImplemented 물리.
- 확인 필요 값.
- 일부 SKIP과 보류 pool.
- appendix counter와 legacy title 이월.
- 데이터 구간 보간.
- 코드 gate 추가 제안 미집행.

판정:

- 각 PASS는 해당 phase의 명시 gate를 통과했다는 뜻으로만 보존한다.
- 문건·코드·실험의 최종 완결 판정은 이번 전체 재감사 뒤로 유보한다.

## Coverage Status

- 이 batch의 7문건, 477행은 `READ`.
- 누적 coverage 반영은 batch JSON 적용 후 123문건, 31,304행이다.
- v1.0.22 잔여는 94문건, 16,378행이다.

## Next

Step 19.6B:
`snapshot_v1022_r1.json` 1,391행을 전문 검독해
v1.0.21→v1.0.22 재조립의 실제 label/equation/asset/bib 이동을 확인한다.
