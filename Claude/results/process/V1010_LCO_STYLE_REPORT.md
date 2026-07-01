# v1.0.10 Ch1 LCO 절 수식-주도 vs 줄글 — 종합 판정

> 3종(LS1 Sonnet5 map/center/hys·LO1 Opus electronic·LC1 Codex peak/decomp/code) 각 청크를 흑연 forward 수식-주도 예시 + 상시 SPEC(RB_CHARTER·HANDOVER_RB·v9 AUTHOR_BRIEF G-derive)과 대조. 원자료 `V1010_LCO_STYLE_draft_{LS1,LO1,LC1}.md`.

## 0. 요지
사용자 지적 **확증**: LCO 절이 부분적으로 줄글 위주다. 단 전부는 아니다 — **진짜 새 물리(전자 엔트로피 유도)는 수식-주도로 잘 썼으나, 흑연 forward 틀을 LCO에 재적용하는 절들(center·hys·peak·decomp·plug-in·MSMR)이 "같은 틀 그대로 적용/한 줄 더한다"식 줄글 결론으로 닫혀** 흑연 forward의 (a)출발→(b)연산→(c)중간식→(d)박스 밀도에 못 미친다. v3/v4의 줄글을 v6로 올리며 수식-주도로 해소한 표준(그리고 v9 AUTHOR_BRIEF의 "모든 추가 식 단계 유도·점프 금지·이 문건으로 LCO ∂U/∂T 산출 가능")이 **LCO 재적용 절에는 적용되지 않았다.**

## 1. 줄글 회귀 확정 (수식화 대상, v1.0.11)
| 절 | 줄 | 등급 | 산문화된 물리 | 필요한 수식 사슬 |
|---|---|---|---|---|
| sec:lco-center | 470-513 | HIGH×2 | 전극무관 논증 단정 비약(L471-476)·∂U_j/∂T 미분이 Gibbs 항등식 다리 없이 괄호 전보체(L477-482) | ΔG=−sFU→∂U/∂T=ΔS/F 다리 문장 + (a→d) |
| sec:lco-hys | 684-708 | HIGH×3 | order-disorder·MIT·도핑 "같은 정규용액 틀 그대로 적용" 서술 3회, Ω_j(0.47/1.49) spinodal 대입 중간식 전무 | 흑연 sec:hys처럼 μ(θ)→g″→spinodal→ΔU_hys를 LCO Ω_j로 대입한 중간식 |
| sec:lco-peak | 1204-1216 | Major(★최약) | "평형 peak 식 전극무관 적용"·T1/T2/T3 위치 줄글 열거, LCO 3전이 합산 peak 박스식 없음 | ξ_eq,j→dξ/dV→ΣQ_j peak_shape→center/height/area 박스(j∈{T1,T2,T3}) |
| sec:lco-decomp | 1690-1724 | Moderate | 분해 박스는 있으나 config 슬롯=ΔS⁰_j·무이중계산·직교가산이 줄글 검산 | Z=Z_config·Z_elec→슬롯 정의→이중계산 금지식 박스 |
| 전자항 plug-in | 1729-1765 | Major | "T1 ΔS_rxn에 몰당 전자항 더하는 한 줄" 결론 | x=x(ξ_eq,1(V))→ΔS_e,1(V,T)→ΔS_rxn,1(V,T)→U_1(T)→dQ/dV forward 사슬 |
| MSMR 동형 | 1741-1753 | Moderate | 대응표(X_j↔Q_j 등)는 좋으나 MSMR→ξ_eq,j→eqpeak 변환 사슬 미폐쇄 | MSMR 식→정규화→대응대입(f=−σ_d)→ξ_eq,j→peak 박스 |

## 2. 정상 수식-주도 (과적발 방지 — 손대지 말 것)
- **sec:lco-map**(L295-349): 도입·매핑 절 성격, 흑연 대응 절과 밀도 대칭. 정상(도입은 본래 서사).
- **sec:lco-Se**(L953-1067): Fermi-Dirac→Sommerfeld **완전 유도** + 이중경로 교차검증. 흑연보다 식 밀도 높음.
- **sec:lco-gate**(L1068-1096): 게이트식은 모델 가정(문헌 연속곡선 부재로 유도 불가·정직 선언)이나 이후 ΔS_e 유도는 완전 수식 사슬.
- N7-N9 흑연 forward 본체: 수식-주도.

## 3. 판정
- **혼합** — 전자 엔트로피 유도(신규 물리)는 수식-주도, LCO 재적용 절(center·hys·peak·decomp·plug-in·MSMR)은 줄글 결론. **G-derive 위반은 후자 6개 지점**.
- 근본 원인: LCO 재적용 절을 "기존 식 그대로 적용"으로 서사 처리 → 흑연 forward의 LCO-특화 수식 사슬(같은 식을 LCO 파라미터·3전이로 재전개)이 빠짐. v9 AUTHOR_BRIEF의 G-derive·G-usable("이 문건으로 LCO ∂U/∂T·세 봉우리 산출 가능") 요구 미충족.

## 4. v1.0.11 수식화 방향 (물리 불변·전개만 수식-주도로)
각 절에 흑연 forward 패턴대로 LCO-특화 (a)→(b)→(c)→(d) 수식 사슬 추가(위 표 "필요한 수식 사슬"). ★물리·결과식·부호 불변(전개 형식만 줄글→수식). 전자 엔트로피·gate·map은 유지.
