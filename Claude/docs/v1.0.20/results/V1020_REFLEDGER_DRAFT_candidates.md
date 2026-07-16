# V1020 서지 전수 검증 원장 — 신규 인용 후보 (DRAFT)

- 검증일: 2026-07-16
- 대상: v1.0.20 에서 신규 인용 예정 후보 9 키 (제안 키 기준) + 파생 원전 2건 (보조 표)
- 방법: DOI 보유 문헌 → Crossref DOI 레지스트리 메타데이터 (`api.crossref.org/works/<DOI>`, 출판사 기탁 1차 메타데이터) 필드 대조. 단행본·시리즈 챕터 → 서지 DB·실물 스캔 목차·출판사/도서관 레코드 교차 확인. WebSearch 는 1차 출처 도달용 보조.
- 판정 기준 (기존 원장 `V1020_REFLEDGER_DRAFT_existing.md` 과 동일): **V1** = 1차 출처(출판사/DOI 메타데이터/저널 사이트)로 핵심 필드 전부 확인 · **V2** = 2차 확인만 가능 또는 경미한 필드 불일치(문헌 식별에는 지장 없음) · **FAIL** = 필드 오류(정정안 제시) 또는 실재 미확인.
- 본 문건은 검증 원장 초안이며 tex 파일은 수정하지 않았다.

## 집계

| 구분 | 총계 | V1 | V2 | FAIL |
|---|---|---|---|---|
| 주 후보 (제안 키 10행) | 10 | 9 | 1 | 0 |
| 보조 원전 (파생 2행) | 2 | 1 | 1 | 0 |
| **합계** | **12** | **10** | **2** | **0** |

- FAIL 0건 — 후보 9건 모두 실재 확인.
- V2 2건: `ashcroftmermin1976` (단행본 — 출판사 각인 변형 병존 + 장/부록 위치는 2차 확인), `safran1987` (Crossref 메타데이터 권번호 41 vs 실물 인쇄본 권번호 40 — 실물이 기준).
- 주요 정정: `msmr_origin2017` 저자 byline (5인, 중간 이니셜 없음) · "MSMR" 명칭 자체는 2017 논문 제목이 아니라 2018 Part I 제목에서 등장 · `kohlrausch1854` 권번호 이중 체계 (Pogg. Ann. 91 = Ann. Phys. 통권 167) 및 2부작 구조.

## 주 후보 표

| 후보 key(제안) | 확정 서지(저자·연도·제목·저널·권·쪽) | DOI | 검증(URL·대조 필드) | 판정(V1/V2/FAIL) | 비고(정정 사항·용도) |
|---|---|---|---|---|---|
| imada1998 | Masatoshi Imada, Atsushi Fujimori, Yoshinori Tokura (1998) "Metal-insulator transitions" — Rev. Mod. Phys. 70(4), 1039–1263 | 10.1103/RevModPhys.70.1039 | Crossref `api.crossref.org/works/10.1103/RevModPhys.70.1039` — 저자 3인·RMP 70(4)·1039–1263·1998·제목 전부 일치. WebSearch 로 APS issue TOC(`journals.aps.org/rmp/issues/70/4`)·Scholar 메타 교차 | V1 | 정정: 끝쪽 1263 확정 (제안은 시작쪽만). 제목 대소문자는 "Metal-insulator transitions". 용도: MIT 배경 리뷰 |
| mott1968 | N. F. Mott (1968) "Metal-Insulator Transition" — Rev. Mod. Phys. 40(4), 677–683 | 10.1103/RevModPhys.40.677 | Crossref `api.crossref.org/works/10.1103/RevModPhys.40.677` — 단독 저자·RMP 40(4)·677–683·1968·제목 전부 일치 | V1 | 제안과 전 필드 일치 (끝쪽 683 추가). 용도: Mott 전이 원전 |
| marianetti2004 | C. A. Marianetti, G. Kotliar, G. Ceder (2004) "A first-order Mott transition in LixCoO2" — Nature Materials 3(9), 627–631 | 10.1038/nmat1178 | Crossref `api.crossref.org/works/10.1038/nmat1178` — 저자 3인·NM 3(9)·627–631·2004(온라인 8월/인쇄 9월) 전부 일치. PubMed 15322532 교차 | V1 | 제안과 전 필드 일치 (끝쪽 631 추가). 용도: LCO MIT (희석 불순물 Mott 전이 기제) |
| vanderven1998 | A. Van der Ven, M. K. Aydinol, G. Ceder, G. Kresse, J. Hafner (1998) "First-principles investigation of phase stability in LixCoO2" — Phys. Rev. B 58(6), 2975–2987 | 10.1103/PhysRevB.58.2975 | Crossref `api.crossref.org/works/10.1103/PhysRevB.58.2975` — 저자 5인·PRB 58(6)·2975–2987·1998·제목 전부 일치. APS 원문 PDF `link.aps.org/pdf/10.1103/PhysRevB.58.2975` 존재 확인 | V1 | 제안과 전 필드 일치 (끝쪽 2987 추가). 용도: LCO 상도표·order/disorder·staging 계산 |
| msmr_origin2017 | Mark Verbrugge, Daniel Baker, Brian Koch, Xingcheng Xiao, Wentian Gu (2017) "Thermodynamic Model for Substitutional Materials: Application to Lithiated Graphite, Spinel Manganese Oxide, Iron Phosphate, and Layered Nickel-Manganese-Cobalt Oxide" — J. Electrochem. Soc. 164(11), E3243–E3253 | 10.1149/2.0341708jes | Crossref `api.crossref.org/works/10.1149/2.0341708jes` — 저자 5인·JES 164(11)·E3243–E3253·2017(온라인 2017-05-25)·제목 전부 일치. IOPscience 랜딩 `iopscience.iop.org/article/10.1149/2.0341708jes` (직접 fetch 403, 검색 결과로 실재 확인). PyBaMM MSMR 문서가 열역학 파라미터 원전으로 인용함을 확인 | V1 | **정정 1**: byline 은 5인 전원 명기 — Verbrugge·Baker 외에 Brian Koch·Xingcheng Xiao·Wentian Gu. Crossref 기탁 byline 에는 중간 이니셜 없음 ("Mark Verbrugge, Daniel Baker", "M. W./D. R." 아님). **정정 2**: "MSMR" 이라는 명칭은 이 2017 논문 제목·초록에 없음 — 명칭 원전은 보조 표의 bakerverbrugge2018 (Part I 제목에 "Multi-Species, Multi-Reaction Model" 명기). 커뮤니티(PyBaMM 등)는 모델 열역학(OCV 식) 원전으로 본 2017 논문을, 명칭·다공전극 정식화 원전으로 2018 Part I 을 인용 — 두 편 병기 권장. **MSMR = "Multi-Species, Multi-Reaction"** (multiple-site 아님). 기존 ch2_bib 의 msmr2024·msmr_partII (2024 온도의존 Part 1/2) 와 구별 |
| williamswatts1970 | Graham Williams, David C. Watts (1970) "Non-symmetrical dielectric relaxation behaviour arising from a simple empirical decay function" — Trans. Faraday Soc. 66, 80–85 | 10.1039/TF9706600080 | Crossref `api.crossref.org/works/10.1039/tf9706600080` — 저자 2인·TFS 66·시작쪽 80·1970·제목 전부 일치 (Crossref 기탁은 시작쪽만; 끝쪽 85 는 통용 서지. RSC 랜딩은 fetch 403) | V1 | 제안과 전 필드 일치. 용도: KWW stretched exponential 원전 (Watts 는 "David C." — D. C. 표기 그대로 유효) |
| kohlrausch1854 | R. Kohlrausch (1854) "Theorie des elektrischen Rückstandes in der Leidener Flasche" — Annalen der Physik und Chemie (Poggendorff) Bd. 91 [Wiley 통권 Ann. Phys. 167], 2부작: (1) 56–82 · (2) 179–214 | 10.1002/andp.18541670103 (1부) · 10.1002/andp.18541670203 (2부) | Crossref `api.crossref.org/works/10.1002/andp.18541670203` — 저자·제목·Ann. Phys. 167(2)·179–214·1854 일치. `…/10.1002/andp.18541670103` — 167(1)·56–82·1854 일치. Wiley 랜딩 `onlinelibrary.wiley.com/doi/10.1002/andp.18541670203`·ADS `1854AnP...167...56K` 교차 | V1 | **정정(권번호 이중 체계)**: 전통 인용 "Pogg. Ann. 91, 179 (1854)" 의 91 은 Poggendorff 시리즈 권번호, Wiley 현대 통권으로는 167 — 둘은 같은 권. 논문은 2부작 (56–82 + 179–214), stretched exponential 통용 인용은 2부 (179–214). bibitem 작성 시 "Pogg. Ann. Phys. Chem. 91, 179–214 (1854)" + Wiley DOI 병기 권장 |
| ashcroftmermin1976 | N. W. Ashcroft, N. D. Mermin (1976) Solid State Physics — Holt, Rinehart and Winston, New York. ISBN 0-03-083993-9 | (단행본 — DOI 없음) | WebSearch — Biblio ISBN 레코드 `biblio.com/9780030839931` (1976·hardcover)·CERN 도서관 레코드 `cds.cern.ch/record/102652` (Holt, Rinehart and Winston 1976)·Wikipedia "Ashcroft and Mermin" 교차. Sommerfeld expansion 위치는 2차 확인 (SCIRP 인용 pp. 46–47 등) | V2 | 출판사·연도 제안대로 확인. 단 후기 인쇄본은 "Saunders College Publishing, Philadelphia" 각인으로도 널리 인용됨 (동일 1976 텍스트의 각인 변형 — 어느 쪽 표기도 실무상 통용). Sommerfeld expansion: Ch. 2 "The Sommerfeld Theory of Metals" (Eq. 2.70, pp. 45–47) + 도출은 Appendix C — 장/부록 번호는 2차 출처 + 지식 기반이므로 본문 인용 시 쪽수 재확인 권장 (V2 사유) |
| dreyer2011 | Wolfgang Dreyer, Clemens Guhlke, Michael Herrmann (2011) "Hysteresis and phase transition in many-particle storage systems" — Continuum Mech. Thermodyn. 23(3), 211–231 | 10.1007/s00161-010-0178-1 | Crossref `api.crossref.org/works/10.1007/s00161-010-0178-1` — 저자 3인·CMT 23(3)·211–231·2011(온라인 2011-01-06/인쇄 5월)·제목·DOI 전부 일치 | V1 | 제안과 전 필드 일치 (호수 3·끝쪽 231 추가). 용도: many-particle 히스테리시스 이론 (기존 ch1_bib dreyer2010 Nature Mater. 논문의 이론 확장판 — 병행 인용 정합) |
| safran1980 | S. A. Safran (1980) "Phase Diagrams for Staged Intercalation Compounds" — Phys. Rev. Lett. 44(14), 937–940 | 10.1103/PhysRevLett.44.937 | Crossref `api.crossref.org/works/10.1103/PhysRevLett.44.937` — 단독 저자·PRL 44(14)·937–940·1980·제목 전부 일치. APS 랜딩 `journals.aps.org/prl/abstract/10.1103/PhysRevLett.44.937` 검색 결과 실재 확인 | V1 | 제안과 전 필드 일치 (끝쪽 940 추가). 용도: staging 상도표 이론 원전. 더 알려진 종설은 보조 표 safran1987 — 원전(1980 PRL) + 종설(1987) 병기 권장 |

## 보조 표 — 파생 원전 (주 후보 검증 중 확인된 병기 후보)

| 후보 key(제안) | 확정 서지(저자·연도·제목·저널·권·쪽) | DOI | 검증(URL·대조 필드) | 판정(V1/V2/FAIL) | 비고(정정 사항·용도) |
|---|---|---|---|---|---|
| bakerverbrugge2018 | Daniel R. Baker, Mark W. Verbrugge (2018) "Multi-Species, Multi-Reaction Model for Porous Intercalation Electrodes: Part I. Model Formulation and a Perturbation Solution for Low-Scan-Rate, Linear-Sweep Voltammetry of a Spinel Lithium Manganese Oxide Electrode" — J. Electrochem. Soc. 165(16), A3952–A3964 | 10.1149/2.0771816jes | Crossref `api.crossref.org/works/10.1149/2.0771816jes` — 저자 2인·JES 165(16)·A3952–A3964·2018·제목 전부 일치. PyBaMM MSMR 문서가 모델 원전으로 인용 | V1 | "MSMR (Multi-Species, Multi-Reaction)" **명칭의 제목 등장 원전**. msmr_origin2017 과 병기 권장 (2017 = OCV 열역학 식 원전, 2018 = 명칭·다공전극 정식화) |
| safran1987 | S. A. Safran (1987) "Stage Ordering in Intercalation Compounds" — Solid State Physics (Advances in Research and Applications), Vol. 40 (H. Ehrenreich, D. Turnbull eds.), Academic Press, pp. 183–246 | 10.1016/S0081-1947(08)60692-X | Crossref `api.crossref.org/works/10.1016/S0081-1947(08)60692-X` — 제목·저자·pp. 183–246·1987 일치. 실물 스캔 목차 (vdoc.pub Vol. 40 스캔) — Vol. 40·1987·Ehrenreich/Turnbull 편·Safran 챕터 p. 183 수록 확인. ScienceDirect 랜딩 fetch 403 | V2 | **메타데이터 이상 1건**: Crossref 기탁 권번호는 41 로 되어 있으나 실물 인쇄본·통용 인용은 **Vol. 40 (1987)** — 실물 기준 Vol. 40 채택 (Crossref 연도 1987 도 Vol. 40 발행연도와만 정합). 끝쪽은 Crossref 183–246 채택. 용도: staging 종설 (safran1980 PRL 과 병기) |

## 잔여 확인 항목 (사용자 결정 불요 — 인용 시점에 재확인 권장)

1. `williamswatts1970` 끝쪽 85: Crossref 기탁이 시작쪽만 담고 있어 끝쪽은 통용 서지 기준 — RSC 원문 접근 가능 환경에서 1회 재확인하면 완전 V1.
2. `ashcroftmermin1976` Sommerfeld expansion 쪽수 (pp. 45–47, Eq. 2.70, Appendix C): 실물 대조 후 각주 인용에 사용.
3. `safran1987` 끝쪽 246: 실물 스캔 목차 추출치(236)와 Crossref(246)가 달랐음 — Crossref 채택했으나 실물 대조 시 최종 확정.
