# P3 RESULT — 챕터2(발열) 교과서화 + v5 (9종 경쟁-체리픽 vN-11)

> 마스터 §P3 · 계획 `../../plans/2026-07-02-v1010-P3-ch2-heat-plan.md`. 대상 `docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex`(통계열역학·가역발열). **순서 코드→문건→코드: 발열 코드 구현은 P4, P3=이론 갈고닦기.**

## 1. 범위·산출
Ch2(코인 하프셀 엔트로피·가역발열의 통계열역학)를 코드·Ch1과 정합하는 물리화학 교재로 정련. 신규 식 0 — 정합 매트릭스 확정 + 발열 유도 정직화 + 정밀도 정정 6건(추가·치환만, 통계열역학 본체 byte 보존). 발열 코드는 P4.

## 2. 정독 커버리지 (head→tail 전영역)
- 대상 Ch2.tex 751줄 전영역(warnbox L102-107·logistic L139-167·config 극한 L247-254·weighted L475-482·srcbox L484-489·revheat srcbox L644-654·종합식 L674-679·피팅추정 L701-708·bib L740·L747).
- Ch1.tex eq:Se L948-1077(전자엔트로피 정합), P1 result(코드 엔트로피항 dS_rxn·dS_a — q_rev 부재 확정).
- 8 supplement(S1-3·O1-3·C1·C3; C2 stall) 전문.

## 3. 방법 = 9종 경쟁-체리픽 (P1·P2 동일)
9드래프트(3S·3O·3C, 무통신 독립 — C2 stall로 8) → 검토1(별세션 Opus) → 체리픽 vN-10(master) → adversarial(별세션 Opus) → finalizer(master, Ch2.tex 실제 통합·재빌드). 커밋 4회.

## 4. 드래프트 (커밋① e2fc2cd)
8 supplement 완성(C1 18.1·C3 18.8·O1 25.3·O2 25.1·O3 21.9·S1 20.0·S2 16.9·S3 23.6 KB). C2(Codex) stall — 8/9 진행(로그).

## 5. 검토1 (별세션, 커밋② fa52aa6) — `V1010_P3_review1.md`
확정 사실 7건: **q_rev=−IT·∂U/∂T=−(IT/F)ΔS(T 한 번, 차원 [W] 무결)** · T-이중곱=지시문 축약(본문 무결·허위적발 금지) · 부호 흡발열 교대 정합 · 코드 dS_rxn(중심)/dS_a(비가역) · **이중계산 직교(P4 구현 시점만 주의)** · v5 w_eff 제거 타당 · **전자엔트로피 Ch1↔Ch2 정합적 중복(모순 아님)**. 정정 필요 3건(Σ Q_j g_j 차원·버전라벨·tier) + C1 full-cell 과대적발 하향 + 부호박스 가독성.

## 6. 체리픽 vN-10 (커밋③ c5e2447) — `V1010_P3_map_v10.md`
채택: O3(정합 매트릭스 12행·전자엔트로피 verbatim 5단계) + O2(발열 q_rev 4단계+11행 차원/부호) + O1(비가역 3분해 I²R+Iη_ct+Iη_diff) + C3(Σ Q_j g_j 정밀화) + C1(부호 convention box NOTE). 26.5KB.

## 7. Adversarial (별세션, refute) — 확정 오류 1건 적발
- **★[줄매핑 오류]** v10 표의 버전라벨 줄이 밀림 — 실제 v9={L395·L399·L400}(v10은 L399 누락·L401 오지목), v11={L485·L747}. **finalizer가 grep 재확인값으로 편입**(적발 반영).
- 정정1(Σ Q_j g_j=Q·∂x/∂U 옳음, L479 현행 ∂x/∂U는 Q배 누락 확정) · 가장약한1곳(srcbox L652 대수 무결·순수 가독성) · D-1(warnbox L102-107이 전셀 범위밖 선언→CRITICAL 격상 거부 옳음) · 신규유입 0 = 정상.
- 완화 지시: "byte 동일"→"함수형 동일·독립 label"(매크로 `k_B`vs`\kB`·인자 `g(E_F,x)`vs`g(E_F)` 차이) · N_A 단위다리(S_e∝k_B¹ vs ∂S_e/∂x∝k_B², R=N_A k_B 항등)는 양쪽 옳음·optional 권고(강제 반영 X, Ch2 미편집).

## 8. Finalizer 편입 (master, Ch2.tex 6정정 — 추가·치환만)
| # | 위치(실측) | 정정 | 형태 |
|---|---|---|---|
| 정정-1 | L479 | `측정 dQ/dV(=∂x/∂U)` → `(=Q ∂x/∂U; x 무차원이라 Q배)` | 치환(가중식 결과 불변, 서술) |
| 정정-2 | L395·L399·L400 | `Chapter 1 v9` → `Chapter 1`(v9 3곳) | 치환 |
| 정정-2 | L485·L747 | `Anode\_Fit\_v11` → `Anode\_Fit\_v1.0.10`(2곳) | 치환 |
| 정정-3 | L251 | occupation2019 인용에 `(방법 수준·dilute 격자기체 한정 참조)` tier 병기 | 추가 |
| 가장약한1곳 | L652 srcbox | 중간형 `−(IT/F)·T·ΔS/T` 제거 → `이를 곧장 대입해 −IT·∂U_oc/∂T=−(IT/F)ΔS`(G-follow) | 치환(대수 동일) |
| D-1 | L653 srcbox | 전셀 음극 몫 `+IT·∂U_an/∂T` 부호반전·범위밖(상단 박스) 방어 NOTE | 추가 |
| D-3 | L162 | `w=RT/F`에 `(자리당 n_j=1 기준; 유효 폭 w_j=n_jRT/F는 §revheat·코드 func\_w)` 다리 | 추가 |

byte 보존: eq:qrev(L645)·eq:Se(L391)·eq:weighted·통계열역학 본체(분배함수→점유→S_config/vib/elec·A·B·D) 손대지 않음.

## 9. 재빌드
xelatex 2-pass(kotex, inline bib) — **0-error, rc=0, 13페이지, PDF 갱신**(566KB Ch1·344KB Ch2). 잔존 v9/v11/지저분 중간형 = grep 0 확인.

## 10. Gate (P3 종료) — PASS
- 발열 유도 완결(q_rev↔ΔS 식→식, T 한 번 무결) ✓ · Ch1 정합(전자엔트로피 정합적 중복·broadening 인계) ✓ · 코드에 없는 발열=P4 예고 명기 ✓ · 교재급 안정객관 어투·독자평가 0 ✓ · PDF 0-error ✓ · CRIT/HIGH 0(adversarial 확정 오류=v10 줄매핑, finalizer에서 grep 재확인 반영) ✓.

## 11. P4 이월 (코드 개정)
- **이중계산 직교 주의**: 중심 ΔS⁰_j(config=0)에 config 분포항 R ln[ξ/(1−ξ)] 재가산 금지 — 코드 구현 시 중심 표준값과 분포항 분리.
- **발열 q_rev 함수 신설**: `q_rev=−IT·∂U/∂T=−(IT/F)ΔS(x)` — 흑연 회귀 0 diff 유지하며 추가. dS_e(전자엔트로피)·비가역 3분해 옵션.
- **w_j 이중지위**: 단상=평형 예측 RT/F, 흑연 두-상=현상학적 자유 피팅 폭(func_w=n·RT/F).
- **LCO 양극**: MSMR 동형(X_j↔Q_j, U_j⁰↔U_j^d, ω_j↔w_j, f↔−σ_d) — Ch1 sec:lco 정합.
- [D-2 vib 부분몰 닫힌식·D-4 T→0 ξ(T) 순서]는 P4/P5 검토 권고(보고만).
