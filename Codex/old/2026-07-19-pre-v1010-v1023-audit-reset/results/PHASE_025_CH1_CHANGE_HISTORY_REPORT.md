# PHASE 025 - Chapter 1 Change History Report

## Scope

- Base input: $old
- Final candidate: $new
- Base lines: 839
- Final candidate lines: 621
- Base SHA256: 2AFD3B0B4B9D66EE373240A5238673590259F8C366B6257C14F9B702D6909A07
- Final SHA256: 18713FC7A0AC8988CB5F8A60AF67D2060823438930603AD15858DDA8AFF2994A

## 변경 원칙

- Claude rebuilt reference file은 수정하지 않았다.
- Codex working copy를 검토한 뒤 별도 Codex candidate v3를 생성했다.
- LaTeX 본문에는 phase, audit, date, author, 작업 이력 같은 process metadata를 남기지 않았다.
- 변경 이력은 이 report와 phase result/ledger/handover에만 남긴다.

## 1. 문서 언어와 paper-facing metadata 정리

### 변경 전

- 문서 상단에 RB 재구성본, RB plan, Date, Author, Claude-side process metadata가 남아 있었다.
- 계획서 template 영향으로 문서 설명 중 English prose가 과도했다.

### 변경 후

- v3에서 본문은 한글 논리 전개 + English technical terms로 재작성했다.
- \author{}\date{}는 빈 metadata로 두고, 작업 이력은 본문에서 제거했다.
- 서두를 관찰 기반으로 재정렬했다: low-temperature long ICA tail, temperature barrier, electrode-potential-assisted effective relaxation barrier, first-pass fitting approximation.

## 2. Branch/staging convention 수정

### 변경 전

- 방전/delithiation branch를 다룬다고 하면서 lithiation staging order가 그대로 들어와 branch convention이 충돌했다.
- j, xi_j, q 증가 방향이 crystallographic stage order와 섞일 위험이 있었다.

### 변경 후

- j를 crystallographic stage number가 아니라 measured discharge/delithiation branch의 effective peak label로 정의했다.
- xi_j=0 -> 1은 branch-local progress라고 명시했다.
- lithiation literature order와 본 장의 discharge fitting convention을 분리했다.

## 3. chi_j, effective barrier, Butler--Volmer/Marcus 해석 분리

### 변경 전

- Delta G_eff = G - chi A를 도입하면서 BEP/Butler--Volmer/Marcus 근거와 common-mode mobility 해석이 충돌했다.
- chi_j가 Ch.3의 transfer coefficient eta_j와 동일물처럼 적혀 있었다.

### 변경 후

- Chapter 1의 chi_j를 Level-A scalar relaxation-barrier sensitivity로 정의했다.
- chi_j는 Chapter 1에서 eta_j와 동일시하지 않는다고 명시했다.
- Directional forward/backward barrier splitting은 Chapter 3로 넘겼다.
- Chapter 1에서는 equilibrium target은 thermodynamics가 정하고, Delta G_eff는 target에 접근하는 scalar relaxation rate만 바꾸는 것으로 정리했다.

## 4. Spectrum과 kernel의 변수 의미 재정리

### 변경 전

- A_L가 probability spectrum인지 amplitude spectrum인지 문맥마다 달랐다.
- A_L dL을 fraction이라고 했다가, 동시에 non-normalized amplitude로 사용했다.
- Single-mode limit에서 A_L=delta(L-L0)라고 하여 amplitude Theta_0가 빠졌다.

### 변경 후

- p_L(L) = relaxation-length probability density로 새로 분리했다.
- A_L(L) = relaxation-length amplitude spectrum으로 정의했다.
- A_L(L)dL은 해당 length mode들이 post-peak progress amplitude에 싣는 양이라고 설명했다.
- Single-mode limit은 A_L(L)=Theta_0 delta(L-L_*)로 고쳤다.
- Jacobian RT/L과 kernel factor 1/L의 origin을 분리했다.

## 5. Kernel integral 전개 보강

### 변경 전

- Integral이 나오는 이유는 설명되어 있었지만, probability/amplitude 혼선 때문에 무엇을 적분하는지 불명확했다.
- Volterra 정상상태 점검이 A_L normalization을 암묵적으로 요구하는 듯했다.

### 변경 후

- Kernel integral은 residual 자체가 아니라 dTheta_tail/dq의 mode-wise derivative contribution을 합하는 식으로 재정의했다.
- Integration variable, result quantity, amplitude spectrum, kernel factor를 각각 설명했다.
- Self-consistency section을 main proof에서 optional correction 위치로 내렸다.

## 6. Self-consistency / Plan A / Plan B 위치 조정

### 변경 전

- Plan A/B solver machinery가 Chapter 1의 중심 논리처럼 보였다.
- 사용자 JCP paper refs. 6/7의 Fredholm ratio-substitution이 graphite Volterra problem에 직접 이식되는 듯한 위험이 있었다.

### 변경 후

- Plan B는 reference evaluation으로 정의했다.
- Plan A는 optional analytic closure로 정의했다.
- 2017 JCP paper의 Eq. (32)는 Fredholm equation이고 Eq. (34)는 unknown-ratio substitution임을 명시했다.
- 현재 graphite equation은 Volterra equation이므로 formula를 직접 복사하지 않고 controlled ratio-substitution idea만 가져온다고 제한했다.

## 7. ICA/DVA와 fitting observable 보강

### 변경 전

- dTheta/dq가 exponential이면 ICA도 곧 exponential인 것처럼 읽힐 수 있었다.
- 실제 fitting에 쓸 observable이 충분히 명확하지 않았다.

### 변경 후

- Exact reduced ICA relation은 C_bg / [1 - (Q_p/Q_cell)dTheta/dq] 형태라고 명시했다.
- Exponential fitting은 small-tail 및 locally constant baseline approximation에서만 가능하다고 제한했다.
- Fitting observable을 명시했다:
  Y_tail(q) = (dQ/dV)_meas - (dQ/dV)_baseline
- First-pass fitting formula를 명시했다:
  Y_tail(q) approx B exp[-(q-q_a)/L]
- B가 포함하는 scale factors와 L이 shape parameter임을 설명했다.

## 8. C-rate 해석 수정

### 변경 전

- “C-rate가 커질수록 tail이 짧아진다”는 식의 unconditional conclusion이 있었다.
- 이는 L=|I|/(Q_cell k)와 충돌할 수 있었다.

### 변경 후

- C-rate effect는 단일 방향으로 단정하지 않도록 수정했다.
- |I| prefactor는 q-coordinate에서 L을 키울 수 있고, potential-assisted rate increase는 k를 키워 L을 줄일 수 있으며, apparent-axis polarization은 measured peak overlap을 바꾼다고 분리했다.
- 따라서 multi-rate data에서 R_n과 chi_j를 분리해야 한다고 정리했다.

## 9. Arrhenius 및 chi_j extraction 조건 보강

### 변경 전

- ln(1/L) 대 1/T slope를 곧바로 effective enthalpy로 읽는 식이 조건 없이 강했다.

### 변경 후

- Eyring prefactor, entropy term, fixed-drive condition을 추가했다.
- k_0(T)가 독립적으로 알려지지 않으면 absolute single-curve 해석이 아니라 multi-temperature 또는 multi-potential difference를 쓰도록 제한했다.
- partial ln L / partial V_drive = - chi s_phi F / RT는 small-drive window에서만 쓰도록 했다.

## 10. Bibliography와 source grounding 수정

### 변경 전

- 사용자 paper와 refs. 6/7 bibliography가 placeholder 형태였다.
- Ref. 6의 article number가 잘못 적힌 상태였다.

### 변경 후

- 사용자 JCP paper를 다음으로 정정했다:
  K. Lee, S. Lee, C. H. Choi, S. Lee, JCP 147, 144111 (2017), DOI 10.1063/1.5000882.
- Ref. 6을 다음으로 정정했다:
  S. Lee, C. Y. Son, J. Sung, S.-H. Chong, JCP 134, 121102 (2011), DOI 10.1063/1.3565476.
- Ref. 7을 다음으로 정정했다:
  C. Y. Son et al., JCP 138, 164123 (2013), DOI 10.1063/1.4802584.

## Verification Summary

- Static LaTeX gate: PASS
- begin/end balance: PASS
- brace balance: PASS
- duplicate labels: none
- missing refs: none
- missing cites: none
- high-risk process metadata: removed from body
- TeX PDF build: NOT_RUN because xelatex, pdflatex, lualatex, 	ectonic were not found in this environment.

## Remaining Review Items

- Human scientific review should still check whether selected equilibrium target shape matches actual low-rate OCV/GITT data.
- Plan A closure must be benchmarked against Plan B before quantitative use.
- ho_G should remain constrained by independent physical assumptions or forward-model family, not uniquely inverted from a single curve.
