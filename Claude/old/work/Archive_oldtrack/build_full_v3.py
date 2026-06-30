# -*- coding: utf-8 -*-
"""Rebuild Ch1~5 _rebuilt.tex bodies into one standalone full document + refs file.
   Ch6 is dissolved (no separate chapter); its content is already absorbed into Ch1 Appendix B.

   Recipe (inherited & verified from build_full.py, Ch6 removed):
     - preamble union (packages, macros, theorem environments; dedup once)
     - each chapter body integrated at \\section level
       (internal \\subsection -> \\subsubsection FIRST, then \\section -> \\subsection)
     - single integrated bibliography (33 keys, Ch1-first union+dedupe) appended at end
     - title page + table of contents
   No modification to chapter source files. Bodies are byte-copied verbatim
   (no summary, no transcription). Label conflicts = 0 (Ch namespaced).

   Two outputs (regenerated):
     - graphite_ica_full_rebuilt.tex  (Ch1~5 merged + 33-key bib + integration note)
     - graphite_ica_refs_rebuilt.tex  (33-key bib only, standalone; existing preamble/title pattern)
"""
import re, io

BASE = r'd:/Projects/Project_Anode_Fit/Claude/docs'
OUT_FULL = f'{BASE}/graphite_ica_full_rebuilt.tex'
OUT_REFS = f'{BASE}/graphite_ica_refs_rebuilt.tex'

CHAPTERS = [1, 2, 3, 4, 5]

# Chapter section titles (per task spec; matched to real chapter content).
CHTITLE = {
 1: r'Chapter 1: 단일 인과 사슬 — 전하보존$\cdot$평형$\cdot$속도론$\cdot$spectrum$\cdot$closure$\cdot$실데이터 피팅(부록 B)',
 2: r'Chapter 2: 전지 가역 반응열 + 비가역 소산열 (Bernardi 에너지 balance)',
 3: r'Chapter 3: 반응속도론 일반화 (Level B) — forward/backward kinetics $\cdot$ detailed balance',
 4: r'Chapter 4: entropy-production 발열 정량화 ($\sum_j n_j^{\eff}I_j\eta_j$)',
 5: r'Chapter 5: 충방전 히스테리시스 (충전 부호 유도 $\cdot$ $\Delta V_\obs\ne\Delta V_\hys$)',
}

# Bib selection priority: Ch1 first, then 2,3,4,5. Each key appears once.
BIB_PRIORITY = [1, 2, 3, 4, 5]


def read_ch(ch):
    return open(f'{BASE}/graphite_ica_ch{ch}_rebuilt.tex', encoding='utf-8').read()


def extract_body(ch):
    """Return chapter body byte-verbatim: from after \\maketitle to just before
       \\begin{thebibliography}. Drops the embedded \\tableofcontents and the
       standalone \\newpage that follow the intro front matter, plus any in-body
       \\sloppy (set once globally). No content/text alteration."""
    txt = read_ch(ch)
    m_start = re.search(r'\\maketitle', txt)
    m_bib = re.search(r'\\begin\{thebibliography\}', txt)
    body = txt[m_start.end():m_bib.start()]
    body = re.sub(r'\\tableofcontents\s*\n', '', body)
    body = re.sub(r'^\\newpage\s*$\n', '', body, flags=re.MULTILINE)
    body = re.sub(r'^\\sloppy\s*$\n', '', body, flags=re.MULTILINE)
    return body.strip('\n')


def demote_headings(body):
    """Demote heading levels by one. Order matters: subsection -> subsubsection
       FIRST, then section -> subsection (so \\subsection does not get caught by
       the \\section rule). \\section* and \\subsection* are demoted identically."""
    body = body.replace(r'\subsection*{', r'\subsubsection*{')
    body = body.replace(r'\subsection{', r'\subsubsection{')
    body = body.replace(r'\section*{', r'\subsection*{')
    body = body.replace(r'\section{', r'\subsection{')
    body = body.replace(r'\addcontentsline{toc}{section}', r'\addcontentsline{toc}{subsection}')
    return body


def breakify_tables(body):
    """Insert zero-width \\brk break opportunities into AL/self-check table rows that
       lack them, so long DOI/ISBN/cite runs can wrap in narrow longtable columns.
       Applied ONLY to table rows (contain ' & ' and end with '\\\\'). Idempotent
       (skips runs already followed by \\brk). Zero-width discretionary: token text
       unchanged; full-file-only typographic break (chapter sources untouched)."""
    out_lines = []
    for line in body.split('\n'):
        s = line.rstrip('\n')
        is_row = (' & ' in s) and s.rstrip().endswith(r'\\')
        if is_row:
            s = re.sub(r'(10\.\d{3,5})/(?!\\brk)', r'\1/\\brk ', s)
            s = re.sub(r'(978-0)-(?!\\brk)', r'\1-\\brk ', s)
            s = re.sub(r'(471)-(?!\\brk)', r'\1-\\brk ', s)
            s = re.sub(r',\x20(?=[A-Za-z0-9])(?!\\brk)', r',\\brk ', s)
            s = re.sub(r';\x20(?=[0-9A-Za-z])(?!\\brk)', r';\\brk ', s)
            for key, brk in (
                ('thomasnewman2003', r'thomasnewman\brk 2003'),
                ('degrootmazur1962', r'degrootmazur\brk 1962'),
                ('evanspolanyi1938', r'evanspolanyi\brk 1938'),
                ('schnakenberg1976', r'schnakenberg\brk 1976'),
                ('funabiki1999ea', r'funabiki\brk 1999ea'),
                ('funabiki1999jes', r'funabiki\brk 1999jes'),
                ('bardfaulkner', r'bard\brk faulkner'),
                ('hindmarsh2005', r'hindmarsh\brk 2005'),
            ):
                s = s.replace(key, brk)
        out_lines.append(s)
    return '\n'.join(out_lines)


def fix_ch2_al_table(body: str) -> str:
    """Ch2 AL/self-check longtables use justified p{} (no raggedright), causing
       'GROUNDED' overfulls. Convert to raggedright (and AL table to footnotesize).
       Full-file-only typographic fix (Ch2 source untouched); cell text unchanged."""
    body = body.replace(
        r'\begin{longtable}{p{0.06\textwidth} p{0.40\textwidth} p{0.13\textwidth} p{0.16\textwidth} p{0.16\textwidth}}',
        r'\begin{longtable}{>{\raggedright\arraybackslash}p{0.05\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.355\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.155\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.195\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.13\textwidth}}')
    body = body.replace(
        r'\begin{longtable}{p{0.74\textwidth} p{0.16\textwidth}}',
        r'\begin{longtable}{>{\raggedright\arraybackslash}p{0.74\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.16\textwidth}}')
    body = body.replace(
        r'\begin{longtable}{p{0.17\textwidth} p{0.16\textwidth} p{0.59\textwidth}}',
        r'\begin{longtable}{>{\raggedright\arraybackslash}p{0.17\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.16\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.59\textwidth}}')
    body = body.replace(
        r'\begin{longtable}{p{0.27\textwidth} p{0.61\textwidth}}',
        r'\begin{longtable}{>{\raggedright\arraybackslash}p{0.27\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.61\textwidth}}')
    body = body.replace(
        r'\begin{longtable}{p{0.36\textwidth} p{0.52\textwidth}}',
        r'\begin{longtable}{>{\raggedright\arraybackslash}p{0.36\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.52\textwidth}}')
    body = body.replace(
        'FLAGGED.\n{\\small\n\\begin{longtable}{>{\\raggedright',
        'FLAGGED.\n{\\footnotesize\n\\setlength{\\tabcolsep}{3pt}\n\\begin{longtable}{>{\\raggedright')
    return body


# ----------------------------------------------------------------------------
# Bibliography union: parse each chapter's \begin..\end{thebibliography},
# split into per-key \bibitem blocks, take each key once with Ch1-first priority.
# ----------------------------------------------------------------------------
def parse_bibitems(ch):
    """Return ordered list of (key, full_bibitem_text) for a chapter, verbatim."""
    txt = read_ch(ch)
    m = re.search(r'\\begin\{thebibliography\}\{99\}(.*?)\\end\{thebibliography\}', txt, flags=re.S)
    block = m.group(1)
    # split on \bibitem (keep delimiter)
    parts = re.split(r'(?=\\bibitem\{)', block)
    items = []
    for p in parts:
        mk = re.match(r'\\bibitem\{([^}]+)\}', p.strip())
        if mk:
            items.append((mk.group(1), p.strip('\n')))
    return items


def build_bib_union():
    """Build 33-key union bibitem text, Ch1-first then 2->3->4->5. Returns
       (ordered_keys, bib_inner_text). Each key once, verbatim from its source."""
    chosen = {}      # key -> bibitem text
    order = []       # key insertion order (Ch1-first, then by chapter appearance)
    for ch in BIB_PRIORITY:
        for key, text in parse_bibitems(ch):
            if key not in chosen:
                chosen[key] = text
                order.append(key)
    inner = '\n'.join(chosen[k] for k in order)
    return order, inner


BIB_KEYS, BIB_INNER = build_bib_union()
assert len(BIB_KEYS) == 33, f'expected 33 keys, got {len(BIB_KEYS)}: {BIB_KEYS}'

THEBIB = '\\begin{thebibliography}{99}\n' + BIB_INNER + '\n\\end{thebibliography}'

# ----------------------------------------------------------------------------
# Shared preamble fragments (macro + theorem union — same as verified recipe).
# ----------------------------------------------------------------------------
THEOREM_UNION = r"""% --- theorem 환경 union (Ch1~5 preamble 합집합, 중복 정의 1회) ---
% (verifybox/linkbox 는 챕터별 caption 문구가 달랐으나, union 정의이므로 대표
%  caption 으로 통일 — 물리 내용·식 변경 0, box heading label 만 통일.)
\newtheorem*{groundingbox}{Grounding}
\newtheorem*{boundbox}{유효범위(Validity bound)}
\newtheorem*{flagbox}{FLAGGED (미확정)}
\newtheorem*{keybox}{Keystone}
\newtheorem*{linkbox}{전달식 (앞 장에서 상속)}
\newtheorem*{verifybox}{정합/유도 검증}
\newtheorem*{practicebox}{실무 팁 (본문 물리식 아님)}
\newtheorem*{loopbox}{도입 관찰로의 폐합}"""

MACRO_UNION = r"""% --- 매크로 union (Ch1~5 preamble 의 \newcommand 합집합, 중복 1회) ---
\newcommand{\dd}{\mathrm{d}}
\newcommand{\eff}{\mathrm{eff}}
\newcommand{\eq}{\mathrm{eq}}
\newcommand{\app}{\mathrm{app}}
\newcommand{\drive}{\mathrm{drive}}
\newcommand{\bg}{\mathrm{bg}}
\newcommand{\cell}{\mathrm{cell}}
\newcommand{\ext}{\mathrm{ext}}
\newcommand{\OCV}{\mathrm{OCV}}
\newcommand{\tot}{\mathrm{tot}}
\newcommand{\irr}{\mathrm{irr}}
\newcommand{\rev}{\mathrm{rev}}
\newcommand{\rxn}{\mathrm{rxn}}
\newcommand{\kin}{\mathrm{kin}}
\newcommand{\ohm}{\mathrm{ohm}}
\newcommand{\conc}{\mathrm{conc}}
\newcommand{\src}{\mathrm{src}}
\newcommand{\loss}{\mathrm{loss}}
\newcommand{\amb}{\mathrm{amb}}
\newcommand{\rlx}{\mathrm{relax}}
\newcommand{\cand}{\mathrm{cand}}
\newcommand{\conv}{\mathrm{conv}}
\newcommand{\prog}{\mathrm{prog}}
\newcommand{\coord}{\mathrm{coord}}
\newcommand{\ct}{\mathrm{ct}}
\newcommand{\sstat}{\mathrm{ss}}
\newcommand{\resid}{\mathrm{resid}}
\newcommand{\film}{\mathrm{film}}
\newcommand{\obs}{\mathrm{obs}}
\newcommand{\trans}{\mathrm{tr}}
\newcommand{\site}{\mathrm{site}}
\newcommand{\curr}{\mathrm{curr}}
\newcommand{\transp}{\mathrm{transport}}
\newcommand{\tr}{\mathrm{tr}}
\newcommand{\chem}{\mathrm{chem}}
\newcommand{\dis}{\mathrm{dis}}
\newcommand{\chg}{\mathrm{ch}}
\newcommand{\rst}{\mathrm{rest}}
\newcommand{\hys}{\mathrm{hys}}
\newcommand{\pol}{\mathrm{pol}}
\newcommand{\tar}{\mathrm{tar}}
\newcommand{\stt}{\mathrm{state}}
\newcommand{\cb}{\mathrm{cb}}
\newcommand{\dyn}{\mathrm{dyn}}
\newcommand{\tol}{\mathrm{tol}}
\newcommand{\noise}{\mathrm{noise}}
\newcommand{\AL}[1]{\textsf{[AL-#1]}}
\newcommand{\brk}{\discretionary{}{}{}}% 표/참고문헌 긴 DOI·ISBN 줄바꿈 허용(zero-width)"""

# ----------------------------------------------------------------------------
# FULL document preamble (Ch6 removed; 5-chapter framing).
# ----------------------------------------------------------------------------
FULL_PREAMBLE = r"""% ====================================================================
% graphite_ica_full_rebuilt.tex — Ch1~5 통합 full 문건 (RB Phase 7.x, standalone)
%   흑연 음극 ICA(dQ/dV) 이론서 RB-series Chapter 1~5 재구성본을 한 문서로 병합.
%   ★ Ch6 해체(2026-06-01): 별도 Chapter 6 없음 — 구 Ch6 (실데이터 피팅 워크플로)
%     내용은 Ch1 부록 B 에 이미 흡수됨. 따라서 본 통합본은 Ch1~5 만 편입한다.
%     · preamble union(documentclass·kotex·amsmath·\AL/\brk 매크로·theorem 환경
%       groundingbox/boundbox/flagbox/keybox/linkbox/verifybox/practicebox/loopbox
%       — 5개 챕터 preamble 합집합, 중복 정의 1회).
%     · 각 챕터 \documentclass/\begin{document}/\end{document}/개별 \tableofcontents 제거.
%     · 챕터 = \section{Chapter N ...}, 챕터 내부 \section→\subsection, \subsection→\subsubsection
%       (article 유지, \part/\chapter 미사용 — \section 레벨 정합).
%     · 통합 bibliography(refs 문건과 동일 33 키 union) 1회 포함.
%     · title page + table of contents.
%   ★ 원본 5개 챕터 _rebuilt.tex 는 수정 0 — body 는 byte-verbatim 복사(요약 0).
%     label 충돌 0(Ch namespaced; Ch1 의 sec:ch6_* 부록 라벨도 타 챕터와 미충돌),
%     cross-chapter 평문 상호참조는 현행 유지(수정 0).
%   ★ theorem 환경 caption 통일 주의: verifybox/linkbox 는 챕터별 caption 문구가
%     달랐으나 union 1회 정의로 대표 caption 을 쓴다(물리 내용·식 변경 0, heading
%     label 만 통일). 상세는 본 문서 말미 통합 노트 참조.
% Date: 2026-06-02  Author: Project_Anode_Fit (Claude 측, RB-series 통합 재생성)
% ====================================================================
\documentclass[11pt,a4paper]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{kotex}
\usepackage{amsmath,amssymb,mathtools,bm}
\usepackage{booktabs,longtable,array}
\usepackage{enumitem}
\usepackage{amsthm}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{setspace}
\setstretch{1.13}
\setlength{\parskip}{0.45em}\setlength{\parindent}{0pt}\setlength{\headheight}{14pt}
% 통합본 전역 줄바꿈 여유(문단 overfull/underfull 흡수; 내용 변경 0):
\setlength{\emergencystretch}{3em}\tolerance=1200\hbadness=4000
\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue, citecolor=blue,
  pdftitle={흑연 음극 ICA tail — Chapter 1~5 통합본 (RB 재구성본)}}
\pagestyle{fancy}\fancyhf{}
\lhead{흑연 음극 ICA(dQ/dV) tail 이론 — Ch.1~5 통합본 (RB)}\rhead{\thepage/\pageref{LastPage}}
\renewcommand{\headrulewidth}{0.4pt}

""" + THEOREM_UNION + "\n\n" + MACRO_UNION + r"""

\title{\textbf{리튬이온전지 흑연 음극 ICA($dQ/dV$) tail 이론 — Chapter 1$\sim$5 통합본}\\[0.5em]
\large 단일 인과 사슬 $\to$ 가역 반응열 $\to$ 반응속도론 $\to$ entropy production $\to$ 히스테리시스\\[0.3em]
\normalsize 하나의 관찰(저온$\cdot$고율 ICA 꼬리 겹침)에서 출발하는 단일 인과 사슬의 5-Chapter 전개\\
(RB 재구성본 통합 — 구 Ch6 는 Ch1 부록 B 로 흡수)}
\author{Project\_Anode\_Fit (RB 재구성본)}
\date{2026-06-02}

\begin{document}
\sloppy
\maketitle

\begin{abstract}
\noindent 본 문서는 흑연 음극 ICA($dQ/dV$) tail 이론 RB-series 재구성본 Chapter 1$\sim$5 를 한 문서로
통합한 것이다. \textbf{Chapter 1} 은 하나의 관찰(``저온$\cdot$고율에서 ICA peak 꼬리가 길어져 다음 peak 와
겹친다'')에서 출발해 열역학이 무대($V_n$, 평형 target $\xi_{\eq}$)를 깔고 동역학(진행률 완화 $+$
relaxation-length spectrum)이 꼬리의 주역임을 보이고, closure(Plan A/B)$\cdot$심플 근사식$\cdot$
\textbf{실데이터 피팅 워크플로(부록 B — 구 Chapter 6 흡수)}까지 본 장 안에서 닫는다. \textbf{Chapter 2}
는 그 위에서 전지 가역 반응열(평형 전위 온도계수 $=$ reaction entropy)과 비가역 소산열(과전압 flux$\times$force)을
Bernardi 에너지 balance 로 잇는다. \textbf{Chapter 3} 은 mobility $k_j$ 를 미시 forward/backward rate
$r_j^\pm$(Level B)로 확대하고 detailed balance 로 $n_j^{\eff}=RT/(Fw_j)$ 를 고정한다. \textbf{Chapter 4} 는
transition-level entropy production 이 거시 비가역 발열 일반형 $\sum_j n_j^{\eff}I_j\eta_j\ge0$ 으로 정확히
환원됨을 보인다. \textbf{Chapter 5} 는 충전 branch 부호 $s_{\phi,j}^b=-1$ 을 유도하고 히스테리시스를
target 의 이력 의존(metastable branch)으로 설명한다. 통합 참고문헌(33 키)과 통합 Assumption
Ledger(AL-1$\sim$69)는 별도 문건 \texttt{graphite\_ica\_refs\_rebuilt.tex} 에 정리되어 있으며, 본
통합본에도 동일 33 키 bibliography 가 1회 포함된다.
\end{abstract}

\tableofcontents
\newpage
"""

# ----------------------------------------------------------------------------
# Assemble FULL document.
# ----------------------------------------------------------------------------
parts = [FULL_PREAMBLE]

for ch in CHAPTERS:
    body = extract_body(ch)
    body = demote_headings(body)
    body = breakify_tables(body)
    if ch == 2:
        body = fix_ch2_al_table(body)
    parts.append('\n% ' + '=' * 68)
    parts.append(f'% ===== Chapter {ch} body (원본 graphite_ica_ch{ch}_rebuilt.tex, byte-verbatim; heading 1단계 demote) =====')
    parts.append('% ' + '=' * 68)
    parts.append(f'\\clearpage\n\\section{{{CHTITLE[ch]}}}\\label{{chap:ch{ch}}}\n')
    parts.append(body)
    parts.append('\n')

# integrated bibliography (same 33 keys as refs file)
parts.append('\n% ' + '=' * 68)
parts.append('% ===== 통합 참고문헌 (33 키 union; Ch1-first dedupe; refs 문건과 동일) =====')
parts.append('% ' + '=' * 68)
parts.append(r'\clearpage')
parts.append(r'\section{통합 참고문헌 (Chapter 1$\sim$5 union, 33 키)}\label{sec:full_bib}')
parts.append(r'아래 33 키는 Chapter 1$\sim$5 의 \texttt{\textbackslash bibitem} 합집합(중복 제거; Ch1 우선)이며, 별도 통합 references 문건(\texttt{graphite\_ica\_refs\_rebuilt.tex})의 bibliography 와 동일하다. 통합 Assumption Ledger(AL-1$\sim$69)는 그 문건에 수록.')
parts.append(THEBIB)

parts.append(r"""
% ====================================================================
\section*{통합 노트 (Ch1~5 병합 메타; 구 Ch6 해체)}
\addcontentsline{toc}{section}{통합 노트}
% ====================================================================
\begin{itemize}[leftmargin=1.6em]
\item \textbf{원본 5개 챕터 수정 0 (body byte-verbatim).} 각 챕터의 \texttt{\textbackslash maketitle}
  이후$\sim$\texttt{\textbackslash begin\{thebibliography\}} 직전 본문을 그대로 복사(요약$\cdot$축약 0).
  label 충돌 0, cross-chapter 평문 상호참조 현행 유지(수정 0).
\item \textbf{Ch6 해체.} 별도 Chapter 6 없음 — 구 Chapter 6(실데이터 피팅 워크플로)은 Ch1
  \emph{부록 B}(\texttt{sec:ch6\_*} 라벨)에 흡수되어 본 통합본에 Ch1 의 일부로 포함된다.
  본문의 ``구 Chapter 6''$\cdot$``부록 B'' 언급은 그 흡수 설명이다.
\item \textbf{heading 1단계 demote.} 챕터 = \texttt{\textbackslash section{Chapter N}}, 챕터 내부
  \texttt{\textbackslash section}$\to$\texttt{\textbackslash subsection},
  \texttt{\textbackslash subsection}$\to$\texttt{\textbackslash subsubsection}
  (article 유지, \texttt{\textbackslash part}/\texttt{\textbackslash chapter} 미사용).
\item \textbf{theorem 환경 caption 통일.} \texttt{verifybox}$\cdot$\texttt{linkbox} 는 union 1회
  정의이므로 대표 caption 으로 통일했다 — box 내부 \emph{물리 내용$\cdot$식은 변경 0}, heading label 문구만 통일.
\item \textbf{통합 bibliography.} 33 키 union(Ch1 우선 dedupe; refs 문건과 동일 서지$\cdot$DOI).
\end{itemize}

\end{document}
""")

full_text = '\n'.join(parts)
with io.open(OUT_FULL, 'w', encoding='utf-8', newline='\n') as f:
    f.write(full_text)

# ----------------------------------------------------------------------------
# REFS document — 33-key bib only, standalone (existing refs preamble/title pattern).
# ----------------------------------------------------------------------------
REFS_DOC = r"""% ====================================================================
% graphite_ica_refs_rebuilt.tex — 통합 references 문건 (RB 재생성, standalone)
%   흑연 음극 ICA(dQ/dV) 이론서 RB-series Chapter 1~5 의 통합 참고문헌(33 키 union).
%   ★ Ch6 해체(2026-06-01): 구 Ch6 는 Ch1 부록 B 로 흡수 — 별도 챕터 없음.
%     5개 챕터의 \bibitem 을 union+dedupe(동일 키 1회, Ch1 우선) 하였다.
%     bibitem 텍스트는 챕터 원문 그대로(서지·DOI 변경 0; \brk 줄바꿈 포함).
%     본 문건의 33 키 bibliography 는 통합본(graphite_ica_full_rebuilt.tex)의
%     통합 참고문헌과 동일하다. standalone 컴파일 가능(article, kotex, amsmath,
%     \AL/\brk 매크로).
% Date: 2026-06-02  Author: Project_Anode_Fit (Claude 측, RB-series 통합 재생성)
% ====================================================================
\documentclass[11pt,a4paper]{article}
\usepackage[margin=20mm]{geometry}
\usepackage{kotex}
\usepackage{amsmath,amssymb,mathtools,bm}
\usepackage{booktabs,longtable,array}
\usepackage{enumitem}
\usepackage{amsthm}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{setspace}
\setstretch{1.13}
\setlength{\parskip}{0.45em}\setlength{\parindent}{0pt}\setlength{\headheight}{14pt}
\setlength{\emergencystretch}{3em}\tolerance=1200\hbadness=4000
\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue, citecolor=blue,
  pdftitle={흑연 음극 ICA tail — 통합 References (33 키 union, RB)}}
\pagestyle{fancy}\fancyhf{}
\lhead{흑연 음극 ICA tail — 통합 References (33 키 union, RB)}\rhead{\thepage/\pageref{LastPage}}
\renewcommand{\headrulewidth}{0.4pt}

""" + MACRO_UNION + r"""

\title{\textbf{리튬이온전지 흑연 음극 ICA($dQ/dV$) tail 이론 — 통합 References}\\[0.5em]
\large 통합 참고문헌 (Chapter 1$\sim$5 union $+$ dedupe, 검증 DOI; 33 키)\\[0.2em]
\normalsize 구 Ch6 는 Ch1 부록 B 로 흡수 — 5개 챕터 \texttt{\textbackslash bibitem} 합집합(Ch1 우선)\\
(통합본 \texttt{graphite\_ica\_full\_rebuilt.tex} 의 통합 참고문헌과 동일)}
\author{Project\_Anode\_Fit (RB 재구성본)}
\date{2026-06-02}

\begin{document}
\sloppy
\maketitle

\section*{문건 성격}
\addcontentsline{toc}{section}{문건 성격}
본 문건은 RB-series 이론서 Chapter 1$\sim$5 재구성본의 \textbf{통합 참고문헌}(33 키)을 모은 standalone
문건이다. 5개 챕터에 분산된 \texttt{\textbackslash bibitem} 을 union$+$dedupe(동일 키 1회, Ch1 우선)
하였으며, 어느 챕터에서도 인용 안 된 dead/orphan 키는 0 — 33 키 전부 본문 인용. bibitem 텍스트는 챕터
원문 그대로(서지$\cdot$DOI 변경 0; \texttt{\textbackslash brk} 줄바꿈 포함). 구 Chapter 6 은 해체되어
Ch1 부록 B 로 흡수되었으므로 별도 챕터 키 추가는 없다.

\tableofcontents
\newpage

\section{통합 참고문헌 (union $+$ dedupe, 33 키)}\label{sec:refs_bib}
""" + THEBIB + r"""

\end{document}
"""

with io.open(OUT_REFS, 'w', encoding='utf-8', newline='\n') as f:
    f.write(REFS_DOC)

print('wrote', OUT_FULL)
print('wrote', OUT_REFS)
print('bib keys (33):', len(BIB_KEYS))
print('full bytes:', len(full_text))
print('refs bytes:', len(REFS_DOC))
