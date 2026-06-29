# Ch1 v8-11 — 통계역학 충실도 검토 (2026-06-30)

> 사용자 요청: v8-11 에 통계역학 보강할 곳(누락·점프) 있는지, 없이도 설명되면 추가 불요. master 직접 정독(v8-11.tex §sec:hys L399–418·§sec:width L586–620 등).

## 결론 한 줄
**v8-11 의 통계역학은 *대체로 완비*** — "결과만, 유도 없음" 의 큰 갭은 없다. **단 한 곳**(평형 점유의 *분포* 프레이밍)만 보강 가치가 있고, 이는 Ch2(분포→엔트로피)·LCO(전자 Fermi–Dirac)로 가는 다리라 Ch1 v9 에 넣는 게 synergistic.

## 이미 잘 들어가 있는 통계역학 (보강 불요)
| 내용 | 위치 | 수준 |
|---|---|---|
| ★**조합→엔트로피**: $W=N!/[n!(N-n)!]$ → Stirling → $S_\mathrm{mix}=-k_BN[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$ | §sec:hys L401–403 | **미시상태 수 세기 → configurational 엔트로피 완전 유도**(분포→엔트로피의 핵심이 이미 있음) |
| 격자기체 $\mu(\theta)=\mu^0+RT\ln[\theta/(1-\theta)]+\Omega(1-2\theta)$ | eq:mu L408 | 평균장(Bragg–Williams) 유도 |
| 정규용액 $\Omega\theta(1-\theta)$ (이웃 쌍 평균장) | L403–404 | 유도 |
| 자유에너지 $g(\xi)$·spinodal($g''=0$) | eq:gxi L414·L418 | 유도 |
| logistic (kinetic 경로): Boltzmann 분포 → Eyring → detailed balance → $\xi_\eq/(1-\xi_\eq)=e^{\mathcal A/RT}$ | §sec:width L587–612 | **완전 유도**(속도식 정지점) |
| logistic (thermo 경로): $g'(\xi)=sF(V_\eq-U)$ | eq:Veq L461 | 자유에너지 최소화 |
→ 곧 **configurational 엔트로피(counting)·격자기체 μ·logistic(2경로)·정규용액·spinodal** 가 모두 *유도*돼 있다. 이건 "한 절" 이 아니라 제대로 된 통계역학 기초다.

## 유일한 보강점 (Ch1 v9 에 1개 추가 권고)
**평형 점유 $\xi_\eq$ 를 *점유 확률 분포*로 명시하는 한 단락.** 현재 $\xi_\eq$ 는 (i) kinetic(detailed balance) (ii) thermo(free-energy) 두 경로로 유도되나, **"$\xi_\eq$ 가 곧 격자기체의 *평형 점유 확률 분포*"**(단일 자리 grand-canonical/Boltzmann 점유 $\langle n\rangle=e^{-\beta\varepsilon}/Z$; $\Omega=0$ 이면 Fermi-함수형 $1/(1+e^{\beta(\varepsilon-\mu)})$)라는 *분배함수/분포* 프레이밍이 빠져 있다.
- **왜 보강**: (a) kinetic·thermo 두 경로를 *하나의 분포* 그림으로 통합 (b) ★Ch2(분포 $-R\sum p\ln p$ 에서 엔트로피 전개)로 가는 *깨끗한 다리* (c) ★LCO 전자 엔트로피(전도 전자 **Fermi–Dirac 분포**)와 직접 parallel — 같은 "점유 분포" 언어.
- **비용**: §sec:width 에 짧은 (e) 소절/단락 1개("(e) 같은 결과의 분포 관점: $\xi_\eq$ = 평형 점유 분포, $Z=1+e^{-\beta\Delta\mu}$ 의 단일 자리 점유"). 결과식·코드·부호 불변, 유도 *추가*만.
- ★사용자 기준 적용: 코어는 *이미 있어* 없이도 Ch1 설명은 닫힌다 → "필수"는 아님. 그러나 v9 가 어차피 LCO/전자 엔트로피를 추가하고 Ch2 가 분포를 전개하므로, 이 분포 프레이밍 1점은 *세 곳을 한 언어로 묶어 설명을 크게 편하게* 함 → **권고(필수 아님)**.

## 추가하지 말 것 (이미 충분·범위)
- vibrational/electronic 엔트로피 분해 = Ch2 의 몫(Ch1 forward 모델엔 불요).
- 분배함수 $Z$ 명시 전개 = W/Stirling 경로로 등가 충족(굳이 중복 X).
- 엔트로피의 온도 미분·가역 발열 = Ch2.

## 권고 (계획 반영)
Ch1 v9 Phase B 에 **통계역학 1점 보강**(ξ_eq 분포 프레이밍) 추가 — LCO 전자 엔트로피·Ch2 분포 전개와 한 언어로. 그 외 통계역학 보강 불요(이미 완비).
