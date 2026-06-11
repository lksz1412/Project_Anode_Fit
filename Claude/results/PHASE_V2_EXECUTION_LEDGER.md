# PHASE_V2 Execution Ledger — Ch1 백지 재작성 v2 (Eyring 척추)

Plan: Claude/plans/2026-06-10-ch1-blank-rewrite-v2-plan.md (/goal GO + 추가 지시: 전수 Fable 작성·검수, 검수 시 Codex 적대 검수 병행).
신규 파일: Claude/docs/graphite_ica_ch1_Fable_v2.tex (직전 판 graphite_ica_ch1_Fable.tex 50p 는 불가침 보존).
게이트: 절당 2-pass 빌드 0/0 + 커밋·푸쉬. 피드백 6항 반영 체크리스트는 V.2 게이트.

| Step | 절 | 작업 | 검수 | Commit |
|---|---|---|---|---|
| 117–118 | V.0 계획·ledger | 본 문건 | — | ecd4e7d |
| 119 | 서론 | 척추 선언+stagebox+두 경로, preamble 재사용 | 빌드 0/0(전방 ref 10 보류)·재정독 | a48b22b |
| 120 | §1 기호 | 척추 순서 사전 표+σ_d 세 작용처 | 0/0·재정독 | de390ce |
| 121 | §2 근본식 | eq:eyring=(1.1)+fig:barrier+세 인자 지도 | 0/0·수치(k₀) 검산 | f6cacd3 |
| 122 | §3 열역학 다리 | G→μ→격자기체(Stirling)→전기화학 (피드백①) | 0/0·부호 물리 검산 | b4b51f3 |
| 123 | §4 정·역과 회수 | BV/BEP 합1 강제→detailed balance→logistic 유도 (피드백④ keystone) | 0/0·극한 검산 | 2f75155 |
| 124 | §5 상분리 | 현 작도→binodal→spinodal 단계 명명 (피드백③), 그림 2 재캡션 | 0/0·binodal 좌표 검산 | cfc3612 |
| 125 | §6 관측축 | 보존식 해 V_n·세 전위·연쇄율·worked example | 0/0·worked 검산 | 68115d5 |
| 126 | §7 기준선 | 종 3량, FWHM 닫힌꼴 없음 (피드백②) | 0/0·면적 보존 검산 | aee7cf6 |
| 127 | §8 C-rate 가지 | 보편 ODE→기억 커널 해→두 극한+fig:kernel | 0/0·L_q 수치 | b97b288 |
| 128 | §9 전위 가지 | ΔG_eff 슬롯·직렬 율속·Marcus 창 | 0/0·전이대 % 검산 | a6455e2 |
| 129 | §10 온도 가지 | Arrhenius 회귀(χ 선행)·분포 1/RT 전파·중첩 | 0/0·σ_lnL 검산 | 2c80394 |
| 130 | §11 합성 | eq:closed·simplefit·3×3 표·비순환 원칙 | 0/0·r_a 보존 검산 | 7a6f44d |
| 131 | §12 합산·겹침 | 보존 vs 독립 층위·융합 두 조건·forward 원칙 | 0/0 | 7b3c4c5 |
| 132 | §13 [확장] 분기 | V_eq loop·eq:hysdU 유도·γ 축소 | 0/0·차원/환원/부호 검산 | ed8f8aa |
| 133 | §14 [확장] 관측 gap | 절편/기울기 분해·gap-T 표+그림·부분 cycle 소절 | 0/0·표 수치 검산 | 73b2a09 |
| 134 | §15 통합·알고리즘 | (1)–(8)+M1–M6+S0–S5+참조표+울타리 (round-trip 사양) | 0/0 (134b: overfull 1 수정) | 0682bb2·aea5362 |
| 135 | §16 검증·반증 | 경쟁 꼬리원 표·히스 세 칼날·마무리 recap | 0/0 | 1987b76 |
| 136a | V.1 완료 게이트 | 잔존 undef(sec:dist→sec:tempbranch) 수정 | **err0/of0/undef0, 32p** | 23f3efe |
| 136b | V.2 챕터 게이트 | 피드백 6항 체크 전부 PASS·전문 통독·수치 검산·orphan 0·RESULT | PHASE_V2_ch1_RESULT.md | 04d56fc |
| 137 | V.R R1 | prose 렌즈(구어체·전보체 4건) + Codex 1차 투입 | 0/0/0 | 56c9b97 |
| 138 | V.R R2 | 코드 시뮬 렌즈 — §15 사양 결정성 3건 | 0/0/0 | f82261f |
| 139 | V.R R3 | PDF 시각 판독 — 그림 10p 결함 0 | 검증 라운드 | ada0210 |
| 140 | V.R R4 | Codex 1차 삼각검증 — 확정 2(ξ_s 반전·r_a 누락)+채택 5 | 0/0/0 | c9d3be8 |
| 141 | V.R R5 | 절별 A(서론·§1·§2) — 반쪽전지 선언·s_I·fig:barrier 파선 χ=½ 재계산 등 16건 | 0/0/0 | 36c0ad1 |
| 142 | V.R R6 | 절별 B(§3·§4) — μ⁰ 기준 몫 신설·쌍 셈 자기일관·골짜기 문장 등 16건 | 재유도 8항 통과 | cba6df7 |
| 143 | V.R R7 | 절별 C(§5·§6) — g′=isotherm 우변 연결·§5 verifybox 등 10건 | 좌표 전수 재계산 통과 | ec88b44 |
| 144 | V.R R8 | 절별 D(§7·§8) — verifybox 곡률 부호 처방 교체 등 5건 | kernel convolution 대조 | fcdf343 |
| 145 | V.R R9 | 절별 E(§9·§10) — LqV 유도 단절·댕글링 예고 2·절편 부호 등 12건 | 재계산 10항 통과 | 8f56f1c |
| 146 | V.R R10 | 절별 F(§11·§12) — ★(1−r_a) 보존 인자 3식+그림 2 재좌표 등 16건 | 좌표 역산 적발 | 4be9623 |
| 147 | V.R R11 | 절별 G(§13·§14) — 거울 쌍 한정·곡률 용어·γ 두 기전 등 10건 | 수치 전수 통과 | fa3b1c9 |
| 148 | V.R R12 | 절별 H(§15·§16) — 실행 순서 2건·Ω 흡수 결정·b_j 행 등 19건 | 코드 시뮬 | 35b00dd |
| 149 | V.R R13 | 꼬리 경로 round-trip 신규 — PASS(χ 0.534, (1−r_a)=ODE 진실) + 사양 발견 2건 반영 | 실행 검증 | 3d3efe2 |
| 150 | V.R R14 | Codex 2차 삼각검증(7건 정상·지적 7건 채택 — w·C_bg/Q_cell 차원·Ω 흡수 조건+복원식·중간 구간 규칙 등) + PDF 시각 스윕 결함 0 | 0/0/0, 35p | 4a2abd6 |
| 151 | V.E E.0 | 예시 구현 절 계획(2026-06-11-ch1-v2-code-example-plan.md) | — | (plan 커밋) |
| 152 | V.E E.1 | graphite_ica_model.py(M1–M6 직역)+run_example 실행 검증 3종 PASS | 54.8mV·면적 0.3998·S1 회복 | (E.1 커밋) |
| 153 | V.E E.2 | §1.17 절 수록(verbatim 분할 diff 게이트) | 0/0/0, 37p | 1cf280f |
| 154–155 | V.E ER1+ER2 | 종단 물리 적대+Codex 코드 절 — 충전 ln_Lq 파손 수렴 적발→방향형 수정+충전 면적 시험 | 0.4000 정확 | ed830f6 |
| 156 | V.E ER3 | 종단 검수 본문 일괄 17건(울타리 ⑪–⑭·plateau 별표·변별 지문 등) | 0/0/0, 38p | 1dd1814 |
| 157–158 | V.E ER4+ER5 | 시각·구조 검증 + 정합 스윕(§14 keybox 옛 강도 동기화) | 0/0/0 | 9b3b118 |
| 159–161 | V.E ER6–ER8 | Codex 3차 투입·prose(전문 정독으로 재수행)·완전성 스윕 | 누락 0 | (기록 커밋) |
| 162–163 | V.E ER9+ER10 | fresh-eyes 전문 통독(확정10·의심6)+Codex 3차(확정1: χ_d) → 일괄 27건+실행·diff 재검증 | 0/0/0, **39p** | 723a85a |
| 164 | V.P P.0 | 교정 pass 계획(2026-06-11-ch1-v2-proofread-pass-plan.md) — GO 후 진행 | — | (plan 커밋) |
| 165–181 | V.P P.1–P.17 | 절별 한큐 루프(정독→인벤토리→refute→수정→재정독→0/0/0→커밋) — 32건 | 절당 커밋 | c5106c7→30f33aa |
| 182–184 | V.P P.R1–R3 | Codex+Fable 전문 통독 병행→삼각검증 21건(현-기준 통일·ICA 부호 규약 등)+overfull 정정 | 0/0/0 | ce3198a·d0cc367 |
| 185–187 | V.P P.R4–R6 | 실무-경로 통독("피팅 착수 가능" 판정)→11건(ΔH^eff 방향성 등)+시각 9p 스윕 | 실행·diff PASS | 9e8b7f1 |
| 188–191 | V.P P.R7–R10 | Codex 최종(A–E 전부 정상)→잔존 3건 수정→종합 게이트 전 항목 PASS | 0/0/0, 39p | (본 커밋) |
| 192 | V.T T.0 | 어조·유도 복원 pass 계획+보강(중간식 번호 부여·코드 주석 T.R5 재매핑·컴팩션 청크 운용) | — | (plan 커밋) |
| 193 | V.T T.2 §1.3 | 어조 제거(도입)+G 축소(2법칙 sketch 제거)+Stirling 전 단계(eq:W/stirlingexp/lnW)+ḡ(eq:gbar)+항별 미분(eq:mixderiv)+전기화학 균형(eq:eqbalance/eqexpand) — 식 번호 재배정 시작(eq:mu=1.10) | 0/0/0, 39p | (본 커밋) |
