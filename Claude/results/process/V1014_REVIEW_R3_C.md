# V1.0.14 P4.1 R3 검수자 C — 레퍼런스 정합 검수 보고서

검수자: C (Sonnet) · 렌즈: 레퍼런스 정합(①인용-주장 정합 ②bibitem 서지 형식 ③orphan/누락 ④tier 표기 일관성 ⑤ch2 독립 bibliography ⑥부록 [A1]-[A5])
대상: `graphite_ica_ch1_v1.0.14.tex`(3229줄, 전문 정독) · `graphite_ica_ch2_v1.0.14.tex`(782줄, 전문 정독) · `appendix_phase_separation.tex`(483줄, 전문 정독)
보조: `V1014_REF_SOURCES.md`(판정 근거로만 사용, 그 자체를 검수 대상으로 삼지 않음)
방법: 전 `\cite{}` 40건(ch1)·24건(ch2) 발생처 문맥 대조 + bibitem 28건(ch1)·14건(ch2) 전수 cross-check + 의심 항목 2건은 WebSearch 실시간 재검증(질문 시점 2026-07-04 기준). ★파일 수정 없음.

---

## 0. 총평(refute 생존 항목만)

대다수 인용은 견고하다 — 특히 이번 개정에서 다뤄졌을 park2021(4곳)·reynier2003·persson2010/2010b·cogswell2012 는 **모두 결함 없음**으로 확인했다(§1). 실제로 생존하는 결함은 (a) 부록의 참고문헌이 본문에 전혀 anchoring 되지 않는 구조적 공백 1건(MEDIUM), (b) ch1↔ch2 두 독립 문헌간 MSMR 인용 키 네이밍 충돌 1건(MEDIUM, 실시간 검색으로 확정), (c) 캡션 tier 병기의 정밀도 손실 1건(LOW) 이다. CRITICAL/HIGH 는 없다.

---

## 1. 인용-주장 정합 — 이번 개정 대상 4건(결함 없음, 근거 명시)

### 1-1. park2021 (흑연 GITT) — 4개소 전부 정합

| 위치 | 원문 인용 | 판정 |
|---|---|---|
| ch1 L1472 | "LCO 양극의 세 전이에는 흑연-특정 구조 무질서 근거를 옮기지 않고 일반 $\eta$ 분포(iii-b)로만 다룬다(LCO 의 평형 $U_j$ 입자 무관성은 흑연 GITT\cite{park2021} 의 직접 증거가 아니라 동형 \emph{가정}이다 — tier C 추정" | 정합 — LCO 로의 외삽을 tier C 로 명시 하향, 원 논문(흑연 전용)의 scope 를 넘지 않음 |
| ch1 L1487 | "흑연 하프셀 GITT 준평형 OCP 가 staging 전위를 입자 크기$\cdot$전극 형상과 무관한 상수로 주므로\cite{park2021}" | 정합 — "흑연 하프셀"로 정확히 scope 한정 |
| ch1 L1603 | "흑연의 GITT 실측 확산계수 $D\approx10^{-11}$--$4\times10^{-10}$ cm$^2$/s\cite{park2021}" | 정합 — REF_SOURCES §6, §8 이 확인한 실제 논문의 D 값과 자릿수까지 일치 |
| ch1 L1623 | "(b)-(iii-b) 의 GITT 한정과 동일\cite{park2021}" | 정합 — 자기참조, 위 hedge 유지 |

bibitem(L3222)도 "구판의 제목 오기 정정"이라 명시하고 실제 논문 제목("Investigation of Lithium Ion Diffusion of Graphite Anode by the GITT")으로 정정되어 있다 — REF_SOURCES §8 이 지적한 과거 오류(LCO/graphite 전셀 논문으로 오기)가 **이미 전부 수정**되었고, 4개소 본문 모두 "흑연 전용" scope 를 정확히 지킨다. **결함 없음.**

### 1-2. reynier2003 (흑연 삽입 엔트로피·엔탈피 실측) — 정합

ch1 L1965: "$\Delta S_\rxn$ 의 부호$\cdot$수십 J/(mol\,K) 스케일은 흑연 삽입 엔트로피 실측\cite{reynier2003} 과 정합(전이별 정밀값 아님 — tier B)." bibitem(L3223)도 동일하게 "부호$\cdot$스케일 anchor(tier B), 전이별 정밀값 아님"으로 일치. ch2(자체 bibitem, L770)에서도 같은 논문을 "저 Li 분율에서 양(config 우세), 고 분율에서 음(vib 우세)" 서술(L332, L391)로 인용 — REF_SOURCES §2 의 실제 논문 취지("부호 반전: 저 x mixing 우세·고 x vibrational 우세")와 정확히 일치. **결함 없음.**

### 1-3. persson2010 / persson2010b (DFT 활성화 경향) — 정합, 저자 목록 실시간 재검증 완료

ch1 L1982-1983: "$\Delta H_a$ 는 저SOC$\to$만충에서 감소하는 DFT 활성화 경향\cite{persson2010,persson2010b} 에 맞춘 스케일이고(전이별 수치의 전용 문헌 anchor 는 근거 미발견 — 실측 계면 활성화 에너지의 문헌 범위 $25$--$59$ kJ/mol 와 겹치는 출발점)" — 과주장 없이 정확히 hedge.

bibitem 저자 목록을 WebSearch 로 직접 재검증(REF_SOURCES §3 의 "후보1" 저자 목록이 두 논문을 뒤섞어 표기하고 있어 교차확인 필요했음):
- `persson2010`(JPCL 1, 1176, 2010, DOI 10.1021/jz100188d, L3224) 저자 = "K. Persson, V. A. Sethuraman, L. J. Hardwick, Y. Hinuma, Y. S. Meng, A. van der Ven, V. Srinivasan, R. Kostecki, G. Ceder" — ACS 공식 페이지 실시간 검색으로 **9인 전원 일치 확인**.
- `persson2010b`(PRB 82, 125416, 2010, DOI 10.1103/PhysRevB.82.125416, L3225) 저자 = "K. Persson, Y. Hinuma, Y. S. Meng, A. Van der Ven, G. Ceder" — APS(link.aps.org) 실시간 검색으로 **5인 전원 일치 확인**.

두 bibitem 모두 정확하다(REF_SOURCES.md 자체의 §3 "후보1" 저자열이 두 논문 저자를 혼합 표기한 것일 뿐, 검수 대상 tex 파일은 오류 없음). **결함 없음 — 오히려 REF_SOURCES.md 초안의 저자열 혼선을 최종본이 올바르게 분리 반영했음을 확인.**

### 1-4. cogswell2012 (계면 에너지 γ) — 정합

ch1 L1587-1588: "계면 에너지는 $\gamma\sim0.1$--$1$ J/m$^2$ 스케일로 상정한다(수치의 전용 문헌 anchor 는 근거 미발견 — tier C; 상분리 입자 전극의 계면 에너지 논의는 Cogswell--Bazant\cite{cogswell2012} 참조." bibitem(L3226)도 "본 문건 $\gamma$ 수치의 출처 아님(스케일 상정은 tier C)"라고 명시 — 과거 v10-10 에서 "사이즈 효과 배제"용으로 의도적으로 뺐던 것을(L22, L24 changelog 주석) 이번엔 "γ 수치 참조"라는 별개 용도로 재도입했음이 REF_SOURCES §6 지적과 정확히 일치하며, 본문도 "출처 아님"으로 과주장을 스스로 차단한다. **결함 없음.**

---

## 2. 생존 결함

### [MEDIUM] F1 — 부록 [A1]-[A5] 가 본문에 전혀 anchoring 되지 않음

`appendix_phase_separation.tex` L468-480 은 다음처럼 5건을 나열한다:

```
\section*{참고문헌}
\begin{enumerate}[label={[A\arabic*]},leftmargin=3.2em]
\item J.~W. Cahn, J.~E. Hilliard, ``Free energy of a nonuniform system. I. ...'' (1958). DOI: 10.1063/1.1744102.
\item J.~W. Cahn, ``On spinodal decomposition,'' ... (1961). DOI: 10.1016/0001-6160(61)90182-1.
\item D.~A. Porter, K.~E. Easterling, Phase Transformations in Metals and Alloys ...
\item M. Hillert, Phase Equilibria, Phase Diagrams and Phase Transformations ...
\item R.~W. Balluffi, S.~M. Allen, W.~C. Carter, Kinetics of Materials ...
\end{enumerate}
```

그러나 본문 전체(L1-467)를 정독한 결과 `\cite{}` 도, "[A1]" 류의 명시적 인라인 마커도 **단 하나도 없다**. 예컨대 L421-424 "$F[\xi]=\int[\cdots]\dd V$ ... 로 확장된다(Cahn--Hilliard)."는 [A1]·[A5] 둘 다와 관련 있을 이론을 이름만으로 부르고 괄호 인용을 달지 않았고, L472-479 표의 "핵생성" 행([A3]·[A5] 대응 추정)도 마찬가지다. 결과적으로 독자는 어느 절의 어느 결과가 [A1]-[A5] 중 어느 항목에서 왔는지 텍스트만으로 추적할 수 없다 — 목록 존재 자체는 서지 정보로서 유효하나(§3 참조), \S\ref{app:link}("본문과의 연결")조차 [A숫자] 표기 없이 절 이름으로만 대응을 서술한다(L454-466). ★검수 지시의 "스타일 상이 허용"은 서식(스타일)에 대한 허용이지, 인용 마커 부재(anchoring 자체의 부재)까지 포괄한다고 보기 어려워 결함으로 보고한다.

**정정 제안**: 관련 문장 옆에 "[A1]", "[A2]" 등 인라인 마커를 최소 1회씩 추가하거나, 각 참고문헌 항목 끝에 "(→ \S\ref{app:...} 대응)"을 부기.

### [MEDIUM] F2 — ch1 `msmr2024` ("Part 1") 과 ch2 `msmr_partI` 는 실제로 다른 논문(실시간 검색 확정) — 챕터간 네이밍 충돌

ch1 bibitem(L3215): `msmr2024` = A. Paul 외, "Quantifying the temperature dependence of the multi-species, multi-reaction (MSMR) model. **Part I**: Parameterization for a meso-carbon micro-bead graphite," *ECS Advances* 3, 042501 (2024). DOI: **10.1149/2754-2734/ad7d1c**. [주석: "Part II: J. Electrochem. Soc., DOI: 10.1149/1945-7111/ad70d9."]

ch2 bibitem(L775): `msmr_partI` = "Quantifying the Entropy and Enthalpy of Insertion Materials for Battery Applications Via the Multi-Species, Multi-Reaction Model," *J. Electrochem. Soc.* (2024). DOI: **10.1149/1945-7111/ad1d27**.

두 키 이름("Part I"/`msmr_partI`)이 같은 논문을 가리키는 것처럼 보이지만, WebSearch 로 두 DOI 를 각각 실시간 확인한 결과 **완전히 다른 두 편**이다 — `ad7d1c`(ECS Advances, "Part 1" 이 실제 제목에 포함, MCMB graphite 전용 파라미터화)와 `ad1d27`(JES, 제목에 "Part I" 자체가 없음, HTFDA 열량계로 NMC811/graphite pouch cell 을 다룸)은 저널·DOI·주제가 다르다. 반면 "Part II"(DOI `ad70d9`)는 ch1 의 주석과 ch2 의 `msmr_partII`(L776) 양쪽에서 **동일 DOI 로 일치**한다.

즉 두 챕터를 함께 읽는 독자는 ch2 의 `msmr_partI` 를 ch1 이 말하는 "Part I"(ECS Advances)로 오인할 위험이 있다 — 실제로는 셋째의 별개 논문이다. bibitem 각각의 저자·제목·DOI 자체는 (ad1d27 페이지 검색으로 확인한 범위에서) 정확하나, **키 네이밍이 오귀속을 유발**한다.

**정정 제안**: ch2 의 `msmr_partI` 키를 `msmr_entropy2024` 등으로 개명하거나, bibitem 끝에 "(Ch.1 의 'Part I'/ECS Advances 논문과는 별개)" 주석 추가.

### [LOW] F3 — tab:staging 캡션(ch1 L1960-1965)의 tier 정밀도 손실

L1961-1963: "전위 anchor: $4\!\to\!3$($0.210$ V)$\cdot$$2\!\to\!1$($0.085$ V)는 Dahn\cite{dahn1991} 의 보고값과 정합, $2\mathrm L\!\to\!2$($0.120$ V)는 Ohzuku 등\cite{ohzuku1993} 의 보고값과 정합(모두 2차 출처 경유 확인)"

REF_SOURCES §1 에 따르면 이 세 값의 실제 근거 강도는 서로 다르다 — $2\to1$(tier A, 정확 일치)·$2\mathrm L\to2$(tier A, 정확 일치)·$4\to3$(tier B, 2차 출처를 통한 근사 확인)인데, 캡션은 셋을 "모두 2차 출처 경유 확인"으로 뭉뚱그린다. 과주장은 아니다(오히려 tier A 두 건을 tier B 수준으로 보수적으로 묶은 셈이라 안전한 방향의 손실이다) — 다만 바로 다음 문장이 $3\to2\mathrm L$ 한 건만 "(tier C — 문헌 간 $5$--$15$ mV 편차)"로 명시적 tier 를 붙인 것과 대조하면, 같은 문단 안에서 tier 표기 입도가 들쭉날쭉하다. CRITICAL 은 아니나 §4(tier 표기 일관성) 렌즈가 요구하는 균질성 기준으로는 결함.

**정정 제안**: "($2\!\to\!1\cdot2\mathrm L\!\to\!2$: tier A 후보, 2차 출처 경유라 tier B 로 보수 처리; $4\!\to\!3$: tier B)" 식으로 세 값에 개별 tier 병기.

---

## 3. 검사했으나 결함 없음으로 확정한 항목(빈 통과 방지용 근거 명시)

- **ch1 bibitem 28건 전수 vs `\cite{}` 40건 전수**: orphan 0, undefined-key 0 (모든 bibitem 이 최소 1회 이상 인용됨: dahn1991·ohzuku1993·bazant2013·eyring1935·hill1960·fowler1939·mcquarrie1976·mckinnon1983·dreyer2010·bloom2005·dubarry2012·reimers1992·menetrier1999·motohashi2009·xia2007·reynier2004·swiderska2019·msmr2024·ml2024·leviaurbach1999·rsc2021·fly2020·dahn1995·park2021·reynier2003·persson2010·persson2010b·cogswell2012).
- **ch2 bibitem 14건 전수 vs `\cite{}` 24건 전수**: orphan 0, undefined-key 0, ch1 bibliography 와 완전 독립(자체 bibitem 만 참조) — lens⑤ 통과.
- **tier A "$g_{\max}=13$" 4개소(L2367, 2480, 2547, 2579)**: 전부 "$\mathrm{CoO_2}$ $x{=}0$ 단일 anchor" 라는 동일 주장에 동일 tier A 를 일관 부여 — 모순 없음(REF_SOURCES §5 는 수치 자체의 원문 직접 대조는 실패했다고 밝히나, 이는 tex 파일의 tier 부여 방식 자체의 결함이 아니라 원문 접근성 문제이므로 별개 사안).
- **reynier2004 의 이중 tier(L2518/2597 tier B "0.18 $k_B$/atom 총합" vs L2599 tier A "config >1/2 지배")**: 언뜻 같은 인용키에 다른 tier 로 보이나 L2603-2610 "★세 양의 구분" 박스가 두 주장이 서로 다른 양(총합 수치 vs 지배 비율)임을 명시적으로 구분 — 동일 값에 다른 tier 가 붙은 사례가 아니므로 결함 아님.
- **T2/T3 config 값(≈0.47/1.49 J/(mol K))의 tier C**: 표(L2058-2059)·본문(L2367-2368, L2785) 3개소 모두 tier C 로 일관.
- **swiderska2019 tier B**: L2217·2234-2235·3053(R6 표) 3개소 모두 일관.
- **[A1] Cahn\&Hilliard 1958** (J. Chem. Phys. 28, 258-267, DOI 10.1063/1.1744102): WebSearch 실시간 재검증 완료 — 저자·권·쪽·DOI 전부 일치.

---

## 4. 미검증(4-tier 보고)

- [A2]-[A5](Cahn 1961·Porter–Easterling·Hillert·Balluffi 등)는 서지 형식상 이상 없어 보이나 이번 라운드에서 개별 실시간 재검색은 하지 않았다 — 정식 학계 정전(canonical) 문헌이라 개연성은 높으나 "확정"은 아니고 "추정"으로 분류한다.
- reynier2004 의 ">1/2 지배, tier A"(L2599) 라벨이 tier B(L2518/2597, "0.18 $k_B$/atom 총합")보다 더 강한 확신도를 가질 근거가 충분한지는 원논문 재확인 없이는 최종 판정 불가 — 결함으로 확정하지 않고 §4 미검증 항목으로 남긴다.
