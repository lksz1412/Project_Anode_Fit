# A2 adversarial — w_eff 제거·기존 보존·부호 회의 (v10-10 vs base_v9)

> 검수 sub A2. 표적: w_eff 제거 완전성 / 전자엔트로피 byte 보존 / 기타 보존 / w 이중지위·부호.
> 방법: diff + sha256 + 빌드 LOG. **반증 시도 = 전부 실패 → 체리픽 PASS.**
> 대상: `v10-10/v10-10.tex` (1807줄) vs `v10-00_spine/base_v9.tex` (1644줄). 전체 변경 = +182 / −19 줄, 10 hunk.

## 1. w_eff 제거 완전성 — PASS

| 자취 | 라이브 결과 |
|---|---|
| `eq:weff` (label) | **ABSENT** (정의 0) |
| `\eqref{eq:weff}` | **NONE** (라이브 0) |
| `func_w_eff` | 라이브 0 (표·표기 항 제거됨) |
| `use_w_eff` | 라이브 0 (tab:inputs·notation·N4 행에서 제거) |
| `w_eff_floor_frac` | 라이브 0 (tab:inputs 행 삭제) |
| `weff`/`w^\eff` (전부) | 라이브 0 |

- `w_eff`/`func_w_eff`/`use_w_eff`/`w_eff_floor_frac`/`cogswell` **유일 잔존 = 헤더 changelog 주석(L7-11, %-블록, `\documentclass` L33 이전)** = inert·과제 허용범위.
- 제거된 19줄 = 전부 w_eff 계열: `eq:weff` 식블록 + "종 좁힘→유효폭" narrowing 서술(L52-60) + `\subsection{폭 — 이상극한과 옵션}` 제목 + notation/tab:inputs/N4-map 표 항목. **narrowing(델타 방향) 서술 제거 확인.** 표 정리 확인.
- 깨진 `\eqref` 0: 제거된 `eq:weff` 참조처 4곳(도핑보정·LCO staging폭·tab:inputs·N4-map)은 전부 `\S\ref{sec:broadening}` 또는 `\eqref{eq:wbase}`(이중지위) 또는 단순 삭제로 정합 치환. 빌드 LOG "Reference undefined" 0·"multiply defined" 0.
- 별개 보존 정상: `\Delta H_a^\eff`·`use_dH_eff`·`eq:dHeff` = **그대로 생존**(N7·tab:inputs·sign-map). w_eff 와 혼동 삭제 0.

## 2. 전자엔트로피 절 byte 보존 — PASS (byte-identical)

- `sec:lco-electronic` (L885-1068 base / L903-1086 v10), Fermi-Dirac→Sommerfeld·MIT 게이트·ΔS_e 삽입<0.
- **184줄 / 18504 byte 동일, SHA-256 `968fd30f…b67ad` 동일.** `diff` 무차이. **1바이트 변경도 없음.**

## 3. 기타 보존 — PASS

| 항목 | 결과 |
|---|---|
| 흑연 4전이 (sec:center N2, U_j) | **byte-identical** (diff 0) |
| LCO staging / ξ_eq 분포 (sec:hys) | 1줄만 변경(도핑보정 `\eqref{eq:weff}`→`sec:broadening` 포인터) 외 **identical** |
| eqpeak interior (sec:eqpeak) | 알려진 staging-폭 1 hunk(weff→이중지위) 외 pre-hunk **identical** |
| 부호 사슬 (sec:signcheck) | **byte-identical** (diff 0), `\checkmark` 9=9 |
| N7·N8·N9 (lag/tail/sum) | **byte-identical** (offset +157 후 diff 0) |
| 그림 | `figure` 10→11 (+1=fig:broadening 신규), caption 14→15. 기존 9 그림 불변 |
| 인용 | broadening/w 계열만 변경: +leviaurbach1999·rsc2021·fly2020·dahn1995·park2021 (dreyer2010 은 base 기존, 재사용), -cogswell2012(드롭). 기존 bibitem(swiderska2019·msmr2024·ml2024 등) 불변. **undefined cite 0** (cite∖bibitem set-diff = ∅) |

- broadening/w/인용 외 변경 = **0** 확인.

## 4. w 이중지위 + 부호 — PASS

- 단상(Ω≤2RT) = `w_j=n_jRT/F` **평형 예측**(검증가능) / 두-상(Ω>2RT) = **현상학적 자유 피팅 폭** 명시(sec:width 신규 ★문단 + sec:broadening). 같은 식 `eq:wbase`, 지위는 Ω_j 가 가름 — 코드 분기 아님 명시.
- two-phase = LiC₁₂·LiC₆ 2개로 통일, 코드 Ω 초기값(전부>2RT) = 거친 추정 note 동반. ✓
- 부호 정합: 전자항 `ΔS_{e,j}<0`(삽입) 보존(sec:lco-electronic byte-identical)·sign-map L1442 electronic 항 보존. apparent-U = U_j+η, 분포=η·ρ(U_j)(중심 불변) 명시. ΔS_e 삽입<0 1:1 유지.

## 5. 빌드

- `v10-10.log`: 0 error, 33 pages, PDF 출력. undefined ref/cite 0·multiply-defined 0. 경고 = 한글 italic font-shape 치환(cosmetic, base 와 동일 성격) 뿐.

---

## 결함표

| # | 심각도 | 내용 |
|---|---|---|
| — | CRIT | **0** |
| — | HIGH | **0** |
| n1 | NOTE | `dreyer2010` 가 신규 broadening 절에서 재인용되나 bibitem 은 base 기존(L1787, 히스테리시스용) — 정상(undefined 아님), 단 broadening 주석은 "+dreyer2010 추가"로 적어 신규처럼 보임(서지 신규 아님·재사용). 표기상 경미. |
| n2 | NOTE | w_eff 자취가 헤더 changelog 주석(L7-11)에 다수 — inert·허용범위이나 grep 시 노이즈. |

## 판정

- **w_eff 라이브 잔존 = 0** (헤더 주석만). 깨진 eqref = 0. narrowing 서술·표 정리 완료.
- **전자엔트로피 절 = byte-identical** (sha256 일치).
- **기존 보존**: 흑연 4전이·signcheck·N7-9 byte-identical, ξ_eq/staging/eqpeak 는 의도된 w→broadening 포인터 외 불변, 인용 정합, undefined 0.
- **부호 정합** 유지. **w 이중지위** 명시.
- **CRIT/HIGH = 0. 반증 실패 → 체리픽 v10-10 PASS.**
- **가장 약한 1곳**: n1 — broadening 절 주석의 "dreyer2010 추가" 표현(실제는 base 기존 bibitem 재사용). 빌드·참조는 정상이라 NOTE 급.
