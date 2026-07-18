# INDEX — v1.0.22 `results/` 산출물 색인 (R9 초안)

> 지위: **초안** — 마스터 확정. R9 마감 창 작성, 2026-07-18.
> 범위: `Claude/docs/v1.0.22/results/` 전 산출물(파일별 1줄 설명·소속 phase). 경로는 `results/` 기준 상대.
> 설명 근거: 파일명 + `V1022_EXECUTION_LEDGER.md`·`V1022_CHANGE_LOG.md` phase 문맥. 내부 미정독 파일은 phase 산출 문맥 기준(★= 본 R9 정독 확인).

---

## 원장·로그 (루트, phase 관통)

| 파일 | 설명 | phase |
|---|---|---|
| ★`V1022_EXECUTION_LEDGER.md` | phase 실행 원장(12-col: Planned/Actual/Block/Purpose/Status/…/Gate/Next) — R0~R8 | 관통 |
| ★`V1022_CHANGE_LOG.md` | 변경 통제 대장(S-001~012 구조·A/C/E/B-### 콘텐츠 — 파일·내용·구조영향) | 관통 |
| ★`V1022_REFERENCE_LEDGER.md` | 인용 가능 키 원장(v1.0.21 V1 승계 선언 + R2+ 신규 등재 20키) | 관통 |
| ★`AUDIT_LINEAGE_v19_v22.md` | 계보 무결 감사 보고(v19→v22 미로그 축소·생략·왜곡 색출 = 0건) | RA |
| ★`R1B_SWEEP_LIST.md` | 구획 전환 스윕 분류표(T1/T2/T3/L1/W/OK — R2/R3 인계) | R1b |
| `snapshot_v1022_r1.json` | R1 구조 스냅샷 baseline(라벨 집합·eqblock 정규화 해시·자산·bibitem) — diff 대조용 | R1 |
| ★`tools_check_structure.py` | 구조 검증·스냅샷·diff 도구(check/snapshot/diff — 라벨 dup·미해소·cite↔bib·env 짝·자산) | R1(S-007) |
| `__pycache__/tools_check_structure.cpython-311.pyc` | 파이썬 바이트코드 캐시(도구 실행 부산물 — 산출물 아님) | 부산물 |
| ★`MERGE_READINESS.md` | 병합 준비 상태 문서(라벨 유일성·매크로·서지·절차·주의점 9) — **R9 산출** | R9 |
| ★`HANDOVER_v1.0.22.md` | 인계 문서(phase 연혁·최종 상태·산출물 지도·결정 대기·다음 버전) — **R9 산출** | R9 |
| ★`INDEX_v1022.md` | 본 색인 — **R9 산출** | R9 |

---

## `comp_R2/` — 흑연 장 완성 (R2)

| 파일 | 설명 |
|---|---|
| `BRIEF_A.md` / `BRIEF_B.md` / `BRIEF_C.md` | R2 3창 기동 브리핑(A=이음매·B=인용 다리·C=통계역학 증축) |
| `CHERRYPICK_R2.md` | 마스터 체리픽 결정(R-1 병합·R-2/R-3 트림·가드 2) |
| `A_seams/SEAM_PLAN.md` | 구획 전환 이음매 집행 계획(SEAM 78행 + W 20행) |
| `A_seams/MISC_8ITEMS.md` | 잡항 8건(부록 letter 충돌 Option 2 등 — S-010) |
| `A_seams/W_RULE.md` | "본 장/본 파트/본서" 어휘 규칙(W_RULE) |
| `A_seams/ch2_sec00_intro_partT.tex` | Part T 서두 "서" 격 개작 초안 |
| `A_seams/ch2_sec10_closing_partT.tex` | Part T 맺음 격 개작 초안 |
| `B_bridges/BRIDGE_TARGETS.md` | 인용 다리 대상 선별(흑연분) |
| `B_bridges/BRIDGE_DRAFTS.md` | 인용 다리 srcbox 초안 모음 |
| `B_bridges/BRIDGE_RISK.md` | 다리 리스크·"확인 필요" 규약 |
| `B_bridges/br_bazant2013.tex` | 다리 초안 — bazant2013(BV χ-분할, eq:br-bazant2013-1) |
| `B_bridges/br_dreyer.tex` | 다리 초안 — dreyer2010/2011(히스 결과 구조) |
| `B_bridges/br_mckinnon1983.tex` | 다리 초안 — mckinnon1983(등온선) |
| `B_bridges/br_weppner_huggins1977.tex` | 다리 초안 — weppner_huggins1977(GITT 측정 원전) |
| `B_bridges/br_baek_pilon2022.tex` | 다리 초안 — baek_pilon2022(엔트로피 판독틀, R-1 병합) |
| `B_bridges/br_bernardi1985.tex` | 다리 초안 — bernardi1985(가역 발열 eq:qrev) |
| `B_bridges/br_allart2018.tex` | 다리 초안 — allart2018(ΔS⁰_j 검증) |
| `B_bridges/br_reynier2003.tex` | 다리 초안 — reynier2003(ΔS_vib 음 baseline) |
| `C_statmech/CLT_DRAFT.tex` | CLT 종형 broadening bgbox 초안(A-011) |
| `C_statmech/CNT_LINK_DRAFT.tex` | CNT 과주행 핵생성 연결 문단 초안(A-012) |
| `C_statmech/REMOVAL_CHECK.md` | 통계역학 블록 제거 용이성 점검(D22-6 사후 제거 조항 대응) |

## `comp_R3/` — LCO 장 완성 (R3)

| 파일 | 설명 |
|---|---|
| `BRIEF_D.md` / `BRIEF_E.md` | R3 기동 브리핑(D=추가 텀 이음매·E=인용 다리 LCO분) |
| `CHERRYPICK_R3.md` | 마스터 체리픽 결정 |
| `D_seams/SEAM_PLAN_R3.md` | LCO 이음매 계획(전환 15·신규 축약형 stale 5) |
| `D_seams/ADDTERM_CHECK.md` | "추가 텀만" 방식 정합 점검 |
| `D_seams/INTRO_NOTATION_FINAL.md` | 장 서두·계승 2단 기호표 확정 |
| `E_bridges/BRIDGE_TARGETS_LCO.md` | LCO 다리 대상 선별 |
| `E_bridges/BRIDGE_DRAFTS_LCO.md` | LCO 다리 초안 모음 |
| `E_bridges/L2_TIER_CANDIDATES.md` | L2 tier 실측 앵커 후보 3건 검증(reynier2004·menetrier1999·kim) |
| `E_bridges/L5_CHARGEORDER_CHECK.md` | L5 charge-order ΔS 0.47/1.49 원전 검증(tier-C 유지 판정) |
| `E_bridges/br_marianetti2004.tex` | 다리 초안 — marianetti2004(MIT 게이트) |
| `E_bridges/br_vanderven1998.tex` | 다리 초안 — vanderven1998(상도표 Ω^cat) |
| `E_bridges/br_reynier2004.tex` | 다리 초안 — reynier2004(엔트로피 삼분해) |
| `E_bridges/br_msmr_lineage.tex` | 다리 초안 — MSMR 계보(msmr_origin2017·bakerverbrugge2018) |

## `comp_R4/` — Si·블렌드 조사 (R4, 저비용→승급)

| 파일 | 설명 |
|---|---|
| `BRIEF_R4.md` | R4 조사 브리핑(D22-4 2단) |
| `REPORT_R4_COMPLETE.md` | R4 완료 보고(4축 22건 검증 확보 판정) |
| `SI_CASES.md` | Si 케이스별 문헌 조사(저비용 1창) |
| `SI_ENTROPY.md` | Si 부분몰 엔트로피 조사 |
| `BLEND_ALIGN.md` | 블렌드 전위 정렬 문헌(host 전환 비가산 시사) |
| `L2_REGISTER_PREP.md` | L2 등재 준비(kim_entropymetry2020) |
| `L5_RESOURCE.md` | L5 재소싱 자료 |
| `upgraded/SIOX_CASES.md` | 승급(sonnet) 재조사 — SiO$_x$ 케이스 5건 |
| `upgraded/SIC_CASES.md` | 승급 재조사 — Si–C 케이스 3건 |
| `upgraded/SI_ENTROPY_UP.md` | 승급 재조사 — Si 엔트로피 6건 |
| `upgraded/BLEND_UP.md` | 승급 재조사 — 블렌드 8건 |

## `comp_R5/` — Ch3 저작 경쟁 (R5, 오푸스 3창)

| 파일 | 설명 |
|---|---|
| `BRIEF_R5.md` | R5 저작 브리핑(경쟁 3창 규약) |
| `CHERRYPICK_R5.md` | 절 단위 체리픽·그래프팅(§3.1 W3·§3.2 W2·§3.3 W1+W3·§3.4 W1·§3.5 W3) |
| `W1/DESIGN_NOTE.md` + `W1/notation.tex` + `W1/s31_map.tex`~`s35_code.tex` | 창1(이론 편향) 독립 저작 688행 — 기호표+5절 |
| `W2/DESIGN_NOTE.md` + `W2/notation.tex` + `W2/s31_map.tex`~`s35_code.tex` | 창2(실측 편향) 독립 저작 592행 |
| `W3/DESIGN_NOTE.md` + `W3/notation.tex` + `W3/s31_map.tex`~`s35_code.tex` | 창3(교육 편향) 독립 저작 669행 |

## `comp_RV/` — 선행 검수 (RV)

| 파일 | 설명 |
|---|---|
| `RV1_CH1_REPORT.md` | Ch1 검수(H0·M3·L7 + 수치 3군 재산출 일치) |
| `RV2_CH2_REPORT.md` | Ch2 검수(H0·M3·L6 + xr 28라벨 aux 대조·산술 전건 재계산) |
| ★`RV3_CROSS_REPORT.md` | 장 간 교차 검수(H2·M4·L5 + 130 xr census + **§5 병합 대비 9항** — MERGE_READINESS 입력) |

## `comp_SM2/` — 통계역학 심화 (SM2)

| 파일 | 설명 |
|---|---|
| `SM2_SURVEY.md` | DIRECTION 후보 풀 소진 판정 조사 |
| `SM2_REMOVAL.md` | 심화 블록 제거 용이성 점검(D22 유보 대응) |
| `SM2_DRAFTS/SM2A_susceptibility.tex` | 평형 peak=등온 감수율 항등 bgbox 초안(A-016 §6) |
| `SM2_DRAFTS/SM2B_ensemble_equiv.tex` | 앙상블 동등성=상대 요동 소멸 bgbox 초안(§2.5) |
| `SM2_DRAFTS/SM2C_two_responses.tex` | 한 자유에너지의 두 응답 bgbox 초안(Part T §2.7) |

## `comp_FR/` — 심층 검토 대공사 (FR)

| 파일 | 설명 |
|---|---|
| `BRIEF_FR_A.md` | FR Phase A 기동 브리핑(23창 절별 4관점) |
| `A01_REVIEW.md` ~ `A23_REVIEW.md` | 절별 심층 검토 보고 23본(보완/논리 재계산/설명/수식화 4관점·4-tier·완성 LaTeX 제안 보존) |
| `RESUME_FR.md` | FR 웨이브 재기동 상태(캡·인터럽트 관통) |
| ★`FR_T_H_TRIAGE_PREP.md` | H 트리아지·검산 준비(기존 14+신규 15=29 — C-040~049) |
| ★`FR_T_ML_TRIAGE.md` | M/L 트리아지 전략·풀·상태·사용자 결정 3건 |
| `EXEC_M1.md` / `EXEC_M2.md` / `EXEC_M3.md` | M 정정형 집행 전담 3창 기록(창1 Ch1·창2 Part T·창3 LCO/Si — C-051) |
| `EXEC_M4.md` | FR 후속 미세 잔여 집행 창4(A13-M1 2곳·A21-M6 동보정·A17-M6 쌍 — C-053) |

## `comp_R6/` · `comp_R7/` · `comp_R8/` — 코드·그림·이월

| 파일 | 설명 | phase |
|---|---|---|
| ★`comp_R6/R6_REPORT.md` | 블렌드 코드(`BlendedAnodeDQDV`) 구현 리포트·게이트 로그·명세 대응·정직 공백(A-017) | R6 |
| `comp_R7/F1_blend_family.tex` | 그림 초안 — fig:blend-family(블렌드 wt% 0/10/20/30 가족 dQ/dV, A-018) | R7 |
| `comp_R7/F1_NOTE.md` | F1 좌표·검증 노트(실계산·worked 교차 일치) | R7 |
| `comp_R7/F2_si_cases.tex` | 그림 초안 — fig:si-cases-shape(케이스 3계열 개형, SiOx placeholder 표식) | R7 |
| `comp_R7/F2_NOTE.md` | F2 좌표·검증 노트 | R7 |
| ★`comp_R8/R8_EXEC.md` | 이월 목록 집행(집행 14·기해소 6·SKIP 21 — 부록 카운터 R9 이관, C-054) | R8 |

---

## 통계

- 총 파일: 127(R9 3본 포함·`.pyc` 캐시 1 포함) — `.md` 85 · `.tex` 초안 39(다리·이음매·통계역학·Ch3 경쟁 W1~3·그림·SM2) · `.json` 스냅샷 1 · `.py` 도구 1 · `.pyc` 1.
- **R9 신규 3본**: `MERGE_READINESS.md`·`HANDOVER_v1.0.22.md`·`INDEX_v1022.md`.
- phase 폴더: `comp_R2`~`comp_R8`·`comp_RV`·`comp_SM2`·`comp_FR`(+ `upgraded/`·`W1~3/`·`A_seams/`·`B_bridges/`·`D_seams/`·`E_bridges/`·`SM2_DRAFTS/` 하위).

*본 색인은 R9 초안. 2026-07-18 기준 파일 트리 실사(`find results -type f`).*
