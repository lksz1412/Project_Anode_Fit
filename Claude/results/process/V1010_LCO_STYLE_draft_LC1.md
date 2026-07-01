# Anode_Fit v1.0.10 Ch1 LCO 스타일 검수 LC1

## 0. 검수 범위와 판정 기준

- ID: LC1
- base prompt: `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/lco_style_base.txt` 전문 정독 완료.
- 대상 원문: `D:/Projects/Project_Anode_Fit/Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex`
- 담당 chunk 전문 확인: L1204-1689, L1690-1739, L1740-1765.
- 맥락 확인: 흑연 forward 기준 L351-469, L1168-1203, L1393-1530; LCO center/전자항/gate L470-560, L953-1203; LCO 전이표 L295-345.
- 검수 범위: 검수 의견만. 코드/TeX 본문 수정 없음.

담당 chunk 최종 판정: **혼합**. 앞선 LCO 전자항 유도(`sec:lco-Se`, `sec:lco-gate`)와 흑연 forward 본체(N6-N9)는 수식-주도 구조가 강하지만, LC1 담당 LCO 결론부인 `sec:lco-peak`, `sec:lco-decomp`, `sec:lco-code`는 상당 부분이 "앞 식을 그대로 적용한다/더한다/교체한다"는 결론 문단으로 닫혀 있어 흑연 forward 절의 `(a) 출발 -> (b) 연산 -> (c) 중간식 -> (d) 박스` 밀도에는 못 미친다.

## 1. 지적 사항

### [Major] LCO 세 봉우리 절이 `eq:eqpeak` 결과를 가져오지만, LCO 세 전이 합성식으로 재전개하지 않는다

- 위치: `sec:lco-peak`, L1204-1216.
- 산문화된 물리: L1205-1206은 "평형 peak 식은 전극을 가리지 않으므로 LCO에도 그대로 적용된다", "위치/순높이/면적이 표의 LCO 전이로 읽힌다"고 결론을 말한다. L1207-1208은 T1/T2/T3 전위 위치를 줄글로 열거하고, L1212-1216은 T1 온도 이동률이 전자항 관측 신호라고 설명한다.
- 문제: LCO 하프셀의 세 봉우리가 실제 forward `dQ/dV`에서 어떻게 한 식으로 만들어지는지, 즉 `j in {T1,T2,T3}`의 logistic, 미분, 용량가중 합, peak center/height/area 추출이 LCO 전용 박스식으로 닫히지 않는다. 결과적으로 핵심 질문인 "세 봉우리 dQ/dV가 수식 사슬인가, 줄글 단정인가"에 대해서는 **줄글 결론에 가깝다**.
- 흑연 forward라면 필요한 수식 사슬:
  - (a) 출발: `\xi_{\eq,j}^\mathrm{LCO}(V,T)=1/(1+\exp[-\sigma_d(V-U_j^d(T))/w_j])`, `j=T1,T2,T3`.
  - (b) 연산: `\dd\xi_{\eq,j}/\dd V=\sigma_d\xi_{\eq,j}(1-\xi_{\eq,j})/w_j`.
  - (c) 중간식: `(dQ/dV)^\mathrm{LCO}=C_\bg+\sum_{j\in\{T1,T2,T3\}}Q_j\xi_{\eq,j}(1-\xi_{\eq,j})/w_j`.
  - (d) 박스: `V_{\peak,j}=U_j^d(T)`, `H_j=Q_j/(4w_j)`, `A_j=Q_j`, plus `\partial_T U_1=\Delta S_{\rxn,1}^\mathrm{cat}/F` and electronic `\propto T` signal.
- v9 AUTHOR_BRIEF/SPEC 근거: base prompt의 "수식 흐름 보존", "유도 중간단계 전부", "수식 주도", "흑연 forward 절처럼 (a)->(b)->(c)->(d)" 기준. 흑연 기준은 L1173-1199에서 보존식 미분, logistic 미분, peak 박스, 위치/높이/면적을 한 사슬로 닫는다.

### [Moderate] `ΔS_rxn=config+vib+electronic` 분해는 박스식은 있으나, config 슬롯과 무이중계산 규칙이 줄글 검산에 머문다

- 위치: `sec:lco-decomp`, L1690-1724.
- 산문화된 물리: L1694-1698에 boxed 분해식은 있다. 그러나 L1702-1706의 "logistic이 자동 생성한다", "중심 표준값만 넣는다", L1707-1715의 "직교 자유도라 더해도 된다/초과하지 않는다"는 핵심 판단이 대부분 설명문이다. `Z=Z_config*Z_elec`, `S=S_config+S_elec`는 L1709-1710에 나오지만, 그 다음이 slot 정의와 중복 제거 박스식으로 이어지지 않는다.
- 문제: 현재 독자는 "config 중심 표준값"과 "봉우리 내부 조성 의존"의 분리 규칙을 문장으로 받아들여야 한다. `\Delta S_j^\mathrm{config}`가 정확히 `\Delta S_j^0`인지, logistic 내부의 `R\ln[(1-\xi)/\xi]`는 어느 식의 어느 항으로 이미 계산되는지, 따라서 forward 슬롯에는 어떤 항만 남는지가 식 사슬로 잠기지 않는다.
- 흑연 forward라면 필요한 수식 사슬:
  - (a) 출발: `S_\mathrm{mix}=-R[\xi\ln\xi+(1-\xi)\ln(1-\xi)]` 또는 기존 logistic 유도식 참조.
  - (b) 연산: `\partial S_\mathrm{mix}/\partial \xi=R\ln[(1-\xi)/\xi]`가 peak 내부 조성 의존을 이미 만들었음을 표시.
  - (c) 중간식: `\Delta S_{\rxn,j}^\mathrm{cat}(x,T)=\Delta S_j^0+\Delta S_j^\mathrm{vib}+\Delta S_{e,j}^\mathrm{mol}(x,T)` with `\Delta S_j^\mathrm{config,slot}\equiv\Delta S_j^0`.
  - (d) 박스: `\Delta S_j^\mathrm{slot}\neq \Delta S_j^0+R\ln[(1-\xi)/\xi]` 같은 이중계산 금지식을 명시.
- v9 AUTHOR_BRIEF/SPEC 근거: G-derive 위반 위험. 핵심 물리인 "가산성"과 "무이중계산"이 결론 문장 중심이며, 흑연 L523-553의 `g(\xi)->g''(\xi)->spinodal`처럼 중간식으로 잠기는 구조가 약하다.

### [Major] 전자항 plug-in은 `한 줄 더한다`로 끝나며, `x(ξ_eq(V)) -> ΔS_e -> U_j(T) -> dQ/dV` 연결식이 담당 chunk 안에서 닫히지 않는다

- 위치: `sec:lco-decomp` L1729-1738, `sec:lco-code` L1740-1765.
- 산문화된 물리: L1730-1734는 전자항이 조성 `x`의 함수이고 전압 격자에서는 `x<->ξ_eq,1(V)` 매핑이 필요하다고 설명한다. L1757-1761은 T1의 `ΔS_rxn` 평가에 몰당 전자항을 "더하는 한 줄"이라고 쓴다.
- 문제: 앞선 L953-1096에 `ΔS_e` 유도와 몰당 환산은 충분히 있으나, 담당 chunk의 코드 일반화 절에서는 plug-in 경로가 식으로 재조립되지 않는다. 특히 `x=x(\xi_{\eq,1}(V))`, `\Delta S_{\rxn,1}^\mathrm{cat}(V,T)`, `U_1(T,V?)`, `\xi_{\eq,1}(V,T)`, `dQ/dV`로 이어지는 forward 사슬이 없다. "전자항 plug-in"이 가장 구현 민감한 자리인데 줄글 설계 항목으로 남아 있다.
- 흑연 forward라면 필요한 수식 사슬:
  - (a) 출발: `x_1(V)=x_\mathrm{start}-\Delta x_1\,\xi_{\eq,1}(V)` 또는 문건이 채택한 조성-진행률 매핑을 정의.
  - (b) 연산: `\Delta S_{e,1}^\mathrm{mol}(V,T)=N_A(\pi^2/3)k_B^2T\,\partial_x g(E_F,x_1(V))`.
  - (c) 중간식: `\Delta S_{\rxn,1}^\mathrm{cat}(V,T)=\Delta S_1^0+\Delta S_1^\mathrm{vib}+\Delta S_{e,1}^\mathrm{mol}(V,T)`.
  - (d) 박스: `U_1(T)=U_1(T_0)+\int_{T_0}^{T}\Delta S_{\rxn,1}^\mathrm{cat}(V,T')/F\,dT'`, then `dQ/dV` T1 term.
- v9 AUTHOR_BRIEF/SPEC 근거: base prompt가 특히 "전자항 plug-in이 수식 사슬(a->b->c->d)로 전개되나 줄글 단정인가"를 물었다. 현재 L1757-1761은 단위 주의는 강하지만 plug-in 자체는 "더하는 한 줄"이라는 산문 결론이다.

### [Moderate] MSMR 동형성은 대응표는 좋지만, `MSMR -> transition-logistic -> eqpeak` 변환이 완전한 수식 사슬은 아니다

- 위치: `sec:lco-code`, L1741-1753.
- 산문화된 물리: L1743-1746에 MSMR 식이 있고, L1747-1752에서 `X_j<->Q_j`, `U_j^0<->U_j^d`, `ω_j<->w_j`, `f<->-σ_d`를 설명한다. 그러나 변환 뒤의 LCO logistic 식과 그 미분 peak 식은 별도 박스로 쓰지 않는다.
- 정상 근거: 이 부분은 완전한 줄글은 아니다. `eq:msmr`가 있고 부호 대응 `f=-σ_d`도 L1749-1752에서 논리적으로 설명된다.
- 남는 결함: 흑연 forward 기준이라면 MSMR 식을 바로 `\xi_{\eq,j}` 꼴로 변환하고, 다시 `eq:eqpeak`의 LCO 합산식으로 이어야 한다. 지금은 "구조가 동형"이라는 판단을 독자가 받아들인 뒤 앞절을 떠올려야 한다.
- 흑연 forward라면 필요한 수식 사슬:
  - (a) MSMR: `x_j=X_j/[1+\exp(f(U-U_j^0)/\omega_j)]`.
  - (b) 정규화: `\xi_j=x_j/X_j`.
  - (c) 대응 대입: `f=-σ_d`, `U->V`, `U_j^0->U_j^d`, `ω_j->w_j`.
  - (d) 박스: `\xi_{\eq,j}=1/[1+\exp[-σ_d(V-U_j^d)/w_j]] -> (dQ/dV)_j`.
- v9 AUTHOR_BRIEF/SPEC 근거: "보편식 먼저"와 "계산편의 비약 배제". 현재는 보편 MSMR 식 다음에 대응을 문장으로 준다.

## 2. Refute / 과적발 방지

- `sec:lco-Se` L953-1066은 정상 수식-주도에 가깝다. Fermi--Dirac 분포 L956-959, Sommerfeld/비열 경로 L964-978, 직접 엔트로피 경로 L980-990, `ΔS_e` 박스 L1013-1017, 몰당 환산 L1022-1027, `T^2` 적분 박스 L1059-1061이 이어진다. 이 구간은 LC1 담당 chunk의 결함 근거로 삼으면 과적발이다.
- `sec:lco-gate` L1068-1096도 정상에 가깝다. 문헌 gap 선언 L1069-1072, logistic gate 박스 L1073-1077, logistic 미분 L1082-1085, `ΔS_e` 닫힌식 L1086-1091이 있다. "게이트" 자체는 수식 사슬로 닫힌다.
- 담당 chunk 내부 L1393-1660의 N7/N8/N9 흑연 forward 본체도 수식-주도다. 예: `L_q` 유도 L1400-1414, `L_q` 평가와 `L_V` L1461-1487, 기억 꼬리 L1511-1535, peak shape/분기 L1564-1588, 합산식 L1649-1658. 다만 이는 LCO 세 봉우리 자체의 신설 설명이라기보다 기존 forward 본체다.
- 따라서 LC1 판단은 "LCO 관련 앞선 유도 전체가 줄글"이 아니다. 결함은 LCO 결론부가 앞선 수식 사슬을 다시 LCO 세 전이/분해/코드 plug-in 형태로 재조립하지 않고 산문 결론으로 닫는 점이다.

## 3. 가장 약한 1곳

가장 약한 곳: **`sec:lco-peak` L1204-1216**.

이유: 이 절은 제목상 "LCO dQ/dV peak — 양극 영역의 세 봉우리"인데, 실제로는 L1205-1208의 짧은 문장으로 `eq:eqpeak` 적용과 T1/T2/T3 위치 열거를 끝낸다. LCO 세 전이의 `ξ_eq,j -> dξ/dV -> ΣQ_j peak_shape_j -> center/height/area -> T1 전자항 온도 이동`이 한 번에 보이는 박스식이 없다. `sec:lco-decomp`와 `sec:lco-code`에는 적어도 boxed 분해식과 MSMR 식이 있지만, 이 절은 거의 전부 참조+줄글이다.

## 4. 담당 chunk 5줄 요약

1. LC1 담당 chunk 판정은 **혼합**: 기존 흑연 forward/N7-N9와 앞선 LCO 전자항 유도는 수식-주도이나, LCO 결론부는 산문 결론 비중이 높다.
2. 세 봉우리 절 L1204-1216은 `eq:eqpeak`을 참조할 뿐 LCO `T1/T2/T3` 합산 peak 식을 새로 닫지 않아 가장 약하다.
3. `ΔS_rxn=config+vib+electronic`은 boxed 식은 있으나 config 중심값/이중계산 금지/직교 가산성의 수식 잠금이 부족하다.
4. 전자항 plug-in은 단위 경고는 강하지만 `x(ξ_eq(V)) -> ΔS_e -> U(T) -> dQ/dV` forward 사슬이 담당 chunk 안에서 식으로 닫히지 않는다.
5. 빈 통과 불가 기준상 수정 후보는 L1204-1216에 LCO 세 전이 peak 박스식을 추가하고, L1729-1765에 전자항 plug-in 수식 사슬을 재조립하는 것이다.
