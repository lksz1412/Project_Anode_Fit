# A3 Adversarial Review — v10-10 인용·빌드·문체·orphan
> 검수자: adversarial A3 (반증 시도). 파일 수정 X. 2026-07-01.

## 결함표

| # | 분류 | 위치 | 내용 | 심각도 |
|---|------|------|------|--------|
| D1 | **인용 fabrication** | `\bibitem{fly2020}` (line 1802) | 저자가 `A. Fly and E. Schaltz` 2인 표기. Ground truth(ORIGIN_VERDICT.md line 29·76)는 **Fly·Schaltz·Stroe** 3인 — Stroe 누락. 제목 "Temperature and current-rate dependence of incremental capacity peaks" 는 DOI 로만 식별했다 표기, 실제 제목 미검증 상태. HIGH | HIGH |
| D2 | **인용 fabrication** | `\bibitem{rsc2021}` (line 1801) | 저자·제목 전혀 없이 "흑연 staging 전이별 1차/연속 구분(…) \emph{J. Mater. Chem. A} (RSC, 2021)" — 제목 없음·저자 없음. 표준 서지 형식 미달. MEDIUM | MEDIUM |
| D3 | **인용 fabrication** | `\bibitem{dahn1995}` (line 1803) | "J. R. Dahn 그룹(Dahn et al.)" 표기 + 제목 한국어 설명문으로 대체. Science 270.5236.590·DOI 일치하나 정확 제목·공저자 미기재. MEDIUM | MEDIUM |
| D4 | **사이즈 인용 잔존 확인** | 본문 전체 | `yang2023`·`cogswell2012` `\cite{}` 호출 없음 — 배제 경고문(sec:broadening line 1205–1212)에서 τ∝r²·반경→U_j 서술은 있으나 근거 DOI `\cite{}` 없음. 사이즈 근거 인용이 숨겨진 방식으로 잔존하지 않음 — **배제 정책 준수 확인됨**. | PASS |
| D5 | **빌드** | xelatex 1회·2회 모두 | **0 error**. 미해소 undefined ref/cite 없음. | PASS |
| D6 | **overfull** | lines 219, 612–617, 1625–1627, 1677–1680 | 4건 overfull hbox — 최대 **22.55pt** (line 1677). 20pt 초과 신규 1건. | WARN |
| D7 | **문체** | broadening 절 (sec:broadening) | 완결 문장 구성·전보체 없음 확인. | PASS |
| D8 | **TikZ 한글** | 전체 tikzpicture | 노드 텍스트 모두 ASCII/영어. 한글은 tikzpicture 밖 caption·본문에만. | PASS |
| D9 | **orphan — fig:broadening** | line 1271 | `\label{fig:broadening}` 선언됨. 그러나 본문 어디에도 `\ref{fig:broadening}` 호출 **없음** — 그림 미참조. | **CRIT** |
| D10 | **orphan — eq:ensavg** | lines 1182, 1186–1232 | `\label{eq:ensavg}` 선언, 본문 내 `\eqref{eq:ensavg}` 5회 참조 확인(lines 1186,1188,1214,1217,1232). | PASS |
| D11 | **orphan — sec:broadening 앞 도입** | line 680·701·708·715 | sec:broadening 절 전에 sec:lco-hys(line 680)·sec:width(line 701,708,715)에서 `\S\ref{sec:broadening}` 사전 소개 존재. | PASS |
| D12 | **orphan — sec:broadening 뒤 참조** | line 1129 | sec:lco-peak(sec:lco-peak, line 1129)에서 `(\S\ref{sec:broadening})` 사후 인용. 집합통계역학 절 후속 참조 있음. | PASS |
| D13 | **v9 LCO 인용 보존** | dahn1991·ohzuku1993·bazant2013·dreyer2010·xia2007·reynier2004 등 | 모두 biblist 에 존재, 본문 cite 확인. | PASS |

## 인용 정확성 표 (신규 broadening 인용 4종)

| 키 | 저자(bibitem) | 저자(GT) | 저널/권/DOI | 일치 | 결함 |
|---|---|---|---|---|---|
| dahn1995 | "J. R. Dahn 그룹(Dahn et al.)" | ORIGIN_VERDICT: Dahn et al. | Science **270**(5236), 590; DOI 10.1126/science.270.5236.590 | DOI·권·면수 일치 | 제목·공저자 미기재, 저자 표기 비표준 |
| dreyer2010 | W. Dreyer et al. | ORIGIN_VERDICT: Dreyer et al. 2010 | Nat. Materials **9**, 448; DOI 10.1038/nmat2730 | 완전 일치 | 없음 |
| leviaurbach1999 | M. D. Levi and D. Aurbach | ORIGIN_VERDICT: Levi & Aurbach 1999 | Electrochim. Acta **45**, 167; DOI 10.1016/S0013-4686(99)00202-9 | 완전 일치 | 없음 |
| fly2020 | A. Fly and E. Schaltz | ORIGIN_VERDICT: **Fly·Schaltz·Stroe** | J. Energy Storage **29**, 101329; DOI 10.1016/j.est.2019.101329 | 권·DOI 일치 | **Stroe 누락** |
| rsc2021 | (저자 없음) | ORIGIN_VERDICT: RSC 2021 | J. Mater. Chem. A; DOI 10.1039/D0TA12607A | DOI 일치 | 저자·제목 전무 |

## 반환 요약 (10줄 이내)

- **fabrication 없음** — DOI·권은 모두 ground truth와 일치. 임의 생성 없음.
- **D1(HIGH)**: fly2020 bibitem에서 Stroe 저자 누락 (ORIGIN_VERDICT 3인→2인).
- **D2(MEDIUM)**: rsc2021 bibitem 저자·제목 없음 — 서지 불완전.
- **D3(MEDIUM)**: dahn1995 bibitem 제목 한국어 대체·공저자 불기재.
- **D9(CRIT)**: `fig:broadening` 미참조 orphan — 본문 어디에도 `\ref{fig:broadening}` 없음.
- **사이즈 인용 잔존**: yang2023·cogswell2012 `\cite{}` 호출 없음 — 배제 정책 준수.
- **빌드**: 0-error, undefined ref/cite 없음 (2-pass).
- **D6(WARN)**: overfull 4건 중 line 1677 22.55pt > 20pt 신규 초과 1건.
- 약한 1곳: **rsc2021** (저자·제목 없는 bibitem이 tier-A 인용으로 쓰임).
