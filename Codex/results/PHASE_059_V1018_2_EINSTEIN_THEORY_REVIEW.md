# Phase 059 v1.0.18.2 Einstein 열역학 재유도

정본일: 2026-07-28

판정: `CONDITIONAL_P059_V1018_2_EINSTEIN_THERMODYNAMIC_ALGEBRA_AND_REFERENCE_ROUNDTRIP_PASS_BUT_REACTION_SPECTRUM_AMPLITUDE_AND_IDENTIFIABILITY_SCOPE_FAIL`

## 결론

단일 조화모드의 대수는 맞다. 영점에너지를 제외한
$Z=[1-e^{-\theta/T}]^{-1}$에서
$A=RT\ln(1-e^{-\theta/T})$,
$U=R\theta/(e^{\theta/T}-1)$,
$S=(U-A)/T$를 얻으면 문건 식과 정확히 같다. 영점에너지
$R\theta/2$를 포함해도 entropy는 같고 기준 접선 subtraction에서
상수는 완전히 소거된다.

$T_{ref}$에서 자유에너지의 접선을 뺀 전위 보정도 맞다.
$\Delta U(T_{ref})=0$, $\Delta S(T_{ref})=0$이며
$d\Delta U/dT=\Delta S/F$다. 독립 계산은 $\theta=700$ K에서
278.15/298.15/318.15/348.15 K의 -3.738/0/3.700/9.138
microvolt/K를 재현했다.

## 물리 범위의 한계

현재 항은 “반응의 진동 엔트로피”를 일반적으로 구현한 것이 아니다.
실제 반응량은 lithiated와 delithiated phonon spectrum의 자유에너지
차이다. 현재는 mode multiplicity가 1, amplitude가 $R$로 고정되고,
reactant/product frequency pair와 phonon-DOS 적분이 없다. 따라서
기준온도에 흡수된 baseline 위의 매우 제한된 phenomenological
curvature 항으로만 읽어야 한다.

이 항은 $dS/dT>0$의 부호와 크기가 고정돼 일반적인 spectral
hardening/softening 차이를 표현하지 못한다. 또한 고온에서는
$\Delta S\to R\ln(T/T_{ref})$가 되어 leading order의
$\theta$ 감도가 사라진다. 세 온도점은 곡률에 필요한 최소 조건일
뿐 baseline·electronic slope·width·noise와 함께 안정적으로
식별하기에 충분하다는 보장은 없다.

그러므로 700 K는 capability demo이지 graphite/LCO 물성값이 아니다.
Haruyama et al.의 phonon 계산은 mode-resolved 접근의 필요성을
지지하지만 이 단일-mode 수치를 검증하지 않는다.

## 다음 단계

Step 38.4에서 theta_E 부재 bit-exact, 활성 branch, derivative
round-trip과 실제 equilibrium/dQdV/entropy full-path coupling을
검사한다.

원본 `Claude/`, `main`은 수정하지 않았다.
