# V1.0.14 Ch.1 문헌 출처 서치 결과 — 전이 초기값 F-G 근거

대상 문건: `docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex` (표 tab:staging·tab:lco-staging·tab:inputs, §broadening (c)(i), §lco-gate)
서치 기준 시점: 2026-07-04 (WebSearch 실시간 조회). **파일 수정 없음 — 본 보고서만 신규 작성.**
신뢰 등급: tier A = 1차 문헌의 정량 확정값(스테이지·수치 직접 일치) · tier B = 동종 계 대표/스케일 anchor(정밀값 아님) · tier C = 추정·스케일 근거(자릿수 정합 정도) · [근거 미발견] = 실검색으로 확정 못함(추정 문헌 임의 부착 안 함).

---

## 1. 흑연 staging 전이 평형 전위 U (표 tab:staging 4건)

| 값 | 현행 인용 유무 | 후보 문헌(서지+DOI) | 정합 근거 | tier | 비고 |
|---|---|---|---|---|---|
| $4\to3$: $U{=}0.210$ V | 서론(L135)에 `\cite{dahn1991,ohzuku1993}` 포괄 인용만, **표 행 단위로는 미특정** | J. R. Dahn, *Phys. Rev. B* **44**, 9170 (1991). DOI: 10.1103/PhysRevB.44.9170 | Dahn 1991 은 dilute→stage4 전이(x≈0.08–0.17 영역)를 **210 mV** 로 보고(검색 요약 확인) — 표의 0.210 V 와 자리수까지 일치 | **B** (2차 출처 통한 확인 — 원문 PDF 직접 대조 못함, 아래 caveat) | Dahn 원논문은 "stage4↔3 전이만 유일하게 뚜렷한 2상 공존이 안 보인다"(연속) 는 점도 보고 — 이는 본 문건 §broadening(a)의 "4→3·3→2L = solid-solution" 서술과 **정합**(문건 내부 논리와 1차 문헌이 서로 지지) |
| $3\to2\mathrm L$: $U{=}0.140$ V | 상동(포괄) | T. Ohzuku, Y. Iwakoshi, K. Sawai, *J. Electrochem. Soc.* **140**, 2490 (1993). DOI: 10.1149/1.2220849 | Ohzuku 1993 dQ/dV 6-peak 분해에서 stage3→2L 전이 **≈0.125 V** (2차 출처 인용) | **C** (스케일 정합, 15 mV 차 — 표의 0.140 V 는 원문 정밀값이 아니라 근사 anchor) | 원문 직접 fetch 시도했으나 PDF 텍스트 추출 실패(binary) — 2차 리뷰가 인용한 수치로만 확인 |
| $2\mathrm L\to2$: $U{=}0.120$ V | 상동(포괄) | 상동(Ohzuku 1993) | Ohzuku 6-peak 분해에서 stage2L→2 전이 **≈0.12 V** — 표값과 **정확 일치** | **A** (2차 출처 통한 확인, 자리수 일치) | 상동 caveat |
| $2\to1$: $U{=}0.085$ V | 상동(포괄) | Dahn 1991 (상동) | Dahn 1991 이 stage2→1 전이를 **85 mV** 로 직접 보고(검색 요약) — 표값과 정확 일치 | **A** (2차 출처 통한 확인) | Ohzuku 는 같은 전이를 0.07 V 로 보고(문헌 간 5–15 mV 편차 — 정상적 시료·조건 의존) |

**caveat(중요):** Dahn(1991)·Ohzuku(1993) 원문 PDF(및 IOPscience 페이지)를 직접 fetch 시도했으나 스캔/압축 PDF 라 텍스트 추출이 실패했다(도구 한계). 위 tier 는 **2차 출처(리뷰 논문·후속 인용 논문)가 인용한 수치**를 근거로 매겼다 — 원문 Figure/Table 번호까지 직접 대조하지는 못했다(따라서 tier A 항목도 "2차 확인" 단서를 붙였다). 원문 access 가 가능해지면 재검증 권고.

---

## 2. 흑연 ΔH_rxn·ΔS_rxn 스케일 (표 tab:staging)

| 값 | 현행 인용 유무 | 후보 문헌 | 정합 근거 | tier | 비고 |
|---|---|---|---|---|---|
| stage $2\to1$: $\Delta S_\rxn=-16$ J/(mol K) | **미인용** — 본문 L2449 는 "$U(298)\approx0.085$ V 를 round-trip 으로 맞추는 슬롯"이라고만 서술, 문헌 인용 없음 | Y. Reynier, R. Yazami, B. Fultz, "The entropy and enthalpy of lithium intercalation into graphite," *J. Power Sources* **119–121**, 850–855 (2003). DOI: 10.1016/S0378-7753(03)00285-4 | 이 논문이 **흑연**(LixCoO2 아님) Li 삽입 엔트로피·엔탈피를 조성 전역에서 직접 측정 — 부호 반전(저 x 는 mixing 성분, 고 x 는 vibrational 성분 우세)과 스케일(수십 J/(mol K) order)이 표의 $-16$ J/(mol K) 와 자릿수 정합 | **B** (스케일 anchor — 전이별 정밀값 아님, 조성 연속함수로 보고돼 특정 stage 경계값과 1:1 대조 안 됨) | **★현재 미인용 문헌 — 신규 bibitem 추가 권고.** 주의: 이 논문은 현재 bibitem `reynier2004`(LixCoO2 용, Phys Rev B 70)와 **저자 겹치나 다른 논문**이다 — 혼동 금지 |
| $\Delta H_\rxn\approx-11700\sim-13500$ J/mol (4건) | 미인용(각주 없음, "$U(298)$ 정합" 서술만) | 상동(Reynier·Yazami·Fultz 2003) | 같은 논문이 "삽입 엔탈피는 항상 음(발열), x 증가에 따라 덜 음"이라고 보고 — 부호·완만한 감소 추세는 정합 | **C** (부호·정성 추세만, 전이별 정량 anchor 아님) | 표의 $\Delta H_\rxn$ 는 $U(298)$ round-trip 역산값이라 원래도 "출발점" 성격 — 위 문헌은 그 스케일이 물리적으로 타당함을 보이는 데 그침 |

---

## 3. Ω>2RT 상분리 문턱 · ΔH_a 활성화 엔탈피 스케일

| 값 | 현행 인용 유무 | 후보 문헌 | 정합 근거 | tier | 비고 |
|---|---|---|---|---|---|
| $\Omega>2RT$ 문턱 자체(식 eq:sm-thresh) | 인용 대상 아님 | — | 이 문턱은 **문헌값이 아니라 문건 내부 유도 결과**다 — Part 0(§sm-mf)의 정규용액 평균장 자유에너지 $g_j''(\xi)$ 이계미분에서 대수적으로 나오는 항등식(Bragg–Williams 표준 결과, 교과서 수준)이라 특정 논문 인용 대상이 아니다 | 해당없음 | 서치 불필요 항목 — 잘못된 기대(task 배경)로 보임, 명확히 함 |
| $\Omega_j=6000$–$13000$ J/mol (전이별 값) | 미인용, "정규용액 추정"(L1950)만 | — | 이 값들 자체는 데이터 피팅 출발점(사용자 override 전제)이라 문헌 anchor 를 요구하지 않는 유형 — 굳이 찾자면 흑연 staging Ω 는 Dahn 1991 phase diagram 의 $T_c=\Omega/2R$ 로부터 역산 가능(stage2↔1 임계온도 관련 문헌) | **C**(간접) | [근거 미발견 — 전이별 특정 논문 anchor는 확정 못함, 상기 Dahn(1991)의 phase diagram 이 정성적 근거가 될 수 있다는 정도] |
| $\Delta H_a=40000$–$48000$ J/mol ("DFT 활성화 경향", 저SOC→만충 감소) | 미인용(L1949 "DFT 활성화 경향"만, `\cite` 없음) | 후보1: K. Persson, V. A. Sethuraman, L. J. Hardwick, Y. Hinuma, Y. S. Meng, A. Van der Ven, B. Kerlau, G. Ceder, "Thermodynamic and kinetic properties of the Li-graphite system from first-principles calculations," *Phys. Rev. B* **82**, 125416 (2010). DOI: 10.1103/PhysRevB.82.125416 | DFT NEB 로 stage I/II Li 이동 장벽 계산(수백 meV order, 조성 의존 감소 경향 보고) — "저 SOC→만충 감소" 정성 경향과 DFT 방법론이 정합, 수치 자릿수(meV→kJ/mol 환산 시 약 20–50 kJ/mol)도 표의 40–48 kJ/mol 과 근접 | **B/C** (방법론·정성 경향 일치, 표의 전이별 정확 수치와 1:1 대조는 원문 직접 확인 필요) | 검색으로 정확 meV 수치 인용문은 확보 못함(원문 fetch 실패) — 후보 제시이며 **확정 아님** |
| (대안 후보 — 실험 활성화에너지) | — | AC impedance 계 여러 문헌: 흑연 계면 전하이동 활성화에너지 $\approx$25–59 kJ/mol (전해질 조성 의존, 예 Yamada 등 *J. Electrochem. Soc.* 계열) | 실험(비 DFT) 이라 "DFT 활성화 경향" 서술과는 방법론이 다르나, **수치 스케일**은 표의 40–48 kJ/mol 범위와 잘 겹침 | **C**(스케일만, 특정 단일 논문 DOI 미확정) | [근거 미발견 — 서치에서 특정 단일 논문·DOI 확정 못함, 리뷰성 요약만 확보] |

---

## 4. LCO 3전이 anchor (표 tab:lco-staging)

| 값 | 현행 인용 유무 | 후보 문헌 | 정합 근거 | tier | 비고 |
|---|---|---|---|---|---|
| T1 (MIT) $x\approx0.75$–$0.94$, $U\sim3.90$ V | **이미 인용**(각주 L2545 `\cite{menetrier1999,reimers1992}`) | M. Ménétrier *et al.*, *J. Mater. Chem.* **9**, 1135 (1999). DOI: 10.1039/a900016j | 검색 확인: "LixCoO2 undergoes insulator-metal transition near x=0.94... electron localization around x=0.75... two-phase region ≈0.75–0.94" — 표의 "$x$ 범위 0.94–0.75" 와 **정확 일치** | **A** (정확 일치, 이미 올바르게 인용됨) | 확정 사항 — 재검토 불필요 |
| T2 (order–disorder a) $U\sim4.05$ V, $x\approx0.55$ | 인용 없음(표에 각주 없이 수치만) — 상위 절에서 Reimers 1992 포괄 인용은 있음 | J. N. Reimers, J. R. Dahn, *J. Electrochem. Soc.* **139**, 2091 (1992). DOI: 10.1149/1.2221184 | 검색 확인: order/disorder 전이 쌍이 "x=1/2 위아래"에 위치, 2차 출처가 "minor peaks at 4.1 V and 4.2 V" 로 인용 — 표의 T2(4.05)·T3(4.17–4.20) 범위와 **스케일 정합**(±50 mV 편차) | **B** | 원문 직접 fetch 는 IOPscience 페이지 초록만 확보(본문 수치 표 미확인) — 재확인 시 원문 Table/Figure 대조 권고 |
| T3 (order–disorder b) $U\sim4.17$–$4.20$ V, $x\approx0.48$ | 상동 | 상동(Reimers·Dahn 1992) | 상동 | **B** | 상동 |
| (T4, 범위 밖) $U\sim4.55$ V, O3→H1-3 | 이미 인용(`\cite{xia2007}`, L1997) | H. Xia, L. Lu, Y. S. Meng, G. Ceder, *J. Electrochem. Soc.* **154**(4), A337 (2007). DOI: 10.1149/1.2509021 | 검색 확인: Xia 2007 은 O3→H1-3 전이를 4.5–4.9 V 충전 범위에서 관측, "two voltage plateaus at about 4.55 and 4.62 V" 보고 — 표의 "$\sim4.55$ V" 와 **정확 일치** | **A**(이미 올바르게 인용됨) | 확정 사항 |
| ★시연값 $U=3.930/3.880/4.050$ V(코드 초기값) | 문건 자체가 "물리 anchor 와 별개, tier-C 시연값"으로 이미 명시(각주 L2011-2016) | — | 해당 없음 — 문건이 이미 자기-플래그 처리(round-trip 피팅으로 override 전제) | 해당없음(이미 확정 처리) | 서치 대상 아님 — 이미 4-tier 분류 완료된 사안, 재논의 불필요 |

---

## 5. MIT 게이트 초기값 $g_{\max}$·$x_\mathrm{MIT}$·$\Delta x_\mathrm{MIT}$

| 값 | 현행 인용 유무 | 후보 문헌 | 정합 근거 | tier | 비고 |
|---|---|---|---|---|---|
| $g_{\max}=13$ e/eV/atom | **이미 인용**(`\cite{motohashi2009}`, L2543 "tier A 단일점"으로 문건이 이미 주장) | T. Motohashi *et al.*, *Phys. Rev. B* **80**, 165114 (2009). DOI: 10.1103/PhysRevB.80.165114; arXiv:0909.3556 | 논문 존재·주제(LixCoO2 전자구조·CoO2 금속상 고 DOS)는 확인. **그러나 "13" 이라는 정확한 수치는 arXiv 초록·PDF 텍스트 추출로 직접 대조하지 못함**(PDF 파싱 실패 2회) | **[근거 미발견 — 수치 직접 대조 불가]** | 문건의 tier A 주장 자체를 반박하는 것은 아니나(논문은 실재·주제 부합), **독립 재확인은 실패**했음을 정직히 보고. 원문 직접 열람(도서관·기관 access) 시 재확인 필요 |
| $x_\mathrm{MIT}\approx0.85$ | 이미 인용(`\cite{menetrier1999,reimers1992}`, L2545) | Ménétrier 1999 (상동) | 검색 확인: MIT 2상역 $x\approx0.75$–$0.94$, 중앙 $\approx0.85$ — **정확 일치** | **A** | 확정 사항 |
| $\Delta x_\mathrm{MIT}\approx0.05$ | 문건이 이미 "2상역 폭(≈0.19)을 logistic ±2Δx 유효폭(≈0.2)에 맞춘 모델 가정"이라고 명시(L2547) | 상동(Menetrier/Reimers 범위에서 유도) | 독립 문헌 anchor 가 아니라 **위 x-범위에서 파생된 모델링 선택**임을 문건 스스로 밝힘 | **C**(문건 자기서술과 일치, 추가 문헌 불요) | 서치 결과도 이 판단을 지지 — 별도 신규 인용 불필요 |

---

## 6. Gibbs–Thomson 배제 논증 상수 (§broadening (c)(i))

| 값 | 현행 인용 유무 | 후보 문헌 | 정합 근거 | tier | 비고 |
|---|---|---|---|---|---|
| $\gamma\sim0.1$–$1$ J/m$^2$ (계면 에너지) | **미인용** — 본문 L1567 "계면 에너지의 문헌 스케일"이라 서술하나 `\cite` 없음(dangling claim) | D. A. Cogswell, M. Z. Bazant, "Coherency Strain and the Kinetics of Phase Separation in LiFePO$_4$ Nanoparticles," *ACS Nano* **6**, 2215–2225 (2012). DOI: 10.1021/nn204177u | 상전이 입자 전극(LiFePO4)의 계면/변형 에너지를 다루는 대표 논문이나, **정확한 J/m² 수치는 PDF 텍스트 추출 실패로 직접 인용문 확보 못함** — 논문 존재·스코프만 확인 | **C**([수치는 근거 미발견], 논문 존재는 확인) | **★주의**: 이 논문은 v10-10 changelog(파일 L24)에서 "사이즈(반경) 효과" 관련 인용으로 **의도적으로 제외**(-cogswell2012) 되었던 문헌이다. 여기서 재인용을 권고하는 것은 \emph{다른 용도}(Gibbs-Thomson 배제 논증의 γ 수치 anchor)이며, 이전 삭제 사유(사이즈 broadening 스코프 배제)와 충돌하지 않음 — 그러나 최종 채택 여부는 사용자 판단 필요 |
| $V_m(\mathrm{LiC_6})=31.9$ cm$^3$/mol | 계산 유도 표시(L1566, 식 자체가 $6\times12.011/2.26$ 로 명시) — 밀도값 출처 미인용 | 흑연 밀도 $\rho=2.26$ g/cm³, 표준 물성값(예: CRC Handbook of Chemistry and Physics, 또는 IUPAC 표준 참조값) | 검색 확인: 2.26 g/cm³ 는 이론밀도(단결정 흑연)로 화학 물성 데이터베이스(Sigma-Aldrich 등)에 일관되게 등재된 표준값 | **A**(표준 물성, 교과서 수준 — 특정 1차 논문 불필요) | 이 항목은 "1차 문헌"보다 "표준 물성 참조서"가 적절 — 필요시 CRC Handbook 인용으로 충분, 별도 저널 논문 anchor 불요 |
| $D\sim10^{-10}$ cm$^2$/s (흑연 내 Li 확산계수) | **본문에 수치 자체가 없음**(L1565 은 $\tau(r)=r^2/D$ 로 일반형만 제시, 구체 D 값 미기재) | S. Park, J. H. Park, H. Yoon, Y. Cho, C.-Y. Yoo, "Investigation of Lithium Ion Diffusion of Graphite Anode by the Galvanostatic Intermittent Titration Technique," *Materials* **14**, 4683 (2021). DOI: 10.3390/ma14164683 | 검색 확인: 이 논문이 GITT 로 흑연 D $=1\times10^{-11}$–$4\times10^{-10}$ cm²/s 보고(SOC 의존, 고-Li 함량에서 $\approx10^{-10}$ cm²/s 수렴) — **정확 일치** | **A** | **★중대 발견 — 이 논문은 이미 bibitem `park2021`로 인용되어 있으나, 현재 bibitem 의 제목·주제 서술이 틀렸다(§8 참조). 실제 논문은 LixCoO2/graphite 전셀이 아니라 흑연 단독 GITT 확산계수 논문**이며, 여기(D 값)에 정확히 재사용 가능 |

---

## 7. 통계역학 기초 문헌 서지 확인

| 서지 | 현재 bibitem | 검증 결과 | 판정 |
|---|---|---|---|
| McKinnon & Haering 1983 | "in *Modern Aspects of Electrochemistry*, No. 15 (White, Bockris, Conway, eds.), Plenum Press (1983), pp. 235–304" | 검색 확인: 편저자·권호·출판사·연도·페이지 전부 **정확 일치**. 이 시기 book chapter 는 DOI 미부여가 정상(디지털화 이전) — DOI 부재는 서지 오류가 아님 | **확정 — 정확** |
| Hill 1960 | "Addison–Wesley (1960); Dover reprint (1986)" | 검색 확인: Dover 판 ISBN 0486652424, 재판연도 **1986 정확**, 508쪽 | **확정 — 정확** |
| Fowler & Guggenheim 1939 | "Cambridge Univ. Press (1939)" | 검색상 이견 없음(표준 서지, 널리 알려진 고전) | **확정 — 정확**(추가 이견 없음) |
| McQuarrie 1976 | "Harper & Row (1976); Univ. Science Books reprint (2000)" | 검색 확인: University Science Books 2000판 ISBN 1891389157, "본질적으로 원판 무변경 재쇄"라는 서술까지 일치 | **확정 — 정확** |
| Dahn·Zheng·Liu·Xue 1995 (`dahn1995`) | "*Science* **270**(5236), 590–593 (1995). DOI: 10.1126/science.270.5236.590" | 검색 확인: 저자 4인(J.R. Dahn, T. Zheng, Y. Liu, J.S. Xue) · 제목 · 권호 · 페이지 · DOI **전부 정확 일치** | **확정 — 정확** |
| Fly & Chen 2020 (`fly2020`) | "*J. Energy Storage* **29**, 101329 (2020). DOI: 10.1016/j.est.2020.101329" | 검색 확인: 저자 2인·권·아티클번호·DOI **정확 일치**(문건이 이미 v10-11 에서 자체 정정 기록한 대로) | **확정 — 정확**(기 정정사항 재확인) |

---

## 8. ★신규 발견 — 기존 bibitem 서지 오류

**`park2021` 제목 오기(확인된 오류, 수정 필요):**

- 현재 문건 표기: `S. Park \emph{et al.}, "Quasi-equilibrium open-circuit potential and entropy of Li$_x$CoO$_2$/graphite cells," Materials 14, 4683 (2021). DOI: 10.3390/ma14164683.`
- 검색으로 확인한 DOI 10.3390/ma14164683 의 **실제 제목**: *"Investigation of Lithium Ion Diffusion of Graphite Anode by the Galvanostatic Intermittent Titration Technique"* (Jong Hyun Park, Hana Yoon, Younghyun Cho, Chung-Yul Yoo, *Materials* **14**, 4683, 2021-08-19).
- 권·쪽·연도·DOI 는 전부 정확하나 **제목과 주제 서술("LixCoO2/graphite 전셀의 준평형 OCP·엔트로피")이 실제 논문과 다르다** — 실제 논문은 **흑연 단독 반쪽전지**의 GITT 확산계수 연구다.
- 다만 실제 논문 내용도 문건이 인용한 취지(GITT 준평형 OCP 플래토가 입자형상 무관하게 staging 전이와 일치 — "GITT is insensitive to particle size and electrode shape", QOCP 플래토 ≈0.22/0.12/0.08 V)를 **지지는 한다** — 완전히 무관한 오귀속은 아니고, 제목/부제 라벨링 오류로 보인다.
- **권고**: bibitem 제목을 실제 논문 제목으로 정정하고, 주석을 "GITT 준평형 OCP = 입자 무관 staging 전위 상수(그리고 이 논문 자체가 D~10⁻¹⁰–10⁻¹¹ cm²/s 확산계수 값도 보고 — §6 항목의 D anchor 로 교차 참조 가능)"로 보강 권고. **파일 수정은 본 sub 권한 밖이라 미실행 — master 검토 대상으로 남김.**

기타 확인한 bibitem(dahn1991, ohzuku1993, bazant2013, eyring1935, dreyer2010, bloom2005, dubarry2012, reimers1992, menetrier1999, motohashi2009, xia2007, reynier2004, swiderska2019, msmr2024, ml2024, leviaurbach1999, rsc2021, mckinnon1983, hill1960, fowler1939, mcquarrie1976, dahn1995, fly2020)는 서치 범위 내에서 서지 오류 발견되지 않음(권·쪽·DOI·저자 일치).

---

## 요약 (확보/미발견 집계)

- **tier A 확인**: 6건 (2→1 전위 0.085V, 2L→2 전위 0.120V, T1 x-범위, T4 xia2007 4.55V, x_MIT=0.85, D~1e-10 cm²/s, V_m 계산근거) — 일부는 이미 올바르게 인용돼 있던 확정 사항.
- **tier B/C 확보**: 8건 (4→3 전위, 3→2L 전위, 그래파이트 ΔS/ΔH 스케일 2건, ΔH_a 스케일 2건, T2/T3 전위, γ 계면에너지) — 스케일 근거는 있으나 전이별 정밀 anchor 는 아님.
- **[근거 미발견]**: 3건 (Ω 전이별 값 자체, g_max=13 의 원문 직접 수치 대조, ΔH_a 단일 확정 논문) — 그럴듯한 문헌을 추정 부착하지 않고 정직히 미확정 처리.
- **신규 인용 후보(현재 미인용)**: Reynier·Yazami·Fultz 2003 (J. Power Sources 119–121, 850, 흑연 엔트로피/엔탈피), Cogswell & Bazant 2012 (ACS Nano 6, 2215, γ 계면에너지 — 단, 과거 의도적 제외 이력 있음 주의).
- **서지 오류 발견**: `park2021` 제목이 실제 논문과 다름(DOI/권/쪽은 정확) — 실제 논문은 흑연 GITT 확산계수 논문이며, D 값(§6)에 교차 활용 가능.
