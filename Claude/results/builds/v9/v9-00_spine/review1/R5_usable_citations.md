# R5 검토 보고 — G-follow/G-usable + 인용 검증 + best-base 추천

> 검수 sub R5 전담 렌즈: G-follow(따라가짐)·G-usable(산출 가능성)·인용 정확성·tier 정직성.
> 대상: v9-01 ~ v9-09. Ground truth: research/CH1v9_LCO/10_sources_master.md·20_extraction/_SUMMARY.md·v9-00_spine/REVIEW_NOTES.md.
> 빈 통과 금지 — 각 초안 최소 1 결함 적시.

---

## (a) 9종 G-follow / G-usable 랭킹

### 렌즈 정의
- **G-follow**: 서론이 "흑연 음극 ICA → 같은 프레임을 양극으로 확장 → LCO 고유 항(전자 엔트로피) 도입"의 일반→흑연→LCO 흐름으로 따라가지나? LCO 절이 부록이 아닌 spine 통합인가?
- **G-usable**: 이 문건만 보고 LCO dQ/dV 피팅 코드(∂U/∂T·ΔS 분해·전자항 plug-in)를 재현 가능한가? 갭(G1–G5)이 round-trip 피팅 위임으로 정직하게 표기됐나?

| 순위 | 초안 | G-follow 점수 | G-usable 점수 | 종합 | 비고 |
|------|------|-------------|-------------|------|------|
| **1** | **v9-06 (Opus)** | ★★★★☆ | ★★★★★ | **최선** | 일반→흑연→LCO 흐름 명시("전극 불문 → 흑연 → LCO"); 전자 엔트로피 절이 N4/N5 직후 spine 위치; C_e 먼저 유도 후 부분몰 전환; MIT 필수성 정당화 4항; logistic 게이트 자기일관성 명시; 갭(G1–G5) round-trip 위임 정직; 코드 plug-in 방법까지 명시. LCO bibitem 전무가 유일 결함. |
| **2** | **v9-04 (Opus)** | ★★★★☆ | ★★★★☆ | 차선 | 서론에 "일반→흑연→LCO" 통합 범위 명시("전개 순서: 일반→흑연 사례→LCO 사례"); 전자 엔트로피 유도 완결(Fermi→Sommerfeld→부분몰→MIT gate); "ML 2024 tier A" 인용하나 bibitem 없음(dangling); reynier2004 bibitem 이 JPS 2003 으로 잘못된 논문. |
| **3** | **v9-02 (Sonnet)** | ★★★★☆ | ★★★★☆ | 3위 | 서론에 흑연·LCO 통합 프레임("같은 forward 모델 프레임으로 통합") 명시; N2 직후 LCO 양극 절; 전자 엔트로피 유도 완결(Fermi→Sommerfeld→부분몰); 삽입 기준 ΔS_e 부호(Li 삽입 양수→ΔS_e<0) 로 쟁점1 분기. reynier2004 DOI 10.1149/1.1646152 수록(검증 필요). |
| **4** | **v9-05 (Opus)** | ★★★☆☆ | ★★★★☆ | 4위 | N0 뒤 "두 번째 전극 — LCO 양극" 통합 소절 명시; 부호 해결책 가장 명쾌(ξ=탈리튬화 진행률 고정·σ_d-라벨 매핑). 단 LCO 인용 bibitem 전무(Xia·Reynier·Motohashi·ml2024 모두 본문에만 혹은 없음). G-usable 양호하나 인용 누락이 독립 사용 장벽. |
| **5** | **v9-01 (Sonnet)** | ★★★☆☆ | ★★★☆☆ | 5위 | N0 직후 LCO 전이표·부호 소절 통합; 전자 엔트로피 절 완결. 결정적 결함: ml2024lco = "(Tier G — gap) Internal note 2024" — bibitem이 허위 인용(실제 논문 정보 없이 내부 노트 처리). 이 항목만으로 인용 신뢰도 최저. 단 Reimers·Ménétrier·Reynier bibitem은 DOI 기재. |
| **6** | **v9-03 (Sonnet)** | ★★★☆☆ | ★★★☆☆ | 6위 | 서론 흑연 집중("흑연 음극 ICA") → LCO 확장은 사후 삽입 구조. ml2024 = "tier-inferred DOI 미확정 placeholder" 가장 정직한 표기(★); xia2018 bibitem이 Xia 2007 이 아닌 Electrochim. Acta 2018 다른 논문. motohashi2019→2009 혼동(bibitem key 2019, 실제 2009). |
| **7** | **v9-07 (Codex)** | ★★☆☆☆ | ★★★☆☆ | 7위 | 전자 엔트로피 절 존재; 기계적 서술. G-follow 보통(LCO 절 통합은 있으나 흐름 다리 박함). LCO 관련 bibitem 전무(Motohashi·Xia·Reynier·Reimers·ml2024 — 어느 것도 없음). |
| **8** | **v9-08 (Codex)** | ★★☆☆☆ | ★★★☆☆ | 8위 | v9-07과 유사; 부분몰 전자 엔트로피 부호 처리에 ζ=탈리튬화 좌표 별도 명시(쟁점1 대응). LCO bibitem 전무. |
| **9** | **v9-09 (Codex)** | ★★☆☆☆ | ★★☆☆☆ | 9위 | 전자 엔트로피 절 존재하나 서술 압축. G-follow 최약(LCO를 "신규 항이 필요한 전극"으로만 도입, 자연 전개 박함). LCO bibitem 전무. |

### 종합 best-base 추천

**→ v9-06을 체리픽 출발 초안으로 추천.**

근거:
1. 서론에서 "전극 불문 일반 → 흑연 → LCO" 흐름을 명시적으로 선언한 유일 초안(v9-04도 유사하나 v9-06이 더 이른 절에서).
2. 전자 엔트로피 절: C_e(전자 비열) 먼저 유도 → S_e → 부분몰 ΔS_e 순서가 가장 교과서적(자연 전개).
3. MIT 필수성 정당화: logistic gate 자기일관성(Fermi-Dirac 점유와 동일 함수형) 설명이 유일하게 있음 → G-usable 최고.
4. 갭 처리: G1–G5 항목 명시 + round-trip 피팅 위임 정직.
5. 코드 plug-in까지 서술(ΔS_rxn 에 ΔS_e 합산 → func_U_j 호출).
6. LCO bibitem 전무가 유일 심각 결함이나, 체리픽 후 v9-03의 정직 표기·v9-02의 DOI 기재 bibitem을 이식하면 해소 가능.

차선: v9-04 — 전자 엔트로피 유도 완결도 비슷, "흑연 대비" 비교 교육 단락 탁월. 단 reynier2004 bibitem 오류가 G-usable 신뢰 손상.

---

## (b) 인용 결함표

### ml2024 (쟁점2 핵심)

Ground truth: arXiv 2302.08991 = Garikipati 그룹, "Bridging scales with ML…order–disorder LixCoO2", *J. Mech. Phys. Solids* **190**, 105727 (2024). DOI: S0022509624001923. Full-text 정독 tier A 확보.

| 초안 | ml2024 처리 | 심각도 | 평가 |
|------|-------------|--------|------|
| v9-01 | `\bibitem{ml2024lco}` = "(Tier G — gap) Simulated evidence … Internal note, 2024" | **CRITICAL** | 허위 bibitem: 실제 논문 정보 없이 내부 노트로 처리. arXiv 2302.08991 은 존재하는 논문. |
| v9-02 | ml2024 인용 없음; 논거 menetrier·reynier 독립 지지로 대체 | HIGH | ml2024 언급 없이 핵심 논거 성립시킴. 독립 지지 전략은 타당하나 MIT 필수성 논거가 약해짐. |
| v9-03 | `\bibitem{ml2024}` = "[tier-inferred, DOI 미확정] 추정: J. Power Sources 계열 (2024 추정). … 실증 후 교체 요망" | MED | 가장 정직한 표기. Ground truth DOI 이식하면 바로 tier A 승격 가능. ★ 체리픽 대상. |
| v9-04 | 본문 "[ML 2024, tier A]" — bibitem 없음(dangling cite) | HIGH | tier A 주장하나 bibitem 없어 LaTeX undefined reference. DOI 기재 시 tier A 정당. |
| v9-05 | ml2024 인용 없음; "config 단독 MIT 불가" 논거 언급 없음 | HIGH | 전자 엔트로피 필수성 논거 중 ML 2024 의 직접 증거 누락 → 필수성 정당화 약화. |
| v9-06 | 본문 "[ML 2024, tier A]" — bibitem 없음(dangling) | HIGH | v9-04 동일 패턴. |
| v9-07 | ml2024 인용 없음; 전자 엔트로피 필수성 논거 내부 논리로만 | MED | 독립 지지(Ménétrier·Reynier)도 명시 없음. |
| v9-08 | 동상 | MED | 동상. |
| v9-09 | 동상 | MED | 동상. |

**판정**: ml2024 = arXiv 2302.08991 = *J. Mech. Phys. Solids* **190**, 105727 (2024), DOI 10.1016/j.jmps.2024.105727 (또는 S0022509624001923)으로 실증됨. 체리픽 시 v9-03의 정직 placeholder를 DOI 실증 결과로 교체하면 tier A로 승격 가능. v9-01의 "(Internal note)"는 반드시 실제 bibitem으로 대체해야 함.

### Reynier/Yazami 2004 DOI 혼동

Ground truth 추출카드: Reynier·Graetz·Swan-Wood·Rez·Yazami·Fultz, *J. Electrochem. Soc.* **151**, A422 (2004). CaltechAUTHORS record 2974.

| 초안 | 기재 내용 | 결함 |
|------|----------|------|
| v9-01 | JES 151, A422 (2004). DOI: 10.1149/1.1646139 | DOI 수치 미검증. 제목 "graphites and disordered carbons"→흑연 논문, LCO 논문 제목은 "Entropy of Li intercalation in LixCoO2" — **제목 오류**. |
| v9-02 | JES 151, A422 (2004). DOI: 10.1149/1.1646152. 제목 "Entropy analysis" | DOI 미검증. 제목 일부만. |
| v9-03 | JES 151, A422 (2004). DOI 없음 | DOI 누락. 제목 "graphites and disordered carbons" — 흑연 논문 제목 사용(v9-01과 동일 오류). |
| v9-04 | **\bibitem{reynier2004}** = JPS **119–121**, 850 **(2003)**. DOI: 10.1016/S0378-7753(03)00285-4 | **CRITICAL**: 다른 논문(2003 JPS). key는 2004인데 2003 JPS 논문 기재. 실측 ΔS LCO 값의 출처가 완전히 다른 논문을 가리킴. |
| v9-05 | Reynier 인용 없음 | LCO bibitem 전무. |
| v9-06 | Reynier 인용 없음 | LCO bibitem 전무. |

**판정**: v9-04의 reynier2004 bibitem은 CRITICAL 오류 — JPS 2003 이 JES 2004 를 대체 불가. 체리픽 시 v9-02의 JES 151/A422 형태를 사용하되 DOI는 추가 검증 필요.

### Xia(Ceder) 인용

Ground truth: Xia, Lu, Meng, Ceder, *J. Electrochem. Soc.* **154**(4), A337 (2007). DOI: 10.1149/1.2509021.

| 초안 | 기재 내용 | 결함 |
|------|----------|------|
| v9-01 | 본문 "tier A=Xia" — bibitem 없음 | bibitem 미수록. |
| v9-02 | `\bibitem{xia2006}` = JPS (2006) "lithium-rich layered oxide cathode" | **HIGH**: 다른 논문(2006 JPS, lithium-rich). Xia 2007 JES dQ/dV 논문이 아님. |
| v9-03 | `\bibitem{xia2018}` = Electrochim. Acta **225**, 573 (2018) | **HIGH**: 다른 논문(2018 EA). |
| v9-04 | 본문 "tier A=Xia" — bibitem 없음 | bibitem 미수록. |
| v9-05~09 | Xia bibitem 없음 | 누락. |

**판정**: Xia 2007 (JES, DOI 10.1149/1.2509021)이 올바른 인용. 현재 9종 모두 올바른 bibitem 없음 — 체리픽 시 신규 bibitem 필수.

### Motohashi 2009/2010 혼동

Ground truth: Motohashi *et al.*, "Electronic phase diagram…", *Phys. Rev. B* **80**, 165114 (2009). DOI: 10.1103/PhysRevB.80.165114.

| 초안 | 기재 내용 | 결함 |
|------|----------|------|
| v9-01 | `\bibitem{motohashi2010}` = PRB **83**, 195128 (2010). DOI: 10.1103/PhysRevB.83.195128 | **HIGH**: 다른 연도·다른 논문(PRB 83 2010 ≠ PRB 80 2009). |
| v9-02 | `\bibitem{motohashi2009}` = PRB **80**, 165114 (2009). DOI: 10.1103/PhysRevB.80.165114 | ★정확. |
| v9-03 | `\bibitem{motohashi2019}` key 오류, 실제 2009 내용 | key 연도 오류(2019). |
| v9-04 | `\bibitem{motohashi2009}` = PRB **80**, 165114 (2009). DOI: 10.1103/PhysRevB.80.165114 | ★정확. |

### Reimers & Dahn 1992

Ground truth: Reimers·Dahn, *J. Electrochem. Soc.* **139**, 2091 (1992). DOI: 10.1149/1.2221184.

v9-01·02·04 모두 JES 139, 2091, DOI 10.1149/1.2221184 — **정확**. v9-05~09: bibitem 없음.

---

## (c) tier 정직성 평가

### 갭(G1–G5) 표기 정직성

| 항목 | 최선 초안 | 최악 초안 | 비고 |
|------|-----------|-----------|------|
| G1 (ΔS(x) 연속표) | v9-05·v9-06 (round-trip 피팅 위임 명시) | v9-07·08·09 (언급 없음) | G1 부재는 설계문서 확정 갭 |
| G2 (g(E_F)(x) 연속함수) | v9-06 ("g(E_F)(x) 미확보, logistic 근사 초기값") | v9-01 ("모델 가정: g_max=13, x_MIT=0.85" 만) | 초기값을 피팅 대상으로 명시해야 |
| G3 (MSMR LCO 파라미터) | v9-02·03 (MSMR 동형 언급) | v9-07~09 (언급 없음) | |
| G4 (도핑 shift 정량) | v9-06 (도핑=smear/shift, 피팅 대상) | v9-09 (언급 없음) | |
| G5 (ΔH_f 절대값) | v9-05·v9-06 (OCV plateau anchor 대체 명시) | v9-03 (언급 없음) | |

### 이중계산(B) 정직성

v9-01·02·04·05·06 모두 이중계산 금지 명시:
- "ΔS°_j(중심 표준값)은 중심값에만, config 분산은 logistic이 자동 생성"
- "ΔS_e(x,T)는 별도 항, logistic 배치 분산과 혼동 금지"

v9-07·08·09: 이중계산 금지 명시 없음 — MED 결함.

### 전자 엔트로피 ∝T 명시

모든 초안(v9-01~09): ΔS_e ∝ T 명시 — 통과.

### g(E_F) 허위 정밀 여부

v9-01·02·04·05·06: g_max=13 e/eV를 "Motohashi tier A anchor, 초기값·피팅 대상" 명시 — 정직.
v9-07·08·09: 수치 기재 후 tier 표기 없음 — MED 결함.

---

## (d) 가장 약한 1곳 (빈 통과 금지)

| 초안 | 가장 약한 결함 | 심각도 |
|------|-------------|--------|
| v9-01 | ml2024lco = Internal note 처리 — 실제 논문 정보 없이 "(Tier G — gap)" bibitem 기재. 허위 학술 인용. | **CRITICAL** |
| v9-02 | `\bibitem{xia2006}` = 2006 JPS "lithium-rich" 다른 논문. tier A 근거가 잘못된 Xia 인용 가리킴. | HIGH |
| v9-03 | `\bibitem{xia2018}` = 2018 Electrochim. Acta 다른 논문. 동일 패턴. | HIGH |
| v9-04 | `\bibitem{reynier2004}` = 2003 JPS 다른 논문 — LCO ΔS 정량값의 출처가 전혀 다른 논문. | **CRITICAL** |
| v9-05 | LCO bibitem 전무 + ml2024 인용 없이 MIT 필수성 논거 독립 지지도 불완전. | HIGH |
| v9-06 | "[ML 2024, tier A]" 본문 인용 + bibitem 없음(dangling). "[ML 2024, tier A]" 주장이 LaTeX undefined. | HIGH |
| v9-07 | LCO bibitem 전무(Motohashi·Xia·Reynier·Reimers·ml2024 모두 없음). | HIGH |
| v9-08 | LCO bibitem 전무 + 부분몰 부호 처리를 ζ vs x 이중 좌표로 기술 — 독자 혼란 위험. | HIGH |
| v9-09 | 전자 엔트로피 서술 가장 압축. MIT 필수성 정당화 논거 없음. LCO bibitem 전무. | HIGH |

---

## 체리픽 지침 (master 삼각검증 입력)

1. **best-base = v9-06**: 서론·LCO 절 위치·유도 완결도·갭 처리·코드 plug-in 명시 최선.
2. **인용 이식 필수**:
   - ml2024: v9-03 placeholder → DOI 10.1016/j.jmps.2024.105727 실증 후 tier A 교체.
   - Xia 2007: 신규 `\bibitem{xia2007}` = JES **154**(4), A337 (2007), DOI 10.1149/1.2509021.
   - Motohashi: v9-02·v9-04의 PRB **80**, 165114 (2009), DOI 10.1103/PhysRevB.80.165114.
   - Reynier: JES **151**, A422 (2004) 형태 유지, DOI 검증 후 기재.
   - Reimers: JES **139**, 2091 (1992), DOI 10.1149/1.2221184.
   - Ménétrier: JMC **9**, 1135 (1999), DOI 10.1039/a900016j.
3. **쟁점1(ΔS_e 부호)**: v9-06은 쟁점1 미명시(중립) → 체리픽 시 REVIEW_NOTES.md의 "v9-05 해결책(ξ=탈리튬화 진행률 고정·σ_d-라벨 매핑)" 채택 명시 필요.
4. **이중계산 B 명시**: v9-06에 이미 있음 — 유지.
5. **tier 표기**: 체리픽 결과물의 모든 수치에 tier(A/B/F/G) 병기 — v9-06이 가장 완결.
