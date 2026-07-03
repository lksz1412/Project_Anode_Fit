# V1.0.14 EXECUTION LEDGER — 어투·물리 엄밀성·Appendix 재배치·코드-문건 연계 정정·이미지 경연

> 마스터 = `../../plans/2026-07-04-v1014-tone-rigor-appendix-figures-plan.md`(rev.2, GO 2026-07-04). 우선순위: ①물리 무결 ②비약 제거 ③수식-주도 ④논문·교과서급 어투. 문건 체리피킹 X(절별 루핑)·이미지만 9종 경연. Sonnet=스캔·초벌·서치, Fable=유도·판정·체리픽. v1.0.13 동결(5995d64) — 증판 = docs/v1.0.14/. 상태 ⬜/🔄/✅.

| Phase | 이름 | Steps | 산출 | Gate | 상태 |
|---|---|---|---|---|---|
| 1.1 | 증판+전수 감사(어투·코드 언급) | 1–4 | v1.0.14/·TONE_AUDIT | 감사 coverage 전문·판정 100% | ✅ |
| 2.1 | 물리 엄밀성 3건(eq1.8 Hill·PSD 유도-배제·spinodal App 초안) | 5–9 | tex 개정·appendix_phase_separation | Fable 재검산·빌드 | ⬜ |
| 2.2 | 구조 재배치(§1.13→App 표·코드 대응 App·§1.7 보강) | 10–14 | tex 개정·App B/C | ref 0·orphan 0 | ⬜ |
| 3.1 | 어투 절별 루핑 | 15–19 | tex 개정 | 감사 전 항목 처분·수식 해시 diff 0 | ⬜ |
| 3.2 | 레퍼런스 보강 | 20–22 | REF_SOURCES·cite 병기 | 전 수치 인용 or [근거 미발견] | ⬜ |
| 4.1 | 축소 검수 5회 | 23–28 | REVIEW_R1..5 | 수렴=연속 2R 확정 0(조기 종료 가) | ⬜ |
| 5.1 | 이미지 경연(대상 ~10 × 9안 S3/O3/C3) | 29–34 | FIG_CONTEST_*·편입 | 좌표 재검산·정합 | ⬜ |
| 6.1 | 마감 | 35–37 | RESULT·HANDOVER·INDEX | 최종 게이트 | ⬜ |

## 진행 로그 (append-only)
- 2026-07-04 GO: 계획 rev.2 승인(면밀 유도 우선 — eq1.8 은 사전 설명·사용자 납득 완료: Hill Ch.7 Langmuir 유도, hard-core 배타 가정 명시·q(T) 연속 자유도 적분·분자분모 상쇄·ε̃ 흡수·Ch2 기호 통일·vib 엔트로피 연결). Step 1 증판 완료: v1.0.14/ 복사·버전 문자열 정밀 패치(계보 연장·잔재 0)·기준선 게이트 green(ch1 0-err/50p/ref 0[3-pass]/of 0·ch2 0-err/14p·회귀 bit-exact 13/13).
- 2026-07-04 P1.1 Steps 2–4 완료: Sonnet 감사 2기 병렬(어투 79건 — 판 이력 태그 16·구어 은유 20·훈계 6·예외 가드 19 / 코드 언급 83행 — 인라인 45·코드주어문 23·표 5·codebox 2, grep 교차 누락 0) → Fable 전 항목 판정 `V1014_AUDIT_ADJUDICATION.md`(채택 130·수정 채택 12·기각 6; ★가드 19건 전건 유지 확정, 부록 = A 검산표·B 구현 대응표로 재지정). 게이트 PASS(coverage 전문·판정 100%).
- 2026-07-04 Step 7 선행 완료(감사 병행 중 본문 무수정 작업으로 우선 처리): `appendix_phase_separation.tex` 독립 초안 — 혼합 자유에너지 격자 유도→현·지렛대→공통접선·binodal(T/T_c 닫힌꼴)→spinodal(요동 2차 전개)→Maxwell 등면적(공통접선 조건의 적분 번역)→핵생성(r*·ΔG* 유도) vs spinodal 분해(Cahn–Hilliard R(k)) + 그림 2매(공통접선 구성 Ω=3RT·상평형도 binodal/spinodal, 좌표 전부 수치 검산: ξ_b=0.0707/0.9293·f_b/RT=−0.0583·ξ_s=0.2113/0.7887·T/T_c=2/3 등온 교점 일치). 빌드 0-err/7p/ref 0/of 0. ★편입 보류 — 사용자 검토 대기(계획 Step 7 사양). 본문 §1.2·§1.5 "부록 참조" 연결은 편입 확정 시 삽입.
- ※계획 표기 정정(Fable 검산): 계획서 Step 5 ③의 vib 엔트로피 부호 표기 "−k_B∂(T ln q)/∂T" 는 q 를 점유 상태 내부 분배함수로 쓸 때 **+k_B∂(T ln q)/∂T** 가 옳다(f_int=−k_BT ln q, S=−∂f/∂T; 조화 모드 검산 S=k_B[(1+n̄)ln(1+n̄)−n̄ ln n̄] 재현 확인). 본문 신설 유도에는 옳은 부호로 기입한다.
