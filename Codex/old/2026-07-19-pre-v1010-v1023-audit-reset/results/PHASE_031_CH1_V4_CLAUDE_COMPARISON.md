# PHASE 031 - Chapter 1 V4 vs Claude Final Comparison

## 1. 비교 대상

| 구분 | 경로 | 행 수 | SHA256 |
|---|---|---:|---|
| Codex V4 | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v4.tex` | 945 | `C1607A7E101B1D3BA4BD4CDF9D88D0C8AEDAFADCEA6BBFF1E525EC540C876517` |
| Claude final | `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch1_rebuilt.tex` | 1627 | `4EB24D9C7C2080B5AEC556BE0E98C8E2E88923F28DC4DDBBDCD3E4CF82AE33AE` |

Claude final은 Chapter 1 본문 뒤에 `부록 B / 구 Chapter 6` 성격의 대형 fitting-practice appendix가 885행부터 1627행까지 붙어 있다. 따라서 비교는 “Chapter 1 theoretical background로서의 완결성”과 “추후 fitting methodology 후보”를 분리해서 보았다.

## 2. Claude final에서 흡수한 장점

| Claude 장점 | Codex V4 반영 방식 |
|---|---|
| 관찰에서 시작하는 narrative: 저온 긴 tail, 고온 짧은 tail | Codex V4 서문과 falsification 절에서 단일 인과 사슬로 유지 |
| logistic equilibrium, charge-balance root, internal electrode potential 구조 | Chapter 1의 무대 I/II로 정리 |
| effective barrier lowering와 relaxation length `L` 연결 | `Delta G_eff = G - chi_j A_j`, `L=|I|/(Q_cell k_j)`로 단계 전개 |
| barrier distribution -> relaxation-length spectrum | `rho_G(G)`에서 `A_L(L)`로 Jacobian 변환 유지 |
| Volterra/self-consistent feedback 문제 인식 | Plan B direct g-grid와 Plan A bounded auxiliary로 분리 |
| simple-fit approximation 필요성 | single-mode tail section에 `q_a`, `L`, `chi_j`, `Delta H_a` extraction order로 반영 |
| 반증 가능성 강조 | Arrhenius, potential-dependence, low-temperature line-shape, `rho_G` forward-only test로 정리 |

## 3. Claude final의 문제와 Codex V4 수정

| 문제 구분 | Claude final 상태 | Codex V4 처리 |
|---|---|---|
| 본문 메타데이터 | `RB 재구성본`, `RB plan`, `Author:`, `Date:`가 TeX 본문/제목부에 남음 | 모두 제거. 변경 이력은 phase report로 분리 |
| convention conflict | `chi_j`를 Ch.3 transfer coefficient `beta_j`와 동일물로 표현 | Ch.1에서는 동일시 금지. Ch.3에서 별도 kinetic model이 있을 때만 대응 검토 |
| old convention residue | `AL{9}` 사용 | Codex V4에는 없음 |
| step-function 오해 위험 | `Heaviside H(L-L_min)`로 support를 기술 | `L in [L_min, infinity)` 정의역 및 적분 하한으로 표현 |
| amplitude loss | single-mode에서 `A_L=delta(...)` 표현 | `A_L(L)=Theta_0 delta(L-L*)`로 amplitude 보존 |
| Eyring correction sign | `y(T)=ln(1/(LT))+chi_j A_j/(RT)` | minus sign으로 수정. 이유: `ln(1/L)` 안에 이미 `+chi A/RT` 포함 |
| extraction order circularity | `chi_j`와 Arrhenius 보정 순서가 문장상 되먹임 | `L -> chi_j -> corrected Eyring` 순서로 고정 |
| C-rate overclaim | C-rate 증가가 tail shortening으로 단순화되는 문맥 존재 | current prefactor, potential acceleration, apparent polarization, transport limitation 경쟁으로 표현 |
| TeX delimiter | `$L$$\to$`, `$R_n$$\cdot$`류 인접 math delimiter | Codex V4에서 제거, static scan `$$=0` |
| bibliography placeholder | 사용자 논문 및 refs 6/7 placeholder title 존재 | full bibliographic entries로 교체 |
| Chapter scope overload | 구 Chapter 6 fitting-practice 부록이 Chapter 1 뒤에 대량 흡수 | Codex V4는 Chapter 1 theoretical background + simple-fit + bounded numeric appendix까지만 유지 |

## 4. 정량 scan 비교

| Pattern | Codex V4 | Claude final | 판단 |
|---|---:|---:|---|
| `RB 재구성본` | 0 | 4 | Codex 개선 |
| `RB plan` | 0 | 1 | Codex 개선 |
| `Author:` | 0 | 1 | Codex 개선 |
| `Date:` | 0 | 1 | Codex 개선 |
| `동일물` | 0 | 2 | Codex 개선 |
| `AL{9}` | 0 | 2 | Codex 개선 |
| `Heaviside` | 0 | 2 | Codex 개선 |
| `H(L-L...)` | 0 | 4 | Codex 개선 |
| `A_L=\delta` | 0 | 3 | Codex 개선 |
| `CHARTER` | 0 | 1 | Codex 개선 |
| `$$` | 0 | 4 | Codex 개선 |
| placeholder bibliography strings | 0 | 3 | Codex 개선 |
| `ch6_` appendix labels | 0 | 137 | Codex는 Chapter 1 scope 유지 |

## 5. Codex V4가 남긴 한계

| 항목 | 이유 |
|---|---|
| Plan A closed-form | 사용자 논문 refs 6/7 방법론은 유용하지만 graphite Volterra feedback에서는 direct grid 대비 검증이 필요 |
| actual fitting value | 현재 산출물은 이론 배경과 근사식이지 실제 피팅 실행 결과가 아님 |
| `rho_G` 독립 입력 | 관측 꼬리에서 직접 역산하면 비유일이라 forward-only로 남김 |
| Chapter 6 appendix material | Claude appendix에는 좋은 실무 요소도 있으나 Chapter 1에는 과적층. 추후 별도 fitting methodology 문서에서 선별 흡수 가능 |

## 6. 결론

Codex V4가 현재 사용자 목표인 “논문/특허로 발전 가능한 Chapter 1 이론 배경, 학부생 수준으로 따라갈 수 있는 무비약 수식 전개, 자체 fitting approximation을 만들 수 있는 논리식”에 더 적합하다. Claude final의 후반 fitting-practice 부록은 별도 methodology chapter 또는 appendix 후보로 보관하고, Chapter 1 본문에는 그대로 합치지 않는 것이 맞다.
