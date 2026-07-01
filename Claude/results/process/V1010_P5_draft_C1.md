# Anode_Fit v1.0.10 P5 감사 드래프트 C1

조: A조(code↔Ch1 상호충실도)  
역할: 감사 의견만. 코드/문건 정정 없음.  
대상: `Anode_Fit_v1.0.10.py` ↔ `graphite_ica_ch1_v1.0.10.tex` 양방향 식·심볼 충실도.

## 0. 실제 확인 범위

- base 프롬프트: `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/p5_audit_base.txt` 19줄 전문.
- 프로젝트 지침: `CLAUDE.md` 전문, `Codex/AGENTS.md` 전문. 루트 `AGENTS.md`는 없음.
- 코드: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` 도구 출력 기준 1-849행 전문.
- Ch1: `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` 도구 출력 기준 1-1932행 전문.
- Ch2: `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` 도구 출력 기준 1-750행 전문.
- 앵커 결과: `V1010_P1_code-audit_RESULT.md` 1-445행, `V1010_P2_ch1_RESULT.md` 1-83행, `V1010_P3_ch2_RESULT.md` 1-54행, `V1010_P4_code-revision_RESULT.md` 1-58행. P1 병렬 출력 중 생략 의심 구간은 191-445행을 별도 재독해 보완했다.

분류 규약: `[확정]` = 코드 줄과 tex 줄/식이 직접 대조됨. `[근거 미발견]` = 요구된 독립 구현 또는 명시 근거를 찾지 못함. `[추정]` = 근거가 있으나 직접 증명은 아님. `[미검증]` = 이번 C1 범위에서 실행/외부 대조하지 않음.

## 1. 요약 판정

흑연 음극 핵심 spine은 대체로 1:1 정합이다. `func_U_j`, `func_ksi_eq`, `func_w/_width`, `func_dU_hys/func_U_branch`, `func_chi_d`, `func_L_q/_resolve_lag_length`, `_causal_lowpass`, `dqdv` 합산은 Ch1의 N1-N9 식과 양방향으로 맞는다.

확정 갭은 7건이다. 최중대 갭은 LCO 쪽이다. Ch1은 `LCO_STAGING_LIT`와 T1/T2/T3 물리 전이표 및 `x_MIT≈0.85`를 제시하지만, 현재 코드는 `LCO_MSMR_LIT` tier-C 시연값으로 3.930/3.880/4.050 V와 `x_MIT=0.50`을 쓴다. 또한 코드의 LCO 전자항 seam은 `x_center`와 `T_ref=298.15`로 동결되어 Ch1의 전압격자 `x↔ξ_eq(V)` 게이트 및 다온도 `T^2` 곡률을 아직 구현하지 않는다.

## 2. Ch1 → 코드 매핑

| Ch1 항목 | Ch1 위치 | 코드 위치 | 판정 |
|---|---:|---:|---|
| 분극 `V_n=V_app-σ_d|I|R_n` | eq:vn, Ch1 363-369 | code 430 | [확정] 식 정합. 단 Ch1 `tab:nodemap`의 코드 줄 `L408`은 현재 코드 기준 stale. |
| `U_j(T)=(-ΔH+TΔS)/F` | eq:Uj, Ch1 447-451 | code 78-79, 382, 456 | [확정] 식·부호 정합. |
| 히스 gap `ΔU_hys` | eq:dUhys, Ch1 610-615 | code 133-140 | [확정] 식 정합. |
| 분기 중심 `U_j^d` | eq:Ubranch, Ch1 630-634 | code 143-148, 469-470 | [확정] 식 정합. |
| 폭 `w_j=n_jRT/F` | eq:wbase, Ch1 714-721 | code 74-75, 294-306 | [확정] 식 정합. `n` 우선으로 `w` 폴백 inert 가능성은 Ch1 1250-1252와 코드 296-306이 정합. |
| `ξ_eq` logistic | eq:xieq, Ch1 770-780 | code 94-97, 477 | [확정] 식·방향 부호 정합. |
| 평형 peak | eq:eqpeak, Ch1 1183-1191 | code 386-388, 486 | [확정] 식 정합. |
| broadening/ensemble | eq:ensavg, Ch1 1277-1292 | 코드 명시 모델 없음 | [확정] 갭 아님. Ch1 1838이 "모델 항 0"으로 명시하고, 코드도 현상학적 `w`와 `L_V`만 둔다. |
| `χ_d` | eq:chid, Ch1 1440-1445 | code 158-163, 309-312 | [확정] 식 정합. |
| `ΔH_a^eff` | eq:dHeff, Ch1 1450-1454 | code 152-155, 315-322 | [확정] 식 정합. |
| `L_q`, `L_V` | eq:Lqfull/eq:LV, Ch1 1467-1481 | code 100-107, 325-369 | [확정] 로그식·단위·부호 정합. |
| 인과 꼬리·충전 역전 | eq:peakshape/eq:reversal, Ch1 1565-1582, 1595-1602 | code 492-497 | [확정] 식 정합. |
| MSMR 동형 | eq:msmr, Ch1 1735-1748 | code 616-618, 641-646 | [확정] 구조 매핑 자체는 정합. |
| 전자 엔트로피 게이트 | eq:dSegate, Ch1 1081-1087 | code 170-185 | [확정/부분] `func_dSe_molar`의 몰당 닫힌식, leading `-`, `÷EV_TO_J`, `π²/3`, `R*kB*T` 계수는 정합. 통합 경로의 `x`·`T` 처리는 아래 갭 G5/G6. |
| 직접 엔트로피 | eq:Sedirect, Ch1 980-985 | code 170-185 | [근거 미발견/비결함] 독립 적분 경로 코드는 없다. 다만 eq:Sedirect는 계수 검증용 유도이고, 런타임은 그 결과 계수 `π²/3`을 `func_dSe_molar`에 사용한다. 별도 구현이 필요하다는 문장 근거는 찾지 못했다. |

## 3. 코드 → Ch1 매핑

| 코드 심볼 | 코드 위치 | Ch1 근거 | 판정 |
|---|---:|---:|---|
| `func_w` | 74-75 | eq:wbase 714-721 | [확정] |
| `func_U_j` | 78-79 | eq:Uj 447-451 | [확정] |
| `func_ksi_eq` | 94-97 | eq:xieq 770-780 | [확정] |
| `func_L_q` | 100-107 | eq:Lqfull 1467-1474 | [확정] |
| `_resolve_lag_length` | 325-369 | eq:Acut, eq:chid, eq:dHeff, eq:LV 1427-1481 | [확정] |
| `_causal_lowpass` | 110-128 | eq:lowpass 1525-1530 | [확정] |
| `func_dSe_molar` | 170-185 | eq:dSemolar/gunit/dSegate 1017-1033, 1081-1087 | [확정] 함수 단위 정합. |
| `_effective_dS_rxn` seam | 533-542, 655-671 | Ch1 1718-1729, sec:lco-code 1735-1760 | [확정/부분] seam 개념은 정합. 현재 구현은 `x_center`, `T_ref` 동결 근사라 Ch1의 full x/T 게이트와는 불일치. |
| `LCOCathodeDQDV` | 641-671 | Ch1 sec:lco-map 295-343, sec:lco-code 1735-1760 | [확정/부분] 상속·부호 비반전·MSMR 동형은 정합. 데이터셋 이름·전이 구성·전자항 좌표는 아래 갭. |
| `entropy_coefficient`, `reversible_heat`, `irreversible_heat` | 544-596 | Ch2 eq:weighted/eq:qrev; Ch1 직접 대상 아님 | [확정] A조 Ch1 갭으로 보지 않음. Ch2 근거는 존재한다. |

## 4. 확정 갭

### G1. Ch1 본문 코드 파일명이 구버전으로 남아 있음

- 위치: Ch1 133행 `Anode_Fit_v11_final.py`.
- 코드/현 상태: 실제 대상은 `Anode_Fit_v1.0.10.py`; Ch1 헤더 2-3행과 date 100행은 1.0.10 matched라고 말한다.
- 문제: 같은 Ch1 내부에서 파일명이 충돌한다. 독자가 어느 코드와 맞대야 하는지 혼란을 준다.
- 맞는 형태: Ch1 133행을 `Anode_Fit_v1.0.10.py` 또는 코드명 없는 `Anode_Fit 1.0.10`으로 맞춤.

### G2. LCO 데이터셋 식별자 불일치

- 위치: Ch1 312, 322, 1750, 1844행 `LCO_STAGING_LIT`.
- 코드: 621행 `LCO_MSMR_LIT`.
- 문제: Ch1이 지시하는 식별자가 코드에 없다. 코드→Ch1과 Ch1→코드 양방향 심볼 매핑에서 직접 실패한다.
- 맞는 형태: 문건 식별자를 `LCO_MSMR_LIT`로 정정하거나, 코드에 alias를 둘지 master가 결정. 현재 코드 명명 철학(MSMR 동형)을 따르면 문건을 `LCO_MSMR_LIT`로 맞추는 편이 자연스럽다.

### G3. LCO 전이 인벤토리와 전위 초기값 불일치

- 위치: Ch1 312-316, table 330-334, 1202-1203행. Ch1은 T1 `~3.90`, T2 `~4.05`, T3 `~4.17--4.20`, optional T4 `~4.55`를 말한다.
- 코드: `LCO_MSMR_LIT` 621-638행은 3.930, 3.880(electronic), 4.050 V 세 항목이며, 4.17--4.20 V T3가 없다.
- 문제: Ch1의 세 전이와 코드의 세 전이가 1:1 대응하지 않는다. 코드에는 3.93 V 주 평탄역과 3.88 V electronic 전이가 함께 있고, Ch1의 4.17--4.20 V order--disorder b 전이는 구현/시연 데이터에 없다.
- 맞는 형태: 둘 중 하나로 정리 필요. (a) Ch1 표를 코드의 tier-C 시연 데이터셋 3.930/3.880/4.050에 맞추고 4.17--4.20은 미구현/후속으로 라벨, 또는 (b) 코드 `LCO_MSMR_LIT`에 Ch1 T1/T2/T3 물리 전이를 반영. 현재 P4 결과 45-48행도 LCO 피크가 3.92/4.04 근방임을 보고하므로, 현 코드 기준으로는 Ch1 표가 과잉/불일치다.

### G4. `x_MIT` anchor 불일치

- 위치: Ch1 eq:ggate 1069-1071행, 설명 1098행: `x_MIT≈0.85`, MIT 범위 `x≈0.75--0.94`.
- 코드: 631-632행 `x_center=0.50`, `x_MIT=0.50`, `dx_MIT=0.05`.
- P4 앵커: `V1010_P4_code-revision_RESULT.md` 53-55행이 `x_MIT=0.50 tier-C placeholder`와 Ch1 anchor 불일치를 P5 이월로 명시.
- 문제: 코드의 전자항 게이트 중심이 Ch1 물리 anchor와 다르다.
- 맞는 형태: 현 코드가 placeholder라면 코드 주석뿐 아니라 Ch1에도 "현재 코드 tier-C 시연은 0.50, 물리 anchor는 0.85"를 명시하거나, 코드 기본값을 물리 anchor로 갱신.

### G5. Ch1의 `x↔ξ_eq(V)` 전압격자 매핑이 코드에 미구현

- 위치: Ch1 1724-1729행은 전자항 `ΔS_e(x,T)`를 dqdv 전압 격자에 잇기 위해 `x=x(ξ_eq,1(V))` 매핑이 필요하다고 말한다.
- 코드: 667-670행은 `func_dSe_molar(tr['x_center'], T_ref, ...)`만 호출한다. `V_work`, `ξ_eq`, `T_work` 배열과 연결하지 않는다.
- 문제: `func_dSe_molar` 함수 자체는 있지만, 모델 경로에서는 전이 진행률/전압별 electronic gate가 아니라 단일 중심값 오프셋만 들어간다.
- 맞는 형태: P4의 단일-기준 근사를 유지할 경우 Ch1의 P4 예고 문단을 "미구현/후속 round-trip"으로 낮춰 라벨링. full 구현을 목표로 하면 `x↔ξ_eq(V)` 평가 경로를 코드에 추가.

### G6. 다온도 전자항 `T` 스케일과 `eq:U1T2` 곡률 미구현

- 위치: Ch1 eq:dSegate 1081-1087행은 `ΔS_e∝T`, eq:U1T2 1055-1056행은 `a_e/(2F)`의 `T^2` 누적을 제시한다.
- 코드: 659-664행 docstring이 `T_ref=298.15` 동결과 `eq:U1T2` 다온도 round-trip 피팅 과제 분리를 명시하고, 668-670행 실제 호출도 `T_ref` 고정이다.
- P4 앵커: P4 결과 40행이 factor-2 문제를 `T_ref` 동결로 해소했고, 55행이 `다온도 T² 곡률` 미구현을 P5 이월로 남겼다.
- 문제: 단일온도/기준온도에서는 의도적 근사이나, Ch1의 full formula가 코드 1.0.10 런타임에 구현됐다고 읽히면 과장이다.
- 맞는 형태: Ch1과 코드 주석 모두 "현재 1.0.10은 T_ref 동결 근사, `eq:U1T2`는 다온도 round-trip 후속"으로 같은 라벨 유지. 코드 구현을 확장할 경우 factor-2 회귀 방지 gate 필요.

### G7. Ch1 `tab:nodemap` 코드 줄 번호가 P4 이후 stale

- 위치: Ch1 1832행 `\code{dqdv} L408`.
- 코드: 현재 분극 줄은 430행 `V_n = V_in - sigma_d * I_abs * self.Rn`.
- 문제: P4가 코드 앞부분에 LCO/발열 함수를 추가하면서 줄 번호가 이동했지만 Ch1 nodemap은 P2 당시 줄 번호를 유지한다. 식 자체는 맞지만 "코드 줄 근거" 요구에는 실패한다.
- 맞는 형태: `tab:nodemap`의 코드 줄 근거를 현재 코드 기준으로 재산정하거나, 줄 번호 대신 심볼+식별 가능한 코드 fragment 중심으로 표기.

## 5. 갭 아님으로 판정한 항목

- `eq:Sedirect`: 별도 적분 코드가 없지만, Ch1에서는 직접 엔트로피 유도로 `π²/3` 계수를 검증하는 역할이다. 코드가 `func_dSe_molar`에서 해당 계수를 쓰므로 계산 결과 계수는 반영됨. standalone 함수 부재를 결함으로 확정하지 않는다.
- broadening `eq:ensavg`: Ch1이 `모델 항 0`, forward-only, 역산 금지를 명시한다. 코드가 별도 ensemble convolution을 두지 않는 것은 문건과 충돌하지 않는다.
- Ch2 발열 함수들: `entropy_coefficient`, `reversible_heat`, `irreversible_heat`는 Ch1이 아니라 Ch2 근거 항목이다. A조 Ch1 상호충실도 결함으로 계산하지 않는다.
- `func_U_j_hys` 미호출: P1에서 이미 死코드/원형보존으로 확정된 사항이고, 현재 Ch1은 실제 경로를 `func_dU_hys`/`func_U_branch`로 매핑한다. A조 신규 갭 아님.

## 6. 3대 무결 최종 확인

- 물리 배경 정확: 흑연 spine과 LCO MSMR 동형의 큰 골격은 물리식과 코드가 정합한다. 다만 LCO 전이표, `x_MIT`, x/T 전자항 처리의 현재 상태는 "물리 anchor"와 "tier-C 시연 코드"를 명시 분리해야 한다.
- 코드 정확: 현재 코드의 흑연 주요 식과 LCO/발열 추가 함수는 자기 주석과 P4 결과 기준으로 의도대로 구현되어 있다. G5/G6은 코드 버그라기보다 Ch1 full formula 대비 미구현/근사 범위 문제다.
- 사용자 의도 반영: P4 이월 4건 중 A조와 직접 관련되는 `x_MIT tier-C`, `다온도 T² 곡률`, `LCO 시연 파라미터`가 모두 실제로 남아 있다. 비가역 3분해는 Ch2/code 영역이라 C1 핵심 갭에는 넣지 않았다.

## 7. master 정정 목록

1. Ch1 133행의 `Anode_Fit_v11_final.py`를 현행 `Anode_Fit_v1.0.10.py` 계열 명칭으로 정정.
2. Ch1의 `LCO_STAGING_LIT` 4곳(312, 322, 1750, 1844행)을 코드의 `LCO_MSMR_LIT`와 맞춤.
3. Ch1 LCO table/본문의 T1/T2/T3 전이표를 현 코드 시연값과 물리 target 중 어느 쪽이 정본인지 결정해 라벨 분리. 현 코드 기준이면 4.17--4.20 V T3는 "미구현/후속"으로 표시.
4. Ch1 `x_MIT≈0.85`와 코드 `x_MIT=0.50`의 관계를 명시. 코드가 placeholder면 문건에 tier-C placeholder 차이를 쓰고, 코드가 물리 기본값이어야 하면 코드 값을 갱신.
5. Ch1 1724-1729행의 `x↔ξ_eq(V)` 매핑을 "현재 코드 미구현"으로 표시하거나 코드에 실제 전압격자 매핑을 구현.
6. Ch1 `eq:U1T2`/`ΔS_e∝T`는 현재 코드가 `T_ref` 동결 근사임을 같은 문단에서 명시. full 다온도 구현 전에는 "구현 완료"로 읽히지 않게 라벨링.
7. Ch1 `tab:nodemap`의 코드 줄 번호를 현재 코드 기준으로 갱신하거나 symbol/fragment 기반으로 바꿔 줄 번호 drift를 제거.

## 8. 4-tier 요약

- [확정] 흑연 핵심식 N1-N9의 수식-코드 매핑은 정합.
- [확정] LCO 데이터셋 이름, LCO 전이 인벤토리, `x_MIT`, electronic gate의 x/T 통합 경로, nodemap 줄 번호는 불일치.
- [근거 미발견] `eq:Sedirect`를 별도 runtime 함수로 구현해야 한다는 문건 근거.
- [추정] LCO 3.930/3.880/4.050 구성은 P4의 tier-C 시연 안정성을 우선한 배치로 보인다. 다만 Ch1 물리표와 혼재되면 독자에게는 정본처럼 읽힌다.
- [미검증] 외부 문헌 DOI/수치 anchor 자체의 최신성·원문 재대조. 이번 C1은 코드↔Ch1 내부 충실도 감사로 제한했다.

## 9. 5줄 요약

조: A조(code↔Ch1 상호충실도), C1.  
확정 갭 수: 7건.  
최중대 갭: LCO 코드 `LCO_MSMR_LIT` tier-C 시연값(3.930/3.880/4.050, `x_MIT=0.50`)과 Ch1 물리표(`LCO_STAGING_LIT`, T3 4.17--4.20, `x_MIT≈0.85`)의 정본 혼재.  
정정 목록: 코드 파일명, LCO 식별자, LCO 전이표, `x_MIT`, `x↔ξ_eq(V)` 구현 라벨, `T_ref`/`eq:U1T2` 라벨, nodemap 줄번호.  
리스크: 흑연 spine은 안정하지만 LCO 전자항을 "구현 완료"로 읽으면 다온도/round-trip 단계에서 factor-2·anchor 혼동이 재발할 수 있다.
