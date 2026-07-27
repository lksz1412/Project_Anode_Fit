# Phase 044 — v1.0.25.2 Source Freeze and Independent Comparison

## Status

`CURRENT-SOURCE AND LINEAGE COMPARISON COMPLETE`

이 문서는 `v1.0.25.2` 현행 원문, Codex Chapter 1--5 후보본, 배포 코드,
시험, 그리고 `v1.0.25.2`가 채택한 archived `sigr.csv` fit 산출물을 새로
대조한 결과다. 이 파일은 blend로 표기되어 있지만 experimental protocol은
현재 provenance addendum에서도 `UNKNOWN`이다.
이전 `codex-local-audit-20260720` 브랜치의 과학 판정은 승계하지 않았다.

핵심 판정은 다음과 같다.

1. 사용자가 말한 전처리·창·목적함수 조건에서 **archived blend-labeled
   curve의 stored profile reconstruction은 실제로 높은 적합도를 보인다.**
2. 그 fit은 14개의 skew-logistic 항과 자유 배경으로 이루어진
   **경험적 곡선 모형**으로 재현된다.
3. 현행 기본 `graphite 7 + Si 7` host 구성은 위 14-peak blend fit의
   parameter vector가 아니다. 두 항목은 수와 kernel 형식만 같고 값과
   물리 제약이 다르다.
4. `v1.0.23` 이후 추가된 모든 내용이 잘못된 것은 아니다. skew kernel의
   면적보존, 공통 전위상의 host 합성, causal memory의 방향성, fit 자체는
   보존 가치가 있다.
5. 그러나 후보 문건의 폭--전자수 동일시, 가역열 부호, 충전 시 상태축
   반전, 열 꼬리식, 그리고 현행 기본 preset 연결은 승격 전에 수정해야 한다.

따라서 이번 검토는 “fit을 폐기”하는 작업이 아니라 다음 세 층을 분리하는
작업이다.

- 관측 자료를 잘 맞추는 surviving stored-8dp empirical profile
- 열역학·속도론 가정을 갖춘 physical host model
- 아직 구현되지 않은 theory/reference model

## 1. Authority and exclusions

### 1.1 Baseline

- Branch: `codex/v1025_2-physics-conformance`
- Baseline commit: `ab196b292e14492b647f87a6c0d1d8c9ed0630ab`
- Current release under review: `v1.0.25.2`
- Scientific source excluded:
  `Claude/docs/v1.0.26A-regsol`,
  `Claude/docs/v1.0.26B-gallery`
- Preserved unrelated dirty file:
  `Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html`

`Claude/results/comp_v26_data`라는 디렉터리 이름만으로 그 내용을
`v1.0.26` 문건으로 승인하지 않았다. 그 안에서는
`HANDOVER_v1025_2.md`가 `v1.0.25.2`의 archived blend-labeled curve 적합
근거로 직접 지목한 fit driver와 산출물만 provenance 확인에 사용했다.

### 1.2 Earlier audit branch

이전 감사:

- branch: `origin/codex-local-audit-20260720`
- tip: `20acd7dacc8aff62740e352bb68775758918602a`

사용 범위:

- 파일 위치
- duplicate 후보
- 읽어야 할 source 후보

사용하지 않은 범위:

- PASS/FAIL
- 결함 수
- 과학적 결론
- 수정 우선순위

이번 독립 재검산에서 이전 감사의 “correctness defect 0”류 결론과 양립하지
않는 결함이 실제로 발견되었으므로, 이전 결과는 과학적 권위로 사용할 수 없다.
실제로 locator로 사용한 주장만 독립 재검산했으며, 이전 audit 전체에 대한
claim-by-claim crosswalk는 수행하지 않았다.

## 2. Byte freeze

지정 text-source byte inventory:

- `Codex/results/PHASE_044_SOURCE_FREEZE_MANIFEST.json`
- `Codex/results/PHASE_044_LINEAGE_DIFF.json`
- inventory files: 1,386
- unique byte contents: 777
- duplicate path instances: 609
- resolved current-release TeX sources: 56
- resolved TeX input edges: 55

대상 suffix는 `.csv`, `.html`, `.json`, `.md`, `.py`, `.tex`, `.txt`다.
PDF, PNG, NPZ 등 binary artifact는 이 1,386 count와 visual QA 범위에
포함되지 않는다. 이 inventory는 지정 text source의 누락·중복을 찾기 위한
기계 목록이며, 목록 등재 자체는 전문 독해 증거가 아니다. 전문 독해 범위는
다음 절에 별도로 기록한다. lineage diff도 “바뀐 byte”만 말하며 그 변화의
과학적 타당성을 판정하지 않는다.

주요 현행 source:

| Source | Lines | SHA-256 |
|---|---:|---|
| `graphite_ica_ch1_codex_candidate_v5.tex` | 991 | `018ab9508a29fe40c38b08bc4ab2a11f866c6384e7bfc00eef7418e29d47a95e` |
| `graphite_ica_ch2_codex_candidate_v1.tex` | 854 | `36fcbe92a596a2b0d4649d4aa884ba3c21735f4586bd393faca00ebadeb97bca` |
| `graphite_ica_ch3_codex_candidate_v1.tex` | 787 | `1994c7cb629332add97a64b62e65294c2a310d80ec3f433c842a71d07ef2a6db` |
| `graphite_ica_ch4_codex_candidate_v1.tex` | 863 | `07e6de7f7081f51058f92220a44550d4448d61e6a10f142670fa3de9edf9f3e6` |
| `graphite_ica_ch5_codex_candidate_v1.tex` | 825 | `ef552427cc430d0c9ea7e94615deff546c98ad58ec12adab0130550a49821159` |
| `Anode_Fit_v1.0.24.py` in v1.0.25.2 | 2,004 | `eaa019f6a2f73d9274fbeea6211fa645d1e734ae98e490efbd473196f4a12746` |
| `CODE_GUIDE_v24.md` in v1.0.25.2 | 374 | `098c00cf7424b723c35ddde5dcd26109889f919129d7595eb7df0e687d20537d` |
| `FITTING_GUIDE.md` in v1.0.25.2 | 137 | `f7ca9038e163cfba6313f85e0cd4f3095ac2890a9ff9eb6f8aa4a8cdf12409e1` |
| `HANDOVER_v1025_2.md` | 132 | `881f8c0b6d8934513b6e4e329c345d444854d63bb86ec09526e987e8ab5e1aa1` |
| `build_two_versions.py` | 223 | `70c50cadfe4c8b170612e275fccfbf7714cef42d9889588cf8316629f9db16ab` |
| `regsol_kernel.py` | 108 | `ed10c8fc2029e874803ff3b9d208817fb735b75ca71f8e8fd2fe3631870c455e` |
| `summary_versions.json` | 873 | `edcafd90b91b6515ca12dca3743678055bc021a52cff3a86a2355467afe8dedc` |
| `C_skew/params_blend.json` | 101 | `c4ba2e46d515eddbbdc4c5d8f3310a9ab90fc8b777e0def0177a22ad127f125e` |

기존 Phase 038/040 문건에 기록된 일부 SHA가 위 현행 byte의 SHA와 다르다.
그러므로 그 문건의 10-pass/build 기록은 당시 대상에는 유효할 수 있어도,
현재 byte를 검증했다는 증거로 재사용할 수 없다.

## 3. Full-read coverage

### 3.1 Codex candidates and their governance

전문 독해:

- Chapter 1 candidate: lines 1--991
- Chapter 2 candidate: lines 1--854
- Chapter 3 candidate: lines 1--787
- Chapter 4 candidate: lines 1--863
- Chapter 5 candidate: lines 1--825
- Phase 038--043 result and planning documents: each file, first line to EOF

부분 발췌만 읽은 후보를 전문 독해로 계수하지 않았다.

### 3.2 Current v1.0.25.2 manuscripts

master 세 본과 모든 recursive `\input` source를 EOF까지 읽었다.

- graphite master plus common preamble, graphite sections, Part-T sections,
  appendices and bibliography
- LCO master plus notation, LCO sections and bibliography
- Si/blend master plus notation, evidence map, material cases, regular-solution
  discussion, blend construction, mechanics, implementation appendix and
  bibliography

기계 include 해석 결과는 56 files / 55 edges이며 unresolved input은 없다.

### 3.3 Current implementation and fit provenance

전문 독해:

- release implementation, 2,004 lines
- code guide, 374 lines
- fitting guide, 137 lines
- v1.0.25 and v1.0.25.2 handover/change/data ledgers
- v1.0.24 and v1.0.25 gate programs
- accepted fit builder, 223 lines
- builder가 top-level 또는 fit 경로에서 import하는
  `test_skew_regsol_v2.py`, `test_gallery_vs_regsol.py`, `bdd_dqdv.py`,
  `regsol_kernel.py`
- stored 8-decimal and presentation 6-decimal parameter artifacts
- active preprocessing, seed/bound, RNG/restart와 kernel dependency bodies

과거 v1.0.10--v1.0.25.2의 version-local authority 문건과 계획서에 대한
version-by-version evolution table은 duplicate hash를 이용해 동일 byte를
한 번만 판독하는 방식으로
`PHASE_044_V1010_V1025_2_LINEAGE_REVIEW.md`에 정리했다.

## 4. Independent stored-8dp empirical-profile reconstruction

검증 도구:

- `Codex/work/v1025_2_physics_branch/phase044_current_source_probes.py`
- `Codex/results/PHASE_044_CURRENT_SOURCE_PROBES.json`

현재 reconstruction 환경:

- Python 3.12.13
- NumPy 2.3.5
- pandas 2.2.3
- SciPy 1.17.0

이는 보존된 vector를 재계산한 현재 환경이다. 원 optimizer run의 package
environment, termination status, Jacobian, evaluation count와 unrounded state는
저장되어 있지 않다.

입력 SHA-256:

| Data | SHA-256 |
|---|---|
| graphite `gr.csv` | `0deb5d1222ca944eaf128c39ca5b35f59929219a6d9445771088baf2222c39d9` |
| silicon `si.csv` | `8b02c776bc34e8410d86fead875d485905b78b28351ca6b295e433b78ff43ac6` |
| blend `sigr.csv` | `e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6` |

blend preprocessing observed from the executable body:

1. finite rows
2. capacity sort and duplicate-capacity collapse
3. isotonic regression of \(V(Q)\)
4. uniform 0.5 mV voltage rebinning over 0.060--0.700 V
5. positive longest run
6. Savitzky--Golay ensemble

driver의 머리말에 있는 dMSMCD/wavelet 설명은 이 active body가 실제로
수행하는 연산이 아니다.

accepted blend result:

| Item | Result |
|---|---:|
| processed points | 1,280 |
| transitions | 14 skew-logistic |
| free parameters | 57 |
| stored 8-decimal observation baseline | 0.5169124 mAh/V |
| stored-8dp recomputed \(R^2\) | 0.99964941790404 |
| stored-8dp recomputed BIC | -4760.653827485789 |
| builder-computed-from-best rounded \(R^2\) | 0.99965 |
| builder-computed-from-best rounded BIC | -4760.7 |
| frozen stored-8dp release path vs independent direct formula, max abs | \(1.42\times10^{-14}\) mAh/V |
| stored-8dp vs presentation-6dp curve, max abs | 0.0069744215 mAh/V |

판정:

- **stored-8dp vector의 archived curve 표현: CONFIRMED**
- **frozen \(s=+1\) static profile에서 release path와 direct formula의
  numerical conformance: \(1.42\times10^{-14}\) mAh/V**
- **original optimizer convergence/global optimum: NOT ESTABLISHED**
- **original optimizer reproduction: NOT AVAILABLE**
- **14항 각각의 phase/host 귀속: NOT ESTABLISHED BY THIS FIT**
- **열·동역학 파라미터의 식별: NOT ESTABLISHED BY THIS FIT**

`build_two_versions.py` lines 99--114는 metrics와 `pred`를 optimizer의
`best`에서 계산한 뒤, `best` 자체는 소수 8자리로 반올림해 `params`에
넣는다. lines 204--206은 당시 `pred`를 summary에서 제외한다.
`params_blend.json`의 transition은 다시 소수 6자리다. 따라서:

- 원 optimizer full-precision vector와 당시 prediction은 남아 있지 않다.
- 보고된 metrics는 builder가 당시 `best`와 `pred`에서 계산해 반올림한
  값이다. builder는 `r.success`를 확인하지 않았고 termination/Jacobian/nfev를
  보존하지 않았다.
- 아래 재계산 metrics/hash는 **저장된 8-decimal vector**의 결과다.
- 현 artifact로 optimizer 원본의 exact reproduction을 주장할 수 없다.

BIC는 smoothing으로 상관된 residual에 i.i.d. Gaussian working likelihood를
적용한 builder 내부 비교량이다. 독립 오차에 대한 엄밀한 evidence로
해석하지 않는다.

Little-endian float64 canonical hashes:

| Array | SHA-256 |
|---|---|
| voltage | `6c7ca15d7b9eaf80561d2d2d834856c9b3076f31f6d7e4e6ce304ddb266020b4` |
| observed dQ/dV | `da0beeb95e2eac332e870e2a342354109f611503d5641a6c3c3045871f9d791e` |
| stored-8dp 57-parameter vector | `08216da1095a02bcb789a60f577f4afd1d581ad659a8129edaba7dc0dc5910d5` |
| stored-8dp reconstructed prediction | `53cc3c3795be327b90a5d040497074bc51f5a141d0b7629bd34a60682d71f800` |
| stored-8dp reconstructed residual | `1b874701ac72403f2836b352386e3c3a4f658c49238fd2fcf0a4931fd79398ec` |

## 5. Highest-severity findings

### F-001 — Width is not electron stoichiometry

Severity: `BLOCKER`

Codex Chapter 3 candidate lines 410--447은

\[
n_j^{\mathrm{eff}}=\frac{RT}{Fw_j}
\]

를 effective electron number로 정의하고, Chapter 4와 5는 이를
\(n_j^{\mathrm{eff}}I_j\eta_j\)에 곱한다.

이 식은 logistic exponent의 기울기를 전기화학 affinity 항에 전부
귀속시켰을 때 얻는 parameterization일 뿐, 전자 화학양론의 유도가 아니다.
전자수 \(z_j\)는 반응식과 Faraday 법칙이 정하고, \(w_j\)는 열역학 isotherm,
정적 heterogeneity, 분해능, 현상학적 skew 등에 따라 변할 수 있다.

실제 기본값 중 \(w=0.158\) mV를 넣으면 위 수는 약 162.6이다. 이를 한
Li 반응의 전자수로 읽는 것은 물리적으로 허용되지 않는다.

수정:

- reaction stoichiometry \(z_j\)와 broadening/slope parameter를 분리한다.
- \(z_j=1\)인 Li insertion reaction을 기준으로 Faraday 변환을 한다.
- Chapter 4의 raw network entropy-production 식은 보존하되,
  \(n_j^{\mathrm{eff}}I_j\eta_j\) 환원은 삭제하고 독립 affinity로 다시 유도한다.

### F-002 — Reversible-heat sign contradiction

Severity: `BLOCKER`

Codex Chapter 2 candidate lines 319--371은 source-positive를 heat generation으로
선언한 뒤

\[
\;I_jT\frac{\partial U_j}{\partial T}
\]

를 쓰면서 \(I_j>0\), \(\partial U_j/\partial T>0\)을 흡열이라고 설명한다.
식과 문장이 같은 부호 규약에 있지 않다.

현행 구현 lines 973--984는

\[
\dot Q_{\mathrm{rev,gen}}=-IT
\left(\frac{\partial U_{\mathrm{OCV}}}{\partial T}\right)
\]

를 사용한다. heat-generation-positive와 고정된 signed-current 규약에서는
후자가 정합한다. 다만 half-cell entropy coefficient를 electrode-local heat에
어떻게 배분할지는 reference/counter electrode와 interface를 포함한 별도
control-volume 정의가 필요하다.

### F-003 — Charging reverses the trajectory, not the state definition

Severity: `BLOCKER`

Codex Chapter 5 candidate lines 228--354는 동일한 물리 상태 \(\xi_j\)를
유지한다고 선언한 뒤, 충전에서 logistic orientation 자체를 뒤집는다.
고정된 state coordinate라면 같은 equilibrium map을 역시간 방향으로 따라야
하며, 방향은 signed extent rate/current가 담당한다.

branch metastability는 다음처럼 표현할 수 있다.

- branch-dependent free-energy landscape or center
- nucleation/pinning state
- signed flux toward a branch-local target

그러나 동일 \(\xi\)의 의미를 유지하면서 \(V\mapsto\xi\)의 orientation을
branch마다 뒤집어서는 안 된다. 그 뒤에 붙은 충전 발열 부호 증명도 함께
재유도해야 한다.

또한 chemical storage는
\(Q_{\mathrm{chem}}=Q_{\mathrm{bg}}^{\mathrm{chem}}+\sum_j a_j\xi_j\)처럼
signed coefficient \(a_j\)로 써야 한다. archived fit preprocessing은
미분 profile의 magnitude를 취하므로 양의 fitted area만으로 \(a_j\)나
reaction orientation을 복원할 수 없다. fixed-sign observation map일 때만
full-window area가 \(\epsilon_{\mathrm{obs}}a_js_j\)로 연결된다.

### F-004 — Chapter 1 small-tail ICA expansion is dimensionally wrong

Severity: `BLOCKER`

Chapter 1 candidate lines 738--806의 exact expression은

\[
\frac{\mathrm dQ}{\mathrm dV_n}
=
\frac{C_{\mathrm{bg}}^{\mathrm{chem}}}
{1-Q_p\,\mathrm d\Theta/\mathrm dQ}.
\]

작은 꼬리에서 올바른 1차 excess는

\[
\Delta\!\left(\frac{\mathrm dQ}{\mathrm dV_n}\right)
\simeq
C_{\mathrm{bg}}^{\mathrm{chem}}\,
\frac{Q_p}{Q_{\mathrm{cell}}}\,
\frac{\Theta_0}{L}
\exp[-(q-q_a)/L].
\]

여기서
\(C_{\mathrm{bg}}^{\mathrm{chem}}
=\partial Q_{\mathrm{bg}}^{\mathrm{chem}}/\partial V_n\)은 chemical-storage
derivative이며 empirical fit의 observation baseline이 아니다. 후보 lines
805--806의 \(Q_p/C_{\mathrm{bg}}\) 계수는 위 exact 식의 전개와
다르고 차원도 \(dQ/dV\)가 아니다.

또한 denominator가 음수가 되는 데이터를 “피팅에서 제외”할 것이 아니라,
그 조건에서는 단조 좌표변환/모형 admissibility가 깨졌다고 판정해야 한다.

### F-005 — OCV basis and transition-entropy basis are not generally equal as written

Severity: `MAJOR`

Chapter 2 candidate lines 432--458의 정합식은 단일 transition에서도 일반적으로
성립하지 않는다. 예를 들어

\[
V_{\mathrm{OCV}}=U(T)+w(T)\operatorname{logit}\xi
\]

이면 fixed state에서

\[
\left.\partial_TV_{\mathrm{OCV}}\right|_\xi
=U'(T)+w'(T)\operatorname{logit}\xi.
\]

후보의 transition entropy 우변은 \(U'\)에 해당하는 standard reaction
entropy만 갖고 두 번째 configurational/state-dependent 항을 빠뜨린다.
\(\xi=1/2\) 또는 \(w'=0\) 같은 특수 조건 외에는 두 basis가 같지 않다.

수정은 둘 중 하나다.

- OCV coefficient 하나를 정본으로 사용한다.
- transition basis를 쓸 경우 partial-molar/configurational entropy를 포함해
  fixed-state derivative에서 다시 유도한다.

### F-006 — Chapter 4 has useful network physics but is the wrong chapter

Severity: `MAJOR`

Chapter 4 candidate lines 344--373의

\[
\frac{Q_j}{z_jF}RT(J_j^+-J_j^-)\ln(J_j^+/J_j^-)\ge0
\]

구조는 보존 가치가 있다. 단,
\(J_j^+=r_j^+(1-\xi_j)\), \(J_j^-=r_j^-\xi_j\)인
\(\mathrm s^{-1}\) occupancy flux를 먼저 정의하고, \(Q_j\)를 C 단위로
변환해야 식이 W가 된다(mAh이면 \(\times3.6\), Ah이면
\(\times3600\)). 또한 explicit
\(\xi_{\rm ss}=r^+/(r^++r^-)\)는 \(r^\pm\)가 state-independent 또는
locally frozen일 때만 성립한다. 그 밖에도:

- 이를 \(n_j^{\mathrm{eff}}I_j\eta_j\)로 환원한 부분은 F-001에 의존한다.
- \(T\dot S_{\mathrm{irr}}\)를 모두 local heat로 놓으려면 등온·local-equilibrium
  및 unresolved energy storage 부재를 명시해야 한다.
- Chapter 2의 irreversible heat, 별도 relaxation heat, transport heat와
  겹쳐 셀 가능성이 있다.
- 프로젝트 장 구조상 Chapter 4는 integrated EOS/DAE여야 하는데 현재 후보는
  두 번째 heat chapter다.

따라서 raw network entropy-production 유도는 Chapter 2의 advanced section
또는 별도 이론 절로 옮기고, Chapter 4는 전하보존--평형--속도--열--관측을
결합하는 통합 방정식 장으로 다시 작성한다.

### F-007 — The current empirical skew observation map is absent from candidates

Severity: `MAJOR`

현행 empirical kernel은

\[
q_{\mathrm{shape}}=\sigma^\alpha,\qquad
\partial_Vq_{\mathrm{shape}}
=\frac{\alpha}{w}\sigma^\alpha(1-\sigma)
\]

를 사용한다. Codex Chapter 2--5 후보는 대부분 \(\alpha=1\) logistic만
상속한다. 이 불일치는 \(\alpha\)를 thermodynamic state에 넣어 해소할 것이
아니라, 현행 empirical observation profile을 별도 module로 보존해 해소한다.
그 module의 amplitude \(A_j\ge0\)는 positive observation area이고 signed
chemical storage coefficient \(a_j\)가 아니다. 특히 현재 absolute
preprocessing 뒤에는 관측 부호가 소실되므로 \(A_j\)에서 \(s_j\)나
reaction direction을 추론하지 않는다.

observation-coordinate의 algebraic inverse는

\[
V=U+w\log\frac{q_{\mathrm{shape}}^{1/\alpha}}
{1-q_{\mathrm{shape}}^{1/\alpha}},
\]

이고 \(\alpha(T)\)를 경험적으로 허용할 때의 profile sensitivity는

\[
\partial_Tq_{\mathrm{shape}}
=
\alpha\sigma^{\alpha-1}\partial_T\sigma
+\sigma^\alpha\ln\sigma\,\alpha'(T)
\]

가 된다. 이는 chemical potential inverse나 reversible entropy 식이 아니다.
\(\alpha\)는 tier-C shape parameter다. accepted
blend14에서는 \(\alpha=0.1540\ldots\sim7.7007\ldots\)이며 최소 폭
1.94054 mV는 0.5 mV grid보다 넓고, stored-8dp 폭 하나가 수치상
0.12 V 상한과 같다.
반면 standalone graphite7에는 0.25 mV grid 이하 폭이 있고 standalone
Si7에는 stored-8dp \(\alpha=0.15,8.0\) 값이 수치상 양 bound와 같다.
원 optimizer의 full-precision vector와 active-set 상태가 없으므로 이를
실제 optimizer bound hit로 단정하지 않는다. profile별 식별성 경고를 섞지
말고, \(q_{\mathrm{shape}}\)를 physical occupancy, charge-balance state 또는
heat state로 재사용하지 않으며 observation/broadening layer에 격리해야
한다.

### F-008 — Spectrum amplitude and normalized kernel measure are mixed

Severity: `MAJOR`

Chapter 1 candidate는 normalized mode weight와 tail-start residual amplitude를
같은 \(A_L\)에 흡수한 뒤, 한 곳에서는 \(\int A_L\,dL=1\)인 kernel로,
다른 곳에서는 amplitude-bearing tail spectrum으로 사용한다.

분리:

\[
a(L)=\frac{Q(L)p(L)}{Q_p},\qquad \int a(L)\,\mathrm dL=1,
\]

\[
\Theta(q)=\int a(L)\xi_L(q)\,\mathrm dL,
\]

\[
K(\Delta q)=\int a(L)L^{-1}e^{-\Delta q/L}\,\mathrm dL.
\]

tail-start residual은 \(b(L)=a(L)r(q_a;L)\)처럼 별도량으로 둔다.

### F-009 — Thermal-tail “mirror” is not a valid derivative

Severity: `MAJOR`

Chapter 2 candidate의 thermal mirror는 heat power와 \(q\)-derivative를
혼용하고, \(k\propto1/L\)에 이미 들어 있는 \(1/L\)을 “없다”고 해석한다.
단일 mode에서 \(e^{-2\Delta q/L}\) 모양이 나올 수 있다는 정성적 FLAG만
남기고, power/energy/derivative와 prefactor를 다시 유도해야 한다.

### F-010 — Actual fit defaults are not the accepted blend fit

Severity: `MAJOR`

현행 release code:

- `DEFAULT_GRAPHITE_TRANSITIONS`: 7
- `DEFAULT_SI_TRANSITIONS`: 7
- constructed blend observation baseline: 0
- declared fitted observation-baseline constants: graphite 0.550, Si 0.051

독립 probe:

- current default와 accepted stored-8dp vector는 둘 다 14×4 parameter
  array라 dimensions만 동일
- serialized file order에서 exact equality는 false
- component-aligned 거리값은 보고하지 않는다. generic fit에는 host label과
  canonical component order가 없고, physical blend는 standalone host
  profile에서 Si capacity를 다시 scale하므로 position-wise subtraction이
  model-invariant 비교가 아니기 때문이다.

원인:

- 기본 7+7은 독립 graphite fit과 독립 Si fit을 host별로 가져와
  \(f_{\mathrm{Si}}\)로 용량을 다시 배분한다.
- accepted blend 14는 blend data에 하나의 generic 14-component mixture를
  직접 fit한 것이다.
- 후자는 host label, common-potential balance, \(f_{\mathrm{Si}}\) constraint를
  fit objective에 갖지 않는다.

동일한 processed blend data에서 default 7+7의 transition은 고정하고
\(f_{\mathrm{Si}}\in[0,0.99]\), \(B_{\mathrm{obs}}\ge0\) 두 값만 unweighted
least squares로 다시 맞추면:

- \(f_{\mathrm{Si}}=0.58122565\)
- \(B_{\mathrm{obs}}\simeq0\)
- \(R^2=-1.61321666\)

가 된다. 반면 stored-8dp direct14는 \(R^2=0.99964942\)다. 이 수치는 두
model의 과학적 우열 비교가 아니다. standalone host data에 맞춘 physical
7+7과 blend data에 직접 맞춘 generic14는 목적함수가 다르기 때문이다.
다만 **성공한 direct14 fit이 shipped default로 배선되어 있지 않다**는
문건--코드 불일치를 직접 확인한다. 따라서 “default blend 14 = accepted
blend fit”이라는 문장을 삭제한다.

### F-011 — The claimed threshold derivative divergence omits a cancellation

Severity: `MAJOR`

Si regular-solution section lines 213--219는 Maxwell gap을 broaden한
\(\mathrm dQ/\mathrm dV\)가 \(\Omega\to2RT^+\)에서 값은 연속이지만
\(\Omega\)-도함수는 발산한다고 쓴다. 근거는 gap mass
\(m=1-2\theta_a=O(\sqrt{\Omega/RT-2})\) 하나다.

그러나 두상식은 gap에 \(m\,\kappa(V-U^\circ)\)를 더하는 동시에
single-phase 적분에서 질량 \(m\)인 중앙 조성구간을 제거한다. 문턱에서 그
구간의 전위가 \(U^\circ\)로 모이므로 제거되는 leading 항 역시
\(m\,\kappa(V-U^\circ)\)이고, 제곱근 항이 상쇄된다. 문건 식을 그대로
Gauss--Legendre 적분한 독립 검산에서도

\[
\max_V|P_{2+\epsilon}(V)-P_2(V)|/\epsilon
=5.869,\ 5.896,\ 5.8988,\ 5.89911\ \mathrm{V^{-1}}
\]

로 \(\epsilon=10^{-2},10^{-3},10^{-4},10^{-5}\)에서 유한값에 수렴했다.
따라서 식의 면적보존과 값의 연속성은 보존하되, “매끄럽지 않음/도함수
발산” 문장과 그 검산 판정은 삭제한다. 이 closure 자체의 production
지위는 계속 `THEORY-ONLY`다. 재현 도구와 출력은
`phase044_regsol_threshold_probe.py`와
`PHASE_044_REGSOL_THRESHOLD_PROBE.json`에 동결했다.

## 6. Current-code conformance defects

### 6.1 Keyless width temperature derivative

`n`과 `w`가 모두 없는 transition에서:

- `_width`: \(RT/F\)
- finite-difference \(dw/dT\): \(8.61688345\times10^{-5}\) V/K
- `_dwdT`: 0
- \(U_{\mathrm{oc}}(x,T)\) finite-difference:
  \(-9.46661405\times10^{-5}\) V/K
- reported entropy coefficient: 0

같은 transition의 width contract가 두 경로에서 다르다.

### 6.2 C-rate time unit

`curve()`는 C-rate를 \(1/\mathrm h\)로 받아 \(I/Q\)에 넣지만,
Eyring factor \(h/k_B\)는 SI seconds다. 같은 물리 rate를 hour basis와
second basis로 넣은 \(L_q\) 비는 약 3600이다.

이 3600은 temperature-independent prefactor이므로 다온도 Eyring
해석에서는 activation entropy/intercept가 보상하는 항이다. \(\Delta H_a\)를
고정하고 legacy hour profile을 physical second profile로 바꾸면

\[
\Delta S_a^{\mathrm{phys}}
=\Delta S_a^{\mathrm{legacy}}-R\ln3600
\simeq\Delta S_a^{\mathrm{legacy}}
-68.081\ \mathrm{J\,mol^{-1}\,K^{-1}}.
\]

\(\Delta S_a\)를 고정한 단일온도 298.15 K fit에서만
\(RT\ln3600=20.298\) kJ/mol을 apparent \(\Delta H_a\) offset으로 쓸 수
있으며, 이 값은 \(T\)에 따라 달라져 물리 enthalpy correction이 아니다.
현 code lines 183--186의 enthalpy-only 설명도 수정 대상이다. compatibility
profile과 SI physical profile을 분리해야 한다.

### 6.3 Nominally stable logistic still warns

`np.where`가 두 branch를 모두 eager-evaluate하여 nominal input에서
overflow 두 건과 invalid divide 한 건을 낸다. 출력은 유한하지만
warnings-as-errors 환경에서는 실패한다. indexed stable branch로 바꿔야 한다.

### 6.4 Trajectory is replaced by a sorted voltage set

`dqdv()`는 입력을 방향별 전압 순서로 정렬한다. 따라서 nonmonotonic acquisition
history는 소실된다. 이 경로는 monotonic single branch로 제한하고,
진짜 trajectory는 time-ordered API로 분리해야 한다.

### 6.5 Variable-temperature path is only partially pointwise

평형 width/center는 \(T(V)\)를 pointwise로 사용하지만, branch shift와 lag length는
평균 \(T\) 하나로 평가한다. 문건에 local-constant approximation으로 한정하거나
trajectory solver를 구현해야 한다.

### 6.6 Finite causal padding is not an exact natural boundary

5\(L\) padding의 미소거 residual은 \(e^{-5}=0.0067379\), 약 0.67%다.
이는 \(-\infty\) 자연경계를 “실현”한 것이 아니라 finite prehistory
approximation이다. 중복된 첫 전압점이면 padding point가 0이 되는 edge도 있다.

### 6.7 Invalid material case can pass silently

현재 default Si transition list가 존재하면 `si_case` validation branch를
우회하므로 존재하지 않는 case 문자열도 생성자가 받아들인다.

### 6.8 Global compatibility switches are mutable shared state

두 문제를 구분해야 한다.

- transition legacy toggle은 module-level default pointer를 바꾼다. 이미
  생성된 instance는 자신의 transition list와 그에 대응하는 `seed_L_V`를
  유지하므로 이 toggle만으로 within-instance stale mismatch는 확인되지
  않았다. 그러나 이후 생성되는 instance는 process-global 호출 순서에
  의존한다.
- `use_si_constants()`는 module-global \(R,F\) 자체를 재바인딩한다. 이후
  기존 instance의 계산에도 새 상수가 들어가지만 생성 때 cache한
  `seed_L_V`는 재계산하지 않는다. 이 경로에는 실제 within-instance
  mixed/stale convention이 생긴다.

상수계와 transition profile을 모두 explicit immutable profile로 바꿔야 한다.

### 6.9 Inline default/profile documentation is internally stale

Release code lines 1372--1388은 graphite7을 “opt-in”, legacy4 default
unchanged, alpha key absent라고 설명한다. 그러나 바로 아래 list lines
1393--1399에는 alpha가 있고, lines 1431--1432는 graphite7+Si7을 default로
지정한다. 같은 주석의 “alpha 7개 중 5개가 상한 8.0 포화”도 stored-8dp
graphite7 stored-8dp 최대 \(7.99623012\)와 다르며 upper bound와 정확히
같은 stored 값은 0개다. 원 optimizer의 active-set 상태는 알 수 없다.

이는 계산 동작과 별개인 사소한 문체 문제가 아니다. profile의 default
지위와 identification evidence를 정반대로 설명하므로, 지정 implementation
section의 authoritative profile table에서 source-derived 값으로 다시
생성해야 한다.

### 6.10 Lumped irreversible heat has no sign/domain guard

Release code lines 1116--1124에는
\(I(U_{\mathrm{oc}}-V)\) terminal polarization heat가 구현되어 있다. 따라서
“irreversible heat 구현 없음”이라고 쓰는 것도 부정확하다. 그러나 함수는
docstring의 \(\ge0\)를 검사하지 않고 signed current/potential convention,
one-path terminal domain, rest internal relaxation과 hidden energy storage
제외를 강제하지 않는다.

이 함수는 좁은 terminal lumped approximation으로 `PARTIAL`이다. local
forward/backward network entropy production의 구현도 아니며, 별도
relaxation heat와 함께 쓸 때 double counting을 막는 integrated energy
balance도 없다.

## 7. What is preserved

다음은 폐기 대상이 아니다.

- skew-logistic derivative와 empirical cumulative profile의 전구간 면적보존
- surviving stored-8dp 14-peak empirical fit
- graphite/Si host를 공통 전위축에서 합성하는 1차 equilibrium architecture
- \(f_{\mathrm{Si}}\to0\) graphite recovery
- fixed-\(q\) implicit OCV derivative의 기본 발상
- reaction entropy와 activation entropy의 분리
- forward/backward mass-action skeleton
- network entropy-production의 nonnegative structure
- reversible/irreversible heat의 개념 분리
- \(R_n\)과 thermal resistance를 구분하는 서술
- identifiability/falsification hierarchy

다만 각 항목은 이 문서의 수정 조건과 validity domain을 붙여 보존한다.

## 8. Manuscript architecture judgment

권고 정본 구조:

1. Chapter 1 — graphite equilibrium, observation map, charge balance
2. Chapter 2 — thermodynamics and heat
3. Chapter 3 — kinetics with fixed reaction stoichiometry
4. Chapter 4 — integrated EOS/DAE
5. Chapter 5 — hysteresis with fixed state orientation
6. Material applications — graphite, LCO, Si/blend
7. Empirical profile — immutable 14-skew fit
8. Implementation conformance appendix/ledger

현재 v1.0.25.2의 LCO와 Si/blend 장은 삭제하지 않는다. Codex Chapter 2 후보는
LCO 수정판이 아니라 별도 graphite thermal chapter이며, Chapter 4 후보도
통합 EOS가 아니라 두 번째 heat chapter다. 유용한 내용을 맞는 위치로 옮긴다.

## 9. Manuscript-purity rule

사용자 제약을 다음처럼 적용한다.

### Manuscript body에 허용

- 물리량과 상태변수
- 가정과 validity domain
- 유도와 극한
- 차원·부호·보존법칙
- 관측 가능량과 식별 조건
- 재료별 물리 closure
- existence/uniqueness와 admissibility
- stable/metastable branch selection
- 물리적 initial/boundary condition

### 지정 implementation section 또는 외부 ledger에만 허용

- class/function/file/test 이름
- branch/commit/version history
- code-level solver loop, library, tolerance와 numerical guard
- default parameter wiring
- regression output와 pass count
- build procedure

Codex 후보의 “deliverable”, “사용자 논문”, “PhD”, “numerical core”,
code-level root-finding workflow, validation table과 현행 release appendix의
code symbol은 본문 밖으로 이동한다. 단, root의 존재·유일성, admissibility와
stable/metastable branch 선택은 mathematical closure이므로 본문에 남긴다.
물리식 자체를 코드에 맞춰 바꾸지 않는다.

## 10. Existing test results and their limit

Executed on the frozen branch:

- `test_gates_v1025.py`: 9/9 PASS
- `test_gates_v1024.py`: PASS
- independent current-source probe: deterministic JSON match

이 PASS가 증명하는 것:

- alpha=1 compatibility
- skew area/smoothness
- selected causal-window behavior
- legacy regression
- selected blend invariants with explicitly supplied transitions

이 PASS가 증명하지 않는 것:

- production default 7+7 profile
- default background consumption
- accepted stored-8dp blend profile entry point
- invalid `si_case`
- warnings-as-errors stable logistic
- keyless \(w(T)\) round trip
- SI rate-time contract
- nonmonotonic trajectory
- candidate Chapter 1--5의 과학적 타당성

특히 v1.0.24 gate는 시작 시 legacy 4-transition mode를 강제한다. 따라서 그
PASS를 현행 default 7+7 검증으로 읽으면 안 된다.

## 11. Phase gate

현재 gate:

- current v1.0.25.2 source comparison: `PASS`
- stored-8dp empirical profile reconstruction: `PASS`
- original optimizer reproduction: `NOT AVAILABLE`
- prior-audit independence: `PASS`
- v1.0.10--v1.0.25.2 lineage review: `PASS`
- manuscript scientific promotion: `BLOCKED`
- implementation modification: `NOT STARTED`

Lineage result:
`PHASE_044_V1010_V1025_2_LINEAGE_REVIEW.md`.

다음 단계는 재검독 중인 `V1025_2_PHYSICS_DECISION_LEDGER.md`에서 각 blocker의
canonical 물리 선택을 잠그고, architecture candidate에 따라 기존 원문을
보존한 새 manuscript source를 만드는 것이다.
