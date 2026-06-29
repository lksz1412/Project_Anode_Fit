# 추출카드 — ML scale-bridging order–disorder LixCoO2 (config 엔트로피·Tc)

- **저자·연도·DOI**: (Garikipati 그룹) "Bridging scales with Machine Learning: from first-principles statistical mechanics to continuum phase field … order–disorder transitions in LixCoO2", *J. Mech. Phys. Solids* **190**, 105727 (2024). arXiv 2302.08991. **★full-text PDF 정독(arXiv, pdftotext)**.
- **축**: C2(상전이·configurational 엔트로피).
- **핵심 방법**: DFT+U → cluster-expansion/IDNN(integrable deep NN) 자유에너지 → Monte Carlo + phase-field. O3 구조(x≥1/3) 한정.
- **지배식/결과**:
  - 자유에너지 $g(x,T)$ = formation energy coarse-grain + **configurational 엔트로피**(MC). x=½ 에서 zig-zag 정렬(12 variants, triangular Li sub-lattice 최저에너지).
  - x≈½ 부근 $g$ 의 비볼록(non-convexity) → **spinodal decomposition**(order–disorder).
- **정량값(값·단위·조건·불확도, full-text tier A)**:
  - **x≈½ order–disorder 전이온도 $T_c$ > 330 K** (실험 정합). → 상온(298 K)에서 x≈½ 정렬상 존재. tier A.
  - spinodal 조성: x=0.525 @260 K, x=0.53 @300 K. 340 K 에선 disordered only.
  - order–disorder interface energy ≈15.45 mJ/m², anti-phase boundary ≈30.9 mJ/m².
  - ★**모델이 x≈0.7–0.9 MIT 2상역을 재현 못 함** — "calculations lack the metal–insulator transition that leads to the two-phase region over x≈0.7–0.9 … voltage plateau not captured". (strain·vibrational entropy 미포함)
- **타당·한계**: ★우리 설계의 **결정적 음의 증거**: 순수 configurational stat-mech(Li-vacancy)만으로는 **3.9 V MIT plateau(x≈0.75–0.94 2상역)를 생성 불가** → **전자 엔트로피 항이 별도로 필요**함을 1차 계산으로 입증. config 항은 x≈½ order–disorder(Tc>330 K)만 설명. 한계: O3·x≥1/3 한정, 전자·strain·phonon 엔트로피 미포함(저자 명시 future work).
- **우리 의도 관련성**:
  - config 엔트로피로 설명되는 것 = **x≈½ order–disorder(상온서 정렬, Tc>330 K)**. 설명 안 되는 것 = **MIT 2상역(3.9 V)** → 전자 엔트로피 항 도입의 **이론적 정당화**(Reynier 0.18 kB/atom 크기 + Motohashi g(E_F)=13 + 이 카드의 "config 만으론 MIT 불가").
  - LCO forward 전이 분해: x≈½ logistic = config(이상 mixing + 정렬보정), x≈0.75–0.94 logistic = 전자(MIT).
- **정독범위**: **full**(arXiv 2302.08991 PDF, pdftotext, MC Tc·spinodal·MIT 누락 본문 정독).
- **tier**: Tc>330 K·spinodal 조성·MIT 누락 모두 **A**(본문 직접).
