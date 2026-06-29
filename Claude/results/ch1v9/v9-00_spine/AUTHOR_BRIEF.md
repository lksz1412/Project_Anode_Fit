# Ch1 v9 — AUTHOR_BRIEF (9종 경쟁 빌드 입력) [스켈레톤·A.3 후 LCO값 확정]

> competition-cherrypick 스킬. base = `base_v8-11.tex`(1208줄, 흑연 음극 dQ/dV forward 교과서). 9 작가(무통신)에게 동일 배포. **LCO 설계값(전이 파라미터·전자 엔트로피 식)은 A.3 `30_synthesis`·`35_electronic_entropy_design` 확정 후 §"LCO 콘텐츠" 채움.**

## 목표 (한 줄)
Ch1 을 **흑연 음극 + LCO 양극 통합 하프셀 dQ/dV forward 교과서**로 — v8-11 의 흑연 서술·식·부호·그림을 *그대로 보존*하고, 양극(LCO) 설명이 필요한 곳에 절·식을 *추가*. 코인 하프셀(vs Li) 범위. 전셀 합성은 범위 외(후속).

## ★보존 (불가침)
- v8-11 의 흑연 전이 4종(stage4→3 등) 결과·$U_j$·$\Delta S_{\rxn,j}$(+29/0/−5/−16)·부호 사슬·logistic·히스·꼬리·역보간 **변경 0**.
- 식별자·대소문자·코드 인코딩·그림 라벨 보존. 기존 식 번호 흐름 유지(LCO 식은 *추가* 번호).
- 정독 근거 없는 복붙·무수정 금지(무수정도 정독 근거).

## ★추가 (LCO 통합 — A.3 확정값으로)
1. **LCO 전이 파라미터**: 전이별 $U_j^\mathrm{cat}(T)$·$\Delta S_{\rxn,j}^\mathrm{cat}$·Ω·폭 (A.3 표). dQ/dV 위치(~3.9V·~4.05/4.17V·고전압 plateau).
2. ★**전자(electronic) 엔트로피 항**: LCO metal–insulator(@x≲1)·order–disorder(@x≈0.5) → $\Delta S_{e,j}(x)$ (Sommerfeld $S_e\simeq\frac{\pi^2}{3}k_B^2 T g(E_F)$ 형, A.3 확정식). Ch1 프레임에 *새 성분*으로 plug-in — $\Delta S_{\rxn,j}^\mathrm{cat}=\Delta S^\mathrm{config}+\Delta S^\mathrm{vib}+\Delta S_{e}$.
3. ★**ξ_eq 분포 프레이밍 1점 보강**(`CH1_statmech_review.md`): §sec:width 에 "$\xi_\eq$ = 평형 점유 *확률 분포*"($Z=1+e^{-\beta\Delta\mu}$ 단일 자리 점유, Ω=0 Fermi-함수형) 짧은 소절 — kinetic·thermo 두 경로를 *분포* 한 언어로 통합 + LCO 전자(Fermi–Dirac)·Ch2 분포 전개로 가는 다리. (결과식·부호 불변, 유도 추가만.)
4. **forward 코드 LCO 일반화(H)**: 전이 파라미터 교체 + 전자 항 plug-in 으로 같은 클래스 적용 가능함을 서술.
5. **도핑 보정**: pure-LCO 문헌값 = 초기값, 첨가제는 봉우리 smear/shift(Al/Mg 비-redox 안정화) — Ch1 GRAPHITE_STAGING_LIT=초기값 철학과 동일.

## 품질 렌즈 (자체 10회 + 검토)
- **G-derive**: 모든 추가 식 단계 유도(점프·"대입하면 닫힌다" 금지). 전자 엔트로피 식은 분포(Fermi–Dirac/Sommerfeld)에서 유도.
- **부호**: 양극 U 높음(~3.9–4.2V vs Li)·$\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ 부호 사슬 흑연과 1:1 정합.
- **G-follow·G-usable**: 따라가지고, 이 문건으로 LCO ∂U/∂T 산출 가능.
- **완결성·orphan 0**: 추가 절은 앞 도입·뒤 사용. 흑연↔LCO 통합 다리(별도 부록 아님).
- **그림 경쟁**: v8-11 그림 보존 + LCO dQ/dV·전자 엔트로피 신규 그림 후보.
- **KNOWN_DEFECTS**: D-PEAK 등 상속 결함 비전파(8-11 정정 반영).

## 산출 (작가별)
`results/ch1v9/v9-0X/v9-0X.tex` (xelatex 0-err) + 간단 노트(추가 절·전자 엔트로피 식·정독 근거·자체 10회 수렴). 9 작가 = v9-01–03 Sonnet·04–06 Opus·07–09 Codex(단계구동·관찰).

## LCO 확정값 (A.3 — `35_electronic_entropy_design.md`·`30_synthesis_gap.md`)
**전이표(하프셀 코인, U_j vs Li, tier A=Xia)**: T1 MIT ~3.90V(x≈0.94–0.75, 전자항 게이트 ON) · T2 order–disorder a ~4.05V(x≈0.55) · T3 order–disorder b ~4.17–4.20V(x≈0.48). (T4 O3→H1-3 ~4.55V = 고전압, ≤4.2–4.5V 면 범위 밖.) 흑연 4전이와 대칭.

**★전자 엔트로피 항(파생 F)**: $S_e=\frac{\pi^2}{3}k_B^2T\,g(E_F,x)$ (Sommerfeld, Fermi–Dirac 유도). 부분몰 $\Delta S_e(x)=\frac{\pi^2}{3}k_B^2T\,\partial g/\partial x$. **모델 가정**: $g(E_F,x)\approx g_{\max}[1-\sigma((x-x_\mathrm{MIT})/\Delta x_\mathrm{MIT})]$, $g_{\max}=13$ e/eV·$x_\mathrm{MIT}\approx0.85$·$\Delta x_\mathrm{MIT}\approx0.05$(초기값, 피팅 대상). 크기 0.18 kB/atom@x=0.833(O3, tier B) — **작지만 MIT 게이트로 필수**(config 단독 MIT 2상역 재현 불가). ★$\propto T$(상수 ΔS_rxn 과 달리 T-선형) 명시.

**ΔS 분해**: $\Delta S_{\rxn,j}^\mathrm{cat}=\Delta S^\mathrm{config}_j$(logistic 자동·중심 표준값=★이중계산 금지 B)$+\Delta S^\mathrm{vib}_j$(음 baseline)$+\Delta S_e(x,T)$(MIT 게이트, LCO 고유).

**LCO ΔS(x) 정량(tier)**: ΔS_lith max ~9.0 kB/atom(overall)·~4.2(O3내)[Reynier A]; charge-order 0.47(x½)/1.49(x⅔) J/K·mol[Motohashi A]; 단전극 dφ/dT≈+0.83 mV/K[B]. config 가 O3 ΔS 지배(>½).

**코드 일반화(H, 확정)**: MSMR $x_j=X_j/(1+\exp[f(U-U_j^0)/\omega_j])$ = Ch1 transition-logistic **동형** → 전이 파라미터 교체 + 전자항 plug-in 만으로 적용(구조 변경 0).

**도핑**: Al³⁺/Mg²⁺ 비-redox → 전자항 보존·상전이 억제(logistic 폭↑·U_j shift) — pure-LCO 값=초기값, 폭/shift 우리 데이터 피팅.

**갭(문서 명시)**: G1 연속 ΔS(x)·G2 g(E_F)(x)·G3 MSMR LCO 파라미터·G4 도핑 shift = round-trip 피팅. G5 ΔH_f 절대 = OCV plateau anchor. 허위 정밀 금지(tier).

**범위 가드**: 코인 하프셀(LCO vs Li) 단독. 전셀 합성 범위 외. 단전극(+0.83) vs 전셀(부호전환) 혼동 금지.
