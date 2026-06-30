# REVIEW — graphite_ica_ch2_v3.tex (검수 sub audit)

> 대상: `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch2_v3.tex` (5p draft, 7 sections + 서/맺음).
> 기준 정독: `22_ch1_vs_literature.md`·`30_synthesis_gap.md`·`10_sources_master.md`·`20_extraction/_SUMMARY.md`·전 추출카드(allart2018·reynier2003·msmr_partI/II·standardised2024·chemmater2015) + `Anode_Fit_v11_final.py`(GRAPHITE_STAGING_LIT·func_U_j).
> 역할: audit 전용(파일 수정·커밋 X — master 가 수정). refute mandate + 가장 약한 1곳 필수 지목. 빈/허위 통과 금지.

---

## 0. 종합 판정

| 렌즈 | 판정 |
|---|---|
| 1. 출처 폐쇄·tier 정직 | **PASS** (cite-closure 완전, 11/11 resolve; 과장단정 0; 날조 수치/식 0) |
| 2. 부호 사슬 | **PASS** (ΔS=+nF∂U/∂T·Q̇_rev=−IT∂U/∂T·∂U_j/∂T=ΔS_rxn,j/F — v11·조사 확정부호와 1:1, 숨은 flip 0) |
| 3. Ch1 정합 정확 | **PARTIAL** (헤드라인 +29·−16 정확; **tab:ds 중간 2행 region↔x 매핑 어긋남 — MEDIUM**) |
| 4. 무비약(G-derive) | **PASS** (eq:bernardi→qrev→coeff→qrev_sum 단계 유도, 미정의 기호 0) |
| 5. 갭 정직 | **PASS** (Electrochim.Acta 2019 식·히스 불확도·DFT 절대값 모두 "미확보/공백" 표기) |
| 6. 백지 확인 | **PASS** (old=히스 토픽 무관, rebuilt=동토픽이나 구조·라벨·AL원장 전혀 미유입) |
| 7. 형식·빌드 | **PASS** (xelatex 2-pass exit=0; undefined ref 0·LaTeX error 0; 폰트 italic 대체 경고만) |

**확정 결함: 2건** (MEDIUM 1 = tab:ds 중간행 region 매핑 / LOW 1 = 표 캡션 출처표기 강화 권고). **과장/날조 단정: 없음.** **부호 사슬: FAIL 없음(전건 PASS).**

---

## 1. 확정 결함 (심각도·행·틀림·옳은형)

### [MEDIUM] 결함 1 — tab:ds(L153–163) Allart region↔x 매핑이 한 행 어긋남
- **위치**: 표 `tab:ds` 행 `3→2L`(L158)·`2L→2`(L159).
- **틀림**: 문헌 ΔS(x) 열이 Allart 2018 의 **region 경계와 x-범위가 불일치**.
  - Allart(full-text, allart2018 카드 L14–16): **Region II = 0.25≤x≤0.5 → ΔS≈−15~0 (큰 히스)**; **Region I = x>0.5 → ΔS≈−5~−16**.
  - 그런데 draft 는 **−15~0(히스)** 를 `3→2L`(x=**0.16–0.25**) 행에, **−5~−16 하단** 을 `2L→2`(x=**0.25–0.50**) 행에 배치 → Allart Region II(0.25–0.5)값을 0.16–0.25 행에, Region I(x>0.5)값을 0.25–0.5 행에 얹음. **두 행 모두 문헌 region 의 x-경계와 한 칸씩 어긋남.**
- **근원**: 조사서 `22_ch1_vs_literature.md`(L9–10)가 이미 동일한 느슨한 매핑("3→2L … −15~0 @ reg II")을 했고 draft 가 충실히 복사 — 즉 **draft 가 조사를 왜곡한 게 아니라, 조사 자체의 region-경계 부정합을 그대로 승계**. 헤드라인 +29(reg IV)·−16(reg I)은 정확하므로 **SrcBox(L143) "정확 대응" 주장 자체는 유효**.
- **옳은형(권고)**: 문헌 ΔS(x) 열을 Allart region 경계에 맞춰 재정렬하거나, 각 행에 "(Allart reg IV/II/I)" 라벨을 달아 x-범위 불일치가 **Ch1 전이정의(plateau 기준) vs Allart region 정의(LiC24 staging)의 해상도 차이**임을 명시(이 차이는 `22_…` L30·allart카드 L21·44 에 이미 인지됨 — 표에 그 단서가 누락). 또는 중간 2행을 "Allart reg II(0.25–0.5): −15~0 / reg I(x>0.5): −5~−16" 로 묶어 x-범위 충돌 제거.

### [LOW] 결함 2 — tab:ds 문헌열·SrcBox 가 단일 출처(allart2018)만 표기
- **위치**: 표 캡션(L151)·SrcBox(L140–146).
- **틀림 아님(정밀도)**: 표는 Allart 만 인용하나, −5~−16@x>0.5 의 부호·정성 교차근거(reynier2003·msmr_partII)는 본문 L133·136 에 따로 있음. 결함은 아니나, 표 단독 판독 시 단일출처처럼 보임.
- **권고**: 표 각주에 "부호·정성 교차: reynier2003·msmr_partII" 1줄(선택).

---

## 2. 렌즈별 검증 근거 (PASS 항목의 실증)

**[렌즈1 출처·tier]**
- cite-closure: 사용 11키(bernardi1985·standardised2024·newman·msmr_partI·reynier2003·allart2018·msmr_partII·chemmater2015·hysteresis2018·occupation2019·jpcc2021) **전부 bibitem 존재** → orphan/undefined 0.
- tier 정직: ΔH calorimetry(L166–167 −13.9/−24.8 kJ/mol)는 bibitem 에 `[abstract tier]` 명기(chemmater2015 카드 일치). occupation2019(L204·250)는 "모델 식 원문 미확보 — 방법 수준만 인용" 정직 표기(_SUMMARY L18·30_synthesis L27 갭과 일치). jpcc2021·chemmater2015 `[abstract tier]` 라벨. **abstract-only 를 원문확인처럼 과장한 곳 없음.**
- 날조 0: 모든 정량(+29·−16·+3~4 mV/K·0.3–0.5 mV/K·std 3.13µV/K·−13.9/−24.8 kJ/mol)이 추출카드에 실존. **조사에 없는 수치/식 발견 못 함.**

**[렌즈2 부호 사슬] — FAIL 없음**
- ΔG=−nFU_oc → ΔS=+nF·∂U/∂T (L86–88) = MSMR Part I Eq.27 + Newman + 조사 확정부호(+). SrcBox(L88–90)가 −부호 문헌표기를 "셀전압 정의 차이"로 정확히 해소(_SUMMARY L32 폐기권고와 동일 논리).
- Q̇_rev=−I·T·∂U/∂T (eq:qrev L78) = Bernardi 형태 일치.
- ∂U_j/∂T=ΔS_rxn,j/F (eq:coeff L102): v11 `func_U_j=(-dH_rxn+T·dS_rxn)/F` 의 ∂/∂T = dS_rxn/F. **코드와 1:1.** 숨은 flip 0.

**[렌즈3 Ch1 정합] — 수치 실증(코드 직접 계산)**
- v11 GRAPHITE_STAGING_LIT: 4→3 dS=+29.0 / 3→2L 0.0 / 2L→2 −5.0 / 2→1 −16.0 — **draft 표 Ch1 열과 정확 일치**.
- U(298) round-trip(F=96485): 0.2109/0.1399/0.1203/0.0853 V = target 0.210/0.140/0.120/0.085 **일치**.
- 내부일관 검산(L168–170): 2→1 `−FU+FT∂U/∂T = −8.23+(−4.77) = −13.00 kJ/mol` = dH_rxn −13000 **정확**(draft "−13.0, 표값과 일치" 옳음).
- ΔH 기준상이 경고(L165–170): 형성(cumulative, graphite+Li금속) vs 전이별(differential) 직접등치 금지·환산 필요 — `22_…` L19·_SUMMARY 와 동일, **등치 안 함**(우연 LiC6 −13.9≈Ch1 −13.0 을 정합주장 안 함). 옳음.

**[렌즈4 무비약]** eq:bernardi(L72) → 항분리 → eq:qrev(L78) → eq:coeff(L102, U_j(T) 미분) → eq:qrev_sum(L109–113, 용량가중합 ΔS̄) 단계 연결. g_j(x)=ξ_eq(1−ξ_eq) 종모양은 v11 L370·468 `ksi_eq*(1-ksi_eq)/w` 와 일치 — **미정의 기호·도약 없음.**

**[렌즈5 갭 정직]** L185(히스 경로의존 불확도 "미확보=공백")·L204·L230–232(Electrochim.Acta 2019 식 "유료·미확보"·DFT 절대값 "실험 우선"·형성↔전이별 환산식 "범위 밖") — 30_synthesis_gap §4 공백목록과 일치. **있는 척 0.**

**[렌즈6 백지]**
- `old/graphite_ica_ch2.tex` = "흑연 음극의 충방전 히스테리시스"(spinodal·gap·memory) — **토픽 무관**, 유입 불가.
- `Archive_rebuilt/…rebuilt.tex` = 동토픽(Bernardi·q_rev)이나 16+ 섹션·AL-20~29 가정원장·candidate relaxation-heat 확장항·`s^conv|I|`·`\dd Q/\dd V` 표기. **v3 는 7섹션·AL원장 없음·candidate항 없음·`\dot Q_\rev`·`dQ/dV` 표기** — 섹션구조·라벨·기호체계 전혀 다름. 공유된 건 Ch1+문헌이 강제하는 물리(2항 balance·∂U/∂T=ΔS/F)뿐. **텍스트 유입 흔적 없음.**

**[렌즈7 빌드]** scratchpad 복제본 xelatex 2-pass 모두 exit=0. 로그: undefined ref 0·LaTeX error 0·overfull 비차단. 경고는 한글/D2Coding italic 폰트셰이프 대체 + 제목 한글 PDF-string Unicode(무해)만.

---

## 3. 가장 약한 3곳 (refute — 빈 통과 금지)

1. **★가장 약함 — tab:ds 중간 2행 region↔x 매핑 어긋남(MEDIUM, 결함1).** Allart Region II(0.25–0.5)·Region I(x>0.5)를 draft 가 0.16–0.25 / 0.25–0.5 행에 한 칸씩 밀려 배치. 헤드라인 +29·−16 은 정확하나 중간 region 의 x-경계 정합이 깨짐. 조사서(`22_…` L9–10)가 동일 매핑을 했어 draft 단독 과실은 아니지만, **표가 "정량 일치"를 주장하는 바로 그 칸에서 region 경계가 안 맞음** = 검토자가 Allart 원표와 대조하면 가장 먼저 걸리는 지점.

2. **eq:qrev_sum 의 g_j(x) "국소 가중"의 물리적 정당성(약하나 결함 아님).** L115 가 g_j 를 ξ_eq(1−ξ_eq)로 동일시하고 "전이 진행 SOC 에서 그 ΔS 가 지배"라 함. ξ_eq(1−ξ_eq)는 dQ/dV **peak shape**(전류응답)이지 평형 **용량분율 ∂x_j/∂x** 와 엄밀히 같지 않음 — 가역발열의 용량가중은 후자가 더 정확. 초안 수준 근사로는 수용 가능하나, "용량 가중 합"의 가중치 정의를 peak-shape 로 둔 것은 후속 정밀화 대상(현재 미정의 도약은 아님).

3. **standardised2024 의 full-cell 값을 graphite 전이 신호 옆에 인용(L199–201·L226–227).** 0.3–0.5 mV/K·std 3.13µV/K 는 **full NMC/graphite-SiO_y 셀**값(standardised 카드 L14·39 Decision-queue: graphite 전극 귀속 한계). draft L200 가 "full-cell" 을 명시해 **과장은 아님**(tier 정직). 다만 L226 "calorimetry 가역 흡열 직접관측과 정합"은 standardised2024(potentiometric protocol)가 아니라 arXiv 2107.00625(calorimetry)가 출처여야 더 정확 — 현재 cite 가 standardised2024 로만 닫혀 미세 출처-매칭 헐거움(LOW 미만, 권고).

---

## 4. 수정 권고 (master 작업용 — 우선순위)

1. **(MEDIUM, 필수)** tab:ds 중간 2행: Allart region 라벨 부착 또는 region 경계로 재정렬. 예—문헌열을 `(reg II 0.25–0.5) −15~0` / `(reg I x>0.5) −5~−16` 로 적고, Ch1 전이 x-범위와의 차이를 표 각주 1줄로 "Ch1 plateau 정의 vs Allart LiC24 staging region 해상도 차이(본문 §2.4·`22_…` 인지)"라 명시. (헤드라인 +29·−16 정확성은 유지되므로 SrcBox 본문은 그대로 둬도 됨.)
2. **(LOW, 선택)** L226 calorimetry 가역흡열 정합 문장에 arXiv 2107.00625(또는 해당 calorimetry 카드) cite 추가 — standardised2024 단독 인용보다 출처-주장 정합.
3. **(LOW, 선택)** tab:ds 캡션/각주에 부호·정성 교차출처(reynier2003·msmr_partII) 1줄.
4. **(NOTE)** eq:qrev_sum g_j(x) 의 가중치 정의(peak-shape vs 용량분율)는 후속 실데이터 단계 정밀화 항목으로 §2.6 한계에 1줄 추가 고려(현재도 결함 아님).

---

## 5. 결론

초안은 **출처 폐쇄·부호 사슬·갭 정직·백지·빌드** 5개 핵심 렌즈에서 **PASS**이며 **과장·날조 단정이 없다**(미검증을 확정처럼 둔 곳 0, 조사에 없는 수치/식 0). 부호 사슬(ΔS=+nF∂U/∂T·Q̇_rev=−IT∂U/∂T·∂U_j/∂T=ΔS/F)은 v11 코드·조사 확정부호와 **전건 1:1**로 FAIL 없음. **유일한 실질 결함은 tab:ds 중간 2행의 Allart region↔x 매핑 어긋남(MEDIUM)** — 헤드라인 정합(+29·−16)은 정확하나 중간 region 의 x-경계가 한 칸 밀렸고, 이는 조사서의 동일 매핑을 승계한 것. master 가 표에 region 라벨/각주만 보강하면 해소된다.
