# Phase 057AH — v1.0.24 author brief·cherrypick·W1–W3 관찰

정본일: 2026-07-28
세부 Step: 19.8B
범위: 5 unique documents, 388 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/comp_R1/AUTHOR_BRIEF.md`
- `results/comp_R1/CHERRYPICK_R1.md`
- `results/comp_R1/W1/NOTES.md`
- `results/comp_R1/W2/NOTES.md`
- `results/comp_R1/W3/NOTES.md`

다섯 문건을 첫 행부터 마지막 행까지 전량 검독했다. 최초 통합
뒤 사용자 지적으로 정식 체리픽을 재집행한 시점과, 각 초안의
정직한 공백을 분리해 읽었다.

## Provisional Findings

### INTENT-PROV-0236 — “시드 물리는 확정, 저자는 변경 금지” 규칙이 경쟁초안의 독립성을 제거했다

AUTHOR_BRIEF는 세 재료의 물리·값을 seed table에서 이미
확정했고, 9개 저작 창에는 이를 바꾸지 말고 상세하게 서술하라고
지시했다. 그 결과 CHERRYPICK 문건이 스스로 인정하듯 graphite
분류에 대해 9개 raw 창 전부가 같은 단정을 반복했고, 기존 §7과
충돌했다.

판정:

- 여러 서술 대안에서 설명력과 오류를 비교하는 competition은
  `PRESERVE_AS_AUTHORING_TOOL`.
- 같은 seed를 반증할 권한이 없는 9개 초안을 독립 물리검증으로
  간주하는 것은 `REJECT`.
- 최종 workflow는 seed-adversary, source verifier, derivation
  checker를 저작 경쟁보다 먼저 독립시킨다.

### INTENT-PROV-0237 — graphite 상분류 충돌을 “피팅된 Ω가 결정”으로 봉합하면 관측과 모델이 순환한다

W3는 seed의 두-상 4/고용체 1 분류와 기존 §7의 두-상 2/
고용체 3 분류가 `1′↔4`, `3↔2L`에서 충돌한다고 밝혔다.
체리픽은 raw 창의 단정을 버리고 §7에 판정을 위임했다.

그러나 “최종 판정은 fitted Ω_j가 정한다”는 봉합도 충분하지
않다. 같은 dQ/dV peak를 맞추기 위해 Ω와 폭·용량·feature 수를
조절한 뒤 그 Ω로 phase identity를 선언하면 모델 선택과
물리 판정이 순환한다.

판정:

- 충돌을 숨기지 않고 단정을 철회한 것은 `PRESERVE`.
- fitted Ω 단독의 phase classifier는 `REJECT`.
- XRD/operando phase evidence, voltage plateau/coexistence,
  temperature evolution을 독립 판정자로 둔다.

### INTENT-PROV-0238 — stage-2L은 물리적으로 중요한 후보지만 당시 수치는 seed-injection demo다

문건들은 stage-2L의 온도 안정화와

`d(Delta U_split)/dT = Delta(Delta S)/F`

라는 열역학 항등을 정확히 강조한다. 반면 `+15/-14 J mol^-1
K^-1`, 병합 약 10℃, 재현 `0.271 mV/℃`는 실제 독립 fitting
결과가 아니라 `Delta(Delta S)=29`를 넣은 demo 또는 tier-C
초기값임을 W2/W3가 명시한다. 상온 feature 추가는 R²를
`-0.44%p` 악화시켰다.

판정:

- 열역학적 분리 기울기와 stage-2L 현상은
  `PRESERVE_AS_PHYSICS`.
- 절대 entropy 배정과 병합온도 수치는 `EMPIRICAL_SEED`.
- 다온도 graphite 데이터에서 두 peak의 center·area·width를
  공동 적합하고 독립 XRD와 대조한다.

### INTENT-PROV-0239 — Si Frumkin kernel은 정당한 후보지만 해당 데이터는 우월성을 보이지 않았다

W2는 순수 Si에서 자유폭 logistic가 `R²=0.9985`, standalone
regular-solution fit이 `R²=0.962`라고 기록했다. blend에서는
`+0.66%p` 개선을 보고했지만, 이는 데이터·자유도·분할이
완전히 기록된 외부 validation이 아니다.

또 Si broadness의 실제 출처가 Ω가 아니라 `n_j>1`인 gallery
폭이라고 스스로 정정했다. 따라서 `Omega<2RT`는 single-phase
guard 역할이고, peak broadening closure 자체는 아니다.

판정:

- homogeneous regular-solution 식은 `THEORY_CANDIDATE`.
- Si 데이터가 이 kernel을 선택했다는 결론은 `REJECT`.
- logistic/free-width, regular solution, distributed-state,
  stress-coupled 모델을 같은 데이터 split과 복잡도 penalty로
  비교한다.

### INTENT-PROV-0240 — `Omega→0` bit-exact logistic 회수는 폭 다중도까지 포함해 재검산해야 한다

초안 식은

`dQ/dV = Q F / |RT/[theta(1-theta)] - 2 Omega|`

이고 `Omega=0`에서 기존 logistic를 bit-exact로 회수한다고
쓴다. 하지만 기존 logistic 폭은 `w_j=n_j RT/F`이고,
Si broadness는 바로 `n_j>1`에서 온다고 같은 문건이 말한다.

`n_j=1`이 아니면 위 식의 `Omega=0` 극한은 자유 `n_j` 폭의
logistic와 일반적으로 동일하지 않다. 코드가 별도 scaling을
넣었는지는 후속 R2/code-history를 확인해야 한다.

판정:

- `n_j=1` 표준 극한은 `DERIVED`.
- 임의 gallery-width와의 bit-exact 회수는 `UNVERIFIED`.
- 문건–코드 계약에서 `n_j`, Ω, effective width의 역할을
  차원·극한별로 다시 검산한다.

### INTENT-PROV-0241 — LCO feature 명칭과 전압 anchor가 저작 시점에도 해결되지 않았다

AUTHOR_BRIEF는 3.70 V(O2), 3.90 V(O3)를 언급했지만,
기존 문건은 T1≈3.90 V, T2≈4.05 V, T3≈4.17–4.20 V를 쓴다.
W1/W3는 이 충돌을 발견하고 O2/O3 명칭을 채택하지 않은 채
feature-general per-peak Ω로 후퇴했다.

판정:

- 미확정 phase label을 억지로 통합하지 않은 것은 `PRESERVE`.
- 현재 LCO peak identity와 high-voltage doped-LCO 물리
  mapping은 `UNVERIFIED`.
- 최종 LCO 장은 조성 x, 결정상, redox/ordering, voltage
  window, dopant를 문헌·데이터와 함께 재구성한다.

### INTENT-PROV-0242 — R²와 내부 산출물을 “실측”으로 부르는 용어를 교정해야 한다

W2는 내부 `regsol`, `ablation`, `T_SPLIT` 산출물을 실측
근거로 분류했다. 일부 입력이 실험 데이터에서 왔더라도,
fit-derived Ω/폭, seed-injection 재현, R² 증분은 직접 물성
측정과 다르다.

판정:

- 재현 가능한 내부 분석값은 `COMPUTATIONAL_EVIDENCE`.
- XRD, calorimetry, entropy profiling, electrochemical curve의
  직접 관측은 `EXPERIMENTAL_EVIDENCE`.
- 최종 문건에서 두 용어와 provenance를 분리한다.

### INTENT-PROV-0243 — 체리픽이 포착한 반례·회귀 기록은 보존할 좋은 작업 이력이다

CHERRYPICK은 base 점수만 남기지 않고 다음을 기록했다.

- raw 초안 전부의 공통 분류 오류.
- 무근거 R²와 tier 과대평가 배제.
- Frumkin 식의 F 위치 오류 배제.
- stage-2L 상온 `-0.44%p` 반례 보존.
- 토글 기본값 drift와 잔존 header 오류 교정.
- refine-b 뒤 별도 검토2에서 회귀 2건 포착.

판정:

- `base + graft + reject + regression` 원장은 `PRESERVE`.
- 최종 phase 계획에도 채택 근거뿐 아니라 폐기 이유와 반례를
  필수 필드로 둔다.

### INTENT-PROV-0244 — 당시 본문에 내부 파일명을 인용한 관행은 최신 사용자 경계와 충돌한다

W2는 검증 artifact를 본문에 `\code{파일명}`으로 인용하는
기존 관행을 따랐고, AUTHOR_BRIEF도 코드 플래그와 파일 경로를
소절 사양에 포함했다.

판정:

- provenance 자체는 반드시 보존한다.
- 이론 문건에서 내부 파일명·함수·플래그를 제거한다.
- 동일 정보는 별도 evidence ledger와 implementation companion에
  두고 이론 문건에는 물리적 가정·식·실험 근거만 남긴다.

## Coverage Status

- 이 batch의 5문건, 388행은 `READ`.
- 누적 coverage 반영 후 목표는 239문건, 49,417행이다.
- 전체 Phase 057 잔여 목표는 32문건, 8,378행이다.

## Next

Step 19.8C:
W4–W6 NOTES 3문건 247행을 전문 검독한다.
