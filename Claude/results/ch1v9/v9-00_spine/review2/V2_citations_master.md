# V2 인용 마스터 검증 보고서
> 검토2 V2 — LCO 인용 fabrication 스캔 + 정확성 검증 + 마스터 bibitem 리스트
> Ground truth: CHERRYPICK_PLAN.md (인용 정정 §)
> 작성: 검수 sub (검토2 V2), 2026-06-30

---

## (a) 9종 인용 정확성 표

범례: ✅ 정확 | ⚠️ 오류/불완전 | ❌ fabrication | — 해당 bibitem 없음(dangling)

### ref 1: Reimers & Dahn 1992 (JES 139, 2091 | DOI 10.1149/1.2221184)

| 초안 | bibkey | 저자 | 권·페이지 | DOI | 판정 |
|------|--------|------|----------|-----|------|
| v9-01 | reimers1992 | Reimers, Dahn | 139, 2091 | 10.1149/1.2221184 | ✅ |
| v9-02 | reimers1992 | Reimers, Dahn | 139, 2091 | 10.1149/1.2221184 | ✅ |
| v9-03 | — | **미정의(bibitem 없음)** | — | — | ❌ dangling — \cite{reimers1992} 미등재 |
| v9-04 | reimers1992 | Reimers, Dahn | 139, 2091 | 10.1149/1.2221184 | ✅ |
| v9-05 | reimers1992 | Reimers, Dahn | 139, 2091 | 10.1149/1.2221184 | ✅ |
| v9-06 | reimers1992 | Reimers, Dahn | 139, 2091 | 10.1149/1.2221184 | ✅ |
| v9-07 | reimers1992lco | Reimers, Dahn | 139, 2091–2097 | 10.1149/1.2221184 | ✅ (key 이름만 다름) |
| v9-08 | reimers1992 | Reimers, Dahn | 139, 2091–2097 | 10.1149/1.2221184 | ✅ |
| v9-09 | reimers1992 | Reimers, Dahn | 139, 2091–2097 | 10.1149/1.2221184 | ✅ |

**v9-03 결함**: `\cite{reimers1992}` 가 본문(L971)에서 사용되나 bibitem 없음 → **dangling**.

---

### ref 2: Ménétrier et al. 1999 (J. Mater. Chem. 9, 1135 | DOI 10.1039/a900016j)

| 초안 | bibkey | 저자 | 권·페이지 | DOI | 판정 |
|------|--------|------|----------|-----|------|
| v9-01 | menetrier1999 | Ménétrier, Saadoune, Levasseur, Delmas | 9, 1135 | 10.1039/a900016j | ✅ |
| v9-02 | menetrier1999 | Ménétrier, Saadoune, Levasseur, Delmas | 9, 1135 | 10.1039/a900016j | ✅ |
| v9-03 | menetrier1999 | Ménétrier, Saadoune, Levasseur, Delmas | 9, 1135 | 10.1039/a900016j | ✅ |
| v9-04 | menetrier1999 | Ménétrier, Saadoune, Levasseur, Delmas | 9, 1135 | 10.1039/a900016j | ✅ |
| v9-05 | menetrier1999 | Ménétrier, Saadoune, Levasseur, Delmas | 9, 1135 | 10.1039/a900016j | ✅ |
| v9-06 | menetrier1999 | Ménétrier, Saadoune, Levasseur, Delmas | 9, 1135 | 10.1039/a900016j | ✅ |
| v9-07 | menetrier1999lco | Ménétrier et al. | 9, 1135–1140 | 10.1039/a900016j | ✅ |
| v9-08 | menetrier1999 | Ménétrier et al. | 9, 1135–1140 | 10.1039/a900016j | ✅ |
| v9-09 | menetrier1999 | Ménétrier et al. | 9, 1135–1140 | 10.1039/a900016j | ✅ |

**9종 모두 정확.**

---

### ref 3: Motohashi et al. 2009 (PRB 80, 165114 | arXiv:0909.3556)

| 초안 | bibkey | 저자(풀) | 권·페이지 | DOI | arXiv | 판정 |
|------|--------|---------|----------|-----|-------|------|
| v9-01 | motohashi2009 | Motohashi, Ono, Sugimoto, Masubuchi, Kikkawa, Kanno, Karppinen, Yamauchi | 80, 165114 | 10.1103/PhysRevB.80.165114 | 0909.3556 | ✅ |
| v9-02 | motohashi2009 | 위 동일 | 80, 165114 | 10.1103/PhysRevB.80.165114 | — | ✅ (arXiv 누락·무해) |
| v9-03 | motohashi2009 | et al. 축약 | 80, 165114 | 10.1103/PhysRevB.80.165114 | 0909.3556 | ✅ |
| v9-04 | motohashi2009 | 위 동일 | 80, 165114 | 10.1103/PhysRevB.80.165114 | 0909.3556 | ✅ |
| v9-05 | motohashi2009 | 위 동일(풀) | 80, 165114 | 10.1103/PhysRevB.80.165114 | 0909.3556 | ✅ |
| v9-06 | motohashi2009 | et al. 축약 | 80, 165114 | 10.1103/PhysRevB.80.165114 | 0909.3556 | ✅ |
| v9-07 | motohashi2009lco | 풀 저자 | 80, 165114 | 10.1103/PhysRevB.80.165114 | 0909.3556 | ✅ |
| v9-08 | motohashi2009 | et al. 축약 | 80, 165114 | 10.1103/PhysRevB.80.165114 | 0909.3556 | ✅ |
| v9-09 | motohashi2009 | et al. 축약 | 80, 165114 | 10.1103/PhysRevB.80.165114 | 0909.3556 | ✅ |

**9종 모두 정확.**

---

### ref 4: Xia/Lu/Meng/Ceder 2007 (JES 154, A337 | DOI 10.1149/1.2509021)

| 초안 | bibkey | 저자 | 권·페이지 | DOI | 판정 |
|------|--------|------|----------|-----|------|
| v9-01 | xia2007 | Xia, Lu, Meng, Ceder | 154, A337 | 10.1149/1.2509021 | ✅ |
| v9-02 | xia2007 | Xia, Lu, Meng, Ceder | 154(4), A337–A342 | 10.1149/1.2509021 | ✅ |
| v9-03 | xia2007 | Xia, Lu, Meng, Ceder | 154(4), A337–A342 | 10.1149/1.2509021 | ✅ |
| v9-04 | xia2007 | Xia, Lu, Meng, Ceder | 154, A337 | 10.1149/1.2509021 | ✅ |
| v9-05 | xia2007 | Xia, Lu, Meng, Ceder | 154, A337 | 10.1149/1.2509021 | ✅ |
| v9-06 | xia2007 | Xia, Lu, Meng, Ceder | 154, A337 | 10.1149/1.2509021 | ✅ |
| v9-07 | xia2007lco | Xia, Lu, Meng, Ceder | 154(4), A337–A342 | 10.1149/1.2509021 | ✅ |
| v9-08 | xia2007 | Xia, Lu, Meng, Ceder | 154(4), A337–A342 | 10.1149/1.2509021 | ✅ |
| v9-09 | xia2007 | Xia, Lu, Meng, Ceder | 154(4), A337–A342 | 10.1149/1.2509021 | ✅ |

**9종 모두 정확.**

---

### ref 5: Reynier et al. 2004 (PRB 70, 174304 | DOI 10.1103/PhysRevB.70.174304)

CHERRYPICK 확정: PRB 70, 174304 (companion JES 151 A422 동일 그룹).

| 초안 | bibkey | venue | 권·페이지 | DOI | 판정 |
|------|--------|-------|----------|-----|------|
| v9-01 | reynier2004 | **JES 151, A422** | A422 | 10.1149/1.1646139 | ⚠️ companion JES 를 primary로 씀. DOI도 JES용. PRB가 확정 primary이나 동일 그룹·실질 정보 동일 — 심각도 LOW |
| v9-02 | reynier2004 | **JES 151, A422** + PRB 70 174304 병기 | A422 | **10.1149/1.1646152** (오기; 정확: 10.1149/1.1646139) | ⚠️ JES DOI 오기 (LOW) |
| v9-03 | reynier2004 | JES 151 A422 + PRB 70 병기 | A422 | DOI 미기재 | ⚠️ DOI 누락(LOW) |
| v9-04 | reynier2004 | PRB 70, 174304 | 174304 | 10.1103/PhysRevB.70.174304 | ✅ |
| v9-05 | reynier2004 | PRB 70, 174304 | 174304 | 10.1103/PhysRevB.70.174304 | ✅ |
| v9-06 | reynier2004 | PRB 70, 174304 | 174304 | 10.1103/PhysRevB.70.174304 | ✅ |
| v9-07 | reynier2004lco | JES 151 A422 + PRB 70 병기 | A422 + 174304 | 10.1103/PhysRevB.70.174304 | ✅ (PRB DOI 기준) |
| v9-08 | reynier2004entropy | JES 151 A422 + PRB 70 병기 | A422 + 174304 | 10.1103/PhysRevB.70.174304 | ✅ |
| v9-09 | reynier2004 | JES 151 A422 + PRB 70 관련 | A422 | 10.1103/PhysRevB.70.174304 | ✅ |

---

### ref 6: Świderska-Mocek et al. 2019 (PCCP 21, 2115 | DOI 10.1039/c8cp06638h) — +0.83 mV/K 출처

**핵심 정정**: CHERRYPICK에서 확정. v9-05 만 Świderska-Mocek 올바르게 채택. 나머지는 `reynier2009`/`wang2009thermal` 등으로 표기.

| 초안 | bibkey | 저자 | venue | 판정 |
|------|--------|------|-------|------|
| v9-01 | reynier2009 | Y. Reynier et al. | J. Power Sources (2009), S0378775309021119 | ⚠️ 잘못된 논문(Reynier 2009 ≠ +0.83 mV/K 출처) |
| v9-02 | wang2009 | C. Wang, Y. Reynier et al. | J. Power Sources (2009) | ⚠️ 잘못된 논문(동일 오귀인) |
| v9-03 | — | **미등재**(+0.83 mV/K 미인용) | — | ⚠️ 미인용(본문 L447에서 수치 언급되나 out-of-scope처리됨) |
| v9-04 | swiderska2019 | Świderska-Mocek, Rudnicka, Lewandowski | PCCP 21, 2115 (2019) | ✅ **정확** |
| v9-05 | swiderska2019 | 위 동일, 풀 | PCCP 21, 2115 (2019), 10.1039/c8cp06638h | ✅ **정확·DOI 완전** |
| v9-06 | reynier2009 | Wang, Y. Reynier et al. | J. Power Sources (2009) | ⚠️ 잘못된 논문 |
| v9-07 | wang2009thermal | Q. Wang, Y. Reynier et al. | J. Power Sources (2009) | ⚠️ 잘못된 논문 |
| v9-08 | wang2009thermal | J. Wang, Y. Reynier et al. | J. Power Sources (2009) | ⚠️ 잘못된 논문 |
| v9-09 | wang2009 | Y. Wang, Y. Reynier et al. | J. Power Sources (2009) | ⚠️ 잘못된 논문 |

**v9-04·v9-05 만 정확. v9-01/02/06/07/08/09 = 잘못된 논문 오귀인(HIGH).**

---

### ref 7: MSMR Part I — ECS Advances 3, 042501 (2024) (Paul, Wolfe, Verbrugge et al.)

CHERRYPICK 확정: ECS Advances 3, 042501 (2024), DOI 10.1149/2754-2734/ad7d1c.

| 초안 | bibkey | venue | 판정 |
|------|--------|-------|------|
| v9-01 | msmr2023 | **JES 168, 010526 (2021)** — Verbrugge et al. "Thermodynamic model for substitution reactions" | ⚠️ 잘못된 논문(2021년 구 MSMR, ECS Adv 2024 아님) |
| v9-02 | msmr2017 | JES 164, E3243 (2017) | ⚠️ 잘못된 논문(더 이전 구버전) |
| v9-03 | baker2022 | JES 169, 010524 (2022) | ⚠️ 잘못된 논문(Baker & Verbrugge 2022, ECS Adv 2024 아님) |
| v9-04 | msmr2024 | **ECS Advances 3, 042501 (2024)** + Part II JES 2024 | ✅ **정확** |
| v9-05 | msmr2024 | ECS Advances 3, 042501 (2024) + Part II JES 2024 ad70d9 | ✅ **정확·최완전** |
| v9-06 | msmr2024 | ECS Advances (2024), 10.1149/2754-2734/ad7d1c + Part II 10.1149/1945-7111/ad70d9 | ✅ **정확** (단, 저자를 "Verbrugge, Baker et al."로 약식) |
| v9-07 | — | **bibitem 없음**(MSMR 미인용) | — dangling 없음, 단순 미인용 |
| v9-08 | — | **bibitem 없음**(MSMR 미인용) | — |
| v9-09 | — | **bibitem 없음**(MSMR 미인용) | — |

**v9-04·v9-05·v9-06 정확. v9-01~03 모두 구버전/잘못된 MSMR 논문(HIGH).**

---

### ref 8: Teichert et al. 2024 (JMPS 190, 105727 | DOI 10.1016/j.jmps.2024.105727 | arXiv:2302.08991)

★ v9-03 의 "R. Aronson" 은 fabrication 확정.

| 초안 | bibkey | 저자 표기 | venue | 판정 |
|------|--------|---------|-------|------|
| v9-01 | garikipati2024 | "K. Garikipati et al. (Garikipati group)" | JMPS 190, 105727 (2024), arXiv:2302.08991 | ⚠️ 저자 불완전(Garikipati가 마지막 저자인데 1저자로 표기). 핵심정보(JMPS·105727·2302.08991) 맞음 → LOW |
| v9-02 | ml2024 | "(Garikipati group)" 익명 | JMPS 190, 105727 (2024), arXiv:2302.08991 | ⚠️ 저자 익명 처리(LOW) |
| v9-03 | ml2024 | **"R. Aronson et al. (Garikipati group)"** | JMPS 190, 105727 (2024), arXiv:2302.08991 | ❌ **FABRICATION** — R. Aronson은 허위 저자 |
| v9-04 | ml2024 | G. H. Teichert, S. Das, M. Faghih Shojaei, J. Holber, T. Mueller, L. Hung, V. Gavini, K. Garikipati | JMPS 190, 105727 (2024), DOI, arXiv | ✅ **정확·저자 완전** |
| v9-05 | ml2024 | G. H. Teichert, S. Das, M. Faghih Shojaei, J. Holber, T. Mueller, L. Hung, V. Gavini, K. Garikipati | JMPS 190, 105727 (2024), 10.1016/j.jmps.2024.105727, arXiv:2302.08991 | ✅ **정확·최완전** |
| v9-06 | ml2024 | "K. Garikipati group" 익명 | JMPS 190, 105727 (2024), DOI, arXiv | ⚠️ 저자 익명(LOW) |
| v9-07 | garikipati2024ml | "K. Garikipati group" 익명 | JMPS 190, 105727 (2024), DOI, arXiv | ⚠️ 저자 익명(LOW) |
| v9-08 | ml2024lco | "K. Garikipati group" 익명 | JMPS 190, 105727 (2024), DOI, arXiv | ⚠️ 저자 익명(LOW) |
| v9-09 | ml2024 | "Garikipati group" 익명 | JMPS 190, 105727 (2024), DOI, arXiv | ⚠️ 저자 익명(LOW) |

**v9-03 = fabrication(CRITICAL). v9-04·v9-05 = 정확. 나머지 = 저자 익명(LOW).**

---

## (b) ★ 검증된 LCO bibitem 마스터 8건 (체리픽 복사용 완성형)

출처: v9-05를 기준으로 하되, v9-04·v9-07 보완. 각 bibitem 옆에 출처 초안 표시.

```latex
%% ── LCO 인용 마스터 8건 (체리픽 복사용, 검토2 V2 검증) ──

\bibitem{reimers1992}
J. N. Reimers and J. R. Dahn,
``Electrochemical and in situ X-ray diffraction studies of lithium intercalation in
  Li$_x$CoO$_2$,''
\emph{J. Electrochem. Soc.} \textbf{139}, 2091--2097 (1992).
DOI: 10.1149/1.2221184.
% 출처: v9-07(페이지범위)·v9-01(저자완전). 확정 DOI.

\bibitem{menetrier1999}
M. M\'en\'etrier, I. Saadoune, S. Levasseur, and C. Delmas,
``The insulator--metal transition upon lithium deintercalation from LiCoO$_2$:
  electronic properties and $^7$Li NMR study,''
\emph{J. Mater. Chem.} \textbf{9}, 1135--1140 (1999).
DOI: 10.1039/a900016j.
% 출처: v9-07. 9종 일치.

\bibitem{motohashi2009}
T. Motohashi, T. Ono, Y. Sugimoto, Y. Masubuchi, S. Kikkawa,
  R. Kanno, M. Karppinen, and H. Yamauchi,
``Electronic phase diagram of the layered cobalt oxide system
  Li$_x$CoO$_2$ ($0\le x\le1$),''
\emph{Phys. Rev. B} \textbf{80}, 165114 (2009).
DOI: 10.1103/PhysRevB.80.165114; arXiv:0909.3556.
% 출처: v9-01(저자완전)·v9-05. 확정.

\bibitem{xia2007}
H. Xia, L. Lu, Y. S. Meng, and G. Ceder,
``Phase transitions and high-voltage electrochemical behavior of LiCoO$_2$
  thin films grown by pulsed laser deposition,''
\emph{J. Electrochem. Soc.} \textbf{154}(4), A337--A342 (2007).
DOI: 10.1149/1.2509021.
% 출처: v9-07·v9-05. 9종 일치.

\bibitem{reynier2004}
Y. Reynier, J. Graetz, T. Swan-Wood, P. Rez, R. Yazami, and B. Fultz,
``Entropy of Li intercalation in Li$_x$CoO$_2$,''
\emph{Phys. Rev. B} \textbf{70}, 174304 (2004).
DOI: 10.1103/PhysRevB.70.174304.
[동 그룹: \emph{J. Electrochem. Soc.} \textbf{151}, A422 (2004).]
% 출처: v9-04·v9-05. PRB 70이 확정 primary.

\bibitem{swiderska2019}
A. {\'S}widerska-Mocek, E. Rudnicka, and A. Lewandowski,
``Temperature coefficients of Li-ion battery single electrode potentials
  and related entropy changes---revisited,''
\emph{Phys. Chem. Chem. Phys.} \textbf{21}, 2115 (2019).
DOI: 10.1039/c8cp06638h.
[LiCoO$_2$ 단전극 $\partial\phi/\partial T\approx+0.83$ mV/K, tier B.]
% 출처: v9-05(DOI 완전). +0.83 mV/K 확정 출처(CHERRYPICK §인용 정정).

\bibitem{msmr2024}
A. Paul, K. Wolfe, M. W. Verbrugge, B. J. Koch, J. S. Lowe, J. Trembly,
  J. A. Staser, and T. R. Garrick,
``Quantifying the Temperature Dependence of the Multi-Species, Multi-Reaction
  (MSMR) Model. Part~1: Parameterization for a Meso-Carbon Micro-Bead Graphite,''
\emph{ECS Advances} \textbf{3}, 042501 (2024).
DOI: 10.1149/2754-2734/ad7d1c.
[Part~II: \emph{J. Electrochem. Soc.}, DOI: 10.1149/1945-7111/ad70d9.]
% 출처: v9-05(가장 완전). ECS Advances 3 확정(CHERRYPICK §인용 정정).

\bibitem{ml2024}
G. H. Teichert, S. Das, M. Faghih Shojaei, J. Holber, T. Mueller,
  L. Hung, V. Gavini, and K. Garikipati,
``Bridging scales with machine learning: from first-principles statistical
  mechanics to continuum phase-field computations to study order--disorder
  transitions in Li$_x$CoO$_2$,''
\emph{J. Mech. Phys. Solids} \textbf{190}, 105727 (2024).
DOI: 10.1016/j.jmps.2024.105727; arXiv:2302.08991.
% 출처: v9-04·v9-05. 저자 확정(CHERRYPICK §). v9-03 "R.Aronson" = fabrication 폐기.
```

---

## (c) 인용 최정확 보완본

**v9-05** = 인용 정확도 최고.
- Świderska-Mocek 2019 bibitem 완전(DOI 포함)
- MSMR ECS Adv 3, 042501 (2024) 정확 + Part II JES DOI 병기
- Teichert et al. 저자 완전 (ml2024)
- Reynier PRB 70, 174304 (2004) primary 정확
- Xia, Reimers, Ménétrier, Motohashi 모두 정확

**v9-04** = 공동 1위. Teichert 저자 완전, Reynier PRB 70 정확, MSMR 정확. 단 swiderska bibitem 에 DOI 있으나 v9-05 대비 약간 간결.

**v9-07** = Reimers·Ménétrier·Motohashi 페이지 범위(끝 페이지)가 가장 완전하나, ml2024 저자 익명, MSMR 미인용으로 -2점.

---

## 종합 fabrication·오류 요약

| 구분 | 초안 | 항목 | 판정 | 비고 |
|------|------|------|------|------|
| FABRICATION | v9-03 | ml2024 저자 "R. Aronson" | ❌ | 허위 저자 — 폐기 |
| HIGH 오류 | v9-01/02/06/07/08/09 | +0.83 mV/K = reynier2009/wang2009 | ⚠️ | 잘못된 논문(Świderska-Mocek 2019가 정확) |
| HIGH 오류 | v9-01/02/03 | MSMR = 2021/2017/2022 구버전 | ⚠️ | ECS Adv 3, 042501 (2024)이 정확 |
| dangling | v9-03 | reimers1992 bibitem 미등재 | ⚠️ | 본문에서 \cite{reimers1992} 사용하나 bibitem 없음 |
| LOW | v9-01 | reynier2004 JES DOI 기재(primary는 PRB) | 경미 | 실질 정보 동일 |
| LOW | v9-02 | reynier2004 JES DOI 오기(10.1149/1.1646152) | 경미 | — |
| LOW | v9-01/02/06/07/08/09 | ml2024 저자 익명/불완전 | 경미 | Garikipati group 익명 |
