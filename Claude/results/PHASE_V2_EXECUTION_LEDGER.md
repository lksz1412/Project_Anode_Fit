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
| 136b | V.2 챕터 게이트 | 피드백 6항 체크 전부 PASS·전문 통독·수치 검산·orphan 0·RESULT | PHASE_V2_ch1_RESULT.md | (본 커밋) |
