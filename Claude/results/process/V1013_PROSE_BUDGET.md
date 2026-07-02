# V1.0.13 Prose Budget — 실측 (P1.1 S3)

측정 대상: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` (2358 lines) ·
`Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex` (777 lines).
측정 스크립트: `Claude/results/process/V1013_prose_count.py` (같은 폴더, 재현 가능).
**본 문서는 실측 보고서다 — 대상 .tex 파일은 일절 수정하지 않았다.**

전문 정독 확인: Ch1 전체(1-2358행) · Ch2 전체(1-777행) 순서대로 생략 없이 head→tail 정독 완료.

---

## 1. 산정 기준 (스크립트 docstring 요지 — 전체는 .py 파일 참조)

| 항목 | 정의 |
|---|---|
| **절 단위** | `\section*{}` · `\section{}` · `\subsection{}` 각 1개 = 1행. 한 헤딩의 "own block" = 그 헤딩 줄부터 **다음 헤딩(같은 레벨이든 하위 subsection 이든) 직전 줄까지** — `\section` 은 그 아래 `\subsection` 들의 본문을 포함하지 않음(별도 행으로 분리 후 하단에서 합산). 마지막 헤딩은 `\begin{thebibliography}` 직전(없으면 `\end{document}` 직전)에서 절단. |
| **줄 수** | 위 own-block 이 원본 파일에서 차지하는 raw 줄 수(헤딩 줄 포함, 다음 헤딩 줄 제외). 전 헤딩의 줄 수 합 = 서론/서~맺음 사이 본문 총 줄 수와 정확히 일치함을 검산(Ch1 2203줄, Ch2 693줄 — 각각 정합 확인). |
| **equation류 환경 수** | `\begin{equation*?}`·`align*?`·`alignat*?`·`multline*?`·`gather*?`·`eqnarray*?` + 단독 `\[ ... \]` 블록의 개수 합. `\begin{cases}...\end{cases}` 는 위 환경에 항상 내포되어 있어(양쪽 파일 전수 확인) 별도 가산 안 함. **함정 발견·수정**: `\\[2pt]`/`\\[0.35em]` 류 LaTeX 줄바꿈-간격 토큰(이중 backslash + 대괄호)이 단독 `\[` 표시수식 개시로 오탐되는 버그를 raw grep 대조로 발견(Ch1 4건, 전부 `\begin{equation}` 내부 nested — 산문 스트립엔 무해, equation count 만 오염됐었음) → `(?<!\\)` 부정 lookbehind 로 수정 후 재검증. |
| **산문 문장 수** | preamble(`\begin{document}` 이전) 제외 · 주석(`%` 미이스케이프 이후) 제거 · 위 equation류 블록·`\[...\]` 제거(공백 치환, 앞뒤 문장은 이어붙음) · `figure`/`table`/`longtable`/`thebibliography` 환경 전체 제거(캡션·표 셀은 "산문"에 불포함 — 서술 흐름이 아닌 구조/보조 콘텐츠로 분류) · 버전/소수 숫자열(`\d+(\.\d+)+`, 예 "1.0.13"·"0.0853") 보호 후 인라인 수식 `$...$` 제거 · `\textbf`/`\emph`/`\textit`/`\footnote`/`\code` 는 내용만 남기고 unwrap · `\cite`/`\ref`/`\eqref`/`\label` 은 통째 제거 · 잔여 LaTeX 명령·중괄호 제거 후, `[.!?]` 로 끝나는 청크 수를 센다(마지막에 종결부호 없이 남는 5자 이상 잔여 조각은 +1). **이것은 언어학적 문장 분리기가 아니라 전 절에 동일 적용되는 재현 가능한 규칙**이므로 절대값보다 절 간 상대 비교(문장/수식 비율)에 신뢰도가 있다. |
| **LCO 판정** | 헤딩의 `\label` 문자열에 `lco` 부분문자열 포함(대소문자 무관) 여부. `\label` 없는 subsection(대부분 상위 `\section`의 유도를 이어받는 하위 단계 — 예: sec:center 자체 본문은 3문장뿐이고 그 밑 무-라벨 subsection 둘이 실제 유도 24문장을 담음)은 "흑연 본체"로 귀속(별도 "공통/서론" 버킷은 스크립트 원시 출력에만 존재, 본 보고서 소계에서는 흑연 본체에 합산 — 근거: 이 문건의 라벨링 관행상 LCO 전용 subsection 은 전부 명시적으로 라벨링되어 있고 그 외 subsection 무라벨은 전극-불문 공통 유도이기 때문). Ch2 는 lco- 라벨 헤딩이 전무하여 전체가 단일 Ch2 소계로 귀속. |

---

## 2. 절별 표 — Chapter 1, 흑연 본체 (32개 헤딩)

| Level | 절 | Label | Lines(구간/개수) | #Eq | #Sent |
|---|---|---|---:|---:|---:|
| section | 서론 — 이 문건이 따라가는 것 | (unlabeled) | 130-196 (67) | 0 | 14 |
| section | 기호와 규약, 실험조건 매핑 (N0) | sec:notation | 197-300 (104) | 1 | 14 |
| section | 분극 — 측정 전위에서 내부 전위로 (N1) | sec:pol | 357-361 (5) | 0 | 2 |
| subsection | 분극 부호 — 방향이 결정한다 | (unlabeled) | 362-385 (24) | 3 | 9 |
| subsection | 작업 격자 — 꼬리가 들어올 여유 | (unlabeled) | 386-410 (25) | 1 | 11 |
| section | 평형 중심 $U_j(T)$ — 열역학에서 (N2) | sec:center | 411-416 (6) | 0 | 3 |
| subsection | $G,\mu$ 와 평형 조건 — 유도 | (unlabeled) | 417-447 (31) | 4 | 10 |
| subsection | $U_j(T)$ — 온도 환산 | (unlabeled) | 448-475 (28) | 2 | 14 |
| section | 히스테리시스 분기 중심 (N3) | sec:hys | 578-585 (8) | 0 | 3 |
| subsection | 상호작용이 평형을 비트는 곳 | (unlabeled) | 586-646 (61) | 4 | 9 |
| subsection | gap 의 닫힌 꼴 | (unlabeled) | 647-692 (46) | 4 | 11 |
| subsection | 방향별 분기 중심 $U_j^{\,d}$ | (unlabeled) | 693-751 (59) | 3 | 9 |
| section | 폭과 평형 점유 $\xi_\eq$ (N4, N5) | sec:width | 918-923 (6) | 0 | 3 |
| subsection | 폭 $w_j$ — 이상 극한과 그 이중지위 | (unlabeled) | 924-952 (29) | 1 | 11 |
| subsection | 평형 점유 — logistic 의 유도 | (unlabeled) | 953-1065 (113) | 4 | 19 |
| subsection | 같은 결과의 분포 관점 | sec:dist | 1066-1140 (75) | 2 | 24 |
| section | 평형 peak — $|I|\to0$ 기준선 (N6) | sec:eqpeak | 1380-1415 (36) | 2 | 14 |
| subsection | **평형 델타가 실측 종이 되는 까닭 (broadening)** | sec:broadening | 1489-1669 (181) | 1 | **59** |
| section | 동역학 지연 길이 $L_V$ (N7) | sec:lag | 1670-1675 (6) | 0 | 3 |
| subsection | 지연의 보편 방정식과 $L_q$ | (unlabeled) | 1676-1701 (26) | 3 | 8 |
| subsection | 컷 affinity $\mathcal A$ | (unlabeled) | 1702-1717 (16) | 1 | 8 |
| subsection | 방향별 전달 계수와 유효 장벽 | (unlabeled) | 1718-1736 (19) | 2 | 5 |
| subsection | $L_q$ 의 평가와 전압축 환산 $L_V$ | (unlabeled) | 1737-1781 (45) | 3 | 21 |
| section | 인과 기억 꼬리와 충전 격자 역전 (N8) | sec:tail | 1782-1786 (5) | 0 | 2 |
| subsection | 지수 기억 — 일반해의 이산형 | (unlabeled) | 1787-1839 (53) | 3 | 11 |
| subsection | peak 모양 — 평형에서 지연을 뺀 것 | (unlabeled) | 1840-1874 (35) | 2 | 12 |
| subsection | ★충전 격자 역전 | (unlabeled) | 1875-1926 (52) | 1 | 7 |
| section | 합산과 역보간 (N9) | sec:sum | 1927-1942 (16) | 1 | 4 |
| subsection | staging 전이 초기값 | (unlabeled) | 1943-1969 (27) | 0 | 4 |
| subsection | 전체 입력 인자와 기본값 | (unlabeled) | 2188-2241 (54) | 0 | 14 |
| subsection | facade 와 전체 진행 한눈에 | (unlabeled) | 2242-2278 (37) | 0 | 3 |
| section | **부호 사슬 전수 검산** | sec:signcheck | 2279-2332 (54) | 0 | **45** |
| **소계** | | | **1349줄** | **48** | **386** |

## 3. 절별 표 — Chapter 1, LCO 관련 (10개 헤딩, `sec:lco-*`)

| Level | 절 | Label | Lines(구간/개수) | #Eq | #Sent |
|---|---|---|---:|---:|---:|
| subsection | 두 번째 전극 — LCO 양극으로의 일반화 | sec:lco-map | 301-356 (56) | 0 | 15 |
| subsection | LCO 평형 중심과 $\partial U_j/\partial T$ | sec:lco-center | 476-577 (102) | 5 | 31 |
| subsection | LCO order--disorder 와 MIT 2상역 | sec:lco-hys | 752-917 (166) | 12 | 34 |
| section | LCO 전자 엔트로피 항 (N5+) | sec:lco-electronic | 1141-1150 (10) | 0 | 5 |
| subsection | 왜 흑연엔 없고 LCO엔 있나 | sec:lco-why | 1151-1160 (10) | 0 | 5 |
| subsection | Fermi--Dirac → Sommerfeld 유도 | sec:lco-Se | 1161-1277 (117) | 7 | 47 |
| subsection | $g(E_F,x)$ MIT-logistic 게이트 | sec:lco-gate | 1278-1379 (102) | 2 | 34 |
| subsection | LCO dQ/dV peak — 세 봉우리 | sec:lco-peak | 1416-1488 (73) | 4 | 18 |
| subsection | LCO $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해 | sec:lco-decomp | 1970-2063 (94) | 5 | 34 |
| subsection | forward 코드의 LCO 일반화 | sec:lco-code | 2064-2187 (124) | 9 | 30 |
| **소계** | | | **854줄** | **44** | **253** |

## 4. 절별 표 — Chapter 2 (20개 헤딩)

| Level | 절 | Label | Lines(구간/개수) | #Eq | #Sent |
|---|---|---|---:|---:|---:|
| section | 서 — 왜 엔트로피에는 통계가 필요한가 | (unlabeled) | 67-110 (44) | 2 | 24 |
| section | 격자기체 분배함수에서 점유 분포로 | sec:partition | 111-119 (9) | 0 | 4 |
| subsection | 단일 자리 대정준 분배함수 | (unlabeled) | 120-139 (20) | 2 | 4 |
| subsection | 전기화학 퍼텐셜과 Ch1 logistic 의 기원 | ssec:logistic | 140-189 (50) | 3 | 14 |
| subsection | 다자리 평균장 — Bragg--Williams | ssec:BW | 190-220 (31) | 3 | 11 |
| section | 점유 분포에서 configurational 엔트로피로 | sec:config | 221-233 (13) | 1 | 3 |
| subsection | 부분몰 configurational 엔트로피 | (unlabeled) | 234-323 (90) | 3 | 22 |
| subsection | 문헌 검증 | (unlabeled) | 324-365 (42) | 0 | 7 |
| section | vibrational·electronic 엔트로피 | sec:vibel | 366-371 (6) | 0 | 3 |
| subsection | vibrational 엔트로피 — Bose--Einstein | (unlabeled) | 372-393 (22) | 1 | 12 |
| subsection | electronic 엔트로피 — Fermi--Dirac/Sommerfeld | ssec:elec | 394-435 (42) | 2 | 16 |
| subsection | 반응 vs 활성화 엔트로피 | (unlabeled) | 436-442 (7) | 0 | 4 |
| section | 섞임과 겹침 | sec:mixing | 443-451 (9) | 0 | 4 |
| subsection | 파생 A — 겹침의 dQ/dV-비중 가중 | ssec:overlap | 452-546 (95) | 5 | 18 |
| subsection | 파생 B — 이중계산 분리 | (unlabeled) | 547-561 (15) | 1 | 5 |
| subsection | **파생 C — 폭 $w$ 의 지위** | ssec:weff | 562-592 (31) | 0 | **18** |
| subsection | 파생 D — 히스테리시스 | ssec:hys | 593-622 (30) | 2 | 8 |
| section | 극한과 코너 | sec:limits | 623-663 (41) | 0 | 11 |
| section | **가역 발열 — 분포를 재배열하는 열** | sec:revheat | 664-745 (82) | 2 | **37** |
| section | 맺음 | (unlabeled) | 746-759 (14) | 0 | 5 |
| **소계** | | | **693줄** | **27** | **230** |

---

## 5. 소계 요약

| 그룹 | 헤딩 수 | 줄 수 | equation류 | 산문 문장 | 문장/수식 비 |
|---|---:|---:|---:|---:|---:|
| **흑연 본체** (Ch1, non-LCO) | 32 | 1349 | 48 | 386 | 8.04 |
| **LCO** (Ch1, `sec:lco-*`) | 10 | 854 | 44 | 253 | 5.75 |
| **Ch2** (전체) | 20 | 693 | 27 | 230 | 8.52 |
| Ch1 합계 (참고) | 42 | 2203 | 92 | 639 | 6.95 |

라인 수 검산: 흑연본체(1349)+LCO(854)=2203=Ch1 서론~부호검산 구간 실제 줄 수(2332-130+1)와 정확히 일치. Ch2(693)=서~맺음 구간 실제 줄 수(759-67+1)와 정확히 일치. 겹침·누락 0.

흥미로운 점: 문장/수식 비율만 보면 LCO(5.75)가 흑연 본체(8.04)·Ch2(8.52)보다 오히려 **낮다** — 즉 "식당 산문량"의 순수 밀도로는 LCO 가 특이하게 과한 것은 아니다. LCO 압축의 근거는 비율이 아니라 **구조적 재-서술**이다: LCO 의 10개 절 다수가 이미 흑연에서 유도된 식(예: 정규용액 상분리, 분기 중심 대칭)을 "글자 그대로 같은 식"이라고 재확인하는 대응(mapping) 절이라, 물리적으로 새로운 내용 대비 서술 오버헤드가 흑연 본체보다 크다(§6 목표치의 근거).

## 6. 문장/수식 비율 상위 5개 절 (압축 우선순위)

| 순위 | 절 | 그룹 | 문장 | 수식 | 비율 |
|---|---|---|---:|---:|---:|
| 1 | 평형 델타가 실측 종이 되는 까닭 (sec:broadening) | Ch1 흑연본체 | 59 | 1 | 59.0 |
| 2 | 부호 사슬 전수 검산 (sec:signcheck) | Ch1 흑연본체 | 45 | 0 | ∞ |
| 3 | 가역 발열 (sec:revheat) | Ch2 | 37 | 2 | 18.5 |
| 4 | 파생 C — 폭 $w$ 의 지위 (ssec:weff) | Ch2 | 18 | 0 | ∞ |
| 5 | $g(E_F,x)$ MIT-logistic 게이트 (sec:lco-gate) | Ch1 LCO | 34 | 2 | 17.0 |

(참고: 6-8위는 sec:lco-map(15문장/0식, LCO), 서론(14문장/0식), sec:notation(14문장/1식) — 모두 "수식이 거의 없는 서술/매핑 절"이라는 공통 패턴.)

---

## 7. 감축 목표 제안

**공통 원칙(전 절 적용, v6 확정 원칙 재확인)**: 수식 사이 다리 산문은 1–2문장 — "수식만 읽어도 대부분 이해"가 기준선이다. 이 원칙은 **유도가 진행 중인 절**(equation 밀도가 높은 절)에 직접 적용 가능하다. 반대로 equation 이 0~1개뿐인 절(서론·검산 체크리스트·지위 서술)은 이 산식으로 목표치를 역산할 수 없다(분모가 0에 가까워 "1.5×(식수+1)" 식이 무의미) — 이런 절은 아래처럼 별도 판단.

### 7.1 LCO 절 — ≥35% 감축 기본값 (사용자 확정 기준, 절별 목표치)

| 절 | 현재 문장 | 목표(-35%, 내림) | 삭감량 | 비율 |
|---|---:|---:|---:|---:|
| sec:lco-map | 15 | 9 | -6 | -40% |
| sec:lco-center | 31 | 20 | -11 | -35% |
| sec:lco-hys | 34 | 22 | -12 | -35% |
| sec:lco-electronic | 5 | 3 | -2 | -40% |
| sec:lco-why | 5 | 3 | -2 | -40% |
| sec:lco-Se | 47 | 30 | -17 | -36% |
| sec:lco-gate | 34 | 22 | -12 | -35% |
| sec:lco-peak | 18 | 11 | -7 | -39% |
| sec:lco-decomp | 34 | 22 | -12 | -35% |
| sec:lco-code | 30 | 19 | -11 | -37% |
| **LCO 합계** | **253** | **161** | **-92** | **-36%** |

LCO 전체를 253→161문장(-36%)으로 낮추면, Ch1 총 문장수는 639→547(-14%)이 된다(흑연 본체 386은 미변경 가정).

### 7.2 흑연 본체·Ch2 — 상위 4개 절 (평가만, 강제 목표 아님·사용자 확정 필요)

LCO 처럼 명시된 고정 비율이 없으므로, 아래는 §6 순위표 기반 **제안값**이며 그대로 적용 여부는 사용자 결정 사항이다.

- **sec:broadening (59문장/1식, 181줄) — 최우선 후보.** ①②③ 세 broadening 출처를 본문에서 설명하고, (iii-a)/(iii-b) 로 다시 쪼개 설명하고, 끝의 keybox 가 다시 한 줄로 요약하는 3중 서술 구조. keybox 로 이미 압축된 결론이 있으므로 본문 (b)(c) 문단의 상당 부분(특히 반복되는 "★" 부연 문장들)이 압축 여지가 큼. 제안 목표 범위 ~35–40문장(-32~-41%) — LCO 기본값과 유사한 폭.
- **sec:signcheck (45문장/0식, 54줄) — 구조상 체크리스트.** S1-S8 + R1-R5 는 이미 유도된 식을 \eqref 로 재확인하는 감사(audit) 목적 나열이라 압축이 곧 검증 커버리지 손실로 이어질 위험. 강한 삭감 비권장 — 문장당 정보밀도는 이미 높음(항목당 1개 결론). 제안: 경미한 손질(~-10%) 또는 미변경.
- **sec:revheat (37문장/2식, Ch2, 82줄) — 부호 규약·한계 서술 문단이 압축 표적.** keybox(계산용 종합식)·procedurebox(5단계 절차)는 이미 구조화되어 있어 그대로 두고, 그 사이 서술 문단(부호 규약 srcbox, "한계·갭" 5항목 문단)에서 절감 여지. 제안 목표 ~28-30문장(-19~-24%).
- **ssec:weff (18문장/0식, Ch2, 31줄) — 절대 길이 자체는 이미 짧음(31줄).** 비율이 높은 건 분모(식수 0)가 작아서일 뿐, 개념적으로 중요한 "narrowing 오독 차단" warnbox 를 포함하므로 큰 삭감보다 경미한 다듬기(~-15%) 권장.

---

## 8. 총계 및 8줄 요약

- **총계**: Ch1 = 42개 헤딩·2203줄·92 equation·639문장(흑연본체 386 + LCO 253). Ch2 = 20개 헤딩·693줄·27 equation·230문장.
- 문장/수식 비율은 LCO(5.75) < 흑연본체(8.04) < Ch2(8.52) — LCO 압축 근거는 밀도가 아니라 흑연 대응(mapping) 구조의 서술 오버헤드다.
- 압축 우선순위 상위 5절: ① sec:broadening(59/1) ② sec:signcheck(45/0) ③ Ch2 sec:revheat(37/2) ④ Ch2 ssec:weff(18/0) ⑤ sec:lco-gate(34/2).
- LCO 10개 절 전부에 -35%~-40% 목표치 산출(합계 253→161, -36%) — 사용자 v6 원칙(다리 산문 1–2문장) 준수 기준.
- 흑연 본체·Ch2 상위 4절은 강제 비율 없이 개별 진단(§7.2) — sec:signcheck 는 체크리스트 특성상 삭감 비권장, sec:broadening 은 LCO 급 삭감(-35% 내외) 제안.
- 라인 수 정합 검증: 소계 합이 실제 파일 구간 줄 수와 정확히 일치(Ch1 2203, Ch2 693) — 절 경계 겹침/누락 0.
- 측정 스크립트는 raw grep 대조로 자체 버그 2건(중첩 중괄호 제목→label 유실, `\\[Npt]` 오탐)을 발견·수정 후 재검증 완료.
- 파일 수정 없음 — 본 라운드는 순수 실측(S3), 실제 압축 편집은 후속 라운드(S4+) 대상.
