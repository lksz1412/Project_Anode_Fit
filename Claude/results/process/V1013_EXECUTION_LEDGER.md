# V1.0.13 EXECUTION LEDGER — 통계역학-first 재구조화 + LCO 후방 통합 + 문건-코드 루프

> 마스터 = `../../plans/2026-07-02-v1013-restructure-master-plan.md`(rev.4). 우선순위(사용자 GO): ①물리 논리 결함 제거(발견 시 정정 필수) ②논리 비약 제거 ③수식-주도. 작성 N=6(S2·C2·F2)+Fable 체리픽(가중3)+figure 경쟁 / 검수 = Fable 단독 10회 가변-청크(수렴=연속 2R 0결함). 사용자 부재 — 자율 완주. 상태 ⬜/🔄/✅.

| Phase | 이름 | Steps | 산출 | Gate | 상태 |
|---|---|---|---|---|---|
| 1.1 | 설계 확정 + 증판 | 1–5 | docs/v1.0.13/·구조맵·용어표·산문예산·CODE_MAP | 4산출물·참조 카운트·orphan 0 | 🔄 |
| 2.1 | Part 0 신설(N=6+figure) | 6–11 | P21 드래프트 6·체리픽 map | ξ_eq 완결 유도·중복 0·산문 예산 | ⬜ |
| 2.2 | Part I 흑연부 재배열·압축 | 12–17 | Ch1 Part I | lco-* 참조 0·빌드·수치 grep | ⬜ |
| 2.3 | 코드 루프 A(흑연) | 18–20 | CODE_MAP 갱신·주석 동기 | orphan 0·회귀 13/13 불변 | ⬜ |
| 3.1 | Part II LCO 재조립·압축 | 21–26 | Ch1 Part II·eq 분할 | 산문 감축·참조 해소·빌드 | ⬜ |
| 3.2 | 코드 루프 B(LCO 3건) | 27–30 | 전극 인지 σ_d·dict T1·docstring | 회귀 불변·의도변경 대조 | ⬜ |
| 4.1 | 용어·약자·overfull 전수 | 31–34 | TERMS 적용·분할 | 전 항목 처분·Overfull>10pt 0 | ⬜ |
| 5.1 | Fable 10회 가변-청크 검수 | 35–40 | REVIEW_R1..10·finalizer | 연속 2R 0결함·전 게이트 | ⬜ |
| 6.1 | Ch2 정합·가이드·샘플·마감 | 41–45 | Ch2·GUIDE·sample·result·INDEX | 두 축·상호충실도 | ⬜ |

## 진행 로그 (append-only)
- 2026-07-03 새벽: P1.1(79e83fc)→P2.1 N=6+체리픽(3fc811a)→커밋A Part 0+C-1(8c4f21e)→커밋B Part II 통합(4b9480f)→루프 A/B(4f1ab12 — 전극 인지 σ_d·T1 재정렬·회귀 불변)→압축 p2/p3(377b5e6)·p1/p4(1bb914c)→용어·overfull 0(363dcf9)→P6 선행(95768e0). P5 R1(Fable×3 통독): 물리 불변 3/3 PASS·HIGH 4(전부 라벨·층위·충실도 — 물리식 위반 0)·MED 18 → master 삼각검증·정정 30여 건(363f5fd). 압축 처분 기록: p3 signcheck 콜론계 기각·p3 잔여 2쌍(생략부 인용)·p4 2쌍 R6 이월. R2(절 단위·⑧렌즈) 발진.
- 2026-07-02 야간 GO: 우선순위 서열 접수(마스터 rev.4). docs/v1.0.13/ 증판(tex 2·py·guide·스크립트 5·figs/) + 버전 문자열 정밀 패치(계보 연장).
- **P1.1 ✅ (S1–S5)**: 구조맵(master — Part 0 배치=N0 직후·Part II 순서·라벨 불변 원칙·리스크) / 용어표(27용어·18약자 — ★FD 약자 충돌(Fermi–Dirac vs finite difference 동일 챕터)·전이/천이 이원화·MSMR 정의 1750줄 지연·GITT/OCV/SOC/DFT 미병기·격자 다의성) / 산문예산(★LCO 밀도 5.75 < 흑연 8.04 — 말 많음의 실체는 구조; outlier=broadening 59문장/1식; 목표 확정 = 세부계획 추기) / CODE_MAP(boxed 30 전수·orphan 13 전부 선언된 항목·창작 0·dead code `func_U_j_hys` 발견 — 루프 A 처분 대상). gate: 4산출물+스크립트 존재·라인 정합 검산 PASS.
- **P2.1 진행**: Codex C1·C2 전 스텝(s1 갈래1 → s2 갈래2+figure) 완료(32.5KB·26.8KB — 스텝별 구동·폴링 감시 준수, 거짓 양성 폴러 1회 교정). F1·F2(Fable)·S1·S2(Sonnet) 가동 중.
- **★게이트 실효성 정정(발견·교정)**: v1.0.12 폴더의 demo_lco_heat·plot_dqdv·test_regression 이 **v1.0.10 코드 경로를 로드**하고 있었음(증판 포인터 잔재). 또한 v1.0.12 커밋3 게이트에서 `test_regression_graphite.py`를 인자 없이 실행 → **capture 모드였음(verify 아님)** — "회귀 13/13" 보고는 실효 게이트가 아니었음을 정정. 물리 결론은 유지(주석-only 변경 + 금회 진짜 verify 로 재확증). v1.0.13 교정: CODE→v1.0.13(env override 가능)·GOLD→프로젝트 내 `golden_graphite_ref.npz`(v1.0.10 코드로 캡처) → **verify 13/13 bit-exact PASS**(v1.0.13 코드 ↔ v1.0.10 golden). demo/plot 포인터 v1.0.13 로 교정.
