# R4 검토 결과 — 인용·빌드·텔레그래프 문체·orphan·그림 (9종 전수)

> 검토자: R4 검수 sub (4-세션 분업, 검토 의견만, 파일 수정 없음)  
> Ground truth: `REVIEW_RISK_PATTERNS.md` 인용 마스터 14건·위험6 문체  
> 검토일: 2026-06-30

---

## (a) 9종 인용·빌드·문체 비교표

| 초안 | fabrication | dangling \cite | undefined bibitem | jpcc2021 "Calculations" | standardised2024 전셀라벨 | 마스터 미등재 bibitem | 문체 위반(전보체) | PDF | TikZ 한글 |
|---|---|---|---|---|---|---|---|---|---|
| v4-01 | 없음 | 없음 | chemmater2015, jpcc2021(본문미인용) | **누락** | **누락** | chemmater2015, numericalverif2026 | **있음** (맺음절 "확정된항목/다음단계" 8건) | O | **있음** (fig2 노드 "탈리튬화", "희박", "만충") |
| v4-02 | 없음 | 없음 | reynolds_huggins, bazant_lattice, chemmater2015 | **누락** | **누락** | chemmater2015, verif42 | **있음** (§10 "한계와공백" 5건) | O | 없음 |
| v4-03 | chemmater2015 (마스터外, DOI 10.1021/acs.chemmater.5b00235) | 없음 | chemmater2015, allart2018 | **누락** | **누락** | chemmater2015 | **있음** (§한계·갭 4건) | O | 없음 |
| v4-04 | 없음 | 없음 | 없음 | **누락** | **누락** | 없음 | **있음** (한계·갭(정직) 830~834행 5건) | O | **있음** (fig:sconfig "중심", fig:overlap "겹침/연속블렌드", fig:weff "상분리") |
| v4-05 | 없음 | 없음 | 없음 | **누락** | **누락** | chemmater2015, numverif2026 | **없음** | O | **있음** (fig:occ_config "점유분포/configurational엔트로피", fig:blend "탈리튬화진행/겹침영역연속블렌드/계단틀림", fig:weff "균질고용체/상분리") |
| v4-06 | 없음 | 없음 | 없음 | **누락** | **누락** | chemmater2015, hill | **있음** (한계·갭 774~779행 6건) | O | 없음 |
| v4-07 | huggins1941 (마스터 huggins2009와 다른 인물·연도·DOI) | 없음 | occupation2019, chemmater2015, standardised2024, hysteresis2018 | **누락** | **누락** (bibitem 있으나 본문 미인용) | chemmater2015, huggins1941 | **없음** | O | 없음 |
| v4-08 | huggins1942 (마스터 huggins2009와 다른 인물·연도·DOI) | 없음 | standardised2024, hysteresis2018, chemmater2015 | **누락** | **누락** (bibitem 있으나 본문 미인용) | chemmater2015, huggins1942 | **없음** | O | 없음 |
| v4-09 | huggins1942, cogswell2012, chemmater2015 (3건 마스터外) | 없음 | occupation2019 | **누락** | **누락** | huggins1942, cogswell2012, chemmater2015 | **없음** | O | 없음 |

---

## (b) fabrication·dangling 결함 상세

### fabrication (마스터 외 저자/연도/DOI 항목) — 엄격 기준

| 초안 | key | 저자·연도 | DOI | 판정 |
|---|---|---|---|---|
| v4-07 | huggins1941 | M. L. Huggins, 1941 | 10.1063/1.1750930 (J. Chem. Phys.) | 마스터가 요구한 huggins2009(Springer 교과서, R. A. Huggins)와 인물·연도·출판물 전부 상이. 정교한 대체 사용. |
| v4-08 | huggins1942 | M. L. Huggins, 1942 | 10.1021/j150415a018 (J. Am. Chem. Soc.) | 동일 문제. 마스터 huggins2009와 인물·연도·출판물 전부 상이. |
| v4-09 | huggins1942 | M. L. Huggins, 1942 | 10.1021/ja01260a068 | 동일 패턴. |
| v4-09 | cogswell2012 | Cogswell & Bazant, 2012 | 10.1021/nn204177u (ACS Nano) | 마스터 14건에 없는 논문. |
| v4-03 | chemmater2015 | 저자명 없음, 2015 | 10.1021/acs.chemmater.5b00235 | 마스터 14건에 없음. 본문 미인용 상태(orphan bibitem). |

> **주의**: "huggins" 계열(v4-07/08/09)은 동명이인(M. L. Huggins ≠ R. A. Huggins) 혼동. 정규용액 이론 원전은 M. L. Huggins가 맞을 수 있으나, 마스터 지정 키(huggins2009 = R. A. Huggins 교과서)와 명시적으로 불일치. 의도적 교체인지 오류인지 작업자 확인 필요.

### 공통 dangling \cite: **9종 전원 없음** (모든 본문 \cite 키에 bibitem 존재)

### 공통 발견 — chemmater2015
- v4-01, v4-02, v4-03, v4-05, v4-06, v4-07, v4-08, v4-09 에 bibitem으로 등재
- 마스터 14건에 없는 항목 (DOI: 10.1021/acs.chemmater.5b00235, Chem. Mater. 2015)
- v4-07 이외 대부분이 본문에서 미인용(orphan bibitem) 상태
- **9종 중 8종이 이 항목을 가짐 — 작업 템플릿에서 유래한 것으로 추정**

### jpcc2021 "Calculations" 누락 — **9종 전원**
- 실제 title: "Thermodynamic Analysis of Li-Intercalated Graphite by First-Principles with Vibrational and Configurational Contributions"
- "Calculations" 단어 없음. 마스터 ★ 요건 미충족 전원.
- 마스터 지정과 실제 DOI(10.1021/acs.jpcc.1c08992) 논문 제목이 달라 title 자체가 다른 논문인지 원문 대조 필요.

### standardised2024 "전셀 값" 라벨 — **9종 전원 누락**
- bibitem에 "(전셀 값, 하프셀 아님)" 또는 동등 라벨 명시 없음
- v4-07, v4-08은 bibitem은 있으나 본문 \cite도 없음 (이중 결함)

---

## (c) 텔레그래프 문체 위반 초안 vs 클린 초안

### 위반 초안 (한계/갭/맺음 절 전보체 확인)

| 초안 | 위반 절 | 위반 건수 | 대표 위반 예 |
|---|---|---|---|
| **v4-01** | `\section*{맺음}` "확정된항목/다음단계" | 8건 | "분배함수→logistic기원(§2.2)" — 동사 없는 명사구 |
| **v4-02** | §10 "한계와공백" | 5건 | "실데이터 round-trip 으로만 확정(후속).", "정량 미확보." |
| **v4-03** | §한계·갭 (714~724행) | 4건 | "실데이터 round-trip 후속", "정량 미확보", "방법 수준만 인용", "interlayer 기술 난점, 실험 우선" |
| **v4-04** | 한계·갭(정직) (830~834행) | 5건 | "히스 하 경로의존 ∂U/∂T 불확실도의 정량 미확보(...만 제시).", "electronic 항은 흑연서 ≈0 가정(준금속);" |
| **v4-06** | 한계·갭(정직) (774~779행) | 6건 | "dQ/dV(T) 직접 추정의 정확도는 실데이터 round-trip 으로만 확정(후속).", "범위 밖" |

### 문체 클린 초안

| 초안 | 판정 | 근거 |
|---|---|---|
| **v4-05** | 클린 | 한계·갭 단락 포함 전 절이 finite verb 완결 문장 |
| **v4-07** | 클린 | 맺음/범위 절 완결 문장. 극한 longtable 셀 명사구는 표 형식으로 허용 |
| **v4-08** | 클린 | 맺음 절 완결 문장 |
| **v4-09** | 클린 | 한글 "한계/갭" 절 없음. Corner limits는 longtable 형식(허용) |

---

## 추가 발견 — 수식 `+` 연산자 누락 (v4-08, v4-09)

- **v4-08** 식 eq:decomp (197~205행): ΔS = ΔS⁰ + R ln[ξ/(1-ξ)] + ΔS_vib + ΔS_el 에서 `+` 기호 전부 누락. PDF에 항들이 연속 나열 또는 컴파일 오류 위험.
- **v4-09** 식 eq:decomp (316~318행) 및 eq:overlap_full (375행): 동일 패턴 `+` 누락.

---

## 인용·문체 종합 판정 — Best 초안

### 인용 기준 best
- **v4-04**: fabrication 0건, dangling 0건, undefined bibitem 0건, DOI 전부 일치, pathria/ashcroft/newman ISBN 명시, chemmater2015 없음. 마스터 14건 완전 등재.
- **v4-05**: fabrication 0건. chemmater2015/numverif2026 추가는 있으나 본문 인용됨(orphan 아님). 마스터 외 2건만 추가.

### 문체 기준 best
- **v4-05**: "한계·갭" 절 포함 전 절이 완결 문장. 9종 중 유일하게 문체·인용 양쪽 모두 결함 수 최소.
- **v4-07, v4-08**: 문체 클린이나 huggins1941/1942 key 오불일치 결함.

### 종합 best 후보
- **v4-05** — 문체 클린 + fabrication 0 + dangling 0. 마스터 외 추가 2건(chemmater2015·numverif2026)은 본문 인용됨. TikZ 한글은 있으나 kotex 로드 시 컴파일 가능. jpcc2021·standardised2024 공통 미충족은 9종 전원 해당이므로 차별 요인 아님.
- **v4-04** — 인용 마스터 14건 완전 등재 + fabrication 0 + dangling 0. 문체 5건 위반이 단점.

---

## 빌드 요약

| 항목 | 결과 |
|---|---|
| PDF 존재 | **9종 전원** |
| LaTeX Error | **9종 전원 없음** |
| Overfull >20pt | v4-01/02/03/04 에서 헤더 영역 ~6pt 수준 (차단 안 됨) |
| undefined \ref/\cite | **9종 전원 없음** |
| 수식 `+` 누락 | v4-08, v4-09 (eq:decomp) |
| 폰트 Warning | 전원 UnBatang italic 미정의 (출력 영향 없음) |

---

## orphan 라벨 공통 패턴

- **그림 4종(fig:*)이 본문 `\ref` 없이 caption만 있는 패턴**이 9종 전원에 공통. fig:weff, fig:sconfig, fig:overlap 계열이 반복.
- **수식 orphan**: 각 초안마다 10~26개 수식이 `\eqref` 미참조. 유도 흐름은 본문 prose에서 서술하나 `\eqref{}` 호출 없음. 의도적 서술 방식인지 본문 누락인지 작업자 확인 필요.
- v4-02에서 `\ref{sec:limit}` (s없음) vs `\label{sec:limits}` (s있음) key 불일치 1건 — PDF에서 `??` 출력 위험.

---

*R4 검수 sub 완료. 파일 수정 없음.*
