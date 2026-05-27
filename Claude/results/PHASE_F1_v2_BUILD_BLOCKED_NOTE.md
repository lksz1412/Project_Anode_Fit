# Phase F1_v2 — LaTeX 빌드 환경 + 첫 시도 (BLOCKED)

**Date**: 2026-05-28
**Cumulative steps**: 1001 ~ 1040
**Phase ID**: `BLOCKED_BUILD_v2`
**Blocker**: 로컬 환경에 LaTeX engine 부재.

## §1. Blocker

본 PC (Project_Anode_Fit Claude 측 작업 환경) 에는 LaTeX 빌드 도구가 설치되어
있지 않음:

```
PowerShell> $cmds = @('xelatex','pdflatex','lualatex','tlmgr','latexmk')
xelatex   -> NOT FOUND
pdflatex  -> NOT FOUND
lualatex  -> NOT FOUND
tlmgr     -> NOT FOUND
latexmk   -> NOT FOUND
```

`Claude/docs/graphite_ica_chapter1.tex` 는 `kotex` 한글 패키지 + `amsmath` +
`mdframed` 등을 사용하므로 **xelatex + kotex** 환경에서 빌드 권장.

## §2. 사용자 빌드 가이드 (사용자 PC 또는 빌드 가능 환경에서)

### Option A: TeX Live (권장)

```powershell
# 1. TeX Live full 설치 (https://tug.org/texlive/) 후
cd D:\Projects\Project_Anode_Fit\Claude\docs
xelatex graphite_ica_chapter1.tex
xelatex graphite_ica_chapter1.tex   # \ref / table of contents 갱신
```

### Option B: MiKTeX

```powershell
# 1. MiKTeX 설치 (https://miktex.org/) + on-the-fly package install ON
cd D:\Projects\Project_Anode_Fit\Claude\docs
xelatex graphite_ica_chapter1.tex
xelatex graphite_ica_chapter1.tex
```

### Option C: Overleaf (online)

1. https://overleaf.com 에 새 프로젝트 업로드
2. `graphite_ica_chapter1.tex` 업로드
3. 컴파일러: `XeLaTeX` 선택
4. 컴파일 → PDF 다운로드

## §3. 예상 빌드 결과

성공 시: `graphite_ica_chapter1.pdf` 생성 (대략 35-45 페이지 추정, 1686 lines
+ 16 longtables + 14 boxed eqns + 8 references)

## §4. F1_v2 Status

**BLOCKED** — 사용자 빌드 후 PDF 검수 (F3_v2) 진입 가능.

빌드 시 에러 발생할 경우:
- `kotex` 미설치 → TeX Live full 설치 또는 MiKTeX 의 패키지 자동 설치
- 인코딩 에러 → UTF-8 로 저장 확인 (이미 UTF-8)
- `mdframed` 미설치 → `\usepackage{mdframed}` 자동 설치 OK
- 표 폭 overflow → `longtable` 의 `p{0.X\textwidth}` 비율 조정

## §5. Next

Phase F2_v2 (빌드 에러 정정) — 빌드 시도 후 실제 에러 발생 시 진입. 현재 BLOCKED.
