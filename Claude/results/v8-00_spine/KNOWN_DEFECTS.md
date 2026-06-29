# v8 알려진 결함 (검토1·체리픽·최종서 반드시 반영)

> v8-04 자체 G-derive 감사가 선적발(나머지 8종도 동일 가능성 — 검토1서 전수 확인). ★는 v7-11 상속(전 v8 공유 추정).

## ★ D-PEAK (eq:peakshape, 수학적 오류·v7-11 상속·최우선)
v7-11 계승 문장 "$L_V$ 작으면 $\xi_\mathrm{lag}\to$ 한 칸 뒤처진 $\xi_\eq$ → $(\xi_\eq-\xi_\mathrm{lag})/L_V$ 가 $d\xi_\eq/dV$ 종으로 환원"은 **틀림**. 점화식 $\xi_{lag,i}=\rho\xi_{lag,i-1}+(1-\rho)\xi_{eq,i}$, $\rho=e^{-\Delta_{grid}/L_V}$:
- $L_V\to0$ ⇒ $\rho\to0$ ⇒ $\xi_{lag}\to\xi_{eq}$(같은 칸) ⇒ peak$\to0$ (종 아님). (수치: L_V=0.3/0.1/0.01 → 0.0025/9e-6/0 vs 참 0.020.)
- $(\xi_{eq}-\xi_{lag})/L_V\to d\xi_{eq}/dV$ 는 **반대 극한 $L_V\gg\Delta_{grid}$**($\rho\to1$)에서 성립.
- 작은 $L_V$ 평형 환원은 *코드의 eq:branch 스위치*($L_V<\nu\Delta_{grid}\Rightarrow \xi_{eq}(1-\xi_{eq})/w$)가 담당 — 매끈한 극한 아님.
**수정**: "L_V 작으면 종 환원" 삭제 → (a) 연속 정당화 $r/L_V=d\xi_{eq}/dV$(quasi-steady)는 $L_V\gtrsim\Delta_{grid}$서, (b) 작은 $L_V$ 평형 회복은 eq:branch 스위치로 명시.

## v8-04 자체 G-derive 추가 결함(전 버전 확인 대상)
- **D-VEQ**: eq:Veq 의 다리 $sF(V_{eq}-U)=g'(\xi)$ 가 §5로 forward-defer(순환). → §5 detailed balance 결과를 앞당기거나 inline 1줄(stationary $RT\ln[\xi/(1-\xi)]=\mathcal A=sF(V-U)$ + 정규용액 $\Omega(1-2\xi)$ 합류).
- **D-DHEFF**: eq:dHeff 의 $\chi_d$ 계수 누락 점프(+Ω 흡수→$-\chi_d\Omega$ 사이 중간식 $r^+=k_0e^{-(\Delta H_a-T\Delta S_a-\chi_d\mathcal A)/RT}$ 필요).
- **D-WEFF**: eq:weff 중심기울기 $sF\,dV/d\xi|_{1/2}=4Fw$ 중간식 누락(이상 $4RT$↔일반 $4Fw^{eff}$ 다리).
- **D-UBR**: eq:Ubranch 는 ansatz(γ·h_η 도입이 유도 아님) → "spinodal 한계 ±½ΔU_hys 위 현상학적 매개변수화"로 명시(유도 가장)하거나 γ 보간 인자 명시.
- **D-VN(minor)**: eq:vn 이항 중간식 없음(자명).
- **fig:overshoot**: 내부 식번호 오기("1.18=1.16"→1.13=1.10=eq:Veq=eq:gpp)·분기 라벨 상하 뒤바뀜·fig:hysloop 와 곡선 데이터 byte 동일(중복). + eq:eyring·bazant2013·dreyer2010 미인용(LOW).

## 적용
- 검토1(Phase 2): 9종 전수로 위 결함 보유 여부 확인(특히 ★D-PEAK 상속).
- 체리픽(v8-10)·최종(v8-11): D-PEAK·D-VEQ·D-DHEFF·D-WEFF·D-UBR 전부 수정한 유도로.
