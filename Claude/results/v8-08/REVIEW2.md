# REVIEW2 — v8-08b (Codex 보완판) 검토2 (적대 검수, 리뷰 전용)

검수자: 검수 sub (수정·커밋 없음). 대상 = `v8-08b.tex` 전문 1198행 정독 + 3보완 직접 검산.
기준(정독) = `Anode_Fit_v11_final.py`·`v7-11.tex`·`AUTHOR_BRIEF_v8.md`·`REVIEW1.md`.
검산 도구: SymPy 기호검증 + 수치검증 + `Anode_Fit_v11_final.py` 자체 self-test 독립 실행.

---

## 1. 보완 반영 검증 (REVIEW1 3개 결함)

### ★D-PEAK [REVIEW1 C1, CRITICAL] — **수정 확정 (정정 수학 직접 검산 PASS)**
- **제거 확인**: v8-08 의 오서술 "작은 `L_V`에서 logistic 미분 종으로 환원"의 핵심 문구 `한 격자 뒤`가 v8-08b 에서 0회(원본 v8-08 1회). L908-911·L919-922 전면 재서술.
- **정정 내용 (L909-911, L920-922)**: ① `L_V≪Δgrid → ρ=e^{-Δgrid/L_V}→0 → ξ_lag→ξ_eq → (ξ_eq-ξ_lag)/L_V` 수치적 0 붕괴(종 아님). ② `L_V≫Δgrid → 1-ρ≈Δgrid/L_V → bell 환원이 이산 저역통과로 해상`. ③ 작은 L_V 평형 복귀는 극한이 아니라 **eq:branch 명시 스위치**(L466 코드 `lag_len_V < min_lag_grid_steps*grid_step`)가 담당 — 코드와 1:1.
- **★직접 검산 (요청 항목)**: 수치로 못박음 — `L_V=0.1Δgrid` 에서 tail peak=4.4e-3≈0 (붕괴 확정), `ρ` 표 `L_V/grid=0.01→ρ=0.0000`·`=100→1-ρ=0.0100=grid/L_V` 정합. 코드 분기는 `if`-스위치(불연속)이지 매끈한 극한이 아님 — 정정 방향 정확. **v7-11 상속 9종 공유 치명 결함 해소.**
- **잔여 nuance (신규결함 아님, 아래 §2-N1)**: `L_V≫Δgrid` 한계는 bell 의 *근사*(lag-shift·broadening; max|tail-bell|=0.379, peak 0.1025 vs 0.100)이지 eq:eqpeak 와 *정확* 일치는 아님. 문서는 "환원 형태를 낸다/해상된다"로만 적어 정확 등치를 주장하지 않음 — 방어 가능, 정정으로서 적정.

### D-VEQ [REVIEW1 C2, HIGH] — **수정 확정 (inline 다리 + 기호검증 PASS)**
- L438 에 `sF(V_{eq,j}(ξ)-U_j)=g_j'(ξ)=RT ln[ξ/(1-ξ)]+Ω_j(1-2ξ)` inline 삽입 확인. eq:Veq(L432) 직후, §5/§6 forward-defer 순환 차단.
- **기호검증**: g(ξ)=g0+RT[ξlnξ+(1-ξ)ln(1-ξ)]+Ωξ(1-ξ) 의 `g'(ξ)`가 문서 다리식과 **항등**(SymPy 잔차=0, 0<ξ<1). 다리→spinodal→artanh gap 사슬도 `gap=(2/F)[Ωu-2RT artanh u]` 와 정확 일치(SymPy+수치 Ω=6k~13k 전건 match=True).

### D-WEFF [REVIEW1 C3, MEDIUM] — **수정 확정 (4Fw 다리 + 검산 PASS)**
- L560-568 derivebox 신설: `g''(ξ)=RT/[ξ(1-ξ)]-2Ω`, `g''(1/2)=4RT-2Ω`, 중심 inverse-logistic 기울기 `sF dV/dξ|_{1/2}=4F w^eff`, `4F w^eff=4RT-2Ω → w^eff=(RT/F)(1-Ω/2RT)`.
- **검산**: `g''(1/2)=4RT-2Ω` SymPy 확인. `4F·w^eff=4RT-2Ω` 수치 Ω=0/3000/2RT 전건 match=True. 코드 `func_w_eff`(L144) 식과 1:1.

---

## 2. 신규 회귀 점검 (★Codex 보완이라 엄격)

신규 결함 = **0건 (CRITICAL/HIGH)**. 보완 3곳 인접 텍스트·식별자·\ref orphan·부호 드리프트 전수 점검.
- **N1 [NOTE, 신규결함 아님]**: D-PEAK 정정의 `L_V≫Δgrid` bell 환원은 근사(shift·broadening)임을 본문이 등치로 오인할 여지 미세. 단 문서 표현은 "해상/환원 형태"로 한정 — 결함 아님, 향후 1구 보강 여지만.
- **회귀 음성 확인**: ① 제거된 오문구 외 인접 박스(eq:peakshape·eq:branch) 식별자·번호 보존. ② D-VEQ inline 이 eq:Veq 번호식·후속 \eqref 깨지 않음(aux undefined ref 0). ③ D-WEFF 신설 박스가 eq:wbase/eq:weff 번호·\code{func\_w\_eff} 정합. ④ 부호장 S1~S8·R1~R4 무변경(아래 §4). ⑤ 빌드 청정: `v8-08b.log` bang=0·fatal=0·undefined ref 0(폰트 italic shape 경고 3건은 cosmetic).
- **코드 독립 실행 재현**: `Anode_Fit_v11_final.py` 직접 실행 `>>> overall OK: True`. dU_hys=86.7mV, dis-chg split +86.9mV(기대 +86.7), Ω=2RT→dU=0, γ=0/|I|→0 dis-chg=5.1e-15, guards 7/7, override isolation True — NOTEb 수치 전건 일치(노트 신뢰가 아닌 독립 재산출).

---

## 3. 재점수 (/35) — REVIEW1 27 → **REVIEW2 33**

| 차원 | R1 | R2 | 근거 |
|---|---|---|---|
| ①G-derive 유도 완결성 | 2 | **5** | D-PEAK 정정 수학 PASS + D-VEQ·D-WEFF 박스 신설, 3사슬 SymPy/수치 검증 |
| ②배치 보존 | 5 | 5 | 절순서·박스·표·식별자 v7-11/v11 완전 보존(보완은 inline/박스 추가뿐) |
| ③부호 8항 v11 1:1 | 5 | 5 | S1~S8+R1~R4 무변경, 코드 self-test 독립 재현 |
| ④G-follow·G-usable·완결성 | 4 | **5** | eq:Veq 순환 차단(inline 다리)으로 읽는 순서 폐곡선 해소 |
| ⑤그림(6개·ASCII·\ref) | 4 | 4 | 변경 없음. fig:derivechain "charge balance" 라벨 모호 잔존(경미) |
| 형식·빌드 자족 | 4 | **5** | xelatex 2-pass PASS·bang0·fatal0·undefined ref0 (로그 직접 확인) |
| 직전수정 새결함 | 3 | **4** | 신규 CRITICAL/HIGH 0. N1 근사-등치 미세 nuance만(−1) |

**합 = 33/35** (G-derive·G-follow·빌드 만점 회복; ⑤ 라벨·N1 nuance 만 잔여).

---

## 4. 부호 8항 (S1~S8) 재검산 — 전건 PASS, 보완 후 드리프트 0

S1 `U_j=(-ΔH+TΔS)/F, ΔG=-FU` ✓(eq:Uj/eqcond·func_U_j L69; U(2→1)=0.0853V 검산) · S2 `ξ_eq=logistic[σ_d(V-U)/w]`, 방전 V↑→ξ↑ ✓(eq:xieq·func_ksi_eq L86) · S3 `dξ/dV=σ_dξ(1-ξ)/w`, peak=|·|≥0 방향불변 ✓(eq:eqpeak L677) · S4 `ΔU_hys≥0, Ω≤2RT→0, ±½σ_d` ✓(SymPy gap=boxed·spinodal 대칭 ±half-gap·코드 dis@0.163/chg@0.077) · S5 `χ_d 충전1-χ, ΔH_a^eff=ΔH_a-χ_dΩ` ✓(eq:chid/dHeff·func L160/L152) · S6 `∂lnL_q/∂V`: 컷상수라 실현0·부등식은 동기 ✓(코드 L_q 전이당 스칼라 동결 L463·정정 일관) · S7 충전 격자역전 `ξ[::-1]…[::-1]`·충전 거울 양수 ✓(eq:reversal·코드 L477; 직접 L_V dis@0.134/chg@0.106 양수) · S8 `V_n=V_app-σ_d|I|R_n` 방전 측정>내부 ✓(eq:vn·코드 L「V_n=V_in-sigma_d*I_abs*Rn」). **부호 결함 0 — 보완 후에도 확정.**
