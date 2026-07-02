# V1013 S1 — 구조 맵 (master 직접, 이동·참조 영향 전수)

> 기준 = `docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex`(v1.0.12 최종 사본, 절 위치 실측 2026-07-02). 원칙: **라벨 이름 불변**(이동해도 `\label` 보존 — 참조 자동 재해소), 이동 경계의 다리 문장은 재봉합(잔재 금지).

## 1. 신규 문서 골격 (Ch1)

| 순서 | 구성 | 원천 | 비고 |
|---|---|---|---|
| 서론 | 기존 유지 | 현행 | roadmap 문단만 Part 구조로 갱신(P2.2) |
| **N0 기호·규약** | `sec:notation`(L197–355) 중 **L197–300** | 현행 | **sec:lco-map(L301–355)은 Part II 로 적출** |
| **★Part 0 — 통계역학 기초** | 신설(P2.1 체리픽) | 신규 + 흡수 | 배치 = N0 직후·N1(sec:pol) 앞. 라벨 eq:sm-* |
| Part I — 흑연(N1–N9) | `sec:pol`(L357)~`sec:sum`(L1927–2187) | 현행 | LCO subsection 전부 적출, Part 0 재접속 |
| **Part II — LCO 양극** | 도입(신설) + 적출 절 6+1 | 이동 | 아래 §2 순서 |
| 전체 입력 인자·facade | L2188–2278 | 이동 | 문서 말미(두 전극 종합이므로 Part II 뒤) |
| 부호 사슬 전수 검산 | `sec:signcheck`(L2279–) | 유지 | 문서 최말미 |

## 2. Part II 내부 순서 (이동 원천 실측)

| # | 절 | 현행 위치(실측) | 이동 시 다리 재봉합 지점 |
|---|---|---|---|
| II-0 | **도입(신설)** — 전극-중립+방향 규약+MSMR 예고 | (신규, lco-map L301–355 흡수) | N0 말미에 "양극 일반화는 Part II" 1문장 포인터 |
| II-1 | `sec:lco-center` | L476–519 (verifybox L496–516·다리 L518–519 포함) | L518–519 다리("다음은…히스 분기")는 흑연 N2→N3 연결로 원래 흑연 다리가 아님 — 적출 후 N2 말미 신규 1문장 |
| II-2 | `sec:lco-hys` | L752–776+ (실측 L752–916, ★분기 부호 문단 포함 — 문단은 II-0 로 흡수) | N3 말미 재봉합 |
| II-3 | `sec:lco-electronic`(3 subsection: lco-why·lco-Se·lco-gate) | L1141–1379 | N5 뒤 흑연 흐름 재봉합 — 독립 section 이라 잔재 적음 |
| II-4 | `sec:lco-peak` | L1416–1488 (★방향 부호 문단은 II-0 로 흡수·각주 처리 재설계) | N6 말미 재봉합 |
| II-5 | `sec:lco-decomp` | L1970–2063 | N9 내부 — 적출 후 N9 흐름 재봉합 |
| II-6 | `sec:lco-code` | L2064–2187 | 〃 |

## 3. Part 0 재접속 (흡수·참조 설계 — 체리픽 재접속 표와 대조 확정)

| 현행 | 처분 |
|---|---|
| `sec:width` L924–952 (w 이중지위) | Part I 잔류, 유도부는 Part 0 참조로 압축 |
| ξ_eq logistic 유도 L953–1065 | **Part 0 로 흡수**(라벨 eq:xieq 등 보존 — 정의 위치만 이동), N4/N5 에는 결과 참조 |
| `sec:dist` L1066–1139 (분포 관점) | **Part 0 로 흡수**(sec:dist 라벨 보존) |
| `sec:hys` L586–646 (μ(θ)·regular solution) | 유도 골격은 Part 0 §3, N3 는 spinodal·gap 적용부터(eq:mu·eq:gxi 라벨은 Part 0 정의로 이동) |
| Ch2 `eq:Z1` 절 L110–180 | Ch2 잔류 + Part 0 참조로 중복 서술 압축(P6.1) |

## 4. 참조 영향 (전수는 S17 gate 에서 grep 재실측)

- lco 절 내부 상호 참조: 이동 후에도 라벨 보존이라 자동 해소. 순서 역전(전방 참조) 발생 여부만 점검 — Part II 내부 순서가 현행 문서 순서와 동일하므로 위험 낮음.
- 흑연부→lco 참조 의심 지점: 서론 roadmap·tab:inputs(LCO 행)·facade·signcheck — 전부 "문서 말미 종합부"로 이동하므로 Part II 뒤 = 후방 참조 유지.
- Part 0 이동 라벨(eq:mu·eq:gxi·eq:xieq·eq:belliden·sec:dist)의 **기존 참조는 전부 후방**(N3 이후에서 참조) → Part 0 이 앞에 오면 전방 참조 0 유지.
- fig:staging(L276 부근 tikz)·fig:hysloop·fig:reversal·fig:blend = 흑연 잔류. lco figure 없음(현행) — P2.1 figure 경쟁이 신설.

## 5. 리스크·중단 조건

- lco-center 적출 시 verifybox(+80/−46 공존 박스)가 Part II 로 감 — N2 쪽에서 이를 참조하는 문장 잔재 스캔 필수.
- `eq:lco-dUdT` 참조 5곳 중 흑연부 잔존이 있으면(실측: L498=verifybox 내부·L1229 상당=lco 내부·나머지 lco 내부) — 전부 lco 내부로 확인됨, 단 S17 gate 재실측.
- Ch2 가 Ch1 lco 절을 참조하는 문자열("Chapter 1 의 LCO" 류) — P6.1 에서 문안 정합.
