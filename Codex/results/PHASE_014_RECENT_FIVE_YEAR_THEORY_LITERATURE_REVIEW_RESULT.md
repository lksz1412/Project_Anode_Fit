# Phase 014 최근 5년 이론 문헌 및 Claude 산출물 통합 검토

검토일: 2026-07-20

## 1. 최종 판정

### 확정

1. 검토 범위는 챕터 1-3 전체다. LCO는 현재 결함의 심각도 때문에 최우선
   심층 트랙이지만 유일한 트랙이 아니다.
2. Claude 산출물은 자료를 모으고 수식을 코드에 일관되게 옮기는 능력은
   보여주지만, 현재 상태를 교과서·리뷰 수준의 과학 정본 또는 물리적으로
   검증된 계산 모델로 승인할 수는 없다.
3. 가장 큰 문제는 LCO다. 단순 보정계수 문제가 아니라 다음 두 모델 클래스
   오류가 동시에 존재한다.
   - 전이별 1차원 진행좌표 `xi_j`와 양의 regular-solution `Omega`가 주는
     scalar curvature를 symmetry-resolved Li/vacancy ordering의 미시적
     증명으로 해석한다. 1차원 축약 자체가 항상 틀린 것은 아니지만, 현재는
     explicit order state에서 유도한 축약이 아니다.
   - 검토한 근거 중 직접 유도가 없는 composition-logistic DOS gate를 전자
     엔트로피의 미시적 모델로 해석한다.
4. 챕터 1은 단일 정규용액·logistic peak mixture를 그래파이트 staging의
   유일한 물리모델로 제시할 수 없다. 다층 staging 자유에너지, 변환동역학,
   전극 수송, 관측·전처리 연산자를 분리한 계층 모델이 필요하다.
5. 챕터 3은 명시적 질량/용량 기준을 가진 제한적 독립-host 평형모델로는
   유지할 수 있다. 유한속도 current partition, finite strain, Si phase/path,
   SiOx/Si-C 내부 host, fracture/LAM/SEI를 포함한 일반 이론으로는 현재 코드와
   문서가 불충분하다.
6. 기존 v1.0.23 회귀 시험은 모두 통과한다. 그러나 이 시험은 구현이 자기
   문서·이전 버전과 일치함을 보일 뿐, 사용한 물리가 LCO·graphite·Si의 실제
   열역학을 재현함을 보이지 않는다.

### 결론

Claude 작업을 전면 폐기할 필요는 없다. 기호 규약, 관측량 경로, 코드 인터페이스
일부는 보존할 가치가 있다. 다만 과학 정본으로 올리려면 다음 원칙으로 재구성해야
한다.

- 유도된 이론, 문헌에서 전이한 수치, 실험 피팅값, 현상론적 basis, 시연값을
  문장과 표에서 분리한다.
- 정적 DFT 에너지, 유한온도 자유에너지, OCV, dU/dT, ICA/DVA를 같은 물리량처럼
  연결하지 않는다.
- equilibrium coexistence, spinodal, kinetic hysteresis, signal-processing
  width를 별도 개념과 별도 출력으로 둔다.
- 코드가 구현하지 않은 상태변수나 온도·속도 의존성을 구현했다고 쓰지 않는다.

## 2. 검토 범위와 증거 무결성

이 결과는 다음 정본을 잇는다.

- Phase 006 LCO 과학감사
- Phase 007 Chapter 3 과학감사
- Phase 010 Claude 산출물 master review와 strengthening roadmap
- Phase 011 31개 Critical/High finding을 연결한 이론-gap matrix
- Phase 012 69개 중복제거 최근문헌 candidate matrix
- Phase 013 32개 source-to-model transfer 판정

최근문헌 검색창은 2021-01-01부터 2026-07-20까지다. 2021년 전체를 포함한다는
운영 규칙은 계획서에 명시했다.

전문 검독 상태는 별도로 보존했다. Chapter 3과 common-method 후보는 worker가
논문 본문의 모델·결과·한계 구간을 읽었지만 전 페이지를 읽지는 않았다. 따라서
그 논문을 이용한 수식·수치 적용은 통합 matrix에서
`RETRIEVE_OR_FULL_READ_BEFORE_IMPLEMENTATION` 또는
`PROVISIONAL_*_FULL_READ_REQUIRED`로 강등했다.

## 3. LCO 우선 심층 판정

### 3.1 1차원 positive-Omega만으로 ordering을 입증할 수 없다

현재 문서는 양의 Omega를 이용한

\[
g(x,T)=RT[x\ln x+(1-x)\ln(1-x)]+\Omega x(1-x)+\cdots
\]

형태를 x=0.5 부근 Li/vacancy ordering과 연결한다. 실제 v1.0.23 전이식의
좌표는 전역 조성 `x`라기보다 전이별 진행좌표 `xi_j`다. 그러나 어느 경우든
독립 상태는 1차원이며, 같은 조성에서 ordered state와 disordered state,
variant degeneracy, symmetry breaking을 구분하는 좌표가 없다. 양의 Omega가
직접 주는 것은 선택한 scalar coordinate의 curvature와 convexity loss다.

[Faghih Shojaei et al. 2024](https://doi.org/10.1016/j.jmps.2024.105726)는
O3 LCO에서 x와 여섯 개 비보존 order parameter를 사용해 12개 symmetry-related
ordering variant를 표현한다. 이 논문은 full free energy와 composition-only
표현에서 안정성 방향과 전이 경로가 달라질 수 있음을 보여준다. 다만 explicit
order state를 최소화해 얻은 reduced scalar free energy의 비볼록성이 언제나
인공적인 것은 아니다. 금지해야 할 것은 축약 과정 없이 scalar curvature를
곧바로 microscopic ordering identity로 부르는 것이다.

따라서 현재 상호작용항은 다음 중 하나로 처리해야 한다.

- ordering이라는 이름을 제거하고 empirical scalar curvature 또는
  documented reduced model로 한정한다.
- 실제 ordering을 주장하려면 `g(x,eta,T)` 또는 symmetry-complete
  `g(x,eta_1,...,eta_6,T)`로 교체한다.

### 3.2 logistic electronic gate의 미시적 근거를 찾지 못했다

v1.0.23은 `func_dSe_molar`에서

\[
\Delta S_e \propto
-T\frac{g_{\max}}{\Delta x}\sigma(x)[1-\sigma(x)]
\]

를 사용하며 `g_max=13`, `x_MIT=0.85`, `Delta x=0.05`를 둔다. 코드 위치는
`Anode_Fit_v1.0.23.py` 236-252행과 950-1019행이다.

이번에 실제로 검토한 직접 LCO 근거에서는 다음을 찾지 못했다. 이는 재현 가능한
전 데이터베이스 systematic review의 보편적 부재 증명이 아니라, 현재 reviewed
set에 한정된 negative finding이다.

- composition-logistic DOS gate의 유도
- O1 또는 endpoint DOS를 O3 전 조성으로 옮기는 전이 규칙
- `Delta x=0.05`의 이론적 유도
- `g_max`와 `Delta x`를 독립적으로 식별하는 관측량

최근 전자구조 연구는 오히려 단순 gate에 반대되는 경계를 준다.

- [Fantin et al. 2023](https://doi.org/10.1103/PRXEnergy.2.043010):
  LiCoO2-CoO2 endpoint에서 self-regulated ligand-metal charge transfer를
  보여주며 연속 composition gate를 주지 않는다.
- [Ahn et al. 2023](https://doi.org/10.1039/D3CP02998K):
  거의 같은 고-Li 조성에서도 magnetic/correlation 선택이 metallic state와
  localized polaron state를 바꾼다.
- Xie et al. 2025 preprint, arXiv:2510.02875:
  x=1과 x=1/3의 DFT+DMFT 비교일 뿐 composition width나 electronic entropy를
  계산하지 않는다.
- [Mattila and Karttunen 2022](https://doi.org/10.1002/pssb.202100665):
  x=0, 0.5, 1의 hybrid-DFT 전자·자기·phonon 계산에서 CoO2의 zero-K electronic
  state조차 방법 의존성이 큼을 보인다. 이는 endpoint DOS를 연속 gate로 옮기는
  데 model discrepancy가 필요함을 강화하지만, 자체로 finite-T reaction entropy를
  주지는 않는다.
- [Hu et al. 2022](https://doi.org/10.1007/s11581-022-04585-5):
  intrinsic-defect electronic structure를 직접 다루는 누락 문헌이다. 현재는
  초록만 확인했으므로 defect smearing으로 `Delta x=0.05`를 정당화하는 데 쓸 수
  없고 전문 회수가 필요하다.

따라서 logistic feature를 남기려면 `electronic DOS`, `O1-to-O3 transfer`,
`MIT entropy`라는 미시적 이름을 제거하고 branch-specific total
OCV/entropy의 empirical localized basis라고 불러야 한다.

### 3.3 현재 코드는 문서가 주장하는 x,T 함수를 구현하지 않는다

직접 코드 확인 결과:

- `LCO_MSMR_LIT`는 `x_center=x_MIT=0.85`를 둔다
  (`Anode_Fit_v1.0.23.py` 953-965행).
- 전자항 계산은 caller x가 아니라 항상 `tr['x_center']`를 사용한다
  (1017-1019행).
- 전자항 계산 온도는 caller T가 아니라 항상 `T_ref=298.15`다
  (1003-1020행).
- 표에 보이는 폭은 0.030, 0.024, 0.028 V지만 각 전이에 `n=1.0`이 있어
  런타임 폭은 세 전이 모두 `RT/F`다 (961-972행, 367-386행).
- 클래스 설명은 graphite 골격에서 유일한 확장이 전자 엔트로피 seam이라고
  쓴다 (977-998행). 실제 Chapter 2가 주장하는 ordering, 구조상, MIT,
  microstructure 상태는 코드에 없다.

독립 수치 probe:

| Probe | 결과 |
|---|---:|
| `func_dSe_molar(x_MIT,...,x_MIT,0.05)`, x_MIT 0.50 대 0.85 | 완전히 동일, 차이 0 |
| `_effective_dS_rxn`, caller T 278.15 대 318.15 K | 완전히 동일, 차이 0 |
| 표시 폭 | 30, 24, 28 mV |
| 298.15 K 런타임 폭 | 모두 25.691238 mV |

이는 중심·온도·표 폭이 실제 출력의 독립 물리 파라미터가 아님을 보여준다.

### 3.4 configurational, vibrational, electronic entropy는 현재 관측으로 분리되지 않는다

\[
G=G_{\mathrm{static}}+F_{\mathrm{conf}}+F_{\mathrm{vib}}+F_{\mathrm{el}}
\]


에서 각 성분에 합이 0인 보상함수를 더해도 total G, OCV, dU/dT는 바뀌지 않는다.
따라서 OCV와 reversible heat만으로 세 성분을 각각 측정했다고 말할 수 없다.

필요한 독립 근거는 다음과 같다.

- configurational: direct-LCO cluster expansion/Monte Carlo, phase boundary,
  superstructure intensity
- vibrational: composition/phase-specific phonons, QHA/anharmonic calculations,
  heat capacity or Raman/neutron validation
- electronic: composition/structure-resolved correlated-electron free energy와
  spectroscopy
- total reaction entropy: 동일 sample과 branch의 multi-temperature
  equilibrium OCV 또는 calorimetry

[Kuroda et al. 2023](https://doi.org/10.1103/PhysRevMaterials.7.115402)의
0 K hull과 O2 gas entropy를 포함한 300 K hull,
[Chen et al. 2021](https://doi.org/10.3969/j.issn.1001-9731.2021.07.008)의
endpoint harmonic phonon correction, Shojaei의 finite-T configurational free
energy는 서로 다른 subset이다. 어느 것도 measured dU/dT 전체와 자동으로
동일하지 않다.

기존 정량 anchor도 바로잡아야 한다. Motohashi의 `13 electrons/eV`는 CoO2의
susceptibility 차이를 Pauli 항으로 해석해 얻은 endpoint inference이지 x=0.85
부근의 연속 조성 DOS 측정값이 아니다. Reynier의 `0.18 k_B/atom`은 두 조성의
계산된 electronic-state entropy difference이지 measured total partial-molar
reaction entropy가 아니다. 둘 다 logistic amplitude/width의 직접 calibration
값으로 사용할 수 없다.

### 3.5 LCO 복구 옵션

#### Option A: 데이터 조건부 생산 복구

평형·다온도 data gate를 통과할 때의 우선 권고안이다. 동일 sample, branch,
rest protocol에서 equilibrated multi-temperature OCV 또는 reversible-heat
자료가 없으면 `kappa(x)`를 새로 피팅하지 않는다. 그 경우 즉시 조치는 기존
logistic 전자항의 비활성화 또는 명시적 empirical demotion이다.

\[
U_b(x,T)=U_{b,\mathrm{ref}}(x)
+\int_{T_{\mathrm{ref}}}^{T}\kappa_b(x,\tau)\,d\tau
\]


또는 제한된 온도창에서

\[
U_b(x,T)=U_{b,\mathrm{ref}}(x)+(T-T_{\mathrm{ref}})\kappa_b(x)
\]


를 사용한다. `U_ref`와 `kappa`는 constrained spline 또는 작은 smooth
basis로 표현한다. charge/discharge branch를 따로 두되 metastable/kinetic
branch를 별도 equilibrium state function이라고 부르지 않는다. localized
feature는 empirical amplitude/center/width와 covariance만 갖는다.

장점: data gate가 있을 때 false microscopic claim, frozen x/T, width
inconsistency를 가장 빨리 수정한다.

한계: ordering 또는 MIT mechanism을 예측하지 않으며, held-out ICA/DVA 재현도
microscopic entropy mechanism의 검증은 아니다.

#### Option B: 중기 order-parameter 재구축

`x`와 별도의 `eta`를 사용한다. 실제 O3 Li0.5CoO2 symmetry를 주장하려면
단일 scalar eta가 충분한지 먼저 증명하고, 그렇지 않으면 symmetry-complete
order vector를 사용한다. equilibrium OCV는 eta minimization과 stability,
common-tangent 검사를 거친다. dynamics를 주장할 때만 conserved x에
Cahn-Hilliard, nonconserved eta에 Allen-Cahn을 사용한다.

필수 validation: variant degeneracy, transition temperature, diffraction
intensity, OCV, x-only projection의 false spinodal 부재.

#### Option C: 장기 CE/MC 연구모델

direct-LCO DFT configuration set, cluster expansion, semi-grand/umbrella Monte
Carlo, differentiable `G(x,eta,T)` surrogate를 구축한다. 이는
configurational ordering의 가장 강한 경로지만 high-x MIT, phonons, oxygen
loss를 자동으로 해결하지 않는다.

## 4. Chapter 1 그래파이트 보강

### 확정된 방향

현재 설명은 다음 5개 층으로 재구성해야 한다.

1. multilayer staging thermodynamics
2. nucleation/spinodal/coarsening/mosaic transformation
3. anisotropic solid diffusion와 porous-electrode transport
4. raw voltage에서 ICA/DVA로 가는 observation/preprocessing operator
5. nonlinear identifiability, uncertainty, model discrepancy

### 우선 추가 문헌

| 우선도 | 문헌 | 역할 | 상태 |
|---|---|---|---|
| Must add | [Cordoba et al. 2024](https://doi.org/10.1103/PhysRevE.109.024132) | multilayer Cahn-Hilliard staging과 x-only 축약의 한계 | 전문 검독 |
| Must add | [Borghed et al. 2026](https://doi.org/10.1016/j.matdes.2026.116218) | ICA phase-group/kernel observation model, width confounding | 전문 검독 |
| Must add | [Jamnuch and Pascal 2023](https://doi.org/10.1038/s41467-023-37857-3) | stage-dependent anharmonic entropy | 전문 검독 |
| Useful add | [BMINN 2026](https://doi.org/10.1016/j.ensm.2026.104997) | chemical-potential inference와 posterior uncertainty의 competing model | preprint 전문, VOR pagination 미검독 |
| Retrieve first | [Paul et al. 2024](https://doi.org/10.1149/1945-7111/ad70d9) | MCMB entropy-coefficient prior | targeted, 전문 필요 |
| Retrieve first | [Agrawal and Bai 2022](https://doi.org/10.1016/j.xcrp.2022.100854) | rate-dependent mosaic/apparent-solid-solution 경계 | targeted, 전문 필요 |
| Retrieve first | [Rykner and Chandesris 2022](https://doi.org/10.1021/acs.jpcc.1c10800) | stacking-order coupled free energy | 전문 미확보 |
| Retrieve first | [Gao et al. 2021](https://doi.org/10.1016/j.joule.2020.12.020) | HOPG 단일 입자의 intercalation-phase separation-plating 경쟁; DOI 연도 검색 맹점 | critic targeted, 전문 필요 |
| Retrieve first | [Lu et al. 2023](https://doi.org/10.1038/s41467-023-40574-6) | geometry, orientation, surface, C-rate와 inter/intraparticle 동역학을 묶는 multiscale phase field | critic targeted, 전문 필요 |
| Retrieve first | [Olson et al. 2023](https://doi.org/10.1021/acs.chemmater.2c01976) | half-cell/full-cell ICA/DVA 변환, balancing, degradation 관측 map | critic targeted, 전문 필요 |

### 보존해야 할 negative result

- reviewed set에서 universal graphite free-energy equation은 발견하지 못했다.
- exact staging voltage를 material/protocol 독립 상수로 만드는 근거를
  발견하지 못했다.
- ICA peak width를 하나의 microstructure parameter로 만드는 근거를
  발견하지 못했다.
- exact Chapter 1 overlapping finite-mixture parameterization의 battery-specific
  uniqueness proof를 reviewed set에서 발견하지 못했다. 이는 적절한
  identifiability 방법론 자체가 없다는 뜻은 아니다.

## 5. Chapter 3 Si/graphite 보강

### 확정된 방향

1. `basis_id`를 두어 fixed-total-active-mass replacement와
   fixed-graphite-mass addition을 분리한다.
2. common electrochemical potential은 equilibrium condition이지
   `G_int=0`의 증명이 아니다.
3. finite rate에서는 `j_Si`, `j_Gr`, 각 host concentration, active area,
   electrolyte/solid potential, total-current closure가 필요하다.
4. general Si mechanics는 multiplicative finite strain과 plastic/viscoplastic
   state가 필요하다. small-strain scalar는 local approximation으로만 둔다.
5. `Omega tr(sigma)/(3F)`의 stress invariant와 sign convention을 명시하고
   thin-film, free particle, constrained particle, porous composite를 구분한다.
6. c-Si, a-Si, Li15Si4, first-cycle, branch, cutoff/history를 상태로 둔다.
7. elemental Si, SiOx, Si-C, Si/graphite physical blend를 서로 다른 material
   adapter로 둔다.
8. fracture/LAM, SEI, cyclable Li, porosity/CBD/contact를 equilibrium voltage
   offset으로 숨기지 않는다.

### 우선 문헌

다음 문헌은 방향성 면에서 중요하지만 이번 phase에서는 targeted read이므로
수식 적용 전 전문 검독이 필요하다.

- [Ai et al. 2022](https://doi.org/10.1016/j.jpowsour.2022.231142):
  separate host current와 rest exchange
- [Jiang et al. 2022](https://doi.org/10.1149/1945-7111/ac5481):
  blend basis와 host-current competition
- [Kobbing et al. 2024](https://doi.org/10.1002/adfm.202308818):
  finite-strain particle-SEI hysteresis
- [Le et al. 2026](https://doi.org/10.1016/j.jmps.2025.106421):
  independent mechanical perturbation으로 stress-potential coupling 검증
- [Fu et al. 2023](https://doi.org/10.1002/adfm.202303936):
  Si phase/path thermodynamics
- Garrick 2024, Bonkile 2024, Schoof 2025, Darikas 2025:
  SiOx volume/basis, degradation states, finite-strain plasticity,
  ICA/DVA cross-sensitivity
- [Lu et al. 2025](https://doi.org/10.1038/s41565-025-02027-7):
  graphite/Si composite의 contact, porosity, current redistribution와
  electro-chemo-mechanical 관측을 직접 연결한다. 따라서 관련 recent work가
  없다는 넓은 부재 주장은 기각한다. 다만 source-specific magnitude는 전이하지
  않는다.
- [Olou'ou Guifo et al. 2022](https://doi.org/10.1039/D1CP05414G):
  Si/graphite bulk, surface, interface의 first-principles 경계를 준다. continuum
  nonseparable bulk `G_int`를 제공하는 것은 아니다.
- [Qu et al. 2022](https://doi.org/10.1002/eem2.12329):
  Li-Si-O bulk phase landscape를 보강한다. electrode-level conversion,
  trapped-Li, contact, first-cycle inventory closure는 별도 문제다.
- [Mertin et al. 2023](https://doi.org/10.1016/j.est.2023.107118)와
  [Feser et al. 2026](https://doi.org/10.1016/j.jpowsour.2026.240046):
  blend entropy hysteresis, internal balancing current, rest relaxation과
  graphite-to-Si transfer 경계를 보강한다. 전문 검독 전 수치 전이는 금지한다.

### 2026년 최신 직접 진단 문헌

- [Wan et al. 2026](https://doi.org/10.1016/j.joule.2026.102531)은
  constant-current charge에서 material-specific health와 degradation-induced
  effective Si OCP deformation을 함께 추정한다. 공식 summary가 보고한
  Si-dominant transition SoC는 fresh 48%, lithium-loss-dominated 73%,
  active-Si-loss-dominated 33%로 이동한다. 이는 Chapter 3에 degradation-path
  state와 uncertainty-conditioned observation model이 필요하다는 직접 근거다.
  다만 effective OCP deformation은 특정 진단 model 안의 식별량이지, 유일한
  microscopic Si free energy가 아니다. 전문과 supplement 회수 전 구현 금지다.
- [Natterer et al. 2026](https://doi.org/10.1016/j.jpowsour.2026.239896)은
  EIS에 대한 aging, SoC, temperature의 주효과와 상호작용을 분해한다. 이
  결과는 EIS 기반 Si/graphite 열화 추정에서 SoC와 temperature를 독립 보정항으로
  분리하거나 생략해서는 안 된다는 경계를 준다. 그러나 effect size나 통계적
  의존성은 host-resolved mechanism의 고유 식별 증명이 아니다.

### reviewed set에서 정확히 남는 근거 미발견

- 현재 reduced blend model에 직접 삽입 가능한 calibrated continuum nonzero
  bulk Si/graphite `G_int`
- cutoff/history에서 Li15Si4 phase fraction을 예측하는 validated porous/full-cell
  closure
- SiOx conversion/trapped-Li를 electrode level에서 검증해 닫는 closure
- contact/CBD/porosity, fracture/LAM, SEI/inventory를 함께 닫는 검증된 reduced
  evolution law
- voltage-only ICA/DVA로 Si/graphite/cathode degradation을 고유하게 분리하는
  증명

### 차단한 수치 전이

- Fu 2023의 `0.26 V`와 `0.26 eV` 표기가 본문/결론에서 충돌한다. governing
  energy normalization과 transferred charge를 재구성하기 전 qualitative
  phase/path evidence로만 둔다.
- Darikas 2025의 약 `14.9%`는 critic이 확인한 case에서 silicon mean relative
  error이며 absolute percentage-point error가 아니다. 절대오차와 상대오차를
  혼용한 기존 서술은 폐기한다.
- Garrick 2024의 약 5 wt% SiOx가 전체 volume change의 약 절반을 설명한다는
  초록-level 결과는 formulation-specific하다. `약 1/5 capacity` 주장은 정확한
  본문 locator가 없어 `NOT_VERIFIED`다.

## 6. 공통 역문제·관측 모델

공통방법론은 재료 파라미터를 제공하지 않는다. 다음 설계 원칙만 전이한다.

- ICA/DVA acquisition, alignment, filtering, differentiation을 likelihood의
  일부로 둔다.
- local Jacobian rank에 더해 nonlinear profile likelihood 또는 posterior
  geometry를 본다.
- residual을 전부 iid measurement noise로 두지 않고 model discrepancy에
  대한 민감도를 검사한다.
- voltage data를 반복해서 더하는 대신 rate, temperature, impedance,
  expansion, reference electrode, diffraction/spectroscopy, independent
  mechanical perturbation처럼 orthogonal observable을 선택한다.
- normalized derivative shape와 absolute capacity/balancing/slippage를 함께
  보존한다.

common-method 20개 unique candidate는 전문 검독이 없으므로 구현 수식의 직접
근거로 승격하지 않았다.

## 7. 교과서·리뷰 구조 판정

### 현재 구조의 문제

현 문서는 교과서형 유도, review-style 문헌 비교, reduced-order fitting guide,
코드 명세가 같은 층위에서 섞인다. 그 결과:

- illustrative parameter가 물성 상수처럼 보인다.
- 한 model class의 결과가 material physics의 유일한 설명처럼 보인다.
- source가 계산한 quantity와 문서가 사용하는 quantity가 달라진다.
- 코드 회귀 통과가 외부 물리 validation처럼 읽힌다.
- scope boundary와 omitted state가 본문 후반이나 주석으로 밀린다.

### 권고 구조

각 챕터를 다음 순서로 통일한다.

1. **Material/state definition:** 조성, phase, branch, temperature, geometry,
   reference state와 sign convention.
2. **Observable definition:** OCV, chemical potential, dU/dT, ICA/DVA,
   capacity/heat의 측정·계산 정의.
3. **Model hierarchy:** 최소 현상론, 중간 explicit-state model, 연구급
   multiscale model을 병렬 비교.
4. **Equilibrium thermodynamics:** minimization, convexification, common
   tangent, stability.
5. **Dynamics and history:** reaction, transport, nucleation, hysteresis,
   degradation.
6. **Observation operator:** sampling, filtering, differentiation,
   electrode/full-cell mapping.
7. **Identifiability and validation:** parameter covariance, competing models,
   held-out protocols, falsification data.
8. **Implementation contract:** 문서 수식과 코드 함수의 1:1 mapping,
   implemented/omitted status.
9. **Validity domain:** composition, T, rate, geometry, cycle, phase,
   high-voltage/degradation exclusions.

모든 식·표·수치에 다음 라벨 중 하나를 붙이는 것이 적절하다.

- `DERIVED`
- `DIRECT_SOURCE`
- `CALIBRATED`
- `EMPIRICAL_BASIS`
- `ILLUSTRATIVE`
- `RETRIEVE_BEFORE_USE`
- `NOT_IMPLEMENTED`

## 8. 코드 변환 판정

### Chapter 1

코드는 현재 logistic/MSMR reduced observation model을 일관되게 계산하는 데는
성공한다. 그러나 multilayer staging free energy, phase-field/mosaic dynamics,
anisotropic/porous transport, non-circular preprocessing와 identifiability
analysis를 구현한 것은 아니다. 따라서 Chapter 1 전체를 코드로 옮겼다고
표현하면 과장이다.

### Chapter 2 LCO

코드 변환은 부적합하다. graphite curve skeleton에 constant electronic entropy
offset을 더했을 뿐, 문서가 논하는 ordering, MIT phase state, finite-T
electronic/vibrational/configurational free energy를 구현하지 않았다. 게다가
x와 T가 frozen되어 문서의 함수적 의존성도 상실한다.

### Chapter 3

zero-Si limit, capacity conservation, smooth fraction sweep 등 내부 수치 gate는
통과한다. 이는 restricted additive/equilibrium model의 구현으로는 유효하다.
finite-rate host currents, nonseparable interaction, phase/path, finite strain,
contact/CBD, fracture/LAM/SEI/inventory는 구현하지 않았거나 명시적
`NotImplemented` 경계다. Chapter 3 전체의 일반 이론 구현으로 승인할 수 없다.

## 9. 실행 우선순위

### P0: 문장과 현 코드의 즉시 과학 복구

1. LCO logistic gate의 DOS/O1-to-O3/MIT microscopic identity를 제거한다.
2. positive-Omega scalar `xi_j` term의 microscopic ordering label을 제거한다.
3. LCO에 actual x, T, branch를 전달하고 하나의 width source만 사용한다.
4. equilibrated multi-temperature data gate가 통과할 때만 LCO Option A를 새
   reduced production baseline으로 삼는다. 통과하지 못하면 logistic 항을
   비활성화/강등한다.
5. Chapter 1 peak width를 empirical observation parameter로 강등하고
   preprocessing provenance를 붙인다.
6. Chapter 3 mass/capacity basis와 stress geometry를 명시한다.
7. Fu `0.26 V/eV`, Darikas error metric, Garrick capacity fraction을 모든
   구현·정량 anchor에서 제거하고 전문 대조 queue로 보낸다.

### P1: 문서 구조 재구축

1. 세 챕터를 공통 9-section model hierarchy로 재배열한다.
2. 각 claim에 evidence/status label과 validity domain을 붙인다.
3. direct-source table, retrieval queue, negative findings를 본문에 보존한다.
4. code-interface mapping과 omitted-state table을 분리한다.
5. source availability, actual read status, online/VOR/issue date type과 exact
   query/dedup log를 분리한다.

### P2: 데이터가 있을 때의 모델 확장

1. Chapter 1 multilayer staging + observation operator.
2. LCO Option B order-parameter model.
3. Chapter 3 finite-rate host-current + phase/path + finite-strain model.
4. nonlinear identifiability, model discrepancy, orthogonal validation.

### P3: 연구급 확장

1. LCO direct DFT/CE/MC/surrogate pipeline.
2. composition-resolved phonon/correlated-electronic free energy.
3. SiOx/Si-C internal chemistry와 contact/SEI/inventory 통합.

## 10. Fresh Sol 비판 통합

두 독립 `gpt-5.6-sol` critic은 각각 LCO 339행, Chapter 1/3/common 476행
보고서를 남겼고, 현재 Codex가 두 파일을 처음부터 끝까지 직접 읽었다.

### 비판으로 확정 수정한 내용

1. LCO regular-solution 좌표는 엄밀히 전역 `x`가 아니라 전이별 `xi_j`다.
   핵심 결함은 scalar model의 존재가 아니라 scalar curvature를 explicit
   symmetry/order state 없이 microscopic ordering으로 부른 것이다.
2. reduced scalar free energy의 비볼록성이 항상 false spinodal이라는 표현은
   폐기했다. documented minimization/reduction에서 생긴 비볼록성은 물리적일 수
   있다. 현재 모델에는 그 reduction provenance가 없다.
3. logistic gate 부재 주장은 `reviewed evidence에서 이 특정 법칙과 g_max,
   Delta x를 함께 유도한 근거를 찾지 못함`으로 좁혔다.
4. LCO Option A는 equilibrated same-sample multi-temperature data가 있는 경우에만
   우선 권고한다. data gate가 없으면 새 `kappa(x)`를 만들지 않고 기존 항을
   비활성화하거나 empirical term으로 강등한다.
5. Chapter 1/3의 넓은 no-suitable-paper 표현을 폐기하고, exact missing closure와
   `in the reviewed set` 한계를 붙였다.
6. Gao 2021, Lu 2023, Olson 2023, Mijailovic 2024, Lu 2025, Olou'ou Guifo
   2022, Qu 2022, Mertin 2023, Feser 2026 및 LCO Mattila 2022, Tan 2021,
   Hu 2022를 별도 candidate addendum에 추가했다.
7. Fu의 `0.26 V/eV`, Darikas의 absolute/relative error, Garrick의 capacity
   fraction을 구현 차단 수치로 분류했다.
8. Rehm과 Li 논문은 `inaccessible`이 아니라 `official access route는 있으나
   이번 pass에서 전문 회수/검독 미완료`로 정정한다. Paese도 official open
   full text다.
9. DOI 문자열의 연도를 출판연도로 사용하지 않는다. Gao 논문은 DOI에 2020이
   들어가지만 2021년 출판되어 review window 안에 있다.
10. LCO critic이 코드·시험 전문 검독 경로로 기록한 snapshot의 `Claude/src`와
    `Claude/tests` 파일은 parent가 재확인한 실제 snapshot에 존재하지 않았다.
    따라서 해당 critic의 경로 provenance는 수용하지 않고, parent가 직접 확인한
    `Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py`와
    `Claude/docs/v1.0.23/test_gates_v1023.py`를 controlling path로 둔다.

### critic gate 판정

| Critic | 판정 | 통합 결과 |
|---|---|---|
| LCO | `HOLD / CORRECTION REQUIRED` | 핵심 model-class 비판 유지, 표현·Option A·문헌 누락 수정 |
| Chapter 1/3/common | `BLOCK` | 구현 승인 중단, omission/addendum와 수치·접근상태 정정 |

따라서 이 보고서는 과학적 결론과 개선 방향을 제공하는 **review result**로는
완료하지만, 최근문헌 package가 equation-level implementation에 준비됐다는
`PASS`를 선언하지 않는다.

## 11. 검증

- `phase012_recent_theory_candidate_matrix.csv`: 69행, 0 duplicate source ID,
  0 duplicate DOI/official URL.
- `phase013_theory_integration_adjudication.csv`: 32행, 0 duplicate
  integration ID, 모든 source ID resolve.
- `phase014_recent_theory_candidate_addendum.csv`: 15행, critic omission과
  date-unresolved watchlist; 0 duplicate source ID/DOI.
- `phase014_theory_integration_addendum.csv`: 8행, 모든 source ID가 Phase 012
  matrix 또는 Phase 014 addendum에 resolve.
- `critic_lco_sol.md`: 339행 전체 직접 재독.
- `critic_crosschapter_sol.md`: 476행 전체 직접 재독.
- v1.0.23 `test_gates_v1023.py`: exit 0, G1/G2/G3/n(T)/R6 gates PASS.
- 별도 LCO probe: center-shift invariance, frozen electronic T input, runtime
  width shadowing 확인.
- source snapshot/Claude/TeX/Python/test/example 수정: 없음.
- Git command: 실행하지 않음.

## 12. Gate

`RECENT_THEORY_REVIEW_BLOCKED_BY_RETRIEVAL`

review와 개선방향 도출은 완료했다. 그러나 gate-critical omission의 전문 검독,
Fu/Darikas/Garrick 수치 재대조, 접근상태 정정, 재현 가능한 search log가 남아
있으므로 equation-level chapter integration과 source/code 수정은 승인하지 않는다.
