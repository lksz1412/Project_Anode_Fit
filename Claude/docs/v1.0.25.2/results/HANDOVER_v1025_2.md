# HANDOVER v1.0.25.2 — 마감 인계 (버전-로컬 권위 문서)

> 작성 2026-07-27 · 대상 = `Claude/docs/v1.0.25.2/` (현행 최신)
> 상세 변경 이력 = 같은 폴더 `ARCHIVE_NOTE.md` **U1~U10**(충돌 시 ARCHIVE_NOTE 가 우선).
> 미반영 잔여 명세 = `Claude/results/HANDOVER_v1025_2_CARRYOVER.md`.

---

## 1. 이 버전이 무엇인가

v1.0.25.1 을 기준으로, **v1.0.26 A/B 조사(regsol 재검증)의 산출물 중 채택 가능한 것을 반영**하고
**확정 피팅 구성을 문건·코드에 실제로 세운** 리비전이다.

### 사용자 확정 사항 (2026-07-27)

| # | 결정 |
|---|---|
| D1 | **이론 = 정칙용액(regsol)** 유지 · **피팅 = 로지스틱 계열** — 두 층을 분리해 선언한다 |
| D2 | 확정 구성 = **skew-logistic 흑연 7 · 실리콘 7 · 블렌드 14 + 자유 배경**, `L_V` 동결 |
| D3 | 그 구성을 **기본값**으로 삼고 **4-전이를 opt-in** 으로 내린다 |
| D4 | 기준 폴더는 v1.0.25 계열 유지(v1.0.26 은 문건 판이 아니라 실측 결과 폴더) |

---

## 2. 폴더 지위 (정위치)

| 경로 | 지위 |
|---|---|
| **`Claude/docs/v1.0.25.2/`** | **현행 최신 작업본.** 표시 버전 v1.0.25.2 · 코드 release 1.0.25.2 |
| `Claude/docs/v1.0.25.1/` | **동결 아카이브** — 빌드 커밋 `bada485` 상태, 차이 0 검증. **PDF 3종은 여기에만** |
| `Claude/docs/v1.0.26A-regsol/` · `v1.0.26B-gallery/` | 실측 결과 폴더(문건 판 아님). 판정 근거로만 |
| `Claude/results/comp_v26_data/` | 적합 스크립트·원 산출물·리포트 원본 |

내부 파일명은 규약(DG-2)대로 `_v1.0.24` 토큰 유지 — **개정 식별자는 폴더명**이 담당한다.

---

## 3. 코드 상태

### 기본 진입 경로 (v1.0.25.2 에서 역전됨)

```
DEFAULT_GRAPHITE_TRANSITIONS = GRAPHITE_MSMR7_LIT      # 흑연 7 전이 skew (alpha 보유)
DEFAULT_SI_TRANSITIONS       = SI_MSMR7_SKEW_LIT       # 실리콘 7 전이 skew
DEFAULT_CBG_GRAPHITE = 0.550   ·   DEFAULT_CBG_SI = 0.051   # 짝 배경
```

- **블렌드 14 = 흑연 7 + 실리콘 7** 이 기본으로 성립한다.
- `use_legacy_4transition(True)` → v1.0.25 거동(흑연 4 전이 대칭 · Si 케이스셋) 복귀.
  `False` → 확정 구성 복귀(기본 상태).
- **명시 인자(`graphite_transitions=` / `si_transitions=`)는 스위치와 무관하게 항상 우선**한다.
- **골든 bit-exact 계약(G1)은 무변경.** 그 계약이 4 전이 기준이므로 `test_gates_v1024.py` 로더가
  로드 직후 레거시를 복원한다 — 바뀐 것은 기본 진입 경로뿐이다.

### 시드의 tier (반드시 함께 읽을 것)

두 7-전이 셋은 **tier-C seed** 이며 피팅 override 전제다:
① 단일 셀 · 비평형 pOCV(완화 없음) 위에서 얻었다.
② **α 가 탐색 상한에 포화**했다(흑연 7 중 5, Si 7 중 1) — 상한 위 어느 값이어도 거의 같은 곡선이므로
**α 는 식별된 값이 아니다.** α 가 하는 일은 계측 분해 한계 아래의 급준 평탄을 세우는 것이다.
③ 폭 0.1 mV 급은 계측 분해 한계 아래다.
④ **배경을 반드시 함께 쓸 것** — 전이만 옮기고 배경을 빠뜨리면 벨리역이 통째로 어긋난다.

---

## 4. 문건 변경 요지

| 위치 | 내용 |
|---|---|
| `ch3v22_sec02b_sifr.tex` | **★`eq:sifr-twophase` 신설** — Ω>2RT 두-상 정칙용액 dQ/dV 닫힌형(혼화갭 닫힌항 + 고용체 밀도⊛broadening 핵). 종전에는 산문 명세뿐이었다. 연속/불연속 구분 각주 포함. 모수 절약 "미확정" → 단일 셀 확정으로 축소 |
| `ch1_sec05b_gr2L.tex` | 해상도 사다리 **기준선을 7-gallery skew 로 이동**(4-전이는 선택) · Ω≷2RT 판정자의 **실측 대응**(Ω/RT 1.9–2.6 = marginal 두-상) · 최저 전위 평탄의 **계측 분해 한계** |
| `ch1_sec18_inputs.tex` | 식별 가드에 **다섯째 손잡이 Ω**(경계 포화 = 미식별) · gallery+α 동시 자유화를 **조건부**로 정정 · **면적 보존 진단 Δ_Q** 신설 · keybox 1단계를 기준선 이동에 맞춤 |
| `ch3v22_sec05_code.tex` | `ssec:code-twophase` — 두-상 종의 **수치 평가 요구명세**(본문에서 이관) |
| `ch1_appB_codemap.tex` | `ssec:code-dqdv-numeric` — 실측 dQ/dV **생성 규약**(본문에서 이관) |
| 마스터 3본 | 표시 버전 → v1.0.25.2 |

**본문/부록 경계(P3-8)**: 수치 구현 절차는 전부 코드 절·부록으로 이관했고, 본문에는 물리식과 그 전제만 남겼다.
검증 = 본문 전 `.tex` 에서 구현 어휘 **0 건** · 코드 토큰 **0 건**.

**상 수는 불변.** 바뀐 것은 곡선 표현의 기본 해상도이며, XRD 상 수(흑연 staging 4)와 `tab:staging` 의
4-전이는 **물리 기준으로 그대로 유효**하다 — 두 축이 갈린 것이지 대체가 아니다.

---

## 5. 검증 상태

| 항목 | 결과 |
|---|---|
| `test_gates_v1024` | R6-G1 · R6-G2 · R6-G3 · coverage **PASS** |
| `test_gates_v1025` | **9/9 PASS** |
| `test_gates_v1024_reflect` | **4/4 PASS** |
| `test_gates_v1024_selfconsistent` | **5/5 PASS** |
| 경로 전환 | 기본 = 7 전이(α 보유) · 레거시 = 4 전이 · 복귀 시 곡선 **bit-exact 재현** · NaN/Inf **0** |
| `tools_check_structure.py` | **STRUCTURE_CHECK: PASS**(unresolved ref 0 · cite-undef 0) |
| `eq:sifr-twophase` 수치 검산 | 면적 = Q (Ω/RT 0–8 × α 1,4,8 전 조합) · Ω→2RT 연속 · Ω<2RT 에서 갭 항 0 — **3/3 확인** |
| 피팅 3판 실행 | 확정 구성 C 가 세 소재 전부 우세(ΔBIC 흑연 −1089.4 · Si −474.2 · 블렌드 −517.7) |
| **XeLaTeX 3-pass** | ❌ **미수행** — 본 환경에 TeX 배포판 부재 |

---

## 6. ★남은 단 하나 — PDF 빌드

```
xelatex ch1_graphite_v1.0.24.tex   (×3)
xelatex ch2_lco_v1.0.24.tex        (×3)
xelatex ch3_si_v1.0.24.tex         (×3)
```

0-error · undefined ref/cite 0 확인. **신규 요소가 위험 지점**이다:
`eq:sifr-twophase`(식 1) · 각주 1 · `\subsection` 2 · `enumerate` 3.
빌드 통과 후 PDF 3종을 본 폴더에 커밋하면 v1.0.25.2 가 마감된다.

---

## 7. 결과 리포트 (이미지 포함)

`results/KERNEL_COMPARISON_REPORT_v1025_2.html` — 자체완결 HTML(적합 곡선 9종 임베드).
A 정칙용액 / B 로지스틱 / C skew-로지스틱 × 흑연·실리콘·블렌드, BIC 판정과 단서 3건 포함.
원본 = `Claude/results/comp_v26_data/KERNEL_COMPARISON_REPORT.html`.

---

## 8. 잔여 과제 (차단 아님)

| # | 항목 |
|---|---|
| A-3′ | 두-상 종 수치 명세를 부록 정식 항목으로 승격(현재 코드 절에 요구명세 형식) |
| D | 함정 기록(Ch2 부록 A) — 양자화 미분 · 비대칭 오구현 · 정규화 오류 |
| C-4 | 소재별 문헌 서지 확장 → **M4**("흑연 물리 두-상 4 vs 2" 표기 불일치) 해소 |
| N7 | `skew-regsol` N=7 스윕(미실행) — regsol 계열 최량이 아직 미측정 |
| N8 | **평형 데이터(GITT / pOCV+hold) 재검** — 현 판정은 전부 비평형 pOCV 위 |
| N9 | 파라미터 불확실도(bootstrap CI) 미산출 — 현 시드는 신뢰값 아님 |
