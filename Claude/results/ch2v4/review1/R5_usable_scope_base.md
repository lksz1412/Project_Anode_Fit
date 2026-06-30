# R5 검수 — G-follow/G-usable + 범위(하프셀) + 종합 best-base
> 작성: R5 검수 sub | 렌즈: G-follow · G-usable · 범위 가드 · 종합 best-base
> Ground truth: v4-00_spine/AUTHOR_BRIEF.md · REVIEW_RISK_PATTERNS.md

---

## (a) 9종 G-usable · 범위 표

| 빌드 | config 부호 | w_eff 형 | G-follow 흐름 | G-usable 수준 | 범위 가드 | 비고 |
|------|------------|---------|--------------|--------------|---------|------|
| **v4-01** | ✅ 정답 `ξ/(1-ξ)` | ❌ WRONG `w/(1-Ω/2RT)` | ✅ 자연 서사 | ✅ 피팅 절차+검증표 | ✅ 명시 | w_eff 외엔 깔끔 |
| **v4-02** | ❌ CRITICAL `(1-ξ)/ξ` 역수 | ❌ WRONG `w/(1-Ω/2RT)` | ✅ 좋음 | ✅ 검증 데이터 | ✅ 명시 | config 부호 결함 — base 부적격 |
| **v4-03** | ✅ 정답 | ❌ WRONG `w/(1-Ω/2RT)` | ⚠️ Bernardi가 끝절에 등장(서사 후반 이동) | ✅ 5행 검증표+절차 | ✅ warnbox | g_mol(E_F) 몰단위 브리지 有 |
| **v4-04** | ❌ CRITICAL `(1-ξ)/ξ` (lines 605, 793) | ❌ WRONG `w/(1-Ω/2RT)` (line 624) | ⚠️ Part 구조 — 7파트, 도입부 Part 유발 산만 | ✅ 검증표 有 | ✅ 범위 명시 line 835 | 자체 sub 3개 띄움(금지 위반), base 부적격 |
| **v4-05** | ✅ 정답 `ξ/(1-ξ)` | ✅ **정답** `w(1-Ω/2RT)` (eq:weff line 528) | ✅ 도입→분배함수→config→vib+el→섞임(A/B/C/D)→극한→가역열 | ✅ 절차 keybox+검증표+완전식 명시 | ✅ warnbox + line 678 "전셀 합성은 본 장 범위 밖" | **유일 w_eff 정답 빌드** |
| **v4-06** | ✅ 정답 | ❌ WRONG `w/(1-Ω/2RT)` (line 577) | ✅ 분포 렌즈 framing 가장 일관됨(distbox) | ✅ 검증표+ΔS 문헌 비교표 | ✅ distbox 명시 | limits표 "Ω→2RT: w_eff→∞" = 역수식과 일관(오류 반영됨) |
| **v4-07** | ✅ 정답 `ξ/(1-ξ)` (lines 95, 243-244, 301-302, 405-407) | ❌ WRONG `w/(1-Ω/2RT)` (line 468-470) | ✅ 서→partition→config→vib+el→overlap→w_eff→hys→limits→Qrev | ✅ procedurebox 5-step + 완전식 eq:overlap_full | ✅ intro+hys절 경계 명시 | 텔레그래프 최소; 서사 명료 |
| **v4-08** | ✅ 정답 (`ξ/(1-ξ)` singletransitiondudt line 155) | ❌ WRONG `w/(1-Ω/2RT)` (line 311) | ✅ 서→partition→config→decomp→overlap→w_eff/hys/limits→산출 | ✅ 피팅 절차 4단계+완전식+warnbox | ✅ line 62-63 명시 | ⚠️ eq:decomp(line 197-203) LaTeX `+` 부호 누락 — 컴파일시 오류 가능 |
| **v4-09** | ✅ 정답 `ξ/(1-ξ)` (line 250-251) | ❌ WRONG `w/(1-Ω/2RT)` (line 438-440) | ✅ 서→Z→logistic→config→vib+el→mixing→w_eff/hys→Qrev → profile | ✅ workbox 5-step + numerical verification table | ✅ warnbox line 113-117 | ⚠️ eq:decomp(line 313-315) · eq:config_in_dudt(line 248-249) LaTeX `+` 누락 다수 |

---

## (b) ★종합 best-base 추천 + 차원별 graft 후보

### ★ best-base: v4-05

**근거:**
- **config 부호 CORRECT** — ξ/(1-ξ) 일관
- **w_eff 정답** — `w(1-Ω/2RT)` (eq:weff line 528), Ω→2RT: w_eff→0, 극한표 정합 (line 609)
- G-follow: 도입→분배함수→점유분포→config(S=-R∑p lnp 유도)→vib(BE)+el(FD/Sommerfeld)→겹침 가중(파생 A, 수치검증)→이중계산 B→w_eff(파생 C)→히스(파생 D)→극한→가역열 → 완전 서사
- G-usable: 하프셀 ∂U/∂T·가역열 산출 완전식 keybox(line 661-670), 피팅 경로 srcbox 명시(line 681-686), 수치 검증표(5행 + 175점 통계), 다온도 dQ/dV round-trip 절차 명시
- 범위: "전셀 합성은 본 장의 범위 밖"(line 678), warnbox, line별 명시
- 분량·충실도: 721줄, 파생 A/B/C/D 전부 섹션화, 극한 6코너 표, 맺음 요약 완비
- 문체: 완결 문장 위주, 전보체 최소

### 차원별 graft 후보

| 차원 | graft 출처 | 이유 |
|-----|-----------|------|
| 분포 렌즈 framing (distbox) | **v4-06** | 각 절 앞 "distribution-as-lens" distbox 환경 = G-follow 보조 |
| G-follow 서 도입부 명료성 | **v4-07** | 가장 짧고 명료한 "가역열은 분포 재배열의 열" 도입(§서, lines 78-116) |
| G-follow procedurebox | **v4-07** | 5-step procedurebox(lines 439-447) — v4-05 srcbox보다 읽기 명료 |
| 수치검증 내러티브(3가지 확인) | **v4-04** | Parts 5-6에서 "세 가지가 확인된다: (i)완전식=FD·(ii)계단부재·(iii)config자동생성" 서술 — v4-05 검증에 추가 가능 |
| 부호 규약 srcbox | **v4-01** | `ΔS=+nF·∂U/∂T` 부호 규약 srcbox 가장 정확(line 783-784 일관) |
| 검증표 상세 (5행 + 175점 통계) | **v4-05 본체** (이미 포함) | |
| ΔS 문헌 비교표 (Allart 대응) | **v4-06** | 4전이별 Ch1 ΔS_rxn ↔ 문헌 표 (lines 710-728) — G-usable 보완 |

---

## (c) 범위 위반 사항

### 직접 위반 (전셀 수치 혼입)
| 빌드 | 위반 위치 | 내용 |
|------|---------|-----|
| **v4-04** | line 816-818 (sec:estimate) | `potentiometric 표준 protocol·불확도(예: full-cell ∂U/∂T 0.3-0.5 mV/K @0-20% SOC)` — "full-cell" 라벨은 있으나 하프셀 본문 맥락에서 full-cell 수치를 단순 수치 예시로 쓴 것 (경계적 위반, 라벨 있음) |
| **v4-06** | line 693-694 (sec:synth) | `standardised2024` 인용으로 `full-cell ∂U/∂T 0.3-0.5 mV/K @0-20% SOC, std.dev ~µV/K` 수치 등장 — "보고 척도 차이" 주석 있으나 전셀 값 명시 라벨 없이 본문 수치로 표기됨 (경계적) |

### 전셀 합성 명시 위반 없음 (∂U_cell=∂U_cat−∂U_an 식 직접 등장 빌드)
- v4-07의 서(lines 84-88)에 `∂U_cell=∂U_cat−∂U_an` 이 "범위 밖" 문장 내 인용으로만 등장 → 위반 아님
- 나머지 빌드들은 전셀 합성식 사용 없음

### 요약
- **직접 전셀 수식 합성 위반**: 0건
- **전셀 수치 라벨 미비 (경계)**: v4-04(라벨 있으나 부족), v4-06(라벨 없이 수치 노출) 2건
- **AUTHOR_BRIEF 범위 가드 위반**: 없음

---

## 부록 — 위험 패턴 전수 집계

| 위험 | v4-01 | v4-02 | v4-03 | v4-04 | v4-05 | v4-06 | v4-07 | v4-08 | v4-09 |
|------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| 위험1 config 부호 | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 위험7 w_eff | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 위험3 exo/endo 기술 | ✅ | ✅ | ✅ | ❌(line 793-800 역매핑) | ✅ | ✅ | ✅ | ✅ | ✅ |
| 위험6 텔레그래프 | 낮음 | 낮음 | 중간 | 중간 | 낮음 | 낮음 | 낮음 | 낮음 | 낮음 |
| LaTeX `+` 누락 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌(eq:decomp) | ❌(eq:decomp, eq:config_in_dudt) |

> ✅ = 해당 위험 없음(정상) / ❌ = 위험 발견
