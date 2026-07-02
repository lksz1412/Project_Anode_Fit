# v1.0.10 인계 무결성 검수 — 9종 UNION 종합 (10차 재검 입력)

> 9 검수(S1-3 Sonnet5·O1-3 Opus·C1-3 Codex, 기록 SPEC 대조) 단점 합집합. ★핵심: **인계 견고**. 제 이전 문제검수(V1010_PROBLEM_REPORT·HANDOVER_v1.0.11)의 R1 "구조결함" 오판 확정.

## A. 인계 무결 확정 (9종 수렴 — 문제 아님)
- **broadening 복원**: v10-11→v1.0.10 **word-for-word 보존**(3기작 L_V/내재RT-F/집합통계역학 apparent-U=U_j+η·w 이중지위·사이즈 배제·forward-only·D1 재정초). 차이는 가독성 4-다리 보강(확장). [S1·C1·C2·C3·O3]
- **KNOWN_DEFECTS 6대**(D-PEAK·D-PEAK2·D-VEQ·D-DHEFF·D-WEFF·D-UBR): v8-11→v9→v10→v1.0.10 정정 형태 **완전 보존**(Compare-Object diff 0·R8 회귀검사 존재·코드 이산 branch-switch). [S2·C1·C3]
- **전자엔트로피 물리**: 무손실(삭제 0)·오히려 강화(교차검증·직교성·단위박스 추가)·수치 전수검증(−45.68·N_A k_B²=R k_B). [O1·S3·C3·S1]
- **Ch2 통계열역학**: v3→v4→v5→v1.0.10 무결(v4=byte-identical·v5→v1.0.10 degradation 0). w_eff 제거 = Ch1과 coordinated supersession. [O3·C2·C3]
- **두 축**: G-derive(전개 비약0) 유지/강화·G-follow(교과서) 유지. P1-P5가 물리 논리 훼손 안 함. [S3·O1·O2·O3·C3·S1]
- **★bell = 의도된 apparent-U/η 물리, 면적=Q 보존, 결함 아님**(v11_final부터 정상). use_w_eff 제거 정당(v11↔v1.0.10 max_abs_diff=0). [전원]

## B. ★제 이전 R1 오판 — 확정·위험 (최우선 정정)
- V1010_PROBLEM_REPORT §1 R1 "폭 모델 구조 결함(near-delta 생성 불가)" + HANDOVER_v1.0.11 Ch1 "near-delta+broadening 2층 재설계"는 **SPEC 미대조 오판**. bell은 결함이 아니라 v10이 3세대 복원한 물리(apparent-U/η + 현상학적 w). ★**v1.0.11이 이 오판 위에서 폭 모델을 near-delta로 재설계하면 복원된 broadening 물리 붕괴 위험**(S1 경고). → v1.0.11 핸드오버에서 R1 **철회·재framing 필수**. [S1·O2 CRIT→HIGH 강등]

## C. 실 인계 결함 (minor, 대부분 governance/문서 — v1.0.11 이월)
| ID | 등급 | 결함 | 근거 |
|---|---|---|---|
| H-1 | MED | 전자엔트로피 "byte-identical" claim stale — 실제 additive(184→235줄, 물리 무결). PHASE_CH1v10_RESULT·헤더·FIX_LIST_v1011 A2 mandate가 산출물과 불일치 → 미래 세션 오판 위험 | O1·S3·C3·S1 (SHA 실측) |
| H-2 | MED | 버전 라벨 stale: Ch1 헤더/PDF 메타 "(v9)"(L71·73)·Ch2 "graphite_ica_ch2_v5.tex/(v5)"(L2·35·37) | C2 |
| H-3 | MED·검증 | ρ_G(G) 동역학 장벽 분포 + σ_G/RT stretched-tail **진단 prose** 손실(v3/v4/v5→v1.0.10). ※모델은 6-30 [과제 MODEL-1 선택]으로 의도적 scope-out(현상학적 w 흡수)이나 진단 prose 손실은 판정 필요 | C1 |
| H-4 | MED | 전자항 magnitude trail: 앞 "|ΔS_e|≈1.5 J/mol·K 소수보정"(L501-505) vs 후 "gate 골 ≈−46 J/mol·K"(L1123-30) — 다른 척도인데 선행참조 없어 G-follow 혼동 | C3 |
| H-5 | LOW | 코드 헤더 L37-44 "옵션 w^eff=(RT/F)(1−Ω/2RT)" 잔재(live 제거됨, 미래 복원 유도 잡음) | C3 |
| H-6 | LOW | FIX_LIST_v911 A3-1 overfull 22.6pt 실제 미정정(v9-11·v10-11·v1.0.10 L1807-09 잔존, "fixed" claim 무효) | C2 |
| H-7 | 제약 | Ch1 §broadening ↔ Ch2 파생 C 단방향 위임 → 동반개정 제약 명기(stale 위험) | O3 |
| H-8 | 강등 | LCO 코드 default(x_MIT 0.50·T3 부재) placeholder — 이미 tier-C 라벨·Phase 4.1 예약. G-usable 실패방지 조건 크게 명기 권고 | O1·C3·S1 |

## D. 오적발 방지 (문제 아님)
bell/병합(의도된 물리·v11_final부터)·면적 ratio(grid artifact)·use_w_eff 제거(정당 dead-path)·radius(회의적 참조·독립 타당)·Ch2 w_eff supersession·D-PEAK small-L(재발0)·fly2020(Crossref supersede).

## E. 10차 재검 쟁점
1. **★R1 오판 반전 확정**: bell=의도 물리·재설계 금지·v1.0.11 위험 경고 — 독립 물리 재확인.
2. **H-3 ρ_G 진단 손실**: 모델 scope-out은 의도(확정)이나 stretched-tail 진단 prose 손실은 실 gap인가 허용 범위인가(6-30 [과제 MODEL-1] 대조).
3. **H-1/H-2/H-5 stale claim/label**: 실 minor 결함 확정(문서 정합).
4. **H-4 magnitude trail**·**H-8 LCO placeholder**: G-follow/usable 실 위험 vs 라벨로 충분.
5. **별개 대기**: LCO 절 수식-주도 vs 줄글 회귀(v6 SPEC 대조) — 이 union엔 미포함(다음 검수).
