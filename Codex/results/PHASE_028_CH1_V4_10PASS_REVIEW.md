# PHASE 028 - Chapter 1 V4 10-Pass Full Review

## 0. Phase 목적

최종 목표는 `graphite_ica_ch1_codex_candidate_v4.tex`가 Chapter 1 단독으로 다음 조건을 만족하는지 검수하고, 발견 문제를 수정한 뒤 검증 가능한 상태로 고정하는 것이다.

- 대상 시스템: LIB graphite anode ICA(dQ/dV)에서 staging/phase-transition peak 뒤 꼬리의 온도 및 전위 의존 거동.
- 핵심 관찰: 낮은 온도에서는 post-peak tail이 길고, 높은 온도에서는 tail이 상대적으로 짧게 끝난다.
- 핵심 논리: 단순 Gaussian peak broadening이 아니라 temperature activation barrier와 electrode-potential-assisted effective barrier lowering이 relaxation length spectrum을 바꾸며 tail shape을 만든다.
- 작성 기준: 한국어 문장 + 학술 용어 영어 병기, 학부생이 따라갈 수 있는 단계식 전개, 변수 첫 등장 설명, 물리적 비약 금지, step-function식 임의 도약 금지, 논문/교과서 근거 없는 가정 금지.
- 산출 목표: Chapter 1만 읽어도 simple real-data fitting approximation을 뽑을 수 있는 수준의 이론 배경.

## 1. 입력 파일과 실제 확인 범위

| 구분 | 경로 | 확인 범위 | 상태 |
|---|---|---:|---|
| Codex Chapter 1 V4 | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v4.tex` | 1-945행 | READ_FULL, 10-pass coverage missing=0 |
| 계획서 | `D:\Projects\Project_Anode_Fit\Codex\plans\2026-06-02-chapter1-v4-full-rebuild-10pass-plan.md` | 전문 참조 | 적용 |
| Claude 최종본 | `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch1_rebuilt.tex` | 1-1627행, 후반 882-1627행 재분할 확인 | 비교 기준 |

Codex V4 SHA256: `C1607A7E101B1D3BA4BD4CDF9D88D0C8AEDAFADCEA6BBFF1E525EC540C876517`

## 2. 10-pass 전문 검수 범위표

각 pass는 서로 다른 chunk 길이 또는 관점으로 1-945행 전체를 덮도록 구성했다. coverage script 결과는 모든 pass에서 `missing=0`이었다.

| Pass | Chunk scheme | Chunks | Missing |
|---|---|---:|---:|
| P1 | section-level: 1-48, 49-91, 92-127, 128-162, 163-173, 174-209, 210-296, 297-396, 397-449, 450-535, 536-570, 571-612, 613-632, 633-688, 689-754, 755-813, 814-858, 859-884, 885-945 | 19 | 0 |
| P2 | fixed 70-line chunks | 14 | 0 |
| P3 | 90-line offset chunks | 12 | 0 |
| P4 | fixed 120-line chunks | 8 | 0 |
| P5 | fixed 55-line chunks | 18 | 0 |
| P6 | dependency-chain chunks | 11 | 0 |
| P7 | reverse 95-line chunks | 10 | 0 |
| P8 | fitting-usability chunks | 11 | 0 |
| P9 | adversarial physics chunks | 10 | 0 |
| P10 | full sweep 1-945 | 1 | 0 |

## 3. Pass별 검수 결과와 수정 반영

| Pass | 검수 초점 | 발견/판단 | 처리 |
|---|---|---|---|
| P1 | 문서 구조, 프로젝트 메타데이터 잔류 | 본문 내 process label/CHARTER류가 남으면 논문 본문 오염 | TeX 본문에서 제거, phase 기록으로 분리 |
| P2 | convention consistency | Ch.1의 `chi_j`가 Ch.3 `beta_j`와 동일물로 고정되면 Level-A/Level-B 경계 붕괴 | `chi_j`는 Ch.1 scalar relaxation-barrier sensitivity, `beta_j`는 Ch.3 kinetic model에서만 대응 가능하도록 고정 |
| P3 | 수식 연쇄와 부호 | Eyring 보정에서 `ln(1/L)` 안에 이미 `+ chi A/RT`가 들어 있는데 다시 더하면 double count | `y(T)=ln[1/(LT)]-chi_j A_j/(RT)`로 수정, 부호 설명 추가 |
| P4 | 변수 도입과 물리량 설명 | `L`, `q_a`, `A`, `Theta_0`, `R_n`, `rho_G`가 fitting 절차에서 물리 의미 없이 튀어나오면 안 됨 | simple-fit 절에서 각 변수를 fitting observable/nuisance/독립 입력으로 분리 |
| P5 | 단위와 차원 | `L`은 전하좌표 기준 무차원 relaxation length, 전압축에서는 `L_phi`로 변환 필요 | `L_phi` 식과 0.2C anchor 설명 유지 |
| P6 | Plan B/Plan A 경계 | Fredholm Plan A를 기본 해법처럼 쓰면 graphite Volterra feedback 문제를 과도 단순화 | Plan B direct g-grid를 항상 보존되는 기준 해법으로, Plan A는 검증 통과 시 closed-form auxiliary로 제한 |
| P7 | reverse reference sweep | undefined label/citation, adjacent math delimiter 회귀 위험 | `missing_refs=0`, `missing_cites=0`, `$$=0`로 확인 |
| P8 | Chapter 1 단독 fitting usability | 이론만 있고 simple fitting approximation이 없으면 사용자가 바로 실데이터에 연결 불가 | single-mode tail 근사식, extraction order, falsification rule을 Chapter 1 내부에 유지 |
| P9 | adversarial physics | C-rate 증가가 항상 tail 단축이라는 식의 단일 부호 주장은 위험 | current prefactor, potential-assisted acceleration, apparent-axis polarization, transport limitation의 경쟁으로 표현 |
| P10 | 최종 sweep | critical/high 논리 결함 없음. 남은 항목은 데이터 검증 영역 | residual risk를 phase report에 분리 기록 |

## 4. 핵심 수정 이력

1. `chi_j` convention을 재고정했다. Ch.1에서는 `chi_j`를 transfer coefficient `beta_j`와 동일시하지 않고, directionless mobility acceleration을 주는 scalar sensitivity로 둔다.
2. effective barrier를 step-function처럼 처리하지 않았다. `Delta G_eff = G - chi_j A_j`는 continuous linearized barrier lowering이며, Marcus small-driving-force bound 안에서만 쓴다.
3. `Heaviside H(L-L_min)` 표기를 제거하고, `L in [L_min, infinity)` 정의역과 lower-limit integral로 support를 표현했다.
4. single-mode spectrum에서 amplitude-less `A_L=delta(...)`를 쓰지 않고, `A_L(L)=Theta_0 delta(L-L*)` 구조로 amplitude를 보존했다.
5. Eyring-corrected Arrhenius 보정 부호를 plus에서 minus로 고쳤다. 이 수정은 물리적 double counting 방지에 해당한다.
6. extraction order를 `OCV/GITT -> L -> chi_j -> Eyring corrected Delta H_a`로 재정렬했다. 따라서 `chi_j`와 `Delta H_a`가 서로 되먹이는 순환 구조가 제거됐다.
7. `0.2C anchor` 식에서 잘못된 step 참조를 수정했다.
8. placeholder bibliography와 process metadata를 Codex V4 TeX 본문에서 제거했다.
9. Chapter 6식 대형 피팅 실무 부록은 Chapter 1 본문에 과적층하지 않고, Chapter 1에는 필요한 최소 simple-fit 및 Plan B numeric appendix만 남겼다.

## 5. 남은 residual risk

| 항목 | 상태 | 이유 |
|---|---|---|
| Plan A Fredholm closure | BOUNDED | graphite 문제는 Volterra/self-consistent feedback이므로 Plan B direct grid 대비 검증 후에만 사용 가능 |
| `rho_G` 구체 분포 | 미확정 | 관측 tail에서 역산하면 비유일. 독립 근거 또는 forward-only 입력 필요 |
| equilibrium isotherm form | 데이터 의존 | logistic을 기본으로 두되, near-peak line-shape이 기각하면 bounded ansatz로만 확장 |
| 실제 parameter value | 데이터 필요 | 현재 문건은 이론/논리/근사식 완성본이며 fitting code나 numerical solver 구축물이 아님 |
| typesetting warnings | 비치명 | XeLaTeX 통과, hyperref/overfull/underfull/font warning만 잔류 |

## 6. Gate 결과

- 논리 gate: PASS with bounded residual risks.
- 전문 검수 coverage gate: PASS, 10 passes, missing=0.
- convention gate: PASS, `AL{9}`, `동일물`, `RB 재구성본`, `CHARTER`, `Heaviside`, `A_L=delta` 위험표현 없음.
- 수식/참조 gate: PASS, duplicate label/missing ref/missing cite/unused bib 모두 0.
- compile gate: PASS, 세부는 `PHASE_029_CH1_V4_VERIFICATION_RESULT.md`.

## 7. 다음 단계 조건

사용자 검토 후 Chapter 1을 baseline으로 확정하면 Chapter 2 계획서를 새로 작성한다. Chapter 2는 이 Chapter 1의 `V_n`, `xi_j`, `xi_eq`, `k_j`, `L`, `chi_j`, `Delta G_eff` convention을 그대로 받아 reversible heat 및 `dV/dT` 확장으로 진행해야 한다.
