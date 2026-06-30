# R3 검수 결과 — 인용·빌드·문체·orphan (2026-06-30)

> 검수 sub R3 담당. 검토 의견만, 파일 수정 없음.
> Ground truth: `ORIGIN_VERDICT.md` DOI 목록 · `base_v9.tex` 기존 인용 8건.

---

## (a) 9종 인용·빌드·문체 교차 표

| 초안 | broadening 절 위치 | levi1999 DOI | fly2020 DOI/권호 | cogswell2012 DOI | rsc2021 존재 | yang2023 존재 | park2021 DOI | v9 기존 인용 보존 | 빌드 (PDF) | 빌드 로그 | Overfull >20pt | 문체 |
|------|-------------------|--------------|-----------------|-----------------|-----------|-----------|--------------|--------------------|-----------|----------|--------------|------|
| v10-01 | `\section` (독립 절, ★) | 텍스트 내 DOI — 정확 | 텍스트 내 DOI — 정확 | 텍스트 내 언급, DOI 없는 산문 | 산문 언급(DOI만) | 텍스트 인용 존재 | 산문 내 DOI 언급 | O (8건) | O | O | 22.6pt (공통) | 완결 문장 ✓ |
| v10-02 | `\section` (독립 절, ★) | 텍스트 내 DOI — 정확 | 텍스트 내 DOI — 정확 | 텍스트 내 DOI 없는 언급 | 산문 언급 | 산문 내 DOI 존재 | 산문 내 DOI | O (8건) | O | O | 22.6pt | 완결 문장 ✓ |
| v10-03 | `\section` (독립 절, ★) | `\bibitem{levi1999}` 정확 DOI | ★vol.28 오류 (올바른 값=29) | `\bibitem{cogswell2012}` nn204177u 정확 | X (bibitem 없음) | X | park2021 저자 "S. Park, T. Kim, S. M. Oh" — 미확인 | O (8건) | O | O | 22.6pt | 완결 문장 ✓ |
| v10-04 | `\section` (독립 절, ★) | `\bibitem{levi1999}` 정확 DOI | ★저자 "M. Schaltz"(올바른 값=E. Schaltz) | nn204177u 정확 | bibitem 존재, 저자명 미확인 DOI 식별 | O (yang2023 bibitem) | DOI 정확 | O (8건) | O | O | 22.6pt | 완결 문장 ✓ |
| v10-05 | `\section` (독립 절, ★) | `\bibitem{levi1999}` 정확 DOI | ★vol.27 오류 (올바른 값=29) | nn204177u 정확 | 인용 없음(rsc2021 bibitem 없음) | X | park2021 저자 "J. Park et al." — 제목 fabrication 가능성 | O (8건) | O | **로그 없음 — 빌드 검증 불가** | 미검증 | 완결 문장 ✓ |
| v10-06 | `\section` (독립 절, ★) | `\bibitem{leviaurbach1999}` key 변경 (levi1999→leviaurbach1999) | ★저자 "R. Schaltz"(올바른 값=E. Schaltz) | nn204177u 정확 | bibitem 존재, 저자 미확인 DOI 식별 | X | park2021 저자 "S. Park et al." — 제목 fabrication | O (8건) | O | O | 22.6pt | 완결 문장 ✓ |
| v10-07 | `\subsection` (기존 절 하위) | `\bibitem{levi1999}` 정확 DOI | E. Schaltz 정확 | nn204177u 정확 | bibitem 존재(DOI-only, 설명 최소) | X | park2021 저자 "J. H. Park, H. Yoon, Y. Cho, C.-Y. Yoo" — 완전 서지 | O (8건) | O | O | 22.6pt | 완결 문장 ✓ |
| v10-08 | `\subsection` (기존 절 하위) | `\bibitem{levi1999}` 정확 DOI | E. Schaltz 정확 | nn204177u 정확 | X (bibitem 없음, cite 없음) | X | park2021 저자 "M. Park et al." 제목 fabrication 가능 | O (8건) | O | O | 22.6pt | 완결 문장 ✓ |
| v10-09 | `\subsection` (기존 절 하위) | `\bibitem{levi1999}` 저자/제목 없는 산문형 bibitem | E. Schaltz 정확 | ★★DOI 오류: nl300563u (Nano Lett.) — 올바른 값 nn204177u (ACS Nano) | X (bibitem 없음) | X | park2021 저자/제목 없는 산문형 bibitem | O (8건) | O | O | 22.6pt | 완결 문장 ✓ |

---

## (b) Fabrication·DOI 오류·orphan 결함 목록

### ★CRITICAL — DOI 오류 (fabrication급)

**[B-1] v10-09 cogswell2012 DOI 오류**
- 파일: `v10-09/v10-09.tex`, 행 1662
- 기재: `\emph{Nano Lett.} \textbf{12}, 2215 (2012). DOI: 10.1021/nl300563u`
- 올바른 값: `\emph{ACS Nano} \textbf{6}, 2215 (2012). DOI: 10.1021/nn204177u`
- 근거: ORIGIN_VERDICT §6 및 여타 8개 초안 일치값. `nl300563u` = Nano Letters 식별자, `nn204177u` = ACS Nano 식별자. 저널·DOI 모두 불일치.

### HIGH — 저자명 오류 (인지 fabrication)

**[B-2] v10-04 fly2020 저자 "M. Schaltz"**
- 파일: `v10-04/v10-04.tex`, 행 1771
- 기재: `A. Fly, M. Schaltz, D.-I. Stroe`
- 올바른 값: `A. Fly, E. Schaltz, D.-I. Stroe` (여타 8개 초안 일치)

**[B-3] v10-06 fly2020 저자 "R. Schaltz"**
- 파일: `v10-06/v10-06.tex`, 행 1760
- 기재: `A. Fly, R. Schaltz, and D.-I. Stroe`
- 올바른 값: E. Schaltz

### HIGH — 권호 오류

**[B-4] v10-03 fly2020 vol.28 오류**
- 파일: `v10-03/v10-03.tex`, 행 1691
- 기재: `\emph{J. Energy Storage} \textbf{28}, 101329 (2020)`
- 올바른 값: vol.29 (여타 7개 초안 일치)

**[B-5] v10-05 fly2020 vol.27 오류**
- 파일: `v10-05/v10-05.tex`, 행 1794
- 기재: `\emph{J. Energy Storage} \textbf{27}, 101329 (2020)`
- 올바른 값: vol.29

### MEDIUM — 누락 인용·서지 불완전

**[B-6] v10-03 rsc2021 bibitem 없음**
- broadening 절에서 4L-3L 연속 전이를 서술하나 `\bibitem{rsc2021}` 없음. `\cite{levi1999}` 단독으로 rsc2021 내용(plateau except for 4L-3L) 인용 필요 누락.

**[B-7] v10-05 rsc2021 불인용**
- broadening 절 내 연속 전이 출처로 rsc2021 미포함(levi1999만).

**[B-8] v10-07, v10-08, v10-09 yang2023 미인용**
- ORIGIN_VERDICT에서 "확정·강한 지지" 등급의 핵심 근거인 Yang 2023 (10.1038/s41467-023-40574-6)이 broadening 절에서 전혀 언급되지 않음.
- v10-07: rsc2021 있으나 yang2023 없음.
- v10-08, v10-09: rsc2021·yang2023 모두 없음.

**[B-9] v10-05 빌드 로그 없음**
- `v10-05/` 디렉터리에 `.log` 파일 부재. xelatex 0-error 여부 미검증.

**[B-10] v10-09·v10-08·v10-03 park2021 서지 불완전**
- v10-09: 저자/제목 없이 산문형 (`graphite GITT/OCP staging constants...`). 학술지 표준 bibitem 미충족.
- v10-08: "M. Park et al." — 제목이 제조된 설명문 형식. 실제 논문 제목 미확인.
- v10-03: "S. Park, T. Kim, S. M. Oh" — 제목 제조. 실제 저자·제목 불일치 가능.

### LOW — 문체·orphan

**[B-11] v10-09 levi1999 서지 산문형**
- `\bibitem{levi1999} M. D. Levi and D. Aurbach, graphite solid-solution/staging peak analysis, \emph{Electrochim. Acta} (1999).` — 제목이 산문 설명이지 실제 논문 제목이 아님. 다른 초안(v10-08: "Frumkin intercalation isotherm...")이 실제 제목에 더 가까움.

**[B-12] v10-07 rsc2021 bibitem "DOI-only entry from project research note" 문구**
- 출판 목적 최종본에는 실제 저자·제목으로 교체 필요(현재는 내부 노트 표현). 단, 저자 미확인 상태가 정직하게 기재된 점은 긍정적.

**[B-13] Overfull 22.6pt (모든 8개 초안 공통)**
- 신규 broadening 절이 아니라 기존 절(longtable 부근) 기인 공통 overfull. 신규 절 단독 결함 아님.

**[B-14] 도입/참조 orphan 없음 확인**
- `fig:broadening` — v10-04/05/06에 `\label{fig:broadening}` 및 `\ref{fig:broadening}` 모두 존재.
- broadening 절을 forward-reference하는 `\S\ref{sec:broadening}` — 각 초안에서 sec:width 등 앞 절에서 참조 존재, orphan 없음.
- TikZ 노드 내 텍스트: 영어 ASCII 확인 (한글 0).

---

## (c) Best 초안 선정

**v10-08**이 현재 기준으로 최선에 가장 가깝다.

근거:
- levi1999·fly2020(E. Schaltz, vol.29)·cogswell2012(nn204177u)·park2021 DOI 모두 정확.
- 빌드 로그 존재, PDF 존재, Fatal error 0.
- v9 기존 인용 8건 보존.
- broadening 절이 subsection으로 기존 평형 peak 절에 통합 — 구조적으로 절 도입/참조 체인이 자연스러움.
- 완결 문장 문체 유지.

단, v10-08의 잔여 결함:
- rsc2021·yang2023 미인용 [B-6처럼 HIGH].
- park2021 저자 "M. Park et al."의 제목 제조 가능성 [B-10, MEDIUM].

**인용 완성도 기준**으로는 **v10-07**이 rsc2021·park2021 완전 서지를 보유하고 DOI도 정확하나, yang2023 미포함 및 fly2020 제목("Prediction of differential voltage curves..." — 실제 논문 제목 여부 미확인)이 잔여 문제.

**yang2023 포함 유일 초안**: v10-04 (단, fly2020 저자 M. Schaltz 오류 [B-2]).

→ **결론**: 단일 best는 없으나, **v10-07의 rsc2021·park2021 서지 + v10-08의 fly2020 저자 정확성 + v10-04의 yang2023**을 cherry-pick하면 인용 완성 초안이 된다.

---

*R3 검수 sub 작성. 파일 수정 없음. master 통합 판단용.*
