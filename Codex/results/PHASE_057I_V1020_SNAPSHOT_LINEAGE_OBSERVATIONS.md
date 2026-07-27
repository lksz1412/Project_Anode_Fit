# Phase 057I — v1.0.20 구조 스냅샷 계보 관찰

정본일: 2026-07-28
세부 Step: 19.4E
범위: 9 unique documents, 10,426 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 구조 스냅샷을 첫 행부터 끝 행까지 검독했다.

- v1.0.19 baseline.
- v1.0.20 P0, P2, P3, P4, P5, P7, P7b, final.

각 1,120–1,299행 JSON은 최대 400행 이하의 연속 구간으로 나누어
전문을 읽었다. 저장소에 있는 `snapshot_v1020_p6.json`은
`snapshot_v1020_p5.json`과 Git blob
`8dfea239d1787582c6c37c41fe6d06f7b204d72b` 및 byte 내용이
완전히 같아, unique-blob queue에서 P5 한 번으로 대표된다.

## Snapshot Summary

| Snapshot | Ch1 labels / eqblocks / bib | Ch2 labels / eqblocks / bib | 주된 구조 변화 |
|---|---:|---:|---|
| v1.0.19 baseline | 219 / 122 / 28 | 69 / 32 / 14 | 비교 기준 |
| v1.0.20 P0 | 219 / 122 / 28 | 69 / 32 / 14 | 파일명 이월, 구조 동일 |
| P2 | 222 / 125 / 29 | 69 / 32 / 14 | Ch1 bare-site 유도식 3개, 서지 1개 |
| P3 | 222 / 125 / 30 | 69 / 32 / 14 | Ch1 서지 1개 |
| P4 | 222 / 125 / 36 | 69 / 32 / 14 | Ch1 LCO 관련 서지 6개 |
| P5/P6 | 222 / 125 / 36 | 69 / 32 / 16 | Ch2 서지 2개 |
| P7 | 222 / 125 / 36 | 69 / 32 / 16 | `eq:lco-slots` 해시 1개 변경, Ch2 산문 행 이동 |
| P7b | 225 / 128 / 36 | 69 / 32 / 16 | 배경 수식 3개 |
| final | 225 / 128 / 36 | 69 / 32 / 16 | Ch1/Ch2=P7b, appendix 최초 snapshot 추가 |

final appendix는 labels 30, eqblocks 19, asset 0, bib 0으로
처음 등재됐다.

## Provisional Findings

### INTENT-PROV-0060 — baseline→P0는 버전 이월이며 새 구조가 아니다

v1.0.19 baseline과 v1.0.20 P0는 최상위 파일명만
`v1.0.19`에서 `v1.0.20`으로 바뀌고,
Ch1/Ch2 label 목록, equation-block hash, asset 수, bibliography 목록이
동일하다.

판정:

- v1.0.20의 출발점은 v1.0.19의 구조적 복제라는 handover를
  기계 기록이 뒷받침한다.
- 이 스냅샷은 문장 전체가 byte-identical임을 뜻하지 않고,
  캡처된 구조 필드가 동일하다는 뜻이다.

### INTENT-PROV-0061 — v1.0.20의 새 수식 자산은 여섯 개로 좁혀진다

phase 간 set/hash 비교 결과는 다음과 같다.

1. P0→P2:
   `eq:sm-baresum`, `eq:sm-baremid`, `eq:sm-bare` 추가,
   `ashcroftmermin1976` 추가.
2. P2→P3:
   `dreyer2011` 추가, equation label/hash 변화 없음.
3. P3→P4:
   `bakerverbrugge2018`, `imada1998`, `marianetti2004`,
   `mott1968`, `msmr_origin2017`, `vanderven1998` 추가,
   equation label/hash 변화 없음.
4. P4→P5:
   Ch2에 `dahn1991`, `ohzuku1993` 추가,
   equation label/hash 변화 없음.
5. P5→P7:
   Ch1에서 `eq:lco-slots` hash
   `33b9f996b18e`→`228a215741f1` 한 건 변경.
6. P7→P7b:
   `eq:sm-exch`, `eq:sm-fdbe`, `eq:lco-mottcrit` 추가.
7. P7b→final:
   Ch1/Ch2 label, eqblock, hash, bib, asset 변화 없음.

판정:

- v1.0.20의 구조상 새 수식은 bare-site 원형 3개와
  배경 보강 3개가 전부다.
- 나머지 주된 작업은 산문 정정, 참조 보강, 자립성, 검수였다는
  계보를 `PRESERVE`.
- “문건 전체 물리 골격 대개정”이라는 해석은 기계 기록과 맞지 않는다.

### INTENT-PROV-0062 — 행 번호 기반 무라벨 수식 비교는 이동과 변경을 구분해야 한다

P5→P7의 Ch2 snapshot에서는 다음 key가 제거·추가처럼 보인다.

- `ch2_sec00_intro.tex:44`→`:45`
- `ch2_sec08_synthesis.tex:49`→`:52`
- `:78`→`:81`
- `:96`→`:99`

그러나 각 쌍의 hash는
`ad55135a5939`, `de91d9f5c758`, `ddff4c11814c`,
`9d4cf379c2b1`로 동일하다. 산문 삽입으로 줄 번호만 이동한 것이다.

판정:

- 무라벨 식은 file:line key의 추가/삭제가 아니라 hash 대응으로
  이동 여부를 먼저 판정한다.
- 후속 구조 감사에서 line-number churn을 물리식 변경으로 세지 않는다.
- 가능한 핵심 식에는 안정 label을 부여해 이 취약성을 줄인다.

### INTENT-PROV-0063 — appendix는 final이 최초 기준선이라 phase 회귀를 증명하지 못한다

`appendix_phase_separation.tex`은 final snapshot에만 처음 등장한다.
labels 30, equation blocks 19를 완전하게 기록하지만
P0–P7b의 appendix snapshot이 없으므로,
final에서 “변화 없음” 또는 “어떤 phase에서 무엇이 바뀜”을
이 JSON 계보만으로 말할 수 없다.

판정:

- final appendix snapshot은 이후 버전의 기준선으로 `PRESERVE`.
- v1.0.20 내부 appendix 회귀 무변경 주장은 `UNVERIFIED`.
- 필요하면 실제 Git diff와 phase commit을 별도 대조한다.

### INTENT-PROV-0064 — 구조 snapshot의 PASS 범위는 과학적 타당성과 다르다

이 스냅샷이 직접 증명하는 것은 다음뿐이다.

- label 집합.
- 검출된 equation block의 정규화 hash와 boxed 여부.
- 문건별 asset count.
- bibliography key 집합.
- 일부 무라벨 수식의 file:line 위치.

다음은 증명하지 못한다.

- 산문 설명의 물리 정확성.
- equation의 유도 타당성, 단위, 부호, 적용 범위.
- 코드가 equation을 정확히 구현하는지.
- 실제 데이터의 peak 저하·broadening·온도/율속 의존을 설명하는지.
- 인용 문헌이 load-bearing 주장과 조건까지 일치하는지.
- label 밖 그림 좌표·표 숫자·파라미터의 과학적 권위.

판정: 구조 snapshot은 `STRUCTURAL_EVIDENCE`로만 사용한다.
build green, hash 안정, label 보존을 empirical validation으로
승격하는 것은 `REJECT`.

### INTENT-PROV-0065 — 기계 계보도 v1.0.20을 품질 보강판으로 한정한다

최종 Ch1은 baseline 대비 labels +6, eqblocks +6, bib +8이고
asset count 336은 그대로다. 최종 Ch2는 labels/eqblocks/asset이
전부 동일하고 bib만 +2다. 캡처된 기존 핵심 식 대부분의 hash가
baseline부터 final까지 유지됐다.

이는 v1.0.20의 handover 정의와 일치한다.

- 기존 물리 골격을 보존.
- bare-site 원형과 배경 수식의 자립성 보강.
- LCO/흑연 문헌 근거 보강.
- 산문 정정과 챕터간 정합.
- 코드는 v1.0.19 matched carry-forward.

판정: `PRESERVE`.
후속 v1.0.21 이상의 확장을 v1.0.20에 소급 귀속하지 않는다.

## Evidence Limits to Carry Forward

1. equation hash 불변은 식 문자열 안정성이지 식의 진실성 증명이 아니다.
2. asset count 불변은 그림 내용이 정확하다는 뜻이 아니다.
3. bibliography key 추가는 주장-scope 검증 완료와 다르다.
4. unlabelled block의 line key는 산문 삽입에 취약하다.
5. appendix phase history는 actual Git diff로 보강해야 한다.
6. 코드/데이터 검증은 Phase 067의 별도 behavior matrix에서 수행한다.

## Coverage Status

- 이 batch의 9 unique 문건은 `READ`.
- v1.0.20 queue: 81/81문건, 17,041/17,041행 `READ`.
- 누적 Phase 057 coverage: 103문건, 18,499행.
- 전체 Phase 057 queue 잔여: 168문건, 39,296행.
- v1.0.20 전문 검독은 완료됐지만 Phase 057 최종 `VERIFIED`는 아니다.

## Next

Step 19.5:
v1.0.21 queue를 논리 batch로 나누고, 사용자 확정 결정과
Q2/Q3/그림/LCO/Si 후보가 실제로 무엇으로 채택·변형·폐기됐는지
전문 검독한다.
