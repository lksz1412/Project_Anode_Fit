# V1 — 부호 일관 + 회귀 검증 + 체리픽 base/graft 확정 (검토2, 검수 sub)

> 역할: 검토 의견만(파일 수정 X). 기준 = ★확정 `ΔS_e ≡ +∂S_e/∂x|_T < 0`(삽입 기준, `CHERRYPICK_PLAN.md` L5-10).
> 검증 방식: 9종 전부 full-read(병렬 검수 sub + master 직접 v9-02/03·인용 대조). refute-first·빈 통과 금지.
> Ground truth: `CHERRYPICK_PLAN.md`·`research/CH1v9_LCO/35_electronic_entropy_design.md`·`base_v8-11.tex`·`review1/R2_sign_convention.md`.

---

## (a) ★ 9종 부호 일관 PASS/FAIL 표 (9b 보완 후)

| 초안 | 명시 규약문 | box `+∂S_e/∂x` | prose ΔS_e<0 | 게이트식 `−(π²/3)…σ'/Δx` | 분해식/code plug-in | +0.83 agnostic | 빌드 | **부호 판정** |
|---|---|---|---|---|---|---|---|---|
| **v9-01** | ✓ L838(삽입 −16 anchor) | ✓ L840 | ✓ L845/864 | ✓ leading − L861 | ✓ L446/1316 | ✓ L846 | 0err/4ovf | **FAIL (1건)** — 그림 캡션 L918 "양봉우리"(positive)가 본문 L864 "음봉우리"·box<0 와 모순. + TikZ 라벨 L902 동일 conflation(MED). 한 단어 캡션 수정이면 PASS. |
| **v9-02** | ✓ L966-969·L977·L1482(R2 확정 명시) | ✓ L971 `<0` 박스 내 명기 | ✓ L978 | ✓ L1009 `−σ'/Δx` | ✓ L1327·L1485 | ✓ L982 | 0err/4ovf | **PASS** — 가장 투명(falsifiable 부호 회귀 self-test verifybox L1493+). |
| **v9-03** | ✓ L948-952("코드 관행=삽입 규약" 명시 호명) | ✓ L944 | ✓ L949-950 | ✓ L978 leading − | ✓ L997-1011·L1430(1_{j=T1}) | ✓ L953/982 | 0err/5ovf | **PASS** — 물리 서술(−∂S_e/∂x>0)과 코드 부호(<0) 명시 분리, 9종 가른 혼동 정면 해소. R3 D1 자기모순(config prose)도 제거됨(L1006-1008). |
| **v9-04** | ✓ L990-997("부호 뒤집기 없음·슬롯 자체 삽입") | ✓ form L979/985 | ✓ L468/1459 | ✓ leading − L985-988(eq:dSegate) | ✓ L1441·plug-in box <0 | ✓ L1001/1610 | 0err/6ovf | **PASS** — pre-9b code-input 플립 진짜 수정. Δμ=+sF(V−U) 보존(L412/843), 단위다리(RT=N_A k_B) 보존. |
| **v9-05** | ✓ L904 박스 내 `<0(삽입 기준)`·L949 molar<0 | ✓ L903 | ✓ L908-913 | ✓ leading − L932 | ✓ L1372-1387 molar | ✓ L914-915/450 | 0err/6ovf | **PASS** — pre-9b box↔prose 모순 수정("+0.18 방출"을 같은 양의 역방향 표기로 명시 frame L911-913). σ_d 매핑틀 byte-불변 보존. |
| **v9-06** | ✓ L922-923·L930-932(2→1 −16 일관) | ✓ L927 box `<0` | ✓ L932-937 | ✓ ∂g/∂x<0 via eq:dSe∘eq:ggate(합성, leading − L951-952) | ✓ L1371·L1383-1384 | ✓ L457-468 | 0err/5ovf | **PASS** — 전 위치 삽입<0, removal>0 은 magnitude로만 분리. MIT 4항 게이트·∝T²·단/전셀 분리 보존. (게이트 음의 닫힌식이 합성형이라 한 줄 signed 식 미인쇄 — substantive 정확, nit.) |
| **v9-07** | ✓ L847·L851 박스 `ΔS_e^ins=∂S_e/∂x<0` | ✓ L843-844 | ✓ L848-851 | ✓ leading − L868-872 | ✓ L1272-1276(double-count rule L1278) | ✓ L1405-1407 | 0err/4ovf | **PASS-with-residual (MED)** — ΔS_e<0 deferral 은 수정(L851)했으나 `∂U^cat/∂T|_e<0` 을 명시 부등식으로 안 적음(L837-838 `=ΔS_e/F∝T` 만) → G-usable 미흡(독자 합성 필요). brief 요구 미충족. |
| **v9-08** | ✓ L838·L847 박스 `ΔS_e^ins(x,T)<0(삽입 기준)` | ✓ L841-842 | ✓ L845 | ✓ leading − L877-881 | ✓ L1280-1284·plug-in note L1289 | ✓ L430-434(신규 추가) | 0err/4ovf | **PASS** — pre-9b ζ=1−x removal 플립 수정. ζ-좌표는 별식(eq:dSedzeta L852)으로 격리·"삽입 plug-in 에선 뒤집어 넣음" 다리(L857). +0.83 sanity 결여(유일 갭)도 보완됨. (LOW: eq:gxicathode L588 `+` 누락 LaTeX 오타, 부호 무관.) |
| **v9-09** | ✓ L843-845 박스 `삽입 기준 ΔS_e=∂S_e/∂x<0` | ✓ L837-839 | ✓ L841-844 | ✓ leading − L868-872 | ✓ L903-912(double-count) | ✓ L431-432/856 | 0err/4ovf | **PASS** — pre-9b HIGH 플립("Li 제거 +기여") 완전 제거. removal +0.18 gain 은 역기준 note 로 분리하고 "삽입 슬롯과 일관 음의 기여로 기록"(L849-850). 하프/전셀 분리(L275-277) 보존. |

**전수 스캔 교차검증**: 9종 모두 위험구문(`제거당 양수`/`Li 제거 방향 전자…+기여`/`removal-positive`) **0건**(grep). HIGH 5건(v9-01/04/06/08/09 역부호 투입) + v9-05 box↔prose 모순 = **9b 보완으로 전부 해소**. v9-02/03(원래 정확)은 회귀 없음.

---

## (b) 회귀 결함표 (9b 보완 유입)

| 초안 | 결함 | 심각도 | 정정 |
|---|---|---|---|
| **v9-01** | fig:elec_entropy 캡션 L918 "국소 **양봉우리**"(positive peak) ↔ 본문 L864 "음봉우리"·box ΔS_e<0 모순 | **MED** | "양봉우리"→"음봉우리" 또는 "\|ΔS_e\| 봉우리"(L864 와 일치). 부호 정정하다 캡션 한 단어 누락. |
| **v9-01** | TikZ 라벨 L902 `ΔS_e(x,T)∝T (MIT peak)` 을 양의 종으로 라벨(signed 기호에 magnitude 곡선) | LOW | `\|ΔS_e\|` 로 표기하거나 라벨 명시. |
| **v9-07** | `∂U^cat/∂T\|_e<0` 명시 부등식 부재(ΔS_e<0 만 적고 U-계수 부호는 독자 합성에 위임) | **MED** | 본문에 `∂U^cat/∂T\|_e=ΔS_e/F<0` 한 줄 추가(brief 요구). |
| **v9-08** | eq:gxicathode L588 config log항과 Ω항 사이 `+` 누락(LaTeX 렌더 글리치) | LOW | `+` 추가. ΔS_e/MIT/Sommerfeld/plug-in 부호와 무관. |
| (회귀 無 확인) | v9-02/03/04/05/06/09: Sommerfeld식·게이트 leading −·분해 박스·Δμ=+sF·단위다리·σ_d 매핑·하프/전셀 분리·**흑연 verbatim(GRAPHITE_STAGING_LIT +29/0/−5/−16, eq:Uj, S1-S8 self-test) 전부 unbroken** | — | 정정 불요. |

> 빈 통과 금지 증거: 흑연 stage 2→1 ΔS=−16·U=0.0853 round-trip·6종 게이트식 leading − 직접 대조·9종 위험구문 grep 0·v9-01 캡션/v9-07 부등식/v9-08 오타는 적극 적발(rubber-stamp 아님).

### ★별도 발견 — 인용 정확성(부호 외, but 체리픽 차단 사유)
| 초안 | LCO 인용 상태 | 판정 |
|---|---|---|
| **v9-05** | bibitem 전건 = CHERRYPICK 인용 마스터 정합: Reimers&Dahn(10.1149/1.2221184)·Ménétrier&Delmas·Xia/Lu/Meng/Ceder(10.1149/1.2509021)·Motohashi PRB80 165114·Reynier PRB70·**Świderska-Mocek PCCP21(+0.83)**·**Teichert et al.(저자 정확, Aronson 없음)**·MSMR ECS Adv3 | ★**정확(graft 원천)** |
| **v9-03** | L1551 `ml2024 = R. Aronson et al.` = **fabrication**(CHERRYPICK L41 폐기 지정) | **CRIT(인용)** — 본체 채택 시 bibitem 전면 교체 필수 |
| **v9-04** | bibitem 0건(\cite dangling, reynier 엉뚱 논문은 pre-9b) | HIGH(인용) |
| **v9-06** | ml2024 "K. Garikipati group"(익명·불완전), LCO bibitem 부실 | MED(인용) |
| **v9-02** | +0.83 = `wang2009`(미검증, 정답=Świderska-Mocek) | MED(인용) |

---

## (c) ★ 최종 체리픽 base 1개 + 차원별 graft map

**★ best-base = v9-06** (검토1 R5 와 일치, 검토2 재확인).
- 사유: 부호 **PASS**(전 위치 삽입<0·removal magnitude 분리) + 흐름 최선(일반→흑연→LCO, C_e→S_e→부분몰 순서, MIT 게이트 자기일관성) + 단전극↔전셀 분리 최상(L457-468) + ∝T²·4항 게이트 정당화 + 빌드 0err. 9종 중 종합 1위.
- base 의 한 nit: 게이트 음의 닫힌식이 합성형(eq:dSe∘eq:ggate) → graft 시 v9-04 한 줄 signed 식으로 보강.

**차원별 graft map (base=v9-06 골격에 이식):**

| 차원 | graft 원천 | 근거 |
|---|---|---|
| **전자 엔트로피 절(부호 규약문)** | **v9-03 L948-952** (또는 v9-02 L1482) | "코드 관행=삽입 규약" 명시 호명 + 물리/코드 부호 명시 분리 = 9종 가른 혼동 정면 해소. base v9-06 도 규약문 보유하나 v9-03 가 가장 명료. |
| **유도 rigor + 단위 다리 + 게이트 닫힌식** | **v9-04** | 완전 Fermi 적분 π²/12→π²/3 명시·eq:dSemolar 단위다리(자리당 k_B→몰당 R N_A, 9종 단독)·eq:dSegate 한 줄 leading − signed 식. base 의 합성형 게이트식 보강. Δμ=+sF(V−U) 도 검증됨. |
| **분포 5단(Z→⟨n⟩→ξ_eq)·3-view box** | **v9-04** (R3 강추) | 단일자리 Z=1+e^{−βΔμ}→Fermi→ξ_eq 5단·Ω=0 극한·전자 Fermi–Dirac 다리. base v9-06 의 §5.4 분포 다리와 정합(게이트 functional form 재사용). |
| **ΔS_rxn^cat decomp(이중계산 B)** | **v9-03 L997-1011** | config 슬롯 prose 가 ΔS_j^0=중심 표준값 한정(R3 D1 자기모순 제거됨)·vib/전자 별 슬롯 명시. v9-05 의 `ΔS^{config,0}` 라벨도 참고. |
| **전이표(T1-T3)** | 9/9 GT 일치 — base v9-06 표 유지 | R3: 전이표 9종 GT 일치. v9-03 만 T3 상한 4.20 미표기 LOW(무관). |
| **σ_d 셀-라벨 매핑(forward 사슬 불변)** | **v9-05 L277-286** | ξ=탈리튬화 진행률 고정·`_direction_to_sigma` 한 곳 흡수·eq 전 사슬 byte-불변·회귀 위험 0. base 양극 처리에 이식. |
| **단전극↔전셀 분리** | base v9-06 L457-468 유지(+v9-09 L275-277 보강) | 둘 다 최선례. v9-09 의 명시 `∂U_cell=∂U_cat−∂U_an` 범위밖 선언 추가 가능. |
| **★LCO 참고문헌 전체** | **v9-05 bibliography L1556-1572** | ★유일 완전·검증·fabrication 0. base v9-06 의 익명/부실 bibitem 폐기, v9-05 set 통째 이식. (v9-03 Aronson·v9-04 dangling 절대 채택 금지.) |
| **부호 회귀 self-test(falsifiable)** | **v9-02 verifybox L1493+** | 수치 못박은 부호 회귀 가드 — 조립본에 이식 시 향후 회귀 차단. |

**이식 금지 리스트(명문)**: v9-03 bibitem(Aronson fabrication)·v9-04 bibitem(dangling)·v9-06 익명 ml2024·v9-03 config prose 의 구 "전체 반응 엔트로피 중심값" 재정의(이미 제거됐으나 구판 혼입 주의)·v9-01 캡션 "양봉우리".

**조립 후 필수 gate**: ① ΔS_e=∂S_e/∂x<0 전 위치(box·prose·캡션·게이트식·decomp·plug-in·nodemap) 통일 재확인 ② removal>0 은 magnitude/물리서술로만, 명시 분리문 1개 ③ `∂U^cat/∂T|_e<0` 명시(v9-07 결함 회피) ④ 인용 8건 추출카드 대조 ⑤ 이중계산 B ⑥ xelatex 0-error ⑦ v9-02 self-test 이식.

---

## (d) 빈 통과 금지 — 검수 정직

- **PASS 7종(v9-02/03/04/05/06/08/09)은 적극 확인**: 6종 게이트식 leading − 직접 대조·흑연 verbatim 표·Δμ·단위다리·σ_d·하프셀 분리 항목별 검산. rubber-stamp 아님.
- **FAIL/residual 2종 적발**: v9-01(캡션 L918 모순, MED) + v9-07(`∂U^cat/∂T|_e<0` 부등식 부재, MED) — 둘 다 brief 요구 대비 구체 결함.
- **base 후보의 인용 결함도 차단**: v9-03(Aronson CRIT)·v9-04(dangling)·v9-06(익명)는 부호 PASS여도 인용으로 graft 제한 → v9-05 bibliography 통째 이식이 유일 안전.
- HIGH 5건+box모순 1건이 9b로 해소됨을 9종 full-read 로 확인(누락 0 주장은 전수 스캔+병렬 절별 검수로 backing).
