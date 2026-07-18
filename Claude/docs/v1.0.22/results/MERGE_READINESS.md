# MERGE_READINESS — v1.0.22 병합 준비 상태 문서 (R9 — 마스터 확정 2026-07-18)

> 지위: **초안** — 마스터(사용자 별도 세션)가 확정. 본 문서는 R9 마감 창(오푸스)이 작성.
> 규율: **병합 빌드 절대 금지(D22-8)** — 병합은 사용자가 별도 세션에서 버전 안정화 후 직접 수행. 본 문서는 **정적 검사·절차 안내까지만**.
> 작성일: 2026-07-18. 근거 = 원장(`V1022_EXECUTION_LEDGER.md`·`V1022_CHANGE_LOG.md`·`V1022_REFERENCE_LEDGER.md`) + 실제 파일·aux·도구 출력에서 확인한 것만. 미확인분은 "미확인" 표기.
> 대상 3본: `ch1_graphite_v1.0.22.tex`(83p) · `ch2_lco_v1.0.22.tex`(25p) · `ch3_si_v1.0.22.tex`(17p) — 각 GREEN(err0·미해소0).

---

## 0. 요약 (한 눈)

| 항목 | 상태 | 근거 |
|---|---|---|
| 전역 라벨 유일성(병합 충돌) | **충돌 0**(콘텐츠 라벨) — 유일 교집합 `LastPage`(패키지 sentinel) | §1 도구+aux 전수 교차 |
| 매크로 통합 | 3장 공통 `common_preamble_v1022.tex` 단일 — 장별 preamble 3본은 **고아**(미\input) | §2 |
| 서지 | 장말 bib 3본 분할 유지(39/15/33) · 의도적 중복 1(swiderska2019) | §3 |
| 병합 절차 | xr 제거 → \input 통합 → 부록 카운터 재정의 → 단일 bib 통합 (4단) | §4 |
| 알려진 주의점 | **5범주**(a~e; (d)=RV3 §5 병합 대비 9항 전건 반영) | §5 |
| 검수 이력 | FR 대공사 H 29·M 정정형 38+3·이월 14 | §6 |

**결론(초안 판정):** 라벨 네임스페이스는 병합 충돌이 없어(§1) 병합의 최대 리스크(대이동 자산·라벨 충돌)는 정적 검사상 해소. 남는 것은 **번호 표기 재계산**(xr → 단일 카운터)과 **부록 카운터 기구 재정의**(§5-a), 그리고 P5 보존 항목·미결정 항목의 사용자 확정(§5-b·c)이다.

---

## 1. 전역 라벨 유일성 (병합 충돌 검사)

### 1.1 구조 검사 도구 출력 (per-master)

명령: `python3 results/tools_check_structure.py check . ch1_graphite_v1.0.22.tex ch2_lco_v1.0.22.tex ch3_si_v1.0.22.tex`
실행 결과(2026-07-18, R9):

```
=== ch1_graphite_v1.0.22.tex (32 files) ===
labels: 241 (dup: 0) []
refs: 980 (unresolved: 0) []
cites: 114 keys, bibitems: 39 (cite-undef: [], bib-uncited: [])
env pairing errors: 0 · asset anchors: 265 tags, unique 265 · math env blocks: 130 (boxed: 33)
=== ch2_lco_v1.0.22.tex (12 files) ===
labels: 77 (dup: 0) []
refs: 314 (unresolved: 0) []
cites: 68 keys, bibitems: 15 (cite-undef: [], bib-uncited: [])
env pairing errors: 0 · asset anchors: 92 tags, unique 92 · math env blocks: 45 (boxed: 13)
=== ch3_si_v1.0.22.tex (10 files) ===
labels: 38 (dup: 0) []
refs: 158 (unresolved: 0) []
cites: 75 keys, bibitems: 33 (cite-undef: [], bib-uncited: [])
env pairing errors: 0 · asset anchors: 0 tags, unique 0 · math env blocks: 11 (boxed: 2)
STRUCTURE_CHECK: PASS   (exit 0)
```

- **주의(도구 한계):** `do_check` 의 `dup` 판정은 **per-master(장 내부)** 만 본다. 장 간 라벨 충돌은 이 값으로 판정되지 않는다(도구는 라벨 합집합을 `unresolved-ref` 판정에만 사용). → 병합 충돌은 §1.2 의 aux 전수 교차로 별도 실사.

### 1.2 3 빌드 aux `\newlabel` 전수 교차 대조 (병합 충돌 실사 — xr 접두 제외)

방법: 3 빌드 aux 의 `\newlabel{NAME}` 을 전수 추출해 장 간 교집합 산정(scratchpad `xcheck_labels.py`, 2026-07-18 실행).

| aux | `\newlabel` 수 | = 소스 라벨 + sentinel | 장 내부 중복 |
|---|---:|---|---|
| `ch1_graphite_v1.0.22.aux` | 242 | 241(소스) + `LastPage` | 0 |
| `ch2_lco_v1.0.22.aux` | 78 | 77(소스) + `LastPage` | 0 |
| `ch3_si_v1.0.22.aux` | 39 | 38(소스) + `LastPage` | 0 |

**장 간 교집합(잠재 병합 충돌):**

| 쌍 | 교집합 | 내용 |
|---|---:|---|
| ch1 ∩ ch2 | 1 | `LastPage` |
| ch1 ∩ ch3 | 1 | `LastPage` |
| ch2 ∩ ch3 | 1 | `LastPage` |
| ch1 ∩ ch2 ∩ ch3 | 1 | `LastPage` |

- **콘텐츠 라벨 충돌 = 0.** 세 장에 공통으로 나타나는 라벨은 `LastPage` 뿐 — `lastpage` 패키지가 각 문서 말미에 emit 하는 **sentinel**(콘텐츠 라벨 아님, `tools_check_structure.py` 의 `PKG_LABELS` 화이트리스트). 병합 후 단일 문서에는 `LastPage` 가 하나만 남으므로 무해.
- **xr 오염 없음(접두 실사):** `\externaldocument` 로 배선된 외부 라벨은 참조 문서 aux 에 **재기록되지 않음**을 확인 — ch3 aux 는 ch1·ch2 를 둘 다 `\externaldocument` 하지만 39 = 38 소스 + `LastPage` 로, `sec:lco-*`·흑연 라벨 등 외부 라벨이 하나도 섞이지 않음. 따라서 "xr 접두 제외"할 대상 자체가 aux 에 부재(외부 라벨은 컴파일 시 메모리 보유, aux 미기록). 교집합 결과는 순수 자기 라벨 기준.
- 라벨 이름 합집합 총계 = 357(=242+78+39 − 2×`LastPage` 중복). 소스 라벨 총계 = 356(241+77+38).

**판정: 병합 시 라벨 개명 불요(콘텐츠 라벨 네임스페이스 충돌 0).** 이는 R1 설계(신규 라벨 장 prefix 관행 + `eq:Se`/`eq:Se-ch2` 등 기존 분리 유지)와 RV3 §0·§1(라벨 충돌 = `LastPage` 뿐·미해소 0·local shadowing 0)의 독립 확인과 일치.

---

## 2. 매크로 통합 상태

### 2.1 공유 preamble 구조

- 3장 마스터(`ch{1,2,3}_*.tex`) 모두 첫 줄에서 `\input{_sections/common_preamble_v1022}` 를 로드하고, 그 위에 **장별 얹기 4종**만 추가:
  - `\hypersetup{pdftitle=…}` · `\lhead{…}` (장별 헤더)
  - `\renewcommand{\theequation}{N.\arabic{equation}}` · `\renewcommand{\thesection}{N.\arabic{section}}` (N=1/2/3 — 장별 번호계)
  - `\externaldocument{…}` (Ch2/Ch3, xr 외부 참조; Ch1 은 전방 참조로 `\externaldocument{ch2…}`)
- `common_preamble_v1022.tex` 내용(R1/S-002 통합 = 구 `ch1_preamble` ∪ `ch2_preamble`, 매크로 충돌 0 검증): documentclass·geometry·kotex·D2Coding·amsmath 계열·`xr-hyper`(hyperref 앞)·hyperref·fancyhdr·lastpage·tikz + box 환경 9종(keybox·codebox·signbox·verifybox·derivbox·bgbox·srcbox·warnbox·procedurebox) + 기호 매크로 21종(`\dd`·`\eff`·`\eq`·`\app`·…·`\kB`·`\code`·`\avg`) + 목차 서식(`\l@section`/`\l@subsection` 재정의). 항법 토글(`\ifnavaid`)은 폐기(D22-1).

### 2.2 장별 preamble 잔여 확인 (고아 소스)

`_sections/` 전량 `\input` 스캔(2026-07-18) 결과, 아래 3본은 **현행 어느 마스터에도 미포함(고아)**:

| 파일 | 상태 | 사유 |
|---|---|---|
| `_sections/ch1_preamble.tex` | 고아(미\input) | S-002 에서 `common_preamble_v1022` 로 통합·대체 |
| `_sections/ch2_preamble.tex` | 고아(미\input) | 〃 |
| `_sections/ch1_appD_si.tex` | 고아(미\input) | R5/S-012 에서 Si 예비지도가 `ch3v22_sec01~05` 본문으로 승격·대체(§0 RV3 확인) |

- **매크로 통합 판정:** 병합 시 preamble 은 `common_preamble_v1022` **1본**만 쓰면 충분(장별 preamble 고아 3본은 병합 대상 아님). 병합 드라이버는 장별 얹기 4종 중 `\theequation`/`\thesection` 장별 고정을 **단일 카운터/장 카운터 체계로 재설계**해야 함(§4·§5-e).
- 고아 파일은 **삭제하지 않음**(P5·이력 보존) — 병합 재조립 시 `\input` 목록에서 제외만 확인.

---

## 3. 서지 방식

### 3.1 장말 bib 3본 분할 유지 (리뷰 모음형)

현행 bibitem 수(파일 직접 카운트 + 도구 교차, 2026-07-18):

| bib 파일 | bibitems | 원장 계보 |
|---|---:|---|
| `_sections/ch1v22_bib.tex` | 39 | R1 분할 39 (변동 없음) |
| `_sections/ch2v22_bib.tex` | 15 | R1 분할 14 + C-038(kim_entropymetry2020, R4m) = 15 |
| `_sections/ch3v22_bib.tex` | 33 | R1 분할 14 + S-012(19키, R5) = 33 |

- 도구 출력(§1.1)의 bibitems(39/15/33)와 일치. cite↔bibitem 불일치 0(cite-undef 0·bib-uncited 0, 3장 전건).

### 3.2 의도적 중복 1건 (swiderska2019)

- `\bibitem{swiderska2019}` 이 `ch1v22_bib.tex:23` 과 `ch2v22_bib.tex:16` **양쪽**에 동일 서지로 존재(직접 확인). LiCoO$_2$ 단전극 $\partial\phi/\partial T\approx+0.83$ mV/K(tier B) — 흑연 열특성 파트(Ch1)와 LCO 장(Ch2) 양쪽에서 load-bearing 이라 리뷰 모음형 관행상 장별 재수록(의도, S-006·R1 비고).
- 별개 PDF 상태에서는 정상(각 장 자기완결). **병합 시 단일 thebibliography 로 통합하면 중복 `\bibitem` 충돌** → 하나로 병합(§4-4). 그 외 키는 장별로 깨끗이 분리(예: `reynier2003`=Ch1 vs `reynier2004`=Ch2 상호오염 0 — RV3-C1).
- 빌드 로그 "multiply defined" 화이트리스트 = `LastPage`·`swiderska2019` 2건뿐(xr 산물·의도 중복). 병합 시 `\externaldocument` 제거로 `LastPage` 경고는 자연 해소, `swiderska2019` 는 bib 통합으로 해소.

### 3.3 V1 원장 승계 관계

- **승계 사슬(원장 자기선언):** v1.0.22 원장은 v1.0.21 원장을 **그대로 승계**; v1.0.21 은 v1.0.20 판정 전건(기존 42 + 신규 12 + appendix [A1]~[A5])을 승계. V2(인용 보류) = `safran1987` 유일. ★확인필요 잔여 = `sethuraman_stresspot2010`(쪽).
- **R2+ 신규 등재 20키**(`V1022_REFERENCE_LEDGER.md` R2+ 표): `kim_entropymetry2020`(R4m·C-038) + R5/S-012 의 19키(Si·SiO$_x$·Si–C·블렌드·엔트로피 계열 — wang_asi2013·mcdowell_coreshell2013·ogata_nmr2014·miyachi_sio2005·kitada_sio2019·zhang_sio2018·yom_sio2016·andersen_sic2019·naboka_sic2021·lee_sic2025·bohm_entropy2024·arnot_calorimetry2021·bohm_thermal2025·wojtala_entropy2022·gautam_blend2024·ai_composite2022·chatzogiannakis_blend2025·zhan_siox2026·tu_blend2024). 전건 Crossref 재검증(기억 서지 0).
- 변경로그 S-012 기재 "(V1 33키)" = R5 등재 직전의 V1 등재 풀 규모(+19 → 이후 확장). 서지 정정 C-050(limthongkul DOI 00514-1·ogata article-number 3217)로 원장 동보정.
- **병합 후에도 장별 bib 유지가 트렌드 정합**(리뷰 모음형 — 마스터플랜 §2·원칙). 단일 참고문헌으로 합칠지는 사용자 결정(§4-4 는 통합 시 절차만 안내).

---

## 4. 병합 절차 (단계별 — 무엇을·왜)

> **본 절은 절차 안내이며, R9 세션은 이 절차를 실행하지 않는다(D22-8).** 사용자 별도 세션 수행 대비.

**1단계 — xr 기계장치 제거.** 3 마스터의 `\externaldocument{…}` 선언과 장별 `\renewcommand{\theequation}`/`\thesection` 고정을 제거.
- *왜:* 병합 후에는 세 장이 한 문서라 외부 참조가 불필요하고, 장별 번호 고정(1.x/2.x/3.x)은 단일 문서의 `chapter`/`section` 카운터와 충돌. 단일 카운터(또는 `\chapter` 기반 N.x 자동)로 대체.
- *영향:* 라벨명은 불변(§1 충돌 0)이나 **식·절 번호 표기 전량 재계산** → 130+ 장 간 교차참조(`\ref`/`\eqref`)가 새 번호로 재렌더(RV3 §5-5·§1: Ch1↔Ch2 xr 참조 130건). 라벨 기반이라 자동 해소되나 **하드코딩 번호 문자열**(§5-a·§5 항목 3)은 수동 추적 필요.

**2단계 — `\input` 통합(단일 드라이버).** 새 병합 마스터가 `common_preamble_v1022` 1본 로드 후, 3장의 본문 `\input` 목록을 장 구분(`\chapter` 또는 파트 구분면)과 함께 순서대로 편입.
- *왜:* preamble 은 이미 공통 1본(§2)이라 매크로 재정의 충돌 없음. 고아 3본(§2.2)은 제외.
- *주의:* **파일명↔소속 반전**(§5 항목 6·RV3 §0): `ch2_sec*`=Ch1 의 Part T, `ch1_sec11~17`=Ch2 의 Part II — 파일명으로 소속 추정 금지, 마스터 3본의 `\input` 순서가 정본.

**3단계 — 부록 카운터 재정의.** 열특성 부록(`ch2_appA_traps`·`ch2_appB_codemap`)의 수동 `\section*{부록 C/D}` + `\phantomsection\label` 을 단일 부록 카운터 체계로 재정의하고, 하드코딩 letter 를 `\ref` 로 전환.
- *왜:* 현재 라벨 `sec:traps-thermal`·`sec:codemap-thermal` 이 stale 카운터 "B" 를 포착(§5-a). 병합으로 전 부록이 한 카운터에 들어가면 letter 재배열이 불가피 → 카운터 기구 정상화가 선행돼야 `\ref` 전환이 오렌더 없이 성립.
- *순서:* 카운터 정상화(라벨이 올바른 letter 포착) → 그 다음 하드코딩 "부록 C/D" → `\ref{…}` 전환. **역순 금지**(R8 판정: 라벨 정상화 미선행 시 `\ref` 는 "부록 B" 오렌더).

**4단계 — 단일 bib 통합(선택).** 장별 bib 유지가 기본(트렌드)이나 단일 참고문헌을 원하면: 3 bib 의 `\bibitem` 을 하나로 합치되 **`swiderska2019` 중복 1건을 제거**(§3.2), cite↔bibitem 재검(전 cite 가 통합 bib 에 존재하는지) 후 단일 `thebibliography`.
- *왜:* 별개 PDF 의 중복 bibitem 이 단일 문서에서는 "multiply defined" 실충돌. 장별 유지 시에는 이 단계 불요(중복은 장 경계로 분리 유지).

---

## 5. 알려진 주의점 (5범주 a~e; (d)는 RV3 §5 병합 대비 9항 전건 반영)

### (a) 부록 카운터 stale — R8 판정 [최우선 기구 이슈]
- **현상(aux 실확인, `ch1_graphite_v1.0.22.aux`):**
  - `\newlabel{sec:traps-thermal}{{B}{78}…}` → "B" 로 해소(부록 C 여야 함)
  - `\newlabel{sec:codemap-thermal}{{B}{79}…}` → "B" 로 해소(부록 D 여야 함)
  - 원인: 열특성 부록이 `\section*`(비번호) + `\phantomsection\label` 이라, 직전 번호 부록(부록 B=`ch1_appB` 의 `\section`)의 카운터를 포착.
- **현행 하중:** 본문·부록 지칭은 **하드코딩 letter "부록 C"/"부록 D"**(`ch2_sec04_einstein:22`·`:110`·`ch2_sec07_revheat:52`·`ch2_sec08_synthesis:95`·`ch1_appB:135`)로, 현재 렌더는 **정확**. 라벨 `sec:traps-thermal`/`sec:codemap-thermal` 은 `\ref` 사용 0건이라 stale 은 **잠재적**(렌더 결함 없음).
- **병합 시:** 카운터 기구 재정의 필요 → 그 다음에 하드코딩 letter 를 `\ref` 화(§4-3 순서). R8 은 "산문·참조 서식 층위 밖·라벨명 변경 금지 저촉"으로 SKIP, R9 병합 주의점으로 이관(C-054④).

### (b) "Part II 도입" 절 제목 — P5 보존 (사용자 결정 대기)
- `ch1_sec11_lcointro.tex:4` `\section{Part II 도입 --- 전극-중립 골격과 방향 규약 (N0$'$)}\label{sec:lco-intro}` (이 파일은 Ch2/LCO 소속). 역사적 인계 chain 표시라 P5 보존, 본문 내 Ch1→Ch2 지칭의 "Part II" 잔재는 C-039①에서 "Chapter 2" 로 정정 완료(장 내 자가상충 해소). **절 제목 자체의 개명 여부 = 사용자 결정.** 파트 순번 비선형(0·I·T[Ch1]·II[Ch2] — II 가 T 뒤)은 병합 시 파트 재명명/Chapter 승격 결정 필요(RV3 §5-1).

### (c) moyassari_blend2022 등재 대기 (사용자 결정)
- `_sections/*.tex`·`V1022_REFERENCE_LEDGER.md` 전수 스캔 결과 `moyassari_blend2022` 는 **어디에도 미등재·미인용**(확인). A23-H1 경로 B 후보 — 0–20 wt% 스윕 실측(DOI 10.1149/1945-7111/ac4545, 하이쿠+검토창 검증 완료). 등재 시 G2 대조 범위가 [0,0.3] 전 구간 커버로 강화. **등재 여부 = 사용자 결정**(FR_T_ML_TRIAGE §사용자 결정 #2). 현행 §3.5 는 이 유령 서지명을 제거하고 실소재(gautam·chatzogiannakis)로 지목(C-049⑦).

### (d) RV3 §5 병합 대비 9항 — 전건 반영 (`results/comp_RV/RV3_CROSS_REPORT.md` §5)

| # | RV3 항목 | 등급 | 현재 상태(원장 대조) |
|---|---|---|---|
| 1 | Part 명칭 선형화 불가(0·I·T·II, II<T 역전) — RV3-B1 | H | Ch1 내부 본문 "Part II" 잔재는 C-039① 정정(→"Chapter 2"). **파트 재명명/Chapter 승격 결정은 병합 시**(+절 제목 (b)). RV/SM2 원장 "H 잔존 0" = 자가상충 해소분 기준 |
| 2 | tier 범례 위치(Ch2 단독) — RV3-D1 | H | C-039②로 **해소**(Ch1 §7 각주에 동일 규약 복제·역의존 해소). 병합 시 전역 위치(공통 preamble/서두)로 이동 권장 |
| 3 | 하드코딩 장/부록 문자열 — RV3-A1·B4 | M | RV3-A1(참조 스타일 3종)은 R8/C-054①②로 통일 집행(Ch1→Ch2 "Chapter 2" 접두 4·"Ch1"→"Chapter 1" 8). **부록 C/D 하드코딩 letter 는 (a)와 동일 — 병합 시 `\ref`화** |
| 4 | "본 장/본 파트/본서" 스코프어 — RV3-B2·B3·D2 | M | C-039⑧(B3 guard "본 장"→"이 절")·⑩(B2 8곳→"본 파트")로 대부분 정정, 장-전역 범위 선언 12곳은 "본 장" 유지(판정). "본서"(D2)는 **병합 후 스코프 재정의 규칙 명문화**(merge-decision) |
| 5 | xr 기계장치(단일 카운터 통합 시 번호 전량 재계산) | M | **병합 시 필수 작업**(§4-1). 라벨명 충돌 0이라 병합 가능하나 130+ 교차참조 번호 재렌더 |
| 6 | 파일명↔소속 반전(§0) | M | 정보성 — 병합 재조립 시 파일명 신뢰 금물(§4-2 주의) |
| 7 | bib 중복 swiderska2019 | L | §3.2 — 병합 시 단일 bib 이면 중복 제거(§4-4) |
| 8 | 고아 소스 ch1_appD_si.tex | L | §2.2 확인(현행 마스터 미포함) — 병합 목록에서 제외. **본 R9 실사로 고아 preamble 2본 추가 발견**(§2.2) |
| 9 | MSMR 계보 이원화(RV3-C2) | L | 상충 없음 — 병합 시 계보 각주 1곳 통합 권장 |

### (e) 기타 발견분 (R9 실사)
- **고아 preamble 2본 추가:** RV3 §5-8 은 `ch1_appD_si.tex` 만 고아로 계상했으나, R9 `\input` 전수 스캔에서 `ch1_preamble.tex`·`ch2_preamble.tex` 도 고아 확인(§2.2 — S-002 통합 잔재). 병합 무해(제외 대상), 이력 보존.
- **asset 앵커 총계:** 도구 집계 ch1 265 + ch2 92 + ch3 0 = 357(R1 "자산 357/357 무유실" 원장 claim 과 일치). Ch3 는 `% 자산:` 주석 규약 미사용(R5/R7 신규 저작 — 앵커는 [V22-*] 계열 별도)이라 도구 집계 0(유실 아님).
- **`sethuraman_stresspot2010` 쪽 번호 ★확인필요**(원장 잔여) — 병합 전 사용자 확인 권장.

---

## 6. 검수 이력 요약 (참조 포인터)

- **FR 대공사(심층 검토, 사용자 지시 "빡세게"):** 23창 절별 4관점 병렬 검토(`comp_FR/A01~A23_REVIEW.md`, 보고 ~600KB). 총 발견 H 29·M 208·L ~120.
  - **H 29 전건 처분**(C-040~049 — 재유도·코드 대조·Crossref·aux 확인 후 축자 집행; 1건 A13-H2 는 P5 부분 집행) + 서지 정정 C-050. 상세 = `comp_FR/FR_T_H_TRIAGE_PREP.md`.
  - **M 정정형 38+3**: C-051(집행 38·SKIP 12, 기계 패스) + C-053(미세 잔여 3). 보완·수식화형 M 158 + L 전건(~120) = **보류 풀**(각 A##_REVIEW.md 에 완성 LaTeX 제안 보존 — 사용자 선별 채택 대기). 상세 = `comp_FR/FR_T_ML_TRIAGE.md`·`EXEC_M1~M4.md`.
  - **이월 14**: R8(C-054) 집행 14·기해소 6·SKIP 21(부록 카운터 (a) 포함). 상세 = `comp_R8/R8_EXEC.md`.
- **선행 검수(RV):** RV1(Ch1)·RV2(Ch2)·RV3(교차) — `comp_RV/`. 트리아지 즉시 정정 ~22곳(C-039). RV3 §5 = 본 문서 §5-d 입력.
- **계보 감사(RA):** v1.0.19→v1.0.22 미로그 축소·생략·왜곡 0건(`AUDIT_LINEAGE_v19_v22.md`). 구획 전환 스윕(R1b) = `R1B_SWEEP_LIST.md`.
- **변경 통제:** 전 변경 = `V1022_CHANGE_LOG.md`(S-001~012·A-011~018·C-038~054 등) ↔ snapshot diff 1:1. 코드 게이트 = `test_gates_v1022.py` R9 재실행 **exit 0**(전건 GREEN).

---

*본 문서는 R9 초안. 병합 실행·시험 빌드는 사용자 별도 세션(D22-8). 수치·상태는 2026-07-18 원장·파일·도구 출력 기준.*
