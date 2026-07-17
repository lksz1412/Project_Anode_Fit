# RV3 — 장 간 교차 정합 검수 보고 (v1.0.22)

> 검수 창: RV3 (Opus) — 장 사이·파트 사이 **경계** 전담. 보고 전용(수정·git·Codex 접근 없음).
> 대상: 신 Ch1(graphite, 80p) + 신 Ch2(LCO, 25p) 전 소스. 초점 = 절 내부가 아니라 경계.
> 작성 시각 기준 파일 상태: `ch1.aux` 09:13 빌드(소스 ≤09:11, **안정**), `ch2.aux` 10:44 빌드(**안정**),
> `ch3` 는 11:21 현재 **동시 저작 중**(아래 §0 참조) — RV3 초점 밖.
> 방법: `.aux` 라벨맵 전수 파싱 + xr 참조 census(스크립트) + 경계 파일 정독.

---

## §0. 조립 구조 지도 (이 검수의 전제 — 명칭 함정 주의)

`ch1_graphite_v1.0.22.tex` (마스터) 와 `ch2_lco_v1.0.22.tex` (마스터) 의 `\input` 순서로 확정한 실제 소속:

| 물리 파일 | 소속 문건 | 파트 |
|---|---|---|
| `ch1_sec00`~`ch1_sec10` | **Ch1** | Part 0(통계역학) · Part I(흑연 곡선) |
| `ch2_sec00`~`ch2_sec10` | **Ch1** | **Part T (흑연 열특성)** ← 파일명은 `ch2_` 지만 Ch1 소속 |
| `ch1_sec18`, `ch1_appA/B`, `ch2_appA/B` | **Ch1** | 입력·부록 |
| `ch1_sec11`~`ch1_sec17` | **Ch2** | **Part II (LCO)** ← 파일명은 `ch1_` 지만 Ch2 소속 |
| `ch2v22_*` | **Ch2** | 서두·기호·bib |

**★핵심 함정(P3.7 대상):** 파일명 접두사(`ch1_`/`ch2_`)와 실제 소속 문건이 교차 반전한다.
`ch2_sec*` = Ch1 의 Part T, `ch1_sec11~17` = Ch2 의 Part II. 병합·검수 시 파일명으로 소속을 추정하면 오판.

**xr 배선:** `ch1` 은 `\externaldocument{ch2}`(전방 22곳 선언), `ch2` 는 `\externaldocument{ch1}`. 라벨 충돌 = `LastPage` 뿐(무해).

**Ch3 상태(초점 밖, 맥락만):** 검수 도중 `ch3_si_v1.0.22.tex` 마스터가 `ch1_appD_si` 를 드롭하고
`ch3v22_sec01_map`~`sec05_code` 신설분으로 교체됨(11:21). → `_sections/ch1_appD_si.tex` 는 **현행 어느 마스터에도 미포함(고아 소스)**.
그 파일의 미해소 참조 3건(`ssec:si-gap`/`ssec:si-anchor`/`ssec:si-facts`, 행 42·48·52)은 빌드 대상이 아니므로 **무효화됨**. (병합 대비 목록에 정리로만 계상.)

---

## §1. xr 장 간 참조 — 전수 결과

전 소스 참조 census(스크립트 `scratchpad/xref_census.py`): **Ch1→Ch2 36건, Ch2→Ch1 94건** 모두 라벨 해소됨.
라벨 충돌 없음(local shadowing 0). **미해소 0건**(Ch1·Ch2 범위). 내용 정합 spot-check 다수 통과(§4-tier 통과 목록).
아래는 경계에서 발견한 **정합/스타일** 이슈만.

| ID | 파일:행 (참조측 → 대상측) | 등급 | 분류 | 문제 | 제안 |
|---|---|---|---|---|---|
| **RV3-A1** | 참조 스타일 전역 (아래 근거행) | **M** | xr 스타일 불일치 | 장 간 참조 표기 규약이 **3종 병존**: ① 명시 "Chapter 2 §…"(`ch2_sec09_method:20`, `ch2_sec02_config:128`, `ch2_sec03_vibel:77`), ② 무접두 "\S\ref{sec:lco-*}"(`ch1_sec02b_part0:30`, `ch1_sec03_center:111`, `ch1_sec05_width:379`), ③ 역사명 "Part II"(`ch1_sec01_n0n1:156`). 셋이 같은 Ch1→Ch2 참조에 혼용 | 한 규약으로 통일(권장 ①). 병합 시 특히 ③ 제거 필요 |
| **RV3-A2** | `ch1_graphite_v1.0.22.tex:8` (주석) | **L** | 카운트 staleness | 주석 "전방 참조(LCO 장 **22곳**)" — 실제 Ch1→Ch2 참조는 **36건**(본문 9 + Part T 6 + 입력/부록 21). 문서화 수치 낡음 | 36 으로 갱신하거나 "본문 N곳+부록" 로 명세 |
| **RV3-A3** | `ch2_appB_codemap.tex:14` → `eq:logistic`(=Ch1 §1.101, Part T) | **L** | 파트 귀속 부정확 | "Part I 의 $\xi_j(V,T)$~\eqref{eq:logistic}" — 그러나 `eq:logistic`(1.101)은 **Part T** 식. `ch2_sec08_synthesis:23` 은 같은 것을 "Part I 의 $\xi_j$(**본 파트 식**~\eqref{eq:logistic})" 로 정확히 이중표기 → 두 곳 표기 불일치 | appB 도 "Part I 개념 / 본 파트 식" 이중표기로 맞추거나 `eq:xieq`(Part I 1.69)로 교체 |

*내용 정합 통과 확인(대표):* `config:128 → sec:lco-decomp`(§2.4 "반응 엔트로피 삼분해와 슬롯 규칙") ✓,
`vibel:77/89 → sec:lco-electronic`(§2.5) ✓, `method:20 → sec:lco-code`(§2.7 "MSMR 동형") ✓,
`ch2v22_notation:7-10 → eq:Uj/logisticsolve/dUhys/Ubranch/sm-mc-balance/sum` 6건 전부 라벨 제목과 의미 일치 ✓,
`partT_divider:14 → eq:sm-mc-balance·eq:eqpeak·sec:width` ✓.

---

## §2. Part 0 ↔ Part I ↔ Part T ↔ Part II 경계 + 기호 충돌

| ID | 파일:행 (양측) | 등급 | 분류 | 문제 | 제안 |
|---|---|---|---|---|---|
| **RV3-B1** | 선언 `ch1_sec00_intro:23-25` ↔ 사용 `ch1_sec01_n0n1:156`, `ch1_sec02b_part0:29` ↔ Ch2 절제목 `ch1_sec11_lcointro:4` | **H** | 역사명 vs 신 구조(P3.7/P5) | Ch1 서론은 자기 구조를 **"Part 0→Part I→Part T"** 세 층으로 선언(§1_sec00:25), **Part II 부재**. 그런데 (a) Ch1 이 Ch2 를 "**Part II**"로 지칭(sec01:156 "Part II(\S\ref{sec:lco-intro})가 연다"), (b) Ch2 의 첫 절 제목이 "**Part II 도입**"(§2.1). 즉 신 구조에서 Chapter 2 인데 본문 정체성은 "Part II". 파트 순번이 0·I·T(Ch1)·II(Ch2)로 **비선형**(II 가 T 뒤) | 장 간 지칭을 "Chapter 2"로 통일. "Part II 도입" 절제목은 역사 보존 대상일 수 있으나(P5), 최소한 Ch1→Ch2 **본문 지칭**에서 "Part II" 제거. 병합 대비 필수 항목 |
| **RV3-B2** | `ch2_sec01_partition:43,58,89`·`ch2_sec02_config:109,131`·`ch2_sec03_vibel:78,81,85`·`ch2_sec04_einstein:20,21`·`ch2_sec06_limits:34,49`·`ch2_sec07_revheat:52,57,58`·`ch2_sec09_method:7,53,57,60,61` (모두 Ch1 Part T) | **M** | 스코프어 오용 | Part T 는 **파트**인데 내부 절들이 "**본 장**"(=this chapter)으로 자기 파트-스코프 진술("본 장의 닫힌식", "본 장이 세운 분포 식"). 서두 `ch2_sec00_intro`·맺음 `ch2_sec10_closing`·`ch2_sec05_mixing`(일부)만 "**본 파트**"로 전환됨 → 같은 파트가 "장/파트" 혼성. `ch2_sec05_mixing` 은 42행 "본 파트" vs 190·193·224행 "본 장"로 **동일 파일 내 혼용**. (구 Ch2 시절 "본 장" 잔재) | Part T 전 절의 파트-스코프 "본 장"→"본 파트" 일괄 전환. Ch1 전체를 뜻하는 "본 장"과 구분 |
| **RV3-B3** | `ch2_sec04_einstein:20-22` (guard 자체), `ch2_appA_traps:51` ↔ 충돌 대상 `ch1_sec04_hys`(§1.4, `sec:hys`) | **M** | 기호충돌 guard 의 스코프 오류 | u_j 동명 guard: "…앞 파트 \S\ref{sec:hys} spinodal 근 $u_j=\sqrt{1-2RT/\Omega_j}$ 와 동명 별개…**본 장 안에서 $u_j$ 는 오직 $\theta_{E,j}/T$**". 그러나 spinodal u_j 도 einstein u_j 도 **둘 다 Ch1**(Part I §1.4 + Part T §1.14). 따라서 "본 장 안에서 오직"은 **거짓**(장 스코프에선 u_j 2의). guard 자신이 "절-국소 기호"라 하면서 스코프어만 "본 장" → 병합유발 자가모순 | "본 장 안에서"→"**본 절/이 절 안에서**"(절-국소). guard 무결성 직결이라 우선 |
| **RV3-B4** | 부록 헤딩 `ch2_appA_traps:4`(부록 C)·`ch2_appB_codemap:4`(부록 D) ↔ 라벨 `sec:traps-thermal`/`sec:codemap-thermal`(둘 다 카운터 "B") ↔ 주석 `:2`(부록 A/부록 B) | **M** | 부록 C/D 재번호 잔재 | 곡선 부록 A·B(`\section` 자동번호) 뒤 열특성 부록은 **`\section*` 수동 "부록 C"/"부록 D"**(병합 후 letter 는 정확). 그러나 ① 라벨 `sec:traps-thermal`·`sec:codemap-thermal` 이 stale 카운터 **"B"** 포착(현재 `\ref` 무사용이라 **잠재적**), ② 소스 주석은 여전히 "부록 A"/"부록 B"(구 Ch2 잔재), ③ 본문 참조는 **하드코딩 "부록 C"/"부록 D"**(`ch2_sec04_einstein:22`, `ch2_sec07_revheat:52`, `ch2_sec08_synthesis:95` 등) — letter 변경 시 동반수정 필요한 취약점 | (a) 라벨 stale 해소 또는 명시적 수동 letter 참조 체계로 통일, (b) 주석 A/B→C/D 정정, (c) 하드코딩 "부록 C/D"를 `\ref` 로 전환(단 라벨 정상화 선행) |

*기호 guard 통과 확인:*
- **g 4종** guard `ch2_sec05_mixing:42-44`: `g_j(x)`(봉우리가중, `eq:gj`) ≠ `g_j(\xi)`(Part 0 조성 F, `sec:sm-mf`/`eq:gxi`) ≠ `g(\theta)`(Part T BW, `eq:BW`) ≠ `g(E_F)`(Part T DOS, `eq:Se-ch2`) — 세 대상 참조 모두 라벨 정확, 스코프어 "본 파트" 정확. ✓ **다만 cross-chapter 로 Ch2 의 `g(E_F,x)` MIT 게이트(`eq:ggate` 2.30)는 5번째 g-역할** — Ch1-국소 "g 4종" 카운트 밖(수용 가능하나 병합 시 재계수 필요).
- **η 2종** guard `ch1_sec05_width:143` ↔ `sec:broadening`(§1.7, `U_app=U_j+η`): 원논문 과전위 η vs 겉보기-중심 국소 η 분리 — 대상 절 내용 일치. ✓ (둘 다 Ch1 Part I 내, cross-chapter 아님.)
- **ξ 배향**: `ch1_sec11_lcointro:37` "흑연 $\xi_j$ 탈리튬화 진행이었듯 LCO 충전(탈리튬화)이 $\xi:0\to1$", 방향 슬롯 `eq:lco-sigmaslot` 전극중립 규약 — Ch1↔Ch2 부호 대칭 일관. ✓

---

## §3. 다리(srcbox) 계보 정합

통합 srcbox "다리" 박스 **13본**(task 의 "11" = R2/R3 **초안 파일** 11개; 일부는 한 박스에 다refs 묶임, 일부 Part T 박스는 ref-bridge 아님).

**흑연/Ch1 측(7 ref 대응):** `sec01`(측정원리: weppner_huggins1977+reynier2003+baek_pilon2022 묶음) · `sec02a`(mckinnon1983) · `sec05`(bazant2013, `eq:br-bazant2013-1`) · `sec07-broadening`(dreyer2010/11) · `sec07-revheat`(bernardi1985) [+ allart2018 은 `sec02_config`·`sec09_method` 인용].
**LCO/Ch2 측(4 ref, 모두 `eq:br-*` 통합):** `sec13`(vanderven1998 §2.12) · `sec14`(reynier2004 §2.20) · `sec15`(marianetti2004 §2.22) · `sec17`(msmr §2.37).

| ID | 항목 | 등급 | 분류 | 문제/확인 | 제안 |
|---|---|---|---|---|---|
| **RV3-C1** | reynier2003(Ch1 bib) vs reynier2004(Ch2 bib) | **L(확인)** | 인용 혼동 리스크 | 동일 저자군 두 논문이 인접 역할(흑연 엔트로피 vs LCO 엔트로피)로 장 분리 인용. bib 는 **깨끗이 분리**(ch1=reynier2003, ch2=reynier2004, 상호오염 0). 혼동 아님 확인 | 유지. 병합 시 두 key 공존 확인만 |
| **RV3-C2** | MSMR 분산 처리 | **L/M(병합)** | 개념 중복 배치 | MSMR 이 **양 장에 분산**: Ch1 Part T(`ch2_sec09_method:20`)는 msmr_partI/II(Garrick·Paul 2024, MCMB 열정량) 인용, Ch2(`sec17`/`sec:lco-code`)는 msmr_origin2017·bakerverbrugge2018(명명 원전) 인용. 상충 아님(다른 측면)이나 계보 근거가 장별로 갈림 | 병합 시 MSMR 계보 각주 1곳 통합 권장. 현 상태 모순 없음 |
| **RV3-C3** | 다리 박스 중복/모순 | **통과** | — | 흑연 7 · LCO 4 다리의 대상 식·계보 주장이 서로/본문과 **모순·중복 없음** 확인(각 박스가 고유 원전·고유 대상식). `msmr_partI` 식별함정은 `ch1v22_bib.tex:40` 각주가 선제 가드("ECS 'Part 1'과 별개 논문") ✓ | — |

---

## §4. 용어·컨벤션 전역

| ID | 파일:행 (양측) | 등급 | 분류 | 문제 | 제안 |
|---|---|---|---|---|---|
| **RV3-D1** | 정의 `ch1_sec11_lcointro:45-47`(**Ch2** §2.1.1 각주) ↔ 사용 `ch1_sec07_broadening:64`(**Ch1** Part I), `ch1_sec01_n0n1:247`(**Ch1**) | **H** | tier 등급 장 간 의존 | tier A/B/C **유일 범례**가 Ch2 §2.1.1 각주에만 존재("등급 표기(**본서 전역**)"). 그러나 Ch1 이 tier 를 사용(sec07:64 "tier C…신뢰 등급 범례는 \S\ref{sec:lco-map} 각주" → **Ch2 로 넘김**; sec01:247 "tier B"). **Ch1 은 독립 PDF** 라 그 각주가 Ch1 문건에 부재 → 표준독자 tier 미해소. "본서 전역" 선언과 물리적 위치(Ch2) 불일치 | tier 범례를 **양 장 공통 위치**(Ch1 기호절/공통 preamble, 또는 각 장 서두)에 배치. 최소한 Ch1 에도 범례 복제 |
| **RV3-D2** | `ch1_sec11_lcointro:45`("본서 전역"), `ch2_appB_codemap:8`("본서가 권위") | **L** | "본서" 스코프 | 단일 장 내부에서 "본서(=책 전체)" 권위·전역 선언. 별개 컴파일 문건에서 "본서" 지칭 대상이 모호(현재 각 장 = 별개 PDF) | 병합 전엔 "본 장/본 문건", 병합 후 "본서" 로 정리하는 규칙 명문화 |

*통과 확인:* `ch2v22_notation:6`·`ch2v22_sec00_intro:4` 의 "본 장"(=Ch2) — 정확. Ch2 가 Ch1 을 "Chapter 1 Part T/Part I" 로 명시 역참조(`ch1_sec14_lcodecomp:47,54`, `ch1_sec15_lcoelec:217,233`) — 명확. ✓

---

## §5. 병합 대비 목록 (MERGE_READINESS 입력)

단일 문건 병합 시 **깨지거나 손봐야 할** 서술 — 우선순위 순:

1. **[H] Part 명칭 선형화 불가.** 현 순번 = Part 0 · I · T(Ch1) · II(Ch2). "Part II"(LCO)가 "Part T"(열특성) 뒤라 II<T 역전. 병합 시 파트 재명명 또는 Chapter 체계로 승격 결정 필요. (RV3-B1)
2. **[H] tier 범례 위치.** Ch2 단독 소재 → 병합 시 전역 위치로 이동해야 "본서 전역" 선언 실체화. (RV3-D1)
3. **[M] 하드코딩 장/부록 문자열.** "Chapter 1"/"Chapter 2"/"Ch1"/"Ch2"(`ch2v22_*`, `ch2_sec08_synthesis:224`, `ch2_sec09_method:20,63`) 및 "부록 C"/"부록 D" 수동 letter(`ch2_sec04_einstein:22`, `ch2_sec07_revheat:52`, `ch2_sec08_synthesis:95`) — 병합 후 장·부록 번호 재배열 시 전부 수동 추적. `\ref`/매크로화 권장. (RV3-A1·B4)
4. **[M] "본 장/본 파트/본서" 스코프어.** Part T 의 "본 장"(RV3-B2), guard 의 "본 장"(RV3-B3), "본서"(RV3-D2) — 병합 후 스코프 재정의 필요.
5. **[M] xr 기계장치.** 각 장 `\externaldocument` + 별도 `.aux`, `\renewcommand{\theequation}{N.\arabic}`·`\thesection` 장별 고정. 병합 시 단일 카운터로 통합하면 **모든 식·절 번호 재계산** → 130+ 교차참조 재검. 라벨명 자체는 충돌 없어(§0) 병합 가능하나 번호 표기 전량 갱신.
6. **[M] 파일명↔소속 반전(§0).** `ch2_sec*`=Part T(Ch1), `ch1_sec11~17`=Part II(Ch2). 병합 재조립 시 파일명 신뢰 금물.
7. **[L] bib 중복.** `swiderska2019` 가 ch1·ch2 bib **양쪽**에 존재(별개 PDF 라 정상, 병합 시 중복 bibitem 충돌). 그 외 key 는 장별 분리.
8. **[L] 고아 소스.** `_sections/ch1_appD_si.tex` 현행 마스터 미포함(§0). 병합 목록에서 제외 확인.
9. **[L] MSMR 계보 이원화(RV3-C2).** 병합 시 한 곳 통합.

---

## §6. 4-tier 요약

**● 중대(H) — 3건**
- RV3-B1 "Part II" 역사명 vs Chapter 2 신 구조(파트 순번 비선형·Ch1 이 Ch2 를 Part II 로 지칭).
- RV3-D1 tier 범례가 Ch2 단독 소재, Ch1 이 이를 사용 → Ch1 독립독자 미해소("본서 전역" 선언 무실체).
- (병합) MERGE #1·#2 상동.

**◐ 주의(M) — 4건**
- RV3-A1 장 간 참조 스타일 3종 병존.
- RV3-B2 Part T 내부 "본 장" 스코프 오용(≈8절, 동일파일 혼용 포함).
- RV3-B3 u_j guard 의 "본 장 안에서 오직" 자가모순(장 스코프에선 u_j 2의).
- RV3-B4 부록 C/D 재번호 잔재(라벨 stale "B" 잠재 + 주석 A/B + 하드코딩 letter).

**○ 경미(L) — 5건**
- RV3-A2 전방참조 카운트 22 vs 36. · RV3-A3 `eq:logistic` "Part I 의" 귀속 표기 불일치.
- RV3-C1 reynier2003/2004 혼동리스크(현 분리 확인). · RV3-C2 MSMR 이원 인용. · RV3-D2 "본서" 스코프.

**✓ 통과 확인(경계 무결)**
- xr 라벨 해소 Ch1↔Ch2 130건 전량·충돌 0·미해소 0(Ch1·Ch2 범위).
- g 4종 guard 내용정확 / η 2종 guard 내용정확 / ξ 배향 전극중립 대칭 일관.
- 다리 13본 상호·본문 모순 0(RV3-C3) / bib 장별 분리 정확(reynier·msmr 계열).
- Ch2→Ch1 "Chapter 1 Part T/Part I" 역참조 명시성 / `ch2v22_notation` 계승기호 6참조 의미일치 / `msmr_partI` 식별함정 선제가드.

---

### 부기 — 검수 한계
- Ch3 는 동시 저작 중(11:21 활성)이라 Ch1/Ch2↔Ch3 교차는 **불안정**하여 본 보고 초점 밖. `ch3v22_notation`·`ch1_appD_si`(고아)의 Ch1/Ch2 역참조는 라벨 해소만 확인, 내용정합 미검(대상 장 변동 중).
- 본 보고는 **09:13/10:44 빌드 `.aux` 기준**. 이후 Ch1/Ch2 재빌드 시 번호 재확인 필요(라벨명은 불변이라 정합 결론 유지).
- **수정 없음. 보고만.** 추가 개선은 본문 미수정, 위 제안란으로만 계상(P5 준수).
