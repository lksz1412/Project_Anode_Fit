# P4 Step2 — 검토1 (별도 세션 Opus, 적대적 교차검증) 결과

> 9 설계 드래프트(S1-3·O1-3·C1-3) vs 코드 703줄(head→tail)+P1+Ch1(sec:lco·전자엔트로피·decomp·MSMR code)+Ch2(qrev·파생B·hys·warnbox). 코드 줄·tex 식 근거. refute 우선.

## ① ★School A vs B 판정 — **B(항등 seam) 승 (조건부)**
- **근거(결정타 c=hook 필요성)**: Ch1 sec:lco-code L1752-1758 = 전자항은 **`func_U_j`가 소비하는 `dS_rxn` 슬롯에 몰당 ΔS_e를 더하는 한 줄**로 들어가고 `∂U_j/∂T←ΔS_rxn/F` 경로는 흑연과 동일. `func_U_j`는 **L360(equilibrium)·L434(dqdv)** 두 곳 호출.
- **School A(독립클래스 O1·S2·S3·C1·C2·C3)**: 말단 순수함수(func_ksi_eq·func_w)는 재사용되나 **dqdv 오케스트레이션 루프(L431-477)는 전자항 주입점(L434)이 내부라 복제 불가피 → DRY 붕괴**. C1 L23-24가 자인. **O1 합성(위임 L111)은 위임 dqdv가 dS_rxn을 내부에서 읽어 전자항 주입점 접근 불가 → 논리적 실패.**
- **School B(O2 경로B·O3)**: L434 인자를 `self._effective_dS_rxn(tr,...)`로 감싸고 base 항등(`return tr['dS_rxn']`) → 흑연 byte 0-diff, LCO override만 dSe 가산. **dqdv 복제 0.** O2 "값 그대로 반환" > O3 "+0.0 가산"(IEEE754 논쟁 원천소거).
- **(a) 0-diff**: 둘 다 통과 가능하나 B는 seam 항등성으로. **(b) 소유권**: A=replace 0(문언 최강)이나 DRY 대가 / B=replace 소수줄(물리불변, 라벨과만 표면충돌, master 판단). **(d) DRY**: B 압승(seam 2줄 vs dqdv 110줄 복제).
- **결론 골격 = O2 경로B seam + O3 §3-2 하네스. ★단 seam을 3경로 공유로 확장(⑤).**

## ② 물리 오류/의심/정상
**정상[확정]**: MSMR 동형(X_j↔Q_j·U_j⁰↔U_j^d·ω_j↔w_j·**f↔−σ_d**, Ch1 eq:msmr L1738 — f=−σ_d는 부호반전 아니라 두 지수표기 자리일치) · q_rev=−IT·∂U/∂T **T 한 번**(entropy_coef가 ∂U/∂T[V/K] 반환) · 전자항 몰당(÷e_V·×N_A·부호<0, 골≈−46 J/mol/K Ch1 L1123) · q_rev 부호(방전 ΔS>0→흡열) · LCO 총계수 ≈+80>0(전자항 −1.5 소수보정, 부호공존 S2 R6·S3 R4 포착).

**오류[확정]**:
- **S1 D1.4(L208-211) "func_U_j가 T 한 번→T² 자동누적" = 오류**: eq:U1T2 L1054 올바른 T² 계수 `a_e/(2F)`, ½은 `∫a_e T'dT'`. 선형 func_U_j에 dS_rxn_eff=ΔS_0+a_e T 넣으면 **½ 손실**(Ch1 L1058 명시 경고). **C3 L268(center T_ref 적분 별도처리)가 유일 정확 → 채택, S1 배제.** (단일온도 곡선엔 무영향, 다온도 발열 T의존서만 발현.)
- **LCO s=−1 논쟁: O계열 옳음**: Ch1 sec:lco-map L304-307 명시 *"방전 σ_d=+1은 LCO엔 리튬화... 부호골격 같다... ∂U_j/∂T=ΔS_rxn/F 부호까지 흑연과 동일"* + L1746 f=−σ_d가 방향일관성 이미 보증. **S3 s=−1 기본값(L157)·C2 scan_sign 3분리(L36)·C3 f_msmr 지역변수(L36) 배제**(Ch1 위반, 근거미발견을 확정처럼). **O1 L62·O2 L48·O3 L58·S1 L54·C1 L34(부호 뒤집기 없음) 채택.**
- **O1 §1.1 합성(위임)**: 전자항 주입점 접근 불가 논리 실패(위 ①).
- **O3 L116 x↔ξ 방향(`x_lo+ξ(x_hi−x_lo)`, ξ↑→x↑)**: Ch1 L308·L1035(탈리튬화 ξ↑⟺x↓) 반대 의심. **S1 L199 `x=1−ξ` 방향 채택**(x_MIT=0.85 정합), round-trip 피팅인자 노출(O3 L120·C1 L303).

## ③ 이중계산·회귀·부호 판정
- **이중계산 직교[확정 정상, 9종 통과]**: dS_rxn=중심 ΔS⁰_j만 · config `(R/F)ln(ξ/(1−ξ))` 런타임 재계산(dict 미오염, O2 §2.3 "재가산 물리적 불가능") · 전자항 T1만(Ch1 Z=Z_config·Z_elec). **★미묘점(O1·O3만 포착): dqdv 경로는 config 무가산(w가 이미 담음, Ch2 L242) / q_rev 경로는 config 명시 가산 — 두 경로 비대칭·이중계산 아님. 골격 주석 필수.**
- **회귀 하네스[유효]**: tobytes()(C1 최소충분)/np.array_equal/SHA-256 전부 bit-exact 유효. **면적=Q assert(P1 §4 결함해소)**: O1 L228·C2 차등 atol(평형종 1e-4·꼬리종 1e-3, 꼬리 ∫=0.99986) · **편입 前 golden 캡처(S3 R5 필수절차)**. DC=1 자동보존(_causal_lowpass 무수정).
- **히스 가역**: 분기평균(Ch2 L582) O3 §2-4·S2 q_rev_hys_avg 구현.

## ④ 체리픽 가이드
| 항목 | 채택 | 배제 |
|---|---|---|
| 구조 | O2 경로B seam + O3 항등반환, **★3경로 공유로 확장** | O1 합성·School A 독립클래스 DRY붕괴 |
| 전자항 함수 | O3 `func_dSe_molar`(몰당·÷e_V·부호<0) | — |
| q_rev 완전식 | O1 `func_dUoc_dT` + O3 `entropy_coefficient`(두경로 직교주석) | — |
| 부호 σ_d | O1 L62·O3 L58(뒤집기 없음) | S3 s=−1·C2 3분리·C3 f_msmr |
| T² | C3 L268(center T_ref 적분) | S1 L208 자동누적 |
| x↔ξ | S1 L199 `x=1−ξ` + 피팅노출 | O3 L116 역방향 |
| 이중계산 | O2 §2.3 + O1/O3 두경로 비대칭 주석 | — |
| 회귀 | C1 tobytes + O1 면적assert + C2 차등atol + S3 편입전캡처 | — |
| 비가역 | lumped I(U_oc−V)만(Ch2 L643 유일 boxed), 3분해 슬롯만 | 3분해 닫힌식 날조 |
| Serena | insert 8 + **replace 2(L434·L360)** + 死코드 보존 | O2 replace 1 과소평가 |

## ⑤ 가장 약한 1곳 (9종 전원 놓침)
**전자항 seam이 dqdv(L434)에만 있으면 equilibrium(L360)·q_rev(entropy_coefficient)에서 LCO T1 전자항 누락 → LCO 세 산출(평형곡선·dqdv곡선·q_rev)이 T1 온도이동 불일치.** 회귀 하네스는 흑연만 봐서 이 LCO 내부 불일치 못 잡음. **해소: 단일 헬퍼 `_lco_effective_dS_rxn(tr,T,xi_T1)`를 equilibrium·dqdv·entropy_coefficient 3경로가 공유(흑연 base 항등, LCO override만 dSe 공급).**

## ⑥ master Serena 편입 주의 5줄
1. **seam 3경로 공유** — `_effective_dS_rxn`(항등 base) dqdv(L434)·equilibrium(L360)·q_rev 모두 적용, LCO override 하나가 세 dSe 공급. replace_symbol_body = L434·L360 **2줄** 인자감싸기(물리불변), 그 외 insert_after.
2. **전자항 단위 3중 가드 즉시 검산** — ÷e_V(곱 금지 ~4e37배)·몰당 R·kB(~10²³배)·부호 leading −. self-test에 골≈−46 J/mol/K assert.
3. **회귀 golden 편입 前 캡처** — 현 HEAD 흑연 dqdv/equilibrium/curve `.npy` 저장 후 편입, np.array_equal(allclose X). 면적=Q 차등 atol.
4. **σ_d 뒤집지 말 것**(Ch1 L304-307). 死코드 func_U_j_hys(L82-91) 불가침(P1).
5. **T² 곡률 func_U_j 자동 안 됨** — 다온도 T1 이동은 eq:U1T2 ½(a_e/2F) 필요, center T_ref 별도(C3). **P4 1차는 dqdv 호출 T 하나로 평가**, T² 곡률은 다온도 피팅 단계 과제로 분리.
