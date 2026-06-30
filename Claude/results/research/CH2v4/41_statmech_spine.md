# Ch2 v4 — 통계역학 분포 spine 설계 (Phase C.1, master)

> Ch2 = 코인 하프셀 데이터 해석용 엔트로피·가역 발열 *통계열역학 챕터*. v3(Bernardi 가역열 survey) 위에 **분포(distribution)를 명시 전개**. 범위 = 단일 전극(vs Li) 하프셀. 전셀 합성 범위 외. ξ·Ω 든 닫힌식.

## 0. 왜 엔트로피엔 통계가 필요한가 (챕터 도입)
엔트로피 = 미시상태 분포의 흩어짐 척도. 가역 발열 $\dot Q_\rev=-IT\,\partial U/\partial T=-(IT/F)\Delta S$ 는 *분포를 재배열하는 열*. ⇒ ∂U/∂T(x) 를 이해하려면 Li(+전자) 점유 분포를 세워야 한다. (Ch1 = forward dQ/dV; Ch2 = 그 분포의 엔트로피·온도·가역열.)

## 1. 격자기체 분배함수 → 점유 분포 (★Ch1 logistic 의 기원)
- **단일 자리 grand-canonical**: 자리 하나가 비거나($\varepsilon=0$) Li 점유($\varepsilon=\varepsilon_0$, 전기화학퍼텐셜 $\mu$)의 2-상태 →
$$Z_1=1+e^{-\beta(\varepsilon_0-\mu)},\qquad \langle n\rangle=\frac{e^{-\beta(\varepsilon_0-\mu)}}{1+e^{-\beta(\varepsilon_0-\mu)}}=\frac{1}{1+e^{\beta(\varepsilon_0-\mu)}}.$$
- $\mu=\mu^0-sF(V-U)$ 대입 ⇒ $\langle n\rangle=\xi_\eq=1/(1+e^{-\sigma_d(V-U)/w})$ = **Ch1 의 logistic**. ★곧 Ch1 의 평형 점유는 *격자기체 점유 확률 분포*이고 $w=RT/F$ 가 분포 폭. (Fermi–Dirac 와 구조 동형 — 자리당 2-상태.)
- **다자리 평균장(Bragg–Williams)**: $g(\theta)=g_0+RT[\theta\ln\theta+(1-\theta)\ln(1-\theta)]+\Omega\,\theta(1-\theta)$. 상호작용 Ω 가 분포를 비튼다(Ω>2RT 면 bimodal=상분리).

## 2. 분포 → configurational 엔트로피 (★핵심 명시)
점유 분포의 Boltzmann/Shannon 엔트로피:
$$S_\mathrm{config}=-R\sum_i p_i\ln p_i=-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)]\quad(\text{자리 1몰당}).$$
- 부분몰(Li 1몰 삽입당): $\dfrac{\partial S_\mathrm{config}}{\partial\theta}=-R\ln\dfrac{\theta}{1-\theta}$. ★이게 ∂U/∂T 의 *x-의존(봉우리 내부)* 부분. 희박($\theta\to0$) +∞·만충($\theta\to1$) −∞.
- ★**Ch1 의 $w=RT/F$ 가 이미 이 항을 담음**: $V(\xi)=U_j+(RT/F)\ln[\xi/(1-\xi)]$ → $\partial V/\partial T|_\xi=\Delta S_{\rxn,j}/F+(R/F)\ln[\xi/(1-\xi)]$. 곧 logistic 폭 = configurational 부분몰 엔트로피. (이중계산 B: $\Delta S_{\rxn,j}$=중심 표준값(ξ=½), config 는 분포가 줌 — 별개 항.)

## 3. vibrational 엔트로피 (포논 분포)
격자 진동 = 포논 Bose–Einstein 분포. $S_\mathrm{vib}=R\sum_k[\,(1+n_k)\ln(1+n_k)-n_k\ln n_k\,]$, $n_k=1/(e^{\beta\hbar\omega_k}-1)$. 삽입 시 결합·격자 변화 → $\Delta S_\mathrm{vib}$ = 고-x 음의 baseline(Reynier "second contribution"). Ch1 의 $\Delta S_{\rxn,j}$ 중심 표준값에 흡수(전이별 상수 근사).

## 4. electronic 엔트로피 (Fermi–Dirac 분포) — Ch1 v9 에서 확장
전도 전자 Fermi–Dirac 분포 → Sommerfeld: $S_e=\frac{\pi^2}{3}k_B^2T\,g(E_F)$. 부분몰 $\Delta S_e=\partial S_e/\partial x<0$(삽입 기준, Ch1 v9 일관). LCO 하프셀 MIT 게이트. 흑연 하프셀 ≈0. ★Ch2 가 이 항을 *분포(FD)* 로 가역열 사슬에 통합 — 세 분포(config 격자기체·vib 포논 BE·electronic FD)가 한 챕터의 엔트로피.

## 5. 총 엔트로피 계수 = 세 분포 기반 합
$$\boxed{\;\frac{\partial U}{\partial T}(x)=\frac{\Delta S(x)}{F},\quad \Delta S(x)=\underbrace{\Delta S^0_j}_{\text{표준(중심)}}+\underbrace{R\ln\frac{1-\xi}{\xi}}_{\text{config 분포}}+\underbrace{\Delta S_\mathrm{vib}}_{\text{포논}}+\underbrace{\Delta S_e}_{\text{FD, MIT}}\;}$$
(측정 ∂U/∂T(x) = 세 분포 기반 엔트로피의 합. 부호: config 가 희박서 +, 만충서 −; vib 음 baseline; electronic 소수.)

## 6. 분포 재배열 = 가역 발열
$\dot Q_\rev=-IT\,\partial U/\partial T=-(IT/F)\,\Delta S(x)$ — Li(+전자) 분포를 한 SOC 에서 다른 SOC 로 옮기는 열. 충/방전 대칭(가역). 비선형 ∂U/∂T(x) = 분포의 x-의존 직접 반영.

## C.1 Gate
분배함수→점유 분포→config/vib/electronic 엔트로피 유도·Ch1 logistic 기원·이중계산 B 분리 확정. seed = Newman·Huggins·Bazant(lattice-gas OCV)·MSMR. → C.2 섞임/겹침·극한 수식.
