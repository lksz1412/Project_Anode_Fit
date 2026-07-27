# v1.0.25.1 — v1.0.25 검증·정직성 touch-up 리비전 (현행 최신)

> ★본 폴더 = v1.0.25(국소 수정판) + 마스터 산문 touch-up 4건(F1 regsol warnbox 정직화·F3 inline·
> M-w §5 포인터·L-bg §6 α=1 표지). 상세·검증·미완 = `results/V1025_1_TOUCHUP_NOTE.md`(권위 기록).
> 표시 버전 = v1.0.25.1(3 마스터), 코드 release = 1.0.25(byte-identical). 파일명·xr 키 불변(DG-2).
> 아래 본문은 **계보 승계분**(v1.0.24.1 원본 노트 + v1.0.25 S1~S6 추기)이며 provenance 참고용 보존이다.

---

# (계보 승계) v1.0.24.1 — v1.0.24 피드백 리비전(FB0~FB9) 동결 아카이브

## 지위
**동결(frozen) · 아카이브 전용.** 본 폴더는 v1.0.24 가 사용자 1차 정독 피드백(F-01~F-11) + 어조 강화(FB8) +
★ 마커 제거(FB9)를 거친 **리비전 완료 상태**의 충실한 스냅샷이다. 이후 개발은 본 폴더가 아니라 `v1.0.24/`
(또는 후속 버전)에서 진행한다. 파일 내용은 수정하지 않는다.

## 출처(provenance)
- 원본 = `Claude/docs/v1.0.24/` (동일 커밋 시점).
- 리비전 캠페인 = `Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md` (FB0~FB9 12-col 원장).
- phase 결과 = `Claude/results/PHASE_FB0_RESULT.md` ~ `PHASE_FB9_RESULT.md`.
- 버전 비교 감사 = `Claude/results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md`.

## 리비전 요약 (v1.0.24 원판 → 본 동결본)
- **FB0~FB7 (F-01~F-11)**: §1.1.4 배경 압축·확률/압력 P 충돌 해소·식1.21 f 명료화·제목 N-태그 제거·register
  평서화·조판(여백/줄간/microtype)·E.3·식2.39 overflow 해소·LCO 서두 재균형·일본어투 용어 정리·**코드=부록 전용**.
- **FB8 (어조 강화)**: 은유·의인·구어 중립화(되밟다→재현·되살리다→복원·비틀다→조정 등) + 정의어 rename
  (생존 지도→대응 지도·정직 공백→미결 공백).
- **FB9 (★ 마커 제거)**: 본문 ★/$\bigstar$ 57개 전량 제거(주석 34행 동결), 앵커 3쌍 phrase 헤더 정합 유지.
- **불변**: 물리 골격·식 번호·`\label` 정의·`\eqref`/`\ref`/`\cite` 키·코드(`.py`) 무변경.

## 구성 (파일명 = v1.0.24 유지 · 동결 사본 방식)
- 마스터 3본: `ch1_graphite_v1.0.24.tex` · `ch2_lco_v1.0.24.tex` · `ch3_si_v1.0.24.tex`
- `_sections/` (56 .tex) · `appendix_phase_separation.tex`
- 코드: `Anode_Fit_v1.0.24.py` (sha256 `f230f59b…`) · `CODE_GUIDE_v24.{md,html}` · `FITTING_GUIDE.md` ·
  `test_gates_v1024*.py`
- 빌드본 PDF 3종(검토·게이트 통과본): `ch1_graphite_v1.0.24.pdf`(97p) · `ch2_lco_v1.0.24.pdf`(30p) ·
  `ch3_si_v1.0.24.pdf`(21p)
- `plans/` · `results/` (버전-로컬 마감 문서: MERGE_READINESS·HANDOVER·INDEX_v24 + FB addenda)
- **제외**: 빌드 중간산물(`*.aux`/`*.log`/`*.out`/`*.toc`/`__pycache__`) — 재빌드로 복원 가능.

## 무결성 검증 (동결 시점)
- `diff -rq v1.0.24 v1.0.24.1` (빌드산물 제외) = **IDENTICAL**.
- 코드 `sha256 = f230f59b…` (FB 캠페인 baseline 과 동일 — 문건 한정 리비전).
- 빌드 GREEN: 0-error · undefined ref/cite 0 · 97/30/21 페이지.
- 본문 ★ = 0 · 주석 ★ = 34(동결).

## 파일명 규약 주의
동결 사본 방식(사용자 결정)이라 **내부 파일명은 v1.0.24 를 유지**한다. 개정 식별자는 **폴더명 `v1.0.24.1`** 이
담당한다(정식 rename 스냅샷 아님). 서브버전 번호 규약은 `v1.0.18.1`/`v1.0.18.2` 선례를 따른다.

---

# ★ v1.0.25 추기 (2026-07-26) — 위 본문은 **v1.0.24.1 동결 아카이브** 기준임

> **읽는 법**: 위 본문(§지위~§파일명 규약 주의)은 `docs/v1.0.24.1/` 동결 사본을 기술한 원문이며 **삭제하지 않고
> 이력으로 보존**한다. 본 폴더 `docs/v1.0.25/` 는 그 사본에서 갈라져 **코드가 실제로 변경된 작업 폴더**이므로,
> 위 본문의 일부 주장은 이 폴더에 대해 **스테일(stale)** 이다. 아래가 그 정정이다. 충돌 시 **본 절이 우선**.

## S1. 스테일 판정 — 위 본문 중 v1.0.25 에 적용되지 않는 주장

| 위 본문 위치 | 주장 | v1.0.25 판정 |
|---|---|---|
| §리비전 요약 "불변" | "코드(`.py`) **무변경**" | **스테일** — v1.0.25 에서 코드가 변경됨(S2) |
| §구성 | "코드: `Anode_Fit_v1.0.24.py` (sha256 `f230f59b…`)" | **스테일** — 본 폴더 코드는 다른 해시(S2) |
| §무결성 검증 | "`diff -rq v1.0.24 v1.0.24.1` = **IDENTICAL**" | **원본 두 폴더에 대해서는 여전히 참**(S4). 단 `v1.0.25` 는 이 등식에 포함되지 않는다 |
| §무결성 검증 | "코드 `sha256 = f230f59b…` (FB 캠페인 baseline 과 동일 — **문건 한정 리비전**)" | **스테일** — v1.0.25 는 문건 한정 리비전이 **아니다**(코드+문건) |
| §무결성 검증 | "빌드 GREEN: 0-error · 97/30/21 페이지" | **v1.0.25 에서는 미검증** — 본 PC 에 TeX 배포판이 없다(S5) |
| §구성 | "빌드본 PDF 3종" | **본 폴더에 부재**(`v1.0.25/*.pdf` 없음). PDF 는 `v1.0.24.1/` 에만 있다 |
| §파일명 규약 주의 | "내부 파일명은 v1.0.24 를 유지" | **유효 — v1.0.25 에서 재확인**(DG-2 사용자 확정, S3) |

## S2. 코드 변경 (v1.0.25) — 파일명 유지 · 내부 release 버전 = 1.0.25

- 파일: `Anode_Fit_v1.0.24.py` (**파일명 불변** — DG-2(a) 규약). 코드 헤더 line 3 = "release 버전 = **1.0.25**".
- **추가**: `func_dxi_eq`(@2 skew, 전이 dict `'alpha'` 부재=1.0=bit-exact) · `_causal_pad`(eq:lag 하한 −∞ 실현) ·
  `R_SI`/`F_SI`/`use_si_constants()`(C3 상수 SI opt-in) · `SI_MSMR7_LIT`(C7 Si 7-gallery opt-in).
- **삭제**: regsol 커널 3종(`_REGSOL_XG`·`_regsol_binodal_xa`·`_regsol_dqdv`) + `equilibrium()` 의 `'kernel'` 분기
  → 커널 계통 = **로지스틱 단일계**. **Ω 파라미터·Ω 소비 함수는 전량 존치**(`func_dU_hys`·`func_dH_a_eff`·
  §7 상성격 판정) — 삭제된 것은 dQ/dV **커널**뿐이다.
- **줄 수**(정정 포함 — 아래 두 수를 혼동하지 말 것):
  - `docs/v1.0.24` · `docs/v1.0.24.1` 아카이브 코드 = **1734 줄**(LF 기준) → `docs/v1.0.25` 코드 = **1917 줄**.
  - regsol 삭제 **그 단계**의 변화는 **1957 → 1917 줄**(−40)이다. 이 1957 은 v1.0.24 아카이브가 아니라
    **v1.0.25 개발 중 C1·C2·C3·C7 추가가 끝난 시점**의 줄 수다(계획서 C6 항 "−40줄" 과 일치).
- 골든 bit-exact 유지: `test_gates_v1024.py` **G1 golden max|d| = 0.0**.

## S3. 문건 변경 (v1.0.25) — 표시 버전 문자열만 (DG-2)

- 마스터 3본 `ch1_graphite_v1.0.24.tex`·`ch2_lco_v1.0.24.tex`·`ch3_si_v1.0.24.tex` 에서 **사람이 읽는 표시 버전만**
  1.0.24 → 1.0.25 로 교체: `\hypersetup{pdftitle=…}` · `\lhead{…}` · `\date{\normalsize 버전 …}` 각 1회.
  각 파일 상단 주석 블록에 v1.0.25 이력 2줄 추가(기존 주석 줄 보존).
- **불변(개명 금지)**: 파일명 · `\input{_sections/…}` 경로 · `\externaldocument{…}` 키 ·
  `_sections/common_preamble_v1024.tex`(그 헤더의 v1024 는 자기 출처 버전을 적은 이력 주석) ·
  파일명·식별자에 박힌 `_v1.0.24`/`v1024`/`v22` 토큰.
- 절 본문(`_sections/*.tex` 56종)·`appendix_phase_separation.tex` 의 내용 편집은 **별건**(계획서 P2·P3 소관).

## S4. 원본 아카이브 무변경 확인

- `docs/v1.0.24.1/` · `docs/v1.0.24/` = **무변경**. 코드 LF-sha256 앞 16자리 = **`f230f59bb10bcc49`**, **두 폴더 동일**.
- 두 폴더의 추적 파일 261개 전부 git 상태 clean(작업 트리 변경 0).
- 빌드산물 제외 `diff -rq v1.0.24 v1.0.24.1` 의 유일한 차이 = `ARCHIVE_NOTE.md`(v1.0.24.1 에만 존재).

## S5. 게이트·빌드 상태 (증빙 출처 구분)

- **마스터 세션 실행분(인용)**: `test_gates_v1024` 전건 PASS · `test_gates_v1024_reflect` **4/4** ·
  `test_gates_v1024_selfconsistent` **5/5** · `test_gates_v1025` **8/8** · 모듈 `__main__` overall OK: **True**.
- **본 추기 작성 서브세션이 직접 확인한 것**(재실행 아님 — 정의 대조): reflect 게이트 정의 4종(G-R1·G-R2·
  **G-R3 = "@3 regsol 커널 삭제 확인"**·G-R4) · selfconsistent 5종(G-E1~G-E5) · v1025 8종(G-α1~α4·G-창·G-극단·
  G-SI·G-si7) 이 각 파일에 실제로 정의되어 있음, 그리고 regsol 심볼이 v1.0.25 코드에서 **주석 2행 외 부재**임.
- **LaTeX 빌드는 v1.0.25 에서 수행되지 않았다**: 본 PC 에 TeX 배포판 부재(xelatex·pdflatex·latexmk·lualatex·tex
  전부 PATH 에 없음, `C:\texlive` 부재). 대신 **구조 검사**로 대체 확인:
  `results/tools_check_structure.py check .` → **STRUCTURE_CHECK: PASS**
  (ch1: label 265·dup 0·unresolved ref 0 / ch2: 82·0·0 / ch3: 44·0·0 / appendix: 30·0·0 · env pairing error 0 ·
  cite-undef 0 · bib-uncited 0). **PDF 페이지 수·0-error 빌드는 미검증** — 재빌드 가능한 환경에서 3-pass 확인 필요.

## S6. 데이터 기록 정정

v1.0.24 데이터·피팅 증빙(`Claude/results/comp_v24/`)의 정정은 원본 수정이 아니라 addendum 으로 처리했다:
**`results/V1025_DATA_ADDENDUM.md`**(A1 프로토콜 혼용 · A2 p-ocvhold 권고 · A3 독립셀 재현성 ·
A4 @3 철회+코드 삭제 · A5 C_bg 비상수 · A6 @1~@5 조합 실측표 · A7 gallery≠상). comp_v24 원본은 무수정 보존.

---

# ★ v1.0.25.2 추기 (2026-07-27) — 확정 구성 반영 + v1.0.26 carryover 1차

> 충돌 시 **본 절이 우선**. 상세 명세·잔여 = `Claude/results/HANDOVER_v1025_2_CARRYOVER.md`.

## U1. 확정 구성 (사용자 2026-07-27)

**skew-logistic 흑연 7 · 실리콘 7 · 블렌드 14 + 자유 배경**, `L_V` 동결(§18 식별 가드).
regsol 은 **이론 층에만** 유지하고 피팅 커널 계통은 **로지스틱 단일계**(v1.0.25 판정 유지).
α 는 신규 물리가 아니라 v1.0.25 가 도입해 둔 `eq:skewpeak` opt-in 의 **발효**다.

## U2. 코드 변경 — additive opt-in 1건 (파일명 불변, DG-2)

- **추가**: `GRAPHITE_MSMR7_LIT`(흑연 7-gallery 시드). `GRAPHITE_STAGING_MSMR6_LIT`·`SI_MSMR7_LIT` 와
  동일 지위. 블렌드 14 = 흑연 7 + Si 7 조합으로 성립.
- **기본 경로 무변경** → 골든 bit-exact 계약(G1) 보존. `'alpha'` 키 미부여(부재=1.0=대칭).
- **tier-C seed 3중 단서**: 단일 셀·비평형 pOCV / 산출 당시 자유 배경 부재로 배경이 한 전이의 Q 를
  겸함(N10 — 그 전이 Q 특히 신뢰 금지) / w=0.1 mV 급은 계측 분해 한계 아래.

## U3. 문건 변경 (신규 식 1 · 신규 절 4 — 전부 additive, 삭제 0)

| 파일 | 내용 |
|---|---|
| `ch3v22_sec02b_sifr.tex` | **★`eq:sifr-twophase` 신설** — Ω>2RT 두-상 정칙용액 dQ/dV 닫힌형(혼화갭 닫힌항 + 고용체 밀도⊛broadening 핵). 종전 §(v) 는 산문 명세뿐이었다. 면적 보존·단일상 연속접속·합성곱이 항등인 이유·격자합 3 함정·이론층 지위 명기. 그리고 :43 "모수 절약(AIC/BIC) 미확정" → 단일 셀 확정으로 조준 축소(N10 단서 병기) |
| `ch1_sec05b_gr2L.tex` | 해상도 사다리에 **7-gallery** 추가(N=7 최소·N=8 포화·근축퇴 쌍 증가·**커널 무관**) / **Ω≷2RT 판정자의 실측 대응**(Ω/RT 1.9–2.5 = marginal 두-상, 독립 앵커 2.5RT·3.4RT 정합, 두 명제 분리) / **최저 전위 평탄의 계측 분해 한계**(FWHM ≲ 1 mV = RT/F 의 1/25) |
| `ch1_sec18_inputs.tex` | 식별 가드에 **다섯째 손잡이 Ω** 추가(경계 포화 = 미식별) / "gallery+α 동시 자유화 지양" → **조건부**로 조준 정정(대가는 적합도가 아니라 점-식별성, L_V 동결은 불변) / **신규 warnbox**: 면적 보존 Δ_Q 를 적합도와 독립된 채택 전 진단으로, 실측 dQ/dV 미분 규약(전위 양자화 0-나눗셈 → 다중창 중앙값 + 평활 + 균일 재빈닝) |
| 마스터 3본 | 표시 버전 1.0.25.1 → **1.0.25.2**(pdftitle·lhead·date). 파일명·`\input` 경로·xr 키 **전부 불변** |

## U4. 검증 (본 리비전)

- `results/tools_check_structure.py check .` → **STRUCTURE_CHECK: PASS**(unresolved ref 0 · cite-undef 0)
- `eq:sifr-twophase` 정의 1회 · 참조 무결 · 기존 라벨 무변경
- **P3-8 게이트**: 편집한 본문 3종 코드토큰 **0**
- 코드 `ast.parse` OK
- ⚠️ **XeLaTeX 빌드 미수행** — 본 환경에 TeX 배포판 부재. **재빌드 3-pass 0-error 확인이 잔여**다.
- ⚠️ **피팅 재실행 미수행** — numpy 부재. `C_skew` 판 산출과 N10 수정 효과 확인이 잔여다.

## U5. 잔여 (다음 예산)

A-3 수치 함정의 부록 정식 등재 · D 함정 기록(Ch2 부록 A) · C-4 소재별 문헌 서지 확장(M4 해소) ·
N7(skew-regsol N=7 스윕) · N8(평형 데이터 재검) · N9(bootstrap CI). 전부 `HANDOVER_v1025_2_CARRYOVER.md`.
