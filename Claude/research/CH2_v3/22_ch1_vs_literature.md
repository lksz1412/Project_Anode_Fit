# Ch2 v3 — Ch1 GRAPHITE_STAGING_LIT ↔ 문헌 정합 대조 (Phase 2.2)

> master CORE 판단. 추출카드(`20_extraction/`)·서브1 _SUMMARY 기반. Ch1 값 = `Anode_Fit_v11_final.py` GRAPHITE_STAGING_LIT(전이별). ★부호 규약 확정: **ΔS=+nF·∂U/∂T**, $\dot Q_\mathrm{rev}=-I\,T\,\partial U/\partial T$ (MSMR Part I Eq.27/28 full-text + Newman; −부호 추출 1건은 추출오류로 폐기).

## 전이별 ΔS 대조 (★헤드라인 — 강한 정합)
| 전이 | Ch1 x 범위 | Ch1 ΔS_rxn [J/mol/K] | 문헌 graphite ΔS(x) (Allart 2018, full-text) | 정합 |
|---|---|---|---|---|
| 4→3 | 0.08–0.16 | **+29.0** | **+29 @ x=0.08**(reg IV) | ★정확 일치 |
| 3→2L | 0.16–0.25 | 0.0 | −15~0 @ reg II(히스 구간) | 범위 내 정합 |
| 2L→2 | 0.25–0.50 | −5.0 | −5~−16 @ x>0.5 하단 | 정합 |
| 2→1 | 0.50–1.00 | −16.0 | **−16 @ x>0.5**(reg I) | ★정확 일치 |
**해석**: Ch1 의 ΔS_rxn 추세(저x 양수→고x 음수, +29→0→−5→−16)가 Allart 2018(full-text) 전극 ΔS 와 *부호·규모 정량 일치*(+29·−16 정확). Reynier 2003(부호: x<0.25 양/config, x>0.25 음/vib)·MSMR Part II(∂U/∂T low-x 양수, ~0.2 부호반전) 와도 정성 정합. ⇒ **Ch1 GRAPHITE_STAGING_LIT 의 ΔS 는 문헌 근거(Allart 계열)에 정합**(아마 동출처 파생). tier: 확정준함(Allart full-text).

## 전이별 ΔH 대조 (내부 일관·문헌 범위)
| 전이 | Ch1 ΔH_rxn [kJ/mol] | Ch1 U(298)[V] | 부분몰 ΔH 환산 검산 | 문헌 |
|---|---|---|---|---|
| 2→1 | −13.0 | 0.085 | $-FU+FT\,\partial U/\partial T=-8.20-4.77=-12.97$ kJ/mol ✓ | 형성 ΔH 와 *기준 다름*(아래) |
- Ch1 ΔH_rxn 은 U·ΔS 와 $U_j(T)=(-\Delta H+T\Delta S)/F$ 로 **내부 정합**(검산: 2→1 −12.97≈−13.0 kJ/mol). 부분몰(differential) ΔH ≈ −13 kJ/mol, 고-x 덜 음(Reynier "Li–Li 반발" 정성 정합).
- ★**기준 주의**: 문헌 LiC6 −13.9·LiC12 −24.8 kJ/mol Li(Chem.Mater.2015)는 **형성(cumulative) 엔탈피**(graphite+Li금속 기준)이고, Ch1 ΔH_rxn 은 **전이별(differential/partial-molar) 반응 엔탈피**다 — *직접 등치 금지*. 비교하려면 형성 엔탈피의 x-미분(differential)으로 환산해야 함(Phase 3 종합서 환산식 명시). 우연히 LiC6 −13.9 ≈ Ch1 2→1 −13.0 이나 *우연·기준 상이*이므로 정합 주장 안 함(tier: 미검증).

## U(298)·중심 전위
- Ch1 U: 0.210/0.140/0.120/0.085 V — 흑연 staging plateau 전위(문헌 dQ/dV peak 위치대)와 정성 정합(정량 peak-위치 대조는 Phase 3).

## 부호 사슬 정합 (Ch1↔문헌)
- $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ (Ch1 U_j(T) 미분) ↔ 문헌 ΔS=+nF·∂U/∂T (n=1 per Li). ★부호 동일(+). Ch1 의 ΔS_rxn>0 @저x ⇒ ∂U/∂T>0 @저x ⇒ MSMR Part II(+3~4 mV/K @low-x) 와 정합.
- 가역 발열 $\dot Q_\mathrm{rev}=-I\,T\,\partial U/\partial T$(Bernardi) ↔ Ch1 전이별 ∂U_j/∂T=ΔS_rxn,j/F 합성으로 직접 산출 가능(Ch2 의 핵심 사슬).

## 괴리·주의 (정직)
1. ΔH 기준 상이(형성 vs 전이별) — 환산 전 등치 금지(tier 미검증).
2. graphite 갤러리/전이 수: 문헌 5~6(MSMR Part I=6, II=5) vs Ch1 4 전이 — staging 정의·dilute stage 포함 여부 차이. master: Ch1 4 전이는 주요 plateau 기준(dilute 1L 제외), 문헌 5~6은 dilute 포함 — *해상도 차이*로 양립(Phase 3 명시).
3. Allart reg II(히스 구간) ΔS −15~0 폭 — Ch1 stage3→2L ΔS=0 은 이 폭의 한 점(히스로 분산). 정합하나 히스 하 단일값 한계.
4. 절대 수치 일부 미검증(Reynier 절대 dE/dT·Electrochim.Acta 2019 식) — Phase 3 갭.

## Gate (Phase 2.2)
PASS — 전이별 ΔS Ch1↔Allart 정량 정합(★+29·−16 정확)·부호 규약 확정·ΔH 내부일관·기준상이 주의 명시·괴리 정직 기록. → Phase 3.1 종합·갭.
