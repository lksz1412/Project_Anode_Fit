# ROUND_visual — v8-11 시각·그림·형식·완결성 검수 (검수 sub, 리뷰 전용)

대상: `v8-11.tex` (1210행, 전문 정독) + `v8-11.pdf` (21p, A4, MiKTeX-dvipdfmx).
기준: `v8-00_spine/AUTHOR_BRIEF_v8.md`.
도구: pdfinfo(21p 확인)·pdftoppm 110/150 dpi 전 페이지 렌더 판독·log 스캔·label/ref 교차·TikZ node Hangul 스캔(스크립트).
검수 자세: refute mandate — 빈 통과 금지, 각 그림에 "혼란 유발" 적대 렌즈 적용.

---

## 1. 빌드 위생 (log 스캔)

| 항목 | 결과 |
|---|---|
| Overfull \hbox | **0** |
| Underfull \hbox | **0** |
| Overfull \vbox | **0** |
| Undefined/multiply-defined reference | **0** |
| LaTeX Font Warning | 3건 (TU/UnBatang it·bx-it, TU/D2Coding it) — **무해** |

폰트 경고 3건은 한글 본문 italic/bold-italic emphasis 와 monospace italic 의 shape 폴백(대체 shape 자동 치환).
그림/ASCII/수식 렌더에는 영향 없음(렌더 판독에서 깨짐·누락 0 확인). 심각도 LOW-, 정정 불요(작가 메모/배포물 품질 무관).

헤더 페이지번호: 전 페이지 `X/21` 형식 수렴 — 3-pass 후 LastPage 정상(p.1~21 일관, undefined ref 0 으로 확인).

---

## 2. 그림 9개 — 그림별 판정 (혼란 유무)

전 9개 신규/유래 TikZ. 렌더 텍스트 영어 ASCII 전용(스크립트: tikz 9블록 中 rendered-node Hangul **0**).
orphan: 9개 label 전부 본문 \ref 보유(아래 §5). 식 정합·곡선 형상 적대 검산 결과:

| # | label | 유래 | 페이지 | 혼란? | 판정 근거 |
|---|---|---|---|---|---|
| 1 | fig:spine | v7-11 그대로 | p.2 | **무** | N0→N9 척추·전이 루프 점선 상자·입출력 라벨 명료, 본문 절 순서와 1:1 |
| 2 | fig:staging | v7-11 그대로 | p.5 | **무** | stage 4→1 갤러리 채움 도식, lithiation/delithiation 화살표 방향 정합, 2L 옅은 음영 |
| 3 | fig:doublewell | 신규 | p.9 | **무** | g(ξ)/RT 대칭 이중웰, g''<0 음영 띠와 ξ_s± 변곡점 위치 식~(spinodal)과 정합 |
| 4 | fig:hysloop | v7-11 유래 | p.10 | **무** | 비단조 V_eq(ξ), 방전 좌상·충전 우하 과주행 경로, ΔU_hys 양방향 화살표 식~(Veq/dUhys) 정합 |
| 5 | fig:barrier | 신규 | p.11 | **무** | (a) 평형 A=0 대칭 / (b) 구동 A>0 χ=1/2, ΔG_a−χA·peak down by χA 식~(bv) 정합 |
| 6 | fig:flux | 신규 | p.12 | **무** | r+(1-ξ) 감소직선 × r-ξ 증가직선 교점=ξ_eq, A>0(검정)→2/3·A=0(회색)→1/2 식~(logisticsolve) 정합 |
| 7 | fig:logistic | v7-11 유래 | p.13 | **무** | ξ_eq S-곡선 + 규격화 종 w|dξ/dV|=ξ(1-ξ), 중심 max 1/4 식~(belliden) 정합 |
| 8 | fig:relaxode | 신규 | p.16 | **무** | 목표 ξ_eq(파선)·뒤처진 ξ_lag(실선)·차 r 화살표, peak=(ξ_eq−ξ_lag)/L_V 라벨 식~(peakshape) 정합 |
| 9 | fig:reversal | v7-11 유래 | p.17/18 | **무** | (a)방전 꼬리→높은 V / (b)충전 꼬리→낮은 V(grid reversed), 거울 대칭·양수 식~(reversal) 정합 |

신규 4(doublewell·barrier·flux·relaxode) 모두 신규 TikZ 확인 — 유도 단계(spinodal·Eyring 비대칭·정지점·완화)를 직접 *돕는다*.
**★fig:relaxode 캡션**: 작가 메모 잔존 **0**. 캡션(소스 925–931행)은 완결 prose — 파선/실선/차/peak 정의 + L_V≫Δgrid(ρ→1) vs 작은 L_V 분기 스위치(식~branch)로의 환원 구분을 정확히 서술. 도식(target 파선·lagged 실선·gap 화살표)과 캡션이 정합. v8-11 보강 목적 달성.

혼란 유발 그림: **0 / 9**.

---

## 3. 표 4종 — 가독 (오버플로·잘림·정렬·페이지 분리)

| 표 | 페이지 | 형식 | 판정 |
|---|---|---|---|
| notation (longtable, 3열) | p.4~5 | 섹션 소제목 multicolumn 행으로 구획 | **가독** — p.4→5 자연 분리, head 반복 정상, 오버플로 0 |
| tab:staging (8열) | p.18 | 2행 헤더(기호/단위), booktabs | **가독** — 4 전이 × 8열 전부 수용, 잘림 0, 정렬 정상 |
| tab:inputs (4열, footnotesize) | p.19 | dict키/생성자/호출 3구획 multicolumn | **가독** — 긴 코드 식별자·식 참조 수용, 오버플로 0 |
| tab:nodemap (4열) | p.20 | N0~N9 노드↔식↔코드 | **가독** — 코드 식별자 열 잘림 0 |

표 가독 결함: **0**. (Overfull hbox 0 이 표 셀 넘침 부재를 정량 뒷받침.)

---

## 4. 형식·완결성 (수식 주도·괄호 전보체·절 다리·앞 동기/뒤 사용)

- **수식 주도**: 각 결과 박스 위 (a)출발→(b)연산→(c)중간식→(d)박스 4-스텝 라벨 가시. 9 박스+보조식 일관. PASS.
- **절 다리**: 절 도입·마무리 다리 존재 — 예 \S(pol) 끝 "다음 절은 …U_j(T)로 들어간다", \S(center) 끝 "히스테리시스 분기다", \S(eqpeak) 끝 "다음 절이 그 지연 길이 L_V 를 세우고". 끊김 0. PASS.
- **추가식/표/그림 앞 동기·뒤 사용**: 모든 그림 본문 선동기(\ref 앞 식)·후사용 확인(§5). 표 4종 모두 도입 문장에서 호출. orphan 0.
- **괄호 전보체**: 본문은 완결 문장 주체. 보충 괄호는 정의/단위 보강 수준으로 과다 전보체 아님(브리프 문체 규범 부합). 결함 없음.
- **재현 가능성(G-usable)**: keybox "이 문건만으로 한 곡선 재현(6단계)"(p.18)가 식 참조 사슬로 닫힘 — tab:staging→N0/N1→…→N9. 실행 가능.

형식 결함 (심각도·행):
| 심각도 | 위치(행) | 내용 |
|---|---|---|
| LOW- | 빌드 log 1077/1159/1204 | 한글 it/bx-it·mono-it font shape 폴백 경고 3건(렌더 무해, 정정 불요) |

**형식 결함 수: 1종(LOW-, 무해 폰트 폴백)** — CRIT/HIGH/MEDIUM **0**.

---

## 5. orphan(앞 동기·본문 \ref) 교차검증

9 label 각각 본문 \ref ≥1 (label 자기행 제외). spine(L107 intro)·staging(L229)·doublewell(L432)·hysloop(L469)·barrier(L590)·flux(L606)·logistic(L700)·relaxode(L906)·reversal(L980). 식 label↔eqref 도 undefined ref 0(log). **orphan 0**.

---

## 가장 약한 1곳 (refute — 빈 통과 금지)

가장 약한 곳 = **한글 italic/mono-italic font-shape 폴백 경고 3건(log 1077/1159/1204)**. 이는 D2Coding/UnBatang 에 italic shape 가 없어 LaTeX 가 upright 로 자동 치환한 것 — 본문 한글 \emph{} 강조가 시각적으로 살지 않을 수 있는 유일한 시각 흠. 단 (1) 렌더 전수 판독에서 깨짐/누락/오정렬 0, (2) 영어 ASCII 그림·수식 무관, (3) 배포물 정합성·완결성 무영향이라 심각도 LOW-(미관 한정). 정정은 선택(예: 한글 emphasis 를 bold 로) — 본 라운드 권고는 정정 불요. 그 외 9 그림·4 표·수식 주도·절 다리·orphan 전부 청정.
