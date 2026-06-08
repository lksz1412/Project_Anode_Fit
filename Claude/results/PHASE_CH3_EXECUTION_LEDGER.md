# PHASE_CH3 Execution Ledger — 흑연 음극 발열 (Ch1+Ch2 기반)

Plan: `Claude/plans/2026-06-09-ch3-heat-build-plan.md` (v2). Branch `rb-rebuild-2026-05-30`. Start `4c8fdc3`.
방식: 절 단위 루프(절마다 빌드·Ch1·Ch2 정합)·최대 effort·NO Workflow·단일문건 규율·master 직접 손검·교과서 깊이.

| Phase | Steps | 절 | Purpose | Status | Build | Gate | Next |
|---|---:|---|---|---|---|---|---:|
| 3.1 | 1-2 | 서론 | T 생성+히스 열원 동기·도착점 thread | PASS | 2p clean | G3.1 | 3 |
| 3.2 | 3-4 | §1 기호 | 새 기호 표(Chapter-N 0) | PASS | clean | G3.2 | 5 |
| 3.3 | 5-9 | §2 배경 | Bernardi 유도·세 갈래 분리(손검 부호·차원) | PASS | 3p clean | G3.3 | 10 |
| 3.4 | 10-13 | §3 가역열 | q_rev (Ch1 1.15) | PENDING | | G3.4 | 14 |
| 3.5 | 14-18 | §4 히스열 | q_hys (Ch2 ΔU_hys, 율무관) ★ | PENDING | | G3.5 | 19 |
| 3.6 | 19-22 | §5 분극열 | q_pol (R_n+완화) | PENDING | | G3.6 | 23 |
| 3.7 | 23-25 | §6 전이별 | dQ/dV·분기 연결 | PENDING | | G3.7 | 26 |
| 3.8 | 26-29 | §7 열수지 | T(t)·τ_th·ΔT∞ | PENDING | | G3.8 | 30 |
| 3.9 | 30-33 | §8 되먹임 | T↔peak/gap 자기일관 | PENDING | | G3.9 | 34 |
| 3.10 | 34-37 | §9/§10 | 파라미터·데이터→예측 | PENDING | | G3.10 | 38 |
| 3.11 | 38-41 | §11 종합식 | master 한 줄 | PENDING | | G3.11 | 42 |
| 3.12 | 42-44 | 검증 | 빌드·Ch1·2 대조·Codex·커밋 | PENDING | | G3.12 | done |

## Ch1·Ch2 인계식 대조표 (전수, 채워가며)
| 인계식 | 출처 | Ch3 사용 위치 | 원문 대조 |
|---|---|---|---|
| ∂U_j/∂T=ΔS_j/(sF) | Ch1 (1.15) | §3 q_rev | (대조 예정) |
| V_app=V_n+s_I|I|R_n | Ch1 (1.3) | §5 q_pol | (대조 예정) |
| L_{q,j}=|I|/(Q_cell k_j) | Ch1 (1.19) | §5 lag | (대조 예정) |
| ΔU_hys=(2/sF)[Ω u−2RT artanh u] | Ch2 | §4 q_hys | (대조 예정) |
| U_j^{dis/chg}=U_j±½γΔU_hys | Ch2 | §4 η_hys | (대조 예정) |
| T_c=Ω/2R | Ch2 | §8 되먹임 | (대조 예정) |

## Findings log
(절별 누적)
