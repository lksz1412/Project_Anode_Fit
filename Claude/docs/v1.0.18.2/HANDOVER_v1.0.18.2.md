# HANDOVER v1.0.18.2 — 제안1 vib Einstein 양자보정 구현 + 연구 로드맵 (18.1 superset)

## ④ Chain 헤더 (거슬러 올라갈 위치)
- **본 handover** = `docs/v1.0.18.2/HANDOVER_v1.0.18.2.md` (v1.0.18.2 완결 = 물리판)
- 근거 = 이규섭 발전 제안서(`_추출본_v2/S_AnodeFit_v1017_review.md`, 5 물리 확장; 원본 프레임·표준식 검증) + `plans/2026-07-08-v1018-physics-extension-master-plan.md`(§9 2-버전 결정) ← `docs/v1.0.18.1/HANDOVER_v1.0.18.1.md`(이월 완결) ← `docs/v1.0.17/HANDOVER_v1.0.17.md` ← v1.0.16(n(T)) ← …
- 레저 = `results/process/V1018_EXECUTION_LEDGER.md`(P4~P8=18.2). 커밋 = 4ff4440(P4+P5 코드)·54b7f6f(P6 문건)·P8(본).
- 자매판 = **v1.0.18.1**(이월 완결·물리 무변경 = 안전 폴백판). 18.2 = 18.1 superset(+제안1+로드맵).

## ① 본 세션 지시·작업 요약
**지시**: 발전 제안서 + 이월 + 누적 이력 → 2-버전(18.1 이월 / 18.2 +제안1). Opus+Sonnet 로 가능한 모든 건·phase별 commit+push. 9종 체리피킹은 비-Fable. 최종 Fable 검수 best-effort.

**18.2 = 18.1 base + 제안1(vib Einstein 양자보정) 구현 + 제안2~5 로드맵**:
- **P4 증판**: 18.1 → 18.2(버전 bump·계보 18.1). 회귀 bit-exact.
- **P5 코드**(`Anode_Fit_v1.0.18.2.py`): 동결 ΔS_vib → **S_vib(T;θ_E)=R[−ln(1−e^{−x})+x/(e^x−1)]** Einstein. 헬퍼 `_vib_theta`·`_S_vib`·`_vib_dU`(중심 Helmholtz 편차)·`_vib_dS`(발열 엔트로피 편차). equilibrium·dqdv·entropy_coefficient 3곳 동기. **검증**: 회귀 0-DIFF PASS(θ_E 부재=골든 불변)·round-trip ∂vib_dU/∂T=vib_dS/F **diff 0.000000 µV/K**·풀경로 EC=∂U_j/∂T diff 0.0000·고온극한 고전 수렴·demo/sample OK.
- **P6 문건**(9종 체리피킹 Sonnet 9 → master): Ch2 §sec:vibel vib Einstein (a-d) 수식주도(eq:Svib-einstein·eq:dSvib·eq:dUvib) + Ch1 eq:lco-slots 노트 + FITTING_GUIDE §1.6. doc↔code 동기.
- **P7 로드맵**(`ROADMAP_future_physics.md`): 제안2(Ω(ξ))·3(Cahn-Hilliard γ_j)·4(Butler-Volmer 농도분극)·5(PSD 나노) + v1.0.16 물리-데이터 이월 = 외부 위임 과제.
- **P8 마감**: 적대검증 + 3대 무결 + HANDOVER·INDEX.

## ② 다음 세션 주의
1. **제안1 = additive·bit-exact**: 전이 dict 에 `'theta_E'`([K], Einstein 온도; +선택 `'theta_E_Tref'` 기본 298.15) 부재 = 현 동결과 **완전 bit-exact**(골든 불변, v1.0.16 n(T) 방식). **기본 데이터셋(GRAPHITE_STAGING_LIT)엔 θ_E 미부여** — capability + 검증만. 실사용은 다온도 실측 후.
2. **표기**: 문서는 무차원비를 **`u≡θ_E/T`**(리튬 함량 `x`와 충돌 회피)·전이별 `θ_{E,j}`. 코드는 지역변수 `x=theta_E/T`(문서 x와 무관). 자유에너지는 `ΔF_vib`/`f_vib`(Faraday 상수 F와 구별 명시).
3. **★식별 조건**: vib θ_E 와 electronic ∝T 분리에는 **준양자 창 걸치는 T 점 3개 이상** 필요. 2-온도(유한차분·현 파생 A round-trip)는 축퇴(곡률·선형 합으로만) — θ_E 개방은 3온도점↑에서만(FITTING_GUIDE §1.6). "섞일 수 있다"는 저-온도점 진단이지 물리적 비식별성 아님.
4. **round-trip 물리**: ∂U/∂T=ΔS(T)/F 는 ΔC_p 상쇄로 T-의존 ΔS 에도 성립 → 중심 U_j 와 가역열을 **같은 자유에너지에서 짝지어** 보정(한쪽만 고치면 비물리).
5. **코드 무변경분**: 제안1 외 물리·방정식·식별자 불변. 흑연 회귀 assert 유지.

## ③ 미완료/이월
- **제안 2~5**: `ROADMAP_future_physics.md` 외부 위임 과제(차기 후보 = 제안 2 Ω(ξ)). 구현 시 additive+doc↔code+verify 패턴(제안1 선례).
- **v1.0.16 물리-데이터**: 다온도 per-T n 진단·two-phase 폭 T-의존·LCO 실값(실측 대기). ★제안1 θ_E 다온도 회귀와 **같은 데이터** — 폭 n(T)·vib θ_E·전자항 동시 식별.
- **Fable 최종검수**: 맨 끝 best-effort 1회(2% 잔량, 미완 가능) — 최종 Ch1 + 작업이력 검토.
