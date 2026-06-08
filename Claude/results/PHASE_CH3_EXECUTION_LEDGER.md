# PHASE_CH3 Execution Ledger — 흑연 음극 발열 (Ch1+Ch2 기반)

Plan: `Claude/plans/2026-06-09-ch3-heat-build-plan.md` (v2). Branch `rb-rebuild-2026-05-30`. Start `4c8fdc3`.
방식: 절 단위 루프(절마다 빌드·Ch1·Ch2 정합)·최대 effort·NO Workflow·단일문건 규율·master 직접 손검·교과서 깊이.

| Phase | Steps | 절 | Purpose | Status | Build | Gate | Next |
|---|---:|---|---|---|---|---|---:|
| 3.1 | 1-2 | 서론 | T 생성+히스 열원 동기·도착점 thread | PASS | 2p clean | G3.1 | 3 |
| 3.2 | 3-4 | §1 기호 | 새 기호 표(Chapter-N 0) | PASS | clean | G3.2 | 5 |
| 3.3 | 5-9 | §2 배경 | Bernardi 유도·세 갈래 분리(손검 부호·차원) | PASS | 3p clean | G3.3 | 10 |
| 3.4 | 10-13 | §3 가역열 | q_rev=−IT∂V/∂T (Ch1 1.15)·부호·worked 30mJ | PASS | 4p clean | G3.4 | 14 |
| 3.5 | 14-18 | §4 히스열 | q_hys=I·½γΔU_hys 율무관·loop면적 등가·worked 16mV ★ | PASS | 4p clean (ext 수정) | G3.5 | 19 |
| 3.6 | 19-22 | §5 분극열 | q_pol=|I|²R_n 율의존·히스 분리·worked | PASS | clean | G3.6 | 23 |
| 3.7 | 23-25 | §6 전이별 | dQ/dV·분기 연결(히스/가역/분극 SOC) | PASS | clean | G3.7 | 26 |
| 3.8 | 26-29 | §7 열수지 | mc_p Ṫ=Q−hA_s(T−T_amb)·τ_th·ΔT∞·극한 | PASS | 6p clean | G3.8 | 30 |
| 3.9 | 30-33 | §8 되먹임 | 음의 자기제한(ΔU_hys↓·k_j↑·R_n↓)·runaway 밖 | PASS | clean | G3.9 | 34 |
| 3.10 | 34-37 | §9/§10 | 파라미터(앞장+c_p,hA_s)·데이터→예측 | PASS | clean | G3.10 | 38 |
| 3.11 | 38-41 | §11 종합식 | master 2식·환원검산(Ω≤2RT·I→0 히스잔존·등온) | PASS | clean | G3.11 | 42 |
| 3.12 | 42-44 | 검증 | 빌드 8p 0/0·인계 .aux 대조·단일문건 규율·Codex(시정)·커밋 | PASS | 8p 0/0 | G3.12 | done |

**Codex 적대검수(agent a35e5d04)**: 인계 번호(1.3/1.15/1.17/1.19/2.5/2.10/2.14) 전수 원문 대조 일치. §3 가역열·§7 열수지 정상. **확정 시정 5건**:
- (2) **§4 q_hys 부호·가중**: I·Σ½γΔU → |I|Σα_j½γΔU (α_j=|I_j|/|I| 전이 전류 분율) — 충전 음수·과산정 해소, q_hys≥0 양분기. loop 면적 ∮V dq(무차원)→∮V dQ(쿨롱).
- (1) **§2 유도 부호**: 엔탈피−전기일 prose 엉킴 → 과전압 기반(η=V_app−V_OCV, 음극 방전 전위 상승) 재서술해 박스식과 일치.
- (5) **§8 자기제한 조건**: Ω·γ T-무관·ΔH_a>0·R_n↓ 명시(폭주 부재 증명 아님).
- 부수: V_OCV^rev=분기 평균 U_j(2.14) 정의, 피팅 파라미터 C_th=mc_p 명확화.
- master 식도 |I| 형으로 정정. 재빌드 8p 0/0.

## Ch1·Ch2 인계식 대조표 (전수, 채워가며)
| 인계식 | 출처 | Ch3 사용 위치 | 원문 대조 |
|---|---|---|---|
| ∂U_j/∂T=ΔS_j/(sF) | Ch1 **1.15** | §3 q_rev·§master | .aux 대조 ✓ |
| V_app=V_n+s_I|I|R_n | Ch1 **1.3** | §5 q_pol·§2 | .aux 대조 ✓ |
| L_{q,j}=|I|/(Q_cell k_j) | Ch1 **1.19** | §5 lag·§8 | .aux 대조 ✓ |
| k_j Eyring | Ch1 **1.17** | §8 되먹임 | .aux 대조 ✓ |
| ΔU_hys=(2/sF)[Ω u−2RT artanh u] | Ch2 **2.10** | §4 q_hys·§master | .aux 대조 ✓ |
| U_j^{dis/chg}=U_j±½γΔU_hys | Ch2 **2.14** | §2·§4 η_hys | .aux 대조 ✓ |
| 참/분극 분리 | Ch2 **2.5** | §2·§5 | .aux 대조 ✓ |
| T_c=Ω/2R | Ch2(verifybox) | §4·§8 되먹임 | 무번호(검산박스) |

## 볼륨 보강 (Phase 3.13~, plan `2026-06-09-ch3-volume-enhancement-plan.md`)
| Phase | 절 | 보강 | Status |
|---|---|---|---|
| 3.13 | 서론 | "왜 발열을(ICA·수명·안전)" 큰 그림 | PASS clean |
| 3.14 | §2 | 2법칙 엔트로피생성 σ̇=Iη/T≥0·De Donder·세갈래 규모비교; **eq:h_three 정합 시정(q_hys=|I|Σα)** | PASS clean |
| 3.15 | §3 | 삽입 엔트로피 두 출처·staging ∂U/∂T 부호 물리 | PASS clean |
| 3.16 | §4 | 준정적 비가역(핵생성 장벽)·binodal/spinodal 발열 상하한·다입자 | PASS clean |
| 3.17 | §5 | 과전압 3분해(ohmic·η_ct·확산)·완화 소산 | PASS 9p |
| 3.19 | §7 | lumped 타당성 Biot·Duhamel 시변 해·다cycle(가역 상쇄/비가역 누적) | PASS 9p |
| 3.20 | §8 | 선형 안정성 dQ_gen/dT<hA_s·runaway 임계 | PASS 9p |
| 3.22 | §11 | 종합 worked(0.2C 방전 세갈래·ΔT∞·되먹임) | PASS 9p |
| 3.18·3.21 | §6·§9/10 | (원 깊이 유지, 후속 보강 가능) | 보류 |
| 3.23 | 전체 | 빌드 9p 0/0·Codex·커밋 | 진행 |
보강: 서론·§2·§3·§4·§5·§7·§8·§11 (8/10절) 교과서 깊이. 8p→9p.

## Findings (절별)
- 신규 작성, 8p, overfull 0·undefined 0. 단일문건 규율: 본문 챕터명 0·§1 Chapter-N 0.
- 손검: Bernardi 부호(음극 방전 전위 상승→q_irr=I(V_app−V_OCV)≥0)·q_hys 율무관·loop면적 등가·환원검산 통과.
- 빌드 중 수정: `\ext` 미정의 추가, `(2.x)` placeholder→실번호(2.10/2.14), 챕터명→앞 장들.
- Codex 적대검수 진행(Bernardi·히스열·되먹임·인계).

## Findings log
(절별 누적)
