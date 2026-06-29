# 추출카드 — Wang/Reynier 2009 thermal mgmt + LCO 엔트로피 계수 프로파일 (C1·C4)

> 통합 카드: (i) JPS 2009 "Effect of entropy change … thermal management" + (ii) 단일전극 ΔS(LiCoO2) 측정 묶음(non-isothermal·potentiometric).

- **저자·연도·DOI**:
  - (i) Wang, Reynier 외, "Effect of entropy change of Li intercalation in cathodes and anodes on Li-ion battery thermal management", *J. Power Sources* (2009), S0378775309021119.
  - (ii) "Temperature coefficients of Li-ion battery single electrode potentials … revisited" (PubMed 30640324); "Single Electrode Entropy Change for LiCoO2 Electrodes" (ECS Trans. 80(10), 219; academia 143468519).
- **축**: C1(엔트로피 계수 ∂U/∂T) 주, C4(가역열) 보조.
- **핵심 방법**: 평형전압 온도계수 ∂U_ocv/∂T (potentiometric / non-isothermal symmetric cell), 하프셀(vs Li). 가역열 = $q_{rev} = I\,T\,\partial U/\partial T$.
- **지배식**: $\Delta S(x) = F\,\partial U_{ocv}/\partial T$; $q_{rev}=T\Delta S$.
- **정량값(값·단위·조건·불확도)**:
  - **LiCoO2 단일전극 전위 온도계수 dφ/dT ≈ +0.83 mV/K** (non-isothermal, "revisited"). 단일전극 ΔS 양(+). tier B(검색 snippet).
  - 전 전극 ΔS_i ≈ 70–120 J/mol·K 범위(SOC 별, LCO 포함 집합값). tier B.
  - LCO **electrode heat effect: +51 ~ −46 kJ/mol** (SOC 의존). Seebeck −2.8 → +1.5 mV/K(초기→Soret 평형). tier B.
  - **셀(LCO−graphite) 엔트로피계수 부호 전환**(전셀 기준, 하프셀 아님 — 주의): −구간 0–37.8% & 65.5–88.5% SOC, +구간 37.8–65.5% & 88.5–100%; min −0.37 mV/K @5% SOC, max +0.1 mV/K @45% SOC. tier B(2차).
  - ★**LCO ΔS ≫ NMC·LFP** — 정성 정설(가역열 비중 큼). tier A.
- **타당·한계**: ∂U/∂T 측정법(potentiometric)·LCO 의 큰 가역열·부호전환 정설을 확보. 한계: full-text 유료(RG 403) → ΔS(x) 곡선 수치표·peak 위치 미확보, dφ/dT=0.83·heat ±51/−46 은 snippet tier B. **셀 부호전환 프로파일은 전셀(LCO−Gr) 합산** — Ch1 LCO 하프셀(vs Li)은 LCO 단일 ΔS 만 필요(혼동 주의).
- **우리 의도 관련성 (L1·L6)**:
  - 양극 ∂U/∂T 의 **부호·크기 스케일**(단일전극 +0.83 mV/K 급, ΔS O(10–100) J/mol·K) = Ch1 U_j(T)=(−ΔH+TΔS)/F 의 ΔS 입력 검증.
  - LCO 가역열 ≫ NMC/LFP → 양극 엔트로피 항이 열적으로 유의 = 전자+config+phonon 합산이 큰 이유(Reynier 카드와 정합).
- **정독범위**: abstract + 검색 snippet(다중 cross). full-text = gated(RG 403) → snippet/abstract.
- **tier**: LCO ΔS≫NMC/LFP **A**; dφ/dT 0.83·heat ±51/−46·부호전환 **B**; ΔS(x) 곡선 수치 **C(미확보)**.
