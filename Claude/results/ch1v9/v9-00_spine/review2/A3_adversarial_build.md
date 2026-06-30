# A3 Adversarial Review — v9-10 인용·빌드·완결성
> 검수 sub A3 (adversarial, 반증 시도)  
> 대상: `Claude/results/ch1v9/v9-10/v9-10.tex` (1609줄)  
> Ground truth: `V2_citations_master.md` · `research/CH1v9_LCO/20_extraction/` 카드  
> 작성: 2026-06-30

---

## 1. ★ 인용 8건 정확성 표

Ground truth = V2 citations master (v9-05 기준 확정 마스터 8건).  
범례: ✅ 정확 | ⚠️ 오류/경미 | ❌ fabrication | — 없음

| # | bibkey | 저자 | 권·페이지 | DOI | v9-10 판정 | 비고 |
|---|--------|------|----------|-----|-----------|------|
| 1 | reimers1992 | J. N. Reimers, J. R. Dahn | JES **139**, 2091--2097 (1992) | 10.1149/1.2221184 | ✅ | 마스터와 1:1 일치 |
| 2 | menetrier1999 | M. Ménétrier, I. Saadoune, S. Levasseur, C. Delmas | J. Mater. Chem. **9**, 1135--1140 (1999) | 10.1039/a900016j | ✅ | 저자 완전·DOI 일치 |
| 3 | motohashi2009 | T. Motohashi … H. Yamauchi (8인) | PRB **80**, 165114 (2009) | 10.1103/PhysRevB.80.165114 + arXiv:0909.3556 | ✅ | 저자 완전·DOI·arXiv 모두 일치 |
| 4 | xia2007 | H. Xia, L. Lu, Y. S. Meng, G. Ceder | JES **154**(4), A337--A342 (2007) | 10.1149/1.2509021 | ✅ | 페이지 범위·DOI 일치 |
| 5 | reynier2004 | Y. Reynier … B. Fultz (6인) | PRB **70**, 174304 (2004) | 10.1103/PhysRevB.70.174304 | ✅ | PRB primary·동 그룹 JES 병기(마스터 동일) |
| 6 | swiderska2019 | A. Świderska-Mocek, E. Rudnicka, A. Lewandowski | PCCP **21**, 2115 (2019) | 10.1039/c8cp06638h | ✅ | +0.83 mV/K 정확 귀속·DOI 완전 |
| 7 | msmr2024 | A. Paul, K. Wolfe, M. W. Verbrugge … T. R. Garrick (8인) | ECS Advances **3**, 042501 (2024) | 10.1149/2754-2734/ad7d1c | ✅ | Part II JES DOI 병기 일치 |
| 8 | ml2024 | G. H. Teichert, S. Das … K. Garikipati (8인) | JMPS **190**, 105727 (2024) | 10.1016/j.jmps.2024.105727; arXiv:2302.08991 | ✅ | 저자 완전·fabrication 없음 |

**결론: 8건 모두 V2 마스터와 정확 일치. "R. Aronson" fabrication(v9-03), wang2009 오귀인(v9-01/06), 구버전 MSMR(v9-01~03) 등 과거 결함은 v9-10에 없음.**

### 핵심 확인 항목
- **+0.83 mV/K**: `\cite{swiderska2019}` 정확 귀속(line 458). Reynier/wang 오귀인 없음. ✅
- **MSMR = ECS Adv 3, 042501**: `\cite{msmr2024}` + DOI 10.1149/2754-2734/ad7d1c 정확 (line 1425, bibitem line 1604). ✅
- **Teichert 저자 완전**: ml2024에 8인 저자 명기(line 1605), 익명 없음. ✅

---

## 2. 빌드 결과

**빌드 명령**: `xelatex -interaction=nonstopmode v9-10.tex` (2-pass)

| 항목 | 결과 |
|------|------|
| LaTeX 오류(! Error) | **0** |
| Undefined citation | **0** |
| Undefined reference | **0** |
| Multiply-defined | **0** |
| Dangling `\cite` (bibitem 없음) | **0** |
| 미인용 bibitem | **0** |
| Overfull hbox > 20pt | **1건** — line 1485–1488, 22.6pt |
| Overfull hbox ≤ 20pt | 4건 (4.6 / 17.3 / 2.2 / 8.1 pt) |
| 출력 | v9-10.pdf, 29 pages |

**빌드 클린. 0-error, 0-undefined. Overfull 22.6pt (line 1485) 만 기준치(20pt) 초과 — LOW 심각도.**

---

## 3. 완결성·orphan 분석

### 3-1. \label / \ref 완결성 (92 labels, 79 refs used)

| 항목 | 수 | 판정 |
|------|---|------|
| Undefined ref (`\ref` without `\label`) | 0 | ✅ |
| Unreferenced label (eq:*) — 중간 유도식 | 8건 | LOW — 설명 아래 |
| Unreferenced label (sec:*) — 미인용 절 | 5건 | LOW — 설명 아래 |

**중간 유도식 미인용 (8건):** `eq:gibbsdef`, `eq:eqbalance`, `eq:Ujmid`, `eq:hysdiff`, `eq:hyssym`, `eq:intfactor`, `eq:Lqmid`, `eq:Lqmid2`  
→ 이들은 모두 (a)→(b)→(c)→(d) 유도 전개의 중간식이다. 박스 결과식(`eq:Uj`, `eq:dUhys` 등)은 인용되나 중간 단계식은 순서 서술용이라 `\eqref` 없어도 orphan이 아님. **구조적으로 정상.**

**미인용 절 레이블 (5건):** `sec:eqpeak`, `sec:lco-gate`, `sec:lco-map`, `sec:lco-peak`, `sec:lco-why`  
→ 이 5개는 subsection/section 레이블이지만 다른 절에서 `\ref{sec:...}`로 링크되지 않은 자립형 절이다. 본문 흐름은 순서 서술로 이어지며 절 번호로만 참조한다. `sec:lco-decomp`, `sec:dist`, `sec:lag`, `sec:center` 등 핵심 절은 모두 인용되고 있어 **중요 orphan 없음.** LOW.

### 3-2. 그림 영어 ASCII 검증

모든 TikZ 그림 캡션 내부 텍스트:

| 그림 | 캡션 영어 label | 한글 포함 여부 |
|------|----------------|--------------|
| fig:spine | "N0 map inputs", "N1 polarization", "input:", "output:", "per-transition loop" 등 | 캡션 본문은 한글, 내부 ASCII 영어 ✅ |
| fig:staging | "lithiation (charge)", "delithiation (discharge)" | ✅ |
| fig:doublewell | "$g''<0$ (unstable)", "two wells" | ✅ |
| fig:hysloop | "discharge overshoot", "charge overshoot" | ✅ |
| fig:barrier | "reaction coordinate", "free energy", "filled site", "transition state", "peak down by χA", "driven A>0" | ✅ |
| fig:flux | "flux [arb.]", "forward r+(1-ξ)", "reverse r-ξ", "gray: A=0" | ✅ |
| fig:logistic | "logistic", "center" | ✅ |
| fig:lco-electronic | "Li content x", "MIT-logistic gate", "insulator", "metal", "ΔSe(x) bump" | ✅ |
| fig:relaxode | "q (capacity coord)", "target ξ_eq", "lagged ξ_lag", "peak shape" | ✅ |
| fig:reversal | "discharge σd=+1: progress V↑", "charge σd=-1: progress V↓ (grid reversed)", "tail → higher/lower V" | ✅ |

**한글 0 in TikZ node/label text. 전량 영어 ASCII.** ✅

### 3-3. 흐름 연결성 — 일반→흑연→LCO

| 다리 | 위치 | 판정 |
|------|------|------|
| 서론 → N0 도입 | 서론 마지막 문단 "아홉 단계 N0→N9" | ✅ |
| N0 → N1 | sec:notation 말미 "방향 부호의 작용처는 셋 — 분극 부호(N1)…" | ✅ |
| N1 → N2 | "다음 절은 전이 루프의 첫 식 — 평형 중심 U_j(T) — 으로 들어간다" | ✅ |
| N2 → N3 | "다음은 같은 루프 안에서 이 중심을 충·방전으로 갈라놓는 히스테리시스 분기다" | ✅ |
| N3 → N4 | "이 center가 다음 절 평형 점유 ξ_eq의 중심으로 들어간다" | ✅ |
| N4 → LCO electronic | "분포 다리" keybox로 ξ_eq–Fermi–Dirac 연결 → sec:lco-electronic | ✅ |
| N5+ → N6 | "그림 fig:logistic가 ξ_eq와 그 미분을 보인다. 다음 절은 이 종이 평형 peak임을 닫는다" | ✅ |
| N6 → N7 | "다음 절이 그 지연 길이 L_V를 세우고" | ✅ |
| N7 → N8 | 자연 연속(지연 길이 확보 후 꼬리 합성곱) | ✅ |
| N8 → N9 | "전이 루프가 각 전이의 peak_shape를 만들면, 코드는… 합산" | ✅ |

**흐름 끊김 없음.** ✅

---

## 4. tier 정직·허위 정밀 검증

| 항목 | 본문 표기 | 판정 |
|------|---------|------|
| +0.83 mV/K | "tier B — LCO 단일전극 potentiometric, 크기·부호 스케일 검증용 초기값" | ✅ |
| g(E_F) 연속 곡선 없음 | "1차 문헌엔 그것이 없다 — Motohashi 등은 anchor 단일점과 정성 추세만" (갭 G2 명시) | ✅ |
| g_max = 13 e/eV | "tier A 단일점, 초기값으로 고정" | ✅ |
| 도핑 보정(g(E_F,x), Ω_j 변화) | "초기값이고 … 데이터로 피팅한다 — 흑연 철학 그대로이며, 허위 정밀을 피해 tier 병기" | ✅ |
| ΔS_e ∝ T 온도 의존 (전자항만 T-선형) | "다른 항과 결정적으로 다르다 … U_1 이동은 ∝T²" (T-선형 ≠ 이동률) | ✅ |
| Motohashi Δ^config 값 "tier A" | "Motohashi [cite] … tier A" | ✅ |
| 전체 초기값 = 피팅 대상 | "신뢰값 아닌 초기값 — 사용자 피팅이 override 전제" 반복 명시 | ✅ |

**허위 정밀 없음. 갭(g(E_F,x), 도핑) "초기값·피팅 위임" 정직 표기.** ✅

---

## 5. 결함 표

| ID | 유형 | 심각도 | 위치 | 내용 | 정정 |
|----|------|--------|------|------|------|
| D1 | Overfull hbox | LOW | line 1485–1488 | 22.6pt 초과 (피팅 스코프 설명 문단) | `\linebreak` 또는 어절 조정 |
| D2 | Overfull hbox | LOW | line 211 | 17.3pt (longtable 헤더 행) | 컬럼 폭 미세 조정 |
| D3 | Unreferenced sec label | INFO | line 1048, 957, 267, 1084, 887 | sec:eqpeak 등 5건 — 자립형 절, 흐름 문제 없음 | 선택적 cross-ref 추가 또는 무시 |
| D4 | Unreferenced eq label | INFO | line 382, 395, 416, 569, 589, 1110, 1171, 1221 | 중간 유도식 8건 — 구조적으로 정상 | 무시 |

**CRITICAL·HIGH 결함 없음.**

---

## 6. 가장 약한 1곳

**D1 — line 1485–1488, Overfull 22.6pt.**  
`\Delta H_\rxn, \Delta S_\rxn, Q, w` 를 나열한 문장이 마진을 22.6pt 침범한다. 출판 품질 기준에서 유일하게 20pt를 초과하는 조판 결함이다. 내용·인용·수식은 무결하나 이 한 줄이 가장 취약한 물리-무관 결함.

---

## 요약 (10줄 이내)

1. **인용 fabrication 없음** — 8 LCO bibitem 전건 V2 마스터와 정확 일치. "R.Aronson" 없음, wang2009 오귀인 없음, 구버전 MSMR 없음.
2. **+0.83 mV/K = Świderska-Mocek 2019 정확 귀속** (tier B 명시).
3. **MSMR = ECS Adv 3, 042501 정확**, Teichert 저자 완전.
4. **dangling \cite 0건, undefined \ref 0건, multiply-defined 0건.**
5. **빌드 0-error, 29p 출력.** Overfull 22.6pt 1건만 LOW.
6. **TikZ 내부 영어 ASCII 전량 확인, 한글 0.**
7. **흐름 N0→N9·흑연→LCO 전 다리 정상.**
8. **tier 정직 전건 통과**, 허위 정밀 없음.
9. CRITICAL·HIGH 결함 없음.
10. **가장 약한 곳**: line 1485–1488 Overfull 22.6pt (LOW, 조판 한 곳).
