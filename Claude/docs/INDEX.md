# docs/ INDEX (MOC) — 구조 A (문건=docs / 코드·빌드·조사=results)

> 문서 탐색 진입점. **docs/ = 문건(최종 .tex/.pdf, 버전별 폴더)만**. 코드·빌드과정·조사는 `../results/`.
> 본문이 진실 — INDEX 와 충돌 시 INDEX 를 고친다. 문서 추가·수정 시 같은 턴에 해당 행 갱신.
> ★2026-06-30 구조 A 재정리: 흩어진 결과물을 docs(문건)/results(코드·빌드·조사)로 통일. 구버전·빌드산물 → `docs/_archive/`.

## ★현행 릴리스 — v1.0.16 (폭 다중도 n 의 온도 함수 n(T) 피팅 지원 — fit-n·실측 T·config 전파, 2026-07-06 완주)
> `v1.0.16/` = CLOSING_v1.0.15 Part 4 확정 방향(폭은 n 으로 fit·실측 T·폭 T-의존 4단 사다리·n(T)면 가역열 config 동반) 반영(**P1~P5 완주**·전건 커밋). 코드 = n(T) 선형 지원(additive; 상수 n·n_T1 부재 = v1.0.15 bit-exact)·`_dwdT` ∂w/∂T 전파·배열 T(V) 지원·n(T)≤0 fail-fast. 문건 = FITTING_GUIDE §1.5(fit-n 규약·4단 사다리) + v1.0.15 격자 debt 정정 + Ch1/Ch2 n(T) 수식-주도(신설 eq:dwdT-nT). 골든 불변(상수 n bit-exact). 근거 = `v1.0.15/CLOSING_v1.0.15.md` · 레저 = `../results/process/V1016_EXECUTION_LEDGER.md` · 인계 = `v1.0.16/HANDOVER_v1.0.16.md`.

| 경로 | 1줄 요약 | 동의어 키워드 | 갱신일 |
|---|---|---|---|
| v1.0.16/Anode_Fit_v1.0.16.py | 코드 v1.0.16 — 폭 n(T)=n+n_T1(T−n_T_ref) 선형 지원·신설 _dwdT(∂w/∂T config 전파)·entropy_coefficient/reversible_heat 배열 T·회귀 13/13 bit-exact(상수 n) | 1.0.16, 코드, n(T), _dwdT, fit n, 배열 T, 폭 온도함수 | 2026-07-06 |
| v1.0.16/graphite_ica_ch1_v1.0.16.tex | Ch1 v1.0.16(58p) — eq:wbase 뒤 n(T) 교차참조(∂w/∂T config 전파). v1.0.15 격자퇴출 승계 | 1.0.16, Ch1, n(T), 폭, eq:wbase | 2026-07-06 |
| v1.0.16/graphite_ica_ch2_v1.0.16.tex | Ch2 v1.0.16(16p) — eq:dxidT 뒤 신설 eq:dwdT-nT(폭 n(T) 온도미분 일반화)·use-this box n(T) note | 1.0.16, Ch2, eq:dwdT-nT, config, n(T) | 2026-07-06 |
| v1.0.16/FITTING_GUIDE.md | 가이드 v1.0.16 — 신설 §1.5(fit-n·실측 T·폭 T-의존 4단 사다리·n(T)→config)·격자 debt 정정(ν/min_lag_grid→점별) | 1.0.16, 피팅, fit n, 4단 사다리, n(T), 실측 T, 격자 debt | 2026-07-06 |
| v1.0.16/HANDOVER_v1.0.16.md | v1.0.16 완주 인계 — Chain(CLOSING_v1.0.15 Part4←…)·P1~P5·주의(n(T) additive·배열 T·4단 사다리 실행 대기) | 핸드오버, 인계, chain, n(T) | 2026-07-06 |

## 직전 안정판 — v1.0.15 (이산 전압 격자 완전 퇴출 → 점별 연속 아키텍처 + Ch2 발열 상세화 + Fable 물리 6종 검토, 2026-07-06 완주, superseded by 1.0.16)
> `v1.0.15/` = 균일 작업 전압 격자(리샘플→저역통과 점화식→역보간)를 **아키텍처에서 완전 퇴출**하고 점별 연속 메모리 적분으로 전환한 증판(**P1~P7 완주**·전건 커밋 8de5157→…→P7). Ch1 §1.9 인과 기억 적분(신설 eq:memory/lag/tail-limit/reversal)·코드 dqdv 점별 재작성·그림 점별 재산출 3축 동기. 골든 6종 게이트 검증 후 재캡처. Ch2 worked example(코드-정합)·P2 물리 6종 검토(Codex3+Opus3, 확정 CRIT/HIGH 0)·dead 삭제·격자 param 제거. 마스터플랜 = `../plans/2026-07-05-v1015-code-doc-sync-master-plan.md` · 결과 = `../results/process/V1015_P{1..7}_RESULT.md` · ledger = `../results/process/V1015_EXECUTION_LEDGER.md` · 인계 = `v1.0.15/HANDOVER_v1.0.15.md`. ★주의: staging `'w'`+`'n'` 중복 키(코드 `'n'` 우선 = w=RT/F) 정리는 사용자 판단 대기.

| 경로 | 1줄 요약 | 동의어 키워드 | 갱신일 |
|---|---|---|---|
| v1.0.15/graphite_ica_ch1_v1.0.15.tex | Ch1 v1.0.15(58p, 0-err/ref 0/of>10 0) — §1.9 점별 인과 기억 적분(신설 eq:memory/lag/tail-limit/reversal, 제거 eq:branch/vwork/lowpass)·격자 퇴출·P2-1/3/4·fig 점별 재산출 | 1.0.15, 점별, 격자 퇴출, 메모리 적분, eq:lag, tail-limit, reversal, 9종 체리픽 | 2026-07-06 |
| v1.0.15/graphite_ica_ch2_v1.0.15.tex | Ch2 v1.0.15(16p) — 발열 worked example 신설(코드-정합 U_oc 74.4·∂U/∂T −0.204·q_rev +60.8)·tab:qrev SOC 부호 교대·P2-2/P2-4 caveat | 1.0.15, Ch2, worked example, 가역 발열, entropy_coefficient, config, tab:qrev | 2026-07-06 |
| v1.0.15/Anode_Fit_v1.0.15.py | 코드 v1.0.15 — dqdv 점별 재아키텍처(격자·역보간·_causal_lowpass 제거)·신설 _causal_memory_pointwise·dead 삭제·회귀 13/13·골든 재캡처 | 1.0.15, 코드, 점별, dqdv, _causal_memory_pointwise, 골든 재캡처 | 2026-07-06 |
| v1.0.15/golden_graphite_ref.npz | 점별 코드 재캡처 골든(13 arrays) — equilibrium bit-exact 앵커·dqdv interp 아티팩트 제거 | 골든, 회귀, 점별 재캡처, 6종 게이트 | 2026-07-06 |
| v1.0.15/appendix_phase_separation.tex | 독립 부록(8p) — v1.0.14 승계(격자 무관·무변경) | spinodal, binodal, 부록, 승계 | 2026-07-06 |
| v1.0.15/HANDOVER_v1.0.15.md | v1.0.15 완주 인계 — Chain(KICKOFF←v1.0.14←…)·P1~P7 요약·주의(staging 'w'/'n' 의도설계·골든 재캡처·v1.0.14 폴백) | 핸드오버, 인계, chain, 격자 퇴출 | 2026-07-06 |
| v1.0.15/CLOSING_v1.0.15.md | ★버전 클로징(**다음 버전 착수 전 필독**) — 최상위 헌법 3종(교과서·논문·수식주도)·프로세스 규율(제안 전 과거이력 확인)·재발방지 전수·w/T 피팅 확정 방향(fit n·실측 T·4단 사다리·n(T)→발열 config) | 클로징, 헌법 3종, 수식주도, 재발방지, 과거이력 확인, w 피팅, fit n, n(T), 필독 | 2026-07-06 |

## 직전 안정판 — v1.0.14 (어투·물리 엄밀성·Appendix 재배치·레퍼런스·이미지 경연, 2026-07-04 완주, superseded by 1.0.15)
> `v1.0.14/` = 사용자 피드백 8건(F-A~F-H) 반영 증판(**P1~P6.1 완주** — 검수 R1~R7 누적 정정 ~98건·물리 실결함 0 수렴·그림 경연 72안 중 8승자 편입): eq 1.8 Hill 면밀 유도(Ξ₁·q(T)·ε̃)·PSD 유도-기반 배제·§1.7 폭 예산·부록 A(부호 검산표)/B(구현 대응표)·본문 코드-언급 0·어투 정련·레퍼런스 DOI 병기. 마스터플랜 = `../plans/2026-07-04-v1014-tone-rigor-appendix-figures-plan.md` · 결과 = `../results/V1014_RESULT.md` · ledger = `../results/process/V1014_EXECUTION_LEDGER.md` · 인계 = `v1.0.14/HANDOVER_v1.0.14.md`. ★검토 완료(07-04): spinodal 부록 = 별도 문건 유지 확정·경연 그림 승인(fig15 간격 정정)·후속 = v1.0.15 코드 계획서 GO 대기.

| 경로 | 1줄 요약 | 동의어 키워드 | 갱신일 |
|---|---|---|---|
| v1.0.14/graphite_ica_ch1_v1.0.14.tex | Ch1 v1.0.14(57p, 0-err/ref 0/of 0) — Part 0 Hill 유도·PSD 수치 배제·폭 예산·부록 A/B·경연 승자 그림 8종·cite 병기 | 1.0.14, Hill, Ξ₁, q(T), widthbudget, psdconv, 부록 A, 부록 B, 경연 | 2026-07-04 |
| v1.0.14/graphite_ica_ch2_v1.0.14.tex | Ch2 v1.0.14(14p) — Ξ₁ 통일·q(T) 각주·+29 귀속 한정·Bernardi 전제 명시·keybox 등온선 귀속 | 1.0.14, Ch2, Ξ₁, vib, Bernardi | 2026-07-04 |
| v1.0.14/appendix_phase_separation.tex | ★독립 문건(8p, **별도 유지 확정** — 편입 안 함) — binodal·spinodal·Maxwell·핵생성/CH 자족 유도+그림 2·ξ=θ 배향 주의 | spinodal, binodal, Maxwell, 핵생성, 별도 부록 | 2026-07-04 |
| v1.0.14/Anode_Fit_v1.0.14.py | 코드 v1.0.14 — docstring eq 참조 16곳(원형 보존 구역 불변)·회귀 13/13 | 1.0.14, 코드, eq 참조 | 2026-07-04 |
| v1.0.14/FITTING_GUIDE.md | 가이드 v1.0.14 — Ω 하한 ≥0·χ tier-3·dS_rxn/dVdq_qa 식별 트랩·문턱 70–74 kJ/mol·r_a 정의 | 피팅, 가이드, Ω 하한, χ tier, silent 트랩, 문턱 | 2026-07-04 |
| v1.0.14/HANDOVER_v1.0.14.md | v1.0.14 완주 세션 인계 — Chain(v1.0.12→v1.0.13→본)·검토 결과 반영·이월 목록 | 핸드오버, 인계, chain | 2026-07-04 |
| v1.0.14/HANDOVER_v1.0.15_KICKOFF.md | 세션 마무리 인계 — 검토 반영(fig15·spinodal 별도 유지)+★v1.0.15 계획 rev.3 확정(이산 격자 완전 퇴출·점별 단일 아키텍처, 실행은 차기 세션 GO 후)·주의 7건(원형 보존 orphan·회귀 재정초·문턱 재산출 등) | 핸드오버, kickoff, 격자 퇴출, 점별, v1.0.15 | 2026-07-04 |
| v1.0.14/figs/ | suite·sample·demo 산출 png(V1–V9 검증 패널 포함) | 검증 그래프, suite 산출 | 2026-07-04 |

## 구버전 문건 — v1.0.13 (직전 안정판, superseded by 1.0.14)
> `v1.0.13/` = 사용자 지적 7건 반영판(**P1~P6.1 완주** — Fable 10회 가변-청크 검수 종결, 물리 실결함 3건 정정): Part 0 통계역학 기초 신설·LCO 전부 후방 Part II 통합·산문 압축·용어 영어 원어 정책·overfull 0·문건-코드 루프(σ_d 전극 인지·전자항 T1=0.85 재정렬·스칼라 평형 강제·'w'-단독 config 게이트). 마스터플랜 = `../plans/2026-07-02-v1013-restructure-master-plan.md` · 결과 = `../results/V1013_RESULT.md` · 인계 = `v1.0.13/HANDOVER_v1.0.13.md`.

| 경로 | 1줄 요약 | 동의어 키워드 | 갱신일 |
|---|---|---|---|
| v1.0.13/graphite_ica_ch1_v1.0.13.tex | Ch1 v1.0.13(50p, 0-err·overfull 0) — Part 0(eq:sm-* 24·TikZ 3)+Part I 순수 흑연+Part II LCO 단일 우산(eq:lco-sigmaslot·fig:lco-dirmap)·C-1 Δμ=+sF(V−U) 정정 | 1.0.13, Part 0, 통계역학, Part II, sigmaslot, 재구조화 | 2026-07-03 |
| v1.0.13/graphite_ica_ch2_v1.0.13.tex | Ch2 v1.0.13(14p) — FD 약자 분리·Part 0 교차참조·C-2 각주·revheat/weff 압축·코너(corner case) 병기 | 1.0.13, Ch2, FD, revheat, weff | 2026-07-03 |
| v1.0.13/Anode_Fit_v1.0.13.py | 코드 v1.0.13 — curve() 전극 인지 σ_d 환산(_delith_is_discharge)·LCO 전자항 T1(x_MIT 0.85) 재정렬·회귀 verify 13/13(golden 프로젝트 내) | 1.0.13, 코드, 전극 인지, T1 재정렬, golden | 2026-07-03 |
| v1.0.13/FITTING_GUIDE.md | 가이드 v1.0.13 — §0 전극 인지 규약(charge 라벨 그대로·`direction=+1` 처방 금지 명시)·ν≳10 정정(닫힌꼴, R3)·전자항 0.85 재정렬 완료 반영·§7 suite V1-V9 완비(graph_suite 는 이식 전 v1.0.10 소재 표기)·S0-S5 승계 | 피팅, 가이드, 전극 인지, x_MIT 0.85, ν, graph_suite | 2026-07-03 |
| v1.0.13/sample_test_v1013.py (+.png) | 샘플 2×2 — T1 재정렬 반영(anchor=demo=0.85)·(c) Bernardi 라벨 병기·glyph 0 재검증 | 샘플, 데모, x_MIT | 2026-07-04 |
| v1.0.13/HANDOVER_v1.0.13.md | v1.0.13 완주 세션 인계 — Chain(v1.0.11→v1.0.12→본), 지시 전문·작업 요약·부호 함정 3종 주의·이월 4건 | 핸드오버, 인계, chain, 부호 함정 | 2026-07-04 |
| v1.0.13/graph_suite_v1013.py | V1-V9 검증 suite v1.0.13 이식(v1.0.10 유래 — CODE·figs 경로 현행화) | suite, V8, 검증 그래프 | 2026-07-04 |

## 구버전 문건 — release 1.0.12 (직전 안정판)
> ★1.0.12 = `v1.0.12/` 한 폴더 증판본(Ch1+Ch2+코드+가이드+데모, 코드 matched). Fable 5대 지시 산출: 감사(`Fable_점검/`)→N=10 경쟁 작성·체리픽·검수 union·10차 재검(verify10)→finalizer 3커밋. 구 1.0.10 블록은 아래 유지(superseded).

| 경로 | 1줄 요약 | 동의어 키워드 | 갱신일 |
|---|---|---|---|
| **★v1.0.12/graphite_ica_ch1_v1.0.12.tex** | ★★★Ch1 v1.0.12(41p, 0-err) — LCO 6절 줄글→(a)-(d) 수식사슬(신설 eq:lco-* 26) + ★방향규약 원자정정(f=+σ_d pairing·F-2 전극중립 한정·세 작용처) + F-1 config +Rln[ξ/(1-ξ)] + B-3 Ω 지위 + H-1 BW 연동 등 verify10 전판정 반영 | 1.0.12, Ch1, LCO 수식화, f=+σ_d, msmrmap, configsplit, 방향 규약, release | 2026-07-02 |
| **★v1.0.12/graphite_ica_ch2_v1.0.12.tex** | ★★★Ch2 v1.0.12(14p, 0-err) — H-1 BW V_eq 부호 정정 + H-2 w_j 지위 일원화(keybox 단상 한정·값 vs 함수형 층위·파생A 전제 명시) | 1.0.12, Ch2, 발열, BW 부호, w 지위, keybox, 파생A 조건부 | 2026-07-02 |
| **★v1.0.12/Anode_Fit_v1.0.12.py** | ★★★코드 v1.0.12 — 흑연+LCO(MSMR)+가역열, 회귀 13/13·demo IDENTICAL. 주석 f=+σ_d 동기화·σ_d 한정 보강(방향 의존 3작용처·전극 인지 확장 = P4 과제) | 1.0.12, 코드, LCOCathodeDQDV, 회귀, f=+σ_d | 2026-07-02 |
| v1.0.12/FITTING_GUIDE.md | 피팅 가이드 v1.0.12 — tier 표·5-Phase round-trip + ★방향규약 §0(LCO 충전↦direction=+1) + S0-S5 비순환 식별사슬·울타리 16·잔차 진단표(D3 선별 복원) + ν≈8-10 권고(D5) + LCO Ω 지위(B-3) | 피팅, 가이드, S0-S5, 식별 사슬, 울타리, 진단표, ν, min_lag_grid_steps, Ω 미배정 | 2026-07-02 |
| v1.0.12/sample_test_v1012.py (+.png) | 종합 샘플 데모 2×2(흑연 staging 분리·LCO MSMR·q_rev 이중축·ΔS_e 게이트 골 −45.7) — glyph 경고 0·영어 라벨·결정론 해시 검증 | 샘플, 데모, 이미지, glyph, dQ/dV, 발열 | 2026-07-02 |

## 구버전 문건 — release 1.0.10 (superseded by 1.0.12)
> ★1.0.10 = 코드(`../results/code/Anode_Fit_v1.0.10.py`) 와 **동일 버전·matched**. dQ/dV 정상 종개형 코드 실증 = `../results/code/figs/anode_fit_v1_0_10_dqdv.png`. 검증보고 = `../results/process/GRAPH_VERIFY_RESULT.md`.

| 경로 | 1줄 요약 | 동의어 키워드 | 갱신일 |
|---|---|---|---|
| **★Ch1_v1.0.10/graphite_ica_ch1_v1.0.10.tex** | ★★★**release 1.0.10**(34p) = Ch1 v10-11 내용 + 버전 1.0.10 라벨 — **코드 Anode_Fit_v1.0.10.py 와 동일 버전·matched**. broadening(집합 통계역학·사이즈 제외)·w 이중지위·w_eff 제거. dQ/dV 정상 종개형 실증 | 1.0.10, release, matched, Ch1, broadening, 코드 동일버전, 종개형 | 2026-07-01 |
| Ch1_v10/graphite_ica_ch1_v10.tex | Ch1 v10(34p, 내부 빌드 계보) — release 1.0.10 의 내용 본체. v9 + broadening 복원·집합 통계역학·사이즈 제외·w_eff 제거 | chapter1, v10, broadening, 집합 통계역학, apparent-U, w_eff 제거 | 2026-07-01 |
| **Ch2_v5/graphite_ica_ch2_v5.tex** | ★★Ch2 v5 **최신**(13p) — v4 + **w_eff(Ω) 절 제거** + w=두-상 현상학적 자유 피팅 + 종 폭 기원은 Ch1 broadening 참조. 통계열역학 본체 보존 | chapter2, v5, w_eff 제거, 자유피팅, 통계열역학, 분포, 섞임 | 2026-07-01 |
| Ch1_v9/graphite_ica_ch1_v9.tex | Ch1 v9(30p) — 흑연+LCO 통합(전자 엔트로피). ⚠️**broadening 누락 → v10 으로 대체됨** | chapter1, v9, LCO, superseded | 2026-06-30 |
| Ch2_v4/graphite_ica_ch2_v4.tex | Ch2 v4(13p) — 통계열역학. ⚠️**§C w_eff 잘못 → v5 로 대체됨** | chapter2, v4, w_eff, superseded | 2026-06-30 |
| Ch1_v8/v8-11.tex | Ch1 v8(21p) — 유도 확장판(흑연). ⚠️broadening 누락 | chapter1, v8, 유도확장, 흑연 | 2026-06-30 |
| Ch1_v7/v7-11.tex | Ch1 v7(17p) — 코드흐름 간결판 | chapter1, v7, 간결, 코드흐름 | 2026-06-30 |
| Ch2_v3/graphite_ica_ch2_v3.tex | Ch2 v3(5p) — 가역 발열 survey 초안 | chapter2, v3, 가역발열, Bernardi, 초안 | 2026-06-30 |
| _archive/ | 구버전(Opus_v4/v5/v6·Fable_v3·원본 ch1/ch2 — ★broadening 설명 원천) + 빌드산물(.aux/.log) + Archive_old/rebuilt | archive, 구버전, broadening 원천, Opus, Fable | 2026-06-30 |
| Fable_점검/FABLE_AUDIT_note_A5_ch2-code.md | Fable 이력 감사 A5 — Ch2(v3→v4→v5→v1.0.10) + 코드(v11_final→v1.0.10) 트랙. w_eff narrowing 오류가 2라운드 적대검수를 통과하고 코드실행 검증(CODE_w_check.md)에서야 발각된 경위·v12 교훈 5건 | Fable, 감사, 이력, w_eff, narrowing, 적대검수, use_w_eff, LCO seam, q_rev, v12 교훈 | 2026-07-02 |
| Fable_점검/FABLE_AUDIT_note_A4_v9-v1011.md | Fable 이력 감사 A4 — Ch1(v9→v10→v1.0.10→v1.0.11) 트랙. broadening 기작③ ρ(U_j)→ρ(U_app) 재정초(R1 오판#1)·"폭 구조결함" CRIT 오판·철회(R1 오판#2, 인계무결성검수가 반증)·LCO 6절 산문회귀가 v9 시점부터 존재함을 원문대조로 확인·v1.0.11 은 docs 폴더가 v1.0.10 과 byte-identical(Phase 1.1 이후 미착수, 진행중 중단) 확인·v12 교훈 4건 | Fable, 감사, 이력, R1 오판, 철회, ρ(U_j), apparent-U, 폭 구조결함, LCO 산문회귀, v1.0.11 중단, byte-identical, v12 교훈 | 2026-07-02 |
| **Fable_점검/FABLE_AUDIT_02_ch1ch2_content.md** | ★Fable 내용 감사(v1.0.11 Ch1·Ch2) — 코어 물리 건전(손검산·SymPy·실측), 문제는 주장·귀속층: HIGH 2(Ch2 BW 부호반전·w_j 지위 챕터내 모순)·MED 11(0.18 오귀속·ν=2 23%점프·꼬리수렴 기호오류·코너 과일반화 등)·이전판정 5/5 유지 | Fable, 내용 감사, 물리 타당성, 비약, 왜곡, 코너케이스, BW 부호, w 지위, 문제 리스트 | 2026-07-02 |
| **Fable_점검/FABLE_AUDIT_03_code_fitness.md** | ★Fable 코드 적합성 감사 — 확정 결함 0(24 boxed 전부 대응·orphan 0·실측 전항 PASS 면적 1.00000·가중식 1e-19), deferred 4(양측 선언)·개선 권고 P1-P4(버전위생·ν 기본값·default 표시·헤더잔재) | Fable, 코드 감사, 양방향 매핑, 실행 실측, deferred, 적합성 | 2026-07-02 |
| **Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md** | ★Fable 이력 전수감사 **종합**(v3→v1.0.11) — 계보·전환별 장단점/문제점 표·관통 패턴 6(설계doc 순응검수 한계·실행기반 검증 결정력 등)·★방향성 유실 표(Eyring 척추 미계승·S0-S5 절삭·§1.18 park)·v12 교훈 9·4-tier | Fable, 감사, 종합, 이력, 계보, Eyring 척추, 방향성 유실, v12 교훈, 관통 패턴 | 2026-07-02 |
| Fable_점검/FABLE_AUDIT_note_A2_v5-v7.md | Fable 이력 감사 A2 — v5→v6(흐름도 재조립·97식 보존 손실0)·v6→v7(코드 수식-구동 재편, 전 유도·해석해·S0-S5 식별·KWW 의도적 절삭 = 재-스코핑, 사용자 사후 불만→v8 촉발). 배열↔깊이 독립 축 교훈 | Fable, 감사, v6, v7, 재조립, 재스코핑, S0-S5, KWW, 절삭, 배열과 깊이 | 2026-07-02 |
| Fable_점검/FABLE_AUDIT_note_A3_v7-v9.md | Fable 이력 감사 A3 — v7→v8(유도 4단 복원·KNOWN_DEFECTS 6종 정정·D-PEAK "v8서 생김"은 근거미발견)·v8→v9(LCO 통합·흑연 byte 보존·ΔS_e 역부호 5건 적발). broadening 후퇴 정량(v4/v5 ~2771/1883줄→v7 894줄) | Fable, 감사, v8, v9, KNOWN_DEFECTS, D-PEAK, LCO, 유도 복원, broadening 후퇴 | 2026-07-02 |
| Fable_점검/FABLE_AUDIT_note_A1_v3-v5.md | Fable 이력 감사 A1 — Ch1 v3(Fable)→v4(Opus)→v5(Opus) 전환. v3→v4=순수 추가(§1.18 적층, §1.1~1.17 바이트 동일)이나 최초 무계획 배치작성이 σ충돌·B/κ 산수오류 배출 후 V4R redo·Fable_v4→Opus_v4 개명. v4→v5=수식-구동 장르전환(97식 verbatim·산문 32% 압축·keybox 14→1·athermal 훅 소거)+V5.R8 미게이트 회귀·구트랙 버전번호 충돌 경고·v12 교훈 8건 | Fable, 감사, 이력, v3, v4, v5, 적층, stacking, 수식-구동, keybox, verbatim, athermal, V5RR, 장르 전환, park, v12 교훈 | 2026-07-02 |

## ★재작업 진행 중 (2026-06-30, `../plans/2026-06-30-rework-broadening-restore-weff-fix-reorg-plan.md`)
- **Ch1 v10**(예정) = v9 정정·통합 — broadening 복원 + w 이중지위 + w_eff 제거 + 기존 LCO/분포 유지.
- **Ch2 v5**(예정) = w_eff 절 제거 + broadening 참조.
- 누락·개선 분석: `../results/MISSING_CONTENT_REVIEW.md`. 조사: `../results/research/radius`(종모양 origin).

## results/ 안내 (문건 아님)
- `results/builds/{v7,v8,v9,ch2_v4}` — 9종 competition 빌드 과정. `results/code/Anode_Fit_v11_final.py` — Ch1 forward 모델(⚠️use_w_eff 버그·v12 정정 대상). `results/research/` — 조사(LCO·통계열역학·radius). `results/process/` — PHASE/LEDGER/HANDOVER.
