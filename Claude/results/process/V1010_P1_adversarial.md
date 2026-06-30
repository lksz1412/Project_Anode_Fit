# P1 Step4 — adversarial 재검수 (별도 세션 Opus) 결과

> vN-10 통합본(`V1010_P1_map_v10.md`) vs 코드(703줄). 코드 전문 정독 + self-test 실행 + 독립 수치검산 + 2 검증 sub 삼각 교차. 모든 판정 줄 근거.

## 총평: CRIT/HIGH = 0
물리식·줄·정정·보완·coverage 모두 코드 ground truth와 충돌 0. 정정 4건(MED 1·LOW 2·NOTE)만.

## 정정 (finalizer 반영)
- **M1(MED)**: z_cut docstring 줄 = **L217**(v10은 L218 3곳 인용). L218은 A_cap_RT docstring. → L218→L217 3곳.
- **L2(LOW)**: §2-B 분기 극한 게이트(L444) = `gamma!=0.0 and Omega>0.0` → "γ=0 **또는 Ω=0**"으로 보강.
- **가장 약한 1곳**: §2-F/§2-D seed L_V `4.91e-08~` 인용 — self-test print는 `.4f` 절단으로 `0.0000` 표시 → "(raw 저장값 기준)" 부기로 외관모순 제거.
- **L1(선택)**: 정정 2 등급에 "tex 문건 대조 의존" 부기.

## 확정 정확 (검증 통과 — 배제·정정 불요)
- 물리식 전수 [확정]: func_w(75)·func_U_j(79)·func_ksi_eq(96-97)·func_L_q(102-107)·_causal_lowpass DC gain=1(119-128)·func_dU_hys(139-140)·func_U_branch(148)·func_dH_a_eff(155)·dqdv peak(475). **독립 적분 = 1.000000**.
- 24심볼 + 6메서드 coverage [확정]: 누락 0(전건 줄 MATCH).
- 정정 1 [확정]: equilibrium 분기중심 미적용(362 raw U_j·365 s 미전달=+1), dqdv는 U_branch(444-448) → γ>0서 peak 불일치. self-test 실증 d=+86.9mV(expect +86.7).
- 정정 3 [확정]: A=min(z_cut·n·RT, A_cap·RT)(331), self-test z_cut=2.0(<4)서 binding 실증(2.184e-08→5.325e-08).
- 보완 1 [확정]: func_U_j_hys 死코드(정의 82·미호출). s=1 default vs func_U_branch sigma_d 무default.
- 보완 2 [확정]: equilibrium T 스칼라 전용(352), dqdv T_is_array 분기로 배열 지원.
- 보완 4 [확정]: self-test(567-703) 면적=Q assert 부재(유한성·guards 7/7·iso만).
- 흑연 전용 [확정]·수치검산 [확정]: ΔU_hys(12000)=86.69mV·2RT=4957.64·Ω=2RT→gap 0.
