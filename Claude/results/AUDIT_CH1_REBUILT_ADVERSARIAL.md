# Ch1 rebuilt 정본 — 전체 적대 무생략 감사 (편집 전, 결함 확정)

- 일자: 2026-06-01
- 대상: `Claude/docs/graphite_ica_ch1_rebuilt.tex` (662줄, 2026-05-30 RB 재구성본; PDF = `Claude/results/graphite_ica_ch1_rebuilt.pdf`)
- 기준: 프로젝트 CLAUDE.md P3 검수 7항목 + 문건 자체 GS-1~4 + 무비약(학부 가독)
- 원칙: **추가가 아니라 검증 먼저**(사용자 6-1 지시). 본 문건은 결함 목록만. 실제 수정은 승인 후.
- 총평: 정본은 전반적으로 **매우 엄밀**. §7~9의 "변수 미정의/적분 비약"(구버전 지적)은 대부분 이미 해소됨(A_0 구분 line 477-482, Jacobian·support line 463-476, 이중계상 경고 line 521-527). 아래는 그럼에도 남은 **진짜 빈틈**.

---

## A. 실제 무생략/논리 결함 (수정 후보)

| ID | 위치 | 기준 | 결함 | 심각도 |
|----|------|------|------|--------|
| G1 | §8 line 512-530 (전체) | **P3-3** | self-consistent 되먹임($V_n\!\to\!\xi_\eq,A_j\!\to\!k_j\!\to\!L\!\to\!\Theta\!\to$전하보존$\to V_n$)이 **산문으로만** 서술됨. P3-3이 요구하는 **dependency graph 또는 표**가 없음. 어느 식·어느 변수에서 순환이 닫히는지 시각/표로 미제시. | HIGH |
| G2 | §8 line 528-530 | **P3-4** | 그 순환을 `정의상 implicit / 수치해법 필요 / 논리공백 / 물리가정충돌` **4분류로 분리 진단**하지 않음. "직접 수치적분=기본, Ch6" 한 줄로 `수치해법 필요`만 암시. P3-4 구조적 진단 누락. | HIGH |
| G3 | §8 line 493 | **GS-1** | "mode별 초기 잔차 $r(q_a)$는 post-peak 공통값으로 근사해 $A_0$ 가중에 흡수" — **단언이지 유도 아님**. $L$이 다른 mode는 post-peak 도달 $q$가 달라 $r(q_a)$가 공통일 근거가 약함. 무비약 위반 소지. | MED |
| G4 | §7→§8 접합 (line 492-498) | **GS-1** | 이산 전이합 $\sum_j Q_{j,\tot}\,\dd\xi_j/\dd q$(식 17·39)에서 단일 연속적분 $\int A_L(1/L)e^{\cdots}\dd L$(식 21)로 가는 **다리가 압축**됨. $A_L$ 안에 (i) 전이별 population $Q_{j,\tot}/Q_p$ 와 (ii) 전이 내부 $\rho_G$ 가 **어떻게 합쳐지는지** 명시 조립이 없음. 사용자가 원래 지적한 "$\sum\!\to\!\int$ 비약"의 잔재. | MED-HIGH |
| G5 | §5 boundbox(line 352-356) ↔ §6·§10 | **P3-4(물리가정충돌) / 유효범위** | 선형 배리어 낮춤 $-\chi_j\mathcal A_j$는 **$\lvert\mathcal A_j\rvert$ 작을 때($V_\drive\!\approx\!U_j$)만 유효**라 명시. 그러나 꼬리=post-peak는 $V_n$이 $U_j$에서 **멀어진** 영역이라 $\lvert V_\drive-U_j\rvert$↑ → $\mathcal A_j$↑. "꼬리 영역=$V_\drive\!\approx\!U_j$"라는 line 355 주장과 post-peak 정의가 **상충 가능**. 유효범위 자기모순 해소 필요. | MED-HIGH |
| G6 | §4 (iii) line 220-221 | **GS-1** | 전기화학 평형조건 $\mu(\xi_\eq)=s_{\phi,j}F(V_n-U_j^0)$ 을 **유도 없이 단언**. 전기화학퍼텐셜 등식($\tilde\mu_\mathrm{Li}=\tilde\mu_{\mathrm{Li}^+}+\tilde\mu_{e^-}$)에서 한 줄 유도가 빠짐. 무비약 경미 위반. | LOW-MED |

## B. 이미 정직하게 FLAGGED 된 모형 가정 (결함 아님 — 수용 여부만 확인)

| ID | 위치 | 내용 | 판단 |
|----|------|------|------|
| F1 | §5 keystone(331-351) | $\chi_j\mathcal A_j$=방향 없는 common-mode mobility 가속(Level A); Marcus 비대칭을 대칭 평균한 모형 선택 | 정직 표기됨. 수용 가능 |
| F2 | §7 flagbox(436-442) | 독립 평행 1차 완화(평균장 ansatz), 협동적 1차 상전이 무시 | 정직 표기됨 |
| F3 | §4 flagbox(263-269) | logistic vs erf 평형 형태 — 흑연 열역학 유도 부재 | 정직 표기됨 |
| F4 | §7 boundbox(483-487) | $\rho_G$ 역매핑 비유일 → forward-only | 정직 표기됨 |

## C. 교차파일 검증 필요 (ch1 단독으로 확정 불가 — 다음 단계 후보)

| ID | 기준 | 확인 대상 |
|----|------|-----------|
| C1 | **P3-5** | ref.6,7(사용자 JCP 2017) 방법론 — ch1은 "ratio-substitution closed-form, Ch6 위임"(line 528)으로 **연기**. P3-5의 4소항목(서지·논문 내 위치·수학구조·변수매핑·물리가정차이) 기록이 Ch6에 있는지, 혹은 ch1 연기가 의도인지 확인. |
| C2 | **P3-6** | "Chapter 2-6 전달"(line 612-616)이 실제 `graphite_ica_ch2~6_rebuilt.tex` 도입부와 충돌 없는지 cross-check. |
| C3 | **GS-3** | 본문 `[AL-1]~[AL-16]` 번호가 `Claude/results/RB_LEDGER_CH1.md`/`RB_AL_MASTER.md` 마스터 체계와 일치하는지. |

## D. P3 7항목 통과표

| P3 | 항목 | 상태 |
|----|------|------|
| 1 | $V_n/V_{n,app}/V_{n,drive}/V_{n,OCV}$ 일관 | PASS (notation 112-115, §5 일관) |
| 2 | 전하보존=중심식(OCV lookup 회귀 X) | PASS (강하게 명시, line 176-177) |
| 3 | 순환의존 dependency graph/표 | **FAIL → G1** |
| 4 | 순환 4분류 진단 | **FAIL → G2** |
| 5 | ref.6,7 4소항목 | 연기(Ch6) → C1 확인 |
| 6 | Ch1↔Ch2-5 전달 정합 | 미검증 → C2 |
| 7 | ver.N vs Chapter 명칭 혼동 | PASS (Chapter 명칭 일관) |

## 권고 (수정은 승인 후)

- 즉시 수정 가치 높음: **G1, G2**(P3 명시 FAIL — dependency graph + 4분류 박스 신설, 순수 추가라 기존 식 불변).
- 무생략 보강: **G4, G3, G5, G6**(기존 유도의 다리 메우기/유효범위 봉합 — 본문 수정 동반).
- 다음 단계: C1~C3 교차파일 검증(원하시면 진행).
