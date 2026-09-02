# R7 — 레퍼런스 마스터 맵 초안 (v2.0.0 마스터 플랜 워크플로 · 판독·등록부 에이전트 산출)

> 작성 = 워크플로 판독·등록부 에이전트(Fable 5.1), 2026-09-03. 통합·commit 은 master 몫이며 본 문건은 초안이다.
> 원천 = `Claude/docs/v1.0.25.1/_sections/ch1v22_bib.tex`·`ch2v22_bib.tex`·`ch3v22_bib.tex`(현행 bib 3본, 전문 정독) + 서지 원장 `Claude/docs/v1.0.23/results/V1023_REFERENCE_LEDGER.md`·`v1.0.22/results/V1022_REFERENCE_LEDGER.md`(전문 정독) + 두 원장이 "그대로 승계"한다고 선언한 상위 원장 `v1.0.21/results/V1021_REFERENCE_LEDGER.md`·`v1.0.20/results/V1020_REFERENCE_LEDGER.md`(전문 정독 — 승계 사슬 확인용) + 선행 서베이 4본(`Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md`·`Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md`·`Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md`·`Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md`, 전문 정독).
> 본문 `_sections/*.tex` 53본은 **기계 스캔**(`\cite` 위치·절 제목·개념 키워드 빈도)만 수행했고 전문 정독은 하지 않았다 — 절별 인용 판정은 그 한계 안에서 읽어야 한다(말미 Read Coverage 참조).
> 보고 표기는 4-tier 로 구분한다: **[확정]** = 원천 path+line 또는 Crossref 응답 실물 근거 · **[근거 미발견]** · **[추정]** = 본 에이전트 판단 · **[미검증]** = 확인 수단 미실행.
> 외부 접근: Crossref REST API(`api.crossref.org/works/{DOI}`)가 열려 있어 2026-09-03 에 **현행 bib 의 DOI 84건 전건**과 **후보 문헌 DOI 74건**을 조회했다. 조회 스크립트·응답 JSON 은 세션 스크래치(휘발)에 있으며, 여기에는 대조 결과만 옮긴다. 서적(ISBN)은 Crossref 로 검증할 수 없어 **[미검증]** 으로 남긴다. 어떤 서지도 기억만으로 확정하지 않았다 — 기억 기반 DOI 후보는 Crossref 응답의 제목·저자·저널·연도가 의도한 문헌과 일치할 때만 "Crossref 확인"으로 적었고, 응답이 다른 문헌을 가리킨 경우는 그대로 "미검증(후보 DOI 오해소)"으로 적었다.

---

## 0. 요지

현행 v1.0.25.1 의 참고문헌은 세 장별 bib 에 **95 `\bibitem`**(Ch1 44 · Ch2 15 · Ch3 36), 중복 키 2건(`swiderska2019` Ch1+Ch2, `verbrugge2017` Ch1+Ch3)을 제하면 **93 distinct 키**다. 본문 `\cite` 명령은 `_sections` 본문 53본에서 262회(다중 키 명령을 키 단위로 펼치면 315회)이고, `ch1v22_bib.tex` 안의 상호 참조 3회를 더하면 brief §4.2 의 "265"와 정확히 맞는다. 93 키 전부가 본문에서 최소 1회 인용되고, 정의되지 않은 키를 인용한 곳은 0건이다. DOI 는 84건이 있고 9건이 없는데, 없는 9건은 서적·장(chapter) 8건과 내부 자료 1건이라 구조적으로 정상이다. Crossref 대조 결과 84건 전건이 해소되고 제목·첫저자·저널·권·연도가 일치하지만, **실질 결함 4건**이 남는다: ① `verbrugge2017`(Ch1 line 49·Ch3 line 43)의 제목이 Crossref 실물과 다르고, 같은 DOI 가 Ch2 의 `msmr_origin2017`(line 17, 제목 정확)로도 등재돼 있어 **한 문헌이 두 키·두 제목**으로 존재한다. ② `schmitt2022`(Ch1 line 48)의 첫저자 이니셜 "J."가 Crossref "C. Schmitt"와 다르며 저자 4인이 "et al."로 생략돼 있다. ③ `koebbing2024`(Ch3 line 19)는 원장 V1022 가 권·호(34(7))를 이미 해소했는데 bib 에 반영되지 않았다. ④ `sethuraman_stresspot2010`(Ch3 line 13)은 쪽이 비어 있고 Crossref 는 시작쪽 A1253 을 준다.

원장(ledger) 쪽은 더 큰 구조 문제가 있다. `V1023_REFERENCE_LEDGER.md` 는 `V1022_REFERENCE_LEDGER.md` 와 **바이트 단위로 동일한 사본**(md5 일치, 제목까지 "V1022")이며, 따라서 v1.0.23 이후 추가된 키 **6건(`lee2017jcp`·`lee2011jcp`·`son2013jcp`·`schmitt2022`·`verbrugge2017`·`artrith2018`)은 어느 원장에도 등재돼 있지 않다**. 반대로 원장에는 있으나 현행 bib 에 없는 키가 4건(`safran1980`·`safran1987`·`williamswatts1970`·`kohlrausch1854`) 있다. "본문 `\cite` 는 원장 V1 키만"이라는 규칙(V1020 line 3)은 v1.0.23 부터 실질적으로 끊겨 있었던 셈이다.

주제별 필수 문헌 체크리스트(§4)는 12 주제 표 · 약 150 행이다. 현행 bib 는 재료 실측·최신 문헌(흑연 staging·LCO·Si 계열) 쪽은 두텁지만, 사용자 기준 ③(리뷰 논문급 레퍼런스)과 ⑤(일반식→특수식의 가정 사다리에 레퍼런스가 확실한 가정)를 v2.0.0 골격(Part I 일반 이론)에 맞추려면 **이론 원전 층이 거의 비어 있다**. 본문 키워드 스캔에서 Marcus·Kramers·Onsager·Nernst–Planck·Fokker–Planck·Preisach·KWW·Kubo(요동-소산)·Ising·Redlich–Kister·Safran 은 **본문 출현 0회**이고, Butler–Volmer 는 1회(§5, bazant2013 의 식 번호 경유), Daumas–Hérold 는 1회(§5b, 원전 인용 없이 이름만)다. 이 공백은 brief §5 작업 챕터 3.1 의 조사 축(열역학·통계역학·동역학·히스테리시스·열)과 정확히 겹치므로, 체크리스트는 그 축을 따라 배열했고 각 항목에 v2.0.0 저작 Phase(4.1~4.9) 배치를 붙였다.

인용 규약 초안(§5)은 열 조항으로, 핵심은 단일 원장(REFERENCE_LEDGER v2)에서 bib 를 **생성**하는 방향(손편집 금지 → 헤더 카운트 스테일·중복 키·미등재 재발 차단), Crossref 5-필드 대조 절차의 명문화, 저자 전원 명기(et al. 금지), 1차 문헌 우선과 tier 태그 유지다.

---

## 1. 현행 서지 자산 실측

### 1.1 카운트와 정의 [확정]

| 항목 | 값 | 정의·근거 |
|---|---|---|
| `\bibitem` 총수 | **95** | Ch1 44(`ch1v22_bib.tex` lines 6–49) + Ch2 15(`ch2v22_bib.tex` lines 6–20) + Ch3 36(`ch3v22_bib.tex` lines 6–19 의 14 + lines 22–43 의 R5 신규 22). brief §4.2 "bibitem 95" 일치 |
| distinct 키 | **93** | 중복 = `swiderska2019`(Ch1 line 23 = Ch2 line 16, 텍스트 동일) · `verbrugge2017`(Ch1 line 49 = Ch3 line 43, 텍스트 동일·제목 오류 공유) |
| `\cite` 명령 수 | **262** (`_sections` 본문 53본, bib 3본 제외) · +3 (`ch1v22_bib.tex` lines 46–47 의 상호참조 `\cite{son2013jcp}`·`\cite{lee2017jcp}`×2) = **265** | brief §4.2 "`\cite` 호출 265" 와 일치(정의 = 명령 수) |
| 키 단위 인용 발생 | **315** | 다중 키 `\cite{a,b}` 를 키별로 펼친 수. 93 키 전부 ≥1회. 미정의 키 인용 0 · 미인용 bib 키 0 |
| 마스터 tex 3본·`appendix_phase_separation.tex` 의 `\cite` | 0 | 부록(상분리)은 `\cite` 대신 수동 번호 `[A1]~[A5]`(`appendix_phase_separation.tex` lines 483–495) |
| DOI 보유 | **84 / 95** (distinct 기준 82 / 93) | DOI 없음 9 = 서적·장 8(`glasstone1941`·`hill1960`·`fowler1939`·`mcquarrie1976`·`ashcroftmermin1976`·`mckinnon1983`·`newman`·`huggins2009`) + 내부 자료 1(`numverif2026`) |
| bib 파일 헤더 카운트 | Ch1 "39종" · Ch2 "14종" · Ch3 "14종" | **스테일** — 실물 44·15·36. 헤더는 R1(v1.0.22) 분할 시점 값이 그대로 남은 것(`ch1v22_bib.tex` line 2, `ch2v22_bib.tex` line 2, `ch3v22_bib.tex` line 2) |

### 1.2 원장(ledger) 계보와 등재 공백 [확정]

원장은 v1.0.20 에서 개설돼 v1.0.21 → v1.0.22 → v1.0.23 으로 "승계 선언" 방식으로 이어진다. 각 원장은 상위 원장 전건을 그대로 승계하고 자기 버전의 신규분만 적는 구조다(`V1021_REFERENCE_LEDGER.md` line 4, `V1022_REFERENCE_LEDGER.md` line 4).

| 원장 | 담는 것 | 상태 |
|---|---|---|
| `v1.0.20/results/V1020_REFERENCE_LEDGER.md`(55줄) | A. 기존 42 키 판정(lines 8–19) · B. 신규 14 행(lines 23–38: imada1998·mott1968·marianetti2004·vanderven1998·msmr_origin2017·bakerverbrugge2018·williamswatts1970·kohlrausch1854·ashcroftmermin1976·dreyer2011·safran1980·safran1987[V2]·glasstone1941·laidlerking1983) · D. 부록 [A1]~[A5](lines 48–54, ISBN·DOI) | 판정 근거 원본. "V2 = safran1987 뿐"(line 41) |
| `v1.0.21/results/V1021_REFERENCE_LEDGER.md`(38줄) | B′ weppner_huggins1977·baek_pilon2022(lines 25–26) · B″ Si 14건(lines 32–36) | koebbing2024·sethuraman_stresspot2010 "필드 조건부" |
| `v1.0.22/results/V1022_REFERENCE_LEDGER.md`(33줄) | R2+ 신규 20 키(kim_entropymetry2020 + R5 19건, lines 10–30) · koebbing2024 권·호 해소 기록(line 4: *Adv. Funct. Mater.* **34**(7) 2308818) | 장별 bib 분할 시점 카운트 "Ch1 39·Ch2 14·Ch3 14"(line 5) |
| `v1.0.23/results/V1023_REFERENCE_LEDGER.md`(33줄) | **V1022 와 바이트 동일 사본**(md5 일치, 제목 "V1022 REFERENCE LEDGER" 그대로) | v1.0.23 신규분(refs 6/7 3키) 미기록 |

이 사슬을 현행 bib 93 키와 대조한 결과는 다음과 같다.

- **bib 에 있으나 어느 원장에도 없는 키 6건**: `lee2017jcp`·`lee2011jcp`·`son2013jcp`(v1.0.23 부록 E, `ch1v22_bib.tex` lines 45–47), `schmitt2022`(v1.0.24 XRD 캠페인, line 48), `verbrugge2017`(line 49 및 `ch3v22_bib.tex` line 43), `artrith2018`(`ch3v22_bib.tex` line 42). 이 6건은 bib 비고에 "Crossref 확정" 등 검증 흔적은 있으나 원장 절차([검증→등재→인용])를 거친 기록이 없다.
- **원장에 있으나 bib 에 없는 키 4건**: `safran1980`(V1)·`safran1987`(V2)·`williamswatts1970`(V1)·`kohlrausch1854`(V1). 뒤 둘은 KWW(Kohlrausch–Williams–Watts) 꼬리 일반형이 scope-out 된 결과(brief §4.5 "KWW/장벽분포 꼬리 일반형(scope-out)")로 읽히고, Safran 계열은 staging 미시 이론이 범위 밖으로 유지된 결과(`SM2_SURVEY.md` line 42 "축 B … 범위 밖 유지")다 [추정 — 삭제 시점을 기록한 원천은 미발견].
- 부록 [A1]~[A5]는 원장 V1020 D 에 판정이 있으나 bib 키가 아니어서 `\cite` 로 연결되지 않는다.

### 1.3 Crossref 대조 결과와 잔여 결함 [확정 — Crossref 응답 2026-09-03]

84 DOI 전건이 해소됐다(HTTP 오류·미해소 0). 자동 대조 항목은 연도(print/online 어느 쪽이든 일치)·첫저자 성(姓)·권·제목 앞 6단어이며, 자동 플래그 6건 중 5건(`dahn1995` 호 번호를 연도로 오인, `reynier2003` 권 "119--121" 표기, `marianetti2004`·`reynier2004` 제목의 수식 첨자, `menetrier1999` 악센트 문자)은 스크립트 측 오탐으로 판정했고, 실제 결함은 아래 표의 R-01~R-06 이다.

| ID | 키 · 위치 | 결함 | Crossref 실물 | 조치 후보 |
|---|---|---|---|---|
| R-01 | `verbrugge2017` — `ch1v22_bib.tex` line 49 · `ch3v22_bib.tex` line 43 | 제목 "…Application to Lithiated Graphite, Spinel Manganese Oxide, **Silicon, and Their Alloys**" 는 실물과 다름. 동일 DOI 10.1149/2.0341708jes 가 `msmr_origin2017`(`ch2v22_bib.tex` line 17)에 **정확한 제목**으로 별도 등재 → 한 문헌·두 키·두 제목 | 제목 = "Thermodynamic Model for Substitutional Materials: Application to Lithiated Graphite, Spinel Manganese Oxide, **Iron Phosphate, and Layered Nickel-Manganese-Cobalt Oxide**", 저자 Verbrugge·Baker·Koch·Xiao·Gu, *JES* 164(11) E3243–E3253 (2017) | v2.0.0 에서 키 1개로 통합·제목 정정(DQ-1). 동결본 v1.0.25.1 은 무수정 |
| R-02 | `schmitt2022` — `ch1v22_bib.tex` line 48 | 첫저자 "J. Schmitt *et al.*" | 저자 4인 = **C.** Schmitt, A. Kube, N. Wagner, K. A. Friedrich; *ChemElectroChem* 9(2) e202101342; online 2021·print 2022 | 이니셜 정정 + 4인 전원 명기(DQ-4·DQ-10) |
| R-03 | `koebbing2024` — `ch3v22_bib.tex` line 19 | 권·호 없음("인쇄 권·호는 사용 시 Crossref 최종 대조") | *Adv. Funct. Mater.* **34**(7) 2308818, online 2023·print 2024 — 원장 V1022 line 4 가 이미 해소 | bib 반영(DQ-11) |
| R-04 | `sethuraman_stresspot2010` — `ch3v22_bib.tex` line 13 | 쪽 없음 | *JES* 157(11) **A1253**(Crossref page 필드 시작쪽만; 끝쪽 [미검증]) | 시작쪽 반영·끝쪽은 출판사 페이지 대조(DQ-11) |
| R-05 | `laidlerking1983` — `ch1v22_bib.tex` line 11 | 제목 "The development of transition-state theory" | Crossref 제목 "Development of transition-state theory" | 관사 유무 — 인쇄면 표기 [미검증]. 경미 |
| R-06 | `dreyer2010`(6인)·`bloom2005`(7인)·`allart2018`(3인)·`schmitt2022`(4인) | "et al." 로 저자 생략 | Crossref 저자 전원 확보 가능 | 리뷰급 규약이면 전원 명기(DQ-4). `allart2018` 은 3인(Allart·Montaru·Gualous)이라 생략할 이유가 없음 |

이 외에 연도가 online/print 로 갈리는 항목(`verbrugge_lisi2016` online 2015·print 2016, `schmitt2022`, `koebbing2024`, `hudak` 류)은 인쇄판 연도 표기 관행(V1022 line 4 비고)을 따르면 현행 표기가 옳다.

---

## 2. 95 `\bibitem` 목록표

표기 규약: "서지"는 축약(첫저자·저널·권·시작쪽·연도)이며 정본은 bib 라인이다. "DOI"는 bib 기재값. "Crossref"는 2026-09-03 대조 판정(일치 = 제목·첫저자·저널·권·연도 일치). "원장"은 §1.2 의 등재 위치. "인용 절"은 `파일 축약(cite 횟수)` — 축약 범례: §n = Ch1 흑연 `ch1_sec0n`(§0 서론·§1 기호/분극·§2a/§2b Part 0·§3 중심·§4 히스·§5 폭·§5b stage-2L·§6 평형 peak·§7 broadening·§8 lag·§9 tail·§10 합산·§18 입력) · Tn = Part T `ch2_sec0n`(T1 분배함수·T2 config·T3 vib/el·T4 Einstein·T5 mixing·T7 가역발열·T8 종합·T9 방법) · Ln = Ch2 LCO `ch1_sec1n`(L11 도입·L12 중심·L13 hys·L14 삼분해·L15 전자·L16 peak·L16b Ω·L17 MSMR) · Sn = Ch3 `ch3v22_sec0n`(S1 지도·S2 케이스·S2b Si-FR·S3 블렌드·S4 기계·S5 코드) · 부록 A(부호검산)/B(코드맵)/D(Si 예비)/E(자기일관)/C·D′(ch2_app A/B).

### 2.1 Ch1 흑연 + Part T — `ch1v22_bib.tex` 44건 [확정]

| # | line | key | 서지(축약) | DOI | Crossref | 원장 | 인용 절(회) |
|---|---|---|---|---|---|---|---|
| 1 | 6 | dahn1991 | Dahn, *PRB* 44, 9170 (1991) | 10.1103/PhysRevB.44.9170 | 일치 | V1020-A | §0(1)·§1(1)·§5b(4)·§7(1)·§10(3)·T1(1)·T5(1) = 12 |
| 2 | 7 | ohzuku1993 | Ohzuku·Iwakoshi·Sawai, *JES* 140, 2490 (1993) | 10.1149/1.2220849 | 일치 | V1020-A(C-003) | §0·§1·§5b·§7·§10(3)·T1·T5 = 9 |
| 3 | 8 | bazant2013 | Bazant, *Acc. Chem. Res.* 46, 1144 (2013) | 10.1021/ar300145c | 일치 | V1020-A | §5(3) |
| 4 | 9 | eyring1935 | Eyring, *JCP* 3, 107 (1935) | 10.1063/1.1749604 | 일치 | V1020-A | §5(1) |
| 5 | 10 | glasstone1941 | Glasstone·Laidler·Eyring, McGraw-Hill (1941) | 없음(서적) | — | V1020-B(ISBN) | §5(1) |
| 6 | 11 | laidlerking1983 | Laidler·King, *J. Phys. Chem.* 87, 2657 (1983) | 10.1021/j100238a002 | 일치(R-05 관사) | V1020-B | §5(1) |
| 7 | 12 | hill1960 | Hill, Addison-Wesley (1960) Ch. 7 | 없음(서적) | — | V1020-A | §2a(2)·§2b(2) = 4 |
| 8 | 13 | fowler1939 | Fowler·Guggenheim, CUP (1939) | 없음(서적) | — | V1020-A | §2a(2) |
| 9 | 14 | mcquarrie1976 | McQuarrie, Harper & Row (1976) | 없음(서적) | — | V1020-A | §2a(3)·§2b(3)·§5(1) = 7 |
| 10 | 15 | ashcroftmermin1976 | Ashcroft·Mermin (1976) Ch. 2·App. C | 없음(서적) | — | V1020-B | §2a(1) |
| 11 | 16 | mckinnon1983 | McKinnon·Haering, *Mod. Aspects Electrochem.* 15, 235 (1983) | 없음(장) | — | V1020-A | §2a(3) |
| 12 | 17 | dreyer2010 | Dreyer *et al.*(6인), *Nat. Mater.* 9, 448 (2010) | 10.1038/nmat2730 | 일치(R-06) | V1020-A | §4(3)·§7(4) = 7 |
| 13 | 18 | dreyer2011 | Dreyer·Guhlke·Herrmann, *CMT* 23, 211 (2011) | 10.1007/s00161-010-0178-1 | 일치 | V1020-B | §4(1)·§7(4) = 5 |
| 14 | 19 | bloom2005 | Bloom *et al.*(7인), *JPS* 139, 295 (2005) | 10.1016/j.jpowsour.2004.07.021 | 일치(R-06) | V1020-A | §0(1) |
| 15 | 20 | weppner_huggins1977 | Weppner·Huggins, *JES* 124, 1569 (1977) | 10.1149/1.2133112 | 일치 | V1021-B′ | §1(3) |
| 16 | 21 | baek_pilon2022 | Baek·Saber·Van der Ven·Pilon, *JPCC* 126, 6096 (2022) | 10.1021/acs.jpcc.1c10414 | 일치 | V1021-B′ | §1(2) |
| 17 | 22 | dubarry2012 | Dubarry·Truchot·Liaw, *JPS* 219, 204 (2012) | 10.1016/j.jpowsour.2012.07.016 | 일치 | V1020-A | §0(1) |
| 18 | 23 | swiderska2019 | Świderska-Mocek·Rudnicka·Lewandowski, *PCCP* 21, 2115 (2019) | 10.1039/c8cp06638h | 일치 | V1020-A | 부록A(1)·§1(1)·L12(2) = 4 [Ch2 중복 수록] |
| 19 | 24 | leviaurbach1999 | Levi·Aurbach, *Electrochim. Acta* 45, 167 (1999) | 10.1016/S0013-4686(99)00202-9 | 일치 | V1020-A(C-002) | §7(2) |
| 20 | 25 | rsc2021 | Onuma *et al.*(9인 명기), *J. Mater. Chem. A* 9, 11187 (2021) | 10.1039/D0TA12607A | 일치 | V1020-A | §7(1) |
| 21 | 26 | fly2020 | Fly·Chen, *J. Energy Storage* 29, 101329 (2020) | 10.1016/j.est.2020.101329 | 일치 | V1020-A | §7(1) |
| 22 | 27 | dahn1995 | Dahn·Zheng·Liu·Xue, *Science* 270, 590 (1995) | 10.1126/science.270.5236.590 | 일치 | V1020-A | §7(1) |
| 23 | 28 | park2021 | Park·Yoon·Cho·Yoo, *Materials* 14, 4683 (2021) | 10.3390/ma14164683 | 일치 | V1020-A | §7(4) |
| 24 | 29 | reynier2003 | Reynier·Yazami·Fultz, *JPS* 119–121, 850 (2003) | 10.1016/S0378-7753(03)00285-4 | 일치 | V1020-A | §1(2)·§5b(1)·§10(1)·T2(1)·T3(2) = 7 |
| 25 | 30 | persson2010 | Persson *et al.*(9인 명기), *JPCL* 1, 1176 (2010) | 10.1021/jz100188d | 일치 | V1020-A | §10(1) |
| 26 | 31 | persson2010b | Persson·Hinuma·Meng·Van der Ven·Ceder, *PRB* 82, 125416 (2010) | 10.1103/PhysRevB.82.125416 | 일치 | V1020-A | §5b(1)·§10(1) = 2 |
| 27 | 32 | cogswell2012 | Cogswell·Bazant, *ACS Nano* 6, 2215 (2012) | 10.1021/nn204177u | 일치 | V1020-A | §7(1) |
| 28 | 33 | bernardi1985 | Bernardi·Pawlikowski·Newman, *JES* 132, 5 (1985) | 10.1149/1.2113792 | 일치 | V1020-A | T7(3)·T9(1) = 4 |
| 29 | 34 | newman | Newman·Thomas-Alyea, *Electrochemical Systems* 3rd ed. (2004) | 없음(서적) | — | V1020-A | T1(1)·T7(1) = 2 |
| 30 | 35 | huggins2009 | Huggins, *Advanced Batteries* (2009) | 없음(서적) | — | V1020-A | T1(1) |
| 31 | 36 | allart2018 | Allart *et al.*(실제 3인: Allart·Montaru·Gualous), *JES* 165, A380 (2018) | 10.1149/2.1251802jes | 일치(쪽 A380–A387; R-06) | V1020-A | §1(1)·T2(4)·T9(3) = 8 |
| 32 | 37 | occupation2019 | Mercer *et al.*(7인 명기), *Electrochim. Acta* 324, 134774 (2019) | 10.1016/j.electacta.2019.134774 | 일치 | V1020-A | T2(1) |
| 33 | 38 | chemmater2015 | Konar·Häussermann·Svensson, *Chem. Mater.* 27, 2566 (2015) | 10.1021/acs.chemmater.5b00235 | 일치 | V1020-A | T2(1) |
| 34 | 39 | jpcc2021 | Haruyama *et al.*(7인 명기), *JPCC* 125, 27891 (2021) | 10.1021/acs.jpcc.1c08992 | 일치 | V1020-A | T3(2)·T4(1) = 3 |
| 35 | 40 | msmr_partI | Garrick *et al.*(7인 명기), *JES* 171, 023502 (2024) | 10.1149/1945-7111/ad1d27 | 일치 | V1020-A(C-005) | T3(1)·T7(1)·T9(1) = 3 |
| 36 | 41 | msmr_partII | Paul *et al.*(8인 명기), *JES* 171, 103505 (2024) | 10.1149/1945-7111/ad70d9 | 일치 | V1020-A(C-006) | T2(1)·T9(1) = 2 |
| 37 | 42 | standardised2024 | Hales·Bulman, *JES* 171, 050535 (2024) | 10.1149/1945-7111/ad4918 | 일치 | V1020-A | T7(1)·T8(1) = 2 |
| 38 | 43 | hysteresis2018 | Zilberman·Rheinfeld·Jossen, *JPS* 395, 179 (2018) | 10.1016/j.jpowsour.2018.05.052 | 일치 | V1020-A(C-007) | T5(2)·T9(1) = 3 |
| 39 | 44 | numverif2026 | 내부 수치 검증(Derivative A), Anode_Fit v1.0.19 | 없음(내부) | — | V1020-A(내부자료) | T5(3)·부록D′(1) = 4 |
| 40 | 45 | lee2017jcp | K. Lee·S. Lee·Choi·S. Lee, *JCP* 147, 144111 (2017) — 사용자 논문 | 10.1063/1.5000882 | 일치 | **미등재** | 부록E(5) |
| 41 | 46 | lee2011jcp | S. Lee·Son·Sung·Chong, *JCP* 134, 121102 (2011) — ref. 6 | 10.1063/1.3565476 | 일치 | **미등재** | 부록E(2) |
| 42 | 47 | son2013jcp | Son·Kim·Kim·Kim·Lee, *JCP* 138, 164123 (2013) — ref. 7 | 10.1063/1.4802584 | 일치 | **미등재** | 부록E(2) |
| 43 | 48 | schmitt2022 | "J. Schmitt *et al.*", *ChemElectroChem* 9, e202101342 (2022) | 10.1002/celc.202101342 | **R-02**(첫저자 C.·4인) | **미등재** | §5b(4) |
| 44 | 49 | verbrugge2017 | Verbrugge·Baker·Koch·Xiao·Gu, *JES* 164, E3243 (2017) | 10.1149/2.0341708jes | **R-01**(제목 오류·`msmr_origin2017` 과 동일 DOI) | **미등재** | §5b(2)·S2b(1) = 3 [Ch3 중복 수록] |

### 2.2 Ch2 LCO — `ch2v22_bib.tex` 15건 [확정]

| # | line | key | 서지(축약) | DOI | Crossref | 원장 | 인용 절(회) |
|---|---|---|---|---|---|---|---|
| 45 | 6 | reimers1992 | Reimers·Dahn, *JES* 139, 2091 (1992) | 10.1149/1.2221184 | 일치 | V1020-A | L13(4)·L15(3)·L16b(2) = 9 |
| 46 | 7 | vanderven1998 | Van der Ven·Aydinol·Ceder·Kresse·Hafner, *PRB* 58, 2975 (1998) | 10.1103/PhysRevB.58.2975 | 일치 | V1020-B | L13(5)·L16b(3) = 8 |
| 47 | 8 | mott1968 | Mott, *RMP* 40, 677 (1968) | 10.1103/RevModPhys.40.677 | 일치 | V1020-B | L15(2) |
| 48 | 9 | imada1998 | Imada·Fujimori·Tokura, *RMP* 70, 1039 (1998) | 10.1103/RevModPhys.70.1039 | 일치 | V1020-B | L15(3) |
| 49 | 10 | marianetti2004 | Marianetti·Kotliar·Ceder, *Nat. Mater.* 3, 627 (2004) | 10.1038/nmat1178 | 일치 | V1020-B | L13(1)·L15(3) = 4 |
| 50 | 11 | kim_entropymetry2020 | Kim *et al.*(8인 명기), *EES* 13, 286 (2020) | 10.1039/C9EE02964H | 일치 | V1022-R2+ | L11(1) |
| 51 | 12 | menetrier1999 | Ménétrier·Saadoune·Levasseur·Delmas, *J. Mater. Chem.* 9, 1135 (1999) | 10.1039/a900016j | 일치 | V1020-A | L11(1)·L15(5)·L16b(1) = 7 |
| 52 | 13 | motohashi2009 | Motohashi *et al.*(8인 명기), *PRB* 80, 165114 (2009) | 10.1103/PhysRevB.80.165114 | 일치 | V1020-A | L11(1)·L13(3)·L15(7)·L16(1)·L16b(2) = 14 (최다 인용) |
| 53 | 14 | xia2007 | Xia·Lu·Meng·Ceder, *JES* 154, A337 (2007) | 10.1149/1.2509021 | 일치 | V1020-A | L11(2)·L16(1) = 3 |
| 54 | 15 | reynier2004 | Reynier·Graetz·Swan-Wood·Rez·Yazami·Fultz, *PRB* 70, 174304 (2004) | 10.1103/PhysRevB.70.174304 | 일치 | V1020-A | L11(2)·L13(1)·L14(3)·L15(4)·L16(1) = 11 |
| 55 | 16 | swiderska2019 | (#18 과 동일 텍스트 — 의도된 중복, D22) | — | — | V1020-A | Ch2 빌드에서 L12(2) |
| 56 | 17 | msmr_origin2017 | Verbrugge·Baker·Koch·Xiao·Gu, *JES* 164, E3243 (2017) — 제목 정확 | 10.1149/2.0341708jes | 일치 | V1020-B | L11(1)·L17(3) = 4 |
| 57 | 18 | bakerverbrugge2018 | Baker·Verbrugge, *JES* 165, A3952 (2018) | 10.1149/2.0771816jes | 일치 | V1020-B | L17(3) |
| 58 | 19 | msmr2024 | Paul *et al.*(8인 명기), *ECS Adv.* 3, 042501 (2024) | 10.1149/2754-2734/ad7d1c | 일치 | V1020-A(C-004) | L11(1)·L17(1) = 2 |
| 59 | 20 | ml2024 | Faghih Shojaei *et al.*(8인 명기), *JMPS* 190, 105726 (2024) | 10.1016/j.jmps.2024.105726 | 일치 | V1020-A(C-001) | L13(2)·L15(1)·L16b(1) = 4 |

### 2.3 Ch3 Si·혼합 — `ch3v22_bib.tex` 36건 [확정]

| # | line | key | 서지(축약) | DOI | Crossref | 원장 | 인용 절(회) |
|---|---|---|---|---|---|---|---|
| 60 | 6 | wen_huggins1981 | Wen·Huggins, *J. Solid State Chem.* 37, 271 (1981) | 10.1016/0022-4596(81)90487-4 | 일치 | V1021-B″ | 부록D(1)·S1(1)·S2(2) = 4 |
| 61 | 7 | limthongkul2003 | Limthongkul·Jang·Dudney·Chiang, *Acta Mater.* 51, 1103 (2003) | 10.1016/S1359-6454(02)00514-1 | 일치(쪽 1103–1113) | V1021-B″ | 부록D·S1·S2(3)·S3 = 6 |
| 62 | 8 | li_dahn2007 | Li·Dahn, *JES* 154, A156 (2007) | 10.1149/1.2409862 | 일치 | V1021-B″ | 부록D·S1·S2 = 3 |
| 63 | 9 | obrovac_christensen2004 | Obrovac·Christensen, *ESSL* 7, A93 (2004) | 10.1149/1.1652421 | 일치 | V1021-B″ | 부록D·S1·S2·S2b = 4 |
| 64 | 10 | chevrier_dahn2009 | Chevrier·Dahn, *JES* 156, A454 (2009) | 10.1149/1.3111037 | 일치 | V1021-B″ | 부록D(2)·S1(2)·S2(1)·S2b(3) = 8 |
| 65 | 11 | beaulieu2001 | Beaulieu·Eberman·Turner·Krause·Dahn, *ESSL* 4, A137 (2001) | 10.1149/1.1388178 | 일치 | V1021-B″ | 부록D·S1·S4 = 3 |
| 66 | 12 | sethuraman_stressevo2010 | Sethuraman·Chon·Shimshak·Srinivasan·Guduru, *JPS* 195, 5062 (2010) | 10.1016/j.jpowsour.2010.02.013 | 일치 | V1021-B″ | 부록D·S1·S2·S4 = 4 |
| 67 | 13 | sethuraman_stresspot2010 | Sethuraman·Srinivasan·Bower·Guduru, *JES* 157(11) (2010) — 쪽 공란 | 10.1149/1.3489378 | **R-04**(A1253) | V1021-B″(조건부) | 부록D·S1·S2·S4 = 4 |
| 68 | 14 | liu_sizefracture2012 | Liu *et al.*(6인 명기), *ACS Nano* 6, 1522 (2012) | 10.1021/nn204476h | 일치 | V1021-B″ | 부록D·S1 = 2 |
| 69 | 15 | obrovac_chevrier2014 | Obrovac·Chevrier, *Chem. Rev.* 114, 11444 (2014) | 10.1021/cr500207g | 일치 | V1021-B″ | 부록D(2)·S1·S2·S3·S4 = 6 |
| 70 | 16 | verbrugge_lisi2016 | Verbrugge·Baker·Xiao, *JES* 163, A262 (2016) | 10.1149/2.0581602jes | 일치(online 2015·print 2016) | V1021-B″ | 부록D(3)·S1(3)·S2b(1) = 7 |
| 71 | 17 | jiang_sihys2020 | Jiang·Offer·Jiang·Marinescu·Wang, *JES* 167, 130533 (2020) | 10.1149/1945-7111/abbbba | 일치 | V1021-B″ | 부록D·S1·S4 = 3 |
| 72 | 18 | larchecahn1973 | Larché·Cahn, *Acta Metall.* 21, 1051 (1973) | 10.1016/0001-6160(73)90021-7 | 일치 | V1021-B″ | 부록D(1)·S4(2) = 3 |
| 73 | 19 | koebbing2024 | Köbbing·Latz·Horstmann, *AFM* 2308818 — 권·호 공란 | 10.1002/adfm.202308818 | **R-03**(34(7)) | V1021 조건부→V1022 해소 | 부록D·S1·S4 = 3 |
| 74 | 22 | wang_asi2013 | Wang *et al.*(11인 명기), *Nano Lett.* 13, 709 (2013) | 10.1021/nl304379k | 일치 | V1022-R2+ | S2(1) |
| 75 | 23 | mcdowell_coreshell2013 | McDowell *et al.*(7인 명기), *Nano Lett.* 13, 758 (2013) | 10.1021/nl3044508 | 일치 | V1022-R2+ | S2(1) |
| 76 | 24 | ogata_nmr2014 | Ogata *et al.*(8인 명기), *Nat. Commun.* 5, 3217 (2014) | 10.1038/ncomms4217 | 일치 | V1022-R2+ | S1·S2·S2b = 3 |
| 77 | 25 | miyachi_sio2005 | Miyachi *et al.*(5인 명기), *JES* 152, A2089 (2005) | 10.1149/1.2013210 | 일치 | V1022-R2+ | S2(1) |
| 78 | 26 | kitada_sio2019 | Kitada *et al.*(6인 명기), *JACS* 141, 7014 (2019) | 10.1021/jacs.9b01589 | 일치 | V1022-R2+ | S2(3) |
| 79 | 27 | zhang_sio2018 | Zhang *et al.*(7인 명기), *JES* 165, A2102 (2018) | 10.1149/2.0431810jes | 일치 | V1022-R2+ | S2(2) |
| 80 | 28 | yom_sio2016 | Yom·Hwang·Cho·Yoon, *JPS* 311, 159 (2016) | 10.1016/j.jpowsour.2016.02.025 | 일치 | V1022-R2+ | S2(2) |
| 81 | 29 | andersen_sic2019 | Andersen *et al.*(9인 명기), *Sci. Rep.* 9, 14814 (2019) | 10.1038/s41598-019-51324-4 | 일치 | V1022-R2+ | S2(4) |
| 82 | 30 | naboka_sic2021 | Naboka·Yim·Abu-Lebdeh, *ACS Omega* 6, 2644 (2021) | 10.1021/acsomega.0c04811 | 일치 | V1022-R2+ | S2(4)·S3(1) = 5 |
| 83 | 31 | lee_sic2025 | Lee *et al.*(14인 명기), *Adv. Energy Mater.* e04250 (2025) — 권 공란 | 10.1002/aenm.202504250 | 일치(Crossref 도 권 미기재) | V1022-R2+ | S2(1) |
| 84 | 32 | bohm_entropy2024 | Böhm *et al.*(6인 명기), *Energies* 17, 5790 (2024) | 10.3390/en17225790 | 일치 | V1022-R2+ | S2(1) |
| 85 | 33 | arnot_calorimetry2021 | Arnot·Allcorn·Harrison, *JES* 168, 110509 (2021) | 10.1149/1945-7111/ac315c | 일치 | V1022-R2+ | S2(1)·S4(1) = 2 |
| 86 | 34 | bohm_thermal2025 | Böhm *et al.*(5인 명기), *JES* 172, 050537 (2025) | 10.1149/1945-7111/adda7a | 일치 | V1022-R2+ | S2(1) |
| 87 | 35 | wojtala_entropy2022 | Wojtala *et al.*(8인 명기), *JES* 169, 100527 (2022) | 10.1149/1945-7111/ac87d1 | 일치 | V1022-R2+ | S2(1) |
| 88 | 36 | gautam_blend2024 | Gautam *et al.*(7인 명기), *ACS AMI* 16, 45809 (2024) | 10.1021/acsami.4c10178 | 일치 | V1022-R2+ | S2(1)·S5(1) = 2 |
| 89 | 37 | ai_composite2022 | Ai·Kirkaldy·Jiang·Offer·Wang·Wu, *JPS* 527, 231142 (2022) | 10.1016/j.jpowsour.2022.231142 | 일치 | V1022-R2+ | S3(3) |
| 90 | 38 | chatzogiannakis_blend2025 | Chatzogiannakis *et al.*(6인 명기), *Batteries & Supercaps* 8, e202500104 (2025) | 10.1002/batt.202500104 | 일치 | V1022-R2+ | S3(2)·S5(1) = 3 |
| 91 | 39 | moyassari_blend2022 | Moyassari *et al.*(7인 명기), *JES* 169, 010504 (2022) | 10.1149/1945-7111/ac4545 | 일치 | V1022-R2+(사용자 등재 결정 2026-07-18) | S5(1) |
| 92 | 40 | zhan_siox2026 | Zhan *et al.*(6인 명기), *J. Energy Storage* 154, 121227 (2026) | 10.1016/j.est.2026.121227 | 일치 | V1022-R2+ | S3(2) |
| 93 | 41 | tu_blend2024 | Tu·Dao·Verbrugge·Koch, *JES* 171, 050539 (2024) | 10.1149/1945-7111/ad4823 | 일치 | V1022-R2+ | S2b(1)·S3(1) = 2 |
| 94 | 42 | artrith2018 | Artrith·Urban·Ceder, *JCP* 148, 241711 (2018) | 10.1063/1.5017661 | 일치 | **미등재** | S2b(2) |
| 95 | 43 | verbrugge2017 | (#44 와 동일 텍스트 — 동일 제목 오류 R-01) | — | — | 미등재 | Ch3 빌드에서 S2b(1) |

### 2.4 bib 키가 아닌 참고문헌 — 부록(상분리) 수동 번호 [확정]

`appendix_phase_separation.tex` lines 485–494: [A1] Cahn·Hilliard, *JCP* 28, 258 (1958), DOI 10.1063/1.1744102 · [A2] Cahn, *Acta Metall.* 9, 795 (1961), DOI 10.1016/0001-6160(61)90182-1 · [A3] Porter·Easterling, *Phase Transformations in Metals and Alloys* 2nd ed. (1992) · [A4] Hillert, *Phase Equilibria, Phase Diagrams and Phase Transformations* 2nd ed. (2008) · [A5] Balluffi·Allen·Carter, *Kinetics of Materials* (2005) Ch. 18–19. [A1]·[A2] DOI 는 Crossref 재확인 일치(2026-09-03). 원장 판정은 V1020 D(lines 50–54, ISBN 포함). v2.0.0 에서 통합 bib 로 갈 경우 이 5건은 키화 대상이다.

---

## 3. 절별 인용 밀도 [확정 — 기계 카운트] · 진단 [추정]

`_sections` 본문 파일별 줄수와 `\cite` 명령 수. 밀도 = 명령 수 / 100줄. 진단 열은 절 제목과 인용 키 분포에서 읽은 본 에이전트의 판단이며, 본문 전문 정독 없이 내린 것이므로 작업 챕터 2.4(서지 감사)에서 재검증돼야 한다.

| 파일 | 절 | 줄 | cite | 밀도 | 진단 |
|---|---|---|---|---|---|
| ch1_sec00_intro | Ch1 서론 | 85 | 2 | 2.4 | 정상 |
| ch1_sec01_n0n1 | §1 기호·매핑·분극 | 228 | 8 | 3.5 | 정상(GITT 원전·Reynier 앵커) |
| ch1_sec02a_part0 | §2 Part 0 앙상블·단일자리·lattice gas | 366 | 7 | 1.9 | 교재 앵커(Hill·McQuarrie·Fowler·McKinnon)만. Langmuir 원전·요동 정리(Kubo) 부재 |
| ch1_sec02b_part0 | §2 Part 0 평균장·전기화학 연결·다클래스·거시 | 449 | 3 | 0.7 | **저밀도**. 정칙용액·이중웰·Legendre 반전을 다루면서 Bragg–Williams·Hildebrand·Lee–Yang·Callen 류 원전 0 |
| ch1_sec03_center | §3 평형 중심 U_j(T) | 115 | 0 | 0 | **무인용**. 열역학 유도(G·μ·Nernst·온도 환산) — 교재(Newman·Callen)·ΔS 실측 원전 필요 |
| ch1_sec04_hys | §4 히스테리시스 분기 중심 | 326 | 3 | 0.9 | **저밀도**. spinodal 27회·핵생성/CNT 8회 언급에 인용은 Dreyer 2건뿐. Cahn 1961·[A3]/[A5]·Kramers·CNT 원전 부재 |
| ch1_sec05_width | §5 ξ_eq·폭 w_j | 401 | 6 | 1.5 | TST(Eyring·Glasstone·Laidler)·Bazant 는 있음. Butler–Volmer 원전(Butler 1924·Erdey-Grúz–Volmer 1930)·Marcus 부재 |
| ch1_sec05b_gr2L | §5b stage-2L | 225 | 12 | 5.3 | 정상. Daumas–Hérold 이름만(line 98) — 원전 또는 리뷰(Dresselhaus 1981) 인용 없음 |
| ch1_sec06_eqpeak | §6 평형 peak(감수율 11회) | 125 | 0 | 0 | **무인용**. 요동–응답(감수율) 서술에 Kubo 1966·Hill 등 앵커 0 |
| ch1_sec07_broadening | §7 두-상 broadening | 357 | 15 | 4.2 | 정상(CLT 서술에 확률론 교재 앵커는 없음) |
| ch1_sec08_lag | §8 동역학 지연 L_V(affinity 3회) | 142 | 0 | 0 | **무인용**. affinity·전달계수·유효 장벽 — de Groot–Mazur/Kondepudi–Prigogine·Bazant 2013 재인용 필요 |
| ch1_sec09_tail | §9 인과 기억 꼬리 | 240 | 0 | 0 | **무인용**. 기억 적분·완화 — Kubo 선형응답·(scope-out 재개방 시) KWW 원전 |
| ch1_sec10_sum | §10 합산·staging 초기값 | 174 | 7 | 4.0 | 정상 |
| ch1_sec11_lcointro | L11 LCO 도입 | 164 | 8 | 4.9 | 정상 |
| ch1_sec12_lcocenter | L12 LCO 중심·∂U/∂T | 105 | 2 | 1.9 | 보통. Hudak 2015·Viswanathan 2010 dU/dT 실측 추가 후보 |
| ch1_sec13_lcohys | L13 order–disorder·MIT 2상역 | 211 | 13 | 6.2 | 정상. Wolverton–Zunger 1998·Chen–Lu–Dahn 2002 추가 후보 |
| ch1_sec14_lcodecomp | L14 반응 엔트로피 삼분해 | 136 | 3 | 2.2 | 보통 |
| ch1_sec15_lcoelec | L15 전자 엔트로피(Mott 15·Sommerfeld 8) | 375 | 20 | 5.3 | 정상 |
| ch1_sec16_lcopeak | L16 LCO peak | 64 | 1 | 1.6 | 보통. Ohzuku–Ueda 1994·Amatucci 1996 추가 후보 |
| ch1_sec16b_lcoomega | L16b per-peak Ω | 150 | 8 | 5.3 | 정상 |
| ch1_sec17_msmr | L17 MSMR 동형 | 172 | 6 | 3.5 | 정상. Baker–Verbrugge 2012 추가 후보 |
| ch1_sec18_inputs | §18 입력·요약 | 85 | 0 | 0 | 요약 절 — 무인용 허용 [추정] |
| ch2_sec00_intro | Part T 서 | 64 | 0 | 0 | 도입 절 — 교재 앵커 1건 권장 |
| ch2_sec01_partition | T1 격자기체 분배함수 | 141 | 3 | 2.1 | Bragg–Williams 3회 언급에 원전 0 |
| ch2_sec02_config | T2 config 엔트로피 | 178 | 7 | 3.9 | 정상 |
| ch2_sec03_vibel | T3 vib/el 엔트로피 | 110 | 5 | 4.5 | 정상 |
| ch2_sec04_einstein | T4 Einstein 진동 | 198 | 1 | 0.5 | **저밀도**. Einstein 모형 교재 앵커(Hill·Ashcroft–Mermin) 필요 |
| ch2_sec05_mixing | T5 섞임·겹침(entropy production 1회) | 243 | 6 | 2.5 | 보통 |
| ch2_sec06_limits | T6 극한·코너 | 47 | 0 | 0 | 검산 절 — 무인용 허용 [추정] |
| ch2_sec07_revheat | T7 가역 발열 | 94 | 5 | 5.3 | 정상. Thomas–Newman 2003·Rao–Newman 1997 추가 후보 |
| ch2_sec08_synthesis | T8 종합식·예제 | 224 | 1 | 0.4 | 계산 절 — 저밀도 허용 [추정] |
| ch2_sec09_method | T9 방법론 출구 | 59 | 6 | 10.2 | 정상 |
| ch2_sec10_closing | Part T 맺음 | 26 | 0 | 0 | 허용 |
| ch3v22_sec01_map | S1 Si 접목 지도 | 117 | 15 | 12.8 | 정상 |
| ch3v22_sec02_cases | S2 케이스별 활물질 | 164 | 33 | 20.1 | 최고 밀도(R5 신규 19종 집중) |
| ch3v22_sec02b_sifr | S2b Si-host 정칙용액(Frumkin 19회) | 210 | 7 | 3.3 | Frumkin 1925 원전 부재 |
| ch3v22_sec03_blend | S3 혼합 음극 대정준 반전 | 265 | 10 | 3.8 | 정상 |
| ch3v22_sec04_mech | S4 기계 히스(Larché–Cahn 6회) | 102 | 9 | 8.8 | 정상. Bower–Guduru–Sethuraman 2011 추가 후보 |
| ch3v22_sec05_code | S5 코드 요구명세 | 63 | 3 | 4.8 | 부록성 |
| 부록 A/B/D/E · ch2_app A/B | — | 84/178/84/203/72/71 | 1/0/17/8/0/1 | — | 코드맵·검산표 무인용은 성격상 허용 [추정] |

요약하면 **무인용 본문 절 4개(§3·§6·§8·§9, 합 622줄)** 와 **저밀도 절 3개(§2b·§4·T4, 합 973줄)** 가 모두 Ch1 의 **이론 유도 층**에 몰려 있다. 재료 실측 층(§5b·§7·L13·L15·S1·S2)은 이미 리뷰급 밀도다. 즉 v2.0.0 서지 작업의 무게중심은 신규 실측 문헌 수집이 아니라 **이론 원전·교재 앵커의 체계적 보강**이다.

---

## 4. 주제별 필수 문헌 체크리스트

각 표의 열: **문헌** · **현행 bib**(O = 키 존재 / △ = 원장에만 또는 부록 수동번호 / X = 없음) · **DOI·검증**(Crossref 확인 2026-09-03 = 본 에이전트가 DOI 조회로 제목·저자·저널·연도 일치를 확인 / 서적 = DOI 없음·ISBN 미대조 [미검증] / 미검증) · **현행 인용 절**(있으면) · **v2.0.0 배치**(brief §5 작업 챕터 4 의 Phase: 4.1 열역학·통계역학 기초 / 4.2 평형 열역학 / 4.3 동역학 / 4.4 열특성 / 4.5 히스테리시스 / 4.6 흑연 / 4.7 LCO / 4.8 Si·블렌드 / 4.9 부록) · **성격**(원전 = 1차 / 교재 / 리뷰). "필수" 판정은 본 에이전트 판단[추정]이며 사용자 기준 ③·⑤ 를 축으로 삼았다. 서지 표기는 Crossref 응답을 그대로 옮긴 것이고, 서적은 저자·서명·출판사·연도만 적는다(쪽수·ISBN 은 실물 대조 전이라 적지 않음).

### 4.1 통계역학 기초 (앙상블·분배함수·요동)

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| T. L. Hill, *An Introduction to Statistical Thermodynamics* (Addison-Wesley 1960; Dover 1986) | O `hill1960` | 서적 | §2a·§2b | 4.1 | 교재 |
| D. A. McQuarrie, *Statistical Mechanics* (Harper & Row 1976) | O `mcquarrie1976` | 서적 | §2a·§2b·§5 | 4.1 | 교재 |
| R. H. Fowler, E. A. Guggenheim, *Statistical Thermodynamics* (CUP 1939) | O `fowler1939` | 서적 | §2a | 4.1 | 교재(원전급) |
| D. Chandler, *Introduction to Modern Statistical Mechanics* (Oxford UP 1987) | X | 서적 [미검증] | — | 4.1(앙상블·요동·평균장) | 교재 |
| L. D. Landau, E. M. Lifshitz, *Statistical Physics, Part 1* 3rd ed. (Pergamon 1980) | X | 서적 [미검증] | — | 4.1(요동·상전이 일반론) | 교재 |
| H. B. Callen, *Thermodynamics and an Introduction to Thermostatistics* 2nd ed. (Wiley 1985) | X | 서적 [미검증] | — | 4.1(Legendre 변환·안정성 조건·Maxwell 관계 — §2b 대정준 반전·SURV Tier3 Legendre 노트) | 교재 |
| R. Kubo, "Statistical-Mechanical Theory of Irreversible Processes. I," *J. Phys. Soc. Jpn.* 12, 570–586 (1957) | X | 10.1143/JPSJ.12.570 Crossref 확인 | — | 4.1/4.3(선형응답 — 전달함수 H(ω) 의 통계역학 자리) | 원전 |
| R. Kubo, "The fluctuation-dissipation theorem," *Rep. Prog. Phys.* 29, 255–284 (1966) | X | 10.1088/0034-4885/29/1/306 Crossref 확인 | — | 4.1(SM2-A 감수율 항등 (dQ/dV)^eq = e²∂⟨N⟩/∂μ 의 앵커 — `SM2_SURVEY.md` lines 62–78) | 원전·리뷰 |
| H. B. Callen, T. A. Welton, "Irreversibility and Generalized Noise," *Phys. Rev.* 83, 34–40 (1951) | X | 10.1103/PhysRev.83.34 Crossref 확인 | — | 4.1 각주 | 원전 |
| I. Langmuir, "The adsorption of gases on plane surfaces of glass, mica and platinum," *JACS* 40, 1361–1403 (1918) | X | 10.1021/ja02242a004 Crossref 확인 | — | 4.1(단일 자리 등온선 원전 — §2a Langmuir 2회 언급) | 원전 |
| T. D. Lee, C. N. Yang, "Statistical Theory of Equations of State and Phase Transitions. II. Lattice Gas and Ising Model," *Phys. Rev.* 87, 410–419 (1952) | X | 10.1103/PhysRev.87.410 Crossref 확인 | — | 4.1(lattice gas ↔ Ising 대응 — 정칙용액 Ω 의 자리) | 원전 |
| E. Ising, "Beitrag zur Theorie des Ferromagnetismus," *Z. Phys.* 31, 253–258 (1925) | X | 10.1007/BF02980577 Crossref 확인 | — | 4.1 각주 | 원전 |
| N. W. Ashcroft, N. D. Mermin, *Solid State Physics* (1976) | O `ashcroftmermin1976` | 서적 | §2a | 4.4/4.7(Sommerfeld 전개·Einstein 모형) | 교재 |
| R. K. Pathria, P. D. Beale, *Statistical Mechanics* 3rd ed. (Elsevier 2011) | X | 서적 [미검증] | — | 4.1(선택) | 교재 |

### 4.2 격자기체 · 정칙용액 · 상분리 (Cahn–Hilliard · Bazant 계열)

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| W. R. McKinnon, R. R. Haering, "Physical Mechanisms of Intercalation," *Mod. Aspects Electrochem.* 15, 235–304 (1983) | O `mckinnon1983` | 없음(장) | §2a | 4.2 | 원전(삽입 lattice gas) |
| R. A. Huggins, *Advanced Batteries* (Springer 2009) | O `huggins2009` | 서적 | T1 | 4.2 | 교재 |
| W. L. Bragg, E. J. Williams, "The effect of thermal agitation on atomic arrangement in alloys," *Proc. R. Soc. A* 145, 699–730 (1934) | X | 10.1098/rspa.1934.0132 Crossref 확인 | — (본문 Bragg–Williams 5회 언급: §2b·T1·T2) | 4.2(평균장 원전) | 원전 |
| J. H. Hildebrand, "Solubility. XII. Regular solutions," *JACS* 51, 66–80 (1929) | X | 10.1021/ja01376a009 Crossref 확인 | — (정칙/정규용액 47회 언급) | 4.2(정칙용액 명명 원전) | 원전 |
| E. A. Guggenheim, *Mixtures* (Oxford UP 1952) | X | 서적 [미검증] | — | 4.2(quasi-chemical·정칙용액 교재) | 교재 |
| O. Redlich, A. T. Kister, "Algebraic Representation of Thermodynamic Properties and the Classification of Solutions," *Ind. Eng. Chem.* 40, 345–348 (1948) | X | 10.1021/ie50458a036 Crossref 확인 | — (Redlich 0회) | 4.2(Ω(ξ) 확장 — brief §4.5 로드맵 제안 2·`LIT_ADVANCE_SYNTHESIS.md` line 21) | 원전 |
| A. Frumkin, "Die Kapillarkurve der höheren Fettsäuren und die Zustandsgleichung der Oberflächenschicht," *Z. Phys. Chem.* 116U, 466–484 (1925) | X | 10.1515/zpch-1925-11629 Crossref 확인 | — (Frumkin 22회, S2b 19회) | 4.2/4.8(Frumkin 등온선 원전) | 원전 |
| M. D. Levi, D. Aurbach, "Frumkin intercalation isotherm…," *Electrochim. Acta* 45, 167 (1999) | O `leviaurbach1999` | 확인 | §7 | 4.2/4.6 | 리뷰 |
| J. W. Cahn, J. E. Hilliard, "Free Energy of a Nonuniform System. I," *JCP* 28, 258–267 (1958) | △ [A1] | 10.1063/1.1744102 Crossref 확인 | 부록(상분리) | 4.2/4.5(키화) | 원전 |
| J. W. Cahn, "On spinodal decomposition," *Acta Metall.* 9, 795–801 (1961) | △ [A2] | 10.1016/0001-6160(61)90182-1 Crossref 확인 | 부록(상분리) | 4.2/4.5(§4 spinodal 27회 언급의 원전) | 원전 |
| D. A. Porter, K. E. Easterling, *Phase Transformations in Metals and Alloys* 2nd ed. (1992) | △ [A3] | 서적(V1020-D ISBN) | 부록 | 4.2/4.5 | 교재 |
| M. Hillert, *Phase Equilibria, Phase Diagrams and Phase Transformations* 2nd ed. (CUP 2008) | △ [A4] | 서적(V1020-D ISBN) | 부록 | 4.2 | 교재 |
| R. W. Balluffi, S. M. Allen, W. C. Carter, *Kinetics of Materials* (Wiley 2005) | △ [A5] | 서적(V1020-D ISBN) | 부록 | 4.2/4.5 | 교재 |
| G. K. Singh, G. Ceder, M. Z. Bazant, "Intercalation dynamics in rechargeable battery materials: General theory and phase-transformation waves in LiFePO4," *Electrochim. Acta* 53, 7599–7613 (2008) | X | 10.1016/j.electacta.2008.03.083 Crossref 확인 | — | 4.2/4.5(삽입 상분리 일반론) | 원전 |
| D. A. Cogswell, M. Z. Bazant, *ACS Nano* 6, 2215 (2012) | O `cogswell2012` | 확인 | §7 | 4.2 | 원전 |
| P. Bai, D. A. Cogswell, M. Z. Bazant, "Suppression of Phase Separation in LiFePO4 Nanoparticles During Battery Discharge," *Nano Lett.* 11, 4890–4896 (2011) | X | 10.1021/nl202764f Crossref 확인 | — | 4.5(율의존 두-상/고용체 — `LIT_ADVANCE_SYNTHESIS.md` §2) | 원전 |
| D. A. Cogswell, M. Z. Bazant, "Theory of Coherent Nucleation in Phase-Separating Nanoparticles," *Nano Lett.* 13, 3036–3041 (2013) | X | 10.1021/nl400497t Crossref 확인 | — | 4.5(핵생성) | 원전 |
| T. R. Ferguson, M. Z. Bazant, "Nonequilibrium Thermodynamics of Porous Electrodes," *JES* 159, A1967–A1985 (2012) | X | 10.1149/2.048212jes Crossref 확인 | — | 4.3/4.5(비평형 열역학 골격 — 다공전극은 Non-goal 경계 표기용) | 원전 |
| R. B. Smith, M. Z. Bazant, "Multiphase Porous Electrode Theory," *JES* 164, E3291–E3310 (2017) | X | 10.1149/2.0171711jes Crossref 확인 | — | 4.3(선택·경계 표기) | 원전 |
| M. Z. Bazant, "Thermodynamic stability of driven open systems and control of phase separation by electro-autocatalysis," *Faraday Discuss.* 199, 423–463 (2017) | X | 10.1039/C7FD00037E Crossref 확인 | — | 4.5(선택) | 원전 |
| A. Van der Ven, Z. Deng, S. Banerjee, S. P. Ong, "Rechargeable Alkali-Ion Battery Materials: Theory and Computation," *Chem. Rev.* 120, 6977–7019 (2020) | X | 10.1021/acs.chemrev.9b00601 Crossref 확인 | — | 4.2 리뷰 앵커 | 리뷰 |
| A. Van der Ven, J. Bhattacharya, A. A. Belak, "Understanding Li Diffusion in Li-Intercalation Compounds," *Acc. Chem. Res.* 46, 1216–1225 (2013) | X | 10.1021/ar200329r Crossref 확인 | — | 4.3(cluster expansion·확산) | 리뷰 |
| A. Yao, V. Viswanathan, "Open-Circuit Voltage Models Should Be Thermodynamically Consistent," *JPCL* 15, 1143–1151 (2024) | X | 10.1021/acs.jpclett.3c03129 Crossref 확인 | — (`LIT_ADVANCE_SYNTHESIS.md` line 21·128 에 서지) | 4.2(정칙용액+공통접선 OCV — 헤드라인 G3/M1) | 원전 |
| D. K. Karthikeyan, G. Sikha, R. E. White, "Thermodynamic model development for lithium intercalation electrodes," *JPS* 185, 1398–1407 (2008) | X | 10.1016/j.jpowsour.2008.07.077 Crossref 확인 | — (`LIT_ADVANCE_SYNTHESIS.md` line 128) | 4.2(Redlich–Kister OCV 모델 선례) | 원전 |

### 4.3 흑연 staging (Dahn · Ohzuku · Safran · Daumas–Hérold)

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| J. R. Dahn, *PRB* 44, 9170 (1991) | O `dahn1991` | 확인 | 12회 | 4.6 | 원전 |
| T. Ohzuku *et al.*, *JES* 140, 2490 (1993) | O `ohzuku1993` | 확인 | 9회 | 4.6 | 원전 |
| J. R. Dahn *et al.*, *Science* 270, 590 (1995) | O `dahn1995` | 확인 | §7 | 4.6 | 원전 |
| J. R. Dahn, R. Fong, M. J. Spoon, "Suppression of staging in lithium-intercalated carbon by disorder in the host," *PRB* 42, 6424–6432 (1990) | X | 10.1103/PhysRevB.42.6424 Crossref 확인 | — | 4.6(무질서→staging 억제 — `dahn1995` 의 물리 근거) | 원전 |
| R. Fong, U. von Sacken, J. R. Dahn, "Studies of Lithium Intercalation into Carbons Using Nonaqueous Electrochemical Cells," *JES* 137, 2009–2013 (1990) | X | 10.1149/1.2086855 Crossref 확인 | — | 4.6(전기화학 흑연 삽입 원전) | 원전 |
| N. Daumas, A. Hérold, *C. R. Acad. Sci. Paris C* 268, 373 (1969) | X | DOI [미검증] (Gallica 등 실물 확인 필요) | §5b line 98 이름만 | 4.6(교대충전 모형 원전 — 확보 불가 시 Dresselhaus 1981 로 대체 인용) | 원전 |
| S. A. Safran, D. R. Hamann, "Long-Range Elastic Interactions and Staging in Graphite Intercalation Compounds," *PRL* 42, 1410–1413 (1979) | X | 10.1103/PhysRevLett.42.1410 Crossref 확인 | — | 4.6/4.2(staging 이론 원전) | 원전 |
| S. A. Safran, "Phase Diagrams for Staged Intercalation Compounds," *PRL* 44, 937–940 (1980) | △ 원장 V1(`safran1980`), bib 없음 | 10.1103/PhysRevLett.44.937 Crossref 확인 | — | 4.6 | 원전 |
| S. A. Safran, "Stage Ordering in Intercalation Compounds," *Solid State Phys.* 40, 183–246 (1987) | △ 원장 V2(`safran1987`) | 10.1016/S0081-1947(08)60692-X Crossref 확인(응답에 권 미기재 — V1020 line 36 "Crossref 권 오기탁" 과 정합, 인쇄본 40) | — | 4.6 리뷰 | 리뷰 |
| M. S. Dresselhaus, G. Dresselhaus, "Intercalation compounds of graphite," *Adv. Phys.* 30, 139–326 (1981) | X | 10.1080/00018738100101367 Crossref 확인 | — | 4.6 리뷰 앵커(staging·Daumas–Hérold 총람) | 리뷰 |
| D. Billaud, B. Henry, M. Lelaurain, P. Willmann, "Revisited structures of dense and dilute stage II lithium-graphite intercalation compounds," *J. Phys. Chem. Solids* 57, 775–781 (1996) | X | 10.1016/0022-3697(95)00348-7 Crossref 확인(저자 4인은 응답 앞 4인 — 전원 여부는 등재 시 재조회) | — | 4.6(stage 2 / 2L 구조 — §5b·brief §4.4 "두-상 4 vs 2 표기(Dahn 1991 본문 확인)" 보조) | 원전 |
| K. Persson *et al.*, *JPCL* 1, 1176 (2010) · *PRB* 82, 125416 (2010) | O ×2 | 확인 | §5b·§10 | 4.6 | 원전 |
| J. Schmitt *et al.* → C. Schmitt *et al.*, *ChemElectroChem* 9, e202101342 (2022) | O `schmitt2022`(R-02) | 확인 | §5b | 4.6 | 원전 |
| J. H. Park *et al.*, *Materials* 14, 4683 (2021) | O `park2021` | 확인 | §7 | 4.6 | 원전 |
| Y. Reynier, R. Yazami, B. Fultz, *JPS* 119–121, 850 (2003) | O `reynier2003` | 확인 | 7회 | 4.4/4.6 | 원전 |
| M. P. Mercer *et al.*, *Electrochim. Acta* 324, 134774 (2019) | O `occupation2019` | 확인 | T2 | 4.6 | 원전(방법 수준) |
| D. R. Baker, M. W. Verbrugge, "Intercalate Diffusion in Multiphase Electrode Materials and Application to Lithiated Graphite," *JES* 159, A1341–A1350 (2012) | X | 10.1149/2.002208jes Crossref 확인 | — | 4.6/4.3(다상 흑연 확산·MSMR 계보) | 원전 |
| M. W. Verbrugge, B. J. Koch, "Electrochemical analysis of lithiated graphite anodes," *JES* 150, A374 (2003) | X | [미검증] — 기억 후보 DOI 10.1149/1.1553790 은 Crossref 에서 **다른 논문**(Marselli *et al.*)으로 해소됨. 서지 자체도 미확정 | — | 4.6(선택) | 원전(?) |
| M. D. Levi, D. Aurbach, "The mechanism of lithium intercalation in graphite film electrodes in aprotic media. Part 1," *J. Electroanal. Chem.* 421, 79–88 (1997) | X | 10.1016/S0022-0728(96)04832-2 Crossref 확인 | — | 4.6(SSCV·PITT 흑연 staging 전기화학) | 원전 |
| H. Onuma *et al.*, *J. Mater. Chem. A* 9, 11187 (2021) | O `rsc2021` | 확인 | §7 | 4.6(비교 인용 유지) | 원전(K-흑연) |

### 4.4 MSMR (Multi-Species, Multi-Reaction — Verbrugge · Baker)

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| M. W. Verbrugge, D. R. Baker, B. J. Koch, X. Xiao, W. Gu, "Thermodynamic Model for Substitutional Materials: Application to Lithiated Graphite, Spinel Manganese Oxide, Iron Phosphate, and Layered Nickel-Manganese-Cobalt Oxide," *JES* 164, E3243–E3253 (2017) | O ×2 (`msmr_origin2017` 정확 / `verbrugge2017` 제목 오류 — R-01) | 10.1149/2.0341708jes 확인 | L11·L17·§5b·S2b | 4.2/4.6/4.7(키 1개로 통합) | 원전 |
| D. R. Baker, M. W. Verbrugge, "Multi-Species, Multi-Reaction Model for Porous Intercalation Electrodes: Part I," *JES* 165, A3952 (2018) | O `bakerverbrugge2018` | 확인 | L17 | 4.2 | 원전(명명) |
| D. R. Baker, M. W. Verbrugge, *JES* 159, A1341 (2012) | X | 확인(§4.3 표) | — | 4.6 | 원전 |
| M. W. Verbrugge, D. R. Baker, X. Xiao, *JES* 163, A262 (2016) — Li–Si | O `verbrugge_lisi2016` | 확인 | 부록D·S1·S2b | 4.8 | 원전 |
| A. Paul *et al.*, *ECS Adv.* 3, 042501 (2024) Part 1 · *JES* 171, 103505 (2024) Part II | O `msmr2024`·`msmr_partII` | 확인 | L11·L17·T2·T9 | 4.4/4.6 | 원전(온도-MSMR) |
| T. R. Garrick *et al.*, *JES* 171, 023502 (2024) | O `msmr_partI` | 확인 | T3·T7·T9 | 4.4 | 원전 |
| M. Tu, T. Dao, M. W. Verbrugge, B. Koch, *JES* 171, 050539 (2024) | O `tu_blend2024` | 확인 | S2b·S3 | 4.8 | 원전 |

### 4.5 엔트로피 · 가역열 (Reynier · Thomas–Newman · Bernardi)

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| D. Bernardi, E. Pawlikowski, J. Newman, *JES* 132, 5 (1985) | O `bernardi1985` | 확인 | T7·T9 | 4.4 | 원전 |
| L. Rao, J. Newman, "Heat-Generation Rate and General Energy Balance for Insertion Battery Systems," *JES* 144, 2697–2704 (1997) | X | 10.1149/1.1837884 Crossref 확인 | — | 4.4(Bernardi 의 삽입 전극 확장) | 원전 |
| K. E. Thomas, J. Newman, "Thermal Modeling of Porous Insertion Electrodes," *JES* 150, A176 (2003) | X | 10.1149/1.1531194 Crossref 확인 | — | 4.4(가역열·엔트로피 항의 표준 정식화) | 원전 |
| K. E. Thomas, C. Bogatu, J. Newman, "Measurement of the Entropy of Reaction as a Function of State of Charge in Doped and Undoped Lithium Manganese Oxide," *JES* 148, A570 (2001) | X | 10.1149/1.1369365 Crossref 확인 | — | 4.4(∂U/∂T 측정법 원전) | 원전 |
| W. B. Gu, C. Y. Wang, "Thermal-Electrochemical Modeling of Battery Systems," *JES* 147, 2910 (2000) | X | 10.1149/1.1393625 Crossref 확인 | — | 4.4(선택) | 원전 |
| V. V. Viswanathan *et al.*, "Effect of entropy change of lithium intercalation in cathodes and anodes on Li-ion battery thermal management," *JPS* 195, 3720–3729 (2010) | X | 10.1016/j.jpowsour.2009.11.103 Crossref 확인 | — | 4.4/4.6/4.7(흑연·LCO 등 ΔS(x) 실측 총람) | 원전 |
| J. Newman, K. E. Thomas-Alyea, *Electrochemical Systems* 3rd ed. (Wiley 2004) | O `newman` | 서적 | T1·T7 | 4.3/4.4 | 교재 |
| Y. Reynier *et al.*, *JPS* 119–121, 850 (2003) · *PRB* 70, 174304 (2004) | O ×2 | 확인 | 7회·11회 | 4.4/4.6/4.7 | 원전 |
| N. S. Hudak, L. E. Davis, G. Nagasubramanian, "Cycling-Induced Changes in the Entropy Profiles of Lithium Cobalt Oxide Electrodes," *JES* 162, A315–A321 (2015) | X | 10.1149/2.0071503jes Crossref 확인(online 2014·print 2015) | — (`LIT_ADVANCE_SYNTHESIS.md` L3·line 128) | 4.7(LCO dU/dT 시드) | 원전 |
| D. Allart *et al.*, *JES* 165, A380 (2018) | O `allart2018` | 확인 | T2·T9 | 4.4/4.6 | 원전 |
| A. Świderska-Mocek *et al.*, *PCCP* 21, 2115 (2019) | O `swiderska2019` | 확인 | §1·L12·부록A | 4.4/4.7 | 원전 |
| A. Hales, J. Bulman, *JES* 171, 050535 (2024) | O `standardised2024` | 확인 | T7·T8 | 4.4 | 원전 |
| I. Zilberman *et al.*, *JPS* 395, 179 (2018) | O `hysteresis2018` | 확인 | T5·T9 | 4.4/4.5 | 원전 |
| S. W. Baek *et al.*, *JPCC* 126, 6096 (2022) | O `baek_pilon2022` | 확인 | §1 | 4.4 해석 지도 | 리뷰 |
| W. Weppner, R. A. Huggins, *JES* 124, 1569 (1977) | O `weppner_huggins1977` | 확인 | §1 | 4.3(GITT) | 원전 |
| H. J. Kim *et al.*, *EES* 13, 286 (2020) | O `kim_entropymetry2020` | 확인 | L11 | 4.7 | 원전 |
| J. Haruyama *et al.*, *JPCC* 125, 27891 (2021) · S. Konar *et al.*, *Chem. Mater.* 27, 2566 (2015) | O ×2 | 확인 | T2·T3·T4 | 4.4 | 원전(abstract tier — 전문 확보 권장) |

### 4.6 전기화학 속도론 (Bard–Faulkner · Newman · Butler–Volmer · Marcus · Bazant MHC · Eyring)

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| H. Eyring, *JCP* 3, 107 (1935) | O `eyring1935` | 확인 | §5 | 4.3 | 원전 |
| S. Glasstone, K. J. Laidler, H. Eyring, *The Theory of Rate Processes* (McGraw-Hill 1941) | O `glasstone1941` | 서적 | §5 | 4.3 | 교재(원전급) |
| K. J. Laidler, M. C. King, *J. Phys. Chem.* 87, 2657 (1983) | O `laidlerking1983` | 확인 | §5 | 4.3 | 리뷰(사적) |
| M. Z. Bazant, *Acc. Chem. Res.* 46, 1144 (2013) | O `bazant2013` | 확인 | §5 | 4.3(BV·MHC·비평형 열역학 통합) | 리뷰·원전 |
| A. J. Bard, L. R. Faulkner, *Electrochemical Methods* 2nd ed. (Wiley 2001) | X | 서적 [미검증] | — | 4.3(BV·교환전류·전달계수 표준 교재) | 교재 |
| J. A. V. Butler, "Studies in heterogeneous equilibria. Part II.—The kinetic interpretation of the Nernst theory of electromotive force," *Trans. Faraday Soc.* 19, 729–733 (1924) | X | 10.1039/tf9241900729 Crossref 확인 | — | 4.3(BV 원전) | 원전 |
| T. Erdey-Grúz, M. Volmer, "Zur Theorie der Wasserstoff Überspannung," *Z. Phys. Chem.* 150A, 203–213 (1930) | X | 10.1515/zpch-1930-15020 Crossref 확인 | — | 4.3(BV 원전) | 원전 |
| R. A. Marcus, "On the Theory of Oxidation-Reduction Reactions Involving Electron Transfer. I," *JCP* 24, 966–978 (1956) | X | 10.1063/1.1742723 Crossref 확인 | — | 4.3 | 원전 |
| R. A. Marcus, "On the Theory of Electron-Transfer Reactions. VI. Unified Treatment for Homogeneous and Electrode Reactions," *JCP* 43, 679–701 (1965) | X | 10.1063/1.1696792 Crossref 확인 | — | 4.3(전극 반응으로의 확장) | 원전 |
| R. A. Marcus, "Electron transfer reactions in chemistry. Theory and experiment," *RMP* 65, 599–610 (1993) | X | 10.1103/RevModPhys.65.599 Crossref 확인 | — | 4.3 리뷰 앵커 | 리뷰 |
| C. E. D. Chidsey, "Free Energy and Temperature Dependence of Electron Transfer at the Metal-Electrolyte Interface," *Science* 251, 919–922 (1991) | X | 10.1126/science.251.4996.919 Crossref 확인 | — | 4.3(MHC 실증) | 원전 |
| P. Bai, M. Z. Bazant, "Charge transfer kinetics at the solid–solid interface in porous electrodes," *Nat. Commun.* 5, 3585 (2014) | X | 10.1038/ncomms4585 Crossref 확인 | — | 4.3(삽입 전극 MHC) | 원전 |
| Y. Zeng, R. B. Smith, P. Bai, M. Z. Bazant, "Simple formula for Marcus–Hush–Chidsey kinetics," *J. Electroanal. Chem.* 735, 77–83 (2014) | X | 10.1016/j.jelechem.2014.09.038 Crossref 확인 | — | 4.3(닫힌 근사식) | 원전 |
| D. Fraggedakis *et al.*, "Theory of coupled ion-electron transfer kinetics," *Electrochim. Acta* 367, 137432 (2021) | X | 10.1016/j.electacta.2020.137432 Crossref 확인 | — | 4.3(선택) | 원전 |
| H. A. Kramers, "Brownian motion in a field of force and the diffusion model of chemical reactions," *Physica* 7, 284–304 (1940) | X | 10.1016/S0031-8914(40)90098-2 Crossref 확인 | — (Kramers 0회) | 4.3/4.5(장벽 탈출·완화 — SURV Tier3 FPT/Kramers 노트) | 원전 |
| P. Hänggi, P. Talkner, M. Borkovec, "Reaction-rate theory: fifty years after Kramers," *RMP* 62, 251–341 (1990) | X | 10.1103/RevModPhys.62.251 Crossref 확인 | — | 4.3 리뷰 앵커(TST↔Kramers 통일) | 리뷰 |
| M. Planck, "Ueber die Erregung von Electricität und Wärme in Electrolyten," *Ann. Phys.* 275, 161–186 (1890) | X | 10.1002/andp.18902750202 Crossref 확인 | — (Nernst–Planck 0회) | 4.3(로드맵 제안 4 BV+Nernst–Planck 재개방 시 원전; Nernst 1888/1889 는 [미검증]) | 원전 |
| J. Newman, W. Tiedemann, "Porous-electrode theory with battery applications," *AIChE J.* 21, 25–41 (1975) · M. Doyle, T. F. Fuller, J. Newman, *JES* 140, 1526–1533 (1993) | X | 10.1002/aic.690210103 · 10.1149/1.2221597 Crossref 확인 | — | 4.3(Non-goal 다공전극 경계 표기용 — 본문 채택 아님) | 원전 |
| W. Weppner, R. A. Huggins (1977) | O | 확인 | §1 | 4.3 | 원전 |
| A. Fly, R. Chen, *J. Energy Storage* 29, 101329 (2020) | O `fly2020` | 확인 | §7 | 4.3/4.6(율의존 peak) | 원전 |

### 4.7 비가역 열역학 (de Groot–Mazur · Kondepudi–Prigogine · Onsager)

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| L. Onsager, "Reciprocal Relations in Irreversible Processes. I," *Phys. Rev.* 37, 405–426 (1931) · "II," *Phys. Rev.* 38, 2265–2279 (1931) | X | 10.1103/PhysRev.37.405 · 10.1103/PhysRev.38.2265 Crossref 확인 | — (Onsager 0회) | 4.3/4.4(flux–force 선형 영역 — brief 3.2 "일반 비평형 열역학 상태식(affinity·flux-force)") | 원전 |
| S. R. de Groot, P. Mazur, *Non-Equilibrium Thermodynamics* (North-Holland 1962; Dover 1984) | X | 서적 [미검증] | — | 4.3/4.4(entropy production·affinity 표준 교재) | 교재 |
| D. Kondepudi, I. Prigogine, *Modern Thermodynamics: From Heat Engines to Dissipative Structures* (Wiley 1998; 2nd ed. 2014) | X | 서적 [미검증] | — | 4.3/4.4(affinity A = −Σν_iμ_i·화학 반응의 entropy production) | 교재 |
| I. Prigogine, *Introduction to Thermodynamics of Irreversible Processes* 3rd ed. (Interscience 1967) | X | 서적 [미검증] | — | 4.4(선택) | 교재 |
| A. Latz, J. Zausch, "Thermodynamic consistent transport theory of Li-ion batteries," *JPS* 196, 3296–3302 (2011) | X | 10.1016/j.jpowsour.2010.11.088 Crossref 확인 | — | 4.4(Li-ion 에서의 entropy production 정식화) | 원전 |
| T. R. Ferguson, M. Z. Bazant (2012) · M. Z. Bazant (2013) | X / O | 확인 | §5(bazant2013) | 4.3 | 원전 |
| R. Kubo (1957·1966) | X | 확인(§4.1 표) | — | 4.3 | 원전 |

### 4.8 완화 · 히스테리시스 (Kramers · Preisach · Dreyer)

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| W. Dreyer *et al.*, *Nat. Mater.* 9, 448 (2010) · W. Dreyer, C. Guhlke, M. Herrmann, *CMT* 23, 211 (2011) | O ×2 | 확인 | §4·§7 | 4.5 | 원전 |
| H. A. Kramers (1940) · P. Hänggi *et al.* (1990) | X | 확인(§4.6 표) | — | 4.5 | 원전·리뷰 |
| F. Preisach, "Über die magnetische Nachwirkung," *Z. Phys.* 94, 277–302 (1935) | X | 10.1007/BF01349418 Crossref 확인 | — (Preisach 0회) | 4.5(명명 노트 — `SURV_SYNTHESIS.md` Tier 3 "Preisach 명명 노트"; 연산자 채택은 기각) | 원전 |
| I. D. Mayergoyz, "Mathematical Models of Hysteresis," *PRL* 56, 1518–1521 (1986) | X | 10.1103/PhysRevLett.56.1518 Crossref 확인 | — | 4.5 | 원전 |
| I. D. Mayergoyz, *Mathematical Models of Hysteresis and Their Applications* (Elsevier 2003) | X | 서적 [미검증] | — | 4.5(선택) | 교재 |
| T. Sasaki, Y. Ukyo, P. Novák, "Memory effect in a lithium-ion battery," *Nat. Mater.* 12, 569–575 (2013) | X | 10.1038/nmat3623 Crossref 확인 | — | 4.5(many-particle 준안정의 실증) | 원전 |
| R. Kohlrausch, *Ann. Phys.* 167, 179–214 (1854) · G. Williams, D. C. Watts, *Trans. Faraday Soc.* 66, 80 (1970) | △ 원장 V1(`kohlrausch1854`·`williamswatts1970`), bib 없음 | 10.1002/andp.18541670203 · 10.1039/tf9706600080 Crossref 확인 | — (KWW 0회) | 4.3(꼬리 일반형 재개방 시에만 — brief §4.5 scope-out 항목) | 원전 |
| P. Bai, D. A. Cogswell, M. Z. Bazant (2011) · D. A. Cogswell, M. Z. Bazant (2013) | X | 확인(§4.2 표) | — | 4.5 | 원전 |
| Y. Jiang *et al.*, *JES* 167, 130533 (2020) · L. Köbbing *et al.*, *AFM* 34(7), 2308818 (2024) | O ×2 | 확인 | S1·S4·부록D | 4.8 | 원전 |
| I. Zilberman *et al.* (2018) | O | 확인 | T5·T9 | 4.5 | 원전 |

### 4.9 LCO (Reimers–Dahn · Ménétrier · Van der Ven · Marianetti)

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| K. Mizushima, P. C. Jones, P. J. Wiseman, J. B. Goodenough, "LixCoO2 (0<x≤1): A new cathode material for batteries of high energy density," *Mater. Res. Bull.* 15, 783–789 (1980) | X | 10.1016/0025-5408(80)90012-4 Crossref 확인 | — | 4.7(LCO 원전) | 원전 |
| J. N. Reimers, J. R. Dahn, *JES* 139, 2091 (1992) | O `reimers1992` | 확인 | L13·L15·L16b | 4.7 | 원전 |
| T. Ohzuku, A. Ueda, "Solid-State Redox Reactions of LiCoO2 (R3m) for 4 Volt Secondary Lithium Cells," *JES* 141, 2972–2977 (1994) | X | 10.1149/1.2059267 Crossref 확인 | — (`LIT_ADVANCE_SYNTHESIS.md` L1) | 4.7(3 feature 골격) | 원전 |
| G. G. Amatucci, J. M. Tarascon, L. C. Klein, "CoO2, The End Member of the LixCoO2 Solid Solution," *JES* 143, 1114–1123 (1996) | X | 10.1149/1.1836594 Crossref 확인 | — | 4.7(고전압 O1 종단) | 원전 |
| Z. Chen, Z. Lu, J. R. Dahn, "Staging Phase Transitions in LixCoO2," *JES* 149, A1604 (2002) | X | 10.1149/1.1519850 Crossref 확인 | — | 4.7(H1-3 staging) | 원전 |
| M. Ménétrier *et al.*, *J. Mater. Chem.* 9, 1135 (1999) | O `menetrier1999` | 확인 | L11·L15·L16b | 4.7 | 원전 |
| A. Van der Ven *et al.*, *PRB* 58, 2975 (1998) | O `vanderven1998` | 확인 | L13·L16b | 4.7 | 원전 |
| C. Wolverton, A. Zunger, "First-Principles Prediction of Vacancy Order-Disorder and Intercalation Battery Voltages in LixCoO2," *PRL* 81, 606–609 (1998) | X | 10.1103/PhysRevLett.81.606 Crossref 확인 | — | 4.7(order–disorder 제일원리 병기) | 원전 |
| C. A. Marianetti, G. Kotliar, G. Ceder, *Nat. Mater.* 3, 627 (2004) | O `marianetti2004` | 확인 | L13·L15 | 4.7 | 원전 |
| N. F. Mott, *RMP* 40, 677 (1968) · M. Imada *et al.*, *RMP* 70, 1039 (1998) | O ×2 | 확인 | L15 | 4.7 | 원전·리뷰 |
| T. Motohashi *et al.*, *PRB* 80, 165114 (2009) | O `motohashi2009` | 확인 | 14회 | 4.7 | 원전 |
| H. Xia *et al.*, *JES* 154, A337 (2007) | O `xia2007` | 확인 | L11·L16 | 4.7 | 원전 |
| Y. Reynier *et al.*, *PRB* 70, 174304 (2004) · N. S. Hudak *et al.* (2015) | O / X | 확인 | 11회 / — | 4.7 | 원전 |
| M. Faghih Shojaei *et al.*, *JMPS* 190, 105726 (2024) | O `ml2024` | 확인 | L13·L15·L16b | 4.7 | 원전 |

### 4.10 Si (Chevrier–Dahn · Artrith · Obrovac)

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| V. L. Chevrier, J. R. Dahn, *JES* 156, A454 (2009) | O `chevrier_dahn2009` | 확인 | 8회 | 4.8 | 원전 |
| N. Artrith, A. Urban, G. Ceder, *JCP* 148, 241711 (2018) | O `artrith2018`(원장 미등재) | 확인 | S2b | 4.8 | 원전 |
| M. N. Obrovac, V. L. Chevrier, *Chem. Rev.* 114, 11444 (2014) | O `obrovac_chevrier2014` | 확인 | 6회 | 4.8 리뷰 앵커 | 리뷰 |
| M. N. Obrovac, L. J. Krause, "Reversible Cycling of Crystalline Silicon Powder," *JES* 154, A103 (2007) | X | 10.1149/1.2402112 Crossref 확인 | — | 4.8(c-Li15Si4 순환 원전) | 원전 |
| T. D. Hatchard, J. R. Dahn, "In Situ XRD and Electrochemical Study of the Reaction of Lithium with Amorphous Silicon," *JES* 151, A838 (2004) | X | 10.1149/1.1739217 Crossref 확인 | — | 4.8(a-Si 경로) | 원전 |
| B. Key *et al.*, "Real-Time NMR Investigations of Structural Changes in Silicon Electrodes for Lithium-Ion Batteries," *JACS* 131, 9239–9249 (2009) | X | 10.1021/ja8086278 Crossref 확인 | — | 4.8(NMR 원전 — `ogata_nmr2014` 선행) | 원전 |
| A. F. Bower, P. R. Guduru, V. A. Sethuraman, "A finite strain model of stress, diffusion, plastic flow, and electrochemical reactions in a lithium-ion half-cell," *JMPS* 59, 804–828 (2011) | X | 10.1016/j.jmps.2011.01.003 Crossref 확인 | — | 4.8(Larché–Cahn 의 유한변형 확장 — GS-1 공백의 참조) | 원전 |
| F. Larché, J. W. Cahn, *Acta Metall.* 21, 1051 (1973) | O `larchecahn1973` | 확인 | S4·부록D | 4.8 | 원전 |
| M. N. Obrovac, L. Christensen (2004) · J. Li, J. R. Dahn (2007) · P. Limthongkul *et al.* (2003) · C. J. Wen, R. A. Huggins (1981) · L. Y. Beaulieu *et al.* (2001) · V. A. Sethuraman *et al.* (2010 ×2) · X. H. Liu *et al.* (2012) · J. W. Wang *et al.* (2013) · M. T. McDowell *et al.* (2013) · K. Ogata *et al.* (2014) | O ×11 | 확인 | S1·S2·S2b·S4·부록D | 4.8 | 원전 |
| SiO·Si–C·블렌드 실측 12종(`miyachi_sio2005`…`zhan_siox2026`) | O | 확인 | S2·S3·S5 | 4.8 | 원전(응용) |
| M. W. Verbrugge *et al.* (2016) · M. Tu *et al.* (2024) · W. Ai *et al.* (2022) | O | 확인 | S2b·S3 | 4.8 | 원전(모델) |

### 4.11 사용자 논문 · refs 6/7 · 적분방정식 · 식별성

| 문헌 | bib | DOI·검증 | 현행 절 | v2.0.0 | 성격 |
|---|---|---|---|---|---|
| K. Lee, S. Lee, C. H. Choi, S. Lee, *JCP* 147, 144111 (2017) | O `lee2017jcp`(원장 미등재) | 10.1063/1.5000882 확인 | 부록E(5) | 4.3/4.9(ratio 닫힘) | 원전(사용자) |
| S. Lee, C. Y. Son, J. Sung, S. Chong, *JCP* 134, 121102 (2011) — ref. 6 | O `lee2011jcp`(미등재) | 10.1063/1.3565476 확인 | 부록E(2) | 4.9 | 원전 — **원문 미소장**(brief §4.1) |
| C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, S. Lee, *JCP* 138, 164123 (2013) — ref. 7 | O `son2013jcp`(미등재) | 10.1063/1.4802584 확인 | 부록E(2) | 4.9 | 원전 — **원문 미소장** |
| F. G. Tricomi, *Integral Equations* (Interscience 1957; Dover 1985) | X | 서적 [미검증] | — | 4.9(Fredholm 2종·Volterra·Neumann 급수 표준 교재 — 부록E Fredholm 5회·Volterra 10회) | 교재 |
| M. K. Transtrum *et al.*, "Perspective: Sloppiness and emergent theories in physics, biology, and beyond," *JCP* 143, 010901 (2015) | X | 10.1063/1.4923066 Crossref 확인 | — | 4.9/방법(SURV Tier 2 Fisher 정보·식별성 채택 시) | 리뷰 |

### 4.12 dQ/dV·DVA 방법론 (현행 유지)

I. Bloom *et al.* (2005) `bloom2005` · M. Dubarry *et al.* (2012) `dubarry2012` · A. Fly, R. Chen (2020) `fly2020` — 전부 O·확인. v2.0.0 서론(4.0)에 그대로 승계.

### 4.13 체크리스트 집계 [확정 — 위 표 합산]

| 주제 | 항목 수 | 현행 bib O | △(원장/부록만) | X | X 중 DOI Crossref 확인 | X 중 서적·미검증 |
|---|---|---|---|---|---|---|
| 4.1 통계역학 기초 | 14 행 | 4 | 0 | 10 | 6 | 4(Chandler·Landau–Lifshitz·Callen·Pathria) |
| 4.2 격자기체·정칙용액·상분리 | 24 행 | 4 | 5 | 15 | 14 | 1(Guggenheim) |
| 4.3 흑연 staging | 21 행 | 9 행(10 키) | 2 | 9 | 7 | 2(Daumas–Hérold 미검증·Verbrugge–Koch 2003 후보 DOI 오해소) |
| 4.4 MSMR | 7 행 | 6 행(7 키) | 0 | 1 | 1 | 0 |
| 4.5 엔트로피·가역열 | 18 행 | 11 행 | 0 | 6 | 6 | 0 |
| 4.6 속도론 | 20 행 | 6 | 0 | 14 행(15 DOI) | 13 행(14 DOI) | 1(Bard–Faulkner) |
| 4.7 비가역 열역학 | 7 행 | 1(bazant2013) | 0 | 5(타 표 중복 Ferguson·Kubo 제외) | 2 행(Onsager 2 DOI·Latz) | 3(de Groot–Mazur·Kondepudi–Prigogine·Prigogine) |
| 4.8 완화·히스테리시스 | 10 행 | 3 행(5 키) | 1 행(2 키) | 4(타 표 중복 제외) | 3 | 1(Mayergoyz 서적) |
| 4.9 LCO | 14 행 | 9 행(10 키) | 0 | 5(Hudak 은 4.5 계상) | 5 | 0 |
| 4.10 Si | 11 행(군 포함) | 대부분 O | 0 | 4 | 4 | 0 |
| 4.11 사용자 논문·적분방정식 | 5 행 | 3 | 0 | 2 | 1 | 1(Tricomi) |

이론 층(4.1·4.2·4.6·4.7·4.8)의 X 가 48건으로 전체 X 의 대부분을 차지하고, 그중 38건은 DOI 를 이미 Crossref 로 확인해 두었으므로 원장 등재는 서지 재타이핑 없이 응답 필드에서 생성할 수 있다. 서적 10건(선택 포함)은 ISBN·판 확인 절차(§5 규약 4)가 별도로 필요하다.

---

## 5. 인용 규약 초안 (v2.0.0 REFERENCE_LEDGER v2 · bib 생성 규칙)

아래는 현행 규칙(V1020 line 3 "본문 `\cite` 는 원장 V1 키만·기억 기반 서지 인용 금지·검증→등재→인용", V1022 line 3 "검증 모델 = 저비용, 부족 시 한 단계 승급(D22-4)", `SM2_SURVEY.md` line 5 "표준 수학/열역학 정리는 무인용 관용")을 승계하되, §1 에서 드러난 균열(원장 사본화·미등재 6건·중복 키·헤더 스테일·et al.)을 구조적으로 막는 방향으로 다듬은 초안이다. 채택 여부는 master·사용자 결정이다.

1. **단일 원장·단일 진실.** `Claude/docs/v2.0.0/results/V2_REFERENCE_LEDGER.md`(+ 기계 가독 `.json`) 하나가 모든 키의 정본이다. 열 = 키 · 확정 서지(저자 전원·제목·저널·권(호)·쪽/아티클·연도) · DOI(또는 ISBN·판) · 상태(V0 후보 / V1 인용 가능 / V2 보류 / V3 폐기) · tier(A 원전·실측 / B 리뷰·2차 / C 방법 수준·abstract / I 내부자료) · 검증일·검증 수단·검증 로그 path · 사용 절. 승계 선언으로 상위 원장을 가리키는 방식은 폐기하고 v1.0.20~v1.0.25.1 의 전건을 **소급 전사**한다(V1023 사본 문제·미등재 6건 해소).
2. **본문 `\cite` 는 V1 키만.** 원장에 없는 키를 본문에 쓰면 빌드 게이트 FAIL. 검증 도구 = `tools_tex_strict_check.py` 류에 "cite 키 ⊆ 원장 V1" 검사를 추가[추정 — 도구 실물 미정독].
3. **기억 서지 금지의 조작적 정의.** 어떤 서지도 Crossref(`api.crossref.org/works/{DOI}`) 또는 출판사 랜딩 페이지 대조 없이 원장에 V1 으로 들어가지 않는다. 기억에서 나온 DOI 후보는 허용하되, 응답의 제목·첫저자·저널·연도가 의도한 문헌과 일치할 때만 V1 이 되고 불일치·미해소는 V0 에 머문다(본 문건 §4 의 Verbrugge–Koch 2003 사례가 그 실례).
4. **Crossref 5-필드 대조 절차.** (a) DOI 조회 → (b) 제목·저자 전원·저널(container-title)·권/호/쪽(article-number 포함)·연도(published-print 우선, online 은 비고) 5 필드를 원장에 전사 → (c) 인쇄판 연도 표기 관행 유지(V1022 line 4) → (d) 응답이 비어 있는 필드(예: `sethuraman_stresspot2010` 끝쪽·`lee_sic2025` 권)는 "★확인필요" 표기 후 V1(필드 조건부) → (e) 조회 스크립트와 응답 JSON 을 `Claude/docs/v2.0.0/results/refcheck/` 에 보존해 재현 가능하게 한다. 서적은 Crossref 대신 출판사 페이지 또는 WorldCat 으로 ISBN·판·연도를 대조하고, 장·절 수준 인용만 허용(쪽수는 실물 대조 전 금지 — V1020 line 33 ashcroftmermin 규약 승계).
5. **저자 전원 명기.** 리뷰급 서지에서는 "et al." 을 쓰지 않는다(현행 4건 R-06 정정). 예외 = 저자 20인 이상은 처음 10인 + "et al." [추정 — 관행 기준].
6. **한 문헌 = 한 키.** 같은 DOI 가 두 키로 존재하면 FAIL(R-01). 키 규약 = `<첫저자성(소문자)>_<주제어>YYYY` 또는 `<첫저자성>YYYY[a|b]`; 기존 키는 자산 무유실 원칙에 따라 유지하고 별칭 표를 둔다.
7. **1차 문헌 우선·tier 병기.** 식·수치·상 판정 등 load-bearing 주장은 tier A 원전을 인용하고 리뷰(tier B)는 병기만 한다(V1021 line 26·34 규약 승계). 교재는 유도 전개의 표준 출처로 절 도입부에 장 수준으로 인용한다. tier 태그는 원장 열이자 bib 비고 대괄호에 유지한다(현행 관행).
8. **절별 인용 하한.** 유도 절은 출발식(사다리의 각 "일반식") 마다 표준 출처 ≥1 · 실측 수치는 각각 1차 문헌 ≥1 · 본문 무인용 절 0(요약·검산·코드 절 제외). 작업 챕터 2.4·5.2 의 게이트 수치로 쓴다.
9. **bib 는 원장에서 생성.** `thebibliography` 블록은 원장 `.json` 에서 스크립트로 생성하며 손편집하지 않는다. 장별 bib(자기완결, D22) 를 유지하든 통합 bib 로 가든 공통 키 텍스트는 자동으로 동일해지고 헤더 카운트는 생성 시점 값이 된다(스테일 차단). 구조 결정(DG-A) 후 확정.
10. **언어·표기.** 서지 제목은 원문 언어 그대로(독일어 제목 포함), 저널 약칭은 ISO 4 또는 저널 자체 표기, 비고는 한글 허용. 수동 번호 [A#] 체계는 폐기하고 전부 키화한다.

---

## Decision Queue

각 항목은 골격·결정 변경이 아니라 통합 초안(마스터 플랜 §11 Decisions Required 또는 작업 챕터 2.4/3.5/5.x 게이트)에 올릴 후보다. 근거는 본문 §번호로 가리킨다.

- **DQ-1 `verbrugge2017`/`msmr_origin2017` 통합과 제목 정정(R-01).** 동일 DOI·두 키·`verbrugge2017` 쪽 제목 오류가 확정됐다(§1.3). 동결본 v1.0.25.1 은 무수정이므로 v2.0.0 에서 처리하되, 남길 키 이름과 처리 시점(작업 챕터 2.4 GAP REGISTER 등재 → 5.1 집행)을 결정해야 한다. 기본값 제안 = `msmr_origin2017` 유지·`verbrugge2017` 별칭 표로 흡수.
- **DQ-2 원장 재개설.** V1023 이 V1022 사본이라 v1.0.23~v1.0.25.1 의 원장 기록이 없다(§1.2). v2.0.0 원장을 §5 규약 1 대로 새로 개설하고 전건 소급 전사할지, 현행 승계 방식으로 V1025 원장을 추가할지. 기본값 제안 = 재개설(단일 진실).
- **DQ-3 미등재 6키 소급 등재.** `lee2017jcp`·`lee2011jcp`·`son2013jcp`·`schmitt2022`·`verbrugge2017`·`artrith2018` 는 검증 흔적은 있으나 원장 절차를 거치지 않았다(§1.2). 소급 등재 시 Crossref 재조회 결과(본 문건 §2 표)를 근거로 쓸 수 있다.
- **DQ-4 저자 전원 명기 규약(R-06).** 현행 bib 는 "et al." 4건이고 다른 항목은 9~14인까지 전원 명기해 일관성이 없다. 리뷰급 기준이면 전원 명기(규약 5)로 통일할지.
- **DQ-5 원장에만 있는 4키(`safran1980`·`safran1987`·`williamswatts1970`·`kohlrausch1854`)의 처리.** KWW 는 scope-out(brief §4.5), Safran 은 범위 밖(`SM2_SURVEY.md` line 42)으로 남았다. v2.0.0 작업 챕터 3.1 조사 축에 "KWW/장벽분포"·"transfer matrix staging" 이 들어 있으므로 재개방 여부는 3.7 결정과 연동된다. 삭제 시점을 기록한 원천은 미발견이므로 작업 챕터 1.4 등록부에서 확인이 필요하다.
- **DQ-6 장별 bib 자기완결(D22) vs 통합 bib.** 3.3 구조 결정(DG-A: 재료별 3장 vs Part I 일반 이론+Part II 재료 적용)에 종속된다. 어느 쪽이든 §5 규약 9(원장에서 생성)로 중복 텍스트 불일치는 사라진다.
- **DQ-7 Daumas–Hérold 1969 원전 확보.** §5b 가 이름만 언급한다(line 98). DOI·서지 모두 [미검증]이므로 실물(Gallica 등) 확보 또는 Dresselhaus 1981 리뷰로 대체 인용할지.
- **DQ-8 refs 6·7 원문.** brief DR-8 과 동일 — 원문 미소장 상태에서 dossier(`PHASE_DIAG_REFS67_DOSSIER.md`)와 Crossref 서지로 V1 등재만 할지, 원문을 확보해 CLAUDE.md P3 #5 의 "원 방법론의 수학적 구조"를 원문 기준으로 재검증할지.
- **DQ-9 서적 검증 절차.** Crossref 로는 후보 서적 11건(Chandler·Landau–Lifshitz·Callen·Pathria·Guggenheim·Bard–Faulkner·de Groot–Mazur·Kondepudi–Prigogine·Prigogine·Mayergoyz·Tricomi)+현행 서적 8건의 ISBN·판을 확인할 수 없다. 규약 4 의 서적 절차(출판사/WorldCat)를 채택할지, 서적은 "장 수준 인용·ISBN 미대조" 로 정직 표기하고 넘어갈지.
- **DQ-10 `schmitt2022` 첫저자 정정(R-02).** Crossref 는 C. Schmitt 4인. 동결본 무수정·v2.0.0 반영.
- **DQ-11 `koebbing2024` 권·호·`sethuraman_stresspot2010` 쪽 반영(R-03·R-04).** 원장은 해소됐거나 Crossref 로 시작쪽이 확인됐다. 끝쪽은 출판사 페이지 대조가 필요하다.
- **DQ-12 bib 헤더 카운트 스테일(39/14/14 → 44/15/36).** 규약 9 채택 시 자동 해소. 채택 전이면 GAP REGISTER 항목.
- **DQ-13 체크리스트 "필수" 판정의 권위.** §4 의 필수·선택 구분은 본 에이전트 판단이다. 특히 다공전극(Newman–Tiedemann·Doyle–Fuller–Newman·Ferguson–Bazant·Smith–Bazant)은 brief §6 Non-goal(전셀·역문제)과 인접하므로 "경계 표기용 인용"에 한정할지, 아예 제외할지 master 삼각검증이 필요하다.
- **DQ-14 Verbrugge–Koch 2003 서지 미확정.** 기억 후보 DOI 가 다른 논문으로 해소됐다(§4.3). 후보에서 제외하거나 Crossref 제목 검색으로 재확인할지.
- **DQ-15 brief 카운트 정의 명시.** brief §4.2 "`\cite` 호출 265" 는 bib 내부 상호참조 3건을 포함한 명령 수다(본문만 262·키 단위 315). 마스터 플랜 2.1 자산 지도 게이트에 정의를 명시해 두지 않으면 카운트 일치 게이트가 정의 차이로 FAIL 할 수 있다.

---

## Read Coverage (파일 · 행 범위 전건)

| 파일 | 행 범위 | 방식 |
|---|---|---|
| `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md` | 1–219 (전문) | Read |
| `Claude/docs/v1.0.25.1/_sections/ch1v22_bib.tex` | 1–57 (전문) | Read |
| `Claude/docs/v1.0.25.1/_sections/ch2v22_bib.tex` | 1–22 (전문) | Read |
| `Claude/docs/v1.0.25.1/_sections/ch3v22_bib.tex` | 1–45 (전문) | Read |
| `Claude/docs/v1.0.23/results/V1023_REFERENCE_LEDGER.md` | 1–33 (전문) | Read + md5 대조 |
| `Claude/docs/v1.0.22/results/V1022_REFERENCE_LEDGER.md` | 1–33 (전문) | Read + md5 대조 |
| `Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md` | 1–38 (전문; 승계 사슬) | Read |
| `Claude/docs/v1.0.20/results/V1020_REFERENCE_LEDGER.md` | 1–55 (전문; 승계 사슬) | Read |
| `Claude/docs/v1.0.25.1/appendix_phase_separation.tex` | 470–498 (부분: 참고문헌 블록·본문 대응 문단) + `\cite`·`[A#]` grep | Read(부분)·Grep |
| `Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md` | 1–130 (전문) | Read |
| `Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md` | 1–45 (전문) | Read |
| `Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md` | 1–136 (전문) | Read |
| `Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md` | 1–50 (전문) | Read |
| `Claude/docs/v1.0.25.1/_sections/*.tex` 53본(bib 제외)·마스터 tex 3본 | **전문 정독 아님** — `\cite` 위치·`\section`/`\subsection` 제목·개념 키워드 빈도의 기계 스캔(Python·Grep)만 | 스크립트 |
| 외부 | Crossref REST API 84 + 74 DOI 조회(2026-09-03) | Invoke-RestMethod / urllib |

미정독·미실행 항목: `Codex/` 전체(금지) · 본문 tex 의 문장 단위 정독(절별 인용 판정은 스캔 기반이라 [추정]) · 서적 ISBN 대조 · Daumas–Hérold 1969 실물 · `tools_tex_strict_check.py` 등 검사 도구 본문.
