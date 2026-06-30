# R2 — w_eff 제거 완전성 + w 이중지위 + 기존 보존 (검수 sub, 9 빌드 교차)

> 대상: `Claude/results/builds/ch1v10/v10-0X/v10-0X.tex`(9종) vs `v10-00_spine/base_v9.tex`(보존 기준, 1644줄).
> Ground truth: `results/research/broadening_w_design.md` + `v10-00_spine/AUTHOR_BRIEF.md`.
> 검토 의견만 — 파일 수정 X. 방법: 라벨 앵커 MD5 byte-비교 + 라인-레벨 unified diff 분류 + live(주석제외) w_eff 식별자 카운트.
> **핵심 구분**: 헤더 주석(`%`) 안의 `w_eff`·`eq:weff` 는 inert(무방). 별개 식별자 `ΔH_a^eff`·`use_dH_eff`·`eq:dHeff` 는 보존 정상(w_eff 아님).

---

## (a) PASS/FAIL 표

### A-1. w_eff 라이브 잔존 (주석 제외, 본문 카운트)

| 빌드 | `\label{eq:weff}`(narrowing 식) | live `\eqref{eq:weff}` | live func/use/floor/w^eff | 깨진 ref | **w_eff 제거** |
|------|:---:|:---:|:---:|:---:|:---:|
| v10-01 (S) | **있음** | 3 | 3+3+2+6 | 없음 | **FAIL** |
| v10-02 (S) | **있음** | 3 | 3+4+2+6 | 없음 | **FAIL** |
| v10-03 (S) | 없음 | 0 | 0+0+1+0 (입력표 1행) | 없음 | **PASS**(경미 1) |
| v10-04 (O) | 없음 | 0 | 0 | 없음 | **PASS(완전)** |
| v10-05 (O) | 없음 | 0 | 1+5+1+1 (legacy 토글 서술) | 없음 | **WEAK PASS** |
| v10-06 (O) | 없음 | 0 | 0 | 없음 | **PASS(완전)** |
| v10-07 (C) | 없음 | 0 | 0 (헤더까지 0) | 없음 | **PASS(완전)** |
| v10-08 (C) | 없음 | 0 | 0 (헤더까지 0) | 없음 | **PASS(완전)** |
| v10-09 (C) | 없음 | 0 | 0 (헤더까지 0) | 없음 | **PASS(완전)** |

- **v10-01/02 = FAIL**: narrowing 식 `w_j^eff=(RT/F)(1−Ω/2RT)`(eq:weff)와 `func_w_eff`/`w_eff_floor_frac` 기계장치를 **그대로 보존**. v01 은 "★주의" 경고문 1줄, v02 는 "단, 이 식은…" 단서만 덧댐 → D2 의 "narrowing 자취 0" 미충족(설명만 추가, 제거 X). 입력표·notation표·node-map N4 행에 `func_w_eff`·`\eqref{eq:weff}` 전부 live.
- **v10-03**: narrowing 식·func_w_eff·notation·nodemap 전부 제거. 잔존 = 입력표 단 1행 `w_eff_floor_frac & 0.05 & (레거시 파라미터, 사용 안 됨)` — 식별자 노출이나 "사용 안 됨" 명시·식 없음. 경미.
- **v10-05**: narrowing 식 제거 완료(eq:weff·label 0)이나 `use_w_eff=False` 토글 서술이 본문 6곳(731-732·1200·1639·1655·1660·notation 214)에 "미사용 legacy" 로 살아있음. 물리 오류는 아니나 "자취 0" 기준 미달.
- **v10-04/06/07/08/09**: 본문 live 자취 0. 04·06 은 헤더 주석에 changelog(inert), 07·08·09 는 헤더에도 0.

### A-2. 기존 보존 (byte MD5 / 라인 diff 분류)

| 빌드 | 전자엔트로피 절(sec:lco-electronic) | LCO staging 표 | 부호사슬(sec:signcheck 표) | ΔH_a^eff 보존 | 깨짐 | **보존** |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| v10-01 | **IDENTICAL** | IDENTICAL | IDENTICAL | 보존 | 없음 | PASS |
| v10-02 | **IDENTICAL** | IDENTICAL | IDENTICAL | 보존 | 없음 | PASS |
| v10-03 | **IDENTICAL** | IDENTICAL | 추가만(bib) | 보존 | 없음 | **PASS** |
| v10-04 | **IDENTICAL** | IDENTICAL | 추가만(bib) | 보존 | 없음 | **PASS** |
| v10-05 | **IDENTICAL** | IDENTICAL | 추가만(bib) | 보존 | 없음 | **PASS** |
| v10-06 | **IDENTICAL** | IDENTICAL | 추가만(bib) | 보존 | 없음 | **PASS** |
| v10-07 | **IDENTICAL** | IDENTICAL | 추가만(bib) | 보존 | 없음 | **PASS** |
| v10-08 | **IDENTICAL** | IDENTICAL | 추가만(bib) | 보존 | 없음 | **PASS** |
| v10-09 | **IDENTICAL** | IDENTICAL | 추가만(bib) | 보존 | 없음 | **PASS** |

- ★**전자 엔트로피 절(Fermi-Dirac→Sommerfeld·MIT 게이트·삽입 ΔS_e<0)은 9종 전부 base 와 byte 동일**(md5 `3c6fd631fb052aaab60be380a681941b`, 178줄). 가장 보존-임계 블록이 전수 무손상.
- **부호사슬 절(sec:signcheck) "DIFFERS"는 손상 아님**: v03-v09 의 차이는 **전부 신규 `\bibitem`(levi1999·fly2020·cogswell2012·park2021·rsc2021/yang2023) 순수 추가뿐 — 기존 줄 삭제·수정 0**. v01/v02 가 "IDENTICAL"인 건 이 span 에 broadening bib 를 안 넣어서지 우월성 아님(오히려 인용 누락).
- **lco_hys 영역 "DIFFERS"도 손상 아님**: 비-weff 변경줄을 전수 정독한 결과 모두 (1) base 671줄 도핑보정 문장의 `(또는 유효 폭을 넓혀, eq:weff)` 절 삭제·dual-status/broadening 상호참조 대체, (2) `\subsection{폭 w_j …}` 헤딩에 "이중지위" 추가 + dual-status 본문 삽입 — **3대 mandate(w_eff제거·w이중지위) 자체**. 흑연/LCO 물리 collateral 0.
- ΔH_a^eff/use_dH_eff/eq:dHeff 기계장치 9종 전부 보존(v03 1243-1287 등 확인). w_eff 청소하며 dH_eff 오삭제한 빌드 없음.

---

## (b) w 이중지위 서술 (검토 렌즈 2)

| 빌드 | 단상 Ω<2RT=nRT/F 평형예측 | 두-상=현상학적 자유피팅폭 | 코드 use_w_eff=False 정합 | 비고 |
|------|:---:|:---:|:---:|------|
| v10-03 | 명시 | 명시(별도 §broadening-wj) | 정합(narrowing 식 제거로 자동 정합) | 절제·완전제거 |
| v10-04 | 명시 | 명시 | 정합 | size featured(R1 영역) |
| v10-05 | 명시(§wdual) | 명시 | `use_w_eff=False` 명문 정합(단 토글 잔존) | — |
| v10-06 | **명시**(Ω>4958 J/mol 수치 게이트로 staging 4전이 전부 two-phase 확정) | **명시**(폭 폴백=초기값 까닭까지) | 정합 | 가장 견고 |
| v10-07/08/09 | 명시(lean) | 명시(lean) | 정합 | 짧지만 보유 |
| v10-01/02 | 명시 | 명시 | **불완전** — narrowing 식·func_w_eff live 라 "코드 항상 nRT/F" 와 모순 잔존 | FAIL 연동 |

- v10-06 의 이중지위 서술(687-708)이 1급: "같은 식 eq:wbase, 다른 지위" 프레임 + Ω_j>2RT(≈4958 J/mol@298K) 수치로 흑연 4전이 전부 two-phase 임을 닫고, 폭 폴백 0.020/0.016/0.014/0.012 V 가 "신뢰값 아니라 초기값"인 까닭까지 연결. LCO 3전이에도 동일 적용(1119-1120).

---

## (c) best 초안 (w_eff 완전제거 + 보존)

**1순위 = v10-06** (보존 PASS + w_eff 완전제거 + 이중지위 1급):
- w_eff: 본문 live 0 / eq:weff·func_w_eff·use_w_eff·floor 전부 제거. 헤더 changelog만 inert.
- 보존: 전자엔트로피 byte-IDENTICAL, LCO staging IDENTICAL, 부호사슬 추가만, ΔH_a^eff 보존, node-map N4=`func_w,_width`(func_w_eff 없음)·N5+ ΔS_e<0 행 무손상.
- 이중지위: §width(687-708)·§broadening(1128-1187, (a)전이별·(b)apparent-U=U_j+η·(c)3대 금지: U_j/반경 역산X·forward-only ill-posed·다입자/PSD모델X) + keybox + TikZ. ※(b)/(c) 의 다입자·forward-only 는 R1 소관이나 R2 보존 관점서 base 물리와 충돌 없음 확인.

**보존-only 대체 = v10-03**(w_eff floor 1행만 cosmetic 잔존; 정리하면 동급) 또는 **v10-04**(본문 완전 0, size featured 는 R1 판단).

---

## (d) 결함표

| ID | 빌드 | 심각도 | 결함 | 근거(줄) |
|----|------|:---:|------|------|
| W1 | v10-01 | **HIGH** | narrowing 식 eq:weff·func_w_eff·w_eff_floor_frac·use_w_eff 전부 보존(경고문만 추가) → D2 "자취 0" FAIL | 705·707-710·202·1579·1584·1628 |
| W2 | v10-02 | **HIGH** | 동일(eq:weff 식·func_w_eff·notation·nodemap live) → FAIL | 710·712-716·202·1582·1587·1631 |
| W3 | v10-05 | MED | narrowing 식은 제거했으나 use_w_eff 토글 서술 6곳 legacy 로 잔존(자취 0 미달) | 731-732·1200·1639·1655·1660·214 |
| W4 | v10-03 | LOW | 입력표 `w_eff_floor_frac` 1행 식별자 노출("사용 안 됨" 명시) — 완전 제거면 행 삭제 권장 | 1573 |
| (보존) | 전체 9종 | — | 보존 결함 0. 전자엔트로피·LCO·부호사슬·ΔH_a^eff·그림 전수 무손상. 깨진 ref 0 | md5/diff 확인 |

> 정직 메모: (b)/(c) 의 broadening 물리 충실도(two-phase 수·다입자 모델 0·forward-only)는 R1 검토 영역. R2 는 ① w_eff 라이브 자취 ② w 이중지위 *유무* ③ base 대비 보존 byte-정합 3렌즈로 한정해 판정함. v10-06·07·08·09 헤더 주석 changelog 의 w_eff 문자열은 inert 로 PASS 처리(기준: 헤더 주석 무방).
