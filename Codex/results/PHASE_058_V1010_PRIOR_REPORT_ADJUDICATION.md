# Phase 058 v1.0.10 과거 문제·무결성 보고서 재판정

정본일: 2026-07-28

대상: Phase 058 Step 29.4

claim matrix:
`Codex/results/PHASE_058_V1010_PRIOR_REPORT_ADJUDICATION.json`

## 판정 경계

이 문서는 역사적 감사 기록이며 새 이론 정본이 아니다. 과거 두
보고서의 투표 수, 작성 모델, `PASS` 문구와 자기 인용을 증거로 세지
않았다. 원고, production source, test/demo, 저장 artifact와 Step
29.1–29.3의 독립 재유도·극한·수치 검산에 다시 연결했다.

두 보고서의 SHA-256은 matrix에 고정했다. 총 31개 claim을
`CONFIRMED`, `PARTIAL`, `REJECTED`, `UNRESOLVED` 중 하나로
처분했다.

| 처분 | 수 |
|---|---:|
| `CONFIRMED` | 10 |
| `PARTIAL` | 9 |
| `REJECTED` | 12 |
| `UNRESOLVED` | 0 |

## 가장 중요한 상충의 해소

### 1. 원래 R1도, 전면 철회도 모두 과도하다

최초 problem report의 “kernel이 near-delta 분리 peak를 만들 수
없다”는 주장은 틀렸다. `n=0.12` demo가 네 local maximum을 만들며,
logistic kernel은 폭을 충분히 좁힐 수 있다.

그러나 integrity report는 이 반례에서 너무 멀리 갔다. “분리가
가능하다”는 것은 수치 표현력을 증명할 뿐 다음을 증명하지 않는다.

- fitted sub-thermal width가 two-phase equilibrium에서 유도됨
- `w`가 입자·조성 이질성인지 측정 broadening인지 식별됨
- finite-current tail과 equilibrium width가 분리됨
- apparent-potential 분포가 실제 물질 상을 뜻함

따라서 정확한 판정은 다음이다.

\[
 \text{peak representability}
 \;\not\Rightarrow\;
 \text{thermodynamic provenance}.
\]

near-delta와 broadening을 무조건 두 번 convolution하라는 옛 처방도
채택하지 않는다. 대신 equilibrium phase response, kinetic state
evolution, ensemble heterogeneity와 observation kernel을 각각 정의하고
forward model에서 조립한 뒤 식별 가능성을 검사한다.

### 2. default kinetic-off 진단은 맞다

problem report R2는 독립 probe와 일치한다. shipped graphite
default에서 `Rn=0`이면 \(I=0\)–1 A 곡선이 동일하고, lag length는
grid switch 아래라 equilibrium branch로 떨어진다. `Rn`은 상수
전위 이동을 만들 뿐 peak height/FWHM을 바꾸지 않는다.

따라서 사용자가 출발점으로 제시한 유한전류 peak 저하·broadening은
v1.0.10 default에서 설명되지 않는다. 이를 “단지 기본값 표시 문제”로
낮춘 integrity report의 전역 결론은 기각한다.

### 3. 내부 정합과 외적 물리 타당성을 혼동했다

면적, entropy finite difference, electronic gate center와 heat
round-trip 중 일부는 해당 구현이 자기 식을 재현한다. 이 결과는
회귀·수치 identity로서 가치가 있다.

그러나 다음 승격은 허용하지 않는다.

- wide-window 면적 보존 → finite-window capacity accounting 완료
- \(-45.68\) J/(mol K) 재생 → LCO electronic entropy 검증
- \(\gamma=0\) 무변화 → hysteresis memory 완결
- source byte 보존 → 물리 개선 전부 승계
- 그림 생성/PASS 출력 → public data validation

특히 electronic gate의 조성 적분은 \(-9.135\) J/(mol K)로,
원고의 \(0.18k_B=1.497\) J/(mol K) anchor보다 6.10배 크다.
이는 forward reference 부족이 아니라 정의·정규화·상분율의 물리
충돌이다.

## 과거 보고서에서 보존할 진단

- R2: default kinetic tail 비활성
- R3: 충전 tail 본문과 caption의 방향 모순
- R4: fitting guide의 전역 \(\Omega>2RT\) bound와 단상 허용의 충돌
- R6: irreversible heat의 비음수 invariant 부재
- R7: 면적 “assert” 명칭과 실제 report-only 동작의 불일치
- H1/H2/H5: byte-identical·버전 라벨·dead header의 provenance 결함
- H6: layout-fixed 주장은 별도 전페이지 render가 필요하다는 경고

이들은 현재 재검증에서 실제 source/output과 연결됐다.

## 과거 보고서에서 강등할 진단

- analytic logistic area는 보존되지만 fitting window 밖 tail은
  observation/censoring 문제로 남는다.
- \(w^\mathrm{eff}\)는 regular-solution 중심 기울기의 국소 근사로는
  논할 수 있으나 interacting equilibrium의 전역 logistic 폭이 아니다.
- branch gap closed form은 자기 식과 일치하지만 measured hysteresis나
  cycle memory의 일반식이 아니다.
- first-order causal relaxation은 유망한 reduced model이지만 legacy
  Eyring prefactor, frozen affinity와 grid handoff는 보존하지 않는다.

## integrity report의 전역 PASS를 기각하는 이유

“잔여가 전부 minor”라는 결론과 달리 다음 blocker가 확인됐다.

1. C-rate–capacity factor-3600 단위 계약
2. interacting free energy와 ideal logistic equilibrium의 혼합
3. default current broadening 부재와 direct lag의 \(I\to0\) 위반
4. grid-dependent mode switch와 molecular-to-electrode
   coarse-graining 부재
5. frozen \(A=4RT\)와 underived
   \(\Delta H_a-\chi\Omega\)
6. entropy-width contract 불일치와 heat sign API 충돌
7. electronic entropy sum-rule 충돌과 \(T^2\) 미구현
8. doped high-voltage LCO, Si, graphite–Si와 public-data validation 부재

이는 문구·라벨 차원이 아니라 사용자의 연구 질문과 직접 연결된
물리·수치·검증 결함이다.

## 후속 설계 명령

v1.0.10에서 보존할 것은 transition-wise capacity conservation,
ideal logistic limit, regular-solution critical condition,
first-order causal relaxation의 reduced-model 가능성,
reversible-heat identity다.

새 이론은 다음 계층을 섞지 않는다.

\[
 \boxed{
 \text{equilibrium free energy}
 \rightarrow
 \text{state kinetics}
 \rightarrow
 \text{electrode/cell transport}
 \rightarrow
 \text{observation model}
 }
\]

이론 원고에는 이 물리·화학 논리와 적용 한계만 둔다. 구현 식별자,
함수명, gate, default와 code conformance는 별도 문건에서 관리한다.

## Step 29 결론

v1.0.10은 완결된 물리 정본이 아니라, 보존 가능한 수학 kernel과
중요한 실패 양식이 함께 있는 역사적 empirical baseline이다.
problem report는 여러 국소 결함을 맞혔지만 R1 처방을 과장했고,
integrity report는 그 과장을 바로잡은 뒤 내부 수치 정합을 전체
물리 무결성으로 과승격했다.

최종 판정:

`PRIOR_REPORTS_CONTAIN_USEFUL_LOCAL_DIAGNOSES_BUT_THE_INTEGRITY_PASS_IS_REJECTED`

다음 Step 30에서는 v1.0.11과 v1.0.12가 위 blocker를 실제 source와
실행 경로에서 무엇을 고쳤고 무엇을 문장만 바꿨는지 commit 단위로
재구성한다.
