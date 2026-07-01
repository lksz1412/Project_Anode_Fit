# P4 Step3 — master 체리픽 설계 vN-10 (Serena 실편입 청사진)

> 검토1(School B 승 + ★3경로 공유) 골격. master 직접 코드 정독으로 앵커 확정: func_U_j=L77-78(선형 T) · equilibrium func_U_j 호출=L358 · dqdv func_U_j 호출=L436. transition 키={dH_rxn,dS_rxn,U,Q,Omega,gamma,h_eta,+동역학}. 전자항 게이트 자체검산: g_max_eV=13·dx_MIT=0.05·T=298 → ΔS_e=−(π²/3)R(k_B T/e_V)(g_max/dx)σ(1−σ)|_max = **−45.7 J/mol/K ✓**(Ch1 L1123 −46 일치).

## A. 채택 골격 (검토1 ④ + 3경로 수정)
- **구조 = School B 항등 seam**, ★**3경로 공유**: 신규 base 메서드 `_effective_dS_rxn(self, tr, T)` = 흑연 항등(`return tr['dS_rxn']`) → equilibrium(L358)·dqdv(L436)·q_rev(신규 entropy_coefficient) **모두 이 seam 경유**. LCO override 하나가 세 경로 dSe 공급.
- **0-diff 보장**: 흑연 base seam이 `tr['dS_rxn']` **그 값 그대로** 반환(+0.0 없음, IEEE754 논쟁 소거) → func_U_j 인자 완전 동일 → byte 일치.
- **replace_symbol_body = 2**(equilibrium·dqdv, 각 인자 1개 seam 래핑, 물리 불변). 그 외 전부 insert_after_symbol.
- 死코드 func_U_j_hys(L82-91) 불가침(P1).

## B. 신규 심볼 (insert_after)
1. **상수** `EV_TO_J = 1.602176634e-19` (eV→J 다리, eq:gunit) — 모듈 상수 뒤.
2. **`func_dSe_molar(x, T, g_max_eV, x_MIT, dx_MIT)`** → 부분몰 전자 엔트로피 [J/(mol·K)] (Ch1 eq:dSegate 게이트형):
   `sig=1/(1+exp(−(x−x_MIT)/dx_MIT)); gate=sig(1−sig); return −(π²/3)·R·(kB·T/EV_TO_J)·(g_max_eV/dx_MIT)·gate`. ★부호 leading −·÷EV_TO_J(곱 금지)·몰당 R·kB(자리당 kB² 아님). func_chi_d 뒤 삽입.
3. **`LCO_MSMR_LIT`** = LCO 3-전이 MSMR 시연 파라미터 dict(★tier-C 시연 기본값, round-trip 피팅 전 — 날조 데이터 아님·피팅 함수 기본 placeholder 명시). Ch1 sec:lco 값 참조(MIT 전이 1개에 electronic 키). GRAPHITE_STAGING_LIT 뒤.
4. **`LCOCathodeDQDV(GraphiteAnodeDischargeDQDV)`** 서브클래스 — `_effective_dS_rxn` override만:
   `dS=tr['dS_rxn']; if tr.get('electronic'): dS=dS+func_dSe_molar(tr['x_center'], T, tr['g_max_eV'], tr['x_MIT'], tr['dx_MIT']); return dS`. (T는 seam 전달값 — 단일온도 곡선서 정확. 배열 T면 element-wise.) GraphiteAnodeDischargeDQDV 뒤.
5. **base 신규 메서드** `_effective_dS_rxn(self, tr, T)` = `return tr['dS_rxn']`(항등). `_direction_to_sigma` 뒤.
6. **base 신규 메서드 `entropy_coefficient(self, V_n, T)`** → ∂U_oc/∂T [V/K] 배열 (Ch2 use-this 가중식): 전이별 `dS_eff/F`(seam) 가중(Q_j·ξ(1−ξ)/w 정규화) + config 분포항 `(R/F)ln[ξ/(1−ξ)]` 가중 가산. ★dqdv엔 config 무가산(w가 담음)/q_rev엔 config 가산 = 두 경로 비대칭(주석 필수).
7. **base 신규 메서드 `reversible_heat(self, V_n, T, I)`** → `−I·T·entropy_coefficient(V_n,T)` [W] (q_rev=−IT·∂U/∂T, **T 한 번**).
8. **base 신규 메서드 `irreversible_heat(self, U_oc, V, I)`** → lumped `I·(U_oc−V)` [W] (Ch2 L643 유일 boxed). 3분해는 docstring 주석만(옵션·Ch2 범위밖·근거 라벨).

## C. base 수정 (replace_symbol_body, seam 2줄)
- **equilibrium** L358: `func_U_j(T, tr['dH_rxn'], tr['dS_rxn'])` → `func_U_j(T, tr['dH_rxn'], self._effective_dS_rxn(tr, T))`. 나머지 본문 byte 보존.
- **dqdv** L436: `func_U_j(T_work, tr['dH_rxn'], tr['dS_rxn'])` → `func_U_j(T_work, tr['dH_rxn'], self._effective_dS_rxn(tr, T_work))`. 나머지 본문 byte 보존.

## D. 배제 (검토1)
- S1 T² 자동누적(½ 손실) · S3 s=−1·C2 3부호분리·C3 f_msmr(σ_d 뒤집기 금지, Ch1 L304-307) · O1 합성(전자항 주입 불가) · O3 x↔ξ 역방향.
- **부호**: LCO도 σ_d=+1 방전(흑연 동일). x↔ξ: `x=1−ξ`(Ch1 L308·L1035, ξ↑⟺x↓), round-trip 피팅인자 노출.
- **T² 곡률**: P4 1차 = seam이 전달 T로 ΔS_e 평가(단일온도 곡선 정확)·q_rev는 표준 Bernardi ∂U/∂T=ΔS_eff/F. Sommerfeld T-스케일(½ a_e/2F) = 다온도 피팅 단계 과제(라벨 분리, C3).

## E. 회귀·검증 (편입 前 golden 캡처)
1. **편입 前** 현 HEAD 흑연 `curve()`/`equilibrium()`/`dqdv()` 골든 `.npy` 저장.
2. 편입 後 `np.array_equal`(allclose 아님) bit 일치 = 흑연 0-diff 게이트.
3. **면적=Q assert**(P1 §4 해소): `trapz(dqdv−baseline, V)≈ΣQ_j`, 차등 atol(평형종 1e-4·꼬리종 1e-3, 꼬리 ∫=0.99986).
4. DC=1 자동보존(_causal_lowpass 무수정).
5. LCO dqdv 정상 개형 + q_rev 곡선(부호: 방전 ΔS>0→흡열) 그래프 생성.

## F. Serena 편입 순서
insert_after ×6(EV_TO_J·func_dSe_molar·LCO_MSMR_LIT·LCOCathodeDQDV·base 4메서드) + replace_symbol_body ×2(equilibrium·dqdv seam). 死코드 불가침. 식별자·정수코드·시그니처 보존.
