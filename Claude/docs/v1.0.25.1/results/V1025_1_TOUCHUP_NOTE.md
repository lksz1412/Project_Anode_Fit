# V1.0.25.1 — v1.0.25 검증·정직성 touch-up 리비전 기록 (현행 최신)

> 작성 = 마스터(Opus 4.8), 2026-07-26. **성격 = v1.0.25(국소 수정판)의 독립 검증 후 문건 산문
> touch-up 리비전.** 선례 v1.0.24→v1.0.24.1(동결 사본 + 리비전 식별 = 폴더명) 규약 승계.
> **원저작 보호**: v1.0.25(저치 Fable5/Opus5/Opus4.8 산출)의 폴더·보고서·커밋은 무수정 보존
> (main 에 cherry-pick 으로 원 메시지·저작 유지). 본 리비전은 별도 폴더 `v1.0.25.1/` 로 둔다.

## ① 배경 — 이 PC 로 v1.0.25 를 가져와 독립 검증

이 PC 는 v1.0.19(2챕터) 시점에서 정체돼 있었고, origin 은 v1.0.24.1(흑연/LCO/Si 3챕터)까지,
브랜치 `v1.0.25-surgical` 은 그 위 2커밋(feat: @2 skew opt-in·인과 pad·SI 상수 opt-in·regsol 삭제·
Si7 opt-in·FWHM 정정 / build: XeLaTeX 3장 통과)까지 진행돼 있었다. 사용자 지시로 Claude 작업만
현행화(로컬 `main` = v1.0.24.1 동기화)한 뒤, **v1.0.25 를 검증하고 반영 여부를 판정**했다.

## ② 마스터 독립 검증 결과 (반영 근거)

| 검증 | 방법 | 결과 |
|---|---|---|
| 전 게이트 | 4종 스위트 **직접 재실행** | ✅ v1024(G1~R6)·reflect 4/4·selfconsistent 5/5·v1025 **9/9**(G-금지 포함) |
| 회귀 안전 | 골든 bit-exact | ✅ module/golden max\|d\| = **0.0** (기본 경로 무변경 = 회귀 위험 0) |
| skew 물리 | 손 검산 | ✅ 정점이동 $\sigma_d w\ln\alpha$(α=2→+17.8 mV)·높이 $(Q/w)[\alpha/(\alpha+1)]^{\alpha+1}$·면적 α무관 |
| FWHM 정정 | 손 검산 + 수치 | ✅ 독립 유도 **(16/3)(RT/F)λ^{3/2}** 정확·수치 확인(λ=0.5:27.5%). v1.0.24 "폭=λ 연속화" 오류 정정 타당 |
| 코드 델타 289줄 | 전문 정독 | ✅ 매 변경 `if α==1: bit-exact` 분기·가드·regsol 삭제 클린·**Ω 물리 전량 보존** |
| 문건 산문 | 적대검수 2세션(Agent) | ✅ 정확성 오류 0. skew/FWHM 수식·수치 삼중(마스터+수치+에이전트) 확인. 발견 = 정직성·G-follow 산문 갭 |

**판정 = 반영(정확성 완결·저위험) + 문건 산문 touch-up 4건.**

## ③ 본 리비전이 반영한 touch-up 4건 (전부 산문 additive · 식·라벨·boxed 불변)

| ID | 파일 | 심각도 | 내용 |
|---|---|---|---|
| **F1** | `_sections/ch3v22_sec02b_sifr.tex`(regsol 삭제 warnbox) | HIGH | 삭제 근거를 **n=1·기준불일치·미검증**임에도 확정처럼 서술하던 것을 완화: "더 적은 가정으로"(방향 오류 — gallery 는 모수 더 많음) → **"별도 커널 계열 도입 없이 기존 로지스틱 자유도만으로"** + 단일 셀·AIC/BIC 미확정 유보 1문(재현 위임 M6) |
| **F3** | 동 파일(eq:sifr-blend box 직후) | LOW | 긍정형 boxed 의 Frumkin-Si 항에 **"해석적 기록·채택 경로는 로지스틱 단일계" inline 표식** 추가(도입 warnbox 국소성 보강) |
| **M-w** | `_sections/ch1_sec05_width.tex`(§5 폭 이중지위) | MED | "유효 폭" 서술에 **"중심 높이 척도이지 반높이 폭 아님 — FWHM 은 λ^{3/2}, §5b" 포인터** 삽입(§5b 정정 취지가 앞 문단서 오독되지 않게) |
| **L-bg** | `_sections/ch1_sec06_eqpeak.tex`(§6 verifybox iii) | LOW-MED | 감수율 항등 유도 서식이 이상격자($\Omega{=}0$)뿐 아니라 **대칭 종($\alpha{=}1$) 한정**임을 box 내부에 명시(skew 는 형상 파라미터로 격하) |

(F2 = supersede 데이터의 리포 미보존 = 재현성 후속 과제, 문건은 이미 "미측정" tier 표기 → 산문 수정 불필요. 별도 후속 N6~N9.)

## ④ 검증 (본 리비전 후)

- 구조 검사 `tools_check_structure.py check` → **STRUCTURE_CHECK: PASS**(전 장 미해소 ref 0·env 0·dup 0·라벨 불변)
- 엄격 검사 `tools_tex_strict_check.py` → **STRICT CHECK: ALL PASS**($ 패리티 불변·중괄호 depth 0·미확인 매크로 0·[E] 신규 라벨 **0**)
- 게이트 = 코드 **byte-identical**(v1.0.25 와 동일) → v1025 **9/9 PASS**·모듈 self-test `overall OK: True`
- CRLF/BOM = 편집 6파일 전건 순수 CRLF·BOM 0

## ⑤ 규약·불변

- **DG-2**: 파일명·`\input`·`\externaldocument` xr 키 불변. **표시 버전만** 3 마스터 pdftitle·lhead·`\date` = **v1.0.25.1**. 코드 release 문자열은 **1.0.25 유지**(코드 byte-identical — 선례 v1.0.24.1 도 코드 sha256 불변인 doc-only 리비전).
- 자산·`\boxed`(39)·`\label` 전건 보존(삭제 0). `eq:sifr-kernel`·`eq:sifr-blend` 식·라벨 불변.

## ⑥ 미완(비차단 후속 — 어느 경로든 별도)

| # | 항목 | 담당 |
|---|---|---|
| **빌드** | v1.0.25.1 XeLaTeX 3-pass 재빌드(이 PC TeX 부재 — 정적/엄격 검사로 ref·env·brace·macro 커버, 조판·페이지 미검증). touch-up 은 신규 매크로·라벨·환경 0 이라 통과 예상 | 회사/TeX 환경 |
| **N4** | 흑연 두-상 **4(Dahn 1991 초록) vs 2(§7 권위)** 표기 불일치 — v1.0.24 선행·챕터 내부 정합. Dahn 1991 **본문** 확인 | 사용자→마스터 |
| **N6~N9** | 신규 CSV 8종 리포 영구보존·재현 스크립트 등재·**regsol 철회 다중셀(n>1) 확인** | 마스터/차기 |

## ⑦ Chain
`V1025_1_TOUCHUP_NOTE.md`(본 문서, v1.0.25.1) ← `HANDOVER_v25.md`(v1.0.25 저치 인계) ← `HANDOVER_v24.md` ← … 
- v1.0.25 원본 검증·판정 상세 = `HANDOVER_v25.md`·`MERGE_READINESS_v25.md`·`V1025_CHANGE_LEDGER.md`(전부 무수정 보존).
