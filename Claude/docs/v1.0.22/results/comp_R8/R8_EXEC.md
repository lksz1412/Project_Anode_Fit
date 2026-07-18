# R8_EXEC — R8 이월 목록 집행 (v1.0.22)

- 실행일: 2026-07-18 (오푸스 집행 창)
- 작업 디렉토리: `Claude/docs/v1.0.22/`
- 규율: git 조작 금지 · 빌드 실행 금지 · `Codex/` 무접촉 · 수식·값·라벨명 변경 금지(산문·참조 서식 층위만) · 애매하면 SKIP+사유
- 출처: `results/comp_RV/RV3_CROSS_REPORT.md`(RV3-A1·B4·L급) + `results/V1022_CHANGE_LOG.md` C-039 행 말미 "R8 이월" 기재
  ("R8 이월: RV3-A1(참조 스타일 3종 통일)·B4a/c(라벨 stale·letter \ref화)·L급 잔여·sec02:109/sec03:85 스코프 재검")
- 선행 처리 확인: FR 대공사(C-040~053)·M 집행(EXEC_M1~M4)·트리아지(C-039) 를 정독해 **각 항목 집행 전 현행 grep 으로 잔존 여부 확인**. `_sections/` 전량 스캔.

---

## 0. 집계 (요약)

| 구분 | 수 | 비고 |
|---|---|---|
| **집행** | **14** | 항목1 참조스타일 4 · 항목3 Ch1축약형 8 · 항목4 L급(RV1-L2) 2 |
| **기해소** | **6** | 선행 phase(C-039·EXEC_M2)가 이미 정정 |
| **SKIP** | **21** | 라벨 mechanism(B4) 2 · 스코프 재검-유지 2 · L급 문체/보완/물리 13 · 항목1 범위 밖 4 |

수정 파일 6본(전량 `_sections/`): `ch1_sec03_center`(1) · `ch1_sec05_width`(3) · `ch1_sec11_lcointro`(1) · `ch1_sec14_lcodecomp`(2) · `ch1_sec17_msmr`(5) · `ch2_appA_traps`(2) = **14 치환**.
집행 후 검증: 잔존 "Ch1/Ch2/Ch3" 축약형 rendered 0건 · "Part II" 절제목·서지(P5) 보존 · `\label`/`\eqref`/`\ref` 라벨명 무변경 · 수식·값 무접촉. **빌드 미실행(규율)** — 렌더 확인은 마스터 재빌드 소관.

---

## 1. 항목 1 — RV3-A1 참조 스타일 3종 통일 (장 간 참조)

권고 규약(RV3-A1) = **① 명시 "Chapter 2 \S\ref{…}"** 로 통일(② 무접두 \S\ref, ③ 역사명 "Part II" 를 ①로).
대상 = Ch1(흑연) → Ch2(LCO) **본문 산문** 절 참조. cross-ch sec:lco-* 라벨은 .aux 상 **2.x** 로 해소(예: sec:lco-electronic=2.5) → Ch1 단독 PDF 에서 bare "§2.5" 는 혼동 유발이라 "Chapter 2" 접두가 정당.

### 집행 (4)

| 파일:행 | 현행 → 개정 | 판정 |
|---|---|---|
| `ch1_sec03_center:113` | `더해진다(\S\ref{sec:lco-code})` → `더해진다(Chapter 2 \S\ref{sec:lco-code})` | 집행 (RV3-A1 예시 sec03:111 상당, 행이동) |
| `ch1_sec05_width:281` | `전극-중립 일반화는 \S\ref{sec:lco-direction})` → `… Chapter 2 \S\ref{sec:lco-direction})` | 집행 (내부 sec:dist 와 cross-ch 를 명시 구분) |
| `ch1_sec05_width:384` | `\S\ref{sec:lco-electronic} 의 LCO 전자 엔트로피와` → `Chapter 2 \S\ref{…} …` | 집행 (**RV3-A1 예시 sec05:379**, 행이동) |
| `ch1_sec05_width:409` | (keybox 분포 다리) `…라는 것이 \S\ref{sec:lco-electronic}` → `… Chapter 2 \S\ref{…}` | 집행 (:384 와 동일 패턴 — 동일 파일 정합) |

### 기해소 (RV3-A1 잔존 — 선행 정정)

| 항 | 현행 확인 | 근거 |
|---|---|---|
| ③ "Part II" (Ch1→Ch2 지칭, sec01:32·156·sec02b:29) | 현행 "Chapter 2" | C-039 ①(RV3-B1/RV1-M2) |
| 예시 sec02b:30 | 현행 `Chapter 2 의 $\Omega_j^\mathrm{cat}$(…\S\ref{sec:lco-hys})` — 접두 존재 | C-039 ① 동반 해소 |
| sec01:160 / sec00_intro:64 / sec07:64 / sec01:33 | 모두 "Chapter 2" 접두 존재 또는 문장 주어가 "Chapter 2(LCO)"로 앵커 | 기존 style ① / C-039 |

### SKIP (범위 밖 — 사유)

| 대상 | 사유 |
|---|---|
| `ch1_sec01:219` (LCO 질서화(\S\ref{sec:lco-hys-od})) | "term(\S\ref)" **병렬 열거**(단상폭·두-상·LCO·Part T) 중 한 항 — "LCO" 어휘가 이미 지시. 한 항만 "Chapter 2" 삽입 시 열거 정합 파괴 |
| 부록 bare lco 참조 (appA:9·46·84, appB:34·95·97·145) | 부록 검산표·코드맵 **기술 register**(":46/:84"는 "본문 \S\ref{sec:lco-center}"로 "본문" 지시 이미 존재). RV1/RV3 이 A1 로 미지목 |
| `ch1_sec18_inputs` 표 행(56–61) | 입력 인자 **표 셀**(\eqref/\ref 목록) — 산문 아님, 셀마다 접두는 잡음 |
| `\eqref{eq:lco-*}` (sec04:223 등) | 식 번호 참조("(2.x)"에 장번호 내포) — RV3-A1 은 절 참조 규약이 초점, 미지목 |
| Ch3 → Ch1/Ch2 bare 참조(ch3v22_*) | **RV3 가 Ch3 를 명시 제외**("동시 저작 중, 초점 밖"). Ch3 계승참조는 R5 저작기 규약(notation:10 "계승분 …값·의미 무변경" 선언)이라 R8 이월 대상 아님 |

---

## 2. 항목 2 — RV3-B4a/c (부록 라벨 stale · letter \ref화)

### SKIP — B4a (라벨 stale 해소)

- 현행: `ch2_appA_traps:6` `\phantomsection\label{sec:traps-thermal}` · `ch2_appB_codemap:6` `\phantomsection\label{sec:codemap-thermal}` — 둘 다 `\section*`(비번호) 뒤 정의.
- **.aux 실검증** (`ch1_graphite_v1.0.22.aux`):
  - `\newlabel{sec:traps-thermal}{{B}{78}…}` → **"B"로 해소**(부록 C 여야 함)
  - `\newlabel{sec:codemap-thermal}{{B}{79}…}` → **"B"로 해소**(부록 D 여야 함)
  - 원인: 직전 번호 부록(부록 B=ch1_appB `\section`)의 카운터를 `\phantomsection` 이 포착.
- **참조하는 `\ref` 0건**(grep 확인) → stale 은 **잠재적**(현재 어디에도 렌더되지 않음).
- SKIP 사유: stale 해소는 카운터 mechanism 조작(`\refstepcounter`/수동 카운터) 또는 라벨 재정의 필요 → **"산문·참조 서식 층위"를 벗어남**(라벨명 변경 금지 규율에도 저촉). 잠재적(무참조)이라 렌더 결함 무. **애매+범위초과 → SKIP.**

### SKIP — B4c (하드코딩 "부록 C/D" → \ref 전환)

- 대상 하드코딩: `ch2_sec04:22`("부록 C") · `ch2_sec04:110`("부록 D") · `ch2_sec07:52`("부록 C") · `ch2_sec08:95`("부록 D") · `ch1_appB:135`("부록 D").
- SKIP 사유: RV3-B4 가 "**라벨 정상화(B4a) 선행**" 을 명시. B4a 가 위 사유로 미집행이므로, 지금 `\ref{sec:traps-thermal}`/`\ref{sec:codemap-thermal}` 로 전환하면 **"부록 B"로 오렌더**(현행 하드코딩 "부록 C/D"는 **정확**한데 오히려 회귀). **선행조건 미충족 → 전환 금지 → SKIP.** 현행 하드코딩 letter 유지가 정답.

### 기해소 — B4b (부록 주석 헤더 C/D)

- `ch2_appA_traps:2` 주석 = 현행 "부록 C"(RV1-L6 대상), `ch2_appB_codemap` 헤더도 정정됨 — C-039 ⑪[RV3-B4b].

---

## 3. 항목 3 — Ch1 축약형 8건 ("Ch1" → "Chapter 1")

LCO 장(Ch2 내용) 파일에서 Chapter 1(흑연)을 "Ch1"로 축약한 참조 **정확히 8건**. 같은 파일들이 이미 "Chapter 1" 전형(sec14:47·54·57, sec15:217·233·277·366)을 쓰므로 축약형만 잔존한 불일치 → 전형으로 통일.

### 집행 (8)

| 파일:행 | 현행 문구 → 개정 |
|---|---|
| `ch1_sec11_lcointro:169` | `Ch1 곡선 클래스` → `Chapter 1 곡선 클래스` (※ 같은 행 "Part II"는 Ch2 자기 절제목 계열 — P5 보존) |
| `ch1_sec14_lcodecomp:70` | `기존 Ch1 logistic 이` → `기존 Chapter 1 logistic 이` |
| `ch1_sec14_lcodecomp:79` | `Ch1 흑연과 동형이며` → `Chapter 1 흑연과 동형이며` |
| `ch1_sec17_msmr:73` | `Ch1 logistic 서식은` → `Chapter 1 logistic 서식은` |
| `ch1_sec17_msmr:82` | `Ch1 의 점유 $\theta_{\eq,j}$` → `Chapter 1 의 점유 …` |
| `ch1_sec17_msmr:83` | `Ch1 의 진행률 $\xi_{\eq,j}$` → `Chapter 1 의 진행률 …` |
| `ch1_sec17_msmr:102` | `Ch1 평형 peak 은` → `Chapter 1 평형 peak 은` |
| `ch1_sec17_msmr:113` | `Ch1 의 곡선 골격` → `Chapter 1 의 곡선 골격` |

검증: 개정 후 `_sections/` 전량 rendered "Ch1/Ch2/Ch3" 축약형 **0건**. "Chapter 1"(item3 3파일) 개수 3(선존)→11(+8).

---

## 4. 항목 4 — L급 잔여 중 참조·표기 정합류 (문체 취향 제외)

RV1·RV2·RV3 의 L 항목 중 **참조 서식·기호 표기 불일치** 성격만 선별 집행. 순수 문체·어감·보완·물리정직·빌드는 SKIP.

### 집행 (2) — RV1-L2

| 파일:행 | 현행 → 개정 | 근거 |
|---|---|---|
| `ch2_appA_traps:40` | `$g_j(\xi)$(Ch1 조성 자유에너지)` → `$g_j(\xi)$(앞 파트 조성 자유에너지)` | RV1-L2. g_j(ξ)=Part 0(sec:sm-mf)=본 장 내부 → "Ch1" 은 stale 자기지칭 |
| `ch2_appA_traps:50` | `$u_j$ vs Ch1 $u_j$` (행 헤더) → `$u_j$ vs 앞 파트 $u_j$` | RV1-L2. 같은 행 내용(:52)이 이미 "앞 파트 \S\ref{sec:hys}·같은 문서 내" → 헤더 정합 회복 |

주: 이 2건은 **Ch1-내부 stale 자기지칭**(부록 C=Part T=Ch1 소속)이라 항목3(Ch2→Ch1, "Chapter 1")과 구분 — 같은 파일 관용어 "앞 파트"(:52)로 통일.

### 기해소 (선행 정정)

| 항 | 확인 | 근거 |
|---|---|---|
| RV1-L6 (appA:2 주석 "부록 A"→C) | 현행 "부록 C" | C-039 ⑪ |
| RV3-A3 (부록 D `ch2_appB:14` eq:logistic 귀속) | 현행 `Part I 기원의 $\xi_j$(본 파트 식~\eqref{eq:logistic})` 이중표기 | C-039 ⑨ |
| RV1-L3 (appB 코드 버전 v1.0.19) | `ch1_appB:5` 현행 v1.0.21(계보 각주). appB:134·bib:44 는 역사 앵커로 의도 보존 | EXEC_M2 A16-M1 |

### SKIP (참조·표기 정합 성격 아님 — 사유)

| 항 | 등급 | SKIP 사유 |
|---|---|---|
| RV1-L1 (sec02a:172 mckinnon 부호 half-line) | L | **보완류**(가드 문장 신설) — 참조서식 불일치 아님. FR 보류 풀 |
| RV1-L4 (eq:Se-ch2 라벨 "-ch2" 접미) | L | RV1 자체 "조치 불요". **라벨명 변경 금지** 규율에도 저촉. 실충돌 0(로그) |
| RV1-L5 (swiderska2019/LastPage multiply-defined) | L | 빌드 로그 **양성 경고**(xr 산물, undefined 0). 산문 아님 |
| RV1-L7 (Q_bg 기호표 미등재) | L | 기호표 **행 추가=보완**, "저우선·재편무관 선존" 자평. 표기 정합 아닌 완결성 |
| RV2-04 (게이트 절연끝점 잔차) | L | 물리 근사 정직성 — 참조·표기 아님. RV2 Tier3 "수정 말 것" |
| RV2-05 (시연값 비단조) | L | 캡션 가드 존재. demo 값 배열 취향. RV2 Tier3 |
| RV2-06 (g_max 단위 "e/eV/atom" vs "states/(eV·Co)") | L | **단위=물리 표기**(값 g_max=13 인접) — "산문·참조 서식" 초과, 값 경계. RV2 **Tier3 "수정 말 것"**. per-atom↔per-Co 정규형 판단 필요 → SKIP |
| RV2-07 (gap 공식 3회 반복) | L | 서술 중복(교육적) — 표기 아님. RV2 Tier3 |
| RV2-08 (multiply-defined 경고) | L | =RV1-L5. 빌드 위생 |
| RV2-09 (파일명 ch1_sec11~17 함정) | L | 유지보수 주석 매핑. 렌더 무영향 |
| RV3-A2 (마스터 주석 "전방참조 22곳" vs 36) | L | **비렌더 주석** metadata. "22"는 변경로그(S-003)에도 계보 기록 → 변경 시 이력 발산. 산문·참조 층 밖 |
| RV3-C2 (MSMR 계보 이원 인용) | L/M | RV3 "현 상태 모순 없음 — **병합 시 통합**". merge 소관 |
| RV3-D2 (sec11:45·appB:8 "본서") | L | sec11:45 "본서 전역"=tier 범례의 **의도적 3장 공통 선언**(C-039 ②가 Ch1 §7 에 동일 wording 복제) → "본 장" 강등 시 의미 축소. appB:8 "본서 권위"=doc-vs-code. RV3 자체 "병합 규칙 명문화" merge-decision |

### 스코프 재검 (C-039 지정) — 재검 후 유지 (SKIP·현행 정당)

| 대상 | 현행 | 재검 결과 |
|---|---|---|
| `ch2_sec02_config:109` | "이것이 **본 장에서** 가장 흔한 실수(같은 물리 두 번 세기)를 막는 원리" | **유지**. 이중계산 함정은 Part I(logistic 자동생성 config)+Part T(분해) 를 **가로지르는 장-전역 pitfall** → "본 장"(Ch1) 이 오히려 정확. C-039 의 "범위 선언 12곳 본 장 유지" 판정과 정합. "본 파트" 강제는 부정확 |
| `ch2_sec03_vibel:88` (구 :85, 행이동) | "**본 장** 주 사례에서 electronic 은 보정항이다" | **유지**. "본 장 주 사례(흑연 하프셀)"=Ch1 대표 사례를 LCO 와 대비하는 **장-스코프 대조** → "본 장" 정당 |

주: Part T 는 "본 파트"(sec00_intro 다수·sec06:50 "본 파트가 세운 분포 식" 등)와 "본 장"이 혼용되나(RV3-B2), C-039 가 파트-구축물 지칭 8곳만 "본 파트"로 전환하고 **장-전역 범위 선언은 "본 장" 유지**로 판정. 위 2건은 후자에 해당 → 유지.

---

## 5. 최종 집계

- **집행 14** = 항목1(4) + 항목3(8) + 항목4-RV1L2(2)
- **기해소 6** = RV3-A1③·A1예시(sec02b:30)·B4b·RV1-L6·RV3-A3·RV1-L3 (선행 C-039·EXEC_M2)
- **SKIP 21** = B4a·B4c(2) + 스코프재검-유지(2) + L급 비정합류(RV1-L1·L4·L5·L7·RV2-04~09·RV3-A2·C2·D2 = 13) + 항목1 범위밖(sec01:219·부록/표 bare·\eqref·Ch3 = 4)

규율 준수: 수식·값·라벨명 무변경(산문·참조 서식 층위만) · git·빌드·Codex 무접촉 · 각 치환 축자 확인 후 집행 · 애매·범위초과 전건 SKIP+사유.
