# Phase 057AX — v1.0.24 HTML code guide 관찰

정본일: 2026-07-28
세부 Step: 19.9A
범위: 1 unique document, 3,812 physical lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html`

첫 행부터 마지막 행까지 전량 검독했다. 프로젝트 서술·markup과
내장 Mermaid 런타임을 분리하고, 런타임 전 구간은 연속 chunk
hash·프로젝트 용어 전수 검색으로 확인했다. HTML parser로 모든
표의 실제 열 수도 검사했다.

## Whole-file Verification

- file size: 3,594,138 bytes
- physical lines: 3,812
- LF count: 3,811; final line은 LF 없이 종료
- SHA-256:
  `c795a947a44b31eb4d0039e67d067a96d51d807e9a3de9fda799534180908aa1`
- project-visible HTML: lines 1–219
- embedded Mermaid vendor runtime: lines 220–3,807
- Mermaid initialization/closing markup: lines 3,808–3,812
- `<script>` open/close: 2/2
- HTML parser가 인식한 tables: 8
- Mermaid blocks: 5

v1.0.24와 v1.0.24.1의 Markdown 및 HTML은 각각 동일 hash다.
따라서 이 파일은 v1.0.24.1에서 새로 수정된 설명이 아니라
v1.0.24 생성물의 동결 복제다.

### Embedded runtime coverage

| 연속 구간 | 행 | SHA-256 |
|---|---:|---|
| 220–619 | 400 | `39ab91303a92f029d5aaf245bf204260336568e8801bb3cbd110cb474797eb49` |
| 620–1,019 | 400 | `dab92d43ec44947379a17a3207b5608ce2924648450efd1094c9c1f07ad08726` |
| 1,020–1,419 | 400 | `4a45d7617b375e4fe7057229e9bb14a01f77404b7a1eb173616fef640778be09` |
| 1,420–1,819 | 400 | `26cc556cb6d961c3d0013252d98044db89c82e174bcf5188011519e32cf9a022` |
| 1,820–2,219 | 400 | `48d933f7aace7eee0f485a3c7ea4b54d4477dfd6ff83b3fe1112cab66d433247` |
| 2,220–2,619 | 400 | `17d73a799ecc9cec61e57889ed71d1c45206579bc7e7d767ff2f9e1252cf40f5` |
| 2,620–3,019 | 400 | `42e2bef986d2ecfa80371fe798e3dafac1c9aed2d5f7faa47d510f3296e4fffb` |
| 3,020–3,419 | 400 | `4952f63af2d14ccea0688367713b4fc991ec155523d68f7ffd7663b6271ef7c9` |
| 3,420–3,807 | 388 | `3e5b4b52e4fa3fb12e55239ab18f49b8b159db0758f8529d349c2c7f606e7b3e` |

이 3,588행의 한글 문자는 0개다. `anode_fit`,
`graphite_staging`, `lco_msmr`, `regsol`, `dq/dv`,
`v1.0.24`의 출현도 모두 0회다. 즉 이 구간은 추가 사용자 의도나
프로젝트 과학을 담은 숨은 서술이 아니라, 자체 포함형 diagram
renderer vendor asset이다.

## Provisional Findings

### INTENT-PROV-0388 — HTML은 별도 과학 정본이 아니라 v1.0.24 code guide의 생성 복제물이다

visible content는 이미 검독한
`Claude/docs/v1.0.24.1/CODE_GUIDE_v24.md`와 같은 구조·주장·
예제를 전달한다. v1.0.24.1에서 의미 변경은 없다.

판정:

- 과학 및 사용자 의도의 정본은 Markdown source와 그 근거
  문건이지 이 HTML artifact가 아니다.
- generated HTML은 배포 편의를 위한 파생물로만 관리한다.
- v1.0.25 이후 상태를 설명하는 최신 guide로 읽지 않는다.

### INTENT-PROV-0389 — 대형 vendor bundle은 검독 범위를 흐리지만 새 프로젝트 의미를 더하지 않는다

3,588/3,812행과 대부분의 byte가 Mermaid runtime이다. 프로젝트
용어 전수 검색과 연속 chunk hash로 전체 구간을 확인했으며,
추가 물리·계획·사용자 피드백은 없었다.

판정:

- source audit에서는 vendor asset과 authored content의 coverage를
  분리 기록한다.
- 향후 문건 배포는 renderer version/hash를 고정하고 generated
  artifact를 재현 가능하게 만드는 편이 낫다.
- bundle 크기나 행 수를 서술 깊이 또는 검토량으로 오인하지 않는다.

### INTENT-PROV-0390 — Markdown→HTML 변환이 세 개의 물리·API 표 행을 손상했다

HTML parser 기준 다음 행의 cell 수가 header와 다르다.

1. 함수 사전의 `equilibrium`: 3열 표가 5열이 됨.
2. 생성자 옵션의 `Rn`: 3열 표가 5열이 됨.
3. 변수 사전의 `V_n`: 4열 표가 6열이 됨.

세 경우 모두 Markdown 원문의 `|I|` 또는 `\|I\|`가 변환 중
cell delimiter로 처리되면서 절댓값 기호와 식의 의미가
쪼개졌다.

판정:

- HTML은 현재 `REGENERATE_REQUIRED`.
- HTML 생성 후 표별 예상 열 수와 수식 escaping을 자동 검증해야
  한다.
- 손상된 HTML의 식을 code–theory conformance 근거로 인용하지
  않는다.

### INTENT-PROV-0391 — `securityLevel:'loose'`는 정적 동결 파일에서는 과학 결함이 아니지만 배포 경계를 명시해야 한다

마지막 초기화 script는 Mermaid를 `securityLevel:'loose'`로
구동한다. 현재 diagram source는 같은 저장소의 정적 authored
content이므로 이 사실 자체가 현 모델의 물리 오류를 만들지는
않는다.

판정:

- 외부 또는 사용자 입력 diagram을 같은 경로로 렌더하는 기능으로
  확장하지 않는다.
- 최종 release artifact에는 최소 권한 설정 또는 신뢰된 정적
  input 전용이라는 생성 계약을 둔다.
- 이 항목을 과학 gate와 혼합하지 않고 artifact-safety gate로
  관리한다.

### INTENT-PROV-0392 — HTML은 v1.0.24의 열역학적 seam을 그대로 증언한다

guide는 regular-solution branch가 `equilibrium()`에만 들어가고
`dqdv()`, `entropy_coefficient()`, `solve_U_oc()`는 계속 logistic을
쓴다고 명시한다. 또한 `delta`를 “regsol kinetic 폭”이라 부르면서
equilibrium kernel의 broadening에 사용한다.

판정:

- 한 transition이 서로 다른 latent thermodynamics를 경로별로
  쓰는 구조는 100% 문건–코드 일치가 아니다.
- equilibrium coexistence broadening, material heterogeneity,
  instrument response, finite-rate kinetics를 별도 물리량으로
  분리해야 한다.
- 당시의 명시적 scope 표기는 정직한 기록으로 보존하되 최종
  모델의 closure로 채택하지 않는다.

### INTENT-PROV-0393 — hard cutoff와 seed table은 물리 법칙으로 승격할 수 없다

HTML은 `z_cut=4.357`, `A_cap_RT=4.0`, fixed seed values,
`SI_SPECIFIC_CAPACITY={1000,1710,3117}`를 API/default로
보여준다. 동시에 대부분의 U·w·Q는 fit override seed라고
설명한다.

판정:

- numerical guard, optimizer seed, material measurement,
  constitutive parameter를 별도 schema와 문건으로 분리한다.
- hard cutoff/cap은 유도·해상도·error tolerance 근거가 없으면
  최종 물리식에 포함하지 않는다.
- 특히 Si 계열 비용량은 조성·반응 범위·전극 formulation에
  따라 달라지므로 고정 “tier-A material constant”로 취급하지
  않고 provenance와 uncertainty를 요구한다.

### INTENT-PROV-0394 — code guide는 최종 이론 문건 밖의 companion이어야 한다

이 파일은 함수명, 클래스, API, 플래그, import 예, `curve_fit`
예시를 중심으로 한다. 이는 당시 code-understanding guide로는
유용하지만 사용자가 확정한 “이론 문건에는 코드 언급 배제”
규칙과는 공존할 수 없다.

판정:

- 최종 theory manuscript에는 이 내용을 편입하지 않는다.
- 별도 implementation specification과 conformance matrix가
  이론의 equation/assumption ID를 코드·시험에 단방향 연결한다.
- 이론을 코드에 맞춰 고치는 방향이 아니라 채택 이론을 먼저
  동결한 뒤 코드가 이를 따르는 순서를 강제한다.

## Direction Recovered

1. HTML과 PDF 같은 생성 산출물을 저자 서술 정본과 분리한다.
2. 생성물도 수식·표가 원문 의미를 보존하는지 자동 검증한다.
3. thermodynamics, heterogeneity, kinetics, observation을 서로
   다른 역할과 단위로 표현한다.
4. API default나 fitting seed를 물리 상수로 승격하지 않는다.
5. code guide와 conformance 문서는 이론 문건 밖에 둔다.

## Coverage Status

- 이 batch의 1문건, 3,812행은 `READ`.
- 누적 coverage 반영 후 목표는 269문건, 57,549행이다.
- 전체 Phase 057 잔여 목표는 2문건, 246행이다.

## Next

Step 19.9B:
v1.0.24 R0 snapshot JSON 1문건과 v1.0.25.2 kernel comparison
HTML 1문건, 합계 246행을 key/value 및 embedded artifact까지
전량 검독한다.
