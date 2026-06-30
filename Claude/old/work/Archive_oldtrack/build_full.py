# -*- coding: utf-8 -*-
"""Merge Ch1~6 _rebuilt.tex bodies into one standalone full document.
   - preamble union (packages, macros, theorem environments)
   - each chapter body integrated at \\section level (internal \\section -> \\subsection, etc.)
   - single integrated bibliography (33 keys, union+dedupe) appended at end
   - title page + table of contents
   No modification to chapter source files. Label conflicts = 0 (verified).
"""
import re, io

BASE = r'd:/Projects/Project_Anode_Fit/Claude/docs'
OUT = f'{BASE}/graphite_ica_full_rebuilt.tex'

# Concise chapter section titles (from each chapter's \lhead / subtitle)
CHTITLE = {
 1: r'Chapter 1 — 열역학 무대 + 극판 전위에 의한 배리어 낮춤 (relaxation-length spectrum)',
 2: r'Chapter 2 — 전지 가역 반응열 + 비가역 소산열 (Bernardi 에너지 balance)',
 3: r'Chapter 3 — 반응속도론: forward/backward kinetics $\cdot$ detailed balance $\cdot$ Butler--Volmer',
 4: r'Chapter 4 — entropy-production 기반 발열 일반화 ($\sum_j n_j^{\eff}I_j\eta_j$)',
 5: r'Chapter 5 — 충방전 branch + 히스테리시스 (충전 부호 유도 $\cdot$ $\Delta V_\obs\ne\Delta V_\hys$)',
 6: r'Chapter 6 — 피팅 실무: 식별성 $\cdot$ 순차 제약 $\cdot$ 반증 (수치는 보조 종속)',
}

def read(ch):
    return open(f'{BASE}/graphite_ica_ch{ch}_rebuilt.tex', encoding='utf-8').read()

def extract_body(ch):
    """Return chapter body: from intro \\section* (after \\maketitle) to just before \\begin{thebibliography}."""
    txt = read(ch)
    # body region: after \maketitle ... before \begin{thebibliography}
    m_start = re.search(r'\\maketitle', txt)
    m_bib = re.search(r'\\begin\{thebibliography\}', txt)
    body = txt[m_start.end():m_bib.start()]
    # remove a leading \sloppy that may appear between document begin and maketitle handled separately
    # drop the embedded \tableofcontents and the immediately following \newpage
    body = re.sub(r'\\tableofcontents\s*\n', '', body)
    # drop a \newpage that directly followed the toc (only the first standalone \newpage right after intro block)
    # Specifically remove the \newpage that preceded the first numbered section; safest: remove \newpage occurring
    # right before the first '% ===' main-section banner after the grounding/intro. We remove ALL standalone
    # '\newpage' lines that are by themselves (chapters only use one, the post-TOC one).
    body = re.sub(r'^\\newpage\s*$\n', '', body, flags=re.MULTILINE)
    # drop any \sloppy lines inside the body (we set \sloppy once globally)
    body = re.sub(r'^\\sloppy\s*$\n', '', body, flags=re.MULTILINE)
    return body.strip('\n')

def demote_headings(body):
    """Demote heading levels by one so chapter internals nest under the chapter \\section.
       Order matters: subsection -> subsubsection FIRST, then section -> subsection."""
    # subsection*{ -> subsubsection*{
    body = body.replace(r'\subsection*{', r'\subsubsection*{')
    body = body.replace(r'\subsection{', r'\subsubsection{')
    # section*{ -> subsection*{  ; section{ -> subsection{
    body = body.replace(r'\section*{', r'\subsection*{')
    body = body.replace(r'\section{', r'\subsection{')
    # addcontentsline toc section -> subsection (intro \section* uses this)
    body = body.replace(r'\addcontentsline{toc}{section}', r'\addcontentsline{toc}{subsection}')
    return body

def breakify_tables(body):
    """Insert zero-width \\brk break opportunities into AL/self-check table rows that
       lack them (e.g. Ch2 AL table authored before the \\brk convention), so long
       DOI/ISBN/cite runs can wrap inside narrow longtable columns.
       Applied ONLY to lines that are table rows (contain ' & ' and end with '\\\\').
       Idempotent: a '/' or ',' already followed by '\\brk' is left as-is.
       This is a typographic break in the generated full file only; chapter sources
       are not modified, and no token text is altered (zero-width discretionary)."""
    out_lines = []
    for line in body.split('\n'):
        s = line.rstrip('\n')
        # heuristics: a longtable data row has ' & ' and ends with '\\' (LaTeX row end)
        is_row = (' & ' in s) and s.rstrip().endswith(r'\\')
        if is_row:
            # DOI/ISBN '/' break: '10.1149/1.x' -> '10.1149/\brk 1.x' (skip if already \brk after)
            s = re.sub(r'(10\.\d{3,5})/(?!\\brk)', r'\1/\\brk ', s)
            s = re.sub(r'(978-0)-(?!\\brk)', r'\1-\\brk ', s)
            s = re.sub(r'(471)-(?!\\brk)', r'\1-\\brk ', s)
            # cite-key list separators inside parens: ', ' / '; ' between keys/DOIs
            # only between word-chars (avoid touching prose); add break after comma/semicolon
            s = re.sub(r',\x20(?=[A-Za-z0-9])(?!\\brk)', r',\\brk ', s)
            s = re.sub(r';\x20(?=[0-9A-Za-z])(?!\\brk)', r';\\brk ', s)
            # long single cite keys: insert a mid-word \brk so they can wrap in a narrow column
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
                # only break when the key is not already broken
                s = s.replace(key, brk)
        out_lines.append(s)
    return '\n'.join(out_lines)

# ---- assemble preamble ----
PREAMBLE = r"""% ====================================================================
% graphite_ica_full_rebuilt.tex — Ch1~6 통합 full 문건 (RB Phase 7.2, standalone)
%   흑연 음극 ICA(dQ/dV) 이론서 RB-series Chapter 1~6 재구성본을 한 문서로 병합.
%     · preamble union(documentclass·kotex·amsmath·\AL/\brk 매크로·theorem 환경
%       groundingbox/boundbox/flagbox/keybox/linkbox/verifybox/practicebox/loopbox
%       — 6개 챕터 preamble 합집합, 중복 정의 1회).
%     · 각 챕터 \documentclass/\begin{document}/\end{document}/개별 \tableofcontents 제거.
%     · 챕터 = \section{Chapter N ...}, 챕터 내부 \section→\subsection, \subsection→\subsubsection
%       (article 유지, \part/\chapter 미사용 — \section 레벨 정합).
%     · 통합 bibliography(refs 문건과 동일 33 키 union) 1회 포함.
%     · title page + table of contents.
%   ★ 원본 6개 챕터 _rebuilt.tex 는 수정 0 — label 충돌 0(검증), cross-chapter
%     \eqref 0(전부 동일 챕터 내 resolve), 따라서 prefix 부여 불필요.
%   ★ theorem 환경 caption 통일 주의: verifybox/linkbox 는 챕터별 caption 문구가
%     달랐으나 union 1회 정의로 대표 caption 을 쓴다(물리 내용·식 변경 0, heading
%     label 만 통일). 상세는 본 문서 말미 통합 노트 참조.
% Date: 2026-06-01  Author: Project_Anode_Fit (Claude 측, RB-series Phase 7.2)
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
  pdftitle={흑연 음극 ICA tail — Chapter 1~6 통합본 (RB 재구성본)}}
\pagestyle{fancy}\fancyhf{}
\lhead{흑연 음극 ICA(dQ/dV) tail 이론 — Ch.1~6 통합본 (RB)}\rhead{\thepage/\pageref{LastPage}}
\renewcommand{\headrulewidth}{0.4pt}

% --- theorem 환경 union (6개 챕터 preamble 합집합, 중복 정의 1회) ---
% (verifybox/linkbox 는 챕터별 caption 문구가 달랐으나, union 정의이므로 대표
%  caption 으로 통일 — 물리 내용·식 변경 0, box heading label 만 통일.)
\newtheorem*{groundingbox}{Grounding}
\newtheorem*{boundbox}{유효범위(Validity bound)}
\newtheorem*{flagbox}{FLAGGED (미확정)}
\newtheorem*{keybox}{Keystone}
\newtheorem*{linkbox}{전달식 (앞 장에서 상속)}
\newtheorem*{verifybox}{정합/유도 검증}
\newtheorem*{practicebox}{실무 팁 (본문 물리식 아님)}
\newtheorem*{loopbox}{도입 관찰로의 폐합}

% --- 매크로 union (Ch1~6 preamble 의 \newcommand 합집합, 중복 1회) ---
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
\newcommand{\brk}{\discretionary{}{}{}}% 표/참고문헌 긴 DOI·ISBN 줄바꿈 허용(zero-width)

\title{\textbf{리튬이온전지 흑연 음극 ICA($dQ/dV$) tail 이론 — Chapter 1$\sim$6 통합본}\\[0.5em]
\large 열역학 무대 $\to$ 동역학 주역 $\to$ 발열 $\to$ 반응속도론 $\to$ entropy production
$\to$ 히스테리시스 $\to$ 피팅 실무\\[0.3em]
\normalsize 하나의 관찰(저온$\cdot$고율 ICA 꼬리 겹침)에서 출발하는 단일 인과 사슬의 6-Chapter 전개\\
(RB 재구성본 통합 — Phase 7.2)}
\author{Project\_Anode\_Fit (RB 재구성본)}
\date{2026-06-01}

\begin{document}
\sloppy
\maketitle

\begin{abstract}
\noindent 본 문서는 흑연 음극 ICA($dQ/dV$) tail 이론 RB-series 재구성본 Chapter 1$\sim$6 을 한 문서로
통합한 것이다. \textbf{Chapter 1} 은 하나의 관찰(``저온$\cdot$고율에서 ICA peak 꼬리가 길어져 다음 peak 와
겹친다'')에서 출발해 열역학이 무대($V_n$, 평형 target $\xi_{\eq}$)를 깔고 동역학(진행률 완화 $+$
relaxation-length spectrum)이 꼬리의 주역임을 보이고 피팅 가능한 닫힌 논리식을 세운다. \textbf{Chapter 2}
는 그 위에서 전지 가역 반응열(평형 전위 온도계수 $=$ reaction entropy)과 비가역 소산열(과전압 flux$\times$force)을
Bernardi 에너지 balance 로 잇는다. \textbf{Chapter 3} 은 mobility $k_j$ 를 미시 forward/backward rate
$r_j^\pm$(Level B)로 확대하고 detailed balance 로 $n_j^{\eff}=RT/(Fw_j)$ 를 고정한다. \textbf{Chapter 4} 는
transition-level entropy production 이 거시 비가역 발열 일반형 $\sum_j n_j^{\eff}I_j\eta_j\ge0$ 으로 정확히
환원됨을 보인다. \textbf{Chapter 5} 는 충전 branch 부호 $s_{\phi,j}^b=-1$ 을 유도하고 히스테리시스를
target 의 이력 의존(metastable branch)으로 설명한다. \textbf{Chapter 6} 은 이 유도식들을 ICA/DVA 데이터에
순차 제약(OCV$\to$GITT$\to$Arrhenius$\to$C-rate)으로 피팅하는 방법론과 반증(forward-only) 시험으로 닫는다.
통합 참고문헌(33 키)과 통합 Assumption Ledger(AL-1$\sim$69)는 별도 문건
\texttt{graphite\_ica\_refs\_rebuilt.tex} 에 정리되어 있으며, 본 통합본에도 동일 33 키 bibliography 가
1회 포함된다.
\end{abstract}

\tableofcontents
\newpage
"""

parts = [PREAMBLE]

def fix_ch2_al_table(body: str) -> str:
    """Ch2 AL/self-check longtables use justified p{} (no raggedright) with a narrow
       tier column, causing 'GROUNDED' overfulls. Convert those two tables to
       footnotesize + raggedright with a wider tier column. Full-file-only typographic
       fix (Ch2 source untouched); cell text/content unchanged."""
    # AL table spec
    body = body.replace(
        r'\begin{longtable}{p{0.06\textwidth} p{0.40\textwidth} p{0.13\textwidth} p{0.16\textwidth} p{0.16\textwidth}}',
        r'\begin{longtable}{>{\raggedright\arraybackslash}p{0.05\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.355\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.155\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.195\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.13\textwidth}}')
    # self-check table (74/16) -> raggedright
    body = body.replace(
        r'\begin{longtable}{p{0.74\textwidth} p{0.16\textwidth}}',
        r'\begin{longtable}{>{\raggedright\arraybackslash}p{0.74\textwidth} '
        r'>{\raggedright\arraybackslash}p{0.16\textwidth}}')
    # notation/aux tables -> raggedright (absorbs minor math overfulls)
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
    # the AL table opens with {\small; bump to {\footnotesize for a touch more room.
    # (Only the AL-table small group — replace the specific occurrence preceding the AL longtable.)
    body = body.replace(
        'FLAGGED.\n{\\small\n\\begin{longtable}{>{\\raggedright',
        'FLAGGED.\n{\\footnotesize\n\\setlength{\\tabcolsep}{3pt}\n\\begin{longtable}{>{\\raggedright')
    return body

def wrap_wide_equations(body: str, ch: int) -> str:
    """Wrap a few inherited single-line wide display equations into break-friendly
       multi-line forms (content/terms identical; full-file-only typographic wrap).
       Targets only equations that overflow by a large margin in the merged doc."""
    if ch == 6:
        # eq:ch6_gitt_decomp — 5-term text sum, 138pt overfull. Wrap with \\.
        old = (r'\begin{equation}' '\n'
               r'\text{GITT relaxation}=\underbrace{\text{solid diffusion}}_{}+\underbrace{\text{electrolyte relaxation}}_{}+' '\n'
               r'\underbrace{\text{phase/staging relaxation}}_{\text{Ch1 }k_j}+\underbrace{\text{OCV curvature}}_{}+\underbrace{\text{measurement filtering}}_{}.' '\n'
               r'\label{eq:ch6_gitt_decomp}' '\n'
               r'\end{equation}')
        new = (r'\begin{multline}' '\n'
               r'\text{GITT relaxation}=\underbrace{\text{solid diffusion}}_{}+\underbrace{\text{electrolyte relaxation}}_{}\\' '\n'
               r'+\underbrace{\text{phase/staging relaxation}}_{\text{Ch1 }k_j}+\underbrace{\text{OCV curvature}}_{}+\underbrace{\text{measurement filtering}}_{}.' '\n'
               r'\label{eq:ch6_gitt_decomp}' '\n'
               r'\end{multline}')
        body = body.replace(old, new)
    return body

for ch in range(1, 7):
    body = extract_body(ch)
    body = demote_headings(body)
    body = breakify_tables(body)
    if ch == 2:
        body = fix_ch2_al_table(body)
    body = wrap_wide_equations(body, ch)
    parts.append('\n% ' + '='*68)
    parts.append(f'% ===== Chapter {ch} body (원본 graphite_ica_ch{ch}_rebuilt.tex, 수정 0; heading 1단계 demote) =====')
    parts.append('% ' + '='*68)
    parts.append(f'\\clearpage\n\\section{{{CHTITLE[ch]}}}\\label{{chap:ch{ch}}}\n')
    parts.append(body)
    parts.append('\n')

# ---- integrated bibliography (same 33 keys as refs file) ----
BIB = open(f'{BASE}/graphite_ica_refs_rebuilt.tex', encoding='utf-8').read()
mb = re.search(r'\\begin\{thebibliography\}.*?\\end\{thebibliography\}', BIB, flags=re.S)
bib_block = mb.group(0)
# strip the per-entry "(인용 장: ...)" emph notes for the full-doc bibliography (keep clean refs);
# they are informational only. Remove ' \emph{(인용 장:...)}'
bib_block = re.sub(r'\s*\\emph\{\(인용 장:[^}]*\)\}', '', bib_block)

parts.append('\n% ' + '='*68)
parts.append('% ===== 통합 참고문헌 (33 키 union+dedupe; refs 문건과 동일) =====')
parts.append('% ' + '='*68)
parts.append(r'\clearpage')
parts.append(r'\section{통합 참고문헌 (Chapter 1$\sim$6 union, 33 키)}\label{sec:full_bib}')
parts.append(r'아래 33 키는 Chapter 1$\sim$6 의 \texttt{\textbackslash bibitem} 합집합(중복 제거)이며, 별도 통합 references 문건(\texttt{graphite\_ica\_refs\_rebuilt.tex})의 bibliography 와 동일하다. 통합 Assumption Ledger(AL-1$\sim$69)는 그 문건에 수록.')
parts.append(bib_block)

parts.append(r"""
% ====================================================================
\section*{통합 노트 (Phase 7.2 병합 메타)}
\addcontentsline{toc}{section}{통합 노트}
% ====================================================================
\begin{itemize}[leftmargin=1.6em]
\item \textbf{원본 6개 챕터 수정 0.} label 충돌 0(285 라벨 전건 무충돌; Ch1 비-prefix 라벨 35종도 Ch2$\sim$6 의
  \texttt{chN} prefix 와 미충돌), cross-chapter \texttt{\textbackslash eqref} 0(모든 \texttt{\textbackslash eqref}
  가 동일 챕터 내 resolve). 따라서 label prefix 부여 \emph{불필요} — 본 통합은 챕터 본문을 그대로 편입했다.
\item \textbf{heading 1단계 demote.} 챕터 = \texttt{\textbackslash section{Chapter N}}, 챕터 내부
  \texttt{\textbackslash section}$\to$\texttt{\textbackslash subsection},
  \texttt{\textbackslash subsection}$\to$\texttt{\textbackslash subsubsection}
  (article 유지, \texttt{\textbackslash part}/\texttt{\textbackslash chapter} 미사용).
\item \textbf{theorem 환경 caption 통일.} \texttt{verifybox}(챕터별 ``정합 검증''/``유도 검증'' 등)$\cdot$
  \texttt{linkbox}(``Ch1 전달식''/``Ch1--3 전달식'' 등)는 union 1회 정의이므로 대표 caption(\,``정합/유도 검증''$\cdot$
  ``전달식 (앞 장에서 상속)''\,)으로 통일했다 — box 내부 \emph{물리 내용$\cdot$식은 변경 0}, heading label 문구만
  통일.
\item \textbf{cross-chapter 상호참조.} ``(L3)''$\cdot$``Ch1 eq:logistic'' 등 본문 plain-text 상호참조는
  현행 유지(\texttt{\textbackslash eqref} 강제 전환 0 — 물리 변경 0).
\item \textbf{통합 bibliography.} 33 키 union(refs 문건과 동일 서지$\cdot$DOI; 인용 장 주석은 통합본에선 생략).
\end{itemize}

\end{document}
""")

with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(parts))

print('wrote', OUT)
print('approx bytes:', len('\n'.join(parts)))
