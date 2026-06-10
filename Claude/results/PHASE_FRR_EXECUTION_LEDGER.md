# PHASE_FRR Execution Ledger — Fable 전면 재검토 (물리 논리 + 교과서 해설)

Plan: `Claude/plans/2026-06-10-full-rereview-physics-pedagogy-plan.md` (GO 6-10 + 보강 3건: 리뷰논문급 깊이·10회=하한 수렴까지·`_Fable` 사본 작업, 원본 .tex/pdf 불가침).
작업본: `graphite_ica_ch1_Fable.tex`(1626행/18절/34p) · `ch3_Fable`(479행/11절/9p) · `ch4_Fable`(323행/8절/6p). Baseline 빌드 전부 0/0. Branch `rb-rebuild-2026-05-30`, start `6f75590`.
인계번호 스냅샷(ch1_Fable.aux): charge 1.1·cbg 1.2·vapp 1.3·smix 1.6·logistic 1.11·dUdT 1.15·weff 1.19·relax 1.20·eyring 1.21·Lq 1.23·affinity 1.27·bv 1.28·db 1.29·hys_dU 1.48·hys_center 1.49·master 1.54·hys_master 1.55.

| Phase/Subphase | Planned Steps | Actual Steps | Block | Purpose | Status | Plan | Result | Machine Artifacts | Validation | Gate | Next Step |
|---|---:|---:|---|---|---|---|---|---|---|---|---:|
| 1.1 | 1–3 | 1–3 | setup | 지침·메모리 재확인, _Fable 사본, 절 지도, baseline 빌드+스냅샷 | PASS | plans/2026-06-10-full-rereview-physics-pedagogy-plan.md | (본 ledger 헤더) | *_Fable.tex/pdf/aux | 빌드 3×0/0, 스냅샷 기록 | PASS_FRR_SETUP | 4 |
| 1.2/1.3 | 4–21 | 4–21 | ch1 절별 | 18절 전문 정독 재작업 | PASS | 〃 | PHASE_FRR_ch1_RESULT.md | ch1_Fable.pdf 35p | 빌드 0/0·절별 기록 | PASS_FRR_CH1_SECTIONS | 22 |
| 1.4 | 22–24 | 22–24 | ch1 gate | 2-pass·인계 불변·규율 0·result | PASS | 〃 | 〃 | .aux 스냅샷 | 인계 전수 일치 | PASS_FRR_CH1_GATE | 25 |
| 3.1–3.3 | 25–38 | 25–38 | ch3 | 11절 전문 정독·η_hys 가중 정합·앞 장 표현 | PASS | 〃 | PHASE_FRR_ch3_RESULT.md | ch3_Fable.pdf 9p | 빌드 0/0·인계 일치 | PASS_FRR_CH3_GATE | 39 |
| 4.1–4.3 | 39–49 | 39–49 | ch4 | 8절 전문 정독·전 유도 검산 일치(무수정) | PASS | 〃 | PHASE_FRR_ch4_RESULT.md | (무수정) | 검산 전수 일치 | PASS_FRR_CH4_GATE | 50 |
| 5.1–5.13 | 50–73 | 50–73 | 재검토 R.1~R.13 | 라운드별 3~4창 전문 정독 재검수→삼각검증→수정→빌드→커밋+푸쉬 (렌즈: 물리·장간·정밀재유도·해설·당글링/사용성·표층·종합·확인×3) | PASS | 〃 | PHASE_FRR_ROUNDS_RESULT.md | *_Fable.pdf 36/10/7p | 수렴공선 29→…→0·식번호 불변·광역 0/0 | PASS_FRR_CONVERGENCE | — |

## Ch1_Fable 절 지도 (baseline 행 기준)
서론 61–110 · §기호 113–170 · §전하보존 171–240 · §평형peak 241–425 · §정규용액 426–533 · §동역학 534–659 · §유효배리어 660–783 · §통계 784–864 · §분포 865–936 · §종합 937–1110 · §겹침 1111–1168 · §DVA 1169–1211 · §분기 1212–1296 · §분기dQdV 1297–1323 · §분극 1324–1359 · §부분cycle 1360–1379 · §master 1380–1526 · §검증 1527–끝

## 절별 기록 (Phase 1.2~4.2 누적 — 행범위·수정/무수정 사유 필수)
| Step | 절 | 정독 행범위 | 물리 수정 | 해설 보강 | 무수정 사유 | Build |
|---|---|---|---|---|---|---|
| 4 | 서론 | 61–110(전문) | 도착점 참조순서 정정(분기→§master 통합) | 상전이→peak 이유(plateau→dQ/dV 치솟음) 1문단·로드맵에 §전하보존 추가 | — | 34p 0/0 |
| 5 | §기호 | 113–172(전문) | r_a 상한→(0,ξ_eq(q_a)]·k^fwd 등재·ρ_G 용량분율 표기 | σ_d 선행 안내(부호 규약) | — | 0/0 |
| 6 | §전하보존 | 175–245(전문) | — | Faraday 계상 근거+선형분할(서로소 자리)·C_bg>0 물리출처(단상 안정성)·plateau 발산=서론 peak 정의와 연결 | (물리 결함 없음 — 이전 라운드 수렴 확인) | 35p 0/0 |
| 7 | §평형peak | 256–438(전문) | s 이중고정 해소(규약/관측 역할 분리) | (iii) s-흡수 괄호 단순화·"perturbation"→임계까지 포함 정정 | 유도부(Stirling·logistic·FWHM)는 검산 일치라 무수정 | 0/0 |
| 8 | §정규용액 | 441–549(전문) | "한 연속"→한 모수축+질적 경계(임계) 정정·V_eq 정의 인용 정정 | z[ε]=유효 척도(장거리 층간 탄성 뭉뚱그림, Daumas–Hérold)·spinodal 닫힌꼴 본절 제시(spine) | g''·T_c·binodal 연립·w_eff 검산 일치 | 0/0 |
| 9 | §동역학 | 552–679(전문) | — | eq:tailTC "peak 낮아짐"=면적보존 경유 주석·slowly-varying 조건 구체화 (χF/RT)L_V≪1≈0.1 수치 | relax·Lq·rsol·tail 재검산 일치 | 0/0 |
| 10 | §유효배리어 | 682–809(전문) | — | — | r⁺/r⁻ 지수·χ상쇄·LqV 감쇠인자 재검산 일치, 3구간·Marcus bound·직렬율속 정비완료 — 보강시 중복 | 0/0 |
| 11 | §통계도구 | 812–890(전문) | — | — | 4도구+jacobian 격하·varprop·KWW 조건부 정비완료 | 0/0 |
| 12 | §분포 | 893–962(전문) | (b) "독립 물리량"→독립 모형(매핑 경로) 정합 | boundbox 공통 q_a 1차근사 한계+상관 방향(stretched 강화) | superpose·보존·rigorbox 검산 일치 | 0/0 |
| 13 | §종합 | 965–1136(전문) | 물리 절 목록 "다섯"→여섯(정규용액 누락 적발)+진입 경로 명시 | — | closed·simplefit·S1–S4·arrhenius 재검산 일치 | 0/0 |
| 14 | §겹침 | 1139–1194(전문) | — | — | 반치반폭 유도·분기 peak쌍 확장·forward 절차 정비완료 — 무수정 | 0/0 |
